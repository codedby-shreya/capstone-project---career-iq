"""
Education Extraction Module
CareerIQ Backend - services/education_extractor.py
 
Detects degree qualifications from resume and job description text
using regex patterns, then returns a match score (0.0 or 1.0).
 
Degree hierarchy (higher index = higher qualification):
    0: high school / 12th
    1: diploma
    2: bsc / ba / bcom / bca / btech / be
    3: msc / ma / mcom / mca / mtech / me / mba
    4: phd / doctorate
"""
 
import re
 
# ---------------------------------------------------------------------------
# Degree patterns  (order matters — more specific first)
# ---------------------------------------------------------------------------
DEGREE_PATTERNS = [
    (4, r'\b(ph\.?d|doctorate|doctor of philosophy)\b'),
    (3, r'\b(m\.?tech|m\.?e\.?|mtech|msc|m\.?sc|mba|m\.?b\.?a|mca|m\.?c\.?a|mcom|ma\b|master)\b'),
    (2, r'\b(b\.?tech|b\.?e\.?|btech|bsc|b\.?sc|bca|b\.?c\.?a|bcom|ba\b|bachelor)\b'),
    (1, r'\b(diploma|polytechnic)\b'),
    (0, r'\b(12th|hsc|higher secondary|high school|ssc|10th)\b'),
]
 
 
def _detect_degree(text: str) -> tuple:
    """
    Return (degree_level, degree_name) for the highest qualification found.
    Returns (-1, 'unknown') if nothing detected.
    """
    text_lower = text.lower()
    for level, pattern in DEGREE_PATTERNS:
        match = re.search(pattern, text_lower)
        if match:
            return level, match.group(0).strip()
    return -1, "unknown"
 
 
def extract_education(text: str) -> dict:
    """
    Extract education details from a single text.
 
    Returns:
        dict: { "degree_level": int, "degree_name": str }
    """
    level, name = _detect_degree(text)
    return {"degree_level": level, "degree_name": name}
 
 
def compare_education(resume_text: str, jd_text: str) -> dict:
    """
    Compare education between resume and job description.
 
    Logic:
        - If resume degree_level >= jd degree_level  → match (score 1.0)
        - Else → no match (score 0.0)
        - If JD has no education requirement          → score 1.0 (not checked)
 
    Returns:
        dict with keys:
            resume_education  (str)
            required_education(str)
            education_match   (bool)
            education_score   (float)
    """
    resume_edu = extract_education(resume_text)
    jd_edu     = extract_education(jd_text)
 
    # If JD doesn't specify any degree, give full marks
    if jd_edu["degree_level"] == -1:
        match = True
        score = 1.0
    else:
        match = resume_edu["degree_level"] >= jd_edu["degree_level"]
        score = 1.0 if match else 0.0
 
    return {
        "resume_education":   resume_edu["degree_name"],
        "required_education": jd_edu["degree_name"],
        "education_match":    match,
        "education_score":    score,
    }
 