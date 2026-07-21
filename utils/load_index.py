import faiss
import pickle

def load_index():
    index = faiss.read_index("data/index.faiss")

    with open("data/chunks.pkl", "rb") as f:
        chunks = pickle.load(f)

    return index, chunks