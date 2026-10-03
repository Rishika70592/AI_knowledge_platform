from abc import ABC, abstractmethod
from typing import Any


class BaseAgent(ABC):

    def __init__(self, name: str, llm):
        self.name = name
        self.llm = llm

    @abstractmethod
    async def run(self, state: Any) -> Any:
        pass
