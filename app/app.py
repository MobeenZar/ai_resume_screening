import streamlit as st
import pandas as pd
import sys
import os

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from app.resume_parser import parse_uploaded_resume
from app.text_preprocessing import preprocess_text
from app.skill_extractor import extract_skills
from app.matching_engine import MatchingEngine

# ==================================================
# Page Configuration (Dark Mode)
# ==================================================
st.set_page_config(
    page_title="AI Resume Screening System",
    layout="wide"
)

st.markdown(
    """
    <style>
    body {
        background-color: #0e1117;
        color: #fafafa;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ==================================================
# Predefined Job Descriptions
# ==================================================
JOB_DESCRIPTIONS = {
    "Select a role": "",
    "ML Expert": (
        "Looking for a Python Developer with experience in Machine Learning, "
        "NLP, and building REST APIs. Knowledge of FastAPI and SQL is a plus."
    ),
    "Java Expert": (
        "Looking for a Java Developer with strong experience in Java, "
        "Spring Boot, JPA, Hibernate, and Oracle database."
    ),
    "Data Scientist": (
        "Seeking a Data Scientist with experience in Python, data analysis, "
        "machine learning, statistics, and data visualization."
    )
}

# ==================================================
# App Header
# ==================================================
st.title("AI-Powered Resume Screening & Ranking")
st.markdown(
    "Upload resumes and rank them using **semantic AI-based matching** "
    "with explainable scoring."
)

# ==================================================
# Job Description Section
# ==================================================
st.subheader("📄 Job Description")

selected_role = st.selectbox(
    "Choose a predefined job role (optional) Or enter the job descrition",
    list(JOB_DESCRIPTIONS.keys())
)

job_description = st.text_area(
    "Job Description Text",
    value=JOB_DESCRIPTIONS[selected_role],
    height=180,
    placeholder="You can also write or edit the job description here..."
)

# ==================================================
# Resume Upload Section
# ==================================================
st.subheader("📂 Upload Resumes")

uploaded_files = st.file_uploader(
    "Upload resumes (PDF / DOCX / TXT)",
    type=["pdf", "docx", "txt"],
    accept_multiple_files=True
)

# ==================================================
# Run Matching
# ==================================================
if st.button("🚀 Run AI Matching"):

    if not job_description.strip():
        st.warning("Please provide a job description.")
        st.stop()

    if not uploaded_files:
        st.warning("Please upload at least one resume.")
        st.stop()

    engine = MatchingEngine()

    # ---------- Process Job Description ----------
    job_text = preprocess_text(job_description)
    job_skills = extract_skills(job_description)

    # ---------- Process Resumes ----------
    resume_names = []
    resume_texts = []
    resume_raw_texts = []
    resume_skills = []

    for file in uploaded_files:
        raw_text = parse_uploaded_resume(file)
        resume_names.append(file.name)
        resume_raw_texts.append(raw_text)
        resume_texts.append(preprocess_text(raw_text))
        resume_skills.append(extract_skills(raw_text))

    # ---------- Scoring ----------
    tfidf_scores, embedding_scores, skill_scores, final_scores = engine.detailed_scores(
        job_text,
        resume_texts,
        job_skills,
        resume_skills
    )

    results_df = pd.DataFrame({
        "Candidate": resume_names,
        "Final Score": final_scores,
        "TF-IDF Score": tfidf_scores,
        "Embedding Score": embedding_scores,
        "Skill Match %": [round(s * 100, 1) for s in skill_scores]
    }).sort_values("Final Score", ascending=False).reset_index(drop=True)

    # ==================================================
    # Resume Ranking Table (Row-Clickable)
    # ==================================================
    st.subheader("📊 Resume Ranking Results")

    st.data_editor(
        results_df,
        hide_index=True,
        disabled=True,
        use_container_width=True,
        key="ranking_table"
    )

    # SAFE access (prevents KeyError)
    selected_rows = st.session_state.get("ranking_table", {}).get("selected_rows", [])

    if selected_rows:
        selected_idx = selected_rows[0]
        selected_resume_name = results_df.loc[selected_idx, "Candidate"]
        raw_text = resume_raw_texts[resume_names.index(selected_resume_name)]

        st.subheader(f"📄 Resume Viewer — {selected_resume_name}")
        st.text_area(
            "Full Resume Content",
            value=raw_text,
            height=400
        )



    # ==================================================
    # Resume Viewer
    # ==================================================
    if selected_rows:
        selected_idx = selected_rows[0]
        selected_resume_name = results_df.loc[selected_idx, "Candidate"]
        raw_text = resume_raw_texts[resume_names.index(selected_resume_name)]

        st.subheader(f"📄 Resume Viewer — {selected_resume_name}")
        st.text_area(
            "Full Resume Content",
            value=raw_text,
            height=400
        )

    # ==================================================
    # Download Results
    # ==================================================
    st.download_button(
        "⬇️ Download Results as CSV",
        data=results_df.to_csv(index=False).encode("utf-8"),
        file_name="resume_ranking_results.csv",
        mime="text/csv"
    )

    # ==================================================
    # Score Explanation
    # ==================================================
    st.subheader("🧠 Scoring Methodology")

    st.markdown(
        """
        **Final Score = Hybrid AI Approach**

        - **40% TF-IDF Similarity**  
          Measures keyword relevance.

        - **50% Semantic Embedding Similarity**  
          Captures contextual meaning using embeddings.

        - **10% Skill Match**  
          Measures overlap between extracted job and resume skills.

        This hybrid model balances interpretability and accuracy.
        """
    )

    # ==================================================
    # Debug (Optional)
    # ==================================================
    with st.expander("🔍 Extracted Skills (Debug View)"):
        st.write("Job Skills:", job_skills)
        for name, skills in zip(resume_names, resume_skills):
            st.write(f"{name}:", skills)
