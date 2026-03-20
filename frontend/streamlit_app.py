import streamlit as st
import requests

st.set_page_config(page_title="Japanese Learning Assistant", page_icon="🎌")

st.title("Japanese Learning Assistant")
st.write("Ask any questions about Japanese grammar, vocabulary, or Kanji!")

question = st.text_area("Your question: ", placeholder="e.g. What does 食べる mean?")
level = st.selectbox("Your JLPT level:", ["Any", "N5", "N4", "N3", "N2", "N1"])

if st.button("Ask"):
    if question.strip() == "":
        st.warning("Please enter a valid question.")

    else:
        with st.spinner("Thinking..."):
            payload = {"query": question}
            if level != "Any":
                payload["level"] = level

            response = requests.post(
                "http://127.0.0.1:8000/chat",
                json=payload,
            )
            data = response.json()
            st.markdown("### Answer")
            st.write(data.get("answer", "No answer for this question."))

            st.markdown("### Sources")
            for source in data.get("sources", []):
                st.write(f"- Level: {source['level']} | Type: {source['type']} | Source: {source['source']}")