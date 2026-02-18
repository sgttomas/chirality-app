# Dependencies

**Deliverable ID:** DEL-10-02
**Deliverable Name:** Site Conditions and Due Diligence Summary
**Package:** PKG-010 -- Due Diligence & Risk Management
**Tracking Mode:** DECLARED + EXTRACTED

## Upstream Dependencies (this deliverable depends on)

_No critical dependencies declared._

## Downstream Dependents (other deliverables depend on this)

_No critical dependents declared._

## Notes

Dependencies are human-curated. Only interface-critical dependencies are recorded here.

---

## Extracted Dependency Register

**Total ACTIVE rows:** 16
**Total RETIRED rows:** 0

### ANCHOR Dependencies (4 ACTIVE)

| DependencyID | AnchorType | TargetType | TargetRefID / TargetName | Confidence |
|---|---|---|---|---|
| DEP-10-02-001 | IMPLEMENTS_NODE | WBS_NODE | PKG-010 -- Due Diligence & Risk Management | HIGH |
| DEP-10-02-002 | TRACES_TO_REQUIREMENT | REQUIREMENT | SOW-0026 | HIGH |
| DEP-10-02-003 | TRACES_TO_REQUIREMENT | REQUIREMENT | SOW-0027 | HIGH |
| DEP-10-02-004 | TRACES_TO_REQUIREMENT | REQUIREMENT | OBJ-008 | HIGH |

### EXECUTION Dependencies -- UPSTREAM (7 ACTIVE)

| DependencyID | DependencyType | TargetType | TargetName | Confidence |
|---|---|---|---|---|
| DEP-10-02-005 | PREREQUISITE | DOCUMENT | RFP Appendix D -- 2021 Geotechnical Investigation Report | HIGH |
| DEP-10-02-006 | PREREQUISITE | DOCUMENT | RFP Appendix D -- Wetland Assessment and Impact Report | HIGH |
| DEP-10-02-007 | PREREQUISITE | DOCUMENT | RFP Appendix D -- Desktop Environmental Assessment | HIGH |
| DEP-10-02-008 | PREREQUISITE | DOCUMENT | RFP Appendix E -- Site Grading Documentation | MEDIUM |
| DEP-10-02-009 | PREREQUISITE | DOCUMENT | RFP Appendix F -- Site Plan / Subdivision Plan | MEDIUM |
| DEP-10-02-010 | PREREQUISITE | DOCUMENT | Flood Zone Mapping | MEDIUM |
| DEP-10-02-011 | CONSTRAINT | EXTERNAL | DEC-013 -- No additional geotechnical investigation | HIGH |

### EXECUTION Dependencies -- DOWNSTREAM (5 ACTIVE)

| DependencyID | DependencyType | TargetType | TargetDeliverableID | TargetName | Confidence |
|---|---|---|---|---|---|
| DEP-10-02-012 | HANDOVER | DELIVERABLE | DEL-10-01 | Risk Register and Mitigation Plan | HIGH |
| DEP-10-02-013 | HANDOVER | DELIVERABLE | DEL-02-02 | Civil Site Concept Plan | HIGH |
| DEP-10-02-014 | HANDOVER | DELIVERABLE | DEL-02-03 | Structural Concept Narrative | HIGH |
| DEP-10-02-015 | HANDOVER | DELIVERABLE | DEL-05-02 | Structural Durability and Maintenance | HIGH |
| DEP-10-02-016 | HANDOVER | DELIVERABLE | DEL-01-06 | Pricing Narrative and Assumptions | HIGH |

---

## Run Notes

**Run timestamp:** 2026-02-17
**Mode:** UPDATE
**Strictness:** CONSERVATIVE
**Consumer context:** NONE
**Decomposition path:** /Users/ryan/ai-env/projects/chirality-app-test/test/execution-6b/_Decomposition/Penhold_PSB_Project_Decomposition_v2.md (v2.3 FINAL)
**Decomposition status:** Available and validated. All anchor IDs confirmed against decomposition content.

**Source documents scanned (AUTO):**
- ANCHOR_DOC: Datasheet.md (selected: contains Identification table with scope items, objectives, package ID)
- EXECUTION_DOCS (order): Guidance.md, Procedure.md, Specification.md, Datasheet.md
- _REFERENCES.md: Read for target resolution (document pointers)
- _CONTEXT.md: Read for deliverable identity confirmation

**Defaults applied:**
- SOURCE_DOCS=AUTO: All four deliverable source documents scanned (Datasheet.md, Guidance.md, Procedure.md, Specification.md)
- DOC_ROLE_MAP=DEFAULT: Datasheet.md selected as ANCHOR_DOC; Guidance.md, Procedure.md, Specification.md as EXECUTION_DOCS
- ANCHOR_DOC=AUTO: Datasheet.md (highest confidence -- contains Identification table with explicit IDs)
- EXECUTION_DOC_ORDER=AUTO: Guidance.md first (Downstream Use table is primary execution signal), then Procedure.md (Prerequisites and Handoff tables), then Specification.md (requirement cross-references)

**Warnings:** None.

**Pass 1 (ANCHOR) findings:**
- 1 parent anchor (IMPLEMENTS_NODE) to PKG-010 -- confirmed in decomposition
- 2 scope item traces (SOW-0026, SOW-0027) -- confirmed in decomposition scope ledger
- 1 objective trace (OBJ-008) -- confirmed in decomposition objectives

**Pass 2 (EXECUTION) findings:**
- 7 UPSTREAM edges: 6 PREREQUISITE (document inputs including 3 BLOCKING Appendix D reports, 2 refinement Appendix E/F, 1 BLOCKING flood zone mapping with TBD source), 1 CONSTRAINT (DEC-013)
- 5 DOWNSTREAM edges: all HANDOVER type to DEL-10-01, DEL-02-02, DEL-02-03, DEL-05-02, DEL-01-06

**Edges NOT extracted (rationale):**
- DEL-07-01 (Construction Methodology): Guidance C-002 mentions construction constraints cross-reference with DEL-07-01, but this is coordination ("address this in construction methodology cross-reference") rather than a specific data/artifact transfer. Excluded per protocol (information flow only).
- RFP Sections 2.3 and 7.4: These are general source references rather than specific prerequisite inputs requiring receipt/approval. The Appendix D/E/F documents are the actual blocking inputs; the RFP section references are contextual.
- Addendum 03: While frequently cited, Addendum 03 is a general project-level document that governs all deliverables. It does not represent a specific information transfer to DEL-10-02 beyond what is captured through the scope item traces (SOW-0026, SOW-0027).

---

## Run History

| Timestamp | Mode | Strictness | Decomposition | Warnings | ACTIVE ANCHOR | ACTIVE EXECUTION |
|---|---|---|---|---|---|---|
| 2026-02-17 | UPDATE | CONSERVATIVE | v2.3 FINAL (available) | None | 4 | 12 |

---

## Lifecycle Summary

| Category | ACTIVE | RETIRED |
|---|---|---|
| ANCHOR (IMPLEMENTS_NODE) | 1 | 0 |
| ANCHOR (TRACES_TO_REQUIREMENT) | 3 | 0 |
| EXECUTION (UPSTREAM) | 7 | 0 |
| EXECUTION (DOWNSTREAM) | 5 | 0 |
| **Total** | **16** | **0** |

### Closure State Breakdown (ACTIVE rows only)

| SatisfactionStatus | Count | Notes |
|---|---|---|
| NOT_APPLICABLE | 4 | All ANCHOR rows |
| PENDING | 6 | Upstream document prerequisites (awaiting access to Appendix D/E/F PDFs and flood zone mapping) |
| SATISFIED | 1 | DEC-013 constraint (decision already made and incorporated) |
| TBD | 5 | Downstream handovers (satisfaction depends on consumer deliverable drafting) |
