import streamlit as st

from crawler import crawl_website
from preprocess import chunk_text
from vector_store import build_faiss_index
from rag import retrieve_chunks, generate_answer


st.set_page_config(page_title="Website RAG Chatbot")


# -------------------------------
# STEP 3.2 — CACHE HEAVY FUNCTION
# -------------------------------
@st.cache_resource(show_spinner=True)
def build_knowledge_base(url):
    pages = crawl_website(url)

    # FIX: pages is a LIST → convert to single string
    full_text = "\n".join(pages)

    chunks = chunk_text(full_text)
    index, stored_chunks = build_faiss_index(chunks)

    return index, stored_chunks


# -------------------------------
# UI
# -------------------------------
st.title("🌐 Website RAG Chatbot")

url = st.text_input("Enter Website URL")

if st.button("Crawl & Build Knowledge Base"):
    if not url.startswith("http"):
        st.warning("Please enter a valid URL")
    else:
        with st.spinner("Crawling website and building knowledge base..."):
            index, stored_chunks = build_knowledge_base(url)

            st.session_state.index = index
            st.session_state.chunks = stored_chunks

            st.success("Knowledge base built successfully!")


question = st.text_input("Ask a question about the website")

if st.button("Ask"):
    if "index" not in st.session_state:
        st.warning("Please crawl a website first")
    else:
        retrieved_chunks = retrieve_chunks(
            question,
            st.session_state.index,
            st.session_state.chunks
        )

        answer = generate_answer(
            question,
            "\n".join(retrieved_chunks)
        )

        st.write("### Answer")
        st.write(answer)

