'''
AI Matching Engine (CORE INTELLIGENCE)
Now we build the heart of the system:
TF-IDF similarity
Sentence embeddings (MiniLM)
Hybrid scoring
Resume ranking

This is the most important part of your project.
'''


import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer

class MatchingEngine:
    def __init__(self):
        self.tfidf = TfidfVectorizer()
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


    def detailed_scores(
        self,
        job_text,
        resume_texts,
        job_skills,
        resume_skills,
        weights=(0.4, 0.5, 0.1)
    ):
        tfidf = self.tfidf_similarity(job_text, resume_texts)
        emb = self.embedding_similarity(job_text, resume_texts)
        skill = self.skill_overlap_score(job_skills, resume_skills)

        final = (
            weights[0] * tfidf +
            weights[1] * emb +
            weights[2] * skill
        )

        return tfidf, emb, skill, final
