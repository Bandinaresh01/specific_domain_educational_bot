from query import load_faiss_database, query_faiss

def test_faiss_bot(subject: str, query: str):
    faiss_db = load_faiss_database(subject)
    if not faiss_db:
        print(f"FAISS index not found for subject: {subject}")
        return
    print(f"FAISS index loaded for subject: {subject}")

    docs = query_faiss(query, faiss_db)
    print(f"Number of documents retrieved: {len(docs)}")
    for i, doc in enumerate(docs):
        print(f"Document {i+1} content preview: {doc.page_content[:200]}...\n")

if __name__ == "__main__":
    test_subject = "computer_network"
    test_query = "What is a computer network?"
    test_faiss_bot(test_subject, test_query)
