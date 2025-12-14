from sentence_transformers import SentenceTransformer
import numpy as np

model = SentenceTransformer("all-MiniLM-L6-v2")

def retrieve_chunks(query, index, chunks, k=5):
    query_embedding = model.encode([query]).astype("float32")
    _, indices = index.search(query_embedding, k)
    return [chunks[i] for i in indices[0]]

def generate_answer(question, context):
    if not context.strip():
        return "No relevant information found."

    return f"""
Answer based on website content:

{context[:1500]}

(This answer is generated locally without OpenAI.)
"""
