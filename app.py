import os
import streamlit as st
import requests


API_BASE = os.getenv("FASTAPI_URL", "https://niti-rag.azurewebsites.net")

st.set_page_config(page_title="NITI RAG QA", layout="centered")
st.title("Ask Questions - NITI RAG System")

query = st.text_input("Enter your question")

if st.button("Get Answer") and query:
    with st.spinner("Generating answer..."):
        try:
            response = requests.post(
                f"{API_BASE}/ask",
                json={"question": query},
                timeout=10
            )
            if not response.ok:
                st.error(f"API error: {response.status_code} {response.text}")
            else:
                data = response.json()
                answer = data.get("answer", "No answer returned.")
                sources = data.get("sources", [])

                st.subheader("Answer:")
                st.write(answer)

                if sources:
                    st.subheader("Sources:")
                    for src in sources:
                        st.write(f"🔗 {src}")
        except requests.exceptions.Timeout:
            st.error("❌ Request timed out. Please try again.")
        except Exception as e:
            st.error(f"❌ Failed to get answer: {e}")
