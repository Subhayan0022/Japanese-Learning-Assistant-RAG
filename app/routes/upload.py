from fastapi import APIRouter, HTTPException, UploadFile, File
from app.models import UploadResponse
from app.services.relevance_checker import check_relevance
from app.services.index_builder import ingest_pdf_bytes, rebuild_index
from app.services.minio_client import upload_file
import app.services.rag_pipeline as rag_pipeline

router = APIRouter()


@router.post("/upload", response_model=UploadResponse)
async def upload_pdf(file: UploadFile = File(...)):
    if not file.filename or not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are accepted.")

    pdf_bytes = await file.read()

    is_relevant, message = check_relevance(pdf_bytes, rag_pipeline.retriever)
    if not is_relevant:
        raise HTTPException(status_code=400, detail=message)

    await upload_file(file.filename, pdf_bytes)

    new_chunks = ingest_pdf_bytes(pdf_bytes, file.filename)
    rebuild_index(new_chunks)
    rag_pipeline.reload_retriever()

    return UploadResponse(
        filename=file.filename,
        chunks_added=len(new_chunks),
        message="PDF uploaded and indexed successfully."
    )
