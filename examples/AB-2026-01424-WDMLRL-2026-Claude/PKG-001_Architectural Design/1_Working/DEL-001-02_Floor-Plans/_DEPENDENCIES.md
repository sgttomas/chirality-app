# Dependencies: DEL-001-02 Architectural Floor Plans

## Coordination (human-owned)
- **Mode:** NOT_TRACKED
- **Notes:** Coordination representation pending -- to be confirmed by human via ORCHESTRATOR.

## Upstream (I need these before I can proceed) -- human-owned declarations
- Dependencies coordinated externally by humans.

## Downstream (These need me) -- human-owned declarations
- Dependencies coordinated externally by humans.

## Extracted Dependency Register

- **Status:** POPULATED
- **Dependencies.csv:** Dependencies.csv (v3.1 schema)
- **Total ACTIVE rows:** 19
- **Total RETIRED rows:** 0

### ANCHOR Rows (3 ACTIVE)

| DependencyID | AnchorType | TargetType | TargetRefID | TargetName | Confidence |
|---|---|---|---|---|---|
| DEP-001-02-A01 | IMPLEMENTS_NODE | WBS_NODE | SOW-0011 | Complete final architectural design for the addition | HIGH |
| DEP-001-02-A02 | TRACES_TO_REQUIREMENT | REQUIREMENT | OBJ-001 | Deliver a code-compliant, fully functional maintenance shop addition | HIGH |
| DEP-001-02-A03 | TRACES_TO_REQUIREMENT | REQUIREMENT | OBJ-003 | Produce complete P.Eng.-stamped IFC design documentation across all disciplines | HIGH |

### EXECUTION Rows (16 ACTIVE)

| DependencyID | Direction | DependencyType | TargetType | TargetDeliverableID / TargetRefID | TargetName | Confidence | EstimateImpactClass |
|---|---|---|---|---|---|---|---|
| DEP-001-02-E01 | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-001-01 | Preliminary Architectural Design | HIGH | BLOCKING |
| DEP-001-02-E02 | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-008-01 | Geotechnical Investigation & Report | HIGH | BLOCKING |
| DEP-001-02-E03 | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-008-02 | Preliminary Site Survey | HIGH | BLOCKING |
| DEP-001-02-E04 | UPSTREAM | INTERFACE | DELIVERABLE | DEL-002-03 | Structural Framing Plans | HIGH | BLOCKING |
| DEP-001-02-E05 | UPSTREAM | INTERFACE | DELIVERABLE | DEL-006-04 | Cistern & Pump Details | HIGH | ADVISORY |
| DEP-001-02-E06 | UPSTREAM | INTERFACE | DELIVERABLE | DEL-003-02 | HVAC Layout Plans | HIGH | ADVISORY |
| DEP-001-02-E07 | UPSTREAM | INTERFACE | DELIVERABLE | DEL-002-06 | Service Pit / Trench Structural Details | HIGH | ADVISORY |
| DEP-001-02-E08 | UPSTREAM | INTERFACE | DELIVERABLE | DEL-002-05 | Mezzanine Framing Details | HIGH | ADVISORY |
| DEP-001-02-E09 | UPSTREAM | INTERFACE | DELIVERABLE | DEL-002-07 | Crane Support Structure Details | HIGH | ADVISORY |
| DEP-001-02-E10 | UPSTREAM | INTERFACE | DELIVERABLE | DEL-002-08 | Steel Plate Embedment Plan | HIGH | ADVISORY |
| DEP-001-02-E11 | UPSTREAM | INTERFACE | DELIVERABLE | DEL-001-09 | Old North Shop Demolition Plans | MEDIUM | ADVISORY |
| DEP-001-02-E12 | DOWNSTREAM | HANDOVER | DELIVERABLE | DEL-009-02 | Building Permit Application & Approval | HIGH | ADVISORY |
| DEP-001-02-E13 | UPSTREAM | CONSTRAINT | DOCUMENT | (none) | Alberta Building Code (current edition) | HIGH | BLOCKING |
| DEP-001-02-E14 | UPSTREAM | PREREQUISITE | DOCUMENT | R-04 | Appendix B Conceptual Drawing (Shop) | HIGH | INFO |
| DEP-001-02-E15 | DOWNSTREAM | HANDOVER | DELIVERABLE | DEL-011-01 | Concrete Superstructure | MEDIUM | ADVISORY |
| DEP-001-02-E16 | DOWNSTREAM | HANDOVER | DELIVERABLE | DEL-004-04 | Lighting Plans | MEDIUM | INFO |

## Run Notes

### Run: 2026-02-26

**Parameters:**
- SCOPE: DEL-001-02_Floor-Plans
- MODE: UPDATE
- STRICTNESS: CONSERVATIVE
- CONSUMER_CONTEXT: TASK_ESTIMATING
- SOURCE_DOCS: AUTO (resolved below)
- ANCHOR_DOC: AUTO (resolved to Datasheet.md)
- EXECUTION_DOC_ORDER: AUTO (resolved order below)

**Resolved paths and defaults:**
- RUN_ROOT: `/Users/ryan/ai-env/projects/chirality-project-test/test/AB-2026-01424-WDMLRL-2026-Claude/PKG-001_Architectural Design/1_Working/DEL-001-02_Floor-Plans`
- DECOMPOSITION_PATH: `/Users/ryan/ai-env/projects/chirality-project-test/test/AB-2026-01424-WDMLRL-2026-Claude/_Decomposition/WDMLRL_Decomposition_Claude.md` (available, validated)
- ANCHOR_DOC: `Datasheet.md` (selected by heuristic: filename contains "datasheet"; confirmed as highest-confidence definition/traceability source)
- EXECUTION_DOC_ORDER: `Procedure.md`, `Specification.md`, `Guidance.md` (Procedure contains explicit prerequisites and workflow steps; Specification contains requirements/verification; Guidance contains considerations and trade-offs)
- SOURCE_DOCS scanned: `Datasheet.md`, `Specification.md`, `Procedure.md`, `Guidance.md` (excluded: `_CONTEXT.md`, `_REFERENCES.md`, `_DEPENDENCIES.md`, `_SEMANTIC.md`, `_SEMANTIC_LENSING.md`, `_STATUS.md`, `Dependencies.csv`)
- _REFERENCES.md: read (used for R-04 location resolution to `_Sources/`)

**Decomposition status:** Available and validated. SOW-0011 confirmed in SSOW section C. OBJ-001 and OBJ-003 confirmed in Objectives section. All target deliverable IDs confirmed in section 7 (Deliverables by Package).

**Extraction notes:**
- Pass 1 (ANCHOR): 3 rows extracted (1 IMPLEMENTS_NODE, 2 TRACES_TO_REQUIREMENT). All identifiers explicitly present in Datasheet.md Identification table.
- Pass 2 (EXECUTION): 16 rows extracted. 6 rows carried forward from prior extraction with updated evidence paths. 10 new rows added based on thorough re-read of Procedure, Specification, and Guidance.
- Prior row DEP-001-02-E07 (previously targeting DEL-011-01 as downstream handover) renumbered to DEP-001-02-E15 to accommodate new upstream interface rows. DependencyID reassigned; content preserved.
- New rows E07-E11 capture structural discipline interfaces (service pit, mezzanine, crane supports, steel plate embedments, Old North Shop renovation) that were explicitly referenced in Procedure steps and Guidance considerations.
- New row E12 captures downstream handover to Building Permit Application (DEL-009-02) explicitly stated in Procedure Steps 7.2 and 9.1.
- New row E13 captures the Alberta Building Code as an explicit CONSTRAINT (document-type dependency). Edition TBD per Conflict CONF-004.
- New row E14 captures Appendix B conceptual drawing (R-04) as an explicit prerequisite document input. SatisfactionStatus set to SATISFIED as document is available.
- New row E16 captures downstream handover to Electrical Lighting Plans (DEL-004-04) explicitly named in Procedure Step 6.1.
- CONSUMER_CONTEXT=TASK_ESTIMATING: EstimateImpactClass and ConsumerHint populated for all EXECUTION rows.

**Warnings:**
- (none)

**Quality check results:**
- Schema: All 30 required columns present. CSV parseable.
- DependencyID: All 19 IDs unique.
- Evidence: All ACTIVE rows have EvidenceFile and SourceRef populated.
- Enums: All values canonical (v3.1 write form).
- Parent anchor: Exactly 1 ACTIVE IMPLEMENTS_NODE row (DEP-001-02-A01). No warning.
- Duplicate check: No obvious duplicates. DEL-001-09 and DEL-001-10 interfaces merged into single row E11 with justification in Notes.
- _DEPENDENCIES.md counts: 19 ACTIVE, 0 RETIRED -- consistent with CSV.

## Run History

| Timestamp | Mode | Strictness | Decomposition | Warnings | ACTIVE Count |
|---|---|---|---|---|---|
| 2026-02-26 (prior run) | UPDATE | CONSERVATIVE | Available | (not recorded) | 11 |
| 2026-02-26 | UPDATE | CONSERVATIVE | Available (validated) | None | 19 |

## Lifecycle Summary

| Status | Count |
|---|---|
| ACTIVE | 19 |
| RETIRED | 0 |

### Closure state breakdown (ACTIVE rows)

| SatisfactionStatus | Count |
|---|---|
| PENDING | 15 |
| TBD | 3 |
| SATISFIED | 1 |

**Notes:**
- 3 ANCHOR rows have SatisfactionStatus=TBD (anchors are structural links; satisfaction is not applicable in the execution sense but tracked for completeness).
- 15 EXECUTION rows are PENDING (upstream inputs not yet received or downstream handovers not yet made).
- 1 EXECUTION row (DEP-001-02-E14, Appendix B conceptual drawing) is SATISFIED (document available in _Sources/).

## Downstream Handoff Notes

**Consumer context: TASK_ESTIMATING**

The following observations are relevant for downstream estimating workflows:

1. **BLOCKING dependencies (4 rows):** DEP-001-02-E01 (DEL-001-01 preliminary design approval), DEP-001-02-E02 (DEL-008-01 geotech report), DEP-001-02-E03 (DEL-008-02 site survey), DEP-001-02-E04 (DEL-002-03 structural framing/column grid). These represent hard prerequisites or critical-path inputs. Estimating for DEL-001-02 cannot be finalized until these dependencies are addressed or assumptions are established.

2. **BLOCKING constraint (1 row):** DEP-001-02-E13 (Alberta Building Code). The applicable edition and occupancy classification are TBD. Code analysis determines egress, fire separations, and accessible design requirements, all of which affect floor plan scope and quantities.

3. **ADVISORY dependencies (9 rows):** Structural detail interfaces (DEL-002-05, DEL-002-06, DEL-002-07, DEL-002-08), mechanical interface (DEL-003-02), plumbing interface (DEL-006-04), Old North Shop coordination (DEL-001-09), and downstream handovers (DEL-009-02, DEL-011-01). These are likely to change quantities/specs but are not hard gates for initial estimating.

4. **INFO dependencies (2 rows):** R-04 Appendix B (already satisfied) and DEL-004-04 lighting plans (downstream consumer).

5. **Estimating readiness assessment:** Initial estimating for DEL-001-02 can proceed with assumptions for the 4 BLOCKING prerequisites (using RFP conceptual dimensions and normal ground conditions), but final estimating requires resolution of those 4 dependencies plus the Alberta Building Code edition confirmation. The Architect's drawing sheet count, scale conventions, and CAD/BIM standards (noted as TBD in Datasheet.md Construction section) also affect estimating scope.
