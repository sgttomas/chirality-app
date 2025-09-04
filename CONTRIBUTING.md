# Contributing to Chirality AI App

Welcome! This guide covers everything you need to contribute to the Chirality AI App - a Next.js application implementing three-pass semantic document generation with matrix-driven orchestration and RAG-enhanced chat.

## Quick Start for Contributors

### Development Setup
```bash
git clone <repository-url>
cd chirality-app
npm install
cp .env.example .env.local  # Add your OpenAI API key
npm run dev
```

### First Contribution Test
1. Navigate to `http://localhost:3001/chirality-core`
2. Enter: "implement a todo list app"
3. Choose "🔄 Three-Pass with Matrix Integration"
4. Verify all 4 documents generate correctly
5. Test chat integration at `/` using generated documents

## Core System Understanding

### Three-Pass Orchestration
The heart of this application is the V1→V2→V3 iterative refinement process:

1. **V1**: Matrix-seeded deterministic scaffolds + AI enhancement
2. **V2**: Cross-referential refinement using insights from other documents  
3. **V3**: Final convergence with full context integration

### Matrix Integration
External semantic matrices serve as "seeds of thought":
- **C matrix** → DS documents (requirements → data specifications)
- **D matrix** → SP documents (objectives → procedures)
- **X+E matrices** → X documents (verification + evaluation → solutions) 
- **E matrix** → M documents (evaluation → guidance)

### Document Types
- **DS** (Data Sheet) - Technical specifications, data fields, validation rules
- **SP** (Standard Procedure) - Step-by-step workflows with inputs/outputs
- **X** (Solution Template) - Integrated solution frameworks
- **M** (Guidance) - Strategic recommendations and risk analysis

## Development Guidelines

### TypeScript Standards
```typescript
// ✅ Good: Explicit interfaces and proper error handling
interface GenerationRequest {
  problem: string;
  context?: Record<string, unknown>;
  options?: GenerationOptions;
}

export async function generateDocument(request: GenerationRequest): Promise<Triple<DocumentItem[]>> {
  try {
    const result = await processGeneration(request);
    return result;
  } catch (error) {
    throw new Error(`Generation failed: ${error instanceof Error ? error.message : 'Unknown error'}`);
  }
}

// ❌ Avoid: Implicit any and poor error handling
async function generate(req: any) {
  return await process(req);
}
```

### React Component Patterns
```tsx
// ✅ Good: Proper TypeScript interfaces with error boundaries
interface ChatMessageProps {
  content: string;
  author: 'user' | 'assistant';
  timestamp?: string;
}

export function ChatMessage({ content, author, timestamp }: ChatMessageProps) {
  return (
    <ErrorBoundary fallback={<MessageErrorFallback />}>
      <div className={`message ${author}`}>
        <div className="content">{content}</div>
        {timestamp && <time className="timestamp">{timestamp}</time>}
      </div>
    </ErrorBoundary>
  );
}
```

### API Route Standards
```typescript
// ✅ Good: Comprehensive error handling with proper HTTP status codes
export async function POST(request: Request) {
  try {
    const body = await request.json();
    
    if (!isValidGenerationRequest(body)) {
      return NextResponse.json(
        { error: 'Invalid request format', details: getValidationErrors(body) },
        { status: 400 }
      );
    }

    const result = await processDocumentGeneration(body);
    return NextResponse.json(result);
    
  } catch (error) {
    console.error('Document generation error:', error);
    return NextResponse.json(
      { error: 'Internal server error', timestamp: new Date().toISOString() },
      { status: 500 }
    );
  }
}
```

## Testing Strategy

### Manual Testing Requirements
For all contributions, test these critical workflows:

**Document Generation**:
- [ ] Single-pass generation for all document types (DS/SP/X/M)
- [ ] Three-pass generation with proper V1→V2→V3 progression
- [ ] Matrix integration with external framework run IDs
- [ ] Error handling for malformed inputs
- [ ] State persistence across browser sessions

**Chat Integration**:
- [ ] RAG context injection from generated documents
- [ ] Streaming chat responses work correctly
- [ ] Command detection (`set problem:`, `generate DS`, etc.)
- [ ] Conversation continuity across multiple exchanges

**System Integration**:
- [ ] Admin dashboard shows correct system state
- [ ] Export functionality generates proper ZIP archives
- [ ] Error boundaries prevent UI crashes
- [ ] Cross-browser compatibility (Chrome, Firefox, Safari, Edge)

### Automated Testing
```bash
npm run type-check  # TypeScript validation (required)
npm run lint        # Code quality checks (required)  
npm test           # Unit tests (run if available)
```

## Contribution Workflow

### Branch Strategy
- **Feature branches**: `feature/add-export-functionality`
- **Bug fixes**: `fix/chat-input-validation`
- **Documentation**: `docs/update-contributing-guide`

### Commit Message Format
```
type(scope): brief description

Documentation Assessment: STANDARD_UPDATE
Scope: TECHNICAL_ACCURACY, USER_EXPERIENCE  
Methodology: FEATURE_DOCUMENTATION

Detailed description of changes, motivation, and impact.
Includes any breaking changes or migration requirements.
```

### Pull Request Requirements
1. **Clear Description**: What problem does this solve? How does it work?
2. **Testing Evidence**: Screenshots, test results, or manual test confirmation
3. **Documentation Updates**: Update relevant docs for user-facing changes
4. **Breaking Changes**: Clear communication of any API or behavior changes

## Key Implementation Areas

### Core Orchestration Engine
**Location**: `src/chirality-core/`
- Document generation logic and three-pass orchestration
- State management with file-based persistence
- LLM integration with OpenAI API
- Validation and error handling systems

### API Layer  
**Location**: `src/app/api/`
- RESTful endpoints for document generation
- Server-sent events for streaming chat
- State management endpoints
- External framework integration

### UI Components
**Location**: `src/components/` and `src/app/`
- Chat interface with real-time streaming
- Document generation interface with progress tracking
- Admin dashboard for system monitoring
- Error boundaries and loading states

### Matrix Integration
**Location**: `src/lib/`
- External framework ingestion
- Matrix-driven generation
- RAG pipeline implementation
- Graph mirror synchronization

## Advanced Topics

### Adding New Document Types
1. Define interface in `src/types/framework.ts`
2. Add generator in `src/lib/generator/`
3. Update orchestration logic in `src/lib/orchestrator/agent.ts`
4. Add validation in validators
5. Update UI components to display new type

### Enhancing Matrix Integration
1. Modify ingestion logic in `src/lib/framework/ingest.ts`
2. Update generator context in `src/lib/generator/types.ts`
3. Enhance matrix-to-scaffold mapping
4. Test with real framework run data

### Improving RAG Performance
1. Optimize document compaction in `src/chirality-core/state/store.ts`
2. Enhance context injection in `src/app/api/chat/stream/route.ts`
3. Improve semantic chunking for better retrieval
4. Test with various document sets

## Quality Assurance

### Code Review Checklist
- [ ] TypeScript strict mode compliance
- [ ] Proper error handling and user feedback
- [ ] Documentation updates for user-facing changes
- [ ] Performance impact assessment
- [ ] Security considerations (input validation, API key handling)
- [ ] Cross-platform compatibility

### Documentation Standards
- **Accuracy**: All examples must be copy-pasteable and working
- **Completeness**: Cover edge cases and error scenarios
- **Clarity**: Write for your intended audience with appropriate detail
- **Currency**: Keep documentation synchronized with code changes

## Getting Help

### Resources
- **[TROUBLESHOOTING.md](TROUBLESHOOTING.md)** - Common issues and solutions
- **[docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)** - System design details
- **[docs/INTERFACE.md](docs/INTERFACE.md)** - Framework contract specification

### Community
- **GitHub Issues**: Bug reports and feature requests
- **GitHub Discussions**: Architecture discussions and questions
- **Code Reviews**: Collaborative improvement through peer review

---

*Contributing to Chirality AI App means participating in systematic semantic operations that transform complex problems into structured, actionable solutions. Your contributions help build a more capable and reliable document generation platform.*