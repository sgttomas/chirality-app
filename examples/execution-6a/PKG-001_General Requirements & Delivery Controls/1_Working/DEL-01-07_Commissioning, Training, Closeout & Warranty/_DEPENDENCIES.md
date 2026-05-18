# Dependencies: DEL-01-07 Commissioning, Training, Closeout & Warranty

## Coordination (human-owned)
- **Mode:** DECLARED
- **Notes:** See _Coordination/_COORDINATION.md for project-level coordination record.

## Upstream (I need these before I can proceed) -- human-owned declarations
- No upstream dependencies declared yet.

## Downstream (These need me) -- human-owned declarations
- No downstream dependencies declared yet.

## Extracted Dependency Register (populated by DEPENDENCIES agent)

- **Status:** COMPLETED
- **Dependencies.csv:** `Dependencies.csv` (14 rows)
- **Summary:**
  - ANCHOR rows: 6 (1 IMPLEMENTS_NODE + 5 TRACES_TO_REQUIREMENT)
  - EXECUTION rows: 8 (5 UPSTREAM + 1 DOWNSTREAM + 2 UPSTREAM package-level)
  - All rows ACTIVE; 0 RETIRED

### ANCHOR Edges (Tree)

| DependencyID | AnchorType | TargetRefID / TargetName | Confidence |
|---|---|---|---|
| DEP-01-07-001 | IMPLEMENTS_NODE | OBJ-009 -- Achieve operational handover readiness | HIGH |
| DEP-01-07-002 | TRACES_TO_REQUIREMENT | SOW-0013 -- Commissioning narrative/approach | HIGH |
| DEP-01-07-003 | TRACES_TO_REQUIREMENT | SOW-0014 -- Deficiency process and warranty review | HIGH |
| DEP-01-07-004 | TRACES_TO_REQUIREMENT | SOW-0015 -- Substantial Performance/Occupancy delivery | HIGH |
| DEP-01-07-005 | TRACES_TO_REQUIREMENT | SOW-0016 -- 12-month warranty and manufacturer warranty assignment | HIGH |
| DEP-01-07-006 | TRACES_TO_REQUIREMENT | SOW-0113 -- Certified as-built legal/topographical survey | HIGH |

### EXECUTION Edges (DAG)

| DependencyID | Direction | Type | Target | Statement (summary) | Confidence |
|---|---|---|---|---|---|
| DEP-01-07-007 | UPSTREAM | PREREQUISITE | DEL-01-04 Permitting Inspections & AHJ Coordination | AHJ inspection results and occupancy permit process feed into SP gate | HIGH |
| DEP-01-07-008 | UPSTREAM | PREREQUISITE | DEL-01-01 Integrated Design Management & Submission Packages | Design Brief provides system scope for commissioning planning | HIGH |
| DEP-01-07-009 | UPSTREAM | CONSTRAINT | RFP 2024_004 (DOCUMENT) | RFP sections 7.3.6/7.3.7/7.4/7.5/7.6 govern commissioning/closeout requirements | HIGH |
| DEP-01-07-010 | UPSTREAM | INTERFACE | PKG-002 Main PSB -- all design discipline outputs | As-built drawings and O&M manuals require discipline design outputs | HIGH |
| DEP-01-07-011 | UPSTREAM | INTERFACE | PKG-003 Site & Civil Works -- civil/site design outputs | Civil/site as-built data required for drawing package and survey coordination | HIGH |
| DEP-01-07-012 | UPSTREAM | INTERFACE | Vendors and manufacturers (EXTERNAL) | O&M data, testing certificates, warranties, start-up reports required | HIGH |
| DEP-01-07-013 | DOWNSTREAM | HANDOVER | Payment Certifier (EXTERNAL) | Deficiency list with monetary values provided for retention calculation | HIGH |
| DEP-01-07-014 | UPSTREAM | CONSTRAINT | CCDC 14-2013 supplementary conditions (DOCUMENT) | Defines Substantial Performance and Payment Certifier roles; may modify retention rights | MEDIUM |

## Run Notes

### Run Configuration
- **Run Date:** 2026-02-17
- **MODE:** UPDATE
- **STRICTNESS:** CONSERVATIVE
- **CONSUMER_CONTEXT:** NONE
- **SOURCE_DOCS (AUTO):** Datasheet.md, Guidance.md, Procedure.md, Specification.md
- **ANCHOR_DOC (AUTO resolved):** Datasheet.md (matched on `datasheet` keyword; contains explicit identification/traceability fields)
- **EXECUTION_DOC_ORDER (AUTO resolved):** Procedure.md, Guidance.md, Specification.md
- **DECOMPOSITION_PATH:** `_Decomposition/Penhold_PSB_Project_Decomposition_FINAL_v1.0_PHASE7.md` (found and used for validation)
- **_REFERENCES.md:** Present; used for RFP location resolution

### Defaults and Assumptions
- ANCHOR_DOC selected by heuristic: Datasheet.md is the highest-confidence match (contains `datasheet` in filename, explicit deliverable identification table with Objective, Scope Items, and Decomposition Entry fields).
- EXECUTION_DOC_ORDER: Procedure.md ranked first (contains `procedure` keyword, explicit prerequisites and step-by-step workflow), then Guidance.md (contains considerations and coordination details), then Specification.md (contains requirements and standards).
- All anchor identifiers (OBJ-009, SOW-0013 through SOW-0016, SOW-0113) validated against decomposition scope ledger and objectives table.
- All deliverable target IDs (DEL-01-04, DEL-01-01) validated against decomposition PKG-001 deliverables table.
- Package-level targets (PKG-002, PKG-003) validated against decomposition Phase 4 packages table.

### Warnings
- None. Parent anchor (IMPLEMENTS_NODE) found: exactly 1. No integrity warnings.

### Extraction Notes
- DEP-01-07-009 (RFP as DOCUMENT constraint): The RFP is a governing input, not a deliverable. TargetType=DOCUMENT; TargetDeliverableID is empty per schema rules for non-deliverable targets.
- DEP-01-07-014 (CCDC 14-2013): Document not yet accessible (location TBD). Confidence=MEDIUM because the document is referenced as applicable but its specific modifications to SP definition and retention are not yet confirmed. See OI-01-07-001 in Datasheet conflict table.
- DEP-01-07-010 and DEP-01-07-011 are package-level interfaces (TargetType=PACKAGE) rather than individual deliverable edges because the as-built drawing requirement spans all disciplines within those packages.

## Run History

| Run Date | Mode | Strictness | Decomposition | Warnings | ACTIVE ANCHOR | ACTIVE EXECUTION | Notes |
|---|---|---|---|---|---|---|---|
| 2026-02-17 | UPDATE | CONSERVATIVE | Found (FINAL v1.0 Phase 7) | None | 6 | 8 | Initial extraction run. 14 total rows. |

## Lifecycle Summary

- **ACTIVE:** 14 (6 ANCHOR + 8 EXECUTION)
- **RETIRED:** 0

### Closure State Breakdown (ACTIVE rows)
- **SatisfactionStatus=TBD:** 14 (all rows -- initial extraction; no closure assessment performed)

## Consumer Handoff Notes (optional)
- CONSUMER_CONTEXT=NONE; no downstream handoff notes generated.
