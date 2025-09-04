# Chirality Framework Interface (CLI + Artifacts)

This document defines the contract between `chirality-app` (consumer) and `chirality-framework` (producer).

## CLI Invocation

- Command:
  ```bash
  chirality compute-pipeline \
    --resolver openai \
    --snapshot-jsonl \
    --out runs/<run_id> \
    --problem-file <path> \
    --max-seconds 900
  ```

- Arguments:
  - `--resolver`: `string`. Resolver backend (e.g., "openai"). For automated testing, "echo" is also accepted.
  - `--snapshot-jsonl`: `flag`. Produce JSONL snapshots per matrix (C,D,X,E).
  - `--out`: `string`. Output directory root for the run artifacts, under `runs/<run_id>`. If omitted, the producer may auto-generate a valid run_id and return it in stdout JSON.
  - `--problem-file`: `string`. Path to a JSON file containing:
      ```json
      { "title": "string", "statement": "string" }
      ```
  - `--max-seconds`: `integer`. Hard timeout in seconds (recommended 900).

- Output discipline: In success, the producer prints exactly one JSON line to stdout (see below). All informational logs are written to stderr or gated behind --verbose.

- Output (stdout last line):
  ```json
  {"run_id":"<run_id>","manifest":"runs/<run_id>/index.json"}
  ```

- Exit Codes:
  - `0`: success
  - `1`: general error (unexpected)
  - `2`: invalid arguments
  - `3`: timeout
  - `4`: I/O error (filesystem)
  - `5`: resolver error (e.g., model/API failure)
  - (Unknown exit codes must be treated as `1` by the consumer)

Producer guarantees:
- Manifest is written last and only if the run completes successfully. On timeout/error, no manifest is produced.
- Paths in the manifest are relative to the run directory.
- The producer may include additional non-breaking fields; the consumer must ignore unknown fields.

## Run Identifier

- Pattern: `^[a-z0-9-_]{1,64}$`
- Forbidden: path traversal (no `/`, `\`, `..`).
- `chirality-app` must reject non-conforming run IDs.
- If --out is omitted, the producer may auto-generate a valid run_id and return it in stdout JSON.

## Output Layout

```
runs/<run_id>/
└── index.json            # Manifest
└── snapshots/
    ├── C.jsonl
    ├── D.jsonl
    ├── X.jsonl
    └── E.jsonl

Notes:
- Additional files or matrices may be present; the consumer should rely on the manifest and ignore unreferenced files.
```

## Manifest Schema (index.json)

- Versioning
  - `framework_schema_version`: semver string managed by `chirality-framework`.
  - Compatibility (in `chirality-app`):
    - Same major: OK.
    - Higher minor/patch: warn, accept.
    - Higher major: reject, actionable error.

- Example (types shown by example):
```json
{
  "run_id": "sample_happy_001",
  "created_at": "2025-09-01T12:34:56.789Z",
  "tool": { "name": "chirality-framework", "version": "1.2.3" },
  "framework_schema_version": "1.0.0",
  "problem": { "title": "My Problem", "statement": "Detailed statement..." },
  "durations": { "total_ms": 123456 },
  "matrices": {
    "C": { "path": "snapshots/C.jsonl", "format": "cells-jsonl-v1", "records": 5, "sha256": "hex...", "bytes": 1234 },
    "D": { "path": "snapshots/D.jsonl", "format": "cells-jsonl-v1", "records": 4, "sha256": "hex...", "bytes": 1111 },
    "X": { "path": "snapshots/X.jsonl", "format": "cells-jsonl-v1", "records": 3, "sha256": "hex...", "bytes": 1000 },
    "E": { "path": "snapshots/E.jsonl", "format": "cells-jsonl-v1", "records": 3, "sha256": "hex...", "bytes": 950 }
  }
}
```

- JSON Schema (Draft 2020-12)
```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://chirality.ai/schemas/framework-manifest-1_0_0.json",
  "type": "object",
  "required": ["run_id","created_at","tool","framework_schema_version","problem","durations","matrices"],
  "properties": {
    "run_id": { "type": "string", "pattern": "^[a-z0-9-_]{1,64}$" },
    "created_at": { "type": "string", "format": "date-time" },
    "tool": {
      "type": "object",
      "required": ["name","version"],
      "properties": {
        "name": { "type": "string" },
        "version": { "type": "string" }
      },
      "additionalProperties": false
    },
    "framework_schema_version": { "type": "string" },
    "problem": {
      "type": "object",
      "required": ["title","statement"],
      "properties": {
        "title": { "type": "string" },
        "statement": { "type": "string" }
      },
      "additionalProperties": false
    },
    "durations": {
      "type": "object",
      "required": ["total_ms"],
      "properties": { "total_ms": { "type": "number" } },
      "additionalProperties": true
    },
    "matrices": {
      "type": "object",
      "required": ["C","D","X","E"],
      "properties": {
        "C": { "$ref": "#/$defs/fileMeta" },
        "D": { "$ref": "#/$defs/fileMeta" },
        "X": { "$ref": "#/$defs/fileMeta" },
        "E": { "$ref": "#/$defs/fileMeta" }
      },
      "additionalProperties": false
    }
  },
  "$defs": {
    "fileMeta": {
      "type": "object",
      "required": ["path","records","sha256"],
      "properties": {
        "path": { "type": "string" },
        "format": { "type": "string" },
        "records": { "type": "number" },
        "sha256": { "type": "string" },
        "bytes": { "type": "number" }
      },
      "additionalProperties": false
    }
  },
  "additionalProperties": false
}
```

## JSONL Snapshot Schema (per line)

- File: `snapshots/C.jsonl` (or D/X/E)
- Each line is a complete JSON object.

- Example:
```json
{"id":"C:normative:completeness:1","matrix":"C","row_label":"Normative","col_label":"Completeness","station":"Requirements","text":"...","citations":["CIT:doc#p3"],"refs":["DS:auth"],"meta":{"order":1}}
```

- JSON Schema (Draft 2020-12)
```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://chirality.ai/schemas/framework-snapshot-1_0_0.json",
  "type": "object",
  "required": ["id","matrix","row_label","col_label","station","text","citations","refs"],
  "properties": {
    "id": { "type": "string" },
    "matrix": { "type": "string", "enum": ["C","D","X","E"] },
    "row_label": { "type": "string" },
    "col_label": { "type": "string" },
    "station": { "type": "string" },
    "text": { "type": "string" },
    "citations": { "type": "array", "items": { "type": "string" } },
    "refs": { "type": "array", "items": { "type": "string" } },
    "meta": {
      "type": "object",
      "properties": { "order": { "type": "number" } },
      "additionalProperties": true
    }
  },
  "additionalProperties": false
}

Notes:
- id format is canonical: "{matrix}:r{row}:c{col}".
- station must match the exact Matrix.station string produced by the framework (e.g., "Problem Requirements", "Solution Objectives", "Verification", "Evaluation").
- The producer may include additional fields; the consumer must ignore unknown fields.
```

## Checksums

- `sha256` computed over the raw JSONL file bytes (no newline normalization).
- Manifest includes `sha256` and optional size (`bytes`) for quick sanity checks.

## Timeouts & Idempotency

- Producer (framework): enforce `--max-seconds`.
- Consumer (app): if `runs/<run_id>` exists with valid manifest, skip re-run unless `force=true`.

## Security & Path Safety

- `run_id` must match the required pattern and is used verbatim under `runs/`.
- No path traversal or separators allowed.

