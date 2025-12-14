def chunk_text(text, chunk_size=500, overlap=100):
    words = text.split()
    chunks = []

    for i in range(0, len(words), chunk_size - overlap):
        chunk = " ".join(words[i:i + chunk_size])
        chunks.append(chunk)

    return chunks


def chunk_pages(pages):
    all_chunks = []

    for page in pages:
        page_chunks = chunk_text(page)
        all_chunks.extend(page_chunks)

    return all_chunks

