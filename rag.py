from openai import OpenAI
import os

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

def retrieve_chunks(query, index, chunks, k=5):
    query_embedding = client.embeddings.create(
        model="text-embedding-3-small",
        input=query
    ).data[0].embedding

    import numpy as np
    D, I = index.search(np.array([query_embedding]).astype("float32"), k)
    return [chunks[i] for i in I[0]]

def generate_answer(question, context):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Answer using only the provided context."},
            {"role": "user", "content": f"Context:\n{context}\n\nQuestion:\n{question}"}
        ],
        temperature=0.2
    )

    return response.choices[0].message.content

