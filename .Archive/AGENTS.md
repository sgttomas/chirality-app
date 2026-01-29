# AGENTS.md — How to use the agent framework in this repo

This file is the operator-facing index and “rules of the road” for using the agents shipped with this repository.

If you’re new, start with **CHIRALITY-APP** (the human guidance agent). It’s a workflow coach that helps you choose the right next step without violating scope boundaries.

---

## 1) The core model (the rules that keep the system coherent)

### Filesystem is the state
- Project “truth” is what is on disk: folders + `_STATUS.md` + the four documents.
- Agents must not maintain a hidden database or private state that diverges from the filesystem.

### Deliverables (working-items) are local
- A **deliverable** (`DEL-xx.yy`) is one folder under `/Users/ryan/ai-env/projects/chirality-app/test/execution/{PKG-ID}_{PkgLabel}/1_Working/{DEL-ID}_{DelLabel}/`.
- Work inside that folder is **local**: no cross-deliverable “crosstalk” by default.

### Local lifecycle (not stage gates)
Deliverables progress through a local lifecycle:

`OPEN → INITIALIZED → IN_PROGRESS → CHECKING → ISSUED`

- **Stage gates** (30/60/90/IFC, etc.) are *human-managed* milestones and are **not** lifecycle states.
- `_STATUS.md` is the authoritative lifecycle indicator.

### Coordination representation vs dependency tracking mode
The framework separates:
- **Coordination representation**: *how humans coordinate* (Schedule-first | Declared deps | Full graph)
- **Dependency tracking mode**: *how much dependency data is captured in-file* (`NOT_TRACKED` | `DECLARED` | `FULL_GRAPH`)

Rules of thumb:
- If `NOT_TRACKED`, do **not** compute or claim “blocked/unblocked” status.
- If `DECLARED`, only declared interface-critical edges may be used for advisory blocker reporting.
- If `FULL_GRAPH`, the graph is intended to be complete and acyclic (DAG).

### Cross-deliverable coherence is optional and human-triggered
- The only sanctioned cross-deliverable coherence mechanism is **RECONCILIATION**.
- RECONCILIATION is invoked by humans with explicit scope and a gate label; it is read-only.

---

## 2) Agent index (what each one is for)

> Filenames may include `_REVISED_..._v3` (or later). Treat the names below as *agent types*.

### CHIRALITY-APP (Human Guidance / Navigator)
- **What it does:** Helps the human choose the correct next step and avoid framework misuse.
- **What it does not do:** Draft engineering content; change `_STATUS.md`; scan cross-deliverable scope unless explicitly asked to run reconciliation.

File: `/Users/ryan/ai-env/projects/chirality-app/agents/AGENT_CHIRALITY-APP.md`

### ORCHESTRATOR (Workspace + visibility)
- **What it does:** Ingests the decomposition; records coordination representation + dependency mode; spawns bounded sub-agents; scans/reports status.
- **What it does not do:** Produce engineering content; assign work; decide stage gates or sequencing.

File: `/Users/ryan/ai-env/projects/chirality-app/agents/AGENT_INSTRUCTIONS_BUNDLE_2026-01-28_v3/AGENT_ORCHESTRATOR_REVISED_v3.md`

### PREPARATION (Scaffolding)
- **What it does:** Creates package/deliverable folders and writes the minimum viable fileset (`_CONTEXT.md`, `_DEPENDENCIES.md`, `_STATUS.md`, `_REFERENCES.md`) idempotently.
- **What it does not do:** Write engineering requirements/specs; infer dependencies.

File: `/Users/ryan/ai-env/projects/chirality-app/agents/AGENT_INSTRUCTIONS_BUNDLE_2026-01-28_v3/AGENT_PREPARATION_REVISED_v3.md`

### 4_DOCUMENTS (Initialize drafts)
- **What it does:** Generates initial drafts of `Datasheet.md`, `Specification.md`, `Guidance.md`, `Procedure.md` for one deliverable.
- **Status rule:** May set `_STATUS.md` from `OPEN → INITIALIZED` **only if the current state is `OPEN`** (no regression).
- **Epistemic rule:** No invention; cite what you can; otherwise mark TBD / ASSUMPTION.

File: `/Users/ryan/ai-env/projects/chirality-app/agents/AGENT_INSTRUCTIONS_BUNDLE_2026-01-28_v3/AGENT_4_DOCUMENTS_REVISED_v3.md`

### WORKING_ITEMS (Human-in-the-loop production)
- **What it does:** Runs a working session for **one** deliverable folder to iteratively produce a coherent set of all four documents.
- **Core rule:** The human engineer is the validator / halting condition.

File: `/Users/ryan/ai-env/projects/chirality-app/agents/AGENT_INSTRUCTIONS_BUNDLE_2026-01-28_v3/AGENT_WORKING_ITEMS_REVISED_v3.md`

### RECONCILIATION (Cross-deliverable coherence checks)
- **What it does:** Read-only scan across a human-defined scope to find terminology/parameter/assumption/interface mismatches; outputs a reconciliation report + conflict table.
- **What it does not do:** Modify deliverables; resolve conflicts without human rulings.

File: `/Users/ryan/ai-env/projects/chirality-app/agents/AGENT_INSTRUCTIONS_BUNDLE_2026-01-28_v3/AGENT_RECONCILIATION.md`

---

## 3) Who is allowed to write what (important)

| Agent | Writes files? | Allowed writes (high level) |
|---|---:|---|
| CHIRALITY-APP | No (by default) | Optional coaching note *only if explicitly requested by human* |
| ORCHESTRATOR | Yes | `test/execution/_Coordination/_COORDINATION.md`; reconciliation outputs folder; *spawns other agents for deliverable work* |
| PREPARATION | Yes | Package/deliverable folders; `_CONTEXT.md`, `_DEPENDENCIES.md`, `_STATUS.md` (=OPEN), `_REFERENCES.md` |
| 4_DOCUMENTS | Yes | Four docs; `_STATUS.md` update `OPEN→INITIALIZED` only if currently `OPEN` |
| WORKING_ITEMS | Yes (human-directed) | Updates four docs; may update `_STATUS.md` when the human decides |
| RECONCILIATION | Yes | Writes a report under `test/execution/_Reconciliation/` only (read-only deliverables) |

---

## 4) Project-specific conventions (from the decomposition)

### Filesystem-safe folder labels
Some package/deliverable names contain characters that cannot appear in folder names (example: `/`).

- Folder names use sanitized labels: `{PKG-ID}_{PkgLabel}` and `{DEL-ID}_{DelLabel}`.
- Canonical (unsanitized) names remain recorded exactly inside `_CONTEXT.md` for traceability.

### Objectives mapping may be package/range-based (best-effort)
If objectives are not listed per deliverable row:
- Use package-based association (mapping expressed as deliverable ranges grouped by package).
- Treat “best-effort” objective mapping as advisory and confirm priority with the human.

### Global boundaries matter
Before locking requirements, consult the decomposition’s:
- **Scope Focus / exclusions**
- **Decisions Captured**

These often encode responsibility splits (Employer vs Contractor) and interface boundaries.

### Baseline reference volumes
The decomposition references Employer's Requirements volumes (Vol 2 Part 1–3), located at `/Users/ryan/ai-env/projects/chirality-app/test/Volume_2_Part_{1,2,3}_Employers_Requirements.pdf`. If you don't have them yet:
- Index their expected location in package `0_References/_REFERENCE_INDEX.md` (or a similar index),
- Treat downstream requirements as **TBD** until the documents are provided.

---

## 5) Copy/paste runbooks (prompt templates)

### A) Kickoff (initialize workspace)
Use ORCHESTRATOR with the decomposition file path and explicitly confirm coordination representation + dependency mode.

**Prompt template:**
- "Run ORCHESTRATOR Function 1 (Initialize) using `/Users/ryan/ai-env/projects/chirality-app/test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md`. I want coordination representation = Schedule-first, dependency mode = NOT_TRACKED. Summarize what you ingest and show the gate question."

### B) Scaffold + initialize drafts
After initialization is confirmed:

**Prompt template:**
- “Run ORCHESTRATOR Function 2 (Scaffold), then initialize drafts with 4_DOCUMENTS for all deliverables. Report missing references.”

### C) Start work on one deliverable (WORKING_ITEMS)
**Prompt template:**
- “Start a WORKING_ITEMS session for DEL-XX.XX. Read `_CONTEXT.md`, `_REFERENCES.md`, and the deliverable entry in the decomposition. Then propose updated Datasheet/Specification/Guidance/Procedure with citations, marking TBD/ASSUMPTION as needed.”

### D) Scan & report status (what’s going on?)
**Prompt template:**
- “Run ORCHESTRATOR Scan & Report. Group deliverables by lifecycle state, and (only if dependency mode isn’t NOT_TRACKED) also show advisory blocked/unblocked based on declared dependencies.”

### E) Cross-deliverable reconciliation (human-triggered)
**Prompt template:**
- “Run RECONCILIATION for scope = PKG-08 and PKG-11 at gate label ‘30% Freeze’. Focus areas: interfaces, parameters, terminology, assumptions.”

---

## 6) Non-negotiable quality rules (how to avoid bad output)

- **No invention:** if it isn’t in a source, mark **TBD** or label **ASSUMPTION/PROPOSAL**.
- **Cite sources:** every non-trivial claim, requirement, or value should be traceable to a reference.
- **Conflict handling:** contradictions produce a **Conflict Table** and a request for a human ruling.
- **Keep scope clean:** WORKING_ITEMS stays inside one deliverable folder. Use RECONCILIATION for cross-deliverable checks.
- **Don’t confuse stage gates with lifecycle:** stage gates can be recorded in coordination notes, but `_STATUS.md` uses only the lifecycle states.

EOF