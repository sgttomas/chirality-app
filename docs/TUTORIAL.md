# chirality‑app Tutorial (v2 foundation)

Hands-on guide to generating structured documents via the foundation traversal (S1–S5 + S11).

## Getting Started

### Prerequisites
- Node.js 18+
- Optional: OpenAI API key (foundation mode works without it)

### Quick Setup
```bash
git clone <repository-url>
cd chirality-app
npm install
cp .env.example .env.local
# Edit .env.local: Add your OpenAI API key
npm run dev
```

Visit http://localhost:3001 to begin.

## Tutorial 1: Basic Document Generation

### Step 1: Set Your Problem
1. Navigate to http://localhost:3001
2. Enter a clear problem statement:
   ```
   Implement a user authentication system for a web application
   ```
3. Click "Update Problem Statement"

### Step 2: Generate Documents (Foundation Mode)
1. Keep mode = Foundation (S1–S5 + S11)
2. Submit and wait for completion (fast path)

### Step 3: Explore Generated Documents
You'll receive four structured documents and a resolution:

**DS (Data Sheet)**
```json
{
  "data_field": "user_credentials",
  "type": "object", 
  "units": "record",
  "source_refs": ["CIT:security_spec#p1"],
  "notes": ["Includes password hash and salt"]
}
```

**SP (Standard Procedure)**  
```json
{
  "step": "validate_user_credentials",
  "purpose": "Authenticate user login attempt",
  "inputs": ["username", "password"],
  "outputs": ["authentication_result", "session_token"],
  "preconditions": ["User exists in database"],
  "postconditions": ["Valid session created or error returned"]
}
```

**GD (Guidance Document)** — Strategic guidance

**EC (Evaluation Checklist)** — Validation procedures

**Final (Resolution)** — Synthesis from all prior documents

### Step 4: Understand the Foundation Traversal
- S1 (J), S2 (DS), S3 (SP), S4 (GD), S5 (EC), S11 (Final)
Later stations build on earlier ones to create a coherent resolution.

## Tutorial 2: Export and Validate

### Step 1: Inspect Exported Files
```bash
curl -s "http://localhost:3001/api/export/run?runId=<runId>" | jq
cat runs/<runId>/run.json | jq
head -3 runs/<runId>/packets.jsonl
```

Tip: You can download `run.json` and `packets.jsonl` via the UI buttons on the results panel, or access them directly from the `runs/<runId>/` directory.

### Step 2: Validate Against Schema
See `tests/schema.test.ts` for an example using AJV.

### Step 3: Commands in Chat
Use special commands to control the system:

```bash
set problem: Design a payment processing system
# Changes the problem statement

generate DS
# Generates only the Data Sheet document

clear
# Clears all generated documents and starts fresh

state  
# Shows current system state and available documents
```

## Tutorial 3: Matrix Guidance (Advanced)

### Step 1: Understand Matrix-Driven Generation
Matrix integration uses external semantic matrices as "seeds of thought":

- **C matrix** → DS documents (requirements → data specifications)
- **D matrix** → SP documents (objectives → procedures)  
- **X matrix** → GD documents (guidance)
- **E matrix** → EC documents (evaluation)

### Step 2: Using Guidance in Prompts
Provide selected matrix elements via `initialVector` when posting to `/api/pipeline/traverse`.

### Step 3: Matrix-Enhanced Generation
When matrices are available:
1. Deterministic scaffolds are pre-generated from matrix content
2. AI enhances these scaffolds during systematic stations (S1)
3. Process and epistemic stations build systematic refinement
4. Result combines structured matrix input with AI creativity

## Tutorial 4: Administration

There is no admin dashboard in v2. Basic health endpoints may not be present. Focus on traversal and export endpoints noted above.

## Tutorial 5: Advanced Features

### Custom Problem Types
Try different problem categories to see how the system adapts:

**Technical Problems**:
```
"Design a microservices architecture for an e-commerce platform"
```

**Process Problems**:  
```
"Create an onboarding process for new software engineers"
```

**Analysis Problems**:
```
"Analyze the risks of migrating from monolith to microservices"
```

### Multi-Session Workflows
1. **Session 1**: Generate documents for "user authentication"
2. **Session 2**: Clear state, generate documents for "session management"  
3. **Session 3**: Use chat to discuss how both systems integrate

The AI maintains conversation continuity while adapting to current document context.

### Quality Assessment
Evaluate document quality using these criteria:

**DS Quality Indicators**:
- Clear data field definitions
- Appropriate type specifications
- Valid source references
- Comprehensive validation rules

**SP Quality Indicators**:
- Sequential, actionable steps
- Clear inputs and outputs  
- Realistic preconditions and postconditions
- Helpful reference materials

**X Quality Indicators**:
- Coherent solution narrative
- Proper integration of DS and SP insights
- Clear precedent and successor relationships
- Contextual implementation guidance

**M Quality Indicators**:
- Strategic, not tactical focus
- Evidence-based justifications
- Comprehensive risk assessment
- Actionable recommendations

## Troubleshooting Your Tutorial

### Generation Issues
**Problem**: Documents don't generate or are incomplete
**Check**: 
1. OpenAI API key is valid: `curl https://api.openai.com/v1/models -H "Authorization: Bearer $OPENAI_API_KEY"`
2. Problem statement is clear and specific
3. No network connectivity issues

**Solution**: Try simpler problem statements, check API key billing status

### Chat Issues  
**Problem**: Chat doesn't reference generated documents
**Check**:
1. Documents exist: Visit `/chat-admin` to verify system state
2. Browser supports Server-Sent Events
3. No ad blockers interfering

**Solution**: Generate documents first, try incognito mode

### Performance Issues
**Expected Performance**:
- Three-pass generation: 2-4 minutes  
- Chat first token: <2 seconds
- State operations: <1 second

**If Slower**:
1. Check OpenAI API status and response times
2. Verify internet connectivity
3. Monitor system resources (CPU/memory)

## Best Practices

### Problem Statement Guidelines
**Good Problem Statements**:
- "Implement user authentication with two-factor verification" ✅
- "Design a REST API for inventory management" ✅
- "Create a data pipeline for real-time analytics" ✅

**Poor Problem Statements**:
- "Make my app better" ❌ (too vague)
- "Fix everything" ❌ (no clear scope)
- "Do the thing we discussed" ❌ (no context)

### Chat Interaction Patterns
**Effective Questions**:
- Reference specific documents: "According to my SP document, how should I..."
- Ask for integration guidance: "How do the DS and SP components work together?"
- Seek implementation details: "What's the best way to implement the X solution?"

**Less Effective Questions**:
- Generic questions without document context
- Questions that ignore generated document insights
- Repetitive questions already answered in documents

### Document Review Process
1. **DS Review**: Verify data specifications are technically accurate
2. **SP Review**: Ensure procedures are actually executable  
3. **GD Review**: Ensure strategic guidance covers prerequisites/successors and context
4. **EC Review**: Validate that evaluation procedures and quality gates are actionable

## Advanced Tutorials

### Tutorial 6: API Integration (v2)
Generate documents programmatically via traversal:

```typescript
import fetch from 'node-fetch';

export async function generateDocs(problemTitle: string, problemStatement: string) {
  const response = await fetch('http://localhost:3001/api/pipeline/traverse', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      problem: { title: problemTitle, statement: problemStatement },
      options: { mode: 'foundation' }
    })
  });
  return await response.json();
}
```

### Tutorial 7: Custom Workflows (v2)
Create specialized workflows for your use cases:

**Requirements Analysis Workflow**:
1. Run foundation traversal to produce DS/SP/GD/EC
2. Export and review documents; refine problem statement as needed

**Technical Design Workflow**:
1. Use SP as implementation backbone with DS constraints
2. Follow GD for strategic considerations; validate via EC

## Getting Help

### Resources
- **[TROUBLESHOOTING.md](../TROUBLESHOOTING.md)** - Common issues and solutions
- **[CONTRIBUTING.md](../CONTRIBUTING.md)** - Development workflow
- **[docs/API_REFERENCE.md](API_REFERENCE.md)** - Complete API documentation

### Community
- **GitHub Issues**: Bug reports and feature requests
- **GitHub Discussions**: Usage questions and best practices

### Self-Diagnosis (v2)
```bash
# Basic API checks
curl -s -X POST http://localhost:3001/api/pipeline/traverse \
  -H 'Content-Type: application/json' \
  -d '{"problem":{"title":"T","statement":"Test"}}' | jq '.traversalId'
curl -s "http://localhost:3001/api/export/run?runId=<runId>" | jq
```

---

*Complete tutorial for systematic document generation with chirality‑app.*
