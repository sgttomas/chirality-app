# Dependencies: DEL-01-06 macOS packaging and distribution evidence

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

- **Status:** COMPLETE — local extraction and validation; no dependency-availability verdict.
- **Register:** `Dependencies.csv` v3.1, 29 columns; 12 ACTIVE rows: 5 ANCHOR (1 parent, 4 traces), 7 EXECUTION; 0 RETIRED; 0 DECLARED.
- **Targets:** 5 EXTERNAL, 0 UNKNOWN; external technical values and receipt remain unresolved as stated below.

| Dependency ID | Class / flow | Target | Meaning |
|---|---|---|---|
| DEP-01-06-001 | ANCHOR / UPSTREAM | PKG-01 | DEL-01-06 implements the explicitly assigned PKG-01 package. |
| DEP-01-06-002 | ANCHOR / UPSTREAM | SOW-098 | The packaging contribution traces to accepted scope SOW-098. |
| DEP-01-06-003 | ANCHOR / UPSTREAM | SOW-117 | The packaging contribution traces to accepted scope SOW-117. |
| DEP-01-06-004 | ANCHOR / UPSTREAM | SOW-134 | The packaging contribution traces to accepted scope SOW-134. |
| DEP-01-06-005 | ANCHOR / UPSTREAM | OBJ-002 | The packaging contribution supports OBJ-002 without claiming its wider architecture or access-mode behavior. |
| DEP-01-06-006 | EXECUTION / UPSTREAM | DEL-01-01 | Packaging consumes the identified stock Codex binary and App hosting basis actually supplied by App DEL-01-01. |
| DEP-01-06-007 | EXECUTION / DOWNSTREAM | PKG-09 | Supply the packaged App candidate and its local install/launch evidence to App PKG-09 for joined examination. |
| DEP-01-06-008 | EXECUTION / UPSTREAM | chirality-app-v4:OI-011 | Receive the OI-011 owners’ definition of signing, notarisation and required Codex entitlements for the selected App/Codex candidate before the packaged distribution witness. |
| DEP-01-06-009 | EXECUTION / UPSTREAM | chirality-app-v4:DEP-005 | Production uses applicable selected Codex/Tauri packaging interfaces, with actual version and environment to be defined before respective implementation/qualification witnesses. |
| DEP-01-06-010 | EXECUTION / UPSTREAM | chirality-app-v4:DEP-004 | Obtain and retain the actual written supplier position through the owner before public release beyond owner use; future Anthropic/Claude terms apply only if that sign-in need arises. |
| DEP-01-06-011 | EXECUTION / DOWNSTREAM | chirality-app-v4:DEP-004 | The owner public distribution decision consumes the written supplier position retained with source, actual custody and applicability. |
| DEP-01-06-012 | EXECUTION / UPSTREAM | SWBPIPE | Useful reusable packaging knowledge may be received from external SWBPIPE through its actual human-relayed coordination route. |

---

## Lifecycle Summary

- ACTIVE 12; RETIRED 0. Closure: NOT_APPLICABLE 5 (anchors); TBD 7 (execution); SATISFIED 0.
- INITIALIZED: source-grounded SOW_V1 exists and independent INIT verification passed; manager recorded the separate status act under the approved policy. No dependency availability or product-readiness verdict.
- DEL-01-01's INITIALIZED threshold means checked local contract maturity only. Actual identified binary/hosting inputs, selected packaging interfaces, owner arrangement, supplier response and package/handoff evidence each need their own evidence.
- OI-011 remains OPEN before the packaged distribution witness. OI-007/DEP-004 remain OPEN/UNCONFIRMED before public release beyond owner use. DEP-005 remains VERSION_AND_ENVIRONMENT_TO_DEFINE. These do not create a blanket owner-use or independent-development gate.

---

## Run Notes

- Workflow: `chirality-root:bundled:workflow:dependency-extract`; SCOPE `DEL-01-06`; RUN_ROOT `/Users/ryan/.codex/worktrees/077c/chirality/projects/chirality-app-v4/execution`.
- DECOMPOSITION_PATH `/Users/ryan/.codex/worktrees/077c/chirality/projects/chirality-app-v4/execution/_Decomposition/checkpoint_snapshots/GROUP3-20260928T001055Z/canonical/SOFTWARE_DECOMP.md`; accepted companion CSVs resolve canonical labels only. No sibling source contract read.
- SOURCE_DOCS, ANCHOR_DOC and EXECUTION_DOC_ORDER: `ScopeOfWork.md` only; DOC_ROLE_MAP DEFAULT; MODE UPDATE; STRICTNESS CONSERVATIVE; CONSUMER_CONTEXT NONE; ARCHITECTURE_BASIS_POLICY NONE.
- Pass 1 completed with one PKG-01 parent and SOW-098/SOW-117/SOW-134/OBJ-002 traces before Pass 2. Execution rows cite positive inputs or handoffs. Ownership exclusions, sibling mentions and runtime behavior alone yielded no edges.
- No prior CSV existed. Declared mirrors added/refreshed/retired: 0/0/0; two initial-setup placeholders skipped. Human-owned mode and declared sections remain byte-identical; preparation history retained.
- Optional SWBPIPE knowledge is explicitly external and nongating; actual source location and receipt remain TBD. PKG-09 is a package-level consumer; no specific examination Deliverable inferred.
- Supplier response, owner's obtaining act and owner's distribution decision retain separate actors and evidence. The downstream decision row records only the explicitly named consumer, with no invented prerequisite between acts.
- Local schema, used enum/ID values, unique rows, one parent, exact quotes (at most 30 words), source preservation and summary checks recorded in `_run_records/dependency-extract-20260927.md`. Optional whole-execution EVQ/DRB report not run. No local extraction warning; unresolved actual inputs are retained, not closed.

## Run History
- 2026-09-27 — WORKING_ITEMS applied preparation; extraction not run.
- 2026-09-28T03:16:47+00:00 — TASK dependency-extract; UPDATE / CONSERVATIVE; explicit accepted decomposition available; ACTIVE 12 (ANCHOR 5 / EXECUTION 7), RETIRED 0; no extraction warnings; actual inputs and open points of need unfulfilled/unclaimed.
