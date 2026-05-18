# Dependencies: DEL-03-05 Environmental Constraints, Flood Hazard & Regulatory Compliance

## Coordination (human-owned)
- **Mode:** DECLARED
- **Notes:** See _Coordination/_COORDINATION.md for project-level coordination record.

## Upstream (I need these before I can proceed) -- human-owned declarations
- No upstream dependencies declared yet.

## Downstream (These need me) -- human-owned declarations
- No downstream dependencies declared yet.

## Extracted Dependency Register

- **Status:** COMPLETED
- **Dependencies.csv:** `Dependencies.csv` (19 rows)
- **Schema Version:** v3.1

### Summary

| Category | Count |
|---|---|
| Total rows | 19 |
| ANCHOR rows | 5 |
| EXECUTION rows | 14 |
| ACTIVE | 19 |
| RETIRED | 0 |

### ANCHOR Edges (Tree -- vertical)

| DependencyID | AnchorType | TargetRefID / TargetName | Confidence | Status |
|---|---|---|---|---|
| DEP-3505-A01 | IMPLEMENTS_NODE | PKG-003 -- Site & Civil Works | HIGH | ACTIVE |
| DEP-3505-A02 | TRACES_TO_REQUIREMENT | SOW-0102 -- Existing site works constraint | HIGH | ACTIVE |
| DEP-3505-A03 | TRACES_TO_REQUIREMENT | SOW-0114 -- Flood hazard constraints and regulator coordination | HIGH | ACTIVE |
| DEP-3505-A04 | TRACES_TO_REQUIREMENT | OBJ-005 -- Deliver complete site/civil works | MEDIUM | ACTIVE |
| DEP-3505-A05 | TRACES_TO_REQUIREMENT | OBJ-008 -- Safe controlled Design-Build delivery | MEDIUM | ACTIVE |

### EXECUTION Edges (DAG -- horizontal)

| DependencyID | Direction | Type | Target | Confidence | Status |
|---|---|---|---|---|---|
| DEP-3505-E01 | UPSTREAM | PREREQUISITE | Adjacent Subdivision Design exhibit (DOCUMENT) | HIGH | ACTIVE |
| DEP-3505-E02 | UPSTREAM | PREREQUISITE | Parcel Flood Zone exhibit (DOCUMENT) | HIGH | ACTIVE |
| DEP-3505-E03 | UPSTREAM | PREREQUISITE | Wetland Assessment and Impact Report (DOCUMENT) | HIGH | ACTIVE |
| DEP-3505-E04 | UPSTREAM | PREREQUISITE | Desktop/Field Environmental Assessment (DOCUMENT) | HIGH | ACTIVE |
| DEP-3505-E05 | UPSTREAM | PREREQUISITE | Site Grading drawings (DOCUMENT) | HIGH | ACTIVE |
| DEP-3505-E06 | UPSTREAM | CONSTRAINT | AEPA -- Water Act application status confirmation (EXTERNAL) | HIGH | ACTIVE |
| DEP-3505-E07 | UPSTREAM | INTERFACE | DEL-03-02 -- stormwater management approach and discharge points (DELIVERABLE) | HIGH | ACTIVE |
| DEP-3505-E08 | UPSTREAM | INTERFACE | DEL-03-02 -- earthwork cut/fill volumes relative to flood fringe (DELIVERABLE) | HIGH | ACTIVE |
| DEP-3505-E09 | DOWNSTREAM | HANDOVER | DEL-03-02 -- confirmed flood hazard constraints map (DELIVERABLE) | HIGH | ACTIVE |
| DEP-3505-E10 | DOWNSTREAM | HANDOVER | DEL-03-02 -- wetland/setback integration output (DELIVERABLE) | HIGH | ACTIVE |
| DEP-3505-E11 | DOWNSTREAM | HANDOVER | DEL-03-02 -- AEPA Water Act conditions affecting grading/stormwater/fill (DELIVERABLE) | HIGH | ACTIVE |
| DEP-3505-E12 | UPSTREAM | CONSTRAINT | AEPA -- Water Act approval letter (EXTERNAL) | HIGH | ACTIVE |
| DEP-3505-E13 | UPSTREAM | CONSTRAINT | Town of Penhold -- Development Permit (EXTERNAL) | HIGH | ACTIVE |
| DEP-3505-E14 | UPSTREAM | CONSTRAINT | Town of Penhold and AEPA -- Fill placement acceptance (EXTERNAL) | HIGH | ACTIVE |

---

## Run Notes

### Run: 2026-02-17

**Run Parameters:**
- MODE: UPDATE
- STRICTNESS: CONSERVATIVE
- CONSUMER_CONTEXT: NONE
- SOURCE_DOCS: AUTO
- ANCHOR_DOC: AUTO

**Resolved Paths & Defaults:**
- RUN_ROOT: `/test/execution-6a/`
- Decomposition: `_Decomposition/Penhold_PSB_Project_Decomposition_FINAL_v1.0_PHASE7.md` (found and used)
- ANCHOR_DOC: `Datasheet.md` (selected by heuristic: contains `datasheet` in filename; has Identification table with scope item IDs, objective IDs, package reference)
- EXECUTION_DOC_ORDER: `Procedure.md`, `Guidance.md`, `Specification.md` (selected by heuristic: Procedure contains `procedure`; Guidance contains `guidance`; Specification contains `spec`)
- _REFERENCES.md: present and used for document location resolution

**Decomposition Validation:**
- Decomposition file located and used for anchor validation and label resolution.
- DEL-03-05 confirmed in PKG-003 deliverables table.
- SOW-0102, SOW-0114 confirmed in scope ledger mapped to DEL-03-05.
- OBJ-005, OBJ-008 confirmed in objectives table.

**Integrity Check Results:**
- Parent anchor (IMPLEMENTS_NODE): 1 found (DEP-3505-A01) -- PASS
- DependencyID uniqueness: 19/19 unique -- PASS
- All ACTIVE rows have EvidenceFile and SourceRef -- PASS
- No RETIRED rows (first run) -- N/A
- No warnings issued.

**Extraction Notes:**
- OBJ-005 and OBJ-008 trace anchors set to MEDIUM confidence because Datasheet explicitly marks them as "ASSUMPTION: best-effort mapping per PACKAGE_HEURISTIC." Decomposition does confirm the mapping but the Datasheet itself hedges.
- DEL-03-02 interface is bidirectional (5 edges: 2 UPSTREAM inputs, 3 DOWNSTREAM handovers). Guidance.md Consideration 5 provides detailed Timing Dependency Guidance with explicit artifact descriptions.
- Four external constraints (E06, E12, E13, E14) extracted from Procedure.md prerequisites and Step B1 pre-construction gate. These represent regulatory approvals/information required before work can proceed.
- Scope boundary statements in Specification.md Out of Scope section (referencing DEL-03-02, DEL-03-04) were NOT extracted as dependencies because they are structural adjacency, not explicit data/artifact transfer.
- DEL-01-03 (H&S Plan) reference in Specification.md Standards table was NOT extracted as a dependency; it is a cross-reference to related scope, not an explicit input/output requirement.

---

## Run History

| Timestamp | Mode | Strictness | Decomposition | Warnings | ACTIVE Anchors | ACTIVE Execution | Total ACTIVE |
|---|---|---|---|---|---|---|---|
| 2026-02-17 | UPDATE | CONSERVATIVE | Found; validated | None | 5 | 14 | 19 |

---

## Lifecycle Summary

| Status | Count |
|---|---|
| ACTIVE | 19 |
| RETIRED | 0 |

| SatisfactionStatus | Count |
|---|---|
| TBD | 17 |
| NOT_APPLICABLE | 2 |

**Notes:**
- IMPLEMENTS_NODE anchor (DEP-3505-A01) and one trace anchor have SatisfactionStatus=NOT_APPLICABLE (anchors represent structural traceability, not closure-tracked obligations).
- Remaining 17 rows (4 trace anchors + 14 execution edges) have SatisfactionStatus=TBD pending downstream workflow assessment.

---

## Consumer Handoff Notes (optional)
- CONSUMER_CONTEXT: NONE -- no consumer-specific handoff notes generated.
