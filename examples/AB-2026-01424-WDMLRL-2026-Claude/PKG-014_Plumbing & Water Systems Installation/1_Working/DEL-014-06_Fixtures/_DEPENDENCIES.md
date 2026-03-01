# DEL-014-06_Fixtures Dependencies

## Dependency Status
**Tracking**: ACTIVE
**RegisterSchemaVersion**: v3.1

## Upstream Dependencies
- DEL-014-01: Cistern & Distribution (water supply rough-in to fixture zones; must be pressurized before final connections)
- DEL-014-02: Septic System (sanitary drain/DWV rough-in at industrial wash station location)
- DEL-014-04: Floor Drains & Sump Drains (DWV rough-in complete; no routing conflicts)
- DEL-015-04: Equipment Power Circuits / PKG-015 (70A electrical circuit stub-out for pressure washer reel)
- PKG-011: Building Structure & Envelope (walls and structural blocking at fixture mounting locations)
- PKG-012: Interior Construction & Fit-Out (interior walls and blocking complete at fixture mounting locations)
- DEL-006-01: Preliminary Plumbing Design (design review participation; approved before IFC production)
- DEL-006-02: Water Distribution Plans (IFC plumbing drawings required before procurement and installation)
- DEL-006-03: Drain & Vent Plans (IFC plumbing drawings required before procurement and installation)
- DEL-006-06: Plumbing Fixture Schedule (authoritative fixture data; required before procurement -- most critical upstream dependency)
- DEL-009-02: Building Permit Application & Approval (required prior to installation)
- DEL-009-03: Safety Code Permits (required prior to installation)

## Downstream Dependencies
- DEL-020-01: Building Systems Commissioning (fixtures must be operational and leak-free for commissioning)
- DEL-008-04: As-Built Survey (as-built markup of installed fixture locations submitted)
- DEL-009-04: Code Compliance Register & Inspection Log (Safety Code inspection reports submitted)
- DEL-021-05: Guarantee Period Obligations (warranty documentation submitted to Owner)

## Notes
Detailed dependency tracking is recorded in Dependencies.csv (v3.1 schema). All dependencies were extracted from deliverable source documents (Datasheet.md, Guidance.md, Procedure.md, Specification.md) and validated against the project decomposition.

---

## Extracted Dependency Register

**Total rows:** 21
**ACTIVE:** 21 | **RETIRED:** 0

| DependencyID | Class | AnchorType | Direction | Type | TargetType | Target | Confidence |
|---|---|---|---|---|---|---|---|
| DEP-014-06-A01 | ANCHOR | IMPLEMENTS_NODE | UPSTREAM | OTHER | WBS_NODE | PKG-014 | HIGH |
| DEP-014-06-A02 | ANCHOR | TRACES_TO_REQUIREMENT | UPSTREAM | OTHER | REQUIREMENT | SOW-0049 | HIGH |
| DEP-014-06-A03 | ANCHOR | TRACES_TO_REQUIREMENT | UPSTREAM | OTHER | REQUIREMENT | SOW-0050 | HIGH |
| DEP-014-06-A04 | ANCHOR | TRACES_TO_REQUIREMENT | UPSTREAM | OTHER | REQUIREMENT | OBJ-001 | HIGH |
| DEP-014-06-A05 | ANCHOR | TRACES_TO_REQUIREMENT | UPSTREAM | OTHER | REQUIREMENT | OBJ-004 | HIGH |
| DEP-014-06-E01 | EXECUTION | N/A | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-014-01 | HIGH |
| DEP-014-06-E02 | EXECUTION | N/A | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-014-02 | HIGH |
| DEP-014-06-E03 | EXECUTION | N/A | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-014-04 | HIGH |
| DEP-014-06-E04 | EXECUTION | N/A | UPSTREAM | INTERFACE | DELIVERABLE | DEL-015-04 | HIGH |
| DEP-014-06-E05 | EXECUTION | N/A | UPSTREAM | PREREQUISITE | PACKAGE | PKG-011 | HIGH |
| DEP-014-06-E06 | EXECUTION | N/A | UPSTREAM | PREREQUISITE | PACKAGE | PKG-012 | HIGH |
| DEP-014-06-E07 | EXECUTION | N/A | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-006-06 | HIGH |
| DEP-014-06-E08 | EXECUTION | N/A | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-006-02 | HIGH |
| DEP-014-06-E09 | EXECUTION | N/A | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-006-03 | HIGH |
| DEP-014-06-E10 | EXECUTION | N/A | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-006-01 | HIGH |
| DEP-014-06-E11 | EXECUTION | N/A | UPSTREAM | CONSTRAINT | DELIVERABLE | DEL-009-02 | HIGH |
| DEP-014-06-E12 | EXECUTION | N/A | UPSTREAM | CONSTRAINT | DELIVERABLE | DEL-009-03 | HIGH |
| DEP-014-06-E13 | EXECUTION | N/A | DOWNSTREAM | HANDOVER | DELIVERABLE | DEL-020-01 | HIGH |
| DEP-014-06-E14 | EXECUTION | N/A | DOWNSTREAM | HANDOVER | DELIVERABLE | DEL-008-04 | MEDIUM |
| DEP-014-06-E15 | EXECUTION | N/A | DOWNSTREAM | HANDOVER | DELIVERABLE | DEL-009-04 | MEDIUM |
| DEP-014-06-E16 | EXECUTION | N/A | DOWNSTREAM | HANDOVER | DELIVERABLE | DEL-021-05 | MEDIUM |

---

## Run Notes

**Run date:** 2026-02-26
**Mode:** UPDATE
**Strictness:** CONSERVATIVE
**Consumer context:** TASK_ESTIMATING

**Defaults used:**
- SOURCE_DOCS: AUTO -- scanned deliverable folder; identified Datasheet.md, Guidance.md, Procedure.md, Specification.md as source documents.
- DOC_ROLE_MAP: DEFAULT -- Datasheet.md classified as ANCHOR_DOC; Procedure.md, Guidance.md, Specification.md classified as EXECUTION_DOCs.
- ANCHOR_DOC: Datasheet.md (contains Identification table with Package, SOW, and deliverable identity fields).
- EXECUTION_DOC_ORDER: Procedure.md (strongest prerequisite/workflow signal), Specification.md (requirements and interface tables), Guidance.md (considerations and commissioning integration).

**Decomposition path:** `/Users/ryan/ai-env/projects/chirality-project-test/test/AB-2026-01424-WDMLRL-2026-Claude/_Decomposition/WDMLRL_Decomposition_Claude.md`
**Decomposition status:** Available and used for anchor validation and target resolution. All target IDs confirmed present in decomposition.

**Warnings:** None.

**Pass 1 (ANCHOR) notes:**
- 1 parent anchor (IMPLEMENTS_NODE) to PKG-014 confirmed in decomposition.
- 2 SOW trace anchors (SOW-0049, SOW-0050) confirmed in decomposition scope ledger.
- 2 objective trace anchors (OBJ-001, OBJ-004) confirmed in decomposition.

**Pass 2 (EXECUTION) notes:**
- 12 upstream execution dependencies extracted (6 physical prerequisites, 1 electrical interface, 4 design document prerequisites, 2 permit constraints, and 1 preliminary design prerequisite).
- 4 downstream handover dependencies extracted (commissioning, as-built survey, code compliance register, warranty).
- PKG-011 and PKG-012 recorded as PACKAGE-level targets because source text references them as packages without specifying a specific deliverable within.
- All execution dependencies are EXPLICIT per source text.
- CONSUMER_CONTEXT=TASK_ESTIMATING: EstimateImpactClass and ConsumerHint populated for all execution rows.

**Estimating impact summary:**
- BLOCKING: 10 rows (DEL-014-01, DEL-014-02, DEL-015-04, PKG-011, PKG-012, DEL-006-06, DEL-006-02, DEL-006-03, DEL-009-02, DEL-009-03)
- ADVISORY: 3 rows (DEL-014-04, DEL-006-01, DEL-020-01)
- INFO: 3 rows (DEL-008-04, DEL-009-04, DEL-021-05)

---

## Run History

| Run Date | Mode | Strictness | Decomposition | Warnings | ANCHOR Active | EXECUTION Active | Total Active |
|---|---|---|---|---|---|---|---|
| 2026-02-26 | UPDATE | CONSERVATIVE | Available (R1 2026-02-25) | None | 5 | 16 | 21 |

---

## Lifecycle Summary

| Category | Count |
|---|---|
| Total rows | 21 |
| ACTIVE | 21 |
| RETIRED | 0 |

**By DependencyClass:**
| Class | ACTIVE | RETIRED |
|---|---|---|
| ANCHOR | 5 | 0 |
| EXECUTION | 16 | 0 |

**By SatisfactionStatus (ACTIVE rows only):**
| SatisfactionStatus | Count |
|---|---|
| PENDING | 16 |
| NOT_APPLICABLE | 5 |

---

## Downstream Handoff Notes

**Consumer context:** TASK_ESTIMATING

This register identifies **10 BLOCKING upstream dependencies** that gate estimating readiness for DEL-014-06:

1. **DEL-006-06 (Plumbing Fixture Schedule)** -- The most critical dependency for estimating. All fixture types, models, specifications, and quantities are TBD pending this document. Without it, fixture procurement costs cannot be estimated with confidence. All TBD attribute values in Datasheet.md resolve through this deliverable.

2. **DEL-006-02 and DEL-006-03 (IFC Plumbing Drawings)** -- Required before procurement and installation. Routing details, connection sizes, and rough-in dimensions affect labor estimating.

3. **DEL-014-01 (Cistern & Distribution)** -- Physical prerequisite. Supply piping rough-in must be complete before fixture connections. Sequencing affects installation labor estimate.

4. **DEL-014-02 (Septic System)** -- Physical prerequisite for industrial wash station drain. Sequencing affects labor estimate.

5. **DEL-015-04 (Equipment Power Circuits)** -- Interface dependency for pressure washer reel 70A circuit. Affects coordination labor and potential rework risk.

6. **PKG-011 / PKG-012 (Structure / Interior Fit-Out)** -- Wall and blocking prerequisites. Must be complete before fixture mounting.

7. **DEL-009-02 / DEL-009-03 (Permits)** -- Regulatory constraints that gate all installation work.

**Key estimating uncertainty:** The design-build nature of this project means fixture specifications do not yet exist. DEL-006-06 (Plumbing Fixture Schedule) is the resolution path for all TBD material specifications. Until produced, fixture material costs are assumption-based. The hot water supply question (CONF-014-06-01) may add a point-of-use water heater to scope, affecting both material and labor estimates.
