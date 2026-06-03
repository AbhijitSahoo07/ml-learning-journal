# 🤖 AI-Powered ML Learning Journal

[![Daily ML Note Generator](https://github.com/workflows/daily_note.yml/badge.svg)](#)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Gemini](https://img.shields.io/badge/powered%20by-Gemini-orange.svg)](https://deepmind.google/technologies/gemini/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

An automated, serverless system that writes, formats, and publishes one high-quality Machine Learning learning note every single day. Using the **Gemini 2.5 Flash API** and **GitHub Actions**, this repository generates comprehensive educational content, mathematical breakdowns, working Python code examples, interview questions, and quizzes without requiring any active computer or local server.

---

## 📂 Repository Structure

```text
ml-learning-journal/
│
├── .github/
│   └── workflows/
│       └── daily_note.yml     # GitHub Actions workflow (runs daily & manually)
│
├── notes/                     # Published markdown notes (named: YYYY-MM-DD-slug.md)
│   └── .gitkeep               # Keeps the folder tracked in git
│
├── generate_note.py           # Core Python generation script (google-genai SDK)
├── requirements.txt           # Python environment dependencies
├── topics.txt                 # Curated list of 100+ machine learning topics
└── README.md                  # Project documentation & configuration guide
```

---

## 🌟 Key Features

- **🔋 Zero Maintenance:** Runs automatically at `00:00 UTC` daily via GitHub Actions.
- **💡 State-Aware Progression:** Inspects the `notes/` directory to track what topics have already been covered and automatically picks the next topic from `topics.txt`—preventing duplicates without database overhead.
- **📚 Rich Note Structure:** Every note is generated in a clean, beginner-friendly Markdown format featuring:
  - **Overview & Problem Solving:** Real-world context.
  - **Algorithm Breakdown:** Step-by-step logic.
  - **Mathematical Intuition:** Detailed LaTeX equations ($y = mx + c$).
  - **Python Examples:** Runnable code snippets using `scikit-learn`, `numpy`, and `pandas`.
  - **Interview Prep:** 10+ detailed interview Q&As per topic.
  - **Interactive Learning:** 5+ multiple-choice questions (MCQs) with explanations.
  - **Curated Reading:** 3+ handpicked resource recommendations.
- **🛡️ Fail-Safe Controls:** Handles API timeouts, rate limits, duplicate runs, and git conflicts gracefully.

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
Finds the next topic in `topics.txt` and previews it without calling the Gemini API or creating files:
```bash
python generate_note.py --dry-run
```

#### B. Generate Today's Note
Set your API key and run the script:
```bash
# On macOS/Linux:
export GEMINI_API_KEY="your_actual_gemini_api_key"
python generate_note.py

# On Windows (Command Prompt):
set GEMINI_API_KEY=your_actual_gemini_api_key
python generate_note.py

# On Windows (PowerShell):
$env:GEMINI_API_KEY="your_actual_gemini_api_key"
python generate_note.py
```

*Note: The script checks if a note has already been generated today. To override this and generate another note, use the `--force` flag:*
```bash
python generate_note.py --force
```

---

## ⚙️ GitHub Secrets Configuration (Automated Daily Runs)

To let GitHub Actions run the generation process automatically every day, you need to configure your Gemini API Key as a repository secret.

1. Go to your repository on GitHub.
2. Navigate to **Settings** > **Secrets and variables** > **Actions**.
3. Click on the **New repository secret** button.
4. Set the name to: `GEMINI_API_KEY`
5. Paste your API key into the **Secret** field.
6. Click **Add secret** to save.

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
