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

    def search(self, query, top_k=2, level=None):
        fetch_k = top_k * 3 if level else top_k
        query_vector = embed_query(query)
        distances, indices = self.index.search(query_vector, fetch_k)

        results = []
        for i, idx in enumerate(indices[0]):
            if idx < len(self.chunks):
                chunk = self.chunks[idx]
                chunk_level = chunk["metadata"].get("level", "unknown")
                if level and chunk_level != "unknown" and chunk_level.upper() != level.upper():
                    continue
                results.append({
                    "chunk": self.chunks[idx],
                    "distance": float(distances[0][i]),
                })
                if len(results) >= top_k:
                    break

        return results
