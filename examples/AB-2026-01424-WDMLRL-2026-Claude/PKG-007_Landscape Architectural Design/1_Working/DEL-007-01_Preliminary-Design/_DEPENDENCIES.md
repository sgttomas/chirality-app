# DEL-007-01 Preliminary Landscape Design — Dependencies

## Tracking Status
- **Dependency Tracking**: TRACKED
- **Register Schema**: v3.1
- **Register File**: Dependencies.csv (16 rows, 16 ACTIVE, 0 RETIRED)

## Upstream Dependencies
- RFP document review and site analysis completion
- Site maps and expansion area documentation review
- Project objectives alignment (OBJ-001, OBJ-003)

## Internal Dependencies
- None. This is the initiating deliverable for landscape design work.

## Downstream Dependencies
- **DEL-007-02**: Landscape Plans (depends on preliminary design approval)
- **DEL-007-03**: Planting & Restoration Plans (depends on site plan framework)
- **DEL-007-04**: Landscape Specification (depends on design intent and plant selection)

## External Dependencies
- Landscape Architect discipline assignment
- Stakeholder review availability
- RFP compliance verification

## Blocking Issues
- None currently identified

## Notes
Dependencies will be tracked once design development phase begins. Current status reflects preliminary planning stage.

---

## Extracted Dependency Register

**Total ACTIVE rows:** 16 | **RETIRED rows:** 0

### ANCHOR Edges (3 rows)

| DependencyID | AnchorType | TargetType | TargetRefID / TargetName | Confidence |
|---|---|---|---|---|
| DEP-007-01-001 | IMPLEMENTS_NODE | WBS_NODE | SOW-0010g | HIGH |
| DEP-007-01-002 | TRACES_TO_REQUIREMENT | REQUIREMENT | OBJ-001 | HIGH |
| DEP-007-01-003 | TRACES_TO_REQUIREMENT | REQUIREMENT | OBJ-003 | HIGH |

### EXECUTION Edges (13 rows)

| DependencyID | Direction | DependencyType | TargetType | Target | Confidence | EstimateImpactClass |
|---|---|---|---|---|---|---|
| DEP-007-01-004 | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-008-01 Geotechnical Investigation & Report | HIGH | BLOCKING |
| DEP-007-01-005 | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-008-02 Preliminary Site Survey | HIGH | BLOCKING |
| DEP-007-01-006 | UPSTREAM | INTERFACE | DELIVERABLE | DEL-005-01 Preliminary Civil Design | HIGH | BLOCKING |
| DEP-007-01-007 | UPSTREAM | INTERFACE | DELIVERABLE | DEL-001-01 Preliminary Architectural Design | MEDIUM | ADVISORY |
| DEP-007-01-008 | UPSTREAM | PREREQUISITE | DOCUMENT | R-01 (RFP) | HIGH | INFO |
| DEP-007-01-009 | UPSTREAM | PREREQUISITE | DOCUMENT | R-07 (Appendix C Site Maps) | HIGH | INFO |
| DEP-007-01-010 | UPSTREAM | CONSTRAINT | EXTERNAL | Camrose County Approval | HIGH | BLOCKING |
| DEP-007-01-011 | UPSTREAM | PREREQUISITE | EXTERNAL | Mandatory Site Meeting (2026-03-03) | HIGH | BLOCKING |
| DEP-007-01-012 | DOWNSTREAM | HANDOVER | DELIVERABLE | DEL-007-02 Landscape Site Plans | HIGH | BLOCKING |
| DEP-007-01-013 | DOWNSTREAM | HANDOVER | DELIVERABLE | DEL-007-03 Planting & Restoration Plans | HIGH | BLOCKING |
| DEP-007-01-014 | DOWNSTREAM | HANDOVER | DELIVERABLE | DEL-007-04 Landscape Specification | HIGH | BLOCKING |
| DEP-007-01-015 | UPSTREAM | INTERFACE | DELIVERABLE | DEL-005-02 Site Grading Plan | MEDIUM | ADVISORY |
| DEP-007-01-016 | UPSTREAM | INTERFACE | DELIVERABLE | DEL-005-04 Driving Surface & Pad Layout | MEDIUM | ADVISORY |

---

## Run Notes

### Run: 2026-02-26

**Parameters:**
- MODE: UPDATE
- STRICTNESS: CONSERVATIVE
- CONSUMER_CONTEXT: TASK_ESTIMATING
- SCOPE: DEL-007-01
- DECOMPOSITION_PATH: /Users/ryan/ai-env/projects/chirality-project-test/test/AB-2026-01424-WDMLRL-2026-Claude/_Decomposition/WDMLRL_Decomposition_Claude.md (found, valid)

**Source document resolution:**
- ANCHOR_DOC: Datasheet.md (selected: contains deliverable identification, SOW reference, objectives, and traceability fields)
- EXECUTION_DOC_ORDER: Procedure.md, Specification.md, Guidance.md (ordered by workflow clarity)
- Additional docs scanned: _CONTEXT.md, _REFERENCES.md (read-only reference)
- SOURCE_DOCS mode: AUTO

**Defaults applied:**
- All ANCHOR rows: DependencyType=OTHER, Direction=UPSTREAM (per protocol)
- All EXECUTION rows: AnchorType=NOT_APPLICABLE (per protocol)
- Extension columns EstimateImpactClass and ConsumerHint populated per CONSUMER_CONTEXT=TASK_ESTIMATING

**Decomposition validation:**
- SOW-0010g confirmed in scope ledger (row: SOW-0010g -> PKG-007 -> DEL-007-01 -> OBJ-001, OBJ-003)
- OBJ-001, OBJ-003 confirmed in decomposition §5 Objectives
- All target deliverable IDs (DEL-008-01, DEL-008-02, DEL-005-01, DEL-005-02, DEL-005-04, DEL-001-01, DEL-007-02, DEL-007-03, DEL-007-04) confirmed in decomposition §7

**Integrity checks:**
- Parent anchor (IMPLEMENTS_NODE): 1 found (SOW-0010g) -- PASS
- DependencyID uniqueness: 16 unique of 16 total -- PASS
- All ACTIVE rows have EvidenceFile and SourceRef -- PASS
- FromDeliverableID consistency: all rows = DEL-007-01 -- PASS
- Enum normalization: all values canonical on write -- PASS
- No legacy Direction values found (no INBOUND/OUTBOUND to normalize)
- No rows RETIRED (first run)
- CSV parseable: confirmed via Python csv.DictReader

**Warnings:** None.

**Extraction notes:**
- DEP-007-01-004, DEP-007-01-005 (geotech/survey): Sources explicitly note these may not be available at preliminary stage; dependency is best-effort for preliminary, required for final. Marked PENDING.
- DEP-007-01-010 (County approval): This is both an upstream constraint on this deliverable (must be submitted and approved) and the gate condition for downstream handovers. Modeled as UPSTREAM CONSTRAINT per protocol (the constraint originates from the County).
- DEP-007-01-011 (site meeting): Explicit prerequisite per R-01 §3.2 and Procedure. Attendance is mandatory.
- DEP-007-01-007, DEP-007-01-015, DEP-007-01-016: Cross-deliverable interfaces named in Procedure Step 4.3 and Specification Verification. Marked MEDIUM confidence because the interface is explicit but the data transfer content is coordination-level rather than a hard artifact gate at the preliminary stage.
- Coordination-only relationships (e.g., PKG-018 general references, weekly meetings SOW-0086) were excluded per information-flow-only extraction rule.

---

## Run History

| Timestamp | Mode | Strictness | Decomposition | Warnings | ANCHOR (Active) | EXECUTION (Active) | Total Active | Retired |
|---|---|---|---|---|---|---|---|---|
| 2026-02-26 | UPDATE | CONSERVATIVE | WDMLRL_Decomposition_Claude.md (valid) | None | 3 | 13 | 16 | 0 |

---

## Lifecycle Summary

| Status | Count |
|---|---|
| ACTIVE | 16 |
| RETIRED | 0 |

| SatisfactionStatus | Count |
|---|---|
| TBD | 8 |
| PENDING | 8 |

| DependencyClass | Active | Retired |
|---|---|---|
| ANCHOR | 3 | 0 |
| EXECUTION | 13 | 0 |

---

## Downstream Handoff Notes

**Consumer context: TASK_ESTIMATING**

The following observations are provided to support downstream task-estimating workflows:

1. **BLOCKING upstream dependencies (5):**
   - DEL-008-01 (Geotech) and DEL-008-02 (Survey) are explicit data prerequisites. At the preliminary stage, these are best-effort inputs; however, for estimating purposes, their availability status affects confidence in scope quantities (soil conditions, topography). If these are not available, estimating should assume conservative site conditions and flag as a variable.
   - DEL-005-01 (Preliminary Civil Design) is a blocking interface for grading/drainage coordination. The landscape design effort cannot proceed meaningfully without understanding the civil grading intent. Estimating should sequence landscape design effort after initial civil coordination.
   - County Approval (DEP-007-01-010) is the contractual gate. Estimating should account for one or more review cycles.
   - Mandatory Site Meeting (DEP-007-01-011) is a hard prerequisite before design work can begin.

2. **BLOCKING downstream handovers (3):**
   - DEL-007-02, DEL-007-03, DEL-007-04 are all gated on DEL-007-01 approval. Estimating for those deliverables should not assume start before DEL-007-01 is approved.

3. **ADVISORY upstream interfaces (3):**
   - DEL-001-01 (Preliminary Architectural), DEL-005-02 (Site Grading Plan), DEL-005-04 (Driving Surface Layout) are cross-check interfaces. These may affect quantities/specs but are not hard gates on starting DEL-007-01 work.

4. **INFO document inputs (2):**
   - R-01 (RFP) and R-07 (Site Maps) are available reference documents with low estimating impact beyond confirming scope.

5. **Scope uncertainty note:** CONF-007-01-001 (landscape treatment extent) is an unresolved conflict that affects the scope boundary. Estimating should treat landscape scope conservatively as functional restoration of the disturbed expansion area unless County confirms a broader program.
