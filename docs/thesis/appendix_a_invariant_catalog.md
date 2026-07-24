# Appendix A — Invariant Catalog

This appendix consolidates the three layers of formally stated invariants that govern the Chirality agent instruction architecture. The invariants are organized by their layer of origin and scope of application: workflow design requirements (R1–R17) apply universally to workflow-component designs; decomposition invariants (I1–I10) govern decomposition; and system-wide invariants (K-*) are enforced across the full agent suite.

The R-series is reproduced from the candidate
`docs/WORKFLOW_COMPONENT_STANDARD.md`; the I-series is reproduced from the
candidate `docs/DECOMPOSITION_STANDARD.md`. They remain candidate text pending
explicit owner acceptance. The ratified K-* catalog in `docs/CONTRACT.md`
governs on divergence.

---

## A.1 Workflow Design Requirements (R1–R17)

Defined in the ratified workflow-component standard. Apply to workflow
component designs together with the ratified K-* invariants.

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
| R10 | Skill tool policy is explicit | Every skill declares its tool policy — preferred, optional, and disallowed tools, and the conditions for falling back from tool execution to direct LLM reasoning. When present, `allowed-tools` in skill frontmatter is authoritative. |
| R11 | Tool contract is explicit | Every deterministic tool declares its input/output contract, scope boundary, and idempotence posture. Tools fail fast with explicit exit codes and never write outside their declared scope. |
| R12 | Skill/tool boundary is preserved | Skills identify tool needs; HELPS_HUMANS implements deterministic helpers; HELPS_HUMANS integrates the result. Skills do not embed inline deterministic logic; tools do not carry method-level guidance. |
| R13 | Claim strength is calibrated | Governed claims do not exceed their warrant under K-CLAIM-1. |
| R14 | Multi-phase integration rules are explicit | Derivative, snapshot, handoff, closure, sequencing, and cycle rules are implemented where applicable. |
| R15 | Registry lifecycle is explicit | Live membership, compatibility, deprecation, and retirement are mechanically visible. |
| R16 | Active-checkout containment is enforced | Task writes remain inside the active checkout under K-WRITE-2. |
| R17 | Design evidence is proportional and complete | Applicable authority, execution, QA, handoff, and retirement concerns are covered without unnecessary structure. |

---

## A.2 Decomposition Invariants (I1–I10)

Defined in `docs/DECOMPOSITION_STANDARD.md`. Apply to all decomposition agents (PROJECT_DECOMP, SOFTWARE_DECOMP, DOMAIN_DECOMP). Verified by AUDIT_DECOMP. These invariants MUST hold across all conforming decomposition agents, regardless of domain.

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

Defined in `docs/CONTRACT.md` (reproduced here as of 2026-07-02; 27 invariants). Enforced across the full agent suite. Invariant IDs are stable and never reused; retired invariants are relocated to the retired section of CONTRACT.md with retirement rationale (as of this reproduction, none have been retired).

### A.3.1 Hierarchy and Identity (CONTRACT §1.1)

| ID | Invariant | Enforcement |
|----|-----------|-------------|
| **K-HIER-1** | Projects are decomposed as **packages containing deliverables** (flat; no nesting; no phases layer). | PROJECT_DECOMP gates; PREPARATION folder creation; human review |
| **K-ID-1** | Deliverable IDs are **stable** and persist across path changes. Path is a physical projection of decomposition, not identity. | PROJECT_DECOMP (ID assignment); all agents (ID referencing) |

### A.3.2 Authority and Approval (CONTRACT §1.2)

| ID | Invariant | Enforcement |
|----|-----------|-------------|
| **K-AUTH-1** | Only **humans** author binding approval records. No agent may claim to certify, approve, sign, seal, or issue work for reliance. | Agent instruction constraints; human review |
| **K-AUTH-2** | Approvals bind to a **specific git SHA**. Content change after approval voids the approval. | Human review; future tooling (SHA comparison) |
| **K-BIND-1** | Approvals are **always binding and only binding**. Non-binding guidance is allowed outside approval records. | Human process discipline |

### A.3.3 Sealing and Context (CONTRACT §1.3)

| ID | Invariant | Enforcement |
|----|-----------|-------------|
| **K-SEAL-1** | No Agent 2 execution before context is sealed, the run is approved at the applicable human gate, and the launch cites that approval record. Runtime presence checks do not manufacture the human act. | Human approval record; ManagedDelegationService structural checks |
| **K-GHOST-1** | Agent 2 context is limited to declared files/references and sealed brief content. No ghost inputs. | Managed declared context; agent instruction constraints; human review |

### A.3.4 Dependencies (CONTRACT §1.4)

| ID | Invariant | Enforcement |
|----|-----------|-------------|
| **K-DEP-1** | Deliverable-local `_DEPENDENCIES.md` and `Dependencies.csv` are **authoritative** for dependencies. There is no central dependency graph; generic read-only aggregation is on-demand via `_Evaluation/`; a calibrated corpus-concordance run may also inventory dependencies under `_Reconciliation/DeliverableConcordance/`. | TASK+dependency-extract (local writes only); EVALUATION (generic audit); RECONCILIATION (activated corpus concordance) |
| **K-DEP-2** | Dependency references to deliverables must **resolve to existing deliverable IDs**. Unresolvable targets use `TargetType=UNKNOWN`. | TASK+dependency-extract (Function 2); validation checks |

### A.3.5 Status and Lifecycle (CONTRACT §1.5)

| ID | Invariant | Enforcement |
|----|-----------|-------------|
| **K-STATUS-1** | `_STATUS.md` is the **canonical, human-readable lifecycle state file** for each deliverable. No other file determines deliverable state. | All agents (read _STATUS.md for state); transition rules in SPEC.md Section 3.3 |

### A.3.6 Staleness and Change Propagation (CONTRACT §1.6)

| ID | Invariant | Enforcement |
|----|-----------|-------------|
| **K-STALE-1** | Upstream changes **propagate staleness** to all transitive dependent deliverables. | Future tooling (staleness calculation); human triage |
| **K-STALE-2** | Stale items must be **triaged by a human** before being considered current. Resolution modes: no impact (clear flag), needs rework, or needs review. | Human triage queue |
| **K-VAL-1** | A deliverable is **dirty** if any governed input has changed since its last approved SHA. | Future tooling (SHA comparison); human review |

### A.3.7 Gates (CONTRACT §1.7)

| ID | Invariant | Enforcement |
|----|-----------|-------------|
| **K-GATE-1** | Gates are **dynamic per project instance**. Minimum required gates: seal transition + pipeline run approval. Additional gates are project-configurable. | ORCHESTRATOR (gate map); human configuration |

*Note (per CONTRACT §1.7):* D-GOV-02, ruled 2026-07-01, derives from K-GATE-1 that no machine BLOCK on the CHECKING→ISSUED judgment may be non-overridable — BLOCKs apply to objective preconditions and hygiene only, and BLOCK override is human-only and recorded.

### A.3.8 Merge and Publication (CONTRACT §1.8)

| ID | Invariant | Enforcement |
|----|-----------|-------------|
| **K-MERGE-1** | Merge to main allowed only when **branch HEAD == approved SHA** for the relevant run. | Human review; future CI check |

### A.3.9 Provenance and Epistemic Integrity (CONTRACT §1.9)

| ID | Invariant | Enforcement |
|----|-----------|-------------|
| **K-PROV-1** | Every non-trivial governed claim must cite evidence with a source path and best-effort section reference, or carry explicit `location TBD`. Dependency rows are a schema-specific instance of this rule and use **`EvidenceFile` + `SourceRef`** per `SPEC.md` §6.5. | Agent instruction constraints; TASK+dependency-extract row validation; governance audits; human review |
| **K-INVENT-1** | Unknown values become **`TBD`**, not guessed. Agents must not invent scope items, dependency targets, parameter values, or engineering content. | All agent instruction invariants; human review |
| **K-CONFLICT-1** | Conflicts between sources must be **surfaced, not silently resolved**. Agents expose disagreements with pointers to the conflicting sources. | Agent instruction invariants (HELPS_HUMANS R7); human adjudication |
| **K-CLAIM-1** | Claims, conclusions, and characterizations must not **overstate what the available warrant supports**. Statements of necessity, sufficiency, universality, completeness, exclusivity, or direct regulatory conclusiveness may be used only when the cited evidence supports that strength; otherwise they must be framed as interpretation, implementation-specific design, or proposal. | Agent instruction constraints; governance audits (AUDIT_GOVERNANCE); human review |

### A.3.10 Write Scope and Snapshots (CONTRACT §1.10)

| ID | Invariant | Enforcement |
|----|-----------|-------------|
| **K-WRITE-1** | Every agent has an **explicit write scope** declared in its header block. No agent writes outside its declared zone. | Agent Type table (WRITE_SCOPE property); human review of diffs |
| **K-WRITE-2** | Agent writes must be **path-contained within the active checkout**. Every `ScopePath` and `AllowedWriteTarget` must normalize to an absolute path that resolves under `git rev-parse --show-toplevel` (`REPO_ROOT`); a target resolving outside it — including via symlink or `..` traversal — is rejected (`SCOPE_OUTSIDE_WORKTREE`) and the task stops. This confines a task's effects to its working root and makes per-working-root and git-worktree isolation safe. | TASK shell (ScopePath normalization, `SPEC.md` §0.2.3); tool path policy; human review of diffs |
| **K-SNAP-1** | Task agent outputs to tool roots are **immutable snapshots**. Pointer files (`_LATEST.md`) may be overwritten; snapshot folders must not. | Agent instruction constraints; SPEC.md Section 11 |

### A.3.11 Agent Index and Governance Surface (CONTRACT §1.11)

| ID | Invariant | Enforcement |
|----|-----------|-------------|
| **K-AGENTS-1** | Root `AGENTS.md` carries the Agent 0/1/2 runtime hierarchy and live index, governance integration and multi-agent orchestration rules, and canonical TASK-skill dispatch relationships. Workspace overlays may specialize but not weaken that governance. UI matrices are deployment routing views, not runtime authority classes. Registry/narrative disagreement is surfaced and the live registry governs. | `AGENTS.md`; D-GOV-11; AUDIT_GOVERNANCE; AUDIT_AGENTS; human review |

### A.3.12 Domain Engine Integration (CONTRACT §1.12)

| ID | Invariant | Enforcement |
|----|-----------|-------------|
| **K-DOMAIN-1** | **Domain engines own authoritative domain truth.** Canonical model files, model states, analysis runs, comparisons, solver outputs, and handoff internals are owned by the domain engine. Chirality governs the work around it (profiles, manifests, proposals, review notes, gates); it is not the solver and is never the source of accepted engineering truth. | DOMAIN_ENGINE persona; profile `protected_write_paths`; human review |
| **K-DOMAIN-2** | **Protected domain paths are write-quarantined.** Agents must not directly write protected domain artifacts. Domain-controlled writes occur only through declared deterministic tools under the active profile. | DOMAIN_ENGINE; TASK ScopePath/AllowedWriteTargets; profile; human review |
| **K-DOMAIN-3** | **Domain operations require an OperationProposal record and explicit human acceptance.** A proposal is `proposal_only` until validated by a declared deterministic tool and accepted by a human; application occurs only through a domain-engine-controlled apply. | DOMAIN_ENGINE Gate 5; profile; K-AUTH-1/K-AUTH-2; human review |
| **K-DOMAIN-4** | **Domain-engine outputs must not be represented as professional approval.** A green validation/PASS is structural evidence only — never code-compliance, certification, sealing, authentication, or external-prover validation absent a cited human authoritative record. Validation-passed is necessary, not sufficient, for engineering correctness. | DOMAIN_ENGINE professional_boundary; K-CLAIM-1; K-AUTH-1; AUDIT_GOVERNANCE; human review |

*Note (per CONTRACT §1.12):* Per the D-GOV-01 scope note, ruled 2026-07-01, engine-owned domain stores are sanctioned authoritative domain truth under K-DOMAIN-1 and are exempt from the governance rebuildable-cache rule.

---

## A.4 Enforcement Map Summary

The following table is reproduced from CONTRACT.md §2 (as of 2026-07-02) and maps each enforcement point to the invariants it is responsible for checking.

| Enforcement Point | Invariants Checked |
|-------------------|-------------------|
| **Agent instructions** (design-time; constrains intent, not guaranteed behavior) | K-GHOST-1, K-WRITE-1, K-WRITE-2, K-SNAP-1, K-PROV-1, K-INVENT-1, K-CONFLICT-1, K-CLAIM-1, K-DEP-1, K-DEP-2, K-AGENTS-1, K-DOMAIN-1, K-DOMAIN-2, K-DOMAIN-3, K-DOMAIN-4 |
| **TASK shell / tool path policy** (runtime) | K-WRITE-2 (ScopePath containment, `SPEC.md` §0.2.3) |
| **DOMAIN_ENGINE** (profile and operation governance) | K-DOMAIN-1, K-DOMAIN-2, K-DOMAIN-3, K-DOMAIN-4 |
| **ORCHESTRATOR** (runtime) | K-SEAL-1, K-GATE-1, K-HIER-1 |
| **Human review** (gate) | K-AUTH-1, K-AUTH-2, K-BIND-1, K-STALE-2, K-MERGE-1, K-VAL-1, K-STATUS-1, K-DOMAIN-1, K-DOMAIN-2, K-DOMAIN-3, K-DOMAIN-4 |
| **Governance audit** (AUDIT_GOVERNANCE / AUDIT_AGENTS) | K-CLAIM-1, K-PROV-1, K-AGENTS-1, K-DOMAIN-4 |
| **Future tooling** (automated) | K-STALE-1, K-VAL-1, K-MERGE-1, K-AUTH-2, K-DEP-2 |
| **PROJECT_DECOMP** (decomposition) | K-HIER-1, K-ID-1 |
