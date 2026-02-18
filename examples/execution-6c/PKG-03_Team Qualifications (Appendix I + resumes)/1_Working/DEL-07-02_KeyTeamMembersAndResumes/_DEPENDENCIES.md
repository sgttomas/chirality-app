# Dependencies: DEL-07-02 Key Team Members and Resumes

## Dependency Tracking Mode
- **Mode:** NOT_TRACKED (declared; original mode from source)
- **Notes:** See execution/_Coordination/_COORDINATION.md. Schedule-first coordination; dependencies coordinated externally by humans. This file now also contains a machine-tracked extracted register (DEPENDENCIES agent output) alongside the original declared sections.

---

## Upstream (I need these before I can proceed)
- Dependencies coordinated externally by humans.

## Downstream (These need me)
- Dependencies coordinated externally by humans.

---

## Extracted Dependency Register

**Total rows:** 7
**ACTIVE rows:** 7
**RETIRED rows:** 0

**Breakdown by class:**
- ANCHOR rows (ACTIVE): 3
- EXECUTION rows (ACTIVE): 4

**Breakdown by direction (ACTIVE):**
- UPSTREAM: 5 (3 ANCHOR + 2 EXECUTION)
- DOWNSTREAM: 2 (0 ANCHOR + 2 EXECUTION)

### Register Table

| DependencyID | Class | AnchorType | Direction | DependencyType | TargetType | TargetRefID / TargetDeliverableID | TargetName | Confidence | Status |
|---|---|---|---|---|---|---|---|---|---|
| DEP-07-02-001 | ANCHOR | IMPLEMENTS_NODE | UPSTREAM | OTHER | WBS_NODE | — | PKG-03 Team Qualifications (Appendix I + resumes) | HIGH | ACTIVE |
| DEP-07-02-002 | ANCHOR | TRACES_TO_REQUIREMENT | UPSTREAM | OTHER | REQUIREMENT | SOW-017 | SOW-017 Provide key member resumes and roles | HIGH | ACTIVE |
| DEP-07-02-003 | ANCHOR | TRACES_TO_REQUIREMENT | UPSTREAM | OTHER | REQUIREMENT | OBJ-006 | OBJ-006 Demonstrate a strong team & firms | HIGH | ACTIVE |
| DEP-07-02-004 | EXECUTION | NOT_APPLICABLE | UPSTREAM | INTERFACE | DELIVERABLE | DEL-07-01 | DEL-07-01 Design-Build Firm Experience Profile | HIGH | ACTIVE |
| DEP-07-02-005 | EXECUTION | NOT_APPLICABLE | DOWNSTREAM | HANDOVER | DELIVERABLE | DEL-07-03 | DEL-07-03 Appendix I Subtrade and Consultant List | HIGH | ACTIVE |
| DEP-07-02-006 | EXECUTION | NOT_APPLICABLE | UPSTREAM | INTERFACE | DELIVERABLE | DEL-08-01 | DEL-08-01 Detailed Project Schedule | HIGH | ACTIVE |
| DEP-07-02-007 | EXECUTION | NOT_APPLICABLE | DOWNSTREAM | HANDOVER | DELIVERABLE | DEL-01-02 | DEL-01-02 Formal Submission Package | HIGH | ACTIVE |

---

## Lifecycle Summary

| Lifecycle State | Count |
|---|---|
| ACTIVE | 7 |
| RETIRED | 0 |
| **Total** | **7** |

**Closure state (ACTIVE rows):**

| SatisfactionStatus | Count |
|---|---|
| TBD | 3 (ANCHOR rows) |
| PENDING | 4 (EXECUTION rows) |

---

## Run Notes

**Run date:** 2026-02-18
**Mode:** UPDATE
**Strictness:** CONSERVATIVE
**Consumer context:** NONE

**Source documents scanned (AUTO):**
- ANCHOR_DOC (auto-selected): `Datasheet.md` — matched heuristic `datasheet`
- EXECUTION_DOC_ORDER (auto-selected, in order):
  1. `Procedure.md` — matched heuristic `procedure`
  2. `Guidance.md` — matched heuristic `guidance`
  3. `Specification.md` — matched heuristic `spec`
  4. `_CONTEXT.md` — supplementary context
  5. `_REFERENCES.md` — supplementary references

**Decomposition path used:** `/Users/ryan/ai-env/projects/chirality-app-test/test/execution-6c/_Decomposition/Penhold_PSB_Project_Decomposition_Final_AddendumIntegrated_v1.md`
**Decomposition status:** FOUND and READ. Anchor validation performed. All target IDs confirmed in decomposition.

**_REFERENCES.md used:** Yes — read for document pointer resolution. References list RFP and Addendum 03 as external sources; no additional EXECUTION dependency rows were emitted solely from _REFERENCES.md entries.

**Defaults applied:**
- `SOURCE_DOCS`: AUTO
- `DOC_ROLE_MAP`: DEFAULT
- `ANCHOR_DOC`: AUTO (selected `Datasheet.md`)
- `EXECUTION_DOC_ORDER`: AUTO
- `CONSUMER_CONTEXT`: NONE (extension columns `EstimateImpactClass`/`ConsumerHint` not populated)

**Pass 1 (ANCHOR) notes:**
- Parent anchor (IMPLEMENTS_NODE) emitted for PKG-03. Confirmed in Decomposition Section 7 (PKG-03 definition) and Section 8 (DEL-07-02 entry).
- Two trace anchors emitted: SOW-017 and OBJ-006, both explicitly stated in Datasheet.md Section 1 and corroborated by Specification.md Section 5.4, Procedure.md Section 5.3, and Decomposition Sections 6 and 10.
- CONSERVATIVE strictness: no implicit anchors added.

**Pass 2 (EXECUTION) notes:**
- DEP-07-02-004 (UPSTREAM INTERFACE from DEL-07-01): Procedure Step 6.1 and Guidance Section 3.4 explicitly state project reference data must be received from DEL-07-01 for consistency of project names, dates, and scope descriptions. This is a specific data/artifact transfer requirement, not mere coordination.
- DEP-07-02-005 (DOWNSTREAM HANDOVER to DEL-07-03): Specification Section 4.3 and Procedure Step 6.2 explicitly state that all key members in DEL-07-02 must appear in Appendix I (DEL-07-03). The personnel roster artifact flows from DEL-07-02 to DEL-07-03.
- DEP-07-02-006 (UPSTREAM INTERFACE from DEL-08-01): Specification REQ-07-02-31 and Procedure Step 6.3 explicitly require availability statements in DEL-07-02 to be aligned against the detailed project schedule (DEL-08-01). Schedule data is a required input.
- DEP-07-02-007 (DOWNSTREAM HANDOVER to DEL-01-02): Specification Section 5.2 and Procedure Step 8 explicitly state the final PDF package is integrated into the master proposal PDF assembly (PKG-01 / DEL-01-02). This is a clear artifact handover.
- NOT extracted (low signal / out of scope):
  - Coordination notes between Proposal Manager and HR/Team Admin — no specific data/artifact transfer stated.
  - References to RFP sections — treated as DOCUMENT/EXTERNAL context, not dependency edges (no evidence of artifact receipt requirement from RFP to this deliverable beyond reading; RFP is a governing reference, not an information producer that hands off to this deliverable in a DAG sense).

**Quality checks passed:**
- [PASS] Required columns present; CSV parseable.
- [PASS] DependencyID unique within register (7 distinct IDs).
- [PASS] All ACTIVE rows contain EvidenceFile and SourceRef (no "location TBD" entries needed).
- [PASS] Status values canonical (ACTIVE / RETIRED).
- [PASS] SatisfactionStatus values canonical (TBD / PENDING).
- [PASS] _DEPENDENCIES.md counts consistent with Dependencies.csv (7 ACTIVE, 0 RETIRED).
- [PASS] No obvious duplicate rows.
- [PASS] Enum values are canonical write-form (no legacy INBOUND/OUTBOUND).
- [PASS] Non-deliverable targets (WBS_NODE, REQUIREMENT) have empty TargetDeliverableID; TargetRefID used instead.
- [PASS] Deliverable targets (DELIVERABLE) have TargetDeliverableID populated.

**Tree x DAG integrity:**
- [PASS] Exactly 1 ACTIVE IMPLEMENTS_NODE anchor found (DEP-07-02-001). No FLOATING_NODE or AMBIGUOUS_ANCHOR warnings required.

---

## Run History

| Run # | Date | Mode | Strictness | Decomposition Status | Warnings | ACTIVE Count |
|---|---|---|---|---|---|---|
| 1 | 2026-02-18 | UPDATE | CONSERVATIVE | FOUND (Penhold_PSB_Project_Decomposition_Final_AddendumIntegrated_v1.md) | None | 7 |
