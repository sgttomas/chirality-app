# DEL-013-05: Welding Station Exhaust System - Dependencies

## Dependency Status
**Tracking Status**: TRACKED
**Register Schema**: v3.1
**Last Extraction**: 2026-02-26

## External Dependencies
- Welding station location and layout finalization
- Welding equipment specifications (County to supply per R-01 S3.4)
- Shop floor plan finalization
- Exhaust outlet location approval (AHJ and environmental authority)
- Alberta OHS Code and environmental compliance review
- Mechanical Contractor availability

## Internal Package Dependencies
- **DEL-013-01** (Heating System): Potential heat recovery interface with welding exhaust (ASSUMPTION; open design question)
- **DEL-013-03** (Makeup Air): Bidirectional interface -- exhaust CFM must be coordinated with makeup air capacity; exhaust volume is a required input to makeup air sizing
- **DEL-013-04** (Equipment Exhaust): Interface -- aggregate exhaust volume, duct routing, and stack proximity coordination required
- **PKG-011** (Building Structure & Envelope): Prerequisite -- IFC structural/envelope drawings required for ductwork penetration locations
- **PKG-015** (Electrical): Interface -- fan motor power circuit and controls wiring coordination

## Critical Integration Points
- Welding fume capture at source is critical for safety
- Exhaust volume affects makeup air requirements (DEL-013-03)
- Filtration critical for particulate control
- Ductwork coordination with workstation layout
- Flexible connections for workstation movement

## Constraint Notes
- Welding exhaust must be captured immediately at source
- Fume filtration must meet Alberta OHS Code standards
- Flexible ductwork allows workstation positioning
- Multiple exhaust hoods may be needed (TBD pending County confirmation -- see CT-002)
- System must be cleanable and filtration maintainable

## Dependency Map
```
County Welding Specs -----> DEL-013-05 (Welding Exhaust)
Welding Station Layout ---> DEL-013-05
AHJ/Environmental -------> DEL-013-05
PKG-011 (Structure) -----> DEL-013-05
PKG-015 (Electrical) <---> DEL-013-05
DEL-013-03 (Makeup) <----> DEL-013-05
DEL-013-04 (Equip Exh) <-> DEL-013-05
DEL-013-01 (Heating) <--?- DEL-013-05 (ASSUMPTION)
                              |
                              v
                    DEL-013-03 (exhaust CFM handover)
```

---

## Extracted Dependency Register

**Total rows**: 12 (ACTIVE: 12, RETIRED: 0)
**ANCHOR rows**: 3 (IMPLEMENTS_NODE: 1, TRACES_TO_REQUIREMENT: 2)
**EXECUTION rows**: 9 (UPSTREAM: 8, DOWNSTREAM: 1)

| DependencyID | Class | AnchorType | Dir | Type | TargetType | Target | Confidence | Status |
|---|---|---|---|---|---|---|---|---|
| DEP-013-05-001 | ANCHOR | IMPLEMENTS_NODE | UP | OTHER | WBS_NODE | SOW-0039 | HIGH | ACTIVE |
| DEP-013-05-002 | ANCHOR | TRACES_TO_REQ | UP | OTHER | REQUIREMENT | OBJ-001 | HIGH | ACTIVE |
| DEP-013-05-003 | ANCHOR | TRACES_TO_REQ | UP | OTHER | REQUIREMENT | OBJ-004 | HIGH | ACTIVE |
| DEP-013-05-004 | EXECUTION | N/A | UP | INTERFACE | DELIVERABLE | DEL-013-03 (Makeup Air) | HIGH | ACTIVE |
| DEP-013-05-005 | EXECUTION | N/A | UP | INTERFACE | DELIVERABLE | DEL-013-04 (Equip Exhaust) | HIGH | ACTIVE |
| DEP-013-05-006 | EXECUTION | N/A | UP | PREREQUISITE | PACKAGE | PKG-011 (Structure) | HIGH | ACTIVE |
| DEP-013-05-007 | EXECUTION | N/A | UP | INTERFACE | PACKAGE | PKG-015 (Electrical) | HIGH | ACTIVE |
| DEP-013-05-008 | EXECUTION | N/A | UP | PREREQUISITE | EXTERNAL | County Welding Specs | HIGH | ACTIVE |
| DEP-013-05-009 | EXECUTION | N/A | UP | CONSTRAINT | EXTERNAL | AHJ/Environmental Approvals | HIGH | ACTIVE |
| DEP-013-05-010 | EXECUTION | N/A | DOWN | HANDOVER | DELIVERABLE | DEL-013-03 (Makeup Air) | HIGH | ACTIVE |
| DEP-013-05-011 | EXECUTION | N/A | UP | INTERFACE | DELIVERABLE | DEL-013-01 (Heating) | LOW | ACTIVE |
| DEP-013-05-012 | EXECUTION | N/A | UP | PREREQUISITE | EXTERNAL | Welding Station Layout | HIGH | ACTIVE |

---

## Run Notes

**Run date**: 2026-02-26
**Mode**: UPDATE
**Strictness**: CONSERVATIVE
**Consumer context**: TASK_ESTIMATING

### Defaults and paths used
- **ANCHOR_DOC**: Datasheet.md (selected: contains Identification table with SOW Reference and Objective Linkage fields)
- **EXECUTION_DOC_ORDER**: Procedure.md, Specification.md, Guidance.md (selected per DOC_ROLE_MAP heuristic: procedure > specification > guidance for execution signal clarity)
- **SOURCE_DOCS scanned**: Datasheet.md, Specification.md, Procedure.md, Guidance.md
- **DECOMPOSITION_PATH**: /Users/ryan/ai-env/projects/chirality-project-test/test/AB-2026-01424-WDMLRL-2026-Claude/_Decomposition/WDMLRL_Decomposition_Claude.md (R1, 2026-02-25)
- **_REFERENCES.md**: Read; used to corroborate document pointers (R-01, R-04). No additional dependency rows emitted solely from _REFERENCES.md.

### Decomposition validation
- SOW-0039 confirmed in scope ledger (line 144): "Install welding station ventilation/exhaust system", IN scope, mapped to PKG-013 / DEL-013-05
- OBJ-001 confirmed in objectives table (line 302): "Deliver a code-compliant, fully functional maintenance shop..."
- OBJ-004 confirmed in objectives table (line 305): "Install and commission all mechanical, plumbing, and water storage systems to operational readiness"
- DEL-013-03 confirmed: Forced-Air Makeup System, PKG-013
- DEL-013-04 confirmed: Heavy Equipment Exhaust System, PKG-013
- DEL-013-01 confirmed: High-Recovery Heating System, PKG-013
- PKG-011 confirmed: Building Structure & Envelope
- PKG-015 confirmed: Electrical & Low-Voltage Installation

### Warnings
- None.

### Extraction decisions
- DEL-013-01 heat recovery interface (DEP-013-05-011): Retained at LOW confidence because Datasheet explicitly marks this as "ASSUMPTION: welding exhaust heat recovery integration is an open design question." Per CONSERVATIVE strictness, this is not suppressed but is flagged as ASSUMPTION in Notes and given EstimateImpactClass=INFO.
- DEL-013-02 (Air Exchanger) and DEL-013-06 (Ceiling Fans): Listed in _CONTEXT.md "Related Deliverables" and original _DEPENDENCIES.md but no specific information/artifact transfer is stated in any source document. Per information-flow-only extraction rules, no execution edges emitted. These are structural adjacency within PKG-013, not dependency edges.
- DEL-013-03 appears in both UPSTREAM (DEP-013-05-004, INTERFACE) and DOWNSTREAM (DEP-013-05-010, HANDOVER) rows. These are distinct edges: the INTERFACE captures the need for coordination data FROM DEL-013-03; the HANDOVER captures the exhaust CFM data flow TO DEL-013-03 for sizing.
- County welding equipment specs (DEP-013-05-008) and welding station layout finalization (DEP-013-05-012) are recorded as separate EXTERNAL PREREQUISITE edges because they are distinct information items from potentially different sources (County vs. project team/County combined).

---

## Run History

| Run | Date | Mode | Strictness | Decomposition | Warnings | ACTIVE Count |
|---|---|---|---|---|---|---|
| 1 | 2026-02-26 | UPDATE | CONSERVATIVE | WDMLRL_Decomposition_Claude.md (R1) | None | 12 |

---

## Lifecycle Summary

| Status | Count |
|---|---|
| ACTIVE | 12 |
| RETIRED | 0 |

| SatisfactionStatus | Count |
|---|---|
| NOT_APPLICABLE | 3 |
| TBD | 9 |

| DependencyClass | ACTIVE | RETIRED |
|---|---|---|
| ANCHOR | 3 | 0 |
| EXECUTION | 9 | 0 |

| EstimateImpactClass | Count |
|---|---|
| BLOCKING | 5 |
| ADVISORY | 2 |
| INFO | 1 |
| (not set -- ANCHOR rows) | 3 |
| (not set -- N/A) | 1 |

---

## Downstream Handoff Notes (CONSUMER_CONTEXT: TASK_ESTIMATING)

### Estimating-critical dependencies

The following EXECUTION dependencies are classified as **BLOCKING** for estimating readiness, meaning that scope or key quantities cannot be confidently estimated without resolution of these dependencies:

1. **DEP-013-05-008** -- County Welding Equipment Specifications (EXTERNAL PREREQUISITE). The welding process type and base metals directly determine fume character, capture velocity requirements, hood type, filtration specification, and fan sizing. Without this input, all major equipment selections are TBD.

2. **DEP-013-05-012** -- Welding Station Layout Finalization (EXTERNAL PREREQUISITE). The number and location of welding stations drives hood quantity, ductwork length and routing, and system capacity. Currently TBD.

3. **DEP-013-05-009** -- AHJ and Environmental Authority Approvals (EXTERNAL CONSTRAINT). Exhaust stack location and height requirements affect building envelope penetration design and may affect filtration requirements if EPEA discharge requirements apply.

4. **DEP-013-05-006** -- PKG-011 IFC Structural/Envelope Drawings (PACKAGE PREREQUISITE). Penetration details and structural coordination required before installation scope can be fully quantified.

5. **DEP-013-05-004** -- DEL-013-03 Makeup Air Coordination (DELIVERABLE INTERFACE). Exhaust CFM must be coordinated with makeup air capacity. Changes to exhaust volume directly affect makeup air system sizing and therefore cost.

### Advisory dependencies

6. **DEP-013-05-005** -- DEL-013-04 Equipment Exhaust Coordination (DELIVERABLE INTERFACE). Aggregate exhaust volume affects duct routing and potentially fan/stack sizing but is unlikely to gate estimating completely.

7. **DEP-013-05-007** -- PKG-015 Electrical Coordination (PACKAGE INTERFACE). Motor power circuit and controls wiring are standard items unlikely to change the estimate significantly but require coordination.

### Estimating assumptions to track

- Welding station count: assumed 1 per R-04 (Appendix B) until County confirms otherwise (CT-002).
- Filtration type: TBD; assumed exhaust-to-exterior (not recirculating) per default (CT-003).
- All major equipment parameters (CFM, fan size, filtration efficiency, ductwork material) are TBD pending design.
- The estimate should carry appropriate contingency for TBD design parameters.
