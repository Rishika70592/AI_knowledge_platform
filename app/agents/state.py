from dataclasses import dataclass, field
from typing import Any


@dataclass
class AgentState:

    question: str

    user_id: str | None = None

    plan: Any = None

    memory: list[dict] = field(
        default_factory=list
    )

    research_results: list[Any] = field(
        default_factory=list
    )

    tool_results: list[Any] = field(
        default_factory=list
    )

    agent_steps: list[Any] = field(
        default_factory=list
    )

    draft: str = ""

    final_answer: str = ""

    review: Any = None

    iteration: int = 0
