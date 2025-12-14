import streamlit as st
from crawler import crawl_website
from preprocess import chunk_text
from vector_store import build_faiss_index
from rag import retrieve_chunks, generate_answer

st.set_page_config(page_title="Website RAG Chatbot")

st.title("🌐 Website RAG Chatbot")

url = st.text_input("Enter Website URL")

if st.button("Crawl & Build Knowledge Base"):
    with st.spinner("Crawling website..."):
        pages = crawl_website(url)
        full_text = " ".join(pages)
        chunks = chunk_text(full_text)
        index, embeddings, stored_chunks = build_faiss_index(chunks)

        st.session_state.index = index
        st.session_state.chunks = stored_chunks

    st.success("Knowledge Base Ready!")

question = st.text_input("Ask a question about the website")

if st.button("Ask"):
    if "index" not in st.session_state:
        st.error("Please crawl a website first.")
    else:
        retrieved = retrieve_chunks(
            question,
            st.session_state.index,
            st.session_state.chunks
        )
        answer = generate_answer(question, "\n".join(retrieved))
        st.write(answer)
