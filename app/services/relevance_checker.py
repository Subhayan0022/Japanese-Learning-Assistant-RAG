import pymupdf as fitz
import numpy as np
from app.services.embeddings import embed_texts
from app.services.retrieval import RetrievalIndex

RELEVANCE_THRESHOLD = 50.0
SAMPLE_PAGES = 3

def extract_sample_text(pdf_bytes: bytes) -> str:
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    text = ""
    for i in range(min(SAMPLE_PAGES, len(doc))):
        text += doc[i].get_text()
    doc.close()
    return text.strip()

def check_relevance(pdf_bytes: bytes, retriever: RetrievalIndex) -> tuple[bool, str]:
    sample_text = extract_sample_text(pdf_bytes)

    if not sample_text:
        return False, "Could not extract text from PDF."

    chunks = [sample_text[i:i+500] for i in range(0, min(len(sample_text), 2000), 500)]

    embeddings = embed_texts(chunks)
    distances, _ = retriever.index.search(np.array(embeddings), 1)
    avg_distance = float(np.mean(distances))

    print(f"Relevance check — avg distance: {avg_distance:.2f}")

    if avg_distance < RELEVANCE_THRESHOLD:
        return True, "PDF is relevant to Japanese learning."
    else:
        return False, f"PDF does not appear to be Japanese learning material (score: {avg_distance:.1f})."
