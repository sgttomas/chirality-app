# Dependencies: DEL-001-05 Interior Elevations

## Coordination (human-owned)
- **Mode:** NOT_TRACKED
- **Notes:** Coordination representation pending -- to be confirmed by human via ORCHESTRATOR.

## Upstream (I need these before I can proceed) -- human-owned declarations
- Dependencies coordinated externally by humans.

## Downstream (These need me) -- human-owned declarations
- Dependencies coordinated externally by humans.

## Extracted Dependency Register

- **Status:** POPULATED
- **Dependencies.csv:** Dependencies.csv (v3.1 schema; 18 rows)
- **Last Run:** 2026-02-26
- **ACTIVE rows:** 18 (3 ANCHOR + 15 EXECUTION)
- **RETIRED rows:** 0

### ANCHOR Edges (3 ACTIVE)

| DependencyID | AnchorType | TargetRefID | TargetName | Confidence |
|---|---|---|---|---|
| DEP-001-05-A01 | IMPLEMENTS_NODE | SOW-0011 | Complete final architectural design for the addition | HIGH |
| DEP-001-05-A02 | TRACES_TO_REQUIREMENT | OBJ-001 | Deliver a code-compliant, fully functional maintenance shop addition | HIGH |
| DEP-001-05-A03 | TRACES_TO_REQUIREMENT | OBJ-003 | Produce complete P.Eng.-stamped IFC design documentation | HIGH |

### EXECUTION Edges (15 ACTIVE)

| DependencyID | Direction | Type | TargetType | Target | Confidence | EstimateImpact |
|---|---|---|---|---|---|---|
| DEP-001-05-E01 | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-001-01 Preliminary Architectural Design | HIGH | BLOCKING |
| DEP-001-05-E02 | UPSTREAM | INTERFACE | DELIVERABLE | DEL-001-02 Architectural Floor Plans | HIGH | ADVISORY |
| DEP-001-05-E03 | UPSTREAM | INTERFACE | DELIVERABLE | DEL-002-07 Crane Support Structure Details | HIGH | ADVISORY |
| DEP-001-05-E04 | UPSTREAM | INTERFACE | DELIVERABLE | DEL-003-04 Exhaust System Plans | HIGH | ADVISORY |
| DEP-001-05-E05 | UPSTREAM | INTERFACE | DELIVERABLE | DEL-006-02 Water Distribution Plans | HIGH | ADVISORY |
| DEP-001-05-E06 | UPSTREAM | INTERFACE | DELIVERABLE | DEL-001-04 Building Sections | HIGH | ADVISORY |
| DEP-001-05-E07 | UPSTREAM | INTERFACE | DELIVERABLE | DEL-002-05 Mezzanine Framing Details | HIGH | ADVISORY |
| DEP-001-05-E08 | UPSTREAM | INTERFACE | DELIVERABLE | DEL-002-06 Service Pit / Trench Structural Details | HIGH | ADVISORY |
| DEP-001-05-E09 | UPSTREAM | INTERFACE | DELIVERABLE | DEL-002-08 Steel Plate Embedment Plan | MEDIUM | INFO |
| DEP-001-05-E10 | UPSTREAM | INTERFACE | DELIVERABLE | DEL-004-05 Receptacle Layout Plans | MEDIUM | ADVISORY |
| DEP-001-05-E11 | DOWNSTREAM | INTERFACE | DELIVERABLE | DEL-001-07 Door & Window Schedule | HIGH | INFO |
| DEP-001-05-E12 | UPSTREAM | INTERFACE | DELIVERABLE | DEL-001-08 Finish Schedule | HIGH | ADVISORY |
| DEP-001-05-E13 | UPSTREAM | INTERFACE | DELIVERABLE | DEL-001-10 Old North Shop Renovation Plans | MEDIUM | ADVISORY |
| DEP-001-05-E14 | UPSTREAM | INTERFACE | DELIVERABLE | DEL-001-11 Architectural Specification | MEDIUM | ADVISORY |
| DEP-001-05-E15 | UPSTREAM | CONSTRAINT | DOCUMENT | Alberta Safety Codes and applicable building codes | HIGH | BLOCKING |

## Run Notes

### Defaults and Paths Used
- **SCOPE:** DEL-001-05_Interior-Elevations
- **RUN_ROOT:** /Users/ryan/ai-env/projects/chirality-project-test/test/AB-2026-01424-WDMLRL-2026-Claude/PKG-001_Architectural Design/1_Working/DEL-001-05_Interior-Elevations
- **DECOMPOSITION_PATH:** /Users/ryan/ai-env/projects/chirality-project-test/test/AB-2026-01424-WDMLRL-2026-Claude/_Decomposition/WDMLRL_Decomposition_Claude.md (found and validated)
- **MODE:** UPDATE
- **STRICTNESS:** CONSERVATIVE
- **CONSUMER_CONTEXT:** TASK_ESTIMATING
- **SOURCE_DOCS:** AUTO -- scanned deliverable folder; identified 4 source documents
- **ANCHOR_DOC:** Datasheet.md (AUTO -- selected by heuristic: contains "datasheet" in filename)
- **EXECUTION_DOC_ORDER:** Procedure.md, Specification.md, Guidance.md (AUTO -- ordered by workflow clarity heuristic)
- **_REFERENCES.md:** Present; used for document location resolution (R-01, R-04 mapped to _Sources/)

### Assumptions and Decisions
- All ANCHOR rows confirmed against decomposition §7 PKG-001 deliverable table. SOW-0011 confirmed as the parent scope item; OBJ-001 and OBJ-003 confirmed as traced objectives.
- DEL-003-04 (Exhaust System Plans) selected as best-fit target for mechanical exhaust coordination (PKG-003). Procedure references PKG-003 broadly; Specification REQ-010 specifically references welding station ventilation coordination with mechanical design. DEL-003-04 is the exhaust-specific deliverable in decomposition.
- DEL-006-02 (Water Distribution Plans) selected as best-fit target for plumbing washroom coordination (PKG-006). Procedure references PKG-006 broadly; Specification REQ-009 specifically references plumbing rough-in. DEL-006-02 covers water distribution including fixture supply.
- DEL-004-05 (Receptacle Layout Plans) selected as best-fit target for electrical coordination (PKG-004). Procedure prerequisites explicitly require receptacle heights, switch locations, and wall-mounted equipment locations. DEL-004-05 covers receptacle layout.
- DEP-001-05-E11 (DEL-001-07) is DOWNSTREAM because interior elevations produce door/opening tags that are consumed by the door schedule. The relationship is bidirectional in practice, but the primary information flow captured here is the elevation-to-schedule tag assignment per REQ-007.
- DEP-001-05-E15 (Alberta Safety Codes) is typed as CONSTRAINT/DOCUMENT because it represents an explicit external compliance requirement (REQ-002) rather than an inter-deliverable data transfer. Specific code edition is TBD per Specification Standards table.
- Mechanical make-up air unit clearance (Procedure Step 2.3) was not given a separate row because DEL-003-04 (E04) already captures the mechanical coordination interface. The make-up air unit is part of the broader mechanical coordination covered by that row.
- Plumbing drain/vent coordination (wash bay mud sump, floor drains) was not given a separate row because DEL-006-02 (E05) captures the primary plumbing interface. The drain/vent scope overlaps with DEL-006-03 but the primary fixture/supply coordination is through DEL-006-02.

### Warnings
- None.

### Quality Check Results
- Schema: PASS -- all required columns present; CSV parseable; RegisterSchemaVersion = v3.1 on all rows.
- DependencyID uniqueness: PASS -- 18 unique IDs.
- Evidence coverage: PASS -- all ACTIVE rows have EvidenceFile and SourceRef populated.
- Enum normalization: PASS -- all enums in canonical write form.
- Parent anchor check: PASS -- exactly 1 ACTIVE IMPLEMENTS_NODE row (DEP-001-05-A01).
- _DEPENDENCIES.md consistency: PASS -- counts match CSV (18 ACTIVE, 0 RETIRED).

## Run History

| Timestamp | Mode | Strictness | DecompositionStatus | Warnings | ACTIVE_ANCHOR | ACTIVE_EXECUTION | RETIRED |
|---|---|---|---|---|---|---|---|
| 2026-02-26 | UPDATE | CONSERVATIVE | Found and validated | None | 3 | 15 | 0 |

## Lifecycle Summary

- **ACTIVE:** 18 (3 ANCHOR + 15 EXECUTION)
- **RETIRED:** 0

### Closure State Breakdown (ACTIVE rows)

| SatisfactionStatus | Count |
|---|---|
| TBD | 18 |

All satisfaction statuses are TBD as this is an initial extraction run. Downstream workflows (estimating, scheduling) will update satisfaction status as prerequisites are met and interfaces are fulfilled.

## Downstream Handoff Notes

**Consumer Context: TASK_ESTIMATING**

The following observations are relevant for task estimating consumers:

1. **BLOCKING dependencies (2 rows):**
   - DEP-001-05-E01: County approval of DEL-001-01 (Preliminary Architectural Design) gates IFC issuance. Until preliminary design is approved, the scope and quantities for interior elevations cannot be finalized. This is the single hardest gate for this deliverable.
   - DEP-001-05-E15: Alberta Safety Codes compliance (REQ-002). The specific code edition is TBD (see Specification Standards table). Code requirements may affect scope (e.g., barrier-free requirements per REQ-013, guardrail height per REQ-015). Until code edition is confirmed with AHJ, some design parameters remain uncertain.

2. **ADVISORY dependencies (13 rows):**
   - Structural inputs (DEL-002-05, DEL-002-06, DEL-002-07): Crane rail elevation, mezzanine deck elevation, and service trench depth are critical coordination inputs per Procedure Step 4 readiness gate. These do not block estimating of the drawing production effort itself, but may affect revision cycles if received late.
   - Architectural companion deliverables (DEL-001-02, DEL-001-04, DEL-001-08, DEL-001-10, DEL-001-11): These are same-package deliverables that are typically developed in parallel. Estimating should assume concurrent development with coordination cycles.
   - Mechanical/Electrical/Plumbing inputs (DEL-003-04, DEL-004-05, DEL-006-02): Cross-discipline coordination inputs. These are advisory because the interior elevations can be drafted with placeholder penetration zones, but coordination review (Procedure Step 5) requires these inputs to be sufficiently advanced.
   - DEL-002-08 (Steel Plate Embedment Plan): INFO-level impact; affects floor-level detail only where steel plate edges meet wall conditions.

3. **Estimating considerations:**
   - The number of drawing sheets is TBD (Datasheet). The room list compilation (Procedure Step 1) and coordination cycle count are the primary drivers of production effort.
   - Two open conflicts (CFT-001-05-01, CFT-001-05-02) may affect scope if resolved in a way that adds or changes interior elevation views.
   - The Old North Shop renovation scope boundary for interior elevations is TBD (Guidance Principle 4 note). This may add or reduce sheets.
