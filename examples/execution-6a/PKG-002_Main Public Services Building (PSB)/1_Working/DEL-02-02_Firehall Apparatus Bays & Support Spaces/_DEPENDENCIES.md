# Dependencies: DEL-02-02 Firehall Apparatus Bays & Support Spaces

## Coordination (human-owned)
- **Mode:** DECLARED
- **Notes:** See _Coordination/_COORDINATION.md for project-level coordination record.

## Upstream (I need these before I can proceed) -- human-owned declarations
- No upstream dependencies declared yet.

## Downstream (These need me) -- human-owned declarations
- No downstream dependencies declared yet.

## Extracted Dependency Register

- **Status:** EXTRACTED
- **Dependencies.csv:** `Dependencies.csv` (15 rows; 15 ACTIVE, 0 RETIRED)
- **Last Run:** 2026-02-17
- **Schema Version:** v3.1

### ANCHOR Rows (6 ACTIVE)

| DependencyID | AnchorType | TargetType | TargetRefID | TargetName | Confidence |
|---|---|---|---|---|---|
| DEP-0202-A01 | IMPLEMENTS_NODE | PACKAGE | -- | PKG-002 Main Public Services Building (PSB) | HIGH |
| DEP-0202-A02 | TRACES_TO_REQUIREMENT | WBS_NODE | SOW-0202 | SOW-0202: Provide four firehall drive-through apparatus bays | HIGH |
| DEP-0202-A03 | TRACES_TO_REQUIREMENT | WBS_NODE | SOW-0203 | SOW-0203: Provide bay services (electrical / compressed air / exhaust mitigation) | HIGH |
| DEP-0202-A04 | TRACES_TO_REQUIREMENT | WBS_NODE | SOW-0205 | SOW-0205: Provide decontamination area with support spaces | HIGH |
| DEP-0202-A05 | TRACES_TO_REQUIREMENT | WBS_NODE | SOW-0206 | SOW-0206: Provide 40 bunker gear lockers | HIGH |
| DEP-0202-A06 | TRACES_TO_REQUIREMENT | WBS_NODE | OBJ-002 | OBJ-002: Operationally functional Fire Department facilities | HIGH |

### EXECUTION Rows (9 ACTIVE)

| DependencyID | Direction | DependencyType | TargetType | Target | Statement (summary) |
|---|---|---|---|---|---|
| DEP-0202-E01 | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-02-01 Architectural Program | Required to confirm floor plan zone allocation for firehall wing |
| DEP-0202-E02 | UPSTREAM | INTERFACE | DELIVERABLE | DEL-02-04 Envelope/Doors | Required for overhead door specs and structural bay clearances |
| DEP-0202-E03 | UPSTREAM | INTERFACE | DELIVERABLE | DEL-02-05 Mechanical | Required for exhaust system design coordination and plumbing |
| DEP-0202-E04 | UPSTREAM | INTERFACE | DELIVERABLE | DEL-02-06 Electrical/IT | Required for electrical-in-bays layout and display system |
| DEP-0202-E05 | UPSTREAM | INTERFACE | DELIVERABLE | DEL-02-07 Emergency Power | Required for secondary door-opening mechanism specification |
| DEP-0202-E06 | UPSTREAM | INTERFACE | DELIVERABLE | DEL-03-01 Site Plan | Required for bay orientation and fire apparatus routing |
| DEP-0202-E07 | DOWNSTREAM | HANDOVER | DELIVERABLE | DEL-02-05 Mechanical | Produces bay exhaust mitigation coordination note for DEL-02-05 |
| DEP-0202-E08 | DOWNSTREAM | HANDOVER | DELIVERABLE | DEL-01-07 Closeout | Produces as-built drawings (firehall wing) for closeout package |
| DEP-0202-E09 | UPSTREAM | CONSTRAINT | DOCUMENT | Alberta Building Code (ABC) | Requires ABC full text for code compliance verification |

## Run Notes

- **Run Date:** 2026-02-17
- **Mode:** UPDATE
- **Strictness:** CONSERVATIVE
- **Consumer Context:** NONE
- **Source Docs (AUTO):** Datasheet.md, Guidance.md, Procedure.md, Specification.md
- **Anchor Doc (AUTO):** Datasheet.md (selected: contains `datasheet` keyword; has Identification/traceability fields)
- **Execution Doc Order (AUTO):** Procedure.md, Guidance.md, Specification.md (Procedure contains explicit prerequisites table; Guidance has considerations table; Specification has requirements and scope boundary)
- **Decomposition Path:** `_Decomposition/Penhold_PSB_Project_Decomposition_FINAL_v1.0_PHASE7.md` (available; validation performed)
- **_REFERENCES.md:** Available; used for reference context (no additional dependency rows emitted from it alone)
- **Warnings:** None.
- **Integrity Checks:**
  - Parent anchor (IMPLEMENTS_NODE): 1 found -- PASS
  - DependencyID uniqueness: 15/15 unique -- PASS
  - All ACTIVE rows have EvidenceFile + SourceRef -- PASS
  - CSV parseable with 29 required columns -- PASS
  - Counts consistent between CSV and this summary -- PASS

## Run History

| Run Date | Mode | Strictness | Decomposition | Warnings | ACTIVE Anchors | ACTIVE Execution | Total ACTIVE |
|---|---|---|---|---|---|---|---|
| 2026-02-17 | UPDATE | CONSERVATIVE | Available (FINAL v1.0 PHASE7) | None | 6 | 9 | 15 |

## Lifecycle Summary

- **ACTIVE:** 15 (6 ANCHOR + 9 EXECUTION)
- **RETIRED:** 0

### Closure-State Breakdown (ACTIVE rows)

| SatisfactionStatus | Count |
|---|---|
| TBD | 14 |
| PENDING | 1 |

- **Note:** DEP-0202-E09 (Alberta Building Code) is set to PENDING because the document is referenced but full text has not yet been obtained (location TBD per source documents).

## Consumer Handoff Notes (optional)
- Consumer context is NONE; no handoff notes generated.
