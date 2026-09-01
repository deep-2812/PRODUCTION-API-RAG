"""
Centralized Configuration
Uses pydantic-settings for validated environment variables.
"""

import os
from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):

    # LLM Configuration
    google_api_key: str
    anthropic_api_key: str
    primary_model: str = "gemini-3.6-flash"
    fallback_model: str = "claude-haiku-4-5"

    # LangSmith
    langchain_tracing_v2: bool = True
    langchain_api_key: str = ""
    langchain_project: str = "production-api-rag"

    # Application
    app_env: str = "development"
    log_level: str = "INFO"
    rate_limit: str = "20/minute"
    cache_ttl_seconds: int = 300
    max_retries: int = 3

    model_config = {"env_file": ".env", "extra": "ignore"}

    def model_post_init(self, __context) -> None:
        """Sync loaded settings to os.environ for LangChain and LangSmith."""
        if self.langchain_tracing_v2:
            os.environ["LANGCHAIN_TRACING_V2"] = "true"
            os.environ["LANGSMITH_TRACING"] = "true"
        if self.langchain_api_key:
            os.environ["LANGCHAIN_API_KEY"] = self.langchain_api_key
            os.environ["LANGSMITH_API_KEY"] = self.langchain_api_key
        if self.langchain_project:
            os.environ["LANGCHAIN_PROJECT"] = self.langchain_project
            os.environ["LANGSMITH_PROJECT"] = self.langchain_project
        if self.google_api_key:
            os.environ["GOOGLE_API_KEY"] = self.google_api_key
        if self.anthropic_api_key:
            os.environ["ANTHROPIC_API_KEY"] = self.anthropic_api_key

    @property
    def is_production(self) -> bool:
        return self.app_env == "production"


@lru_cache()
def get_settings() -> Settings:
    """Cached settings instance - loaded once, reused everywhere."""
    return Settings()