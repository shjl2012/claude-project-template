# Architecture

<!-- This file holds stable knowledge that isn't readable from code alone.
     Target: ~500 tokens. If it grows beyond that, split by domain.
     Update rarely — only when a structural decision changes.
     If a fact CAN be learned by reading source files, it does NOT belong here. -->

## What This Project Does

[2-3 sentences: problem being solved, primary users, key constraints]

## Tech Stack Decisions

| Decision | Choice | Why |
|---|---|---|
| [e.g. Database] | [e.g. PostgreSQL + PostGIS] | [e.g. Spatial indexing needed for buffer queries] |
| [e.g. ORM vs raw SQL] | [e.g. Raw psycopg2] | [e.g. PostGIS functions not well-supported by ORMs] |
| [e.g. Validation] | [e.g. Pydantic planned] | [e.g. Type safety at API boundary] |

## Data / Pipeline Flow

```
[Input source] → [Step 1] → [Step 2] → [Step 3] → [Output]
```

[Any non-obvious decisions made at each step]

## Layer Contracts

[List any interfaces where two components must stay in sync.
 This is where per-directory CLAUDE.md files point for context.]

- **[Layer A] → [Layer B]**: [What must match — e.g. "field names exported by cleaner must match DB column names in writer"]
- **[Layer B] → [Schema]**: [What must match — e.g. "writer column list must match CREATE TABLE definition"]

## Key Invariants

[Facts that future Claude sessions must know to avoid breaking things,
 but that aren't obvious from reading the code:]

- [e.g. "All spatial operations use EPSG:3826 internally; data is stored and served in EPSG:4326"]
- [e.g. "Year values are in local calendar format, not CE — always convert before display"]
- [e.g. "The `properties` column is JSONB specifically to avoid schema migrations for facility attributes"]

## What Is NOT Here (and Why)

- **[Old/reference codebase path]**: [Why it exists, when to consult it, do not modify]
- **[External dependency]**: [Why this specific version/approach was locked in]
