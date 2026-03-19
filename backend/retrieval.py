import json
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

MODEL_NAME = "paraphrase-multilingual-MiniLM-L12-v2"

class RetrievalIndex:
    def __init__(self):
        self.model = SentenceTransformer(MODEL_NAME)
        self.index = faiss.read_index("data/faiss.index")

        with open("data/chunks.json", "r", encoding="utf-8") as f:
            self.chunks = json.load(f)

        print(f"Retrieval Index ready with: {len(self.chunks)} chunks loaded")


    def search(self, query, top_k=2):
        query_vector = self.model.encode([query])
        distances, indices = self.index.search(query_vector, top_k)

        results = []
        for i, idx in enumerate(indices[0]):
            if idx < len(self.chunks):
                results.append({
                    "chunk": self.chunks[idx],
                    "distance": distances[0][i],
                })
        return results