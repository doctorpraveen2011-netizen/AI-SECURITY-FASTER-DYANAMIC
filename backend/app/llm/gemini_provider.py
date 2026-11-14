import time
from typing import List, Dict, Any, AsyncGenerator, Optional
from google import genai
from google.genai import types
from app.llm.provider_interface import BaseLLMProvider
from app.core.config import settings

class GeminiProvider(BaseLLMProvider):
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or settings.GEMINI_API_KEY
        self.client = None
        if self.api_key:
            try:
                self.client = genai.Client(api_key=self.api_key)
            except Exception as e:
                print(f"[GeminiProvider] Initialization warning: {e}")

    async def validate_connection(self) -> Dict[str, Any]:
        if not self.api_key or not self.client:
            return {
                "status": "unconfigured",
                "message": "Gemini API key is not configured. Set GEMINI_API_KEY in .env or Settings.",
                "latency_ms": 0.0,
                "provider": "gemini"
            }
        start_time = time.time()
        try:
            # Lightweight verification ping
            response = await self.client.aio.models.generate_content(
                model="gemini-1.5-flash",
                contents="ping",
                config=types.GenerateContentConfig(max_output_tokens=5)
            )
            latency = (time.time() - start_time) * 1000
            return {
                "status": "connected",
                "message": "Successfully connected to Google Gen AI (Gemini) API",
                "latency_ms": round(latency, 2),
                "provider": "gemini"
            }
        except Exception as e:
            return {
                "status": "error",
                "message": f"Gemini connection error: {str(e)}",
                "latency_ms": (time.time() - start_time) * 1000,
                "provider": "gemini"
            }

    async def generate_completion(
        self,
        messages: List[Dict[str, str]],
        model_name: Optional[str] = None,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 2048,
    ) -> Dict[str, Any]:
        target_model = model_name or settings.DEFAULT_GEMINI_MODEL

        if not self.client or not self.api_key:
            return {
                "content": f"[Gemini Provider Unconfigured] GEMINI_API_KEY is not set. Please configure your key in Settings or .env to enable live Gemini 1.5/2.0 responses.\n\n(Simulated baseline for '{target_model}': Prompt received with {len(messages)} message(s)).",
                "tokens_used": 38,
                "latency_ms": 72.0,
                "model_name": target_model,
                "provider": "gemini",
                "is_simulated": True
            }

        start_time = time.time()
        # Build contents from messages
        contents = []
        for m in messages:
            role = "user" if m.get("role") in ["user", "system"] else "model"
            contents.append(types.Content(
                role=role,
                parts=[types.Part.from_text(text=m.get("content", ""))]
            ))

        config = types.GenerateContentConfig(
            system_instruction=system_prompt if system_prompt else None,
            temperature=temperature,
            max_output_tokens=max_tokens
        )

        try:
            response = await self.client.aio.models.generate_content(
                model=target_model,
                contents=contents,
                config=config
            )
            latency = (time.time() - start_time) * 1000
            
            content_text = response.text or ""
            tokens_used = 0
            if hasattr(response, "usage_metadata") and response.usage_metadata:
                tokens_used = (response.usage_metadata.prompt_token_count or 0) + \
                              (response.usage_metadata.candidates_token_count or 0)

            return {
                "content": content_text,
                "tokens_used": tokens_used or 50,
                "latency_ms": round(latency, 2),
                "model_name": target_model,
                "provider": "gemini",
                "is_simulated": False
            }
        except Exception as e:
            latency = (time.time() - start_time) * 1000
            return {
                "content": f"Gemini API Error: {str(e)}",
                "tokens_used": 0,
                "latency_ms": round(latency, 2),
                "model_name": target_model,
                "provider": "gemini",
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
        target_model = model_name or settings.DEFAULT_GEMINI_MODEL

        if not self.client or not self.api_key:
            chunks = [
                "[Gemini Provider Notice: GEMINI_API_KEY is not configured in environment.]\n",
                "To interact with live Gemini models, configure your key in Settings.\n",
                f"Echoed prompt: {messages[-1].get('content', '') if messages else ''}"
            ]
            for chunk in chunks:
                yield chunk
            return

        contents = []
        for m in messages:
            role = "user" if m.get("role") in ["user", "system"] else "model"
            contents.append(types.Content(
                role=role,
                parts=[types.Part.from_text(text=m.get("content", ""))]
            ))

        config = types.GenerateContentConfig(
            system_instruction=system_prompt if system_prompt else None,
            temperature=temperature,
            max_output_tokens=max_tokens
        )

        try:
            stream = await self.client.aio.models.generate_content_stream(
                model=target_model,
                contents=contents,
                config=config
            )
            async for chunk in stream:
                if chunk.text:
                    yield chunk.text
        except Exception as e:
            yield f"\n[Gemini Stream Error: {str(e)}]"
