# Dependencies: DEL-10-04 Project production dependency DAG

## Dependency Tracking Mode
- **Mode:** FULL_GRAPH
- **Register:** the declared sections of this file together with Dependencies.csv (schema v3.1) when present (docs/SPEC.md §5.3)
- **Notes:** `projects/chirality-app-v4/execution/_Coordination/_COORDINATION.md`; no individual human-declared edge yet. Accepted interface descriptions are sources for later extraction, not declarations inferred by scaffolding.

---

## Declared Upstream (I need these before I can proceed)
- None declared at initial setup.

## Declared Downstream (These need me)
- None declared at initial setup.

---

## Extracted Dependency Register
- **Register:** `Dependencies.csv` (v3.1, 29 canonical columns).
- **Rows:** 14 ACTIVE; 4 ANCHOR (1 parent, 3 traces), 10 EXECUTION (9 upstream, 1 downstream); 0 RETIRED; 14 EXTRACTED, 0 DECLARED.
- **Targets:** 4 DELIVERABLE, 5 DOCUMENT, 1 EXTERNAL, 1 WBS_NODE, 3 REQUIREMENT; 0 UNKNOWN.

| ID | Class / direction / type | Target | Satisfaction |
|---|---|---|---|
| DEP-10-04-001 | ANCHOR / UPSTREAM / OTHER | PKG-10 | NOT_APPLICABLE |
| DEP-10-04-002 | ANCHOR / UPSTREAM / OTHER | SOW-211 | NOT_APPLICABLE |
| DEP-10-04-003 | ANCHOR / UPSTREAM / OTHER | OBJ-006 | NOT_APPLICABLE |
| DEP-10-04-004 | ANCHOR / UPSTREAM / OTHER | OBJ-010 | NOT_APPLICABLE |
| DEP-10-04-005 | EXECUTION / UPSTREAM / PREREQUISITE | DEL-10-01 | TBD |
| DEP-10-04-006 | EXECUTION / UPSTREAM / PREREQUISITE | DEL-10-02 | TBD |
| DEP-10-04-007 | EXECUTION / UPSTREAM / PREREQUISITE | DEL-10-03 | TBD |
| DEP-10-04-008 | EXECUTION / UPSTREAM / PREREQUISITE | Accepted App v4 allocation and node inventory | TBD |
| DEP-10-04-009 | EXECUTION / UPSTREAM / PREREQUISITE | Applicable local ScopeOfWork contracts, dependency evidence and human declarations | TBD |
| DEP-10-04-010 | EXECUTION / UPSTREAM / INTERFACE | Current external contribution and open-matter records | TBD |
| DEP-10-04-011 | EXECUTION / UPSTREAM / CONSTRAINT | Selected project-dag method | TBD |
| DEP-10-04-012 | EXECUTION / UPSTREAM / PREREQUISITE | Independent graph examination record | TBD |
| DEP-10-04-013 | EXECUTION / UPSTREAM / CONSTRAINT | Human owner — actual graph basis and version decisions | TBD |
| DEP-10-04-014 | EXECUTION / DOWNSTREAM / HANDOVER | DEL-10-02 | TBD |

## Lifecycle Summary
- INITIALIZED: source-grounded SOW_V1 exists and independent INIT verification passed; manager recorded the separate status act under the approved policy. No dependency availability or product-readiness verdict.
- Register lifecycle: 14 ACTIVE, 0 RETIRED. Closure: 4 NOT_APPLICABLE anchors, 10 TBD execution relationships; 0 SATISFIED. No lifecycle status changed by this run.

## Run Notes
- Run: 2026-09-27; selected method `chirality-root:bundled:workflow:dependency-extract`; method basis `ffb2b6289dde79a35f22f5d87256df0aa4d3289a`; supplied setup candidate `ddd721a90ade401d452d102e6e40d1ffdae654eb` (identical-tree main integration `82efe62783bbe8ac7d21476a6662195c0b0a7587`).
- Parameters: SCOPE `DEL-10-04`; RUN_ROOT `/Users/ryan/.codex/worktrees/077c/chirality/projects/chirality-app-v4/execution`; DECOMPOSITION_PATH `/Users/ryan/.codex/worktrees/077c/chirality/projects/chirality-app-v4/execution/_Decomposition/checkpoint_snapshots/GROUP3-20260928T001055Z/canonical/SOFTWARE_DECOMP.md`; SOURCE_DOCS / ANCHOR_DOC / EXECUTION_DOC_ORDER `ScopeOfWork.md`; DOC_ROLE_MAP `DEFAULT`; MODE `UPDATE`; STRICTNESS `CONSERVATIVE`; CONSUMER_CONTEXT `NONE`; ARCHITECTURE_BASIS_POLICY `NONE`.
- Two passes: four explicit anchors were resolved first (one PKG-10 parent, SOW-211 and two objective traces); execution extraction followed. Canonical labels use accepted companion CSVs; historical candidate labels remain historical under the supplied brief. No sibling ScopeOfWork was read.
- Source SHA256 before/after: `fb62502a0f59b226607ed6a04cbbd9ffbafab35edcfe45a1a7307cfcc80d2177`; unchanged. Human-owned mode/upstream/downstream sections preserved byte-for-byte. Existing history preserved. No prior register existed; no row retired or removed.
- Declared mirroring: 0 added, 0 refreshed, 0 retired; 2 initial-setup placeholder entries skipped. No declared edges inferred.
- CLM-002 positively consumes the three sibling contributions. REQ-008 provides a distinct later handoff to DEL-10-02. These relationships retain their actual conditions; extraction makes no project topology, scheduling or cycle-resolution decision.
- The graph consumes local source evidence and the external/open-matter account, not a guessed input from each named provider or inventory member. No standalone supplier-delivery edge is inferred from DEP-001..006. Preserve pending SWB, optional/unqualified PEC including D108's retained limitation, later Domains with unresolved allocation, and receiving-owner choices at their source-stated points of need.
- INITIALIZED describes a checked local Deliverable contract only; actual applicable records, accepted graph, live satisfaction evidence, independent examination and human decisions require separate evidence. All 10 execution satisfaction states remain TBD. Human decisions and independent examination are distinct contributions; no synthetic ordering between human acts, self-bootstrap graph prerequisite, 30% passage, release, qualification or adoption claim.
- Unresolved: future graph objective/selection and basis/version subjects; applicable record availability/currency; actual independent examiner/record; actual human decision custody. B3 tracking mode is already chosen. `_REFERENCES.md` points to a later scoped OI-017 disposition; it is not an edge source or a claim that all DEL-10-01 outputs are fulfilled. No broad hold is inferred.
- Validation: canonical schema, all used enum values, all stable ID values and local integrity checks PASS (details in `_run_records/dependency-extract-20260927.md`). Optional whole-execution EVQ/DRB was not run; all local quotes are verbatim, at most 30 words, with precise non-placeholder loci and matching ID prefixes. No structural warnings.

## Run History
- 2026-09-27 — WORKING_ITEMS applied preparation; extraction not run.
- 2026-09-27 — TASK dependency-extract; UPDATE / CONSERVATIVE; explicit accepted GROUP3 decomposition path above used; 14 ACTIVE (4 ANCHOR / 10 EXECUTION), 0 RETIRED; no structural warnings; local checks PASS.
