# AUDIT_AGENT.md
**AGENT_* Coherence & Conformance Audit Rubric**  
**Canonical standard:** `AGENT_HELPS_HUMANS.md`. All other `AGENT_*.md` files must conform unless the canonical contains an internal contradiction that prevents system functionality (rare; minimal fix only).

---

## 0) How to use this rubric
Fill this rubric out **for every AGENT_*.md file** provided.

### Marking scheme (use everywhere)
For each checklist item, mark one:
- ✅ **Conforms** (matches v2 or correctly defers to it)
- ⚠️ **Partial** (mostly aligns; has ambiguity/drift; low-risk)
- ❌ **Non‑conformant** (contradiction, role drift, contract mismatch, safety/policy conflict)
- N/A **Not applicable** (frame not expected for this layer/file)

### Evidence rule (mandatory)
For every ⚠️ or ❌:
- Provide **one short excerpt** (≤ 25 words) from the file and location: `{filename — section heading}`  
- Provide the **canonical requirement** excerpt (≤ 25 words) and location: `{AGENT_HELPS_HUMANS — section heading}`  
- Provide a **conformance fix** (specific edit instruction; minimal change preferred)

### Severity
Assign severity per issue:
- **Blocker:** would cause unsafe behavior, permission misuse, persistent contradictions, or breaks the architecture boundaries
- **High:** changes outcomes or makes behavior unreliable
- **Medium:** causes confusion / inconsistent formatting / increased cost
- **Low:** style/wording drift with minimal behavioral effect

---

## 1) Audit metadata
- Auditor:
- Date:
- Bundle name / source:
- Canon file:
- Total files audited:

---

## 2) Canon extraction (v2 baseline)
Fill this once after reading v2.

### 2.1 Canonical role model (summary)
- Agent 0 / Type 0 (Architect) — primary responsibilities:
- Agent 1 / Type 1 (Manager) — primary responsibilities:
- Agent 2 / Type 2 (Specialist) — primary responsibilities:

### 2.2 Canonical contracts (must list)
List the **minimum required contracts** v2 defines that other files must respect.
- Brief schema requirements:
- Output schema requirements:
- Provenance / evidence requirements:
- QA gates / review requirements:
- Decision-rights / escalation rules:
- Tool/write quarantine rules (if any):
- Versioning/deprecation expectations (if any):

### 2.3 Canonical glossary (terms that must not drift)
List key terms and their canonical meaning in v2.
- Term:
- Term:
- Term:

---

## 3) System-wide glossary mapping (cross-file)
As you audit, record synonyms/drifts here so the patch plan can converge vocabulary.

| Canon term (v2) | Variant term found | File(s) | Drift type (synonym / meaning change) | Fix (rename / define / defer) |
|---|---|---|---|---|

---

# 4) Per-file audit worksheet (copy/paste this section for EACH file)

## 4.A File card
- File name:
- Claimed role (if stated):
- **Assigned role (auditor):** Agent 0 / Agent 1 / Agent 2 / Other
- Purpose (1 sentence):
- Depends on (other agents/contracts/tools):
- Produces (artifacts/outputs):
- Primary user interaction? (Yes/No; how?)

### 4.B Conformance summary (1–5 bullets)
- Overall status: **Conformant / Conformant with edits / Non‑conformant**
- Top 3 issues (IDs):
- Highest severity issue and why:
- Recommended action: **Edit to conform / Deprecate / Merge / Split into layer-specific files**

---

## 4.C Layer checklist selection
✅ Fill **ONLY ONE** checklist below as the “primary checklist” based on Assigned role.  
Then also fill the **Role Drift Detectors** (section 4.G) no matter what.

- [ ] Agent 0 / Type 0 checklist (Architect)
- [ ] Agent 1 / Type 1 checklist (Manager)
- [ ] Agent 2 / Type 2 checklist (Specialist)

---

# 4.D Agent 0 / Type 0 Checklist (Architect)
> Use this checklist if this file is intended to be **canonical/constitutional** (defines roles, contracts, values, permissions, interfaces).

## Ontology (what exists)
- [ ] ✅/⚠️/❌ Defines canonical entities (agents, roles, artifacts, states) **consistent with v2**
- [ ] ✅/⚠️/❌ Defines boundaries between Agent 0/1/2 (what each can/can’t do)
- [ ] ✅/⚠️/❌ Avoids runtime task execution steps (Architect should not “do the work”)
Notes / evidence / fix:

## Axiology (what matters)
- [ ] ✅/⚠️/❌ Defines explicit value hierarchy / trade-off policy consistent with v2
- [ ] ✅/⚠️/❌ Defines quality bar and what is allowed to be “good enough”
Notes / evidence / fix:

## Teleology (ends/success criteria)
- [ ] ✅/⚠️/❌ Defines “definition of done” and stopping rules consistent with v2
- [ ] ✅/⚠️/❌ Defines acceptance criteria templates (not execution plans)
Notes / evidence / fix:

## Deontology (must/must-not; authority)
- [ ] ✅/⚠️/❌ Defines “must/never” rules and **precedence order** (what wins on conflict)
- [ ] ✅/⚠️/❌ Defines escalation/decision-rights map consistent with v2
Notes / evidence / fix:

## Epistemology (how we know)
- [ ] ✅/⚠️/❌ Defines evidence standards (citations, verification levels, uncertainty reporting)
- [ ] ✅/⚠️/❌ Defines acceptable sources/tools (policy-level)
Notes / evidence / fix:

## Methodology (process architecture)
- [ ] ✅/⚠️/❌ Defines canonical workflow patterns (fan-out/fan-in, gating, brief-first)
- [ ] ✅/⚠️/❌ Does **not** contain detailed per-task SOPs that belong in Specialists
Notes / evidence / fix:

## Cybernetics (feedback & control)
- [ ] ✅/⚠️/❌ Defines QA gates, error taxonomy, retry/escalation policy
- [ ] ✅/⚠️/❌ Defines observability expectations (what gets reported upstream)
Notes / evidence / fix:

## Hermeneutics (interpretation policy)
- [ ] ✅/⚠️/❌ Defines ambiguity-handling rules (when to ask vs proceed)
- [ ] ✅/⚠️/❌ Defines intent-parsing policy (policy-level, not conversation tactics)
Notes / evidence / fix:

## Semiotics (language discipline)
- [ ] ✅/⚠️/❌ Defines canonical glossary / naming conventions
- [ ] ✅/⚠️/❌ Prevents synonym drift (requires deference to canonical terms)
Notes / evidence / fix:

## Interface / Contract theory (layer interfaces)
- [ ] ✅/⚠️/❌ Defines brief schema + output schema + invariants + versioning
- [ ] ✅/⚠️/❌ Defines compatibility/backward-compat expectations
Notes / evidence / fix:

## Systems engineering (non-functional requirements)
- [ ] ✅/⚠️/❌ Defines NFR targets (reliability, latency, cost, maintainability)
- [ ] ✅/⚠️/❌ Provides guidance for trade-offs consistent with axiology
Notes / evidence / fix:

## Governance (stewardship)
- [ ] ✅/⚠️/❌ Defines ownership, change control, deprecation, review cadence
- [ ] ✅/⚠️/❌ Defines how lower layers propose changes (not edit canon)
Notes / evidence / fix:

## Security & privacy (threat model)
- [ ] ✅/⚠️/❌ Defines data-handling, least privilege, redaction/logging constraints
- [ ] ✅/⚠️/❌ Prevents unsafe tool/data flows
Notes / evidence / fix:

## Human factors (ergonomics)
- [ ] ✅/⚠️/❌ Defines handoff clarity standards (brief quality, user cognitive load)
- [ ] ✅/⚠️/❌ Defines trust calibration norms (confidence, uncertainty)
Notes / evidence / fix:

## Rhetoric (tone as mechanism)
- [ ] ✅/⚠️/❌ Defines style constraints by layer (Architect voice vs Manager vs Specialist)
- [ ] ✅/⚠️/❌ Style rules support the axiology and epistemology (no misleading certainty)
Notes / evidence / fix:

---

# 4.E Agent 1 / Type 1 Checklist (Manager)
> Use this checklist if the file **orchestrates**: decomposes work, writes briefs, routes to specialists, merges, and gates quality.

## Ontology (mapping intent to system model)
- [ ] ✅/⚠️/❌ Uses v2 canonical roles/entities; does not redefine them
- [ ] ✅/⚠️/❌ Correctly maps user requests → task graph → specialists
Notes / evidence / fix:

## Hermeneutics (primary interpreter)
- [ ] ✅/⚠️/❌ Has explicit ambiguity-handling (ask vs assume) consistent with v2
- [ ] ✅/⚠️/❌ Converts intent into **briefs**, not direct execution
Notes / evidence / fix:

## Methodology (planning & fan-out/fan-in)
- [ ] ✅/⚠️/❌ Uses fan-out/fan-in patterns where appropriate
- [ ] ✅/⚠️/❌ Includes review gates/checkpoints before final synthesis
Notes / evidence / fix:

## Interface / Contract theory (briefing & validation)
- [ ] ✅/⚠️/❌ Produces briefs that match v2 schema (inputs, constraints, outputs, acceptance)
- [ ] ✅/⚠️/❌ Validates Specialist outputs against schema; rejects/requests fixes
Notes / evidence / fix:

## Cybernetics (control loops)
- [ ] ✅/⚠️/❌ Defines QA steps, retries, escalation triggers consistent with v2
- [ ] ✅/⚠️/❌ Monitors for drift/inconsistency; consolidates conflicts deterministically
Notes / evidence / fix:

## Epistemology (evidence integration)
- [ ] ✅/⚠️/❌ Enforces evidence standards (citations, verification level) per v2
- [ ] ✅/⚠️/❌ Reconciles conflicting evidence and reports uncertainty
Notes / evidence / fix:

## Axiology + Teleology (value + success enforcement)
- [ ] ✅/⚠️/❌ Chooses plans aligned with v2 priorities/trade-offs
- [ ] ✅/⚠️/❌ Uses clear acceptance criteria / DoD and knows when to stop
Notes / evidence / fix:

## Deontology + Security/Privacy (policy enforcement)
- [ ] ✅/⚠️/❌ Blocks disallowed actions; escalates decisions correctly
- [ ] ✅/⚠️/❌ Routes data/tools safely; applies redaction/least privilege
Notes / evidence / fix:

## Semiotics (language alignment)
- [ ] ✅/⚠️/❌ Uses canonical terminology in briefs and synthesis
- [ ] ✅/⚠️/❌ Prevents synonym drift across specialists
Notes / evidence / fix:

## Systems engineering (NFR-aware orchestration)
- [ ] ✅/⚠️/❌ Makes cost/latency/reliability trade-offs consistent with v2
- [ ] ✅/⚠️/❌ Avoids over-fanout or over-context that violates budgets
Notes / evidence / fix:

## Governance (change reporting)
- [ ] ✅/⚠️/❌ Does not edit canon; reports needed changes upward
- [ ] ✅/⚠️/❌ Maintains clear version references when using contracts
Notes / evidence / fix:

## Human factors + Rhetoric (user interface)
- [ ] ✅/⚠️/❌ Communicates plan/assumptions/risks clearly
- [ ] ✅/⚠️/❌ Calibrates confidence; avoids misleading certainty
Notes / evidence / fix:

---

# 4.F Agent 2 / Type 2 Checklist (Specialist)
> Use this checklist if the file **executes** a narrow task domain under a brief, returns outputs + evidence, and stays stateless.

## Praxeology (execution)
- [ ] ✅/⚠️/❌ Narrow scope: “do one type of thing really well”
- [ ] ✅/⚠️/❌ Executes only what’s in the brief; avoids orchestration behavior
Notes / evidence / fix:

## Interface / Contract theory (follow the brief; output to spec)
- [ ] ✅/⚠️/❌ Input expectations match v2 brief schema (doesn’t demand extra hidden context)
- [ ] ✅/⚠️/❌ Output format matches v2 schema (structured, checkable, acceptance-ready)
Notes / evidence / fix:

## Epistemology (evidence & verification)
- [ ] ✅/⚠️/❌ Provides evidence/citations/verification per v2 standards
- [ ] ✅/⚠️/❌ Reports uncertainty and failure modes transparently
Notes / evidence / fix:

## Cybernetics (self-check + error reporting)
- [ ] ✅/⚠️/❌ Includes local self-checks and quality validation
- [ ] ✅/⚠️/❌ Emits clear error states (can’t comply / missing input / conflict) to Manager
Notes / evidence / fix:

## Methodology (SOP inside the task)
- [ ] ✅/⚠️/❌ Has repeatable steps for its domain (within brief scope)
- [ ] ✅/⚠️/❌ Avoids adding global workflow rules (belongs to Agent 0/1)
Notes / evidence / fix:

## Deontology + Security/Privacy (strict compliance)
- [ ] ✅/⚠️/❌ Does not introduce new global prohibitions/permissions; defers to v2
- [ ] ✅/⚠️/❌ Handles data safely (redaction, least privilege, no oversharing)
Notes / evidence / fix:

## Semiotics (terminology discipline)
- [ ] ✅/⚠️/❌ Uses canonical terms; avoids synonyms that change meaning
Notes / evidence / fix:

## Human factors + Rhetoric (deliverable clarity)
- [ ] ✅/⚠️/❌ Output is readable and action-ready for Manager/user
- [ ] ✅/⚠️/❌ Tone is appropriate and non-deceptive
Notes / evidence / fix:

---

# 4.G Role Drift Detectors (fill for EVERY file)
> These detect whether the file is “doing the wrong layer’s thinking.”

Mark each item and add notes/evidence if ⚠️ or ❌.

## Architect drift (Agent 0 doing execution)
- [ ] ✅/⚠️/❌ Contains tool-level step-by-step execution or domain SOPs that belong in Specialists
Notes / evidence / fix:

## Manager drift (Agent 1 collapsing into Specialist)
- [ ] ✅/⚠️/❌ Performs significant execution instead of briefing/routing/synthesizing
Notes / evidence / fix:

## Specialist drift (Agent 2 becoming Manager/Architect)
- [ ] ✅/⚠️/❌ Introduces global policies/values/contracts or orchestrates other agents
Notes / evidence / fix:

## Contract drift
- [ ] ✅/⚠️/❌ Uses a different brief/output schema than v2
Notes / evidence / fix:

## Terminology drift
- [ ] ✅/⚠️/❌ Redefines canonical terms or introduces conflicting synonyms
Notes / evidence / fix:

---

# 5) Issue log (system-wide)
Add one row per issue found (across all files). Reuse IDs in file worksheets.

| ID | Severity | File(s) | Type (Non-conformance / Drift / Gap / Redundancy / Ambiguity) | Symptom (behavior) | Evidence (≤25w + location) | Canon requirement (≤25w + v2 location) | Fix (minimal edit) |
|---|---|---|---|---|---|---|---|

---

# 6) Patch plan (system-wide)
## 6.1 Prioritized edit sequence
1.
2.
3.

## 6.2 Consolidation plan (single source of truth)
- Rules to centralize in v2 (if missing/unclear in v2):
- Rules to delete from other files and replace with reference to v2:
- Files to split/merge due to role confusion:

## 6.3 Optional patches
For each file with recommended edits, provide either:
- `unified diff` patch, or
- `BEGIN REWRITE / END REWRITE` for specific sections

---

## 7) Final coherence judgment
- Coherence score: High / Medium / Low
- Main risks if left unfixed:
- Expected behavior improvements after patch plan:
- Any required minimal fix to v2 itself (only if internally contradictory):
