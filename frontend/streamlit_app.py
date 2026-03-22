import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import streamlit as st
import requests
from frontend.quiz_parser import parse_quiz
from config.settings import BACKEND_URL

st.set_page_config(page_title="Japanese Learning Assistant", page_icon="🎌")

st.title("Japanese Learning Assistant")

level = st.selectbox("Your JLPT level:", ["Any", "N5", "N4", "N3", "N2", "N1"])

tab_chat, tab_breakdown, tab_quiz = st.tabs(["Ask a Question", "Sentence Breakdown", "Quiz"])

with tab_chat:
    question = st.text_area("Your question:", placeholder="e.g. What does 食べる mean?", key="chat")

    if st.button("Ask", key="ask_btn"):
        if question.strip() == "":
            st.warning("Please enter a question.")
        else:
            with st.spinner("Thinking..."):
                payload = {"query": question}
                if level != "Any":
                    payload["level"] = level

                response = requests.post(f"{BACKEND_URL}/chat", json=payload)
                data = response.json()
                st.markdown("### Answer")
                st.write(data.get("answer", "No answer."))

                st.markdown("### Sources")
                for source in data.get("sources", []):
                    st.write(f"- Level: {source['level']} | Type: {source['type']} | Source: {source['source']}")

with tab_breakdown:
    sentence = st.text_area("Japanese sentence:", placeholder="e.g. 私は学校に行きます", key="breakdown")

    if st.button("Break Down", key="breakdown_btn"):
        if sentence.strip() == "":
            st.warning("Please enter a sentence.")
        else:
            with st.spinner("Analyzing..."):
                payload = {"sentence": sentence}
                if level != "Any":
                    payload["level"] = level

                response = requests.post(f"{BACKEND_URL}/breakdown", json=payload)
                data = response.json()
                st.markdown("### Breakdown")
                st.write(data.get("breakdown", "Could not break down."))

                st.markdown("### Sources")
                for source in data.get("sources", []):
                    st.write(f"- Level: {source['level']} | Type: {source['type']} | Source: {source['source']}")

with tab_quiz:
    topic = st.text_input("Topic:", placeholder="e.g. particles, verbs, kanji", key="quiz_topic")
    num_questions = st.slider("Number of questions:", min_value=1, max_value=5, value=3, key="quiz_num")

    if st.button("Generate Quiz", key="quiz_btn"):
        if topic.strip() == "":
            st.warning("Please enter a topic.")
        else:
            with st.spinner("Generating quiz..."):
                payload = {"topic": topic, "num_of_questions": num_questions}
                if level != "Any":
                    payload["level"] = level

                response = requests.post(f"{BACKEND_URL}/quiz", json=payload)
                data = response.json()
                questions = parse_quiz(data.get("quiz", ""))
                st.session_state["quiz_questions"] = questions
                st.session_state["quiz_submitted"] = False

    if "quiz_questions" in st.session_state and st.session_state["quiz_questions"]:
        questions = st.session_state["quiz_questions"]

        with st.form("quiz_form"):
            user_answers = []
            for i, q in enumerate(questions):
                st.markdown(f"**Q{i + 1}: {q['question']}**")
                answer = st.radio(
                    "Select your answer:",
                    q["options"],
                    key=f"q_{i}",
                    label_visibility="collapsed"
                )
                user_answers.append(answer)

            submitted = st.form_submit_button("Submit Quiz")

        if submitted:
            st.session_state["quiz_submitted"] = True
            score = 0

            st.markdown("---")
            st.markdown("### Results")

            for i, q in enumerate(questions):
                correct_letter = q["answer"]
                selected = user_answers[i]
                selected_letter = selected[0] if selected else ""

                if selected_letter == correct_letter:
                    st.success(f"Q{i + 1}: Correct!")
                    score += 1
                else:
                    correct_option = next((o for o in q["options"] if o.startswith(correct_letter)), correct_letter)
                    st.error(f"Q{i + 1}: Wrong. Correct answer: {correct_option}")

            st.markdown(f"### Score: {score}/{len(questions)}")
