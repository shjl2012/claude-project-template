# Spec Delta

## MODIFIED Requirements

### Requirement: Session start routes to the active OpenSpec change
CLAUDE.md's Session Start section SHALL direct a new session to determine the active (non-archived) OpenSpec change and its next action by querying OpenSpec directly (e.g. `openspec list --json` for the active change, that change's `tasks.md` for the next unchecked task) rather than reading a hand-maintained "Next" field in a project file. It SHALL direct the session to consult `SESSION.md` only for machine/environment handoff notes and non-spec blockers.

#### Scenario: Starting a session with an active change
- **WHEN** a new session reads CLAUDE.md's Session Start instructions
- **THEN** it is directed to run an OpenSpec query (e.g. `openspec list --json`) to find the active change and read that change's `tasks.md` for the next action, instead of reading a Next field from a project file

#### Scenario: Starting a session with no active change
- **WHEN** a new session reads CLAUDE.md's Session Start instructions and `openspec list --json` reports no non-archived change
- **THEN** it is directed to check `SESSION.md` only for machine/environment handoff notes and non-spec blockers, not for phase or next-action information

## ADDED Requirements

### Requirement: SESSION.md is scoped to information OpenSpec does not track
The system SHALL provide a `SESSION.md` file (replacing `CURRENT_STATE.md`) that records only information OpenSpec's change-tracking does not cover: machine/environment handoff details and blockers that are not tied to any single OpenSpec change's content. It SHALL NOT contain phase, next-action, or active-artifact fields that duplicate what an OpenSpec change's `proposal.md`/`tasks.md` already tracks.

#### Scenario: SESSION.md fields
- **WHEN** a user inspects `SESSION.md`
- **THEN** it contains only a **Machine** field (OS/username, runtime env, services to start) and a **Blockers** field limited to non-spec-shaped blockers, with no Phase, Next, or Active artifact field

#### Scenario: No CURRENT_STATE.md remains
- **WHEN** a user inspects the repository root
- **THEN** no `CURRENT_STATE.md` file is present and CLAUDE.md/README.md contain no references to it
