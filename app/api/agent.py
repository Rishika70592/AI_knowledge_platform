from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.llm.ollama_client import OllamaClient
from app.agents.orchestrator import AgentOrchestrator
from app.agents.tool_agent import ToolCallingAgent

from app.services.retrieval_service import RetrievalService

router = APIRouter(
    prefix="/api/v1/agents",
    tags=["AI Agents"],
)

class ToolRequest(BaseModel):
    question: str


class ToolResponse(BaseModel):
    question: str
    answer: str


class ResearchRequest(BaseModel):
    question: str


class ResearchResponse(BaseModel):
    question: str
    answer: str
    iterations: int


llm = OllamaClient(
    base_url="http://localhost:11434",
    model="llama3.2:3b",
)
retrieval_service = RetrievalService()
orchestrator = AgentOrchestrator(
    llm=llm,
    retrieval_service=retrieval_service,
    max_iterations=2,
)


@router.post(
    "/research",
    response_model=ResearchResponse,
)
async def research(
    request: ResearchRequest,
):

    if not request.question.strip():
        raise HTTPException(
            status_code=400,
            detail="Question cannot be empty.",
        )

    state = await orchestrator.run(
        request.question
    )

    return ResearchResponse(
        question=request.question,
        answer=state.final_answer or "",
        iterations=state.iteration,
    )
@router.post(
    "/tool-research",
    response_model=ToolResponse,
)
async def tool_research(
    request: ToolRequest,
):

    if not request.question.strip():

        raise HTTPException(
            status_code=400,
            detail="Question cannot be empty.",
        )
    tool_agent = ToolCallingAgent(
    llm
)
    answer = await tool_agent.run(
        request.question
    )

    return ToolResponse(
        question=request.question,
        answer=answer,
    )
