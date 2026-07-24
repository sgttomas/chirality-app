import json
import sys
from argparse import Namespace
from pathlib import Path

import pytest

import tools.retrieval.query_source_index as query_tool


def make_args(mode: str, **overrides) -> Namespace:
    data = {
        "mode": mode,
        "source_doc": None,
        "artifact_role": None,
        "chunk_type": None,
        "audit_kind": None,
        "category_id": None,
        "knowledge_type_id": None,
        "subject_id": None,
        "archive_state": "ACTIVE",
    }
    data.update(overrides)
    return Namespace(**data)


def make_build(tmp_path: Path, *, dense: bool = True) -> dict:
    if dense:
        (tmp_path / "embeddings_norm.npy").write_bytes(b"")
    return {
        "row_count": 1000,
        "embeddings_norm_path": "embeddings_norm.npy",
        "embedding_model": "test-model",
    }


def test_default_mode_is_hybrid():
    args = query_tool.build_arg_parser().parse_args(["--query", "x"])

    assert args.mode == "hybrid"


def test_hybrid_mode_calls_bm25_dense_and_rrf(monkeypatch, tmp_path):
    calls = []
    args = make_args("hybrid")
    build = make_build(tmp_path)

    monkeypatch.setattr(query_tool, "allowed_rows", lambda snapshot, args: None)

    def fake_bm25(snapshot, query, k, allowed):
        calls.append(("bm25", query, k, allowed))
        return [(1, 9.0), (2, 8.0)]

    def fake_dense(snapshot, query, k, allowed, build):
        calls.append(("dense", query, k, allowed))
        return [(2, 0.8), (3, 0.7)]

    def fake_rrf(bm25_hits, dense_hits, k):
        calls.append(("rrf", bm25_hits, dense_hits, k))
        return [(2, 0.25, 2, 1)]

    def fake_hydrate(snapshot, ranked, bm25_hits, dense_hits):
        calls.append(("hydrate", ranked, bm25_hits, dense_hits))
        return [{"chunk_id": "CHK-2"}]

    monkeypatch.setattr(query_tool, "bm25_topk", fake_bm25)
    monkeypatch.setattr(query_tool, "dense_topk", fake_dense)
    monkeypatch.setattr(query_tool, "rrf", fake_rrf)
    monkeypatch.setattr(query_tool, "hydrate", fake_hydrate)

    hits = query_tool.query_one(tmp_path, "needle", 2, build, args)

    assert hits == [{"chunk_id": "CHK-2"}]
    assert [c[0] for c in calls] == ["bm25", "dense", "rrf", "hydrate"]
    assert calls[2] == ("rrf", [(1, 9.0), (2, 8.0)], [(2, 0.8), (3, 0.7)], 2)


def test_dense_mode_calls_only_dense(monkeypatch, tmp_path):
    args = make_args("dense")
    build = make_build(tmp_path)

    monkeypatch.setattr(query_tool, "allowed_rows", lambda snapshot, args: None)
    monkeypatch.setattr(
        query_tool,
        "bm25_topk",
        lambda *a, **k: pytest.fail("bm25_topk should not run in dense mode"),
    )

    def fake_dense(snapshot, query, k, allowed, build):
        return [(3, 0.9), (4, 0.8), (5, 0.7)]

    def fake_hydrate(snapshot, ranked, bm25_hits, dense_hits):
        assert ranked == [(3, None, None, 1), (4, None, None, 2)]
        assert bm25_hits == []
        assert dense_hits == [(3, 0.9), (4, 0.8), (5, 0.7)]
        return [{"chunk_id": "CHK-3"}, {"chunk_id": "CHK-4"}]

    monkeypatch.setattr(query_tool, "dense_topk", fake_dense)
    monkeypatch.setattr(query_tool, "hydrate", fake_hydrate)

    hits = query_tool.query_one(tmp_path, "semantic", 2, build, args)

    assert [h["chunk_id"] for h in hits] == ["CHK-3", "CHK-4"]


def test_bm25_mode_calls_only_bm25(monkeypatch, tmp_path):
    args = make_args("bm25")
    build = make_build(tmp_path)

    monkeypatch.setattr(query_tool, "allowed_rows", lambda snapshot, args: None)
    monkeypatch.setattr(
        query_tool,
        "dense_topk",
        lambda *a, **k: pytest.fail("dense_topk should not run in bm25 mode"),
    )

    def fake_bm25(snapshot, query, k, allowed):
        return [(7, 12.0), (8, 11.0), (9, 10.0)]

    def fake_hydrate(snapshot, ranked, bm25_hits, dense_hits):
        assert ranked == [(7, None, 1, None), (8, None, 2, None)]
        assert bm25_hits == [(7, 12.0), (8, 11.0), (9, 10.0)]
        assert dense_hits == []
        return [{"chunk_id": "CHK-7"}, {"chunk_id": "CHK-8"}]

    monkeypatch.setattr(query_tool, "bm25_topk", fake_bm25)
    monkeypatch.setattr(query_tool, "hydrate", fake_hydrate)

    hits = query_tool.query_one(tmp_path, "lexical", 2, build, args)

    assert [h["chunk_id"] for h in hits] == ["CHK-7", "CHK-8"]


def test_dense_mode_errors_when_embeddings_are_absent(monkeypatch, tmp_path):
    args = make_args("dense")
    build = make_build(tmp_path, dense=False)

    monkeypatch.setattr(query_tool, "allowed_rows", lambda snapshot, args: None)
    monkeypatch.setattr(
        query_tool,
        "dense_topk",
        lambda *a, **k: pytest.fail("dense_topk should not run without embeddings"),
    )

    with pytest.raises(RuntimeError, match="dense embeddings are not built"):
        query_tool.query_one(tmp_path, "semantic", 2, build, args)


def test_filters_flow_to_allowed_rows(monkeypatch, tmp_path):
    args = make_args("bm25", category_id="CAT-001", chunk_type="LEDGER_ATOM")
    build = make_build(tmp_path)
    seen = {}

    def fake_allowed(snapshot, passed_args):
        seen["category_id"] = passed_args.category_id
        seen["chunk_type"] = passed_args.chunk_type
        return {1}

    def fake_bm25(snapshot, query, k, allowed):
        assert allowed == {1}
        return [(1, 4.0)]

    monkeypatch.setattr(query_tool, "allowed_rows", fake_allowed)
    monkeypatch.setattr(query_tool, "bm25_topk", fake_bm25)
    monkeypatch.setattr(query_tool, "hydrate", lambda *a: [{"chunk_id": "CHK-1"}])

    query_tool.query_one(tmp_path, "filtered", 1, build, args)

    assert seen == {"category_id": "CAT-001", "chunk_type": "LEDGER_ATOM"}


def test_json_output_includes_mode(monkeypatch, capsys):
    monkeypatch.setattr(sys, "argv", ["query_source_index.py", "--query", "x", "--json", "--mode", "dense"])
    monkeypatch.setattr(query_tool, "resolve_snapshot_path", lambda snapshot, domain_root: Path("/snapshot"))
    monkeypatch.setattr(query_tool, "load_index_build", lambda snapshot: {"row_count": 1})

    def fake_query_one(snapshot, query, k, build, args):
        assert args.mode == "dense"
        return [{"chunk_id": "CHK-1"}]

    monkeypatch.setattr(query_tool, "query_one", fake_query_one)

    assert query_tool.main() == 0
    payload = json.loads(capsys.readouterr().out)

    assert payload["mode"] == "dense"
    assert payload["results"] == [{"chunk_id": "CHK-1"}]


def test_render_filters_skips_default_archive_state():
    args = make_args("bm25", category_id="CAT-001", chunk_type="LEDGER_ATOM")
    rendered = query_tool.render_filters(args)
    assert "category_id=CAT-001" in rendered
    assert "chunk_type=LEDGER_ATOM" in rendered
    assert "archive_state" not in rendered  # ACTIVE is the default, omitted


def test_log_query_writes_header_once_then_appends(tmp_path):
    log = tmp_path / "Query_Log.csv"
    common = dict(snapshot=Path("/snap/SRCIDX_X"), domain_root="domains/d",
                  mode="bm25", filters="", k=3, utc="2026-01-01T00:00:00Z")
    query_tool.log_query(log, query="alpha", result_count=2, **common)
    query_tool.log_query(log, query="beta", result_count=0, **common)
    lines = log.read_text(encoding="utf-8").splitlines()
    assert lines[0] == ",".join(query_tool.QUERY_LOG_COLUMNS)
    assert len(lines) == 3  # header + 2 rows
    assert lines[1].split(",")[query_tool.QUERY_LOG_COLUMNS.index("ResultCount")] == "2"
    assert lines[1].split(",")[query_tool.QUERY_LOG_COLUMNS.index("Snapshot")] == "SRCIDX_X"


def test_main_run_log_records_one_row_per_query(monkeypatch, tmp_path):
    log = tmp_path / "Query_Log.csv"
    monkeypatch.setattr(sys, "argv", [
        "query_source_index.py", "--query", "needle", "--mode", "bm25", "--json", "--run-log", str(log),
    ])
    monkeypatch.setattr(query_tool, "resolve_snapshot_path", lambda snapshot, domain_root: Path("/snapshot"))
    monkeypatch.setattr(query_tool, "load_index_build", lambda snapshot: {"row_count": 1})
    monkeypatch.setattr(query_tool, "query_one", lambda *a, **k: [{"chunk_id": "C1"}, {"chunk_id": "C2"}])

    assert query_tool.main() == 0
    lines = log.read_text(encoding="utf-8").splitlines()
    assert len(lines) == 2  # header + 1 row
    row = lines[1].split(",")
    assert row[query_tool.QUERY_LOG_COLUMNS.index("ResultCount")] == "2"
    assert row[query_tool.QUERY_LOG_COLUMNS.index("Query")] == "needle"


def test_run_log_and_log_dir_are_mutually_exclusive(monkeypatch, capsys):
    monkeypatch.setattr(sys, "argv", [
        "query_source_index.py", "--query", "x", "--run-log", "/tmp/a.csv", "--log-dir", "/tmp",
    ])
    with pytest.raises(SystemExit):
        query_tool.main()
