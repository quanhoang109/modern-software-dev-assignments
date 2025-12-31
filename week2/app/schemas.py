"""Pydantic schemas for API request/response validation.

This module defines well-typed data models for all API endpoints,
replacing raw Dict[str, Any] with structured Pydantic models.
"""
from __future__ import annotations

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field


# ============================================================
# Note Schemas
# ============================================================

class NoteCreate(BaseModel):
    """Request schema for creating a new note."""
    content: str = Field(..., min_length=1, description="The note content text")


class NoteResponse(BaseModel):
    """Response schema for a note."""
    id: int
    content: str
    created_at: str


class NoteListResponse(BaseModel):
    """Response schema for listing notes."""
    notes: List[NoteResponse]


# ============================================================
# Action Item Schemas
# ============================================================

class ActionItemResponse(BaseModel):
    """Response schema for an action item."""
    id: int
    text: str


class ActionItemDetailResponse(BaseModel):
    """Detailed response schema for an action item."""
    id: int
    note_id: Optional[int]
    text: str
    done: bool
    created_at: str


class ExtractRequest(BaseModel):
    """Request schema for extracting action items."""
    text: str = Field(..., min_length=1, description="Text to extract action items from")
    save_note: bool = Field(default=False, description="Whether to save the text as a note")


class ExtractResponse(BaseModel):
    """Response schema for action item extraction."""
    note_id: Optional[int]
    items: List[ActionItemResponse]


class ExtractLLMRequest(BaseModel):
    """Request schema for LLM-powered action item extraction."""
    text: str = Field(..., min_length=1, description="Text to extract action items from")
    save_note: bool = Field(default=False, description="Whether to save the text as a note")
    model: str = Field(default="llama3.2:3b", description="Ollama model to use")


class MarkDoneRequest(BaseModel):
    """Request schema for marking an action item as done."""
    done: bool = Field(default=True, description="Whether the item is done")


class MarkDoneResponse(BaseModel):
    """Response schema for marking an action item as done."""
    id: int
    done: bool
