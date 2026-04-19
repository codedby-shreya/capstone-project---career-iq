"""
Text Cleaning Utility
CareerIQ Backend - utils/text_cleaner.py
"""
 
import re
 
 
def clean_text(text: str) -> str:
    """
    Cleans raw resume/job description text before NLP processing.
 
    Steps:
    1. Convert to lowercase
    2. Remove punctuation and special characters (keep alphanumeric + spaces)
    3. Remove extra whitespace
 
    Args:
        text (str): Raw text
 
    Returns:
        str: Cleaned text
    """
    if not text:
        return ""
 
    # Convert to lowercase
    text = text.lower()
 
    # Remove punctuation and special characters
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
 
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text).strip()
 
    return text