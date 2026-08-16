from app.services.extraction import extract_text_by_page
from app.services.cleaning import clean_text
from app.services.chunking import chunk_text
from app.services.embeddings import embed_texts
from app.models import Document, Chunk
from app.db.db import AsyncSessionLocal

async def ingest_document(filename: str, file_bytes: bytes):
    async with AsyncSessionLocal() as session:
        document = Document(filename=filename, status="processing")
        session.add(document)
        await session.flush()

        pages = extract_text_by_page(file_bytes)
        document.num_pages = len(pages)

        all_chunks = []
        for page in pages:
            cleaned = clean_text(page["text"])
            if not cleaned:
                continue
            for c in chunk_text(cleaned):
                all_chunks.append({"content": c, "page_number": page["page_number"]})

        embeddings = await embed_texts([c["content"] for c in all_chunks])

        for idx, (chunk_data, vector) in enumerate(zip(all_chunks, embeddings)):
            session.add(Chunk(
                document_id=document.id,
                content=chunk_data["content"],
                chunk_index=idx,
                page_number=chunk_data["page_number"],
                embedding=vector,
            ))

        document.status = "ready"
        await session.commit()

        class Result:
            id = document.id
            status = document.status
            chunk_count = len(all_chunks)
        return Result()