import json
from typing import Any

from app.agents.base import BaseAgent
from app.agents.tools import ToolRegistry
from app.schemas.agent import AgentStep, ToolResult


class ReActAgent(BaseAgent):

    def __init__(
        self,
        llm,
        tools: ToolRegistry,
        max_steps: int = 4,
    ):
        super().__init__("react_agent", llm)

        self.tools = tools
        self.max_steps = max_steps

    def _build_tool_description(self) -> str:

        tools = self.tools.schemas()

        if not tools:
            return "No tools are available."

        return json.dumps(
            tools,
            indent=2,
        )

    @staticmethod
    def _clean_json(response: str) -> str:

        response = response.strip()

        if response.startswith("```json"):
            response = response[7:].strip()

        elif response.startswith("```"):
            response = response[3:].strip()

        if response.endswith("```"):
            response = response[:-3].strip()

        return response

    async def run(self, state):

        tool_description = self._build_tool_description()

        history = []

        for step_number in range(
            1,
            self.max_steps + 1,
        ):

            prompt = f"""
You are an agent that can reason and use tools.

User question:
{state.question}

Previous observations:
{json.dumps(history, indent=2)}

Available tools:
{tool_description}

Choose exactly ONE action.

Return ONLY JSON.

If you need a tool:

{{
  "action": "tool",
  "tool_name": "tool_name",
  "arguments": {{}}
}}

If you can answer:

{{
  "action": "final",
  "answer": "final answer"
}}

Rules:
- Never invent tool results.
- Use a tool when information is needed.
- Use the previous observations.
- Stop when enough information is available.
"""

            response = await self.llm.generate(
                prompt=prompt,
                temperature=0.0,
            )

            try:
                data = json.loads(
                    self._clean_json(response)
                )

            except json.JSONDecodeError:

                state.agent_steps.append(
                    AgentStep(
                        step_number=step_number,
                        agent=self.name,
                        action="invalid_output",
                        input=response,
                    )
                )

                break

            action = data.get("action")

            if action == "final":

                answer = data.get(
                    "answer",
                    "",
                )

                state.final_answer = answer

                state.agent_steps.append(
                    AgentStep(
                        step_number=step_number,
                        agent=self.name,
                        action="final",
                        output=answer,
                    )
                )

                return state

            if action != "tool":

                state.agent_steps.append(
                    AgentStep(
                        step_number=step_number,
                        agent=self.name,
                        action="invalid_action",
                        output=data,
                    )
                )

                break

            tool_name = data.get(
                "tool_name"
            )

            arguments = data.get(
                "arguments",
                {},
            )

            try:

                result = await self.tools.execute(
                    tool_name,
                    arguments,
                )

                tool_result = ToolResult(
                    tool_name=tool_name,
                    success=True,
                    result=result,
                )

            except Exception as exc:

                tool_result = ToolResult(
                    tool_name=tool_name,
                    success=False,
                    error=str(exc),
                )

            state.tool_results.append(
                tool_result
            )

            history.append(
                {
                    "tool": tool_name,
                    "arguments": arguments,
                    "result": (
                        tool_result.result
                        if tool_result.success
                        else tool_result.error
                    ),
                }
            )

            state.agent_steps.append(
                AgentStep(
                    step_number=step_number,
                    agent=self.name,
                    action="tool",
                    input={
                        "tool_name": tool_name,
                        "arguments": arguments,
                    },
                    output=(
                        tool_result.result
                        if tool_result.success
                        else tool_result.error
                    ),
                )
            )

        return state
