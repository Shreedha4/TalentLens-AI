# TalentLens AI Resume Analyzer

Link : https://talentlens-ai-wx4t.onrender.com

An intelligent, modular, and production-ready AI Resume Analyzer built with FastAPI (Python) and a premium, dark-themed HTML5/JS/CSS frontend. It extracts text and technical/soft skills from PDF resumes, calculates similarity with a job description using a custom TF-IDF Cosine Similarity engine, and ranks candidates in a sleek visual dashboard.

## Features

1. **PDF Text Extraction**: Uses PyMuPDF (`fitz`) for fast, clean text extraction.
2. **Skill Extraction**: Matches extracted text against a curated list of 150+ technology, management, and soft skills using boundary-safe regular expressions (supporting complex symbols like `C++`, `C#`, `.NET`).
3. **TF-IDF Similarity Matcher**: Runs a custom, robust Term Frequency-Inverse Document Frequency and Cosine Similarity scoring engine in pure Python.
4. **Ranking System**: Ranks candidate profiles dynamically in descending order of similarity score.
5. **Interactive Dashboard UI**: Drag-and-drop file upload, circular score indicators, skill-match highlights, and statistics overview.

---

## Project Structure

```
ai_resume_analyzer/
├── data/                       # Directory where uploaded resumes are stored
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI API & Home Route Serving Static UI
│   ├── parser.py               # PDF parser using PyMuPDF (fitz)
│   ├── matcher.py              # Skill extractor & custom TF-IDF similarity matcher
│   ├── ranking.py              # Ranking aggregation pipeline
│   └── static/                 # Front-end Assets
│       ├── index.html          # Dashboard skeleton
│       ├── style.css           # Premium styling & animations
│       └── app.js              # Interactivity & API connection
├── requirements.txt            # Python dependencies
└── README.md                   # Setup and usage guide
```

---

## Quick Start

### 1. Prerequisites
Ensure you have **Python 3.8+** installed.

### 2. Set Up Virtual Environment & Dependencies
Create a virtual environment, activate it, and install dependencies:

```bash
# Clone or navigate to project directory
cd C:\Users\Shreedha\.gemini\antigravity\scratch\ai_resume_analyzer

# Create virtual environment
python -m venv venv

# Activate on Windows (PowerShell)
.\venv\Scripts\Activate.ps1
# OR Windows (cmd)
.\venv\Scripts\activate.bat
# OR macOS/Linux
source venv/bin/activate

# Install requirements
pip install -r requirements.txt
```

### 3. Run the Application
Start the Uvicorn server:

```bash
uvicorn app.main:app --reload
```

---

## Usage

### Web Interface
Once the server is running, open your web browser and go to:
[http://localhost:8000](http://localhost:8000)

1. Paste a job description into the **Job Details** text area.
2. Drag and drop PDF resumes into the **Resumes Upload** zone (or browse files).
3. Click **Analyze & Rank Resumes** to view candidate metrics, score rings, and matching skills.

### API Endpoint: `/analyze` [POST]

Allows programmatic submission of resumes and job descriptions.

#### Request Form Data:
* `job_description` (string): Text requirements for the position.
* `resumes` (files): List of PDF file uploads.

#### Sample Request using `curl`:
```bash
curl -X POST "http://localhost:8000/analyze" \
  -F "job_description=Python developer with FastAPI, SQL and Docker knowledge." \
  -F "resumes=@/path/to/resume1.pdf" \
  -F "resumes=@/path/to/resume2.pdf"
```

#### Sample Response:
```json
[
  {
    "filename": "john_doe_resume.pdf",
    "score": 64.3,
    "extracted_skills": ["Python", "FastAPI", "SQL", "Docker", "Git", "Agile"],
    "matching_skills": ["Python", "FastAPI", "SQL", "Docker"],
    "total_skills_count": 6,
    "matching_skills_count": 4
  },
  {
    "filename": "jane_smith_resume.pdf",
    "score": 38.1,
    "extracted_skills": ["Java", "Spring Boot", "SQL", "HTML"],
    "matching_skills": ["SQL"],
    "total_skills_count": 4,
    "matching_skills_count": 1
  }
]
```
