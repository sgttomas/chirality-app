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

# Check pipeline configuration
curl http://localhost:3001/api/pipeline/traverse | jq
```

## Core Architecture

### Semantic Valley Traversal System
Chirality implements canonical semantic valley traversal through 11 stations (S1-S11) following the ontological path: 
`{problem} → Systematic → Process → Epistemic → Process → Epistemic → Alethic → Epistemic → Alethic → Epistemic → Alethic → {resolution}`

**Station Pipeline** (S1-S11):
- **S1**: Problem Statement (problem) - J operation
- **S2**: Data Sheet (systematic) - DS operation from Matrix C
- **S3**: Standard Procedure (process) - SP operation from Matrix D  
- **S4**: Guidance Document (epistemic) - GD operation from Matrix X
- **S5**: Evaluation Checklist (process) - EC operation from Matrix E
- **S6**: Solution Statements (epistemic) - SS operation
- **S7**: Requirements Assessment (alethic) - RA operation
- **S8**: Risk Analysis (epistemic) - Risk operation
- **S9**: Implementation Plan (alethic) - IP operation
- **S10**: Quality Assurance (epistemic) - QA operation
- **S11**: Final Resolution (resolution) - Final operation

**Traversal Modes**:
- **Foundation Mode**: S1-S5 + S11 (6 stations) - Core document generation
- **Full Mode**: S1-S11 (11 stations) - Complete traversal with iteration cycles

**Data Structure**: Packet<T> provides canonical document structure with id, createdAt, station, modality, payload, and meta fields.


### Document Types & Operations
- **J**: Problem Statement Analysis from S1
- **DS**: Data Sheet generation from S2 using Matrix C
- **SP**: Standard Procedure creation from S3 using Matrix D  
- **GD**: Guidance Document generation from S4 using Matrix X
- **EC**: Evaluation Checklist creation from S5 using Matrix E
- **SS**: Solution Statements from S6
- **RA**: Requirements Assessment from S7
- **Risk**: Risk Analysis from S8
- **IP**: Implementation Plan from S9
- **QA**: Quality Assurance from S10
- **Final**: Resolution synthesis from S11

### Key System Components

#### Orchestration Engine (`/src/core/orchestrator.ts`)
- Routes all requests to semantic valley traversal pipeline
- Supports both foundation and full traversal modes
- Implements fallback mode without API key for foundation traversal
- Validates station transitions and data dependencies

#### State Management (`/src/core/state.ts`)
- In-memory state management with atomic operations
- Maintains run state, packets, and metadata
- Tracks station progression and document accumulation

#### LLM Service (`/src/core/llm/service.ts`)
- OpenAI integration with configurable models
- Disabled mode for fallback operations without API calls
- Deterministic stub content generation for testing/CI

#### Station Processors (`/src/core/stations/S[1-11].ts`)
- Individual processors for each semantic valley station
- Context-aware content generation using accumulated documents
- Matrix integration for stations S2-S5

#### API Layer (`/src/app/api/`)
- RESTful endpoints for pipeline traversal and exports
- Foundation mode support without API key requirement
- Error handling with proper status codes and messages

## Critical Implementation Details

### Environment Configuration
```bash
# Required for LLM operations
OPENAI_API_KEY=sk-proj-...     # Required for full mode, optional for foundation mode
OPENAI_MODEL=gpt-4.1-nano      # REQUIRED - no hardcoded fallbacks

# Feature flags
FEATURE_GRAPH_ENABLED=true     # Enable Neo4j graph features (optional)

# Optional for graph features
NEO4J_URI=bolt://localhost:7687
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=...
```

**Foundation Mode Fallback**: The system can run foundation mode (S1-S5+S11) without a valid API key using disabled LLM mode for testing and CI purposes.

### TypeScript Strict Mode
Project uses TypeScript strict mode - NO `as any` shortcuts allowed. Always define proper interfaces:

**Packet Structure**:
```typescript
interface Packet {
  id: string;                    // Unique identifier
  createdAt: string;            // ISO timestamp
  station: Station;             // S1-S11
  modality: Modality;           // problem|systematic|process|epistemic|alethic|resolution
  payload: Record<string, any>; // Operation results (J, DS, SP, etc.)
  meta?: {                      // Optional metadata
    duration?: number;
    tokens?: TokenUsage;
  };
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
- `/src/core/` - Core orchestration engine and services
- `/src/domain/` - Station definitions, packets, and validators
- `/src/components/` - React UI components
- `/tests/` - Test suites including fallback mode tests
- `/runs/` - Generated run exports
- `/schemas/` - JSON schemas for validation

## Testing Requirements

Before any commit:
1. Run `npm run type-check` - Must pass with zero errors
2. Run `npm run lint` - Fix all linting issues
3. Run `npm test` - Ensure all tests pass (42 expected including fallback tests)
4. Test generation manually if core logic changed

For orchestration changes:
- Verify foundation mode works without API key
- Test both foundation (6 stations) and full (11 stations) modes
- Check packet structure compliance and data dependencies

## Common Development Patterns

### Adding New API Endpoint
1. Create route in `/src/app/api/[feature]/route.ts`
2. Use NextRequest/NextResponse from 'next/server'
3. Implement proper error handling and validation
4. Add corresponding types in `/src/types/`
5. Add feature flag gating if optional (check FEATURE_GRAPH_ENABLED pattern)

### Modifying Station Processing
1. Update station logic in `/src/core/stations/S[1-11].ts`
2. Maintain Packet structure compliance with correct modality
3. Update validators in `/src/domain/validators.ts` for data dependencies
4. Test with both foundation and full traversal modes

### Adding Fallback Support
1. Use `createOrchestrator(apiKey, allowFallback)` for foundation mode without API key
2. LLMService with `disabled: true` generates deterministic stubs
3. Add comprehensive tests in `/tests/fallback.test.ts`
4. Ensure CI validation works with disabled mode

## Performance Considerations

- **Foundation Mode**: ~30 seconds (6 LLM calls, S1-S5+S11)
- **Full Mode**: 5-10 minutes (11 LLM calls, S1-S11)
- **Fallback Mode**: <1 second (no LLM calls, deterministic stubs)
- State operations: Sub-second in-memory operations
- API responses: <2 seconds first token target

## Security & Production

- Environment-based configuration - no hardcoded API keys or models
- Foundation mode fallback for CI/testing without exposing API keys
- Proper error handling with sanitized error messages
- Input validation on all API endpoints
- TypeScript strict mode enforced throughout

## Key Philosophical Concepts

### Chirality Metaphor
Knowledge has "handedness" - same facts create different knowledge based on interpretive orientation. Each document type represents different semantic chirality applied to the same problem.

### Seeds of Thought and Evidence
- **Seeds of Thought**: External matrices providing structured input
- **Seeds of Evidence**: Generated documents indexed for RAG enhancement

### Semantic Valley Traversal
Transform complex problems through controlled semantic valley traversal across ontological modalities (problem → systematic → process → epistemic → alethic → resolution), with each station building upon the accumulated semantic context from previous stations.