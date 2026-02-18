# Dependencies: DEL-07-01 Design-Build Firm Experience Profile

## Dependency Tracking Mode
- **Mode:** TRACKED (upgraded from NOT_TRACKED by DEPENDENCIES agent run)
- **Notes:** Previous state was NOT_TRACKED (human-coordinated). This file now contains a machine-generated extracted register. Declared sections below remain human-owned.

---

## Declared Upstream Dependencies (human-owned)

- DEL-07-02 (Key Team Members and Resumes) — develop in parallel; firm experience must align with proposed team capabilities
- DEL-07-03 (Appendix I Subtrade and Consultant List) — develop in parallel; firm capabilities must align with subtrade structure
- DEL-01-01 (Compliance Matrix) — provides RFP requirements roadmap for firm experience content
- RFP Section 7.1.6 / Appendix A (OSR) — required before content can be drafted (currently TBD / PDF not accessible)
- Addendum 03 — scope clarifications affecting firm/team requirements

## Declared Downstream Dependencies (human-owned)

- DEL-01-02 (Final Submission Package) — receives final DEL-07-01 document for integration into proposal PDF

---

## Extracted Dependency Register

**Run date:** 2026-02-18
**ACTIVE rows:** 10
**RETIRED rows:** 0
**Total rows:** 10

### Summary Table

| DependencyID | Class | AnchorType | Direction | DependencyType | TargetType | TargetID / TargetName | Confidence | SatisfactionStatus |
|---|---|---|---|---|---|---|---|---|
| DEP-07-01-001 | ANCHOR | IMPLEMENTS_NODE | UPSTREAM | OTHER | WBS_NODE | PKG-03 | HIGH | TBD |
| DEP-07-01-002 | ANCHOR | TRACES_TO_REQUIREMENT | UPSTREAM | OTHER | REQUIREMENT | SOW-016 | HIGH | TBD |
| DEP-07-01-003 | ANCHOR | TRACES_TO_REQUIREMENT | UPSTREAM | OTHER | REQUIREMENT | OBJ-006 | HIGH | TBD |
| DEP-07-01-004 | EXECUTION | NOT_APPLICABLE | UPSTREAM | PREREQUISITE | DOCUMENT | RFP-2024_004 (§7.1.6) | HIGH | PENDING |
| DEP-07-01-005 | EXECUTION | NOT_APPLICABLE | UPSTREAM | PREREQUISITE | DOCUMENT | RFP-AppA-OSR | HIGH | PENDING |
| DEP-07-01-006 | EXECUTION | NOT_APPLICABLE | UPSTREAM | INTERFACE | DELIVERABLE | DEL-07-02 | HIGH | PENDING |
| DEP-07-01-007 | EXECUTION | NOT_APPLICABLE | UPSTREAM | INTERFACE | DELIVERABLE | DEL-07-03 | HIGH | PENDING |
| DEP-07-01-008 | EXECUTION | NOT_APPLICABLE | UPSTREAM | INTERFACE | DELIVERABLE | DEL-01-01 | MEDIUM | PENDING |
| DEP-07-01-009 | EXECUTION | NOT_APPLICABLE | DOWNSTREAM | HANDOVER | DELIVERABLE | DEL-01-02 | HIGH | PENDING |
| DEP-07-01-010 | EXECUTION | NOT_APPLICABLE | UPSTREAM | PREREQUISITE | DOCUMENT | ADD-03 | HIGH | PENDING |

---

## Run Notes

### Run Configuration
| Setting | Value |
|---|---|
| **Run date** | 2026-02-18 |
| **Mode** | UPDATE |
| **Strictness** | CONSERVATIVE |
| **Consumer context** | NONE |
| **Source docs** | AUTO (Datasheet.md, Specification.md, Guidance.md, Procedure.md, _CONTEXT.md, _REFERENCES.md, _SEMANTIC.md) |
| **Anchor doc** | Datasheet.md (contains WBS Ref, Primary Objective, Scope Item — highest-confidence anchor signals) |
| **Execution doc order** | Procedure.md (primary), Specification.md, Guidance.md, _CONTEXT.md |
| **Decomposition path** | /Users/ryan/ai-env/projects/chirality-app-test/test/execution-6c/_Decomposition/Penhold_PSB_Project_Decomposition_Final_AddendumIntegrated_v1.md |
| **Decomposition status** | FOUND — validation and label resolution performed |
| **_REFERENCES.md** | FOUND — used to resolve document target locations |

### Defaults Applied
- `SOURCE_DOCS`: AUTO — all non-dependency, non-generated files in deliverable folder scanned.
- `ANCHOR_DOC`: AUTO resolved to Datasheet.md (contains "Package", "Primary Objective", "Scope Item" fields — strongest anchor signals).
- `EXECUTION_DOC_ORDER`: AUTO resolved as Procedure.md, Specification.md, Guidance.md, _CONTEXT.md.
- `CONSUMER_CONTEXT`: NONE — extension columns (EstimateImpactClass, ConsumerHint) not populated.

### Anchor Validation Against Decomposition
- **PKG-03** confirmed: Decomposition §7 lists PKG-03 as "Team Qualifications (Appendix I + resumes)" with primary deliverables DEL-07-01, DEL-07-02, DEL-07-03.
- **DEL-07-01** confirmed: Decomposition §8 defines "DEL-07-01_DesignBuildFirmExperienceProfile".
- **SOW-016** confirmed: Decomposition §9 lists SOW-016 as "Provide Design-Build firm experience narrative (relevant projects; delivery credibility)"; Scope Ledger §10 maps SOW-016 to DEL-07-01 in PKG-03.
- **OBJ-006** confirmed: Decomposition §6 lists OBJ-006 as "Demonstrate a strong team & firms"; Scope Ledger §10 maps SOW-016 to OBJ-006.

### CONSERVATIVE Strictness Decisions
- **DEL-02-01 interface excluded:** Specification §Interface Requirements lists "DEL-02-01: Firm experience should demonstrate credibility for proposed concept approach" but marks it as ASSUMPTION. Under CONSERVATIVE strictness, no EXECUTION row emitted.
- **Guidance coordination statements excluded:** Multiple "coordinate with" / "develop in parallel" statements in Guidance and Procedure not converted to EXECUTION rows unless an explicit artifact transfer was stated.
- **_SEMANTIC.md excluded from extraction:** Contains semantic algebra matrices (analysis metadata), not source text with dependency cues.

### Warnings
- None. One ACTIVE parent anchor (IMPLEMENTS_NODE) found. No FLOATING_NODE or AMBIGUOUS_ANCHOR condition.

---

## Lifecycle Summary

| Dimension | Count |
|---|---|
| **ACTIVE rows** | 10 |
| **RETIRED rows** | 0 |
| **ANCHOR rows (ACTIVE)** | 3 |
| **EXECUTION rows (ACTIVE)** | 7 |
| **IMPLEMENTS_NODE anchors** | 1 |
| **TRACES_TO_REQUIREMENT anchors** | 2 |
| **SatisfactionStatus = TBD** | 3 |
| **SatisfactionStatus = PENDING** | 7 |
| **Confidence = HIGH** | 9 |
| **Confidence = MEDIUM** | 1 |

### Closure State Breakdown

| DependencyID | SatisfactionStatus | Notes |
|---|---|---|
| DEP-07-01-001 | TBD | Anchor to parent package — structural; closure not applicable in same sense |
| DEP-07-01-002 | TBD | Anchor to SOW-016 — structural traceability |
| DEP-07-01-003 | TBD | Anchor to OBJ-006 — structural traceability |
| DEP-07-01-004 | PENDING | RFP PDF not accessible at extraction time; execution blocked |
| DEP-07-01-005 | PENDING | OSR (RFP Appendix A) not accessible at extraction time; tailoring blocked |
| DEP-07-01-006 | PENDING | DEL-07-02 not yet complete; interface unresolved |
| DEP-07-01-007 | PENDING | DEL-07-03 not yet complete; interface unresolved |
| DEP-07-01-008 | PENDING | DEL-01-01 status unknown; compliance roadmap dependency |
| DEP-07-01-009 | PENDING | DEL-07-01 not yet complete; handover to DEL-01-02 not yet executed |
| DEP-07-01-010 | PENDING | Addendum 03 PDF not accessible at extraction time |

---

## Run History

| Run # | Date | Mode | Strictness | Decomposition Status | Warnings | ACTIVE Count | Notes |
|---|---|---|---|---|---|---|---|
| 1 | 2026-02-18 | UPDATE | CONSERVATIVE | FOUND | None | 10 | Initial DEPENDENCIES agent run; upgraded from NOT_TRACKED. Previous _DEPENDENCIES.md contained only placeholder text (no declared rows). |
