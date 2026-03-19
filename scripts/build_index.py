import json
import numpy as np
import faiss

def build_index(embeddings):
    dimensions = embeddings.shape[1]
    faiss_index = faiss.IndexFlatL2(dimensions)
    faiss_index.add(embeddings)
    print(f"Faiss index build with: {faiss_index.ntotal} vectors and dimensions: {dimensions}")
    return faiss_index


if __name__ == "__main__":
    embeddings = np.load("data/embeddings.npy")
    faiss_index = build_index(embeddings)
    faiss.write_index(faiss_index, "data/faiss.index")
    print("Faiss Index saved to data/faiss.index")