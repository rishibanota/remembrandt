"""Command-line interface for remembrandt."""

from __future__ import annotations

import argparse
import json
import sys
from typing import List, Optional

from agent_memory.store import CATEGORIES, MemoryStore


def _print_entry(e, index=None) -> None:
    prefix = f"{index:>3}. " if index is not None else ""
    created = (e.created_at or "").replace("T", " ")[:16]
    tags = " ".join("#" + t for t in e.tags)
    print(f"{prefix}[{e.id}] ({e.category}) {created}")
    print(f"{'':>{len(prefix)}}  {e.content}")
    if tags:
        print(f"{'':>{len(prefix)}}  {tags}")


def cmd_remember(args, store: MemoryStore) -> int:
    tags = [t for t in (args.tags or []) if t]
    e = store.add(args.content, category=args.category, tags=tags, source="cli")
    print(f"Remembered entry #{e.id} in '{e.category}'.")
    return 0


def cmd_recall(args, store: MemoryStore) -> int:
    entries = store.list(category=args.category) if args.category else store.list()
    if not entries:
        print("Nothing remembered yet. Use `remembrandt remember <text>`.")
        return 0
    for i, e in enumerate(entries, 1):
        _print_entry(e, i)
    print(f"\n{len(entries)} entr{'y' if len(entries) == 1 else 'ies'} total.")
    return 0


def cmd_search(args, store: MemoryStore) -> int:
    entries = store.search(args.query)
    if not entries:
        print(f"No matches for {args.query!r}.")
        return 0
    for i, e in enumerate(entries, 1):
        _print_entry(e, i)
    print(f"\n{len(entries)} match{'es' if len(entries) == 1 else ''}.")
    return 0


def cmd_resume(args, store: MemoryStore) -> int:
    path = store.write_resume(title=args.title)
    print(f"Wrote {path}")
    print("-" * 60)
    print(store.resume(args.title))
    return 0


def cmd_status(args, store: MemoryStore) -> int:
    st = store.status()
    print(f"Store:   {st['dir']}")
    print(f"Exists:  {'yes' if st['exists'] else 'no'}")
    print(f"Entries: {st['entries']}")
    if st["categories"]:
        for cat, n in sorted(st["categories"].items()):
            print(f"  - {cat}: {n}")
    return 0


def cmd_forget(args, store: MemoryStore) -> int:
    removed = 0
    for eid in args.id:
        if store.delete(eid):
            removed += 1
    print(f"Forgot {removed} entr{'y' if removed == 1 else 'ies'}.")
    return 0


def cmd_edit(args, store: MemoryStore) -> int:
    e = store.get(args.id)
    if e is None:
        print(f"No entry #{args.id}.")
        return 1
    content = args.content if args.content is not None else e.content
    category = args.category if args.category is not None else e.category
    tags = args.tags if args.tags is not None else e.tags
    updated = store.update(args.id, content=content, category=category, tags=tags)
    print(f"Updated entry #{updated.id}." if updated else "Update failed.")
    return 0


def cmd_reset(args, store: MemoryStore) -> int:
    n = store.reset()
    print(f"Cleared {n} entr{'y' if n == 1 else 'ies'}.")
    return 0


def cmd_export(args, store: MemoryStore) -> int:
    entries = [e.to_dict() for e in store.list()]
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(entries, f, indent=2)
        print(f"Exported {len(entries)} entries to {args.output}")
    else:
        print(json.dumps(entries, indent=2))
    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="remembrandt",
        description="Persistent memory for coding agents. Never forgets.",
    )
    p.add_argument("--dir", help="Override the memory store directory.")
    sub = p.add_subparsers(dest="command", required=True)

    r = sub.add_parser("remember", help="Store a new memory.")
    r.add_argument("content", help="What to remember.")
    r.add_argument("-c", "--category", default="note",
                   choices=list(CATEGORIES) + ["custom"],
                   help="Category of the memory.")
    r.add_argument("-t", "--tags", nargs="*", help="Optional space-separated tags.")
    r.add_argument("--custom-category", dest="custom_category",
                   help="A custom category name (only when -c custom).")
    r.set_defaults(func=cmd_remember)

    rc = sub.add_parser("recall", help="List memories (newest first).")
    rc.add_argument("category", nargs="?", help="Filter by category.")
    rc.set_defaults(func=cmd_recall)

    s = sub.add_parser("search", help="Search memories.")
    s.add_argument("query", help="Text to search for.")
    s.set_defaults(func=cmd_search)

    rs = sub.add_parser("resume", help="Generate a human/MEMORY.md resume file.")
    rs.add_argument("--title", default="Project Memory",
                    help="Heading for the compiled memory file.")
    rs.set_defaults(func=cmd_resume)

    st = sub.add_parser("status", help="Show store stats.")
    st.set_defaults(func=cmd_status)

    f = sub.add_parser("forget", help="Delete one or more entries by id.")
    f.add_argument("id", type=int, nargs="+", help="Entry id(s) to delete.")
    f.set_defaults(func=cmd_forget)

    e = sub.add_parser("edit", help="Edit an existing entry.")
    e.add_argument("id", type=int, help="Entry id to edit.")
    e.add_argument("--content", help="New content.")
    e.add_argument("--category", help="New category.")
    e.add_argument("--tags", nargs="*", help="New tags.")
    e.set_defaults(func=cmd_edit)

    rst = sub.add_parser("reset", help="Delete ALL memories. Use with care.")
    rst.set_defaults(func=cmd_reset)

    ex = sub.add_parser("export", help="Export all entries as JSON.")
    ex.add_argument("-o", "--output", help="Write to a file instead of stdout.")
    ex.set_defaults(func=cmd_export)

    return p


def main(argv: Optional[List[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    store = MemoryStore(root=args.dir if getattr(args, "dir", None) else None)

    # Resolve custom category
    if getattr(args, "category", None) == "custom":
        custom = getattr(args, "custom_category", None)
        if not custom:
            parser.error("--custom-category is required when using -c custom.")
        args.category = custom

    try:
        return args.func(args, store)
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    except KeyboardInterrupt:
        return 130


if __name__ == "__main__":
    raise SystemExit(main())
