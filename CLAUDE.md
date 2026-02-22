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

## Key Conventions

- **[Domain constant]**: [value or file pointer]
- **[Naming convention]**: [rule]
- **Tasks**: `to_do/P{0-3}_{priority}_*.md` — delete file when complete
- **[Any other invariant short enough for inline mention]**

<!-- ── HOW TO USE THIS FILE ──────────────────────────────────────────────────
  Keep this file under ~200 tokens (roughly 150 words of prose).
  If a convention needs more than one line, it belongs in ARCHITECTURE.md.
  If a trigger needs context to act on, it belongs in the file it points to.
  This file is auto-loaded on every session — every token here competes with
  task-relevant context. When in doubt, leave it out.
─────────────────────────────────────────────────────────────────────────── -->
