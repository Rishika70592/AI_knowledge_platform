"""def chunk_text(text: str, chunk_size: int = 800, overlap: int = 150) -> list[str]:
    words = text.split()
    chunks = []
    start = 0
    while start < len(words):
        end = start + chunk_size
        chunk = " ".join(words[start:end])
        chunks.append(chunk)
        start += chunk_size - overlap
    return chunks"""

import nltk
nltk.download('punkt', quiet=True)
nltk.download('punkt_tab', quiet=True)
from nltk.tokenize import sent_tokenize
import numpy as np

# ======== ====================================
# LEVEL 1 — Fixed-size sliding window (original)
# ============================================
def chunk_fixed_size(text: str, chunk_size: int = 800, overlap: int = 150) -> list[str]:
    words = text.split()
    chunks = []
    start = 0
    while start < len(words):
        end = start + chunk_size
        chunk = " ".join(words[start:end])
        chunks.append(chunk)
        start += chunk_size - overlap
    return chunks


# ============================================
# LEVEL 2 — Sentence-aware chunking
# ============================================
def chunk_by_sentences(text: str, chunk_size: int = 800, overlap: int = 150) -> list[str]:
    sentences = sent_tokenize(text)
    chunks = []
    current_chunk = []
    current_length = 0

    for sentence in sentences:
        sentence_length = len(sentence.split())

        if current_length + sentence_length > chunk_size and current_chunk:
            chunks.append(" ".join(current_chunk))

            overlap_sentences = []
            overlap_length = 0
            for s in reversed(current_chunk):
                s_len = len(s.split())
                if overlap_length + s_len > overlap:
                    break
                overlap_sentences.insert(0, s)
                overlap_length += s_len

            current_chunk = overlap_sentences
            current_length = overlap_length

        current_chunk.append(sentence)
        current_length += sentence_length

    if current_chunk:
        chunks.append(" ".join(current_chunk))

    return chunks


# ============================================
# LEVEL 4 — Semantic chunking (embedding-based breakpoints)
# ============================================
def chunk_semantic(text: str, similarity_threshold: float = 0.5, min_chunk_sentences: int = 3) -> list[str]:
    from sentence_transformers import SentenceTransformer

    model = SentenceTransformer("all-MiniLM-L6-v2")
    sentences = sent_tokenize(text)

    if len(sentences) <= min_chunk_sentences:
        return [" ".join(sentences)]

    embeddings = model.encode(sentences)

    def cosine_sim(a, b):
        return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

    similarities = [
        cosine_sim(embeddings[i], embeddings[i + 1])
        for i in range(len(embeddings) - 1)
    ]

    chunks = []
    current_chunk = [sentences[0]]

    for i, sim in enumerate(similarities):
        if sim < similarity_threshold and len(current_chunk) >= min_chunk_sentences:
            chunks.append(" ".join(current_chunk))
            current_chunk = [sentences[i + 1]]
        else:
            current_chunk.append(sentences[i + 1])

    if current_chunk:
        chunks.append(" ".join(current_chunk))

    return chunks


# ============================================
# Dispatcher — chosen via config
# ============================================
def chunk_text(text: str, strategy: str = "fixed", chunk_size: int = 800, overlap: int = 150) -> list[str]:
    if strategy == "fixed":
        return chunk_fixed_size(text, chunk_size, overlap)
    elif strategy == "sentence":
        return chunk_by_sentences(text, chunk_size, overlap)
    elif strategy == "semantic":
        return chunk_semantic(text)
    else:
        raise ValueError(f"Unknown chunking strategy: {strategy}")

