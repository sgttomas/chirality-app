# Deliverable Dependencies: DEL-006-02

**Deliverable ID:** DEL-006-02
**Name:** Water Distribution Plans
**Package:** PKG-006 — Plumbing Design

## Declared Upstream Dependencies

- DEL-006-01 — Preliminary Plumbing Design (County-approved)
- DEL-006-04 — Cistern & Pump Details (upstream interface; source of distribution)
- DEL-006-07 — Plumbing Calculation Package (hydraulic calcs inform pipe sizing)
- DEL-006-08 — Plumbing Specification (governing spec for materials/standards)
- DEL-008-01 — Geotechnical Investigation Report
- DEL-008-02 — Preliminary Site Survey
- DEL-001-02 — Architectural Floor Plans (fixture location coordination)
- DEL-002-02 — Structural Foundation Plan (slab penetration/sleeve coordination)

## Declared Downstream Dependencies

- PKG-014 — Plumbing & Water Systems Installation (IFC drawing set consumed for construction)
- Safety Code Officer — IFC drawing set reviewed for inspection

---

## Extracted Dependency Register

**Register:** `Dependencies.csv` (v3.1)
**Total ACTIVE rows:** 21
**Total RETIRED rows:** 0

### ANCHOR Rows (4 ACTIVE)

| DependencyID | AnchorType | TargetRefID | TargetName | Confidence |
|---|---|---|---|---|
| DEP-006-02-001 | IMPLEMENTS_NODE | SOW-0016 | Complete final plumbing design (water supply drainage septic) | HIGH |
| DEP-006-02-002 | TRACES_TO_REQUIREMENT | OBJ-001 | Deliver a code-compliant, fully functional maintenance shop addition | HIGH |
| DEP-006-02-003 | TRACES_TO_REQUIREMENT | OBJ-003 | Produce complete, P.Eng.-stamped IFC design documentation | HIGH |
| DEP-006-02-004 | TRACES_TO_REQUIREMENT | OBJ-004 | Install and commission all plumbing and water storage systems | HIGH |

### EXECUTION Rows (17 ACTIVE)

| DependencyID | Direction | DependencyType | TargetType | Target | Confidence | EstimateImpactClass |
|---|---|---|---|---|---|---|
| DEP-006-02-005 | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-006-01 — Preliminary Plumbing Design | HIGH | BLOCKING |
| DEP-006-02-006 | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-008-01 — Geotechnical Investigation Report | HIGH | BLOCKING |
| DEP-006-02-007 | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-008-02 — Preliminary Site Survey | HIGH | BLOCKING |
| DEP-006-02-008 | UPSTREAM | INTERFACE | DELIVERABLE | DEL-001-02 — Architectural Floor Plans | HIGH | ADVISORY |
| DEP-006-02-009 | UPSTREAM | INTERFACE | DELIVERABLE | DEL-002-02 — Structural Foundation Plan | HIGH | ADVISORY |
| DEP-006-02-010 | UPSTREAM | INTERFACE | DELIVERABLE | DEL-006-04 — Cistern and Pump Details | HIGH | BLOCKING |
| DEP-006-02-011 | UPSTREAM | INTERFACE | DELIVERABLE | DEL-006-07 — Plumbing Calculation Package | HIGH | BLOCKING |
| DEP-006-02-012 | UPSTREAM | INTERFACE | DELIVERABLE | DEL-006-08 — Plumbing Specification | MEDIUM | ADVISORY |
| DEP-006-02-013 | DOWNSTREAM | HANDOVER | PACKAGE | PKG-014 — Plumbing & Water Systems Installation | HIGH | ADVISORY |
| DEP-006-02-014 | UPSTREAM | INTERFACE | PACKAGE | PKG-004 — Electrical Design | MEDIUM | ADVISORY |
| DEP-006-02-015 | UPSTREAM | INTERFACE | DELIVERABLE | DEL-006-06 — Plumbing Fixture Schedule | HIGH | ADVISORY |
| DEP-006-02-016 | UPSTREAM | INTERFACE | DELIVERABLE | DEL-006-03 — Drain and Vent Plans | MEDIUM | INFO |
| DEP-006-02-017 | UPSTREAM | INTERFACE | DELIVERABLE | DEL-006-05 — Septic System Details | MEDIUM | INFO |
| DEP-006-02-018 | UPSTREAM | INTERFACE | PACKAGE | PKG-003 — Mechanical Design | MEDIUM | ADVISORY |
| DEP-006-02-019 | UPSTREAM | PREREQUISITE | DOCUMENT | R-06 — Appendix B (Plumbing) conceptual drawing | HIGH | INFO |
| DEP-006-02-020 | UPSTREAM | PREREQUISITE | DOCUMENT | R-01 — RFP Design Requirements (§3.4) | HIGH | INFO |
| DEP-006-02-021 | DOWNSTREAM | HANDOVER | EXTERNAL | Safety Code Officer | MEDIUM | INFO |

---

## Run Notes

**Run date:** 2026-02-26
**Mode:** UPDATE
**Strictness:** CONSERVATIVE
**Consumer context:** TASK_ESTIMATING

### Defaults and Paths Used

| Parameter | Value | Rationale |
|---|---|---|
| DECOMPOSITION_PATH | `_Decomposition/WDMLRL_Decomposition_Claude.md` | Provided by invoker |
| ANCHOR_DOC | `Datasheet.md` | AUTO — selected as highest-confidence anchor doc (contains SOW Reference, Objectives Supported, identification table) |
| EXECUTION_DOC_ORDER | `Procedure.md`, `Specification.md`, `Guidance.md` | AUTO — Procedure has explicit prerequisites table and workflow steps; Specification has requirements; Guidance has purpose/principles |
| SOURCE_DOCS | `Datasheet.md`, `Procedure.md`, `Specification.md`, `Guidance.md` | AUTO — all candidate source docs in deliverable folder, excluding dependency artifacts and generated files |
| _REFERENCES.md | Read (used for document target resolution) | Available in deliverable folder |

### Warnings

(none)

### Integrity Check Results

- Parent anchor (IMPLEMENTS_NODE): 1 found (DEP-006-02-001 -> SOW-0016). PASS.
- DependencyID uniqueness: 21 unique IDs for 21 rows. PASS.
- All ACTIVE rows have EvidenceFile and SourceRef. PASS.
- All enums are canonical write-form. PASS.
- No RETIRED rows (first comprehensive extraction). PASS.
- CSV parseable: confirmed via automated check. PASS.

### Extraction Notes

- **Pass 1 (Anchor):** Extracted 1 IMPLEMENTS_NODE anchor (SOW-0016) and 3 TRACES_TO_REQUIREMENT anchors (OBJ-001, OBJ-003, OBJ-004) from Datasheet.md identification table. All confirmed against Decomposition §7 PKG-006.
- **Pass 2 (Execution):** Extracted 17 execution edges from Procedure.md (prerequisites table, steps), Specification.md (requirements, verification), Guidance.md (purpose, principles, considerations), and Datasheet.md (references, conditions). Key additions over prior extraction: DEL-006-06 (fixture schedule interface), DEL-006-03 and DEL-006-05 (scope boundary interfaces), PKG-003 (mechanical coordination interface), R-06 and R-01 (document prerequisites), Safety Code Officer (downstream consumer).
- **Target resolution:** All deliverable targets resolved against Decomposition §7. Package targets (PKG-003, PKG-004, PKG-014) resolved against Decomposition §6. Document targets (R-01, R-06) resolved against _REFERENCES.md.
- **EstimateImpactClass populated** for all EXECUTION rows per CONSUMER_CONTEXT=TASK_ESTIMATING. BLOCKING assigned to explicit prerequisites and interfaces that gate scope/quantities (DEL-006-01, DEL-008-01, DEL-008-02, DEL-006-04, DEL-006-07). ADVISORY assigned to interfaces that likely influence specs/approach but are not hard gates. INFO assigned to scope boundary interfaces and available document inputs.

---

## Run History

| Run | Date | Mode | Strictness | Decomposition | Warnings | ACTIVE Anchors | ACTIVE Execution | Notes |
|---|---|---|---|---|---|---|---|---|
| 1 | 2026-02-26 | UPDATE | CONSERVATIVE | Available (WDMLRL_Decomposition_Claude.md R1) | None | 4 | 17 | Initial comprehensive extraction. CONSUMER_CONTEXT=TASK_ESTIMATING. 21 total ACTIVE rows. |

---

## Lifecycle Summary

| Status | Count |
|---|---|
| ACTIVE | 21 |
| RETIRED | 0 |

### Closure Lifecycle Breakdown (ACTIVE rows)

| SatisfactionStatus | Count | Notes |
|---|---|---|
| TBD | 19 | Pending design development |
| SATISFIED | 2 | R-06 (Appendix B Plumbing) and R-01 (RFP) are available |

---

## Downstream Handoff Notes

**Consumer context:** TASK_ESTIMATING

### Estimating-Critical Dependencies

The following EXECUTION dependencies are classified as **BLOCKING** for estimating readiness. These represent inputs without which scope or key quantities cannot be confidently determined for DEL-006-02:

| DependencyID | Target | Rationale |
|---|---|---|
| DEP-006-02-005 | DEL-006-01 — Preliminary Plumbing Design | County-approved preliminary design defines the scope baseline. Without it, distribution layout is not confirmed. Mandatory hold point (Procedure Step 8A). |
| DEP-006-02-006 | DEL-008-01 — Geotechnical Investigation Report | Foundation/slab design affects penetration locations. Prerequisite for meaningful coordination. |
| DEP-006-02-007 | DEL-008-02 — Preliminary Site Survey | Site conditions affect cistern/pump location and external piping routes. |
| DEP-006-02-010 | DEL-006-04 — Cistern and Pump Details | Cistern/pump interface defines the supply source for the entire distribution network. Pipe sizing depends on pump output. Scope boundary (CF-002) unresolved. |
| DEP-006-02-011 | DEL-006-07 — Plumbing Calculation Package | Hydraulic calculations determine pipe sizes, pressure zones, and fixture flow rates. Multiple Datasheet values are TBD pending this deliverable. |

### Advisory Dependencies (Estimating)

The following EXECUTION dependencies are classified as **ADVISORY** -- they are likely to influence quantities, specifications, or procurement approach but are not hard gates:

| DependencyID | Target | Rationale |
|---|---|---|
| DEP-006-02-008 | DEL-001-02 — Architectural Floor Plans | Room layouts affect fixture rough-in locations and pipe routing lengths. |
| DEP-006-02-009 | DEL-002-02 — Structural Foundation Plan | Sleeve/penetration locations affect pipe routing. |
| DEP-006-02-012 | DEL-006-08 — Plumbing Specification | Material selection (pipe type, fittings) affects material costs. Currently TBD. |
| DEP-006-02-013 | PKG-014 — Plumbing Installation | Downstream consumer; installation approach may inform drawing detail level. |
| DEP-006-02-014 | PKG-004 — Electrical Design | Heat tracing (if selected) adds electrical scope and cost. |
| DEP-006-02-015 | DEL-006-06 — Plumbing Fixture Schedule | Fixture count and types affect pipe sizing and material quantities. |
| DEP-006-02-018 | PKG-003 — Mechanical Design | Utility room layout affects pipe routing and clearances. |

### Unresolved Scope Questions Affecting Estimates

1. **CF-001 (Hot water provision):** Whether hot water piping is in scope of DEL-006-02 significantly affects pipe material quantities, heater equipment, and installation labor. TBD pending Plumbing Engineer / County ruling.
2. **CF-002 (Bulk fill piping scope boundary):** Whether bulk fill distribution piping is in DEL-006-02 or DEL-006-04 affects drawing scope and associated material quantities. TBD pending Plumbing Engineer determination at preliminary design.
