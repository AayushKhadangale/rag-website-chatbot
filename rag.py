import os
import openai
import numpy as np

openai.api_key = os.environ.get("OPENAI_API_KEY")

def retrieve_chunks(query, index, chunks, k=3):
    embedding = openai.Embedding.create(
        model="text-embedding-ada-002",
        input=query
    )["data"][0]["embedding"]

    query_vector = np.array([embedding]).astype("float32")
    distances, indices = index.search(query_vector, k)

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

    return response["choices"][0]["message"]["content"]

