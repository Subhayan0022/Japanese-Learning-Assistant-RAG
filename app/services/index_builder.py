import json
import numpy as np
import faiss
import pymupdf as fitz
from app.services.embeddings import embed_texts
from config.settings import CHUNKS_PATH, EMBEDDINGS_PATH, FAISS_INDEX_PATH, CHUNK_SIZE, CHUNK_OVERLAP


def _split_text(text: str) -> list[str]:
    chunks = []
    start = 0
    while start < len(text):
        end = start + CHUNK_SIZE
        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)
        start = end - CHUNK_OVERLAP
    return chunks


def ingest_pdf_bytes(pdf_bytes: bytes, filename: str) -> list[dict]:
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    chunks = []

    for page_num in range(len(doc)):
        text = doc[page_num].get_text().strip()
        if not text:
            continue
        for chunk_text in _split_text(text):
            chunks.append({
                "text": chunk_text,
                "metadata": {
                    "source": filename,
                    "page": str(page_num + 1),
                    "type": "general",
                    "level": "unknown"
                }
            })

    doc.close()
    print(f"Ingested {len(chunks)} chunks from {filename}")
    return chunks


def rebuild_index(new_chunks: list[dict]):
    with open(CHUNKS_PATH, "r", encoding="utf-8") as f:
        existing_chunks = json.load(f)

    existing_embeddings = np.load(EMBEDDINGS_PATH)

    new_texts = [c["text"] for c in new_chunks]
    new_embeddings = embed_texts(new_texts)

    all_chunks = existing_chunks + new_chunks
    all_embeddings = np.vstack([existing_embeddings, new_embeddings])

    with open(CHUNKS_PATH, "w", encoding="utf-8") as f:
        json.dump(all_chunks, f, ensure_ascii=False, indent=4)

    np.save(EMBEDDINGS_PATH, all_embeddings)

    dimensions = all_embeddings.shape[1]
    index = faiss.IndexFlatL2(dimensions)
    index.add(all_embeddings)
    faiss.write_index(index, FAISS_INDEX_PATH)

    print(f"Index rebuilt: {index.ntotal} total vectors")
