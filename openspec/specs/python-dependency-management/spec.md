# python-dependency-management Specification

## Purpose

Establishes uv as the project's Python dependency manager, replacing Poetry, so dependency installation, locking, and dev-tooling setup follow one consistent workflow.

## Requirements

### Requirement: uv replaces Poetry as the dependency manager
The project SHALL manage Python dependencies via `uv` using `pyproject.toml` and `uv.lock`, and SHALL NOT rely on Poetry-specific configuration (`poetry.toml`, `[tool.poetry]` build config, `requirement.txt` bootstrap file).

#### Scenario: No Poetry artifacts remain
- **WHEN** the repository root is inspected
- **THEN** `poetry.toml` and `requirement.txt` do not exist, and `pyproject.toml` contains no `[tool.poetry]` package-mode/build-system configuration

### Requirement: Dev dependencies declared via PEP 735 groups
`pyproject.toml` SHALL declare development-only dependencies (including `vulture`) under `[dependency-groups]` rather than a Poetry dependency group.

#### Scenario: Dev dependency group present
- **WHEN** `pyproject.toml` is read
- **THEN** a `[dependency-groups]` `dev` list exists and includes `vulture`

### Requirement: Documentation reflects uv workflow
CLAUDE.md, ARCHITECTURE.md, and README.md SHALL describe uv (installation, sync, add) as the package-management convention instead of Poetry.

#### Scenario: README prerequisites reviewed
- **WHEN** README.md's Prerequisites section is read
- **THEN** it instructs installing `uv` rather than Poetry, and dependency-related commands use `uv` (e.g. `uv sync`, `uv add`)
