# Dependencies: DEL-001-01 Preliminary Architectural Design

## Coordination (human-owned)
- **Mode:** NOT_TRACKED
- **Notes:** Coordination representation pending -- to be confirmed by human via ORCHESTRATOR.

## Upstream (I need these before I can proceed) -- human-owned declarations
- Dependencies coordinated externally by humans.

## Downstream (These need me) -- human-owned declarations
- Dependencies coordinated externally by humans.

## Extracted Dependency Register

- **Status:** POPULATED
- **Dependencies.csv:** 17 rows (3 ANCHOR + 14 EXECUTION)
- **Schema Version:** v3.1

### ANCHOR Edges (Tree)

| DependencyID | AnchorType | TargetRefID | TargetName | Confidence |
|---|---|---|---|---|
| DEP-001-01-A01 | IMPLEMENTS_NODE | SOW-0010a | Deliver preliminary architectural design for County approval | HIGH |
| DEP-001-01-A02 | TRACES_TO_REQUIREMENT | OBJ-001 | Deliver a code-compliant, fully functional maintenance shop addition | HIGH |
| DEP-001-01-A03 | TRACES_TO_REQUIREMENT | OBJ-003 | Produce complete P.Eng.-stamped IFC design documentation across all disciplines | HIGH |

### EXECUTION Edges (DAG)

| DependencyID | Direction | DependencyType | TargetType | Target | Confidence | EstimateImpactClass |
|---|---|---|---|---|---|---|
| DEP-001-01-E01 | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-008-01 Geotechnical Investigation & Report | HIGH | BLOCKING |
| DEP-001-01-E02 | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-008-02 Preliminary Site Survey | HIGH | BLOCKING |
| DEP-001-01-E03 | DOWNSTREAM | HANDOVER | DELIVERABLE | DEL-001-02 Architectural Floor Plans (IFC) | HIGH | BLOCKING |
| DEP-001-01-E04 | DOWNSTREAM | INTERFACE | DELIVERABLE | DEL-002-01 Preliminary Structural Design | HIGH | ADVISORY |
| DEP-001-01-E05 | UPSTREAM | CONSTRAINT | EXTERNAL | Camrose County Preliminary Design Approval | HIGH | BLOCKING |
| DEP-001-01-E06 | UPSTREAM | PREREQUISITE | DOCUMENT | R-01 AB-2026-01424-WDMLRL RFP.pdf | HIGH | BLOCKING |
| DEP-001-01-E07 | DOWNSTREAM | INTERFACE | DELIVERABLE | DEL-003-01 Preliminary Mechanical Design | HIGH | ADVISORY |
| DEP-001-01-E08 | DOWNSTREAM | INTERFACE | DELIVERABLE | DEL-004-01 Preliminary Electrical Design | HIGH | ADVISORY |
| DEP-001-01-E09 | DOWNSTREAM | INTERFACE | DELIVERABLE | DEL-005-01 Preliminary Civil Design | HIGH | ADVISORY |
| DEP-001-01-E10 | DOWNSTREAM | INTERFACE | DELIVERABLE | DEL-006-01 Preliminary Plumbing Design | HIGH | ADVISORY |
| DEP-001-01-E11 | DOWNSTREAM | INTERFACE | DELIVERABLE | DEL-007-01 Preliminary Landscape Design | MEDIUM | INFO |
| DEP-001-01-E12 | UPSTREAM | PREREQUISITE | DOCUMENT | R-04 Appendix B (Shop) Conceptual Floor Plan | HIGH | BLOCKING |
| DEP-001-01-E13 | UPSTREAM | PREREQUISITE | DOCUMENT | R-07 Appendix C - Site Maps | MEDIUM | ADVISORY |
| DEP-001-01-E14 | UPSTREAM | CONSTRAINT | EXTERNAL | Mandatory Site Meeting (March 3, 2026) | HIGH | BLOCKING |

---

## Run Notes

### Run: 2026-02-26

**Parameters:**
- SCOPE: DEL-001-01_Preliminary-Design
- RUN_ROOT: `PKG-001_Architectural Design/1_Working/DEL-001-01_Preliminary-Design`
- DECOMPOSITION_PATH: `_Decomposition/WDMLRL_Decomposition_Claude.md` (R1 -- 2026-02-25)
- MODE: UPDATE
- STRICTNESS: CONSERVATIVE
- SOURCE_DOCS: AUTO
- ANCHOR_DOC: AUTO (resolved to `Datasheet.md`)
- EXECUTION_DOC_ORDER: AUTO (resolved to `Specification.md`, `Procedure.md`, `Guidance.md`)
- CONSUMER_CONTEXT: TASK_ESTIMATING

**Defaults and Resolutions:**
- ANCHOR_DOC selected as `Datasheet.md` (matches heuristic: contains "datasheet" and has Identification table with SOW reference and Objectives Supported fields).
- EXECUTION_DOC_ORDER: `Specification.md` (requirements with explicit dependency statements), `Procedure.md` (prerequisites and steps with explicit inputs), `Guidance.md` (purpose statement with coordination framework, considerations with discipline interfaces).
- `_REFERENCES.md` present and used for document target resolution (R-01, R-04 pointers).
- Decomposition document located and read successfully. Used for: validating SOW-0010a, OBJ-001, OBJ-003 identifiers; resolving deliverable IDs for all target deliverables; confirming package assignments.

**Source Documents Scanned:**
1. `Datasheet.md` -- ANCHOR_DOC. 121 lines. Identification table, Attributes, Conditions, Construction, Site Conditions, References.
2. `Specification.md` -- EXECUTION_DOC. 177 lines. Scope, Requirements REQ-001 through REQ-013, Standards, Verification, Documentation.
3. `Procedure.md` -- EXECUTION_DOC. 252 lines. Prerequisites, Steps 1-8, Verification, Records.
4. `Guidance.md` -- EXECUTION_DOC. 226 lines. Purpose, Principles P-1 through P-5, Considerations C-1 through C-14, Vocabulary Notes, Departure Log, Assumption Register, Trade-offs, Conflict Table.

**Extraction Decisions:**
- Pass 1 (ANCHOR): 1 IMPLEMENTS_NODE row (SOW-0010a) and 2 TRACES_TO_REQUIREMENT rows (OBJ-001, OBJ-003) extracted from Datasheet.md Identification table. All confirmed against decomposition.
- Pass 2 (EXECUTION): 14 rows extracted. Key extraction decisions:
  - E01-E02: Geotech and survey prerequisites from REQ-013 (Specification.md). Corroborated by Datasheet Conditions, Guidance P-4, Procedure Step 1.3.
  - E03: Downstream handover to final design (DEL-001-02 as lead representative) from REQ-001 approval gate. This is a single row representing the gate; downstream deliverables DEL-001-02 through DEL-001-11 are all gated.
  - E04, E07-E11: Discipline interface rows for all six coordinated preliminary designs (structural, mechanical, electrical, civil, plumbing, landscape). Evidence: Guidance Purpose statement explicitly names all six disciplines; Procedure Step 5.1 enumerates specific coordination items for structural, mechanical, electrical, civil, and plumbing; REQ-011 (electrical) and REQ-012c (plumbing) provide additional evidence. Landscape (E11) has lower confidence -- named in Guidance Purpose but no specific coordination items enumerated.
  - E05: County approval constraint from REQ-001.
  - E06, E12: RFP (R-01) and conceptual floor plan (R-04) as document prerequisites. Both explicitly listed in Procedure prerequisites.
  - E13: Site maps (R-07) as document prerequisite. Listed in Procedure prerequisites; Guidance C-1 and Datasheet Site Conditions note R-07 not yet read in detail. SatisfactionStatus set to PENDING.
  - E14: Mandatory site meeting constraint from Procedure prerequisites and Step 1.2. Attendance is a disqualification condition per R-01 ss3.2.

**Not Extracted (rationale):**
- R-02 (Addendum 1), R-03 (Appendix A forms), R-05 (Electrical appendix), R-06 (Plumbing appendix): Listed in Procedure Step 1.1 for general review, but no explicit statement that design cannot proceed without them specifically. R-05 and R-06 are noted as "should be reviewed" (Guidance C-10) but no explicit dependency statement.
- DEL-002-01 through DEL-007-01 as UPSTREAM interfaces: The source documents frame DEL-001-01 as the lead/provider of the spatial framework; the other disciplines are consumers. Bidirectional coordination exists but the explicit information flow direction is FROM architecture TO other disciplines. No source text states DEL-001-01 requires specific data FROM those deliverables.
- Coordination-only relationships (e.g., weekly meetings, billing coordination): No specific artifact/data transfer stated.

**Warnings:**
- None. All quality checks passed.

---

## Run History

| Timestamp | Mode | Strictness | Decomposition | Warnings | ACTIVE ANCHOR | ACTIVE EXECUTION |
|---|---|---|---|---|---|---|
| 2026-02-26 | UPDATE | CONSERVATIVE | `_Decomposition/WDMLRL_Decomposition_Claude.md` (R1, 2026-02-25) -- OK | None | 3 | 14 |

---

## Lifecycle Summary

### Extraction Lifecycle

| Status | Count |
|---|---|
| ACTIVE | 17 |
| RETIRED | 0 |

### By DependencyClass

| Class | ACTIVE | RETIRED |
|---|---|---|
| ANCHOR | 3 | 0 |
| EXECUTION | 14 | 0 |

### Closure Lifecycle (SatisfactionStatus of ACTIVE rows)

| SatisfactionStatus | Count |
|---|---|
| TBD | 14 |
| SATISFIED | 2 |
| PENDING | 1 |

**Notes:**
- E06 (R-01 RFP) and E12 (R-04 Appendix B) set to SATISFIED -- documents are available per Procedure prerequisites.
- E13 (R-07 Site Maps) set to PENDING -- document is available but noted as "not read in detail" in Datasheet and Guidance C-1; data extraction from R-07 is TBD.
- All other rows are TBD pending project mobilization and execution.

---

## Downstream Handoff Notes (CONSUMER_CONTEXT: TASK_ESTIMATING)

### Estimating Impact Summary

**BLOCKING dependencies (5):** These gate meaningful estimating for DEL-001-01. Scope or key quantities cannot be finalized without them.

| DependencyID | Target | Rationale |
|---|---|---|
| DEP-001-01-E01 | DEL-008-01 Geotech | Foundation approach is variable-price and unknown until geotech completes. Affects structural coordination and overall building placement. |
| DEP-001-01-E02 | DEL-008-02 Site Survey | Building footprint dimensions are approximate (scaled from conceptual plan); survey confirmation needed for final quantities. |
| DEP-001-01-E05 | County Approval | Approval gate; rework risk if design direction changes post-review. Estimating should acknowledge revision cycle risk. |
| DEP-001-01-E06 | R-01 RFP | Primary program source. SATISFIED -- available. |
| DEP-001-01-E14 | Mandatory Site Meeting | Disqualification gate. Key design parameters to be confirmed at meeting (presentation format, area tolerance, elevation count). |

**ADVISORY dependencies (7):** These are likely to influence quantities, specs, or procurement approach but are not hard gates.

| DependencyID | Target | Rationale |
|---|---|---|
| DEP-001-01-E03 | DEL-001-02 (downstream) | Handover to final design; estimating for final design deliverables depends on preliminary approval. |
| DEP-001-01-E04 | DEL-002-01 Structural | Coordination may change crane bay dimensions, column grid, mezzanine loading -- affects quantities. |
| DEP-001-01-E07 | DEL-003-01 Mechanical | Exhaust routing and heating system approach may affect space allocation. |
| DEP-001-01-E08 | DEL-004-01 Electrical | Three-phase service entry point may affect spatial layout. |
| DEP-001-01-E09 | DEL-005-01 Civil | Mud sump and drainage connection may affect site layout quantities. |
| DEP-001-01-E10 | DEL-006-01 Plumbing | Cistern location and wash bay drainage affect space planning. |
| DEP-001-01-E13 | R-07 Site Maps | Site orientation/boundary data pending detailed review. |

**INFO dependencies (1):**

| DependencyID | Target | Rationale |
|---|---|---|
| DEP-001-01-E11 | DEL-007-01 Landscape | Low likelihood of changing architectural quantities at preliminary stage. |

**Estimating Readiness Assessment:**
- DEL-001-01 is a design presentation deliverable (not a construction package). Estimating effort is primarily architectural labor hours.
- The BLOCKING dependencies on geotech (E01) and survey (E02) affect the scope of the design work itself (foundation approach, building placement), not the effort to produce the preliminary presentation directly. However, if geotech results are unavailable, the presentation will need to carry more open items and may require revision post-geotech.
- The mandatory site meeting (E14) is a critical path item for resolving several TBD parameters (area tolerance, presentation format, elevation count) that affect effort estimates.
- R-04 (E12) is the primary spatial reference and is SATISFIED; this de-risks the floor plan production effort.
