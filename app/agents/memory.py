from typing import Any, Dict, List, Optional


class MemoryManager:

    def __init__(self, max_items: int = 50):
        self.max_items = max_items
        self.items: List[Dict[str, Any]] = []

    def add(
        self,
        memory_type: str,
        content: Any,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> None:

        item = {
            "type": memory_type,
            "content": content,
            "metadata": metadata or {},
        }

        self.items.append(item)

        if len(self.items) > self.max_items:
            self.items = self.items[-self.max_items:]

    def get_all(self) -> List[Dict[str, Any]]:
        return self.items.copy()

    def get_by_type(
        self,
        memory_type: str,
    ) -> List[Dict[str, Any]]:

        return [
            item
            for item in self.items
            if item["type"] == memory_type
        ]

    def get_recent(
        self,
        limit: int = 10,
    ) -> List[Dict[str, Any]]:

        return self.items[-limit:]

    def clear(self) -> None:
        self.items.clear()
