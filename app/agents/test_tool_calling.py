import asyncio

from app.agents.tool_agent import ToolCallingAgent
from app.agents.tools import ToolRegistry

from app.mcp.client import MCPClient
from app.mcp.register_tools import register_filesystem_tools

from app.llm.ollama_client import OllamaClient


async def main():

    print("Starting MCP Tool Calling test...")

    # -------------------------------------------------
    # 1. Create ToolRegistry
    # -------------------------------------------------

    registry = ToolRegistry()

    # -------------------------------------------------
    # 2. Create Filesystem MCP Client
    # -------------------------------------------------

    filesystem_client = MCPClient(
        command="python",
        args=[
            "-m",
            "app.mcp.filesystem_server",
        ],
    )

    try:

        # -------------------------------------------------
        # 3. Connect to MCP server
        # -------------------------------------------------

        print("\nConnecting to Filesystem MCP server...")

        await filesystem_client.connect()

        print("MCP connected.")

        # -------------------------------------------------
        # 4. Register MCP tools
        # -------------------------------------------------

        print("\nRegistering MCP tools...")

        await register_filesystem_tools(
            tool_registry=registry,
            client=filesystem_client,
        )

        # -------------------------------------------------
        # 5. Show registered tools
        # -------------------------------------------------

        print("\nRegistered tools:")

        for tool in registry.list_tools():
            print(
                f"- {tool.name}: "
                f"{tool.description}"
            )

        # -------------------------------------------------
        # 6. Create LLM
        # -------------------------------------------------

        llm = OllamaClient()

        # -------------------------------------------------
        # 7. Create ToolCallingAgent
        # -------------------------------------------------

        agent = ToolCallingAgent(
            llm=llm,
            tool_registry=registry,
            max_steps=3,
        )

        # -------------------------------------------------
        # 8. Ask question
        # -------------------------------------------------

        question = (
            "Read mcp_test.txt and tell me "
            "exactly what it contains."
        )

        print("\nUser question:")
        print(question)

        # -------------------------------------------------
        # 9. Run agent
        # -------------------------------------------------

        print("\nRunning ToolCallingAgent...")

        answer = await agent.run(
            question=question
        )

        # -------------------------------------------------
        # 10. Print final answer
        # -------------------------------------------------

        print("\nFinal answer:")
        print(answer)

    finally:

        # -------------------------------------------------
        # 11. Close MCP connection
        # -------------------------------------------------

        print("\nClosing MCP connection...")

        await filesystem_client.close()

        print("Done.")


if __name__ == "__main__":
    asyncio.run(main())
