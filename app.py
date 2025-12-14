import streamlit as st
from crawler import crawl_website
from preprocess import chunk_text
from vector_store import build_faiss_index
from rag import retrieve_chunks, generate_answer

st.set_page_config(page_title="Website RAG Chatbot", layout="centered")
st.title("🌐 Bajaj Finserv Chatbot")

@st.cache_resource(show_spinner=True)
def build_knowledge_base(url):
    pages = crawl_website(url)

    if not pages:
        raise ValueError("No pages were crawled")

    full_text = "\n".join(pages)

    if not full_text.strip():
        raise ValueError("Crawled pages are empty")

    chunks = chunk_text(full_text)

    if not chunks:
        raise ValueError("No text chunks found")

    index, stored_chunks = build_faiss_index(chunks)
    return index, stored_chunks

url = st.text_input("Enter Website URL")

if st.button("Crawl & Build Knowledge Base"):
    if not url:
        st.warning("Please enter a valid URL")
    else:
        with st.spinner("Crawling website and building knowledge base..."):
            index, chunks = build_knowledge_base(url)
            st.session_state.index = index
            st.session_state.chunks = chunks
            st.success("Knowledge base built successfully!")

question = st.text_input("Ask a question about the website")

if st.button("Ask"):
    if "index" not in st.session_state:
        st.warning("Please crawl a website first")
    else:
        retrieved = retrieve_chunks(
            question,
            st.session_state.index,
            st.session_state.chunks
        )
        answer = generate_answer(question, "\n".join(retrieved))
        st.write(answer)
