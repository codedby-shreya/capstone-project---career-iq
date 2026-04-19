import re
import spacy
import pdfplumber
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

nlp=spacy.load("en_core_web_sm")
#Text Extraction

#Text Processing

#After text processing
job_description=""
resume_text= ""

#For finding the education match score
def extract_education(text):
    education_patterns=[r'b\.tech',r'phd']
    found=[]

    for pattern in education_patterns:
        if re.search(pattern,text,re.IGNORECASE):
            found.append(pattern)
    
    return found 

jd_education= extract_education(job_description)
resume_education= extract_education(resume_text)


#For finding the experience match score
def extract_experience(text):
    
    matches=re.findall(pattern,text,re.IGNORECASE)

    if matches:
        return max([int(year) for year in matches])
    return 0

jd_exp=extract_experience(job_description)
resume_exp=extract_experience(resume_text)

experience_score=min(resume_exp/jd_exp)

#For the extraction of skills
def extract_skills(text):
    doc=nlp(text)
    skill=[]

    for chunk in doc.noun_chunks:
        skill.append()

    return skill

jd_skills=extract_skills(job_description)
resume_skill=extract_skills(resume_text)

matched_skill= ""


def compute_similarity(resume,jd):
    return 


def calculate_score(similarity,skill_ratio,exp_ratio,edu_ratio):
    score=()

    return round(score,2)

#Output in JSON
'''Result page: Readiness Score
               bar chart- (x-axis= skill_score, education,similarity,experience) (y-axis=numbers)
               Pie Chart- Matched
               Ribbon Chart- Useless Skill 
               Matched Skills - Checklist
               Skills Reqired
               Experience
               Education
               Final Verdict

'''