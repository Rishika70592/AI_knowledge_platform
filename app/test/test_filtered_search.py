import asyncio
from app.services.search import search_chunks

async def main():
    doc_id = "84c08692-cbf1-4175-bfb7-f8c4ec535a71"

    print("=== Filtered to one document ===")
    results = await search_chunks("What is Robozonix", top_k=3, document_id=doc_id)
    for r in results:
        print(f"[Page {r['page_number']}] {r['content'][:100]}")

    print("\n=== Unfiltered (all documents) ===")
    results = await search_chunks("What is Robozonix", top_k=3)
    for r in results:
        print(f"[Page {r['page_number']}] {r['content'][:100]}")

asyncio.run(main())