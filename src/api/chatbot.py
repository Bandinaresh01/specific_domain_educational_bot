from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel
from typing import List
import os
from ..services.preprocessing import preprocess_all_subjects

router = APIRouter()

class ChatRequest(BaseModel):
    question: str
    subject: str

class ChatResponse(BaseModel):
    answer: str
    context: str

@router.get("/subjects", response_model=List[str])
async def list_subjects():
    pdf_dir = "educational_pdf"
    if not os.path.exists(pdf_dir):
        return []
    subjects = [d for d in os.listdir(pdf_dir) if os.path.isdir(os.path.join(pdf_dir, d))]
    return subjects

@router.post("/chat", response_model=ChatResponse)
async def query_chatbot(chat_request: ChatRequest):
    # Placeholder: Implement search logic using VectorStore
    # For now, return dummy response
    return ChatResponse(answer="This is a placeholder answer.", context="Placeholder context.")

@router.post("/admin/reindex")
async def reindex_subjects(background_tasks: BackgroundTasks):
    background_tasks.add_task(preprocess_all_subjects)
    return {"message": "Reindexing started in background."}
