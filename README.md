# 🤖 AI-Powered ML Learning Journal

[![Daily ML Note Generator](https://github.com/workflows/daily_note.yml/badge.svg)](#)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Gemini](https://img.shields.io/badge/powered%20by-Gemini-orange.svg)](https://deepmind.google/technologies/gemini/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

An automated, serverless system that writes, formats, and publishes high-quality Machine Learning learning notes daily. Using the **Gemini 3.8 Flash API** and **GitHub Actions**, this repository generates a dynamic number of comprehensive educational notes each day (randomly picking between 1 and 10 notes daily), with mathematical breakdowns, working Python code examples, interview questions, and quizzes without requiring any active computer or local server.

---

## 📂 Repository Structure

```text
ml-learning-journal/
│
├── .github/
│   └── workflows/
│       └── daily_note.yml     # GitHub Actions workflow (runs daily & manually with dynamic note count)
│
├── notes/                     # Published markdown notes (named: YYYY-MM-DD-slug.md)
│   └── .gitkeep               # Keeps the folder tracked in git
│
├── generate_note.py           # Core Python generation script (google-genai SDK)
├── requirements.txt           # Python environment dependencies
├── topics.txt                 # Curated list of 1,260+ ML, OpenCV, YOLO, AWS, and NLP topics
└── README.md                  # Project documentation & configuration guide
```

---

## 🌟 Key Features

- **🔋 Zero Maintenance:** Runs automatically at `00:00 UTC` daily via GitHub Actions.
- **🎲 Dynamic Daily Generation:** Instead of a fixed count, each run randomly picks between 1 and 10 notes to generate and publish, giving a lively, realistic learning rhythm.
- **📚 Curated 1,260+ Topic Roadmap:** Comprehensive syllabus covering:
  - **Core Machine Learning & Mathematics:** Classical supervised, unsupervised, reinforcement learning, statistics, probability, and linear algebra.
  - **OpenCV & Computer Vision:** Image filtering, transformations, contours, feature detection (SIFT, ORB), optical flow, camera calibration, stereo vision, and DNN modules.
  - **YOLO & Modern Object Detection:** Architectures from YOLOv1 to YOLO11, YOLO-World, RT-DETR, loss functions (CIoU, DFL), NMS algorithms, multi-task heads (pose, segmentation, OBB), and TensorRT/ONNX deployment.
  - **AWS Machine Learning & Cloud AI:** Amazon SageMaker (Studio, Pipelines, Model Registry, Endpoints, Feature Store, JumpStart), Amazon Bedrock, Rekognition, Comprehend, Textract, Kendra, Lex, Transcribe, Polly, and AWS MLOps infrastructure.
  - **NLP, Transformers & Modern GenAI:** Tokenization (BPE, WordPiece), Attention mechanisms, BERT/T5/LLaMA/Mistral architectures, PEFT (LoRA, QLoRA), Alignment (RLHF, DPO, ORPO), RAG architectures, Vector DBs, vLLM, and Quantization.
- **💡 State-Aware Progression:** Inspects the `notes/` directory to track what topics have already been covered and automatically picks the next topic from `topics.txt`—preventing duplicates without database overhead.
- **📚 Crisp ~100-Word Note Structure:** Every note is generated as a high-yield, bite-sized study card (~100 words) featuring:
  - **Core Concept:** A punchy 1-2 sentence overview explaining what it is and why it matters.
  - **Key Mechanism & Intuition:** Concise explanation of how it works with essential LaTeX equations ($y = mx + c$).
  - **Key Practical Takeaway:** Actionable insight for production applications and technical interviews.
  - **Ultra-Fast & Quota-Safe:** Lightweight ~100-word footprint generates in <1 second and eliminates token rate-limit bottlenecks.
- **🛡️ Fail-Safe Controls:** Handles API timeouts, rate limits, duplicate runs, and git conflicts gracefully with automated retry loops and exponential backoff.

---

## 🛠️ Local Setup & Execution

You can run the script locally to generate notes, test prompts, or verify the topic-picking logic.

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/ml-learning-journal.git
cd ml-learning-journal
```

### 2. Set Up a Virtual Environment
```bash
# Create environment
python -m venv venv

# Activate environment
# On macOS / Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Running the Script

Make sure you get a free Gemini API Key from [Google AI Studio](https://aistudio.google.com/).

#### A. Run a Dry Run (Safe Test)
Finds the next topics in `topics.txt` and previews them without calling the Gemini API or creating files:
```bash
# Preview 1 note
python generate_note.py --dry-run

# Preview a batch with random count (1-10)
python generate_note.py --dry-run --random
```

#### B. Generate Notes
Set your API key and run the script:
```bash
# On macOS/Linux:
export GEMINI_API_KEY="your_actual_gemini_api_key"
# Single note:
python generate_note.py
# Random notes (between 1 and 10 notes):
python generate_note.py --random
# Specific number of notes:
python generate_note.py --count 5

# On Windows (PowerShell):
$env:GEMINI_API_KEY="your_actual_gemini_api_key"
python generate_note.py --random
```

*Flags Reference:*
- `--random`: Randomly selects a number of notes between 1 and 10 to generate.
- `--count N`: Generates $N$ notes sequentially with rate-limit pacing.
- `--force`: Bypasses the same-day generation check.
- `--push`: Automatically commits and pushes each generated note to GitHub after saving.
- `--delay SECONDS`: Delay between consecutive notes to stay within API rate limits (default: 10s).

---

## ⚙️ GitHub Secrets Configuration (Automated Daily Runs)

To let GitHub Actions run the generation process automatically every day, you need to configure your Gemini API Key as a repository secret.

### 🔑 Adding Multiple API Keys (Bypassing Rate & Quota Limits)
You can provide **multiple API keys** to distribute traffic, avoid rate limits (15 RPM), and bypass daily quota exhaustion. The generator automatically round-robins across all keys and instantly rotates if a key encounters a rate limit or quota warning.

Choose either setup:
* **Option A (Single Secret - Comma-Separated):**
  1. In **Settings** > **Secrets and variables** > **Actions**, edit or create `GEMINI_API_KEY`.
  2. Enter your keys separated by commas (or newlines):
     ```text
     AIzaSyKey1...,AIzaSyKey2...,AIzaSyKey3...
     ```
* **Option B (Separate Secrets):**
  Create individual secrets named:
  * `GEMINI_API_KEY_1`
  * `GEMINI_API_KEY_2`
  * `GEMINI_API_KEY_3` ... (up to 5 or more)

The script automatically detects all keys, balances the load per note, and rotates keys with minimal delay when limits are hit.

### Workflow Configuration Details
The workflow `.github/workflows/daily_note.yml` uses the `github-actions[bot]` user to securely commit and push changes back to the repository. It has the `contents: write` permission enabled to allow automated commits.

---

## 🔮 Future Enhancements (Built-in Placeholders)

The `generate_note.py` script has modular placeholder functions to easily extend the repository in future phases. Look inside `generate_note.py` for:

*   **`generate_daily_quiz_standalone()`**: Generates standalone quizzes or flashcards.
*   **`generate_daily_interview_questions_standalone()`**: Generates flashcard documents for exam preparation.
*   **`generate_daily_coding_exercise()`**: Generates a interactive Jupyter Notebook (`.ipynb`) with coding exercises.
*   **`generate_daily_ml_project()`**: Automatically constructs a mini-project folder with dataset guidelines.
*   **`generate_weekly_summary()`**: Aggregates the notes from the past 7 days into a consolidated weekly review guide.

---

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.
