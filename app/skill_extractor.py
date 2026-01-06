import spacy
from pathlib import Path

MODEL_PATH = Path(__file__).resolve().parent.parent / "models" / "en_core_web_sm" / "en_core_web_sm-3.8.0"
nlp = spacy.load(MODEL_PATH)

# nlp = spacy.load("en_core_web_sm")

# Curated skill list (extend anytime)
SKILL_SET = {
    "python", "machine learning", "nlp", "deep learning",
    "tensorflow", "keras", "scikit-learn", "pandas",
    "numpy", "sql", "git", "fastapi", "flask",
    "matplotlib", "linux", "java", "spring boot", "docker", "springboot", 
    "angular", "mybatis", "oracle"
}

def extract_skills(text: str) -> list:
    """
    Extract skills using phrase matching + keyword matching.
    """
    text = text.lower()
    extracted = []

    for skill in SKILL_SET:
        if skill in text:
            extracted.append(skill)

    return sorted(set(extracted))
'''

import re

SKILL_ALIASES = {
    "python": ["python"],
    "machine learning": ["machine learning", "ml"],
    "nlp": ["nlp", "natural language processing"],
    "deep learning": ["deep learning", "dl"],
    "tensorflow": ["tensorflow"],
    "keras": ["keras"],
    "scikit-learn": ["scikit-learn", "sklearn"],
    "pandas": ["pandas"],
    "numpy": ["numpy"],
    "sql": ["sql"],
    "git": ["git", "github"],
    "fastapi": ["fastapi"],
    "flask": ["flask"],
    "api": ["api", "apis", "rest api", "rest apis"],
    "linux": ["linux"]
}

def extract_skills(text: str) -> list:
    text = text.lower()
    found_skills = set()

    for canonical, variants in SKILL_ALIASES.items():
        for v in variants:
            if re.search(rf"\b{re.escape(v)}\b", text):
                found_skills.add(canonical)

    return sorted(found_skills)

    
'''


