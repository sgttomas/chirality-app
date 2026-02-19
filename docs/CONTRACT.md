# CONTRACT — Invariant Catalog and Change Policy

This document is the authoritative catalog of binding invariants for the Chirality project execution system. It also defines the change policy for governance documents and structural changes.

Invariants listed here are enforceable constraints that agents, tooling, and human processes must respect. Each invariant includes its enforcement point (where and how compliance is checked).

---

## 1. Invariant Catalog

### 1.1 Hierarchy and Identity

| ID | Invariant | Enforcement |
|----|-----------|-------------|
| **K-HIER-1** | Projects are decomposed as **packages containing deliverables** (flat; no nesting; no phases layer). | PROJECT_DECOMP gates; PREPARATION folder creation; human review |
| **K-ID-1** | Deliverable IDs are **stable** and persist across path changes. Path is a physical projection of decomposition, not identity. | PROJECT_DECOMP (ID assignment); all agents (ID referencing) |

### 1.2 Authority and Approval

| ID | Invariant | Enforcement |
|----|-----------|-------------|
| **K-AUTH-1** | Only **humans** author binding approval records. No agent may claim to certify, approve, sign, seal, or issue work for reliance. | Agent instruction constraints; human review |
| **K-AUTH-2** | Approvals bind to a **specific git SHA**. Content change after approval voids the approval. | Human review; future tooling (SHA comparison) |
| **K-BIND-1** | Approvals are **always binding and only binding**. Non-binding guidance is allowed outside approval records. | Human process discipline |

### 1.3 Sealing and Context

| ID | Invariant | Enforcement |
|----|-----------|-------------|
| **K-SEAL-1** | No Type 2 agent execution before context is **sealed and gate-approved** by a human. | ORCHESTRATOR (seal check); human gate approval |
| **K-GHOST-1** | Type 2 agent context is limited to **folder contents + declared references**. No ghost inputs. | Agent instruction constraints (WRITE_SCOPE, _REFERENCES.md); human review of diffs |

### 1.4 Dependencies

| ID | Invariant | Enforcement |
|----|-----------|-------------|
| **K-DEP-1** | Deliverable-local `_DEPENDENCIES.md` and `Dependencies.csv` are **authoritative** for dependencies. There is no central dependency graph; aggregation is on-demand via `_Reconciliation/`. | DEPENDENCIES agent (local writes only); RECONCILIATION agent (read-only aggregation) |
| **K-DEP-2** | Dependency references to deliverables must **resolve to existing deliverable IDs**. Unresolvable targets use `TargetType=UNKNOWN`. | DEPENDENCIES agent (Function 2); validation checks |

### 1.5 Status and Lifecycle

| ID | Invariant | Enforcement |
|----|-----------|-------------|
| **K-STATUS-1** | `_STATUS.md` is the **canonical, human-readable lifecycle state file** for each deliverable. No other file determines deliverable state. | All agents (read _STATUS.md for state); transition rules in SPEC.md Section 3.3 |

### 1.6 Staleness and Change Propagation

| ID | Invariant | Enforcement |
|----|-----------|-------------|
| **K-STALE-1** | Upstream changes **propagate staleness** to all transitive dependent deliverables. | Future tooling (staleness calculation); human triage |
| **K-STALE-2** | Stale items must be **triaged by a human** before being considered current. Resolution modes: no impact (clear flag), needs rework, or needs review. | Human triage queue |
| **K-VAL-1** | A deliverable is **dirty** if any governed input has changed since its last approved SHA. | Future tooling (SHA comparison); human review |

### 1.7 Gates

| ID | Invariant | Enforcement |
|----|-----------|-------------|
| **K-GATE-1** | Gates are **dynamic per project instance**. Minimum required gates: seal transition + pipeline run approval. Additional gates are project-configurable. | ORCHESTRATOR (gate map); human configuration |

### 1.8 Merge and Publication

| ID | Invariant | Enforcement |
|----|-----------|-------------|
| **K-MERGE-1** | Merge to main allowed only when **branch HEAD == approved SHA** for the relevant run. | Human review; future CI check |

### 1.9 Provenance and Epistemic Integrity

| ID | Invariant | Enforcement |
|----|-----------|-------------|
| **K-PROV-1** | Every extracted dependency row must cite evidence: **`EvidenceFile` + `SourceRef`** (or explicit `location TBD`). | DEPENDENCIES agent (Function 5 quality checks); SPEC.md Section 6.5 |
| **K-INVENT-1** | Unknown values become **`TBD`**, not guessed. Agents must not invent scope items, dependency targets, parameter values, or engineering content. | All agent instruction invariants; human review |
| **K-CONFLICT-1** | Conflicts between sources must be **surfaced, not silently resolved**. Agents expose disagreements with pointers to the conflicting sources. | Agent instruction invariants (HELPS_HUMANS R7); human adjudication |

### 1.10 Write Scope and Snapshots

| ID | Invariant | Enforcement |
|----|-----------|-------------|
| **K-WRITE-1** | Every agent has an **explicit write scope** declared in its header block. No agent writes outside its declared zone. | Agent Type table (WRITE_SCOPE property); human review of diffs |
| **K-SNAP-1** | Task agent outputs to tool roots are **immutable snapshots**. Pointer files (`_LATEST.md`) may be overwritten; snapshot folders must not. | Agent instruction constraints; SPEC.md Section 11 |

---

## 2. Enforcement Map Summary

| Enforcement Point | Invariants Checked |
|-------------------|-------------------|
| **Agent instructions** (compile-time) | K-GHOST-1, K-WRITE-1, K-SNAP-1, K-PROV-1, K-INVENT-1, K-CONFLICT-1, K-DEP-1, K-DEP-2 |
| **ORCHESTRATOR** (runtime) | K-SEAL-1, K-GATE-1, K-HIER-1 |
| **Human review** (gate) | K-AUTH-1, K-AUTH-2, K-BIND-1, K-STALE-2, K-MERGE-1, K-VAL-1, K-STATUS-1 |
| **Future tooling** (automated) | K-STALE-1, K-VAL-1, K-MERGE-1, K-AUTH-2, K-DEP-2 |
| **PROJECT_DECOMP** (decomposition) | K-HIER-1, K-ID-1 |

---

## 3. Change Policy

### 3.1 Governance Document Changes

Changes to governance documents (`docs/DIRECTIVE.md`, `docs/TYPES.md`, `docs/CONTRACT.md`, `docs/SPEC.md`, `docs/PLAN.md`) require:

1. Branch creation
2. Pull request with clear description of changes and rationale
3. Human review and approval
4. Merge to main

### 3.2 Agent Instruction Changes

Any change to an `AGENT_*.md` file that alters **write scope, tool access, or primary outputs** requires:

1. Branch + PR + human review (same as governance docs)
2. Recorded release note describing the material change

Minor changes (clarifications, typo fixes, rationale updates) may be committed directly with a descriptive commit message.

### 3.3 Decomposition Changes

Changes to the project decomposition require:

1. PROJECT_DECOMP conversation with human confirmation gates
2. Folder tree reconciliation (PREPARATION updates affected folders)
3. Dependency refresh for affected deliverables (DEPENDENCIES agent)
4. Staleness recalculation for downstream dependents

### 3.4 Structural Changes

Changes that affect the execution root structure (adding/removing packages, deliverables, tool roots) require:

1. Human approval
2. PREPARATION agent execution for scaffolding
3. Git commit with descriptive message

---

## 4. Invariant Change Protocol

Adding, modifying, or retiring an invariant in this catalog requires:

1. Proposal with rationale (why the invariant needs to change)
2. Impact assessment (which agents, documents, and processes are affected)
3. Branch + PR + human review
4. Update to enforcement map if enforcement points change
5. Notification to affected agent instruction files (if they reference the invariant)

Invariant IDs (`K-*`) are never reused. Retired invariants are moved to an appendix (Section 5) with retirement rationale.

---

## 5. Retired Invariants

No invariants have been retired.

---

EOF
