# DEL-008-01 Dependencies

## Upstream Dependencies
None identified. This deliverable is a foundational investigation without upstream technical dependencies.

## Downstream Dependencies
- **PKG-002**: Foundation Design (requires geotech investigation results)
- **PKG-010**: Detailed Design Packages (requires geotechnical characterization)

## External Dependencies
- Site access for field investigations
- Client approval for investigation methodology
- Weather conditions for field work execution

## Tracking Status
**TRACKED** -- Dependencies extracted and registered in Dependencies.csv (v3.1).

## Notes
This deliverable initiates the geotechnical characterization stream and provides foundational data for multiple downstream packages.

---

## Extracted Dependency Register

**Total ACTIVE rows:** 16 (3 ANCHOR + 13 EXECUTION)
**Total RETIRED rows:** 0

### ANCHOR Edges (3 ACTIVE)

| DependencyID | AnchorType | TargetRefID | TargetName | Confidence |
|---|---|---|---|---|
| DEP-008-01-A001 | IMPLEMENTS_NODE | SOW-0001 | Conduct geotechnical investigation and provide complete report to Owner | HIGH |
| DEP-008-01-A002 | TRACES_TO_REQUIREMENT | OBJ-003 | Design documentation completeness | HIGH |
| DEP-008-01-A003 | TRACES_TO_REQUIREMENT | OBJ-006 | Contract price reconciliation -- foundation variable-price element | HIGH |

### EXECUTION Edges -- UPSTREAM (7 ACTIVE)

| DependencyID | DependencyType | TargetType | TargetName | Confidence | EstimateImpactClass |
|---|---|---|---|---|---|
| DEP-008-01-E001 | PREREQUISITE | EXTERNAL | Contract Award (CCDC 14-2013) | HIGH | BLOCKING |
| DEP-008-01-E002 | PREREQUISITE | EXTERNAL | Site Access Authorization (County/Owner) | HIGH | BLOCKING |
| DEP-008-01-E003 | CONSTRAINT | EXTERNAL | Client Approval of Investigation Methodology | HIGH | BLOCKING |
| DEP-008-01-E004 | INTERFACE | DELIVERABLE | Preliminary Structural Design (PKG-002 / DEL-002-01) | MEDIUM | ADVISORY |
| DEP-008-01-E005 | CONSTRAINT | DELIVERABLE | Prime Contractor Designation & OH&S Program (PKG-019 / DEL-019-01) | HIGH | ADVISORY |
| DEP-008-01-E006 | PREREQUISITE | DOCUMENT | AB-2026-01424-WDMLRL RFP (R-01) | HIGH | INFO |
| DEP-008-01-E007 | PREREQUISITE | DOCUMENT | AB-2026-01424-Appendix C - Site Maps (R-07) | HIGH | INFO |

### EXECUTION Edges -- DOWNSTREAM (6 ACTIVE)

| DependencyID | DependencyType | TargetType | TargetName | Confidence | EstimateImpactClass |
|---|---|---|---|---|---|
| DEP-008-01-E008 | HANDOVER | EXTERNAL | Owner (Camrose County) | HIGH | BLOCKING |
| DEP-008-01-E009 | HANDOVER | DELIVERABLE | Foundation Design Package (PKG-002 / DEL-002-11) | HIGH | BLOCKING |
| DEP-008-01-E010 | HANDOVER | PACKAGE | Civil Design (PKG-005) | MEDIUM | ADVISORY |
| DEP-008-01-E011 | HANDOVER | PACKAGE | Foundation Construction (PKG-010) | MEDIUM | ADVISORY |
| DEP-008-01-E012 | ENABLES | EXTERNAL | Foundation Pricing Negotiation (RFP S4.8.2) | HIGH | BLOCKING |
| DEP-008-01-E013 | CONSTRAINT | EXTERNAL | County Site Preparation (Brushing/Clearing/Cut-Fill) | HIGH | ADVISORY |

---

## Run Notes

### Run 2026-02-26T2 (Refresh Extraction)

**Parameters:**
- SCOPE: DEL-008-01
- MODE: UPDATE
- STRICTNESS: CONSERVATIVE
- CONSUMER_CONTEXT: TASK_ESTIMATING
- DECOMPOSITION_PATH: /Users/ryan/ai-env/projects/chirality-project-test/test/AB-2026-01424-WDMLRL-2026-Claude/_Decomposition/WDMLRL_Decomposition_Claude.md (found, R1 2026-02-25)

**Source Documents (AUTO resolution):**
- ANCHOR_DOC: Datasheet.md (matched heuristic: filename contains "datasheet")
- EXECUTION_DOC_ORDER:
  1. Procedure.md (matched heuristic: filename contains "procedure")
  2. Specification.md (matched heuristic: filename contains "spec")
  3. Guidance.md (matched heuristic: filename contains "guidance")
  4. Datasheet.md (secondary pass for execution cues)

**Decomposition status:** Available and validated. All anchor identifiers (SOW-0001, OBJ-003, OBJ-006) confirmed present in decomposition. All deliverable/package targets resolved against decomposition Section 7.

**Defaults applied:**
- SOURCE_DOCS: AUTO (scanned deliverable folder; excluded _DEPENDENCIES.md, _REFERENCES.md, _CONTEXT.md, _SEMANTIC.md, _SEMANTIC_LENSING.md, _STATUS.md, Dependencies.csv)
- DOC_ROLE_MAP: DEFAULT heuristic
- ANCHOR_DOC: AUTO -> Datasheet.md
- EXECUTION_DOC_ORDER: AUTO -> Procedure.md, Specification.md, Guidance.md, Datasheet.md

**Warnings:**
- (none)

**Schema corrections applied (this run):**
- TargetRefID populated for ANCHOR rows (A001: SOW-0001; A002: OBJ-003; A003: OBJ-006) and DOCUMENT rows (E006: R-01; E007: R-07). Previously these stable IDs were stored only in TargetName; corrected per schema rule: "use TargetRefID (if a stable ID exists) and TargetName."
- TargetName updated for ANCHOR rows to use descriptive names rather than bare IDs.
- TargetLocation for A001 corrected from "Decomposition SSOW §A" to "Decomposition SSOW S3-A" for consistency.

**Assumptions logged in rows:**
- DEP-008-01-E004: Structural load data interface marked ASSUMPTION per source (standard practice, not explicitly in RFP). Confidence=MEDIUM.

**Quality check results:**
- Schema: PASS -- all required columns present, CSV parseable, DependencyIDs unique.
- Evidence: PASS -- all ACTIVE rows have EvidenceFile and SourceRef.
- Parent anchor: PASS -- exactly 1 IMPLEMENTS_NODE row (DEP-008-01-A001).
- Enum normalization: PASS -- all values canonical.
- Lifecycle: PASS -- all rows FirstSeen=LastSeen=2026-02-26, Status=ACTIVE.
- TargetRefID placement: PASS -- non-deliverable targets use TargetRefID for stable IDs; TargetDeliverableID empty.
- Deliverable targets: PASS -- TargetType=DELIVERABLE rows have TargetDeliverableID populated (E004: DEL-002-01; E005: DEL-019-01; E009: DEL-002-11).
- _DEPENDENCIES.md consistency: PASS -- counts match CSV (16 ACTIVE, 0 RETIRED).

### Run 2026-02-26 (Initial Extraction)

**Parameters:**
- SCOPE: DEL-008-01
- MODE: UPDATE
- STRICTNESS: CONSERVATIVE
- CONSUMER_CONTEXT: TASK_ESTIMATING
- DECOMPOSITION_PATH: /Users/ryan/ai-env/projects/chirality-project-test/test/AB-2026-01424-WDMLRL-2026-Claude/_Decomposition/WDMLRL_Decomposition_Claude.md (found, R1 2026-02-25)

**Source Documents (AUTO resolution):**
- ANCHOR_DOC: Datasheet.md (matched heuristic: filename contains "datasheet")
- EXECUTION_DOC_ORDER:
  1. Procedure.md (matched heuristic: filename contains "procedure")
  2. Specification.md (matched heuristic: filename contains "spec")
  3. Guidance.md (matched heuristic: filename contains "guidance")
  4. Datasheet.md (secondary pass for execution cues)

**Decomposition status:** Available and validated. All anchor identifiers (SOW-0001, OBJ-003, OBJ-006) confirmed present in decomposition. All deliverable/package targets resolved against decomposition Section 7.

**Defaults applied:**
- SOURCE_DOCS: AUTO (scanned deliverable folder; excluded _DEPENDENCIES.md, _REFERENCES.md, _CONTEXT.md, _SEMANTIC.md, _SEMANTIC_LENSING.md, _STATUS.md)
- DOC_ROLE_MAP: DEFAULT heuristic
- ANCHOR_DOC: AUTO -> Datasheet.md
- EXECUTION_DOC_ORDER: AUTO -> Procedure.md, Specification.md, Guidance.md, Datasheet.md

**Warnings:**
- (none)

**Assumptions logged in rows:**
- DEP-008-01-E004: Structural load data interface marked ASSUMPTION per source (standard practice, not explicitly in RFP). Confidence=MEDIUM.

**Quality check results:**
- Schema: PASS -- all required columns present, CSV parseable, DependencyIDs unique.
- Evidence: PASS -- all ACTIVE rows have EvidenceFile and SourceRef.
- Parent anchor: PASS -- exactly 1 IMPLEMENTS_NODE row (DEP-008-01-A001).
- Enum normalization: PASS -- all values canonical.
- Lifecycle: PASS -- all rows FirstSeen=LastSeen=2026-02-26, Status=ACTIVE.
- _DEPENDENCIES.md consistency: PASS -- counts match CSV (16 ACTIVE, 0 RETIRED).

---

## Run History

| Timestamp | Mode | Strictness | Decomposition | Warnings | ACTIVE Anchors | ACTIVE Execution | Total ACTIVE |
|---|---|---|---|---|---|---|---|
| 2026-02-26 | UPDATE | CONSERVATIVE | Available (R1 2026-02-25) | (none) | 3 | 13 | 16 |
| 2026-02-26T2 | UPDATE | CONSERVATIVE | Available (R1 2026-02-25) | (none) | 3 | 13 | 16 |

---

## Lifecycle Summary

| Status | Count |
|---|---|
| ACTIVE | 16 |
| RETIRED | 0 |

| SatisfactionStatus | Count |
|---|---|
| TBD | 16 |

| DependencyClass | ACTIVE | RETIRED |
|---|---|---|
| ANCHOR | 3 | 0 |
| EXECUTION | 13 | 0 |

---

## Downstream Handoff Notes

**Consumer context:** TASK_ESTIMATING

This register has been prepared with estimating-oriented extension columns (`EstimateImpactClass`, `ConsumerHint`) populated for all EXECUTION rows.

**Key findings for estimating readiness:**

1. **BLOCKING dependencies (4 upstream + 3 downstream = 7 rows):** Contract award (E001), site access (E002), and client approval (E003) are upstream hard gates -- field work cannot commence until these are resolved. Downstream, the handover to Owner (E008), foundation design package (E009), and foundation pricing negotiation (E012) are BLOCKING because they represent the primary value outputs of this deliverable that gate downstream estimating and pricing.

2. **ADVISORY dependencies (5 rows):** The structural load data interface from PKG-002 (E004) is marked ADVISORY because the source identifies it as standard practice but not an RFP requirement -- the investigation can proceed with conservative assumptions if load data is unavailable, but scope/cost may change. OH&S program (E005), civil design handover (E010), foundation construction handover (E011), and County site preparation sequencing (E013) are ADVISORY as they influence scope definition but do not hard-gate the investigation itself.

3. **INFO dependencies (2 rows):** RFP document (E006) and Site Maps (E007) are informational inputs already in hand.

4. **Variable-price mechanism:** The foundation pricing negotiation (E012) depends directly on the geotech report findings. The report's assessment of "normal ground conditions" vs. "deleterious subgrade material" (REQ-004, RFP S4.8.2) is the commercial trigger. Estimators should note that foundation scope quantities and pricing are not lockable until this report is delivered and the negotiation concludes.

5. **Scope uncertainty for estimating:** The investigation program scope (borehole count, depth, test program) is TBD by the Geotechnical Engineer (Specification -- Investigation Program Adequacy Criteria). Estimators should use parametric or allowance-based pricing until the investigation program is defined.
