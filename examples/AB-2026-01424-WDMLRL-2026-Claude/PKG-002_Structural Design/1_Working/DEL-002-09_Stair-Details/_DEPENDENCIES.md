# Dependencies: DEL-002-09 Stair Details

## Coordination (human-owned)
- **Mode:** NOT_TRACKED
- **Notes:** Coordination representation pending -- to be confirmed by human via ORCHESTRATOR.

## Upstream (I need these before I can proceed) -- human-owned declarations
- Dependencies coordinated externally by humans.

## Downstream (These need me) -- human-owned declarations
- Dependencies coordinated externally by humans.

## Extracted Dependency Register

- **Status:** COMPLETE
- **Dependencies.csv:** `Dependencies.csv` (v3.1, 14 rows)
- **Last Run:** 2026-02-26
- **ACTIVE Rows:** 14 (3 ANCHOR, 11 EXECUTION)
- **RETIRED Rows:** 0

### ANCHOR Rows (3)

| DependencyID | AnchorType | TargetRefID | TargetName | Confidence |
|---|---|---|---|---|
| DEP-002-09-A01 | IMPLEMENTS_NODE | SOW-0012 | Complete final structural design | HIGH |
| DEP-002-09-A02 | TRACES_TO_REQUIREMENT | OBJ-001 | Code-compliant fully functional facility | HIGH |
| DEP-002-09-A03 | TRACES_TO_REQUIREMENT | OBJ-003 | Complete P.Eng.-stamped IFC documentation | HIGH |

### EXECUTION Rows (11)

| DependencyID | Direction | DependencyType | TargetType | Target | Confidence | EstimateImpactClass |
|---|---|---|---|---|---|---|
| DEP-002-09-E01 | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-002-05 Mezzanine Framing Details | HIGH | BLOCKING |
| DEP-002-09-E02 | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-002-03 Structural Framing Plans | HIGH | BLOCKING |
| DEP-002-09-E03 | UPSTREAM | INTERFACE | DELIVERABLE | DEL-002-10 Structural Calculation Package | HIGH | ADVISORY |
| DEP-002-09-E04 | DOWNSTREAM | HANDOVER | DELIVERABLE | DEL-011-07 Mezzanine Structure & Stairs | HIGH | BLOCKING |
| DEP-002-09-E05 | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-008-01 Geotechnical Investigation & Report | HIGH | BLOCKING |
| DEP-002-09-E06 | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-002-08 Steel Plate Embedment Plan | MEDIUM | ADVISORY |
| DEP-002-09-E07 | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-001-02 Architectural Floor Plans | HIGH | BLOCKING |
| DEP-002-09-E08 | UPSTREAM | CONSTRAINT | DELIVERABLE | DEL-002-01 Preliminary Structural Design | HIGH | BLOCKING |
| DEP-002-09-E09 | UPSTREAM | INTERFACE | DELIVERABLE | DEL-002-12 Structural Specification | MEDIUM | ADVISORY |
| DEP-002-09-E10 | UPSTREAM | PREREQUISITE | DOCUMENT | Alberta Building Code (current edition) | HIGH | BLOCKING |
| DEP-002-09-E11 | UPSTREAM | INTERFACE | DELIVERABLE | DEL-002-04 Structural Sections & Details | MEDIUM | ADVISORY |

## Run Notes

### Run 2026-02-26 (current)

**Parameters:**
- SCOPE: DEL-002-09_Stair-Details
- RUN_ROOT: `/Users/ryan/ai-env/projects/chirality-project-test/test/AB-2026-01424-WDMLRL-2026-Claude/PKG-002_Structural Design/1_Working/DEL-002-09_Stair-Details`
- MODE: UPDATE
- STRICTNESS: CONSERVATIVE
- CONSUMER_CONTEXT: TASK_ESTIMATING
- DECOMPOSITION_PATH: `/Users/ryan/ai-env/projects/chirality-project-test/test/AB-2026-01424-WDMLRL-2026-Claude/_Decomposition/WDMLRL_Decomposition_Claude.md`

**Source document resolution (AUTO):**
- SOURCE_DOCS (AUTO): Datasheet.md, Specification.md, Procedure.md, Guidance.md
- ANCHOR_DOC (AUTO): Datasheet.md (contains Identification table with SOW and OBJ references)
- EXECUTION_DOC_ORDER (AUTO): Procedure.md (explicit prerequisites table), Specification.md (requirements and related deliverables), Guidance.md (principles and considerations), Datasheet.md (construction/references tables)
- _REFERENCES.md: read for document pointer resolution (R-01, R-04)

**Decomposition status:** Available and validated. All target IDs confirmed against decomposition scope ledger, packages, and deliverables tables.

**Existing register:** Prior run had 8 rows (3 ANCHOR, 5 EXECUTION). This run updates to 14 rows (3 ANCHOR, 11 EXECUTION). Prior E01 reclassified from INTERFACE to PREREQUISITE per Procedure prerequisites table evidence. Prior E02 reclassified from INTERFACE to PREREQUISITE per same. 6 new rows added (E05-E11) from Procedure prerequisites, authorization requirements, and cross-reference evidence.

**Assumptions and decisions:**
- DEL-002-08 (E06): Procedure lists this as a prerequisite but Guidance CON-002 notes conditional vs. unconditional ambiguity. Preserved as PREREQUISITE with MEDIUM confidence and ADVISORY impact class until CON-002 is resolved by human ruling.
- Alberta Building Code (E10): Regulatory document, not a project deliverable. Recorded as TargetType=DOCUMENT because it is an explicit required input in the Procedure prerequisites table.
- DEL-002-04 (E11): Listed in Specification Related Deliverables and Datasheet Construction table. Classified as INTERFACE (not PREREQUISITE) because no explicit "required before" language found; it is a coordination/cross-reference relationship with explicit mention.

**Warnings:**
- None. Parent anchor (IMPLEMENTS_NODE) count = 1. No integrity issues detected.

## Run History

| Timestamp | Mode | Strictness | Consumer | Decomposition | Warnings | ACTIVE Count |
|---|---|---|---|---|---|---|
| 2026-02-26 | UPDATE | CONSERVATIVE | TASK_ESTIMATING | Available (WDMLRL_Decomposition_Claude.md R1) | None | 14 (3A + 11E) |

## Lifecycle Summary

| Category | Count |
|---|---|
| **ACTIVE** | 14 |
| **RETIRED** | 0 |
| **Total** | 14 |

### Closure State Breakdown (ACTIVE rows)

| SatisfactionStatus | Count |
|---|---|
| TBD | 14 |
| PENDING | 0 |
| IN_PROGRESS | 0 |
| SATISFIED | 0 |
| WAIVED | 0 |
| NOT_APPLICABLE | 0 |

### By DependencyClass

| Class | ACTIVE | RETIRED |
|---|---|---|
| ANCHOR | 3 | 0 |
| EXECUTION | 11 | 0 |

## Downstream Handoff Notes

**Consumer Context: TASK_ESTIMATING**

The following observations are relevant for downstream task estimating workflows:

### Blocking Dependencies (6 EXECUTION rows with EstimateImpactClass=BLOCKING)

These dependencies gate meaningful estimating. Scope or key quantities cannot be fully established until these inputs are available:

1. **DEP-002-09-E01** -- DEL-002-05 (Mezzanine Framing Details): The mezzanine top landing elevation, framing layout, and connection interface must be known before the stair's total rise, connection type, and top landing detail can be established. Without this, stair geometry, member sizing, and connection quantities are indeterminate.

2. **DEP-002-09-E02** -- DEL-002-03 (Structural Framing Plans): The overall structural grid and slab layout determine where the stair base is located. Without this, the stair footprint cannot be fixed and base anchorage details cannot be designed.

3. **DEP-002-09-E05** -- DEL-008-01 (Geotechnical Investigation & Report): Slab bearing conditions and geotechnical parameters are required for stair base anchor design. Without the geotech report, anchor embedment and base plate design quantities are TBD.

4. **DEP-002-09-E07** -- DEL-001-02 (Architectural Floor Plans): Stair location, clear width, and architectural intent must be confirmed before structural detailing proceeds.

5. **DEP-002-09-E08** -- DEL-002-01 (Preliminary Structural Design): County approval of the preliminary design is an explicit authorization gate (R-01 section 3.3.2) before IFC details can proceed. This is a schedule constraint on IFC issue, not just a technical input.

6. **DEP-002-09-E10** -- Alberta Building Code (current edition): Regulatory document required for stair geometry, live loads, handrail/guardrail requirements. Edition year is TBD (Specification REQ-004 [A-001]).

### Advisory Dependencies (4 EXECUTION rows with EstimateImpactClass=ADVISORY)

These dependencies are likely to influence quantities, specs, or procurement approach but do not hard-gate estimating:

1. **DEP-002-09-E03** -- DEL-002-10 (Structural Calculation Package): Calculations support the stair design but are developed in parallel; the drawing set can be estimated without final calculations if design basis assumptions are established.

2. **DEP-002-09-E06** -- DEL-002-08 (Steel Plate Embedment Plan): Whether a floor embedment exists at the stair base affects anchorage detail type and quantity. Conditional status per CON-002.

3. **DEP-002-09-E09** -- DEL-002-12 (Structural Specification): Material and workmanship standards affect specification callouts on drawings but are unlikely to change overall stair quantity or scope.

4. **DEP-002-09-E11** -- DEL-002-04 (Structural Sections & Details): Overall building sections provide context for stair placement within the building envelope.

### Key TBD Items Affecting Estimating Readiness

- **Stair material** (steel vs. concrete) -- TBD; material selection determines governing design standard (CSA S16 vs. CSA A23.3), fabrication approach, and cost profile. (Datasheet, Guidance C-2)
- **Stair width, tread/riser dimensions, number of runs** -- TBD; dependent on Alberta Building Code and mezzanine elevation. (Datasheet Attributes)
- **Live load design value** -- TBD; dependent on occupancy classification under ABC. (Datasheet Attributes, Specification REQ-002)
- **Guardrail scope boundary** -- TBD; CON-001 unresolved (DEL-002-09 vs. DEL-002-05). (Guidance CON-001)
- **DEL-002-08 required vs. conditional** -- TBD; CON-002 unresolved. (Guidance CON-002)
