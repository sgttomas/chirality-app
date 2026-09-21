# audit-governance — method

## Method

### Pass 0 — Preconditions

1. Validate the brief: confirm `EXECUTION_ROOT` and `GOVERNANCE_DOCS` are present and paths resolve.
2. Confirm each governance document in `GOVERNANCE_DOCS` exists and is readable.
3. Confirm `AGENT_DIR` exists and contains `AGENT_*.md` files.
4. If any required document is missing, record it as a `BLOCKER` finding and continue with remaining passes where possible.
5. Create the snapshot folder: `{EXECUTION_ROOT}/_Evaluation/GovernanceAudit/GovernanceAudit_{YYYY-MM-DD}_{HHmm}/`.

---

### Pass 1 — Count Integrity

Verify that counts cited in documents match actual counts.

**1a. K-* invariant count:**
- Count the number of K-* invariants defined in `CONTRACT.md` §1 (active invariants only; exclude §3 retired).
- Compare against any count cited in `INIT.md`, `AGENTS.md`, `DBM_Agent_Instruction_Architecture.md`, `README.md`, or other governance documents.
- Record each mismatch as an issue.

**1b. Agent count:**
- Count `AGENT_*.md` files in `AGENT_DIR` (excluding non-instruction files like templates).
- Count roles in `agents/registry.json` and compare the live entry doctrine and instruction files.
- Compare against any count cited in `INIT.md`, `README.md`, or other governance documents.
- Record each mismatch as an issue.

**1c. Tool count:**
- If `TOOL_REGISTRY` exists, count tools defined there.
- Compare against any count cited in `INIT.md`, `README.md`, or other governance documents.
- Record each mismatch as an issue.

---

### Pass 2 — Cross-Reference Resolution

Verify that document-internal and cross-document references resolve.

**2a. Section references:**
- Scan all governance documents for patterns: `§X`, `§X.Y`, `Section X`, `see §X`, `defined in DOCUMENT.md §X`.
- For each reference, verify the cited section exists in the target document.
- Record unresolvable references as issues.

**2b. Document references:**
- Scan for references to filenames (e.g., `CONTRACT.md`, `SPEC.md §6.5`, `TYPES.md §10`).
- Verify the referenced document exists.
- Where a specific section is cited, verify the section exists.
- Record unresolvable references as issues.

**2c. Content alignment (spot-check):**
- For references that include a description (e.g., "defined in TYPES.md §10, the Epistemic Ontology"), verify the cited section's heading or content matches the description.
- Record significant mismatches as issues.

---

### Pass 3 — Invariant ID Integrity

Verify that invariant IDs are consistent across the repo.

**3a. K-* invariants:**
- Build the canonical K-* ID set from `CONTRACT.md` §1.
- Scan all governance documents and agent instruction files for K-* ID references.
- Report any K-* ID cited outside `CONTRACT.md` that does not exist in the catalog.
- Record uncited K-* IDs as observations. Assess their significance against the governing contract rather than equating absence of citations with an invalid invariant.

**3b. R1–R17 requirements:**
- Build the canonical R-ID set from `docs/WORKFLOW_COMPONENT_STANDARD.md` under “Requirement identifier continuity”.
- Scan all governance documents for R-ID references.
- Report any R-ID cited that does not exist in the canonical set.
- Record uncited R-IDs as observations and assess their significance against the accepted requirement; an unused reference alone does not establish nonconformance.

**3c. I1–I10 invariants:**
- Build the canonical I-ID set from `docs/DECOMPOSITION_STANDARD.md`.
- Scan all governance documents for I-ID references.
- Report any I-ID cited that does not exist in the canonical set.
- Report any I-ID in the canonical set that is never cited outside the defining document (orphaned invariants).

---

### Pass 4 — Terminology Consistency

Verify that terms defined in `TYPES.md` are used consistently.

**4a. Canonical term extraction:**
- Extract defined terms from `TYPES.md`: entity names (Package, Deliverable, Artifact), enum values (lifecycle states, dependency classes, dependency types, target types, epistemic labels), ID formats, and agent role vocabulary.

**4b. Usage scan:**
- Scan governance documents for usage of canonical terms.
- Flag instances where a defined term appears to be used with a different meaning (semantic drift).
- Flag instances where a synonym or variant spelling is used instead of the canonical term (e.g., "phase" instead of "package", "subtask" instead of "deliverable").

**4c. Enum consistency:**
- For each enum defined in `TYPES.md`, verify that governance documents and agent instructions reference the same values.
- Report any enum value referenced that does not exist in the canonical set.

---

### Pass 5 — Agent Inventory Consistency

Verify that the agent inventory is synchronized across all tracking locations.

**5a. Filesystem vs. role registry:**
- List all `AGENT_*.md` files in `AGENT_DIR`.
- List all roles and instruction paths in `agents/registry.json`.
- Report any live role instruction missing from the registry.
- Report any registered instruction path without a corresponding file.

**5b. Competing agent index detection:**
- `agents/registry.json` is the machine-readable role inventory; AGENTS.md is the entry doctrine. Scan the other governance documents in scope (including `DBM_Agent_Instruction_Architecture.md`, `INIT.md`, `README.md`) for any agent index table or agent enumeration that duplicates the registry inventory.
- Report any such competing index as an issue, noting whether its membership or classifications diverge from the registry.
- Prose that names individual agents in context (e.g., dispatch relationships) is not a competing index; only enumerations presented as an inventory are.

**5c. Agent header validation:**
- For each role, read its type, instruction path, entry eligibility, delegation eligibility, and capability configuration from `agents/registry.json`.
- Compare against the role relationships in AGENTS.md and the four-section instructions.
- Report any mismatch in declared properties.

---

### Pass 6 — Document Hierarchy Coherence

Verify that the governance document hierarchy is internally coherent.

**6a. DIRECTIVE → CONTRACT alignment:**
- Verify that each principle in `DIRECTIVE.md` §2 is reflected in at least one K-* invariant in `CONTRACT.md`.
- Report any DIRECTIVE principle with no corresponding CONTRACT invariant.

**6b. SPEC ↔ role registry write_scope alignment:**
- Compare the role capability/write ceilings in agents/registry.json with the workflow output contracts and accepted brief targets in scope.
- Check that governed output roots have an explicit workflow owner and that each granted target fits the owning contract and outer runtime boundary.
- Report mismatched ownership, undeclared writes, or unsupported enforcement claims. Role prose is not a path registry; a valid brief may authorize bounded project paths outside named workflow output roots.

**6c. TYPES.md ↔ SPEC.md schema alignment:**
- Verify that enum values used in `SPEC.md` schemas (e.g., Dependencies.csv column enums) match the canonical values in `TYPES.md`.
- Report any discrepancy.

**6d. CONTRACT enforcement map:**
- Verify that every K-* invariant in `CONTRACT.md` §2 (Enforcement Map Summary) references invariants that exist in §1.
- Verify that every K-* invariant in §1 appears in at least one enforcement point in §2.

---

### Pass 7 — Claim Strength Calibration (K-CLAIM-1)

Verify that governance documents, agent instructions, and system-level documentation do not overstate what their warrant supports.

**7a. Universality and necessity claims:**
- Scan governance docs and thesis for statements of necessity ("the only way," "must take this form," "could not be absent," "deductively necessary") and verify that cited evidence supports that strength.
- Flag any universality claim where the evidence supports only an implementation-specific design or a local architectural choice.

**7b. Regulatory conclusiveness:**
- Scan for language that presents regulatory mappings as settled regulatory fact rather than firm interpretation.
- Flag any claim that a standard "applies directly" or "satisfies" requirements without qualification, where the evidence supports only an interpretive argument.

**7c. Scope drift:**
- Flag any claim where a conclusion established for a specific context (one jurisdiction, one project type, one decomposition variant) is stated as though it applies universally.

**7d. Mutable counts and provenance:**
- Flag hardcoded mutable counts in governance docs; verify mutable counts against live canonical sources (`AGENTS.md`, `workflows/`, and `tools/REGISTRY.md`).
- Flag provenance claims ("analysis of N files") that no longer match the governed suite.

Report findings as issue log entries with `IssueType: K-CLAIM-1` and Category `CLAIM_CALIBRATION` and severity `WARNING` for unsupported universality/necessity or scope drift; stale counts are `INFO` unless they materially misstate the governed contract, then `WARNING`.

---

### Synthesis and Output

1. Compile all findings into `Governance_Audit_Report.md`.
2. Compile the structured issue log into `Governance_Audit_IssueLog.csv`.
3. Generate the machine-readable summary `governance_audit_summary.json`.
4. Generate the self-assessment `QA_Report.md`.
5. Write the verbatim brief to `Brief.md`.
6. Update `_LATEST.md` pointer.
7. Return to the invoking manager: snapshot path, top issues (≤15), blockers, and recommended next action.

---
