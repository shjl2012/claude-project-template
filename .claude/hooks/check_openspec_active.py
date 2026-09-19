#!/usr/bin/env python3
"""PreToolUse (Write|Edit) gate: coding tasks require an active OpenSpec change.

Reads hook input JSON on stdin. For Write/Edit calls targeting a .py file
under src/, tests/, scripts/ or a .ipynb file under notebooks/, blocks the
call (decision: block) unless openspec/changes/ contains at least one
directory other than "archive" — the proxy for "an OpenSpec change is
currently in flight" (see CLAUDE.md Repo level workflow rules 1-3).
"""
import json
import os
import re
import sys

GATED_PATTERN = re.compile(
    r"^(?:src|tests|scripts)/.*\.py$|^notebooks/.*\.ipynb$"
)


def has_active_change(project_root):
    changes_dir = os.path.join(project_root, "openspec", "changes")
    if not os.path.isdir(changes_dir):
        return False
    for entry in os.listdir(changes_dir):
        if entry == "archive":
            continue
        if os.path.isdir(os.path.join(changes_dir, entry)):
            return True
    return False


def main():
    try:
        data = json.load(sys.stdin)
    except json.JSONDecodeError:
        return

    if data.get("tool_name") not in ("Write", "Edit"):
        return

    file_path = data.get("tool_input", {}).get("file_path", "")
    project_root = os.getcwd()
    rel_path = os.path.relpath(file_path, project_root) if os.path.isabs(file_path) else file_path

    if not GATED_PATTERN.match(rel_path):
        return

    if has_active_change(project_root):
        return

    output = {
        "decision": "block",
        "reason": (
            "No active OpenSpec change found under openspec/changes/. "
            "This repo requires an OpenSpec change (proposal -> apply) before "
            "editing code in src/, tests/, scripts/, or notebooks/. "
            "Run /opsx:propose to start one."
        ),
    }
    print(json.dumps(output))


if __name__ == "__main__":
    try:
        main()
    except Exception:
        pass
