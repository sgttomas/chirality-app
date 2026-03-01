# DEL-015-04_Equipment-Power Dependencies

## Dependency Status
**Tracking**: ACTIVE
**Register**: Dependencies.csv (v3.1)

## Upstream Dependencies
- DEL-015-01: Three-Phase Power Service (electrical supply)
- Equipment specifications and locations (external)

## Downstream Dependencies
- DEL-015-05: Low-Voltage Systems (control system integration)

## Extracted Dependency Register

**Total rows:** 22
- ANCHOR: 9 (1 IMPLEMENTS_NODE, 6 TRACES_TO_REQUIREMENT [SOW], 2 TRACES_TO_REQUIREMENT [OBJ])
- EXECUTION: 13 (7 UPSTREAM PREREQUISITE, 2 UPSTREAM INTERFACE, 2 UPSTREAM CONSTRAINT, 1 DOWNSTREAM HANDOVER, 1 DOWNSTREAM ENABLES)

| DependencyID | Class | AnchorType | Dir | Type | TargetType | Target | Confidence | Status |
|---|---|---|---|---|---|---|---|---|
| DEP-015-04-001 | ANCHOR | IMPLEMENTS_NODE | UP | OTHER | PACKAGE | PKG-015 | HIGH | ACTIVE |
| DEP-015-04-002 | ANCHOR | TRACES_TO_REQ | UP | OTHER | REQUIREMENT | SOW-0059 | HIGH | ACTIVE |
| DEP-015-04-003 | ANCHOR | TRACES_TO_REQ | UP | OTHER | REQUIREMENT | SOW-0060 | HIGH | ACTIVE |
| DEP-015-04-004 | ANCHOR | TRACES_TO_REQ | UP | OTHER | REQUIREMENT | SOW-0061 | HIGH | ACTIVE |
| DEP-015-04-005 | ANCHOR | TRACES_TO_REQ | UP | OTHER | REQUIREMENT | SOW-0062 | HIGH | ACTIVE |
| DEP-015-04-006 | ANCHOR | TRACES_TO_REQ | UP | OTHER | REQUIREMENT | SOW-0063 | HIGH | ACTIVE |
| DEP-015-04-007 | ANCHOR | TRACES_TO_REQ | UP | OTHER | REQUIREMENT | SOW-0066 | HIGH | ACTIVE |
| DEP-015-04-008 | ANCHOR | TRACES_TO_REQ | UP | OTHER | WBS_NODE | OBJ-001 | HIGH | ACTIVE |
| DEP-015-04-009 | ANCHOR | TRACES_TO_REQ | UP | OTHER | WBS_NODE | OBJ-005 | HIGH | ACTIVE |
| DEP-015-04-010 | EXECUTION | N/A | UP | PREREQUISITE | DELIVERABLE | DEL-015-01 | HIGH | ACTIVE |
| DEP-015-04-011 | EXECUTION | N/A | UP | PREREQUISITE | DELIVERABLE | DEL-004-02 | HIGH | ACTIVE |
| DEP-015-04-012 | EXECUTION | N/A | UP | PREREQUISITE | DELIVERABLE | DEL-004-06 | HIGH | ACTIVE |
| DEP-015-04-013 | EXECUTION | N/A | UP | PREREQUISITE | DELIVERABLE | DEL-004-08 | HIGH | ACTIVE |
| DEP-015-04-014 | EXECUTION | N/A | UP | INTERFACE | DELIVERABLE | DEL-016-01 | HIGH | ACTIVE |
| DEP-015-04-015 | EXECUTION | N/A | UP | PREREQUISITE | DELIVERABLE | DEL-011-01 | MEDIUM | ACTIVE |
| DEP-015-04-016 | EXECUTION | N/A | UP | PREREQUISITE | DELIVERABLE | DEL-002-07 | MEDIUM | ACTIVE |
| DEP-015-04-017 | EXECUTION | N/A | UP | INTERFACE | PACKAGE | PKG-013 | HIGH | ACTIVE |
| DEP-015-04-018 | EXECUTION | N/A | UP | CONSTRAINT | EXTERNAL | Equipment Specs (External) | HIGH | ACTIVE |
| DEP-015-04-019 | EXECUTION | N/A | UP | CONSTRAINT | EXTERNAL | AB Safety Code Permit | HIGH | ACTIVE |
| DEP-015-04-020 | EXECUTION | N/A | DN | HANDOVER | DELIVERABLE | DEL-020-01 | HIGH | ACTIVE |
| DEP-015-04-021 | EXECUTION | N/A | DN | ENABLES | DELIVERABLE | DEL-015-05 | MEDIUM | ACTIVE |
| DEP-015-04-022 | EXECUTION | N/A | UP | INTERFACE | DELIVERABLE | DEL-004-03 | MEDIUM | ACTIVE |

---

## Run Notes

### Run 2026-02-26 (Initial Extraction)

**Parameters:**
- SCOPE: DEL-015-04
- MODE: UPDATE
- STRICTNESS: CONSERVATIVE
- CONSUMER_CONTEXT: TASK_ESTIMATING
- SOURCE_DOCS: AUTO

**Paths used:**
- RUN_ROOT: /Users/ryan/ai-env/projects/chirality-project-test/test/AB-2026-01424-WDMLRL-2026-Claude
- DELIVERABLE_PATH: .../PKG-015_Electrical & Low-Voltage Installation/1_Working/DEL-015-04_Equipment-Power/
- DECOMPOSITION_PATH: _Decomposition/WDMLRL_Decomposition_Claude.md (available; validated)
- _REFERENCES.md: present; used for document pointer resolution

**Source document role assignments (AUTO heuristic):**
- ANCHOR_DOC: Datasheet.md (definition/traceability signal -- contains Identification, Attributes, Conditions, References)
- EXECUTION_DOC_ORDER: Procedure.md (highest workflow clarity), Specification.md, Guidance.md
- Additional read-only inputs: _CONTEXT.md, _REFERENCES.md, _DEPENDENCIES.md (declared edges)

**Decomposition status:** Available. Used for:
- Validating parent anchor (PKG-015 confirmed at decomposition line 526)
- Resolving deliverable IDs and canonical names for all targets
- Confirming SOW-to-deliverable mappings in scope ledger
- Confirming objective references (OBJ-001, OBJ-005)

**Defaults and assumptions:**
- No existing Dependencies.csv; created fresh (MODE=UPDATE, no prior rows to merge).
- Declared edges from _DEPENDENCIES.md preserved: DEL-015-05 downstream (DEP-015-04-021, Origin=DECLARED).
- Equipment specifications dependency (Procedure P-06) recorded as EXTERNAL TargetType since no specific deliverable ID exists for equipment procurement beyond cranes (DEL-016-01 handled separately).
- DEL-002-07 is a design deliverable (drawing set) in the decomposition; Procedure P-04 references "crane runway beams in place" which is physical construction under PKG-011. Both the design reference and the structural prerequisite are captured.

**Warnings:**
- None. Parent anchor found (1 IMPLEMENTS_NODE). No ambiguity.

**Estimating context notes:**
- CONSUMER_CONTEXT=TASK_ESTIMATING: EstimateImpactClass and ConsumerHint populated for all EXECUTION rows.
- 7 EXECUTION rows marked BLOCKING: DEL-015-01 (power service), DEL-004-02 (IFC drawings), DEL-004-06 (panel schedules), DEL-004-08 (calculations), DEL-016-01 (crane specs), PKG-013 (exhaust fan scope boundary), equipment specifications (external).
- 3 EXECUTION rows marked ADVISORY: DEL-011-01 (superstructure), DEL-002-07 (crane supports), Alberta Safety Code permit, DEL-004-03 (power distribution plans).
- 1 EXECUTION row marked INFO: DEL-020-01 (commissioning handover -- downstream, does not affect estimating readiness).
- 1 DECLARED row with TBD impact: DEL-015-05 (no explicit artifact transfer in source documents).

---

## Run History

| Timestamp | Mode | Strictness | Consumer | Decomposition | Warnings | ACTIVE Anchors | ACTIVE Execution | Total ACTIVE |
|---|---|---|---|---|---|---|---|---|
| 2026-02-26 | UPDATE | CONSERVATIVE | TASK_ESTIMATING | Available (validated) | None | 9 | 13 | 22 |

---

## Lifecycle Summary

| Metric | Count |
|---|---|
| Total rows | 22 |
| ACTIVE | 22 |
| RETIRED | 0 |
| Origin: EXTRACTED | 21 |
| Origin: DECLARED | 1 |

**Closure-state breakdown (ACTIVE rows):**

| SatisfactionStatus | Count |
|---|---|
| NOT_APPLICABLE | 9 (all ANCHOR rows) |
| PENDING | 11 (EXECUTION rows awaiting upstream delivery) |
| TBD | 2 (downstream EXECUTION rows -- closure state not yet determinable) |

---

## Downstream Handoff Notes (CONSUMER_CONTEXT: TASK_ESTIMATING)

This section provides guidance for downstream task-estimating workflows consuming this dependency register.

### Blocking dependencies for estimating readiness

The following upstream dependencies are marked `EstimateImpactClass=BLOCKING` because they gate the ability to produce meaningful quantity/scope estimates for DEL-015-04:

1. **DEL-004-02 (IFC Electrical Drawings)** and **DEL-004-06 (Panel Schedules)**: Without IFC design, circuit layouts, wiring methods, conduit routing, and breaker assignments are all TBD. Material quantities cannot be estimated.
2. **DEL-004-08 (Electrical Calculation Package)**: Conductor sizing depends on load calculations. Without this, wire gauge and conduit fill cannot be determined.
3. **DEL-016-01 (Crane Procurement)**: Crane circuit voltage, amperage, and power supply method (conductor bar vs. festoon vs. bus duct) are entirely TBD pending crane manufacturer data. This affects both material type and quantity for the two most complex circuits (C-01, C-02).
4. **PKG-013 (Mechanical scope boundary)**: The number of exhaust fan circuits (C-07) is TBD pending scope clarification between SOW-0066 (this deliverable) and SOW-0038/SOW-0039 (PKG-013). See CON-015-04-001 in Guidance.md.
5. **Equipment Specifications (External)**: Voltage for circuits C-04, C-05, C-06 is TBD pending equipment nameplates. Conductor sizing and breaker selection cannot be finalized without this data.
6. **DEL-015-01 (Three-Phase Power Service)**: While this does not block quantity estimation per se, it is a hard prerequisite for energization and commissioning. If the service voltage or panel configuration changes, it could affect all downstream circuit designs.

### Advisory dependencies

- **DEL-011-01 / DEL-002-07 (Structure / Crane Supports)**: Physical prerequisites for crane circuit rough-in. Unlikely to change material quantities but affect sequencing and potentially conduit routing.
- **Alberta Safety Code Permit**: Regulatory prerequisite; does not affect quantity estimation but is a scheduling gate.
- **DEL-004-03 (Power Distribution Plans)**: Provides conduit routing detail; partially overlaps with DEL-004-02. May refine routing quantities.

### Estimating readiness assessment

DEL-015-04 is **NOT ready for detailed quantity estimating** until at minimum:
- IFC electrical design package (DEL-004-02, DEL-004-03, DEL-004-06, DEL-004-08) is issued
- Crane manufacturer electrical data (via DEL-016-01) is received
- Exhaust fan scope boundary (PKG-013 interface) is resolved
- Equipment nameplate data (compressor, pumps, pressure washer, door operators) is confirmed

Rough-order-of-magnitude estimating may proceed using the known amperage values (40A compressor, 70A pump, 70A washer) with assumptions for voltage and wiring method, but crane circuits and exhaust fan circuits have insufficient data for even ROM estimates.

## Notes
Detailed dependency tracking managed within project execution framework.
