def chunk_text(pages, chunk_size=500, overlap=100):
    """
    pages: list[str] returned by crawler
    """
    text = "\n".join(pages)   # 🔑 FIX: join list into string

    words = text.split()
    chunks = []

    for i in range(0, len(words), chunk_size - overlap):
        chunk = " ".join(words[i:i + chunk_size])
        if chunk.strip():
            chunks.append(chunk)

    return chunks

