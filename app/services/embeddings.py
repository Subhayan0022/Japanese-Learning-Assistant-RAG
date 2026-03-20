from sentence_transformers import SentenceTransformer
from config.settings import EMBEDDING_MODEL

model = None

def get_model():
    global model
    if model is None:
        model = SentenceTransformer(EMBEDDING_MODEL)
    return model

def embed_texts(texts):
    return get_model().encode(texts, show_progress_bar=True)

def embed_query(query):
    return get_model().encode([query])
