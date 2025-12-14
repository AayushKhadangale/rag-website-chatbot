import os
import openai
import numpy as np
from sentence_transformers import SentenceTransformer

# Load OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Embedding model (same as vector store)
embedder = SentenceTransformer("all-MiniLM-L6-v2")

def retrieve_chunks(question, index, chunks, top_k=3):
    """
    Retrieve top-k relevant chunks using FAISS
    """
    question_embedding = embedder.encode([question]).astype("float32")
    distances, indices = index.search(question_embedding, top_k)

    return [chunks[i] for i in indices[0]]

def generate_answer(question, context):
    """
    Generate final answer using OpenAI
    """
    if not openai.api_key:
        raise ValueError("OPENAI_API_KEY not found in environment")

    prompt = f"""
Use the context below to answer the question clearly.

Context:
{context}

Question:
{question}
"""

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.2
    )

    return response["choices"][0]["message"]["content"]

