from typing import Any, Dict, List, Optional
from uuid import uuid4

from pydantic import BaseModel, Field


class ResearchTask(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    question: str
    purpose: str
    status: str = "pending"


class Plan(BaseModel):
    original_question: str
    tasks: List[ResearchTask] = Field(default_factory=list)


class RetrievedDocument(BaseModel):
    content: str
    score: float = 0.0
    metadata: Dict[str, Any] = Field(default_factory=dict)


class ResearchResult(BaseModel):
    task_id: str
    findings: List[str] = Field(default_factory=list)
    sources: List[Dict[str, Any]] = Field(default_factory=list)
    confidence: float = 0.0


class ReviewResult(BaseModel):
    approved: bool
    score: float
    issues: List[str] = Field(default_factory=list)
    suggestions: List[str] = Field(default_factory=list)


class ToolCall(BaseModel):
    tool_name: str
    arguments: Dict[str, Any] = Field(default_factory=dict)


class ToolResult(BaseModel):
    tool_name: str
    success: bool
    result: Any = None
    error: Optional[str] = None


class AgentStep(BaseModel):
    step_number: int
    agent: str
    action: str
    input: Any = None
    output: Any = None


class AgentState(BaseModel):
    question: str

    user_id: str | None = None

    plan: Optional[Plan] = None

    research_results: List[ResearchResult] = Field(
        default_factory=list
    )

    draft: Optional[str] = None

    review: Optional[ReviewResult] = None

    final_answer: Optional[str] = None

    iteration: int = 0

    memory: List[Dict[str, Any]] = Field(
        default_factory=list
    )

    tool_results: List[ToolResult] = Field(
        default_factory=list
    )

    agent_steps: List[AgentStep] = Field(
        default_factory=list
    )

    metadata: Dict[str, Any] = Field(
        default_factory=dict
    )

