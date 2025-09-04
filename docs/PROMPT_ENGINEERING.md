# Prompt Engineering Guide

Comprehensive guide to the systematic prompt engineering approach used in Chirality AI App for consistent, high-quality document generation.

## Core System Prompt Architecture

### Four-Document Pipeline Structure
```typescript
`You are the Chirality Prompt Engine running a four-document pipeline: DS → SP → X → M.`
`Do two passes: propose (temp=0.7) then finalize (temp=0.5).`
`STRICT JSON ONLY: {"text":<payload>,"terms_used":string[],"warnings":string[]}. No prose outside JSON.`
```

### Document-Specific Payload Keys
```typescript
// Required JSON structure per document type
- DS: {data_field, units, type, source_refs, notes}
- SP: {step, purpose, inputs, outputs, preconditions, postconditions, refs}  
- X: {heading, narrative, precedents, successors, context_notes, refs}
- M: {statement, justification, trace_back, assumptions, residual_risk}
```

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

### V2 Refinement (Cross-Referential)
```typescript
// Each document sees V1 outputs from others
if (finals?.DS) pinned.push(`Pinned DS: ${compactDS(finals.DS.text)}`);
if (finals?.SP) pinned.push(`Pinned SP: ${compactSP(finals.SP.text)}`);
if (finals?.X)  pinned.push(`Pinned X: ${compactX(finals.X.text)}`);
if (finals?.M)  pinned.push(`Pinned M: ${compactM(finals.M.text)}`);

`If new inputs conflict with pinned Finals, explain in "warnings" and prefer the latest Final unless the evidence is stronger.`
```

### V3 Convergence (Full Context)
Final refinement with complete cross-document visibility and RAG evidence injection.

## Document-Specific Prompt Strategies

### DS (Data Sheet) Prompts
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

### SP (Standard Procedure) Prompts  
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

### X (Solution Template) Prompts
**Objective**: Synthesize comprehensive solution framework

```typescript
const xPrompt = [
  `Generate a Solution Template (X) integrating DS and SP for: ${problem}`,
  `Create cohesive solution narrative combining data and procedures.`,
  `Include contextual notes, precedent analysis, and implementation strategy.`,
  `Focus on integration patterns and architectural coherence.`
].join('\n');
```

**Key Instructions**:
- Integrate insights from DS and SP documents
- Provide architectural guidance
- Include precedent analysis and pattern recognition
- Focus on solution coherence and completeness

### M (Guidance) Prompts
**Objective**: Provide strategic oversight and risk analysis

```typescript
const mPrompt = [
  `Generate strategic Guidance (M) for: ${problem}`,
  `Provide oversight, recommendations, and risk considerations.`,
  `Include justification for approach and residual risk assessment.`,
  `Focus on strategic decision-making and long-term considerations.`
].join('\n');
```

**Key Instructions**:
- Emphasize strategic thinking over tactical details
- Include risk assessment and mitigation strategies
- Provide justification for recommended approaches
- Consider long-term implications and trade-offs

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

### Matrix Integration Context
```typescript
// Matrix cells provide structured context
`Matrix context from ${matrixType}:
Station: ${cell.station}
Content: ${cell.text}
Citations: ${cell.citations.join(', ')}
References: ${cell.refs.join(', ')}`
```

## Temperature and Parameter Management

### Generation Parameters
```typescript
// V1: Higher creativity for initial generation
const v1Params = {
  temperature: 0.7,
  max_tokens: 800,
  top_p: 0.95
};

// V2: Balanced refinement
const v2Params = {
  temperature: 0.6,
  max_tokens: 800,
  top_p: 0.9
};

// V3: Conservative convergence  
const v3Params = {
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
// Prompt validation for Triple structure compliance
`Validate response format:
- Must be valid JSON object
- Must contain: text, terms_used, warnings fields
- text field must match document type schema
- terms_used must be string array
- warnings must be string array`
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
// V2 refinement leverages V1 outputs
`Refinement context:
Previous generation: ${JSON.stringify(v1Result.text)}
Cross-document insights: ${extractInsights(allV1Results)}
Refinement objective: Improve coherence and cross-references

Generate improved version incorporating cross-document insights while maintaining core structure.`
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