"""
Skill Extraction Module
CareerIQ Backend - services/skill_extractor.py
 
Uses a keyword list + spaCy noun chunks to extract skills from
resume text and job description, then computes:
  - matched_skills   : skills present in both
  - missing_skills   : skills required but not in resume
  - irrelevant_skills: skills in resume but not required by job
  - skill_score      : matched / required (0.0 – 1.0)
"""
 
import spacy
 
# ---------------------------------------------------------------------------
# Keyword bank  (extend this list as needed)
# ---------------------------------------------------------------------------
SKILL_KEYWORDS = [
    # Programming languages
    "python", "java", "c", "c++", "c#", "r", "go", "rust", "kotlin", "swift",
    "scala", "ruby", "php", "typescript", "javascript", "bash", "matlab",
 
    # Web / frameworks
    "html", "css", "react", "nextjs", "nodejs", "flask", "django", "fastapi",
    "spring", "angular", "vue", "express", "bootstrap", "tailwind",
 
    # Data / ML / AI
    "machine learning", "deep learning", "nlp", "natural language processing",
    "computer vision", "data science", "data analysis", "data engineering",
    "tensorflow", "pytorch", "keras", "scikit-learn", "sklearn",
    "numpy", "pandas", "matplotlib", "seaborn", "plotly",
    "transformers", "huggingface", "bert", "gpt", "llm",
 
    # Databases
    "sql", "mysql", "postgresql", "mongodb", "sqlite", "redis", "firebase",
    "oracle", "cassandra", "elasticsearch",
 
    # Cloud / DevOps
    "aws", "azure", "gcp", "docker", "kubernetes", "git", "github",
    "linux", "ci/cd", "jenkins", "terraform", "ansible",
 
    # Other tech
    "rest api", "graphql", "microservices", "agile", "scrum",
    "opencv", "pdfplumber", "spacy", "nltk",
 
    # Soft / generic
    "problem solving", "communication", "teamwork", "leadership",
    "project management", "research",
]
 
# Load spaCy model once at module level
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    nlp = None
    print("[skill_extractor] WARNING: spaCy model 'en_core_web_sm' not found. "
          "Run: python -m spacy download en_core_web_sm")
 
 
# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
 
def _keyword_skills(text: str) -> set:
    """Return all SKILL_KEYWORDS found in text (already lowercase)."""
    found = set()
    for skill in SKILL_KEYWORDS:
        # whole-word match so 'r' doesn't match inside 'research'
        if skill in ("r", "c"):
            import re
            pattern = r'\b' + re.escape(skill) + r'\b'
            import re as _re
            if _re.search(pattern, text):
                found.add(skill)
        else:
            if skill in text:
                found.add(skill)
    return found
 
 
def _spacy_skills(text: str) -> set:
    """Extract noun chunks via spaCy as additional skill candidates."""
    if nlp is None:
        return set()
    doc = nlp(text[:100_000])          # cap to avoid memory issues
    chunks = set()
    for chunk in doc.noun_chunks:
        token = chunk.text.lower().strip()
        if 2 <= len(token) <= 40:      # ignore single chars and very long phrases
            chunks.add(token)
    return chunks
 
 
# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------
 
def extract_skills(text: str) -> list:
    """
    Extract skills from a single piece of text (resume OR job description).
 
    Returns a list of skill strings found in the text.
    """
    text_lower = text.lower()
    keyword_hits = _keyword_skills(text_lower)
    spacy_hits   = _spacy_skills(text_lower)
 
    # Combine: keyword hits are authoritative; spaCy chunks are supplementary
    all_skills = keyword_hits | spacy_hits
    return sorted(all_skills)
 
 
def compare_skills(resume_text: str, jd_text: str) -> dict:
    """
    Compare skills between resume and job description.
 
    Args:
        resume_text (str): Cleaned resume text
        jd_text     (str): Cleaned job description text
 
    Returns:
        dict with keys:
            matched_skills    (list)
            missing_skills    (list)
            irrelevant_skills (list)
            skill_score       (float) 0.0 – 1.0
    """
    resume_skills = set(extract_skills(resume_text))
    jd_skills     = set(extract_skills(jd_text))
 
    matched    = resume_skills & jd_skills
    missing    = jd_skills - resume_skills
    irrelevant = resume_skills - jd_skills
 
    skill_score = round(len(matched) / len(jd_skills), 2) if jd_skills else 0.0
 
    return {
        "matched_skills":    sorted(matched),
        "missing_skills":    sorted(missing),
        "irrelevant_skills": sorted(irrelevant),
        "skill_score":       skill_score,
    }
 