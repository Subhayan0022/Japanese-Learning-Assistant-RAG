from app.services.retrieval import RetrievalIndex
from app.services.llm import generate_response

retriever = RetrievalIndex()

def ask(question, top_k=2):
    results = retriever.search(question, top_k=top_k)

    context = "\n\n".join(r["chunk"]["text"] for r in results)

    prompt = f"""You are a Japanese Language teaching assistant.
    Answer the question using ONLY the context provided below.
    If the answer is not in the context, say "I dont have that information right now."
    
    Context: {context}
    Question: {question}
    Answer:"""

    answer = generate_response(prompt)

    sources = [r["chunk"]["metadata"] for r in results]

    return {"answer" : answer, "sources" : sources}

