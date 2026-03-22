def get_level_instruction(level):
    if not level:
        return "Explain at a general level suitable for any learner."
    instructions = {
        "N5": "The student is a beginner. Use simple English, short sentences, and basic explanations.",
        "N4": "The student knows basics. Explain clearly with some grammatical terms",
        "N3": "The student is intermediate.Use moderate detail and grammatical terminology.",
        "N2": "The student is upper intermediate. Give detailed explanations with nuance.",
        "N1": "The student is advanced. Give in-depth explanations, compare similar patterns, discuss nuance."
    }

    return instructions.get(level.upper(), "Explain at a general level suitable for any learner.")

def build_prompt(context, question, level_instruction):
    return f"""You are a Japanese language teaching assistant.

        STRICT RULES:
        - Answer ONLY using the context provided below. Do not use any outside knowledge.
        - If the context does not contain enough information to answer, respond with EXACTLY: "I don't have information about that topic yet."
        - Do NOT generate, invent, or assume any information not present in the context.
        - Always include Japanese characters (kanji/hiragana/katakana) alongside romaji.
        - Only use examples that appear in the context.

        STUDENT LEVEL:
        {level_instruction}

        CONTEXT:
        {context}

        QUESTION: {question}

        Provide your answer in this format:

        Explanation:
        (Clear, simple explanation based on context)

        Examples:
        (Only use examples found in the context)

        Notes:
        (Only mention notes found in the context)"""


def build_breakdown_prompt(sentence, context, level_instruction):
    return f""" You are a Japanese language teaching assistant.
    STRICT RULES:
    - Break down the given Japanese sentence word by word.
    - For each word, provide: the word, its reading in hiragana, romanji, part of speech, and English meaning.
    - Use the context below to ground your explanations.
    - If a grammar point appears in the context, reference it.
    - Do NOT make up grammar rules not found in the context.
    
    STUDENT LEVEL: {level_instruction}
    
    CONTEXT: {context}
    
    SENTENCE: {sentence}
    
    Provide your breakdown in this format:
    
    Breakdown:
    - [word] ([reading]) - [part of speech] - [meaning]
    
    Grammar Notes:
    (Explain any grammar patterns used in the sentence, based on context)"""

def build_quiz_prompt(topic, context, level_instruction, num_of_questions):
    return f"""You are a Japanese language quiz generator.

STRICT RULES:
- You MUST generate EXACTLY {num_of_questions} questions. Not more, not less.
- Each question must test actual Japanese language knowledge (grammar, vocabulary, meaning, usage).
- Each question must have 4 options (A, B, C, D) with exactly one correct answer.
- Include Japanese characters in the questions and options where appropriate.
- Do NOT ask questions about section titles, page numbers, or document structure.
- Focus on practical knowledge: meanings, translations, correct usage, conjugations.

STUDENT LEVEL:
{level_instruction}

CONTEXT:
{context}

TOPIC: {topic}

Provide the quiz in this format:

Q1: [question]
A) [option]
B) [option]
C) [option]
D) [option]
Answer: [letter]

Q2: [question]
...up to Q{num_of_questions} only. Stop after Q{num_of_questions}."""