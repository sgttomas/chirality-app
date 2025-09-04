# Chirality AI App Tutorial

Complete hands-on guide to generating structured documents and using RAG-enhanced chat for systematic problem-solving.

## Getting Started

### Prerequisites
- Node.js 18+
- OpenAI API key
- 15 minutes for complete tutorial

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
1. Navigate to http://localhost:3001/chirality-core
2. Enter a clear problem statement:
   ```
   Implement a user authentication system for a web application
   ```
3. Click "Update Problem Statement"

### Step 2: Generate Documents
1. Choose "🔄 Three-Pass with Matrix Integration" (recommended)
2. Watch the progress indicator as V1→V2→V3 refinement occurs
3. Generation takes 2-4 minutes for complete three-pass process

### Step 3: Explore Generated Documents
You'll receive four structured documents:

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

**X (Solution Template)**
```json
{
  "heading": "Authentication Flow Integration",
  "narrative": "Comprehensive user authentication implementing secure credential validation with session management",
  "precedents": ["DS:user_credentials", "SP:validate_user_credentials"],
  "context_notes": ["Must handle edge cases for account lockout"]
}
```

**M (Guidance)**
```json
{
  "statement": "Implement multi-factor authentication for enhanced security",
  "justification": "Password-only authentication insufficient for sensitive applications",
  "trace_back": ["X:auth_integration", "SP:credential_validation"],
  "residual_risk": ["Brute force attacks on weak passwords"]
}
```

### Step 4: Understand the Three-Pass Process
- **V1**: Initial generation with forward dependencies only
- **V2**: Cross-referential refinement where each document learns from others  
- **V3**: Final convergence with complete context integration

Notice how V2 documents reference concepts from other documents, and V3 achieves full coherence.

## Tutorial 2: RAG-Enhanced Chat

### Step 1: Start Chatting
1. After generating documents, navigate to http://localhost:3001
2. Your generated documents are automatically loaded as context
3. Ask questions that leverage your documents:

### Step 2: Context-Aware Conversations
Try these example questions:

**Technical Implementation**:
```
"What database schema should I use for the user_credentials data field?"
```

The AI response will reference your DS document and provide grounded recommendations.

**Procedural Guidance**:
```
"Walk me through implementing the validate_user_credentials procedure"
```

The AI will reference your SP document and provide step-by-step guidance.

**Solution Architecture**:
```
"How do all these authentication components fit together?"
```

The AI will synthesize insights from all your documents (DS/SP/X/M).

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

## Tutorial 3: Matrix Integration (Advanced)

### Step 1: Understand Matrix-Driven Generation
Matrix integration uses external semantic matrices as "seeds of thought":

- **C matrix** → DS documents (requirements → data specifications)
- **D matrix** → SP documents (objectives → procedures)  
- **X+E matrices** → X documents (verification + evaluation → solutions)
- **E matrix** → M documents (evaluation → guidance)

### Step 2: Using Framework Integration
With external framework runs:

```bash
# Example API call for matrix integration
curl -X POST http://localhost:3001/api/agent/run \
  -H "Content-Type: application/json" \
  -d '{"framework_run_id": "sample_happy_001", "enable_rag": true}'
```

### Step 3: Matrix-Enhanced Generation
When matrices are available:
1. Deterministic scaffolds are pre-generated from matrix content
2. AI enhances these scaffolds during V1 generation
3. V2 and V3 proceed with standard cross-referential refinement
4. Result combines structured matrix input with AI creativity

## Tutorial 4: System Administration

### Step 1: Monitor System Health
1. Visit http://localhost:3001/chat-admin for admin dashboard
2. Check system status:
   ```bash
   curl http://localhost:3001/api/healthz      # Basic health
   curl http://localhost:3001/api/readyz       # Dependencies
   curl http://localhost:3001/api/chat/debug   # Detailed status
   ```

### Step 2: State Management
```bash
# View current state
curl http://localhost:3001/api/core/state

# Clear state (reset everything)
curl -X DELETE http://localhost:3001/api/core/state

# Update problem statement via API
curl -X POST http://localhost:3001/api/core/state \
  -H "Content-Type: application/json" \
  -d '{"problem": {"statement": "New problem description"}}'
```

### Step 3: Export Documents
```bash
# Export with RBAC (requires approver role when enabled)
curl -H "x-role: approver" \
  http://localhost:3001/api/agent/export/abc123 \
  --output documents.zip
```

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
3. **X Review**: Check that solution integrates DS and SP coherently
4. **M Review**: Validate that guidance provides strategic value

## Advanced Tutorials

### Tutorial 6: API Integration
Learn to integrate Chirality AI App into your workflow:

```typescript
// Example: Automated documentation generation
import fetch from 'node-fetch';

async function generateProjectDocs(problemStatement: string) {
  // Set problem
  await fetch('http://localhost:3001/api/core/state', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ problem: { statement: problemStatement } })
  });
  
  // Generate documents
  const response = await fetch('http://localhost:3001/api/core/orchestrate', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({})
  });
  
  return await response.json();
}
```

### Tutorial 7: Custom Workflows
Create specialized workflows for your use cases:

**Requirements Analysis Workflow**:
1. Generate DS for data requirements
2. Generate SP for validation procedures  
3. Use chat to explore edge cases
4. Iterate with refined problem statements

**Technical Design Workflow**:
1. Generate complete document set
2. Use X document as architecture foundation
3. Use M document for risk assessment
4. Chat for implementation details

## Getting Help

### Resources
- **[TROUBLESHOOTING.md](../TROUBLESHOOTING.md)** - Common issues and solutions
- **[CONTRIBUTING.md](../CONTRIBUTING.md)** - Development workflow
- **[docs/API_REFERENCE.md](API_REFERENCE.md)** - Complete API documentation

### Community
- **GitHub Issues**: Bug reports and feature requests
- **GitHub Discussions**: Usage questions and best practices

### Self-Diagnosis
```bash
# Health check sequence
curl http://localhost:3001/api/healthz
curl http://localhost:3001/api/readyz  
curl http://localhost:3001/api/chat/debug
curl http://localhost:3001/api/core/state
```

---

*Complete tutorial for systematic document generation and RAG-enhanced problem solving with Chirality AI App.*