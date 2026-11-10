# Tasks

## 1. Shared policy module + git hooks

- [x] 1.1 Write `.githooks/branch_policy.py` (stdlib-only): protected-branch detection, branch→change-name mapping, "change still unarchived in tree/index" check, and a CLI entry for `pre-commit` / `pre-merge-commit`. Verify with a scratch-repo script that exercises every git-side scenario in specs/git-branch-workflow/spec.md (direct commit, conflicted merge, squash, unarchived/archived/no-change merges, outside a repo).
- [x] 1.2 Write executable `.githooks/pre-commit` and `.githooks/pre-merge-commit` wrappers. Verify `git ls-files -s .githooks` shows mode 100755 for both.
- [x] 1.3 Write idempotent `.githooks/install` (sets `core.hooksPath=.githooks`, `merge.ff=false`, `pull.ff=only`). Verify running it twice in a scratch clone leaves the same `git config --local --list`, and that `git pull` on a lagging `main` fast-forwards while `git merge feat/x` creates a merge commit.

## 2. Claude Code hook

- [x] 2.1 Write `.claude/hooks/check_git_branch.py` dispatching on SessionStart / PreToolUse Bash / PreToolUse Write|Edit per design.md decision 5, importing `.githooks/branch_policy.py`. Verify by piping hook-input JSON for each Claude-side spec scenario (commit on main, merge --squash/--ff-only, unarchived merge, branch -D, change-dir write on main / mismatched / matching branch, archive path, SessionStart with and without install) and checking block/allow output.
- [x] 2.2 Register the hook in `.claude/settings.json` (PreToolUse `Bash`, PreToolUse `Write|Edit`, SessionStart) alongside the existing entries. Verify `python3 -m json.tool .claude/settings.json` passes and existing entries are unchanged.

## 3. Workflow documentation

- [x] 3.1 Add the commit → `--no-ff` merge → `git branch -d` steps to `openspec/config.yaml` archive guidance. Verify `openspec instructions` / archive workflow still parses the config (`openspec context --json` succeeds).
- [x] 3.2 Add rule 4 (branch workflow) to `CLAUDE.md` Repo level workflow rules, staying brief per the file's size guidance. Verify by reading the rendered section.
- [x] 3.3 Update `README.md`: `.githooks/install` in Prerequisites, branch workflow in the OpenSpec workflow line, `.githooks/` in Project Structure, GitHub branch-protection recommendation, `pull.ff=only` note. Verify all four spots by grep.

## 4. Integration

- [x] 4.1 Run `.githooks/install` in this repo and confirm a direct `git commit` on `main` is rejected while commits on this branch succeed. Run `openspec validate add-git-branch-workflow --strict` and confirm it passes.

## Workflow follow-up

- Copy the enforcement files into `n8n_openclaw_agent` via that repo's own `add-git-branch-workflow` change.
- After review: commit, archive this change on `feat/add-git-branch-workflow`, merge `--no-ff` into `main`, delete the branch with `git branch -d`.
