# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

[One-line project identity: what it does and its key goal/metric]

## Session Start

Run `openspec list --json` to find the active (non-archived) change, then read that change's `tasks.md` for the next unchecked task. If no active change exists, check `SESSION.md` only for machine/environment handoff notes and non-spec blockers.

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

<!-- Keep this file near ~150 words (see README Design Principles). If a
     convention needs more than one line, it belongs in ARCHITECTURE.md. -->

## Repo level workflow rules
1. **Brainstorm before creative work.** Invoke the `superpowers:brainstorming` skill for any brainstorming task, including but not limited to: understanding the requirements of a new feature, finding the root cause of a bug or error, or refactoring/restructuring code.

2. **Use the OpenSpec workflow for all coding tasks.** Strictly follow the write openspec change -> apply workflow for any coding task within this repo.

3. **OpenSpec is the single source of truth for specs.** All specs must be written using OpenSpec, including specs produced during a `superpowers:brainstorming` session. Brainstorming output should be captured into OpenSpec rather than left in chat or ad-hoc docs.
