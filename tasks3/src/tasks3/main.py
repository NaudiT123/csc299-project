import argparse
import json
from pathlib import Path
from datetime import datetime
from enum import Enum

class Priority(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

class TaskManager:
    def __init__(self, file_path):
        self.file_path = Path(file_path)
        self._ensure_data_directory()
        
    def _ensure_data_directory(self):
        self.file_path.parent.mkdir(parents=True, exist_ok=True)
        if not self.file_path.exists():
            self.file_path.write_text("[]", encoding="utf-8")

    def add_task(self, title, description, priority="medium"):
        tasks = self._load_tasks()
        new_id = max((t.get("id", 0) for t in tasks), default=0) + 1
        task = {
            "id": new_id,
            "title": title,
            "description": description,
            "priority": priority,
            "completed": False,
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat()
        }
        tasks.append(task)
        self._save_tasks(tasks)
        return task

    def list_tasks(self, show_completed=False, priority=None):
        tasks = self._load_tasks()
        if not show_completed:
            tasks = [t for t in tasks if not t.get("completed", False)]
        if priority:
            tasks = [t for t in tasks if t.get("priority") == priority]
        return tasks

    def delete_task(self, task_id):
        tasks = self._load_tasks()
        tasks = [t for t in tasks if t["id"] != task_id]
        self._save_tasks(tasks)

    def update_task(self, task_id, title=None, description=None, priority=None):
        tasks = self._load_tasks()
        updated = None
        for t in tasks:
            if t["id"] == task_id:
                if title is not None:
                    t["title"] = title
                if description is not None:
                    t["description"] = description
                if priority is not None:
                    t["priority"] = priority
                t["updated_at"] = datetime.now().isoformat()
                updated = t
                break
        if updated:
            self._save_tasks(tasks)
        return updated

    def complete_task(self, task_id):
        tasks = self._load_tasks()
        completed = None
        for t in tasks:
            if t["id"] == task_id:
                t["completed"] = True
                t["completed_at"] = datetime.now().isoformat()
                t["updated_at"] = t["completed_at"]
                completed = t
                break
        if completed:
            self._save_tasks(tasks)
        return completed

    def search_tasks(self, query):
        tasks = self._load_tasks()
        q = query.lower()
        return [t for t in tasks if q in t["title"].lower() or q in t["description"].lower()]

    def _load_tasks(self):
        try:
            with self.file_path.open("r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            return []
        except json.JSONDecodeError:
            return []

    def _save_tasks(self, tasks):
        self.file_path.write_text(json.dumps(tasks, indent=2, ensure_ascii=False), encoding="utf-8")

def _print_tasks(tasks):
    if not tasks:
        print("No tasks found.")
        return
    for t in tasks:
        status = "✓" if t.get("completed", False) else " "
        prio = t.get("priority", "medium").upper()
        print(f"[{status}] ID: {t['id']}, Priority: {prio}")
        print(f"    Title: {t['title']}")
        print(f"    Description: {t['description']}")
        if t.get("completed_at"):
            print(f"    Completed at: {t['completed_at']}")
        print()

def main():
    # Always use tasks2/data/tasks.json relative to this file
    data_file = Path(__file__).resolve().parent.parent / "data" / "tasks.json"
    task_manager = TaskManager(data_file)

    parser = argparse.ArgumentParser(description="Enhanced Task Manager CLI")
    subparsers = parser.add_subparsers(dest="command", help="Commands")

    add_parser = subparsers.add_parser("add", help="Add a new task")
    add_parser.add_argument("title", help="Task title")
    add_parser.add_argument("description", help="Task description")
    add_parser.add_argument("--priority", choices=["low", "medium", "high"], default="medium",
                            help="Task priority (default: medium)")

    list_parser = subparsers.add_parser("list", help="List tasks")
    list_parser.add_argument("--all", action="store_true", help="Include completed tasks")
    list_parser.add_argument("--priority", choices=["low", "medium", "high"], help="Filter by priority")

    delete_parser = subparsers.add_parser("delete", help="Delete a task")
    delete_parser.add_argument("task_id", type=int, help="ID of task to delete")

    update_parser = subparsers.add_parser("update", help="Update a task")
    update_parser.add_argument("task_id", type=int, help="ID of task to update")
    update_parser.add_argument("--title", help="New task title")
    update_parser.add_argument("--description", help="New task description")
    update_parser.add_argument("--priority", choices=["low", "medium", "high"], help="New task priority")

    complete_parser = subparsers.add_parser("complete", help="Mark a task as complete")
    complete_parser.add_argument("task_id", type=int, help="ID of task to complete")

    search_parser = subparsers.add_parser("search", help="Search tasks")
    search_parser.add_argument("query", help="Search query")

    args = parser.parse_args()

    if args.command == "add":
        task = task_manager.add_task(args.title, args.description, args.priority)
        print(f'Task added: {task["title"]} (Priority: {task["priority"]})')

    elif args.command == "list":
        tasks = task_manager.list_tasks(show_completed=args.all, priority=args.priority)
        _print_tasks(tasks)

    elif args.command == "delete":
        task_manager.delete_task(args.task_id)
        print(f"Task {args.task_id} deleted")

    elif args.command == "update":
        task = task_manager.update_task(args.task_id, args.title, args.description, args.priority)
        print(f"Task {args.task_id} updated" if task else f"Task {args.task_id} not found")

    elif args.command == "complete":
        task = task_manager.complete_task(args.task_id)
        print(f"Task {args.task_id} marked complete" if task else f"Task {args.task_id} not found")

    elif args.command == "search":
        tasks = task_manager.search_tasks(args.query)
        if tasks:
            print(f"Found {len(tasks)} matching tasks:")
        _print_tasks(tasks)

    else:
        parser.print_help()

if __name__ == "__main__":
    main()