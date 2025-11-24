# Tasks: Task Manager CLI

**Status**: Completed 2025-11-22
**Prerequisites**: spec.md, plan.md, constitution.md

## Format: `[ID] [Status] [Story] Description`

- **[✅]**: Completed
- **[Story]**: Which user story this task belongs to

---

## Phase 1: Setup (Shared Infrastructure)

- [✅] T001 Create project structure with main.py, task_manager.py, data/, tests/
- [✅] T002 Initialize Python project with pyproject.toml (openai, python-dotenv dependencies)
- [✅] T003 Configure .gitignore for key.env, tasks.json, .venv

---

## Phase 2: Foundational (Blocking Prerequisites)

- [✅] T004 Setup JSON storage with _load()/_save() functions in task_manager.py
- [✅] T005 Implement Task type definition (Dict[str, object])
- [✅] T006 Create argparse CLI structure in main.py with subcommands
- [✅] T007 Setup python-dotenv environment loading with multi-path search
- [✅] T008 Implement graceful error handling for missing files/corrupt JSON
- [✅] T009 Setup timestamp generation with datetime.now(timezone.utc)

---

## Phase 3: User Story 1 - Basic Task Management (Priority: P1) 🎯 MVP

### Tests for User Story 1
- [✅] T010 Create test_manager.py with temp_store fixture
- [✅] T011 Write tests for add_task (basic, priority, due date, validation, ID increment)
- [✅] T012 Write tests for list_tasks (empty, all, pending, completed, sorting)
- [✅] T013 Write tests for complete_task (existing, nonexistent, already completed)
- [✅] T014 Write tests for delete_task (existing, nonexistent, multiple)

### Implementation for User Story 1
- [✅] T015 Implement add_task() in task_manager.py with validation
- [✅] T016 Implement list_tasks() with filter_mode and sort_mode
- [✅] T017 Implement complete_task() with status update
- [✅] T018 Implement delete_task() with task removal
- [✅] T019 Add CLI commands in main.py: add, list, complete, delete
- [✅] T020 Add interactive prompts for optional fields (due date, priority)
- [✅] T021 Add --quick flag to skip prompts

---

## Phase 4: User Story 2 - Task Organization (Priority: P2)

### Tests for User Story 2
- [✅] T022 Write tests for search_tasks (query matching title/description/summary)
- [✅] T023 Write tests for edit_task (title, description, due date, validation)
- [✅] T024 Write tests for set_priority (valid range, invalid, nonexistent)
- [✅] T025 Write tests for clear_tasks (empty store, with tasks, file preservation)

### Implementation for User Story 2
- [✅] T026 Implement search_tasks() with case-insensitive matching
- [✅] T027 Implement edit_task() with optional field updates
- [✅] T028 Implement set_priority() with range validation
- [✅] T029 Implement clear_tasks() with count return
- [✅] T030 Add CLI commands: search, edit, set-priority, clear
- [✅] T031 Add confirmation prompt for clear command with --yes flag

---

## Phase 5: User Story 3 - AI Enhancement (Priority: P3)

### Tests for User Story 3
- [✅] T032 Create test_ai.py with mocked OpenAI client
- [✅] T033 Write tests for _generate_summary() (success, error, no key, no package)
- [✅] T034 Write tests for prioritize_task() (priority setting, reasoning, validation, errors)
- [✅] T035 Write tests for suggest_tasks() (list return, context inclusion, prefix cleaning, errors)

### Implementation for User Story 3
- [✅] T036 Implement _generate_summary() with gpt-4o-mini (60 tokens)
- [✅] T037 Add --summarize flag to add command
- [✅] T038 Implement prioritize_task() with AI analysis (100 tokens)
- [✅] T039 Implement suggest_tasks() with context support (300 tokens)
- [✅] T040 Add CLI commands: prioritize, suggest
- [✅] T041 Add graceful degradation for missing API key

---

## Phase 6: User Story 4 - Task Statistics (Priority: P4)

### Implementation for User Story 4
- [✅] T042 Implement get_overview() with statistics calculation
- [✅] T043 Calculate high priority (≤2), overdue (due_date < today), incomplete counts
- [✅] T044 Add overview CLI command with formatted output
- [✅] T045 Update README with overview command documentation

---

## Phase 7: Storage Integrity & Edge Cases

### Tests
- [✅] T046 Create test_storage.py for JSON persistence tests
- [✅] T047 Test file creation, valid JSON format, field storage
- [✅] T048 Test data persistence across operations
- [✅] T049 Test ID uniqueness, task order preservation
- [✅] T050 Test null values, empty strings, special characters
- [✅] T051 Test storage updates (complete, edit, delete, clear)
- [✅] T052 Test edge cases (missing file, empty file, corrupt JSON, wrong structure)
- [✅] T053 Test timestamp storage and ISO 8601 format

---

## Phase 8: Polish & Cross-Cutting Concerns

- [✅] T054 Update README.md with all features and usage examples
- [✅] T055 Create key.env.example template file
- [✅] T056 Update constitution.md with testing standards
- [✅] T057 Create agent-file.md with project guidelines
- [✅] T058 Create checklist.md for pre-commit QA
- [✅] T059 Fix datetime.utcnow() deprecation warnings
- [✅] T060 Move tasks.json to data/ directory
- [✅] T061 Verify all 78 tests pass with no warnings

---

## Final Status

**Completed**: 61/61 tasks (100%)
**Tests Passing**: 78/78 (33 manager + 22 storage + 23 AI)
**Test Coverage**: Core functions, storage integrity, AI features (mocked)
**Documentation**: README, constitution, agent-file, checklist, plan, spec all complete
**Ready for**: GitHub commit and deployment

---

## Implementation Notes

- All tests written with pytest and fixtures for isolation
- AI tests use unittest.mock to avoid real API calls
- Storage tests verify JSON integrity and error recovery
- Interactive UX implemented with --quick fallback
- Confirmation prompts added for destructive operations
- All code uses type hints and docstrings
- No warnings in test output after datetime fix

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [ ] T001 Create project structure per implementation plan
- [ ] T002 Initialize [language] project with [framework] dependencies
- [ ] T003 [P] Configure linting and formatting tools

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

Examples of foundational tasks (adjust based on your project):

- [ ] T004 Setup database schema and migrations framework
- [ ] T005 [P] Implement authentication/authorization framework
- [ ] T006 [P] Setup API routing and middleware structure
- [ ] T007 Create base models/entities that all stories depend on
- [ ] T008 Configure error handling and logging infrastructure
- [ ] T009 Setup environment configuration management

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - [Title] (Priority: P1) 🎯 MVP

**Goal**: [Brief description of what this story delivers]

**Independent Test**: [How to verify this story works on its own]

### Tests for User Story 1 (OPTIONAL - only if tests requested) ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [ ] T010 [P] [US1] Contract test for [endpoint] in tests/contract/test_[name].py
- [ ] T011 [P] [US1] Integration test for [user journey] in tests/integration/test_[name].py

### Implementation for User Story 1

- [ ] T012 [P] [US1] Create [Entity1] model in src/models/[entity1].py
- [ ] T013 [P] [US1] Create [Entity2] model in src/models/[entity2].py
- [ ] T014 [US1] Implement [Service] in src/services/[service].py (depends on T012, T013)
- [ ] T015 [US1] Implement [endpoint/feature] in src/[location]/[file].py
- [ ] T016 [US1] Add validation and error handling
- [ ] T017 [US1] Add logging for user story 1 operations

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - [Title] (Priority: P2)

**Goal**: [Brief description of what this story delivers]

**Independent Test**: [How to verify this story works on its own]

### Tests for User Story 2 (OPTIONAL - only if tests requested) ⚠️

- [ ] T018 [P] [US2] Contract test for [endpoint] in tests/contract/test_[name].py
- [ ] T019 [P] [US2] Integration test for [user journey] in tests/integration/test_[name].py

### Implementation for User Story 2

- [ ] T020 [P] [US2] Create [Entity] model in src/models/[entity].py
- [ ] T021 [US2] Implement [Service] in src/services/[service].py
- [ ] T022 [US2] Implement [endpoint/feature] in src/[location]/[file].py
- [ ] T023 [US2] Integrate with User Story 1 components (if needed)

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - [Title] (Priority: P3)

**Goal**: [Brief description of what this story delivers]

**Independent Test**: [How to verify this story works on its own]

### Tests for User Story 3 (OPTIONAL - only if tests requested) ⚠️

- [ ] T024 [P] [US3] Contract test for [endpoint] in tests/contract/test_[name].py
- [ ] T025 [P] [US3] Integration test for [user journey] in tests/integration/test_[name].py

### Implementation for User Story 3

- [ ] T026 [P] [US3] Create [Entity] model in src/models/[entity].py
- [ ] T027 [US3] Implement [Service] in src/services/[service].py
- [ ] T028 [US3] Implement [endpoint/feature] in src/[location]/[file].py

**Checkpoint**: All user stories should now be independently functional

---

[Add more user story phases as needed, following the same pattern]

---

## Phase N: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [ ] TXXX [P] Documentation updates in docs/
- [ ] TXXX Code cleanup and refactoring
- [ ] TXXX Performance optimization across all stories
- [ ] TXXX [P] Additional unit tests (if requested) in tests/unit/
- [ ] TXXX Security hardening
- [ ] TXXX Run quickstart.md validation

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3)
- **Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - May integrate with US1 but should be independently testable
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - May integrate with US1/US2 but should be independently testable

### Within Each User Story

- Tests (if included) MUST be written and FAIL before implementation
- Models before services
- Services before endpoints
- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes, all user stories can start in parallel (if team capacity allows)
- All tests for a user story marked [P] can run in parallel
- Models within a story marked [P] can run in parallel
- Different user stories can be worked on in parallel by different team members

---

## Parallel Example: User Story 1

```bash
# Launch all tests for User Story 1 together (if tests requested):
Task: "Contract test for [endpoint] in tests/contract/test_[name].py"
Task: "Integration test for [user journey] in tests/integration/test_[name].py"

# Launch all models for User Story 1 together:
Task: "Create [Entity1] model in src/models/[entity1].py"
Task: "Create [Entity2] model in src/models/[entity2].py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Test User Story 1 independently
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 → Test independently → Deploy/Demo
4. Add User Story 3 → Test independently → Deploy/Demo
5. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1
   - Developer B: User Story 2
   - Developer C: User Story 3
3. Stories complete and integrate independently

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Verify tests fail before implementing
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence
