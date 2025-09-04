# Migration Guide: v1.0.0 → v2.0.0

This guide summarizes breaking changes and how to update integrations.

## Summary of Changes

- Project renamed to `chirality-app` and version bumped to 2.0.0
- Greenfield implementation of canonical 11‑station pipeline
- Default “foundation” mode (S1–S5 + S11) for fast output
- New API surface: traverse + export endpoints only
- Canonical packet schema with JSONL export and CI validation
- UI updated to show stations with modality chips and mode selector
- CI with schema validation and legacy sweep

## Removed / Deprecated

- Legacy chat/RAG endpoints (`/api/chat/*`) — out of scope
- Agent/framework endpoints (`/api/agent/*`) — replaced by app traversal/export
- Nine‑station (S0–S8) model — replaced by S1–S11 ontology
- Triple structure — replaced by Packet

## New Interfaces

### POST /api/pipeline/traverse
```json
{
  "problem": { "title": "string", "statement": "string" },
  "options": { "mode": "foundation" | "full" }
}
```

### GET /api/export/run?runId=...
Returns file paths and sizes if exported.

## Environment

- `OPENAI_MODEL` is the single source for model selection (no hardcoded names)
- Foundation mode works without `OPENAI_API_KEY` (LLM fallbacks)

## Packets & Exports

- Exports live under `runs/<runId>/` as `run.json` and `packets.jsonl`
- Packets validate against `schemas/packet.json`

## Validation & CI

- CI creates a foundation run and validates packets via AJV
- Legacy sweep rejects deprecated references in active code

## What To Update in Your Integrations

- Replace any references to `/api/agent/*` or chat endpoints with `/api/pipeline/traverse`
- Stop depending on nine‑station fields; use station metadata from responses
- Consume JSONL packets when you need per‑station outputs
- Set `OPENAI_MODEL` in your environment; avoid hardcoded model names

## FAQ

- Q: Can I still run full (S1–S11)?
  - A: Yes. Pass `{ options: { mode: "full" } }` to the traverse API.
- Q: Do I need an API key?
  - A: Only for real LLM output. Foundation mode will produce structured fallbacks without it.
- Q: Where is matrix ingestion?
  - A: Matrices (C/D/X/E) conceptually guide station prompts; ingestion is optional and currently out of scope.

