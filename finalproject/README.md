## Task Manager CLI (with optional AI summaries)

This CLI provides a lightweight personal task / knowledge management system with JSON storage and optional OpenAI-powered summarization.

### Features
- Add tasks with title, description, due date, priority (1=high .. 5=low)
- List tasks (filter pending/completed; sort by priority or due date)
- Mark tasks complete (shows ✔ vs ✘)
- Delete tasks
- Clear all tasks with confirmation
- View task statistics overview (total, high priority, overdue, incomplete counts)
- Search tasks (title, description, summary) with prefix-first ordering (typing initial letters like `b`, `br`, `bru` surfaces matching titles first, then other substring hits)
- Update task priority (manually or via AI)
- AI-powered intelligent task prioritization based on urgency, importance, and complexity
- Edit existing tasks (title, description, due date)
- Optional AI summary generation when adding tasks (requires OpenAI API key)
- AI-powered task suggestions based on existing tasks and context
- Quick add mode with `--quick` (skips prompts; uses no due date and priority=3)

### Data Storage
Tasks are stored in `tasks.json` (array of task objects). Fields:
```
id, title, description, created_at, due_date, priority, status, summary
```

### Requirements
- Python 3.13+
- `openai` (already declared in `pyproject.toml`)
- `pytest` (for running tests)

### OpenAI Setup (Optional)
1. Copy `key.env.example` to `key.env`
2. Replace `sk-your-api-key-here` with your actual OpenAI API key
3. The app will automatically load the key from `key.env`

If the key is missing, AI features (summarize, prioritize, suggest) are skipped gracefully.

**Cost estimate**: ~$0.05-$0.20/month for typical personal use with gpt-4o-mini.

### Usage Examples
```powershell
# Add a task (with AI summary)
python main.py add --title "Write report" --description "Quarterly financial analysis" --due 2025-12-01 --priority 2 --summarize

# List all tasks sorted by priority (default)
python main.py list --filter all --sort priority

# List pending tasks sorted by due date
python main.py list --filter pending --sort due

# List tasks with AI summaries displayed
python main.py list --show-summary

# Complete a task
python main.py complete --id 3

# Delete a task
python main.py delete --id 4

# Clear all tasks (with confirmation prompt)
python main.py clear

# Clear all tasks (skip confirmation)
python main.py clear --yes

# Search tasks
python main.py search --query "report"

# AI-powered prioritization (analyzes task and sets priority automatically)
python main.py prioritize --id 2

# Manually set priority
python main.py set-priority --id 2 --priority 1

# Edit a task
python main.py edit --id 3 --title "Updated title" --description "New description" --due 2025-12-15

# Get AI task suggestions
python main.py suggest

# Get AI task suggestions with context
python main.py suggest --context "work project deadline next week"

# View task statistics overview
python main.py overview

# Show available commands
python main.py options

# Quick add (no due date set, priority defaults to 3 silently)
python main.py add --title "Brainstorm project ideas" --quick

# Interactive add (omitting --due and --priority triggers prompts)
python main.py add --title "Start outline"

# Quick add with AI summary
python main.py add --title "Draft proposal" --quick --summarize
```

### Notes
- Due date format must be `YYYY-MM-DD`; invalid dates are ignored.
- Summaries use model `gpt-4o-mini` with a concise prompt.
- Designed for simple local workflow; no concurrency locking.
- If you omit `--priority` / `--due`, the CLI will prompt unless you pass `--quick`.
- `--quick` skips prompts, sets priority=3, and leaves due date unset.
- API key is loaded via `python-dotenv` from `key.env`, `.env`, or `.venv/key.env` (searches in that order).
- High priority tasks are defined as priority ≤ 2 (shown in overview statistics).

### Testing
Comprehensive test suite included with 82 tests covering:
- **Core functions** (`test_manager.py`): add, list, complete, delete, edit, set priority, clear, search (prefix-first ordering)
- **Storage integrity** (`test_storage.py`): JSON persistence, data validation, edge cases
- **AI features** (`test_ai.py`): summarize, prioritize, suggest (mocked, no API calls)

Run tests:
```powershell
# All tests
$env:PYTHONPATH = "$PWD"; pytest tests/ -v

# Specific test file
$env:PYTHONPATH = "$PWD"; pytest tests/test_manager.py -v
```

### Future Enhancements (Ideas)
- Tags & categories
- Export to Markdown
- Recurring tasks
- Automatic priority suggestions via AI

---
Enjoy managing your tasks!
