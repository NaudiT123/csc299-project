# Task Manager CLI Constitution

## Core Principles

### I. Simplicity First
The task manager prioritizes ease of use and clarity over feature complexity. Every feature must have a clear, single purpose. Interactive prompts guide users when optional parameters are omitted, while `--quick` flag allows power users to skip prompts. If a user needs documentation to understand basic operations, the interface is too complex.

### II. AI Enhancement, Not Dependency
AI features (summarization, prioritization, suggestions) are optional enhancements that gracefully degrade when unavailable. Core task management functionality (add, list, edit, delete, complete) must work without any API keys or external services.

### III. Local-First Data
All task data is stored locally in human-readable JSON format. Users maintain full ownership and control of their data. No cloud dependencies, no databases, no vendor lock-in. The `tasks.json` file should be portable and manually editable if needed.

### IV. Consistency in Command Interface
All CLI commands follow a predictable pattern: `python main.py <command> [--options]`. Related operations use consistent flag naming (e.g., `--id` for task identification, `--priority` for priority levels). Output format is consistent across commands.

### V. Fail Gracefully
Invalid inputs, missing files, API errors, or unavailable services should never crash the application. Provide helpful error messages. Default to safe fallbacks (e.g., default priority 3, skip AI if API key missing).

### VI. Transparency in AI Operations
When AI is used, clearly indicate it to the user. Show AI reasoning for priorities. Distinguish between AI-generated content (summaries, suggestions) and user-entered data. Always allow manual override of AI decisions.

## Data Standards

### JSON Storage Format
- Single `tasks.json` file in `data/` directory
- Array of task objects with consistent schema
- Required fields: `id`, `title`, `created_at`, `status`, `priority`
- Optional fields: `description`, `due_date`, `summary`
- UTC timestamps in ISO 8601 format
- Priority range: 1 (high) to 5 (low)
- Status values: `"pending"` or `"complete"`

### Input Validation
- Due dates must be `YYYY-MM-DD` format or null
- Priority must be integer 1-5 (default: 3)
- Task IDs are positive integers, auto-incrementing
- Empty titles are rejected
- Invalid dates are silently ignored (kept as existing value)

## AI Integration Standards

### OpenAI API Usage
- Model: `gpt-4o-mini` for all AI operations
- API key loaded via `python-dotenv` from multiple locations (search order: `key.env`, `.env`, `.venv/key.env`)
- Key stored in environment variable `OPENAI_API_KEY`
- Graceful fallback when key missing or API unavailable
- Error messages class name only, no stack traces exposed to users
- Token limits: 60 (summaries), 100 (prioritization), 300 (suggestions)

### AI Feature Requirements
- Summaries: max 30 words, concise task description
- Prioritization: Must provide reasoning with priority assignment
- Suggestions: 3-5 actionable tasks based on context
- All AI output must be sanitized and validated before storage

### Statistics & Overview
- High priority defined as priority ≤ 2 (most urgent tasks)
- Overdue tasks: pending tasks with due_date < today
- Incomplete tasks: all tasks with status="pending"
- Overview provides: total count, high priority count, overdue count, incomplete count

## Command Design Principles

### Mandatory for All Commands
- Clear help text accessible via `--help`
- Consistent status icons: ✔ (complete), ✘ (pending)
- Task ID required for modifications (complete, delete, edit, prioritize)
- Confirmation messages after successful operations
- Error messages when operations fail (e.g., "Task #X not found")
- Destructive operations (clear) require confirmation unless `--yes` flag provided

### Search Behavior
- Search is case-insensitive across title, description, and summary fields
- Results are ordered with prefix matches (title starts with query) first, followed by other substring matches
- Incremental queries (e.g. `b`, `br`, `bru`) progressively narrow prefix matches while still including broader substring matches

### Output Format Standards
- Human-readable by default
- Structured format: `[status] #id (Ppriority) due:date title`
- Use `-` for missing optional values
- No ANSI colors (maintain simplicity and compatibility)

## Security & Privacy

### API Key Management
- Never commit API keys to version control
- `key.env` and `.env` must be in `.gitignore`
- Provide `key.env.example` as template for users
- Use environment variables via `python-dotenv` only
- No hardcoded keys in source code
- README must document secure key setup

### Data Privacy
- `tasks.json` must be in `.gitignore`
- No telemetry or external data transmission (except OpenAI API when explicitly requested)
- User tasks remain local and private

## Development Standards

### Code Organization
- `task_manager.py`: All data operations and AI functions
- `main.py`: CLI interface and argument parsing only
- `tests/`: Comprehensive test suite (test_manager.py, test_storage.py, test_ai.py)
- `.specify/memory/constitution.md`: Project principles and standards
- `key.env.example`: Template for API key configuration
- Clear separation: business logic vs. interface
- Type hints required for function signatures
- Docstrings for all public functions

### Testing Requirements
- Comprehensive test suite with 78+ tests covering all core functionality
- Unit tests for all CRUD operations (add, list, complete, delete, edit, set-priority, clear)
- Storage integrity tests (JSON persistence, data validation, edge cases, error recovery)
- AI feature tests using mocks (no real API calls, no costs during testing)
- Tests must pass before committing changes
- Use pytest framework with fixtures for test isolation
- Mock external dependencies (OpenAI API) to ensure tests run offline
- Test both success and failure paths
- Verify graceful degradation when API unavailable

### Documentation
- README with complete usage examples
- Feature list kept current
- All commands documented in `options` command
- Clear distinction between required and optional dependencies

## Command Inventory

Current implemented commands:
- `add`: Create task (with optional interactive prompts or `--quick` mode)
- `list`: View tasks (filter: all/pending/completed; sort: priority/due)
- `complete`: Mark task as done
- `delete`: Remove single task
- `clear`: Remove all tasks (with confirmation)
- `search`: Find tasks by text query
- `prioritize`: AI-powered priority assignment
- `set-priority`: Manual priority setting
- `edit`: Update task fields
- `suggest`: AI task recommendations
- `overview`: Display task statistics summary
- `options`: List all commands

## Governance

This constitution guides all development decisions. When adding features:
1. Does it maintain simplicity?
2. Does it work without AI?
3. Is data stored locally?
4. Are commands consistent?
5. Does it fail gracefully?

If answer to any question is "no", reconsider the feature or redesign to comply.

**Version**: 1.1.1 | **Ratified**: 2025-11-22 | **Last Amended**: 2025-11-22
