# DEL-014-02_Septic Dependencies

## Dependency Status
**Tracking**: ACTIVE
**Register**: Dependencies.csv (v3.1)

## Upstream Dependencies (Declared)
- Site preparation and soil assessment (external)
- Environmental compliance verification (external)

## Downstream Dependencies (Declared)
- DEL-014-04: Floor Drains & Sump Drains (drainage integration)
- DEL-014-06: Plumbing Fixtures (fixture installation feeds septic)

## Notes
Detailed dependency tracking managed within project execution framework.

---

## Extracted Dependency Register

**Total ACTIVE rows:** 13
**ANCHOR rows:** 3 (1 IMPLEMENTS_NODE, 2 TRACES_TO_REQUIREMENT)
**EXECUTION rows:** 10

| DependencyID | Class | AnchorType | Dir | Type | TargetType | Target | Confidence | Status |
|---|---|---|---|---|---|---|---|---|
| DEP-014-02-001 | ANCHOR | IMPLEMENTS_NODE | UPSTREAM | OTHER | WBS_NODE | SOW-0043 | HIGH | ACTIVE |
| DEP-014-02-002 | ANCHOR | TRACES_TO_REQUIREMENT | UPSTREAM | OTHER | REQUIREMENT | OBJ-001 | HIGH | ACTIVE |
| DEP-014-02-003 | ANCHOR | TRACES_TO_REQUIREMENT | UPSTREAM | OTHER | REQUIREMENT | OBJ-004 | HIGH | ACTIVE |
| DEP-014-02-004 | EXECUTION | N/A | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-006-05 (Septic System Details) | HIGH | ACTIVE |
| DEP-014-02-005 | EXECUTION | N/A | UPSTREAM | INTERFACE | DELIVERABLE | DEL-006-03 (Drain and Vent Plans) | HIGH | ACTIVE |
| DEP-014-02-006 | EXECUTION | N/A | DOWNSTREAM | INTERFACE | DELIVERABLE | DEL-014-04 (Floor Drains and Sump Drains) | HIGH | ACTIVE |
| DEP-014-02-007 | EXECUTION | N/A | DOWNSTREAM | INTERFACE | DELIVERABLE | DEL-014-06 (Plumbing Fixtures) | HIGH | ACTIVE |
| DEP-014-02-008 | EXECUTION | N/A | UPSTREAM | PREREQUISITE | DOCUMENT | Geotechnical Investigation Report | HIGH | ACTIVE |
| DEP-014-02-009 | EXECUTION | N/A | UPSTREAM | CONSTRAINT | EXTERNAL | Development/Building/Safety Code Permits | HIGH | ACTIVE |
| DEP-014-02-010 | EXECUTION | N/A | UPSTREAM | INTERFACE | PACKAGE | PKG-015 (Electrical -- conditional) | LOW | ACTIVE |
| DEP-014-02-011 | EXECUTION | N/A | UPSTREAM | INTERFACE | PACKAGE | PKG-018 (Sitework -- vacuum truck access) | MEDIUM | ACTIVE |
| DEP-014-02-012 | EXECUTION | N/A | DOWNSTREAM | HANDOVER | PACKAGE | PKG-020 (Commissioning and Closeout) | HIGH | ACTIVE |
| DEP-014-02-013 | EXECUTION | N/A | UPSTREAM | PREREQUISITE | DOCUMENT | R-06 Appendix B Plumbing Layout Drawing | HIGH | ACTIVE |

---

## Run Notes

**Run Date:** 2026-02-26
**Mode:** UPDATE
**Strictness:** CONSERVATIVE
**Consumer Context:** TASK_ESTIMATING
**Decomposition Path:** _Decomposition/WDMLRL_Decomposition_Claude.md (R1 -- 2026-02-25)
**Decomposition Status:** AVAILABLE -- validation and label resolution performed

### Defaults Applied
- **SOURCE_DOCS:** AUTO -- scanned deliverable folder, identified 4 source documents: Datasheet.md, Guidance.md, Procedure.md, Specification.md
- **DOC_ROLE_MAP:** DEFAULT heuristic applied
  - ANCHOR_DOC: Datasheet.md (matched "datasheet" keyword; contains Identification table with Governing SOW and Supports Objectives)
  - EXECUTION_DOCS: Procedure.md (primary -- contains Prerequisites table and sequenced Steps), Guidance.md (secondary -- contains Principles and Considerations with interface details), Specification.md (tertiary -- contains Requirements and Standards)
- **ANCHOR_DOC:** Datasheet.md (AUTO selection)
- **EXECUTION_DOC_ORDER:** Procedure.md, Guidance.md, Specification.md, Datasheet.md (AUTO ordering by workflow clarity)

### Extraction Notes
- Pass 1 (ANCHOR): 3 rows extracted. 1 parent anchor (SOW-0043) confirmed in Decomposition scope ledger. 2 objective traces (OBJ-001, OBJ-004) confirmed in Decomposition deliverables table and objective-package mapping.
- Pass 2 (EXECUTION): 10 rows extracted. All rows have explicit evidence citations. 1 row (DEP-014-02-010, PKG-015 electrical interface) is conditional/ASSUMPTION with LOW confidence -- alarm requirement TBD pending code confirmation.
- The declared upstream dependencies ("Site preparation and soil assessment" and "Environmental compliance verification") were not extracted as separate rows because the source documents do not provide sufficiently specific target identifiers or artifact descriptions beyond what is already captured in the geotechnical report prerequisite (DEP-014-02-008) and permit constraint (DEP-014-02-009). The declared items are preserved in the declared sections above.

### Warnings
- None. Parent anchor check: 1 ACTIVE IMPLEMENTS_NODE found (pass). No duplicate rows detected. All ACTIVE rows have EvidenceFile and SourceRef.

---

## Run History

| Run | Date | Mode | Strictness | Consumer | Decomposition | Warnings | ACTIVE Count |
|---|---|---|---|---|---|---|---|
| 1 | 2026-02-26 | UPDATE | CONSERVATIVE | TASK_ESTIMATING | AVAILABLE (R1) | None | 13 |

---

## Lifecycle Summary

| Status | Count |
|---|---|
| ACTIVE | 13 |
| RETIRED | 0 |

| SatisfactionStatus | Count |
|---|---|
| PENDING | 9 |
| NOT_APPLICABLE | 3 |
| TBD | 0 |
| SATISFIED | 1 |

---

## Downstream Handoff Notes (TASK_ESTIMATING)

The following dependency rows are flagged as relevant to task estimating readiness:

### BLOCKING (3 rows -- scope or key quantities unknown without these inputs)
- **DEP-014-02-004** (DEL-006-05, IFC Plumbing Drawings): Hard gate. Installation cannot commence and material quantities cannot be finalized until IFC drawings are approved. Tank material, bedding specification, connection details, and invert elevations all depend on this design deliverable.
- **DEP-014-02-008** (Geotechnical Investigation Report): Hard gate. Bedding requirements, embedment depth, frost protection, and backfill compaction specifications all depend on geotechnical data. Without this report, installation method and quantities are indeterminate.
- **DEP-014-02-009** (Permits): Constraint. Work cannot legally commence without development, building, and Safety Code permits.

### ADVISORY (4 rows -- likely to change quantities/specs or procurement approach)
- **DEP-014-02-005** (DEL-006-03, Drain and Vent Plans): Pipe routing and connection method details affect material quantities for the connection scope.
- **DEP-014-02-006** (DEL-014-04, Floor Drains): Interface coordination may affect pipe sizing, routing, or connection count.
- **DEP-014-02-007** (DEL-014-06, Plumbing Fixtures): Interface coordination may affect connection count and inlet sizing.
- **DEP-014-02-011** (PKG-018, Sitework): Vacuum truck access provisions may affect site preparation scope allocation.

### INFO (2 rows -- informational context, low likelihood of changing totals)
- **DEP-014-02-012** (PKG-020, Commissioning and Closeout): Documentation handover; does not affect installation quantities.
- **DEP-014-02-013** (R-06, Appendix B Plumbing Drawing): Already satisfied; conceptual reference only.

### TBD (1 row -- insufficient evidence to classify)
- **DEP-014-02-010** (PKG-015, Electrical): Conditional interface for alarm/monitoring system. If code-required, adds electrical scope; if not, no impact. Classification deferred until code confirmation.
