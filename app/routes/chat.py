from fastapi import APIRouter, HTTPException
from app.models import QuestionRequest, BreakdownRequest
from app.services.rag_pipeline import ask, breakdown

router = APIRouter()

@router.post("/chat")
def ask_question(request: QuestionRequest):
    try:
        return ask(request.query, level=request.level)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/breakdown")
def breakdown_sentence(request: BreakdownRequest):
    try:
        return breakdown(request.sentence, level=request.level)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))