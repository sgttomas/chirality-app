# App v4 INITIAL setup proposal

**One coordination choice is pending; the final decomposition and downstream project definition are already authorized.** Basis: [accepted Group3](../_Decomposition/checkpoint_snapshots/_LATEST_ACCEPTED.md),11 Packages/41 Deliverables/262 scope IDs. Inspection at Git `ffb2b6289dde79a35f22f5d87256df0aa4d3289a` found no package/deliverable scaffolds, local SoWs, `_COORDINATION.md` or active scope-change state. `INITIAL` is therefore the selected setup mode.

## Recommended grouped choice

| Item | Proposed policy |
|---|---|
| Coordination representation | `DEPENDENCY_TRACKED`: the examined dependency graph drives sequencing; no calendar schedule is invented. |
| Tracking | `FULL_GRAPH`: aim for a complete, acyclic production-order view; publish actual coverage and gaps. Compute blocked/available only from warranted edges after closure/cycle treatment, and from the accepted current DAG once one exists. |
| Dependency preparation | Agents propose source-grounded candidates from local SoWs and accepted interfaces; humans can add declarations in `_DEPENDENCIES.md`. Extraction mirrors declarations in `Dependencies.csv`; an inferred proposal is never made a human declaration. Candidate graph edges remain subject to the graph decisions. |
| Default threshold | `INITIALIZED` is the default **contract-definition maturity** threshold. It does not mean code, a technical input, supplier qualification or provider delivery is ready. Each dependency requiring an actual artifact, decision, test result or adoption states that evidence/condition explicitly; a lifecycle label alone cannot satisfy it. |
| Lifecycle policy | The actual preparation actor creates `OPEN`. After a valid source-grounded `SOW_V1` and its affected independent check pass, WORKING_ITEMS records `INITIALIZED` as a separate status act. SoW authors use `NO_STATUS_TOUCH`. No automatic `SEMANTIC_READY`, `IN_PROGRESS`, `CHECKING` or `ISSUED`. |
| Definition scope and continuation | Scaffold all11/41 and initialize one local `ScopeOfWork.md` per Deliverable, then extract dependencies and examine closure. This selects definition work, not implementation. Proceed between these already-authorized preparation stages once their checks pass; report defects and repair within scope. |
| Missing inputs/cycles | Keep external contributions and unresolved choices visible. Unresolved cycle edges are non-gating in computation but their affected work remains held; exclusion does not supply a missing input. Independent definition continues. |
| Optional work | No schedule, estimates, optional semantic-lensing pipeline or legacy four-document kits. No unsolicited MEMORY files. |

This choice is reserved by [project-setup method Phase1.2](../../../../workflows/project-setup/resources/method.md#phase-12-confirm-coordination-representation): **“Do not proceed until the human confirms.”** Phase1.3 asks for threshold/declaration rules; the contract requires the human-confirmed lifecycle policy. Representation/tracking alternatives remain `SCHEDULE_FIRST` or `HYBRID`, and `DECLARED` (explicitly partial) or `NOT_TRACKED` (no dependency-derived readiness claim). The recommendation fits the authorized route to an examined project DAG without inventing a schedule. No dependent setup mutations occur before the choice.

## Concrete sequence and ownership

1. **Complete:** record actual Group3 acceptance and freeze the exact final subject/audit. Record D108 separately as later receiving currency; accepted bytes stay unchanged.
2. **After the grouped choice:** WORKING_ITEMS records `_COORDINATION.md`, inventories targets and applies the effective `preparation` skill using deterministic scaffold tools. Preserve exact accepted fields, all41 minimum filesets and existing paths. Validate each newly created fileset.
3. **Local contracts:** fresh terminal TASKs run `chirality-root:bundled:workflow:scope-of-work`, `MODE=INIT`, one Deliverable per brief. Start with at most three concurrent authors from different interface contexts; each owns only its exact `ScopeOfWork.md` and run-local checks. Shared interface/ownership matters route through WORKING_ITEMS. Scale the next bounded cohort only after initial fan-in demonstrates consistent interpretation. A separate TASK checks affected fidelity and interfaces; producer checks are not independent review.
4. **Dependencies:** after checked local contracts, bounded TASKs run `dependency-extract` once per Deliverable; a separate `audit-dep-closure` TASK checks the frozen inventory/evidence. WORKING_ITEMS integrates repairs and routes nontrivial SCCs to bounded cases. No heuristic edge becomes accepted merely through extraction.
5. **Project DAG:** select `project-dag` from the same source-qualified library. Present its concrete basis/edge semantics/coverage/SCC treatments for checkpoint1; assemble and independently examine the version, then present checkpoint2 for actual acceptance. Only then publish its accepted pointer and hand off to local work-graph construction. Closure observation is not DAG acceptance. DAG acceptance does not pass30% or satisfy inputs.

WORKING_ITEMS owns coordination/control files, source integration and Git. TASKs are native terminal descendants with explicit disjoint scopes; these are brief restrictions, not sandbox claims. No sibling, provider, workflow or product source is assigned. Future contract gaps return at their point of need; none changes the present11/41 setup inventory. Standing Git closeout remains separate from all governed decisions.

Selected source: `chirality-root:bundled:workflow:project-setup`; effective preparation descriptor `{kind: skill, name: preparation, source: bundled, sourceRootId: chirality-root}` resolves to `.agents/skills/preparation/SKILL.md` in this repository. Actual origins/hashes and the resulting decision are retained in the current work graph/run evidence, without a new workflow or broad source-copy packet.
