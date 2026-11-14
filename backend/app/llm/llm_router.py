import asyncio
from typing import Dict, Any, List, Optional, AsyncGenerator
from app.llm.claude_provider import ClaudeProvider
from app.llm.gemini_provider import GeminiProvider
from app.core.config import settings

class LLMRouter:
    def __init__(self):
        self.claude = ClaudeProvider()
        self.gemini = GeminiProvider()

    def update_keys(self, anthropic_key: Optional[str] = None, gemini_key: Optional[str] = None):
        if anthropic_key is not None:
            settings.ANTHROPIC_API_KEY = anthropic_key
            self.claude = ClaudeProvider(api_key=anthropic_key)
        if gemini_key is not None:
            settings.GEMINI_API_KEY = gemini_key
            self.gemini = GeminiProvider(api_key=gemini_key)

    def get_provider(self, provider_name: str):
        if provider_name.lower() == "gemini":
            return self.gemini
        return self.claude

    async def get_all_provider_status(self) -> Dict[str, Any]:
        claude_status, gemini_status = await asyncio.gather(
            self.claude.validate_connection(),
            self.gemini.validate_connection()
        )
        return {
            "claude": claude_status,
            "gemini": gemini_status,
            "any_connected": claude_status["status"] == "connected" or gemini_status["status"] == "connected"
        }

    async def generate_completion(
        self,
        provider: str,
        messages: List[Dict[str, str]],
        model_name: Optional[str] = None,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 2048
    ) -> Dict[str, Any]:
        p = self.get_provider(provider)
        return await p.generate_completion(
            messages=messages,
            model_name=model_name,
            system_prompt=system_prompt,
            temperature=temperature,
            max_tokens=max_tokens
        )

    async def generate_stream(
        self,
        provider: str,
        messages: List[Dict[str, str]],
        model_name: Optional[str] = None,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 2048
    ) -> AsyncGenerator[str, None]:
        p = self.get_provider(provider)
        async for chunk in p.generate_stream(
            messages=messages,
            model_name=model_name,
            system_prompt=system_prompt,
            temperature=temperature,
            max_tokens=max_tokens
        ):
            yield chunk

    async def side_by_side_comparison(
        self,
        prompt: str,
        claude_model: str = "claude-3-5-sonnet-20241022",
        gemini_model: str = "gemini-1.5-flash",
        system_prompt: Optional[str] = None
    ) -> Dict[str, Any]:
        messages = [{"role": "user", "content": prompt}]
        
        claude_task = self.claude.generate_completion(
            messages=messages,
            model_name=claude_model,
            system_prompt=system_prompt
        )
        gemini_task = self.gemini.generate_completion(
            messages=messages,
            model_name=gemini_model,
            system_prompt=system_prompt
        )
        
        claude_res, gemini_res = await asyncio.gather(claude_task, gemini_task)
        
        return {
            "claude": claude_res,
            "gemini": gemini_res,
            "latency_delta_ms": round(claude_res["latency_ms"] - gemini_res["latency_ms"], 2),
            "tokens_total": claude_res["tokens_used"] + gemini_res["tokens_used"]
        }

llm_router = LLMRouter()
