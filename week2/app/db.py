"""Database layer for SQLite operations.

This module provides database connection management and CRUD operations
for notes and action items tables.
"""
from __future__ import annotations

import sqlite3
from contextlib import contextmanager
from typing import Generator, List, Optional

from .config import get_settings


# ============================================================
# Connection Management
# ============================================================

def _ensure_data_directory() -> None:
    """Create data directory if it doesn't exist."""
    settings = get_settings()
    settings.data_dir.mkdir(parents=True, exist_ok=True)


@contextmanager
def get_connection() -> Generator[sqlite3.Connection, None, None]:
    """Context manager for database connections.

    Yields:
        A SQLite connection with Row factory enabled.

    Example:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM notes")
    """
    _ensure_data_directory()
    settings = get_settings()
    connection = sqlite3.connect(settings.db_path)
    connection.row_factory = sqlite3.Row
    try:
        yield connection
    finally:
        connection.close()


# ============================================================
# Database Initialization
# ============================================================

def init_db() -> None:
    """Initialize the database schema.

    Creates the notes and action_items tables if they don't exist.
    """
    _ensure_data_directory()
    with get_connection() as connection:
        cursor = connection.cursor()

        # Create notes table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS notes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                content TEXT NOT NULL,
                created_at TEXT DEFAULT (datetime('now'))
            )
        """)

        # Create action_items table with foreign key
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS action_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                note_id INTEGER,
                text TEXT NOT NULL,
                done INTEGER DEFAULT 0,
                created_at TEXT DEFAULT (datetime('now')),
                FOREIGN KEY (note_id) REFERENCES notes(id) ON DELETE CASCADE
            )
        """)

        connection.commit()


# ============================================================
# Note Operations
# ============================================================

def insert_note(content: str) -> int:
    """Insert a new note into the database.

    Args:
        content: The note content text.

    Returns:
        The ID of the newly created note.
    """
    with get_connection() as connection:
        cursor = connection.cursor()
        cursor.execute("INSERT INTO notes (content) VALUES (?)", (content,))
        connection.commit()
        return int(cursor.lastrowid)


def get_note(note_id: int) -> Optional[sqlite3.Row]:
    """Retrieve a single note by ID.

    Args:
        note_id: The ID of the note to retrieve.

    Returns:
        The note row if found, None otherwise.
    """
    with get_connection() as connection:
        cursor = connection.cursor()
        cursor.execute(
            "SELECT id, content, created_at FROM notes WHERE id = ?",
            (note_id,),
        )
        return cursor.fetchone()


def list_notes() -> List[sqlite3.Row]:
    """Retrieve all notes ordered by ID descending.

    Returns:
        List of note rows.
    """
    with get_connection() as connection:
        cursor = connection.cursor()
        cursor.execute(
            "SELECT id, content, created_at FROM notes ORDER BY id DESC"
        )
        return list(cursor.fetchall())


# ============================================================
# Action Item Operations
# ============================================================

def insert_action_items(items: List[str], note_id: Optional[int] = None) -> List[int]:
    """Insert multiple action items into the database.

    Args:
        items: List of action item text strings.
        note_id: Optional note ID to associate the items with.

    Returns:
        List of IDs for the newly created action items.
    """
    with get_connection() as connection:
        cursor = connection.cursor()
        ids: List[int] = []

        for item in items:
            cursor.execute(
                "INSERT INTO action_items (note_id, text) VALUES (?, ?)",
                (note_id, item),
            )
            ids.append(int(cursor.lastrowid))

        connection.commit()
        return ids


def list_action_items(note_id: Optional[int] = None) -> List[sqlite3.Row]:
    """Retrieve action items, optionally filtered by note ID.

    Args:
        note_id: Optional note ID to filter by.

    Returns:
        List of action item rows.
    """
    with get_connection() as connection:
        cursor = connection.cursor()

        if note_id is None:
            cursor.execute(
                "SELECT id, note_id, text, done, created_at "
                "FROM action_items ORDER BY id DESC"
            )
        else:
            cursor.execute(
                "SELECT id, note_id, text, done, created_at "
                "FROM action_items WHERE note_id = ? ORDER BY id DESC",
                (note_id,),
            )

        return list(cursor.fetchall())


def get_action_item(action_item_id: int) -> Optional[sqlite3.Row]:
    """Retrieve a single action item by ID.

    Args:
        action_item_id: The ID of the action item to retrieve.

    Returns:
        The action item row if found, None otherwise.
    """
    with get_connection() as connection:
        cursor = connection.cursor()
        cursor.execute(
            "SELECT id, note_id, text, done, created_at "
            "FROM action_items WHERE id = ?",
            (action_item_id,),
        )
        return cursor.fetchone()


def mark_action_item_done(action_item_id: int, done: bool) -> bool:
    """Mark an action item as done or not done.

    Args:
        action_item_id: The ID of the action item to update.
        done: Whether the item is done.

    Returns:
        True if the item was updated, False if not found.
    """
    with get_connection() as connection:
        cursor = connection.cursor()
        cursor.execute(
            "UPDATE action_items SET done = ? WHERE id = ?",
            (1 if done else 0, action_item_id),
        )
        connection.commit()
        return cursor.rowcount > 0
