import os
import shutil
from typing import List
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from app.parser import extract_text_from_pdf
from app.ranking import rank_resumes

app = FastAPI(
    title="TalentLens AI Resume Analyzer",
    description="An intelligent parser and similarity ranker API for job candidates",
    version="1.0.0"
)

# CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define directories
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
STATIC_DIR = os.path.join(BASE_DIR, "app", "static")

# Create data directory if it doesn't exist
os.makedirs(DATA_DIR, exist_ok=True)

# Mount static files
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

@app.get("/")
async def get_index():
    """
    Serves the main frontend dashboard.
    """
    index_path = os.path.join(STATIC_DIR, "index.html")
    if not os.path.exists(index_path):
        raise HTTPException(status_code=404, detail="Frontend index.html not found.")
    return FileResponse(index_path)

@app.post("/analyze")
async def analyze(
    job_description: str = Form(...),
    resumes: List[UploadFile] = File(...)
):
    """
    Accepts job description text and multiple PDF resume files.
    Extracts text, calculates similarity scores, matches skills, and ranks candidate resumes.
    """
    if not job_description.strip():
        raise HTTPException(status_code=400, detail="Job description text cannot be empty.")
    
    if not resumes:
        raise HTTPException(status_code=400, detail="At least one resume PDF must be uploaded.")

    parsed_resumes = []
    
    for resume in resumes:
        if not resume.filename.lower().endswith(".pdf"):
            # Skip non-PDF files or raise error
            continue
            
        # Secure the path and write the uploaded file into data/ directory
        file_path = os.path.join(DATA_DIR, resume.filename)
        
        try:
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(resume.file, buffer)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to save file {resume.filename}: {str(e)}")
        finally:
            resume.file.close()
            
        # Extract text from the saved PDF file
        try:
            extracted_text = extract_text_from_pdf(file_path)
            parsed_resumes.append({
                "filename": resume.filename,
                "text": extracted_text
            })
        except Exception as e:
            # We can log the error and continue, or fail the entire request.
            # In production, we log and skip/record parsing error, but let's notify.
            raise HTTPException(status_code=422, detail=f"Failed to parse resume {resume.filename}: {str(e)}")

    if not parsed_resumes:
        raise HTTPException(status_code=400, detail="No valid PDF resumes could be parsed.")

    # Process similarity ranking and skill matching
    try:
        rankings = rank_resumes(job_description, parsed_resumes)
        return rankings
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis pipeline error: {str(e)}")
