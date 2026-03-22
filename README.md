# Japanese Learning Assistant (RAG)

A full-stack web application that answers Japanese grammar questions, breaks down sentences, and generates quizzes — powered by Retrieval-Augmented Generation (RAG). Built entirely with local, free tools. No LangChain, no paid APIs.

## Features

- **Ask Questions** — Get grounded answers about Japanese grammar, vocabulary, and kanji
- **Sentence Breakdown** — Paste a Japanese sentence and get a word-by-word analysis with readings, parts of speech, and grammar notes
- **Quiz Generation** — Generate interactive multiple-choice quizzes on any topic with scoring
- **JLPT Level Filtering** — Adapt responses to your level (N5 beginner to N1 advanced)
- **PDF Ingestion** — Load Japanese textbooks and study guides as your knowledge base
- **Hallucination Control** — Distance-based retrieval filtering and strict grounding rules ensure answers come from your data

## Architecture

```
User Question
     |
     v
  Embed Query (sentence-transformers)
     |
     v
  FAISS Similarity Search --> Top-K Chunks
     |
     v
  Build Prompt (context + rules + level)
     |
     v
  Ollama (Mistral) --> Grounded Response
```

## Tech Stack

| Component   | Technology                                    |
|-------------|-----------------------------------------------|
| LLM         | Ollama (Mistral 7B)                           |
| Embeddings  | sentence-transformers (multilingual MiniLM)   |
| Vector DB   | FAISS                                         |
| Backend     | FastAPI                                       |
| Frontend    | Streamlit                                     |
| PDF Parsing | PyMuPDF                                       |

## Project Structure

```
├── app/
│   ├── main.py                    # FastAPI entry point
│   ├── models/                    # Pydantic request models
│   ├── routes/
│   │   └── chat.py                # API endpoints (/chat, /breakdown, /quiz)
│   └── services/
│       ├── embeddings.py          # Embedding model (singleton)
│       ├── llm.py                 # Ollama communication
│       ├── prompt_builder.py      # Prompt templates
│       ├── rag_pipeline.py        # Core RAG orchestration
│       └── retrieval.py           # FAISS search with level filtering
├── config/
│   └── settings.py                # Centralized configuration (env-aware)
├── data/
│   ├── raw/                       # Source PDFs (gitignored)
│   ├── processed/                 # Chunks and embeddings (generated)
│   └── faiss_index/               # FAISS index (generated)
├── frontend/
│   ├── streamlit_app.py           # Streamlit UI with tabs
│   └── quiz_parser.py             # Quiz response parser
├── scripts/
│   ├── ingest.py                  # PDF ingestion and chunking
│   ├── embed.py                   # Embedding generation
│   └── build_index.py             # FAISS index builder
├── Dockerfile                     # Backend container
├── Dockerfile.frontend            # Frontend container
├── docker-compose.yml             # Multi-container setup
└── requirements.txt
```

## Getting Started

### Prerequisites

- Python 3.12+
- [Ollama](https://ollama.com/) installed and running

### Local Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/Subhayan0022/Japanese-Learning-Assistant-RAG.git
   cd Japanese-Learning-Assistant-RAG
   ```

2. **Create and activate virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Pull the LLM model**
   ```bash
   ollama pull mistral
   ```

5. **Add data**

   Place PDF files (Japanese textbooks, grammar guides) into `data/raw/`.

6. **Build the knowledge base**
   ```bash
   PYTHONPATH=. python scripts/ingest.py
   PYTHONPATH=. python scripts/embed.py
   PYTHONPATH=. python scripts/build_index.py
   ```

7. **Start the backend**
   ```bash
   uvicorn app.main:app --reload
   ```

8. **Start the frontend** (in a new terminal)
   ```bash
   streamlit run frontend/streamlit_app.py
   ```

9. Open `http://localhost:8501` in your browser.

### Docker Setup

1. **Make sure Ollama is running** on your host machine.

2. **Configure Ollama to accept external connections**
   ```bash
   sudo mkdir -p /etc/systemd/system/ollama.service.d
   echo '[Service]
   Environment="OLLAMA_HOST=0.0.0.0"' | sudo tee /etc/systemd/system/ollama.service.d/override.conf
   sudo systemctl daemon-reload
   sudo systemctl restart ollama
   ```

3. **Add data** into `data/raw/` and build the knowledge base (step 6 above).

4. **Build and run**
   ```bash
   docker compose up --build
   ```

5. Open `http://localhost:8501`.

## API Endpoints

### POST /chat
Ask a Japanese language question.
```json
{
  "query": "What is the topic marker particle?",
  "level": "N5"
}
```

### POST /breakdown
Break down a Japanese sentence word by word.
```json
{
  "sentence": "私は学校に行きます",
  "level": "N5"
}
```

### POST /quiz
Generate a multiple-choice quiz.
```json
{
  "topic": "particles",
  "level": "N4",
  "num_of_questions": 3
}
```

## Configuration

All settings are in `config/settings.py` and can be overridden via environment variables:

| Variable           | Default                              | Description                    |
|--------------------|--------------------------------------|--------------------------------|
| `OLLAMA_URL`       | `http://127.0.0.1:11434/api/generate`| Ollama API endpoint            |
| `MODEL_NAME`       | `mistral`                            | LLM model name                 |
| `TEMPERATURE`      | `0.2`                                | LLM temperature                |
| `EMBEDDING_MODEL`  | `paraphrase-multilingual-MiniLM-L12-v2` | Sentence transformer model |
| `TOP_K`            | `2`                                  | Number of chunks to retrieve   |
| `DISTANCE_THRESHOLD`| `24.0`                              | Max distance for relevant chunks|
| `CHUNK_SIZE`       | `500`                                | Characters per chunk           |
| `CHUNK_OVERLAP`    | `50`                                 | Overlap between chunks         |

## License

See [LICENSE](LICENSE) for details.
