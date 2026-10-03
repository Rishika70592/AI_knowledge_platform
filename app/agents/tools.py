from dataclasses import dataclass
from typing import Any, Callable


@dataclass
class Tool:
    name: str
    description: str
    parameters: dict
    function: Callable


class ToolRegistry:

    def __init__(self):
        self._tools: dict[str, Tool] = {}

    def register(
        self,
        name: str,
        description: str,
        parameters: dict,
        function: Callable,
    ):
        if name in self._tools:
            raise ValueError(
                f"Tool '{name}' is already registered."
            )

        self._tools[name] = Tool(
            name=name,
            description=description,
            parameters=parameters,
            function=function,
        )

    def get(self, name: str) -> Tool | None:
        return self._tools.get(name)

    def list_tools(self) -> list[Tool]:
        return list(self._tools.values())

    async def execute(
        self,
        name: str,
        arguments: dict[str, Any],
    ):
        tool = self.get(name)

        if tool is None:
            raise ValueError(
                f"Unknown tool: {name}"
            )

        result = tool.function(**arguments)

        if hasattr(result, "__await__"):
            result = await result

        return result

    def get_openai_tools(self) -> list[dict]:
        """
        Convert our internal tools into
        OpenAI-compatible tool definitions.

        Ollama supports this tool schema too.
        """

        tools = []

        for tool in self._tools.values():

            tools.append(
                {
                    "type": "function",
                    "function": {
                        "name": tool.name,
                        "description": tool.description,
                        "parameters": tool.parameters,
                    },
                }
            )

        return tools
