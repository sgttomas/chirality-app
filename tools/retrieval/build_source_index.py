#!/usr/bin/env python3
"""Build BM25 and optional dense vector sidecars for a source database snapshot.

Usage:
  python3 tools/retrieval/build_source_index.py \
      --snapshot domains/piping-design/_LocalIndexes/_LATEST.md

Inputs:
  --snapshot       Source database snapshot directory or _LATEST.md pointer.
  --model          fastembed model name. Default: BAAI/bge-base-en-v1.5.
  --dim            Expected embedding dimension. Default: 768.
  --batch          Embedding batch size. Default: 64.
  --no-embeddings  Build BM25 only; query will run lexical-only.
  --force          Replace existing V2 index artifacts in the snapshot.

Outputs:
  <snapshot>/bm25/
  <snapshot>/embeddings.npy            unless --no-embeddings
  <snapshot>/embeddings_norm.npy       unless --no-embeddings
  Updates catalog.sqlite index_rows and index_builds.

This is V2-only. It does not read or preserve prior tools/retrieval/_index
artifacts.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import sqlite3
import sys
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "tools" / "source_catalog"))
from source_database import DEFAULT_DOMAIN_ROOT, resolve_snapshot_path  # noqa: E402

INDEX_NAME = "source_v2"
DEFAULT_MODEL = "BAAI/bge-base-en-v1.5"
DEFAULT_DIM = 768


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--snapshot", type=Path)
    ap.add_argument("--domain-root", type=Path, default=DEFAULT_DOMAIN_ROOT)
    ap.add_argument("--model", default=DEFAULT_MODEL)
    ap.add_argument("--dim", type=int, default=DEFAULT_DIM)
    ap.add_argument("--batch", type=int, default=64)
    ap.add_argument("--no-embeddings", action="store_true")
    ap.add_argument("--force", action="store_true")
    args = ap.parse_args()

    try:
        snapshot = resolve_snapshot_path(args.snapshot, args.domain_root)
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    db_path = snapshot / "catalog.sqlite"
    if not db_path.exists():
        print(f"ERROR: missing catalog.sqlite in {snapshot}", file=sys.stderr)
        return 2

    bm25_dir = snapshot / "bm25"
    emb_path = snapshot / "embeddings.npy"
    emb_norm_path = snapshot / "embeddings_norm.npy"
    existing = [p for p in (bm25_dir, emb_path, emb_norm_path) if p.exists()]
    if existing and not args.force:
        print(
            "ERROR: index artifacts already exist; rerun with --force to replace them",
            file=sys.stderr,
        )
        for p in existing:
            print(f"  {p}", file=sys.stderr)
        return 2
    if args.force:
        if bm25_dir.exists():
            shutil.rmtree(bm25_dir)
        for p in (emb_path, emb_norm_path):
            if p.exists():
                p.unlink()

    print(f"[1/4] Loading active chunks from {snapshot}")
    rows = load_chunks(db_path)
    if not rows:
        print("ERROR: no active chunks found", file=sys.stderr)
        return 1
    texts = [r["text"] for r in rows]
    print(f"      {len(rows):,} chunks")

    print("[2/4] Building BM25S index")
    import bm25s

    corpus_tokens = bm25s.tokenize(texts, stopwords="en", show_progress=False)
    bm25 = bm25s.BM25()
    bm25.index(corpus_tokens, show_progress=False)
    bm25.save(str(bm25_dir))
    print(f"      saved {bm25_dir}")

    embeddings_written = False
    if args.no_embeddings:
        print("[3/4] Skipping embeddings (--no-embeddings)")
    else:
        print(f"[3/4] Encoding embeddings via fastembed ({args.model})")
        embs = encode_texts(texts, args.model, args.dim, args.batch)
        np.save(emb_path, embs)
        norms = np.linalg.norm(embs, axis=1, keepdims=True)
        norms[norms == 0] = 1.0
        np.save(emb_norm_path, (embs / norms).astype(np.float32))
        embeddings_written = True
        print(f"      saved {emb_path.name} and {emb_norm_path.name}")

    print("[4/4] Writing index rows and build metadata")
    built_utc = datetime.now(timezone.utc).isoformat(timespec="seconds")
    input_hash = chunks_digest(rows)
    con = sqlite3.connect(str(db_path))
    con.execute("PRAGMA foreign_keys = ON")
    con.execute("DELETE FROM index_rows WHERE index_name = ?", (INDEX_NAME,))
    con.executemany(
        "INSERT INTO index_rows (index_name, row_index, chunk_id) VALUES (?, ?, ?)",
        ((INDEX_NAME, i, r["chunk_id"]) for i, r in enumerate(rows)),
    )
    con.execute("DELETE FROM index_builds WHERE index_name = ?", (INDEX_NAME,))
    con.execute(
        """
        INSERT INTO index_builds (
          index_name, built_utc, embedding_model, embedding_dim, row_count,
          bm25_dir, embeddings_path, embeddings_norm_path, input_chunks_sha256,
          status
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            INDEX_NAME,
            built_utc,
            None if args.no_embeddings else args.model,
            None if args.no_embeddings else args.dim,
            len(rows),
            "bm25/",
            "embeddings.npy" if embeddings_written else None,
            "embeddings_norm.npy" if embeddings_written else None,
            input_hash,
            "BM25_ONLY" if args.no_embeddings else "READY",
        ),
    )
    con.commit()
    con.close()

    update_meta(snapshot, built_utc, len(rows), args, input_hash, embeddings_written)
    print(f"DONE: {snapshot}")
    return 0


def load_chunks(db_path: Path) -> list[dict]:
    con = sqlite3.connect(str(db_path))
    con.row_factory = sqlite3.Row
    rows = [
        dict(r) for r in con.execute(
            """
            SELECT chunk_id, text
            FROM chunks
            WHERE archive_state='ACTIVE' AND chunk_type != 'EXTRACTION_ERROR'
            ORDER BY chunk_id
            """
        ).fetchall()
    ]
    con.close()
    return rows


def encode_texts(texts: list[str], model_name: str, dim: int, batch: int) -> np.ndarray:
    from fastembed import TextEmbedding

    model = TextEmbedding(model_name=model_name)
    embs = np.empty((len(texts), dim), dtype=np.float32)
    written = 0
    for i, vec in enumerate(model.embed(texts, batch_size=batch)):
        v = np.asarray(vec, dtype=np.float32)
        if v.shape[0] != dim:
            raise RuntimeError(f"unexpected dim {v.shape[0]} (expected {dim})")
        embs[i] = v
        written += 1
        if written % 1000 == 0:
            print(f"      {written:,}/{len(texts):,}")
    if written != len(texts):
        raise RuntimeError(f"embedded {written} != {len(texts)}")
    return embs


def chunks_digest(rows: list[dict]) -> str:
    h = hashlib.sha256()
    for row in rows:
        h.update(row["chunk_id"].encode("utf-8"))
        h.update(b"\0")
        h.update(row["text"].encode("utf-8"))
        h.update(b"\0")
    return h.hexdigest()


def update_meta(
    snapshot: Path,
    built_utc: str,
    row_count: int,
    args: argparse.Namespace,
    input_hash: str,
    embeddings_written: bool,
) -> None:
    meta_path = snapshot / "meta.json"
    meta = json.loads(meta_path.read_text(encoding="utf-8"))
    meta["retrieval_index"] = {
        "index_name": INDEX_NAME,
        "built_utc": built_utc,
        "row_count": row_count,
        "lexical": "bm25s",
        "bm25_dir": "bm25/",
        "dense": None if args.no_embeddings else "numpy_cosine",
        "embedding_model": None if args.no_embeddings else args.model,
        "embedding_dim": None if args.no_embeddings else args.dim,
        "embeddings": "embeddings.npy" if embeddings_written else None,
        "embeddings_norm": "embeddings_norm.npy" if embeddings_written else None,
        "input_chunks_sha256": input_hash,
        "status": "BM25_ONLY" if args.no_embeddings else "READY",
    }
    meta_path.write_text(json.dumps(meta, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    raise SystemExit(main())
