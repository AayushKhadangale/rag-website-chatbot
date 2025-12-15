import streamlit as st
from crawler import crawl_website
from preprocess import chunk_text
from vector_store import build_faiss_index
from rag import retrieve_chunks, generate_answer
st.set_page_config("Website RAG Chatbot")
st.title("🌐Bajaj Finserv Chatbot")
@st.cache_resource(show_spinner=True)
def build_kb(url):
   pages = crawl_website(url)
   if not pages:
       raise ValueError("No pages crawled")
   full_text = "\n".join(pages)
   chunks = chunk_text(full_text)
   index, stored_chunks = build_faiss_index(chunks)
   return index, stored_chunks
url = st.text_input("Enter website URL")
if st.button("Crawl & Build Knowledge Base"):
   try:
       index, chunks = build_kb(url)
       st.session_state.index = index
       st.session_state.chunks = chunks
       st.success("Knowledge base ready!")
   except Exception as e:
       st.error(str(e))
question = st.text_input("Ask a question")
if st.button("Ask"):
   if "index" not in st.session_state:
       st.warning("Please crawl a website first")
   else:
       with st.spinner("Thinking..."):
           retrieved = retrieve_chunks(
               question,
               st.session_state.index,
               st.session_state.chunks
           )
           answer = generate_answer(question, retrieved)
           st.write(answer)
