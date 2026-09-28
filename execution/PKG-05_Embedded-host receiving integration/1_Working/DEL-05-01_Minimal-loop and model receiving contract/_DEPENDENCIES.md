# Dependencies: DEL-05-01 Minimal-loop and model receiving contract

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
- **Register:** `Dependencies.csv` (v3.1; 29 columns).
- **Status:** locally extracted and checked; no global closure or accepted DAG claim.
- **Rows:** 24 ACTIVE; 0 RETIRED; 24 EXTRACTED; 0 DECLARED.
- **Classes:** 13 ANCHOR (1 parent, 11 scope traces, 1 objective trace); 11 EXECUTION.
- **Execution targets:** 7 local Deliverables; 3 EXTERNAL (1 SWBPIPE host-evidence contribution, 2 owner decision conditions); 1 UNKNOWN model-interface basis.

| Dependency IDs | Class / direction | Target / actual input |
| --- | --- | --- |
| DEP-05-01-001 | ANCHOR / UPSTREAM | PKG-05 parent |
| DEP-05-01-002–012 | ANCHOR / UPSTREAM | Eleven explicit scope references |
| DEP-05-01-013 | ANCHOR / UPSTREAM | OBJ-004 objective |
| DEP-05-01-014 | EXECUTION / UPSTREAM / INTERFACE | DEL-03-01 adopted catalog/read-basis schemas |
| DEP-05-01-015 | EXECUTION / UPSTREAM / INTERFACE | DEL-03-02 proposal/validation/outcome meaning |
| DEP-05-01-016 | EXECUTION / UPSTREAM / INTERFACE | DEL-02-01 portable workflow/role/checkpoint declarations |
| DEP-05-01-017 | EXECUTION / UPSTREAM / INTERFACE | DEL-02-03 workflow execution/checkpoint receiving meaning |
| DEP-05-01-018 | EXECUTION / UPSTREAM / INTERFACE | DEL-04-01 adopted policy and human-act distinctions |
| DEP-05-01-019 | EXECUTION / UPSTREAM / INTERFACE | DEL-04-03 human-act/run-record meanings |
| DEP-05-01-020 | EXECUTION / UPSTREAM / INTERFACE | DEL-05-02 panel receiving needs |
| DEP-05-01-021 | EXECUTION / UPSTREAM / PREREQUISITE | External SWBPIPE evidence at actual host-conformance claims |
| DEP-05-01-022 | EXECUTION / UPSTREAM / CONSTRAINT | OI-013 owner choices before affected implementation boundary contracts |
| DEP-05-01-023 | EXECUTION / UPSTREAM / CONSTRAINT | OI-014 owner allocation before affected structural/production allocation |
| DEP-05-01-024 | EXECUTION / UPSTREAM / PREREQUISITE | UNKNOWN actual model-interface/protocol/fixture basis at use |

---

## Lifecycle Summary
- INITIALIZED: source-grounded SOW_V1 exists and independent INIT verification passed; manager recorded the separate status act under the approved policy. No dependency availability or product-readiness verdict.
- Extraction: ACTIVE 24; RETIRED 0. Closure: NOT_APPLICABLE 13 anchors; PENDING 11 execution inputs; SATISFIED 0.
- RequiredMaturity: INITIALIZED for 7 local Deliverable contract interfaces; TBD for 4 non-Deliverable execution inputs and 13 anchors. No ProposedMaturity supplied.
- INITIALIZED is only the approved local contract threshold. Adopted technical artifacts, agreed owner choices, actual external evidence and model-interface details remain distinct unfulfilled/unconfirmed inputs at their actual points of need.

---

## Run Notes
- Workflow: `chirality-root:bundled:workflow:dependency-extract`; source basis `ffb2b6289dde79a35f22f5d87256df0aa4d3289a`; unchanged method on setup candidate `ddd721a90ade401d452d102e6e40d1ffdae654eb` / identical-tree integration `82efe62783bbe8ac7d21476a6662195c0b0a7587` per dispatch brief. Actual method hashes are recorded in `_run_records/dependency-extract-20260927.md`.
- SCOPE `DEL-05-01`; RUN_ROOT `/Users/ryan/.codex/worktrees/077c/chirality/projects/chirality-app-v4/execution`; DECOMPOSITION_PATH `/Users/ryan/.codex/worktrees/077c/chirality/projects/chirality-app-v4/execution/_Decomposition/checkpoint_snapshots/GROUP3-20260928T001055Z/canonical/SOFTWARE_DECOMP.md`. Explicit accepted companion rows resolve IDs/labels; current local target paths come from dispatch metadata. Historical candidate labels in preserved snapshot bytes do not reverse the accepted basis identified by the brief and source.
- SOURCE_DOCS `[ScopeOfWork.md]`; DOC_ROLE_MAP `DEFAULT`; ANCHOR_DOC `ScopeOfWork.md`; EXECUTION_DOC_ORDER `[ScopeOfWork.md]`; MODE `UPDATE`; STRICTNESS `CONSERVATIVE`; CONSUMER_CONTEXT `NONE`; ARCHITECTURE_BASIS_POLICY `NONE`.
- Pass 1 completed with one parent and twelve trace anchors before Pass 2. Existing CSV absent: 24 rows added; none refreshed or retired. No row deleted. Declared mirror counts: added 0, refreshed 0, retired 0; two initial-setup placeholder entries skipped. Human-owned mode/upstream/downstream bytes and prior Run History preserved.
- Source SHA256 before/after: `6fbbb580bdacb7f34b4df98a826519a28c087aff6e589ad27330ee556a83b568`; matches dispatch. All rows cite positive `ScopeOfWork.md` evidence at a specific locus with verbatim quotes of at most 30 words. CLM-002 explicitly states consumption; the seven local interfaces are not inferred from its ownership list alone.
- Open inputs: exact host candidate and adopted interfaces, model supplier/version/wire/fixture basis, actual native/validation/failure/responsiveness observations, OI-013 host choices and OI-014 shared allocation. External owners retain host construction and human decisions. No invented common service or ownership transfer.
- Runtime/product outcomes are not independently emitted as project inputs: no local-server/API-key availability edge, no future human-acceptance/check/approval/reliance prerequisite, no Pi dependency. References/exclusions/adjacency create no edges. Unnamed joined-examination ownership does not resolve a downstream Deliverable; no guessed downstream edge emitted.
- Local checks: schema, every used core enum and stable-ID format, one parent, unique IDs/semantic rows, field completeness, quote/locus binding, source stability, exact human-section/history preservation and summary counts. Validation details and output hashes are in the local run record. Optional whole-execution EVQ/DRB scan not run; local evidence/binding checks cover this register without reading sibling source contracts.
- No source, references, status, decomposition or sibling writes; no Git mutation, delegation, external messaging, lifecycle advancement, project graph assembly, adoption or global closure.

## Run History
- 2026-09-27 — WORKING_ITEMS applied preparation; extraction not run.
- 2026-09-28T03:11:20.190351+00:00 — TASK native child `/root/renewal_research_strategy/dep_del_05_01`; dependency-extract UPDATE / CONSERVATIVE; explicit accepted decomposition available; 24 ACTIVE (13 ANCHOR / 11 EXECUTION), 0 RETIRED; one parent; source/declared sections preserved; unresolved model-interface basis and owner/external conditions retained.
