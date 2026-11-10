#!/usr/bin/env python3
"""Branch workflow policy shared by the git hooks and the Claude Code hook.

Rules (see openspec specs/git-branch-workflow/spec.md):
  - `main` / `master` are protected; nothing is committed to them directly,
    except concluding a conflicted merge.
  - An OpenSpec change `<name>` lives on a branch whose last `/` segment is
    `<name>`; it may only be merged into a protected branch once
    `openspec/changes/<name>/` is gone (archived) from the merged tree.

CLI: `branch_policy.py pre-commit|pre-merge-commit` (called by .githooks/*).
Exits 1 with a message on a violation, 0 otherwise (including outside a repo).
Stdlib only, no project-specific paths: this file is identical in every project.
"""
import os
import subprocess
import sys

PROTECTED_BRANCHES = ("main", "master")
CHANGES_DIR = "openspec/changes"
ARCHIVE_DIR = "archive"
HOOKS_PATH = ".githooks"


def git(root, *args):
    """Run git in `root`; return stripped stdout, or None if git fails."""
    try:
        result = subprocess.run(
            ["git", "-C", root, *args], capture_output=True, text=True, timeout=10
        )
    except (OSError, subprocess.TimeoutExpired):
        return None
    return result.stdout.strip() if result.returncode == 0 else None


def repo_root(path):
    return git(path, "rev-parse", "--show-toplevel")


def current_branch(root):
    return git(root, "symbolic-ref", "--quiet", "--short", "HEAD")


def is_protected(branch):
    return branch in PROTECTED_BRANCHES


def change_name(branch):
    return branch.rsplit("/", 1)[-1]


def git_path_exists(root, name):
    path = git(root, "rev-parse", "--path-format=absolute", "--git-path", name)
    return bool(path) and os.path.exists(path)


def change_in_ref(root, ref, name):
    return bool(git(root, "ls-tree", "-d", "--full-tree", "--name-only", ref, f"{CHANGES_DIR}/{name}"))


def change_in_index(root, name):
    return bool(git(root, "ls-files", "--", f"{CHANGES_DIR}/{name}/"))


def hooks_installed(root):
    return git(root, "config", "core.hooksPath") == HOOKS_PATH


def unarchived_message(name, branch):
    return (
        f"OpenSpec change '{name}' is not archived yet, so '{branch}' cannot be merged "
        f"into a protected branch. Archive it on '{branch}' first (/opsx:archive), "
        f"commit, then merge with `git merge --no-ff {branch}`."
    )


def direct_commit_message(root, branch):
    if git_path_exists(root, "SQUASH_MSG"):
        return (
            f"Squash merges into '{branch}' are not allowed. "
            f"Run `git reset --merge`, then merge with `git merge --no-ff <branch>`."
        )
    return (
        f"Direct commits to protected branch '{branch}' are not allowed. "
        f"Create a working branch first: `git switch -c <type>/<change-name>`."
    )


def check_commit(root):
    """Policy for `git commit`: violation message or None."""
    branch = current_branch(root)
    if not is_protected(branch):
        return None
    if not git_path_exists(root, "MERGE_HEAD"):
        return direct_commit_message(root, branch)
    merged = git(root, "for-each-ref", "--points-at", "MERGE_HEAD",
                 "--format=%(refname:short)", "refs/heads", "refs/remotes") or ""
    for ref in merged.splitlines():
        if change_in_ref(root, "MERGE_HEAD", change_name(ref)):
            return unarchived_message(change_name(ref), ref)
    return None


def check_merge(root, refs, flags=()):
    """Policy for `git merge <flags> <refs>` run from `root`: message or None."""
    branch = current_branch(root)
    if not is_protected(branch):
        return None
    bad_flags = sorted({"--squash", "--ff", "--ff-only"} & set(flags))
    if bad_flags:
        return (
            f"`git merge {' '.join(bad_flags)}` into protected branch '{branch}' is not "
            f"allowed. Merges into '{branch}' must create a merge commit: `git merge --no-ff <branch>`."
        )
    for ref in refs:
        if change_in_ref(root, ref, change_name(ref)):
            return unarchived_message(change_name(ref), ref)
    return None


def check_pre_merge_commit(root, reflog_action):
    """Clean `git merge`: refs come from GIT_REFLOG_ACTION ("merge <ref>...")."""
    if not is_protected(current_branch(root)):
        return None
    words = reflog_action.split()
    refs = words[1:] if words[:1] == ["merge"] else []
    for ref in refs:
        if change_in_index(root, change_name(ref)):
            return unarchived_message(change_name(ref), ref)
    return None


def check_change_path(root, rel_path):
    """Writing `rel_path` (relative to root): message or None."""
    parts = rel_path.replace(os.sep, "/").split("/")
    prefix = CHANGES_DIR.split("/")
    if parts[: len(prefix)] != prefix or len(parts) <= len(prefix) + 1:
        return None
    name = parts[len(prefix)]
    if name == ARCHIVE_DIR:
        return None
    branch = current_branch(root)
    if branch is None:
        return None
    if is_protected(branch):
        return (
            f"OpenSpec change '{name}' must not be written on protected branch '{branch}'. "
            f"Switch to its branch first: `git switch -c <type>/{name}` (untracked files follow)."
        )
    if change_name(branch) != name:
        return (
            f"OpenSpec change '{name}' does not belong to branch '{branch}': the branch name "
            f"must end in '/{name}'. Switch with `git switch -c <type>/{name}` or `git switch <type>/{name}`."
        )
    return None


def main(argv):
    root = repo_root(os.getcwd())
    if root is None or len(argv) != 2:
        return 0
    if argv[1] == "pre-commit":
        message = check_commit(root)
    elif argv[1] == "pre-merge-commit":
        message = check_pre_merge_commit(root, os.environ.get("GIT_REFLOG_ACTION", ""))
    else:
        return 0
    if message:
        print(f"branch policy: {message}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
