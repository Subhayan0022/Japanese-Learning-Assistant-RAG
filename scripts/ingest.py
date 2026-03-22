import json
import os
import fitz
from config.settings import RAW_DATA_DIR, CHUNKS_PATH, CHUNK_SIZE, CHUNK_OVERLAP

def split_text(text, chunk_size, overlap):
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]

        if chunk.strip():
            chunks.append(chunk.strip())
        start = end - overlap

    return chunks

def parse_pdf_chunks(filepath):
    doc = fitz.open(filepath)
    filename = os.path.basename(filepath)
    chunks = []

    for page_num in range(len(doc)):
        page = doc[page_num]
        text = page.get_text().strip()

        if not text:
            continue

        page_chunks = split_text(text, CHUNK_SIZE, CHUNK_OVERLAP)

        for chunk_text in page_chunks:
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
    return chunks


def ingest_all():
    all_chunks = []

    for filename in os.listdir(RAW_DATA_DIR):
        filepath = os.path.join(RAW_DATA_DIR, filename)
        if filename.endswith(".pdf"):
            chunks = parse_pdf_chunks(filepath)
            print(f"[PDF] {filename}: {len(chunks)} chunks")
        else:
            print(f"[PDF] {filename}: unsupported file type")
            continue

        all_chunks.extend(chunks)

    return all_chunks


if __name__ == "__main__":
    chunks = ingest_all()

    print(f"TOTAL CHUNKS: {len(chunks)}")
    for idx, chunk in enumerate(chunks):
        print(f"Chunk {idx + 1}")
        print(f"Metadata {chunk['metadata']}")
        print(f"Chunk text: {chunk['text'][:80]}....")
        print()

    with open(CHUNKS_PATH, "w", encoding="utf-8") as f:
        json.dump(chunks, f, ensure_ascii=False, indent=4)

    print(f"Chunks written to {CHUNKS_PATH}")