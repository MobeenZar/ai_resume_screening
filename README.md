
# ai_resume_screening
Cap stone project for AtomCamp DS &amp; AI 

# How to run this application
There are 2 ways to run and test this application.
1. Run from the streamlit cloud
https://ai-resumescreening-mzar.streamlit.app/

2. Run by pulling the docker image from docker hub.
   docker run -d --name ai-resume-screening-app -p 8501:8501 mobeenzar/ai-resume-screening
   And then running: http://localhost:8501



📦 Create Virtual Environment & Install Dependencies

python -m venv venv 
venv\Scripts\activate 
 
pip install streamlit spacy scikit-learn pandas numpy \ 
           sentence-transformers PyPDF2 python-docx 
 
python -m spacy download en_core_web_sm 

📄 requirements.txt 
streamlit 
spacy 
scikit-learn 
pandas 
numpy 
sentence-transformers 
PyPDF2 
python-docx 
 
🚀 Phase 3: AI Matching Engine (CORE INTELLIGENCE) 
Build the heart of the system: 
•	TF-IDF similarity 
•	Sentence embeddings (MiniLM) 
•	Hybrid scoring 
•	Resume ranking 
This is the most important part of your project. 
 
📄 1. Matching Engine Module 
📌 app/matching_engine.py 

import numpy as np 
from sklearn.feature_extraction.text import TfidfVectorizer 
from sklearn.metrics.pairwise import cosine_similarity 
from sentence_transformers import SentenceTransformer 

class MatchingEngine: def init(self): self.tfidf = TfidfVectorizer() 
self.embedder = SentenceTransformer("all-MiniLM-L6-v2") 

def tfidf_similarity(self, job_text, resume_texts): 
   corpus = [job_text] + resume_texts 
   tfidf_matrix = self.tfidf.fit_transform(corpus) 
   similarities = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:]) 
   return similarities.flatten() 
 
def embedding_similarity(self, job_text, resume_texts): 
   job_emb = self.embedder.encode(job_text) 
   resume_embs = self.embedder.encode(resume_texts) 
   similarities = cosine_similarity([job_emb], resume_embs) 
   return similarities.flatten() 
 
def skill_overlap_score(self, job_skills, resume_skills): 
   scores = [] 
   job_set = set(job_skills) 
   for skills in resume_skills: 
       if not job_set: 
           scores.append(0.0) 
       else: 
           scores.append(len(job_set & set(skills)) / len(job_set)) 
   return np.array(scores) 
 
def hybrid_score( 
   self, 
   job_text, 
   resume_texts, 
   job_skills, 
   resume_skills, 
   weights=(0.4, 0.5, 0.1) 
): 
   tfidf_scores = self.tfidf_similarity(job_text, resume_texts) 
   emb_scores = self.embedding_similarity(job_text, resume_texts) 
   skill_scores = self.skill_overlap_score(job_skills, resume_skills) 
 
   final_scores = ( 
       weights[0] * tfidf_scores + 
       weights[1] * emb_scores + 
       weights[2] * skill_scores 
   ) 
   return final_scores 

🧪 2. Test the Matching Engine 
📌 app/test_matching_engine.py 

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
 
Run: 
python -m app.test_matching_engine 
 
✅ Expected Result 
•	resume_1.txt → highest score 
•	resume_2.txt → medium 
•	resume_3.txt → lower 
 
 
 




