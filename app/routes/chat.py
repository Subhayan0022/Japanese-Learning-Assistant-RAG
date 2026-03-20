from typing import Optional

from fastapi import APIRouter
from pydantic import BaseModel
from app.services.rag_pipeline import ask

router = APIRouter()

class QuestionRequest(BaseModel):
    query: str
    level: Optional[str] = None

@router.post("/chat")
def ask_question(request: QuestionRequest):
    return ask(request.query, level=request.level)
