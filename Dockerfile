# -------------------------------
# Base image
# -------------------------------
FROM python:3.10-slim
# FROM pytorch/pytorch:2.1.0-cpu

# -------------------------------
# Environment settings
# -------------------------------
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# -------------------------------
# System dependencies
# -------------------------------
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# -------------------------------
# Working directory
# -------------------------------
WORKDIR /app

# -------------------------------
# Install Python dependencies
# -------------------------------
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
# RUN python -m spacy download en_core_web_sm 
RUN python -m spacy download en_core_web_sm

# -------------------------------
# Copy project
# -------------------------------
COPY . .

# -------------------------------
# Expose Streamlit port
# -------------------------------
EXPOSE 8501

# -------------------------------
# Streamlit configuration
# -------------------------------
# ENV STREAMLIT_SERVER_ADDRESS=0.0.0.0
ENV STREAMLIT_SERVER_PORT=8501
ENV STREAMLIT_BROWSER_GATHER_USAGE_STATS=false

# -------------------------------
# Run Streamlit app
# -------------------------------
CMD ["streamlit", "run", "app/main.py"]