# Feature Specification: Task Manager CLI

**Feature Branch**: `main`  
**Created**: 2025-11-22  
**Status**: Completed  
**Input**: Personal task management CLI with JSON storage and optional AI features

## User Scenarios & Testing

### User Story 1 - Basic Task Management (Priority: P1)

As a user, I want to create, view, complete, and delete tasks so I can manage my daily work.

**Why this priority**: Core functionality that must work independently of any other features. Provides immediate value for task tracking.

**Independent Test**: Can create a task, view it in the list, mark it complete, and delete it using only local JSON storage with no external dependencies.

**Acceptance Scenarios**:

1. **Given** no tasks exist, **When** I add a task with title and description, **Then** the task appears with status pending and auto-incremented ID
2. **Given** tasks exist, **When** I list tasks, **Then** I see all tasks with status icons (✔/✘), priority, and due dates
3. **Given** a pending task exists, **When** I mark it complete, **Then** status changes to complete and persists
4. **Given** a task exists, **When** I delete it, **Then** it's removed from storage permanently

---

### User Story 2 - Task Organization (Priority: P2)

As a user, I want to filter, sort, search, and prioritize tasks so I can focus on what matters.

**Why this priority**: Enhances usability once basic CRUD works. Still fully functional without AI.

**Independent Test**: With multiple tasks created, can filter by status, sort by priority/due date, search by text, and manually set priorities.

**Acceptance Scenarios**:

1. **Given** mixed pending/complete tasks, **When** I filter by pending, **Then** only pending tasks appear
2. **Given** tasks with different priorities, **When** I sort by priority, **Then** tasks appear in priority order (1-5)
3. **Given** tasks with keywords, **When** I search for a term, **Then** matching tasks appear with titles that start with the query listed first, followed by other substring matches
4. **Given** a task exists, **When** I set priority to 1, **Then** priority updates and persists

---

### User Story 3 - AI Enhancement (Priority: P3)

As a user, I want AI to help summarize, prioritize, and suggest tasks so I can work more efficiently.

**Why this priority**: Optional enhancement that adds value but isn't required for core functionality. Gracefully degrades without API key.

**Independent Test**: With OpenAI API key configured, can generate summaries for new tasks, get AI-powered priority recommendations, and receive task suggestions based on context.

**Acceptance Scenarios**:

1. **Given** API key is set, **When** I add a task with --summarize, **Then** an AI summary appears in the task
2. **Given** API key is set and task exists, **When** I run prioritize, **Then** AI analyzes and sets priority with reasoning
3. **Given** API key is set, **When** I request suggestions, **Then** 3-5 relevant task ideas appear
4. **Given** API key is missing, **When** I use AI features, **Then** graceful error message appears and app continues

---

### User Story 4 - Task Statistics (Priority: P4)

As a user, I want to see an overview of my tasks so I understand my workload at a glance.

**Why this priority**: Nice-to-have analytics feature that provides value after core features are stable.

**Independent Test**: With various tasks in different states, running overview shows accurate counts for total, high priority, overdue, and incomplete tasks.

**Acceptance Scenarios**:

1. **Given** tasks exist with mixed priorities, **When** I run overview, **Then** count of high priority tasks (≤2) is accurate
2. **Given** tasks with past due dates, **When** I run overview, **Then** overdue count matches pending tasks past their due date
3. **Given** empty task list, **When** I run overview, **Then** shows "0 tasks" without errors

---

### Edge Cases

- What happens when tasks.json is corrupted? → System treats as empty and creates fresh file
- What happens when tasks.json doesn't exist? → System creates it on first add
- What happens when API key is invalid? → Returns error message, app continues without AI
- What happens when user provides invalid date format? → Date is ignored, task created without due date
- What happens when priority is out of range? → Defaults to 3
- What happens when completing/deleting nonexistent task? → Returns "Task #X not found" message
- What happens when clearing with no tasks? → Returns "Cleared 0 tasks"
 - What happens when query has no prefix matches? → Returns only substring matches in original insertion order
 - What happens when query case differs? → Case-insensitive; results identical

## Requirements

### Functional Requirements

- **FR-001**: System MUST store tasks in JSON format in data/tasks.json file
- **FR-002**: System MUST auto-increment task IDs starting from 1
- **FR-003**: System MUST validate priority as integer 1-5 (default 3)
- **FR-004**: System MUST validate due dates as YYYY-MM-DD format
- **FR-005**: System MUST prompt for optional fields when omitted (unless --quick flag)
- **FR-006**: System MUST work without OpenAI API key (AI features gracefully degrade)
- **FR-007**: System MUST require confirmation for destructive operations (clear)
- **FR-008**: System MUST persist data immediately after each operation
- **FR-009**: System MUST handle corrupted/missing JSON files gracefully
- **FR-010**: System MUST use environment variables for API key (never hardcode)
- **FR-011**: System MUST use consistent command pattern: `python main.py <command> [--options]`
- **FR-012**: System MUST provide clear error messages for all failures
 - **FR-013**: System MUST order prefix matches (title starts with query) before other substring matches (case-insensitive)

### Key Entities

- **Task**: Represents a single work item with id (int), title (str), description (str), created_at (ISO timestamp), due_date (YYYY-MM-DD or null), priority (1-5), status (pending/complete), summary (str, AI-generated or empty)
- **Storage**: JSON file at data/tasks.json containing array of task objects

## Success Criteria

### Measurable Outcomes

- **SC-001**: Users can add, list, complete, and delete tasks without any API configuration (100% offline capable)
- **SC-002**: All 82 automated tests pass (37 manager + 22 storage + 23 AI with mocks)
- **SC-003**: Commands respond instantly for local operations (<100ms)
- **SC-004**: AI operations complete within 2 seconds when API available
- **SC-005**: System handles corrupt JSON without data loss (recovers gracefully)
- **SC-006**: No crashes on invalid input (validates and provides helpful error messages)
- **SC-007**: API key remains secure (never exposed in code, gitignored, example template provided)
- **SC-008**: High priority tasks (≤2) correctly identified in overview statistics
 - **SC-009**: Search returns prefix matches first for mixed prefix / substring queries
