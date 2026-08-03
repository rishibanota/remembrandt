---
name: remembrandt
description: >
  Persistent project memory for coding agents. Use this skill to never lose
  context across sessions. At the start of work, read the project's MEMORY.md
  to recover decisions, gotchas and the changelog. During work, capture
  important decisions, gotchas and progress so they survive session restarts.
  Call the `remembrandt` CLI to remember, recall, search and resume.
metadata:
  version: 0.1.0
  license: MIT
  tags: [memory, agent, claude-code, cursor, codex, context]
---

# remembrandt — Persistent Agent Memory

You are the memory layer for this project. Your job is to make sure nothing
important the human or another agent decided is ever lost, even across
completely fresh sessions.

## When to do this

1. **On session start** — if a `.remembrandt/MEMORY.md` file exists, read it
   *first* before doing any other work. It is the single source of truth for
   project context: prior decisions, gotchas, and the changelog.
2. **Whenever a meaningful decision is made** — record it so future sessions
   (or the human) know *why* the code is the way it is.
3. **Whenever a gotcha / pitfall is discovered** — record it so the same bug
   is never reintroduced.
4. **Whenever a task is completed** — append to the changelog.
5. **At the end of a working session** — regenerate `MEMORY.md` with
   `remembrandt resume` so the human can review and commit it.

## How to use the CLI

```bash
remembrandt remember "Use `uv` for dependency management" --category decision --tags uv
remembrandt remember "Never mutate the shared config object" --category gotcha
remembrandt recall                      # list everything, newest first
remembrandt recall decision             # filter by category
remembrandt search uv                   # search all entries
remembrandt resume                      # write .remembrandt/MEMORY.md
remembrandt status                      # show stats
remembrandt forget 12                   # delete entry #12
```

If the `remembrandt` executable is not installed, run the equivalent
`python -m agent_memory ...` commands from the project root.

## Recommended categories

- **decision** — architectural and code decisions and their rationale
- **changelog** — what changed and when (a lightweight changelog)
- **gotcha** — pitfalls, sharp edges and things to never do again
- **note** — general useful notes
- **context** — background, requirements, constraints about the project

Keep entries short, specific and self-contained. Prefer many small entries
over one giant blob. Add tags when it helps searching.
