from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")  # 384

async def embed_texts(texts: list[str]) -> list[list[float]]:
    embeddings = model.encode(texts, convert_to_numpy=True)
    return embeddings.tolist()