import PyPDF2
import docx

def parse_uploaded_resume(uploaded_file) -> str:
    """
    Parse PDF, DOCX, or TXT uploaded via Streamlit
    """
    file_type = uploaded_file.type

    # PDF
    if file_type == "application/pdf":
        reader = PyPDF2.PdfReader(uploaded_file)
        text = ""
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text
        return text

    # DOCX
    elif file_type == (
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    ):
        doc = docx.Document(uploaded_file)
        return "\n".join([para.text for para in doc.paragraphs])

    # TXT
    elif file_type == "text/plain":
        return uploaded_file.read().decode("utf-8")

    else:
        raise ValueError("Unsupported file format")
