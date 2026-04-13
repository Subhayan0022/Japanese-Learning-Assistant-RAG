import json
import numpy as np
from app.services.embeddings import embed_texts
from config.settings import CHUNKS_PATH, EMBEDDINGS_PATH


def generate_embeddings(chunks):
    texts = [chunk["text"] for chunk in chunks]

    print(f"Generating embeddings for {len(chunks)} chunks...")
    embeddings = embed_texts(texts)

    print(f"Embedding shape: {embeddings.shape}")
    return embeddings


if __name__ == "__main__":
    with open(CHUNKS_PATH, "r", encoding="utf-8") as f:
        chunks = json.load(f)
    embeddings = generate_embeddings(chunks)

    np.save(EMBEDDINGS_PATH, embeddings)
    print(f"Embeddings saved to {EMBEDDINGS_PATH}")
