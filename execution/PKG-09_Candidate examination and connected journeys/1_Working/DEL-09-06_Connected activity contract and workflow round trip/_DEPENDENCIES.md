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
- **Status:** EXTRACTED; 24 ACTIVE rows (11 ANCHOR; 13 EXECUTION); 0 RETIRED; 0 DECLARED.
- **Canonical register:** `Dependencies.csv` (v3.1; 29 columns).
- **Targets:** 4 local Deliverables, 2 Package inputs, 7 EXTERNAL execution rows; 0 UNKNOWN rows. Exactly 1 parent anchor and 10 scope/objective trace anchors.

| Dependency | Class / type | Direction | Target |
|---|---|---|---|
| DEP-09-06-001 | ANCHOR / IMPLEMENTS_NODE | UPSTREAM | PKG-09 |
| DEP-09-06-002 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | SOW-040 |
| DEP-09-06-003 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | SOW-041 |
| DEP-09-06-004 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | SOW-236 |
| DEP-09-06-005 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | SOW-237 |
| DEP-09-06-006 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | SOW-238 |
| DEP-09-06-007 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | SOW-240 |
| DEP-09-06-008 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | SOW-241 |
| DEP-09-06-009 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | OBJ-001 |
| DEP-09-06-010 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | OBJ-004 |
| DEP-09-06-011 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | OBJ-008 |
| DEP-09-06-012 | EXECUTION / INTERFACE | UPSTREAM | PKG-02 |
| DEP-09-06-013 | EXECUTION / INTERFACE | UPSTREAM | DEL-02-03 |
| DEP-09-06-014 | EXECUTION / INTERFACE | UPSTREAM | PKG-03 |
| DEP-09-06-015 | EXECUTION / INTERFACE | UPSTREAM | DEL-04-03 |
| DEP-09-06-016 | EXECUTION / INTERFACE | UPSTREAM | DEL-05-01 |
| DEP-09-06-017 | EXECUTION / INTERFACE | UPSTREAM | DEL-05-02 |
| DEP-09-06-018 | EXECUTION / PREREQUISITE | UPSTREAM | DEP-001 |
| DEP-09-06-019 | EXECUTION / PREREQUISITE | UPSTREAM | DEP-001 |
| DEP-09-06-020 | EXECUTION / HANDOVER | DOWNSTREAM | DEP-001 |
| DEP-09-06-021 | EXECUTION / CONSTRAINT | UPSTREAM | OI-021 |
| DEP-09-06-022 | EXECUTION / CONSTRAINT | UPSTREAM | OI-001 |
| DEP-09-06-023 | EXECUTION / CONSTRAINT | UPSTREAM | OI-002 |
| DEP-09-06-024 | EXECUTION / PREREQUISITE | UPSTREAM | Accountable person — actual content-bound human act in V4-EXM-14 |

## Lifecycle Summary
- ACTIVE: 24; RETIRED: 0.
- SatisfactionStatus: NOT_APPLICABLE 11 (anchors); TBD 13 (execution). SATISFIED: 0.
- INITIALIZED: source-grounded SOW_V1 exists and independent INIT verification passed; manager recorded the separate status act under the approved policy. No dependency availability or product-readiness verdict.
- RequiredMaturity=INITIALIZED on 3 local Deliverable inputs means checked local contracts only. Required technical behavior, received external contributions, actual human acts and completed witness evidence remain separate unmet/unverified conditions. The resolved DEL-04-03 input retains RequiredMaturity=TBD under the identity-only repair; remaining targets use TBD.

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

## Run History
- 2026-09-27 — WORKING_ITEMS applied preparation; extraction not run.
- 2026-09-28T03:35:55+00:00 — UPDATE / CONSERVATIVE; accepted snapshot `projects/chirality-app-v4/execution/_Decomposition/checkpoint_snapshots/GROUP3-20260928T001055Z/canonical/SOFTWARE_DECOMP.md` available; warnings none; ACTIVE 24 (ANCHOR 11, EXECUTION 13), RETIRED 0; actual inputs unclaimed.
- 2026-09-28T04:24:05+00:00 — UPDATE / CONSERVATIVE, R5 only; DEP-09-06-015 target PKG-04 → DEL-04-03, accepted G3 allocation and local CLM-003 verified; ACTIVE 24 (ANCHOR 11, EXECUTION 13), RETIRED 0, local Deliverable inputs 4, Package inputs 2, EXTERNAL 7, UNKNOWN 0; warnings none; maturity, satisfaction and actual-input conditions preserved. See `_run_records/dependency-target-resolution-20260928.md`.
