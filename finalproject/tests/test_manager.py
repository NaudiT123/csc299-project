"""Unit tests for task_manager.py core functions."""

import pytest
from pathlib import Path
import json
import tempfile
from datetime import datetime

from task_manager import (
    add_task,
    list_tasks,
    complete_task,
    delete_task,
    edit_task,
    set_priority,
    clear_tasks,
    search_tasks,
)


@pytest.fixture
def temp_store():
    """Create a temporary tasks.json file for testing."""
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
        temp_path = Path(f.name)
    yield temp_path
    # Cleanup
    if temp_path.exists():
        temp_path.unlink()


class TestAddTask:
    def test_add_basic_task(self, temp_store):
        task = add_task(temp_store, title="Test Task", description="Test description")
        assert task["id"] == 1
        assert task["title"] == "Test Task"
        assert task["description"] == "Test description"
        assert task["status"] == "pending"
        assert task["priority"] == 3

    def test_add_task_with_priority(self, temp_store):
        task = add_task(temp_store, title="High Priority", priority=1)
        assert task["priority"] == 1

    def test_add_task_with_due_date(self, temp_store):
        task = add_task(temp_store, title="Deadline Task", due_date="2025-12-31")
        assert task["due_date"] == "2025-12-31"

    def test_add_task_invalid_priority(self, temp_store):
        task = add_task(temp_store, title="Bad Priority", priority=10)
        assert task["priority"] == 3  # Should default to 3

    def test_add_task_invalid_date(self, temp_store):
        task = add_task(temp_store, title="Bad Date", due_date="invalid-date")
        assert task["due_date"] is None

    def test_add_multiple_tasks_increments_id(self, temp_store):
        task1 = add_task(temp_store, title="First")
        task2 = add_task(temp_store, title="Second")
        task3 = add_task(temp_store, title="Third")
        assert task1["id"] == 1
        assert task2["id"] == 2
        assert task3["id"] == 3


class TestListTasks:
    def test_list_empty_store(self, temp_store):
        tasks = list_tasks(temp_store)
        assert tasks == []

    def test_list_all_tasks(self, temp_store):
        add_task(temp_store, title="Task 1")
        add_task(temp_store, title="Task 2")
        add_task(temp_store, title="Task 3")
        tasks = list_tasks(temp_store, filter_mode="all")
        assert len(tasks) == 3

    def test_list_pending_tasks(self, temp_store):
        add_task(temp_store, title="Task 1")
        task2 = add_task(temp_store, title="Task 2")
        add_task(temp_store, title="Task 3")
        complete_task(temp_store, task2["id"])
        
        pending = list_tasks(temp_store, filter_mode="pending")
        assert len(pending) == 2

    def test_list_completed_tasks(self, temp_store):
        task1 = add_task(temp_store, title="Task 1")
        add_task(temp_store, title="Task 2")
        task3 = add_task(temp_store, title="Task 3")
        complete_task(temp_store, task1["id"])
        complete_task(temp_store, task3["id"])
        
        completed = list_tasks(temp_store, filter_mode="completed")
        assert len(completed) == 2

    def test_list_sorted_by_priority(self, temp_store):
        add_task(temp_store, title="Low", priority=5)
        add_task(temp_store, title="High", priority=1)
        add_task(temp_store, title="Medium", priority=3)
        
        tasks = list_tasks(temp_store, sort_mode="priority")
        assert tasks[0]["priority"] == 1
        assert tasks[1]["priority"] == 3
        assert tasks[2]["priority"] == 5

    def test_list_sorted_by_due_date(self, temp_store):
        add_task(temp_store, title="Later", due_date="2025-12-31")
        add_task(temp_store, title="Sooner", due_date="2025-11-30")
        add_task(temp_store, title="Middle", due_date="2025-12-15")
        
        tasks = list_tasks(temp_store, sort_mode="due")
        assert tasks[0]["due_date"] == "2025-11-30"
        assert tasks[1]["due_date"] == "2025-12-15"
        assert tasks[2]["due_date"] == "2025-12-31"


class TestCompleteTask:
    def test_complete_existing_task(self, temp_store):
        task = add_task(temp_store, title="To Complete")
        result = complete_task(temp_store, task["id"])
        assert result is True
        
        tasks = list_tasks(temp_store)
        assert tasks[0]["status"] == "complete"

    def test_complete_nonexistent_task(self, temp_store):
        result = complete_task(temp_store, 999)
        assert result is False

    def test_complete_already_completed_task(self, temp_store):
        task = add_task(temp_store, title="Task")
        complete_task(temp_store, task["id"])
        result = complete_task(temp_store, task["id"])
        assert result is True  # Should still return True


class TestDeleteTask:
    def test_delete_existing_task(self, temp_store):
        task = add_task(temp_store, title="To Delete")
        result = delete_task(temp_store, task["id"])
        assert result is True
        
        tasks = list_tasks(temp_store)
        assert len(tasks) == 0

    def test_delete_nonexistent_task(self, temp_store):
        result = delete_task(temp_store, 999)
        assert result is False

    def test_delete_from_multiple_tasks(self, temp_store):
        task1 = add_task(temp_store, title="Keep 1")
        task2 = add_task(temp_store, title="Delete")
        task3 = add_task(temp_store, title="Keep 2")
        
        delete_task(temp_store, task2["id"])
        tasks = list_tasks(temp_store)
        assert len(tasks) == 2
        assert tasks[0]["title"] == "Keep 1"
        assert tasks[1]["title"] == "Keep 2"


class TestEditTask:
    def test_edit_title(self, temp_store):
        task = add_task(temp_store, title="Original")
        result = edit_task(temp_store, task["id"], title="Updated")
        assert result is True
        
        tasks = list_tasks(temp_store)
        assert tasks[0]["title"] == "Updated"

    def test_edit_description(self, temp_store):
        task = add_task(temp_store, title="Task", description="Old desc")
        edit_task(temp_store, task["id"], description="New desc")
        
        tasks = list_tasks(temp_store)
        assert tasks[0]["description"] == "New desc"

    def test_edit_due_date(self, temp_store):
        task = add_task(temp_store, title="Task", due_date="2025-12-01")
        edit_task(temp_store, task["id"], due_date="2025-12-31")
        
        tasks = list_tasks(temp_store)
        assert tasks[0]["due_date"] == "2025-12-31"

    def test_edit_multiple_fields(self, temp_store):
        task = add_task(temp_store, title="Original", description="Old", due_date="2025-12-01")
        edit_task(temp_store, task["id"], title="New", description="Updated", due_date="2025-12-31")
        
        tasks = list_tasks(temp_store)
        assert tasks[0]["title"] == "New"
        assert tasks[0]["description"] == "Updated"
        assert tasks[0]["due_date"] == "2025-12-31"

    def test_edit_nonexistent_task(self, temp_store):
        result = edit_task(temp_store, 999, title="Nope")
        assert result is False

    def test_edit_invalid_date(self, temp_store):
        task = add_task(temp_store, title="Task", due_date="2025-12-01")
        edit_task(temp_store, task["id"], due_date="invalid")
        
        tasks = list_tasks(temp_store)
        assert tasks[0]["due_date"] == "2025-12-01"  # Should keep original


class TestSetPriority:
    def test_set_valid_priority(self, temp_store):
        task = add_task(temp_store, title="Task")
        result = set_priority(temp_store, task["id"], 1)
        assert result is True
        
        tasks = list_tasks(temp_store)
        assert tasks[0]["priority"] == 1

    def test_set_priority_range(self, temp_store):
        for p in range(1, 6):
            task = add_task(temp_store, title=f"Priority {p}")
            set_priority(temp_store, task["id"], p)
        
        tasks = list_tasks(temp_store, sort_mode="priority")
        for i, task in enumerate(tasks):
            assert task["priority"] == i + 1

    def test_set_invalid_priority_too_low(self, temp_store):
        task = add_task(temp_store, title="Task")
        result = set_priority(temp_store, task["id"], 0)
        assert result is False

    def test_set_invalid_priority_too_high(self, temp_store):
        task = add_task(temp_store, title="Task")
        result = set_priority(temp_store, task["id"], 6)
        assert result is False

    def test_set_priority_nonexistent_task(self, temp_store):
        result = set_priority(temp_store, 999, 3)
        assert result is False


class TestClearTasks:
    def test_clear_empty_store(self, temp_store):
        count = clear_tasks(temp_store)
        assert count == 0

    def test_clear_with_tasks(self, temp_store):
        add_task(temp_store, title="Task 1")
        add_task(temp_store, title="Task 2")
        add_task(temp_store, title="Task 3")
        
        count = clear_tasks(temp_store)
        assert count == 3
        
        tasks = list_tasks(temp_store)
        assert len(tasks) == 0

    def test_clear_preserves_file(self, temp_store):
        add_task(temp_store, title="Task")
        clear_tasks(temp_store)
        
        # File should still exist with empty array
        assert temp_store.exists()
        with temp_store.open() as f:
            data = json.load(f)
        assert data == []

    def test_clear_then_add(self, temp_store):
        add_task(temp_store, title="Task 1")
        add_task(temp_store, title="Task 2")
        clear_tasks(temp_store)
        
        new_task = add_task(temp_store, title="New Task")
        assert new_task["id"] == 1  # ID should reset to 1


class TestSearchTasks:
    def test_search_prefix_priority(self, temp_store):
        t1 = add_task(temp_store, title="Brush teeth")
        t2 = add_task(temp_store, title="Do laundry", description="Buy bleach and detergent")
        t3 = add_task(temp_store, title="Buy groceries")
        t4 = add_task(temp_store, title="Remember birthday")

        results = search_tasks(temp_store, "b")
        ids = [r["id"] for r in results]
        # Prefix matches (titles starting with 'b'): t1, t3 appear first, then other substring matches t2, t4
        assert ids == [t1["id"], t3["id"], t2["id"], t4["id"]]

    def test_search_incremental_prefix(self, temp_store):
        t1 = add_task(temp_store, title="Brush teeth")
        t2 = add_task(temp_store, title="Do laundry", description="Need brown bags")
        t3 = add_task(temp_store, title="Broken screen repair")

        results_br = search_tasks(temp_store, "br")
        titles_br = [r["title"].lower() for r in results_br]
        # Only titles starting with 'br' should be first; others containing 'br' appear after
        assert titles_br[0].startswith("br")
        # Ensure prefix match count is correct (Brush teeth, Broken screen repair)
        assert set(titles_br[:2]) == {"brush teeth", "broken screen repair"}

    def test_search_substring_only(self, temp_store):
        add_task(temp_store, title="Alpha task")
        add_task(temp_store, title="Gamma work", description="Contains the term milk here")
        add_task(temp_store, title="Delta")
        results = search_tasks(temp_store, "milk")
        assert len(results) == 1
        assert "milk" in results[0]["description"].lower()

    def test_search_case_insensitive(self, temp_store):
        add_task(temp_store, title="Brush teeth")
        add_task(temp_store, title="Buy milk")
        r_lower = search_tasks(temp_store, "b")
        r_upper = search_tasks(temp_store, "B")
        assert [t["id"] for t in r_lower] == [t["id"] for t in r_upper]
