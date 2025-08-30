from flask import Flask, request, jsonify, render_template
import os
from query import load_faiss_database, query_faiss, generate_answer

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/subjects', methods=['GET'])
def get_subjects():
    index_dir = "faiss_index"
    subjects = []
    if os.path.exists(index_dir):
        for item in os.listdir(index_dir):
            if item.endswith("_latest"):
                subject = item.replace("_latest", "")
                subjects.append(subject)
    return jsonify(subjects)

@app.route('/query', methods=['POST'])
def query():
    data = request.json
    subject = data.get('subject')
    user_query = data.get('query')

    if not subject or not user_query:
        return jsonify({"error": "Subject and query are required"}), 400

    faiss_db = load_faiss_database(subject)
    if not faiss_db:
        return jsonify({"error": f"No data found for subject '{subject}'"}), 404

    similar_docs = query_faiss(user_query, faiss_db)
    context = "\n\n".join([doc.page_content for doc in similar_docs])

    answer = generate_answer(user_query, context)
    return jsonify({"answer": answer})

if __name__ == '__main__':
    app.run(debug=True)
