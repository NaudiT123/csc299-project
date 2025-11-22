# Tasks5

CLI task manager governed by the Spec-Kit constitution (`.specify/memory/constitution.md`) and related spec documents in `.specify/specs/`. The constitution defines principles (clarity, iterative planning, validation) that guide how tasks are added and maintained.

## Governance (Constitution Alignment)

- Central truth sources live in `.specify/specs/` (plan, checklist, spec, tasks).
- The `tasks.md` spec can enumerate canonical task titles (extend code later to enforce).
- Changes should be intentional: update spec files first, then apply via the CLI.

## Current Functionality (Implemented)

- Add a task
- List tasks
- Complete a task
- Delete a task
- JSON persistence in `data/tasks.json`

(Validation/export mentioned in earlier drafts are not yet implemented in `src/task_manager.py`.)

## Roadmap (Constitution Driven)

Planned (not yet implemented):
- Spec enforcement (only allow titles listed in `.specify/specs/tasks.md`)
- Validation command
- Task export/import
- Metadata (priority, status from spec)

## Installation

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt  # if added
```

Initialize data (optional):
```bash
echo [] > data\tasks.json
```

## Usage

From project root (Windows):
```bash
python src\task_manager.py add "Example Task"
python src\task_manager.py list
python src\task_manager.py complete 1
python src\task_manager.py delete 1
```

## Data Storage

`data/tasks.json` contains a list of objects:
```json
[
  { "id": 1, "title": "Example Task", "completed": false }
]
```

## Directory Overview

```
src/task_manager.py         CLI logic
data/tasks.json             Persistent task data
.specify/memory/constitution.md  Governance principles
.specify/specs/*.md         Specs and task definitions
```

