#!/usr/bin/env python3
"""
AI-Powered ML Learning Journal - Daily Note Generator

This script automates the generation of daily machine learning notes. It reads topics
from a text file, identifies the next uncompleted topic, calls the Gemini API to
generate a detailed markdown note, and saves the file with a date prefix.

Requirements:
- Python 3.11+
- google-genai
"""

import argparse
import datetime
import logging
import os
import random
import re
import subprocess
import sys
import time
from pathlib import Path
from typing import Set, Tuple, Optional

# Setup logging with a professional format
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# Try importing the Google GenAI SDK
try:
    from google import genai
    from google.genai import errors
    from google.genai import types
except ImportError:
    logger.error(
        "Failed to import 'google-genai'. "
        "Please install it using 'pip install google-genai'."
    )
    sys.exit(1)


def slugify(text: str) -> str:
    """
    Convert a topic name to a URL-friendly, filesystem-safe lowercase slug.
    
    Args:
        text: The raw topic string.
        
    Returns:
        A cleaned slug string.
    """
    # Convert to lowercase and replace non-alphanumeric with spaces
    slug = text.lower()
    slug = re.sub(r"[^a-z0-9\s-]", "", slug)
    # Replace spaces and multiple hyphens with a single hyphen
    slug = re.sub(r"[\s-]+", "-", slug)
    return slug.strip("-")


def get_covered_topics(notes_dir: Path) -> Set[str]:
    """
    Scan the notes directory to extract slugs of topics already generated.
    
    Filenames are expected to follow the pattern: YYYY-MM-DD-topic-slug.md
    
    Args:
        notes_dir: Path to the directory containing notes.
        
    Returns:
        A set of already covered topic slugs.
    """
    covered = set()
    if not notes_dir.exists():
        return covered

    # Pattern to match YYYY-MM-DD-slug.md
    pattern = re.compile(r"^\d{4}-\d{2}-\d{2}-(.+)\.md$")
    for file_path in notes_dir.glob("*.md"):
        match = pattern.match(file_path.name)
        if match:
            covered.add(match.group(1))
            
    return covered


def get_next_topic(topics_file: Path, covered_slugs: Set[str]) -> Optional[Tuple[str, str]]:
    """
    Read topics.txt and return the first topic that is not yet covered.
    
    Args:
        topics_file: Path to topics.txt.
        covered_slugs: A set of already generated topic slugs.
        
    Returns:
        A tuple of (topic_name, topic_slug) if found, otherwise None.
    """
    if not topics_file.exists():
        logger.error(f"Topics file not found at: {topics_file}")
        raise FileNotFoundError(f"Topics file not found at: {topics_file}")

    with open(topics_file, "r", encoding="utf-8") as f:
        topics = [line.strip() for line in f if line.strip() and not line.strip().startswith("#")]

    for topic in topics:
        slug = slugify(topic)
        if slug not in covered_slugs:
            return topic, slug

    return None


def get_gemini_api_keys() -> list[str]:
    """
    Collect all Gemini API keys from environment variables.
    Supports GEMINI_API_KEY, GEMINI_API_KEYS, or GEMINI_API_KEY_1, GEMINI_API_KEY_2, etc.,
    with comma-separated, semicolon-separated, space-separated, or newline-separated values.
    
    Returns:
        A list of unique API key strings.
    """
    keys = []
    detected_vars = []
    for env_var, value in os.environ.items():
        if ("GEMINI" in env_var.upper() and "KEY" in env_var.upper()) or env_var.startswith("GEMINI_API"):
            if value:
                detected_vars.append(env_var)
                for k in re.split(r"[,;\s\|\n\r]+", value):
                    k = k.strip()
                    if k and k not in keys:
                        keys.append(k)
    logger.info(f"Loaded {len(keys)} Gemini API key(s) from environment: {detected_vars}")
    return keys


def generate_note_content(topic: str, model_name: str = "gemini-3.8-flash", key_offset: Optional[int] = None) -> str:
    """
    Call the Gemini API using the google-genai library to generate a note for the given topic.
    Supports seamless automatic key rotation, high-demand backoff, and rate-limit bypass.
    
    Args:
        topic: The topic name.
        model_name: The Gemini model identifier (default: gemini-3.8-flash).
        key_offset: Optional starting key index for round-robin rotation.
        
    Returns:
        The generated markdown content as a string.
        
    Raises:
        ValueError: If the API returns an empty response or no API keys found.
        Exception: For API errors or connection failures.
    """
    # Upgrade deprecated model identifiers
    if "2.5-flash" in model_name or "2.0-flash" in model_name or "1.5-flash" in model_name:
        logger.info(f"Mapping model identifier '{model_name}' to official 'gemini-3.8-flash'.")
        model_name = "gemini-3.8-flash"

    api_keys = get_gemini_api_keys()
    if not api_keys:
        logger.error("GEMINI_API_KEY environment variable is not set.")
        raise ValueError("GEMINI_API_KEY environment variable is not set.")

    if key_offset is None:
        key_offset = random.randint(0, len(api_keys) - 1)

    system_instruction = (
        "You are an expert AI and Machine Learning educator. Your goal is to write a concise, punchy, "
        "and beginner-friendly study note of approximately 100 words in raw Markdown format about the requested ML topic. "
        "Strictly limit the entire note to around 100 words. Do not wrap the final output in markdown code fences like ```markdown ... ```. Output raw markdown."
    )

    prompt = f"""Write a concise, high-yield study note of approximately 100 words on the topic: "{topic}".
The output must strictly be around 100 words in raw markdown format, following this exact structure:

# {topic}

### Core Concept
A clear, 1-2 sentence explanation of what {topic} is and why it matters in machine learning.

### Key Mechanism & Intuition
2-3 concise sentences detailing how it works, including any essential mathematical intuition or formula (use $...$ for inline LaTeX if applicable).

### Key Takeaway
A punchy 1-2 bullet point summary or practical insight for real-world usage and interviews.

Strictly adhere to the 100-word limit. Do not include excessive code or boilerplate."""

    fallback_prompt = f"""Write an ultra-concise 80-100 word study note on "{topic}":

# {topic}

### Core Concept
[1-2 clear sentences defining the topic]

### How It Works
[2 concise sentences on the mechanism or formula]

### Key Takeaway
- [Essential practical takeaway]

Keep the output strictly under 100 words in raw markdown."""

    max_retries = 8
    base_delay = 5.0  # seconds
    response = None

    for attempt in range(1, max_retries + 1):
        # Rotate API key based on the key_offset and attempt number
        key_index = (key_offset + attempt - 1) % len(api_keys)
        current_key = api_keys[key_index]
        masked_key = f"{current_key[:6]}...{current_key[-4:]}" if len(current_key) > 10 else "***"
        current_model = model_name
        
        # Switch to fallback prompt (retrieving less content) on attempt 3 or later to avoid token/rate limits
        current_prompt = prompt if attempt < 3 else fallback_prompt
        if attempt >= 3:
            logger.warning(
                f"Attempt {attempt}: Switching to simplified/concise fallback prompt (retrieving less content) "
                f"to resolve or avoid API quota/rate limit issues."
            )
        try:
            logger.info(
                f"Sending request to Gemini API for topic: '{topic}' "
                f"using model: '{current_model}' with key #{key_index + 1}/{len(api_keys)} ({masked_key}) "
                f"(Attempt {attempt}/{max_retries})..."
            )
            # Initialize Client dynamically with the rotated key using v1beta API version
            client = genai.Client(
                api_key=current_key,
                http_options=types.HttpOptions(api_version="v1beta")
            )
            response = client.models.generate_content(
                model=current_model,
                contents=current_prompt,
                config=types.GenerateContentConfig(
                    system_instruction=system_instruction,
                    temperature=0.2,  # Lower temperature for educational accuracy
                    max_output_tokens=350,  # Strictly limit output to ~100 words
                )
            )
            break  # Successfully generated content, exit the retry loop
        except errors.APIError as e:
            error_msg = str(e).lower()
            status_code = getattr(e, "code", None)

            # If the API complains about developer instruction or v1 vs v1beta, fallback to embedding system instruction in prompt
            if "developer instruction" in error_msg or "v1beta" in error_msg:
                logger.warning(
                    f"Attempt {attempt}: API reported developer instruction incompatibility. "
                    f"Retrying with instructions embedded directly into contents..."
                )
                try:
                    combined_prompt = f"{system_instruction}\n\n{current_prompt}"
                    response = client.models.generate_content(
                        model=current_model,
                        contents=combined_prompt,
                        config=types.GenerateContentConfig(
                            temperature=0.2,
                            max_output_tokens=350,
                        )
                    )
                    break
                except Exception as inner_e:
                    logger.warning(f"Embedded instruction fallback attempt failed: {inner_e}")

            # Check if error is due to high demand (HTTP 503), rate limits (HTTP 429), or transient server issues
            is_high_demand = status_code in [503, 502, 504] or "high demand" in error_msg or "unavailable" in error_msg
            is_rate_limit = status_code in [429] or "quota" in error_msg or "exhausted" in error_msg

            if (is_high_demand or is_rate_limit or status_code == 500) and attempt < max_retries:
                if len(api_keys) > 1:
                    delay = 2.0
                    logger.warning(
                        f"Attempt {attempt}: Hit status {status_code} ({'High Demand/503' if is_high_demand else 'Rate Limit'}). "
                        f"Rotating to next API key #{((key_index + 1) % len(api_keys)) + 1} in {delay:.1f}s..."
                    )
                else:
                    delay = base_delay * (1.5 ** (attempt - 1))
                    logger.warning(
                        f"Attempt {attempt}: Gemini API is experiencing high demand (status {status_code}). "
                        f"Backing off for {delay:.1f}s to allow demand spike to clear... Error: {e}"
                    )
                time.sleep(delay)
            else:
                logger.error(f"Gemini API error occurred on attempt {attempt}: {e}")
                raise e
        except Exception as e:
            # Catch transient network/client issues and retry
            if attempt < max_retries:
                delay = base_delay * (2 ** (attempt - 1))
                logger.warning(
                    f"Transient network or client error: {e}. Retrying in {delay:.1f} seconds..."
                )
                time.sleep(delay)
            else:
                logger.error(f"Unexpected error occurred on attempt {attempt}: {e}")
                raise e

    if not response or not response.text:
        logger.error("Received empty response from Gemini API.")
        raise ValueError("Received empty response from Gemini API.")

    # Clean the response in case the model ignored instructions and wrapped in code blocks
    content = response.text.strip()
    if content.startswith("```markdown"):
        content = content[11:].strip()
    if content.startswith("```html"):
        content = content[7:].strip()
    if content.startswith("```"):
        content = content[3:].strip()
    if content.endswith("```"):
        content = content[:-3].strip()

    return content


def save_note(notes_dir: Path, topic_slug: str, content: str, date_str: Optional[str] = None) -> Path:
    """
    Save the generated content into a markdown file in the notes directory.
    
    Args:
        notes_dir: Path to save the note.
        topic_slug: Slug of the topic.
        content: Markdown content.
        date_str: Optional date string in YYYY-MM-DD format (defaults to today).
        
    Returns:
        The Path to the saved file.
    """
    notes_dir.mkdir(parents=True, exist_ok=True)
    
    if not date_str:
        date_str = datetime.date.today().strftime("%Y-%m-%d")
        
    filename = f"{date_str}-{topic_slug}.md"
    file_path = notes_dir / filename
    
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
        
    logger.info(f"Successfully generated and saved note: {file_path}")
    return file_path


# =====================================================================
# Placeholders for Future Enhancements (as requested in specifications)
# =====================================================================

def generate_daily_quiz_standalone(topic: str) -> None:
    """
    Placeholder: Generates a dedicated daily quiz file or interactive quiz for the topic.
    To be implemented in future phase.
    """
    logger.info(f"[Future Enhancement] Generating standalone quiz for: {topic} (Not implemented)")
    pass


def generate_daily_interview_questions_standalone(topic: str) -> None:
    """
    Placeholder: Generates a standalone PDF/Markdown flashcard set of interview questions.
    To be implemented in future phase.
    """
    logger.info(f"[Future Enhancement] Generating interview flashcards for: {topic} (Not implemented)")
    pass


def generate_daily_coding_exercise(topic: str) -> None:
    """
    Placeholder: Generates a Jupyter notebook (.ipynb) containing a guided coding exercise for the topic.
    To be implemented in future phase.
    """
    logger.info(f"[Future Enhancement] Generating Jupyter notebook coding exercise for: {topic} (Not implemented)")
    pass


def generate_daily_ml_project(topic: str) -> None:
    """
    Placeholder: Generates a small end-to-end project directory for the topic.
    To be implemented in future phase.
    """
    logger.info(f"[Future Enhancement] Generating end-to-end ML project folder for: {topic} (Not implemented)")
    pass


def generate_weekly_summary(week_number: int) -> None:
    """
    Placeholder: Aggregates the last 7 notes and generates a weekly summary, review guide, and aggregate quiz.
    To be implemented in future phase.
    """
    logger.info(f"[Future Enhancement] Generating weekly summary for week {week_number} (Not implemented)")
    pass


def git_commit_and_push(file_path: Path, part: int, total: int, topic_name: str) -> bool:
    """
    Commit and push the generated note to git remote.
    
    Args:
        file_path: Path to the generated note.
        part: Index of this note in the batch.
        total: Total notes in this batch.
        topic_name: Name of the topic.
        
    Returns:
        True if commit and push succeeded, False otherwise.
    """
    try:
        # Stage note
        subprocess.run(["git", "add", str(file_path)], check=True, capture_output=True, text=True)
        
        # Check if changes exist
        diff = subprocess.run(["git", "diff", "--cached", "--quiet"], capture_output=True)
        if diff.returncode == 0:
            logger.info("No staged changes to commit.")
            return False
            
        commit_msg = f"docs: Auto-generate daily learning note (Part {part} of {total} - {topic_name})"
        subprocess.run(["git", "commit", "-m", commit_msg], check=True, capture_output=True, text=True)
        logger.info(f"Committed: {commit_msg}")
        
        # Determine branch
        branch = "main"
        branch_check = subprocess.run(["git", "show-ref", "--quiet", "refs/heads/master"], capture_output=True)
        if branch_check.returncode == 0:
            branch = "master"
            
        # Pull with rebase or fallback merge
        pull_rebase = subprocess.run(["git", "pull", "--rebase", "origin", branch], capture_output=True, text=True)
        if pull_rebase.returncode != 0:
            subprocess.run(["git", "rebase", "--abort"], capture_output=True)
            subprocess.run(["git", "pull", "--no-rebase", "-X", "ours", "origin", branch], capture_output=True)
            
        push_res = subprocess.run(["git", "push", "origin", "HEAD"], capture_output=True, text=True)
        if push_res.returncode == 0:
            logger.info(f"Successfully pushed note to origin: {file_path.name}")
            return True
        else:
            logger.warning(f"Git push returned non-zero exit code: {push_res.stderr.strip()}")
            return False
    except Exception as e:
        logger.warning(f"Failed to auto-commit/push to git: {e}")
        return False


# =====================================================================
# Main Flow
# =====================================================================

def main() -> None:
    parser = argparse.ArgumentParser(description="Generate daily ML learning notes using Gemini API.")
    parser.add_argument(
        "--model",
        type=str,
        default=os.environ.get("GEMINI_MODEL", "gemini-3.8-flash"),
        help="Gemini model to use (default: gemini-3.8-flash)"
    )
    parser.add_argument(
        "--notes-dir",
        type=str,
        default="notes",
        help="Directory to save generated notes (default: notes)"
    )
    parser.add_argument(
        "--topics-file",
        type=str,
        default="topics.txt",
        help="File containing list of topics (default: topics.txt)"
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Generate notes even if notes were already generated today."
    )
    parser.add_argument(
        "--count",
        type=int,
        default=1,
        help="Number of notes to generate in this run (default: 1)"
    )
    parser.add_argument(
        "--random",
        action="store_true",
        help="Randomly pick the number of notes to generate between --min-random and --max-random (default: 1 to 10)"
    )
    parser.add_argument(
        "--min-random",
        type=int,
        default=1,
        help="Minimum number of notes when using --random (default: 1)"
    )
    parser.add_argument(
        "--max-random",
        type=int,
        default=10,
        help="Maximum number of notes when using --random (default: 10)"
    )
    parser.add_argument(
        "--max-per-day",
        type=int,
        default=10,
        help="Maximum number of notes to generate per day (default: 10)"
    )
    parser.add_argument(
        "--delay",
        type=float,
        default=10.0,
        help="Delay in seconds between consecutive note generations (default: 10.0)"
    )
    parser.add_argument(
        "--push",
        action="store_true",
        help="Automatically git commit and push each generated note."
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Find upcoming topics and print them, but do not call API or write files."
    )
    
    args = parser.parse_args()
    
    base_dir = Path(__file__).parent.resolve()
    notes_path = base_dir / args.notes_dir
    topics_path = base_dir / args.topics_file

    logger.info("Starting Daily Note Generator...")
    
    # Determine target note count
    if args.random:
        total_notes = random.randint(args.min_random, args.max_random)
        logger.info(f"Random mode active: selected {total_notes} note(s) to generate (range: {args.min_random}-{args.max_random}).")
    else:
        total_notes = max(1, args.count)
        logger.info(f"Target note count: {total_notes}")

    today_str = datetime.date.today().strftime("%Y-%m-%d")
    
    # Scan covered topics
    try:
        covered_slugs = get_covered_topics(notes_path)
        logger.info(f"Found {len(covered_slugs)} already covered topics in notes directory.")
    except Exception as e:
        logger.error(f"Error scanning notes directory: {e}")
        sys.exit(1)

    generated_count = 0

    for i in range(1, total_notes + 1):
        logger.info(f"=== Note {i} of {total_notes} ===")

        # 1. Check daily limit
        if not args.force and not args.dry_run:
            today_notes = list(notes_path.glob(f"{today_str}-*.md"))
            if len(today_notes) >= args.max_per_day:
                logger.info(f"Daily limit reached ({len(today_notes)}/{args.max_per_day} notes today). Halting further generation.")
                break

        # 2. Determine next topic
        try:
            next_topic_info = get_next_topic(topics_path, covered_slugs)
        except FileNotFoundError:
            sys.exit(1)
        except Exception as e:
            logger.error(f"Error reading topics file: {e}")
            sys.exit(1)

        if not next_topic_info:
            logger.warning("All topics in topics.txt have already been covered!")
            break

        topic_name, topic_slug = next_topic_info
        logger.info(f"Next topic identified: '{topic_name}' (Slug: '{topic_slug}')")

        if args.dry_run:
            logger.info(f"[Dry Run] Would generate note for: '{topic_name}'")
            covered_slugs.add(topic_slug)
            generated_count += 1
            continue

        # 3. Generate note content from Gemini API (rotating starting key index)
        try:
            content = generate_note_content(topic_name, model_name=args.model, key_offset=i - 1)
        except Exception as e:
            logger.error(f"Failed to generate content for '{topic_name}': {e}")
            break

        # 4. Save the note
        try:
            saved_file = save_note(notes_path, topic_slug, content, today_str)
            covered_slugs.add(topic_slug)
            generated_count += 1

            # Write to GITHUB_OUTPUT environment file if available
            github_output = os.environ.get("GITHUB_OUTPUT")
            if github_output:
                try:
                    with open(github_output, "a", encoding="utf-8") as f:
                        f.write(f"note_file={saved_file.relative_to(base_dir)}\n")
                        f.write(f"topic_name={topic_name}\n")
                    logger.info("Wrote outputs to GITHUB_OUTPUT.")
                except Exception as e:
                    logger.error(f"Failed to write to GITHUB_OUTPUT: {e}")
        except Exception as e:
            logger.error(f"Failed to save note for '{topic_name}': {e}")
            break

        # 5. Git commit and push if requested
        if args.push:
            git_commit_and_push(saved_file, i, total_notes, topic_name)

        # 6. Trigger placeholder functions
        generate_daily_quiz_standalone(topic_name)
        generate_daily_interview_questions_standalone(topic_name)
        generate_daily_coding_exercise(topic_name)
        generate_daily_ml_project(topic_name)

        if len(covered_slugs) >= 7 and len(covered_slugs) % 7 == 0:
            week_num = len(covered_slugs) // 7
            generate_weekly_summary(week_num)

        # 7. Pause between consecutive calls to avoid rate limits
        if i < total_notes and not args.dry_run:
            logger.info(f"Waiting {args.delay} seconds before generating next note...")
            time.sleep(args.delay)

    logger.info(f"Process completed. Successfully generated {generated_count} of {total_notes} note(s).")


if __name__ == "__main__":
    main()
