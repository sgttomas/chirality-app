# Dependencies: DEL-001-01 Preliminary Architectural Design

## Coordination (human-owned)
- **Mode:** NOT_TRACKED
- **Notes:** Coordination representation pending -- to be confirmed by human via ORCHESTRATOR.

## Upstream (I need these before I can proceed) -- human-owned declarations
- Dependencies coordinated externally by humans.

## Downstream (These need me) -- human-owned declarations
- Dependencies coordinated externally by humans.

## Extracted Dependency Register

- **Status:** POPULATED
- **Dependencies.csv:** 18 rows (3 ANCHOR + 15 EXECUTION)
- **Schema Version:** v3.1

### ANCHOR Edges (Tree)

| DependencyID | AnchorType | TargetRefID | TargetName | Confidence |
|---|---|---|---|---|
| DEP-001-01-A01 | IMPLEMENTS_NODE | SOW-0010a | Deliver preliminary architectural design for County approval | HIGH |
| DEP-001-01-A02 | TRACES_TO_REQUIREMENT | OBJ-001 | Deliver a code-compliant, fully functional maintenance shop addition | HIGH |
| DEP-001-01-A03 | TRACES_TO_REQUIREMENT | OBJ-003 | Produce complete P.Eng.-stamped IFC design documentation across all disciplines | HIGH |

### EXECUTION Edges (DAG)

| DependencyID | Direction | DependencyType | TargetType | Target | Confidence |
|---|---|---|---|---|---|
| DEP-001-01-E01 | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-008-01 Geotechnical Investigation & Report | HIGH |
| DEP-001-01-E02 | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-008-02 Preliminary Site Survey | HIGH |
| DEP-001-01-E03 | DOWNSTREAM | HANDOVER | DELIVERABLE | DEL-001-02 Architectural Floor Plans (IFC) | HIGH |
| DEP-001-01-E04 | DOWNSTREAM | INTERFACE | DELIVERABLE | DEL-002-01 Preliminary Structural Design | HIGH |
| DEP-001-01-E05 | UPSTREAM | CONSTRAINT | EXTERNAL | Camrose County Preliminary Design Approval | HIGH |
| DEP-001-01-E06 | UPSTREAM | PREREQUISITE | DOCUMENT | R-01 AB-2026-01424-WDMLRL RFP.pdf | HIGH |
| DEP-001-01-E07 | DOWNSTREAM | INTERFACE | DELIVERABLE | DEL-003-01 Preliminary Mechanical Design | HIGH |
| DEP-001-01-E08 | DOWNSTREAM | INTERFACE | DELIVERABLE | DEL-004-01 Preliminary Electrical Design | HIGH |
| DEP-001-01-E09 | DOWNSTREAM | INTERFACE | DELIVERABLE | DEL-005-01 Preliminary Civil Design | HIGH |
| DEP-001-01-E10 | DOWNSTREAM | INTERFACE | DELIVERABLE | DEL-006-01 Preliminary Plumbing Design | HIGH |
| DEP-001-01-E11 | DOWNSTREAM | INTERFACE | DELIVERABLE | DEL-007-01 Preliminary Landscape Design | MEDIUM |
| DEP-001-01-E12 | UPSTREAM | PREREQUISITE | DOCUMENT | R-04 Appendix B (Shop) Conceptual Floor Plan | HIGH |
| DEP-001-01-E13 | UPSTREAM | PREREQUISITE | DOCUMENT | R-07 Appendix C - Site Maps | MEDIUM |
| DEP-001-01-E14 | UPSTREAM | CONSTRAINT | EXTERNAL | Mandatory Site Meeting (March 3, 2026) | HIGH |
| DEP-001-01-E15 | UPSTREAM | PREREQUISITE | DOCUMENT | R-10 Addendum 4 (precast walls, folding doors, crane spacing, mezzanine railing) | HIGH |

---

## Run Notes

### Run: 2026-03-26 (R2 refresh)

**Parameters:**
- SCOPE: DEL-001-01_Preliminary-Design (as part of PKG-001 full refresh)
- RUN_ROOT: `examples/AB-2026-01424-WDMLRL-2026-Claude/`
- DECOMPOSITION_PATH: `_Decomposition/WDMLRL_Decomposition_Claude.md` (R2 -- 2026-03-26, SCA-001: Addenda 2, 3, 4)
- MODE: UPDATE
- STRICTNESS: CONSERVATIVE
- SOURCE_DOCS: AUTO
- ANCHOR_DOC: AUTO (resolved to `Datasheet.md`)
- EXECUTION_DOC_ORDER: AUTO (resolved to `Specification.md`, `Procedure.md`, `Guidance.md`)
- CONSUMER_CONTEXT: NONE

**Defaults and Resolutions:**
- ANCHOR_DOC selected as `Datasheet.md` (matches heuristic: contains "datasheet" with Identification table).
- EXECUTION_DOC_ORDER: `Specification.md`, `Procedure.md`, `Guidance.md`.
- _REFERENCES.md: read for document target resolution.
- Decomposition R2 located and validated. Key R2 changes affecting this deliverable: SOW-0011 updated (interior walls precast concrete, Add. 4 Q5); SOW-0025 updated (folding outward OH doors, Add. 4 Q4); SOW-0032 updated (mezzanine railing with forklift gate, Add. 4 Q6); new references R-08, R-09, R-10 added.

**Extraction Decisions:**
- Pass 1 (ANCHOR): 3 rows carried forward, all confirmed against R2 decomposition. No changes to anchor targets.
- Pass 2 (EXECUTION): 14 prior rows confirmed ACTIVE; all updated with LastSeen=2026-03-26.
- 1 new row added: DEP-001-01-E15 (R-10 Addendum 4 as prerequisite document). Addendum 4 materially changes building parameters (precast concrete interior walls, folding outward overhead doors, max 25-ft crane runway bay spacing, corbel-supported crane, mezzanine railing with forklift gate) that are core to the preliminary architectural design content.
- R-08 (Addendum 2) and R-09 (Addendum 3) were considered but not extracted as separate rows: their content is captured through the updated SOW items already referenced via the decomposition. CONSERVATIVE mode requires explicit information-flow statements; Addenda 2 and 3 content is subsumed by Addendum 4 and the decomposition updates.

**Not Extracted (rationale):**
- Same exclusions as prior run (R-02, R-03, R-05, R-06; discipline deliverables as upstream; coordination-only relationships).

**Warnings:**
- None. All quality checks passed.

### Run: 2026-02-26 (initial extraction)

**Parameters:**
- MODE: UPDATE | STRICTNESS: CONSERVATIVE | CONSUMER_CONTEXT: TASK_ESTIMATING
- DECOMPOSITION_PATH: R1, 2026-02-25
- 17 rows extracted (3 ANCHOR + 14 EXECUTION). No warnings.

---

## Run History

| Timestamp | Mode | Strictness | Decomposition | Warnings | ACTIVE ANCHOR | ACTIVE EXECUTION |
|---|---|---|---|---|---|---|
| 2026-02-26 | UPDATE | CONSERVATIVE | R1, 2026-02-25 -- OK | None | 3 | 14 |
| 2026-03-26 | UPDATE | CONSERVATIVE | R2, 2026-03-26 (SCA-001) -- OK | None | 3 | 15 |

---

## Lifecycle Summary

### Extraction Lifecycle

| Status | Count |
|---|---|
| ACTIVE | 18 |
| RETIRED | 0 |

### By DependencyClass

| Class | ACTIVE | RETIRED |
|---|---|---|
| ANCHOR | 3 | 0 |
| EXECUTION | 15 | 0 |

### Closure Lifecycle (SatisfactionStatus of ACTIVE rows)

| SatisfactionStatus | Count |
|---|---|
| TBD | 15 |
| SATISFIED | 2 |
| PENDING | 1 |

**Notes:**
- E06 (R-01 RFP) and E12 (R-04 Appendix B) remain SATISFIED -- documents available.
- E13 (R-07 Site Maps) remains PENDING -- available but not yet read in detail.
- E15 (R-10 Addendum 4) set to TBD -- document is available but design impact assessment pending.
- All other rows are TBD pending project mobilization and execution.
