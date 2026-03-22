def parse_quiz(quiz_text):
    questions = []
    current_q = None

    for line in quiz_text.strip().split("\n"):
        line = line.strip()
        if not line:
            continue
        if line.startswith("Q") and ":" in line:
            if current_q:
                questions.append(current_q)
            current_q = {"question": line.split(":", 1)[1].strip(), "options": [], "answer": ""}
        elif line.startswith(("A)", "B)", "C)", "D)")):
            if current_q:
                current_q["options"].append(line)
        elif line.startswith("Answer:"):
            if current_q:
                current_q["answer"] = line.split(":")[1].strip()

    if current_q:
        questions.append(current_q)

    return questions
