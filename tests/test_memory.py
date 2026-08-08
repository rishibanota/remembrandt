"""Tests for the remembrandt memory store and CLI."""

import json
import subprocess
import sys
from pathlib import Path

import pytest

from agent_memory.store import CATEGORIES, MemoryStore, validate_category


# ---------------------------------------------------------------- fixtures
@pytest.fixture()
def store(tmp_path):
    return MemoryStore(root=tmp_path / "mem")


# ------------------------------------------------------------------- store
def test_add_and_get(store):
    e = store.add("Use uv for deps", category="decision", tags=["uv", "tooling"])
    assert e.id == 1
    got = store.get(1)
    assert got is not None
    assert got.category == "decision"
    assert got.content == "Use uv for deps"
    assert set(got.tags) == {"uv", "tooling"}
    assert got.created_at and got.updated_at


def test_ids_increment(store):
    a = store.add("one")
    b = store.add("two")
    assert a.id == 1
    assert b.id == 2


def test_empty_content_rejected(store):
    with pytest.raises(ValueError):
        store.add("   ")


def test_invalid_category_rejected(store):
    with pytest.raises(ValueError):
        store.add("x", category="has space")


def test_custom_category_allowed(store):
    e = store.add("x", category="my-custom_thing")
    assert e.category == "my-custom_thing"


def test_list_newest_first(store):
    store.add("first")
    store.add("second")
    store.add("third")
    ids = [e.id for e in store.list()]
    assert ids == [3, 2, 1]


def test_list_filter_by_category(store):
    store.add("dec", category="decision")
    store.add("note", category="note")
    got = store.list(category="decision")
    assert [e.content for e in got] == ["dec"]


def test_search(store):
    store.add("Use uv for dependency management", category="decision", tags=["uv"])
    store.add("Refactor auth to JWT", category="changelog")
    assert len(store.search("uv")) == 1
    assert len(store.search("auth")) == 1
    assert store.search("nothing") == []


def test_delete(store):
    store.add("temp")
    assert store.delete(1) is True
    assert store.get(1) is None
    assert store.delete(999) is False


def test_update(store):
    store.add("old", category="note")
    e = store.update(1, content="new content", category="decision", tags=["a"])
    assert e.content == "new content"
    assert e.category == "decision"
    assert e.tags == ["a"]


def test_reset(store):
    store.add("a")
    store.add("b")
    assert store.reset() == 2
    assert store.count() == 0


def test_resume_renders_sections(store):
    store.add("Decision A", category="decision")
    store.add("Gotcha B", category="gotcha")
    md = store.resume()
    assert "# Project Memory" in md
    assert "## Decision" in md
    assert "## Gotcha" in md
    assert "Decision A" in md
    assert "Gotcha B" in md


def test_write_resume_creates_file(store):
    store.add("x")
    path = store.write_resume()
    assert path.exists()
    assert "Project Memory" in path.read_text()


def test_status(store):
    store.add("a", category="note")
    st = store.status()
    assert st["entries"] == 1
    assert st["categories"]["note"] == 1


def test_validate_category_defaults():
    assert validate_category("decision") == "decision"
    assert validate_category(" DECISION ") == "decision"


def test_categories_are_valid():
    for c in CATEGORIES:
        assert validate_category(c) == c


import os


# -------------------------------------------------------------------- cli
def run_cli(tmp_path, *args):
    env = os.environ.copy()
    env["REMBRANDT_DIR"] = str(tmp_path / "mem")
    src_dir = str(Path(__file__).parent.parent / "src")
    env["PYTHONPATH"] = f"{src_dir}{os.pathsep}{env.get('PYTHONPATH', '')}"
    return subprocess.run(
        [sys.executable, "-m", "agent_memory", *args],
        capture_output=True,
        text=True,
        env=env,
    )


def test_cli_remember_recall(tmp_path):
    r = run_cli(tmp_path, "remember", "hello world", "-c", "note")
    assert r.returncode == 0
    assert "Remembered entry #1" in r.stdout

    r2 = run_cli(tmp_path, "recall")
    assert r2.returncode == 0
    assert "hello world" in r2.stdout


def test_cli_search(tmp_path):
    run_cli(tmp_path, "remember", "Use uv for deps", "-t", "uv")
    r = run_cli(tmp_path, "search", "uv")
    assert "Use uv for deps" in r.stdout


def test_cli_status(tmp_path):
    run_cli(tmp_path, "remember", "x")
    r = run_cli(tmp_path, "status")
    assert "Entries: 1" in r.stdout


def test_cli_export(tmp_path):
    run_cli(tmp_path, "remember", "data point", "-c", "decision")
    r = run_cli(tmp_path, "export")
    data = json.loads(r.stdout)
    assert data[0]["category"] == "decision"


def test_cli_custom_category(tmp_path):
    r = run_cli(tmp_path, "remember", "y", "-c", "custom",
                "--custom-category", "mycat")
    assert r.returncode == 0
    r2 = run_cli(tmp_path, "recall", "mycat")
    assert "y" in r2.stdout


def test_cli_invalid_category_fails(tmp_path):
    r = run_cli(tmp_path, "remember", "x", "-c", "bad category")
    assert r.returncode == 2


def test_cli_help(tmp_path):
    r = run_cli(tmp_path, "--help")
    assert r.returncode == 0
    assert "remembrandt" in r.stdout
