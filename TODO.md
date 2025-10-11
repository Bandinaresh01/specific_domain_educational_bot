# TODO: Preprocess PDFs, Store FAISS Indices, Push to GitHub

## Step 1: Environment Setup
- [x] Update `requirements.txt` to add `PyPDF2` for PDF text extraction.
- [x] Create directory `data/indices/` for storing FAISS files.

## Step 2: Implement Preprocessing Pipeline
- [x] Extend `src/services/vector_store.py`: Add `create_index` method and subject-specific path handling.
- [x] Create `src/services/preprocessing.py`: Functions for PDF traversal, text extraction, chunking, embedding, and indexing.
- [x] Update `src/api/chatbot.py`: Implement `/subjects` and `/admin/reindex` endpoints.
- [x] Update `src/services/background_jobs.py`: Add preprocessing task.
- [x] Create `scripts/preprocess.py`: CLI script to run full preprocessing.

## Step 3: Run Preprocessing
- [ ] Install dependencies: `pip install -r requirements.txt`.
- [ ] Execute preprocessing: `python scripts/preprocess.py`.

## Step 4: GitHub Push
- [ ] Check Git status.
- [ ] Initialize Git if needed.
- [ ] Add files, commit, set remote (user provides URL), push.
