# Task Manager (tasks3)

Simple CLI task manager.

## Tests

File: tests/test_main3.py  
Purpose: verify core TaskManager functionality.

Covered:
- add_task: creates a task with id 1, correct title, default priority "medium", completed False.

- delete_task: after adding two tasks and deleting the first, only the second remains when listing all tasks.

## Running Tests

```bash
pytest -q
```

Uses a temporary directory (tmp_path) so tests do not affect real data.

## Project Structure

- src/tasks3/main.py: TaskManager and CLI.
- tests/test_main3.py: Unit tests for add/delete behavior.

## Notes

Extend tests similarly for update, complete, and search when those methods are implemented.