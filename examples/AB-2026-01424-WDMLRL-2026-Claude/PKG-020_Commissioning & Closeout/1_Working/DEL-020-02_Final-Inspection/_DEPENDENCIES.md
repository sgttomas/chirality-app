# DEL-020-02: Dependencies

**Deliverable ID:** DEL-020-02_Final-Inspection
**Dependency Tracking Status:** TRACKED
**Register Schema:** v3.1

## Upstream Dependencies
- **DEL-020-01** (Commissioning): All building systems must be commissioned and operational before final inspection
- **PKG-019** (Construction Management & OH&S): All construction activities must be substantially complete and quality control verified
- **PKG-009** (Permitting & Regulatory Compliance): All Alberta Safety Code permit inspections must be completed and approved before requesting Owner final inspection

## Internal Package Dependencies
- **DEL-020-03** (Closeout-Docs): Final inspection results and CCC are included in closeout documentation

## External Package Dependencies
- **PKG-021** (Bonding, Insurance & Warranty): CCC issuance date establishes the start of the 2-year guarantee period

## Cross-Project Dependencies
None currently identified.

## Dependency Notes
Final inspection cannot occur until commissioning is substantially complete. CCC issuance marks substantial completion and triggers remaining deficiency remediation and final closeout activities.

## Monitoring
Dependencies will be monitored through status reports and coordination with commissioning and construction teams.

---

## Extracted Dependency Register

**Total ACTIVE rows:** 14 (6 ANCHOR + 8 EXECUTION)
**Total RETIRED rows:** 0

### ANCHOR Rows (6 ACTIVE)

| DependencyID | AnchorType | TargetType | TargetRefID | TargetName | Confidence |
|---|---|---|---|---|---|
| DEP-020-02-001 | IMPLEMENTS_NODE | WBS_NODE | PKG-020 | Commissioning & Closeout | HIGH |
| DEP-020-02-002 | TRACES_TO_REQUIREMENT | REQUIREMENT | SOW-0091 | Complete all Work on or before December 31 2026 | HIGH |
| DEP-020-02-003 | TRACES_TO_REQUIREMENT | REQUIREMENT | SOW-0092 | Conduct final self-inspection and request final Owner inspection | HIGH |
| DEP-020-02-004 | TRACES_TO_REQUIREMENT | REQUIREMENT | SOW-0093 | Provide documentation for CCC | HIGH |
| DEP-020-02-005 | TRACES_TO_REQUIREMENT | REQUIREMENT | OBJ-001 | Code-compliant fully functional delivery | HIGH |
| DEP-020-02-006 | TRACES_TO_REQUIREMENT | REQUIREMENT | OBJ-002 | Complete all work on or before December 31 2026 | HIGH |

### EXECUTION Rows (8 ACTIVE)

| DependencyID | Direction | DependencyType | TargetType | Target | Confidence | EstimateImpactClass |
|---|---|---|---|---|---|---|
| DEP-020-02-007 | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-020-01_Commissioning | HIGH | BLOCKING |
| DEP-020-02-008 | UPSTREAM | PREREQUISITE | PACKAGE | PKG-019 (Construction Management & OH&S) | HIGH | BLOCKING |
| DEP-020-02-009 | DOWNSTREAM | HANDOVER | DELIVERABLE | DEL-020-03_Closeout-Docs | HIGH | ADVISORY |
| DEP-020-02-010 | UPSTREAM | PREREQUISITE | PACKAGE | PKG-009 (Permitting & Regulatory Compliance) | HIGH | BLOCKING |
| DEP-020-02-011 | UPSTREAM | CONSTRAINT | DOCUMENT | CCDC 14-2013 | MEDIUM | ADVISORY |
| DEP-020-02-012 | UPSTREAM | PREREQUISITE | DOCUMENT | IFC Drawings (all disciplines) | HIGH | ADVISORY |
| DEP-020-02-013 | DOWNSTREAM | ENABLES | PACKAGE | PKG-021 (Bonding, Insurance & Warranty) | HIGH | INFO |
| DEP-020-02-014 | UPSTREAM | CONSTRAINT | DOCUMENT | RFP AB-2026-01424-WDMLRL | HIGH | BLOCKING |

---

## Run Notes

### Run: 2026-02-26

**Parameters:**
- MODE: UPDATE
- STRICTNESS: CONSERVATIVE
- CONSUMER_CONTEXT: TASK_ESTIMATING
- SOURCE_DOCS: AUTO

**Paths used:**
- RUN_ROOT: `/Users/ryan/ai-env/projects/chirality-project-test/test/AB-2026-01424-WDMLRL-2026-Claude`
- DECOMPOSITION_PATH: `_Decomposition/WDMLRL_Decomposition_Claude.md` (found, validated)
- DELIVERABLE_PATH: `PKG-020_Commissioning & Closeout/1_Working/DEL-020-02_Final-Inspection/`

**Source document resolution (AUTO):**
- ANCHOR_DOC: `Datasheet.md` (selected by heuristic: contains "datasheet" in filename; highest anchor-signal match)
- EXECUTION_DOC_ORDER: `Procedure.md`, `Specification.md`, `Guidance.md` (ordered by workflow clarity)
- Excluded from scan: `_DEPENDENCIES.md`, `_REFERENCES.md`, `_CONTEXT.md`, `_SEMANTIC.md`, `_SEMANTIC_LENSING.md`, `_STATUS.md` (generated/metadata files)

**Decomposition validation:**
- DEL-020-02_Final-Inspection confirmed in decomposition Section 7, PKG-020 deliverable table (line 569)
- PKG-020 confirmed in decomposition Section 6, Management & Closeout Packages (line 353)
- SOW-0091, SOW-0092, SOW-0093 confirmed in decomposition Section 8 scope ledger (lines 684-686)
- OBJ-001, OBJ-002 confirmed in decomposition Section 5 objectives (lines 302-303)
- All anchor targets validated successfully against decomposition

**Defaults applied:**
- `DOC_ROLE_MAP`: DEFAULT
- `ANCHOR_DOC`: AUTO -> Datasheet.md
- `EXECUTION_DOC_ORDER`: AUTO -> Procedure.md, Specification.md, Guidance.md

**Assumptions recorded:**
- DEP-020-02-010: REQ-020-02-012 (Safety Code inspection prerequisite) is marked ASSUMPTION in the source specification, pending confirmation. Extracted as PREREQUISITE with HIGH confidence because the logical inference is strong (RFP SS3.3.2) but the requirement itself is flagged as pending confirmation.

**Warnings:**
- None. All integrity checks passed.

**Quality checks passed:**
- [PASS] Required columns present and CSV parseable (31 columns, 14 rows)
- [PASS] DependencyID unique within register (14 unique IDs)
- [PASS] All ACTIVE rows have EvidenceFile and SourceRef
- [PASS] Status and SatisfactionStatus values are canonical
- [PASS] Parent anchor check: exactly 1 ACTIVE IMPLEMENTS_NODE (DEP-020-02-001 -> PKG-020)
- [PASS] FromDeliverableID consistent: all rows = DEL-020-02_Final-Inspection
- [PASS] No obvious duplicate rows
- [PASS] Enum values normalized to write form
- [PASS] TargetDeliverableID populated only for TargetType=DELIVERABLE; TargetRefID used for non-deliverable targets

---

## Run History

| Timestamp | Mode | Strictness | Decomposition | Warnings | ANCHOR ACTIVE | EXECUTION ACTIVE | Total ACTIVE |
|---|---|---|---|---|---|---|---|
| 2026-02-26 | UPDATE | CONSERVATIVE | _Decomposition/WDMLRL_Decomposition_Claude.md (validated) | None | 6 | 8 | 14 |

---

## Lifecycle Summary

### Extraction Lifecycle
| Status | Count |
|---|---|
| ACTIVE | 14 |
| RETIRED | 0 |

### Closure Lifecycle (ACTIVE rows)
| SatisfactionStatus | Count |
|---|---|
| NOT_APPLICABLE | 6 |
| PENDING | 7 |
| TBD | 1 |

**Notes:** The 6 NOT_APPLICABLE rows are ANCHOR class (traceability links, not satisfiable in the execution sense). The 7 PENDING rows are EXECUTION prerequisites/handovers/enables that have not yet been fulfilled. The 1 TBD row (DEP-020-02-011) is the CCDC 14-2013 constraint where satisfaction status cannot be determined until the full contract text is reviewed.

---

## Downstream Handoff Notes

**Consumer context:** TASK_ESTIMATING

### Estimating-Relevant Dependencies

**BLOCKING (4 rows):** These dependencies gate meaningful estimating. Scope or key quantities for DEL-020-02 cannot be fully estimated without resolution of these inputs.

| DependencyID | Target | Statement |
|---|---|---|
| DEP-020-02-007 | DEL-020-01_Commissioning | Commissioning must be substantially complete before final inspection can proceed. Estimating impact: the scope of final inspection depends on commissioning outcomes (systems verified, deficiencies identified during commissioning). |
| DEP-020-02-008 | PKG-019 (Construction Mgmt) | All construction must be substantially complete and QC verified. Estimating impact: the volume and complexity of inspection items depends on what has been constructed and QC-verified. |
| DEP-020-02-010 | PKG-009 (Permitting) | Safety Code inspections must be complete. Estimating impact: Safety Code inspection outcomes may generate additional remediation scope before final inspection. |
| DEP-020-02-014 | RFP AB-2026-01424-WDMLRL | RFP governs all inspection and CCC requirements. Estimating impact: the RFP is already accessible and its requirements are documented in the deliverable's Specification. This is BLOCKING because it is the normative authority for all requirements. |

**ADVISORY (4 rows):** These dependencies are likely to influence quantities, specifications, or approach but do not constitute hard gates for estimating.

| DependencyID | Target | Statement |
|---|---|---|
| DEP-020-02-009 | DEL-020-03_Closeout-Docs | CCC and inspection summary are outputs forwarded downstream. Estimating impact: the documentation effort for producing the CCC and consolidated summary should be included in the DEL-020-02 estimate. |
| DEP-020-02-011 | CCDC 14-2013 | Contract form may impose additional CCC format or issuance requirements not visible in the RFP. Estimating impact: if CCDC 14-2013 requires additional documentation or process steps, the estimate would need to account for them. |
| DEP-020-02-012 | IFC Drawings | IFC drawings must be current before inspection. Estimating impact: the effort to verify IFC drawings against as-built conditions should be included; the number of drawing sheets depends on design package scope. |

**INFO (1 row):**

| DependencyID | Target | Statement |
|---|---|---|
| DEP-020-02-013 | PKG-021 (Warranty) | CCC triggers the 2-year guarantee period. Estimating impact: low for DEL-020-02 estimation; the guarantee period is a PKG-021 concern. |

### Key Estimating Observations

1. **DEL-020-02 is a process/closeout deliverable, not a construction deliverable.** The primary cost drivers are labor-hours for inspection walkthrough, deficiency documentation, remediation coordination, and administrative effort for the CCC process.

2. **The largest estimating uncertainty is deficiency volume.** The number and severity of deficiencies discovered during self-inspection and Owner inspection is unknown until construction and commissioning are substantially complete. This makes DEP-020-02-007 (commissioning) and DEP-020-02-008 (construction management) the most impactful BLOCKING dependencies for estimating.

3. **The CCC issuance is Owner-controlled.** The Proponent cannot self-certify completion. Estimating should include contingency for re-inspection cycles if the Owner identifies additional deficiencies or declines CCC on first attempt.
