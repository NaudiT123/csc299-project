# Tasks Manager 2.0

An enhanced version of the original Tasks Manager with additional features:

## New Features
- Priority levels (low, medium, high) for tasks
- Mark tasks as complete
- Delete tasks
- Update existing tasks
- Search functionality
- Show/hide completed tasks
- Better command-line interface with subcommands

## Usage

```bash
# Add a new task
python src/main.py add "Task Title" "Task Description" --priority high

# List all incomplete tasks
python src/main.py list

# List all tasks including completed ones
python src/main.py list --all

# List tasks with specific priority
python src/main.py list --priority high

# Complete a task
python src/main.py complete 1

# Delete a task
python src/main.py delete 1

# Update a task
python src/main.py update 1 --title "New Title" --description "New Description" --priority low

# Search tasks
python src/main.py search "keyword"
```

## Task Properties
- ID (automatically assigned)
- Title
- Description
- Priority (low/medium/high)
- Completion status
- Creation timestamp
- Last update timestamp
- Completion timestamp (when completed)