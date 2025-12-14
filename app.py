import streamlit as st

from crawler import crawl_website
from preprocess import chunk_text
from vector_store import build_faiss_index
from rag import retrieve_chunks, generate_answer


# -------------------------
# Streamlit Page Config
# -------------------------
st.set_page_config(page_title="Website RAG Chatbot", layout="centered")

st.title("🌐 Website RAG Chatbot")


# -------------------------
# STEP 3.2 — CACHE HEAVY OPS
# -------------------------
@st.cache_resource(show_spinner=True)
def build_knowledge_base(url):
    pages = crawl_website(url)
    chunks = chunk_text(pages)
    index, stored_chunks = build_faiss_index(chunks)
    return index, stored_chunks


# -------------------------
# URL INPUT
# -------------------------
url = st.text_input("Enter Website URL")


# -------------------------
# BUILD KB BUTTON
# -------------------------
if st.button("Crawl & Build Knowledge Base"):
    if not url:
        st.warning("Please enter a valid URL")
    else:
        with st.spinner("Crawling website and building knowledge base..."):
            index, stored_chunks = build_knowledge_base(url)

            st.session_state.index = index
            st.session_state.chunks = stored_chunks

        st.success("Knowledge base built successfully!")


# -------------------------
# QUESTION ANSWERING
# -------------------------
if "index" in st.session_state and "chunks" in st.session_state:
    question = st.text_input("Ask a question about the website")

    if st.button("Ask"):
        with st.spinner("Thinking..."):
            retrieved_chunks = retrieve_chunks(
                question,
                st.session_state.index,
                st.session_state.chunks
            )

            answer = generate_answer(
                question,
                "\n".join(retrieved_chunks)
            )

        st.markdown("### ✅ Answer")
        st.write(answer)

