# Contributing to remembrandt

Thank you for your interest in contributing to **remembrandt**! 🎉

`remembrandt` is a lightweight, zero-dependency persistent memory CLI and AI agent skill for Claude Code, Cursor, and Codex. Our goal is to give AI coding agents a durable, human-readable memory so they never forget context between sessions.

This document outlines the guidelines and steps to help you contribute effectively.

---

## 📜 Table of Contents

- [Code of Conduct](#-code-of-conduct)
- [Design Principles](#-design-principles)
- [Getting Started](#-getting-started)
- [Development Setup](#-development-setup)
- [Development Workflow](#-development-workflow)
- [Project Architecture](#-project-architecture)
- [Coding Standards & Rules](#-coding-standards--rules)
- [Submitting a Pull Request](#-submitting-a-pull-request)
- [Reporting Issues](#-reporting-issues)

---

## 🤝 Code of Conduct

By participating in this project, you agree to abide by our [Code of Conduct](CODE_OF_CONDUCT.md). Please read it to understand expected behaviors and community standards.

---

## ⚡ Design Principles

When contributing to `remembrandt`, keep these core principles in mind:

1. **Zero Runtime Dependencies**: `remembrandt` MUST run with standard Python 3.9+ without requiring external third-party libraries at runtime (`dependencies = []`).
2. **Speed & Lightness**: Memory reads and writes must be instantaneous so agents can call `remembrandt` with minimal latency.
3. **Agent Agnostic**: The tool and `SKILL.md` format should work seamlessly across Claude Code, Cursor, Codex, and other LLM agent runners.
4. **Human-Readable & Transparent**: All memory is stored in plain, human-editable files under `.remembrandt/` and compiled to `.remembrandt/MEMORY.md`.
5. **Cross-Platform Compatibility**: Installation scripts and execution must work smoothly across macOS, Linux, and Windows (bash & PowerShell).

---

## 🚀 Getting Started

### Prerequisites

* **Python**: `3.9` or higher
* **Git**: Installed and configured
* **uv** (Optional but recommended) or standard `venv`

---

## 🛠️ Development Setup

1. **Fork and Clone the Repository**:
   ```bash
   git clone https://github.com/YOUR_USERNAME/remembrandt.git
   cd remembrandt
   ```

2. **Create a Virtual Environment**:
   Using `venv`:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

   Or using `uv`:
   ```bash
   uv venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install Editable Package with Development Dependencies**:
   ```bash
   pip install -e ".[dev]"
   ```

---

## 🧪 Development Workflow

### Running Tests

We use `pytest` for unit and integration testing.

```bash
# Run pytest directly
python -m pytest

# Or using Makefile
make test
```

### Manual CLI Testing & Smoke Tests

Verify the CLI locally during development:

```bash
# Test remember command
remembrandt remember "Use uv for dependency management" -c decision -t uv

# Recall active memories
remembrandt recall

# Check status
remembrandt status

# Generate MEMORY.md
remembrandt resume

# Run demo reset command via Makefile
make demo-reset
```

---

## 🏗️ Project Architecture

```
remembrandt/
├── src/
│   └── agent_memory/
│       ├── __init__.py
│       ├── cli.py        # CLI entry points and argument parsing
│       ├── store.py      # Core file-based storage & memory management logic
│       ├── models.py     # Data structures (MemoryEntry, Categories)
│       └── renderer.py   # Markdown generator for MEMORY.md
├── tests/
│   └── test_memory.py    # Test suite for CLI and store logic
├── scripts/
│   ├── install.sh        # Linux/macOS installation script
│   └── install.ps1       # Windows PowerShell installation script
├── SKILL.md              # Agent skill specification for Claude/Cursor/Codex
├── pyproject.toml        # Package definition & build configuration
└── Makefile              # Shortcut commands for local development
```

---

## 📏 Coding Standards & Rules

* **Python Code Style**:
  * Follow PEP 8 guidelines.
  * Use clear type hints (`from typing import Optional, List, Dict`).
  * Standard library imports only for runtime modules.
* **Test Coverage**:
  * Write unit tests for new features and bug fixes in `tests/`.
  * Ensure existing tests pass before submitting PRs.
* **Installer Scripts**:
  * If updating installation logic, update both `scripts/install.sh` and `scripts/install.ps1` to ensure parity between macOS/Linux and Windows.
* **Agent Skill (`SKILL.md`)**:
  * Keep agent instructions concise, clear, and actionable.

---

## 📥 Submitting a Pull Request

1. **Create a Feature Branch**:
   ```bash
   git checkout -b feat/your-feature-name
   # or
   git checkout -b fix/your-bug-fix
   ```

2. **Commit Your Changes**:
   Use descriptive commit messages (following Conventional Commits format when possible):
   * `feat: add search filtering by category`
   * `fix: handle empty tag list in memory renderer`
   * `docs: update installation instructions`

3. **Push to Your Fork**:
   ```bash
   git push origin feat/your-feature-name
   ```

4. **Open a Pull Request**:
   * Fill out the [Pull Request Template](.github/PULL_REQUEST_TEMPLATE.md).
   * Reference any relevant issue numbers (e.g., `Fixes #42`).
   * Ensure all CI checks pass.

---

## 🐛 Reporting Issues

* **Bug Reports**: Open an issue using our [Bug Report Template](.github/ISSUE_TEMPLATE/bug_report.yml).
* **Feature Requests**: Open an issue using our [Feature Request Template](.github/ISSUE_TEMPLATE/feature_request.yml).
* **Security Concerns**: Please report security vulnerabilities privately according to our [Security Policy](SECURITY.md).

Thank you for helping make `remembrandt` better! 🚀
