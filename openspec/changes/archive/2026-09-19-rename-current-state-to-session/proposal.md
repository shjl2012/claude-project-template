# Proposal

## Why

`CURRENT_STATE.md`'s Phase/Next/Active-artifact fields duplicate what OpenSpec's CLI already tracks live and authoritatively (`openspec list --json` for the active change, its `tasks.md` for the next unchecked task, `proposal.md` for the "why"). Hand-copying that into prose creates a second, unenforced source of truth that can silently drift from reality — confirmed in this repo, where the file was never updated across three real OpenSpec changes despite the "Session Start" trigger (part of the `task-workflow-governance` spec) directing sessions to read it first. Meanwhile, two of its fields — **Machine** (OS/username/runtime env/services to start) and non-spec **Blockers** (not tied to any single change's content) — have no OpenSpec equivalent and remain genuinely useful for handoff across machines/sessions. The file should be narrowed to only what OpenSpec doesn't cover, and renamed to reflect that narrower purpose.

## What Changes

- **BREAKING**: Rename `CURRENT_STATE.md` to `SESSION.md`. Drop the **Phase**, **Next**, and **Active artifact** fields entirely. Keep only **Blockers** (non-spec-shaped only — e.g. "waiting on a vendor API key," not anything tracked by an OpenSpec change) and **Machine**.
- Update root `CLAUDE.md`'s Session Start line: instead of "Read `CURRENT_STATE.md` first ... Then open the active change ... named in the Next field," direct the session to query OpenSpec directly (`openspec list --json` for the active change, its `tasks.md` for the next action) and consult `SESSION.md` only for machine/environment handoff notes and non-spec blockers. (`CLAUDE.md`'s Project Layout table only lists directories, not root files, so it needs no change.)
- Update `README.md` everywhere it references `CURRENT_STATE.md`: the Project Structure diagram, the Files table, the "Starting a new project" step 4, and the Design Principles bullet — rename to `SESSION.md` and describe the narrowed scope.
- Modify the `task-workflow-governance` capability spec's "Session start routes to the active OpenSpec change" requirement to describe querying OpenSpec directly rather than reading a hand-maintained Next field, and add a requirement describing `SESSION.md`'s narrowed, OpenSpec-complementary scope.

## Capabilities

### New Capabilities
(none)

### Modified Capabilities
- `task-workflow-governance`: the "Session start routes to the active OpenSpec change" requirement changes from "read `CURRENT_STATE.md`'s Next field" to "query OpenSpec directly (`openspec list`/`tasks.md`)"; a new requirement defines `SESSION.md`'s narrowed scope (Machine + non-spec Blockers only) as the file OpenSpec's tracking doesn't cover.

## Impact

- Renamed: `CURRENT_STATE.md` → `SESSION.md` (content restructured, two fields dropped).
- Modified: `CLAUDE.md` (Session Start section, Project Layout table), `README.md` (Project Structure diagram, Files table, Design Principles, "Starting a new project" step 4), `openspec/specs/task-workflow-governance/spec.md`.
- Anyone using this template must update any external references to `CURRENT_STATE.md` and adopt the narrower `SESSION.md` fields; sessions now rely on the `openspec` CLI being available to determine current phase/next action rather than reading a static file.
