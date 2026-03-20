from fastapi import FastAPI
from app.routes.chat import router

app = FastAPI()

app.include_router(router)

@app.get("/")
def root():
    return {"status": "Japanese learning assistant is running"}
