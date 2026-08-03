#!/usr/bin/env bash
# Install the remembrandt CLI and register it as a Claude Code skill.
# Usage:  bash scripts/install.sh   (or:  make install)
set -euo pipefail

# --- 1. Install the CLI (editable) so `remembrandt` is on PATH ---
echo ">> Installing remembrandt CLI..."
if command -v pip3 >/dev/null 2>&1; then
  pip3 install -e "$(cd "$(dirname "$0")/.." && pwd)"
else
  echo "!! pip3 not found. Install Python 3 and retry, or run from the repo "
  echo "   using:  python -m agent_memory <command>"
fi

# --- 2. Register the Claude Code skill ---
SKILLS_DIR="${CLAUDE_SKILLS_DIR:-$HOME/.claude/skills}"
TARGET="$SKILLS_DIR/remembrandt"
if [ -f "SKILL.md" ]; then
  mkdir -p "$SKILLS_DIR"
  cp -r . "$TARGET" 2>/dev/null || cp SKILL.md "$TARGET/"
  echo ">> Claude Code skill installed at $TARGET"
else
  echo ">> SKILL.md not found next to installer; skipping skill registration."
  echo "   (Create $SKILLS_DIR/remembrandt/SKILL.md manually.)"
fi

echo ">> Done. Try:  remembrandt remember 'hello world' && remembrandt recall"
