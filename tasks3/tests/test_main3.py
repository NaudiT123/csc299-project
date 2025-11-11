import sys
import importlib
from pathlib import Path
import pytest

@pytest.fixture
def main_module():
    src = Path(__file__).resolve().parents[1] / "src"
    if str(src) not in sys.path:
        sys.path.insert(0, str(src))
    return importlib.import_module("tasks3.main")

#testing taskmanager add_task creates task with id=1, correct title, default priority medium, and completed=false
def test_add_task(tmp_path, main_module):
    data_file = tmp_path / "data" / "tasks.json"
    tm = main_module.TaskManager(data_file)
    t = tm.add_task("Title1", "Desc1")
    assert t["id"] == 1
    assert t["title"] == "Title1"
    assert t["priority"] == "medium"
    assert t["completed"] is False

#testing taskmanager delete_task removes only the specified task after adding two tasks and deleting the first. list_tasks should return only the second task.
def test_delete_task(tmp_path, main_module):
    data_file = tmp_path / "data" / "tasks.json"
    tm = main_module.TaskManager(data_file)
    t1 = tm.add_task("A", "a")
    t2 = tm.add_task("B", "b")
    tm.delete_task(t1["id"])
    remaining = tm.list_tasks(show_completed=True)
    assert len(remaining) == 1
    assert remaining[0]["id"] == t2["id"]