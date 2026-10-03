import json
from typing import Any

from app.agents.base import BaseAgent
from app.schemas.agent import ReviewResult


class ReviewerAgent(BaseAgent):

    def __init__(self, llm):
        super().__init__("reviewer", llm)

    @staticmethod
    def _clean_json_response(response: str) -> str:
        """
        Remove common Markdown code fences from LLM JSON output.
        """
        response = response.strip()

        if response.startswith("```json"):
            response = response[len("```json"):].strip()

        elif response.startswith("```"):
            response = response[len("```"):].strip()

        if response.endswith("```"):
            response = response[:-3].strip()

        return response

    @staticmethod
    def _normalize_string_list(value: Any, key: str) -> list[str]:
        """
        Convert LLM output into list[str].

        Handles:
            ["some issue"]

        and:

            [{"issue": "some issue"}]

        and:

            "some issue"

        """
        if value is None:
            return []

        if not isinstance(value, list):
            value = [value]

        result = []

        for item in value:

            if isinstance(item, str):
                text = item.strip()

                if text:
                    result.append(text)

            elif isinstance(item, dict):
                text = item.get(key)

                if text is None:
                    # Fallback for unexpected dictionary structure
                    text = item.get("text")

                if text is None:
                    text = item.get("description")

                if text is not None:
                    text = str(text).strip()

                    if text:
                        result.append(text)

            else:
                text = str(item).strip()

                if text:
                    result.append(text)

        return result

    @staticmethod
    def _normalize_score(value: Any) -> float:
        """
        Safely convert score to a float between 0 and 1.
        """
        try:
            score = float(value)
        except (TypeError, ValueError):
            return 0.0

        return max(0.0, min(1.0, score))

    @staticmethod
    def _normalize_bool(value: Any) -> bool:
        """
        Safely convert common LLM boolean representations.
        """
        if isinstance(value, bool):
            return value

        if isinstance(value, str):
            return value.strip().lower() in {
                "true",
                "1",
                "yes",
                "approved",
            }

        if isinstance(value, (int, float)):
            return bool(value)

        return False

    async def run(self, state):

        # Nothing to review
        if not state.draft:
            return state

        prompt = f"""
You are a strict answer reviewer.

Your job is to review the draft answer against the question and research.

Question:
{state.question}

Draft:
{state.draft}

Research:
{state.research_results}

Review the draft for:

1. Factual support
2. Completeness
3. Relevance
4. Clarity
5. Unsupported claims

Return ONLY valid JSON.

Required format:

{{
  "approved": true,
  "score": 0.85,
  "issues": [],
  "suggestions": []
}}

Strict output rules:

- "approved" MUST be a boolean.
- "score" MUST be a number between 0 and 1.
- "issues" MUST be an array of strings.
- "suggestions" MUST be an array of strings.
- Do NOT put objects inside "issues".
- Do NOT put objects inside "suggestions".
- Do NOT include Markdown.
- Do NOT include ```json.
- Do NOT include any text before or after the JSON.
- Approve only when the answer is sufficiently supported by the research.
- If there are unsupported claims, list them in "issues".
- If the answer needs improvement, list concrete improvements in "suggestions".
"""

        try:
            response = await self.llm.generate(
                prompt=prompt,
                temperature=0.0,
            )

        except Exception as exc:
            # Do not let an LLM failure crash the whole API request.
            state.review = ReviewResult(
                approved=False,
                score=0.0,
                issues=[
                    f"Reviewer LLM failed: {str(exc)}"
                ],
                suggestions=[
                    "Retry the review."
                ],
            )

            return state

        # ---------------------------------------------------------
        # Parse LLM response
        # ---------------------------------------------------------

        try:
            cleaned_response = self._clean_json_response(response)

            data = json.loads(cleaned_response)

            if not isinstance(data, dict):
                raise ValueError("Reviewer response must be a JSON object.")

        except (json.JSONDecodeError, ValueError, TypeError):

            state.review = ReviewResult(
                approved=False,
                score=0.0,
                issues=[
                    "Reviewer returned invalid JSON."
                ],
                suggestions=[
                    "Retry the review with a valid JSON response."
                ],
            )

            return state

        # ---------------------------------------------------------
        # Normalize reviewer output
        # ---------------------------------------------------------

        approved = self._normalize_bool(
            data.get("approved", False)
        )

        score = self._normalize_score(
            data.get("score", 0.0)
        )

        issues = self._normalize_string_list(
            data.get("issues", []),
            key="issue",
        )

        suggestions = self._normalize_string_list(
            data.get("suggestions", []),
            key="suggestion",
        )

        # ---------------------------------------------------------
        # Create validated ReviewResult
        # ---------------------------------------------------------

        state.review = ReviewResult(
            approved=approved,
            score=score,
            issues=issues,
            suggestions=suggestions,
        )

        return state
