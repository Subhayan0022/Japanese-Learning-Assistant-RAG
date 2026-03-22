from fastapi import APIRouter, HTTPException
from app.models import QuestionRequest, BreakdownRequest, QuizRequest
from app.services.rag_pipeline import ask, breakdown, quiz

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


@router.post("/quiz")
def generate_quiz(request: QuizRequest):
    try:
        return quiz(request.topic, top_k=5, level=request.level, num_of_questions=request.num_of_questions)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))