# AUDIT_DEPENDENCIES.md
**Dependency Register Coherence & Conformance Audit Rubric**  
**Canonical standards:**  
1) `AGENT_DEPENDENCIES.md` — defines the dependency extraction invariants and the canonical `Dependencies.csv` schema  
2) `Dependencies.csv` + `_DEPENDENCIES.md` artifacts in each deliverable folder (the objects being audited)

*Optional secondary reference:* `AGENT_RECONCILE_DEPENDENCIES.md` — defines how closure review consumes dependency fields.

---

## 0) How to use this rubric
Fill this rubric out **for every deliverable in scope** that is expected to have:
- `{deliverable}/Dependencies.csv` and/or
- `{deliverable}/_DEPENDENCIES.md`

### Marking scheme (use everywhere)
For each checklist item, mark one:
- ✅ **Conforms**
- ⚠️ **Partial** (mostly aligns; ambiguity/drift; low-risk)
- ❌ **Non‑conformant** (schema break, evidence missing, referential integrity break, unsafe drift)
- N/A **Not applicable** (deliverable not expected to have dependency artifacts)

### Evidence rule (mandatory)
For every ⚠️ or ❌:
- Provide **one short excerpt** (≤ 25 words) from the artifact and location:
  - `{deliverable}/Dependencies.csv — row/column}` or `{deliverable}/_DEPENDENCIES.md — section heading}`
- Provide the **canonical requirement** excerpt (≤ 25 words) and location:
  - `{AGENT_DEPENDENCIES.md — section heading}`
- Provide a **conformance fix** (specific edit instruction; minimal change preferred)
  - If the fix requires editing files, route it to **CHANGE (Type 1)**.

### Severity
Assign severity per issue:
- **Blocker:** breaks tooling/consumption, corrupts schema, missing essential evidence, or makes registers unusable
- **High:** causes incorrect dependency understanding, likely misroutes reconciliation work
- **Medium:** causes confusion / inconsistent formatting / increased cost
- **Low:** style/wording drift with minimal behavioral effect

---

## 1) Audit metadata
- Auditor:
- Date:
- Project / bundle:
- Canon file(s): `AGENT_DEPENDENCIES.md` (required)
- Scope (deliverables/packages/paths):
- Total deliverables audited:

---

## 2) Canon extraction (fill once)
After reading `AGENT_DEPENDENCIES.md`, summarize the required invariants and schemas.

### 2.1 Canonical artifacts
- Required artifact(s) per deliverable:
- Allowed write scope(s):
- Must-not-edit list (four deliverable docs, etc.):

### 2.2 Canonical schema (Dependencies.csv)
List the **required columns** and any required enums.

- Required columns:
- Required enums (if specified):
  - `Direction`:
  - `TargetType`:
  - `Origin`:
  - `Status`:
- Evidence requirements:
- Non-destructive update requirements:

### 2.3 Canonical glossary (terms that must not drift)
- Dependency:
- Declared vs Extracted:
- SourceRef / EvidenceFile:
- Status / SatisfactionStatus:

---

## 3) System-wide glossary mapping (cross-deliverable)
As you audit, record synonyms/drifts here so the patch plan can converge vocabulary.

| Canon term | Variant term found | Deliverable(s) | Drift type (synonym / meaning change) | Fix (rename / define / defer) |
|---|---|---|---|---|

---

# 4) Per-deliverable audit worksheet (copy/paste for EACH deliverable)

## 4.A Deliverable card
- Deliverable ID:
- Deliverable name:
- Path:
- Dependencies.csv present? (Y/N)
- _DEPENDENCIES.md present? (Y/N)
- Rows in Dependencies.csv (if present):
- Last updated timestamp (if available):

### 4.B Conformance summary (1–5 bullets)
- Overall status: **Conformant / Conformant with edits / Non‑conformant**
- Top 3 issues (IDs):
- Highest severity issue and why:
- Recommended action:
  - **Fix register**
  - **Re-run extraction (via ORCHESTRATOR → DEPENDENCIES)**
  - **Ignore / N/A**

---

## 4.C Checklist — Dependencies.csv schema and hygiene

### Schema presence (Blocker if missing and expected)
- [ ] ✅/⚠️/❌ Required columns exist (match canon)
- [ ] ✅/⚠️/❌ No unexpected breaking columns (extra columns allowed if non-breaking)
- [ ] ✅/⚠️/❌ CSV is parseable (consistent delimiter, header row, no obvious corruption)

### Identity / uniqueness
- [ ] ✅/⚠️/❌ `DependencyID` is present for every row
- [ ] ✅/⚠️/❌ `DependencyID` values are unique within the deliverable
- [ ] ✅/⚠️/❌ `FromDeliverableID` matches the deliverable’s identity (best-effort)

### Required content fields
- [ ] ✅/⚠️/❌ `Statement` present (or explicit `TBD` with rationale)
- [ ] ✅/⚠️/❌ `TargetType` present
- [ ] ✅/⚠️/❌ Direction present (`UPSTREAM`/`DOWNSTREAM` per canon)
- [ ] ✅/⚠️/❌ `Origin` present (`DECLARED` vs `EXTRACTED`)

### Evidence conformance (core)
- [ ] ✅/⚠️/❌ Every `Status=ACTIVE` row has `EvidenceFile` + `SourceRef` (or explicitly `location TBD`)
- [ ] ✅/⚠️/❌ `EvidenceQuote` length policy respected (if present)
- [ ] ✅/⚠️/❌ Unknown targets are not invented (UNKNOWN is allowed; raw text preserved)

### Status / lifecycle hygiene
- [ ] ✅/⚠️/❌ `FirstSeen` and `LastSeen` exist for extracted rows (if canon requires)
- [ ] ✅/⚠️/❌ `LastSeen` >= `FirstSeen` (when both exist)
- [ ] ✅/⚠️/❌ Unseen extracted rows are marked `RETIRED` (not deleted)
- [ ] ✅/⚠️/❌ Declared rows are not silently retired without explanation

---

## 4.D Checklist — _DEPENDENCIES.md structure and contract

### Human-owned declared sections preserved
- [ ] ✅/⚠️/❌ Declared upstream/downstream sections exist and are not renamed
- [ ] ✅/⚠️/❌ Extracted register section exists (if extraction is in use)
- [ ] ✅/⚠️/❌ Run Notes exist and record defaults/assumptions

### Coherence with CSV
- [ ] ✅/⚠️/❌ Counts in `_DEPENDENCIES.md` match (or explain drift from) `Dependencies.csv`
- [ ] ✅/⚠️/❌ Any tables in `_DEPENDENCIES.md` do not contradict the CSV

---

## 4.E Checklist — Referential integrity (cross-deliverable)

- [ ] ✅/⚠️/❌ Internal targets (`TargetType=DELIVERABLE`) refer to real deliverable IDs (best-effort check)
- [ ] ✅/⚠️/❌ Target deliverable references are consistent (`TargetDeliverableID`, `TargetName`)
- [ ] ✅/⚠️/❌ `TargetLocation` values are usable (or explicitly `TBD`)
- [ ] ✅/⚠️/❌ No obvious duplicate edges across deliverables (same From/To/Type/Statement) unless justified

---

## 4.F Checklist — Drift / invention detectors

- [ ] ✅/⚠️/❌ Dependency statements are traceable to the four documents via evidence fields
- [ ] ✅/⚠️/❌ Notes clearly distinguish FACT vs ASSUMPTION vs PROPOSAL (if used)
- [ ] ✅/⚠️/❌ Unknowns remain unknown (not “resolved” without evidence)

---

# 5) Issue log (system-wide)
Add one row per issue found (across all deliverables). Reuse IDs in worksheets.

| ID | Severity | Deliverable(s) | Type (Schema / Evidence / Integrity / Drift / Gap / Ambiguity) | Symptom | Evidence (≤25w + location) | Canon requirement (≤25w + location) | Fix (minimal edit) |
|---|---|---|---|---|---|---|---|

---

# 6) Patch plan (system-wide)
## 6.1 Prioritized edit sequence
1.
2.
3.

## 6.2 Remediation routing
For each fix, specify the correct owner:
- **CHANGE (Type 1)** — apply edits to registers/docs (approval-gated)
- **ORCHESTRATOR (Type 1)** — re-run extraction tasks (invokes DEPENDENCIES)
- **RECONCILIATION (Type 1)** — re-run audits/reviews and synthesize

## 6.3 Optional automation notes
If you see repeatable schema drift, propose:
- a lightweight validator,
- or a consistent “repair” routine (but do not implement it here).

---

# 7) Final coherence judgment
- Coherence score: High / Medium / Low
- Main risks if left unfixed:
- Expected behavior improvements after patch plan:
