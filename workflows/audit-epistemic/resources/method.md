# audit-epistemic — method

## Method

### Pass 0 — Preconditions and scope resolution

1) Resolve `EXECUTION_ROOT` (default `execution/`).
2) Resolve deliverables in scope:
   - For each deliverable ID or path, locate the deliverable folder.
   - Resolve `LEGACY_FOUR_DOC | SOW_V1 | MIGRATION_DUAL | AMBIGUOUS | INVALID`;
     accept dual only when the brief cites exact path-scoped migration authority.
   - Check for Dependencies.csv if `INCLUDE_DEPENDENCIES_CSV=true`.
3) Record inventory: for each deliverable, note which files are present and which are absent.
4) If zero deliverables resolve: write `Brief.md` with `RUN_STATUS = FAILED_INPUTS` and stop.
5) If no recognized production contract exists: record `NOT_INITIALIZED` and
   skip. Record partial or unauthorized mixed formats as `INVALID` and stop
   that deliverable's audit.

---

### Pass 1 — Epistemic label coverage scan

For each production source: the four files in legacy mode, or each registered
claim and substantive prose block in validated `ScopeOfWork.md` under the
accepted SOW/authorized migration basis:

1) Identify **non-trivial claims** — assertions about parameters, requirements, constraints, acceptance criteria, design choices, scope boundaries, or technical values. Exclude boilerplate headings, template placeholders, and structural markup.
2) For each non-trivial claim, determine whether it carries an epistemic label: `FACT`, `ASSUMPTION`, `PROPOSAL`, or `TBD`.
3) Compute **label coverage** = (claims with explicit labels) / (total non-trivial claims identified).
4) Record per-document and per-deliverable coverage rates.

When `AUDIT_DEPTH=STANDARD`:
- Focus on structurally marked claims (inline labels, tagged values, Notes fields with epistemic markers).

When `AUDIT_DEPTH=DEEP`:
- Additionally scan prose paragraphs for unlabeled assertions that appear to make factual or technical claims without epistemic marking.

---

### Pass 2 — Provenance verification

For each claim with an epistemic label:

1) **FACT claims:** Verify that a source citation exists (file path + section reference, or equivalent provenance pointer). If no citation is found, record a `MISSING_PROVENANCE` finding (K-PROV-1 violation).
2) **ASSUMPTION claims:** Verify that the assumption is documented — either inline or in a referenced assumptions register. If undocumented, record `UNDOCUMENTED_ASSUMPTION`.
3) **PROPOSAL claims:** Verify that the proposal is clearly marked as requiring human decision. If it could be mistaken for a decided fact, record `AMBIGUOUS_PROPOSAL`.
4) **TBD claims:** Verify that the TBD is actionable — does it identify what is unknown and what resolution is needed? If it is a bare placeholder with no context, record `BARE_TBD`.

Compute **provenance completeness** = (FACT claims with valid citations + ASSUMPTION claims with documentation) / (total FACT + ASSUMPTION claims).

---

### Pass 3 — Gap detection

Scan all documents for:

1) **Explicit gaps:** TBD markers, `location TBD` provenance entries, placeholder values (e.g., `[TBD]`, `TBC`, `TBA`, `N/A — pending`, `to be determined`).
2) **Potential unwarranted claims:** Values, parameters, or assertions that:
   - Lack both a source citation and a TBD marker,
   - Are not labeled as ASSUMPTION or PROPOSAL,
   - Appear to state specific technical content (numeric values, material selections, code/standard references, design parameters).

For each potential unwarranted claim, record:
- The claim text and location,
- Why it appears unwarranted (no label, no citation, no TBD),
- Severity: `WARNING` if the claim is a specific technical value; `INFO` if it is a general statement.

Compute **gap count** = total explicit TBD markers + potential unwarranted claims.

---

### Pass 4 — Conflict detection

In legacy mode, compare key parameters, requirements, and constraints **across
documents within the deliverable**. In SOW mode, perform the same checks
across registered claims and the Ontology, Epistemology, Praxeology, and
Axiology sections:

1) Extract key-value assertions from each document (parameters, limits, acceptance criteria, scope statements, material/code references).
2) For each key that appears in multiple documents, compare values.
3) If values differ, record a `CONFLICT` finding with:
   - The conflicting key,
   - The value in each document (with file + section),
   - Whether a Conflict Table entry already exists for this key.
4) If a conflict is found that has NOT been recorded in a Conflict Table or a
registered `CON-*` entry, flag as `UNRECORDED_CONFLICT` (K-CONFLICT-1
violation).

Compute **conflict count** = total parameter/value conflicts detected.

---

### Pass 5 — Warrant lifecycle assessment

For each claim identified in Passes 1-3, classify its warrant state per `TYPES.md` §10.4:

| Warrant State | Criteria |
|---|---|
| `UNWARRANTED` | Claim exists but has no source citation; status is TBD or PROPOSAL (or unlabeled) |
| `CITED` | Claim has a source citation; status is FACT or ASSUMPTION |
| `REVIEWED` | Claim has been examined by a professional (evidence of review disposition in _STATUS.md or review records) |
| `AUTHENTICATED` | Claim is part of an issued deliverable with SHA-bound approval |

Produce a **warrant state distribution** for the deliverable:
- Count and percentage of claims in each warrant state.
- Identify claims in critical sections (acceptance criteria, safety requirements, scope boundaries) that remain UNWARRANTED.

---

### Pass 6 — Cross-document consistency

In legacy mode, compare across the four document kit files for:

1) **Scope boundaries:** Do Datasheet, Specification, Guidance, and Procedure agree on what is in scope and what is excluded?
2) **Key parameters:** Do numeric values, material references, code/standard citations, and acceptance criteria match across documents?
3) **Acceptance criteria:** Are the acceptance criteria in Specification.md reflected in the verification steps in Procedure.md?
4) **Design intent alignment:** Does the rationale in Guidance.md align with the requirements in Specification.md?

Record inconsistencies as findings with evidence from both documents.

For `SOW_V1` or an authorized migration-dual candidate, replace this pass with cross-section
and reference-graph consistency: unique registered IDs; resolved compound
references; output-to-objective coverage; requirement/claim-to-criterion
coverage; criterion-to-verification coverage; source/warrant coverage; and
contradictions among Ontology, Epistemology, Praxeology, and Axiology sections.
WORKING_ITEMS (workflow: review)'s `AC-*` namespace is the same SOW acceptance-criterion registry,
not a parallel audit-generated namespace.

---

### Pass 7 — Dependencies.csv provenance audit

If `INCLUDE_DEPENDENCIES_CSV=true` and Dependencies.csv exists:

1) For each row where `Status = ACTIVE`:
   - Check `EvidenceFile` is present and non-empty (not `location TBD`).
   - Check `SourceRef` is present and non-empty (not `location TBD`).
2) Compute **dependency provenance completeness** = (ACTIVE rows with both EvidenceFile AND SourceRef present and not `location TBD`) / (total ACTIVE rows).
3) For rows missing provenance, record `DEP_MISSING_PROVENANCE` findings with the `DependencyID` and `Statement`.
4) Check `Notes` field for epistemic labels (FACT, ASSUMPTION, PROPOSAL) where present.

---

### Pass 8 — Publish snapshot and return summary

1) Compile all findings into the output artifacts:
   - `Epistemic_Audit_Report.md` — narrative report organized by pass, with warrant state summary.
   - `Epistemic_Audit_IssueLog.csv` — structured issue log.
   - `epistemic_audit_summary.json` — machine-readable metrics.
   - `QA_Report.md` — self-assessment.
2) Write all artifacts into the snapshot folder.
3) Update `_LATEST.md` pointer.
4) Return to the invoking manager:
   - Snapshot path,
   - Aggregate metrics (label coverage %, provenance completeness %, gap count, conflict count),
   - Top issues (up to 10),
   - Warrant state distribution,
   - Recommended next action (e.g., add epistemic labels, attach provenance, resolve conflicts, schedule review).

---
