"""Data model and persistence layer for remembrandt.

The memory store is deliberately simple and debuggable:
a directory of tiny JSON files (one per entry) plus an optional
human-readable MEMORY.md compiled from them. No database, no server.
"""

from __future__ import annotations

import json
import os
import re
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Optional

CATEGORIES = ("decision", "changelog", "gotcha", "note", "context")

# Recommended prefix, but any non-empty, lowercase, ASCII name is allowed.
_CATEGORY_RE = re.compile(r"^[a-z][a-z0-9_-]{0,30}$")

DEFAULT_DIR = ".remembrandt"
ENTRIES_DIR = "entries"
MEMORY_FILE = "MEMORY.md"
INDEX_FILE = "index.json"


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


@dataclass
class Entry:
    category: str
    content: str
    tags: List[str] = field(default_factory=list)
    source: str = "cli"
    id: Optional[int] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "category": self.category,
            "content": self.content,
            "tags": sorted(set(self.tags)),
            "source": self.source,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }

    @classmethod
    def from_dict(cls, d: dict) -> "Entry":
        return cls(
            id=d.get("id"),
            category=d.get("category", "note"),
            content=d.get("content", ""),
            tags=list(d.get("tags", [])),
            source=d.get("source", "cli"),
            created_at=d.get("created_at"),
            updated_at=d.get("updated_at"),
        )


def validate_category(category: str) -> str:
    c = (category or "").strip().lower()
    if not _CATEGORY_RE.match(c):
        raise ValueError(
            f"Invalid category {category!r}. Use lowercase letters, digits, "
            f"dashes or underscores (e.g. {', '.join(CATEGORIES)})."
        )
    return c


class MemoryStore:
    """File-backed, append-friendly memory store."""

    def __init__(self, root: Optional[Path] = None):
        env = os.environ.get("REMBRANDT_DIR")
        if env:
            root = Path(env).expanduser().resolve()
        elif root is None:
            root = Path.cwd() / DEFAULT_DIR
        self.root = Path(root)
        self.entries_dir = self.root / ENTRIES_DIR

    # ----- lifecycle -----
    def ensure(self) -> None:
        self.entries_dir.mkdir(parents=True, exist_ok=True)

    def exists(self) -> bool:
        return self.entries_dir.is_dir()

    # ----- entry files -----
    def _next_id(self) -> int:
        highest = 0
        for p in self.entries_dir.glob("*.json"):
            try:
                highest = max(highest, int(p.stem))
            except ValueError:
                continue
        return highest + 1

    def _entry_path(self, entry_id: int) -> Path:
        return self.entries_dir / f"{entry_id:05d}.json"

    # ----- operations -----
    def add(
        self,
        content: str,
        category: str = "note",
        tags: Optional[List[str]] = None,
        source: str = "cli",
    ) -> Entry:
        content = (content or "").strip()
        if not content:
            raise ValueError("Content cannot be empty.")
        category = validate_category(category)
        self.ensure()
        entry = Entry(
            id=self._next_id(),
            category=category,
            content=content,
            tags=[t.strip().lstrip("#") for t in (tags or []) if t.strip()],
            source=source,
            created_at=now_iso(),
            updated_at=now_iso(),
        )
        self._write(entry)
        return entry

    def _write(self, entry: Entry) -> None:
        tmp = self._entry_path(entry.id).with_suffix(".tmp")
        tmp.write_text(json.dumps(entry.to_dict(), indent=2), encoding="utf-8")
        os.replace(tmp, self._entry_path(entry.id))

    def list(self, category: Optional[str] = None) -> List[Entry]:
        if not self.exists():
            return []
        entries: List[Entry] = []
        for p in sorted(self.entries_dir.glob("*.json")):
            try:
                entry = Entry.from_dict(json.loads(p.read_text(encoding="utf-8")))
            except (json.JSONDecodeError, OSError):
                continue
            if category and entry.category != category:
                continue
            entries.append(entry)
        # newest first
        entries.sort(key=lambda e: e.id or 0, reverse=True)
        return entries

    def get(self, entry_id: int) -> Optional[Entry]:
        p = self._entry_path(entry_id)
        if not p.exists():
            return None
        try:
            return Entry.from_dict(json.loads(p.read_text(encoding="utf-8")))
        except (json.JSONDecodeError, OSError):
            return None

    def update(self, entry_id: int, content: Optional[str] = None,
               category: Optional[str] = None,
               tags: Optional[List[str]] = None) -> Optional[Entry]:
        entry = self.get(entry_id)
        if entry is None:
            return None
        if content is not None:
            content = content.strip()
            if not content:
                raise ValueError("Content cannot be empty.")
            entry.content = content
        if category is not None:
            entry.category = validate_category(category)
        if tags is not None:
            entry.tags = sorted({t.strip().lstrip("#") for t in tags if t.strip()})
        entry.updated_at = now_iso()
        self._write(entry)
        return entry

    def delete(self, entry_id: int) -> bool:
        p = self._entry_path(entry_id)
        if p.exists():
            p.unlink()
            return True
        return False

    def search(self, query: str) -> List[Entry]:
        q = (query or "").strip().lower()
        if not q:
            return self.list()
        results = []
        for e in self.list():
            haystack = " ".join(
                [e.content, e.category, *e.tags]
            ).lower()
            if q in haystack:
                results.append(e)
        return results

    def count(self) -> int:
        if not self.exists():
            return 0
        return len(list(self.entries_dir.glob("*.json")))

    # ----- compiled resume -----
    def resume(self, title: str = "Project Memory") -> str:
        entries = self.list()
        if not entries:
            return (
                f"# {title}\n\n"
                "_No entries yet. Start capturing with "
                "`remembrandt remember <category> <text>`._\n"
            )
        lines = [f"# {title}", ""]
        order = CATEGORIES + ("other",)
        grouped: dict = {}
        for e in entries:
            key = e.category if e.category in order else "other"
            grouped.setdefault(key, []).append(e)
        for cat in order:
            if cat not in grouped:
                continue
            lines.append(f"## {cat.capitalize()}")
            lines.append("")
            for e in grouped[cat]:
                ts = (e.created_at or "")[:10]
                tagline = f" _{' '.join('#' + t for t in e.tags)}_" if e.tags else ""
                lines.append(f"- **{e.id}** [{ts}] {e.content}{tagline}")
            lines.append("")
        return "\n".join(lines).rstrip() + "\n"

    def write_resume(self, title: str = "Project Memory") -> Path:
        self.ensure()
        path = self.root / MEMORY_FILE
        path.write_text(self.resume(title), encoding="utf-8")
        return path

    def status(self) -> dict:
        return {
            "dir": str(self.root),
            "exists": self.exists(),
            "entries": self.count(),
            "categories": self._category_counts(),
        }

    def _category_counts(self) -> dict:
        counts: dict = {}
        for e in self.list():
            counts[e.category] = counts.get(e.category, 0) + 1
        return counts

    def reset(self) -> int:
        n = 0
        if self.exists():
            for p in self.entries_dir.glob("*.json"):
                p.unlink()
                n += 1
        return n
