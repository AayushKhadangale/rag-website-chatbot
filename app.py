import streamlit as st
from crawler import crawl_website
from preprocess import chunk_text
from vector_store import build_faiss_index
from rag import retrieve_chunks, generate_answer

st.set_page_config(page_title="Website RAG Chatbot", layout="centered")

st.title("🌐 Website RAG Chatbot")

# ---------- CACHE HEAVY OPERATION ----------
@st.cache_resource(show_spinner=True)
def build_knowledge_base(url):
    pages = crawl_website(url)
    chunks = chunk_text(pages)
    index, stored_chunks = build_faiss_index(chunks)
    return index, stored_chunks

# ---------- UI ----------
url = st.text_input("Enter Website URL")

if st.button("Crawl & Build Knowledge Base"):
    if not url:
        st.warning("Please enter a valid URL")
    else:
        index, stored_chunks = build_knowledge_base(url)
        st.session_state.index = index
        st.session_state.chunks = stored_chunks
        st.success("Knowledge base built successfully!")

question = st.text_input("Ask a question about the website")

if st.button("Ask"):
    if "index" not in st.session_state:
        st.warning("Please crawl a website first.")
    else:
        retrieved = retrieve_chunks(
            st.session_state.index,
            st.session_state.chunks,
            question
        )
        answer = generate_answer(question, "\n".join(retrieved))
        st.write(answer)

