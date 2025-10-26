# Task Manager CLI

This project is a simple command-line interface (CLI) based task manager written in Python. It allows users to add tasks and list existing tasks, with all tasks stored in a JSON file.

## Features

- Add a new task with a title and description
- List all existing tasks
- Tasks are saved in a JSON file, which is created if it does not already exist

## File Structure

```
task-manager/
├── src/
│   ├── __init__.py
│   └── main.py
├── data/
│   └── tasks.json
├── requirements.txt
└── README.md
```

## Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   ```
2. Navigate to the project directory:
   ```
   cd task-manager
   ```

## Usage

To run the task manager, use the following commands:

### Add a task
```
python src/main.py --add "Task Title" "Task Description"
```

### List all tasks
```
python src/main.py --list
```

