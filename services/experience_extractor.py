"""
Experience Extraction Module
CareerIQ Backend - services/experience_extractor.py
 
Extracts years of experience from resume and job description text
using regex, then computes an experience ratio score.
"""
 
import re
 
 
# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
 
_YEAR_PATTERNS = [
    # "3+ years", "3 years", "three years"
    r'(\d+)\+?\s*years?\s*(of\s+)?(experience|exp)',
    # "experience of 2 years"
    r'experience\s+of\s+(\d+)\+?\s*years?',
    # standalone "2 years" near experience keyword
    r'(\d+)\+?\s*years?\s+experience',
]
 
_WORD_TO_NUM = {
    "one": 1, "two": 2, "three": 3, "four": 4, "five": 5,
    "six": 6, "seven": 7, "eight": 8, "nine": 9, "ten": 10,
}
 
 
def _extract_years(text: str) -> float:
    """
    Extract the maximum number of years of experience mentioned in text.
    Returns 0.0 if nothing found.
    """
    text_lower = text.lower()
 
    # Replace word numbers with digits for easier matching
    for word, num in _WORD_TO_NUM.items():
        text_lower = re.sub(r'\b' + word + r'\b', str(num), text_lower)
 
    years_found = []
    for pattern in _YEAR_PATTERNS:
        matches = re.findall(pattern, text_lower)
        for match in matches:
            # findall returns tuples when there are groups
            val = match[0] if isinstance(match, tuple) else match
            try:
                years_found.append(float(val))
            except ValueError:
                pass
 
    return max(years_found) if years_found else 0.0
 
 
# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------
 
def extract_experience(text: str) -> dict:
    """
    Extract experience years from a single text.
 
    Returns:
        dict: { "years": float }
    """
    return {"years": _extract_years(text)}
 
 
def compare_experience(resume_text: str, jd_text: str) -> dict:
    """
    Compare experience between resume and job description.
 
    Score logic:
        - If JD requires 0 years   → score 1.0
        - ratio = resume_years / required_years, capped at 1.0
 
    Returns:
        dict with keys:
            resume_experience   (float)  years found in resume
            required_experience (float)  years required by JD
            experience_score    (float)  0.0 – 1.0
    """
    resume_years   = _extract_years(resume_text)
    required_years = _extract_years(jd_text)
 
    if required_years == 0:
        score = 1.0
    else:
        score = min(round(resume_years / required_years, 2), 1.0)
 
    return {
        "resume_experience":   resume_years,
        "required_experience": required_years,
        "experience_score":    score,
    }
 