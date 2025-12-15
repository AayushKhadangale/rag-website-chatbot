import os
import requests
import numpy as np
from sentence_transformers import SentenceTransformer
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
MODEL = "meta-llama/llama-3-8b-instruct"
embedder = SentenceTransformer("all-MiniLM-L6-v2")
def retrieve_chunks(question, index, chunks, k=5):
   q_embedding = embedder.encode([question]).astype("float32")
   distances, indices = index.search(q_embedding, k)
   return [chunks[i] for i in indices[0]]
def generate_answer(question, context_chunks):
   context = "\n\n".join(context_chunks)
   payload = {
       "model": MODEL,
       "messages": [
           {
               "role": "user",
               "content": f"""
Answer ONLY using the context below.
If not present, say you don't know.
Context:
{context}
Question:
{question}
"""
           }
       ],
       "temperature": 0.3
   }
   headers = {
       "Authorization": f"Bearer {OPENROUTER_API_KEY}",
       "Content-Type": "application/json"
   }
   res = requests.post(
       "https://openrouter.ai/api/v1/chat/completions",
       headers=headers,
       json=payload,
       timeout=30
   )
   res.raise_for_status()
   return res.json()["choices"][0]["message"]["content"]
