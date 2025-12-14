import openai
import os

openai.api_key = os.environ.get("OPENAI_API_KEY")

def retrieve_chunks(index, chunks, query, top_k=5):
    from sentence_transformers import SentenceTransformer
    model = SentenceTransformer("all-MiniLM-L6-v2")

    query_embedding = model.encode([query])
    distances, indices = index.search(query_embedding, top_k)

    return [chunks[i] for i in indices[0]]

def generate_answer(question, context):
    prompt = f"""
Answer the question using the context below.

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

    return response.choices[0].message["content"]

