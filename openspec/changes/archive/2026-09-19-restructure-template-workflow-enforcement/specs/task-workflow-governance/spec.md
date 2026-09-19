# Spec Delta

## Purpose

Defines OpenSpec as the sole task-tracking and coding-workflow gate for this repo, replacing the `to_do/` convention, so all coding work is planned and traceable through OpenSpec changes.

## ADDED Requirements

### Requirement: OpenSpec is the sole task-tracking system
The system SHALL NOT provide or reference a `to_do/` directory or file-based task convention. All task tracking SHALL occur via `openspec/changes/`.

#### Scenario: No to_do directory exists
- **WHEN** a user inspects the repository root
- **THEN** no `to_do/` directory is present and CLAUDE.md/README.md contain no references to it

### Requirement: Session start routes to the active OpenSpec change
CLAUDE.md's Session Start section SHALL direct a new session to the active (non-archived) OpenSpec change under `openspec/changes/` rather than a `to_do/` task file.

#### Scenario: Starting a session with an active change
- **WHEN** a new session reads CLAUDE.md's Session Start instructions
- **THEN** it is directed to check `openspec/changes/` for the active change instead of a `to_do/` file

### Requirement: Coding tasks require an active OpenSpec change
The repository SHALL enforce, via a PreToolUse hook, that `Write` or `Edit` operations targeting code files under `src/`, `tests/`, `scripts/` (`.py`) or `notebooks/` (`.ipynb`) are blocked unless at least one non-archived change directory exists under `openspec/changes/`.

#### Scenario: Edit attempted with no active change
- **WHEN** a `Write` or `Edit` tool call targets a `.py` file under `src/` and `openspec/changes/` contains no directories other than `archive`
- **THEN** the hook blocks the operation and its message directs the user to run `/opsx:propose`

#### Scenario: Edit allowed with an active change
- **WHEN** a `Write` or `Edit` tool call targets a `.py` file under `src/` and `openspec/changes/` contains at least one non-archived change directory
- **THEN** the hook allows the operation to proceed

#### Scenario: Edit outside gated directories is unaffected
- **WHEN** a `Write` or `Edit` tool call targets a file outside `src/`, `tests/`, `scripts/`, `notebooks/` (e.g. `README.md`)
- **THEN** the hook does not block the operation regardless of active-change state
