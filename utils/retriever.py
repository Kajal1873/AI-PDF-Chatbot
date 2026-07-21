from utils.embeddings import model
from utils.hybrid_search import bm25_search, reciprocal_rank_fusion
from utils.reranker import rerank

def retrieve_chunks(question, index, bm25, chunks, top_k):

    # ---------- Semantic Search (FAISS) ----------
    query_embedding = model.encode([question])

    _, faiss_indices = index.search(query_embedding, top_k)

    # ---------- Keyword Search (BM25) ----------
    

    bm25_indices = bm25_search(question, bm25, chunks, top_k)

    
    # ---------- Reciprocal Rank Fusion ----------
    faiss_results = [i for i in faiss_indices[0] if i >= 0]

    merged_indices = reciprocal_rank_fusion(
        faiss_results,
        bm25_indices
    )

    merged_indices = merged_indices[:top_k]
    # ---------- Build Context ----------
    context = []
    sources = []

    seen_chunks = set()
    seen_sources = set()

    for i in merged_indices:

        if i >= len(chunks):
            continue

        text = chunks[i]["text"]

        if text in seen_chunks:
            continue

        seen_chunks.add(text)
        context.append(text)

        source = {
            "pdf": chunks[i]["pdf"],
            "page": chunks[i]["page"]
        }

        key = (source["pdf"], source["page"])

        if key not in seen_sources:
            seen_sources.add(key)
            sources.append(source)

    return "\n\n".join(context), sources