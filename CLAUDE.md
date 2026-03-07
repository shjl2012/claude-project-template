# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

[One-line project identity: what it does and its key goal/metric]

## Session Start

Read `CURRENT_STATE.md` first — current phase, next action, active artifact, machine. Then open the active task file in `to_do/` named in the Next field.

## Triggers

| When | Open |
|------|------|
| [Coupling-risk action, e.g. "Modifying models/ or serializers/"] | [File to read] + [Script to run, if any] |
| [Another trigger] | [What to open] |
| Need session history or past rationale | `[path/to/archived/CONVERSATION_CONTEXT.md]` |

## Project Layout

| Directory | Purpose |
|-----------|---------|
| `src/` | Python source modules |
| `data/` | Raw, processed, and external data |
| `notebooks/` | Jupyter notebooks for EDA and experiments |
| `tests/` | Pytest test suite |
| `scripts/` | Standalone scripts and pipeline runners |
| `docs/` | Human-facing project documentation |
| `to_do/` | Task specs with planning — move to `recycle_bin/` when complete |
| `recycle_bin/` | Soft-delete holding area (no rm — move here instead) |

## Key Conventions

- **Package management**: Poetry via `pyproject.toml` — do not use pip install directly
- **[Domain constant]**: [value or file pointer]
- **[Naming convention]**: [rule]
- **No rm**: Move unwanted files to `recycle_bin/` instead of deleting
- **Tasks**: `to_do/P{0-3}_{priority}_*.md` — plan + implement, move to `recycle_bin/` when complete
- **Docs**: Every directory has a `CLAUDE.md` (for Claude) and `README.md` (for humans)
- **[Any other invariant short enough for inline mention]**

<!-- ── HOW TO USE THIS FILE ──────────────────────────────────────────────────
  Keep this file under ~200 tokens (roughly 150 words of prose).
  If a convention needs more than one line, it belongs in ARCHITECTURE.md.
  If a trigger needs context to act on, it belongs in the file it points to.
  This file is auto-loaded on every session — every token here competes with
  task-relevant context. When in doubt, leave it out.
─────────────────────────────────────────────────────────────────────────── -->
