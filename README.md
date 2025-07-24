# 🎓 AI-Powered Educational Chatbot for University Syllabi

An intelligent chatbot that answers student queries based on university syllabus PDFs. It uses **FAISS** for efficient vector similarity search, **SentenceTransformer** for semantic embeddings, **Gemini 1.5 Flash** for generating answers, and a **Flask-based web interface** for smooth interaction.

---

## 🔍 Overview

This project solves a common problem in academic settings: helping students find accurate, syllabus-aligned answers quickly. Instead of generic web results, this chatbot provides **subject-specific, document-based answers** using real syllabus PDFs uploaded by faculty or admins.

---

## 🚀 Features

- 🔍 **PDF-based QA System** – Answers are retrieved from syllabus documents.
- ⚡ **FAISS Vector Store** – Fast and scalable similarity search.
- 🧠 **Gemini API (LLM)** – Generates high-quality natural language responses.
- 🗂️ **Subject-wise Navigation** – Organized by folder (e.g., `big_data`, `computer_vision`, etc.).
- 🌐 **Flask Frontend** – Simple and elegant UI to interact with the chatbot.

---

## 🧱 Tech Stack

| Component              | Technology                  |
|------------------------|-----------------------------|
| Backend (LLM)          | Gemini 1.5 Flash (Google)   |
| Vector Embedding       | SentenceTransformer (SBERT) |
| Vector Indexing        | FAISS                       |
| Web Framework          | Flask (Python)              |
| Deployment             | Localhost / Render / Railway |
| PDF Parsing            | PyMuPDF / pdfplumber        |

---

## 📂 Project Structure

