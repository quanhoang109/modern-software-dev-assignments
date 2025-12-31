"""Application configuration settings.

This module centralizes all configuration values using Pydantic settings
for type-safe environment variable parsing.
"""
from __future__ import annotations

from pathlib import Path
from functools import lru_cache

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Application
    app_name: str = "Action Item Extractor"
    debug: bool = False

    # Database
    base_dir: Path = Path(__file__).resolve().parents[1]
    data_dir: Path = base_dir / "data"
    db_path: Path = data_dir / "app.db"

    # LLM Settings
    default_llm_model: str = "llama3.2:3b"
    llm_temperature: float = 0.1

    class Config:
        env_prefix = "ACTION_EXTRACTOR_"
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    """Get cached application settings."""
    return Settings()
