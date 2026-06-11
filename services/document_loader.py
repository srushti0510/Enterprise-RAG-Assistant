from pypdf import PdfReader
from docx import Document
from services.url_loader import load_website


def load_pdf(uploaded_file):
    reader = PdfReader(uploaded_file)
    pages = []

    for page_num, page in enumerate(reader.pages, start=1):
        page_text = page.extract_text()
        if page_text and page_text.strip():
            pages.append({
                "text": page_text,
                "page": page_num
            })

    return pages


def load_docx(uploaded_file):
    doc = Document(uploaded_file)
    text = ""

    for para in doc.paragraphs:
        if para.text.strip():
            text += para.text + "\n"

    return [{
        "text": text,
        "page": None
    }]


def load_source(source, source_type):
    if source_type == "pdf":
        return load_pdf(source)

    elif source_type == "docx":
        return load_docx(source)

    elif source_type == "url":
        website_text = load_website(source)

        return [{
            "text": website_text,
            "page": None
        }]

    else:
        raise ValueError("Unsupported source type")


def load_document(uploaded_file):
    file_name = uploaded_file.name.lower()

    if file_name.endswith(".pdf"):
        return load_pdf(uploaded_file)

    elif file_name.endswith(".docx"):
        return load_docx(uploaded_file)

    else:
        raise ValueError("Unsupported file type.")