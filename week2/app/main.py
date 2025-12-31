"""FastAPI application entry point.

This module configures and runs the Action Item Extractor application.
"""
from __future__ import annotations

from contextlib import asynccontextmanager
from pathlib import Path
from typing import AsyncGenerator

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

from .config import get_settings
from .db import init_db
from .routers import action_items, notes


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Application lifespan context manager.

    Handles startup and shutdown events:
    - Startup: Initialize the database
    - Shutdown: Cleanup resources (if needed)
    """
    # Startup
    init_db()
    yield
    # Shutdown (cleanup if needed)


# Create application instance
settings = get_settings()
app = FastAPI(
    title=settings.app_name,
    description="Extract action items from notes using heuristics or LLM",
    version="1.0.0",
    lifespan=lifespan,
)


# ============================================================
# Routes
# ============================================================

@app.get("/", response_class=HTMLResponse)
def index() -> str:
    """Serve the frontend HTML page.

    Returns:
        The HTML content of the index page.
    """
    html_path = Path(__file__).resolve().parents[1] / "frontend" / "index.html"
    return html_path.read_text(encoding="utf-8")


# Include routers
app.include_router(notes.router)
app.include_router(action_items.router)


# Mount static files
static_dir = Path(__file__).resolve().parents[1] / "frontend"
app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")
