 =======import os
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
# Load environment variables
load_dotenv()

# Configure Gemini API
api_key = os.getenv("GEMINI_API_KEY")
print(f"API Key: {api_key}")
genai.configure(api_key=api_key)
# Load environment variables
load_dotenv()

# Configure Gemini API
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
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
    prompt = f"""
    Based on the following reference material, answer the user's question.
    If the reference material does not contain relevant information, provide your best answer based on general knowledge.

    Reference:
    {context}

    Question: {query}
    """
    response = model.generate_content(prompt)
    return response.text

def chatbot(subject: str):
    """
    Run the chatbot for a specific subject.

    Args:
        subject: Name of the subject
    """
    faiss_db = load_faiss_database(subject)
    if not faiss_db:
        print(f"No FAISS index found for subject '{subject}'.")
        return

    print(f"Chatbot loaded for subject: {subject}\n")

    while True:
        user_query = input("Ask a question (or type 'exit' to quit): ").strip()
        if user_query.lower() == "exit":
            print("Exiting.")
            break

        similar_docs = query_faiss(user_query, faiss_db)
        context = "\n\n".join([doc.page_content for doc in similar_docs])

        answer = generate_answer(user_query, context)
        print(answer)

if __name__ == "__main__":
    subject_choice = input("Select subject: ").strip().lower()
    chatbot(subject_choice)
