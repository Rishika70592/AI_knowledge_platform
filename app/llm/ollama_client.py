import httpx
from typing import Optional, Any


class OllamaClient:

    def __init__(
        self,
        base_url: str = "http://localhost:11434",
        model: str = "llama3.2:3b",
        timeout: float = 1000.0,
    ):
        self.base_url = base_url.rstrip("/")
        self.model = model
        self.timeout = timeout

    async def generate(
        self,
        prompt: str,
        system: Optional[str] = None,
        temperature: float = 0.2,
    ) -> str:

        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": temperature,
            },
        }

        if system:
            payload["system"] = system

        async with httpx.AsyncClient(
            timeout=self.timeout
        ) as client:

            response = await client.post(
                f"{self.base_url}/api/generate",
                json=payload,
            )

            response.raise_for_status()

            data = response.json()

            return data.get(
                "response",
                ""
            ).strip()

    async def chat(
        self,
        messages: list[dict[str, Any]],
        tools: Optional[list[dict[str, Any]]] = None,
        temperature: float = 0.2,
    ) -> dict[str, Any]:

        payload = {
            "model": self.model,
            "messages": messages,
            "stream": False,
            "options": {
                "temperature": temperature,
            },
        }

        if tools:
            payload["tools"] = tools

        async with httpx.AsyncClient(
            timeout=self.timeout
        ) as client:

            response = await client.post(
                f"{self.base_url}/api/chat",
                json=payload,
            )

            response.raise_for_status()

            return response.json()

    async def health(self) -> bool:

        try:

            async with httpx.AsyncClient(
                timeout=5
            ) as client:

                response = await client.get(
                    f"{self.base_url}/api/tags"
                )

                return response.status_code == 200

        except Exception:

            return False
