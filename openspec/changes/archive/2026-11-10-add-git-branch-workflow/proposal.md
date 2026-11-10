# Proposal

## Why

The template defines how work is planned (OpenSpec change → apply → archive) but says nothing about how that work reaches `main`. In practice commits land directly on `main`, nothing ties a change to a branch, and merge style varies. Because this template is the basis for every project, the branch workflow needs to be defined once, enforced the same way everywhere, and kept the same in every repo.

## What Changes

- **No direct commits to protected branches** (`main`, `master`): git and the Claude Code harness both reject them. The only exception is concluding a merge.
- **One OpenSpec change = one branch** named `<type>/<change-name>` (e.g. `feat/add-git-branch-workflow`). Its change directory can only be created on that branch. Branches that have no change (`docs/…`, `chore/…`, `dependabot/…`) are still allowed.
- **Merge only after archive, and always `--no-ff`**: merging a change branch into a protected branch is rejected while its change is unarchived. Squash and fast-forward merges into a protected branch are rejected. After merging, the source branch is deleted with `git branch -d`.
- New, project-agnostic enforcement files that are identical in every project: `.githooks/` (git `pre-commit` + `pre-merge-commit` hooks, a shared policy module, an `install` script), plus a Claude Code hook registered for `Bash`, `Write|Edit` and `SessionStart`.
- `openspec/config.yaml` archive guidance gains the commit → merge → delete-branch steps. CLAUDE.md gains workflow rule 4. README gains the setup step and the workflow.

## Capabilities

### New Capabilities
- `git-branch-workflow`: how work moves from a branch to a protected branch: branch-per-change naming, protected-branch commit and merge rules, merge style, branch cleanup, and how the rules are enforced and installed.

### Modified Capabilities
<!-- None: task-workflow-governance requirements (OpenSpec as sole tracker, session start, SESSION.md scope, code-edit gate) are unchanged. -->

## Impact

- New files: `.githooks/branch_policy.py`, `.githooks/pre-commit`, `.githooks/pre-merge-commit`, `.githooks/install`, `.claude/hooks/check_git_branch.py`.
- Modified: `.claude/settings.json` (new hook registrations), `openspec/config.yaml` (archive guidance), `CLAUDE.md` (rule 4), `README.md` (Prerequisites + workflow).
- Per-clone setup: every clone must run `.githooks/install` once, because git does not activate versioned hooks automatically. A SessionStart warning catches clones that skipped it.
- Existing projects adopt it by copying the same files. `n8n_openclaw_agent` is the first such project.
- Not covered: merges made on GitHub (PR merge button) bypass local hooks. Server-side branch protection is a per-repo setting outside this template.
