# Troubleshooting (v2.0.0)

Practical steps to diagnose and fix common issues in chirality‑app. This guide reflects the v2 endpoints and features: traversal (foundation/full), exports, and packet schema validation.

## Quick Checks
- Dev server: `npm run dev` (watch for chosen port; 3001 is common)
- Traversal (foundation mode):
  ```bash
  curl -s -X POST http://localhost:3001/api/pipeline/traverse \
    -H 'Content-Type: application/json' \
    -d '{"problem":{"title":"T","statement":"Test"}}' | jq
  ```
- Export metadata:
  ```bash
  curl -s "http://localhost:3001/api/export/run?runId=<runId>" | jq
  ls -la runs/<runId>/ && head -3 runs/<runId>/packets.jsonl
  ```

## Common Errors
- `ERR_INVALID_JSON`: Request body is not valid JSON
- `ERR_MISSING_FIELDS`: Missing `problem.title` or `problem.statement`
- `ERR_ORCHESTRATOR_INIT`: Failed to initialize orchestrator (e.g., full mode without valid API key)
- `ERR_TRAVERSAL_FAILED`: Station processing error
- `ERR_RUN_NOT_FOUND`: Export files not found for `runId`
- `ERR_EXPORT_FAILED`: Internal error reading export metadata

## Orchestrator & Modes
- Foundation mode (default) runs S1–S5 + S11 and works without `OPENAI_API_KEY` (LLM fallbacks).
- Full mode (S1–S11) attempts LLM calls and requires a valid `OPENAI_API_KEY`.
- For foundation results only, send `{"options": {"mode": "foundation"}}` in the request body.

## Exports
- On success, exports are written to `runs/<runId>/`:
  - `run.json` – run summary and durations
  - `packets.jsonl` – one Packet per station
- If `/api/export/run` returns `ERR_RUN_NOT_FOUND`:
  - Verify the run completed
  - Confirm `runs/<runId>/` exists and has both files
  - Check filesystem permissions for the `runs/` directory

## Validate Packets with AJV
- Validate locally:
  ```bash
  node -e '
    const fs = require("fs");
    const Ajv = require("ajv");
    const addFormats = require("ajv-formats");
    const schema = JSON.parse(fs.readFileSync("schemas/packet.json","utf8"));
    const packets = fs.readFileSync("runs/<runId>/packets.jsonl","utf8").trim().split("\n").map(JSON.parse);
    const ajv = new Ajv({strict:false}); addFormats(ajv);
    const validate = ajv.compile(schema);
    for (const [i,p] of packets.entries()) if (!validate(p)) { console.error(`Packet ${i+1} failed`, validate.errors); process.exit(1); }
    console.log(`All ${packets.length} packets validate ✔`);
  '
  ```
- CI already validates a sample run against `schemas/packet.json`.

## Environment & Model
- `OPENAI_MODEL` controls the model (no hardcoded names in code). Example:
  ```bash
  echo $OPENAI_MODEL
  # recommended: gpt-4.1-nano
  ```
- Foundation mode does not require `OPENAI_API_KEY`. Full mode does – verify with:
  ```bash
  curl https://api.openai.com/v1/models -H "Authorization: Bearer $OPENAI_API_KEY"
  ```

## Performance & Reliability
- Disk space: ensure there’s room under `runs/`
- Port conflicts: `PORT=3002 npm run dev`
- Memory: `NODE_OPTIONS="--max-old-space-size=4096" npm run dev`

## Reset
```bash
# Stop dev server (Ctrl+C), then:
rm -rf node_modules package-lock.json .next
npm install
npm run dev
```

## Getting Help
- Include: Node/npm versions, `OPENAI_MODEL`, cURL outputs, logs, and the `runId`
- See: README.md, ARCHITECTURE.md, docs/INTERFACE.md, docs/API_REFERENCE.md
