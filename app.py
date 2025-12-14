import streamlit as st
from crawler import crawl_website
from preprocess import chunk_text
from vector_store import build_faiss_index
from rag import retrieve_chunks, generate_answer

st.set_page_config(page_title="Website RAG Chatbot", layout="centered")
st.title("🌐 Website RAG Chatbot")

@st.cache_resource(show_spinner=True)
def build_knowledge_base(url):
    pages = crawl_website(url)

    if not pages:
        raise ValueError("No pages were crawled")

    full_text = "\n\n".join(pages)   # 🔥 CRITICAL FIX
    chunks = chunk_text(full_text)

    if not chunks:
        raise ValueError("No chunks created")

    index, stored_chunks = build_faiss_index(chunks)
    return index, stored_chunks

url = st.text_input("Enter Website URL")

if st.button("Crawl & Build Knowledge Base"):
    if not url:
        st.warning("Please enter a valid URL")
    else:
        with st.spinner("Crawling website and building knowledge base..."):
            index, stored_chunks = build_knowledge_base(url)
            st.session_state.index = index
            st.session_state.chunks = stored_chunks
            st.success("Knowledge base built successfully!")

if "index" in st.session_state:
    question = st.text_input("Ask a question about the website")

    if st.button("Ask"):
        retrieved = retrieve_chunks(
            question,
            st.session_state.index,
            st.session_state.chunks
        )
        answer = generate_answer(question, "\n".join(retrieved))
        st.write(answer)

