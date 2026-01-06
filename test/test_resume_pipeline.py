from app.resume_parser import parse_text_resume
from app.skill_extractor import extract_skills
from app.text_preprocessing import preprocess_text

resume_text = parse_text_resume("data/sample_resumes/resume_1.txt")
processed_text = preprocess_text(resume_text)
skills = extract_skills(resume_text)

print("Processed Text:")
print(processed_text)
print("\nExtracted Skills:")
print(skills)
