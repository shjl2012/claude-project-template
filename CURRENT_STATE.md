# Current State

<!-- UPDATE THIS FILE at end of every session (overwrite, do not append).
     Fields: phase, next, blockers, artifact, machine. Keep under 80 lines. -->

**Phase**: [Phase name and brief status, e.g. "1b — Auth refactor (in progress)"]

**Next**: [Specific enough to act on immediately — name the task file]
- [e.g. Implement token refresh logic — see `to_do/P1_HIGH_auth_refactor.md`]

**Blockers**: [Dependency or decision blocking progress, or "None"]

**Active artifact**: [Notebook / branch / PR / server, or "None"]

**Machine**: [OS + username] | [runtime env] | [any services to start]

---

## End-of-Session Update Protocol

Overwrite the fields above before closing. Do not append — this file is always current state only.

```
**Phase**: [phase name and brief status]
**Next**: [what to do next session, names the task file]
**Blockers**: [or "None"]
**Active artifact**: [or "None"]
**Machine**: [OS + username] | [env] | [services]
```

## Machine-Switch Protocol

On the new machine before starting work:
1. `git pull` to get latest state
2. Update the `Machine` field above
3. Start required services (db, dev server, etc.)
