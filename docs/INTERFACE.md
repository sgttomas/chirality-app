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

### GET /api/export/run?runId=...
- Returns metadata for exported run files if present.

Response (200)
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

Errors
```json
{ "code": "ERR_RUN_NOT_FOUND" | "ERR_EXPORT_FAILED", "message": "...", "details": {"...": "..."} }
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

