# Deliverable Dependencies: DEL-006-01

**Deliverable ID:** DEL-006-01
**Name:** Preliminary Plumbing Design

## Dependency Tracking

**Status:** ACTIVE

## Declared Upstream Dependencies

- DEL-008-01 (Geotechnical Investigation Report) -- required for cistern/septic foundation assumptions
- DEL-008-02 (Preliminary Site Survey) -- required for site layout and drain invert elevations
- DEL-001-01 (Preliminary Architectural Design) -- room layout and fixture placement coordination
- DEL-002-01 (Preliminary Structural Design) -- cistern pad, mud sump, floor slab penetration coordination
- DEL-005-01 (Preliminary Civil Design) -- septic tank setback, external drainage, bulk fill access
- DEL-003-01 (Preliminary Mechanical Design) -- utility room layout coordination
- R-01 (RFP) and R-06 (Appendix B Plumbing) -- primary source documents

## Declared Downstream Dependencies

- DEL-006-02 through DEL-006-08 -- County-approved preliminary design is baseline for all detailed PKG-006 deliverables
- PKG-014 (Plumbing and Water Systems Installation) -- design outputs consumed for construction

## Extracted Dependency Register

| Count | Class | Status |
|-------|-------|--------|
| 3 | ANCHOR | ACTIVE |
| 13 | EXECUTION | ACTIVE |
| **16** | **Total** | **ACTIVE** |

| DependencyID | Class | AnchorType | Direction | Type | TargetType | Target | Confidence | EstImpact |
|---|---|---|---|---|---|---|---|---|
| DEP-006-01-001 | ANCHOR | IMPLEMENTS_NODE | UPSTREAM | OTHER | WBS_NODE | SOW-0010f | HIGH | -- |
| DEP-006-01-002 | ANCHOR | TRACES_TO_REQUIREMENT | UPSTREAM | OTHER | REQUIREMENT | OBJ-003 | HIGH | -- |
| DEP-006-01-003 | ANCHOR | TRACES_TO_REQUIREMENT | UPSTREAM | OTHER | REQUIREMENT | OBJ-004 | HIGH | -- |
| DEP-006-01-004 | EXECUTION | NOT_APPLICABLE | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-008-01 (Geotech Report) | HIGH | BLOCKING |
| DEP-006-01-005 | EXECUTION | NOT_APPLICABLE | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-008-02 (Site Survey) | HIGH | BLOCKING |
| DEP-006-01-006 | EXECUTION | NOT_APPLICABLE | UPSTREAM | INTERFACE | DELIVERABLE | DEL-001-01 (Arch. Prelim.) | HIGH | ADVISORY |
| DEP-006-01-007 | EXECUTION | NOT_APPLICABLE | UPSTREAM | INTERFACE | DELIVERABLE | DEL-002-01 (Struct. Prelim.) | HIGH | ADVISORY |
| DEP-006-01-008 | EXECUTION | NOT_APPLICABLE | UPSTREAM | INTERFACE | DELIVERABLE | DEL-005-01 (Civil Prelim.) | HIGH | ADVISORY |
| DEP-006-01-009 | EXECUTION | NOT_APPLICABLE | UPSTREAM | INTERFACE | DELIVERABLE | DEL-003-01 (Mech. Prelim.) | HIGH | ADVISORY |
| DEP-006-01-010 | EXECUTION | NOT_APPLICABLE | UPSTREAM | CONSTRAINT | DOCUMENT | R-01 (RFP) | HIGH | INFO |
| DEP-006-01-011 | EXECUTION | NOT_APPLICABLE | UPSTREAM | CONSTRAINT | DOCUMENT | R-06 (App B Plumbing) | HIGH | INFO |
| DEP-006-01-012 | EXECUTION | NOT_APPLICABLE | DOWNSTREAM | HANDOVER | DELIVERABLE | DEL-006-02 (Water Dist. Plans) | HIGH | BLOCKING |
| DEP-006-01-013 | EXECUTION | NOT_APPLICABLE | DOWNSTREAM | HANDOVER | DELIVERABLE | DEL-006-08 (Plumbing Spec.) | MEDIUM | ADVISORY |
| DEP-006-01-014 | EXECUTION | NOT_APPLICABLE | DOWNSTREAM | ENABLES | PACKAGE | PKG-014 (Plumbing Install.) | MEDIUM | ADVISORY |
| DEP-006-01-015 | EXECUTION | NOT_APPLICABLE | UPSTREAM | CONSTRAINT | EXTERNAL | County Approval (REQ-001) | HIGH | BLOCKING |
| DEP-006-01-016 | EXECUTION | NOT_APPLICABLE | DOWNSTREAM | INTERFACE | DELIVERABLE | DEL-018-05 (Wash Bay Drainage) | HIGH | ADVISORY |

## Run Notes

- **Run date:** 2026-02-26
- **MODE:** UPDATE
- **STRICTNESS:** CONSERVATIVE
- **CONSUMER_CONTEXT:** TASK_ESTIMATING
- **DECOMPOSITION_PATH:** /Users/ryan/ai-env/projects/chirality-project-test/test/AB-2026-01424-WDMLRL-2026-Claude/_Decomposition/WDMLRL_Decomposition_Claude.md (Available, R1 2026-02-25)
- **SOURCE_DOCS:** AUTO -- scanned Datasheet.md, Specification.md, Procedure.md, Guidance.md
- **ANCHOR_DOC:** Datasheet.md (contains explicit SOW and OBJ references in Identification table)
- **EXECUTION_DOC_ORDER:** Procedure.md (strongest prerequisite/workflow signals), Specification.md (requirements and scope boundary signals), Guidance.md (considerations and trade-offs), Datasheet.md (construction notes and interface references)
- **_REFERENCES.md:** Read; used to confirm R-01 and R-06 locations (_Sources/)
- **Defaults:** All defaults per AGENT_DEPENDENCIES protocol; no overrides applied
- **Warnings:** None
- **Anchor validation:** 1 IMPLEMENTS_NODE (SOW-0010f) confirmed in Decomposition SSOW §C and §7 PKG-006. 2 TRACES_TO_REQUIREMENT (OBJ-003, OBJ-004) confirmed in Decomposition §5 and §7 PKG-006. All target IDs resolved.
- **New rows this run:** DEP-006-01-015 (County approval constraint from Specification REQ-001), DEP-006-01-016 (downstream interface to DEL-018-05 from Datasheet construction note)
- **Retired rows this run:** None

## Run History

| Timestamp | Mode | Strictness | Decomposition | Warnings | ACTIVE Count |
|---|---|---|---|---|---|
| 2026-02-26T00:00 | UPDATE | CONSERVATIVE | Available (WDMLRL_Decomposition_Claude.md) | None | 14 |
| 2026-02-26T12:00 | UPDATE | CONSERVATIVE | Available (WDMLRL_Decomposition_Claude.md, R1 2026-02-25) | None | 16 |

## Lifecycle Summary

- **ACTIVE:** 16 (3 ANCHOR, 13 EXECUTION)
- **RETIRED:** 0
- **SatisfactionStatus breakdown:** TBD: 16

## Downstream Handoff Notes

**CONSUMER_CONTEXT: TASK_ESTIMATING**

Key estimating-relevant dependencies for DEL-006-01:

**BLOCKING upstream (3):**
- DEP-006-01-004: DEL-008-01 (Geotechnical Investigation Report) -- explicit prerequisite that gates cistern and septic foundation assumptions. Estimating cannot finalize plumbing scope quantities without geotechnical data (bearing capacity, groundwater level).
- DEP-006-01-005: DEL-008-02 (Preliminary Site Survey) -- explicit prerequisite that gates site layout and drain invert elevations. Gravity drainage feasibility (a key design assumption per Guidance trade-offs) depends on survey data.
- DEP-006-01-015: Camrose County Approval (REQ-001) -- explicit approval gate. The preliminary design must be approved before detailed design (DEL-006-02 through DEL-006-08) can commence. This gates the transition from preliminary to detailed estimating.

**ADVISORY upstream (4):**
- DEP-006-01-006 through DEP-006-01-009: Interdisciplinary coordination interfaces (Architectural, Structural, Civil, Mechanical preliminary designs). Design decisions from these deliverables may change fixture locations, routing, material quantities, and coordination requirements. Not hard gates but may affect scope and quantities.

**INFO upstream (2):**
- DEP-006-01-010, DEP-006-01-011: RFP (R-01) and Appendix B Plumbing (R-06) are source constraint documents. Already available. No estimating impact beyond the requirements they contain.

**BLOCKING downstream (1):**
- DEP-006-01-012: DEL-006-01 County-approved output is the baseline for DEL-006-02 through DEL-006-08 (all detailed plumbing design deliverables). Estimating for detailed plumbing design work cannot proceed meaningfully until this preliminary design is approved.

**ADVISORY downstream (3):**
- DEP-006-01-013: Preliminary specification outlines are a specific artifact input to DEL-006-08 (Plumbing Specification).
- DEP-006-01-014: PKG-014 (Plumbing and Water Systems Installation) consumes plumbing design outputs for construction estimating and execution.
- DEP-006-01-016: DEL-018-05 (Wash Bay Drainage and Mud Sump) consumes the design interface for REQ-009 wash bay drainage. Design decisions in the preliminary plumbing design (drain routing, mud sump connection) affect construction scope for this deliverable.

**Estimating readiness summary:** DEL-006-01 has 3 BLOCKING upstream dependencies (2 prerequisite deliverables + 1 external approval gate) and 1 BLOCKING downstream handover. Preliminary estimating of this deliverable's own effort (Plumbing Engineer hours for preliminary design) can proceed with available source documents, but scope quantities for downstream construction estimating (PKG-014, DEL-018-05) require completion of this deliverable and its upstream prerequisites.
