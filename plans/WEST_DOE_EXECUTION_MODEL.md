# Execution Model: West Doe Two-Root DBM Remediation Campaign

## Context

Defines the agent topology for executing the remediation plan at
`plans/WEST_DOE_TWO_ROOT_DBM_REMEDIATION_AND_PUBLICATION_PLAN.md`. This is a
separate execution-model document. Vendor/model-specific orchestration stays
here, not in the normative workflow plan.

For this campaign, regenerated KTY-local artifacts, hypergraph outputs,
AUDIT_DECOMP snapshots, and final publication packages are all treated as
**derivative packages**. The accepted `_ScopeChange` snapshot in each root
remains the authoritative remediation boundary; later phases consume
derivative packages only through an explicit handoff-state that names the
accepted source snapshot and closure status.

---

## Package Architecture — Governance Terms

The following terms apply consistently across both roots in this campaign and
align with the decomposition-family definitions in `AGENT_DECOMP_BASE.md`.

| Term | Definition |
|---|---|
| **Canonical working package** | The main decomposition document + authoritative companion registers + `_ScopeChange` state. This is the authoritative amendment surface for each root. |
| **Authoritative companion register** | A CSV, JSON, or structured markdown file holding heavy machine-truth as the primary working surface for that data (e.g., domain ledger, category register, KTY register). |
| **Derived publication artifact** | A single-file render, publication bundle, or review document assembled from the modular package. Not the amendment surface. Includes `Rewritten_DBM.md` and other `DBM_PUBLISHER` outputs. |
| **Package-role label** | An explicit declaration of each artifact's role: working surface, authoritative companion register, snapshot/handoff artifact, or derived publication artifact. |

The modular decomposition package is the preferred package shape for both roots.
Remediation agents, publication agents, and the cross-root conformity gate all
operate on the canonical working package as the authoritative truth surface.
Derivative packages (regenerated KTY artifacts, hypergraph snapshots,
`AUDIT_DECOMP` snapshots, and `DBM_PUBLISHER` publication packages) are
downstream consumers of that truth, not substitutes for it.

---

## Agent Topology

```
CAMPAIGN CONTROLLER (SCOPE_CHANGE persona, Opus)
├── Phase 1: Freeze authority inputs
├── Phase 2: Build and approve allocation matrix
│
├── [after Phases 1-2, human opens new sessions]
│
│   CONDITIONAL CONCURRENCY ZONE
│   ┌─────────────────────────────────────────────────────────┐
│   │                                                         │
│   │  DEEPCUT REMEDIATION AGENT (Opus, separate session)     │
│   │  ├── Phase 3: SCOPE_CHANGE on Deepcut (SCA-003)         │
│   │  ├── Phase 4: Regenerate Deepcut downstream             │
│   │  │   └── Sonnet subagents (one per KTY, on-demand)      │
│   │  └── Writes: plans/Deepcut_Terminology_Decisions.md     │
│   │      Stops after Phase 4. No Phase 8 work.              │
│   │                                                         │
│   │  COMP & LIQUIDS REMEDIATION AGENT (Opus, separate sess) │
│   │  ├── Phase 5: SCOPE_CHANGE on C&L (SCA-003)             │
│   │  ├── Phase 6: Regenerate C&L downstream                 │
│   │  │   └── Sonnet subagents (one per KTY, on-demand)      │
│   │  └── Stops after Phase 6. No Phase 8 work.              │
│   │                                                         │
│   │  CONCURRENCY RULES:                                     │
│   │  • Root-local rows (DEEPCUT_ONLY / COMP_LIQ_ONLY)       │
│   │    may run in parallel                                   │
│   │  • SHARED_INTERFACE rows: Deepcut normalizes first,      │
│   │    human reviews, then C&L finalizes                     │
│   │  • Blockers → stop, record, escalate to controller      │
│   └─────────────────────────────────────────────────────────┘
│
├── [human reviews Deepcut_Terminology_Decisions.md]
├── [both remediation agents complete and stop]
│
├── Phase 7: Cross-root conformity gate (Opus subagent)
│   ├── Assess first, write second
│   ├── Any write reopens affected root into local remediation
│   │   loop before publication
│   └── Phase 7 must PASS before any Phase 8 work
│
├── [human opens fresh publication sessions]
│
│   DEEPCUT PUBLICATION AGENT (Opus, fresh session)
│   ├── Adopts AGENT_DBM_PUBLISHER.md persona
│   └── Phase 8A: Normal DBM_PUBLISHER workflow for Deepcut
│
│   COMP & LIQUIDS PUBLICATION AGENT (Opus, fresh session)
│   ├── Adopts AGENT_DBM_PUBLISHER.md persona
│   └── Phase 8B: Normal DBM_PUBLISHER workflow for C&L
```

---

## Model Assignments

| Role | Model | Phases | Persona | Launched by |
|------|-------|--------|---------|-------------|
| Campaign controller | Opus | 1, 2, 7 | SCOPE_CHANGE | Human |
| Deepcut remediation agent | Opus | 3, 4 only | SCOPE_CHANGE | Human (new session) |
| Comp & Liquids remediation agent | Opus | 5, 6 only | SCOPE_CHANGE | Human (new session) |
| KTY-scoped task agents | Sonnet | Within 4 or 6 | Per skill | Root Opus agent |
| Cross-root conformity agent | Opus | 7 | Campaign assessor | Campaign controller |
| Deepcut publication agent | Opus | 8A only | DBM_PUBLISHER | Human (fresh session) |
| C&L publication agent | Opus | 8B only | DBM_PUBLISHER | Human (fresh session) |

---

## Ownership Boundaries

### Remediation root agents may

- Read the frozen source authority package (Process_DBM_fixed.md,
  metadata/tables.yaml, relevant data/*.csv)
- Read the frozen allocation matrix
- Write to their own root's decomposition, _ScopeChange, and KTY-local
  artifacts
- Write the approved handoff artifact (plans/Deepcut_Terminology_Decisions.md
  for Deepcut only)
- Launch Sonnet subagents for KTY-local tasks
- Emit handoff-state artifacts that identify accepted source snapshots,
  derivative-package status, closure verdict, and next-phase blockers

### Remediation root agents must NOT

- Edit the frozen source authority package
- Edit plans/Authority_Allocation_Matrix.csv
- Edit the other root's files
- Adopt DBM_PUBLISHER persona
- Begin any publication planning or execution
- Perform full-root tasks via Sonnet (see below)
- Treat derivative-package outputs as authoritative replacements for accepted
  `_ScopeChange` state

### Publication agents may

- Execute a normal DBM_PUBLISHER workflow within their root
- Read all campaign artifacts as provenance inputs

### Publication agents must NOT

- Modify decomposition truth (that was remediation work)
- Modify the other root's files

---

## Subagent Dispatch Rules

### Sonnet subagents (strictly KTY-local)

1. **One KTY per agent.** A Sonnet subagent handles exactly one KTY. No
   cross-KTY work.
2. **No decomposition writes.** Only the root Opus agent modifies decomposition
   truth.
3. **No cross-KTY writes.** A Sonnet agent scoped to KTY-04-09 does not touch
   KTY-04-10's artifacts.
4. **Explicit input/output contract:**
   - Input: KTY ID, folder path, specific task, relevant matrix slice, accepted
     terminology decisions (for C&L)
   - Output: files written/modified (paths), blocking issues found, pass/fail
     status

### Tasks that stay with Opus (not delegated to Sonnet)

- `TASK + decomposition-package-review` (full-root/package scope)
- DOMAIN_HYPERGRAPH (full-root scope)
- AUDIT_DECOMP (full-root scope)
- terminology QA / stale-term closure
- Cross-root conformity assessment
- Publication gating
- SCOPE_CHANGE gate decisions
- Any task spanning multiple KTYs

---

## Conditional Concurrency Rules

After Phases 1-2 are complete, the two remediation agents may run concurrently
under these constraints:

### Allowed in parallel

- DEEPCUT_ONLY matrix rows in the Deepcut root
- COMP_LIQ_ONLY matrix rows in the Comp & Liquids root
- KTY-local regeneration tasks that do not depend on shared terminology or
  shared-interface outcomes

### Not allowed in parallel (serialized)

- SHARED_INTERFACE work, unless the campaign controller explicitly clears a
  specific row for parallel treatment
- Any work that depends on Deepcut's terminology normalization decisions

### Deepcut remains first-pass normalization owner

- For shared terminology and shared-system wording
- Comp & Liquids may assess or prepare shared-interface work in parallel
- Comp & Liquids must NOT finalize conflicting shared terminology or
  shared-interface resolutions until:
  1. Deepcut's relevant terminology decisions are written
  2. The human has reviewed and accepted them

### Blocker protocol

If either root agent discovers a dependency or conflict:

1. Stop work on the affected scope unit
2. Record the blocker (what, why, which matrix row)
3. Escalate to the campaign controller
4. Continue with non-blocked root-local work

---

## Phase 7 Write Discipline

The cross-root conformity agent operates under this rule:

1. **Assess first.** Read both roots, the allocation matrix, and the
   terminology decisions file. Produce a conformity report for every
   SHARED_INTERFACE row.
2. **Write second.** Only after assessment is complete and the human has
   reviewed the conformity report.
3. **Any write reopens the affected root** into a local remediation loop. The
   write does not bypass root-agent ownership — it triggers a targeted fix
   (SCOPE_CHANGE or domain-documents rerun) within the affected root, and that
   root must pass local acceptance before publication proceeds.
4. **Report results to human** after each remediation cycle.

## Handoff-State Requirements

Every root handoff into Phase 7 must include an explicit handoff-state record.
At minimum it must state:

- accepted `_ScopeChange` snapshot path
- whether each required derivative package is `CURRENT`,
  `STALE_REBUILD_REQUIRED`, or `DEFERRED_BY_HUMAN`
- most recent `AUDIT_DECOMP` snapshot path and verdict
- closure verdict for the root: `READY_FOR_PHASE_7` or
  `OPEN_PENDING_DERIVATIVE_CLOSURE`
- remaining blockers and the next owning workflow

---

## Inter-Agent Handoff Protocol

### Deepcut to Comp & Liquids (plans/Deepcut_Terminology_Decisions.md)

Created by the Deepcut remediation agent after Phase 4. Structure:

```markdown
# Deepcut Terminology Decisions

## Campaign Reference
- Amendment: SCA-003
- Snapshot: {path}
- Date: {date}

## Normalized Shared Terms
| Term | Canonical Form | Prior Deepcut Form | Prior C&L Form | Matrix Row |
|------|---------------|-------------------|----------------|------------|

## SHARED_INTERFACE Resolution Summary
| AuthorityRef | Resolution | Deepcut Action | C&L Implication |
|-------------|-----------|----------------|-----------------|

## Open Issues Affecting Comp & Liquids
{list}
```

Human reviews this file before the Comp & Liquids agent reads it.

### Remediation agents to Phase 7

Both remediation agents produce handoff artifacts when they stop:

- Updated _ScopeChange/_LATEST.md in their root
- RUN_SUMMARY.md in their SCA-003 snapshot
- Handoff_State.md in their SCA-003 snapshot
- Confirmation that required derivative packages are current and AUDIT_DECOMP
  passes, or an explicit open-closure record if not

---

## Freeze Discipline

The following artifacts are frozen after Phase 2 and must not be edited by any
root agent:

- `domain-test/domains/West_Doe_Combined/_Sources/west_doe_process_design_basis_clean/`
  (entire package)
- `plans/Authority_Allocation_Matrix.csv`
- `domain-test/domains/West_Doe_Combined/_Sources/26020-04-PR-PDB-001 R0_IFD Uncontrolled 2026.04.16.pdf`

Only the campaign controller may amend frozen artifacts, and only if the
campaign is intentionally restarted.

---

## Root Agent Prompts

### Deepcut Remediation Agent (Phases 3-4 only)

The prompt must require the agent to:

1. Read `INIT.md` and `AGENTS.md`
2. Read `agents/AGENT_SCOPE_CHANGE.md` and adopt the SCOPE_CHANGE persona
3. Read `plans/WEST_DOE_TWO_ROOT_DBM_REMEDIATION_AND_PUBLICATION_PLAN.md` —
   focus on Phases 3 and 4
4. Read `plans/SCOPE_CHANGE_PRE_EXECUTION_ASSESSMENT.md`
5. Read `plans/WEST_DOE_EXECUTION_MODEL.md` — focus on ownership boundaries,
   subagent dispatch rules, conditional concurrency, and freeze discipline
6. Read the frozen allocation matrix: `plans/Authority_Allocation_Matrix.csv`
7. Read the cleaned source authority files:
   - `domain-test/domains/West_Doe_Combined/_Sources/west_doe_process_design_basis_clean/Process_DBM_fixed.md`
   - `domain-test/domains/West_Doe_Combined/_Sources/west_doe_process_design_basis_clean/metadata/tables.yaml`
   - Relevant `data/*.csv` files as needed during execution
8. Execute Phase 3 (SCOPE_CHANGE SCA-003 on Deepcut) with full 5-gate protocol
9. Execute Phase 4 (regenerate downstream) using Sonnet subagents for KTY-local
   `domain-documents` tasks only; then dispatch `TASK + kty-metadata-align`
   for each amended KTY as a separate root-agent-owned step; then run
   `TASK + decomposition-package-review` for the full root when
   decomposition-local truth changed materially; then run DOMAIN_HYPERGRAPH;
   then run AUDIT_DECOMP; then run terminology/stale-term closure and any
   targeted reruns; then record derivative-package closure status in
   handoff-state; keep multi-KTY tasks with the root Opus agent
10. Write `plans/Deepcut_Terminology_Decisions.md` after Phase 4
11. Stop after Phase 4. Do not begin any Phase 8 work or adopt DBM_PUBLISHER
    persona
12. Produce handoff artifacts for Phase 7, including derivative-package status
    and closure verdict

### Comp & Liquids Remediation Agent (Phases 5-6 only)

The prompt must require the agent to:

1. Read `INIT.md` and `AGENTS.md`
2. Read `agents/AGENT_SCOPE_CHANGE.md` and adopt the SCOPE_CHANGE persona
3. Read `plans/WEST_DOE_TWO_ROOT_DBM_REMEDIATION_AND_PUBLICATION_PLAN.md` —
   focus on Phases 5 and 6
4. Read `plans/SCOPE_CHANGE_PRE_EXECUTION_ASSESSMENT.md`
5. Read `plans/WEST_DOE_EXECUTION_MODEL.md` — focus on ownership boundaries,
   subagent dispatch rules, conditional concurrency, and freeze discipline
6. Read the frozen allocation matrix: `plans/Authority_Allocation_Matrix.csv`
7. Read the reviewed `plans/Deepcut_Terminology_Decisions.md`
8. Read the cleaned source authority files:
   - `domain-test/domains/West_Doe_Combined/_Sources/west_doe_process_design_basis_clean/Process_DBM_fixed.md`
   - `domain-test/domains/West_Doe_Combined/_Sources/west_doe_process_design_basis_clean/metadata/tables.yaml`
   - Relevant `data/*.csv` files as needed during execution
9. Execute Phase 5 (SCOPE_CHANGE SCA-003 on Comp & Liquids) with full 5-gate
   protocol
10. Execute Phase 6 (regenerate downstream) using Sonnet subagents for KTY-local
    `domain-documents` tasks only; then dispatch `TASK + kty-metadata-align`
    for each amended KTY as a separate root-agent-owned step; then run
    `TASK + decomposition-package-review` for the full root when
    decomposition-local truth changed materially; then run DOMAIN_HYPERGRAPH;
    then run AUDIT_DECOMP; then run terminology/stale-term closure and any
    targeted reruns; then record derivative-package closure status in
    handoff-state; keep multi-KTY tasks with the root Opus agent
11. Stop after Phase 6. Do not begin any Phase 8 work or adopt DBM_PUBLISHER
    persona
12. Produce handoff artifacts for Phase 7, including derivative-package status
    and closure verdict

### Publication Agents (Phase 8A / 8B — fresh sessions after Phase 7)

Each publication agent:

1. Reads `INIT.md`, `AGENTS.md`, `agents/AGENT_DBM_PUBLISHER.md`
2. Adopts the DBM_PUBLISHER persona
3. Executes a normal DBM_PUBLISHER workflow for its root
4. Uses remediated root state, the cleaned source authority package as
   provenance, and the allocation matrix as an optional planning aid
