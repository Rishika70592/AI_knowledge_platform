from typing import Any


class MCPToolAdapter:

    def __init__(
        self,
        client,
        tool_name: str,
    ):
        self.client = client
        self.tool_name = tool_name

    async def execute(
        self,
        **arguments: Any,
    ):
        return await self.client.call_tool(
            self.tool_name,
            arguments,
        )
