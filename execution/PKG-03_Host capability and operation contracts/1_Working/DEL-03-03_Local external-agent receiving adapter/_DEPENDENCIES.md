# Dependencies: DEL-03-03 Local external-agent receiving adapter

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
- **Counts:** 14 ACTIVE rows: 5 ANCHOR (1 parent, 4 scope/objective traces), 9 EXECUTION (8 UPSTREAM, 1 DOWNSTREAM); 0 RETIRED; 0 DECLARED; EXECUTION target types: DELIVERABLE 6, EXTERNAL 3.

| DependencyID | Class / anchor | Direction / type | Target | Satisfaction | Status |
|---|---|---|---|---|---|
| DEP-03-03-001 | ANCHOR / IMPLEMENTS_NODE | UPSTREAM / OTHER | PKG-03 | NOT_APPLICABLE | ACTIVE |
| DEP-03-03-002 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM / OTHER | SOW-148 | NOT_APPLICABLE | ACTIVE |
| DEP-03-03-003 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM / OTHER | SOW-183 | NOT_APPLICABLE | ACTIVE |
| DEP-03-03-004 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM / OTHER | SOW-184 | NOT_APPLICABLE | ACTIVE |
| DEP-03-03-005 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM / OTHER | OBJ-004 | NOT_APPLICABLE | ACTIVE |
| DEP-03-03-006 | EXECUTION / NOT_APPLICABLE | UPSTREAM / PREREQUISITE | DEL-03-01 | PENDING | ACTIVE |
| DEP-03-03-007 | EXECUTION / NOT_APPLICABLE | UPSTREAM / PREREQUISITE | DEL-03-02 | PENDING | ACTIVE |
| DEP-03-03-008 | EXECUTION / NOT_APPLICABLE | UPSTREAM / PREREQUISITE | DEL-04-01 | PENDING | ACTIVE |
| DEP-03-03-009 | EXECUTION / NOT_APPLICABLE | UPSTREAM / PREREQUISITE | Codex native-tool capability for the selected local MCP or CLI boundary | PENDING | ACTIVE |
| DEP-03-03-010 | EXECUTION / NOT_APPLICABLE | UPSTREAM / INTERFACE | External host owner: catalog-derived local MCP/CLI endpoint contract | PENDING | ACTIVE |
| DEP-03-03-011 | EXECUTION / NOT_APPLICABLE | UPSTREAM / PREREQUISITE | SWBPIPE | PENDING | ACTIVE |
| DEP-03-03-012 | EXECUTION / NOT_APPLICABLE | DOWNSTREAM / HANDOVER | DEL-09-09 | PENDING | ACTIVE |
| DEP-03-03-013 | EXECUTION / NOT_APPLICABLE | UPSTREAM / INTERFACE | DEL-01-01 | PENDING | ACTIVE |
| DEP-03-03-014 | EXECUTION / NOT_APPLICABLE | UPSTREAM / INTERFACE | DEL-02-03 | PENDING | ACTIVE |

## Lifecycle Summary
- ACTIVE: 14; RETIRED: 0. Satisfaction (ACTIVE): NOT_APPLICABLE 5; PENDING 9.
- INITIALIZED on local Deliverable relationships is the approved contract threshold only. Identified technical inputs, policy adoption, access grants, actual host delivery, human acts and joined qualification retain separate evidence requirements. Extraction advances no lifecycle or acceptance.

## Run Notes
- Scope `DEL-03-03`; selected method `chirality-root:bundled:workflow:dependency-extract`. MODE=UPDATE; STRICTNESS=CONSERVATIVE; CONSUMER_CONTEXT=NONE; ARCHITECTURE_BASIS_POLICY=NONE; DOC_ROLE_MAP=DEFAULT.
- RUN_ROOT: `/Users/ryan/.codex/worktrees/077c/chirality/projects/chirality-app-v4/execution`.
- DECOMPOSITION_PATH: `/Users/ryan/.codex/worktrees/077c/chirality/projects/chirality-app-v4/execution/_Decomposition/checkpoint_snapshots/GROUP3-20260928T001055Z/canonical/SOFTWARE_DECOMP.md`. Accepted companion identities/labels resolved in Packages.csv, Deliverables.csv, ScopeLedger.csv and Objectives.csv; source snapshot's historical candidate wording is not a new acceptance claim.
- SOURCE_DOCS=ANCHOR_DOC=EXECUTION_DOC_ORDER=`ScopeOfWork.md` only. Pass 1 completed the explicit parent and 4 traces before Pass 2 execution extraction.
- Source SHA256 before/after: `5ac5db97eba3851eb5324054e5a2b38429a53e8e9c85428903432cd8d9efb1b6`; matches dispatch. All 12 rows cite positive source loci and verbatim evidence of at most 30 words.
- Existing register absent; 12 extracted rows added, none removed. Declaration mirrors added/refreshed/retired: 0/0/0; 2 initial placeholders skipped. Human-owned mode and declaration bytes preserved; preparation history retained.
- Required local schema/enum/ID and consistency checks passed; exactly 1 parent; no duplicate row/ID, missing evidence, noncanonical enum, quote mismatch or source/declared-section change. Optional whole-execution EVQ/DRB report not run; local equivalent checks find EVQ-003=0, EVQ-004=0, DRB-006=0.
- External endpoint contract and later actual SWBPIPE contribution evidence are separate inputs. Codex capability and actual external contribution locations remain unresolved where the source supplies none. No external target is mapped to an App Deliverable.
- OI-001/002 conditions remain with adopted PKG-04 input at their production-policy points of need. OI-003 extension decision, OI-013 host boundary, OI-014 allocation, OI-021 first activity and TBD-007 receiving interface retain their source owners/timing; no independent App definition hold, wire schema, shared service, endpoint delivery or deployment is invented.
- REQ-002 enablement and REQ-004 human-act/outcome behaviors are product requirements, not synthetic production edges. Ownership/exclusion lists and citations alone create no edges. Faithful recording never supplies a missing human act or an acceptance-before-checking prerequisite.
- Local extraction establishes neither global graph closure nor delivery, adoption, qualification, release, human acceptance or professional reliance. Run evidence: `_run_records/dependency-extract-20260927.md`.

- Target resolution R3 (2026-09-28 UTC): updated only `DEP-03-03-008` from the PKG-04 package reference to policy producer `DEL-04-01`; identity, direction/type, statement, source/quote, maturity and PENDING satisfaction remain unchanged. The preceding extraction notes remain historical. Exact repair and checks: `_run_records/dependency-target-resolution-20260928.md`.
- Repair provenance: accepted `projects/chirality-app-v4/execution/_Decomposition/checkpoint_snapshots/GROUP3-20260928T001055Z/canonical/ScopeLedger.csv` SOW-074/179/180/181/182/235 and `projects/chirality-app-v4/execution/_Decomposition/checkpoint_snapshots/GROUP3-20260928T001055Z/canonical/Deliverables.csv` DEL-04-01 identify the adopted policy meaning/representation obligation. Supplied `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-INITIAL-SETUP-20260927/TARGET_RESOLUTION.md` R3 (SHA256 `f85a371853ec5ef18d3a1b1ebdc016e37e1bbd321217f726c4350204a2cefaa1`) supplies prior independent producer OUT-001/002 proof; no sibling SoW was read in this repair. OI-001/OI-002 decisions remain with Owner with App/SWB contract owners; actual adopted policy, host enforcement and satisfaction remain unclaimed.
- Repair local checks passed: canonical schema/used enums/standard ID formats; 12 unchanged IDs and 11 byte-identical untouched rows; 1 parent; 0 duplicate rows or missing evidence/quote/locus/prefix findings; all 12 quotes remain verbatim. Human-owned sections, prior history, source, status, references and old run record remain byte-identical. Global closure/EVQ/DRB was not run while peers write. MODE=UPDATE, STRICTNESS=CONSERVATIVE and other recorded defaults/paths remain in force; this run is an identity-only subset with no maturity default applied.

- **Run 2026-09-29 (DX-3, APP-V4-BASIS-ALIGN-20260928; dependency-extract UPDATE after SCA-V4-001 SoW revision).** Method `chirality-root:bundled:workflow:dependency-extract` (WORKFLOW.md SHA256 `e5523ebabccf44337ec531280d4d91be2ce7ff1477bd39568a18bb0c4c9f18c3`). Brief: run folder `BRIEFS.md` § DX (group DX-3). Defaults and chosen paths: SCOPE=DEL-03-03; MODE=UPDATE; STRICTNESS=CONSERVATIVE; CONSUMER_CONTEXT=NONE; ARCHITECTURE_BASIS_POLICY=NONE; DOC_ROLE_MAP=DEFAULT; SOURCE_DOCS=ANCHOR_DOC=EXECUTION_DOC_ORDER=`ScopeOfWork.md` only (explicit; `Design/` DRAFT files not read, per `_COORDINATION.md` "Agent-proposed candidates derive from local SoWs and accepted interfaces"); RUN_ROOT=`projects/chirality-app-v4/execution`; DECOMPOSITION_PATH=`projects/chirality-app-v4/execution/_Decomposition/SOFTWARE_DECOMP.md` (current, post-SCA-V4-001; companion rows used for label/identity resolution only).
- Source `ScopeOfWork.md` SHA256 `fdd22e25a0a43c55d31ca38f3fcb44931af8ebee6d34da62ff1f214013fb2881` (commit `340ecf341`, SCA-V4-001 REVISE), unchanged during the run. Pass 1 (anchors) re-confirmed parent PKG-03 and traces SOW-148/183/184 and OBJ-004 unchanged before Pass 2.
- Pass 2 result: 2 rows added (`DEP-03-03-013` UPSTREAM INTERFACE DEL-01-01; `DEP-03-03-014` UPSTREAM INTERFACE DEL-02-03), both from the revised CLM-002 consumption sentence (SCA-V4-001 edit E-0303-07). 1 row refreshed in place (`DEP-03-03-008`: Statement/SourceRef/Notes for revised TBD-001/TBD-002, C1 S-03-1 / E-0303-01; SatisfactionStatus unchanged). 11 rows re-observed unchanged (LastSeen only). 0 retired. All 14 quotes re-checked verbatim against the current SoW.
- Typing: the two new rows are INTERFACE, not PREREQUISITE, because CLM-002 names consumed interface facts/definitions while the Praxeology opening paragraph lists only the DEL-03-01/02 contracts, PKG-04 policy, native-tool capability and endpoint contract as production-start inputs. ASSUMPTION: this typing reading; it does not change any arc.
- Not extracted (no SoW ground): DEL-03-04 supplier mirror (M-03-1), DEL-04-02 (N-B5), DEL-02-01 (N-B6), DEL-04-03 supplier mirror (N-14-mir), DEL-02-03 supplier mirror (N-24-mir): "not extracted: no SoW ground; consumer row represents the arc". **No UPSTREAM row to DEL-04-03 (N-B8) is written**: the SoW names no DEL-04-03 input (withheld per the P2/K1 ruling). No row to DEL-09-06 (K-11): the SoW does not name DEL-09-06. APP-V4-FIRST-INCREMENT-20260928-DECISION-2 D5 and APP-V4-SWBPIPE-INTAKE-20260928-DECISION-4/-5 are applied decisions in REQ-002/REQ-003, not open inputs; no row.
- Declaration mirrors added/refreshed/retired: 0/0/0; 2 `None declared at initial setup.` placeholders skipped. Human-owned sections byte-identical. CSV line endings normalized to CRLF (row DEP-03-03-008 previously carried an LF terminator from the R3 repair).
- Function 5 checks: `validate_dependencies_schema.py` VALID (29 columns, 14 rows); `validate_enum.py` 21 distinct enum/value invocations, 0 failures; `validate_id_format.sh` 30 invocations, 0 failures; unique IDs; DEP prefix matches FromDeliverableID; exactly 1 ACTIVE parent anchor (no FLOATING_NODE/AMBIGUOUS_ANCHOR); no blank quote (EVQ-003) or placeholder locus (EVQ-004); no Status=CANDIDATE. Run record: `_run_records/dependency-extract-20260929.md`.

## Run History
- 2026-09-27 — WORKING_ITEMS applied preparation; extraction not run.
- 2026-09-28T03:20:59+00:00 — TASK `/root/renewal_research_strategy/dep_del_03_03`; UPDATE / CONSERVATIVE; decomposition `projects/chirality-app-v4/execution/_Decomposition/checkpoint_snapshots/GROUP3-20260928T001055Z/canonical/SOFTWARE_DECOMP.md` and accepted companion identity rows available. ACTIVE=12 (ANCHOR=5; EXECUTION=7); RETIRED=0. Mandatory local checks passed; no integrity warnings. Actual external availability/receipt/adoption and unresolved interface choices remain unclaimed.
- 2026-09-28T04:25:33+00:00 — TASK `/root/renewal_research_strategy/resolve_dep_03_03`; bounded R3 UPDATE / CONSERVATIVE using accepted G3 companion rows and the supplied target-resolution report. `DEP-03-03-008` now targets `DEL-04-01`; ACTIVE=12 (ANCHOR=5; EXECUTION=7), RETIRED=0, EXTERNAL=3, UNKNOWN=0. RequiredMaturity=TBD, ProposedMaturity blank and SatisfactionStatus=PENDING preserved; mandatory local checks passed, no global check or graph change.
- 2026-09-29T14:38:50+00:00 — TASK DX-3 (APP-V4-BASIS-ALIGN-20260928); UPDATE / CONSERVATIVE; SOURCE_DOCS=ScopeOfWork.md; decomposition `projects/chirality-app-v4/execution/_Decomposition/SOFTWARE_DECOMP.md` available. Added 2 (DEL-01-01, DEL-02-03 UPSTREAM INTERFACE), refreshed 1 (DEP-03-03-008), retired 0. ACTIVE=14 (ANCHOR=5; EXECUTION=9), RETIRED=0. Mandatory local checks passed; no integrity warnings.
