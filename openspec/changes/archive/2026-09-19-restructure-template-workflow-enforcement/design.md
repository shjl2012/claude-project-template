# Design

## Context

See `proposal.md` — Why, for the motivating mismatches. This document covers the mechanics of closing them: `openspec/changes/archive/` already exists (created by `openspec init`) as the destination for archived changes, so "any subdirectory of `openspec/changes/` other than `archive`" is a reliable, already-available proxy for "an OpenSpec change is currently in flight." `docs/` is already established (per `docs/CLAUDE.md`) as content Claude reads only when pointed there, not auto-loaded — which is exactly the trigger mechanism CLAUDE.md's Triggers table already uses elsewhere, so moving code-quality guidance there requires no new mechanism.

## Goals / Non-Goals

**Goals:**
- Make "OpenSpec is the single source of truth" true structurally, not just declared in prose.
- Bring CLAUDE.md back under its own stated token budget without losing information — by relocating, not deleting.
- Make code-quality checklist wording match what's actually enforced at runtime.
- Give the two previously-unenforced workflow rules (brainstorm-first, OpenSpec-for-all-coding-tasks) an actual runtime gate, using the same hook pattern (`.claude/hooks/`, registered in `.claude/settings.json`) already established by the existing PostToolUse hook.
- Complete the Poetry→uv migration cleanly, with no leftover dual-tooling state.

**Non-Goals:**
- Building a general-purpose duplicate-code detector. No automated tool reliably catches "duplicate validation logic" cheaply; the design accepts this as a self-check, not something to solve with new tooling.
- Migrating any existing project that was scaffolded from this template — this change affects the template repo only.
- Changing OpenSpec's own CLI behavior or schema.

## Decisions

**Active-change proxy for the new PreToolUse gate.** Rather than trying to detect "did brainstorming happen" (no artifact marks that), the gate checks for an active OpenSpec change, since rule 3 already requires brainstorming output to land in OpenSpec. One check covers both unenforced rules. Alternative considered: a marker file written by the brainstorming skill itself — rejected because it would require modifying the superpowers plugin, which is outside this repo's control, whereas OpenSpec changes are already this repo's own artifact.

**Hook scope: directories, not just extensions.** The gate matches `.py` files under `src/`, `tests/`, `scripts/` and `.ipynb` under `notebooks/`, rather than gating every `.py`/`.ipynb` file anywhere in the repo. This avoids blocking edits to files like `.claude/hooks/*.py` or example snippets inside `docs/`, which aren't "coding tasks" in the sense the workflow rules mean. Alternative considered: gate by extension repo-wide — rejected as overly broad and likely to block the template's own tooling files.

**Block, not warn.** Per explicit confirmation, the gate hard-blocks (`decision: block`) rather than only adding `additionalContext`, matching the "strictly follow" language already in CLAUDE.md's rule 2. This makes the new hook behave like the existing TODO-marker check in `check_code_quality.py` (block on the unambiguous case) rather than like its heuristic warnings.

**PEP 735 dependency-groups over `[tool.poetry.group.dev]`.** Since Poetry is being removed, dev dependencies move to the standard `[dependency-groups]` table (PEP 735), which `uv` reads natively — avoids reintroducing a tool-specific dependency block right after removing the other one.

**`[tool.uv] package = false`.** Mirrors the current `[tool.poetry] package-mode = false` intent (this is a non-installable application, not a library) using uv's equivalent setting, so `uv sync` doesn't attempt to build/install the project itself.

**Code-quality guidance moves to `docs/`, not `ARCHITECTURE.md`.** ARCHITECTURE.md is reserved for stable architectural decisions (~500 token budget, updated rarely); the debloat guidelines are operational guidance consulted at code-edit time, which matches `docs/`'s existing "read when pointed here" role better, and keeps ARCHITECTURE.md focused.

## Risks / Trade-offs

- **New gate could block legitimate small edits** (e.g. a one-line typo fix) that don't warrant a full OpenSpec change → Mitigation: the block message tells the user to run `/opsx:propose`; OpenSpec changes are cheap to create, and this matches the explicitly confirmed "strictly follow" intent rather than carving out exceptions that would weaken the rule.
- **vulture may still have false negatives/positives** (heuristic tool) → Mitigation: unchanged from today; this change only ensures it's installed and runs, not that its output is perfectly precise. It remains a warning, not a blocker, in the existing PostToolUse hook.
- **uv migration could break a contributor's existing local Poetry-based setup** → Mitigation: README Prerequisites is updated with the uv install command; this is a one-time, explicit, user-approved breaking change (see proposal Impact).
- **Removing `to_do/` discards its example file as a reference for task-writing conventions** → Mitigation: OpenSpec's own proposal/tasks artifacts (this very change) now serve as the lived example of how work is structured; no separate example file is needed.
