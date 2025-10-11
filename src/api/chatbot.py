from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel
from typing import List
import os
from ..services.preprocessing import preprocess_all_subjects
from ..services.vector_store import VectorStore
from ..services.embeddings import generate_embeddings
import numpy as np

router = APIRouter()

class ChatRequest(BaseModel):
    question: str
    subject: str

class ChatResponse(BaseModel):
    answer: str
    context: str

@router.get("/subjects", response_model=List[str])
async def list_subjects():
    pdf_dir = "../educational_pdf"
    if not os.path.exists(pdf_dir):
        return []
    subjects = [d for d in os.listdir(pdf_dir) if os.path.isdir(os.path.join(pdf_dir, d))]
    return subjects

@router.post("/chat", response_model=ChatResponse)
async def query_chatbot(chat_request: ChatRequest):
    try:
        vector_store = VectorStore(chat_request.subject)
        query_embedding = generate_embeddings([chat_request.question])[0]
        results = vector_store.search(query_embedding, k=3)
        context = " ".join([res[0] for res in results])
        # Placeholder answer; in a real app, use an LLM to generate based on context
        answer = f"Based on the retrieved context: {context[:500]}..."
        return ChatResponse(answer=answer, context=context)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/admin/reindex")
async def reindex_subjects(background_tasks: BackgroundTasks):
    background_tasks.add_task(preprocess_all_subjects)
    return {"message": "Reindexing started in background."}
