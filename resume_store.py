import os
import json
from dotenv import load_dotenv
import pdfplumber
from docx import Document

load_dotenv()

RESUME_PATH = "./stored_resume.txt"

def extract_text_from_pdf(file_path: str) -> str:
    text = []
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            t = page.extract_text()
            if t:
                text.append(t)
    return "\n".join(text)

def extract_text_from_docx(file_path: str) -> str:
    doc = Document(file_path)
    return "\n".join([p.text for p in doc.paragraphs if p.text.strip()])

def save_resume(text: str):
    with open(RESUME_PATH, "w", encoding="utf-8") as f:
        f.write(text)

def load_resume() -> str:
    if not os.path.exists(RESUME_PATH):
        return ""
    with open(RESUME_PATH, "r", encoding="utf-8") as f:
        return f.read()

def resume_exists() -> bool:
    return os.path.exists(RESUME_PATH) and os.path.getsize(RESUME_PATH) > 0

def process_resume_file(file_path: str) -> str:
    ext = file_path.lower().split(".")[-1]
    if ext == "pdf":
        text = extract_text_from_pdf(file_path)
    elif ext in ["docx", "doc"]:
        text = extract_text_from_docx(file_path)
    elif ext == "txt":
        with open(file_path, "r", encoding="utf-8") as f:
            text = f.read()
    else:
        raise ValueError(f"Unsupported file type: {ext}")
    save_resume(text)
    return text

if __name__ == "__main__":
    # Test with stored resume
    if resume_exists():
        print("Resume found:")
        print(load_resume()[:500])
    else:
        print("No resume stored yet.")