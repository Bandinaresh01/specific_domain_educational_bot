from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import os
from dotenv import load_dotenv
from query import load_faiss_database, query_faiss, generate_answer

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return render_template('intro.html')

@app.route('/select')
def select_subject():
    return render_template('subject_select.html')

@app.route('/chat/<subject>')
def chat(subject):
    return render_template('chat.html', subject=subject)

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

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/health', methods=['GET'])
def health():
    return {"status": "ok"}, 200

@app.route('/query', methods=['POST'])
def query():
    try:
        data = request.json or {}
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
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"error": "Internal server error"}), 500

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
