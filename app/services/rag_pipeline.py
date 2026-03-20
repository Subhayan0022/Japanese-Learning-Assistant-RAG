from app.services.retrieval import RetrievalIndex
from app.services.llm import generate_response

retriever = RetrievalIndex()

DISTANCE_THRESHOLD = 24.0

def ask(question, top_k=2):
    results = retriever.search(question, top_k=top_k)

    # Filter out chunks that are too far away (not relevant)
    relevant_results = [r for r in results if r["distance"] < DISTANCE_THRESHOLD]

    if not relevant_results:
        return {
            "answer": "I don't have information about that topic yet.",
            "sources": []
        }

    context = "\n\n".join(r["chunk"]["text"] for r in relevant_results)

    prompt = f"""You are a Japanese language teaching assistant.

    STRICT RULES:
    - Answer ONLY using the context provided below. Do not use any outside knowledge.
    - If the context does not contain enough information to answer, respond with EXACTLY: "I don't have information about that topic yet."
    - Do NOT generate, invent, or assume any information not present in the context.
    - Always include Japanese characters (kanji/hiragana/katakana) alongside romaji.
    - Only use examples that appear in the context.
    
    CONTEXT:
    {context}
    
    QUESTION: {question}
    
    If the context contains relevant information, provide your answer in this format:
    
    Explanation:
    (Clear, simple explanation based on context)
    
    Examples:
    (Only use examples found in the context)
    
    Notes:
    (Only mention notes found in the context)"""

    answer = generate_response(prompt)

    sources = [r["chunk"]["metadata"] for r in relevant_results]

    return {"answer" : answer, "sources" : sources}

