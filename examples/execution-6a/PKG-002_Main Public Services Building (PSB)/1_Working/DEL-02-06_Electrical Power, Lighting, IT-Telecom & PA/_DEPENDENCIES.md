# Dependencies: DEL-02-06 Electrical Power, Lighting, IT/Telecom & PA

## Coordination (human-owned)
- **Mode:** DECLARED
- **Notes:** See _Coordination/_COORDINATION.md for project-level coordination record.

## Upstream (I need these before I can proceed) -- human-owned declarations
- No upstream dependencies declared yet.

## Downstream (These need me) -- human-owned declarations
- No downstream dependencies declared yet.

## Extracted Dependency Register

- **Status:** COMPLETE
- **Dependencies.csv:** Dependencies.csv (19 rows)
- **Schema Version:** v3.1
- **Summary:**
  - **ANCHOR rows:** 10 (1 IMPLEMENTS_NODE + 7 TRACES_TO_REQUIREMENT for SOW items + 2 TRACES_TO_REQUIREMENT for objectives)
  - **EXECUTION rows:** 9 (7 UPSTREAM + 2 DOWNSTREAM)
  - **All rows ACTIVE**

### ANCHOR Edges (Tree -- Definition Traceability)

| DependencyID | AnchorType | TargetType | TargetName | Confidence |
|---|---|---|---|---|
| DEP-0206-A01 | IMPLEMENTS_NODE | WBS_NODE | PKG-002 -- Main Public Services Building (PSB) | HIGH |
| DEP-0206-A02 | TRACES_TO_REQUIREMENT | REQUIREMENT | SOW-0224 | HIGH |
| DEP-0206-A03 | TRACES_TO_REQUIREMENT | REQUIREMENT | SOW-0225 | HIGH |
| DEP-0206-A04 | TRACES_TO_REQUIREMENT | REQUIREMENT | SOW-0226 | HIGH |
| DEP-0206-A05 | TRACES_TO_REQUIREMENT | REQUIREMENT | SOW-0227 | HIGH |
| DEP-0206-A06 | TRACES_TO_REQUIREMENT | REQUIREMENT | SOW-0228 | HIGH |
| DEP-0206-A07 | TRACES_TO_REQUIREMENT | REQUIREMENT | SOW-0203 (partial) | HIGH |
| DEP-0206-A08 | TRACES_TO_REQUIREMENT | REQUIREMENT | SOW-0208 (partial) | HIGH |
| DEP-0206-A09 | TRACES_TO_REQUIREMENT | REQUIREMENT | OBJ-001 | HIGH |
| DEP-0206-A10 | TRACES_TO_REQUIREMENT | REQUIREMENT | OBJ-002 | HIGH |

### EXECUTION Edges (DAG -- Information Flow)

| DependencyID | Direction | DependencyType | TargetType | Target | Statement Summary |
|---|---|---|---|---|---|
| DEP-0206-E01 | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-02-01 (Architectural Program) | Floor plan, room schedule, IT room location/sizing -- blocking |
| DEP-0206-E02 | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-02-02 (Firehall Apparatus Bays) | Apparatus bay layout for electrical service location |
| DEP-0206-E03 | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-02-05 (Mechanical/Plumbing) | HVAC loads and door opener electrical requirements |
| DEP-0206-E04 | UPSTREAM | INTERFACE | DELIVERABLE | DEL-02-07 (Emergency Power) | ATS location and essential loads list coordination |
| DEP-0206-E05 | DOWNSTREAM | HANDOVER | DELIVERABLE | DEL-02-07 (Emergency Power) | Essential/non-essential load classification (R-17) |
| DEP-0206-E06 | UPSTREAM | INTERFACE | DELIVERABLE | DEL-03-04 (Site Utilities) | External electrical service from site utility tie-ins |
| DEP-0206-E07 | UPSTREAM | INTERFACE | DELIVERABLE | DEL-02-04 (Structure/Envelope) | Ceiling height and structural clearance for fixture mounting |
| DEP-0206-E08 | UPSTREAM | PREREQUISITE | DOCUMENT | Functional Program (Appendix B) | Meeting room EM workstation layout -- blocking for Step A-7 |
| DEP-0206-E09 | DOWNSTREAM | HANDOVER | DELIVERABLE | DEL-01-07 (Commissioning/Closeout) | Commissioning of electrical/lighting/IT/PA systems |

## Run Notes

### Run: 2026-02-17

- **Mode:** UPDATE
- **Strictness:** CONSERVATIVE
- **Consumer Context:** NONE
- **Decomposition Path:** `_Decomposition/Penhold_PSB_Project_Decomposition_FINAL_v1.0_PHASE7.md` (located and used)
- **Source Documents (AUTO):**
  - ANCHOR_DOC: `Datasheet.md` (selected: contains identification, scope coverage, and objective support fields)
  - EXECUTION_DOCS (ordered): `Procedure.md`, `Specification.md`, `Guidance.md`
- **_REFERENCES.md:** Read; used to confirm Functional Program (Appendix B) document pointer
- **Defaults applied:** SOURCE_DOCS=AUTO, ANCHOR_DOC=AUTO, EXECUTION_DOC_ORDER=AUTO

### Assumptions and Warnings

- No warnings. Decomposition was located and used for anchor validation and label resolution.
- Parent anchor (IMPLEMENTS_NODE) count: 1. Check PASSED.
- All anchor identifiers (SOW-0203, SOW-0208, SOW-0224-0228, OBJ-001, OBJ-002) confirmed present in decomposition scope ledger.
- DEL-02-07 interface is bidirectional: DEL-02-06 receives ATS location/essential loads list (UPSTREAM) and provides load classification (DOWNSTREAM via R-17).
- Functional Program (Appendix B) is listed as a blocking prerequisite but its location remains TBD per _REFERENCES.md and Procedure.

## Run History

| Timestamp | Mode | Strictness | DecompositionStatus | Warnings | ACTIVE_ANCHOR | ACTIVE_EXECUTION | Total_ACTIVE |
|---|---|---|---|---|---|---|---|
| 2026-02-17 | UPDATE | CONSERVATIVE | Located and used (v1.0 PHASE7) | None | 10 | 9 | 19 |

## Lifecycle Summary

- **ACTIVE:** 19 (10 ANCHOR + 9 EXECUTION)
- **RETIRED:** 0
- **SatisfactionStatus breakdown (EXECUTION rows):**
  - TBD: 9
  - SATISFIED: 0
  - PENDING: 0
- **SatisfactionStatus breakdown (ANCHOR rows):**
  - NOT_APPLICABLE: 10

## Consumer Handoff Notes (optional)
- Consumer context is NONE; no handoff notes generated.
