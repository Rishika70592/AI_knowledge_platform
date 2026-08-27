from app.services.search import search_chunks
from app.services.keyword_search import keyword_search

async def hybrid_search(query: str, top_k: int = 5, rrf_k: int = 60):
    vector_results = await search_chunks(query, top_k=10)
    keyword_results = await keyword_search(query, top_k=10)

    scores = {}
    content_map = {}

    for rank, chunk in enumerate(vector_results, 1):
        key = (chunk["document_id"], chunk["page_number"], chunk["content"][:50])
        scores[key] = scores.get(key, 0) + 1 / (rrf_k + rank)
        content_map[key] = chunk

    for rank, chunk in enumerate(keyword_results, 1):
        key = (chunk["document_id"], chunk["page_number"], chunk["content"][:50])
        scores[key] = scores.get(key, 0) + 1 / (rrf_k + rank)
        content_map[key] = chunk

    ranked_keys = sorted(scores.keys(), key=lambda k: scores[k], reverse=True)

    return [content_map[k] for k in ranked_keys[:top_k]]