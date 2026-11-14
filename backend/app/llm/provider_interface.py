from abc import ABC, abstractmethod
from typing import List, Dict, Any, AsyncGenerator, Optional

class BaseLLMProvider(ABC):
    @abstractmethod
    async def generate_completion(
        self,
        messages: List[Dict[str, str]],
        model_name: Optional[str] = None,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 2048,
    ) -> Dict[str, Any]:
        """
        Generate a non-streaming completion.
        Returns dict with:
        - content: str
        - tokens_used: int
        - latency_ms: float
        - model_name: str
        """
        pass

    @abstractmethod
    async def generate_stream(
        self,
        messages: List[Dict[str, str]],
        model_name: Optional[str] = None,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 2048,
    ) -> AsyncGenerator[str, None]:
        """
        Stream completion chunks.
        """
        pass

    @abstractmethod
    async def validate_connection(self) -> Dict[str, Any]:
        """
        Check if API key is present and validate connection.
        Returns:
        - status: 'connected' | 'unconfigured' | 'error'
        - message: str
        - latency_ms: float
        """
        pass
