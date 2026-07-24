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

For the Chirality self-domain, build from the manifest-referenced governance
core corpus. Source files are not copied; catalog paths are recorded as
`@repo/<RepoRelPath>` and resolved through `--repo-root`:

```sh
python3 tools/source_catalog/build_source_database.py \
  --domain-root domains/chirality \
  --repo-root . \
  --source-manifest domains/chirality/_Sources/Source_Manifest.csv
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

For the initial Chirality self-domain milestone, build BM25 only first:

```sh
python3 tools/retrieval/build_source_index.py \
  --snapshot domains/chirality/_LocalIndexes/_LATEST.md \
  --no-embeddings
```

Optionally build dense embeddings later after the catalog and BM25 retrieval
path are accepted:

```sh
python3 tools/retrieval/build_source_index.py \
  --snapshot domains/chirality/_LocalIndexes/_LATEST.md
```

## Query

Default hybrid search uses BM25 plus dense cosine retrieval when embeddings are
available, then fuses ranks:

```sh
python3 tools/retrieval/query_source_index.py \
  --snapshot domains/piping-design/_LocalIndexes/_LATEST.md \
  --query "support spacing for steam lines" \
  --k 10
```

Pure dense semantic search ranks by embedding cosine only:

```sh
python3 tools/retrieval/query_source_index.py \
  --snapshot domains/chirality/_LocalIndexes/_LATEST.md \
  --query "epistemic warrant and professional accountability" \
  --mode dense \
  --k 10
```

Pure BM25 lexical search ranks by keyword match only:

```sh
python3 tools/retrieval/query_source_index.py \
  --snapshot domains/chirality/_LocalIndexes/_LATEST.md \
  --query "derivative-package rule" \
  --mode bm25 \
  --k 10
```

Atom-only dense search is useful for semantic discovery over accepted atomic
knowledge units:

```sh
python3 tools/retrieval/query_source_index.py \
  --snapshot domains/chirality/_LocalIndexes/_LATEST.md \
  --query "human authority over epistemic warrant" \
  --mode dense \
  --chunk-type LEDGER_ATOM \
  --k 20
```

Useful filters:

```sh
--mode hybrid
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

The public result contract returns retrieval mode on each query payload plus
stable IDs and provenance on each result row:

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

Validate the Chirality self-domain snapshot with repo-path resolution:

```sh
python3 tools/source_catalog/validate_source_database.py \
  --snapshot domains/chirality/_LocalIndexes/_LATEST.md \
  --domain-root domains/chirality \
  --repo-root .
```

Use `--skip-hash-verify` for quick checks over very large local corpora.

## Rebuild Policy

Rebuild the source database whenever source files, audit sidecars, or
decomposition ledgers change. Rebuild the retrieval index whenever `Chunks.csv`
or `catalog.sqlite` chunks change.

Snapshots are immutable after build. `_LATEST.md` is the mutable pointer to the
current snapshot.
