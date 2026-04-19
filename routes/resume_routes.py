"""
Resume Routes
CareerIQ Backend - routes/resume_routes.py
 
Endpoints:
    POST /analyze   — accepts resume PDF + job description text,
                      returns full career readiness analysis as JSON
"""
 
import os
from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
 
from services.extraction_service  import extract_text_from_pdf
from services.skill_extractor     import compare_skills
from services.education_extractor import compare_education
from services.experience_extractor import compare_experience
from services.score_calculator    import compute_similarity, compute_final_score
from utils.text_cleaner           import clean_text
 
resume_bp = Blueprint("resume", __name__)
 
# Temporary upload folder
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), "..", "upload")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
ALLOWED_EXTENSIONS = {"pdf"}
 
 
def _allowed_file(filename: str) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
 
 
# ---------------------------------------------------------------------------
# POST /analyze
# ---------------------------------------------------------------------------
@resume_bp.route("/analyze", methods=["POST"])
def analyze():
    """
    Accepts:
        - resume    : PDF file (multipart/form-data)
        - job_description : plain text (form field)
 
    Returns:
        JSON response with full analysis result
    """
    # ── Validate inputs ────────────────────────────────────────────────────
    if "resume" not in request.files:
        return jsonify({"error": "No resume file uploaded"}), 400
 
    file = request.files["resume"]
    job_description = request.form.get("job_description", "").strip()
 
    if file.filename == "":
        return jsonify({"error": "Empty filename"}), 400
 
    if not _allowed_file(file.filename):
        return jsonify({"error": "Only PDF files are supported"}), 400
 
    if not job_description:
        return jsonify({"error": "Job description is required"}), 400
 
    # ── Save PDF temporarily ───────────────────────────────────────────────
    filename = secure_filename(file.filename)
    pdf_path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(pdf_path)
 
    try:
        # ── Extract & clean text ───────────────────────────────────────────
        resume_text = extract_text_from_pdf(pdf_path)
        jd_text     = clean_text(job_description)
 
        if not resume_text:
            return jsonify({"error": "Could not extract text from resume PDF"}), 422
 
        # ── Run all extractors ─────────────────────────────────────────────
        skill_result    = compare_skills(resume_text, jd_text)
        education_result = compare_education(resume_text, jd_text)
        experience_result = compare_experience(resume_text, jd_text)
        similarity_score  = compute_similarity(resume_text, jd_text)
 
        # ── Compute final score ────────────────────────────────────────────
        scores = compute_final_score(
            skill_score       = skill_result["skill_score"],
            education_score   = education_result["education_score"],
            experience_score  = experience_result["experience_score"],
            similarity_score  = similarity_score,
        )
 
        # ── Build response ─────────────────────────────────────────────────
        response = {
            "scores": scores,
            "skills": {
                "matched_skills":    skill_result["matched_skills"],
                "missing_skills":    skill_result["missing_skills"],
                "irrelevant_skills": skill_result["irrelevant_skills"],
            },
            "education": {
                "resume_education":   education_result["resume_education"],
                "required_education": education_result["required_education"],
                "education_match":    education_result["education_match"],
            },
            "experience": {
                "resume_experience":   experience_result["resume_experience"],
                "required_experience": experience_result["required_experience"],
            },
        }
 
        return jsonify(response), 200
 
    except Exception as e:
        return jsonify({"error": f"Internal error: {str(e)}"}), 500
 
    finally:
        # Clean up uploaded file
        if os.path.exists(pdf_path):
            os.remove(pdf_path)
 