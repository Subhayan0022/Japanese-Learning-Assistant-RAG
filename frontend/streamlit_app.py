import streamlit as st
import requests

st.set_page_config(page_title="Japanese Learning Assistant", page_icon="🎌")

st.title("Japanese Learning Assistant")

level = st.selectbox("Your JLPT level:", ["Any", "N5", "N4", "N3", "N2", "N1"])

tab_chat, tab_breakdown = st.tabs(["Ask a Question", "Sentence Breakdown"])

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

                response = requests.post("http://127.0.0.1:8000/chat", json=payload)
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

                response = requests.post("http://127.0.0.1:8000/breakdown", json=payload)
                data = response.json()
                st.markdown("### Breakdown")
                st.write(data.get("breakdown", "Could not break down."))

                st.markdown("### Sources")
                for source in data.get("sources", []):
                    st.write(f"- Level: {source['level']} | Type: {source['type']} | Source: {source['source']}")
