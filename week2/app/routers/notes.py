"""Notes API router.

This module provides endpoints for creating and retrieving notes.
"""
from __future__ import annotations

from typing import List

from fastapi import APIRouter

from .. import db
from ..exceptions import NoteNotFoundError
from ..schemas import NoteCreate, NoteResponse, NoteListResponse


router = APIRouter(prefix="/notes", tags=["notes"])


@router.post("", response_model=NoteResponse)
def create_note(payload: NoteCreate) -> NoteResponse:
    """Create a new note.

    Args:
        payload: The note creation request with content.

    Returns:
        The created note with ID and timestamp.
    """
    note_id = db.insert_note(payload.content.strip())
    note = db.get_note(note_id)
    return NoteResponse(
        id=note["id"],
        content=note["content"],
        created_at=note["created_at"],
    )


@router.get("", response_model=NoteListResponse)
def list_all_notes() -> NoteListResponse:
    """Retrieve all notes.

    Returns:
        List of all notes ordered by ID descending.
    """
    rows = db.list_notes()
    notes = [
        NoteResponse(
            id=row["id"],
            content=row["content"],
            created_at=row["created_at"],
        )
        for row in rows
    ]
    return NoteListResponse(notes=notes)


@router.get("/{note_id}", response_model=NoteResponse)
def get_single_note(note_id: int) -> NoteResponse:
    """Retrieve a single note by ID.

    Args:
        note_id: The ID of the note to retrieve.

    Returns:
        The note with the given ID.

    Raises:
        NoteNotFoundError: If the note is not found.
    """
    row = db.get_note(note_id)
    if row is None:
        raise NoteNotFoundError(note_id)
    return NoteResponse(
        id=row["id"],
        content=row["content"],
        created_at=row["created_at"],
    )
