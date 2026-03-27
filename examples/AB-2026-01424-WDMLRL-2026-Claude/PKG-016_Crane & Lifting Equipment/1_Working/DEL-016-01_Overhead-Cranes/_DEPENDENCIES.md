# DEL-016-01_Overhead-Cranes | Dependencies

## Dependency Tracking Status
**Tracking Status**: TRACKED
**Register Schema Version**: v3.1
**Last Extraction Run**: 2026-03-26

---

## Upstream Dependencies
Dependencies that must be satisfied before this deliverable can proceed:

| Dependency ID | Description | Status | Notes |
|---------------|-------------|--------|-------|
| STRUCT-001 | Structural frame design for crane beams | Pending | Building structure must support crane loads |
| ELEC-001 | Electrical service sizing for crane motors | Pending | Power supply specifications required |
| SITE-001 | Shop floor construction readiness | Pending | Building envelope must be closed |

## Downstream Dependencies
Deliverables that depend on completion of this deliverable:

| Dependent ID | Description | Status | Notes |
|--------------|-------------|--------|-------|
| OPS-001 | Operator training and certification | Pending | Cannot begin until equipment installed |
| MAINT-001 | Maintenance scheduling system | Pending | Requires equipment specs for maintenance planning |

## Critical Path Assessment
- **On Critical Path**: YES
- **Justification**: Equipment procurement lead times are typically 8-12 weeks; installation prerequisites for facility operations

---

## Extracted Dependency Register

**Total ACTIVE rows**: 17
**Total RETIRED rows**: 0

### ANCHOR Edges (4 ACTIVE)

| DependencyID | AnchorType | TargetRefID | TargetName | Confidence |
|---|---|---|---|---|
| DEP-016-01-A01 | IMPLEMENTS_NODE | SOW-0067 | Supply and install two 5-tonne overhead cranes on trolley | HIGH |
| DEP-016-01-A02 | TRACES_TO_REQUIREMENT | OBJ-001 | Deliver a code-compliant fully functional maintenance shop addition | HIGH |
| DEP-016-01-A03 | TRACES_TO_REQUIREMENT | OBJ-004 | Install and commission all mechanical systems to operational readiness | HIGH |
| DEP-016-01-A04 | TRACES_TO_REQUIREMENT | OBJ-005 | Install and commission all electrical systems to operational readiness | HIGH |

### EXECUTION Edges (13 ACTIVE)

| DependencyID | Direction | DependencyType | TargetType | TargetName | EstimateImpactClass | Confidence |
|---|---|---|---|---|---|---|
| DEP-016-01-E01 | UPSTREAM | PREREQUISITE | DELIVERABLE | Crane Support Structure Details (DEL-002-07) | BLOCKING | HIGH |
| DEP-016-01-E02 | UPSTREAM | PREREQUISITE | DELIVERABLE | Equipment Power Circuits (DEL-015-04) | BLOCKING | HIGH |
| DEP-016-01-E03 | UPSTREAM | PREREQUISITE | PACKAGE | Building Structure and Envelope (PKG-011) | BLOCKING | HIGH |
| DEP-016-01-E04 | UPSTREAM | INTERFACE | DELIVERABLE | Crane Support Structure Details (DEL-002-07) | BLOCKING | HIGH |
| DEP-016-01-E05 | UPSTREAM | INTERFACE | PACKAGE | Electrical Design (PKG-004) | ADVISORY | MEDIUM |
| DEP-016-01-E06 | DOWNSTREAM | INTERFACE | DELIVERABLE | Crane Support Structure Details (DEL-002-07) | ADVISORY | HIGH |
| DEP-016-01-E07 | DOWNSTREAM | INTERFACE | PACKAGE | Electrical Design (PKG-004) | ADVISORY | HIGH |
| DEP-016-01-E08 | DOWNSTREAM | HANDOVER | UNKNOWN | Operator training and certification (OPS-001) | INFO | HIGH |
| DEP-016-01-E09 | DOWNSTREAM | HANDOVER | UNKNOWN | Maintenance scheduling system (MAINT-001) | INFO | MEDIUM |
| DEP-016-01-E10 | DOWNSTREAM | HANDOVER | DELIVERABLE | Closeout Documentation (DEL-020-03) | INFO | HIGH |
| DEP-016-01-E11 | UPSTREAM | CONSTRAINT | EXTERNAL | Alberta Safety Codes -- Lifting Equipment | BLOCKING | HIGH |
| DEP-016-01-E12 | UPSTREAM | CONSTRAINT | DOCUMENT | RFP Section 3.4 -- Design Requirements (R-01) | BLOCKING | HIGH |
| DEP-016-01-E13 | UPSTREAM | CONSTRAINT | DOCUMENT | Appendix B -- Shop Floor Plan (R-04) | ADVISORY | HIGH |

---

## Lifecycle Summary

| Status | Count |
|--------|-------|
| ACTIVE | 17 |
| RETIRED | 0 |

| SatisfactionStatus | Count |
|--------------------|-------|
| NOT_APPLICABLE | 4 |
| PENDING | 13 |

| DependencyClass | Count |
|-----------------|-------|
| ANCHOR | 4 |
| EXECUTION | 13 |

---

## Downstream Handoff Notes

**Consumer Context**: TASK_ESTIMATING

The following notes are provided for downstream estimating workflows:

### Blocking Dependencies (6 rows)
These dependencies gate meaningful estimating because scope or key quantities are unknown without them:

1. **DEP-016-01-E01** (STRUCT-001): Structural runway must be installed before crane installation. Estimating crane installation labor and schedule requires knowing when the structural runway will be complete.
2. **DEP-016-01-E02** (ELEC-001): Electrical power circuit must be available for crane testing. Estimating commissioning timeline requires electrical readiness.
3. **DEP-016-01-E03** (SITE-001): Building envelope closure is a hard prerequisite. Crane installation cannot be estimated for schedule without knowing building envelope completion date.
4. **DEP-016-01-E04**: Crane span dimension from structural design (DEL-002-07) is required before the procurement RFQ can be issued. Without this, crane equipment pricing cannot be obtained.
5. **DEP-016-01-E11**: Alberta Safety Code compliance is a non-negotiable constraint. Estimating must account for inspection scheduling lead time (ASSUMPTION: 4-6 weeks per Procedure Step D3).
6. **DEP-016-01-E12**: RFP S3.4 is the governing requirements document. All specification-level requirements for estimating originate here.

### Advisory Dependencies (4 rows)
These dependencies are likely to change quantities, specs, or procurement approach but are not hard gates:

1. **DEP-016-01-E05**: Voltage/amperage from electrical design affects crane model selection but three-phase power type is already confirmed.
2. **DEP-016-01-E06**: Crane load data output to structural design -- affects structural package estimating, not this deliverable's estimate directly.
3. **DEP-016-01-E07**: Crane electrical data output to electrical design -- affects electrical package estimating, not this deliverable's estimate directly.
4. **DEP-016-01-E13**: Appendix B constrains geometric parameters. Layout is known; specific dimensions require confirmation.

### Informational Dependencies (3 rows)
These provide context but are unlikely to change totals:

1. **DEP-016-01-E08**: Downstream handover to OPS-001 (operator training).
2. **DEP-016-01-E09**: Downstream handover to MAINT-001 (maintenance scheduling).
3. **DEP-016-01-E10**: Downstream handover to DEL-020-03 (closeout documentation).

### Key Estimating Risks
- **Procurement lead time**: 8-12 weeks for crane equipment is a critical-path risk. Estimating must include this in schedule modeling.
- **Bidirectional interface with DEL-002-07**: This deliverable both receives crane span data FROM and provides crane load data TO the structural design. This creates a coordination loop that may require iterative estimating.
- **TBD parameters affecting cost**: Crane duty class, single vs. double girder configuration, shared vs. independent runways are all unresolved decisions that significantly affect both equipment cost and structural cost.

---

## Run Notes

### Run 2026-02-26

**Parameters:**
- MODE: UPDATE
- STRICTNESS: CONSERVATIVE
- CONSUMER_CONTEXT: TASK_ESTIMATING
- SOURCE_DOCS: AUTO (resolved to: Datasheet.md, Guidance.md, Procedure.md, Specification.md)
- ANCHOR_DOC: Datasheet.md (selected: contains identification section with SOW Reference, Supports Objectives)
- EXECUTION_DOC_ORDER: Procedure.md, Specification.md, Guidance.md, Datasheet.md
- DECOMPOSITION_PATH: _Decomposition/WDMLRL_Decomposition_Claude.md (found and used)
- _REFERENCES.md: Present and used for document pointer resolution (R-01, R-04)

**Defaults applied:**
- DOC_ROLE_MAP: DEFAULT heuristic. Datasheet.md matched ANCHOR_DOC (contains "datasheet"). Procedure.md, Specification.md, Guidance.md matched EXECUTION_DOC candidates.
- All four source documents were scanned; _CONTEXT.md, _REFERENCES.md, _STATUS.md, _SEMANTIC.md, _SEMANTIC_LENSING.md excluded as non-source artifacts.

**Decomposition validation:**
- SOW-0067 confirmed in decomposition scope ledger (line 662): IN, PKG-016, DEL-016-01, OBJ-001/OBJ-004/OBJ-005.
- OBJ-001, OBJ-004, OBJ-005 confirmed in decomposition objective-package mapping.
- DEL-002-07 confirmed in decomposition deliverable table (PKG-002).
- DEL-015-04 confirmed in decomposition deliverable table (PKG-015).
- DEL-020-03 confirmed in decomposition deliverable table (PKG-020).
- PKG-011 confirmed in decomposition package table.
- PKG-004 confirmed in decomposition package table.
- OPS-001 and MAINT-001 are NOT found in the decomposition; recorded as TargetType=UNKNOWN.

**Warnings:**
- None. Parent anchor (IMPLEMENTS_NODE) found: 1 row (DEP-016-01-A01). No FLOATING_NODE or AMBIGUOUS_ANCHOR condition.

**Extraction decisions:**
- The existing _DEPENDENCIES.md declared STRUCT-001, ELEC-001, SITE-001, OPS-001, and MAINT-001 as dependency IDs. These are informal labels from the prior (pre-extraction) version. The extracted register uses canonical DependencyIDs (DEP-016-01-Exx) and records the informal labels in Notes and EvidenceQuote fields.
- DEL-002-07 appears in two distinct roles: (1) as the source of the structural runway prerequisite (DEP-016-01-E01, PREREQUISITE), and (2) as the source of crane span data required before procurement (DEP-016-01-E04, INTERFACE). These are semantically distinct dependencies (installation-phase vs. procurement-phase) and are kept as separate rows.
- DEL-002-07 also appears as a DOWNSTREAM interface target (DEP-016-01-E06) because this deliverable provides crane load data to the structural engineer. This bidirectional relationship is correct and intentional.
- PKG-004 appears as both UPSTREAM interface (DEP-016-01-E05, voltage/amperage needed for crane selection) and DOWNSTREAM interface (DEP-016-01-E07, crane electrical data provided for circuit sizing). This bidirectional relationship is correct.
- Cross-package references to PKG-017 and PKG-018 mentioned in the prior _DEPENDENCIES.md Interdependency Matrix were evaluated. The source documents do not state explicit information/asset transfer to/from PKG-017 or PKG-018. Per CONSERVATIVE strictness, these are excluded as coordination-only / structural adjacency.

### Run 2026-03-26 (SCA-001 Refresh)

**Parameters:**
- MODE: UPDATE
- STRICTNESS: CONSERVATIVE
- CONSUMER_CONTEXT: NONE
- SOURCE_DOCS: AUTO (resolved to: Datasheet.md, Guidance.md, Procedure.md, Specification.md)
- ANCHOR_DOC: Datasheet.md
- EXECUTION_DOC_ORDER: Procedure.md, Specification.md, Guidance.md, Datasheet.md
- DECOMPOSITION_PATH: _Decomposition/WDMLRL_Decomposition_Claude.md R2 (2026-03-26, SCA-001)
- _REFERENCES.md: Present and used

**SCA-001 impact assessment:**
- SOW-0067 updated in decomposition with crane parameters from Addenda 3 and 4: hook height 26' (Add. 3, Q3), max 25' runway bay spacing (Add. 4, Q2), corbel-supported on side walls (Add. 4, Q3).
- _CONTEXT.md updated to reflect these parameters.
- These parameter changes refine existing interfaces but do not create new dependency edges. The structural interface with DEL-002-07 (DEP-016-01-E01, E04, E06) now explicitly includes corbel design; this was already captured as the crane support structure interface.
- No new dependencies identified. All 17 existing rows confirmed ACTIVE.

**Decomposition validation:**
- SOW-0067 confirmed in R2 decomposition scope ledger with updated parameters.
- All target IDs re-validated against R2 decomposition: no changes to target resolution.

**Warnings:**
- None. Parent anchor (IMPLEMENTS_NODE) found: 1 row. No FLOATING_NODE or AMBIGUOUS_ANCHOR.

---

## Run History

| Timestamp | Mode | Strictness | Decomposition | Warnings | ACTIVE Anchor | ACTIVE Execution | ACTIVE Total |
|-----------|------|------------|---------------|----------|---------------|------------------|--------------|
| 2026-02-26 | UPDATE | CONSERVATIVE | _Decomposition/WDMLRL_Decomposition_Claude.md (used) | None | 4 | 13 | 17 |
| 2026-03-26 | UPDATE | CONSERVATIVE | _Decomposition/WDMLRL_Decomposition_Claude.md R2 (used) | None | 4 | 13 | 17 |

---

## Dependency Management Notes
- Dependencies tracked at register level with full schema v3.1 compliance.
- All structural and electrical coordination dependencies captured with bidirectional interface edges.
- Building readiness prerequisites (structural runway, electrical circuit, building envelope) identified as BLOCKING for estimating.
- OPS-001 and MAINT-001 downstream targets cannot be resolved to decomposition deliverable IDs; recorded as UNKNOWN pending project-level reconciliation.

## Interdependency Matrix
No interdependencies tracked within PKG-016 (single deliverable package).

Cross-Package Dependencies (extracted):
- PKG-002 (Structural Design): DEL-002-07 -- bidirectional interface (crane span IN; crane load data OUT) + installation prerequisite
- PKG-004 (Electrical Design): bidirectional interface (voltage/amperage IN; crane electrical data OUT)
- PKG-011 (Building Structure & Envelope): building envelope closure prerequisite
- PKG-015 (Electrical Installation): DEL-015-04 -- electrical power circuit prerequisite
- PKG-020 (Commissioning & Closeout): DEL-020-03 -- documentation handover
