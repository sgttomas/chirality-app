# API Reference (v2.0.0)

Canonical REST API documentation for chirality‑app. For a concise overview, see docs/INTERFACE.md.

Base URL: `http://localhost:3001`

## Endpoints

### POST /api/pipeline/traverse
- Execute traversal in `foundation` (default) or `full` mode.

Request
```json
{
  "problem": { "title": "string", "statement": "string" },
  "options": { "mode": "foundation" | "full" }
}
```

Response
```json
{
  "traversalId": "run_...",
  "stations": [ {"station":"S1","label":"Problem Statement","modality":"problem","operation":"J"} ],
  "resolution": "string",
  "metadata": { "durations": {"S1": 123}, "totalDuration": 456, "totalTokens": 0 }
}
```

Errors: `ERR_INVALID_JSON`, `ERR_MISSING_FIELDS`, `ERR_ORCHESTRATOR_INIT`, `ERR_TRAVERSAL_FAILED`

### GET /api/export/run?runId=...&include=seeds
- Inspect export presence and sizes for a run.
- Optional: Include matrix seeds with `include=seeds` parameter.

Parameters:
- `runId` (required): The run identifier
- `include` (optional): Set to `seeds` to include seed extraction

Response (without seeds)
```json
{
  "runId": "run_...",
  "files": { "runJson": "runs/<runId>/run.json", "packetsJsonl": "runs/<runId>/packets.jsonl" },
  "size": { "runJson": 1234, "packetsJsonl": 5678, "total": 6912 }
}
```

Response (with seeds)
```json
{
  "runId": "run_...",
  "files": { "runJson": "runs/<runId>/run.json", "packetsJsonl": "runs/<runId>/packets.jsonl" },
  "size": { "runJson": 1234, "packetsJsonl": 5678, "total": 6912 },
  "seeds": {
    "initialVector": {
      "matrixC": ["..."],
      "matrixD": ["..."],
      "matrixX": ["..."],
      "matrixE": ["..."]
    },
    "metadata": {
      "runId": "run_...",
      "extractedAt": "2025-01-02T00:00:00.000Z",
      "totalCells": 123,
      "counts": { "C": 30, "D": 35, "X": 30, "E": 28 },
      "preHeuristicsCounts": { "C": 40, "D": 40, "X": 35, "E": 38 },
      "postHeuristicsCounts": { "C": 30, "D": 35, "X": 30, "E": 28 },
      "preHeuristicsTotal": 153,
      "postHeuristicsTotal": 123,
      "sourceFiles": ["snapshots/C.jsonl", "..."],
      "checksumVerified": true,
      "checksums": { "C": "ok", "D": "ok", "X": "ok", "E": "ok" },
      "warnings": []
    }
  }
}
```

Errors: `ERR_RUN_NOT_FOUND`, `ERR_EXPORT_FAILED`

Note: Soft failures during seed extraction return 200 OK with `seeds.metadata.warnings` populated.

### POST /api/import/seeds
- Import framework seeds from a run directory (independent of app exports).

Request
```json
{
  "runId": "run_1234567890_abc123",
  "options": {
    "runsDir": "fixtures/runs",
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
      "runId": "run_1234567890_abc123",
      "extractedAt": "2025-09-05T02:25:19.786Z",
      "totalCells": 6,
      "counts": { "C": 2, "D": 2, "X": 1, "E": 1 },
      "preHeuristicsCounts": { "C": 2, "D": 2, "X": 1, "E": 1 },
      "postHeuristicsCounts": { "C": 2, "D": 2, "X": 1, "E": 1 },
      "preHeuristicsTotal": 6,
      "postHeuristicsTotal": 6,
      "sourceFiles": ["snapshots/C.jsonl", "snapshots/D.jsonl", "snapshots/X.jsonl", "snapshots/E.jsonl"],
      "checksumVerified": false,
      "checksums": { "C": "mismatch", "D": "mismatch", "X": "mismatch", "E": "mismatch" },
      "warnings": ["Checksum mismatch for C: expected deadbeef, got 98ab..."]
    }
  }
}
```

Notes:
- Production: Only accepts `run_{timestamp}_{random}` format runIds
- Development: Also accepts `sample_{name}` fixture runIds
- Options are optional; defaults from `seedsConfig` are used
- Uses `CHIRALITY_RUNS_DIR` environment variable (default: `runs`)
- Cache-aware: returns cached seeds if valid, otherwise extracts fresh
- `runsDir` option override only works in development mode
- Checksum behavior: Production fails hard on mismatch (strict mode); Development warns and continues (safe mode)

Errors: `ERR_INVALID_JSON`, `ERR_MISSING_RUN_ID`, `ERR_INVALID_RUN_ID`, `ERR_SEEDS_EXTRACTION_FAILED`

## Packets & Schema

- JSONL export: `runs/<runId>/packets.jsonl` (one packet per line)
- Summary: `runs/<runId>/run.json`
- Schema: `schemas/packet.json` (validated in CI)

Packet example
```json
{
  "id": "S5-abcdefghijkL",
  "createdAt": "2025-09-04T00:00:00.000Z",
  "station": "S5",
  "modality": "process",
  "payload": { "EC": "..." },
  "meta": { "duration": 250, "tokens": { "prompt": 0, "completion": 0, "total": 0 } }
}
```

## Environment

- `OPENAI_API_KEY`: Optional for `foundation` (fallbacks), required for real LLM in `full`
- `OPENAI_MODEL`: Model selection via env var (no hardcoded names in code)

## Notes

- Foundation mode: S1→S2→S3→S4→S5→S11
- Full mode: S1→…→S11 (S6–S10 currently placeholders)
- Matrix concepts (C/D/X/E) guide station prompts but are not required API inputs.

## Examples

```bash
# Pipeline traversal
curl -s -X POST http://localhost:3001/api/pipeline/traverse \
  -H 'Content-Type: application/json' \
  -d '{"problem": {"title":"Auth","statement":"Implement authentication"}}'

# Export run metadata
curl -s "http://localhost:3001/api/export/run?runId=run_..." | jq

# Import seeds from framework run
curl -s -X POST http://localhost:3001/api/import/seeds \
  -H 'Content-Type: application/json' \
  -d '{"runId": "sample_happy_001", "options": {"runsDir": "fixtures/runs"}}' | jq
```

---

This document supersedes earlier agent/chat/framework API references. Legacy materials are archived.
