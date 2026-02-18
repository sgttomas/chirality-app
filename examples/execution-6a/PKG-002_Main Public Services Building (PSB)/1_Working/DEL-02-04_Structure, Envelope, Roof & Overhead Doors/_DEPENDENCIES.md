# Dependencies: DEL-02-04 Structure, Envelope, Roof & Overhead Doors

## Coordination (human-owned)
- **Mode:** DECLARED
- **Notes:** See _Coordination/_COORDINATION.md for project-level coordination record.

## Upstream (I need these before I can proceed) -- human-owned declarations
- No upstream dependencies declared yet.

## Downstream (These need me) -- human-owned declarations
- No downstream dependencies declared yet.

## Extracted Dependency Register

- **Status:** COMPLETE
- **Dependencies.csv:** `Dependencies.csv` (19 rows)
- **RegisterSchemaVersion:** v3.1

### Summary

| DependencyClass | AnchorType | Count (ACTIVE) |
|---|---|---|
| ANCHOR | IMPLEMENTS_NODE | 1 |
| ANCHOR | TRACES_TO_REQUIREMENT | 8 |
| EXECUTION | NOT_APPLICABLE | 10 |
| **Total** | | **19** |

### ANCHOR Rows (9 ACTIVE)

| DependencyID | AnchorType | TargetRefID | TargetName | Confidence |
|---|---|---|---|---|
| DEP-0204-A01 | IMPLEMENTS_NODE | PKG-002 | Main Public Services Building (PSB) | HIGH |
| DEP-0204-A02 | TRACES_TO_REQUIREMENT | SOW-0201 | Main building 50-year design life | HIGH |
| DEP-0204-A03 | TRACES_TO_REQUIREMENT | SOW-0215 | Overhead doors min 16 ft clear height and car wash grade hardware | HIGH |
| DEP-0204-A04 | TRACES_TO_REQUIREMENT | SOW-0216 | 16x16 overhead doors with motorized openers and secondary opening mechanism | HIGH |
| DEP-0204-A05 | TRACES_TO_REQUIREMENT | SOW-0217 | Durable resilient interior flooring; sealed concrete acceptable | HIGH |
| DEP-0204-A06 | TRACES_TO_REQUIREMENT | SOW-0220 | Building durability/ease of repair and adaptability/expansion | HIGH |
| DEP-0204-A07 | TRACES_TO_REQUIREMENT | SOW-0221 | Solar-capable roof with future solar loading consideration | HIGH |
| DEP-0204-A08 | TRACES_TO_REQUIREMENT | OBJ-001 | Deliver turnkey code-compliant commissioned PSB | HIGH |
| DEP-0204-A09 | TRACES_TO_REQUIREMENT | OBJ-006 | Achieve durability low-maintenance and lifecycle performance with solar-ready roof | HIGH |

### EXECUTION Rows (10 ACTIVE)

| DependencyID | Direction | DependencyType | TargetType | Target | Confidence |
|---|---|---|---|---|---|
| DEP-0204-E01 | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-02-01 Architectural Program Layout & Code Planning | HIGH |
| DEP-0204-E02 | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-02-02 Firehall Apparatus Bays & Support Spaces | HIGH |
| DEP-0204-E03 | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-02-03 Public Works Shop Bays Workshop & Support Spaces | HIGH |
| DEP-0204-E04 | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-02-07 Emergency Power & Backup Generator | HIGH |
| DEP-0204-E05 | UPSTREAM | PREREQUISITE | DOCUMENT | Geotechnical Investigation Report (RFP Appendix D) | HIGH |
| DEP-0204-E06 | UPSTREAM | CONSTRAINT | EXTERNAL | Alberta Building Code (NBCC-based) | HIGH |
| DEP-0204-E07 | DOWNSTREAM | INTERFACE | DELIVERABLE | DEL-03-02 Grading Earthworks Drainage & Stormwater | HIGH |
| DEP-0204-E08 | DOWNSTREAM | INTERFACE | DELIVERABLE | DEL-02-05 Mechanical Plumbing Ventilation & Exhaust | HIGH |
| DEP-0204-E09 | DOWNSTREAM | INTERFACE | DELIVERABLE | DEL-03-03 Pavements Aggregate Yard Areas & Concrete Aprons | MEDIUM |
| DEP-0204-E10 | UPSTREAM | PREREQUISITE | DOCUMENT | Site Grading Drawings (RFP Appendix E) | HIGH |

## Run Notes

### Run: 2026-02-17

- **MODE:** UPDATE
- **STRICTNESS:** CONSERVATIVE
- **CONSUMER_CONTEXT:** NONE
- **SOURCE_DOCS:** AUTO (resolved: Datasheet.md, Specification.md, Procedure.md, Guidance.md)
- **ANCHOR_DOC:** AUTO (resolved: Datasheet.md -- contains Identification section with explicit scope/objective traceability)
- **EXECUTION_DOC_ORDER:** AUTO (resolved: Procedure.md, Specification.md, Guidance.md)
- **DECOMPOSITION_PATH:** `_Decomposition/Penhold_PSB_Project_Decomposition_FINAL_v1.0_PHASE7.md` -- FOUND and used for validation
- **_REFERENCES.md:** Present and read; used for document target resolution

**Anchor validation:**
- Parent anchor (IMPLEMENTS_NODE): 1 found -- PKG-002. Validated against decomposition.
- Trace anchors: 6 SOW items (SOW-0201, SOW-0215, SOW-0216, SOW-0217, SOW-0220, SOW-0221) and 2 objectives (OBJ-001, OBJ-006). All confirmed in decomposition scope ledger and objectives table.

**Execution extraction notes:**
- 6 UPSTREAM dependencies extracted (4 deliverable prerequisites, 2 document/external prerequisites).
- 3 DOWNSTREAM interfaces extracted (DEL-03-02 stormwater, DEL-02-05 mechanical/plumbing, DEL-03-03 aprons).
- 1 additional UPSTREAM document prerequisite (Site Grading Drawings).
- DEL-02-05 interface is bidirectional in practice (sumps feed floor slab slopes and vice versa); recorded as DOWNSTREAM from DEL-02-04 perspective because DEL-02-04 produces floor slab design that DEL-02-05 needs for sump placement.
- DEL-03-03 apron interface recorded at MEDIUM confidence because the out-of-scope note implies but does not strongly state a data transfer requirement; however, floor levels at door thresholds are a necessary input for apron design.
- Cold storage deliverables (DEL-04-02, DEL-04-03) noted as out-of-scope boundaries; no information-flow dependency extracted (structural adjacency only).
- Guidance C-06 (DEL-02-07 secondary door mechanism) confirmed the prerequisite already captured from Procedure prerequisites; no duplicate row created.

**Warnings:** None.

## Run History

| Timestamp | Mode | Strictness | Decomposition | Warnings | ACTIVE Anchors | ACTIVE Execution |
|---|---|---|---|---|---|---|
| 2026-02-17 | UPDATE | CONSERVATIVE | Found (Phase 7 v1.0) | None | 9 | 10 |

## Lifecycle Summary

| Status | Count |
|---|---|
| ACTIVE | 19 |
| RETIRED | 0 |

| SatisfactionStatus | Count |
|---|---|
| TBD | 19 |
| PENDING | 0 |
| IN_PROGRESS | 0 |
| SATISFIED | 0 |

## Consumer Handoff Notes (optional)
- CONSUMER_CONTEXT is NONE; no handoff notes generated.
