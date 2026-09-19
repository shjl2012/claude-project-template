# Session

<!-- UPDATE THIS FILE at end of every session (overwrite, do not append).
     Fields: blockers, machine. Phase/next/active-artifact tracking lives in
     OpenSpec (openspec/changes/) — see CLAUDE.md's Session Start section. -->

**Blockers**: [Non-spec-shaped blocker, e.g. "waiting on a vendor API key," or "None" — anything tracked by an OpenSpec change belongs in that change's artifacts, not here]

**Machine**: [OS + username] | [runtime env] | [any services to start]

---

## End-of-Session Update Protocol

Overwrite the fields above before closing. Do not append — this file is always current state only.

```
**Blockers**: [or "None"]
**Machine**: [OS + username] | [env] | [services]
```

For phase, next action, and active artifact, look at the active OpenSpec change under `openspec/changes/` instead — see CLAUDE.md's Session Start section.

## Machine-Switch Protocol

On the new machine before starting work:
1. `git pull` to get latest state
2. Update the `Machine` field above
3. Start required services (db, dev server, etc.)
