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

### GET /api/export/run?runId=...
- Inspect export presence and sizes for a run.

Response
```json
{
  "runId": "run_...",
  "files": { "runJson": "runs/<runId>/run.json", "packetsJsonl": "runs/<runId>/packets.jsonl" },
  "size": { "runJson": 1234, "packetsJsonl": 5678, "total": 6912 }
}
```

Errors: `ERR_RUN_NOT_FOUND`, `ERR_EXPORT_FAILED`

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
curl -s -X POST http://localhost:3001/api/pipeline/traverse \
  -H 'Content-Type: application/json' \
  -d '{"problem": {"title":"Auth","statement":"Implement authentication"}}'

curl -s "http://localhost:3001/api/export/run?runId=run_..." | jq
```

---

This document supersedes earlier agent/chat/framework API references. Legacy materials are archived.
