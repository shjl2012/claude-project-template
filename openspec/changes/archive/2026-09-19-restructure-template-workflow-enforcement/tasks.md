# Tasks

## 1. Python dependency management: Poetry → uv

- [x] 1.1 Rewrite `pyproject.toml`: remove `[build-system]` (poetry-core) and `[tool.poetry]` package-mode block; add `[tool.uv] package = false`; add `[dependency-groups] dev = ["vulture"]`. Verify with `uv sync` completing without error and `uv.lock` being generated.
- [x] 1.2 Remove `poetry.toml` and `requirement.txt`. Verify with `git status` showing them deleted and no remaining references via `grep -rn "poetry\|requirement.txt" --include=*.md .` (excluding this change's own files).
- [x] 1.3 Add `.venv/` to `.gitignore`. Verify `git check-ignore .venv/some-file` returns success after `uv sync` creates `.venv/`.
- [x] 1.4 Update `ARCHITECTURE.md`'s Tech Stack Decisions row and `CLAUDE.md`'s Key Conventions package-management bullet to describe uv + `uv.lock` instead of Poetry. Verify by grepping both files for "Poetry" (should be absent) and "uv" (should be present).
- [x] 1.5 Update `README.md`: Prerequisites gets a uv install line and `uv sync`/`uv add` usage; Project Structure diagram and Files table drop `poetry.toml`/`requirement.txt` and add `uv.lock`. Verify by reading the rendered sections against `pyproject.toml`'s actual contents.

## 2. Retire to_do/, route workflow through OpenSpec

- [x] 2.1 `git rm -r to_do/`. Verify with `git status` showing the directory removed and `ls to_do` failing.
- [x] 2.2 Update `CLAUDE.md`: Session Start points at the active OpenSpec change under `openspec/changes/` instead of a `to_do/` task file; Project Layout and Key Conventions drop `to_do/` rows/bullets and add a one-line pointer to `openspec/changes/`. Verify by grepping `CLAUDE.md` for "to_do" (should be absent).
- [x] 2.3 Update `CLAUDE.md`'s Triggers table: change the `/opsx:propose` row from "Starting a new feature or nontrivial fix" to cover all new coding tasks, matching rule 2's "strictly follow ... for any coding task." Verify by reading the row against rule 2's wording for consistency.
- [x] 2.4 Update `README.md`: drop `to_do/` from the Project Structure diagram, Files table, and "Starting a new project" step 5 (replace with proposing the first OpenSpec change via `/opsx:propose`); drop the `to_do/`-specific bullet from Design Principles. Verify by grepping `README.md` for "to_do" (should be absent).

## 3. Relocate and generalize code-quality guidance

- [x] 3.1 Create `docs/CODE_QUALITY.md` containing the current "AI Code Quality & Debloat Guidelines" content, with the "Backend & API Development (FastAPI/Pydantic)" section reheaded/reworded to be framework-neutral (FastAPI/Pydantic kept only as an example). Verify by reading the new file's section header and confirming no other section names a specific framework as its scope.
- [x] 3.2 Reword the checklist item about duplicate validation code/hardcoded config values from "Mandatory... verify" to a self-check instruction (no automated duplicate-logic detection exists). Verify by reading the item's wording against what `.claude/hooks/check_code_quality.py` actually checks (TODO markers, hardcoded-secret heuristic, vulture).
- [x] 3.3 Remove the full "AI Code Quality & Debloat Guidelines" block from `CLAUDE.md` and replace it with a single Trigger row: "Writing/editing code → docs/CODE_QUALITY.md (hook enforces a subset automatically)". Verify `CLAUDE.md`'s word count is back near its stated ~150-word/200-token budget (excluding tables) via `wc -w CLAUDE.md`.

## 4. Generalize OpenSpec archive guidance

- [x] 4.1 Replace `openspec/config.yaml`'s archive-step guidance (Chinese section names from an unrelated project) with a generic, bracketed-placeholder example instructing the archive step to check whether the change affects the project's own README sections. Verify with `openspec validate` (or `openspec context --json`) not erroring on the config, and no remaining non-English/project-specific text in the file.
- [x] 4.2 Add a note in `README.md`'s "Starting a new project" steps telling users to customize `openspec/config.yaml`'s archive guidance to reference their own README's actual section names. Verify by reading the new step against the placeholder added in 4.1.

## 5. Add the OpenSpec-active-change gate hook

- [x] 5.1 Write `.claude/hooks/check_openspec_active.py`: PreToolUse hook, reads stdin JSON, matches `Write`/`Edit` tool calls whose `file_path` is a `.py` file under `src/`, `tests/`, `scripts/` or a `.ipynb` file under `notebooks/`; blocks (`decision: block`) unless `openspec/changes/` contains at least one directory other than `archive`; block message points at `/opsx:propose`. Verify by manually piping sample PreToolUse JSON (matching and non-matching file paths, with and without an active change present) into the script and checking stdout matches the expected block/allow decision for each case.
- [x] 5.2 Register the hook in `.claude/settings.json` under `PreToolUse` with matcher `Write|Edit`, alongside the existing `PostToolUse` entry. Verify by re-reading `.claude/settings.json` and confirming both hooks are present and valid JSON.
- [x] 5.3 End-to-end check: with no active OpenSpec change present, attempt a `Write` to a file under `src/` and confirm it is blocked with a message referencing `/opsx:propose`; with this change's own directory present under `openspec/changes/`, confirm the same edit is allowed.

## 6. Remove personal local settings from the template

- [x] 6.1 `git rm --cached .claude/settings.local.json` (or full `git rm` if not needed locally) and add `.claude/settings.local.json` to `.gitignore`. Verify with `git status` showing it untracked/removed and `git check-ignore .claude/settings.local.json` succeeding.

## 7. Final validation

- [x] 7.1 Run `openspec validate restructure-template-workflow-enforcement --strict` (or equivalent) and confirm it passes with the three new capability deltas.
- [x] 7.2 Confirm no dangling references remain: `grep -rn "to_do\|Poetry\|poetry.toml\|requirement.txt" README.md CLAUDE.md ARCHITECTURE.md openspec/config.yaml` returns nothing unexpected.
