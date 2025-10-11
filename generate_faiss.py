# This file is deprecated. Use preprocess.py for generating FAISS indices from actual PDF/PPT documents.

import os
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings

# Example: Your documents should be loaded per subject
# Replace this with your actual document loading logic
def load_documents_for_subject(subject):
    # Dummy example: Replace with your own loader
    # Return a list of strings or Document objects
    return ["Example content for " + subject]

subjects = ["computer_network_vafa52be8bf13660fb10f46e35ec34f53"]  # Add all your subjects here

embedding_model = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2')
faiss_index_dir = "faiss_index"

os.makedirs(faiss_index_dir, exist_ok=True)

for subject in subjects:
    docs = load_documents_for_subject(subject)
    vector_store = FAISS.from_texts(docs, embedding_model)
    subject_dir = os.path.join(faiss_index_dir, subject)
    os.makedirs(subject_dir, exist_ok=True)
    vector_store.save_local(subject_dir)
    print(f"FAISS index generated for subject: {subject}")
