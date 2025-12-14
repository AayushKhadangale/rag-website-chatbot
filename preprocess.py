def chunk_text(pages, chunk_size=500, overlap=100):
    chunks = []

    for page in pages:
        words = page.split()
        for i in range(0, len(words), chunk_size - overlap):
            chunk = " ".join(words[i:i + chunk_size])
            chunks.append(chunk)

    return chunks

