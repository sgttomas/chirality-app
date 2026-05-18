# Dependencies: DEL-002-07 Crane Support Structure Details

## Coordination (human-owned)
- **Mode:** NOT_TRACKED
- **Notes:** Coordination representation pending -- to be confirmed by human via ORCHESTRATOR.

## Upstream (I need these before I can proceed) -- human-owned declarations
- Dependencies coordinated externally by humans.

## Downstream (These need me) -- human-owned declarations
- Dependencies coordinated externally by humans.

## Extracted Dependency Register

- **Status:** COMPLETE
- **Dependencies.csv:** 13 rows (13 ACTIVE, 0 RETIRED)
- **Schema Version:** v3.1

### ANCHOR Edges (3 ACTIVE)

| DependencyID | AnchorType | TargetType | TargetRefID | TargetName | Confidence |
|---|---|---|---|---|---|
| DEP-002-07-A01 | IMPLEMENTS_NODE | WBS_NODE | SOW-0012 | Complete final structural design (concrete structure 35' ceiling) | HIGH |
| DEP-002-07-A02 | TRACES_TO_REQUIREMENT | REQUIREMENT | OBJ-001 | Code-compliant fully functional maintenance shop addition | HIGH |
| DEP-002-07-A03 | TRACES_TO_REQUIREMENT | REQUIREMENT | OBJ-003 | Complete P.Eng.-stamped IFC design documentation | HIGH |

### EXECUTION Edges -- UPSTREAM (7 ACTIVE)

| DependencyID | DependencyType | TargetType | TargetID | TargetName | EstimateImpactClass | Confidence |
|---|---|---|---|---|---|---|
| DEP-002-07-E01 | PREREQUISITE | DELIVERABLE | DEL-016-01 | Two 5-Tonne Overhead Cranes (Crane Supplier Data Sheet) | BLOCKING | HIGH |
| DEP-002-07-E04 | PREREQUISITE | DELIVERABLE | DEL-002-01 | Preliminary Structural Design | BLOCKING | HIGH |
| DEP-002-07-E05 | PREREQUISITE | DELIVERABLE | DEL-008-01 | Geotechnical Investigation & Report | BLOCKING | HIGH |
| DEP-002-07-E07 | CONSTRAINT | EXTERNAL | SOW-0006 | Building Permit | BLOCKING | HIGH |
| DEP-002-07-E02 | INTERFACE | DELIVERABLE | DEL-002-03 | Structural Framing Plans | ADVISORY | HIGH |
| DEP-002-07-E06 | INTERFACE | DELIVERABLE | DEL-002-04 | Structural Sections & Details | ADVISORY | HIGH |
| DEP-002-07-E03 | INTERFACE | DELIVERABLE | DEL-004-03 | Power Distribution Plans | ADVISORY | MEDIUM |

### EXECUTION Edges -- DOWNSTREAM (3 ACTIVE)

| DependencyID | DependencyType | TargetType | TargetID | TargetName | EstimateImpactClass | Confidence |
|---|---|---|---|---|---|---|
| DEP-002-07-E08 | HANDOVER | DELIVERABLE | DEL-002-10 | Structural Calculation Package | ADVISORY | HIGH |
| DEP-002-07-E09 | HANDOVER | DELIVERABLE | DEL-016-01 | Two 5-Tonne Overhead Cranes | ADVISORY | HIGH |
| DEP-002-07-E10 | HANDOVER | DELIVERABLE | DEL-011-01 | Concrete Superstructure | ADVISORY | HIGH |

---

## Run Notes

### Run: 2026-03-26 (SCA-001 refresh)

**Parameters:**
- SCOPE: PKG-002 (all deliverables DEL-002-01 through DEL-002-12)
- MODE: UPDATE | STRICTNESS: CONSERVATIVE | CONSUMER_CONTEXT: NONE
- DECOMPOSITION_PATH: `_Decomposition/WDMLRL_Decomposition_Claude.md` (R2 -- 2026-03-26, SCA-001)
- SOURCE_DOCS: AUTO | ANCHOR_DOC: Datasheet.md | EXECUTION_DOC_ORDER: Procedure.md, Specification.md, Guidance.md

**SCA-001 impact assessment (significant for this deliverable):**
- SOW-0067 updated: "hook height 26' (Add. 3, Q3); max 25' runway bay spacing (Add. 4, Q2); corbel-supported on side walls -- crane supplier provides loading to contractor (Add. 4, Q3)."
- _CONTEXT.md updated (2026-03-26): "Crane support via corbels on side walls (not free-standing). Max 25' runway bay spacing. Hook height 26'. Crane supplier provides loading data to contractor (Add. 3 Q3, Add. 4 Q2-3)."
- **Key resolutions from addenda:**
  1. **Support type resolved:** Corbels on side walls confirmed (Add. 4, Q3). Prior run noted "Support configuration (corbels vs. dedicated crane columns) is TBD." This uncertainty is now resolved. The corbel support means crane loads transfer directly into precast wall panels, creating a tighter structural interface between crane support and wall panel design.
  2. **25' max bay spacing:** New explicit dimensional constraint (Add. 4, Q2). Affects column/wall spacing shown on framing plans.
  3. **26' hook height:** New explicit minimum (Add. 3, Q3). Constrains runway beam elevation relative to 35' ceiling.
  4. **Crane supplier provides loading:** Confirms that crane loading data flows from supplier to contractor (design-builder). This aligns with existing DEP-002-07-E01 (crane supplier data prerequisite).
- **Impact on existing dependencies:** All 13 existing rows remain valid. The crane supplier data prerequisite (E01) is reinforced by Add. 4 Q3 ("crane supplier provides loading to contractor"). The framing plans interface (E02) is reinforced by the 25' bay spacing constraint. No existing edges are invalidated.
- **Potential new dependency signal:** Precast wall panel design data (corbel locations, panel dimensions, connection capacity) becomes a structural interface because corbels are cast into/attached to precast panels. This would be a new EXTERNAL or DELIVERABLE interface. However, source documents (Datasheet, Procedure, Specification, Guidance) have not yet been updated to list precast panel data as an explicit crane support input. Under CONSERVATIVE strictness, no new row emitted.
- **Recommendation:** After source documents are updated, a precast wall panel interface dependency should be extracted. The corbel-to-precast-panel connection is a critical structural interface that warrants an explicit EXECUTION row.

**Extraction result:**
- All 13 existing ACTIVE rows re-confirmed. LastSeen updated to 2026-03-26.
- No new rows. No RETIRED rows.

**Warnings:**
- None. Parent anchor present and unique.

**Note on prior Downstream Handoff Notes:** The prior run's note that "Support configuration (corbels vs. dedicated crane columns) is TBD" is now partially resolved by Add. 4, Q3 confirming corbel support. This reduces estimating uncertainty for crane support structural quantities.

---

### Run 2026-02-26 (initial extraction)

**Parameters:**
- SCOPE: DEL-002-07_Crane-Support-Details
- RUN_ROOT: `PKG-002_Structural Design/1_Working/DEL-002-07_Crane-Support-Details/`
- DECOMPOSITION_PATH: `_Decomposition/WDMLRL_Decomposition_Claude.md` (R1 2026-02-25) -- AVAILABLE, used for validation and target resolution
- MODE: UPDATE
- STRICTNESS: CONSERVATIVE
- CONSUMER_CONTEXT: TASK_ESTIMATING
- SOURCE_DOCS: AUTO (resolved below)
- ANCHOR_DOC: AUTO (resolved to `Datasheet.md`)

**Source document resolution (AUTO):**
- ANCHOR_DOC: `Datasheet.md` (contains Identification table with SOW/OBJ references -- highest anchor signal)
- EXECUTION_DOCS (in scan order):
  1. `Procedure.md` (contains explicit Prerequisites table -- highest execution signal)
  2. `Specification.md` (contains Requirements and Verification with cross-deliverable references)
  3. `Guidance.md` (contains Principles, Considerations, and Trade-offs with dependency context)

**Defaults applied:**
- DOC_ROLE_MAP: DEFAULT heuristic used. `Datasheet.md` matched ANCHOR_DOC pattern; `Procedure.md` matched EXECUTION_DOC pattern.
- _REFERENCES.md: read for document pointer resolution; used to confirm R-01 and R-04 locations.

**Decomposition validation results:**
- SOW-0012: CONFIRMED in SSOW section C (Final Design) -- "Complete final structural design (concrete structure, 35' ceiling)"
- OBJ-001: CONFIRMED in Objectives section -- "Deliver a code-compliant, fully functional maintenance shop addition..."
- OBJ-003: CONFIRMED in Objectives section -- "Produce complete, P.Eng.-stamped IFC design documentation..."
- DEL-002-07: CONFIRMED in PKG-002 deliverables table -- "Crane Support Structure Details" / Drawing Set / SOW-0012
- All target deliverable IDs confirmed in decomposition deliverable tables.

**Prior CSV handling:**
- Prior `Dependencies.csv` contained 8 rows (DEP-002-07-A01 through DEP-002-07-E04). All anchor rows (A01-A03) were matched and refreshed. Execution rows were re-evaluated:
  - Prior DEP-002-07-E01 (crane supplier data, TargetType=EXTERNAL) was updated: target resolved to DEL-016-01 (DELIVERABLE) via decomposition, DependencyType corrected from implicit to PREREQUISITE based on Procedure Prerequisites table evidence.
  - Prior DEP-002-07-E04 (DEL-016-01 DOWNSTREAM HANDOVER) was re-sequenced to DEP-002-07-E09 to group by direction. New DEP-002-07-E04 now holds the DEL-002-01 prerequisite.
  - DependencyID re-sequencing note: IDs were reassigned for logical grouping since this is the initial authoritative extraction run. All prior rows were provisional.
- 5 new EXECUTION rows added (E05-E08, E10) based on explicit evidence in Procedure.md and Specification.md.

**Warnings:** None.

**Integrity check results:**
- Parent anchor (IMPLEMENTS_NODE): 1 ACTIVE row (DEP-002-07-A01) -- PASS
- DependencyID uniqueness: 13 unique / 13 total -- PASS
- All ACTIVE rows have EvidenceFile and SourceRef -- PASS
- FromDeliverableID consistency: all rows = DEL-002-07 -- PASS
- CSV parseable with 31 columns, 13 data rows -- PASS
- No duplicate rows detected -- PASS

---

## Run History

| Timestamp | Mode | Strictness | Consumer | Decomposition | Warnings | ANCHOR Active | EXECUTION Active | Total Active |
|---|---|---|---|---|---|---|---|---|
| 2026-03-26 | UPDATE | CONSERVATIVE | NONE | WDMLRL_Decomposition_Claude.md R2 SCA-001 (available) | None | 3 | 10 | 13 |
| 2026-02-26 | UPDATE | CONSERVATIVE | TASK_ESTIMATING | WDMLRL_Decomposition_Claude.md R1 (available) | None | 3 | 10 | 13 |

---

## Lifecycle Summary

| Category | Count |
|---|---|
| Total rows | 13 |
| ACTIVE | 13 |
| RETIRED | 0 |

### By DependencyClass

| Class | ACTIVE | RETIRED |
|---|---|---|
| ANCHOR | 3 | 0 |
| EXECUTION | 10 | 0 |

### By SatisfactionStatus (ACTIVE rows)

| SatisfactionStatus | Count |
|---|---|
| TBD | 13 |

### By EstimateImpactClass (EXECUTION ACTIVE rows)

| EstimateImpactClass | Count |
|---|---|
| BLOCKING | 4 |
| ADVISORY | 6 |

---

## Downstream Handoff Notes

**Consumer context: TASK_ESTIMATING**

The following observations are relevant for downstream task estimating workflows:

**BLOCKING dependencies (4):** These gate meaningful estimating of DEL-002-07 scope. Key quantities (runway beam sizing, support configuration, connection details) cannot be finalized without:
1. **DEP-002-07-E01 -- Crane supplier data sheet (DEL-016-01):** The single most critical upstream input. Crane wheel loads, bridge geometry, rail requirements, and minimum hook height are fundamental design inputs. Without this data, structural sizing is based on assumed conservative loads (see Procedure Step 1.4 fallback path). Estimating crane support material quantities under assumed loads carries rework risk.
2. **DEP-002-07-E04 -- Preliminary structural design approval (DEL-002-01):** County approval is a contractual gate (RFP SS3.3.2). IFC drawings cannot be issued without this approval. Estimating effort should account for potential revision cycles if preliminary approach changes.
3. **DEP-002-07-E05 -- Geotechnical report (DEL-008-01):** Required for crane column/foundation bearing capacity. If crane support uses dedicated columns, foundation design depends on geotechnical data.
4. **DEP-002-07-E07 -- Building permit (SOW-0006):** Procedure Step 6B explicitly gates IFC stamp on building permit status. This is a hard constraint on deliverable completion.

**ADVISORY dependencies (6):** These affect quantities, specs, or scope detail but do not hard-gate estimating:
- Structural framing plans (DEL-002-03) and structural sections (DEL-002-04) provide the building grid and column layout context.
- Electrical coordination (DEL-004-03) affects conductor bar/festoon zone -- minor quantity impact on structural drawings.
- Downstream handovers to DEL-002-10, DEL-016-01, and DEL-011-01 define distribution obligations but do not constrain estimating of DEL-002-07 itself.

**Key estimating uncertainties:**
- Support configuration (corbels vs. dedicated crane columns) is TBD, pending structural engineer decision. This materially affects structural quantities.
- Crane arrangement (shared runway vs. two independent runways) is TBD per CONF-007-02.
- Runway beam material is assumed steel wide-flange (standard practice) but not confirmed.
