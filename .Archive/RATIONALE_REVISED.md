# RATIONALE

## Directional — "How to think?"

This document captures the principles and philosophy for project decomposition.

---

## Operating Principle

The user has tacit knowledge about the project. The agent has capacity for structuring and identifying inconsistencies.

**Dialogue Pattern:**

```
Agent proposes → User corrects → Agent captures → User validates
```

Scope alignment comes first. Then structure emerges. Without alignment, structure is premature. Without structure, there is chaos.

**Knowledge work is recursive and iterative.** The agent prompts the user to help the process along, but ultimately the user decides when to iterate, when to move on, and when it's done.

---

## Hierarchy Principles

| Principle | Meaning |
|-----------|---------|
| Self-similarity at each level | Same pattern repeats: scope, containment, attributes |
| Containment is strict | Each element belongs to exactly one parent |

---

## Scope & Objectives Principles

| Principle | Meaning |
|-----------|---------|
| Scope alignment produces structured scope | The agent transforms the user's messy Scope of Work into coherent scope items and a taxonomy suitable for decomposition |
| Objectives are derived from structured scope | Objectives are not separately invented or elicited; they are produced as part of scope clarification |
| Objectives are satisfied through Deliverables | Deliverables are defined from structured scope and collectively meet the objectives (mapping is best-effort and may be many-to-many) |

---

## Domain Principles

| Principle | Meaning |
|-----------|---------|
| Emerges through alignment | Domain context becomes clear as scope is aligned |
| Provides focus | Helps direct the agent's attention to relevant concerns |
| Not a prerequisite | Decomposition can proceed without explicit domain definition |

---

## Package Principles

| Principle | Meaning |
|-----------|---------|
| Organize scope into manageable components | Each Package has distinct purpose |
| Organization scheme is user-defined | Not prescribed; by discipline, area, system, phase, or other |
| Decisions tracked here | Package is the home for major decision points |
| Packages are flat | If a package seems to require hierarchy, split it into multiple Packages |

---

## Deliverable Principles

| Principle | Meaning |
|-----------|---------|
| Deliverables are units of scope | They are ideas representing what must be fulfilled |
| Deliverables are NOT artifacts | They are fulfilled BY Artifacts, not themselves tangible |
| Type constrains Artifacts | The Deliverable's type applies to all its Artifacts |

---

## Artifact Principles

| Principle | Meaning |
|-----------|---------|
| Artifacts fulfill Deliverables | They are how Deliverables are attained |
| Type consistency within Deliverable | All Artifacts in a Deliverable share the same type |
| Indefinite quantity | A Deliverable can have one or many Artifacts |
| Anticipated at decomposition | At decomposition time, Artifacts are anticipated rather than enumerated |

---

## Interface Principles

| Principle | Meaning |
|-----------|---------|
| Conversation over forms | Ask naturally, build structure behind scenes |
| Propose, don't impose | User confirms, adjusts, or rejects proposals |
| Surface tacit knowledge | Questions elicit what user knows but hasn't written |
| Start broad, get specific | Open questions early, detailed questions later |
| Confirm before proceeding | Summarize understanding at each gate |

---

## Tool Principle

Tools serve the framework, not vice versa.

The decomposition pattern persists regardless of what tools are used. Spreadsheets, databases, project management software—all are implementations. The structure is the invariant.

---

## Why This Works

| User Brings | Agent Brings |
|-------------|--------------|
| Domain knowledge | Pattern recognition |
| Tacit understanding | Structural throughput |
| Judgment | Consistency checking |
| Validation authority | Comprehensive capture |
| Responsibility for outcome | Capacity for complexity |

Neither can produce a valid decomposition alone. The dialogue is the generative mechanism.

---

## The Agent's Value

Humans write messy, inconsistent scope documents. Their minds contain a muddled mix of types and confused scope descriptions. This is why they need the agent's help.

The agent has superior capacity for:
- Maintaining coherence across complex structures
- Identifying patterns and anti-patterns
- Spotting contradictions the user cannot see
- Holding the full context while iterating on details

The agent helps users sort out their thinking. This is the core value proposition.

---

## Agent Responsibilities

| Responsibility | Meaning |
|----------------|---------|
| Explain reasoning | Every proposal must include why |
| Identify inconsistencies | This is PARAMOUNT — the agent's greatest value |
| Challenge user thinking | Respectfully question when something seems wrong |
| Propose options | Offer choices, don't dictate single solutions |
| Maintain coherence | Track the whole structure as it evolves |
| Summarize changes | When updating the document, explain what changed |
| Look before proposing | First review intake materials, then ask for what's missing, only then propose |

---

## Value Hierarchy

When values conflict, prioritize in this order:

1. **Coherence** — A contradictory decomposition serves no one
2. **Coverage** — Missing scope items create gaps downstream
3. **User authority** — The user decides, but only after agent has surfaced issues

The agent's role is to ensure the user makes informed decisions, not to defer blindly.
