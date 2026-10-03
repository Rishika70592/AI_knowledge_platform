from app.services.retrieval_service import RetrievalService

from app.agents.tools import ToolRegistry
from app.agents.tool_functions import KnowledgeBaseTools


tool_registry = ToolRegistry()


retrieval_service = RetrievalService()


knowledge_tools = KnowledgeBaseTools(
    retrieval_service=retrieval_service,
)


tool_registry.register(
    name="search_knowledge_base",
    description=(
        "Search the user's knowledge base for "
        "relevant documents and information."
    ),
    parameters={
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": "The search query.",
            },
            "top_k": {
                "type": "integer",
                "description": "Maximum number of results.",
                "default": 5,
            },
        },
        "required": ["query"],
    },
    function=knowledge_tools.search_knowledge_base,
)
