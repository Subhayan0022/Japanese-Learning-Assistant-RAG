import json
import numpy as np
from sentence_transformers import SentenceTransformer

MODEL_NAME = "paraphrase-multilingual-MiniLM-L12-v2"

def generate_embeddings(chunks):
    print(f"Initializing model :{MODEL_NAME}")
    model = SentenceTransformer(MODEL_NAME)

    texts = [chunk["text"] for chunk in chunks]

    print(f"Generating embeddings for {len(chunks)} chunks...")
    embeddings = model.encode(texts, show_progress_bar=True)

    print(f"Embedding shape : {embeddings.shape}")
    return embeddings

if __name__ == "__main__":
    with open("data/chunks.json", "r", encoding="utf-8") as f:
        chunks = json.load(f)
    embeddings = generate_embeddings(chunks)

    np.save("data/embeddings.npy", embeddings)
    print(f"Embeddings saved to data/embeddings.npy")