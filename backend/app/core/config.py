import os
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    PROJECT_NAME: str = "AI-Powered Personalized Learning Path Recommender"
    VERSION: str = "0.1.0"
    API_V1_STR: str = "/api/v1"
    
    # SQLite default, easily overridable via DATABASE_URL env var (e.g. postgresql://user:pass@host/db)
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./learning_recommender.db")
    ECHO_SQL: bool = False

    # Phase 5: LLM Conversational Assistant Settings
    GEMINI_API_KEY: str | None = os.getenv("GEMINI_API_KEY", None)
    LLM_MODEL: str = os.getenv("LLM_MODEL", "gemini-1.5-flash")
    LLM_TEMPERATURE: float = float(os.getenv("LLM_TEMPERATURE", "0.2"))

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True,
        extra="ignore"
    )

settings = Settings()
