# Dependencies: DEL-002-04 Structural Sections & Details

## Coordination (human-owned)
- **Mode:** NOT_TRACKED
- **Notes:** Coordination representation pending — to be confirmed by human via ORCHESTRATOR.

## Upstream (I need these before I can proceed) — human-owned declarations
- Dependencies coordinated externally by humans.

## Downstream (These need me) — human-owned declarations
- Dependencies coordinated externally by humans.

## Extracted Dependency Register

- **Status:** COMPLETE
- **Dependencies.csv:** `Dependencies.csv` (v3.1 schema, 18 rows)
- **Total ACTIVE rows:** 18 (3 ANCHOR + 15 EXECUTION)
- **Total RETIRED rows:** 0

### ANCHOR Rows (3 ACTIVE)

| DependencyID | AnchorType | TargetRefID | TargetName | Confidence |
|---|---|---|---|---|
| DEP-002-04-A01 | IMPLEMENTS_NODE | SOW-0012 | Complete final structural design — concrete structure 35 ft ceiling | HIGH |
| DEP-002-04-A02 | TRACES_TO_REQUIREMENT | OBJ-001 | Code-compliant functional facility | HIGH |
| DEP-002-04-A03 | TRACES_TO_REQUIREMENT | OBJ-003 | Complete P.Eng.-stamped IFC documentation | HIGH |

### EXECUTION Rows (15 ACTIVE)

| DependencyID | Direction | Type | TargetType | Target | Confidence | EstimateImpact |
|---|---|---|---|---|---|---|
| DEP-002-04-E01 | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-002-01 Preliminary Structural Design | HIGH | BLOCKING |
| DEP-002-04-E02 | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-008-01 Geotechnical Investigation & Report | HIGH | BLOCKING |
| DEP-002-04-E03 | UPSTREAM | INTERFACE | DELIVERABLE | DEL-008-02 Preliminary Site Survey | HIGH | ADVISORY |
| DEP-002-04-E04 | UPSTREAM | INTERFACE | DELIVERABLE | DEL-002-03 Structural Framing Plans | HIGH | ADVISORY |
| DEP-002-04-E05 | UPSTREAM | INTERFACE | DELIVERABLE | DEL-002-10 Structural Calculation Package | HIGH | ADVISORY |
| DEP-002-04-E06 | UPSTREAM | INTERFACE | DELIVERABLE | DEL-001-02 Architectural Floor Plans | MEDIUM | ADVISORY |
| DEP-002-04-E07 | UPSTREAM | INTERFACE | EXTERNAL | Crane Supplier Information | HIGH | BLOCKING |
| DEP-002-04-E08 | UPSTREAM | CONSTRAINT | EXTERNAL | County Confirmation — Service Pit Depth | HIGH | BLOCKING |
| DEP-002-04-E09 | UPSTREAM | CONSTRAINT | EXTERNAL | County Confirmation — Mezzanine Design Load | HIGH | BLOCKING |
| DEP-002-04-E10 | UPSTREAM | INTERFACE | DELIVERABLE | DEL-002-02 Foundation Plan | HIGH | ADVISORY |
| DEP-002-04-E11 | UPSTREAM | INTERFACE | DELIVERABLE | DEL-002-12 Structural Specification | MEDIUM | ADVISORY |
| DEP-002-04-E12 | UPSTREAM | INTERFACE | PACKAGE | PKG-003 Mechanical Design | MEDIUM | ADVISORY |
| DEP-002-04-E13 | UPSTREAM | INTERFACE | PACKAGE | PKG-004 Electrical Design | MEDIUM | ADVISORY |
| DEP-002-04-E14 | UPSTREAM | INTERFACE | PACKAGE | PKG-006 Plumbing Design | MEDIUM | ADVISORY |
| DEP-002-04-E15 | UPSTREAM | INTERFACE | PACKAGE | PKG-001 Architectural Design | MEDIUM | ADVISORY |

---

## Run Notes

### Run Parameters
- **Run date:** 2026-02-26
- **MODE:** UPDATE
- **STRICTNESS:** CONSERVATIVE
- **CONSUMER_CONTEXT:** TASK_ESTIMATING
- **SOURCE_DOCS:** AUTO (resolved to: Datasheet.md, Specification.md, Procedure.md, Guidance.md)
- **ANCHOR_DOC:** AUTO (resolved to: Datasheet.md — contains Identification table with SOW/OBJ references)
- **EXECUTION_DOC_ORDER:** AUTO (resolved to: Procedure.md, Specification.md, Guidance.md)
- **DECOMPOSITION_PATH:** `_Decomposition/WDMLRL_Decomposition_Claude.md` (R1 — 2026-02-25)
- **_REFERENCES.md:** Present; lists R-01 and R-04 as applicable references

### Decomposition Validation
- SOW-0012: CONFIRMED in decomposition §3 SSOW (section C — Design Final) and §8 Scope Ledger
- OBJ-001: CONFIRMED in decomposition §5 Objectives
- OBJ-003: CONFIRMED in decomposition §5 Objectives
- DEL-002-01: CONFIRMED in decomposition §7 PKG-002 deliverables
- DEL-002-02: CONFIRMED in decomposition §7 PKG-002 deliverables
- DEL-002-03: CONFIRMED in decomposition §7 PKG-002 deliverables
- DEL-002-10: CONFIRMED in decomposition §7 PKG-002 deliverables
- DEL-002-12: CONFIRMED in decomposition §7 PKG-002 deliverables
- DEL-008-01: CONFIRMED in decomposition §7 PKG-008 deliverables
- DEL-008-02: CONFIRMED in decomposition §7 PKG-008 deliverables
- DEL-001-02: CONFIRMED in decomposition §7 PKG-001 deliverables
- PKG-001, PKG-003, PKG-004, PKG-006: CONFIRMED in decomposition §6 Packages

### Warnings
- None.

### Assumptions
- Multi-discipline coordination interfaces (E12-E15) recorded at package level because source documents name disciplines/packages rather than specific deliverable IDs for penetration drawings.
- DEL-001-02 interface (E06) is distinct from PKG-001 architectural section coordination (E15): E06 covers floor plan room layout inputs; E15 covers section-level wall/door header coordination per Procedure Step 15.

### Decisions
- Existing prior-run rows (DEP-002-04-A01 through DEP-002-04-E06) were renumbered to maintain sequential consistency after adding new rows. Prior E03 (DEL-002-03) became E04; prior E04 (DEL-002-10) became E05; prior E05 (DEL-001-02) became E06; prior E06 (Crane Supplier) became E07. New rows E03, E08-E15 added.
- County Owner inputs (service pit depth, mezzanine load) recorded as EXTERNAL CONSTRAINT rather than DELIVERABLE because they are owner decisions, not deliverables in the decomposition.
- All EXECUTION rows tagged with ConsumerHint=TASK_ESTIMATING per CONSUMER_CONTEXT.
- BLOCKING reserved for hard gates (County approval, geotech, owner confirmations on TBD scope items, crane supplier data). ADVISORY used for parallel-development interfaces.

---

## Run History

| Timestamp | Mode | Strictness | Decomposition | Warnings | ACTIVE Anchors | ACTIVE Execution | Total ACTIVE |
|---|---|---|---|---|---|---|---|
| 2026-02-26 | UPDATE | CONSERVATIVE | WDMLRL_Decomposition_Claude.md (R1) | None | 3 | 15 | 18 |

---

## Lifecycle Summary

### Extraction Lifecycle
- **ACTIVE:** 18 rows (3 ANCHOR + 15 EXECUTION)
- **RETIRED:** 0 rows

### Closure Lifecycle (SatisfactionStatus breakdown — ACTIVE rows only)
- **TBD:** 18
- **PENDING:** 0
- **IN_PROGRESS:** 0
- **SATISFIED:** 0
- **WAIVED:** 0
- **NOT_APPLICABLE:** 0

---

## Downstream Handoff Notes

**Consumer context:** TASK_ESTIMATING

### Estimating-Critical Dependencies (BLOCKING)

The following dependencies are classified as BLOCKING for estimating purposes — scope or key quantities cannot be reliably established without these inputs:

1. **DEP-002-04-E01** — County approval of DEL-002-01 (Preliminary Structural Design). Hard gate per R-01 §3.3.2. Final design (and therefore estimating of final drawing production effort) cannot proceed without this approval.

2. **DEP-002-04-E02** — DEL-008-01 Geotechnical Investigation & Report. Required for foundation and service pit depth determination. Without geotech data, below-grade concrete quantities are estimated on assumption of normal ground conditions per R-01 §4.8.2.

3. **DEP-002-04-E07** — Crane Supplier Information (external). Crane runway beam size, rail type, and end stop requirements are unknown without supplier data. Guidance T-04 proposes a provisional design fallback if supplier data is unavailable, but estimating accuracy is degraded.

4. **DEP-002-04-E08** — County Confirmation of Service Pit Depth. Pit depth is not stated anywhere in RFP or conceptual drawings (CON-002). This directly drives concrete volume, formwork quantity, excavation depth, and waterproofing scope for the service pit structural sections.

5. **DEP-002-04-E09** — County Confirmation of Mezzanine Design Load. Mezzanine live load is described functionally ("heavy items — oil totes, pumping equipment") without a numeric value (CON-001). The structural design and therefore member sizes/reinforcing quantities depend on this value.

### Advisory Dependencies

Remaining EXECUTION dependencies (E03-E06, E10-E15) are ADVISORY: they affect interface completeness and coordination quality but do not gate the estimating of primary structural quantities. Parallel development is expected per standard design-build workflow.

### Estimating Risk Notes

- The construction method decision (cast-in-place vs. tilt-up vs. precast — CON-004 in Guidance.md) is not captured as a formal dependency because it is an internal design decision rather than an external input. However, it fundamentally changes the detail types and production effort for this deliverable. Estimators should confirm the assumed construction method before establishing drawing production hours.
- Steel plate embedment dimensions (thickness, plan size, anchor type) are TBD per CON-003. This affects material quantities for the embedment details but is captured indirectly via the general geotech and owner-confirmation dependencies.
