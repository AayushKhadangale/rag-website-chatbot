import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")

def build_faiss_index(chunks):
    if not chunks:
        raise ValueError("No text chunks found to build FAISS index")

    embeddings = model.encode(chunks)
    embeddings = np.array(embeddings).astype("float32")

    dim = embeddings.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(embeddings)

    return index, chunks