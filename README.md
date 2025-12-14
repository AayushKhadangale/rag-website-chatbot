# Website RAG Chatbot

This project is a Retrieval-Augmented Generation (RAG) chatbot that can answer questions based on the content of any website URL.

## Features
- Crawls a website (up to limited depth)
- Cleans and chunks text
- Builds FAISS vector index
- Uses OpenAI embeddings + LLM for Q&A
- Built with Streamlit

## How to Run
1. Enter a website URL
2. Click "Crawl & Build Knowledge Base"
3. Ask questions about the website

## Tech Stack
- Python
- Streamlit
- FAISS
- OpenAI API
- BeautifulSoup
