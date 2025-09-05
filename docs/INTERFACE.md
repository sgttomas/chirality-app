# Chirality App Interface (API + Artifacts)

This document describes the v2.0.0 application interface for traversal and export, replacing older framework CLI contracts. Framework integration docs are archived; this file is the canonical reference for the app.

## Endpoints

- POST `/api/pipeline/traverse` — Execute traversal
- GET `/api/export/run?runId=...` — Inspect export metadata for a run

### POST /api/pipeline/traverse
- Runs an 11‑station traversal in the selected mode (defaults to foundation).

Request
```json
{
  "problem": {
    "title": "string",
    "statement": "string",
    "initialVector": {"...": "..."}
  },
  "options": { "mode": "foundation" | "full" }
}
```

Response (200)
```json
{
  "traversalId": "run_...",
  "stations": [
    {"station":"S1","label":"Problem Statement","modality":"problem","operation":"J"}
  ],
  "resolution": "string",
  "metadata": {
    "durations": {"S1": 123},
    "totalDuration": 456,
    "totalTokens": 789
  }
}
```

Errors (JSON)
```json
{ "code": "ERR_INVALID_JSON" | "ERR_MISSING_FIELDS" | "ERR_ORCHESTRATOR_INIT" | "ERR_TRAVERSAL_FAILED", "message": "...", "details": {"...": "..."} }
```

Notes
- Foundation mode does not require an API key; stations use structured fallbacks.
- Full mode attempts LLM calls per station.

### GET /api/export/run?runId=...&include=seeds
- Returns metadata for exported run files if present.
- Optional: Include matrix seeds extraction with `include=seeds` parameter.

Parameters
- `runId` (required): Run identifier (format: `run_{timestamp}_{random}`)
- `include` (optional): Set to `seeds` to include seed extraction from framework matrices

Response (200) without seeds
```json
{
  "runId": "run_...",
  "files": {
    "runJson": "runs/<runId>/run.json",
    "packetsJsonl": "runs/<runId>/packets.jsonl"
  },
  "size": { "runJson": 1234, "packetsJsonl": 5678, "total": 6912 }
}
```

Response (200) with seeds
```json
{
  "runId": "run_...",
  "files": {
    "runJson": "runs/<runId>/run.json",
    "packetsJsonl": "runs/<runId>/packets.jsonl"
  },
  "size": { "runJson": 1234, "packetsJsonl": 5678, "total": 6912 },
  "seeds": {
    "initialVector": {
      "matrixC": ["text1", "text2"],
      "matrixD": ["text3", "text4"],
      "matrixX": ["text5", "text6"],
      "matrixE": ["text7", "text8"]
    },
    "metadata": {
      "runId": "run_...",
      "extractedAt": "2025-01-02T12:34:56.789Z",
      "totalCells": 123,
      "counts": { "C": 30, "D": 35, "X": 30, "E": 28 },
      "sourceFiles": ["snapshots/C.jsonl", "snapshots/D.jsonl", "snapshots/X.jsonl", "snapshots/E.jsonl"],
      "checksumVerified": true,
      "warnings": []
    }
  }
}
```

Errors
```json
{ "code": "ERR_RUN_NOT_FOUND" | "ERR_EXPORT_FAILED", "message": "...", "details": {"...": "..."} }
```

Notes
- Soft failures during seed extraction return 200 OK with warnings in `seeds.metadata.warnings`
- Seeds are cached to `runs/<runId>/seeds.json` for performance
- Matrix format must be `cells-jsonl-v1` for extraction to work

### POST /api/import/seeds
- Import framework seeds independent of app exports (manifest + snapshots).
- Cache-aware; uses CHIRALITY_RUNS_DIR (default: runs) and seeds.json.

Parameters
- Body JSON:
  - runId: string (required)
  - options (optional):
    - `runsDir`: string (dev only; override base runs dir)
    - `heuristics`: boolean
    - `minItems`: number
    - `maxItems`: number
    - `maxLength`: number
    - `verifyChecksums`: boolean

Request
```json
{
  "runId": "run_1725570000_ab12cd",
  "options": {
    "heuristics": true,
    "minItems": 6,
    "maxItems": 12,
    "maxLength": 120,
    "verifyChecksums": true
  }
}
```

Response (200)
```json
{
  "seeds": {
    "initialVector": {
      "matrixC": ["text1", "text2"],
      "matrixD": ["text3", "text4"],
      "matrixX": ["text5", "text6"],
      "matrixE": ["text7", "text8"]
    },
    "metadata": {
      "runId": "run_1725570000_ab12cd",
      "extractedAt": "2025-09-05T12:34:56.789Z",
      "totalCells": 48,
      "counts": { "C": 12, "D": 12, "X": 12, "E": 12 },
      "preHeuristicsCounts": { "C": 20, "D": 20, "X": 15, "E": 18 },
      "postHeuristicsCounts": { "C": 12, "D": 12, "X": 12, "E": 12 },
      "preHeuristicsTotal": 73,
      "postHeuristicsTotal": 48,
      "sourceFiles": ["snapshots/C.jsonl","snapshots/D.jsonl","snapshots/X.jsonl","snapshots/E.jsonl"],
      "checksumVerified": true,
      "checksums": { "C": "ok", "D": "ok", "X": "ok", "E": "ok" },
      "warnings": []
    }
  }
}
```

Notes
- Production: accepts run_{timestamp}_{random} runIds only.
- Development: also accepts sample_{name} fixture runIds; options.runsDir override allowed.
- Cache behavior: returns cached seeds if seeds.json is fresh; otherwise extracts and (if enabled) persists a fresh cache.
- Heuristics: sentence-first trim, whitespace normalize, bullet/emoji strip, case-insensitive dedupe, length clamp; no padding if below min (warning only).
- Checksum behavior: Production fails hard on mismatch; Development warns and continues.

Errors
```json
{ "code": "ERR_INVALID_JSON" | "ERR_MISSING_RUN_ID" | "ERR_INVALID_RUN_ID" | "ERR_SEEDS_EXTRACTION_FAILED", "message": "...", "details": {"...": "..."} }
```

## Packets and Artifacts

- Packet JSON Schema: `schemas/packet.json` (validated by AJV in CI)
- Exports directory: `runs/<runId>/`
  - `run.json`: Run summary, durations, counts, resolution
  - `packets.jsonl`: One JSON line per station packet

Packet outline
```json
{
  "id": "S2-<hash>",
  "createdAt": "2025-09-04T12:34:56.789Z",
  "station": "S2",
  "modality": "systematic",
  "payload": { "DS": "..." },
  "meta": {
    "duration": 123,
    "tokens": { "prompt": 0, "completion": 0, "total": 0 },
    "label": "Data Sheet"
  }
}
```

## Environment

- `OPENAI_API_KEY`: Required for real LLM calls; optional for foundation mode
- `OPENAI_MODEL`: Single source of truth for model selection (e.g., `gpt-4.1-nano`)

## Compatibility

- Older framework CLI and matrix manifest docs are archived. Matrix concepts (C/D/X/E) inform station prompts but are not required inputs to this API.

## Error Codes

- `ERR_INVALID_JSON`: Request body could not be parsed
- `ERR_MISSING_FIELDS`: Required fields absent (e.g., problem.title/statement)
- `ERR_ORCHESTRATOR_INIT`: Orchestrator could not initialize (e.g., missing key in full mode)
- `ERR_TRAVERSAL_FAILED`: Station processing failed
- `ERR_RUN_NOT_FOUND`: Export not found for given `runId`
- `ERR_EXPORT_FAILED`: Unexpected error retrieving export metadata

## Examples

```bash
curl -s -X POST http://localhost:3001/api/pipeline/traverse \
  -H 'Content-Type: application/json' \
  -d '{"problem": {"title":"Auth","statement":"Implement authentication"}, "options": {"mode": "foundation"}}'

curl -s "http://localhost:3001/api/export/run?runId=run_1725450000_abcd12" | jq
```

