# Task Manager Constitution

## Principles

- **Simplicity:** Keep the codebase minimal and easy to understand.
- **Portability:** Runs on any system with Python 3.8+ and no external dependencies.
- **Data Integrity:** Tasks are reliably stored in a JSON file.
- **Transparency:** All operations are confirmed via CLI output.

## Constraints

- Single-file implementation (`task_manager.py`)
- Only standard Python libraries (`json`, `os`, `sys`)
- Data stored in `tasks.json` in the project root
- No user authentication or multi-user support
- No GUI; CLI only

## Project Structure

```text
task_manager.py
tasks.json
specs/
  ├── plan.md
  ├── spec.md
  ├── tasks.md
  ├── checklist.md
  └── constitution.md
```

## Change Management

- All changes must be documented in `specs/tasks.md`
- Major changes require updates to `specs/plan.md` and `specs/spec.md`
- The constitution should be updated if project scope or constraints change

## Review Gates

- Must pass simplicity and portability checks before adding new features
- No feature may introduce external dependencies or break CLI compatibility

**Version**: 1.0.0 | **Ratified**: 2025-11-20 | **Last Amended**: 2025-11-20
