# Task Manager CLI Development Guidelines

Auto-generated from all feature plans. Last updated: 2025-11-22

## Active Technologies

- **Python 3.12+**: Core application language
- **OpenAI API (gpt-4o-mini)**: Optional AI features (summarize, prioritize, suggest)
- **python-dotenv**: Environment variable management
- **pytest**: Testing framework
- **argparse**: CLI command parsing
- **JSON**: Local data storage

## Project Structure

```text
finalproject/
├── main.py                 # CLI entry point, argument parsing
├── task_manager.py         # Core business logic and AI functions
├── data/
│   └── tasks.json         # Task data storage (gitignored)
├── tests/
│   ├── __init__.py
│   ├── test_manager.py    # Core function tests
│   ├── test_storage.py    # JSON persistence tests
│   └── test_ai.py         # AI feature tests (mocked)
├── .specify/
│   ├── memory/
│   │   └── constitution.md # Project principles
│   └── specs/
│       └── agent-file.md   # This file
├── key.env.example        # API key template
├── README.md              # User documentation
├── pyproject.toml         # Dependencies
└── .gitignore             # Git exclusions
```

## Commands

### Development
```powershell
# Run application
python main.py <command> [options]

# Run all tests
$env:PYTHONPATH = "$PWD"; pytest tests/ -v

# Run specific test file
$env:PYTHONPATH = "$PWD"; pytest tests/test_manager.py -v

# Install dependencies
pip install openai python-dotenv pytest
```

### Application Commands
```powershell
python main.py add --title "Task" [--description "..."] [--due YYYY-MM-DD] [--priority 1-5] [--summarize] [--quick]
python main.py list [--filter all|pending|completed] [--sort priority|due]
python main.py complete --id N
python main.py delete --id N
python main.py clear [--yes]
python main.py search --query "text"
python main.py prioritize --id N
python main.py set-priority --id N --priority 1-5
python main.py edit --id N [--title "..."] [--description "..."] [--due YYYY-MM-DD]
python main.py suggest [--context "..."]
python main.py overview
python main.py options
```

## Code Style

### Python
- Type hints required for all function signatures
- Docstrings for all public functions
- PEP 8 style compliance
- Use `pathlib.Path` for file operations
- Use `datetime.now(timezone.utc)` (not deprecated `utcnow()`)
- Graceful error handling with helpful messages
- No crash on invalid inputs

### Project-Specific Conventions
- Priority: 1 (high) to 5 (low), default 3
- High priority defined as ≤ 2
- Status: `"pending"` or `"complete"`
- Dates: ISO 8601 format (`YYYY-MM-DD`)
- CLI pattern: `python main.py <command> [--options]`
- Confirmation for destructive operations (clear --yes)

## Recent Changes

### 1. Overview Command (2025-11-22)
- Added `get_overview()` function returning task statistics
- Displays: total tasks, high priority count (≤2), overdue count, incomplete count
- CLI command: `python main.py overview`

### 2. Comprehensive Test Suite (2025-11-22)
- 78 tests across 3 test files
- Core functions: CRUD operations, sorting, filtering
- Storage: JSON persistence, edge cases, corruption recovery
- AI features: Mocked tests (no API costs)

### 3. Clear Tasks Function (2025-11-22)
- Added `clear_tasks()` with confirmation prompt
- CLI command: `python main.py clear [--yes]`
- Returns count of deleted tasks

### 4. Prefix-First Search Ordering (2025-11-22)
- Updated `search_tasks()` to return tasks whose titles start with the query before other substring matches
- Supports incremental discovery (typing initial letters surfaces likely matches early)
- Case-insensitive across title, description, summary

<!-- MANUAL ADDITIONS START -->
<!-- MANUAL ADDITIONS END -->
