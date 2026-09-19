#!/usr/bin/env python3
"""PostToolUse (Write|Edit) enforcement of the CLAUDE.md Code Quality Checklist.

Reads hook input JSON on stdin and, for edits to .py files, checks only the
newly written content (Edit's new_string / Write's content) for:
  - leftover TODO/FIXME/placeholder markers -> blocks (decision: block)
  - likely hardcoded config/secret values   -> warns (additionalContext)
  - vulture dead-code findings for the file -> warns (additionalContext)

Blocking is limited to the unambiguous TODO/placeholder case; the other two
checks are heuristic and reported as warnings so the model can judge context.
"""
import json
import os
import re
import subprocess
import sys

TODO_PATTERN = re.compile(r"#.*\b(TODO|FIXME|XXX|placeholder)\b", re.IGNORECASE)
ALLOW_PATTERN = re.compile(r"noqa:\s*todo|allow-todo", re.IGNORECASE)
HARDCODED_PATTERN = re.compile(
    r'\b(password|passwd|secret|api_key|apikey|token|host|ip_address)\s*=\s*["\'][^"\']+["\']',
    re.IGNORECASE,
)


def new_content_from(data):
    tool_input = data.get("tool_input", {})
    if data.get("tool_name") == "Edit":
        return tool_input.get("new_string", "")
    return tool_input.get("content", "")


def run_vulture(file_path):
    project_root = os.getcwd()
    try:
        result = subprocess.run(
            ["vulture", file_path, "--min-confidence", "80"],
            cwd=project_root,
            capture_output=True,
            text=True,
            timeout=20,
        )
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return None
    return result.stdout.strip() or None


def main():
    try:
        data = json.load(sys.stdin)
    except json.JSONDecodeError:
        return

    file_path = data.get("tool_input", {}).get("file_path", "")
    if not file_path.endswith(".py"):
        return

    new_content = new_content_from(data)
    block_reasons = []
    warnings = []

    for lineno, line in enumerate(new_content.splitlines(), start=1):
        if TODO_PATTERN.search(line) and not ALLOW_PATTERN.search(line):
            block_reasons.append(f"line {lineno}: {line.strip()}")
        if HARDCODED_PATTERN.search(line):
            warnings.append(f"line {lineno}: possible hardcoded config value: {line.strip()}")

    vulture_hits = run_vulture(file_path)
    if vulture_hits:
        warnings.append("vulture dead-code findings:\n" + vulture_hits)

    output = {}
    if warnings:
        output["hookSpecificOutput"] = {
            "hookEventName": "PostToolUse",
            "additionalContext": "Code Quality Checklist warnings (CLAUDE.md):\n" + "\n\n".join(warnings),
        }
    if block_reasons:
        output["decision"] = "block"
        output["reason"] = (
            "CLAUDE.md Code Quality Checklist: leftover TODO/placeholder marker(s):\n"
            + "\n".join(block_reasons)
            + "\nRemove it, finish the implementation, or mark it explicitly authorized"
            " with `# allow-todo` on that line."
        )

    if output:
        print(json.dumps(output))


if __name__ == "__main__":
    try:
        main()
    except Exception:
        pass
