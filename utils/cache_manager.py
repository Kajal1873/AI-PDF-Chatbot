import os

from utils.embeddings import create_embeddings
from utils.vector_store import (
    create_vector_store,
    save_vector_store,
    load_vector_store,
    save_chunks,
    load_chunks,
)


def load_or_create_pdf_cache(filename, chunks):

    faiss_path = os.path.join("indexes", filename + ".faiss")
    chunk_path = os.path.join("chunks", filename + ".pkl")

    if os.path.exists(faiss_path) and os.path.exists(chunk_path):

        index = load_vector_store(filename)
        chunks = load_chunks(filename)

    else:

        embeddings = create_embeddings(chunks)

        index = create_vector_store(embeddings)

        save_vector_store(index, filename)
        save_chunks(chunks, filename)

    return index, chunks
