# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

[One-line project identity: what it does and its key goal/metric]

## Session Start

Read `CURRENT_STATE.md` first — current phase, next action, active artifact, machine. Then open the active change under `openspec/changes/` named in the Next field.

## Triggers

| When | Open |
|------|------|
| [Coupling-risk action, e.g. "Modifying models/ or serializers/"] | [File to read] + [Script to run, if any] |
| [Another trigger] | [What to open] |
| Starting any new coding task | Run `/opsx:propose` (OpenSpec) before touching code — requires `openspec` CLI, see README Prerequisites |
| Writing or editing code | `docs/CODE_QUALITY.md` (hook enforces a subset automatically) |
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
| `openspec/changes/` | Task tracking — active OpenSpec changes (see Repo level workflow rules) |
| `recycle_bin/` | Soft-delete holding area (no rm — move here instead) |

## Key Conventions

- **Package management**: uv via `pyproject.toml` + `uv.lock` — do not use pip install directly
- **[Domain constant]**: [value or file pointer]
- **[Naming convention]**: [rule]
- **No rm**: Move unwanted files to `recycle_bin/` instead of deleting
- **Tasks**: Tracked exclusively via `openspec/changes/`
- **Docs**: Every directory has a `CLAUDE.md` (for Claude) and `README.md` (for humans)
- **Skills**: Superpowers plugin skills (TDD, debugging, planning) auto-activate — install once per machine, see README Prerequisites
- **[Any other invariant short enough for inline mention]**

<!-- ── HOW TO USE THIS FILE ──────────────────────────────────────────────────
  Keep this file under ~200 tokens (roughly 150 words of prose).
  If a convention needs more than one line, it belongs in ARCHITECTURE.md.
  If a trigger needs context to act on, it belongs in the file it points to.
  This file is auto-loaded on every session — every token here competes with
  task-relevant context. When in doubt, leave it out.
─────────────────────────────────────────────────────────────────────────── -->

## Repo level workflow rules
1. **Brainstorm before creative work.** Invoke the `superpowers:brainstorming` skill for any brainstorming task, including but not limited to: understanding the requirements of a new feature, finding the root cause of a bug or error, or refactoring/restructuring code.

2. **Use the OpenSpec workflow for all coding tasks.** Strictly follow the write openspec change -> apply workflow for any coding task within this repo.

3. **OpenSpec is the single source of truth for specs.** All specs must be written using OpenSpec, including specs produced during a `superpowers:brainstorming` session. Brainstorming output should be captured into OpenSpec rather than left in chat or ad-hoc docs.
