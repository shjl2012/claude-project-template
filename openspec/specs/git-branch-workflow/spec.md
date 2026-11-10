# git-branch-workflow Specification

## Purpose

Defines how work moves from a working branch into a protected branch: one branch per OpenSpec change, no direct commits to protected branches, merge only after archive using merge commits, branch cleanup, and how these rules are enforced in git and in Claude Code.

## Requirements

### Requirement: Protected branches
The branches named `main` and `master` SHALL be treated as protected branches. All other branches are working branches.

#### Scenario: Branch classification
- **WHEN** the current branch is `main`
- **THEN** the protected-branch rules in this spec apply to it
- **AND** they do not apply to a branch named `feat/add-x`

### Requirement: No direct commits to protected branches
A commit on a protected branch SHALL be rejected unless it concludes an in-progress merge (`git merge` stopped on conflicts) that itself satisfies the merge rules in this spec.

#### Scenario: Direct commit rejected
- **WHEN** a user runs `git commit` while on `main` with no merge in progress
- **THEN** the commit is rejected with a message directing the user to create a working branch

#### Scenario: Concluding a conflicted merge
- **WHEN** a `--no-ff` merge of an archived change branch into `main` stopped on conflicts and the user commits the resolution
- **THEN** the commit is allowed

#### Scenario: Squash merge commit rejected
- **WHEN** a user runs `git merge --squash feat/add-x` on `main` followed by `git commit`
- **THEN** the commit is rejected

### Requirement: One branch per OpenSpec change
Each OpenSpec change SHALL be developed on its own working branch whose final `/`-separated segment equals the change name (`<type>/<change-name>`, e.g. `feat/add-x` for change `add-x`). A working branch with no OpenSpec change (e.g. `docs/…`, `chore/…`, `dependabot/…`) SHALL be permitted.

#### Scenario: Change files written on a matching branch
- **WHEN** Claude Code writes a file under `openspec/changes/add-x/` while on branch `feat/add-x`
- **THEN** the write is allowed

#### Scenario: Change files written on a protected branch
- **WHEN** Claude Code writes a file under `openspec/changes/add-x/` while on `main`
- **THEN** the write is blocked with a message directing the user to `git switch -c <type>/add-x`

#### Scenario: Change files written on a mismatched branch
- **WHEN** Claude Code writes a file under `openspec/changes/add-x/` while on branch `feat/add-y`
- **THEN** the write is blocked with a message naming the expected branch suffix

#### Scenario: Archived change files are exempt
- **WHEN** Claude Code writes a file under `openspec/changes/archive/`
- **THEN** the branch-mapping check does not block it

### Requirement: Change branches merge only after archive
A merge into a protected branch SHALL be rejected when the merged branch's change directory `openspec/changes/<change-name>/` is still present (unarchived) in the merge result. Merges of branches with no matching change directory SHALL be allowed.

#### Scenario: Unarchived change branch
- **WHEN** a user merges `feat/add-x` into `main` and `openspec/changes/add-x/` exists on `feat/add-x`
- **THEN** the merge is rejected with a message directing the user to archive the change first

#### Scenario: Archived change branch
- **WHEN** a user merges `feat/add-x` into `main` after `openspec/changes/add-x/` was moved under `openspec/changes/archive/` on that branch
- **THEN** the merge is allowed

#### Scenario: Branch without a change
- **WHEN** a user merges `docs/readme-layout` into `main` and no `openspec/changes/readme-layout/` exists
- **THEN** the merge is allowed

### Requirement: Merges into protected branches use merge commits
Merges into a protected branch SHALL always create a merge commit (`--no-ff`). Fast-forward and squash merges of a working branch into a protected branch SHALL be rejected or prevented. Updating a protected branch from its own remote (`git pull`) SHALL fast-forward without creating a merge commit.

#### Scenario: Default merge creates a merge commit
- **WHEN** a user on a configured clone runs `git merge feat/add-x` on `main` and `main` has not diverged
- **THEN** a merge commit is created instead of a fast-forward

#### Scenario: Squash or fast-forward requested by Claude Code
- **WHEN** Claude Code runs `git merge --squash`, `git merge --ff` or `git merge --ff-only` while on `main`
- **THEN** the command is blocked

#### Scenario: Pulling a protected branch
- **WHEN** a user on a configured clone runs `git pull` on `main` that is behind `origin/main`
- **THEN** `main` is fast-forwarded and no merge commit is created

### Requirement: Source branch is deleted after merge
After a change branch is merged into a protected branch, it SHALL be deleted with the safe delete (`git branch -d`). Claude Code SHALL NOT force-delete branches (`git branch -D`).

#### Scenario: Claude Code force-delete blocked
- **WHEN** Claude Code runs `git branch -D feat/add-x`
- **THEN** the command is blocked with a message directing it to merge first and use `git branch -d`

#### Scenario: Archive guidance includes merge and cleanup
- **WHEN** a change is archived via the OpenSpec archive workflow
- **THEN** the archive guidance directs committing the archive on the change branch, merging it with `--no-ff` into the protected branch, and deleting the source branch with `git branch -d`

### Requirement: Enforcement is layered and project-agnostic
The rules SHALL be enforced by versioned git hooks (which cover any committer on a configured clone) and by Claude Code hooks (which cover Claude even on an unconfigured clone). The enforcement files SHALL contain no project-specific paths so they can be copied unchanged between projects. Outside a git repository the hooks SHALL allow everything.

#### Scenario: Claude on an unconfigured clone
- **WHEN** git hooks are not installed and Claude Code runs `git commit` on `main`
- **THEN** the Claude Code hook blocks the command

#### Scenario: Same files in every project
- **WHEN** the enforcement files of two projects built from this template are compared
- **THEN** they are byte-identical

### Requirement: One-step per-clone setup
The repository SHALL provide a single command that activates the versioned git hooks and the merge/pull settings for a clone. A Claude Code session started in a clone where it has not been run SHALL be told to run it.

#### Scenario: Setup applied
- **WHEN** a user runs `.githooks/install` in a fresh clone
- **THEN** `core.hooksPath` is `.githooks`, `merge.ff` is `false` and `pull.ff` is `only`, and running it again changes nothing

#### Scenario: Setup missing
- **WHEN** a Claude Code session starts in a clone whose `core.hooksPath` is not `.githooks`
- **THEN** the session receives a notice to run `.githooks/install`
