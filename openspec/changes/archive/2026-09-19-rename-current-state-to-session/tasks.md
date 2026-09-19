# Tasks

## 1. Replace CURRENT_STATE.md with SESSION.md

- [x] 1.1 Create `SESSION.md` with only **Blockers** (non-spec-shaped only) and **Machine** fields, an End-of-Session Update Protocol referencing those two fields (and pointing to the active OpenSpec change for phase/next tracking), and the existing Machine-Switch Protocol. Verify by reading the new file against the `task-workflow-governance` spec delta's "SESSION.md fields" scenario.
- [x] 1.2 `git rm CURRENT_STATE.md` (after 1.1 creates its replacement) and verify with `git status` showing it removed and `ls CURRENT_STATE.md` failing.

## 2. Update CLAUDE.md

- [x] 2.1 Rewrite the Session Start section to direct a session to query OpenSpec directly for phase/next info (e.g. `openspec list --json` for the active change, that change's `tasks.md` for the next action) and to consult `SESSION.md` only for machine/environment handoff notes and non-spec blockers. Verify by grepping `CLAUDE.md` for "CURRENT_STATE" (should be absent) and confirming the section matches the spec delta's "Session start routes to the active OpenSpec change" requirement.

## 3. Update README.md

- [x] 3.1 Update the Project Structure diagram's file entry (rename `CURRENT_STATE.md` → `SESSION.md`, updated one-line description).
- [x] 3.2 Update the Files table row (rename, new Purpose/Update-frequency description reflecting Blockers + Machine only).
- [x] 3.3 Update "Starting a new project" step 4 to reference setting up `SESSION.md`'s Machine field instead of "starting phase."
- [x] 3.4 Update the Design Principles bullet about the file (rename, describe narrowed scope: holds only machine/session handoff + non-spec blockers, not project phase). Verify by grepping `README.md` for "CURRENT_STATE" (should be absent) and "SESSION.md" (should be present in all four spots).

## 4. Final validation

- [x] 4.1 Confirm no dangling references: `grep -rn "CURRENT_STATE" README.md CLAUDE.md openspec/specs/task-workflow-governance/spec.md` returns nothing.
- [x] 4.2 Run `openspec validate rename-current-state-to-session --strict` and confirm it passes with the `task-workflow-governance` delta.
