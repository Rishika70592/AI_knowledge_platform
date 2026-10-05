import asyncio
from app.services.keyword_search import keyword_search

async def main():
    results = await keyword_search("Krishna Daripa")
    for r in results:
        print(f"\n[Page {r['page_number']}] score={r['score']:.4f}")
        print(r['content'][:200])

asyncio.run(main())