from sentence_transformers import CrossEncoder

reranker = CrossEncoder(
    "cross-encoder/ms-marco-MiniLM-L-6-v2",
    trust_remote_code=True
)


def rerank(question, contexts, top_k=5):

    pairs = []

    for text in contexts:
        pairs.append([question, text])

    scores = reranker.predict(pairs)

    ranked = sorted(
        zip(contexts, scores),
        key=lambda x: x[1],
        reverse=True
    )

    return [text for text, _ in ranked[:top_k]]