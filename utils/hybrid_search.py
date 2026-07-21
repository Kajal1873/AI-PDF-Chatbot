import rank_bm25

print("Imported from:", rank_bm25.__file__)

from rank_bm25 import BM25Okapi


def create_bm25(chunks):

    documents = []

    for chunk in chunks:
        documents.append(chunk["text"].split())

    return BM25Okapi(documents)


def bm25_search(question, bm25, chunks, top_k):

    tokens = question.split()

    scores = bm25.get_scores(tokens)

    ranked = sorted(
        range(len(scores)),
        key=lambda i: scores[i],
        reverse=True
    )

    return ranked[:top_k]

def reciprocal_rank_fusion(faiss_results, bm25_results, k=60):
    scores = {}

    for rank, idx in enumerate(faiss_results):
        scores[idx] = scores.get(idx, 0) + 1 / (k + rank)

    for rank, idx in enumerate(bm25_results):
        scores[idx] = scores.get(idx, 0) + 1 / (k + rank)

    ranked = sorted(
        scores.items(),
        key=lambda x: x[1],
        reverse=True
    )

    return [idx for idx, _ in ranked]