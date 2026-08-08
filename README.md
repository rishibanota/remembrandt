<p align="center">
  <img src="assets/hero.png" alt="remembrandt" width="800"/>
</p>

<h1 align="center">remembrandt</h1>

<p align="center">
  <b>Never forgets.</b> Persistent memory for Claude Code, Cursor and Codex coding agents.
</p>

<p align="center">
  <a href="#"><img src="https://img.shields.io/badge/license-MIT-blue" alt="MIT"></a>
  <a href="#"><img src="https://img.shields.io/badge/python-3.9+-informational" alt="Python 3.9+"></a>
  <a href="#"><img src="https://img.shields.io/badge/zero-dependencies-brightgreen" alt="Zero dependencies"></a>
  <a href="#"><img src="https://img.shields.io/github/stars/rishibanota/remembrandt?style=social" alt="stars"></a>
</p>

<p align="center">
  <b>Your coding agent forgets everything between sessions.</b> remembrandt is a tiny
  skill + CLI that gives it a durable, human-readable memory — so it picks up
  exactly where it left off: the decisions, the gotchas, the changelog. Always.
</p>

---

## 🤔 The problem

You spend 20 minutes re-explaining your architecture to Claude Code, Cursor or
Codex. It answers, you close the terminal… and the next session it asks the
*same questions* again. Context is rebuilt from scratch every single time.

**That is the #1 complaint about coding agents.** They're brilliant — and
completely amnesiac.

## ✨ The fix

remembrandt is a **skill you drop into any agent** (Claude Code, Cursor, Codex)
plus a **zero-dependency CLI**. It maintains a lightweight, file-based memory
store for your project and regenerates a `MEMORY.md` your agent reads at the
start of every session.

> Your agent finally remembers: the rationale behind that `why`, the footgun it
> hit yesterday, what shipped last week — without you repeating a word.

---

## 📸 Demo

```
$ remembrandt remember "Use uv for dependency management" --category decision --tags uv
Remembered entry #1 in 'decision'.

$ remembrandt remember "Never mutate the shared config object" --category gotcha
Remembered entry #2 in 'gotcha'.

$ remembrandt recall
  1. [3] (changelog) Refactor auth to JWT
  2. [2] (gotcha)     Never mutate the shared config object
  3. [1] (decision)   Use uv for dependency management   #uv

$ remembrandt resume
Wrote .remembrandt/MEMORY.md
```

The compiled `MEMORY.md` it writes — **this is what your agent reads on startup**:

```markdown
# Project Memory

## Decision
- **1** [2026-08-03] Use uv for dependency management _#uv_

## Changelog
- **3** [2026-08-03] Refactor auth to JWT

## Gotcha
- **2** [2026-08-03] Never mutate the shared config object
```

---

## 🚀 Quick start

### Option A — Agent skill (Claude Code / Cursor / Codex)

```bash
# macOS / Linux
bash scripts/install.sh

# Windows PowerShell
powershell -ExecutionPolicy Bypass -File scripts/install.ps1
```

This installs the CLI **and** registers the `SKILL.md` so your agent
automatically reads `MEMORY.md` at session start and captures what matters.

### Option B — Just the CLI (Python)

```bash
pip install -e ".[dev]"     # or simply run:  python -m agent_memory
remembrandt --help
```

### Option C — Cursor / Codex manual

Copy [`SKILL.md`](SKILL.md) into your agent's skills directory
(`~/.cursor/skills/remembrandt/`, etc.) and make sure `remembrandt` is on PATH.

---

## 🧠 Commands

| Command | Description |
|---|---|
| `remembrandt remember <text> [-c CATEGORY] [-t TAG ...]` | Store a memory |
| `remembrandt recall [category]` | List memories, newest first |
| `remembrandt search <query>` | Search all memories |
| `remembrandt resume [--title ...]` | Regenerate `MEMORY.md` |
| `remembrandt status` | Show store stats |
| `remembrandt edit <id> [--content ...]` | Edit an entry |
| `remembrandt forget <id>...` | Delete entries |
| `remembrandt export [-o file]` | Export all entries as JSON |
| `remembrandt reset` | Clear all memories |

**Categories:** `decision`, `changelog`, `gotcha`, `note`, `context` — or any
custom name with `-c custom --custom-category mycat`.

**How your agent is told to use it** (see [`SKILL.md`](SKILL.md)):

> 1. On session start, read `.remembrandt/MEMORY.md` **first**.
> 2. Record decisions, gotchas and completed work as they happen.
> 3. Regenerate `MEMORY.md` at the end of a session with `remembrandt resume`.

---

## 💾 How it works

Pure files. No database, no server, no cloud, no vendor lock-in.

```
.your-project/
└── .remembrandt/
    ├── MEMORY.md            ← human/agent-readable compiled memory
    └── entries/
        ├── 00001.json       ← one tiny JSON file per memory
        ├── 00002.json
        └── ...
```

- **Private by default** — memory lives in your repo; commit it if you want
  teammates' agents to share it, or gitignore it for a solo workflow.
- **Portable** — it's just JSON + Markdown. Read it anywhere.
- **Zero dependencies** — Python 3.9+ standard library only.

---

## ⚙️ Configuration

| Env var | Purpose |
|---|---|
| `REMBRANDT_DIR` | Override the memory store location (default `.remembrandt/`) |
| `CLAUDE_SKILLS_DIR` | Override where the Claude Code skill is installed |

---

## 🧪 Development & testing

```bash
make install      # install CLI + skill
make test         # run the test suite (pytest)
make demo         # run a live CLI demo in a scratch dir
make demo-data    # rebuild the demo data in examples/demo
```

The test suite covers the store and the CLI end-to-end (23 tests):

```bash
python -m pytest -q
# .......................   [100%]  23 passed
```

---

## 🗺️ Roadmap

- [ ] Multi-agent shared memory (your team's agents all read the same store)
- [ ] `mcp` server wrapper so any MCP client can call `remember`/`recall`
- [ ] Automatic memory capture via git hooks (commit → changelog entry)
- [ ] TTL / pruning for stale entries
- [ ] VSCode extension with an in-editor memory panel

---

## 🤝 Contributing

PRs, issues and ideas are very welcome. Open an issue or submit a PR — the
roadmap above is a great place to start.

## 📄 License

[MIT](LICENSE)

---

<p align="center">
  <sub>Made for developers who are tired of repeating themselves.</sub>
</p>
