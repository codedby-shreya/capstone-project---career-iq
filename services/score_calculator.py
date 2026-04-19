"""
Score Calculator
CareerIQ Backend - services/score_calculator.py
 
Combines skill_score, education_score, experience_score, and
TF-IDF cosine similarity into a final career readiness score.
 
Weights (can be tuned):
    skill_score       : 40 %
    similarity_score  : 30 %
    education_score   : 20 %
    experience_score  : 10 %
"""
 
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
 
 
# ---------------------------------------------------------------------------
# Weights
# ---------------------------------------------------------------------------
WEIGHTS = {
    "skill":       0.40,
    "similarity":  0.30,
    "education":   0.20,
    "experience":  0.10,
}
 
 
def compute_similarity(resume_text: str, jd_text: str) -> float:
    """
    Compute TF-IDF cosine similarity between resume and job description.
 
    Returns:
        float: similarity score between 0.0 and 1.0
    """
    if not resume_text.strip() or not jd_text.strip():
        return 0.0
 
    vectorizer = TfidfVectorizer()
    try:
        tfidf_matrix = vectorizer.fit_transform([resume_text, jd_text])
        score = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
        return round(float(score), 2)
    except Exception as e:
        print(f"[score_calculator] Similarity error: {e}")
        return 0.0
 
 
def compute_final_score(
    skill_score: float,
    education_score: float,
    experience_score: float,
    similarity_score: float,
) -> dict:
    """
    Compute the weighted final career readiness score.
 
    Args:
        skill_score       (float): 0.0 – 1.0
        education_score   (float): 0.0 – 1.0
        experience_score  (float): 0.0 – 1.0
        similarity_score  (float): 0.0 – 1.0
 
    Returns:
        dict with keys:
            skill_score        (float)
            education_score    (float)
            experience_score   (float)
            similarity_score   (float)
            final_score        (float)  0.0 – 100.0 (percentage)
            verdict            (str)
    """
    final = (
        WEIGHTS["skill"]      * skill_score +
        WEIGHTS["education"]  * education_score +
        WEIGHTS["experience"] * experience_score +
        WEIGHTS["similarity"] * similarity_score
    )
    final_pct = round(final * 100, 1)
 
    if final_pct >= 75:
        verdict = "Strong Match – Ready to Apply!"
    elif final_pct >= 50:
        verdict = "Moderate Match – Work on Missing Skills"
    else:
        verdict = "Low Match – Significant Skill Gaps Found"
 
    return {
        "skill_score":       round(skill_score * 100, 1),
        "education_score":   round(education_score * 100, 1),
        "experience_score":  round(experience_score * 100, 1),
        "similarity_score":  round(similarity_score * 100, 1),
        "final_score":       final_pct,
        "verdict":           verdict,
    }
 