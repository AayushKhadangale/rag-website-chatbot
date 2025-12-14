import openai
import os
from sentence_transformers import SentenceTransformer
import numpy as np

openai.api_key = os.environ.get("OPENAI_API_KEY")


def retrieve_chunks(query, index, chunks, k=3):
    model = SentenceTransformer("all-MiniLM-L6-v2")
    query_embedding = model.encode([query]).astype("float32")

    _, indices = index.search(query_embedding, k)
    return [chunks[i] for i in indices[0]]


def generate_answer(question, context):
    prompt = f"""
Answer the question using ONLY the context below.

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

    return response.choices[0].message.content

