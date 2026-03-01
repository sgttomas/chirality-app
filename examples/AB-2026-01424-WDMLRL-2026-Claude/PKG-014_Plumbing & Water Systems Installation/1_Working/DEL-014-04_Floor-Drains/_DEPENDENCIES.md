# DEL-014-04 Floor Drains & Sump Drains — Dependencies

## Dependency Status
**Tracking**: ACTIVE
**RegisterSchemaVersion**: v3.1

---

## Upstream Dependencies

- **DEL-006-03** (Drain & Vent Plans, PKG-006): IFC plumbing drawings required before installation; hold-point declared
- **DEL-014-02** (Septic System, PKG-014): Drainage destination for shop floor and sump drains; connection point required
- **DEL-018-05** (Wash Bay Drainage & Mud Sump, PKG-018): Wash bay drain interface; scope boundary must be formally agreed
- **PKG-011** (General Contractor, Concrete Scope): Mandatory pre-pour coordination; drains must be set before slab pour
- **DEL-014-05** (Emergency Shower, PKG-014): Emergency shower drain sizing depends on shower unit selection
- **DEL-009-03** (Safety Code Permits, PKG-009): Plumbing permit required before installation commences

## Downstream Dependencies

- **DEL-014-06** (Plumbing Fixtures, PKG-014): Washroom drain interface; fixture drainage integration
- **DEL-020-01** (Building Systems Commissioning, PKG-020): Drain systems included in commissioning scope; readiness gate required

---

## Extracted Dependency Register

**Total ACTIVE rows:** 13 (5 ANCHOR + 8 EXECUTION)
**Total RETIRED rows:** 0

### ANCHOR Edges (5)

| DependencyID | AnchorType | TargetType | TargetRefID / TargetName | Confidence |
|---|---|---|---|---|
| DEP-014-04-A01 | IMPLEMENTS_NODE | WBS_NODE | PKG-014 — Plumbing & Water Systems Installation | HIGH |
| DEP-014-04-A02 | TRACES_TO_REQUIREMENT | REQUIREMENT | SOW-0045 | HIGH |
| DEP-014-04-A03 | TRACES_TO_REQUIREMENT | REQUIREMENT | SOW-0046 | HIGH |
| DEP-014-04-A04 | TRACES_TO_REQUIREMENT | REQUIREMENT | OBJ-001 | HIGH |
| DEP-014-04-A05 | TRACES_TO_REQUIREMENT | REQUIREMENT | OBJ-004 | HIGH |

### EXECUTION Edges (8)

| DependencyID | Direction | DependencyType | Target | Confidence | EstimateImpactClass |
|---|---|---|---|---|---|
| DEP-014-04-E01 | UPSTREAM | PREREQUISITE | DEL-006-03 (Drain & Vent Plans) | HIGH | BLOCKING |
| DEP-014-04-E02 | UPSTREAM | INTERFACE | DEL-014-02 (Septic System) | HIGH | ADVISORY |
| DEP-014-04-E03 | UPSTREAM | INTERFACE | DEL-018-05 (Wash Bay Drainage & Mud Sump) | HIGH | BLOCKING |
| DEP-014-04-E04 | UPSTREAM | PREREQUISITE | PKG-011 (General Contractor — Concrete) | HIGH | BLOCKING |
| DEP-014-04-E05 | UPSTREAM | INTERFACE | DEL-014-05 (Emergency Shower) | MEDIUM | ADVISORY |
| DEP-014-04-E06 | UPSTREAM | CONSTRAINT | DEL-009-03 (Safety Code Permits) | HIGH | BLOCKING |
| DEP-014-04-E07 | DOWNSTREAM | INTERFACE | DEL-014-06 (Plumbing Fixtures) | MEDIUM | ADVISORY |
| DEP-014-04-E08 | DOWNSTREAM | HANDOVER | DEL-020-01 (Building Systems Commissioning) | MEDIUM | INFO |

---

## Lifecycle Summary

| Status | Count |
|---|---|
| ACTIVE | 13 |
| RETIRED | 0 |

| SatisfactionStatus | Count |
|---|---|
| NOT_APPLICABLE | 5 (ANCHOR rows) |
| PENDING | 8 (EXECUTION rows) |

---

## Run Notes

**Run timestamp:** 2026-02-26
**Mode:** UPDATE
**Strictness:** CONSERVATIVE
**Consumer context:** TASK_ESTIMATING

**Defaults applied:**
- ANCHOR_DOC: `Datasheet.md` (selected: filename contains "datasheet"; highest-confidence anchor signal)
- EXECUTION_DOC_ORDER: `Procedure.md`, `Specification.md`, `Guidance.md` (selected: filenames match execution doc patterns)
- SOURCE_DOCS: `Datasheet.md`, `Guidance.md`, `Procedure.md`, `Specification.md` (all non-generated source docs in deliverable folder)
- DECOMPOSITION_PATH: `_Decomposition/WDMLRL_Decomposition_Claude.md` (provided by invoker; validated successfully)

**Decomposition validation:** PASSED — DEL-014-04 found at decomposition S7 line 515; PKG-014, SOW-0045, SOW-0046, OBJ-001, OBJ-004 all confirmed.

**Warnings:** None.

**Assumptions logged:**
- None required. All anchor and execution edges are backed by explicit source evidence.

**Estimating impact summary (CONSUMER_CONTEXT=TASK_ESTIMATING):**
- 4 BLOCKING dependencies: DEL-006-03 (IFC drawings), DEL-018-05 (scope boundary), PKG-011 (concrete coordination), DEL-009-03 (permits)
- 3 ADVISORY dependencies: DEL-014-02 (septic interface), DEL-014-05 (emergency shower interface), DEL-014-06 (fixtures interface)
- 1 INFO dependency: DEL-020-01 (commissioning handover)

---

## Run History

| Timestamp | Mode | Strictness | Decomposition | Warnings | ACTIVE Count |
|---|---|---|---|---|---|
| 2026-02-26 | UPDATE | CONSERVATIVE | Validated (WDMLRL_Decomposition_Claude.md) | None | 13 (5A + 8E) |

---

## Downstream Handoff Notes

**Consumer context:** TASK_ESTIMATING

For task estimating purposes, the following dependencies are most significant:

1. **DEL-006-03 (BLOCKING):** IFC plumbing drawings are the single most critical upstream dependency. Until these are available, drain types, sizes, quantities, and routing cannot be finalized. All TBD material/specification attributes in the Datasheet (8 entries) depend on this input. Estimating should treat drain product specifications as TBD until IFC design is available.

2. **DEL-018-05 (BLOCKING):** The wash bay drain scope boundary (CFT-014-04-01) must be resolved to determine which contractor is responsible for the drainage pipe from the interior wash bay drain to the exterior mud sump. This affects quantity takeoff scope.

3. **PKG-011 (BLOCKING):** Concrete slab pour sequencing is a hard constraint. Drain rough-in must be complete and inspected before the slab pour. This affects schedule risk and sequencing.

4. **DEL-009-03 (BLOCKING):** Plumbing permit is a regulatory gate that must be obtained before any installation work begins.

5. **Oil/grease interceptor (CFT-014-04-02):** The requirement for an oil/grease interceptor upstream of the septic connection is TBD. If required, this adds a significant material/installation scope item. This is tracked in Specification REQ-014-04-11 and depends on the Plumbing Engineer's determination via DEL-006-03.
