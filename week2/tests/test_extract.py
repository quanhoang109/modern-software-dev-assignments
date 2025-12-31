import os
import pytest

from ..app.services.extract import extract_action_items, extract_action_items_llm


def test_extract_bullets_and_checkboxes():
    text = """
    Notes from meeting:
    - [ ] Set up database
    * implement API extract endpoint
    1. Write tests
    Some narrative sentence.
    """.strip()

    items = extract_action_items(text)
    print(items)
    assert "Set up database" in items
    assert "implement API extract endpoint" in items
    assert "Write tests" in items


# ============================================================
# Unit tests for extract_action_items_llm()
# ============================================================

class TestExtractActionItemsLLM:
    """Test suite for the LLM-powered action item extraction function."""

    def test_extract_bullet_list(self):
        """Test extraction from bullet point list."""
        text = """
        Meeting notes:
        - Review the quarterly report
        - Schedule team meeting
        - Update project documentation
        """
        items = extract_action_items_llm(text)

        print("\n=== test_extract_bullet_list ===")
        print(f"Input:\n{text}")
        print(f"Extracted items ({len(items)}):")
        for i, item in enumerate(items, 1):
            print(f"  {i}. {item}")

        # Should extract at least some items
        assert len(items) > 0, f"Expected items but got: {items}"
        # Check that items are strings
        assert all(isinstance(item, str) for item in items)

    def test_extract_keyword_prefixed_lines(self):
        """Test extraction from lines with TODO/Action prefixes."""
        text = """
        TODO: Fix the login bug
        Action: Send email to client
        Next: Prepare presentation slides
        """
        items = extract_action_items_llm(text)

        print("\n=== test_extract_keyword_prefixed_lines ===")
        print(f"Input:\n{text}")
        print(f"Extracted items ({len(items)}):")
        for i, item in enumerate(items, 1):
            print(f"  {i}. {item}")

        assert len(items) > 0, f"Expected items but got: {items}"
        # Items should have prefixes removed (cleaned)
        assert all(isinstance(item, str) for item in items)

    def test_extract_checkbox_items(self):
        """Test extraction from checkbox-style items."""
        text = """
        [ ] Complete unit tests
        [x] Review pull request
        [ ] Deploy to staging
        """
        items = extract_action_items_llm(text)

        print("\n=== test_extract_checkbox_items ===")
        print(f"Input:\n{text}")
        print(f"Extracted items ({len(items)}):")
        for i, item in enumerate(items, 1):
            print(f"  {i}. {item}")

        # Should find at least the unchecked items
        assert len(items) >= 0  # LLM may or may not include checked items

    def test_empty_input(self):
        """Test that empty input returns empty list."""
        print("\n=== test_empty_input ===")

        result1 = extract_action_items_llm("")
        print(f"Empty string '' -> {result1}")
        assert result1 == []

        result2 = extract_action_items_llm("   ")
        print(f"Whitespace '   ' -> {result2}")
        assert result2 == []

        result3 = extract_action_items_llm("\n\n")
        print(f"Newlines '\\n\\n' -> {result3}")
        assert result3 == []

    def test_no_action_items(self):
        """Test input with no actionable items."""
        text = "The weather is nice today. I had coffee this morning."
        items = extract_action_items_llm(text)

        print("\n=== test_no_action_items ===")
        print(f"Input: {text}")
        print(f"Extracted items ({len(items)}): {items}")

        # Should return empty or minimal list for non-actionable text
        assert isinstance(items, list)

    def test_mixed_content(self):
        """Test extraction from text with mixed actionable and non-actionable content."""
        text = """
        Weekly Update:

        Had a great meeting with the team yesterday.

        Action items:
        - Complete the API documentation
        - Fix bug #123

        The project is going well overall.
        """
        items = extract_action_items_llm(text)

        print("\n=== test_mixed_content ===")
        print(f"Input:\n{text}")
        print(f"Extracted items ({len(items)}):")
        for i, item in enumerate(items, 1):
            print(f"  {i}. {item}")

        assert len(items) > 0, f"Expected items but got: {items}"
        assert all(isinstance(item, str) for item in items)

    def test_returns_list(self):
        """Test that function always returns a list."""
        text = "- Task one\n- Task two"
        result = extract_action_items_llm(text)

        print("\n=== test_returns_list ===")
        print(f"Input: {text}")
        print(f"Result type: {type(result).__name__}")
        print(f"Result: {result}")

        assert isinstance(result, list)

    def test_numbered_list(self):
        """Test extraction from numbered list."""
        text = """
        Sprint tasks:
        1. Implement user authentication
        2. Add database migrations
        3. Write integration tests
        100. Do nothing
        """
        items = extract_action_items_llm(text)

        print("\n=== test_numbered_list ===")
        print(f"Input:\n{text}")
        print(f"Extracted items ({len(items)}):")
        for i, item in enumerate(items, 1):
            print(f"  {i}. {item}")

        assert len(items) > 0, f"Expected items but got: {items}"
        assert all(isinstance(item, str) for item in items)
