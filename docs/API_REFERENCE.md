# API Reference

Complete REST API documentation for Chirality AI App endpoints.

**Base URL**: `http://localhost:3001` (development)  
**Authentication**: OpenAI API key via environment variables

## Core Endpoints

### Document Generation

#### POST /api/core/orchestrate
**Three-pass document generation with matrix integration**

Generates all four document types (DS/SP/X/M) using V1→V2→V3 iterative refinement with optional matrix-driven scaffolding.

**Request**:
```typescript
{} // Empty body - uses current problem from state
```

**Response**:
```typescript
{
  success: true,
  pass1: {
    DS: Triple<DSItem[]>,
    SP: Triple<SPItem[]>, 
    X: Triple<XItem[]>,
    M: Triple<MItem[]>
  },
  pass2: {
    DS: Triple<DSItem[]>,
    SP: Triple<SPItem[]>,
    X: Triple<XItem[]>, 
    M: Triple<MItem[]>
  },
  final: {
    X: Triple<XItem[]>  // Final resolution
  },
  logs: string[],        // Generation progress logs
  totalTimeSeconds: number
}
```

#### POST /api/core/run  
**Single document generation**

**Request**:
```typescript
{
  kind: "DS" | "SP" | "X" | "M"  // Document type to generate
}
```

**Response**:
```typescript
{
  kind: string,           // Document type generated
  triple: Triple<any>,    // Generated document with metadata
  latencyMs: number      // Generation time in milliseconds
}
```

#### POST /api/agent/run
**External framework run processing with matrix integration**

**Request**:
```typescript
{
  framework_run_id: string,  // Framework run identifier
  enable_rag?: boolean,      // Enable RAG indexing
  options?: {
    phase_timing?: boolean,   // Include detailed timing
    validation?: boolean      // Strict validation mode
  }
}
```

**Response**:
```typescript
{
  success: boolean,
  run_id: string,
  agent_result: {
    matrices: {
      C: MatrixCell[],
      D: MatrixCell[],
      X: MatrixCell[],
      E: MatrixCell[]
    },
    drafts: {
      DS?: any,
      SP?: any,
      X?: any,
      M?: any
    },
    finals: {
      DS: Triple<any>,
      SP: Triple<any>,
      X: Triple<any>,
      M: Triple<any>
    }
  },
  timing: {
    framework_ms: number,
    ingestion_ms: number,
    refinement_ms: number,
    persistence_ms: number
  }
}
```

#### GET /api/agent/export/[runId]
**Streaming export with RBAC validation**

**Headers Required**:
```
x-role: approver  // Must have approver role
```

**Response**: Streaming ZIP file with complete run artifacts

### Chat Interface

#### POST /api/chat/stream
**RAG-enhanced streaming chat with document context**

**Request**:
```typescript
{
  message: string,              // User message
  conversationId?: string      // Optional conversation tracking
}
```

**Response**: Server-Sent Events stream
```
data: {"type": "content", "content": "partial response text"}
data: {"type": "content", "content": " more text"}
data: {"type": "done"}
```

#### GET /api/chat/debug
**System status and debugging information**

**Response**:
```typescript
{
  status: "operational",
  documents: {
    hasDS: boolean,
    hasSP: boolean,
    hasX: boolean,
    hasM: boolean
  },
  problem: string | null,
  lastGenerated: string | null,
  systemInfo: {
    model: string,
    timestamp: string
  }
}
```

### State Management

#### GET /api/core/state
**Retrieve current application state**

**Response**:
```typescript
{
  problem?: {
    statement: string
  },
  finals?: {
    DS?: Triple<DSItem[]>,
    SP?: Triple<SPItem[]>,
    X?: Triple<XItem[]>,
    M?: Triple<MItem[]>
  },
  metadata?: {
    lastGenerated: string,
    generationMode: "single" | "three-pass"
  }
}
```

#### POST /api/core/state
**Update application state**

**Request**:
```typescript
{
  problem?: {
    statement: string
  },
  finals?: {
    DS?: Triple<DSItem[]>,
    SP?: Triple<SPItem[]>, 
    X?: Triple<XItem[]>,
    M?: Triple<MItem[]>
  }
}
```

#### DELETE /api/core/state
**Clear all application state**

**Response**:
```typescript
{
  success: true,
  message: "State cleared successfully"
}
```

### Health Monitoring

#### GET /api/healthz
**Basic health check**

**Response**:
```typescript
{
  status: "healthy",
  timestamp: string
}
```

#### GET /api/readyz
**Readiness check with dependencies**

**Response**:
```typescript
{
  status: "ready",
  checks: {
    openai: "connected" | "error",
    storage: "accessible" | "error"
  },
  timestamp: string
}
```

## Data Types

### Triple Structure
All documents follow the Triple pattern:

```typescript
interface Triple<T> {
  text: T,                    // Document-specific content structure
  terms_used: string[],       // Keywords and terms used in generation
  warnings: string[]          // Generation warnings and notes
}
```

### Document Content Types

#### DS (Data Sheet)
```typescript
interface DSItem {
  data_field: string,         // Data element name
  type?: string,              // Data type specification
  units?: string,             // Units of measurement
  source_refs?: string[],     // Reference sources
  notes?: string[]            // Additional notes
}
```

#### SP (Standard Procedure)
```typescript
interface SPItem {
  step: string,               // Procedure step description
  purpose?: string,           // Step objective
  inputs?: string[],          // Required inputs
  outputs?: string[],         // Expected outputs
  preconditions?: string[],   // Prerequisites
  postconditions?: string[],  // Post-step conditions
  refs?: string[]             // Reference materials
}
```

#### X (Solution Template)
```typescript
interface XItem {
  heading: string,            // Solution section heading
  narrative: string,          // Detailed description
  precedents?: string[],      // Dependencies
  successors?: string[],      // Follow-up items
  context_notes?: string[],   // Contextual information
  refs?: string[]             // References
}
```

#### M (Guidance)
```typescript
interface MItem {
  statement: string,          // Guidance statement
  justification?: string,     // Reasoning
  trace_back?: string[],      // Supporting evidence
  assumptions?: string[],     // Underlying assumptions
  residual_risk?: string[]    // Remaining risks
}
```

### Matrix Types
```typescript
interface MatrixCell {
  id: string;
  matrix: 'C' | 'D' | 'X' | 'E';
  row: number;
  col: number;
  row_label: string;
  col_label: string;
  station: string;
  text: string;
  citations: string[];
  refs: string[];
  meta?: { order?: number; [k: string]: unknown };
}
```

## Error Handling

### Standard Error Response
```typescript
{
  error: string,              // Error message
  details?: any,              // Additional error details
  timestamp: string           // Error timestamp
}
```

### HTTP Status Codes
- **200 OK**: Successful request
- **400 Bad Request**: Invalid request parameters
- **401 Unauthorized**: Missing or invalid authentication
- **403 Forbidden**: Insufficient permissions (RBAC)
- **500 Internal Server Error**: Server-side error
- **503 Service Unavailable**: External API unavailable

## Authentication & Security

### Environment Configuration
```bash
# Required
OPENAI_API_KEY=sk-proj-your-api-key-here
OPENAI_MODEL=gpt-4.1-nano

# Optional - Matrix Integration
FEATURE_GRAPH_ENABLED=true
NEO4J_URI=bolt://localhost:7687
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=your-neo4j-password

# Optional - Export Security  
RBAC_ENABLED=true  # Requires approver role for exports
```

### API Security
- **Core Endpoints**: No authentication required (OpenAI key managed server-side)
- **Export Endpoints**: RBAC with approver role requirement when enabled
- **Rate Limiting**: Based on OpenAI account limits
- **Input Validation**: Request sanitization and type checking

## Performance Characteristics

### Generation Timing
- **Single Document**: 3-8 seconds per document
- **Three-Pass Generation**: 2-4 minutes total (12 LLM calls)
- **Matrix Integration**: +30-60 seconds for framework ingestion

### Chat Response Timing
- **First Token**: 500ms-2s depending on context size
- **Streaming Rate**: 20-50 tokens/second
- **Context Injection**: Minimal latency impact

### Concurrency Support
- **Document Generation**: 5 concurrent generations recommended
- **Chat Streams**: 100+ concurrent connections supported
- **State Operations**: High concurrency with atomic file locking

## Usage Examples

### Complete Workflow
```typescript
// 1. Set problem statement
await fetch('/api/core/state', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    problem: { statement: 'Implement user authentication system' }
  })
});

// 2. Generate documents with three-pass process
const generation = await fetch('/api/core/orchestrate', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({})
});

const documents = await generation.json();

// 3. Chat with document context
const chatResponse = await fetch('/api/chat/stream', {
  method: 'POST', 
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    message: 'What are the security considerations for password storage?'
  })
});
```

### Matrix Integration Workflow
```typescript
// 1. Process external framework run with matrices
const agentResult = await fetch('/api/agent/run', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    framework_run_id: 'sample_happy_001',
    enable_rag: true,
    options: { phase_timing: true, validation: true }
  })
});

// 2. Export complete run with RBAC validation
const exportStream = await fetch('/api/agent/export/abc123', {
  headers: { 'x-role': 'approver' }
});

// Stream comes as ZIP file download
```

---

*API Reference for Chirality AI App - Complete endpoint documentation with examples and type definitions.*