import asyncio

from app.agents.orchestrator import AgentOrchestrator
from app.agents.tools import ToolRegistry

from app.mcp.client import MCPClient
from app.mcp.tool_adapter import MCPToolAdapter


async def register_client_tools(
    registry: ToolRegistry,
    client: MCPClient,
):
    """
    Discover tools from one MCP server
    and register them in ToolRegistry.
    """

    tools = await client.list_tools()

    for tool in tools:

        adapter = MCPToolAdapter(
            client=client,
            tool_name=tool.name,
        )

        registry.register(
            name=tool.name,
            description=tool.description or "",
            parameters=tool.input_schema,
            function=adapter.execute,
        )


async def main():

    print()
    print("=" * 60)
    print("FINAL AI AGENT TEST")
    print("=" * 60)

    # --------------------------------------------------
    # 1. Create MCP clients
    # --------------------------------------------------

    filesystem_client = MCPClient(
        command="python",
        args=[
            "-m",
            "app.mcp.filesystem_server",
        ],
    )

    github_client = MCPClient(
        command="python",
        args=[
            "-m",
            "app.mcp.github_server",
        ],
    )

    # --------------------------------------------------
    # 2. Connect MCP servers
    # --------------------------------------------------

    print("\nConnecting Filesystem MCP...")

    await filesystem_client.connect()

    print("Filesystem MCP connected.")

    print("\nConnecting GitHub MCP...")

    await github_client.connect()

    print("GitHub MCP connected.")

    # --------------------------------------------------
    # 3. Create registry
    # --------------------------------------------------

    registry = ToolRegistry()

    # --------------------------------------------------
    # 4. Register MCP tools
    # --------------------------------------------------

    print("\nRegistering MCP tools...")

    await register_client_tools(
        registry,
        filesystem_client,
    )

    await register_client_tools(
        registry,
        github_client,
    )

    print("\nRegistered tools:")

    for tool in registry.list_tools():
        print(
            f"- {tool.name}: "
            f"{tool.description}"
        )

    # --------------------------------------------------
    # 5. Create LLM
    # --------------------------------------------------

    from app.llm.ollama_client import OllamaClient

    llm = OllamaClient()

    # --------------------------------------------------
    # 6. Create retrieval service
    # --------------------------------------------------

    from app.services.retrieval_service import (
        RetrievalService,
    )

    retrieval_service = RetrievalService()

    # --------------------------------------------------
    # 7. Create orchestrator
    # --------------------------------------------------

    orchestrator = AgentOrchestrator(
        llm=llm,
        retrieval_service=retrieval_service,
        tool_registry=registry,
        max_iterations=2,
    )

    # --------------------------------------------------
    # 8. Ask the agent a question
    # --------------------------------------------------

    question = (
        "Read mcp_test.txt and tell me exactly "
        "what it contains."
    )

    print()
    print("=" * 60)
    print("USER QUESTION")
    print("=" * 60)

    print(question)

    print()
    print("Running full agent...")

    # --------------------------------------------------
    # 9. Run orchestrator
    # --------------------------------------------------

    state = await orchestrator.run(
        question=question,
        user_id=None,
    )

    # --------------------------------------------------
    # 10. Print final answer
    # --------------------------------------------------

    print()
    print("=" * 60)
    print("FINAL ANSWER")
    print("=" * 60)

    print(state.final_answer)

    # --------------------------------------------------
    # 11. Print pipeline information
    # --------------------------------------------------

    print()
    print("=" * 60)
    print("PIPELINE DEBUG")
    print("=" * 60)

    print(
        "\nPlan tasks:",
        len(state.plan.tasks)
        if state.plan
        else 0,
    )

    print(
        "Research results:",
        len(state.research_results),
    )

    print(
        "Tool results:",
        len(state.tool_results),
    )

    print(
        "Agent steps:",
        len(state.agent_steps),
    )

    if state.review:
        print(
            "Review approved:",
            state.review.approved,
        )

    # --------------------------------------------------
    # 12. Print tool results
    # --------------------------------------------------

    print()
    print("=" * 60)
    print("TOOL RESULTS")
    print("=" * 60)

    for result in state.tool_results:
        print(result)

    # --------------------------------------------------
    # 13. Close MCP connections
    # --------------------------------------------------

    print()
    print("Closing MCP connections...")

    await filesystem_client.close()
    await github_client.close()

    print("Done.")


if __name__ == "__main__":
    asyncio.run(main())
