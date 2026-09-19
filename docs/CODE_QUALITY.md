# AI Code Quality & Debloat Guidelines

## Core Principles
* **Enforce DRY:** Never generate duplicate logic. Before writing any new function, utility, or class, search the codebase (`grep`/`find`) to ensure a similar helper does not already exist.
* **Write Pythonic Code:** Prioritize Python built-ins, `list/dict comprehensions`, and standard libraries (`pathlib`, `itertools`, `collections`, `dataclasses`). Do not reinvent wheels with custom loops or manual logic.
* **Eliminate Architectural Bloat:** Keep code shallow. Avoid unnecessary abstraction layers, superfluous interface classes, or useless generic wrappers that only delegate calls.

## API & Service-Layer Development
* **Streamline Exception Handling:** Do not wrap every database call or API routine in a local `try...except Exception: raise` block. Trust and rely on the framework's global exception handlers (e.g. FastAPI's exception handlers).
* **Reuse Models:** Leverage your validation/schema library's inheritance, mixing, or composition features (e.g. Pydantic model inheritance). Avoid creating redundant schemas with overlapping fields for similar API endpoints.
* **Optimize Async/Sync:** Do not introduce asynchronous overhead or `async/await` syntax for tasks that are inherently synchronous, local, or CPU-bound unless explicitly required.

## Automation & Scripting
* **No Speculative Logging:** Do not spam arbitrary `print()` statements or chatty `logger.info()` lines inside core utility loops. Keep terminal outputs focused, clean, and meaningful.
* **Lean Dependencies:** Prioritize existing packages in the environment. Do not suggest or install new third-party packages for tasks that can be easily handled by standard libraries.

## Code Quality Checklist
Before finalizing any code modification or implementation:
1. Run static dead-code analysis if applicable (`vulture` or `deadcode`) — the PostToolUse hook (`.claude/hooks/check_code_quality.py`) runs `vulture` automatically on edited `.py` files and reports findings as warnings.
2. Self-check that there is no duplicate validation code or hardcoded configuration values — no automated tool checks this; it relies on your own review.
3. Ensure no placeholder code or "TODOs" are left behind unless explicitly authorized (`# allow-todo`) — the PostToolUse hook blocks unauthorized TODO/FIXME/placeholder markers automatically.
