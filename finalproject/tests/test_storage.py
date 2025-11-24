"""Unit tests for task_manager.py storage operations."""

import pytest
from pathlib import Path
import json
import tempfile
from datetime import datetime, timezone

from task_manager import add_task, complete_task, edit_task, delete_task, clear_tasks


@pytest.fixture
def temp_store():
    """Create a temporary tasks.json file for testing."""
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
        temp_path = Path(f.name)
    yield temp_path
    # Cleanup
    if temp_path.exists():
        temp_path.unlink()


class TestJSONStorage:
    def test_creates_file_on_first_add(self, temp_store):
        """Verify file is created when adding first task."""
        if temp_store.exists():
            temp_store.unlink()
        
        add_task(temp_store, title="First Task")
        assert temp_store.exists()

    def test_stores_valid_json(self, temp_store):
        """Verify stored data is valid JSON."""
        add_task(temp_store, title="Task 1")
        add_task(temp_store, title="Task 2")
        
        with temp_store.open() as f:
            data = json.load(f)
        
        assert isinstance(data, list)
        assert len(data) == 2

    def test_stores_all_required_fields(self, temp_store):
        """Verify all required fields are stored."""
        task = add_task(
            temp_store,
            title="Complete Task",
            description="Full description",
            due_date="2025-12-31",
            priority=1
        )
        
        with temp_store.open() as f:
            data = json.load(f)
        
        stored_task = data[0]
        assert stored_task["id"] == task["id"]
        assert stored_task["title"] == "Complete Task"
        assert stored_task["description"] == "Full description"
        assert stored_task["due_date"] == "2025-12-31"
        assert stored_task["priority"] == 1
        assert stored_task["status"] == "pending"
        assert "created_at" in stored_task

    def test_persists_across_operations(self, temp_store):
        """Verify data persists after multiple operations."""
        task1 = add_task(temp_store, title="Task 1", priority=2)
        task2 = add_task(temp_store, title="Task 2", priority=3)
        task3 = add_task(temp_store, title="Task 3", priority=1)
        
        # Verify all three are stored
        with temp_store.open() as f:
            data = json.load(f)
        assert len(data) == 3
        
        # Complete one
        complete_task(temp_store, task2["id"])
        
        # Verify all still present with correct status
        with temp_store.open() as f:
            data = json.load(f)
        assert len(data) == 3
        assert data[1]["status"] == "complete"
        assert data[0]["status"] == "pending"
        assert data[2]["status"] == "pending"

    def test_json_format_is_readable(self, temp_store):
        """Verify JSON is formatted with indentation for readability."""
        add_task(temp_store, title="Test Task")
        
        content = temp_store.read_text()
        # Should have newlines and indentation
        assert "\n" in content
        assert "  " in content or "\t" in content


class TestDataIntegrity:
    def test_id_uniqueness(self, temp_store):
        """Verify IDs are unique and incrementing."""
        ids = set()
        for i in range(10):
            task = add_task(temp_store, title=f"Task {i}")
            assert task["id"] not in ids, f"Duplicate ID: {task['id']}"
            ids.add(task["id"])
        
        # IDs should be sequential
        assert ids == set(range(1, 11))

    def test_task_order_preserved(self, temp_store):
        """Verify tasks maintain insertion order in storage."""
        titles = ["First", "Second", "Third", "Fourth"]
        for title in titles:
            add_task(temp_store, title=title)
        
        with temp_store.open() as f:
            data = json.load(f)
        
        stored_titles = [t["title"] for t in data]
        assert stored_titles == titles

    def test_null_values_stored_correctly(self, temp_store):
        """Verify null/None values are stored as JSON null."""
        add_task(temp_store, title="No Due Date", due_date=None, priority=3)
        
        with temp_store.open() as f:
            data = json.load(f)
        
        assert data[0]["due_date"] is None

    def test_empty_strings_stored_correctly(self, temp_store):
        """Verify empty strings are preserved."""
        add_task(temp_store, title="Minimal Task", description="", priority=3)
        
        with temp_store.open() as f:
            data = json.load(f)
        
        assert data[0]["description"] == ""

    def test_special_characters_in_strings(self, temp_store):
        """Verify special characters are properly escaped and stored."""
        special_text = 'Test "quotes" and \\backslash\\ and \nnewline'
        add_task(temp_store, title=special_text, description=special_text)
        
        with temp_store.open() as f:
            data = json.load(f)
        
        assert data[0]["title"] == special_text
        assert data[0]["description"] == special_text


class TestStorageUpdates:
    def test_complete_updates_storage(self, temp_store):
        """Verify completing task updates JSON file."""
        task = add_task(temp_store, title="To Complete")
        
        complete_task(temp_store, task["id"])
        
        with temp_store.open() as f:
            data = json.load(f)
        
        assert data[0]["status"] == "complete"

    def test_edit_updates_storage(self, temp_store):
        """Verify editing task updates JSON file."""
        task = add_task(temp_store, title="Original", description="Old")
        
        edit_task(temp_store, task["id"], title="Updated", description="New")
        
        with temp_store.open() as f:
            data = json.load(f)
        
        assert data[0]["title"] == "Updated"
        assert data[0]["description"] == "New"

    def test_delete_removes_from_storage(self, temp_store):
        """Verify deleting task removes it from JSON file."""
        task1 = add_task(temp_store, title="Keep")
        task2 = add_task(temp_store, title="Delete")
        task3 = add_task(temp_store, title="Also Keep")
        
        delete_task(temp_store, task2["id"])
        
        with temp_store.open() as f:
            data = json.load(f)
        
        assert len(data) == 2
        ids = [t["id"] for t in data]
        assert task2["id"] not in ids
        assert task1["id"] in ids
        assert task3["id"] in ids

    def test_clear_empties_storage(self, temp_store):
        """Verify clearing tasks results in empty array."""
        add_task(temp_store, title="Task 1")
        add_task(temp_store, title="Task 2")
        add_task(temp_store, title="Task 3")
        
        clear_tasks(temp_store)
        
        with temp_store.open() as f:
            data = json.load(f)
        
        assert data == []


class TestStorageEdgeCases:
    def test_handles_missing_file(self, temp_store):
        """Verify operations work when file doesn't exist yet."""
        if temp_store.exists():
            temp_store.unlink()
        
        # Should not crash, should create file
        task = add_task(temp_store, title="First")
        assert task["id"] == 1
        assert temp_store.exists()

    def test_handles_empty_file(self, temp_store):
        """Verify operations work with empty file."""
        temp_store.write_text("")
        
        task = add_task(temp_store, title="First After Empty")
        assert task["id"] == 1

    def test_handles_corrupted_json(self, temp_store):
        """Verify graceful handling of invalid JSON."""
        temp_store.write_text("{ invalid json }")
        
        # Should treat as empty and start fresh
        task = add_task(temp_store, title="After Corruption")
        assert task["id"] == 1

    def test_handles_json_object_instead_of_array(self, temp_store):
        """Verify graceful handling of wrong JSON structure."""
        temp_store.write_text('{"wrong": "structure"}')
        
        # Should treat as empty and start fresh
        task = add_task(temp_store, title="After Wrong Structure")
        assert task["id"] == 1

    def test_concurrent_id_generation(self, temp_store):
        """Verify ID generation works correctly with existing tasks."""
        # Manually create a task with high ID
        data = [
            {"id": 5, "title": "Manual Task", "status": "pending", "priority": 3, "created_at": "2025-11-22T00:00:00"}
        ]
        with temp_store.open('w') as f:
            json.dump(data, f)
        
        # Next task should get ID 6
        task = add_task(temp_store, title="Next Task")
        assert task["id"] == 6


class TestTimestampStorage:
    def test_created_at_is_stored(self, temp_store):
        """Verify created_at timestamp is stored."""
        task = add_task(temp_store, title="Timestamped Task")
        
        with temp_store.open() as f:
            data = json.load(f)
        
        assert "created_at" in data[0]
        assert data[0]["created_at"] == task["created_at"]

    def test_created_at_format_is_iso8601(self, temp_store):
        """Verify timestamp follows ISO 8601 format."""
        task = add_task(temp_store, title="Task")
        
        # Should be parseable as ISO format
        timestamp = task["created_at"]
        # Will raise ValueError if not valid ISO format
        parsed = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
        assert isinstance(parsed, datetime)

    def test_timestamps_are_chronological(self, temp_store):
        """Verify timestamps increase with each task."""
        task1 = add_task(temp_store, title="First")
        task2 = add_task(temp_store, title="Second")
        task3 = add_task(temp_store, title="Third")
        
        t1 = datetime.fromisoformat(task1["created_at"].replace('Z', '+00:00'))
        t2 = datetime.fromisoformat(task2["created_at"].replace('Z', '+00:00'))
        t3 = datetime.fromisoformat(task3["created_at"].replace('Z', '+00:00'))
        
        assert t1 <= t2 <= t3
