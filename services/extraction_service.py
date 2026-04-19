"""
Resume Text Extraction Service
CareerIQ Backend - services/extraction_service.py
"""
 
import pdfplumber
from utils.text_cleaner import clean_text
 
 
def extract_text_from_pdf(pdf_path: str) -> str:
    """
    Extracts raw text from a PDF resume using pdfplumber.
 
    Args:
        pdf_path (str): File path to the uploaded PDF
 
    Returns:
        str: Cleaned extracted text from the PDF
    """
    raw_text = ""
 
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    raw_text += page_text + "\n"
    except Exception as e:
        print(f"[extraction_service] Error reading PDF: {e}")
        return ""
 
    return clean_text(raw_text)