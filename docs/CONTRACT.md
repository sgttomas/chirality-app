# CONTRACT — Invariant Catalog

> **Status: RATIFIED — owner ratification 2026-07-11 (K-AUTH-1).** Owner direction of record (2026-07-11, in-session, Ryan Tufts): "You can now take all the `docs/` out of the DRAFT state, making them authoritative." This document is accepted root governance in full. Provenance: it re-established the monorepo-root governance layer (root `docs/` was hollowed out during the four-repo merge; see `plans/monorepo_root_governance_and_path_anchoring_2026-06-15.md`), authored from the prior root canon (`.archive/CONTRACT.md`), reproducing the 21 established invariants verbatim and adding six: **K-WRITE-2** (ScopePath containment), **K-AGENTS-1** (the Chirality `AGENTS.md` contract), and **K-DOMAIN-1..4** (domain engine integration).
>
> **Ratification history.** Per D-GOV-05 (docs/governance_harness/_DECISIONS/), ruled by the owner 2026-07-01, the **minimal harness basis** was ratified first: the source-of-truth rule, K-AUTH-1, K-AUTH-2, the generated-output rule, K-WRITE-2, K-PROV-1, K-STATUS-1, and the D-GOV-02 finding-severity taxonomy. The 2026-07-11 full ratification subsumes that partial basis; D-GOV-05 remains the ruling of record for the earlier partial state.

This document is the authoritative catalog of binding invariants for the Chirality agent operating system.

Invariants listed here are enforceable constraints that agents, tooling, and human processes must respect. Each invariant includes its enforcement point (where and how compliance is checked).

Invariant IDs (`K-*`) are **stable and never reused**. Retired invariants are moved to §3 with retirement rationale. Working roots (`projects/*`, `domains/*`) MAY extend this catalog in their own `docs/CONTRACT.md` (the app-dev workspace, for example, adds runtime `K-PATH-*`/`K-ROOT-*` families; the OpenPipeStress workspace forks into an `OPS-K-*` namespace); a working-root catalog MUST NOT weaken a framework invariant defined here.

---

## 1. Invariant Catalog

### K-* Invariant Index

All K-* identifiers defined in this section are listed below with their definition locations. There are **27 stable invariants** across 12 subsections.

| K-* ID | Subsection | Topic |
|---|---|---|
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
| K-WRITE-2 | 1.10 | Write Scope and Snapshots |
| K-SNAP-1 | 1.10 | Write Scope and Snapshots |
| K-AGENTS-1 | 1.11 | Agent Index and Governance Surface |
| K-DOMAIN-1 | 1.12 | Domain Engine Integration |
| K-DOMAIN-2 | 1.12 | Domain Engine Integration |
| K-DOMAIN-3 | 1.12 | Domain Engine Integration |
| K-DOMAIN-4 | 1.12 | Domain Engine Integration |

---

### 1.1 Hierarchy and Identity

| ID | Invariant | Enforcement |
|---|---|---|
| **K-HIER-1** | Projects are decomposed as **packages containing deliverables** (flat; no nesting; no phases layer). | PROJECT_DECOMP gates; PREPARATION folder creation; human review |
| **K-ID-1** | Deliverable IDs are **stable** and persist across path changes. Path is a physical projection of decomposition, not identity. | PROJECT_DECOMP (ID assignment); all agents (ID referencing) |

### 1.2 Authority and Approval

| ID | Invariant | Enforcement |
|---|---|---|
| **K-AUTH-1** | Only **humans** author binding approval records. No agent may claim to certify, approve, sign, seal, or issue work for reliance. | Agent instruction constraints; human review |
| **K-AUTH-2** | Approvals bind to a **specific git SHA**. Content change after approval voids the approval. | Human review; future tooling (SHA comparison) |
| **K-BIND-1** | Approvals are **always binding and only binding**. Non-binding guidance is allowed outside approval records. | Human process discipline |

### 1.3 Sealing and Context

| ID | Invariant | Enforcement |
|---|---|---|
| **K-SEAL-1** | No delegated child execution before context is **sealed**, the run is approved at the applicable human gate, and the launch cites that human approval record. A non-empty reference is necessary runtime metadata, not proof that approval occurred. | Human approval record and review; ManagedDelegationService structural checks; fail-closed legacy adapter |
| **K-GHOST-1** | Agent 2 context is limited to declared read scopes and accepted references. No ghost inputs. | Managed child session metadata; permission overlay and path policy; sealed brief; human review |

### 1.4 Dependencies

| ID | Invariant | Enforcement |
|---|---|---|
| **K-DEP-1** | Deliverable-local `_DEPENDENCIES.md` and `Dependencies.csv` are **authoritative** for dependencies. There is no central dependency graph; generic read-only aggregation is on-demand via `_Evaluation/`; a calibrated corpus-concordance run may also inventory dependencies under `_Reconciliation/DeliverableConcordance/`. | TASK+dependency-extract (local writes only); EVALUATION (generic audit); RECONCILIATION (activated corpus concordance) |
| **K-DEP-2** | Dependency references to deliverables must **resolve to existing deliverable IDs**. Unresolvable targets use `TargetType=UNKNOWN`. | TASK+dependency-extract (Function 2); validation checks |

### 1.5 Status and Lifecycle

| ID | Invariant | Enforcement |
|---|---|---|
| **K-STATUS-1** | `_STATUS.md` is the **canonical, human-readable lifecycle state file** for each deliverable. No other file determines deliverable state. | All agents (read _STATUS.md for state); transition rules in SPEC.md Section 3.3 |

### 1.6 Staleness and Change Propagation

| ID | Invariant | Enforcement |
|---|---|---|
| **K-STALE-1** | Upstream changes **propagate staleness** to all transitive dependent deliverables. | Future tooling (staleness calculation); human triage |
| **K-STALE-2** | Stale items must be **triaged by a human** before being considered current. Resolution modes: no impact (clear flag), needs rework, or needs review. | Human triage queue |
| **K-VAL-1** | A deliverable is **dirty** if any governed input has changed since its last approved SHA. | Future tooling (SHA comparison); human review |

### 1.7 Gates

| ID | Invariant | Enforcement |
|---|---|---|
| **K-GATE-1** | Gates are **dynamic per project instance**. Minimum required gates: seal transition + pipeline run approval. Additional gates are project-configurable. | PROJECT_SETUP (gate map); human configuration |

*Note:* D-GOV-02 (docs/governance_harness/_DECISIONS/), ruled 2026-07-01, derives from K-GATE-1 that no machine BLOCK on the CHECKING→ISSUED judgment may be non-overridable — BLOCKs apply to objective preconditions and hygiene only, and BLOCK override is human-only and recorded. Per D-GOV-17 (ruled 2026-07-18), a validator finding may never mechanically reject content the owner has adopted or ruled — where ruled text trips a validator, the validator is defective and is corrected under review, never the ruled text; other instruction-surface validator boundary cases are handled by D-GOV-17's recorded-exception correction protocol rather than anticipatory enumeration.

### 1.8 Merge and Publication

| ID | Invariant | Enforcement |
|---|---|---|
| **K-MERGE-1** | Merge to main allowed only when **branch HEAD == approved SHA** for the relevant run. | Human review; future CI check |

### 1.9 Provenance and Epistemic Integrity

| ID | Invariant | Enforcement |
|---|---|---|
| **K-PROV-1** | Every non-trivial governed claim must cite evidence with a source path and best-effort section reference, or carry explicit `location TBD`. Dependency rows are a schema-specific instance of this rule and use **`EvidenceFile` + `SourceRef`** per `SPEC.md` §6.5. | Agent instruction constraints; TASK+dependency-extract row validation; governance audits; human review |
| **K-INVENT-1** | Unknown values become **`TBD`**, not guessed. Agents must not invent scope items, dependency targets, parameter values, or engineering content. | All agent instruction invariants; human review |
| **K-CONFLICT-1** | Conflicts between sources must be **surfaced, not silently resolved**. Agents expose disagreements with pointers to the conflicting sources. | Workflow-component standard R7; agent instruction invariants; human adjudication |
| **K-CLAIM-1** | Claims, conclusions, and characterizations must not **overstate what the available warrant supports**. Statements of necessity, sufficiency, universality, completeness, exclusivity, or direct regulatory conclusiveness may be used only when the cited evidence supports that strength; otherwise they must be framed as interpretation, implementation-specific design, or proposal. | Agent instruction constraints; governance audits (AUDIT_GOVERNANCE); human review |

### 1.10 Write Scope and Snapshots

| ID | Invariant | Enforcement |
|---|---|---|
| **K-WRITE-1** | Every agent has an **explicit write scope** declared in its header block. No agent writes outside its declared zone. | Agent Type table (WRITE_SCOPE property); human review of diffs |
| **K-WRITE-2** | Agent writes must be **path-contained within the active checkout**. Every `ScopePath` and `AllowedWriteTarget` must normalize to an absolute path that resolves under `git rev-parse --show-toplevel` (`REPO_ROOT`); a target resolving outside it — including via symlink or `..` traversal — is rejected (`SCOPE_OUTSIDE_WORKTREE`) and the task stops. This confines a task's effects to its working root and makes per-working-root and git-worktree isolation safe. | TASK shell (ScopePath normalization, `SPEC.md` §0.2.3); tool path policy; human review of diffs |
| **K-SNAP-1** | Task agent outputs to tool roots are **immutable snapshots**. Pointer files (`_LATEST.md`) may be overwritten; snapshot folders must not. | Agent instruction constraints; SPEC.md Section 11 |

### 1.11 Agent Index and Governance Surface

| ID | Invariant | Enforcement |
|---|---|---|
| **K-AGENTS-1** | A Chirality **`AGENTS.md` is an authoritative governance surface, not merely an index**, and agents treat it as authoritative. Under D-GOV-11, the framework-root `AGENTS.md` MUST carry the Agent 0/1/2 runtime hierarchy and live index, governance integration rules (derivative-package, snapshot, handoff-state, closure, sequencing, cycle-resolution), multi-agent orchestration rules, and canonical `TASK`-skill dispatch relationships. A working-root (`projects/*`, `domains/*`) `AGENTS.md` MAY overlay or specialize the suite for that workspace but MUST NOT weaken framework governance. UI matrices are deployment routing views, not runtime authority classes. Where live registries (`agents/`, `skills/`, `tools/`) and narrative disagree, the live registry governs and the discrepancy is surfaced. | `AGENTS.md`; D-GOV-11; AUDIT_GOVERNANCE; AUDIT_AGENTS; human review |

### 1.12 Domain Engine Integration

| ID | Invariant | Enforcement |
|---|---|---|
| **K-DOMAIN-1** | **Domain engines own authoritative domain truth.** Canonical model files, model states, analysis runs, comparisons, solver outputs, and handoff internals are owned by the domain engine. Chirality governs the work around it (profiles, manifests, proposals, review notes, gates); it is not the solver and is never the source of accepted engineering truth. | DOMAIN_ENGINE persona; profile `protected_write_paths`; human review |
| **K-DOMAIN-2** | **Protected domain paths are write-quarantined.** Agents must not directly write protected domain artifacts. Domain-controlled writes occur only through declared deterministic tools under the active profile. | DOMAIN_ENGINE; TASK ScopePath/AllowedWriteTargets; profile; human review |
| **K-DOMAIN-3** | **Domain operations require an OperationProposal record and explicit human acceptance.** A proposal is `proposal_only` until validated by a declared deterministic tool and accepted by a human; application occurs only through a domain-engine-controlled apply. | DOMAIN_ENGINE Gate 5; profile; K-AUTH-1/K-AUTH-2; human review |
| **K-DOMAIN-4** | **Domain-engine outputs must not be represented as professional approval.** A green validation/PASS is structural evidence only - never code-compliance, certification, sealing, authentication, or external-prover validation absent a cited human authoritative record. Validation-passed is necessary, not sufficient, for engineering correctness. | DOMAIN_ENGINE professional_boundary; K-CLAIM-1; K-AUTH-1; AUDIT_GOVERNANCE; human review |

*Note:* Per the D-GOV-01 (docs/governance_harness/_DECISIONS/) scope note, ruled 2026-07-01, engine-owned domain stores are sanctioned authoritative domain truth under K-DOMAIN-1 and are exempt from the governance rebuildable-cache rule.

### 1.13 Shared Runtime

| ID | Invariant | Enforcement |
|---|---|---|
| **K-RUNTIME-1** | One opt-in per-user daemon is the exclusive production owner of engines, credentials, sessions, delegation, tools, turn locks, interruption, and local-model residency. Desktop, CLI, and project proxies MUST NOT construct a competing runtime. | Runtime daemon singleton; client conformance; packaged-process inspection |
| **K-CONTROL-1** | Runtime control uses authenticated, project-scoped HTTP/1.1 over `{userData}/runtime/control.sock` beneath a `0700` directory with a `0600` socket. A TCP control listener is forbidden. | Socket-mode, authorization, stale-owner, and listener tests |
| **K-PROJECT-1** | A tracked `chirality.project.json` contains stable identity and relative authority references only. Secrets, resolved machine paths, client tokens, and approval metadata remain user-data state. Authority-affecting manifest drift disables adapters until explicit re-registration. | Manifest schema/hash/containment tests; secret scan |
| **K-STORE-2** | Central runtime sessions remain JSON/JSONL and import legacy project-local sessions lazily and non-destructively. Runtime state never replaces checkout-contained governance truth. | Migration, replay, restart, and source-preservation tests |
| **K-RESIDENCY-1** | The daemon manages at most one primary local LLM. Activation is explicit, drains rather than interrupts active Pi work, never unloads unknown helper models, records a residency epoch, and fails closed without fallback. | Fake-oMLX and opt-in live proofs |
| **K-ROLE-2** | Agent 0/1/2 names authority and responsibility, not a durable model assignment. Every governed run records actual adapter/provider/model and substitutions. | AgentRun/session attribution; governance scan |
| **K-EXPORT-1** | The public export may include generic runtime packages, CLI, contracts, and safe adapters. Credentials, machine state, and private project adapters are excluded. | Export allowlist/boundary checks |

K-WRITE-2 continues to govern agent and tool writes to project truth. The
daemon’s socket, encrypted credentials, client tokens, logs, residency
evidence, and central runtime session mirrors may live beneath the application
user-data directory because they are explicitly non-authoritative operational
state; they do not grant an agent permission to write outside its checkout
scope.

---

## 2. Enforcement Map Summary

| Enforcement Point | Invariants Checked |
|---|---|
| **Agent instructions** (design-time; constrains intent, not guaranteed behavior) | K-GHOST-1, K-WRITE-1, K-WRITE-2, K-SNAP-1, K-PROV-1, K-INVENT-1, K-CONFLICT-1, K-CLAIM-1, K-DEP-1, K-DEP-2, K-AGENTS-1, K-DOMAIN-1, K-DOMAIN-2, K-DOMAIN-3, K-DOMAIN-4, K-ROLE-2 |
| **TASK shell / tool path policy** (runtime) | K-WRITE-2 (ScopePath containment, `SPEC.md` §0.2.3) |
| **DOMAIN_ENGINE** (profile and operation governance) | K-DOMAIN-1, K-DOMAIN-2, K-DOMAIN-3, K-DOMAIN-4 |
| **PROJECT_SETUP** (runtime) | K-SEAL-1, K-GATE-1, K-HIER-1 |
| **Human review** (gate) | K-AUTH-1, K-AUTH-2, K-BIND-1, K-STALE-2, K-MERGE-1, K-VAL-1, K-STATUS-1, K-DOMAIN-1, K-DOMAIN-2, K-DOMAIN-3, K-DOMAIN-4 |
| **Governance audit** (AUDIT_GOVERNANCE / AUDIT_AGENTS) | K-CLAIM-1, K-PROV-1, K-AGENTS-1, K-DOMAIN-4 |
| **Future tooling** (automated) | K-STALE-1, K-VAL-1, K-MERGE-1, K-AUTH-2, K-DEP-2 |
| **PROJECT_DECOMP** (decomposition) | K-HIER-1, K-ID-1 |
| **Shared runtime daemon and clients** (runtime) | K-RUNTIME-1, K-CONTROL-1, K-PROJECT-1, K-STORE-2, K-RESIDENCY-1, K-ROLE-2 |
| **Public export builder** (publication boundary) | K-EXPORT-1 |

---

## 3. Retired Invariants

No invariants have been retired.
