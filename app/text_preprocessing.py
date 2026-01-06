import re
import spacy

# from pathlib import Path

# MODEL_PATH = Path(__file__).parent / "en_core_web_sm"
# nlp = spacy.load(MODEL_PATH)

# nlp = spacy.load("en_core_web_sm")

try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    from spacy.cli import download
    download("en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")

def clean_text(text: str) -> str:
    text = text.lower()
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"[^a-zA-Z0-9 ]", "", text)
    return text.strip()

def preprocess_text(text: str) -> str:
    doc = nlp(clean_text(text))
    tokens = [
        token.lemma_
        for token in doc
        if not token.is_stop and not token.is_punct
    ]
    return " ".join(tokens)
