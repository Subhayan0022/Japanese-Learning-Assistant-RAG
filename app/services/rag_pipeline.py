from app.services.retrieval import RetrievalIndex
from app.services.llm import generate_response
from app.services.prompt_builder import build_prompt, get_level_instruction, build_breakdown_prompt, build_quiz_prompt
from config.settings import DISTANCE_THRESHOLD, TOP_K

retriever = RetrievalIndex()

# This function is for answering Japanese related questions.
def ask(question, top_k=TOP_K, level=None):
    results = retriever.search(question, top_k=top_k, level=level)

    relevant_results = [r for r in results if r["distance"] < DISTANCE_THRESHOLD]

    if not relevant_results:
        return {
            "answer": "I don't have information about that topic yet.",
            "sources": []
        }

    context_parts = []
    for i, r in enumerate(relevant_results, 1):
        meta = r["chunk"]["metadata"]
        context_parts.append(
            f"[Source {i} | Level: {meta['level']} | Type: {meta['type']}]\n{r['chunk']['text']}"
        )
    context = "\n\n".join(context_parts)

    level_instruction = get_level_instruction(level)
    prompt = build_prompt(context, question, level_instruction)
    answer = generate_response(prompt)

    sources = [r["chunk"]["metadata"] for r in relevant_results]

    return {"answer": answer, "sources": sources}

# This function is for breaking down Japanese text.
def breakdown(sentence, top_k=TOP_K, level=None):
    results = retriever.search(sentence, top_k=top_k, level=level)

    relevant_results = [r for r in results if r["distance"] < DISTANCE_THRESHOLD]

    context = ""
    if relevant_results:
        context_parts = []
        for i, r in enumerate(relevant_results, 1):
            meta = r["chunk"]["metadata"]
            context_parts.append(
                f"[Source {i} | Level: {meta['level']} | Type: {meta['type']}] \n{r['chunk']['text']} "
            )
        context = "\n\n".join(context_parts)

    level_instruction = get_level_instruction(level)
    prompt = build_breakdown_prompt(sentence, context, level_instruction)
    answer = generate_response(prompt)

    sources = [r["chunk"]["metadata"] for r in relevant_results]

    return {"breakdown": answer, "sources": sources}

# This function is for generating quiz.
def quiz(topic, top_k=TOP_K, level=None, num_of_questions=3):
    results = retriever.search(topic, top_k=top_k, level=level)

    relevant_results = [r for r in results if r["distance"] < DISTANCE_THRESHOLD]

    if not relevant_results:
        return {
            "quiz": "I don't have information about that topic yet.",
            "sources": []
        }

    context_parts = []
    for i, r in enumerate(relevant_results, 1):
        meta = r["chunk"]["metadata"]
        context_parts.append(
            f"[Source {i} | Level: {meta['level']} | Type: {meta['type']}]\n{r['chunk']['text']} "
        )
    context = "\n\n".join(context_parts)

    level_instruction = get_level_instruction(level)
    prompt = build_quiz_prompt(topic, context, level_instruction, num_of_questions)
    answer = generate_response(prompt, temperature=0.7)

    sources = [r["chunk"]["metadata"] for r in relevant_results]
    return {"quiz": answer, "sources": sources}

