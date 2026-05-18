# tools/retrieval

V2 source retrieval for `piping-design` and future DOMAIN packages.

The retrieval layer is a derived local query index over a source database
snapshot. It does not own source truth, does not copy source files, and does
not require Postgres, a server process, SQLite extensions, LanceDB, DuckDB,
Chroma, or cloud services.

## Supported V2 Stack

| Layer | Choice |
|---|---|
| Catalog | SQLite `catalog.sqlite` built by `tools/source_catalog/build_source_database.py` |
| Lexical | `bm25s` persisted under `<snapshot>/bm25/` |
| Embeddings | `fastembed` with `BAAI/bge-base-en-v1.5` by default |
| Dense storage/search | NumPy `embeddings.npy` + `embeddings_norm.npy`, cosine via dot product |
| Alignment | SQLite `index_rows` maps internal row numbers to stable `chunk_id` values |
| Public identity | `chunk_id` and `artifact_id`, not row numbers |

Historical `tools/retrieval/_index/` artifacts are not part of the V2
contract.

## Snapshot Layout

Source database snapshots live under the domain package:

```text
domains/piping-design/_LocalIndexes/
  _LATEST.md
  snapshots/
    SRCIDX_<UTC>/
      catalog.sqlite
      SourceDocs.csv
      Artifacts.csv
      AuditState.csv
      Chunks.csv
      bm25/
      embeddings.npy
      embeddings_norm.npy
      meta.json
      QA_Report.md
```

`catalog.sqlite` is the authoritative derived query catalog for that snapshot.
CSV files are review/export surfaces. Source files remain in their existing
filesystem locations and are referenced by relative path plus SHA-256.

## Build

Build the source database snapshot:

```sh
python3 tools/source_catalog/build_source_database.py \
  --domain-root domains/piping-design
```

Build BM25 + dense retrieval sidecars into that snapshot:

```sh
python3 tools/retrieval/build_source_index.py \
  --snapshot domains/piping-design/_LocalIndexes/_LATEST.md
```

For fixture tests or quick lexical-only builds:

```sh
python3 tools/retrieval/build_source_index.py \
  --snapshot <snapshot-or-latest> --no-embeddings
```

## Query

```sh
python3 tools/retrieval/query_source_index.py \
  --snapshot domains/piping-design/_LocalIndexes/_LATEST.md \
  --query "support spacing for steam lines" \
  --k 10
```

Useful filters:

```sh
--source-doc SRC-PIPING-MANUAL
--artifact-role SOURCE_MARKDOWN
--chunk-type SECTION_NODE
--audit-kind equations
--category-id CAT-003
--knowledge-type-id KTY-03-01
--subject-id SUB-03-01-02
--archive-state ACTIVE
--json
```

The public result contract returns stable IDs and provenance:

- `chunk_id`
- `artifact_id`
- `source_doc_id`
- `rel_path`
- `source_ref`
- `chunk_type`
- structural IDs when available
- BM25 / dense ranks and scores
- text preview

Internal row numbers are implementation detail only.

## Validate

```sh
python3 tools/source_catalog/validate_source_database.py \
  --snapshot domains/piping-design/_LocalIndexes/_LATEST.md
```

Use `--skip-hash-verify` for quick checks over very large local corpora.

## Rebuild Policy

Rebuild the source database whenever source files, audit sidecars, or
decomposition ledgers change. Rebuild the retrieval index whenever `Chunks.csv`
or `catalog.sqlite` chunks change.

Snapshots are immutable after build. `_LATEST.md` is the mutable pointer to the
current snapshot.
