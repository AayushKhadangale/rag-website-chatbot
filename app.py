import streamlit as st
from crawler import crawl_website
from preprocess import chunk_text
from vector_store import build_faiss_index
from rag import retrieve_chunks, generate_answer

st.set_page_config(page_title="Website RAG Chatbot")

st.title("🌐 Website RAG Chatbot")

# URL input
url = st.text_input("Enter Website URL")

# Crawl button
if st.button("Crawl & Build Knowledge Base"):
    if not url:
        st.error("Please enter a valid URL")
    else:
        with st.spinner("Crawling website and building knowledge base..."):
            pages = crawl_website(url)
            full_text = " ".join(pages)

            chunks = chunk_text(full_text)

            # ✅ FIXED LINE (ONLY 2 VALUES)
            index, stored_chunks = build_faiss_index(chunks)

            # ✅ STORE IN SESSION STATE
            st.session_state.index = index
            st.session_state.chunks = stored_chunks

        st.success("Knowledge Base Built Successfully!")

# Question input
question = st.text_input("Ask a question about the website")

if st.button("Ask"):
    if "index" not in st.session_state or "chunks" not in st.session_state:
        st.error("Please crawl a website first.")
    else:
        retrieved_chunks = retrieve_chunks(
            question,
            st.session_state.index,
            st.session_state.chunks
        )

        answer = generate_answer(question, "\n".join(retrieved_chunks))
        st.write(answer)

