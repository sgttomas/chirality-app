# D-GOV-25 — Acceptance of the first root decomposition (D-GOV-21 §6 step 8) with three ruled dispositions

Status:       RULED
HumanRuling:  "Merge PR #347 (CI green). Candidate SHA for the exact-candidate ruling: ec62af0700e530c1640698fa406398cb1cb45d29 / Decisions: 1. Record a reasoned deferral. 2. Update the labels as warranted. 3. Proceed in the manner you recommend." (owner, 2026-07-25; full verbatim fence below)
AcceptedCandidateSHA: ec62af0700e530c1640698fa406398cb1cb45d29
CandidateMergeSHA: ea0ad7a566ddb51d89297bfcf491636f1fc5dd15 (merge of PR #347 into `main`, 2026-07-25, at explicit owner direction — the accepted decomposition's basis on `main`)
PublicationSHA: ed5dc0a87b53f45a32057f7fe4c79b8d5a107538 (this record's publication commit; backfilled in the same tranche per the `f1549afb1` precedent)
EffectiveSHA: 653fabc9b3e8abf369f5e776a7d3ee24bf235e7a (merge of PR #348 into `main`, 2026-07-25, performed at explicit owner direction; backfilled by the step-9 materialization tranche per precedent)
Date:         2026-07-25
FramedBy:     Agent-drafted (Agent 0, `HELP_HUMAN` posture) at explicit owner direction (continue from D-GOV-21 §6 step 8, 2026-07-25, in-session)
AcceptedBasis: `main@24726a73c` (candidate authored and verified at that basis; ruled at the exact candidate commit)
DecisionKey:  `root_decomposition_acceptance`
RecordConvention: D-GOV-18/19/21/22/23/24 exact candidate-SHA ruling pattern; supersede-never-edit
Candidate:    `execution/_Decomposition/` package (working surface `Chirality_Root_SOFTWARE_DECOMP_v1_0.md` + six authoritative companion registers), committed at the AcceptedCandidateSHA, staged with all seven gates PENDING_OWNER_RULING

## Status note

This record is RULED. The owner accepted the candidate first root
decomposition against the exact candidate commit
`ec62af0700e530c1640698fa406398cb1cb45d29` and issued three dispositions.
On any disagreement between this summary and the ruled candidate at that
SHA (as amended by the ruled dispositions applied in this record's
publication tranche), the ruling governs.

**Acceptance vehicle (K-AUTH-2).** The owner's message did not use the
"I rule APPROVED for O-A" formula of D-GOV-18..24; it directed the merge,
designated the exact candidate SHA "for the exact-candidate ruling",
resolved the three decision items surfaced at the gate, and directed
"Proceed in the manner you recommend" — where the recommendation of record
(presented at the gate) was that such a ruling closes the decomposition
half of step 8 as acceptance of Gates 1–7 and the Gate 7 basis-for-
downstream-work declaration. K-AUTH-2 admits approval vehicles; this
record states the vehicle exactly and claims nothing beyond it. Any owner
correction supersedes.

## Recorded ruling

The owner ruled in-session on 2026-07-25:

<!-- BEGIN OWNER RULING VERBATIM -->
Merge PR #347 (CI green). Candidate SHA for the exact-candidate ruling: ec62af0700e530c1640698fa406398cb1cb45d29

Decisions:

1. Record a reasoned deferral.
2. Update the labels as warranted.
3. Proceed in the manner you recommend.
<!-- END OWNER RULING VERBATIM -->

The three numbered decisions map 1:1 to the three decision items surfaced
with the candidate at the gate (Receipt 46; run record
`execution/_Coordination/AgentRuns/ROOT-STEP8-DECOMP-20260725/`):

1. **OI-013** — the situated-working-root half of OBJ-2's success
   condition: **reasoned deferral recorded** (not covered at v1 stage;
   deferral text applied to the decomposition in this tranche).
2. **OI-001 / OI-002** — the two D-14-class source-currency findings:
   **labels updated as warranted** — the ledger keeps the PRD's source
   labels and carries effect annotations (17 PROPOSED items in effect per
   the D-GOV-22 adoption ruling, confirmed here); the standing-
   verification reading of the discharged §9.1 obligations and C-1..C-4
   is confirmed; the adopted PRD bytes remain untouched (D-13).
3. **OI-003 / OI-004** (framing strains) and mechanics — **accepted as
   staged / proceed as recommended**: the SOFTWARE_DECOMP framing and the
   standing-conformance reading stand with strains on record; the
   recommended post-ruling tranche (this one) applies the dispositions,
   publishes this record, and performs root Project Setup's guard-state
   instantiation.

## What is accepted

The first root decomposition of the Chirality Root product, derived solely
from the adopted PRD (`docs/PRD_ROOT.md`): **6 packages / 45 deliverables /
103 scope items**, F4 trace registers closed in both directions (with
OBJ-2's situated-root clause now carried as a recorded, reasoned deferral),
D-15 four-category coverage demonstrated. The decomposition package under
`execution/_Decomposition/` is the accepted basis for downstream root work
(Decomposition Standard Gate 7), as amended only by the ruled dispositions
applied in this record's publication tranche and recorded in the package's
own Decision Log.

## What this ruling does and does not release

- **Released — root Project Setup (packet §6 step 8, second act):** guard
  STATE instantiation under `execution/_harness/` (`adapter.yaml`,
  `surface_ownership.yaml`, `work_graph.yaml`, `root_guards.yaml`) against
  the accepted decomposition, performed in this tranche by a PROJECT_SETUP-
  role instance and verified by the live G0–G4 validators.
- **Not released — step 9 materialization.** No `PKG-*`/`DEL-*` structure
  is created under root `execution/`. Materialization remains behind the
  D-GOV-21 §5.3 gate and a further owner act, from this accepted
  decomposition only, with G0–G4 registered, running in CI, and passing.
- Practitioner-harness adoption of the root adapter remains a separately
  authorized open item; nothing here amends `PROJECT_ALIASES` or the
  loader.

## Downstream coordination (M6)

Pin survey at this basis: no downstream loop pins or mirrors the surfaces
this tranche changes (the app-dev authority corpus pins DIRECTIVE,
CONTRACT, SPEC, TYPES, PLAN, PRD, and two agent files — none touched).
Disposition: **none-required**; recorded with rationale in the tranche
manifest `docs/governance_harness/tranche_manifests/ROOT-STEP8-ACCEPT-20260725.yaml`.
