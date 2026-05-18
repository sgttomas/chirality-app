# Dependencies: DEL-05-07 Cash Allowance - FF&E (20k DB-allocated)

## Coordination (human-owned)
- **Mode:** DECLARED
- **Notes:** See _Coordination/_COORDINATION.md for project-level coordination record.

## Upstream (I need these before I can proceed) -- human-owned declarations
- No upstream dependencies declared yet.

## Downstream (These need me) -- human-owned declarations
- No downstream dependencies declared yet.

## Extracted Dependency Register

- **Status:** COMPLETE
- **Dependencies.csv:** 4 rows (4 ACTIVE, 0 RETIRED)
- **Schema Version:** v3.1

### Summary

| DependencyID | Class | AnchorType | Direction | Type | TargetType | TargetName | Confidence | Status |
|---|---|---|---|---|---|---|---|---|
| DEP-0507-A001 | ANCHOR | IMPLEMENTS_NODE | UPSTREAM | OTHER | WBS_NODE | SOW-0506 | HIGH | ACTIVE |
| DEP-0507-A002 | ANCHOR | TRACES_TO_REQUIREMENT | UPSTREAM | OTHER | REQUIREMENT | OBJ-010 | HIGH | ACTIVE |
| DEP-0507-E001 | EXECUTION | NOT_APPLICABLE | UPSTREAM | PREREQUISITE | DOCUMENT | Addendum 03 s1.18 | HIGH | ACTIVE |
| DEP-0507-E002 | EXECUTION | NOT_APPLICABLE | UPSTREAM | INTERFACE | DELIVERABLE | DEL-05-06 (Appliances & Laundry) | HIGH | ACTIVE |

### Counts by Class
- **ANCHOR:** 2 (1 IMPLEMENTS_NODE, 1 TRACES_TO_REQUIREMENT)
- **EXECUTION:** 2 (1 PREREQUISITE, 1 INTERFACE)

## Run Notes

### Run: 2026-02-17 (initial extraction)

**Parameters:**
- MODE: UPDATE
- STRICTNESS: CONSERVATIVE
- CONSUMER_CONTEXT: NONE
- SOURCE_DOCS: AUTO (resolved: Datasheet.md, Specification.md, Guidance.md, Procedure.md)
- ANCHOR_DOC: AUTO (resolved: Datasheet.md)
- EXECUTION_DOC_ORDER: AUTO (resolved: Procedure.md, Guidance.md, Specification.md)
- DECOMPOSITION_PATH: _Decomposition/Penhold_PSB_Project_Decomposition_FINAL_v1.0_PHASE7.md (found and used)
- _REFERENCES.md: present and used for document pointer resolution

**Defaults applied:**
- ANCHOR_DOC selected as Datasheet.md (contains "datasheet" in filename; explicit Identification table with Scope Item, Supported Objective, Governing Source fields).
- EXECUTION_DOC_ORDER: Procedure.md first (contains "procedure" in filename; has explicit Prerequisites section), then Guidance.md (contains considerations and conflict table), then Specification.md (contains requirements and standards).

**Decomposition validation:**
- SOW-0506 confirmed in SSOW table (Phase 2) and Phase 6 traceability matrix. Maps to DEL-05-07_Optional-FFandE-Allowance, PKG-005, OBJ-010.
- OBJ-010 confirmed in Phase 3 objectives table: "Provide transparent, separable pricing for optional scope items."
- DEC-005 confirmed in Decision Log: "FF&E: treat as $20,000 cash allowance; DB allocates within allowance."
- PKG-005 confirmed in Phase 4 packages table.

**Pass 1 (Anchor) notes:**
- Parent anchor (IMPLEMENTS_NODE) emitted for SOW-0506. Single parent; no ambiguity.
- Trace anchor (TRACES_TO_REQUIREMENT) emitted for OBJ-010. Explicit in Datasheet and confirmed in Decomposition.
- DEC-005 was considered as a potential anchor target but is a decision reference, not a definition node or requirement. It is recorded in the Datasheet as Decision Reference and informs the deliverable content, but does not constitute a separate anchor edge under the ANCHOR model. No anchor emitted for DEC-005.

**Pass 2 (Execution) notes:**
- Addendum 03 s1.18 (PREREQUISITE, DOCUMENT): Governing source explicitly identified in Datasheet. Confirmed in PDF source. Directs FF&E as additional item separate from base costs. This is a required input that gates how the deliverable is structured.
- DEL-05-06 (INTERFACE, DELIVERABLE): Explicit in Procedure Prerequisites ("Coordination with DEL-05-06 to prevent scope overlap in the FF&E boundary definition"). Reinforced by Guidance CON-002 (scope overlap conflict), Specification REQ-05 verification (appliance overlap), and Guidance Example Boundary Distinction table. This is a genuine information-flow interface: boundary definition for DEL-05-07 requires knowing what DEL-05-06 covers to prevent double-counting.
- DEC-005 ($20k value source): Considered as a potential EXECUTION prerequisite but DEC-005 is a decomposition decision record, not an external deliverable or document requiring receipt. The information from DEC-005 is already embedded in the deliverable source documents. No separate execution edge emitted.
- DEL-02-01 (architectural program / space understanding): Considered but not emitted. Procedure Prerequisites mention "Understanding of the spaces in the Penhold PSB program" but this is contextual knowledge, not an explicit artifact transfer or required input receipt. Under CONSERVATIVE strictness, this does not meet the information-flow threshold.
- DEL-01-01 (proposal submission): Considered as a potential DOWNSTREAM handover (FF&E package feeds into proposal). Not emitted because no source document explicitly states DEL-01-01 requires receipt of the DEL-05-07 output as a named input. Under CONSERVATIVE strictness, structural adjacency in proposal assembly is not sufficient.

**Warnings:** None.

## Run History

| Timestamp | Mode | Strictness | DecompositionStatus | Warnings | ACTIVE Count |
|---|---|---|---|---|---|
| 2026-02-17 | UPDATE | CONSERVATIVE | Found and used | None | 4 |

## Lifecycle Summary

- **ACTIVE:** 4 (2 ANCHOR, 2 EXECUTION)
- **RETIRED:** 0
- **SatisfactionStatus breakdown:** TBD: 4, PENDING: 0, IN_PROGRESS: 0, SATISFIED: 0, WAIVED: 0, NOT_APPLICABLE: 0

## Consumer Handoff Notes (optional)
- CONSUMER_CONTEXT: NONE -- no consumer-specific handoff notes generated.
