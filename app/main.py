from fastapi import FastAPI
from pydantic import BaseModel
import requests

app = FastAPI()

class QuestionRequest(BaseModel):
    question: str

@app.get("/")
def root():
    return {"status": "Japanese learning assistant is running"}

@app.post("/ask")
def ask(request: QuestionRequest):
  response = requests.post(
      "http://localhost:11434/api/generate",
      json={
          "model": "mistral",
          "prompt": request.question,
          "stream": False
      }
  )
  data = response.json()
  answer = data.get("response", "")
  return {"answer": answer}
