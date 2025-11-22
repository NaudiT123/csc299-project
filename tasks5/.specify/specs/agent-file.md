# Task Manager Development Guidelines

Auto-generated from all feature plans. Last updated: 2024-01-15

## Active Technologies

- **Language**: Python 3.8+
- **Storage**: JSON file-based (tasks.json)
- **Dependencies**: Standard library only (json, os, sys)
- **Platform**: Cross-platform CLI

## Project Structure

```text
task_manager.py          # Main CLI application
tasks.json               # Data file (auto-created)
specs/
  ├── plan.md
  ├── spec.md
  ├── tasks.md
  ├── checklist.md
  └── constitution.md
```

## Commands

```bash
python task_manager.py list
python task_manager.py add "Task title here"
python task_manager.py complete 1
python task_manager.py delete 1
```

## Code Style

- Use standard library only, no external dependencies
- Simple functions, no classes needed
- Direct JSON file I/O
- Print confirmations for all operations
- Use f-strings for output formatting

## Recent Changes

1. Initial Implementation – Basic CRUD operations for tasks with JSON persistence
