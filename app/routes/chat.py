from fastapi import APIRouter, HTTPException
from app.models import QuestionRequest
from app.services.rag_pipeline import ask

router = APIRouter()

@router.post("/chat")
def ask_question(request: QuestionRequest):
    try:
        return ask(request.query, level=request.level)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
