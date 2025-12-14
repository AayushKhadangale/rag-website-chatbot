import os
from openai import OpenAI
import numpy as np

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

def retrieve_chunks(query, index, chunks, k=3):
    query_embedding = client.embeddings.create(
        model="text-embedding-3-small",
        input=query
    ).data[0].embedding

    query_vector = np.array([query_embedding]).astype("float32")
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

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content

