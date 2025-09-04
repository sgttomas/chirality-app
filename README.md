# Chirality App (v2.0.0)

[![CI](https://github.com/sgttomas/chirality-app/actions/workflows/ci.yml/badge.svg)](https://github.com/sgttomas/chirality-app/actions/workflows/ci.yml)

A lean Next.js application that transforms problem statements into structured documents via the canonical 11‑station semantic valley pipeline. v2.0.0 introduces a greenfield implementation with a default “foundation” mode (S1–S5 + S11), strict packet schema, exports, API surface, UI, and CI with a legacy sweep.

## What It Does

The app produces four core documents and a final resolution:

- S1: Problem analysis (J)
- S2: Data Sheet (DS from Matrix C)
- S3: Standard Procedure (SP from Matrix D)
- S4: Guidance Document (GD from Matrix X)
- S5: Evaluation Checklist (EC from Matrix E)
- S11: Final Resolution (Final)

Modes:
- Foundation (default): S1→S2→S3→S4→S5→S11
- Full: S1→…→S11 (S6–S10 reserved for iterative refinement; placeholders today)

## Quick Start

### Prerequisites
- Node.js 18+
- Optional: OpenAI API key (foundation mode works without one via LLM fallbacks)

### Installation
```bash
npm install
cp .env.example .env.local
# Edit .env.local with your OpenAI API key
npm run dev
```

Visit http://localhost:3001. Enter a problem, pick a traversal mode, and run.

Environment variables (configure in `.env.local`):
```
# Required only if you want real LLM output; otherwise foundation mode uses fallbacks
OPENAI_API_KEY=sk-proj-...

# Single source of truth for the model (code reads the env var only)
OPENAI_MODEL=gpt-4.1-nano
```

## How It Works

### 11‑Station Pipeline with Foundation Mode
The canonical stations are S1–S11 across modalities: problem → systematic → process → epistemic → process → epistemic → alethic → epistemic → alethic → resolution. The app defaults to a “foundation” path (S1–S5 + S11) that generates the 4 core documents and a final resolution quickly.

### Matrix‑Guided Generation
Framework matrices seed generation conceptually:
- C → Data Sheet (S2)
- D → Standard Procedure (S3)
- X → Guidance Document (S4)
- E → Evaluation Checklist (S5)

### Packets and Exports
- Every station emits a Packet saved to `runs/<runId>/packets.jsonl` and summarized in `runs/<runId>/run.json`.
- Canonical schema lives at `schemas/packet.json` and is validated in CI.

## Project Structure

```
schemas/                # JSON Schemas (packet.json)
src/
  app/
    api/
      export/run/       # GET export current run metadata
      pipeline/traverse/# POST run traversal
    page.tsx            # UI entry with traversal form
  components/           # TraversalInterface, Modality chips, etc.
  core/
    llm/                # LLM service (reads OPENAI_MODEL)
    stations/           # S1..S11 processors
    orchestrator.ts     # Mode-aware traversal execution
    state.ts            # Run state and document store
    exporter.ts         # Writes run.json + packets.jsonl
  domain/               # Station/Packet types, validators
```

## Usage Examples

### Run Foundation Traversal (UI)
1) Start dev server: `npm run dev`
2) Open `http://localhost:3001`
3) Enter a problem and keep mode = Foundation
4) Submit and view S1..S5 + S11 outputs

### Run Foundation Traversal (API)
```bash
curl -s -X POST http://localhost:3001/api/pipeline/traverse \
  -H 'Content-Type: application/json' \
  -d '{
        "problem": { "title": "Auth", "statement": "Implement user authentication" },
        "options": { "mode": "foundation" }
      }' | jq '.traversalId, .resolution[0:120]'
```

### Inspect Exported Files
```bash
curl -s "http://localhost:3001/api/export/run?runId=<yourRunId>" | jq
cat runs/<yourRunId>/run.json | jq
wc -l runs/<yourRunId>/packets.jsonl
```

### Validate a Run Locally (AJV)
```bash
# Validate all packets against schemas/packet.json using AJV (node one-liner)
node -e '
  const fs = require("fs");
  const Ajv = require("ajv");
  const addFormats = require("ajv-formats");
  const schema = JSON.parse(fs.readFileSync("schemas/packet.json","utf8"));
  const packets = fs.readFileSync("runs/<yourRunId>/packets.jsonl","utf8").trim().split("\n").map(JSON.parse);
  const ajv = new Ajv({strict:false}); addFormats(ajv);
  const validate = ajv.compile(schema);
  for (const [i,p] of packets.entries()) if (!validate(p)) { console.error(`Packet ${i+1} failed`, validate.errors); process.exit(1); }
  console.log(`All ${packets.length} packets validate ✔`);
'
```

## Development

### Available Scripts
- `npm run dev` - Development server
- `npm run build` - Production build
- `npm run type-check` - TypeScript validation  
- `npm run lint` - Code linting
- `npm test` - Run test suites

### CI
- Typecheck, lint, tests, build
- Generate sample traversal; validate packets via AJV against `schemas/packet.json`
- Uploads build artifacts and a sample run ZIP
- Legacy sweep rejects deprecated patterns (see workflow)

### Key Technologies
- Next.js 15 + React 18 + TypeScript
- OpenAI API via centralized LLM service; `OPENAI_MODEL` env var
- File-based run exports (JSON + JSONL)

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for development guidelines, coding standards, and contribution workflow.

## Documentation

- **[TROUBLESHOOTING.md](TROUBLESHOOTING.md)** - Common issues and solutions
- **[ROADMAP.md](ROADMAP.md)** - Project direction and planned features
- **[CHANGELOG.md](CHANGELOG.md)** - Version history and changes
- **[docs/](docs/)** - API reference, tutorial, and architecture details

Migration from v1? See [docs/MIGRATION.md](docs/MIGRATION.md).

## License

MIT - See LICENSE file for details.

---

*Transform complex problems into structured solutions through an 11‑station semantic valley pipeline.*
