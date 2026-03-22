from typing import Optional
from pydantic import BaseModel

class QuestionRequest(BaseModel):
    query: str
    level: Optional[str] = None
