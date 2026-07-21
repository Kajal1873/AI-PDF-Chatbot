import faiss
import numpy as np
import os
import pickle

def create_vector_store(embeddings):

    embeddings = np.array(embeddings).astype("float32")

    dimension = embeddings.shape[1]

    index = faiss.IndexFlatL2(dimension)

    index.add(embeddings)

    return index


def save_vector_store(index, filename):

    os.makedirs("indexes", exist_ok=True)

    path = os.path.join("indexes", filename + ".faiss")

    faiss.write_index(index, path)

def load_vector_store(filename):

    path = os.path.join("indexes", filename + ".faiss")

    return faiss.read_index(path)

def save_chunks(chunks, filename):

    os.makedirs("chunks", exist_ok=True)

    path = os.path.join("chunks", filename + ".pkl")

    with open(path, "wb") as file:

        pickle.dump(chunks, file)

def load_chunks(filename):

    path = os.path.join("chunks", filename + ".pkl")

    with open(path, "rb") as file:

        return pickle.load(file)