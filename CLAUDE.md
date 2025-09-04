# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Essential Commands

### Development
```bash
# Start development server (port 3001 with Turbopack)
npm run dev

# Alternative without Turbopack
npm run dev:webpack

# Run TypeScript type checking (CRITICAL - always run before committing)
npm run type-check

# Run linter
npm run lint

# Run tests
npm test

# Run specific test file
npx jest tests/generators.test.ts

# Test three-pass orchestration
npm run orchestrate:test

# Clean install and fresh start
npm run fresh
```

### Production
```bash
# Build for production
npm run build

# Start production server
npm run start

# Analyze bundle size
npm run analyze
```

### System Health & Debugging
```bash
# Check API health
curl http://localhost:3001/api/healthz
curl http://localhost:3001/api/readyz

# View current state
curl http://localhost:3001/api/core/state | jq

# Clear state
curl -X DELETE http://localhost:3001/api/core/state

# Debug chat system
curl http://localhost:3001/api/chat/debug | jq
```

## Core Architecture

### Three-Pass Document Generation System
The heart of Chirality is V1→V2→V3 iterative refinement that transforms problems into four document types:

1. **V1 (Matrix-Seeded Generation)**: Initial generation using external matrices as "seeds of thought" + AI enhancement
2. **V2 (Cross-Referential Refinement)**: Each document learns from V1 outputs of other documents
3. **V3 (Final Convergence)**: Complete context integration with full cross-references

Document flow: `Problem → Matrices → V1 Drafts → V2 Refinement → V3 Finals → RAG Indexing`

### Document Types & Matrix Mappings
- **DS (Data Sheet)**: Data specifications from C matrix (requirements)
- **SP (Standard Procedure)**: Workflows from D matrix (objectives)  
- **X (Solution Template)**: Integrated solutions from X+E matrices (verification/evaluation)
- **M (Guidance)**: Strategic recommendations from E matrix (evaluation)

### Key System Components

#### Orchestration Engine (`/src/chirality-core/orchestrate.ts`)
- Manages three-pass generation with dependency tracking
- Handles matrix integration and deterministic scaffolding
- Implements Triple structure (text, terms_used, warnings) validation

#### State Management (`/src/chirality-core/state/store.ts`)
- File-based persistence in `/store/state.json`
- Atomic operations with lockfile protection
- Maintains problem statement and all generated documents

#### RAG Pipeline (`/src/chirality-core/rag/`)
- Indexes generated documents as "seeds of evidence"
- 4000 char limit per document for context injection
- Powers chat interface with grounded responses

#### Framework Integration (`/lib/framework/ingest.ts`)
- Ingests JSONL matrix snapshots from chirality-framework
- Validates against strict schema (v1.0.0)
- Generates deterministic scaffolds ordered by meta.order then id

#### API Layer (`/src/app/api/`)
- RESTful endpoints for generation, chat, and state
- Server-sent events for streaming responses
- RBAC with approver roles for export operations

## Critical Implementation Details

### Environment Configuration
```bash
# Required in .env.local
OPENAI_API_KEY=sk-proj-...
OPENAI_MODEL=gpt-4.1-nano

# Optional for graph features
FEATURE_GRAPH_ENABLED=true
NEO4J_URI=bolt://localhost:7687
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=...
```

### TypeScript Strict Mode
Project uses TypeScript strict mode - NO `as any` shortcuts allowed. Always define proper interfaces:
```typescript
interface Triple<T> {
  text: T;
  terms_used: string[];
  warnings: string[];
}
```

### Matrix Cell Structure
When working with framework integration, matrices must follow:
```typescript
interface MatrixCell {
  id: string;           // Format: "C:r1:c1"
  matrix: 'C'|'D'|'X'|'E';
  row: number;          // REQUIRED - not row_label
  col: number;          // REQUIRED - not col_label
  row_label: string;
  col_label: string;
  station: string;      // Must match framework stations exactly
  text: string;
  citations: string[];
  refs: string[];
  meta?: { order?: number };
}
```

### Error Handling Patterns
Always use production-ready error handling:
```typescript
try {
  const result = await processGeneration(request);
  return NextResponse.json(result);
} catch (error) {
  console.error('Generation failed:', error);
  return NextResponse.json(
    { error: error instanceof Error ? error.message : 'Unknown error' },
    { status: 500 }
  );
}
```

### File Organization
- `/src/app/api/` - Next.js API routes (App Router)
- `/src/chirality-core/` - Core orchestration engine
- `/lib/` - Generators, framework integration, utilities
- `/src/components/` - React UI components
- `/fixtures/runs/` - Test framework run data
- `/store/` - Persistent state storage

## Testing Requirements

Before any commit:
1. Run `npm run type-check` - Must pass with zero errors
2. Run `npm run lint` - Fix all linting issues
3. Run `npm test` - Ensure all tests pass (52 expected)
4. Test generation manually if core logic changed

For matrix integration changes:
- Test with `fixtures/runs/sample_happy_001/`
- Verify deterministic ordering (meta.order then id)
- Check Triple structure compliance

## Common Development Patterns

### Adding New API Endpoint
1. Create route in `/src/app/api/[feature]/route.ts`
2. Use NextRequest/NextResponse from 'next/server'
3. Implement proper error handling and validation
4. Add corresponding types in `/src/types/`

### Modifying Document Generation
1. Update generator in `/lib/generator/[type].ts`
2. Maintain Triple structure compliance
3. Update validators in `/src/chirality-core/validators.ts`
4. Test with three-pass orchestration

### Working with Matrices
1. Ingest with `/lib/framework/ingest.ts`
2. Generate scaffolds maintaining order (meta.order → id)
3. Pass to generators via `initialVector`
4. Preserve citations and refs from matrix cells

### Implementing RAG Features
1. Respect corpus limits (4000 chars per doc)
2. Use compactor functions for document reduction
3. Index after generation completion
4. Test chat context injection

## Performance Considerations

- Three-pass generation: 2-4 minutes (12 LLM calls)
- Single document: 3-8 seconds
- Chat first token: <2 seconds target
- State operations: Must be sub-second
- Use streaming for long operations via PassThrough

## Security & Production

- RBAC enforced for exports (x-role: approver header)
- SOC2 audit logging for compliance
- No secrets in code - use environment variables
- Validate all external inputs
- Atomic file operations with lockfile protection

## Key Philosophical Concepts

### Chirality Metaphor
Knowledge has "handedness" - same facts create different knowledge based on interpretive orientation. Each document type represents different semantic chirality applied to the same problem.

### Seeds of Thought and Evidence
- **Seeds of Thought**: External matrices providing structured input
- **Seeds of Evidence**: Generated documents indexed for RAG enhancement

### Systematic Semantic Operations
Transform complex problems through controlled semantic stereochemistry - systematic manipulation of interpretive handedness through three-pass refinement.