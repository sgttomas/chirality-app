#!/usr/bin/env python3
"""Query a Chirality source database V2 snapshot.

Usage:
  python3 tools/retrieval/query_source_index.py \
      --snapshot domains/piping-design/_LocalIndexes/_LATEST.md \
      --query "support spacing for steam lines" --k 10

Inputs:
  --snapshot           Snapshot directory or _LATEST.md pointer.
  --query              Single query string.
  --batch              CSV with a `query` column.
  --mode               Retrieval mode: hybrid, dense, or bm25.
  --json               Emit JSON.

Filters:
  --source-doc
  --artifact-role
  --chunk-type
  --audit-kind
  --category-id
  --knowledge-type-id
  --subject-id
  --archive-state      ACTIVE or ARCHIVE. Default ACTIVE.

Returns stable chunk/artifact IDs and provenance paths. Internal row indices are
not part of the public result contract.
"""
from __future__ import annotations

import argparse
import csv
import json
import sqlite3
import sys
from datetime import datetime, timezone
from functools import lru_cache
from pathlib import Path

import numpy as np

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "tools" / "source_catalog"))
from source_database import DEFAULT_DOMAIN_ROOT, resolve_snapshot_path, stable_id  # noqa: E402
from research_packet import QUERY_LOG_COLUMNS  # noqa: E402

INDEX_NAME = "source_v2"
RRF_K = 60

FILTER_ARG_KEYS = [
    "source_doc", "artifact_role", "chunk_type", "audit_kind",
    "category_id", "knowledge_type_id", "subject_id", "archive_state",
]


def render_filters(args: argparse.Namespace) -> str:
    """Compact `k=v;k=v` rendering of the non-default filter args."""
    parts = []
    for key in FILTER_ARG_KEYS:
        val = getattr(args, key, None)
        if val and not (key == "archive_state" and val == "ACTIVE"):
            parts.append(f"{key}={val}")
    return ";".join(parts)


def resolve_domain_label(snapshot: Path, fallback: Path) -> str:
    """Best-effort repo-relative domain root for the Query_Log, from the snapshot's meta.json."""
    meta_path = snapshot / "meta.json"
    if meta_path.exists():
        try:
            md = json.loads(meta_path.read_text(encoding="utf-8")).get("domain_root")
            if md:
                try:
                    return str(Path(md).resolve().relative_to(REPO_ROOT))
                except ValueError:
                    return str(md)
        except Exception:
            pass
    return str(fallback)


def log_query(
    log_path: Path,
    *,
    snapshot: Path,
    domain_root: Path,
    mode: str,
    query: str,
    filters: str,
    k: int,
    result_count: int,
    utc: str,
) -> None:
    """Append one canonical Query_Log.csv row. Header is written once."""
    row = {
        "QueryID": stable_id("Q", utc, str(snapshot), query, mode, filters),
        "UTC": utc,
        "DomainRoot": str(domain_root),
        "Snapshot": Path(snapshot).name,
        "Mode": mode,
        "Query": query,
        "Filters": filters,
        "K": k,
        "ResultCount": result_count,
        "Notes": "",
    }
    new_file = not log_path.exists()
    log_path.parent.mkdir(parents=True, exist_ok=True)
    with log_path.open("a", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=QUERY_LOG_COLUMNS, extrasaction="ignore")
        if new_file:
            writer.writeheader()
        writer.writerow(row)


def main() -> int:
    ap = build_arg_parser()
    args = ap.parse_args()

    if not args.query and not args.batch:
        ap.error("provide --query or --batch")

    if args.run_log and args.log_dir:
        ap.error("--run-log and --log-dir are mutually exclusive")

    try:
        snapshot = resolve_snapshot_path(args.snapshot, args.domain_root)
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    log_path: Path | None = None
    if args.run_log:
        log_path = args.run_log
    elif args.log_dir:
        log_path = args.log_dir / "Query_Log.csv"
    if log_path is not None:
        # Snapshots are immutable; never write a run log inside one.
        resolved = log_path.resolve()
        if resolved == snapshot or snapshot in resolved.parents:
            print(
                f"ERROR: refusing to write query log inside the immutable snapshot: {resolved}",
                file=sys.stderr,
            )
            return 2

    try:
        build = load_index_build(snapshot)
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    queries = collect_queries(args)
    filters = render_filters(args)
    domain_label = resolve_domain_label(snapshot, args.domain_root) if log_path else ""
    results = []
    for tag, query in queries:
        try:
            hits = query_one(snapshot, query, args.k, build, args)
        except RuntimeError as exc:
            print(f"ERROR: {exc}", file=sys.stderr)
            return 2
        if log_path is not None:
            log_query(
                log_path,
                snapshot=snapshot,
                domain_root=domain_label,
                mode=args.mode,
                query=query,
                filters=filters,
                k=args.k,
                result_count=len(hits),
                utc=datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            )
        results.append({"tag": tag, "query": query, "mode": args.mode, "results": hits})

    if args.emit_json:
        print(json.dumps(results if args.batch else results[0], indent=2))
    else:
        for payload in results:
            mode = payload["mode"]
            print(f"QUERY {payload['tag']} [mode={mode}]: {payload['query']}")
            for i, hit in enumerate(payload["results"], start=1):
                if mode == "dense":
                    score = hit.get("cosine_score")
                elif mode == "bm25":
                    score = hit.get("bm25_score")
                else:
                    score = hit.get("rrf_score")
                bm = hit.get("bm25_rank")
                dn = hit.get("dense_rank")
                print(
                    f"{i:02d}. score={score} bm25={bm} dense={dn} "
                    f"{hit['chunk_id']} {hit['chunk_type']} {hit['rel_path']}"
                )
                preview = (hit.get("text_preview") or "").replace("\n", " ")
                if preview:
                    print(f"    {preview[:220]}")
    return 0


def build_arg_parser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--snapshot", type=Path)
    ap.add_argument("--domain-root", type=Path, default=DEFAULT_DOMAIN_ROOT)
    ap.add_argument("--query")
    ap.add_argument("--batch", type=Path)
    ap.add_argument("--k", type=int, default=15)
    ap.add_argument(
        "--mode",
        choices=("hybrid", "dense", "bm25"),
        default="hybrid",
        help="Retrieval mode. hybrid fuses BM25 and dense ranks; dense uses cosine only; bm25 uses lexical BM25 only.",
    )
    ap.add_argument("--json", action="store_true", dest="emit_json")
    ap.add_argument(
        "--run-log",
        type=Path,
        help="Append one Query_Log.csv row per query to this file (e.g. <packet>/Query_Log.csv). Off by default.",
    )
    ap.add_argument(
        "--log-dir",
        type=Path,
        help="Append rows to <dir>/Query_Log.csv. Mutually exclusive with --run-log. Never writes inside an immutable snapshot.",
    )
    ap.add_argument("--source-doc")
    ap.add_argument("--artifact-role")
    ap.add_argument("--chunk-type")
    ap.add_argument("--audit-kind")
    ap.add_argument("--category-id")
    ap.add_argument("--knowledge-type-id")
    ap.add_argument("--subject-id")
    ap.add_argument("--archive-state", choices=("ACTIVE", "ARCHIVE"), default="ACTIVE")
    return ap


def collect_queries(args: argparse.Namespace) -> list[tuple[str, str]]:
    queries: list[tuple[str, str]] = []
    if args.query:
        queries.append(("--query", args.query))
    if args.batch:
        with args.batch.open("r", encoding="utf-8", newline="") as f:
            for i, row in enumerate(csv.DictReader(f), start=1):
                q = (row.get("query") or "").strip()
                if q:
                    queries.append((f"row{i}", q))
    return queries


def open_db(snapshot: Path) -> sqlite3.Connection:
    con = sqlite3.connect(str(snapshot / "catalog.sqlite"))
    con.row_factory = sqlite3.Row
    return con


def load_index_build(snapshot: Path) -> dict:
    con = open_db(snapshot)
    row = con.execute(
        "SELECT * FROM index_builds WHERE index_name = ?", (INDEX_NAME,)
    ).fetchone()
    con.close()
    if row is None:
        raise RuntimeError("source_v2 index is not built; run build_source_index.py")
    return dict(row)


def allowed_rows(snapshot: Path, args: argparse.Namespace) -> set[int] | None:
    where = ["ir.index_name = ?", "c.archive_state = ?"]
    params: list[object] = [INDEX_NAME, args.archive_state]
    if args.source_doc:
        where.append("c.source_doc_id = ?")
        params.append(args.source_doc)
    if args.artifact_role:
        where.append("a.artifact_role = ?")
        params.append(args.artifact_role)
    if args.chunk_type:
        where.append("c.chunk_type = ?")
        params.append(args.chunk_type)
    if args.audit_kind:
        where.append("c.audit_kind = ?")
        params.append(args.audit_kind)
    if args.category_id:
        where.append("c.category_id = ?")
        params.append(args.category_id)
    if args.knowledge_type_id:
        where.append("instr(COALESCE(c.knowledge_type_id, ''), ?) > 0")
        params.append(args.knowledge_type_id)
    if args.subject_id:
        where.append("instr(COALESCE(c.subject_id, ''), ?) > 0")
        params.append(args.subject_id)

    con = open_db(snapshot)
    rows = [
        int(r["row_index"])
        for r in con.execute(
            f"""
            SELECT ir.row_index
            FROM index_rows ir
            JOIN chunks c ON c.chunk_id = ir.chunk_id
            JOIN artifacts a ON a.artifact_id = c.artifact_id
            WHERE {' AND '.join(where)}
            """,
            params,
        ).fetchall()
    ]
    con.close()
    if not rows:
        return set()
    return set(rows)


def query_one(
    snapshot: Path,
    query: str,
    k: int,
    build: dict,
    args: argparse.Namespace,
) -> list[dict]:
    allowed = allowed_rows(snapshot, args)
    row_count = int(build["row_count"])
    if allowed == set():
        return []
    fan = min(row_count, max(k * 20, 100))

    mode = args.mode
    if mode == "bm25":
        bm = bm25_topk(snapshot, query, fan, allowed)
        ranked = rank_single(bm, k, rank_kind="bm25")
        return hydrate(snapshot, ranked, bm, [])

    if mode == "dense":
        if not has_dense_embeddings(snapshot, build):
            raise RuntimeError(
                "dense embeddings are not built for this snapshot; "
                "use --mode bm25 or rebuild without --no-embeddings"
            )
        dense = dense_topk(snapshot, query, fan, allowed, build)
        ranked = rank_single(dense, k, rank_kind="dense")
        return hydrate(snapshot, ranked, [], dense)

    if mode == "hybrid":
        bm = bm25_topk(snapshot, query, fan, allowed)
        dense: list[tuple[int, float]] = []
        if has_dense_embeddings(snapshot, build):
            dense = dense_topk(snapshot, query, fan, allowed, build)
        fused = rrf(bm, dense, k)
        return hydrate(snapshot, fused, bm, dense)

    raise RuntimeError(f"unsupported retrieval mode: {mode}")


def has_dense_embeddings(snapshot: Path, build: dict) -> bool:
    rel = build.get("embeddings_norm_path")
    return bool(rel) and (snapshot / rel).exists()


def rank_single(
    hits: list[tuple[int, float]],
    k: int,
    *,
    rank_kind: str,
) -> list[tuple[int, float | None, int | None, int | None]]:
    ranked = []
    for rank, (row, _score) in enumerate(hits[:k], start=1):
        bm_rank = rank if rank_kind == "bm25" else None
        dense_rank = rank if rank_kind == "dense" else None
        ranked.append((row, None, bm_rank, dense_rank))
    return ranked


def bm25_topk(
    snapshot: Path,
    query: str,
    k: int,
    allowed: set[int] | None,
) -> list[tuple[int, float]]:
    import bm25s

    bm25 = bm25s.BM25.load(str(snapshot / "bm25"))
    q_tokens = bm25s.tokenize([query], stopwords="en", show_progress=False)
    docs, scores = bm25.retrieve(q_tokens, k=k, show_progress=False)
    hits = [(int(d), float(s)) for d, s in zip(docs[0], scores[0])]
    if allowed is not None:
        hits = [(r, s) for r, s in hits if r in allowed]
    return hits


@lru_cache(maxsize=4)
def load_embeddings(path: str) -> np.ndarray:
    return np.load(path)


def dense_topk(
    snapshot: Path,
    query: str,
    k: int,
    allowed: set[int] | None,
    build: dict,
) -> list[tuple[int, float]]:
    from fastembed import TextEmbedding

    model = TextEmbedding(model_name=build["embedding_model"])
    qv = np.asarray(next(iter(model.embed([query]))), dtype=np.float32)
    norm = np.linalg.norm(qv)
    if norm > 0:
        qv = qv / norm
    embs = load_embeddings(str(snapshot / build["embeddings_norm_path"]))
    sims = embs @ qv
    if allowed is not None:
        mask = np.zeros(sims.shape[0], dtype=bool)
        for row in allowed:
            if 0 <= row < mask.shape[0]:
                mask[row] = True
        sims = np.where(mask, sims, -np.inf)
    kk = min(k, sims.shape[0])
    if kk == 0:
        return []
    part = np.argpartition(-sims, kk - 1)[:kk]
    idx = part[np.argsort(-sims[part])]
    return [(int(i), float(sims[i])) for i in idx if sims[i] != -np.inf]


def rrf(
    bm25_hits: list[tuple[int, float]],
    dense_hits: list[tuple[int, float]],
    k: int,
) -> list[tuple[int, float, int | None, int | None]]:
    bm_rank = {row: i + 1 for i, (row, _) in enumerate(bm25_hits)}
    dn_rank = {row: i + 1 for i, (row, _) in enumerate(dense_hits)}
    rows = set(bm_rank) | set(dn_rank)
    scored = []
    for row in rows:
        score = 0.0
        if row in bm_rank:
            score += 1.0 / (RRF_K + bm_rank[row])
        if row in dn_rank:
            score += 1.0 / (RRF_K + dn_rank[row])
        scored.append((row, score, bm_rank.get(row), dn_rank.get(row)))
    scored.sort(key=lambda x: x[1], reverse=True)
    return scored[:k]


def hydrate(
    snapshot: Path,
    fused: list[tuple[int, float | None, int | None, int | None]],
    bm25_hits: list[tuple[int, float]],
    dense_hits: list[tuple[int, float]],
) -> list[dict]:
    if not fused:
        return []
    bm_score = dict(bm25_hits)
    dn_score = dict(dense_hits)
    rows = [r for r, *_ in fused]
    placeholders = ",".join("?" for _ in rows)
    con = open_db(snapshot)
    meta = {
        int(r["row_index"]): dict(r)
        for r in con.execute(
            f"""
            SELECT ir.row_index, c.chunk_id, c.artifact_id, c.source_doc_id,
                   c.chunk_type, c.rel_path, c.source_ref, c.heading, c.page_label,
                   c.category_id, c.knowledge_type_id, c.subject_id,
                   c.atomic_unit_id, c.audit_kind, c.audit_state,
                   a.artifact_role, substr(c.text, 1, 500) AS text_preview
            FROM index_rows ir
            JOIN chunks c ON c.chunk_id = ir.chunk_id
            JOIN artifacts a ON a.artifact_id = c.artifact_id
            WHERE ir.index_name = ? AND ir.row_index IN ({placeholders})
            """,
            [INDEX_NAME, *rows],
        ).fetchall()
    }
    con.close()
    out = []
    for row_index, rrf_score, bm_rank, dn_rank in fused:
        m = meta.get(row_index)
        if not m:
            continue
        m.pop("row_index", None)
        out.append(
            {
                **m,
                "rrf_score": round(rrf_score, 6) if rrf_score is not None else None,
                "bm25_rank": bm_rank,
                "bm25_score": round(bm_score.get(row_index, 0.0), 4) if bm_rank else None,
                "dense_rank": dn_rank,
                "cosine_score": round(dn_score.get(row_index, 0.0), 4) if dn_rank else None,
            }
        )
    return out


if __name__ == "__main__":
    raise SystemExit(main())
