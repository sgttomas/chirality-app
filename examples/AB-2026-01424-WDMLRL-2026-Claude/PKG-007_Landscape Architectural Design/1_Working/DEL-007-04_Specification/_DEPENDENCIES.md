# DEL-007-04 Landscape Specification -- Dependencies

## Tracking Status
- **Dependency Tracking**: ACTIVE
- **Register Schema Version**: v3.1
- **Last Extraction Run**: 2026-02-26

## Upstream Dependencies
- **DEL-007-01**: Preliminary Landscape Design (County approval required before specification issuance)
- **DEL-007-02**: Landscape Site Plans (must be approved; provides material callouts, layout dimensions)
- **DEL-007-03**: Planting & Restoration Plans (must be approved; provides species list, installation standards)
- **DEL-005-02**: Site Grading Plan from PKG-005 Civil Design (drainage integration)
- **DEL-005-03**: Drainage Plan from PKG-005 Civil Design (drainage integration)
- **DEL-008-01**: Geotechnical Investigation & Report from PKG-008 (subsoil data for pad design, planting, grading)
- **DEL-006-03**: Drain & Vent Plans from PKG-006 Plumbing Design (wash bay mud sump interface)
- **DEL-002-12**: Structural Specification from PKG-002 (cement pad structural requirements)
- **R-01**: RFP governing requirements
- **R-04**: Appendix B conceptual drawings (pad locations, site layout)

## Downstream Dependencies
- **DEL-018-02**: Site Grading & Landscaping (PKG-018) -- construction execution consumes this specification
- **DEL-018-03**: Gravel Driving Surface (PKG-018) -- construction execution consumes driving surface standards
- **DEL-018-04**: Cement & Gravel Pads (PKG-018) -- construction execution consumes pad standards
- **DEL-018-05**: Wash Bay Drainage & Mud Sump (PKG-018) -- construction execution consumes mud sump specification

## Internal Dependencies
- Landscape architect specification development process
- Coordination with design documentation

## External Dependencies
- Landscape Architect discipline assignment
- Material supplier and specification database access
- Construction industry standards and best practices
- Quality assurance and inspection protocols
- Stakeholder review and approval availability

## Blocking Issues
- None currently identified (all upstream dependencies are in PENDING satisfaction status)

## Notes
Dependency tracking activated 2026-02-26. Current status reflects scaffold/preliminary design stage; specification drafted with TBD placeholders pending upstream deliverable approvals.

---

## Extracted Dependency Register

**Total rows:** 18 | **ACTIVE:** 17 | **RETIRED:** 1

### ANCHOR Rows (3 ACTIVE, 1 RETIRED)

| DependencyID | AnchorType | TargetRefID | TargetName | Confidence | Status |
|---|---|---|---|---|---|
| DEP-007-04-001 | IMPLEMENTS_NODE | SOW-0017 | Complete landscape architectural design | HIGH | ACTIVE |
| DEP-007-04-002 | IMPLEMENTS_NODE | SOW-0076 | Site grading and landscaping | MEDIUM | RETIRED |
| DEP-007-04-003 | TRACES_TO_REQUIREMENT | OBJ-001 | Deliver code-compliant functional shop addition | HIGH | ACTIVE |
| DEP-007-04-004 | TRACES_TO_REQUIREMENT | OBJ-003 | Produce complete P.Eng.-stamped IFC design docs | HIGH | ACTIVE |

### EXECUTION Rows -- UPSTREAM (10)

| DependencyID | DependencyType | TargetDeliverableID | TargetName | Confidence | SatisfactionStatus | EstimateImpactClass |
|---|---|---|---|---|---|---|
| DEP-007-04-010 | PREREQUISITE | DEL-007-01 | Preliminary Landscape Design | HIGH | PENDING | BLOCKING |
| DEP-007-04-011 | PREREQUISITE | DEL-007-02 | Landscape Site Plans | HIGH | PENDING | BLOCKING |
| DEP-007-04-012 | PREREQUISITE | DEL-007-03 | Planting & Restoration Plans | HIGH | PENDING | BLOCKING |
| DEP-007-04-013 | INTERFACE | DEL-005-02 | Site Grading Plan | HIGH | PENDING | BLOCKING |
| DEP-007-04-014 | INTERFACE | DEL-005-03 | Drainage Plan | HIGH | PENDING | BLOCKING |
| DEP-007-04-015 | PREREQUISITE | DEL-008-01 | Geotechnical Investigation & Report | HIGH | PENDING | BLOCKING |
| DEP-007-04-016 | INTERFACE | DEL-006-03 | Drain & Vent Plans | MEDIUM | PENDING | ADVISORY |
| DEP-007-04-017 | CONSTRAINT | R-01 | RFP | HIGH | SATISFIED | INFO |
| DEP-007-04-018 | CONSTRAINT | R-04 | Appendix B (Shop) | HIGH | SATISFIED | INFO |
| DEP-007-04-024 | INTERFACE | DEL-002-12 | Structural Specification | MEDIUM | PENDING | ADVISORY |

### EXECUTION Rows -- DOWNSTREAM (4)

| DependencyID | DependencyType | TargetDeliverableID | TargetName | Confidence | SatisfactionStatus | EstimateImpactClass |
|---|---|---|---|---|---|---|
| DEP-007-04-020 | ENABLES | DEL-018-02 | Site Grading & Landscaping | HIGH | TBD | BLOCKING |
| DEP-007-04-021 | ENABLES | DEL-018-03 | Gravel Driving Surface | MEDIUM | TBD | ADVISORY |
| DEP-007-04-022 | ENABLES | DEL-018-04 | Cement & Gravel Pads | MEDIUM | TBD | ADVISORY |
| DEP-007-04-023 | ENABLES | DEL-018-05 | Wash Bay Drainage & Mud Sump | MEDIUM | TBD | ADVISORY |

---

## Lifecycle Summary

| Category | Count |
|---|---|
| ACTIVE | 17 |
| RETIRED | 1 |
| **Satisfaction Status** | |
| PENDING | 8 |
| SATISFIED | 2 |
| TBD | 4 |
| NOT_APPLICABLE | 3 (ANCHOR rows, ACTIVE only) |

---

## Run Notes

### Defaults Applied
- **SOURCE_DOCS**: AUTO -- scanned deliverable folder; identified Datasheet.md (ANCHOR_DOC), Procedure.md, Guidance.md, Specification.md (EXECUTION_DOCS)
- **DOC_ROLE_MAP**: DEFAULT -- Datasheet.md matched ANCHOR_DOC pattern; Procedure.md, Guidance.md, Specification.md matched EXECUTION_DOC patterns
- **ANCHOR_DOC**: Datasheet.md (matched "datasheet" pattern)
- **EXECUTION_DOC_ORDER**: Procedure.md (highest workflow clarity), Specification.md, Guidance.md
- **MODE**: UPDATE
- **STRICTNESS**: CONSERVATIVE
- **CONSUMER_CONTEXT**: TASK_ESTIMATING

### Decomposition Status
- **Path**: /Users/ryan/ai-env/projects/chirality-project-test/test/AB-2026-01424-WDMLRL-2026-Claude/_Decomposition/WDMLRL_Decomposition_Claude.md
- **Status**: AVAILABLE -- used for anchor validation, target resolution, and label resolution
- **Revision**: R1 -- 2026-02-25

### Integrity Warnings
- [RESOLVED] AMBIGUOUS_ANCHOR: Previously two IMPLEMENTS_NODE anchors (SOW-0017 and SOW-0076). SOW-0076 (DEP-007-04-002) RETIRED by human ruling 2026-02-26 — SOW-0076 belongs to PKG-018/DEL-018-02 per decomposition Scope Ledger. Warning cleared: exactly 1 ACTIVE IMPLEMENTS_NODE remains (SOW-0017).

### Assumptions
- DEP-007-04-002: RETIRED. SOW-0076 anchor was listed in Datasheet SOW Reference but decomposition maps it to PKG-018. Human confirmed it reflects a specification-to-construction relationship, not a direct implementation anchor for DEL-007-04.
- DEP-007-04-016: Target resolved to DEL-006-03 (Drain & Vent Plans) as the most likely PKG-006 deliverable providing mud sump drainage interface data. Procedure P9 references PKG-006 broadly.
- DEP-007-04-021/022/023: Downstream ENABLES relationships to PKG-018 construction deliverables are IMPLICIT (inferred from Specification scope statement and decomposition package mapping, not from an explicit "output consumed by" statement).
- DEP-007-04-024: Target resolved to DEL-002-12 (Structural Specification) for cement pad structural requirements. Procedure Step 6.1 references PKG-002 Structural Engineer broadly.

### Extraction Notes
- `_REFERENCES.md` was consulted for document target resolution (R-01 -> _Sources/; R-07 -> _Sources/).
- Existing `_DEPENDENCIES.md` declared dependencies were used as corroborating evidence but do not generate rows on their own.
- No Dependencies.csv existed prior to this run; all rows are new extractions.

---

## Run History

| Timestamp | Mode | Strictness | Consumer | Decomp Status | Warnings | ACTIVE Count |
|---|---|---|---|---|---|---|
| 2026-02-26 | UPDATE | CONSERVATIVE | TASK_ESTIMATING | AVAILABLE (R1 2026-02-25) | AMBIGUOUS_ANCHOR (2 IMPLEMENTS_NODE rows) | 18 |
| 2026-02-26 | MANUAL | — | — | — | AMBIGUOUS_ANCHOR resolved: DEP-007-04-002 RETIRED by human ruling (SOW-0076 → PKG-018) | 17 |

---

## Downstream Handoff Notes

**Consumer Context: TASK_ESTIMATING**

The following observations are relevant for task-level estimating:

1. **Six BLOCKING upstream dependencies** gate specification finalization: DEL-007-01 (County approval), DEL-007-02 (site plans), DEL-007-03 (planting plans), DEL-005-02 (grading), DEL-005-03 (drainage), DEL-008-01 (geotech). Estimating for DEL-007-04 should assume these remain incomplete and factor in rework/revision risk.

2. **One BLOCKING downstream dependency**: DEL-018-02 (Site Grading & Landscaping construction) cannot proceed without this specification. PKG-018 estimating should account for this gate.

3. **Two unresolved scope conflicts** affect estimating precision:
   - CONF-007-04-01: Cement pad specification authority (PKG-005 vs PKG-007) -- affects which package bears pad structural specification effort.
   - CONF-007-04-02: Drainage feature scope boundary (PKG-005 vs PKG-007) -- affects which package bears swale/erosion control specification effort.

4. **Key TBDs affecting scope magnitude**: Gravel driving surface design vehicle parameters (motor scraper class undefined); planting species/schedule (entirely TBD pending DEL-007-03); cement pad dimensions/mix design (TBD pending DEL-007-02 and structural coordination); mud sump sizing (TBD pending PKG-006 coordination).

5. **Document dependencies SATISFIED**: R-01 (RFP) and R-04 (Appendix B) are available and have been reviewed. No document-access blockers.
