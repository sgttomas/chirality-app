# Dependencies: DEL-001-10 Old North Shop Renovation Plans

## Coordination (human-owned)
- **Mode:** TRACKED
- **Notes:** Dependency register extracted by DEPENDENCIES agent. Coordination representation confirmed via extraction from source documents.

## Upstream (I need these before I can proceed) -- human-owned declarations
- Dependencies coordinated externally by humans.

## Downstream (These need me) -- human-owned declarations
- Dependencies coordinated externally by humans.

---

## Extracted Dependency Register

**Status:** COMPLETE
**Dependencies.csv:** 18 rows (18 ACTIVE, 0 RETIRED)
**Schema Version:** v3.1

### ANCHOR Dependencies (3 ACTIVE)

| DependencyID | AnchorType | TargetRefID | TargetName | Confidence |
|---|---|---|---|---|
| DEP-001-10-A01 | IMPLEMENTS_NODE | SOW-0070, SOW-0071, SOW-0072, SOW-0073, SOW-0074 | Renovate Old North Shop (all renovation scope) | HIGH |
| DEP-001-10-A02 | TRACES_TO_REQUIREMENT | OBJ-001 | Deliver a code-compliant, fully functional maintenance shop addition | HIGH |
| DEP-001-10-A03 | TRACES_TO_REQUIREMENT | OBJ-003 | Produce complete P.Eng.-stamped IFC design documentation | HIGH |

### EXECUTION Dependencies -- UPSTREAM (12 ACTIVE)

| DependencyID | Type | TargetType | Target | EstimateImpact | Confidence |
|---|---|---|---|---|---|
| DEP-001-10-E01 | CONSTRAINT | DELIVERABLE | DEL-001-01 Preliminary Architectural Design | BLOCKING | HIGH |
| DEP-001-10-E02 | PREREQUISITE | DELIVERABLE | DEL-001-09 Old North Shop Demolition Plans | BLOCKING | HIGH |
| DEP-001-10-E03 | INTERFACE | DELIVERABLE | DEL-001-02 Architectural Floor Plans | ADVISORY | MEDIUM |
| DEP-001-10-E06 | INTERFACE | DELIVERABLE | DEL-001-11 Architectural Specification | ADVISORY | HIGH |
| DEP-001-10-E07 | INTERFACE | PACKAGE | PKG-002 Structural Design | BLOCKING | HIGH |
| DEP-001-10-E08 | INTERFACE | PACKAGE | PKG-006 Plumbing Design | BLOCKING | HIGH |
| DEP-001-10-E09 | INTERFACE | PACKAGE | PKG-003 Mechanical Design | ADVISORY | MEDIUM |
| DEP-001-10-E10 | INTERFACE | PACKAGE | PKG-004 Electrical Design | ADVISORY | HIGH |
| DEP-001-10-E12 | PREREQUISITE | EXTERNAL | Existing Conditions Field Survey | BLOCKING | HIGH |
| DEP-001-10-E13 | CONSTRAINT | EXTERNAL | County Preliminary Design Approval | BLOCKING | HIGH |
| DEP-001-10-E14 | CONSTRAINT | EXTERNAL | Alberta Building Code Edition Confirmation from AHJ | BLOCKING | MEDIUM |
| DEP-001-10-E15 | PREREQUISITE | EXTERNAL | Mandatory Site Meeting Attendance | BLOCKING | HIGH |

### EXECUTION Dependencies -- DOWNSTREAM (3 ACTIVE)

| DependencyID | Type | TargetType | Target | EstimateImpact | Confidence |
|---|---|---|---|---|---|
| DEP-001-10-E04 | HANDOVER | DELIVERABLE | DEL-001-07 Door & Window Schedule | ADVISORY | HIGH |
| DEP-001-10-E05 | HANDOVER | DELIVERABLE | DEL-001-08 Finish Schedule | ADVISORY | HIGH |
| DEP-001-10-E11 | HANDOVER | PACKAGE | PKG-017 Existing Building Renovation | BLOCKING | HIGH |

---

## Run Notes

**Run Date:** 2026-02-26
**Mode:** UPDATE
**Strictness:** CONSERVATIVE
**Consumer Context:** TASK_ESTIMATING

### Paths Used
- **RUN_ROOT:** `/Users/ryan/ai-env/projects/chirality-project-test/test/AB-2026-01424-WDMLRL-2026-Claude/PKG-001_Architectural Design/1_Working/DEL-001-10_Renovation-Plans`
- **DECOMPOSITION_PATH:** `/Users/ryan/ai-env/projects/chirality-project-test/test/AB-2026-01424-WDMLRL-2026-Claude/_Decomposition/WDMLRL_Decomposition_Claude.md` (available; used for validation)
- **ANCHOR_DOC (AUTO):** `Datasheet.md` (selected by heuristic: filename contains "datasheet")
- **EXECUTION_DOC_ORDER (AUTO):** `Procedure.md`, `Specification.md`, `Guidance.md`, `Datasheet.md`
- **SOURCE_DOCS (AUTO):** `Datasheet.md`, `Specification.md`, `Procedure.md`, `Guidance.md`
- **_REFERENCES.md:** Present; used for document pointer context (2 applicable references: R-01 RFP, R-04 Appendix B Shop)

### Defaults Applied
- SOURCE_DOCS=AUTO: scanned deliverable folder; excluded `_DEPENDENCIES.md`, `_REFERENCES.md`, `_CONTEXT.md`, `_STATUS.md`, `_SEMANTIC.md`, `_SEMANTIC_LENSING.md`, `Dependencies.csv`
- ANCHOR_DOC=AUTO: selected `Datasheet.md` (highest-confidence match for definition/traceability signal)
- EXECUTION_DOC_ORDER=AUTO: Procedure.md first (strongest workflow signal), then Specification.md, Guidance.md, Datasheet.md

### Decomposition Validation
- Decomposition file located and used for validation
- DEL-001-10 confirmed in PKG-001 deliverable table (SS7)
- SOW-0070 through SOW-0074 confirmed in SSOW (SS3-I)
- OBJ-001 and OBJ-003 confirmed in Objectives (SS5)
- PKG-017 downstream deliverables (DEL-017-01 through DEL-017-04) confirmed in SS7 PKG-017 table
- All target deliverable/package IDs resolved against decomposition

### Package ID Mapping Note
- Source documents (Specification REQ-009) reference "PKG-003/PKG-004" for mechanical/plumbing and "PKG-005" for electrical. The decomposition maps these disciplines differently: Mechanical/HVAC = PKG-003, Electrical = PKG-004, Plumbing = PKG-006. Dependency rows use decomposition IDs (PKG-003, PKG-004, PKG-006) per referential integrity rules. This discrepancy is noted in the relevant row Notes fields.

### Warnings
- None. All quality checks pass.

### Assumptions
- ANCHOR rows A02/A03 association to OBJ-001/OBJ-003 is by package group heuristic (decomposition maps objectives to packages, not individual deliverables). Noted as FACT with caveat in row Notes.
- DEP-001-10-E14 (AHJ code edition confirmation) assumes NBC 2019 Alberta Edition until confirmed. Marked in row Notes.

### Items Not Extracted (conservative filter)
- Geotechnical report dependency (Procedure Prerequisites): conditional on whether locker room requires new footings. Not emitted at CONSERVATIVE strictness because the need is unresolved.
- RFP (R-01) and Appendix B (R-04) as document dependencies: these are reference sources, not information-flow dependencies from other deliverables. Not emitted.
- Coordination with DEL-001-03 through DEL-001-06 (Exterior Elevations, Building Sections, Interior Elevations, Reflected Ceiling Plans): Specification lists these as excluded scope ("covered by DEL-001-02 through DEL-001-08") but no explicit artifact transfer is stated beyond the DEL-001-02 junction interface and the DEL-001-07/DEL-001-08 schedule handovers. Not emitted individually.

---

## Run History

| Run Date | Mode | Strictness | Consumer | Decomposition | Warnings | ACTIVE Anchors | ACTIVE Execution | Total ACTIVE |
|---|---|---|---|---|---|---|---|---|
| 2026-02-26 | UPDATE | CONSERVATIVE | TASK_ESTIMATING | Available (validated) | None | 3 | 15 | 18 |

---

## Lifecycle Summary

| Metric | Count |
|---|---|
| Total rows | 18 |
| ACTIVE | 18 |
| RETIRED | 0 |
| ANCHOR (ACTIVE) | 3 |
| EXECUTION (ACTIVE) | 15 |
| UPSTREAM (ACTIVE) | 15 |
| DOWNSTREAM (ACTIVE) | 3 |

### SatisfactionStatus Breakdown (ACTIVE rows)

| Status | Count |
|---|---|
| TBD | 3 (all ANCHOR rows) |
| PENDING | 15 (all EXECUTION rows) |

### EstimateImpactClass Breakdown (ACTIVE EXECUTION rows)

| Class | Count |
|---|---|
| BLOCKING | 9 |
| ADVISORY | 6 |

---

## Downstream Handoff Notes

**Consumer Context:** TASK_ESTIMATING

### Estimating-Relevant Summary

This deliverable has **9 BLOCKING** execution dependencies that gate meaningful estimating:

**Hard gates (BLOCKING -- scope or key quantities unknown without these):**
1. **DEP-001-10-E01** -- County preliminary design approval via DEL-001-01 gates IFC production
2. **DEP-001-10-E02** -- DEL-001-09 Demolition Plans must establish post-demolition conditions before renovation design basis is known
3. **DEP-001-10-E07** -- PKG-002 Structural Design input required for mezzanine modifications
4. **DEP-001-10-E08** -- PKG-006 Plumbing Design input required for washroom/kitchenette/laundry rough-ins
5. **DEP-001-10-E11** -- PKG-017 construction packages consume this drawing set (downstream blocking)
6. **DEP-001-10-E12** -- Existing conditions field survey must be completed (no as-built information currently available)
7. **DEP-001-10-E13** -- County preliminary design approval is an external gate
8. **DEP-001-10-E14** -- AHJ confirmation of governing building code edition
9. **DEP-001-10-E15** -- Mandatory site meeting attendance required before design proceeds

**Advisory (likely to affect quantities/specs but not a hard gate):**
1. **DEP-001-10-E03** -- Interface with DEL-001-02 floor plans at building junction
2. **DEP-001-10-E04** -- Handover to DEL-001-07 Door & Window Schedule
3. **DEP-001-10-E05** -- Handover to DEL-001-08 Finish Schedule
4. **DEP-001-10-E06** -- Interface with DEL-001-11 Architectural Specification (material/workmanship)
5. **DEP-001-10-E09** -- Interface with PKG-003 Mechanical Design
6. **DEP-001-10-E10** -- Interface with PKG-004 Electrical Design

### Key Estimating Risk
The field survey (DEP-001-10-E12) and demolition plans (DEP-001-10-E02) are the primary estimating blockers. Until the Old North Shop existing conditions are field-verified and the demolition scope is established, the renovation design basis is undefined. Renovation quantities (demolition extent, new construction extent, fixture counts, finish areas) cannot be reliably estimated without these inputs.

The multi-discipline interface dependencies (PKG-002 Structural, PKG-006 Plumbing, PKG-003 Mechanical, PKG-004 Electrical) indicate that estimating for this deliverable should be coordinated with these discipline packages; the renovation scope touches structural, plumbing, mechanical, and electrical work that will be designed by others.
