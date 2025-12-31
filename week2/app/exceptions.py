"""Custom exceptions for the application.

This module defines application-specific exceptions with clear error messages.
"""
from __future__ import annotations

from fastapi import HTTPException, status


class NoteNotFoundError(HTTPException):
    """Raised when a note is not found in the database."""

    def __init__(self, note_id: int):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Note with id {note_id} not found"
        )


class ActionItemNotFoundError(HTTPException):
    """Raised when an action item is not found in the database."""

    def __init__(self, action_item_id: int):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Action item with id {action_item_id} not found"
        )


class EmptyContentError(HTTPException):
    """Raised when required content is empty or missing."""

    def __init__(self, field_name: str = "content"):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"{field_name} is required and cannot be empty"
        )


class ExtractionError(HTTPException):
    """Raised when action item extraction fails."""

    def __init__(self, message: str = "Failed to extract action items"):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=message
        )
