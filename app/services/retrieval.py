import json
import faiss
from app.services.embeddings import embed_query
from config.settings import FAISS_INDEX_PATH, CHUNKS_PATH

class RetrievalIndex:
    def __init__(self):
        self.index = faiss.read_index(FAISS_INDEX_PATH)

        with open(CHUNKS_PATH, "r", encoding="utf-8") as f:
            self.chunks = json.load(f)

        print(f"Retrieval Index ready with: {len(self.chunks)} chunks loaded")

    def search(self, query, top_k=2):
        query_vector = embed_query(query)
        distances, indices = self.index.search(query_vector, top_k)

        results = []
        for i, idx in enumerate(indices[0]):
            if idx < len(self.chunks):
                results.append({
                    "chunk": self.chunks[idx],
                    "distance": distances[0][i],
                })
        return results