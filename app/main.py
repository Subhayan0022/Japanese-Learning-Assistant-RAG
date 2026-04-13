from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.routes.chat import router
from app.routes.upload import router as upload_router
from app.services.minio_client import ensure_bucket


@asynccontextmanager
async def lifespan(app: FastAPI):
    await ensure_bucket()
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(router)
app.include_router(upload_router)

@app.get("/")
def root():
    return {"status": "Japanese learning assistant is running"}
