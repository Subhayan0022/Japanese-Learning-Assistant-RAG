import os

# LLM
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://127.0.0.1:11434/api/generate")
MODEL_NAME = os.getenv("MODEL_NAME", "mistral")
TEMPERATURE = float(os.getenv("TEMPERATURE", "0.2"))

# API
BACKEND_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:8000")

# Embeddings
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "paraphrase-multilingual-MiniLM-L12-v2")

# Paths
CHUNKS_PATH = os.getenv("CHUNKS_PATH", "data/processed/chunks.json")
EMBEDDINGS_PATH = os.getenv("EMBEDDINGS_PATH", "data/processed/embeddings.npy")
FAISS_INDEX_PATH = os.getenv("FAISS_INDEX_PATH", "data/faiss_index/faiss.index")
RAW_DATA_DIR = os.getenv("RAW_DATA_DIR", "data/raw")

# Retrieval
TOP_K = int(os.getenv("TOP_K", "2"))
DISTANCE_THRESHOLD = float(os.getenv("DISTANCE_THRESHOLD", "24.0"))

# Chunking
CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "500"))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "50"))
