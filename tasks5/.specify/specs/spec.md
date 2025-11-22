# Feature Specification: Task Management System

**Feature Branch**: `tasks-manager`
**Created**: 2025-11-21
**Status**: Draft
**Input**: User description: "CLI-based task manager with JSON storage"

## Overview

A simple command-line task manager that stores tasks in a JSON file. Supports basic CRUD operations: add tasks, list all tasks, mark tasks as completed, and delete tasks.

**Commands**:
- `python task_manager.py add "<title>"` - Create a new task
- `python task_manager.py list` - Show all tasks with status
- `python task_manager.py complete <id>` - Mark task as done
- `python task_manager.py delete <id>` - Remove a task

## User Scenarios & Testing

### User Story 1 - Create Tasks (Priority: P1)
As a user, I want to add new tasks so I can track things I need to do.

**Why this priority**: Core functionality for any task manager.

**Independent Test**: Run `python task_manager.py add "Test Task"` and verify it appears in `tasks.json` and prints "Task created: Test Task".

**Acceptance Scenarios**:
1. **Given** no tasks exist, **When** I add a new task, **Then** it is created with id=1, completed=false, and saved to tasks.json.
2. **Given** existing tasks, **When** I add a new task, **Then** it receives the next sequential ID.

---

### User Story 2 - List Tasks (Priority: P1)
As a user, I want to list all tasks so I can see what needs to be done.

**Why this priority**: Essential for viewing tasks.

**Independent Test**: Run `python task_manager.py list` and verify all tasks are displayed with ✓ or ✗ status indicators.

**Acceptance Scenarios**:
1. **Given** no tasks exist, **When** I list tasks, **Then** nothing is displayed (or empty list message).
2. **Given** tasks with mixed completion status, **When** I list tasks, **Then** completed tasks show ✓ and incomplete show ✗.

---

### User Story 3 - Complete Tasks (Priority: P2)
As a user, I want to mark tasks as completed so I know what is done.

**Why this priority**: Important for tracking progress.

**Independent Test**: Run `python task_manager.py complete 1` and verify the task's completed field becomes true in tasks.json and prints "Task 1 marked as completed."

**Acceptance Scenarios**:
1. **Given** an incomplete task with id=1, **When** I complete it, **Then** its completed status updates to true in the list and JSON.
2. **Given** a non-existent task id, **When** I try to complete it, **Then** the command completes without error (current behavior).

---

### User Story 4 - Delete Tasks (Priority: P2)
As a user, I want to delete tasks so I can remove things I no longer need to track.

**Why this priority**: Useful for managing the list.

**Independent Test**: Run `python task_manager.py delete 1` and verify the task is removed from tasks.json and prints "Task 1 deleted."

**Acceptance Scenarios**:
1. **Given** an existing task with id=1, **When** I delete it, **Then** it is removed from the list and JSON file.
2. **Given** a non-existent task id, **When** I try to delete it, **Then** the command completes without error (current behavior).

## Data Model

**Task Object**:
```json
{
  "id": 1,
  "title": "Task title",
  "completed": false
}
```

**Storage**: `tasks.json` (array of task objects)

## Edge Cases

- Empty task list: list command displays nothing
- Missing arguments: prints usage message
- Invalid command: prints "Invalid command or missing arguments."
- Non-existent task IDs: prints "Task <id> not found."

## Related Documentation

- [plan.md](plan.md)
- [tasks.md](tasks.md)
- [checklist.md](checklist.md)