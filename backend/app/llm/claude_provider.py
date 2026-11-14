import time
from typing import List, Dict, Any, AsyncGenerator, Optional
import anthropic
from app.llm.provider_interface import BaseLLMProvider
from app.core.config import settings

class ClaudeProvider(BaseLLMProvider):
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or settings.ANTHROPIC_API_KEY
        self.client = None
        if self.api_key:
            try:
                self.client = anthropic.AsyncAnthropic(api_key=self.api_key)
            except Exception as e:
                print(f"[ClaudeProvider] Initialization warning: {e}")

    async def validate_connection(self) -> Dict[str, Any]:
        if not self.api_key or not self.client:
            return {
                "status": "unconfigured",
                "message": "Anthropic API key is not configured. Set ANTHROPIC_API_KEY in .env or Settings.",
                "latency_ms": 0.0,
                "provider": "claude"
            }
        start_time = time.time()
        try:
            # Lightweight verification ping using Claude 3 Haiku
            response = await self.client.messages.create(
                model="claude-3-haiku-20240307",
                max_tokens=5,
                messages=[{"role": "user", "content": "ping"}]
            )
            latency = (time.time() - start_time) * 1000
            return {
                "status": "connected",
                "message": "Successfully connected to Anthropic Claude Messages API",
                "latency_ms": round(latency, 2),
                "provider": "claude"
            }
        except anthropic.AuthenticationError as e:
            return {
                "status": "error",
                "message": f"Authentication failed: {str(e)}",
                "latency_ms": (time.time() - start_time) * 1000,
                "provider": "claude"
            }
        except Exception as e:
            return {
                "status": "error",
                "message": f"Connection error: {str(e)}",
                "latency_ms": (time.time() - start_time) * 1000,
                "provider": "claude"
            }

    async def generate_completion(
        self,
        messages: List[Dict[str, str]],
        model_name: Optional[str] = None,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 2048,
    ) -> Dict[str, Any]:
        target_model = model_name or settings.DEFAULT_CLAUDE_MODEL
        
        # If no client or API key, provide a diagnostic fallback explaining configuration
        if not self.client or not self.api_key:
            return {
                "content": f"[Claude Provider Unconfigured] ANTHROPIC_API_KEY is not set. Please configure your key in Settings or .env to enable live Claude 3.5 responses.\n\n(Simulated baseline for '{target_model}': Prompt received with {len(messages)} message(s)).",
                "tokens_used": 42,
                "latency_ms": 85.0,
                "model_name": target_model,
                "provider": "claude",
                "is_simulated": True
            }

        start_time = time.time()
        # Format messages for Anthropic (role must be 'user' or 'assistant')
        anthropic_messages = []
        for m in messages:
            role = m.get("role", "user")
            if role in ["user", "assistant"]:
                anthropic_messages.append({"role": role, "content": m.get("content", "")})
        
        kwargs: Dict[str, Any] = {
            "model": target_model,
            "messages": anthropic_messages,
            "max_tokens": max_tokens,
            "temperature": temperature,
        }
        if system_prompt:
            kwargs["system"] = system_prompt

        try:
            response = await self.client.messages.create(**kwargs)
            latency = (time.time() - start_time) * 1000
            
            # Extract text
            content_text = ""
            for block in response.content:
                if hasattr(block, "text"):
                    content_text += block.text

            tokens_used = (response.usage.input_tokens if response.usage else 0) + \
                          (response.usage.output_tokens if response.usage else 0)

            return {
                "content": content_text,
                "tokens_used": tokens_used,
                "latency_ms": round(latency, 2),
                "model_name": target_model,
                "provider": "claude",
                "is_simulated": False
            }
        except Exception as e:
            latency = (time.time() - start_time) * 1000
            return {
                "content": f"Claude API Error: {str(e)}",
                "tokens_used": 0,
                "latency_ms": round(latency, 2),
                "model_name": target_model,
                "provider": "claude",
                "error": str(e),
                "is_simulated": False
            }

    async def generate_stream(
        self,
        messages: List[Dict[str, str]],
        model_name: Optional[str] = None,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 2048,
    ) -> AsyncGenerator[str, None]:
        target_model = model_name or settings.DEFAULT_CLAUDE_MODEL

        if not self.client or not self.api_key:
            chunks = [
                "[Claude Provider Notice: ANTHROPIC_API_KEY is not configured in environment.]\n",
                "To interact with live Claude 3.5 Sonnet, configure your key in Settings.\n",
                f"Echoed prompt: {messages[-1].get('content', '') if messages else ''}"
            ]
            for chunk in chunks:
                yield chunk
            return

        anthropic_messages = []
        for m in messages:
            role = m.get("role", "user")
            if role in ["user", "assistant"]:
                anthropic_messages.append({"role": role, "content": m.get("content", "")})

        kwargs: Dict[str, Any] = {
            "model": target_model,
            "messages": anthropic_messages,
            "max_tokens": max_tokens,
            "temperature": temperature,
        }
        if system_prompt:
            kwargs["system"] = system_prompt

        try:
            async with self.client.messages.stream(**kwargs) as stream:
                async for text in stream.text_stream:
                    yield text
        except Exception as e:
            yield f"\n[Stream Error: {str(e)}]"
