from app.matching_engine import MatchingEngine
from app.resume_parser import parse_text_resume
from app.text_preprocessing import preprocess_text
from app.skill_extractor import extract_skills

# Job Description
job_description = """
Looking for a Python Developer with experience in Machine Learning,
NLP, and building REST APIs. Knowledge of FastAPI and SQL is a plus.
"""

job_text = preprocess_text(job_description)
job_skills = extract_skills(job_description)

# Load resumes
resume_files = [
    "data/sample_resumes/resume_1.txt",
    "data/sample_resumes/resume_2.txt",
    "data/sample_resumes/resume_3.txt"
]

resume_texts = []
resume_skills = []

for file in resume_files:
    text = parse_text_resume(file)
    resume_texts.append(preprocess_text(text))
    resume_skills.append(extract_skills(text))

engine = MatchingEngine()
scores = engine.hybrid_score(
    job_text,
    resume_texts,
    job_skills,
    resume_skills
)

for file, score in zip(resume_files, scores):
    print(f"{file}: {score:.3f}")
