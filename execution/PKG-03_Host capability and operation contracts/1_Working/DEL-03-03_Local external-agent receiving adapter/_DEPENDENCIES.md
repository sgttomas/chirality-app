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
- **Counts:** 12 ACTIVE rows: 5 ANCHOR (1 parent, 4 scope/objective traces), 7 EXECUTION (6 UPSTREAM, 1 DOWNSTREAM); 0 RETIRED; 0 DECLARED; 3 EXTERNAL targets; 0 UNKNOWN targets.

| DependencyID | Class / anchor | Direction / type | Target | Satisfaction |
|---|---|---|---|---|
| DEP-03-03-001 | ANCHOR / IMPLEMENTS_NODE | UPSTREAM / OTHER | PKG-03 | NOT_APPLICABLE |
| DEP-03-03-002 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM / OTHER | SOW-148 | NOT_APPLICABLE |
| DEP-03-03-003 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM / OTHER | SOW-183 | NOT_APPLICABLE |
| DEP-03-03-004 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM / OTHER | SOW-184 | NOT_APPLICABLE |
| DEP-03-03-005 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM / OTHER | OBJ-004 | NOT_APPLICABLE |
| DEP-03-03-006 | EXECUTION / NOT_APPLICABLE | UPSTREAM / PREREQUISITE | DEL-03-01 | PENDING |
| DEP-03-03-007 | EXECUTION / NOT_APPLICABLE | UPSTREAM / PREREQUISITE | DEL-03-02 | PENDING |
| DEP-03-03-008 | EXECUTION / NOT_APPLICABLE | UPSTREAM / PREREQUISITE | DEL-04-01 | PENDING |
| DEP-03-03-009 | EXECUTION / NOT_APPLICABLE | UPSTREAM / PREREQUISITE | Codex native-tool capability for the selected local MCP or CLI boundary | PENDING |
| DEP-03-03-010 | EXECUTION / NOT_APPLICABLE | UPSTREAM / INTERFACE | External host owner: catalog-derived local MCP/CLI endpoint contract | PENDING |
| DEP-03-03-011 | EXECUTION / NOT_APPLICABLE | UPSTREAM / PREREQUISITE | SWBPIPE | PENDING |
| DEP-03-03-012 | EXECUTION / NOT_APPLICABLE | DOWNSTREAM / HANDOVER | DEL-09-09 | PENDING |

## Lifecycle Summary
- ACTIVE: 12; RETIRED: 0. Satisfaction: NOT_APPLICABLE 5; PENDING 7; SATISFIED 0.
- INITIALIZED: source-grounded SOW_V1 exists and independent INIT verification passed; manager recorded the separate status act under the approved policy. No dependency availability or product-readiness verdict.
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

## Run History
- 2026-09-27 — WORKING_ITEMS applied preparation; extraction not run.
- 2026-09-28T03:20:59+00:00 — TASK `/root/renewal_research_strategy/dep_del_03_03`; UPDATE / CONSERVATIVE; decomposition `projects/chirality-app-v4/execution/_Decomposition/checkpoint_snapshots/GROUP3-20260928T001055Z/canonical/SOFTWARE_DECOMP.md` and accepted companion identity rows available. ACTIVE=12 (ANCHOR=5; EXECUTION=7); RETIRED=0. Mandatory local checks passed; no integrity warnings. Actual external availability/receipt/adoption and unresolved interface choices remain unclaimed.
- 2026-09-28T04:25:33+00:00 — TASK `/root/renewal_research_strategy/resolve_dep_03_03`; bounded R3 UPDATE / CONSERVATIVE using accepted G3 companion rows and the supplied target-resolution report. `DEP-03-03-008` now targets `DEL-04-01`; ACTIVE=12 (ANCHOR=5; EXECUTION=7), RETIRED=0, EXTERNAL=3, UNKNOWN=0. RequiredMaturity=TBD, ProposedMaturity blank and SatisfactionStatus=PENDING preserved; mandatory local checks passed, no global check or graph change.
