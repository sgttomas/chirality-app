# Prompt Engineering Guide (v2 foundation)

This guide outlines station‑specific prompt strategies for S1–S5 and S11, and the fallback behavior used in foundation mode.

## Core System Prompt Architecture

- Each station call includes: modality, operation label, accumulated context (problem + prior documents), and optional matrix guidance.
- In foundation mode without an API key, LLM calls are allowed to fail; each station returns a structured fallback template.

### Station Operations (foundation)
- S1 (J): Problem analysis and categorization
- S2 (DS): Data requirements and specifications (Matrix C)
- S3 (SP): Step‑by‑step operational workflow (Matrix D)
- S4 (GD): Strategic guidance, prerequisites, successors, risks (Matrix X)
- S5 (EC): Procedural validation and quality gates (Matrix E)
- S11 (Final): Final resolution synthesis using all prior documents

### Citation Integration
```typescript
`Citations: include evidence IDs (e.g., "CIT:src#p") inside source_refs/refs/trace_back when used.`
```

## Three-Pass Orchestration Prompts

### V1 Generation (Matrix-Seeded)
When matrices are available, scaffolds are pre-loaded:

```typescript
// Matrix scaffolds converted to Triple format
const scaffoldFinals: Record<string, any> = {};
if (ingestResult.drafts.DS) scaffoldFinals.DS = { 
  text: ingestResult.drafts.DS, 
  terms_used: [], 
  warnings: ['Seeded from deterministic matrix scaffold.'] 
};

// Injected as pinned context
`---
Continuity (most recent Finals):
Pinned DS: ${compactDS(scaffoldFinals.DS.text)}
---`
```

### Context Assembly
- Problem statement is always included
- Prior station outputs are appended (DS → SP → GD → EC)
- Matrix guidance (C/D/X/E) may be provided via `initialVector`

### Fallback Strategy
- On LLM error, stations return structured placeholders with clear headings and checklists
- Packets still include durations/tokens (0) and validate against schema

## Document-Specific Prompt Strategies

### DS (Data Sheet) Prompt (S2)
**Objective**: Create precise technical specifications

```typescript
const dsPrompt = [
  `Generate a comprehensive Data Sheet (DS) for: ${problem}`,
  `Focus on concrete data elements, types, validation rules, and source traceability.`,
  `Include field definitions, constraints, relationships, and reference citations.`,
  `Structure as array of data_field objects with technical precision.`
].join('\n');
```

**Key Instructions**:
- Emphasize technical precision over narrative
- Include validation rules and constraints
- Maintain traceability to source materials
- Use standardized data type specifications

### SP (Standard Procedure) Prompt (S3)
**Objective**: Create actionable step-by-step procedures

```typescript
const spPrompt = [
  `Generate a Standard Procedure (SP) for: ${problem}`,
  `Create sequential, executable steps with clear inputs/outputs.`,
  `Include preconditions, postconditions, and reference materials.`,
  `Focus on operational clarity and implementation guidance.`
].join('\n');
```

**Key Instructions**:
- Emphasize sequential workflow structure
- Define clear inputs and expected outputs  
- Include validation checkpoints
- Reference supporting materials and tools

### GD (Guidance Document) Prompt (S4)
Focus on prerequisites, dependencies, successors, quality standards, risk considerations, and wider context integration.

### EC (Evaluation Checklist) Prompt (S5)
Define step‑wise validation procedures, measurable criteria, and process control checkpoints mapped to S1–S4 outputs.

## Context Management Strategies

### Document Compaction for RAG
```typescript
// Efficient context injection without token overflow
function compactDS(ds: DSItem[]): string {
  return ds.map(item => `${item.data_field}:${item.type || 'any'}`).join(', ');
}

function compactSP(sp: SPItem[]): string {
  return sp.map(item => `${item.step}`).join(' → ');
}

function compactX(x: XItem[]): string {
  return x.map(item => `[${item.heading}]`).join(' + ');
}

function compactM(m: MItem[]): string {
  return m.map(item => item.statement).join('; ');
}
```

### Matrix Guidance Snippets
Add concise bullet‑point excerpts from matrices (C/D/X/E) aligned to each station’s objective.

## Temperature and Parameter Management

### Generation Parameters
```typescript
// Systematic: Higher creativity for initial generation
const systematicParams = {
  temperature: 0.7,
  max_tokens: 800,
  top_p: 0.95
};

// Process/Epistemic: Balanced refinement
const processEpistemicParams = {
  temperature: 0.6,
  max_tokens: 800,
  top_p: 0.9
};

// Alethic: Conservative convergence  
const alethicParams = {
  temperature: 0.5,
  max_tokens: 800,
  top_p: 0.85
};
```

### Context Window Management
```typescript
// Automatic context truncation to stay within limits
const maxContextLength = 4000; // chars per document for RAG injection
const truncatedContext = context.length > maxContextLength 
  ? context.substring(0, maxContextLength) + '...[truncated]'
  : context;
```

## Error Handling in Prompts

### Graceful Degradation
```typescript
// Fallback prompt when context is unavailable
const fallbackPrompt = [
  `Generate a minimal ${documentType} for: ${problem}`,
  `No additional context available - provide basic structure.`,
  `Include warnings about limited context in the warnings array.`,
  `Follow strict JSON format requirements.`
].join('\n');
```

### Validation Prompts
```typescript
// Prompt validation for Packet structure compliance
`Validate response format:
- Must be valid JSON object
- Must contain: text field (required)
- text field must match document type schema
- context field optional: { terms?: string[], notes?: string[] }
- flags field optional: { risk?: boolean }`
```

## Chat Integration Prompts

### RAG Context Injection
```typescript
const chatInstructions = [
  'You are the Chirality Chat engine.',
  'Use pinned DS/SP/X/M as ground truth context for this session.',
  'Prefer cited evidence; include citation IDs when relevant.',
  'Maintain conversation continuity while staying grounded in generated documents.'
];

if (hasDocuments) {
  instructions.push('--- Pinned Finals (compact) ---');
  if (DS) instructions.push(`DS: ${compactDS(DS.text)}`);
  if (SP) instructions.push(`SP: ${compactSP(SP.text)}`);
  if (X) instructions.push(`X: ${compactX(X.text)}`);
  if (M) instructions.push(`M: ${compactM(M.text)}`);
  instructions.push('--- End Pinned ---');
}
```

### Command Recognition
```typescript
// Command detection patterns
const commandPatterns = {
  setProblem: /^set problem:\s*(.+)$/i,
  generateDoc: /^generate\s+(DS|SP|X|M)$/i,
  clearState: /^clear$/i,
  showState: /^state$/i
};
```

## Quality Assurance Prompts

### Validation Instructions
```typescript
`Quality requirements:
- Technical accuracy in specifications
- Clear actionable steps in procedures  
- Coherent integration in solution templates
- Strategic value in guidance documents
- Complete citation of all reference materials
- Appropriate warning flags for limitations`
```

### Cross-Reference Validation
```typescript
// Ensure cross-document references are valid
`Cross-reference validation:
- Verify all cited document sections exist
- Check citation format consistency  
- Ensure reference flow makes logical sense
- Flag broken or circular references in warnings`
```

## Advanced Prompt Techniques

### Iterative Refinement Pattern
```typescript
// Station refinement leverages prior station outputs
`Refinement context:
Previous station: ${JSON.stringify(priorStation.text)}
Cross-station insights: ${extractInsights(allPriorStations)}
Refinement objective: Improve coherence and cross-references

Generate improved version incorporating cross-station insights while maintaining core structure.`
```

### Matrix-Guided Generation
```typescript
// Matrix cells provide deterministic structure
`Matrix-guided generation:
Source matrix: ${cell.matrix} (${cell.station})
Row: ${cell.row_label}
Column: ${cell.col_label}  
Content: ${cell.text}
Citations: ${cell.citations}
References: ${cell.refs}

Generate ${documentType} incorporating this matrix structure while maintaining systematic approach.`
```

## Troubleshooting Common Prompt Issues

### Invalid JSON Output
**Problem**: LLM returns prose instead of JSON
**Solution**: Strengthen JSON enforcement
```typescript
`CRITICAL: Response must be valid JSON only. No explanations, no prose, no markdown.
Example: {"text":[{"data_field":"user_id","type":"string"}],"terms_used":["user","authentication"],"warnings":[]}`
```

### Incomplete Document Structure  
**Problem**: Missing required fields or poor structure
**Solution**: Enhanced schema enforcement
```typescript
`Required structure for ${docType}:
${JSON.stringify(exampleStructure, null, 2)}
All fields marked as required must be present.
Use empty arrays [] for optional list fields when no data available.`
```

### Context Overflow
**Problem**: Too much context causing truncation
**Solution**: Prioritized context injection
```typescript
// Priority order for context inclusion
1. Current document requirements (always included)
2. Direct dependencies (DS for SP, DS+SP for X, etc.)
3. Matrix scaffolds (if available)
4. Previous generation warnings
5. Additional context (truncated if needed)
```

## Performance Optimization

### Prompt Efficiency
- **Concise instructions**: Minimize token usage while maintaining clarity
- **Structured templates**: Reusable prompt components
- **Context prioritization**: Most important information first
- **Batch processing**: Combine related instructions

### Response Optimization
- **Streaming support**: Enable real-time feedback
- **Token limits**: Appropriate max_tokens for document types
- **Temperature tuning**: Balance creativity with consistency
- **Stop sequences**: Prevent over-generation

---

*Prompt engineering documentation for systematic document generation with matrix integration and iterative refinement.*
