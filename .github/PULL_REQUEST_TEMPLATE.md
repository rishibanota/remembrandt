## 📝 Description

Please include a summary of the changes and the context/motivation behind them. If this PR fixes an open issue, link to it below.

Fixes #(issue number)

---

## 🔀 Type of Change

Please delete options that are not relevant.

- [ ] 🐛 **Bug fix** (non-breaking change which fixes an issue)
- [ ] ✨ **New feature** (non-breaking change which adds functionality)
- [ ] 💥 **Breaking change** (fix or feature that would cause existing functionality to not work as expected)
- [ ] 📚 **Documentation update** (README, SKILL.md, or docs changes)
- [ ] ⚙️ **Refactoring / Maintenance** (code cleanup, performance improvement, or dev tool updates)

---

## 🧪 How Has This Been Tested?

Please describe the tests that you ran to verify your changes. Provide instructions so we can reproduce.

- [ ] **Unit Tests**: Ran `python -m pytest` / `make test` and all 23+ tests passed.
- [ ] **CLI Smoke Test**: Manually executed `remembrandt remember`, `recall`, and `resume` in a local test directory.
- [ ] **Agent Skill Test**: Verified compatibility with Claude Code / Cursor / Codex if `SKILL.md` or memory formatting was changed.

---

## 📋 Checklist

- [ ] My code follows the code style and guidelines of this project.
- [ ] I have performed a self-review of my own code.
- [ ] I have commented my code, particularly in hard-to-understand areas.
- [ ] I have made corresponding updates to the documentation (`README.md`, `SKILL.md`, etc.).
- [ ] My changes generate no new warnings or errors.
- [ ] I have added tests that prove my fix is effective or that my feature works.
- [ ] New and existing unit tests pass locally with my changes.
- [ ] I have kept runtime dependencies to zero (`dependencies = []`).
- [ ] If changing installer scripts, I updated both `scripts/install.sh` and `scripts/install.ps1`.
