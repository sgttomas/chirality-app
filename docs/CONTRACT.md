# CONTRACT — Invariant Catalog

> **Status: RATIFIED — owner ratification 2026-07-11 (K-AUTH-1).** Owner direction of record (2026-07-11, in-session, Ryan Tufts): "You can now take all the `docs/` out of the DRAFT state, making them authoritative." This document is accepted root governance in full. Provenance: it re-established the monorepo-root governance layer (root `docs/` was hollowed out during the four-repo merge; see `plans/monorepo_root_governance_and_path_anchoring_2026-06-15.md`), authored from the prior root canon (`.archive/CONTRACT.md`), reproducing the 21 established invariants verbatim and adding six: **K-WRITE-2** (ScopePath containment), **K-AGENTS-1** (the Chirality `AGENTS.md` contract), and **K-DOMAIN-1..4** (domain engine integration).
>
> **Ratification history.** Per D-GOV-05 (docs/governance_harness/_DECISIONS/), ruled by the owner 2026-07-01, the **minimal harness basis** was ratified first: the source-of-truth rule, K-AUTH-1, K-AUTH-2, the generated-output rule, K-WRITE-2, K-PROV-1, K-STATUS-1, and the D-GOV-02 finding-severity taxonomy. The 2026-07-11 full ratification subsumes that partial basis; D-GOV-05 remains the ruling of record for the earlier partial state.

This document is the authoritative catalog of binding invariants for Chirality Root and the agent operating system it contains.

Invariants listed here are enforceable constraints that agents, tooling, and human processes must respect. Each invariant includes its enforcement point (where and how compliance is checked).

Invariant IDs (`K-*`) are **stable and never reused**. Retired invariants are moved to §3 with retirement rationale. Working roots (`projects/*`, `domains/*`) MAY extend this catalog in their own `docs/CONTRACT.md` (the app-dev workspace, for example, adds runtime `K-PATH-*`/`K-ROOT-*` families; the OpenPipeStress workspace forks into an `OPS-K-*` namespace); a working-root catalog MUST NOT weaken a framework invariant defined here.

---

## 1. Invariant Catalog

### K-* Invariant Index

All K-* identifiers defined in this section are listed below with their definition locations. There are **40 stable invariants** across 14 subsections.

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
| K-RUNTIME-1 | 1.13 | Shared Runtime |
| K-CONTROL-1 | 1.13 | Shared Runtime |
| K-PROJECT-1 | 1.13 | Shared Runtime |
| K-STORE-2 | 1.13 | Shared Runtime |
| K-RESIDENCY-1 | 1.13 | Shared Runtime (retired by D-GOV-43 item 13) |
| K-ROLE-2 | 1.13 | Shared Runtime |
| K-EXPORT-1 | 1.13 | Shared Runtime |
| K-TM-1 | 1.14 | Task Management |
| K-TM-2 | 1.14 | Task Management |
| K-TM-3 | 1.14 | Task Management |
| K-TM-4 | 1.14 | Task Management |
| K-TM-5 | 1.14 | Task Management |
| K-TM-6 | 1.14 | Task Management |

---

### 1.1 Hierarchy and Identity

| ID | Invariant | Enforcement |
|---|---|---|
| **K-HIER-1** | Projects are decomposed as **packages containing deliverables** (flat; no nesting; no phases layer). | `project-decomp` grouped checkpoints; `preparation` folder creation; human review |
| **K-ID-1** | Deliverable IDs are **stable** and persist across path changes. Path is a physical projection of decomposition, not identity. | decomposition workflows (ID assignment); all agents (ID referencing) |

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
| **K-DEP-1** | Deliverable-local `_DEPENDENCIES.md` and `Dependencies.csv` are **authoritative** for dependencies. There is no central dependency graph; generic read-only aggregation is on-demand via `_Evaluation/`; a calibrated corpus-concordance run may also inventory dependencies under `_Reconciliation/DeliverableConcordance/`. | TASK+dependency-extract (local writes only); WORKING_ITEMS with evaluation-protocol (generic audit) or reconciliation (activated corpus concordance) |
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
| **K-GATE-1** | Gates are **dynamic per project instance**. Minimum required gates: seal transition + pipeline run approval. Additional gates are project-configurable. | WORKING_ITEMS with project-setup (gate map); human configuration |

*Note:* D-GOV-02 (docs/governance_harness/_DECISIONS/), ruled 2026-07-01, derives from K-GATE-1 that no machine BLOCK on the CHECKING→ISSUED judgment may be non-overridable — BLOCKs apply to objective preconditions and hygiene only, and BLOCK override is human-only and recorded. Per D-GOV-17 (ruled 2026-07-18), a validator finding may never mechanically reject content the owner has adopted or ruled — where ruled text trips a validator, the validator is defective and is corrected under review, never the ruled text; other instruction-surface validator boundary cases are handled by D-GOV-17's recorded-exception correction protocol rather than anticipatory enumeration.

### 1.8 Merge and Publication

| ID | Invariant | Enforcement |
|---|---|---|
| **K-MERGE-1** | Merge to main is permitted within owner-authorized scope when required CI passes and independent review has no unresolved blocking findings, covering the actual candidate revision. Reassess affected checks after candidate changes and verify the source HEAD at merge. The standing Git grant in `PRD_ROOT.md` §5.3.1 supplies merge-execution authority without per-merge owner approval; explicit holds and later owner directions prevail. | Independent review; required CI; source-HEAD verification |

Owner amendment of 2026-09-12: standing authorization for Git integration is
not human acceptance of future content. K-AUTH-1/2 still govern acceptance for
reliance; merging does not approve a deliverable, change its lifecycle, or
publish a product release. Ordinary PR history records the reviewed source,
checks, independent review, and resulting merge; no separate approval registry
or recurring owner confirmation is required.

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
| **K-WRITE-2** | Agent writes must be **path-contained within the selected working root**. Every `ScopePath` and `AllowedWriteTarget` must normalize to an absolute path that resolves under `WORKING_ROOT`, which itself resolves within the active writable checkout (`REPO_ROOT`). A target resolving outside it — including the read-only `INSTRUCTION_ROOT`, a sibling pack, a symlink escape, or `..` traversal — is rejected (`SCOPE_OUTSIDE_WORKTREE` or `WRITE_TARGET_OUTSIDE_WORKTREE`) and the task stops. For the root product only, `WORKING_ROOT = REPO_ROOT` under D-GOV-21. | TASK shell (ScopePath normalization, `SPEC.md` §0.2.3); runtime project-root containment; tool path policy; human review of diffs |
| **K-SNAP-1** | Task agent outputs to tool roots are **immutable snapshots**. Pointer files (`_LATEST.md`) may be overwritten; snapshot folders must not. | Agent instruction constraints; SPEC.md Section 11 |

### 1.11 Agent Index and Governance Surface

| ID | Invariant | Enforcement |
|---|---|---|
| **K-AGENTS-1** | A Chirality **`AGENTS.md` is an authoritative governance surface**, carrying runtime entry doctrine and the four-role index. Under the D-GOV-41 prospective amendment, `agents/registry.json` supplies machine-readable role configuration, `workflows/` supplies explicitly selected methods, and canonical documents retain shared governance and integration rules. Working-root overlays may specialize the suite within accepted authority and cannot weaken framework governance. Live registries govern discovery over narrative lists; discrepancies are surfaced. Incompatible consumers retain their accepted basis until owning-loop adoption. | `AGENTS.md`; `docs/AGENT_WORKFLOW_RUNTIME.md`; D-GOV-41; workflow conformance and human review |

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
| **K-RUNTIME-1** | The Chirality App starts, owns, and stops one simplified Runtime service as a child process, and that service is the exclusive owner of the stock, version-pinned `codex app-server` child together with sessions, delegation, tools, turn locks, and interruption for that App instance. There is no per-user LaunchAgent and no exclusive per-user daemon. Credentials are custodied by Codex within Chirality's effective Codex home; the App never reads, copies, or relays credential material. Desktop, CLI, and project proxies MUST NOT construct a competing runtime (D-GOV-43 items 1, 6 and 7 as re-expressed by the A2 supplement). | Child-process ownership, relaunch, and quit tests; client conformance; packaged-process inspection |
| **K-CONTROL-1** | Runtime control uses authenticated, project-scoped HTTP/1.1 over one Unix-domain socket beneath the application user-data directory, with a `0700` parent directory and a `0600` socket, and per-launch client tokens private to the application. Stale-socket recovery verifies current-user ownership and absence of a live recorded process before removal. The accepted supervisor-socket design (R7-A through DEL-02-07) is retired with the daemon under D-GOV-43 item 7 as re-expressed by the A2 supplement. No second socket and no TCP control listener are permitted under any configuration. | Socket-mode, authorization, stale-owner, and listener tests |
| **K-PROJECT-1** | A tracked `chirality.project.json` contains stable identity and relative authority references only. Secrets, resolved machine paths, client tokens, and approval metadata remain user-data state. Authority-affecting manifest drift disables adapters until explicit re-registration. | Manifest schema/hash/containment tests; secret scan |
| **K-STORE-2** | Central runtime sessions remain JSON/JSONL and import legacy project-local sessions lazily and non-destructively. Runtime state never replaces checkout-contained governance truth. | Migration, replay, restart, and source-preservation tests |
| **K-RESIDENCY-1** | Retired from the live contract by D-GOV-43 item 13 (local models deferred; residency requirements retired with the daemon). The prior text is preserved in git history and in §3. | Retired |
| **K-ROLE-2** | Agent 0/1/2 names authority and responsibility, not a durable model assignment. Every governed run records actual adapter/provider/model and substitutions. | AgentRun/session attribution; governance scan |
| **K-EXPORT-1** | The public export may include generic runtime packages, CLI, contracts, and safe adapters. Credentials, machine state, and private project adapters are excluded. | Export allowlist/boundary checks |

K-WRITE-2 continues to govern agent and tool writes to project truth. The
Runtime service's socket, per-launch client tokens, logs, the App's thread
index, and Chirality's effective Codex home (including the shared Codex
sessions store and the Codex-custodied `auth.json`) may live beneath the
application user-data directory because they are explicitly non-authoritative
operational state; they do not grant an agent permission to write outside its
checkout scope.

### 1.14 Task Management

| ID | Invariant | Enforcement |
|---|---|---|
| **K-TM-1** | Task Management owns per-loop Action Item registers and nothing else. Every other domain's state is displayed by citation and remains with its owner | Governance audit; future tooling (`taskmgmt validate`) |
| **K-TM-2** | Registers are git-tracked files inside the owning loop's coordination surface. Any service store or index is a rebuildable, gitignored projection per D-GOV-01, never cited as authority. No engine-store exemption | Governance audit; future tooling (`taskmgmt validate`); D-GOV-01 projection discipline |
| **K-TM-3** | Register writes are judgment acts of the owning loop. Rows carry no directives; no cross-loop register writes; reading a register creates no duty outside a loop's own adopted instruments; no agent appears as accountable (A) for any row (K-AUTH-1) | Human review (the owner triage session is the sole disposition authority); agent instructions |
| **K-TM-4** | Graceful absence, re-scoped `[FINDING F-20]`: no act **outside a loop's own adopted instruments** may require a Task Management read or write. A loop binds itself by its own revocable ruling; deleting the service and its projections blocks nothing anywhere; registers remain plain readable, writable files. Kill test at every release (PEC-K-01 / PEC-SVC-004 pattern) | Release kill test (PEC-K-01 / PEC-SVC-004 pattern); human review |
| **K-TM-5** | A register row, view, or scan output never constitutes approval, acceptance, scope, priority authority, or lifecycle effect. Closure evidence binds to bytes (`EvidenceSha`); a row whose evidence changed after closure is stale, not still-closed | Human review; future tooling (`EvidenceSha` byte comparison per K-AUTH-2) |
| **K-TM-6** | Closure-capable schema: every register schema version carries `Status` and `Disposition`; a register that cannot record its own closure is invalid | Future tooling (register schema validation); governance audit |

Row text is verbatim from the adopted Chirality Task Management PRD §10
(Revision 2, adopted by D-GOV-32; subject SHA-256
`97e2ae6525ecbfdc52ff22aee85e1182a751c1090c2aa2f52faaf9e080f35d18`). D-GOV-32
Effect 5 adopted K-TM-1..6 as product invariants and reserved their entry
into this catalog to a governed tranche; this subsection is that entry, and
the "candidate" label in the PRD's §10 heading ends here.

---

## 2. Enforcement Map Summary

| Enforcement Point | Invariants Checked |
|---|---|
| **Shared governance, role instructions, and workflow contracts** (design-time; constrains intent, not guaranteed behavior) | K-GHOST-1, K-WRITE-1, K-WRITE-2, K-SNAP-1, K-PROV-1, K-INVENT-1, K-CONFLICT-1, K-CLAIM-1, K-DEP-1, K-DEP-2, K-AGENTS-1, K-DOMAIN-1, K-DOMAIN-2, K-DOMAIN-3, K-DOMAIN-4, K-ROLE-2, K-TM-3 |
| **TASK shell / tool path policy** (runtime) | K-WRITE-2 (ScopePath containment, `SPEC.md` §0.2.3) |
| **WORKING_ITEMS with domain-engine** (profile and operation governance) | K-DOMAIN-1, K-DOMAIN-2, K-DOMAIN-3, K-DOMAIN-4 |
| **WORKING_ITEMS with project-setup** (runtime) | K-SEAL-1, K-GATE-1, K-HIER-1 |
| **Human review** (gate) | K-AUTH-1, K-AUTH-2, K-BIND-1, K-STALE-2, K-MERGE-1, K-VAL-1, K-STATUS-1, K-DOMAIN-1, K-DOMAIN-2, K-DOMAIN-3, K-DOMAIN-4, K-TM-3, K-TM-4, K-TM-5 |
| **TASK with audit-governance / audit-agents** | K-CLAIM-1, K-PROV-1, K-AGENTS-1, K-DOMAIN-4, K-TM-1, K-TM-2, K-TM-6 |
| **Future tooling** (automated) | K-STALE-1, K-VAL-1, K-MERGE-1, K-AUTH-2, K-DEP-2, K-TM-1, K-TM-2, K-TM-5, K-TM-6 |
| **WORKING_ITEMS with decomposition workflows** | K-HIER-1, K-ID-1 |
| **Application-owned Runtime service and Codex child** (runtime) | K-RUNTIME-1, K-CONTROL-1, K-PROJECT-1, K-STORE-2, K-ROLE-2 |
| **Public export builder** (publication boundary) | K-EXPORT-1 |

---

## 3. Retired Invariants

| ID | Retired by | Prior invariant (preserved, not live) |
|---|---|---|
| **K-RESIDENCY-1** | D-GOV-43 item 13 (ruled 2026-09-11; applied by the A2 application tranche) | The daemon manages at most one primary local LLM. Activation is explicit, drains rather than interrupts active Pi work, never unloads unknown helper models, records a residency epoch, and fails closed without fallback. Enforcement was fake-oMLX and opt-in live proofs. Local models, when taken up, are Codex model providers. |
