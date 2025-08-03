import os
import streamlit as st
import requests

API_BASE = os.getenv("FASTAPI_URL", "https://niti-rag.azurewebsites.net").rstrip("/")

st.set_page_config(page_title="NITI RAG QA", layout="centered")
st.title("Ask Questions - NITI RAG System")

query = st.text_input("Enter your question")

if st.button("Get Answer") and query:
    st.write(f"**DEBUG:** Using FASTAPI_URL = {API_BASE}")
    with st.spinner("Generating answer..."):
        try:
            response = requests.post(
                f"{API_BASE}/ask",
                json={"question": query},
                timeout=15
            )
            st.write(f"**DEBUG:** HTTP Status Code: {response.status_code}")
            try:
                data = response.json()
            except Exception as e:
                st.error(f"Failed to parse JSON response: {e}")
                st.text(response.text)
                st.stop()

            answer = data.get("answer", "No answer returned.")
            sources = data.get("sources", [])

            st.subheader("Answer:")
            st.write(answer)

            if sources:
                st.subheader("Sources:")
                for src in sources:
                    st.write(f"🔗 {src}")
        except requests.exceptions.Timeout:
            st.error("❌ Request timed out (after 15s). Backend may be slow or unreachable.")
        except requests.exceptions.RequestException as e:
            st.error(f"❌ Request failed: {e}")
