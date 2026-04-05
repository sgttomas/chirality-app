# CONTRACT — Invariant Catalog

This document is the authoritative catalog of binding invariants for the Chirality project execution system.

Invariants listed here are enforceable constraints that agents, tooling, and human processes must respect. Each invariant includes its enforcement point (where and how compliance is checked).

Invariant IDs (`K-*`) are **stable and never reused**. Retired invariants are moved to §3 with retirement rationale.

---

## 1. Invariant Catalog

### K-* Invariant Index

All K-* identifiers defined in this section are listed below with their definition locations. There are **21 stable invariants** across 10 subsections.

| K-* ID | Subsection | Topic |
|--------|------------|-------|
| K-HIER-1 | 1.1 | Hierarchy and Identity |
| K-ID-1 | 1.1 | Hierarchy and Identity |
| K-AUTH-1 | 1.2 | Authority and Approval |
| K-AUTH-2 | 1.2 | Authority and Approval |
| K-BIND-1 | 1.2 | Authority and Approval |
| K-SEAL-1 | 1.3 | Sealing and Context |
| K-GHOST-1 | 1.3 | Sealing and Context |
| K-DEP-1 | 1.4 | Dependencies |
| K-DEP-2 | 1.4 | Dependencies |
| K-STATUS-1 | 1.5 | Status and Lifecycle |
| K-STALE-1 | 1.6 | Staleness and Change Propagation |
| K-STALE-2 | 1.6 | Staleness and Change Propagation |
| K-VAL-1 | 1.6 | Staleness and Change Propagation |
| K-GATE-1 | 1.7 | Gates |
| K-MERGE-1 | 1.8 | Merge and Publication |
| K-PROV-1 | 1.9 | Provenance and Epistemic Integrity |
| K-INVENT-1 | 1.9 | Provenance and Epistemic Integrity |
| K-CONFLICT-1 | 1.9 | Provenance and Epistemic Integrity |
| K-CLAIM-1 | 1.9 | Provenance and Epistemic Integrity |
| K-WRITE-1 | 1.10 | Write Scope and Snapshots |
| K-SNAP-1 | 1.10 | Write Scope and Snapshots |

---

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
| **K-PROV-1** | Every non-trivial governed claim must cite evidence with a source path and best-effort section reference, or carry explicit `location TBD`. Dependency rows are a schema-specific instance of this rule and use **`EvidenceFile` + `SourceRef`** per `SPEC.md` §6.5. | Agent instruction constraints; DEPENDENCIES row validation; governance audits; human review |
| **K-INVENT-1** | Unknown values become **`TBD`**, not guessed. Agents must not invent scope items, dependency targets, parameter values, or engineering content. | All agent instruction invariants; human review |
| **K-CONFLICT-1** | Conflicts between sources must be **surfaced, not silently resolved**. Agents expose disagreements with pointers to the conflicting sources. | Agent instruction invariants (HELPS_HUMANS R7); human adjudication |
| **K-CLAIM-1** | Claims, conclusions, and characterizations must not **overstate what the available warrant supports**. Statements of necessity, sufficiency, universality, completeness, exclusivity, or direct regulatory conclusiveness may be used only when the cited evidence supports that strength; otherwise they must be framed as interpretation, implementation-specific design, or proposal. | Agent instruction constraints; governance audits (AUDIT_GOVERNANCE); human review |

### 1.10 Write Scope and Snapshots

| ID | Invariant | Enforcement |
|----|-----------|-------------|
| **K-WRITE-1** | Every agent has an **explicit write scope** declared in its header block. No agent writes outside its declared zone. | Agent Type table (WRITE_SCOPE property); human review of diffs |
| **K-SNAP-1** | Task agent outputs to tool roots are **immutable snapshots**. Pointer files (`_LATEST.md`) may be overwritten; snapshot folders must not. | Agent instruction constraints; SPEC.md Section 11 |

---

## 2. Enforcement Map Summary

| Enforcement Point | Invariants Checked |
|-------------------|-------------------|
| **Agent instructions** (design-time; constrains intent, not guaranteed behavior) | K-GHOST-1, K-WRITE-1, K-SNAP-1, K-PROV-1, K-INVENT-1, K-CONFLICT-1, K-CLAIM-1, K-DEP-1, K-DEP-2 |
| **ORCHESTRATOR** (runtime) | K-SEAL-1, K-GATE-1, K-HIER-1 |
| **Human review** (gate) | K-AUTH-1, K-AUTH-2, K-BIND-1, K-STALE-2, K-MERGE-1, K-VAL-1, K-STATUS-1 |
| **Future tooling** (automated) | K-STALE-1, K-VAL-1, K-MERGE-1, K-AUTH-2, K-DEP-2 |
| **PROJECT_DECOMP** (decomposition) | K-HIER-1, K-ID-1 |

---

## 3. Retired Invariants

No invariants have been retired.

---

EOF
