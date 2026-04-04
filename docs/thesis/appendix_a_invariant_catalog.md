# Appendix A — Invariant Catalog

This appendix consolidates the three layers of formally stated invariants that govern the Chirality agent instruction architecture. The invariants are organized by their layer of origin and scope of application: workflow design requirements (R1–R9) apply universally to all agents and all workflow designs; decomposition invariants (I1–I10) govern all decomposition agents; and system-wide invariants (K-*) are enforced across the full agent suite. All invariants are reproduced faithfully from their authoritative source documents.

---

## A.1 Workflow Design Requirements (R1–R9)

Defined in `AGENT_HELPS_HUMANS.md`. Apply to all agents and all workflow designs. A workflow design is considered compliant when all nine requirements are satisfied.

| ID | Requirement | Rule |
|----|-------------|------|
| R1 | Human decision rights are explicit | Human-owned decisions are enumerated and preserved. |
| R2 | Task agents are straight-through | Task agents run without requiring mid-run human decisions. |
| R3 | Write quarantine is enforced | Every agent has an explicit write scope. Tool roots are isolated from source truth. |
| R4 | Snapshots are immutable | Each run produces a new snapshot folder. Pointer files may be overwritten; snapshots may not. |
| R5 | Provenance is mandatory | Aggregated/extracted data includes `SourcePath` and best-effort `SectionRef`. |
| R6 | No invention behavior is defined | Missing data becomes `TBD` with assumptions captured. |
| R7 | Conflicts/duplicates are surfaced | The system does not hide or silently resolve discrepancies unless explicitly directed. |
| R8 | Brief-driven execution exists | Pipelines have a defined brief format (INIT-TASK-style) and deterministic outputs. |
| R9 | Publication is hygienic | Version control publishing is reviewable and non-destructive by default. |

---

## A.2 Decomposition Invariants (I1–I10)

Defined in `AGENT_DECOMP_BASE.md`. Apply to all decomposition agents (PROJECT_DECOMP, SOFTWARE_DECOMP, DOMAIN_DECOMP). Verified by AUDIT_DECOMP. These invariants MUST hold across all conforming decomposition agents, regardless of domain.

| ID | Invariant | Rule |
|----|-----------|------|
| I1 | Human-validated decomposition | The structured outline and decomposition MUST be confirmed by the human at defined gates. No gate may be skipped. |
| I2 | No invention | Do not create atomic units, objectives, partitions, production units, or artifacts beyond what the source material and user intent support. If unknown, mark `TBD` and surface as an open issue. |
| I3 | Partitions are flat | Do not create nested partitions. If more granularity is needed, propose additional partitions at the same level. |
| I4 | No overlap / no gaps at the partition level | Every IN-scope atomic unit MUST be assigned to exactly one partition. Forced decision if ambiguous; human resolves at gates. |
| I5 | Stable identifiers | Once assigned, IDs MUST remain stable across revisions unless the human explicitly requests renumbering. |
| I6 | Deterministic production-unit ID ↔ partition ID coupling | The production unit ID MUST be mechanically derived from its parent partition ID. The coupling format is domain-specific (defined by the conforming agent) but the coupling itself is invariant. |
| I7 | Objective mapping is best-effort | Objectives are derived from the source material. Unmapped objectives MUST be surfaced as open issues. |
| I8 | Traceable rationale | Non-trivial assignment decisions MUST be recorded as explicit decisions in the decomposition output. |
| I9 | Ledger + telemetry | Every decomposition MUST include a machine-checkable ledger and a Coverage & Telemetry summary. These make coverage provable and quality comparable across revisions. |
| I10 | Vocabulary discipline | Every decomposition MUST include a Vocabulary Map. Canonical terms are used consistently; synonyms are mapped; semantic drift is prevented. |

---

## A.3 System-Wide Invariants (K-*)

Defined in `CONTRACT.md`. Enforced across the full agent suite. Invariant IDs are stable and never reused; retired invariants are relocated to the retired section of CONTRACT.md with retirement rationale.

| ID | Invariant | Enforcement |
|----|-----------|-------------|
| **K-HIER-1** | Projects are decomposed as **packages containing deliverables** (flat; no nesting; no phases layer). | PROJECT_DECOMP gates; PREPARATION folder creation; human review |
| **K-ID-1** | Deliverable IDs are **stable** and persist across path changes. Path is a physical projection of decomposition, not identity. | PROJECT_DECOMP (ID assignment); all agents (ID referencing) |
| **K-AUTH-1** | Only **humans** author binding approval records. No agent may claim to certify, approve, sign, seal, or issue work for reliance. | Agent instruction constraints; human review |
| **K-AUTH-2** | Approvals bind to a **specific git SHA**. Content change after approval voids the approval. | Human review; future tooling (SHA comparison) |
| **K-BIND-1** | Approvals are **always binding and only binding**. Non-binding guidance is allowed outside approval records. | Human process discipline |
| **K-SEAL-1** | No Type 2 agent execution before context is **sealed and gate-approved** by a human. | ORCHESTRATOR (seal check); human gate approval |
| **K-GHOST-1** | Type 2 agent context is limited to **folder contents + declared references**. No ghost inputs. | Agent instruction constraints (WRITE_SCOPE, _REFERENCES.md); human review of diffs |
| **K-DEP-1** | Deliverable-local `_DEPENDENCIES.md` and `Dependencies.csv` are **authoritative** for dependencies. There is no central dependency graph; aggregation is on-demand via `_Reconciliation/`. | DEPENDENCIES agent (local writes only); RECONCILIATION agent (read-only aggregation) |
| **K-DEP-2** | Dependency references to deliverables must **resolve to existing deliverable IDs**. Unresolvable targets use `TargetType=UNKNOWN`. | DEPENDENCIES agent (Function 2); validation checks |
| **K-STATUS-1** | `_STATUS.md` is the **canonical, human-readable lifecycle state file** for each deliverable. No other file determines deliverable state. | All agents (read _STATUS.md for state); transition rules in SPEC.md Section 3.3 |
| **K-STALE-1** | Upstream changes **propagate staleness** to all transitive dependent deliverables. | Future tooling (staleness calculation); human triage |
| **K-STALE-2** | Stale items must be **triaged by a human** before being considered current. Resolution modes: no impact (clear flag), needs rework, or needs review. | Human triage queue |
| **K-VAL-1** | A deliverable is **dirty** if any governed input has changed since its last approved SHA. | Future tooling (SHA comparison); human review |
| **K-GATE-1** | Gates are **dynamic per project instance**. Minimum required gates: seal transition + pipeline run approval. Additional gates are project-configurable. | ORCHESTRATOR (gate map); human configuration |
| **K-MERGE-1** | Merge to main allowed only when **branch HEAD == approved SHA** for the relevant run. | Human review; future CI check |
| **K-PROV-1** | Every extracted dependency row must cite evidence: **`EvidenceFile` + `SourceRef`** (or explicit `location TBD`). | DEPENDENCIES agent (Function 5 quality checks); SPEC.md Section 6.5 |
| **K-INVENT-1** | Unknown values become **`TBD`**, not guessed. Agents must not invent scope items, dependency targets, parameter values, or engineering content. | All agent instruction invariants; human review |
| **K-CONFLICT-1** | Conflicts between sources must be **surfaced, not silently resolved**. Agents expose disagreements with pointers to the conflicting sources. | Agent instruction invariants (HELPS_HUMANS R7); human adjudication |
| **K-WRITE-1** | Every agent has an **explicit write scope** declared in its header block. No agent writes outside its declared zone. | Agent Type table (WRITE_SCOPE property); human review of diffs |
| **K-SNAP-1** | Task agent outputs to tool roots are **immutable snapshots**. Pointer files (`_LATEST.md`) may be overwritten; snapshot folders must not. | Agent instruction constraints; SPEC.md Section 11 |

### Enforcement Map Summary

The following table is reproduced from CONTRACT.md §2 and maps each enforcement point to the invariants it is responsible for checking.

| Enforcement Point | Invariants Checked |
|-------------------|-------------------|
| **Agent instructions** (design-time; constrains intent, not guaranteed behavior) | K-GHOST-1, K-WRITE-1, K-SNAP-1, K-PROV-1, K-INVENT-1, K-CONFLICT-1, K-DEP-1, K-DEP-2 |
| **ORCHESTRATOR** (runtime) | K-SEAL-1, K-GATE-1, K-HIER-1 |
| **Human review** (gate) | K-AUTH-1, K-AUTH-2, K-BIND-1, K-STALE-2, K-MERGE-1, K-VAL-1, K-STATUS-1 |
| **Future tooling** (automated) | K-STALE-1, K-VAL-1, K-MERGE-1, K-AUTH-2, K-DEP-2 |
| **PROJECT_DECOMP** (decomposition) | K-HIER-1, K-ID-1 |
