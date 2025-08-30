# TODO List for Correcting Educational Chatbot Code

## 1. Update requirements.txt
- Add missing dependencies: unstructured, pdfplumber

## 2. Update existing app.py
- Change PDF_BASE_PATH to "educational_pdf"
- Ensure compatibility with new structure

## 3. Create preprocess.py
- Consolidate preprocessing logic from app.py and notebook
- Include OCR, hashing, FAISS creation
- Use proper naming conventions (subject-based)
- Handle new files via hashing

## 4. Create query.py
- Extract query logic from notebook
- Use environment variables for API key
- Make modular for different subjects

## 5. Create new app.py (Flask)
- Implement web interface for chatbot
- Integrate preprocess and query modules

## 6. Test and Validate
- Install dependencies
- Run preprocessing on educational_pdf
- Test query functionality
