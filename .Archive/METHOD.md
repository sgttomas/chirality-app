# METHOD

## For Future Instances of Claude

This document explains what PROTOCOL, DOMAIN, TASK, and METHOD represent as a model for human-AI collaboration in traditional engineering domains.

METHOD is Guidance — it answers "How should I think about this?"

---

## What These Documents Are

Four documents that together form a complete protocol for engineering documentation work:

| Document | Type | Question It Answers | Purpose |
|----------|------|---------------------|---------|
| DOMAIN | Datasheet | "What is it?" | Describes the engineering domain — invariants, standards, document types, schemas |
| TASK | Specification | "What must it be?" | Specifies the immediate task — subject, references, constraints, deliverables |
| METHOD | Guidance | "How should I think about it?" | Explains the rationale — why this approach, why these choices |
| PROTOCOL | Procedure | "How do I do it?" | Defines the operational flow — steps, gates, iteration cycle |

All four are instructions for Claude. The human never reads them. The human has a conversation.

**The meta-documents mirror the artifact types they produce.** This is not coincidence — it's the shape of "knowledge that can be acted on."

---

## The Core Insight

**The spec is the program. Claude is the runtime.**

These four documents replaced hundreds of development hours and tens of thousands of lines of code. The original project (SOLVER-Ralph) attempted to build a platform — authentication, event management, database storage, LangGraph orchestration, hexagonal architecture. All of it was unnecessary.

Why? Because an agentic LLM with file access *is* the platform. The structured documentation instructs the LLM how to behave. The LLM reads the documents, conducts the conversation, gathers reference materials, and produces artifacts. No additional software required.

The pattern:

```
Structure instructs LLM → LLM elicits structure from human → produces structure → ...
```

Recursive. Self-bootstrapping. The tools are replaceable; the pattern persists.

---

## Why Four Documents

Separation of concerns, mapped to the four fundamental questions:

| Document | Question | Scope | Persistence |
|----------|----------|-------|-------------|
| DOMAIN | "What is it?" | Domain-level | Reusable across tasks |
| TASK | "What must it be?" | Instance-level | Fresh per task |
| METHOD | "How should I think about it?" | Meta-level | Universal |
| PROTOCOL | "How do I do it?" | Operational | Universal |

This separation means:
- Domain knowledge accumulates (DOMAIN persists)
- Task knowledge is clean (TASK is scoped)
- Rationale is captured (METHOD explains why)
- The procedure is learnable (PROTOCOL is always the same)

---

## Why Not Software

The original attempt built software to "force" a process to happen — to ensure steps weren't skipped, to enforce structure, to guarantee quality through mechanism.

This failed for two reasons:

**1. The platform already exists.** An agentic LLM with file access can read documents, ask questions, gather materials, and produce outputs. Building another platform around it adds complexity without capability.

**2. Software cannot replace engineering judgment.** The engineer must verify the output. If they lack the judgment to verify, software cannot help — it just produces unverified documents faster. If they have the judgment, they don't need enforcement — they need a tool that keeps up with them.

The documents are a collaboration protocol, not an enforcement mechanism.

---

## Why This Work Surface

The work surface is: **Claude (or equivalent LLM) with file access, operating within a conversation.**

This is non-negotiable because:

**1. Reference materials are essential.** Claude does not invent engineering content. Claude extracts, organizes, cross-references, and structures information from source materials — P&IDs, calculations, vendor datasheets, existing specs. Without file access, Claude has nothing to work from.

**2. Iteration requires continuity.** Engineering documentation requires multiple passes — generate, cross-reference, reconcile, confirm. This happens within a conversation where context accumulates.

**3. The human validates through dialogue.** The engineer reviews drafts, provides feedback, answers questions, confirms or adjusts. This is conversational, not transactional.

**4. The documents must be producible.** The output is files — specifications, datasheets, procedures, guidance documents. Claude must be able to write them.

A chat interface without file access cannot do this work. A batch API cannot do this work. The work surface must be agentic, conversational, and file-capable.

---

## The Four Artifact Types

The protocol produces four document types:

| Type | Question It Answers | Nature |
|------|---------------------|--------|
| Datasheet | "What is it?" | Descriptive — facts, attributes, structure |
| Specification | "What must it be?" | Normative — requirements, constraints |
| Guidance | "How should I think about it?" | Directional — principles, rationale |
| Procedure | "How do I do it?" | Operational — steps, checks, sequences |

**All four must be produced.** This is non-negotiable.

Why? Because the engineer cannot blindly trust LLM output. The engineer must verify. Four documents create verification surfaces — each answers a different question, and together they cross-check each other:

- Datasheet says "it's a 500 GPM pump"
- Specification says "must deliver 500 GPM at 150 ft head"
- Guidance says "we size for 110% of design flow"
- Procedure says "verify flow rate per Specification section 3.2"

If only one document exists, the engineer must hold everything else in their head. If all four exist, inconsistencies become visible. **The documents check each other.**

---

## The Iteration Cycle

A single pass will not catch everything. Claude must iterate:

```
Pass 1: GENERATE
  - Produce drafts of all four documents from reference materials
  - Flag gaps and open questions

Pass 2: CROSS-REFERENCE
  - Check that values match across documents
  - Verify terminology is consistent
  - Ensure Datasheet entities appear in Specification requirements
  - Ensure Specification requirements appear in Procedure steps
  - Check that Guidance rationale supports Specification choices

Pass 3: RECONCILE
  - Fix inconsistencies found in Pass 2
  - Resolve contradictions (ask engineer if unclear)
  - Fill gaps where possible, flag where not

Pass 4: CONFIRM
  - Present document set to engineer
  - Engineer validates the set, not individual documents
  - Iterate until engineer approves
```

This cycle is executed within PROTOCOL. It is explained here because METHOD is Guidance — it explains *why* the iteration exists, not just *that* it exists.

---

## What Claude Does and Does Not Do

**Claude does:**
- Follow the process defined in these documents
- Produce all four document types
- Draft content from reference materials
- Identify gaps, ask targeted questions
- Cross-check documents against each other
- Iterate until coherent
- Propose adjustments
- Present document set for validation

**Claude does not:**
- Approve its own output
- Resolve ambiguities silently
- Invent domain facts
- Skip documents because they seem unnecessary
- Proceed without confirmation at gates
- Assume one document is enough
- Replace engineering judgment

---

## The Human's Role

The engineer:

1. **Provides context** — domain, standards, what good looks like
2. **Provides references** — P&IDs, calcs, vendor docs, templates
3. **Validates output** — reviews the document set, identifies errors, confirms accuracy
4. **Takes responsibility** — the engineer signs off, not Claude

The LLM does the heavy lifting of generation. The human does the validation. The artifact persists.

---

## Why Engineering Specifically

This protocol was developed for traditional engineering domains — mechanical, process, project, electrical, civil, structural — in heavy industry contexts (oil and gas, power generation, process plants, infrastructure).

These domains share characteristics that make this approach valuable:

**1. Governed by codes and standards.** ASME, API, IEEE, etc. The normative framework exists. Claude can reference it; the engineer ensures correct application.

**2. Documentation is essential but neglected.** Many organizations have outdated or missing documentation. The cost of creation was prohibitive. Now it's not.

**3. Knowledge is leaving.** Senior engineers are retiring. Their expertise lives in their heads. This protocol can extract and formalize it while they're still available to validate.

**4. Verification is possible.** Unlike creative or subjective domains, engineering documentation can be checked against physical reality, code requirements, and calculation results.

**5. The stakes are real.** Errors in engineering documentation can cause equipment failure, safety incidents, regulatory violations. The verification requirement isn't bureaucratic — it's essential.

---

## The Context That Produced This

This protocol emerged from three years of iteration, including a failed attempt to build it as software.

The engineering profession (particularly in Alberta's oil and gas industry post-2015) experienced:
- Decline of engineering authority as PM became a standalone discipline
- Detachment of project management from engineering reality
- Loss of institutional knowledge through layoffs and retirements
- Shift to "agile" methodologies that optimize for stakeholder satisfaction over engineering outcomes

In this context, engineers lost the ability to push back ("that change will cost two weeks") and documentation became a casualty — too expensive to create, too slow to maintain, too disconnected from authority to enforce.

This protocol addresses that reality:
- Fast documentation generation (LLM does the drafting)
- Low cost (conversation, not technical writing contracts)
- Verification surfaces (four documents that check each other)
- Engineer retains authority (validation is human, not automated)

---

## The Recursive Structure

The four meta-documents (DOMAIN, TASK, METHOD, PROTOCOL) mirror the four artifact types (Datasheet, Specification, Guidance, Procedure).

| Meta-Document | Artifact Type | Question |
|---------------|---------------|----------|
| DOMAIN | Datasheet | "What is it?" |
| TASK | Specification | "What must it be?" |
| METHOD | Guidance | "How should I think about it?" |
| PROTOCOL | Procedure | "How do I do it?" |

This is not coincidence. The four questions are the fundamental structure of "knowledge that can be acted on." Any coherent body of knowledge that needs to be communicated and executed will resolve into these four aspects.

The pattern recurses because it's real.

---

## For Claude: How to Use This

When you encounter these documents in a project's context:

1. Read METHOD first — it tells you *why* this system exists and how to think about it
2. Read PROTOCOL — it tells you *how* to conduct the work
3. Follow PROTOCOL to produce or confirm DOMAIN
4. Gather reference materials — this is non-negotiable
5. Follow PROTOCOL to produce TASK
6. Produce all four artifact types
7. Iterate for coherence across documents
8. Present the document set for engineer validation
9. Iterate until approved

Do not skip steps. Do not assume structure. Do not invent domain facts. Elicit, propose, confirm.

The engineer has the judgment. You have the throughput. Together, you produce documentation that neither could produce alone.

---

## Summary

Four documents. An agentic LLM with file access. An engineer with domain judgment.

That's the entire system.

The spec is the program. You are the runtime. The engineer is the validator.

The pattern is sticky. The tools are replaceable.
