# Dependencies: DEL-09-06 Connected activity contract and workflow round trip

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
- **Status:** EXTRACTED_AND_LOCALLY_VALIDATED
- **Register:** `Dependencies.csv` (v3.1; 29 columns).
- **Counts:** 34 ACTIVE rows: 11 ANCHOR (1 parent, 10 scope/objective traces), 23 EXECUTION (21 UPSTREAM, 2 DOWNSTREAM); 0 RETIRED; 0 DECLARED; EXECUTION target types: DELIVERABLE 12, EXTERNAL 9, PACKAGE 2.

| DependencyID | Class / anchor | Direction / type | Target | Satisfaction | Status |
|---|---|---|---|---|---|
| DEP-09-06-001 | ANCHOR / IMPLEMENTS_NODE | UPSTREAM / OTHER | PKG-09 | NOT_APPLICABLE | ACTIVE |
| DEP-09-06-002 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM / OTHER | SOW-040 | NOT_APPLICABLE | ACTIVE |
| DEP-09-06-003 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM / OTHER | SOW-041 | NOT_APPLICABLE | ACTIVE |
| DEP-09-06-004 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM / OTHER | SOW-236 | NOT_APPLICABLE | ACTIVE |
| DEP-09-06-005 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM / OTHER | SOW-237 | NOT_APPLICABLE | ACTIVE |
| DEP-09-06-006 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM / OTHER | SOW-238 | NOT_APPLICABLE | ACTIVE |
| DEP-09-06-007 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM / OTHER | SOW-240 | NOT_APPLICABLE | ACTIVE |
| DEP-09-06-008 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM / OTHER | SOW-241 | NOT_APPLICABLE | ACTIVE |
| DEP-09-06-009 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM / OTHER | OBJ-001 | NOT_APPLICABLE | ACTIVE |
| DEP-09-06-010 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM / OTHER | OBJ-004 | NOT_APPLICABLE | ACTIVE |
| DEP-09-06-011 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM / OTHER | OBJ-008 | NOT_APPLICABLE | ACTIVE |
| DEP-09-06-012 | EXECUTION / NOT_APPLICABLE | UPSTREAM / INTERFACE | PKG-02 | TBD | ACTIVE |
| DEP-09-06-013 | EXECUTION / NOT_APPLICABLE | UPSTREAM / INTERFACE | DEL-02-03 | TBD | ACTIVE |
| DEP-09-06-014 | EXECUTION / NOT_APPLICABLE | UPSTREAM / INTERFACE | PKG-03 | TBD | ACTIVE |
| DEP-09-06-015 | EXECUTION / NOT_APPLICABLE | UPSTREAM / INTERFACE | DEL-04-03 | TBD | ACTIVE |
| DEP-09-06-016 | EXECUTION / NOT_APPLICABLE | UPSTREAM / INTERFACE | DEL-05-01 | TBD | ACTIVE |
| DEP-09-06-017 | EXECUTION / NOT_APPLICABLE | UPSTREAM / INTERFACE | DEL-05-02 | TBD | ACTIVE |
| DEP-09-06-018 | EXECUTION / NOT_APPLICABLE | UPSTREAM / PREREQUISITE | DEP-001 | TBD | ACTIVE |
| DEP-09-06-019 | EXECUTION / NOT_APPLICABLE | UPSTREAM / PREREQUISITE | DEP-001 | TBD | ACTIVE |
| DEP-09-06-020 | EXECUTION / NOT_APPLICABLE | DOWNSTREAM / HANDOVER | DEP-001 | TBD | ACTIVE |
| DEP-09-06-021 | EXECUTION / NOT_APPLICABLE | UPSTREAM / CONSTRAINT | OI-021 | TBD | ACTIVE |
| DEP-09-06-022 | EXECUTION / NOT_APPLICABLE | UPSTREAM / CONSTRAINT | OI-001 | TBD | ACTIVE |
| DEP-09-06-023 | EXECUTION / NOT_APPLICABLE | UPSTREAM / CONSTRAINT | OI-002 | TBD | ACTIVE |
| DEP-09-06-024 | EXECUTION / NOT_APPLICABLE | UPSTREAM / PREREQUISITE | Accountable person — actual content-bound human act in V4-EXM-14 | TBD | ACTIVE |
| DEP-09-06-025 | EXECUTION / NOT_APPLICABLE | UPSTREAM / INTERFACE | DEL-02-01 | TBD | ACTIVE |
| DEP-09-06-026 | EXECUTION / NOT_APPLICABLE | UPSTREAM / INTERFACE | DEL-02-02 | TBD | ACTIVE |
| DEP-09-06-027 | EXECUTION / NOT_APPLICABLE | UPSTREAM / INTERFACE | DEL-03-01 | TBD | ACTIVE |
| DEP-09-06-028 | EXECUTION / NOT_APPLICABLE | UPSTREAM / INTERFACE | DEL-03-02 | TBD | ACTIVE |
| DEP-09-06-029 | EXECUTION / NOT_APPLICABLE | UPSTREAM / INTERFACE | DEL-03-03 | TBD | ACTIVE |
| DEP-09-06-030 | EXECUTION / NOT_APPLICABLE | UPSTREAM / INTERFACE | DEL-04-01 | TBD | ACTIVE |
| DEP-09-06-031 | EXECUTION / NOT_APPLICABLE | UPSTREAM / INTERFACE | DEL-04-02 | TBD | ACTIVE |
| DEP-09-06-032 | EXECUTION / NOT_APPLICABLE | UPSTREAM / INTERFACE | DEL-01-01 | TBD | ACTIVE |
| DEP-09-06-033 | EXECUTION / NOT_APPLICABLE | DOWNSTREAM / HANDOVER | DEP-001 | TBD | ACTIVE |
| DEP-09-06-034 | EXECUTION / NOT_APPLICABLE | UPSTREAM / CONSTRAINT | APP-V4-SWBPIPE-INTAKE-20260928-DECISION-3 | TBD | ACTIVE |

## Lifecycle Summary
- ACTIVE: 34; RETIRED: 0. Satisfaction (ACTIVE): NOT_APPLICABLE 11; TBD 23.
- Execution SatisfactionStatus=TBD is the register convention. INITIALIZED on Deliverable targets is local contract maturity only; actual contributions at the joined witness remain required and unclaimed. Recorded SWBPIPE answers are not commitments.

## Run Notes
- Method: `chirality-root:bundled:workflow:dependency-extract`; SCOPE=DEL-09-06; MODE=UPDATE; STRICTNESS=CONSERVATIVE; CONSUMER_CONTEXT=NONE; ARCHITECTURE_BASIS_POLICY=NONE; DOC_ROLE_MAP=DEFAULT.
- RUN_ROOT: `/Users/ryan/.codex/worktrees/077c/chirality/projects/chirality-app-v4/execution`.
- DECOMPOSITION_PATH: `/Users/ryan/.codex/worktrees/077c/chirality/projects/chirality-app-v4/execution/_Decomposition/checkpoint_snapshots/GROUP3-20260928T001055Z/canonical/SOFTWARE_DECOMP.md`. The accepted snapshot supplies identity/label lookup only; historical candidate wording is preserved in those bytes. The assignment supplies its accepted basis.
- SOURCE_DOCS=ANCHOR_DOC=EXECUTION_DOC_ORDER=`ScopeOfWork.md`. Pass 1 resolved 1 parent, 7 scope and 3 objective anchors before Pass 2 extracted 13 execution rows. Source SHA256 matched dispatch before and after: `511f2c0016920cbf67476f1b8d911ed85d6cfa419e7a6b15f3c7e20457779b37`.
- Declared mirroring: added 0; refreshed 0; retired 0; skipped 2 initial-setup placeholders. Human-owned mode/upstream/downstream bytes and existing history are preserved.
- Positive CLM-003 supply statements support the local inputs. PKG-02 workflow-making/receiving and DEL-02-03 specific execution compatibility are distinct contributions; PKG-05 supply resolves to its two expressly named receiving contracts. No completion gate for an entire package is inferred.
- External SWB construction/interface receipt, host candidate/execution evidence and outgoing workflow handoff are separate relations, all qualified at actual points of need. Source-referenced external account locations identify records, not provider deployment or receipt. DEL-09-06 retains the complete first connected activity and joined witness responsibility.
- OI-021 and applicable OI-001/002 answers remain open at their own dependent points of need; exact act/person/environment and provider custody remain unresolved. Actual act evidence is required only by the prescribed witness/checkpoint; no generic approval or favorable-decision completion rule is added.
- No edges are inferred from CLM-006 / REQ-008 owner exclusions to DEL-09-02/07/09/05 or DEL-11-03. PEC and Domains are not initial prerequisites; later Domains/external-channel/extension contributions and OI-003 stay at their separate points of need. Independent App work continues.
- `_REFERENCES.md` and sibling SoWs were not read. No source, status, decomposition, project graph, instruction or Git changes; no acceptance, release, adoption, qualification or external delivery claim.
- Mandatory schema, used-enum and supported-ID validators passed. Local checks passed for evidence substring/word limit, canonical fields, unique IDs, target placement, parent count, duplicate absence, counts and preserved bytes. Optional whole-root EVQ/DRB check omitted; no project-wide result claimed. External-reference namespaces DEP-001 and OI-001/002/021 are source references, outside the dependency-row ID validator grammar.
- Warnings: none under the workflow's integrity-warning classes. Open source conditions above remain unresolved; local extraction does not establish dependency closure.

- 2026-09-28 target-resolution UPDATE (R5 only): `DEP-09-06-015` resolves the App/shared record contribution from PKG-04 to DEL-04-03 on accepted `projects/chirality-app-v4/execution/_Decomposition/checkpoint_snapshots/GROUP3-20260928T001055Z/canonical/Deliverables.csv` DEL-04-03 and `ScopeLedger.csv` SOW-094/095/096/143/186. The independently produced `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-INITIAL-SETUP-20260927/TARGET_RESOLUTION.md` (SHA256 `f85a371853ec5ef18d3a1b1ebdc016e37e1bbd321217f726c4350204a2cefaa1`) carries the prior producer OUT-001/002 and CLM-004/005 proof; no sibling SoW was read by this repair.
- R5 preserves the row's ID, source statement/locator/quote, UPSTREAM/INTERFACE classification, ACTIVE status, RequiredMaturity=TBD, blank ProposedMaturity and SatisfactionStatus=TBD. Host-specific recording/receipts remain external SWBPIPE contributions; the person performs the human act, and actual record instances/act evidence remain required at handoff/witness. No new allocation, satisfied input or completed witness is claimed.
- Repair read extent and checks are recorded in `_run_records/dependency-target-resolution-20260928.md`. All other register rows, declared sections, existing history, source/control files and the old run record remain unchanged. Mandatory local schema/enum/ID and preservation checks passed; no whole-root validation or graph refresh was run during peer writes.

- **Run 2026-09-29 (DX-3, APP-V4-BASIS-ALIGN-20260928; dependency-extract UPDATE after SCA-V4-001 SoW revision).** Method `chirality-root:bundled:workflow:dependency-extract` (WORKFLOW.md SHA256 `e5523ebabccf44337ec531280d4d91be2ce7ff1477bd39568a18bb0c4c9f18c3`). Brief: run folder `BRIEFS.md` § DX (group DX-3). Defaults and chosen paths: SCOPE=DEL-09-06; MODE=UPDATE; STRICTNESS=CONSERVATIVE; CONSUMER_CONTEXT=NONE; ARCHITECTURE_BASIS_POLICY=NONE; DOC_ROLE_MAP=DEFAULT; SOURCE_DOCS=ANCHOR_DOC=EXECUTION_DOC_ORDER=`ScopeOfWork.md` only (explicit; `Design/` DRAFT files, including the relay files, not read); RUN_ROOT=`projects/chirality-app-v4/execution`; DECOMPOSITION_PATH=`projects/chirality-app-v4/execution/_Decomposition/SOFTWARE_DECOMP.md` (current, post-SCA-V4-001).
- Source `ScopeOfWork.md` SHA256 `287d47a1260e7433c3f16578c67345d067472165421c65848bd15e44d92a7923` (commit `340ecf341`), unchanged during the run. Pass 1 re-confirmed parent PKG-09 and traces SOW-040/041/236/237/238/240/241 and OBJ-001/004/008 (not amended by SCA-V4-001).
- **Guard clarification (integrator ruling, 2026-09-29).** As first dispatched, the guard read "DEL-09-06 must not gain rows that consume any SCC-002 member". Read literally, it stopped this deliverable: the revised CLM-003 forces 6 such rows. The integrator ruled the wording wrong. The intended guard, per node P2, is: **no row that makes an SCC-002 member depend on DEL-09-06, and no DOWNSTREAM row from DEL-09-06 to an SCC-002 member**. DEL-09-06 consuming SCC-002 members is allowed. The six rows (N-19, N-C1…N-C4, N-08) are in the refreshed 41-arc set the owner accepted under DECISION-6. This register satisfies the intended guard: it has no DOWNSTREAM deliverable row, and no row names DEL-03-04, DEL-09-07 or DEL-09-09. The candidate validated before the stop was applied unchanged.
- Pass 2 result: 8 deliverable rows added from revised CLM-003 (C1 S9-6-3, edit E-0906-03), each UPSTREAM INTERFACE: `DEP-09-06-025` DEL-02-01, `-026` DEL-02-02, `-027` DEL-03-01, `-028` DEL-03-02, `-029` DEL-03-03, `-030` DEL-04-01, `-031` DEL-04-02, `-032` DEL-01-01. 2 external rows added: `DEP-09-06-033` DOWNSTREAM HANDOVER to DEP-001 (relay question set and recorded answers, OUT-004; C1 S9-6-4) and `DEP-09-06-034` UPSTREAM CONSTRAINT on APP-V4-SWBPIPE-INTAKE-20260928-DECISION-3 (TBD-003(c), host joins deferred). Refreshed in place: `-016` and `-017` (re-quoted; the old quote was no longer verbatim), `-022` and `-023` (revised TBD-002: DECISION-1 D2/D3 rulings; C1 S9-6-1), `-024` (checkpoint phasing, DECISION-4 D4-1). Package rows `-012` and `-014` kept (notes only). 12 rows re-observed unchanged. 0 retired.
- Not extracted: supplier mirrors R9-6-4 (DEL-09-01) and R9-6-5 (DEL-09-07): "not extracted: no SoW ground; consumer row represents the arc". CLM-006 names DEL-09-02/05/07/09 and DEL-11-03 only as owners of separate qualification (no rows; K-6/K-7).
- Declaration mirrors added/refreshed/retired: 0/0/0; 2 placeholders skipped. Human-owned sections byte-identical.
- Function 5 checks: `validate_dependencies_schema.py` VALID (29 columns, 34 rows); `validate_enum.py` 23 invocations, 0 failures; `validate_id_format.sh` 63 invocations, 0 failures; unique IDs; prefix matches; exactly 1 ACTIVE parent anchor; no blank quote or placeholder locus; no Status=CANDIDATE. SCC membership over all 41 working-tree registers equals DAG-001's; DEL-09-06 is in no SCC. Run record: `_run_records/dependency-extract-20260929.md`.

## Run History
- 2026-09-27 — WORKING_ITEMS applied preparation; extraction not run.
- 2026-09-28T03:35:55+00:00 — UPDATE / CONSERVATIVE; accepted snapshot `projects/chirality-app-v4/execution/_Decomposition/checkpoint_snapshots/GROUP3-20260928T001055Z/canonical/SOFTWARE_DECOMP.md` available; warnings none; ACTIVE 24 (ANCHOR 11, EXECUTION 13), RETIRED 0; actual inputs unclaimed.
- 2026-09-28T04:24:05+00:00 — UPDATE / CONSERVATIVE, R5 only; DEP-09-06-015 target PKG-04 → DEL-04-03, accepted G3 allocation and local CLM-003 verified; ACTIVE 24 (ANCHOR 11, EXECUTION 13), RETIRED 0, local Deliverable inputs 4, Package inputs 2, EXTERNAL 7, UNKNOWN 0; warnings none; maturity, satisfaction and actual-input conditions preserved. See `_run_records/dependency-target-resolution-20260928.md`.
- 2026-09-29T14:38:50+00:00 — TASK DX-3 (APP-V4-BASIS-ALIGN-20260928); UPDATE / CONSERVATIVE; SOURCE_DOCS=ScopeOfWork.md; decomposition `projects/chirality-app-v4/execution/_Decomposition/SOFTWARE_DECOMP.md` available. First stopped on the literal guard, then applied after the integrator clarified it. Added 10 (8 UPSTREAM INTERFACE deliverable rows; DEP-001 HANDOVER; DECISION-3 CONSTRAINT), refreshed 5 (016, 017, 022, 023, 024), retired 0. ACTIVE=34 (ANCHOR=11; EXECUTION=23), RETIRED=0. Mandatory local checks passed; no integrity warnings.
