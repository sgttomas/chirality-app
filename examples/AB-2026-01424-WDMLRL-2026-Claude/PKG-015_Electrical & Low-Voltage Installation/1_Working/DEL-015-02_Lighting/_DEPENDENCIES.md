# DEL-015-02_Lighting Dependencies

## Dependency Status
**Tracking**: ACTIVE
**RegisterSchemaVersion**: v3.1

## Upstream Dependencies
- DEL-015-01: Three-Phase Power Service (electrical supply) -- must be installed and approved before lighting energization
- Building structure and ceiling completion (DEL-011-01, external prerequisite)

## Downstream Dependencies
- DEL-020-01: Building Systems Commissioning (lighting close-out package and commissioning test record)

---

## Extracted Dependency Register

**Total rows:** 16
**ACTIVE:** 16 | **RETIRED:** 0

### ANCHOR rows (8 ACTIVE)

| DependencyID | AnchorType | TargetType | TargetRefID / TargetName | Confidence |
|---|---|---|---|---|
| DEP-015-02-001 | IMPLEMENTS_NODE | WBS_NODE | PKG-015 -- Electrical & Low-Voltage Installation | HIGH |
| DEP-015-02-002 | TRACES_TO_REQUIREMENT | REQUIREMENT | SOW-0052 -- Main Shop lighting | HIGH |
| DEP-015-02-003 | TRACES_TO_REQUIREMENT | REQUIREMENT | SOW-0053 -- Wash Bay lighting | HIGH |
| DEP-015-02-004 | TRACES_TO_REQUIREMENT | REQUIREMENT | SOW-0054 -- Office lighting | HIGH |
| DEP-015-02-005 | TRACES_TO_REQUIREMENT | REQUIREMENT | SOW-0055 -- Utility Room lighting | HIGH |
| DEP-015-02-006 | TRACES_TO_REQUIREMENT | REQUIREMENT | SOW-0056 -- Parts/Tool Room lighting | HIGH |
| DEP-015-02-007 | TRACES_TO_REQUIREMENT | REQUIREMENT | OBJ-001 -- Core installation objectives | HIGH |
| DEP-015-02-008 | TRACES_TO_REQUIREMENT | REQUIREMENT | OBJ-005 -- Electrical systems readiness | HIGH |

### EXECUTION rows (8 ACTIVE)

| DependencyID | Direction | DependencyType | TargetDeliverableID | TargetName | EstimateImpactClass |
|---|---|---|---|---|---|
| DEP-015-02-009 | UPSTREAM | PREREQUISITE | DEL-015-01 | Three-Phase Power Service | BLOCKING |
| DEP-015-02-010 | UPSTREAM | PREREQUISITE | DEL-004-04 | Lighting Plans (IFC Drawings) | BLOCKING |
| DEP-015-02-011 | UPSTREAM | CONSTRAINT | DEL-009-03 | Safety Code Permits | BLOCKING |
| DEP-015-02-012 | UPSTREAM | PREREQUISITE | DEL-011-01 | Concrete Superstructure | BLOCKING |
| DEP-015-02-013 | UPSTREAM | INTERFACE | DEL-016-01 | Two 5-Tonne Overhead Cranes | ADVISORY |
| DEP-015-02-014 | UPSTREAM | INTERFACE | DEL-013-06 | Ceiling Fans | ADVISORY |
| DEP-015-02-015 | UPSTREAM | PREREQUISITE | DEL-004-06 | Panel Schedules | ADVISORY |
| DEP-015-02-016 | DOWNSTREAM | HANDOVER | DEL-020-01 | Building Systems Commissioning | INFO |

---

## Run Notes

**Run timestamp:** 2026-02-26
**Mode:** UPDATE
**Strictness:** CONSERVATIVE
**Consumer context:** TASK_ESTIMATING

### Defaults and Paths Used

| Setting | Value | Reason |
|---|---|---|
| RUN_ROOT | /Users/ryan/ai-env/projects/chirality-project-test/test/AB-2026-01424-WDMLRL-2026-Claude | Provided by invoker |
| DECOMPOSITION_PATH | _Decomposition/WDMLRL_Decomposition_Claude.md | Provided by invoker; file exists and was used for anchor validation and target resolution |
| SOURCE_DOCS | AUTO | Scanned deliverable folder; identified 4 candidate source documents |
| ANCHOR_DOC | Datasheet.md | Selected via DEFAULT heuristic (filename contains "datasheet"); highest-confidence anchor signal source |
| EXECUTION_DOC_ORDER | Procedure.md, Specification.md, Guidance.md | Procedure selected first (filename contains "procedure"); Specification second (contains "spec"); Guidance third (contains "guidance") |
| _REFERENCES.md | Present and read | Used to cross-reference document pointers; no dependency rows emitted solely from _REFERENCES.md |

### Assumptions and Decisions

1. **Parent anchor target:** PKG-015 selected as the IMPLEMENTS_NODE target because DEL-015-02 is a deliverable within package PKG-015, and the Datasheet explicitly identifies Package ID = PKG-015.

2. **SOW traces:** Five SOW trace rows emitted (SOW-0052 through SOW-0056) matching the explicit "Related SOWs" field in Datasheet Identification. All confirmed in decomposition scope ledger.

3. **Objective traces:** Two objective trace rows (OBJ-001, OBJ-005) emitted from Datasheet "Objectives Addressed" field. Both confirmed in decomposition.

4. **DEL-004-04 resolution:** Procedure P-1 requires "IFC electrical drawings for the lighting system." Resolved to DEL-004-04 (Lighting Plans) via decomposition line 412. DEL-004-04 is the most specific deliverable for lighting IFC drawings.

5. **DEL-004-06 resolution:** Procedure Step 9 requires panel schedule data. Resolved to DEL-004-06 (Panel Schedules) via decomposition line 414. Marked ADVISORY rather than BLOCKING because the panel schedule is needed at the termination phase (Phase 4), not at project start, and the primary IFC dependency (DEL-004-04) already gates Phase 1.

6. **DEL-009-03 resolution:** Procedure P-2 requires Safety Code Permit. Resolved to DEL-009-03 (Safety Code Permits) via decomposition line 468.

7. **DEL-011-01 resolution:** Procedure P-3 requires building structure/ceiling completion. Resolved to DEL-011-01 (Concrete Superstructure) via decomposition line 481. This is the most specific structural deliverable for the ceiling/structure prerequisite.

8. **DEL-016-01 resolution:** Procedure P-6 requires crane shop drawings from PKG-016. Resolved to DEL-016-01 (Two 5-Tonne Overhead Cranes) via decomposition line 533.

9. **DEL-013-06 resolution:** Procedure Step 3a requires ceiling fan mounting location coordination. Resolved to DEL-013-06 (Ceiling Fans, PKG-013) via decomposition line 506. Confidence MEDIUM because the ceiling fan scope ownership is itself unresolved (Guidance CONF-L-03).

10. **DEL-020-01 downstream:** Procedure Step 14 produces a close-out package. DEL-020-01 (Building Systems Commissioning) is identified in decomposition as dependent on all installation packages. Confidence MEDIUM because the direct consumption relationship is inferred from decomposition structure rather than a single explicit statement.

11. **Not extracted -- DEL-015-03 (Receptacles):** Referenced in Specification Out of Scope and _REFERENCES.md as "coordinated layout," but no explicit information/artifact transfer is stated. Excluded per information-flow-only rule.

12. **Not extracted -- DEL-015-04 (Equipment Power):** Referenced in Specification REQ-L-12 alongside PKG-016 for crane clearance, but the dependency is on the crane data itself (captured via DEL-016-01), not on DEL-015-04 outputs. Excluded per information-flow-only rule.

### Warnings

No warnings. All integrity checks pass:
- Exactly 1 ACTIVE IMPLEMENTS_NODE parent anchor (no FLOATING_NODE, no AMBIGUOUS_ANCHOR)
- All ACTIVE rows have EvidenceFile and SourceRef
- All DependencyIDs are unique
- All FromDeliverableID values = DEL-015-02
- TargetDeliverableID populated only for TargetType=DELIVERABLE rows
- TargetRefID populated only for non-DELIVERABLE target types
- All enums are canonical write-form values

---

## Run History

| Timestamp | Mode | Strictness | Decomposition | Warnings | ACTIVE ANCHOR | ACTIVE EXECUTION | RETIRED |
|---|---|---|---|---|---|---|---|
| 2026-02-26 | UPDATE | CONSERVATIVE | WDMLRL_Decomposition_Claude.md (available, used) | None | 8 | 8 | 0 |

---

## Lifecycle Summary

| Metric | Count |
|---|---|
| Total rows | 16 |
| ACTIVE | 16 |
| RETIRED | 0 |

### Closure-state breakdown (ACTIVE rows)

| SatisfactionStatus | Count |
|---|---|
| TBD | 9 |
| PENDING | 7 |

**Notes:** ANCHOR rows are set to SatisfactionStatus=TBD (traceability links do not have a satisfaction gate). EXECUTION UPSTREAM rows are set to PENDING (prerequisites/constraints/interfaces are identified but not yet fulfilled). The downstream HANDOVER row (DEP-015-02-016) is TBD.

---

## Downstream Handoff Notes

**Consumer context:** TASK_ESTIMATING

### Estimating-relevant observations

1. **Four BLOCKING upstream dependencies** gate meaningful estimating progress:
   - **DEL-015-01** (Three-Phase Power Service): Without confirmed power availability, the electrical scope cannot be energized. However, fixture procurement and rough-in can be estimated independently of power service status.
   - **DEL-004-04** (Lighting Plans / IFC Drawings): This is the primary estimating gate. Until IFC drawings are issued, the following remain TBD and cannot be estimated: mounting method for all zones, Wash Bay fixture wattage/lumens, conduit type, circuit assignments, panel schedules, circuit breaker sizes, switching/controls strategy. See Datasheet "Unresolved Design Parameters Register" for the complete list of 8 TBD parameters.
   - **DEL-009-03** (Safety Code Permits): Permit status affects schedule but does not directly change quantity estimates.
   - **DEL-011-01** (Concrete Superstructure): Building structure completion is a sequencing constraint; it does not affect lighting quantities but determines installation timing.

2. **Two ADVISORY upstream interfaces** may affect estimating:
   - **DEL-016-01** (Crane shop drawings): Crane clearance data may affect fixture mounting hardware selection and suspension lengths in the Main Shop.
   - **DEL-013-06** (Ceiling Fans): Fan location coordination may affect fixture positioning but not quantities.

3. **Estimating readiness assessment:** The lighting deliverable has well-defined fixture counts (35 total across 5 zones) sourced from explicit SOWs. The Main Shop high-bay specification (150W / 22,000 lm) is explicit. Rough estimating of fixture procurement and basic installation labor is feasible now. However, precise estimating of the following line items requires IFC drawings (DEL-004-04):
   - Branch circuit wiring (conduit type, lengths, conductor sizing)
   - Mounting hardware (method and materials for each zone)
   - Switching/controls devices
   - Wash Bay fixture specification (wattage/lumen TBD)
   - Panel capacity allocation

4. **Scope uncertainties affecting estimates:**
   - Emergency/exit lighting scope is unresolved (CONF-L-02) -- if included, adds fixtures, wiring, and battery backup units
   - Ceiling fan coordination interface is unresolved (CONF-L-03) -- if fans change fixture layout, rework risk exists
