# Design

## Context

The template already enforces "an OpenSpec change must exist before code edits" with a Claude Code PreToolUse hook (`check_openspec_active.py`). Each project customizes that hook's gated paths, so it is not identical across projects. Nothing currently touches git. See proposal.md for motivation and specs/git-branch-workflow/spec.md for the rules.

Git behaviour was checked in a scratch repo (git 2.x) and shapes the decisions below:
- `git merge --no-ff` (clean) runs `pre-merge-commit`, **not** `pre-commit`. `MERGE_HEAD` is not yet written, but `GIT_REFLOG_ACTION` is `merge <ref>` and the index holds the merge result.
- Concluding a conflicted merge runs `pre-commit` with `.git/MERGE_HEAD` present.
- `git merge --squash` + `git commit` runs `pre-commit` with `.git/SQUASH_MSG` and no `MERGE_HEAD`.
- Fast-forward merges run no hook at all.
- `branch.main.mergeoptions=--no-ff` makes a plain `git pull` on a lagging `main` create a junk merge commit. `merge.ff=false` + `pull.ff=only` gives `--no-ff` local merges and fast-forward-only pulls.

## Goals / Non-Goals

**Goals:**
- One policy implementation shared by git hooks and the Claude Code hook, so the two never disagree.
- Enforcement files that are byte-identical across projects (no project paths, stdlib-only Python 3).

**Non-Goals:**
- Server-side enforcement (GitHub branch protection, PR merge style). Documented as a per-repo setting.
- Validating branch `<type>` prefixes or commit message format.
- Catching every way a shell command can disguise a git call. The Claude hook is a best-effort early guard; git hooks are the real guard.

## Decisions

1. **Policy module in `.githooks/branch_policy.py`, thin shell wrappers per git hook.** `pre-commit` and `pre-merge-commit` are 2-line `sh` scripts that `exec python3 "$(dirname "$0")/branch_policy.py" <hook-name>`. The Claude hook `.claude/hooks/check_git_branch.py` imports the same module by path. *Alternative:* separate sh and Python implementations, rejected because the rules would drift apart. *Alternative:* pre-commit framework or husky, rejected because it adds an install dependency, and Python 3 is already required by existing hooks.

2. **Change ↔ branch mapping by final path segment.** `change_name = branch.rsplit("/", 1)[-1]`. A branch is treated as a change branch if `openspec/changes/<change_name>/` exists in the tree being checked. This needs no registry and keeps the `<type>/` prefix habit (Conventional-Commit types) free-form. *Alternative:* an exact `change/<name>` prefix, rejected because it loses the type information already used in branch names.

3. **"Archived" = change directory absent from the merge result.** In `pre-merge-commit` this is checked against the index (`git ls-files openspec/changes/<name>/`). In the conflicted-merge `pre-commit` path and in the Claude hook it is checked against the merged ref (`git ls-tree -d <ref> openspec/changes/<name>`). The merged branch name comes from `GIT_REFLOG_ACTION` (pre-merge-commit), from `git branch --points-at MERGE_HEAD` (conflict path), or from the command arguments (Claude hook). If no branch name can be resolved (e.g. merging a raw SHA), the merge is allowed. Branch-ness is unknown in that case, and blocking it would stop legitimate merges.

4. **`--no-ff` via config, not via a hook.** Fast-forwards run no hook, so `.githooks/install` sets `merge.ff=false` and `pull.ff=only` (repo-local config). The Claude hook additionally rejects `--ff`, `--ff-only` and `--squash` merges on a protected branch. Squash merges are caught anyway by `pre-commit`, since there is no `MERGE_HEAD`. Trade-off: `pull.ff=only` also applies to working branches, so a diverged working branch needs `git pull --rebase` or `git pull --no-ff` explicitly.

5. **Claude hook registrations (one script, dispatching on `hook_event_name`/`tool_name`):**
   - `PreToolUse` `Bash`: tokenizes the command into segments (`&&`, `||`, `;`, `|`, newlines), tracks `cd <dir>` and `git -C <dir>`, and for each git call evaluates `commit` (protected branch, no merge in progress → block; merge in progress → archive check on `MERGE_HEAD`), `merge` (protected branch: block `--squash`/`--ff`/`--ff-only`; archive check on the named ref) and `branch -D`/`--delete --force` (block).
   - `PreToolUse` `Write|Edit`: a path under `openspec/changes/<name>/` (not `archive/`) is blocked on a protected branch or when the branch's final segment ≠ `<name>`.
   - `SessionStart`: if inside a git repo and `core.hooksPath` ≠ `.githooks`, emit `additionalContext` telling Claude to run `.githooks/install`.
   It is registered as a separate hook entry, so the existing project-specific `check_openspec_active.py` stays untouched.

6. **Fail-open on internal errors, fail-closed on rule violations.** Like the existing hooks, an exception inside the Claude hook allows the call, so a hook bug cannot brick a session. Git hooks exit non-zero only on a detected violation.

## Risks / Trade-offs

- [Clone never runs `.githooks/install`] → SessionStart notice for Claude sessions. README Prerequisites lists it next to `uv sync`.
- [Human uses `--no-verify` or merges on GitHub] → Accepted. Local hooks are guardrails, not security. README recommends enabling GitHub branch protection.
- [Claude hook misparses an exotic command] → It only *blocks* on a positive match, so a misparse lets the command through to the git hooks, which act as the backstop.
- [Change directory created on `main` via the `openspec new change` CLI, which is Bash, not Write] → The first Write into it is blocked, and the message says `git switch -c <type>/<name>`. Untracked files follow the switch, so nothing is lost.
- [`pull.ff=only` surprises on diverged working branches] → Documented in README with the `--rebase` alternative.

## Migration Plan

- Template: land on `feat/add-git-branch-workflow`, archive, merge `--no-ff`, delete branch. This is the first use of the new workflow on the template itself.
- Existing projects (`n8n_openclaw_agent` first): copy the five enforcement files, add the settings.json hook entries, rule 4 and the archive-guidance lines, then run `.githooks/install`. The project goes through its own OpenSpec change on its own branch.
- Rollback: `git config --unset core.hooksPath` (plus `merge.ff`/`pull.ff`) disables the git side, and removing the settings.json entries disables the Claude side.
