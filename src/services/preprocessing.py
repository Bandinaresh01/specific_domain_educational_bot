import os
from PyPDF2 import PdfReader
from .embeddings import generate_embeddings
from .vector_store import VectorStore
import numpy as np

def extract_text_from_pdf(pdf_path: str) -> str:
    """Extract text from a PDF file."""
    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    return text

def chunk_text(text: str, chunk_size: int = 500) -> list[str]:
    """Split text into chunks of approximately chunk_size characters."""
    words = text.split()
    chunks = []
    current_chunk = ""
    for word in words:
        if len(current_chunk) + len(word) + 1 > chunk_size:
            chunks.append(current_chunk.strip())
            current_chunk = word
        else:
            current_chunk += " " + word
    if current_chunk:
        chunks.append(current_chunk.strip())
    return chunks

def preprocess_subject(subject: str, pdf_dir: str = "educational_pdf"):
    """Preprocess all PDFs for a given subject."""
    subject_dir = os.path.join(pdf_dir, subject)
    if not os.path.exists(subject_dir):
        print(f"Subject directory {subject_dir} not found.")
        return

    vector_store = VectorStore(subject)
    all_texts = []
    all_embeddings = []

    for pdf_file in os.listdir(subject_dir):
        if pdf_file.endswith('.pdf'):
            pdf_path = os.path.join(subject_dir, pdf_file)
            print(f"Processing {pdf_path}")
            text = extract_text_from_pdf(pdf_path)
            chunks = chunk_text(text)
            if chunks:
                embeddings = generate_embeddings(chunks)
                all_texts.extend(chunks)
                all_embeddings.extend(embeddings)

    if all_embeddings:
        embeddings_array = np.array(all_embeddings)
        vector_store.update_index(embeddings_array, all_texts)
        print(f"Updated index for subject: {subject}")

def preprocess_all_subjects(pdf_dir: str = "educational_pdf"):
    """Preprocess all subjects."""
    if not os.path.exists(pdf_dir):
        print(f"PDF directory {pdf_dir} not found.")
        return

    subjects = [d for d in os.listdir(pdf_dir) if os.path.isdir(os.path.join(pdf_dir, d))]
    for subject in subjects:
        preprocess_subject(subject, pdf_dir)
