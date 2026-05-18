# Dependencies

**Deliverable ID:** DEL-01-06
**Tracking Mode:** DECLARED (critical dependencies only)

## Upstream Dependencies (this deliverable depends on)

_No critical dependencies declared._

## Downstream Dependents (other deliverables depend on this)

_No critical dependents declared._

## Notes

Dependencies are human-curated. Only interface-critical dependencies are recorded here.

---

## Extracted Dependency Register

**Total ACTIVE rows:** 14
**ANCHOR rows:** 4 (1 IMPLEMENTS_NODE, 3 TRACES_TO_REQUIREMENT)
**EXECUTION rows:** 10 (4 PREREQUISITE, 3 INTERFACE, 1 HANDOVER, 2 PREREQUISITE-document)

| DependencyID | Class | AnchorType | Dir | Type | TargetType | Target | Status |
|---|---|---|---|---|---|---|---|
| DEP-0106-001 | ANCHOR | IMPLEMENTS_NODE | UPSTREAM | OTHER | WBS_NODE | PKG-001 | ACTIVE |
| DEP-0106-002 | ANCHOR | TRACES_TO_REQUIREMENT | UPSTREAM | OTHER | REQUIREMENT | SOW-0030 | ACTIVE |
| DEP-0106-003 | ANCHOR | TRACES_TO_REQUIREMENT | UPSTREAM | OTHER | REQUIREMENT | SOW-0031 | ACTIVE |
| DEP-0106-004 | ANCHOR | TRACES_TO_REQUIREMENT | UPSTREAM | OTHER | REQUIREMENT | OBJ-007 | ACTIVE |
| DEP-0106-005 | EXECUTION | N/A | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-01-05 (Schedule B) | ACTIVE |
| DEP-0106-006 | EXECUTION | N/A | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-01-03 (Bonding & Insurance) | ACTIVE |
| DEP-0106-007 | EXECUTION | N/A | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-01-04 (Schedule A) | ACTIVE |
| DEP-0106-008 | EXECUTION | N/A | UPSTREAM | PREREQUISITE | DOCUMENT | RFP Section 8.5 | ACTIVE |
| DEP-0106-009 | EXECUTION | N/A | UPSTREAM | PREREQUISITE | DOCUMENT | Addendum 03 | ACTIVE |
| DEP-0106-010 | EXECUTION | N/A | UPSTREAM | PREREQUISITE | DOCUMENT | Decomposition v2.3 (DEC-011/012/013) | ACTIVE |
| DEP-0106-011 | EXECUTION | N/A | UPSTREAM | INTERFACE | DOCUMENT | RFP Appendix H | ACTIVE |
| DEP-0106-012 | EXECUTION | N/A | DOWNSTREAM | HANDOVER | DELIVERABLE | DEL-01-02 (Submission Package) | ACTIVE |
| DEP-0106-013 | EXECUTION | N/A | UPSTREAM | INTERFACE | DELIVERABLE | DEL-01-04 (consistency) | ACTIVE |
| DEP-0106-014 | EXECUTION | N/A | UPSTREAM | INTERFACE | DELIVERABLE | DEL-01-05 (consistency) | ACTIVE |

---

## Lifecycle Summary

| Category | Count |
|---|---|
| ACTIVE | 14 |
| RETIRED | 0 |
| SatisfactionStatus: SATISFIED | 1 |
| SatisfactionStatus: PENDING | 6 |
| SatisfactionStatus: TBD | 7 |

---

## Run Notes

**Run Date:** 2026-02-17
**Mode:** UPDATE
**Strictness:** CONSERVATIVE
**Consumer Context:** NONE

**Defaults and paths used:**
- DECOMPOSITION_PATH: `/test/execution-6b/_Decomposition/Penhold_PSB_Project_Decomposition_v2.md` (v2.3 FINAL, located automatically)
- SOURCE_DOCS: AUTO -- scanned deliverable folder; identified Datasheet.md, Specification.md, Procedure.md, Guidance.md
- DOC_ROLE_MAP: DEFAULT heuristic applied
  - ANCHOR_DOC: `Datasheet.md` (contains identification, scope items, objective alignment)
  - EXECUTION_DOCS: `Procedure.md` (primary -- contains prerequisites P-01 through P-05 and workflow steps), `Specification.md` (secondary -- contains requirements R-01 through R-12), `Guidance.md` (tertiary -- contains principles and considerations)
- _REFERENCES.md: Read and used for cross-reference validation (DEL-01-03, DEL-01-04, DEL-01-05 confirmed)

**Warnings:** None.

**Extraction notes:**
- Pass 1 (ANCHOR): Extracted 1 parent anchor (IMPLEMENTS_NODE to PKG-001) and 3 trace anchors (SOW-0030, SOW-0031, OBJ-007). All identifiers confirmed against decomposition.
- Pass 2 (EXECUTION): Extracted 10 execution edges. Key findings:
  - DEL-01-05 (Schedule B) has an explicit 80% completion prerequisite before narrative authoring proceeds (Procedure P-02, Spec R-12).
  - DEL-01-03 (Bonding & Insurance) is a prerequisite for the insurance/bonding cost inclusion statement (Procedure P-05, Spec R-06).
  - DEL-01-04 (Schedule A) is both a prerequisite (P-05) and an ongoing consistency interface (R-08).
  - DEL-01-02 (Formal Submission Package) is the downstream consumer of the finalized narrative (Procedure Step 12).
  - Three document-level dependencies captured: RFP Section 8.5, Addendum 03, and Decomposition decisions.
  - Decomposition decision dependency (DEP-0106-010) marked SATISFIED -- all three decisions (DEC-011, DEC-012, DEC-013) are CLOSED.
  - RFP Appendix H captured as an interface (pricing template format).
- Design Lead availability (Procedure P-04) was considered but not extracted as a dependency because it represents coordination/availability rather than information/artifact transfer.
- Tax treatment (Datasheet attribute, Guidance CT-001) not extracted as a dependency -- it is an internal ambiguity for human ruling, not an information flow edge.
- "Owner Services & Utilities" exclusion (Guidance CT-002) not extracted -- pending human ruling on whether it is a formal exclusion or illustrative example.

---

## Run History

| Timestamp | Mode | Strictness | Decomposition | Warnings | ACTIVE Count |
|---|---|---|---|---|---|
| 2026-02-17 | UPDATE | CONSERVATIVE | Penhold_PSB_Project_Decomposition_v2.md (v2.3 FINAL) | None | 14 |
