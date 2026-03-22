from typing import Optional
from pydantic import BaseModel

class QuestionRequest(BaseModel):
    query: str
    level: Optional[str] = None

class BreakdownRequest(BaseModel):
    sentence: str
    level: Optional[str] = None

class QuizRequest(BaseModel):
    topic: str
    level: Optional[str] = None
    num_of_questions: Optional[int] = 3
