from __future__ import annotations

import os
import re
from typing import List
import json
from typing import Any
from ollama import chat
from dotenv import load_dotenv

load_dotenv()

BULLET_PREFIX_PATTERN = re.compile(r"^\s*([-*•]|\d+\.)\s+")
KEYWORD_PREFIXES = (
    "todo:",
    "action:",
    "next:",
)


def _is_action_line(line: str) -> bool:
    stripped = line.strip().lower()
    if not stripped:
        return False
    if BULLET_PREFIX_PATTERN.match(stripped):
        return True
    if any(stripped.startswith(prefix) for prefix in KEYWORD_PREFIXES):
        return True
    if "[ ]" in stripped or "[todo]" in stripped:
        return True
    return False


def extract_action_items(text: str) -> List[str]:
    lines = text.splitlines()
    extracted: List[str] = []
    for raw_line in lines:
        line = raw_line.strip()
        if not line:
            continue
        if _is_action_line(line):
            cleaned = BULLET_PREFIX_PATTERN.sub("", line)
            cleaned = cleaned.strip()
            # Trim common checkbox markers
            cleaned = cleaned.removeprefix("[ ]").strip()
            cleaned = cleaned.removeprefix("[todo]").strip()
            extracted.append(cleaned)
    # Fallback: if nothing matched, heuristically split into sentences and pick imperative-like ones
    if not extracted:
        sentences = re.split(r"(?<=[.!?])\s+", text.strip())
        for sentence in sentences:
            s = sentence.strip()
            if not s:
                continue
            if _looks_imperative(s):
                extracted.append(s)
    # Deduplicate while preserving order
    seen: set[str] = set()
    unique: List[str] = []
    for item in extracted:
        lowered = item.lower()
        if lowered in seen:
            continue
        seen.add(lowered)
        unique.append(item)
    return unique


def _looks_imperative(sentence: str) -> bool:
    words = re.findall(r"[A-Za-z']+", sentence)
    if not words:
        return False
    first = words[0]
    # Crude heuristic: treat these as imperative starters
    imperative_starters = {
        "add",
        "create",
        "implement",
        "fix",
        "update",
        "write",
        "check",
        "verify",
        "refactor",
        "document",
        "design",
        "investigate",
    }
    return first.lower() in imperative_starters


def extract_action_items_llm(text: str, model: str = "llama3.2:3b") -> List[str]:
    """Extract action items from text using an LLM.

    Uses Ollama's structured outputs to get a JSON array of action items.

    Args:
        text: The input text containing notes/tasks to extract action items from.
        model: The Ollama model to use for extraction.

    Returns:
        A list of extracted action item strings.
    """
    # Handle empty input
    if not text or not text.strip():
        return []

    # System prompt for action item extraction
    system_prompt = """You are an action item extractor. Given a text containing notes,
extract all actionable tasks and return them as a JSON array of strings.

Rules:
- Extract clear, actionable items (tasks that someone needs to do)
- Remove bullet points, checkboxes, and prefixes like "TODO:", "Action:", etc.
- Keep each action item concise but complete
- If no action items are found, return an empty array []
- Return ONLY the JSON array, no other text"""

    user_prompt = f"""Extract action items from the following text:

{text}

Return a JSON array of action item strings."""

    try:
        response = chat(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            format="json",
            options={"temperature": 0.1},
        )

        # Parse the JSON response
        content = response.message.content.strip()
        result = json.loads(content)

        # Handle different response formats
        if isinstance(result, list):
            # Direct list of strings
            return [str(item) for item in result if item]
        elif isinstance(result, dict):
            # Dict with various possible keys (action_items, actionItems, items, etc.)
            items = (
                result.get("action_items")
                or result.get("actionItems")
                or result.get("items")
                or result.get("actions")
                or result.get("tasks")
                or []
            )
            return [str(item) for item in items if item]
        else:
            return []

    except json.JSONDecodeError:
        # If JSON parsing fails, return empty list
        return []
    except Exception as e:
        # Log error and return empty list for robustness
        print(f"Error in extract_action_items_llm: {e}")
        return []
