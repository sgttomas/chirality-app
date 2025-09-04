# Chirality AI App

A Next.js application that transforms complex problems into structured solutions through three-pass semantic document generation, enhanced by RAG chat and matrix-driven orchestration.

## What It Does

**Chirality AI** generates coherent, cross-referenced documents through a systematic three-pass refinement process:

1. **Matrix Integration**: Leverages semantic matrices from chirality-framework as "seeds of thought"
2. **Document Generation**: Creates DS/SP/X/M documents through V1→V2→V3 iterative refinement  
3. **RAG Enhancement**: Uses generated documents as evidence for intelligent chat responses

### Core Document Types
- **DS** (Data Sheet) - Data specifications, fields, types, validation rules
- **SP** (Standard Procedure) - Step-by-step implementation workflows
- **X** (Solution Template) - Integrated solution frameworks with verification criteria
- **M** (Guidance) - Strategic recommendations, risk analysis, best practices

## Quick Start

### Prerequisites
- Node.js 18+
- OpenAI API key
- Optional: Neo4j for graph features

### Installation
```bash
npm install
cp .env.example .env.local
# Edit .env.local with your OpenAI API key
npm run dev
```

Visit http://localhost:3001 to start generating documents and chatting.

## How It Works

### Three-Pass Orchestration
1. **V1**: Matrix-seeded deterministic scaffolds → AI enhancement
2. **V2**: Cross-referential refinement using insights from other documents  
3. **V3**: Final convergence with full context integration

### Matrix-Driven Generation
External matrices (from chirality-framework) serve as structured "seeds of thought":
- **C matrix** → DS documents (requirements → data specifications)
- **D matrix** → SP documents (objectives → procedures) 
- **X+E matrices** → X documents (verification + evaluation → solutions)
- **E matrix** → M documents (evaluation → guidance)

### RAG Chat Integration
Generated documents become "seeds of evidence" for intelligent conversations:
- Automatic context injection from your generated documents
- Grounded responses with citation support
- Maintains conversation coherence across sessions

## Project Structure

```
src/
├── app/                    # Next.js App Router
│   ├── chirality-core/     # Document generation interface  
│   ├── chat-admin/         # System monitoring dashboard
│   └── api/
│       ├── core/           # Document generation endpoints
│       ├── chat/           # RAG streaming chat
│       └── agent/          # External framework integration
├── chirality-core/         # Core orchestration engine
├── lib/                    # Generator libraries, ingestion, utilities
└── components/             # React UI components
```

## Usage Examples

### Document Generation
```bash
# Navigate to /chirality-core
# Enter: "implement user authentication system"  
# Choose: "🔄 Three-Pass with Matrix Integration"
# Result: Structured DS/SP/X/M documents with cross-references
```

### Enhanced Chat
```bash
# After generating documents, use chat:
# Ask: "How should I handle password reset flows?"
# AI response: References your generated DS/SP documents automatically
```

### Matrix Integration
```bash
# External matrix processing:
POST /api/agent/run
{ "framework_run_id": "sample_001", "enable_rag": true }
# Uses chirality-framework matrices as generation seeds
```

## Development

### Available Scripts
- `npm run dev` - Development server
- `npm run build` - Production build
- `npm run type-check` - TypeScript validation  
- `npm run lint` - Code linting
- `npm test` - Run test suites

### Key Technologies
- **Frontend**: Next.js 15, React 18, TypeScript, Tailwind CSS
- **AI**: OpenAI API with streaming support
- **State**: File-based JSON persistence + Zustand
- **Graph**: Optional Neo4j integration for enhanced discovery

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for development guidelines, coding standards, and contribution workflow.

## Documentation

- **[TROUBLESHOOTING.md](TROUBLESHOOTING.md)** - Common issues and solutions
- **[ROADMAP.md](ROADMAP.md)** - Project direction and planned features  
- **[CHANGELOG.md](CHANGELOG.md)** - Version history and changes
- **[docs/](docs/)** - Technical specifications and architecture details

## License

MIT - See LICENSE file for details.

---

*Transform complex problems into structured solutions with AI-powered three-pass document generation.*