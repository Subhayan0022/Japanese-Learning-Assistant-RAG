# LLM
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "mistral"
TEMPERATURE = 0.2

# Embeddings
EMBEDDING_MODEL = "paraphrase-multilingual-MiniLM-L12-v2"

# Paths
CHUNKS_PATH = "data/processed/chunks.json"
EMBEDDINGS_PATH = "data/processed/embeddings.npy"
FAISS_INDEX_PATH = "data/faiss_index/faiss.index"
RAW_DATA_DIR = "data/raw"

# Retrieval
TOP_K = 2
DISTANCE_THRESHOLD = 24.0

#Chunking
CHUNK_SIZE = 500
CHUNK_OVERLAP = 50
