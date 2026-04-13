import numpy as np
import faiss
from config.settings import EMBEDDINGS_PATH, FAISS_INDEX_PATH


def build_index(embeddings):
    dimensions = embeddings.shape[1]
    faiss_index = faiss.IndexFlatL2(dimensions)
    faiss_index.add(embeddings)
    print(f"Faiss index build with: {faiss_index.ntotal} vectors and dimensions: {dimensions}")
    return faiss_index


if __name__ == "__main__":
    embeddings = np.load(EMBEDDINGS_PATH)
    faiss_index = build_index(embeddings)
    faiss.write_index(faiss_index, FAISS_INDEX_PATH)
    print(f"Faiss Index saved to {FAISS_INDEX_PATH}")
