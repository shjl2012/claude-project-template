# claude-project-template

A minimal documentation system for AI-assisted development with Claude Code. Designed to solve three problems: repeated codebase scanning each session, schema/contract drift between coupled files, and cross-session state loss across machines.

## Project Structure

```
.
├── CLAUDE.md              # Auto-loaded index with triggers (~200 tokens max)
├── CURRENT_STATE.md       # Current phase, next action, machine (overwrite each session)
├── ARCHITECTURE.md        # Stable architectural decisions (~500 tokens)
├── pyproject.toml         # Poetry project & dependency configuration
├── poetry.toml            # Poetry local settings
├── requirement.txt        # Minimal bootstrap dependencies (poetry itself)
├── src/                   # Python source modules
│   ├── CLAUDE.md
│   └── README.md
├── data/                  # Raw, processed, and external data
│   ├── CLAUDE.md
│   └── README.md
├── notebooks/             # Jupyter notebooks for EDA and experiments
│   ├── CLAUDE.md
│   └── README.md
├── tests/                 # Pytest test suite
│   ├── CLAUDE.md
│   └── README.md
├── scripts/               # Standalone scripts and pipeline runners
│   ├── CLAUDE.md
│   └── README.md
├── docs/                  # Human-facing project documentation
│   ├── CLAUDE.md
│   └── README.md
├── to_do/                 # Task specs (move to recycle_bin when complete)
│   ├── CLAUDE.md
│   ├── README.md
│   └── P{n}_{priority}_*.md
└── recycle_bin/            # Soft-delete holding area (no rm allowed)
    ├── CLAUDE.md
    └── README.md
```

## Files

| File | Purpose | Update frequency |
|---|---|---|
| `CLAUDE.md` | Auto-loaded index with triggers. ~200 tokens max. | Rarely — only when project structure changes |
| `CURRENT_STATE.md` | Current phase, next action, active artifact, machine. | Every session (overwrite, never append) |
| `ARCHITECTURE.md` | Stable decisions not readable from code. ~500 tokens. | Rarely — only when architectural decisions change |
| `to_do/P{n}_{priority}_*.md` | Per-task spec with context, steps, output contract. | Delete when task is complete |

## How to Use

### Starting a new project

1. Copy this directory into your project root
2. Fill in `CLAUDE.md`: project identity, triggers for your coupling-risk locations, key conventions
3. Fill in `ARCHITECTURE.md`: tech stack decisions, layer contracts, key invariants
4. Set `CURRENT_STATE.md` to your starting phase
5. Create task files in `to_do/` for your first work items

### Two-file pattern (enforced)

Every directory has two documentation files:
- **`CLAUDE.md`** — For Claude Code. Triggers, contracts, and coupling rules. Loaded automatically when Claude enters the directory.
- **`README.md`** — For humans. Purpose, structure, and usage conventions.

### Per-directory CLAUDE.md (content guidance)

Add coupling rules to a directory's `CLAUDE.md` when two or more files share a contract that breaks silently if one side changes without the other. Keep it to 3–5 lines:

```markdown
# Schema Contract — [layer name]

Any change to `[file A]:[symbol]` must be propagated to:
- `[file B]:[symbol]`
- `[file C]:[symbol]`

Read `ARCHITECTURE.md` (Layer Contracts section) before committing.
```

Common locations: ORM models + serializers, DB writer + SQL schema, API types + client types.

### ARCHITECTURE.md (conditional)

Add this when:
- `CLAUDE.md` Key Conventions starts growing beyond ~5 lines, OR
- The project has a user-facing README that's the wrong audience for architectural invariants

### Critical commands (conditional)

If test/build/lint commands aren't self-evident from project structure, add a Commands section to `CLAUDE.md` or `ARCHITECTURE.md`:

```markdown
## Commands
- **Test**: `pytest tests/` or `npm test`
- **Build**: `docker compose up` or `make build`
- **Lint**: `ruff check .` or `eslint src/`
```

## Design Principles

- **CLAUDE.md is auto-loaded unconditionally** — every token competes with task context. Keep it minimal. If in doubt, leave it out.
- **CURRENT_STATE.md is overwritten, never appended** — it holds current state only. Historical log belongs in a separate archive file.
- **Triggers fire at the right moment** — point to files that Claude should open *when a specific action is taken*, not always.
- **Per-directory CLAUDE.md is structural enforcement** — it fires automatically when Claude enters the directory, not when Claude remembers to check.
- **Task files are moved to `recycle_bin/` when done** — they're specs, not history. Completed work belongs in git history or an archive.
- **No rm allowed** — move unwanted files to `recycle_bin/` for manual cleanup.
