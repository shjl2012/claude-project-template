# Proposal

## Why

The repo's stated intention is to enforce task/coding workflows through CLAUDE.md, make OpenSpec the single source of truth for specs and change records, and use a runtime hook for code-quality control. A review of the current state found several places where the repo contradicts that intention: a parallel `to_do/` task system still competes with OpenSpec as the place work is tracked; CLAUDE.md exceeds its own stated token budget and hardcodes a FastAPI-specific guideline into an otherwise stack-agnostic template; the code-quality checklist claims "Mandatory" enforcement it doesn't actually have (vulture may not be installed, duplicate-logic detection isn't checked at all); `openspec/config.yaml`'s archive guidance references README sections from an unrelated project; and only the code-quality goal has a runtime hook — the "brainstorm first" and "OpenSpec for all coding tasks" rules are unenforced text. Separately, the user has decided to move Python dependency management from Poetry to uv going forward.

## What Changes

- **BREAKING**: Remove the `to_do/` directory and its task-file convention entirely; task tracking moves exclusively to `openspec/changes/`.
- Update `CLAUDE.md`: Session Start points at the active OpenSpec change instead of a `to_do/` file; the OpenSpec trigger covers all new coding tasks (not just "nontrivial" ones); `to_do/` references removed from Project Layout/Key Conventions; the "AI Code Quality & Debloat Guidelines" block is removed from CLAUDE.md (moved to `docs/CODE_QUALITY.md`) to bring the file back within its stated token budget.
- Add `docs/CODE_QUALITY.md` containing the code-quality/debloat guidance, generalized away from a FastAPI/Pydantic-specific section, with the "duplicate validation/hardcoded config" checklist item reworded to a self-check rather than a claimed-enforced rule.
- **BREAKING**: Add a new PreToolUse hook (`.claude/hooks/check_openspec_active.py`) that blocks `Write`/`Edit` to code files under `src/`, `tests/`, `scripts/`, `notebooks/` unless `openspec/changes/` has at least one active (non-archived) change directory — the runtime proxy for "brainstorm first" and "OpenSpec for all coding tasks," since brainstorming output is required to land in OpenSpec and no other artifact marks that it happened.
- Add `vulture` as a dev dependency so the dead-code checklist item is actually enforced instead of silently no-op'ing when the tool is absent.
- Replace `openspec/config.yaml`'s archive-step guidance (currently referencing Chinese-language section names from an unrelated project) with a generic, bracketed-placeholder example, plus a README note telling users to customize it per project.
- Remove `.claude/settings.local.json` from git tracking and add it to `.gitignore` — it currently ships another user's machine-specific paths, which don't belong in a shared template.
- **BREAKING**: Switch Python dependency management from Poetry to uv: `pyproject.toml` drops the Poetry build-system/package-mode config in favor of `[tool.uv] package = false` and PEP 735 `[dependency-groups]`; `poetry.toml` and `requirement.txt` are removed; `.gitignore` gains `.venv/`; `CLAUDE.md`, `ARCHITECTURE.md`, and `README.md` are updated to describe uv instead of Poetry.

## Capabilities

### New Capabilities
- `task-workflow-governance`: OpenSpec as the sole task-tracking system (no `to_do/`), CLAUDE.md/README routing to it, and the PreToolUse hook that requires an active OpenSpec change before code edits under `src/`, `tests/`, `scripts/`, `notebooks/` are allowed.
- `code-quality-enforcement`: The code-quality/debloat guidance in `docs/CODE_QUALITY.md`, its stack-agnostic scope, and which checklist items the existing PostToolUse hook actually enforces vs. which remain self-checks.
- `python-dependency-management`: uv as the project's dependency manager (`pyproject.toml` + `uv.lock`), replacing Poetry.

### Modified Capabilities
(none — this is a greenfield template with no existing specs)

## Impact

- Removed: `to_do/` (directory + contents), `poetry.toml`, `requirement.txt`, tracked `.claude/settings.local.json`.
- Added: `docs/CODE_QUALITY.md`, `.claude/hooks/check_openspec_active.py`, `dependency-groups.dev` (vulture) in `pyproject.toml`, `uv.lock` (generated on first `uv sync`).
- Modified: `CLAUDE.md`, `ARCHITECTURE.md`, `README.md`, `openspec/config.yaml`, `.claude/settings.json` (new hook registration), `pyproject.toml`, `.gitignore`.
- Anyone using this template must install `uv` instead of Poetry, and any in-flight work must have (or start) an active OpenSpec change before editing code under the gated directories.
