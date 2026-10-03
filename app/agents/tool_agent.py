import json

from app.agents.base import BaseAgent
from app.agents.tools import ToolRegistry


class ToolCallingAgent(BaseAgent):

    def __init__(
        self,
        llm,
        tool_registry: ToolRegistry,
        max_steps: int = 3,
    ):
        super().__init__(
            "tool_calling_agent",
            llm,
        )

        self.tool_registry = tool_registry
        self.max_steps = max_steps

    @staticmethod
    def _parse_arguments(arguments):

        if arguments is None:
            return {}

        if isinstance(arguments, dict):
            return arguments

        if isinstance(arguments, str):

            try:
                return json.loads(arguments)

            except json.JSONDecodeError:
                return {}

        return {}

    async def run(self, question: str):

        messages = [
            {
                "role": "system",
                "content": """
You are a research assistant with access to MCP tools.

Your job is to answer the user's question accurately.

Rules:
- Use tools when additional information is required.
- Use filesystem tools when the user asks about files.
- Use GitHub tools when the user asks about GitHub repositories.
- Use PostgreSQL tools when the user asks about database structure.
- Never invent tool results.
- Analyze tool results before answering.
- You may call multiple tools when necessary.
- When enough information is available, provide the final answer.
- Do not mention internal tool execution unless useful.
""",
            },
            {
                "role": "user",
                "content": question,
            },
        ]

        tools = self.tool_registry.get_openai_tools()

        if not tools:
            return ""

        for step in range(self.max_steps):

            response = await self.llm.chat(
                messages=messages,
                tools=tools,
                temperature=0.1,
            )

            message = response.get(
                "message",
                {},
            )

            tool_calls = message.get(
                "tool_calls"
            )

            # ----------------------------------------------
            # Final answer
            # ----------------------------------------------

            if not tool_calls:

                return (
                    message.get(
                        "content",
                        "",
                    )
                    or ""
                ).strip()

            # ----------------------------------------------
            # Preserve assistant message
            # ----------------------------------------------

            messages.append(message)

            # ----------------------------------------------
            # Execute MCP tools
            # ----------------------------------------------

            for tool_call in tool_calls:

                function = tool_call.get(
                    "function",
                    {},
                )

                tool_name = function.get(
                    "name"
                )

                arguments = self._parse_arguments(
                    function.get(
                        "arguments",
                        {},
                    )
                )

                try:

                    tool_result = (
                        await self.tool_registry.execute(
                            name=tool_name,
                            arguments=arguments,
                        )
                    )

                    result = {
                        "success": True,
                        "tool": tool_name,
                        "result": tool_result,
                    }

                except Exception as exc:

                    result = {
                        "success": False,
                        "tool": tool_name,
                        "error": str(exc),
                    }

                # ------------------------------------------
                # Return tool result to Ollama
                # ------------------------------------------

                messages.append(
                    {
                        "role": "tool",
                        "tool_call_id": tool_call.get(
                            "id"
                        ),
                        "content": json.dumps(
                            result,
                            default=str,
                        ),
                    }
                )

        return (
            "The tool execution limit was reached "
            "before the research could be completed."
        )
