from typing import Dict, Any, List

MODELS_REGISTRY: Dict[str, Dict[str, Any]] = {
    "claude-3-5-sonnet-20241022": {
        "id": "claude-3-5-sonnet-20241022",
        "provider": "claude",
        "display_name": "Claude 3.5 Sonnet",
        "context_window": 200000,
        "max_output_tokens": 8192,
        "recommended": True,
        "is_vision": True,
    },
    "claude-3-haiku-20240307": {
        "id": "claude-3-haiku-20240307",
        "provider": "claude",
        "display_name": "Claude 3 Haiku",
        "context_window": 200000,
        "max_output_tokens": 4096,
        "recommended": False,
        "is_vision": True,
    },
    "claude-3-opus-20240229": {
        "id": "claude-3-opus-20240229",
        "provider": "claude",
        "display_name": "Claude 3 Opus",
        "context_window": 200000,
        "max_output_tokens": 4096,
        "recommended": False,
        "is_vision": True,
    },
    "gemini-1.5-flash": {
        "id": "gemini-1.5-flash",
        "provider": "gemini",
        "display_name": "Gemini 1.5 Flash",
        "context_window": 1000000,
        "max_output_tokens": 8192,
        "recommended": True,
        "is_vision": True,
    },
    "gemini-1.5-pro": {
        "id": "gemini-1.5-pro",
        "provider": "gemini",
        "display_name": "Gemini 1.5 Pro",
        "context_window": 2000000,
        "max_output_tokens": 8192,
        "recommended": False,
        "is_vision": True,
    },
    "gemini-2.0-flash-exp": {
        "id": "gemini-2.0-flash-exp",
        "provider": "gemini",
        "display_name": "Gemini 2.0 Flash",
        "context_window": 1000000,
        "max_output_tokens": 8192,
        "recommended": False,
        "is_vision": True,
    }
}

def get_models_by_provider(provider: str) -> List[Dict[str, Any]]:
    return [model for model in MODELS_REGISTRY.values() if model["provider"] == provider]

def get_model_info(model_name: str) -> Dict[str, Any]:
    return MODELS_REGISTRY.get(model_name, {
        "id": model_name,
        "provider": "claude" if "claude" in model_name.lower() else "gemini",
        "display_name": model_name,
        "context_window": 128000,
        "max_output_tokens": 4096,
        "recommended": False
    })
