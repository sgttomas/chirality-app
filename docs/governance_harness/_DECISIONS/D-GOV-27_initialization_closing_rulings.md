# D-GOV-27 — Initialization-phase closing rulings: lifecycle transition, ResponsibleParty, register reconciliation, contract refresh, exact-prose packet

Status:       RULED
HumanRuling:  Owner, in-session, 2026-07-25, via structured decision prompts; verbatim selections fenced below (K-AUTH-2 vehicle stated)
PublicationSHA: 3ed51532751b8404e402f749064d6a2cb240a607 (this record's publication commit; backfilled in the same tranche per precedent)
EffectiveSHA: bfb21d11a955b98eb0a4885cc7777ad8df27fd75 (merge of PR #355 into `main`, 2026-07-25; backfilled by this closeout tranche)
Date:         2026-07-25
FramedBy:     Agent-drafted (Agent 0, `HELP_HUMAN` posture); the divergence evidence and options were surfaced from the ROOT-INIT-SOW-20260725 fan-in (Receipt 51)
AcceptedBasis: `main@8edb96fb1` (post-PR-#354 — all 45 scopes of work accepted)
DecisionKey:  `initialization_closing`
RecordConvention: supersede-never-edit
Run record:   `execution/_Coordination/AgentRuns/ROOT-INIT-SOW-20260725/`

## Recorded rulings

The initialization phase plan was approved by the owner in-session 2026-07-25
with four decisions recorded verbatim in
`execution/_Coordination/WORKPLAN_2026-07-25_root_initialization.md`
(one PR ×45; one closing tranche; candidate AC/VER authorization;
ResponsibleParty "Ryan Tufts" assigned at close). PR #354 (merge
`8edb96fb1`) accepted the 45 authored contracts at the human gate. At that
gate the owner ruled the following, selecting from structured options whose
full text is preserved in the session transcript; the selected options
verbatim:

<!-- BEGIN OWNER RULING VERBATIM (selected options, 2026-07-25) -->
1. Divergences (SOW-010, SOW-020, SOW-001/061, SOW-069): "Additive
   propagation (Recommended)" — Ledger item-level mappings stand; the four
   deliverable-register rows gain the missing objective (DEL-01-04 +OBJ-003;
   DEL-03-01, DEL-03-06, DEL-06-04 +OBJ-004), with consequent
   register/telemetry/working-surface/_CONTEXT updates.
2. Contracts: "Update frontmatter + CON now" — PR 2 also amends the four
   contracts (add the ruled objective to frontmatter, annotate CON-* as
   ruled), with re-validation of all four.
3. Prose packet: "Fold in all four restatements (Recommended)" — PRD O-1
   enumeration (D-13 supersession mechanics), DIRECTIVE §1 and §2.6 stale
   enumerations (desktop-packaging list NOT gaining `.github/workflows/`),
   TYPES §1.4 — exact prose staged for review at the PR 2 gate.
<!-- END OWNER RULING VERBATIM -->

Sequencing direction of record (owner, same session): "merge PR #354" after
electing to merge first and attend to the gate items in PR 2.

**Vehicle (K-AUTH-2).** No exact candidate SHA was designated; the rulings
adopt the recommendations above as dispositions, the exact applied prose is
staged in this tranche, and approval binds at the merge SHA of the
human-gated PR carrying it (the EffectiveSHA above, backfilled on merge).
The owner reviews the exact prose at that gate; any owner correction
supersedes.

## Effects applied in this tranche

1. **Lifecycle transition (approved plan, decision 2).** All 45 deliverables
   advance `OPEN → INITIALIZED` via `tools/scaffolding/write_status.sh`
   (actor `TASK+scope-of-work`, per `docs/SPEC.md` §3.3, after 45× `SOW_V1`
   validation at PR #354). The live CI pin in
   `tools/practitioner_harness/test_root_adoption.py` moves
   `| OPEN | 45 |` → `| INITIALIZED | 45 |` in the same PR (pin discipline:
   never silently).
2. **ResponsibleParty (approved plan, decision 4).** `Ryan Tufts` is
   assigned on all 45 `_CONTEXT.md` files and the deliverable register's
   `ResponsibleParty` column — a human-authorized bulk edit executed
   mechanically (K-AUTH-1: the assignment is the owner's act; the agent
   transcribes it).
3. **Register reconciliation (ruling 1).** Additive propagation across the
   accepted decomposition's companion registers (the amendment surface):
   deliverable register `SupportsObjectives` (4 rows); objective register
   `MappedDeliverables` (OBJ-003 +DEL-01-04; OBJ-004 +DEL-03-01, DEL-03-06,
   DEL-06-04); forward coverage register `DeliverableIDs` (OBJ-3, OBJ-4
   rows); working-surface objective and deliverable tables updated to match;
   decision log gains DEC-021 citing this record. The scope ledger is
   untouched — its item-level mappings were ruled correct.
4. **Contract refresh (ruling 2).** The four affected `ScopeOfWork.md`
   contracts gain the ruled objective in `package_objective_refs`, and each
   existing CON-* divergence record (DEL-01-04, DEL-03-01, DEL-06-04) gains
   a ruled-disposition sentence citing this record; DEL-03-06 (which
   disclosed no CON for this divergence) gains the frontmatter update only.
   All four re-validate `PASS format=SOW_V1`; all 45 re-validated at
   tranche close.
5. **Exact-prose packet (ruling 3).**
   - `docs/DIRECTIVE.md` §1 and §2.6 first list, and `docs/TYPES.md` §1.4
     Instruction Root row: the instruction-surface enumeration gains
     `CLAUDE.md` and `.github/workflows/`, aligning with `docs/SPEC.md`
     §0.2.1 as ruled by D-GOV-26. The §2.6 desktop-packaging sublist is
     deliberately unchanged (it enumerates what is packaged as
     `instruction-root/`, which gains neither member).
   - `docs/PRD_ROOT.md` §5.2 O-1: superseded by instrument, not edited —
     per the PRD's own D-13 (adopted bytes are never overwritten at their
     path). **Superseding statement:** the shared instruction surface is
     `AGENTS.md`, `CLAUDE.md`, `agents/`, `skills/`, `tools/`, root
     `docs/`, `init/`, and `.github/workflows/`, as enumerated by
     `docs/SPEC.md` §0.2.1 (D-GOV-26); O-1's six-member enumeration is
     stale as of that ruling and is read through this supersession. The
     placement copy's pointer block (placement metadata above the
     horizontal rule, outside the adopted bytes) gains an amendment-of-
     record note pointing here; every byte below the rule is unchanged.
6. **Work graph.** The six package nodes return `active → pending`
   (nothing is dispatched between phases); `accepted_basis` comment updated.
7. **D-GOV-26 EffectiveSHA backfill:**
   `31b8dc94acca50dbaf9a518a23dad8583c8c6c62` (merge of PR #351), owed to
   the next tranche per precedent — discharged here.

## Downstream coordination (M6)

Pin survey at the AcceptedBasis: no project or domain loop pins any file
touched by this tranche. The app-dev authority corpus's current-version
hashes were matched against both candidates and resolve to the
**project-local** `projects/chirality-app-dev/docs/` copies (DIRECTIVE,
CONTRACT, SPEC, TYPES, PLAN, PRD), not root `docs/`; its two `AGENT_*`
pins are historical-snapshot hashes of `agents/` files untouched here; the
harness-premerge instruction-root fixture likewise consumes the
project-local docs. Root `docs/PRD_ROOT.md`, root `docs/DIRECTIVE.md`,
root `docs/TYPES.md`, and `tools/practitioner_harness/test_root_adoption.py`
are pinned by no loop. Disposition: `none-required`, recorded in the
tranche manifest with this survey as rationale.
