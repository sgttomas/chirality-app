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
| Can be nested | Packages may contain other Packages if desired |

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

## Anti-Patterns

| Anti-Pattern | Why It Fails |
|--------------|--------------|
| Agent invents structure without input | No grounding in tacit knowledge |
| User works without structure | Knowledge stays tacit, cannot be shared |
| Skipping confirmation gates | Errors propagate without correction |
| Resolving ambiguity silently | Assumptions become hidden defects |
| Structuring before scope alignment | Structure built on unstable foundation |
| Failing to surface contradictions | Inconsistencies become embedded defects |
| Proposing without explaining reasoning | User cannot evaluate or correct the proposal |
| Agent self-approves | Bypasses user validation |
