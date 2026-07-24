import json
import sqlite3
import sys

import tools.source_catalog.check_snapshot_freshness as fresh
from tools.source_catalog.source_database import sha256_file


def build_fixture(tmp_path):
    """A minimal snapshot: domain source file + catalog.sqlite(artifacts) + meta.json."""
    domain_root = tmp_path / "domain"
    (domain_root / "src").mkdir(parents=True)
    src = domain_root / "src" / "a.md"
    src.write_text("hello world\n", encoding="utf-8")

    snapshot = tmp_path / "snap"
    snapshot.mkdir()
    con = sqlite3.connect(str(snapshot / "catalog.sqlite"))
    con.execute("CREATE TABLE artifacts (artifact_id TEXT, rel_path TEXT, sha256 TEXT)")
    con.execute(
        "INSERT INTO artifacts VALUES (?, ?, ?)",
        ("ART-1", "src/a.md", sha256_file(src)),
    )
    con.commit()
    con.close()
    (snapshot / "meta.json").write_text(
        json.dumps({"build_utc": "2026-01-01T00:00:00Z", "domain_root": str(domain_root)}),
        encoding="utf-8",
    )
    return snapshot, src


def run(snapshot, monkeypatch):
    monkeypatch.setattr(sys, "argv", ["check_snapshot_freshness.py", "--snapshot", str(snapshot), "--json"])
    return fresh.main()


def test_fresh_when_source_unchanged(tmp_path, monkeypatch, capsys):
    snapshot, _src = build_fixture(tmp_path)
    rc = run(snapshot, monkeypatch)
    payload = json.loads(capsys.readouterr().out)
    assert rc == 0
    assert payload["verdict"] == "FRESH"
    assert payload["counts"]["changed"] == 0
    assert payload["counts"]["missing"] == 0


def test_stale_when_source_changes(tmp_path, monkeypatch, capsys):
    snapshot, src = build_fixture(tmp_path)
    src.write_text("hello CHANGED world\n", encoding="utf-8")
    rc = run(snapshot, monkeypatch)
    payload = json.loads(capsys.readouterr().out)
    assert rc == 1
    assert payload["verdict"] == "STALE"
    assert payload["counts"]["changed"] == 1


def test_stale_when_source_missing(tmp_path, monkeypatch, capsys):
    snapshot, src = build_fixture(tmp_path)
    src.unlink()
    rc = run(snapshot, monkeypatch)
    payload = json.loads(capsys.readouterr().out)
    assert rc == 1
    assert payload["verdict"] == "STALE"
    assert payload["counts"]["missing"] == 1
