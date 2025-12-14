import os
import openai

# Load API key from environment (Streamlit Secrets)
openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_answer(question, context):
    if not openai.api_key:
        raise ValueError("OPENAI_API_KEY not found in environment")

    prompt = f"""
Use the context below to answer the question clearly and concisely.

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

