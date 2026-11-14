import os
from pathlib import Path
from typing import List, Optional
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "AI SECURITY FASTER"
    API_V1_STR: str = "/api"
    SECRET_KEY: str = "ai-security-faster-super-secret-key-2026"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24

    # Database
    # Support PostgreSQL when provided, SQLite fallback for instant zero-dependency local runs
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./ai_security.db")

    # Frontier LLM API Keys
    ANTHROPIC_API_KEY: Optional[str] = os.getenv("ANTHROPIC_API_KEY", "")
    GEMINI_API_KEY: Optional[str] = os.getenv("GEMINI_API_KEY", "")
    
    # Models
    DEFAULT_CLAUDE_MODEL: str = "claude-3-5-sonnet-20241022"
    DEFAULT_GEMINI_MODEL: str = "gemini-1.5-flash"

    # MCP Server
    MCP_SERVER_HOST: str = "127.0.0.1"
    MCP_SERVER_PORT: int = 8765

    # Wazuh SIEM
    WAZUH_API_URL: str = os.getenv("WAZUH_API_URL", "https://127.0.0.1:55000")
    WAZUH_API_USER: str = os.getenv("WAZUH_API_USER", "wazuh")
    WAZUH_API_PASSWORD: str = os.getenv("WAZUH_API_PASSWORD", "wazuh")
    WAZUH_VERIFY_SSL: bool = False

    # Storage Paths
    BASE_DIR: Path = Path(__file__).resolve().parent.parent.parent
    SANDBOX_DIR: Path = BASE_DIR / "sandbox_data"
    KNOWLEDGE_BASE_DIR: Path = BASE_DIR / "knowledge_base"

    class Config:
        case_sensitive = True
        env_file = ".env"

settings = Settings()

# Ensure sandbox and knowledge directories exist
settings.SANDBOX_DIR.mkdir(parents=True, exist_ok=True)
settings.KNOWLEDGE_BASE_DIR.mkdir(parents=True, exist_ok=True)
