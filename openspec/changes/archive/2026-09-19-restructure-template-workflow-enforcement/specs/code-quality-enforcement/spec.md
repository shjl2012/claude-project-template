# Spec Delta

## Purpose

Defines the code-quality guidance available to Claude Code sessions in this template and specifies which parts of it are actually enforced at runtime by hooks versus left as self-checks, so the documentation never claims stronger enforcement than what runs.

## ADDED Requirements

### Requirement: Code-quality guidance lives outside CLAUDE.md
The AI code-quality and debloat guidance SHALL be documented in `docs/CODE_QUALITY.md`, and CLAUDE.md SHALL reference it via a single Trigger row rather than embedding the full guidance.

#### Scenario: CLAUDE.md stays within budget
- **WHEN** CLAUDE.md is read
- **THEN** it contains a Trigger row pointing to `docs/CODE_QUALITY.md` for code edits, and does not contain the full "AI Code Quality & Debloat Guidelines" text

### Requirement: Guidance is stack-agnostic
The code-quality guidance SHALL NOT scope its API/service-layer guidance to a specific framework (e.g. FastAPI/Pydantic); such frameworks SHALL appear only as examples.

#### Scenario: Framework-specific section reviewed
- **WHEN** `docs/CODE_QUALITY.md`'s API/service-layer section is read
- **THEN** its header and requirements are framework-neutral, with FastAPI/Pydantic mentioned only as an example

### Requirement: Checklist wording matches actual enforcement
Each item in the code-quality checklist SHALL be worded to match what is actually enforced: items backed by the PostToolUse hook may state they are enforced; items with no automated check (e.g. duplicate-logic detection) SHALL be worded as a self-check rather than "Mandatory."

#### Scenario: Duplicate-logic checklist item reviewed
- **WHEN** the checklist item about duplicate validation code/hardcoded config is read
- **THEN** it instructs the model to self-check rather than asserting mandatory automated enforcement

### Requirement: Dead-code scan does not silently no-op
The project SHALL declare `vulture` as a dev dependency so the PostToolUse hook's dead-code scan runs consistently for contributors who install project dependencies.

#### Scenario: vulture available after dependency install
- **WHEN** a contributor installs the project's dev dependencies
- **THEN** `vulture` is available on PATH and the existing PostToolUse hook's dead-code scan produces findings instead of silently returning none
