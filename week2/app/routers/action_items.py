"""Action Items API router.

This module provides endpoints for extracting and managing action items.
"""
from __future__ import annotations

from typing import List

from fastapi import APIRouter

from .. import db
from ..exceptions import ActionItemNotFoundError
from ..schemas import (
    ActionItemDetailResponse,
    ActionItemResponse,
    ExtractRequest,
    ExtractResponse,
    MarkDoneRequest,
    MarkDoneResponse,
)
from ..services.extract import extract_action_items


router = APIRouter(prefix="/action-items", tags=["action-items"])


@router.post("/extract", response_model=ExtractResponse)
def extract(payload: ExtractRequest) -> ExtractResponse:
    """Extract action items from text using heuristics.

    Args:
        payload: The extraction request with text and optional save_note flag.

    Returns:
        The extracted action items with optional note ID.
    """
    text = payload.text.strip()
    note_id = None

    if payload.save_note:
        note_id = db.insert_note(text)

    items = extract_action_items(text)
    ids = db.insert_action_items(items, note_id=note_id)

    return ExtractResponse(
        note_id=note_id,
        items=[
            ActionItemResponse(id=item_id, text=item_text)
            for item_id, item_text in zip(ids, items)
        ],
    )


@router.get("", response_model=List[ActionItemDetailResponse])
def list_all(note_id: int = None) -> List[ActionItemDetailResponse]:
    """Retrieve all action items, optionally filtered by note ID.

    Args:
        note_id: Optional note ID to filter action items.

    Returns:
        List of action items with full details.
    """
    rows = db.list_action_items(note_id=note_id)
    return [
        ActionItemDetailResponse(
            id=row["id"],
            note_id=row["note_id"],
            text=row["text"],
            done=bool(row["done"]),
            created_at=row["created_at"],
        )
        for row in rows
    ]


@router.post("/{action_item_id}/done", response_model=MarkDoneResponse)
def mark_done(action_item_id: int, payload: MarkDoneRequest) -> MarkDoneResponse:
    """Mark an action item as done or not done.

    Args:
        action_item_id: The ID of the action item to update.
        payload: The request with done status.

    Returns:
        The updated action item status.

    Raises:
        ActionItemNotFoundError: If the action item is not found.
    """
    success = db.mark_action_item_done(action_item_id, payload.done)
    if not success:
        raise ActionItemNotFoundError(action_item_id)
    return MarkDoneResponse(id=action_item_id, done=payload.done)
