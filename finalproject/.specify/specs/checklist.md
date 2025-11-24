# Pre-Commit Checklist: Task Manager CLI

**Purpose**: Quality assurance checklist before committing changes to the task manager
**Created**: 2025-11-22
**Feature**: Task Manager CLI with AI integration

## Code Quality

- [x] CHK001 All functions have type hints
- [x] CHK002 All public functions have docstrings
- [x] CHK003 No hardcoded API keys in source code
- [x] CHK004 Error handling with graceful degradation
- [x] CHK005 PEP 8 style compliance (no major linting errors)

## Testing

- [x] CHK006 All existing tests pass: `pytest tests/ -v`
- [x] CHK007 New features have corresponding tests
- [x] CHK008 Tests use mocks for external APIs (no real API calls)
- [x] CHK009 Edge cases covered (empty input, invalid data, missing files)
- [x] CHK010 No warnings in test output

## Documentation

- [x] CHK011 README.md updated with new features
- [x] CHK012 Usage examples added for new commands
- [x] CHK013 Constitution updated if principles changed
- [x] CHK014 Comments added for complex logic

## Security & Privacy

- [x] CHK015 Sensitive files in .gitignore (key.env, tasks.json)
- [x] CHK016 key.env.example updated if needed
- [x] CHK017 No personal task data in commits
- [x] CHK018 Environment variables used for secrets

## Functionality

- [x] CHK019 Feature works without API key (graceful degradation)
- [x] CHK020 Interactive prompts guide users appropriately
- [x] CHK021 Confirmation required for destructive operations
- [x] CHK022 Error messages are clear and helpful
- [x] CHK023 Data persists correctly in data/tasks.json

## Git Hygiene

- [ ] CHK024 Commit message is descriptive
- [ ] CHK025 No debug code or console.logs left in
- [ ] CHK026 No temporary test files included
- [ ] CHK027 Changes are focused (single feature/fix per commit)

## Notes

- Check items off as completed: `[x]`
- Run tests before committing: `$env:PYTHONPATH = "$PWD"; pytest tests/ -v`
- Verify data directory structure: `data/tasks.json` (not root level)
