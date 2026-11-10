#!/usr/bin/env python3
"""Claude Code hook for the branch workflow (SessionStart, PreToolUse Bash / Write|Edit).

Applies the rules in .githooks/branch_policy.py (imported by path, so git and
Claude never disagree) before Claude runs a command or writes a file:
  - Bash: blocks `git commit` on a protected branch (unless concluding a merge
    of an archived change), `git merge --squash/--ff/--ff-only` or merging an
    unarchived change into a protected branch, and `git branch -D`.
  - Write|Edit: blocks writes under openspec/changes/<name>/ unless the current
    branch ends in /<name> (archive/ is exempt).
  - SessionStart: reminds Claude to run .githooks/install if it has not been run.

Best-effort early guard: it only blocks on a positive match and allows
everything on internal errors; the git hooks are the backstop.
"""
import importlib.util
import json
import os
import shlex
import sys

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def load_policy():
    path = os.path.join(PROJECT_ROOT, ".githooks", "branch_policy.py")
    spec = importlib.util.spec_from_file_location("branch_policy", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


GIT_OPTS_WITH_VALUE = {"-C", "-c", "--git-dir", "--work-tree", "--namespace"}
MERGE_OPTS_WITH_VALUE = {"-m", "-s", "-X", "-F", "--message", "--strategy", "--strategy-option", "--file", "--into-name"}
SEPARATOR_CHARS = set("();<>|&")


def segments(command):
    """Split a shell command into simple-command token lists (best effort)."""
    for line in command.splitlines():
        lexer = shlex.shlex(line, posix=True, punctuation_chars=True)
        lexer.whitespace_split = True
        current = []
        try:
            for token in lexer:
                if token and set(token) <= SEPARATOR_CHARS:
                    if current:
                        yield current
                    current = []
                else:
                    current.append(token)
        except ValueError:
            current = []
        if current:
            yield current


def short_flag_has(arg, letter):
    return arg.startswith("-") and not arg.startswith("--") and letter in arg[1:]


def check_branch_delete(args):
    deleting = any(a == "--delete" or short_flag_has(a, "d") for a in args)
    forced = any(a == "--force" or short_flag_has(a, "f") for a in args)
    if any(short_flag_has(a, "D") for a in args) or (deleting and forced):
        return (
            "Force-deleting branches (`git branch -D`) is not allowed. Merge the branch "
            "into a protected branch first, then delete it with `git branch -d`."
        )
    return None


def check_merge_command(root, args):
    if "--abort" in args or "--quit" in args:
        return None
    if "--continue" in args:
        return policy.check_commit(root)
    flags, refs, skip = [], [], False
    for arg in args:
        if skip:
            skip = False
        elif arg in MERGE_OPTS_WITH_VALUE:
            skip = True
        elif arg.startswith("-"):
            flags.append(arg)
        else:
            refs.append(arg)
    return policy.check_merge(root, refs, flags)


def check_git_call(cwd, tokens):
    """tokens start after `git`; returns a violation message or None."""
    i = 0
    while i < len(tokens) and tokens[i].startswith("-"):
        if tokens[i] == "-C" and i + 1 < len(tokens):
            cwd = os.path.join(cwd, os.path.expanduser(tokens[i + 1]))
        i += 2 if tokens[i] in GIT_OPTS_WITH_VALUE else 1
    if i >= len(tokens):
        return None
    sub, args = tokens[i], tokens[i + 1:]
    root = policy.repo_root(cwd) if os.path.isdir(cwd) else None
    if root is None:
        return None
    if sub == "commit":
        return policy.check_commit(root)
    if sub == "merge":
        return check_merge_command(root, args)
    if sub == "branch":
        return check_branch_delete(args)
    return None


def check_bash(command, cwd):
    for tokens in segments(command):
        while tokens and "=" in tokens[0] and not tokens[0].startswith("="):
            tokens = tokens[1:]
        if not tokens:
            continue
        if tokens[0] == "cd":
            target = tokens[1] if len(tokens) > 1 else "~"
            cwd = os.path.join(cwd, os.path.expanduser(target))
        elif os.path.basename(tokens[0]) == "git":
            message = check_git_call(cwd, tokens[1:])
            if message:
                return message
    return None


def check_write(file_path, cwd):
    path = os.path.join(cwd, file_path)
    existing = os.path.dirname(path)
    while existing and not os.path.isdir(existing):
        existing = os.path.dirname(existing)
    root = policy.repo_root(existing) if existing else None
    if root is None:
        return None
    return policy.check_change_path(root, os.path.relpath(os.path.realpath(path), os.path.realpath(root)))


def deny(message):
    return {
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "permissionDecisionReason": f"Branch workflow: {message}",
        }
    }


def session_notice(cwd):
    root = policy.repo_root(cwd)
    if root is None or policy.hooks_installed(root):
        return None
    return {
        "hookSpecificOutput": {
            "hookEventName": "SessionStart",
            "additionalContext": (
                "Branch workflow git hooks are not active in this clone "
                "(core.hooksPath is not .githooks). Run `.githooks/install` once "
                "(or ask the user to) before committing or merging."
            ),
        }
    }


def handle(data):
    cwd = data.get("cwd") or os.getcwd()
    if data.get("hook_event_name") == "SessionStart":
        return session_notice(cwd)
    tool_input = data.get("tool_input", {})
    tool = data.get("tool_name")
    if tool == "Bash":
        message = check_bash(tool_input.get("command", ""), cwd)
    elif tool in ("Write", "Edit"):
        message = check_write(tool_input.get("file_path", ""), cwd)
    else:
        message = None
    return deny(message) if message else None


def main():
    try:
        data = json.load(sys.stdin)
    except json.JSONDecodeError:
        return
    output = handle(data)
    if output:
        print(json.dumps(output))


if __name__ == "__main__":
    try:
        policy = load_policy()
        main()
    except Exception:
        pass
