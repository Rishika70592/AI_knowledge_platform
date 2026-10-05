import asyncio
import json
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from app.services.hybrid_search import hybrid_search


def load_test_questions():
    with open(os.path.join(os.path.dirname(__file__), "test_questions.json"), "r") as f:
        return json.load(f)

async def evaluate_question(test_case, top_k=5):
    results = await hybrid_search(test_case["question"], top_k=top_k)
    

    combined_text = " ".join(r["content"] for r in results).lower()
    expected_terms = test_case["expected_answer_contains"]

    found_terms = [term for term in expected_terms if term.lower() in combined_text]
    recall_score = len(found_terms) / len(expected_terms)

    top_result_pages = [r["page_number"] for r in results]
    expected_page = test_case.get("expected_page")
    page_found = expected_page in top_result_pages if expected_page is not None else None
    #page_found = test_case.get("expected_page") in top_result_pages

    return {
        "id": test_case["id"],
        "question": test_case["question"],
        "recall_score": recall_score,
        "found_terms": found_terms,
        "missing_terms": [t for t in expected_terms if t not in found_terms],
        "expected_page_found": page_found,
        "top_distance": results[0].get("distance", results[0].get("score")) if results else None,
        
    }

async def main():
    test_questions = load_test_questions()
    print(f"Running evaluation on {len(test_questions)} test questions...\n")

    all_results = []
    for test_case in test_questions:
        result = await evaluate_question(test_case)
        all_results.append(result)

        status = "PASS" if result["recall_score"] >= 0.5 else "FAIL"
        print(f"[{status}] {result['id']}: {result['question']}")
        top_dist_str = f"{result['top_distance']:.4f}" if result['top_distance'] is not None else "N/A"
        print(f"    Recall: {result['recall_score']:.2f} | Page found: {result['expected_page_found']} | Top score/distance: {top_dist_str}")    
       
        if result["missing_terms"]:
            print(f"    Missing terms: {result['missing_terms']}")
        print()

    avg_recall = sum(r["recall_score"] for r in all_results) / len(all_results)
    pages_found = sum(1 for r in all_results if r["expected_page_found"])

    print("=" * 50)
    print(f"Average recall score: {avg_recall:.2f}")
    print(f"Correct page found: {pages_found}/{len(all_results)}")

if __name__ == "__main__":
    asyncio.run(main())