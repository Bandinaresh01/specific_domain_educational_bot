import os
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Gemini API
api_key = os.getenv("GEMINI_API_KEY")
print(f"API Key: {api_key}")
genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-2.0-flash")

# Initialize embedding model (must match the one used during saving)
embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

def load_faiss_database(subject: str, index_dir: str = "faiss_index"):
    """
    Load the FAISS index for a given subject.

    Args:
        subject: Name of the subject
        index_dir: Directory where indices are stored

    Returns:
        FAISS vector store or None if not found
    """
    subject_index_dir = os.path.join(index_dir, f"{subject}_latest")
    if os.path.exists(os.path.join(subject_index_dir, "index.faiss")) and os.path.exists(os.path.join(subject_index_dir, "index.pkl")):
        faiss_db = FAISS.load_local(subject_index_dir, embedding_model, allow_dangerous_deserialization=True)
        return faiss_db
    else:
        return None

def query_faiss(query: str, faiss_db, k: int = 3):
    """
    Perform similarity search on the FAISS database.

    Args:
        query: User's query
        faiss_db: FAISS vector store
        k: Number of similar documents to retrieve

    Returns:
        List of similar documents
    """
    similar_docs = faiss_db.similarity_search(query, k=k)
    return similar_docs

def generate_answer(query: str, context: str) -> str:
    """
    Generate an answer using Gemini based on the context.

    Args:
        query: User's query
        context: Retrieved context from documents

    Returns:
        Generated answer
    """
    try:
        prompt = f"""
        You are an expert educational assistant specializing in the subject matter provided. Your role is to help students understand concepts clearly and accurately based on the reference material.

        Instructions:
        - Answer the question directly and comprehensively using the reference material.
        - If the reference material lacks sufficient information, supplement with accurate general knowledge but clearly indicate when doing so.
        - Provide explanations with examples where appropriate to aid learning.
        - Keep answers concise yet informative, avoiding unnecessary verbosity.
        - Structure answers logically: start with a direct answer, then explain, and end with key takeaways if relevant.
        - Use simple language suitable for students, but maintain technical accuracy.
        - If the question is not related to the subject, politely redirect to relevant topics.
        - Format your response using markdown: Use **bold** for emphasis, *italics* for terms, - for bullet points, 1. for numbered lists, and paragraphs for explanations. Ensure the output is well-structured and easy to read.

        Reference Material:
        {context}

        Student Question: {query}

        Answer:
        """
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error generating answer: {str(e)}. Please check your GEMINI_API_KEY in .env file."


