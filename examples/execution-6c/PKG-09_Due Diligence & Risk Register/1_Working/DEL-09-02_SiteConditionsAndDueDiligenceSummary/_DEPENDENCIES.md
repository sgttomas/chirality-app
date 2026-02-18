# Dependencies: DEL-09-02 SiteConditionsAndDueDiligenceSummary

## Dependency Tracking Mode
- **Mode:** NOT_TRACKED (original declared mode; see execution/_Coordination/_COORDINATION.md)
- **Notes:** Schedule-first coordination; dependencies coordinated externally by humans. This file now also contains a machine-readable extracted register (see below) produced by the DEPENDENCIES agent.

---

## Upstream (I need these before I can proceed)

*(Human-declared; coordinated externally)*

- Dependencies coordinated externally by humans.

---

## Downstream (These need me)

*(Human-declared; coordinated externally)*

- Dependencies coordinated externally by humans.

---

## Extracted Dependency Register

**Total rows:** 15
**ACTIVE:** 15 | **RETIRED:** 0
**ANCHOR rows (ACTIVE):** 4 (1 IMPLEMENTS_NODE + 3 TRACES_TO_REQUIREMENT)
**EXECUTION rows (ACTIVE):** 11 (6 UPSTREAM + 5 DOWNSTREAM)

### Summary Table

| DependencyID | Class | AnchorType | Direction | Type | TargetType | TargetRefID / TargetDeliverableID | TargetName | Confidence | Status |
|---|---|---|---|---|---|---|---|---|---|
| DEP-09-02-001 | ANCHOR | IMPLEMENTS_NODE | UPSTREAM | OTHER | PACKAGE | PKG-09 | PKG-09 Due Diligence & Risk Register | HIGH | ACTIVE |
| DEP-09-02-002 | ANCHOR | TRACES_TO_REQUIREMENT | UPSTREAM | OTHER | REQUIREMENT | SOW-024 | SOW-024: Survey approach and assumptions | HIGH | ACTIVE |
| DEP-09-02-003 | ANCHOR | TRACES_TO_REQUIREMENT | UPSTREAM | OTHER | REQUIREMENT | SOW-025 | SOW-025: Site due diligence summary | HIGH | ACTIVE |
| DEP-09-02-004 | ANCHOR | TRACES_TO_REQUIREMENT | UPSTREAM | OTHER | REQUIREMENT | OBJ-008 | OBJ-008: Manage risk and unknowns transparently | HIGH | ACTIVE |
| DEP-09-02-005 | EXECUTION | NOT_APPLICABLE | UPSTREAM | PREREQUISITE | DOCUMENT | REF-GEOTECH | Geotechnical Investigation Report | HIGH | ACTIVE |
| DEP-09-02-006 | EXECUTION | NOT_APPLICABLE | UPSTREAM | PREREQUISITE | DOCUMENT | REF-WETLAND | Wetland Assessment Report | HIGH | ACTIVE |
| DEP-09-02-007 | EXECUTION | NOT_APPLICABLE | UPSTREAM | PREREQUISITE | DOCUMENT | REF-ENVIRO | Desktop Environmental Assessment | MEDIUM | ACTIVE |
| DEP-09-02-008 | EXECUTION | NOT_APPLICABLE | UPSTREAM | PREREQUISITE | DOCUMENT | REF-GRADING | Site Grading Document | HIGH | ACTIVE |
| DEP-09-02-009 | EXECUTION | NOT_APPLICABLE | UPSTREAM | PREREQUISITE | DOCUMENT | REF-FLOODZONE | Flood Zone Mapping | HIGH | ACTIVE |
| DEP-09-02-010 | EXECUTION | NOT_APPLICABLE | UPSTREAM | PREREQUISITE | DOCUMENT | REF-ADJSUBDIV | Adjacent Subdivision Design | MEDIUM | ACTIVE |
| DEP-09-02-011 | EXECUTION | NOT_APPLICABLE | DOWNSTREAM | HANDOVER | DELIVERABLE | DEL-02-01 | DEL-02-01 Concept Design Package | HIGH | ACTIVE |
| DEP-09-02-012 | EXECUTION | NOT_APPLICABLE | DOWNSTREAM | HANDOVER | DELIVERABLE | DEL-05-03 | DEL-05-03 Pricing Narrative and Assumptions | HIGH | ACTIVE |
| DEP-09-02-013 | EXECUTION | NOT_APPLICABLE | DOWNSTREAM | HANDOVER | DELIVERABLE | DEL-09-01 | DEL-09-01 Risk Register and Mitigation Plan | HIGH | ACTIVE |
| DEP-09-02-014 | EXECUTION | NOT_APPLICABLE | DOWNSTREAM | HANDOVER | DELIVERABLE | DEL-08-01 | DEL-08-01 Detailed Project Schedule | HIGH | ACTIVE |
| DEP-09-02-015 | EXECUTION | NOT_APPLICABLE | UPSTREAM | INTERFACE | DELIVERABLE | DEL-04-01 | DEL-04-01 Construction Methodology Narrative | MEDIUM | ACTIVE |

---

## Run Notes

**Run date:** 2026-02-18
**Agent:** DEPENDENCIES (Type 2), AGENT_TYPE=2
**MODE:** UPDATE
**STRICTNESS:** CONSERVATIVE
**CONSUMER_CONTEXT:** NONE

**Source documents scanned (AUTO):**
- `Datasheet.md` — selected as ANCHOR_DOC (contains identification, attributes, scope/condition information)
- `Specification.md` — EXECUTION_DOC (requirements with explicit cross-deliverable references)
- `Guidance.md` — EXECUTION_DOC (principles, considerations, cross-deliverable coordination)
- `Procedure.md` — EXECUTION_DOC (prerequisites, steps, reference materials)
- `_CONTEXT.md` — ANCHOR_DOC supplement (scope traceability, objective traceability)
- `_REFERENCES.md` — used for TargetLocation resolution on DOCUMENT rows
- `_SEMANTIC.md` — read; no additional dependency signals beyond what source docs provide

**Decomposition path used:** `/Users/ryan/ai-env/projects/chirality-app-test/test/execution-6c/_Decomposition/Penhold_PSB_Project_Decomposition_Final_AddendumIntegrated_v1.md`
Decomposition status: FOUND and READ. Used for:
- Validating PKG-09 as parent package (confirmed in Section 7)
- Validating DEL-09-02 entry (confirmed in Section 8)
- Validating SOW-024 and SOW-025 scope traceability (confirmed in Section 10)
- Validating OBJ-008 objective (confirmed in Section 6)
- Resolving canonical labels for all referenced deliverable IDs (DEL-02-01, DEL-05-03, DEL-09-01, DEL-08-01, DEL-04-01)

**DOC_ROLE_MAP:** DEFAULT applied.
- ANCHOR_DOC selected: `Datasheet.md` (contains "Identification" table with Package, Deliverable ID, Scope Traceability context)
- EXECUTION_DOC_ORDER: `Procedure.md`, `Specification.md`, `Guidance.md` (in workflow-clarity order)

**Defaults applied:**
- `SOURCE_DOCS`: AUTO
- `ANCHOR_DOC`: AUTO (resolved to `Datasheet.md` + `_CONTEXT.md` supplement)
- `EXECUTION_DOC_ORDER`: AUTO
- `MODE`: UPDATE (overwrite per invocation instructions)
- `STRICTNESS`: CONSERVATIVE — only EXPLICIT signals emitted; no IMPLICIT anchors or inferred execution edges without stated evidence
- `CONSUMER_CONTEXT`: NONE

**Prior state:** The existing `_DEPENDENCIES.md` contained only a NOT_TRACKED mode declaration with no machine-readable rows. No prior `Dependencies.csv` existed. This is the first DEPENDENCIES agent run for this deliverable.

**Pass 1 (ANCHOR) notes:**
- Parent anchor: PKG-09 resolved from Decomposition Section 7 and confirmed in Datasheet.md Identification table. One IMPLEMENTS_NODE row emitted.
- Requirement traces: SOW-024 and SOW-025 from _CONTEXT.md Scope Traceability; OBJ-008 from _CONTEXT.md Objectives. All three confirmed in Decomposition Sections 6 and 10. Three TRACES_TO_REQUIREMENT rows emitted.
- No additional scope items (SOW-026, SOW-027) traced to this deliverable — those map to DEL-09-01 per decomposition Section 10.

**Pass 2 (EXECUTION) notes:**
- UPSTREAM PREREQUISITE (6 rows): Six reference report documents are explicitly listed as required inputs in Procedure.md Prerequisites table and classified by criticality in B-006. Four are BLOCKING (Geotechnical Report, Wetland Assessment, Site Grading, Flood Zone Mapping); two are IMPORTANT (Environmental Assessment, Adjacent Subdivision Design). All are currently inaccessible (PDF read errors). TargetType=DOCUMENT used; TargetDeliverableID left empty per schema rules.
- DOWNSTREAM HANDOVER (4 rows): DEL-02-01, DEL-05-03, DEL-09-01, DEL-08-01 are explicitly named in Datasheet.md (Conditions > Normal Operating Context) and Specification.md R-12 as deliverables that consume outputs of DEL-09-02. All resolved against decomposition.
- UPSTREAM INTERFACE (1 row): DEL-04-01 is explicitly named in Specification.md R-14 as required input for construction phase constraints section.
- NOT extracted: RFP PDF and Addendum PDFs are source/authority documents but not deliverable-to-deliverable information flow dependencies. Coordination-only mentions (e.g., "coordinate with PKG-02 estimator during working sessions") were excluded per conservative information-flow-only rule.

**Quality check results:**
- DependencyID uniqueness: PASS (15 unique IDs)
- Required columns present: PASS
- ACTIVE rows with EvidenceFile + SourceRef: PASS (all 15 rows have evidence)
- Canonical enum values: PASS
- Parent anchor count (ACTIVE, IMPLEMENTS_NODE): 1 — PASS (no FLOATING_NODE, no AMBIGUOUS_ANCHOR warning required)
- TargetDeliverableID placement: PASS (empty for DOCUMENT/PACKAGE/REQUIREMENT targets; populated for DELIVERABLE targets)
- _DEPENDENCIES.md counts consistent with Dependencies.csv: PASS

---

## Lifecycle Summary

| Dimension | Count |
|---|---|
| Total rows | 15 |
| ACTIVE | 15 |
| RETIRED | 0 |
| ANCHOR / IMPLEMENTS_NODE (ACTIVE) | 1 |
| ANCHOR / TRACES_TO_REQUIREMENT (ACTIVE) | 3 |
| EXECUTION / UPSTREAM (ACTIVE) | 6 |
| EXECUTION / DOWNSTREAM (ACTIVE) | 5 |

**SatisfactionStatus breakdown (ACTIVE rows):**

| SatisfactionStatus | Count |
|---|---|
| SATISFIED | 1 |
| PENDING | 11 |
| TBD | 3 |

Notes:
- DEP-09-02-001 (parent anchor, IMPLEMENTS_NODE): SATISFIED — structural definition relationship; permanently resolved.
- DEP-09-02-002, 003, 004 (TRACES_TO_REQUIREMENT): TBD — scope traceability is defined; closure depends on deliverable completion and verification.
- DEP-09-02-005 through 010 (UPSTREAM PREREQUISITE/INTERFACE document inputs): PENDING — reference reports are required but currently inaccessible; PM action required to obtain source PDFs.
- DEP-09-02-011 through 015 (DOWNSTREAM HANDOVER + UPSTREAM INTERFACE): PENDING — dependent deliverables not yet confirmed as consuming this deliverable's outputs.

---

## Run History

| Run # | Timestamp | Mode | Strictness | Decomposition Status | Warnings | ACTIVE Count |
|---|---|---|---|---|---|---|
| 1 | 2026-02-18 | UPDATE | CONSERVATIVE | FOUND (Penhold_PSB_Project_Decomposition_Final_AddendumIntegrated_v1.md) | None | 15 |
