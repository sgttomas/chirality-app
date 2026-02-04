# Stability Assessment Report — Project Template → Domain Template (Chirality App)

Date: 2026-02-03  
Scope: Assess **stable patterns** preserved during the transition from a **project template** (PKG/DEL, deliverables) to a **domain knowledge template** (CAT/KTY, knowledge artifacts), across:
- **Ontology** (what exists / entities & relations)
- **Epistemology** (what counts as true / how truth is grounded)
- **Praxeology** (how work is done / operational method)
- **Axiology** (what is valued / what success prioritizes)

Primary inputs:
- `DOMAIN_TEMPLATE_SPEC.md` (domain-template contract draft)
- `DECISION.md` (replace strategy draft)
- `GUIDANCE.md`, `PATCH_PLAN.md`, `INVENTORY.md` (transition framing + inventory + plan)
- `README.md`, `AGENTS.md` (project-template conventions and governance)
- `AGENT_DOMAIN_DECOMP.md` (domain decomposition protocol)

---

## Executive summary

The transition is framed as a **context shift with label/role substitutions**, not a reinvention of the system. The stable patterns are:

1. **Filesystem-as-state remains the control surface.** Both contexts treat on-disk artifacts as the source of truth, and tool roots as snapshot-producing “reports,” not mutable working state.
2. **Flat partitioning + stable IDs remains the backbone.** Each context uses a flat partition primitive and enforces stable identifiers. (Context-specific nouns are treated as semantics; see Appendix B for project-template validation.)
3. **Layered agent governance remains constant.** Type 0/1/2 layering, write-scope discipline, and gate-controlled human validation persist unchanged.
4. **Anti-invention + provenance-first truth persists.** Both contexts require explicit uncertainty (TBD), traceable rationale, and “no silent fixes.”
5. **Work remains lifecycle-driven**, but the lifecycle target changes from **deliverables/doc sets** to **knowledge artifacts**.

---

## 1) Ontology — what stays stable

### Stable ontological pattern: “Partition → Work Unit → Artifacts”
Project template ontology (conceptual):
- Partition: **Package (PKG)** (flat partition of scope)
- Work unit: **Deliverable (DEL)** (unit of production)
- Artifacts: 4-doc set + metadata files per deliverable folder

Domain template ontology (conceptual):
- Partition: **Category (CAT)** (flat partition of in-scope source units)
- Work unit: **Knowledge Type (KTY)** (reusable kind of knowledge object)
- Artifacts: concrete knowledge artifacts (procedure/checklist/template/etc.) + metadata per KTY folder

**What’s stable:** the **shape** of the ontology. Only the labels and semantics of the “work unit” shift.

### Stable ontological invariants
- **Flat partitions** are required (no nesting) and must cover the in-scope universe without gaps/overlaps:
  - Project: packages are flat partitions of scope.
  - Domain: categories are flat partitions of IN-scope units, and every IN unit maps to exactly one category.
- **Stable IDs** are required for longitudinal tracking (renumbering only by explicit human choice).
- **One-parent rule** stays stable:
  - Deliverable belongs to one package.
  - Knowledge Type belongs to one category.
- **Ledger-based traceability** stays stable:
  - Project decomposition uses a scope ledger.
  - Domain decomposition uses a domain ledger.

### Stable structural roles (context-neutral)

To avoid mixing project-template nouns into the domain knowledge context, we describe the *stable structure* using **context-neutral roles**, and we treat context-specific nouns as **semantics** that belong to their own contexts.

| Structural role | Meaning |
|---|---|
| Partition primitive | Flat partition of the in-scope universe (no nesting; no overlap; no gaps) |
| Work-unit primitive | Unit of production that owns a local workspace and produces artifacts |
| Atomic units | Smallest traceable units extracted from source material (ledger rows) |
| Success criteria | High-level objectives derived from source intent |
| Traceability table | Ledger proving coverage and mappings |
| Cross-scope checks | Read-only scans / syntheses across a chosen scope |
| Output stores | On-disk locations for working state vs snapshots |

**Domain knowledge canonical labels (used throughout):**
- Partition primitive: **Category (CAT)**
- Work-unit primitive: **Knowledge Type (KTY)**
- Atomic units: **Source Units** (e.g., `HBK-####`)
- Artifacts: **Knowledge Artifacts** (e.g., Procedure, Checklist, Template, Guidance, Reference)

---

## 2) Epistemology — what stays stable

### Stable epistemic posture: “Grounded, auditable, explicit uncertainty”
Across both contexts, truth is not “what the model says,” but what can be **anchored** to explicit sources and artifacts:

- **No invention**: missing knowledge must be marked `TBD` / open issue rather than fabricated.
- **Provenance** is mandatory: source refs are tracked (project references; domain SourceRef per unit).
- **Human validation gates** remain the acceptance mechanism for structural decisions (boundaries, category assignment, objectives, etc.).

### Stable epistemic mechanisms (how correctness is checked)
- **Machine-checkable coverage telemetry** is a core motif:
  - Project decomposition: scope coverage is enforced by ledger mapping.
  - Domain decomposition: unit→category must be complete (Unassigned IN units must be 0), and missing KT mappings are surfaced as open issues.
- **Decision logging**: non-trivial boundary/mapping decisions are recorded, not hidden.

### What changes (but preserves the epistemic pattern)
- The unit of grounding shifts:
  - Project: grounding often ties to SOW / project inputs and deliverable-local documents.
  - Domain: grounding ties to `_Sources/` documents and extracted atomic units (HBK-####).

---

## 3) Praxeology — what stays stable

### Stable praxeological pattern: “Gate-controlled decomposition → scaffold → produce artifacts → QA → publish”
Project flow (typical):
1) PROJECT_DECOMP produces decomposition
2) PREPARATION / 4_DOCUMENTS scaffold and draft deliverable docs
3) WORKING_ITEMS iterates on a deliverable
4) DEPENDENCIES / AGGREGATION / RECONCILIATION / ESTIMATING provide cross-scope tooling
5) Lifecycle advances to ISSUED via human validation

Domain flow (proposed):
1) DOMAIN_DECOMP produces domain decomposition under `run/_Decomposition/`
2) DOMAIN_SCAFFOLD creates CAT/KTY folder structure under `run/_Domain/`
3) KNOWLEDGE_ARTIFACTS drafts artifacts per Knowledge Type
4) DOMAIN_TELEMETRY + DOMAIN_RECONCILIATION provide QA/coverage checks
5) Knowledge artifacts progress toward PUBLISHED via human approval

**What’s stable:** the “pipeline shape” and the discipline: decompose first, then scaffold, then produce bounded artifacts, then QA, then publish.

### Stable operational constraints
- **Write-scope discipline** remains: each agent is constrained to a zone (tool roots, decomposition, deliverable/KTY local).
- **Cross-scope operations are opt-in**: aggregation/reconciliation are invoked deliberately, not as background processes.
- **Snapshot orientation** remains: tool roots output timestamped snapshots and may update `_LATEST.md`, but do not overwrite history.

### What changes (but keeps the praxeological form)
- The scaffold target: from deliverable folders to category/type folders.
- The primary artifact set: from the “4 Documents” to a set of knowledge artifacts keyed to Knowledge Types.

---

## 4) Axiology — what stays stable

### Stable values: control, auditability, and human accountability
Across both contexts the framework values:
- **Auditability / traceability** over “fast but opaque” generation.
- **Human agency** as the halting condition and approval gate.
- **Conservative change management**: avoid dual-mode complexity unless explicitly chosen; prefer explicit deprecations and clear docs.

### Stable “quality” definition
Quality is defined less by eloquence and more by:
- coverage (no gaps at partition level),
- consistency (no silent conflicts),
- provenance (traceability to sources),
- and review readiness (structured artifacts, decision logs, snapshots).

### What changes (but preserves value alignment)
- The “thing being protected” shifts from project deliverables/lifecycle to domain knowledge artifacts/lifecycle.
- Backward compatibility is explicitly deprioritized in the current decision framing (replace strategy).

---

## 5) Stable patterns checklist (for transition QA)

Use this as a quick verification lens when reviewing edits:

### Ontology (structure)
- [ ] Flat partitions remain (no nesting, no overlaps, no gaps)
- [ ] Stable IDs remain mandatory
- [ ] One-parent mapping rule remains
- [ ] Ledger remains the canonical mapping table

### Epistemology (truth)
- [ ] No-invention rule remains explicit
- [ ] Provenance is required; missing refs become TBD/OpenIssue
- [ ] Human gates remain the acceptance mechanism
- [ ] Decision log remains required for non-trivial boundary choices

### Praxeology (method)
- [ ] Decompose → scaffold → produce → QA → publish pipeline preserved
- [ ] Write scopes remain narrow and declared
- [ ] Tool roots produce snapshots; inputs are not overwritten
- [ ] Cross-scope checks remain opt-in

### Axiology (values)
- [ ] Auditability is prioritized over speed
- [ ] Explicit deprecations preferred over silent drift
- [ ] Human accountability is preserved

---

## 6) Terminology discipline for domain knowledge

In the **domain knowledge context**, the canonical nouns are:

- **Sources** (a multi-file corpus under `_Sources/`)
- **Source Units** (`HBK-####`) extracted from Sources
- **Categories** (`CAT-###`) as the flat partition primitive
- **Knowledge Types** (`KTY-CC-TT_{shortDescription}`) as the work-unit primitive
- **Knowledge Artifacts** (instances produced under a Knowledge Type)

**Rule:** Project-template nouns MUST NOT be used to name domain entities. If cross-context comparison is required for validation, it must be confined to an explicitly labeled appendix (see Appendix B).


---

## 7) Risks to stability (watch-outs)

1) **Category drift**: violating “alterations of type, not category” creates ontology churn that breaks ID stability and longitudinal comparisons.
2) **Dual meaning of “References”**: `_REFERENCES.md` already has a specific role; avoid naming a folder `_References/` when `_Sources/` is intended.
3) **Tool-root recursion**: snapshots must not become their own inputs unless explicitly included, or epistemic grounding will degrade.
4) **Agent index divergence**: `AGENTS.md` must match the actual agent suite; inventory already flags mismatches.

---

## 8) Recommended next QA action (minimal)

After applying the domain-template edits, run a repo-wide grep for legacy project primitives:
- `PKG-`, `DEL-`, `4 Documents`, `OPEN → INITIALIZED → ... → ISSUED`
and verify they are either:
- removed, or
- explicitly documented as deprecated under `_LegacyProject/` (if retained).

---


---

## Appendix B — Project-template contract cross-check (PROJECT_DECOMP)

> This appendix uses project-template terminology only to validate that the structural invariants in this report agree with the canonical PROJECT_DECOMP contract.
> It is not part of the domain knowledge ontology.


This section was added on 2026-02-03 after reviewing the **canonical PROJECT_DECOMP agent contract**.

### Where the prior analysis matches PROJECT_DECOMP

**1) Ontology shape (stable):** PROJECT_DECOMP explicitly defines the same structural skeleton I described:
- Atomic units (**Scope Items**) → flat partitions (**Packages**) → work units (**Deliverables**) → anticipated **Artifacts**, with **Objectives** and **Coverage & Telemetry**.  
This mirrors the domain side’s **Handbook Units → Categories → Knowledge Types → Knowledge Artifacts**, which is why the “partition → work unit → artifacts” mapping remains the right stable pattern.

**2) Epistemic rules (stable):** PROJECT_DECOMP’s invariants include **human validation gates**, **no invention**, and **traceable rationale**, plus a ledger + telemetry system for machine-checkable completeness. That aligns with the domain-side DOMAIN_DECOMP contract.

**3) Praxeology (stable):** PROJECT_DECOMP is explicitly **phase/gate controlled** (Phases 1–7) with the same “living decomposition document” method. This is the same praxeological pattern as DOMAIN_DECOMP; only the nouns differ.

**4) Axiology (stable):** The rationale emphasizes long-horizon reliability, stable referents, antifragile telemetry, and vocabulary control—exactly the value posture captured in the earlier report.

### Where the prior analysis needed correction / tightening

**A) Deliverable ID convention (too generic before):** PROJECT_DECOMP is precise about deliverable IDs:
- Deliverables must use **`DEL-PP-LL_{shortDescription}`** (hyphen-separated package/deliverable pair, underscore before suffix) and explicitly rejects the older dot style.  
The earlier report described deliverables generally but did not name this pattern; this update corrects that.

**B) Scope Item ID example (not stated before):** PROJECT_DECOMP defines scope items as `ScopeItemID` with an example **`SOW-0001`**.  
The earlier report referred to “SSOW / scope items” conceptually; this update makes the identifier convention explicit.

**C) Boundary of “PROJECT_DECOMP” vs “project workflow”:** PROJECT_DECOMP governs decomposition only. The earlier report referenced downstream project workflow steps (e.g., scaffolding drafts) as part of the project context; that’s accurate for the repo’s overall method, but it is **not** part of PROJECT_DECOMP itself. This update clarifies that those steps belong to other agents (e.g., PREPARATION / 4_DOCUMENTS), not PROJECT_DECOMP.

### Net result

The stability analysis still holds: the transition preserves the **same decomposition ontology and control discipline**, and swaps the domain nouns:
- **Scope Item ↔ Handbook Unit**
- **Package ↔ Category**
- **Deliverable ↔ Knowledge Type**
- **Artifact ↔ Knowledge Artifact**
…but the updated report now reflects PROJECT_DECOMP’s **exact ID conventions** and the correct boundary between decomposition and downstream production workflows.


## Appendix A — Evidence anchors (where these patterns come from)

- “Domain template only” + replace strategy + constraints (type changes preferred): see `DECISION.md`, `DOMAIN_TEMPLATE_SPEC.md`, `GUIDANCE.md`.
- Domain ontology primitives and ID rules (HBK/OBJ/CAT/KTY, stable IDs, flat categories): `DOMAIN_TEMPLATE_SPEC.md` and `AGENT_DOMAIN_DECOMP.md`.
- Filesystem-as-state + lifecycle + separation of local vs cross-scope operations (project context): `README.md`, `AGENTS.md`.
- Transition mechanics (what gets added/modified/deprecated): `PATCH_PLAN.md` and `INVENTORY.md`.
