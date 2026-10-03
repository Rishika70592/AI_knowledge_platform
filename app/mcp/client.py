from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


class MCPClient:

    def __init__(
        self,
        command: str,
        args: list[str],
    ):
        self.server_params = StdioServerParameters(
            command=command,
            args=args,
        )

        self._stdio = None
        self._session = None

    async def connect(self):

        self._stdio = stdio_client(
            self.server_params
        )

        read, write = await self._stdio.__aenter__()

        self._session = ClientSession(
            read,
            write,
        )

        await self._session.__aenter__()

        await self._session.initialize()

    async def list_tools(self):

        if self._session is None:
            raise RuntimeError(
                "MCP client is not connected."
            )

        result = await self._session.list_tools()

        return result.tools

    async def call_tool(
        self,
        name: str,
        arguments: dict,
    ):

        if self._session is None:
            raise RuntimeError(
                "MCP client is not connected."
            )

        return await self._session.call_tool(
            name,
            arguments,
        )

    async def close(self):

        if self._session is not None:
            await self._session.__aexit__(
                None,
                None,
                None,
            )

        if self._stdio is not None:
            await self._stdio.__aexit__(
                None,
                None,
                None,
            )
