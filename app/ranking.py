from typing import List, Dict, Any
from app.matcher import TFIDFMatcher, extract_skills

def rank_resumes(job_description: str, resumes_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Ranks a list of resumes against a job description.
    
    Args:
        job_description (str): Text of the job description.
        resumes_data (List[Dict[str, Any]]): List of dicts, each with 'filename' and 'text'.
        
    Returns:
        List[Dict[str, Any]]: Ranked list of resume results, each with similarity score,
                              matching skills, and extracted skills.
    """
    if not resumes_data:
        return []
        
    # Extract skills from job description to cross-reference
    jd_skills = set(extract_skills(job_description))
    
    # Form corpus for TF-IDF training: [Job Description, Resume 1 Text, Resume 2 Text, ...]
    corpus = [job_description] + [resume['text'] for resume in resumes_data]
    
    # Initialize TF-IDF Matcher
    matcher = TFIDFMatcher(corpus)
    
    # Vectorize Job Description
    jd_vector = matcher.compute_tfidf(job_description)
    
    ranked_candidates = []
    
    # Score each resume
    for resume in resumes_data:
        resume_text = resume['text']
        filename = resume['filename']
        
        # Vectorize resume and calculate cosine similarity
        resume_vector = matcher.compute_tfidf(resume_text)
        similarity = matcher.cosine_similarity(jd_vector, resume_vector)
        
        # Round similarity score to percentage (0 - 100%)
        score = round(similarity * 100, 1)
        
        # Extract skills from resume
        resume_skills = extract_skills(resume_text)
        
        # Find matching skills between resume and job description
        matching_skills = [skill for skill in resume_skills if skill in jd_skills]
        
        ranked_candidates.append({
            "filename": filename,
            "score": score,
            "extracted_skills": resume_skills,
            "matching_skills": matching_skills,
            "total_skills_count": len(resume_skills),
            "matching_skills_count": len(matching_skills)
        })
        
    # Sort candidates by score descending
    ranked_candidates.sort(key=lambda x: x['score'], reverse=True)
    
    return ranked_candidates
