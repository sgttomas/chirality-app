# D-GOV-21 Implementation Handoff — root working-root exception tranche

Handoff state per the AGENTS.md handoff-state and snapshot rules, emitted by
the D-GOV-21 implementation tranche (PACKET.md §14 step 3, §6 step 3).

## Accepted upstream state

- **Ruling:** D-GOV-21 RULED 2026-07-25 — "I rule APPROVED for O-A against
  candidate SHA c038c493e871c95871823281b45890ba9404624b" (owner).
- **AcceptedCandidateSHA:** `c038c493e871c95871823281b45890ba9404624b`
  (PACKET.md Rev 3, `_PROPOSALS/D-GOV-21_root-working-root-exception/`).
- **PublicationSHA:** `75b7aa6d1fb019846ac76fb775df2fc1652ab8a8`
  (`_DECISIONS/D-GOV-21_root_working_root_exception.md`).
- **EffectiveSHA:** `ee42157290618e3f84be0e0b651c041387ad6ee0` — the
  human-gated merge of this tranche's branch into `main` (PR #338,
  2026-07-25, merged at explicit owner direction; backfilled by the
  ROOT-LOOP-REORIENT-20260725 tranche).

## Tranche contents (this commit)

Annex A applied exactly as ruled (application semantics: exact wording at
identified anchors; complete resulting text for sentence/row units — no
deviations, so no exact-prose re-acceptance round is required):

- `docs/DIRECTIVE.md` — S1 (:199, :202, :204), S2 (:13), S3 (:76),
  S4 (:300), S5 (:301)
- `docs/SPEC.md` — S6 (:48, :52), S7 (:79 `{WORKING_ROOT}` row), S8 (:97)
- `docs/TYPES.md` — S9 (Working Root and Execution Root rows)

S10 and §3b propagation:

- `execution/_Coordination/LOOP_INIT.md` — bootstrap fence and §6 write-rule
  rewritten to describe the D-GOV-21 arrangement (orientation, not authority)
- `README.md` — Core Architecture separation description, exception added

Guard G0 (materialization fence), shipped and wired:

- `tools/validation/validate_root_materialization_fence.py`
- `tools/validation/test_validate_root_materialization_fence.py` (9 tests)
- `.github/workflows/governance-harness.yml` — G0 step added (BLOCK fails
  the run per D-GOV-02)

Records and notices:

- `docs/governance_harness/_DECISIONS/_REGISTER.md` — D-GOV-21 row
- `docs/governance_harness/_DECISIONS/D-GOV-21_root_working_root_exception.md`
  — PublicationSHA backfilled (f1549afb1 precedent)
- `projects/chirality-app-dev/execution/_Coordination/NOTICE_D-GOV-21_ROOT_DOCTRINE_AMENDMENT.md`
  (routed M6 notice; demonstrably active pinned surface)
- `domains/chirality/_Coordination/NOTICE_D-GOV-21_ROOT_DOCTRINE_AMENDMENT.md`
  (routed M6 notice; substitutes for absent corpus-drift detection)
- this handoff file

## Tranche manifest (M2/G4 discipline, recorded ahead of G4 existing)

Protected instruction-surface paths changed by this tranche:
`docs/DIRECTIVE.md`, `docs/SPEC.md`, `docs/TYPES.md`,
`docs/governance_harness/**` (records), `tools/validation/**` (G0),
`.github/workflows/governance-harness.yml`, `README.md`. Authorization: the
D-GOV-21 owner ruling itself (independent owner authorization; the exact
edits are the ruled Annex A). Merge gate: human-gated PR — never self-merged.

## Derivative-package status

- **Public export staging (`exports/chirality-app`): regeneration DEFERRED.**
  `docs/` is in the export allowlist; the Annex A edits stale the exported
  copies and manifest hashes. Regenerate from the merged EffectiveSHA before
  any subsequent public-export apply; do not apply an export from a
  pre-D-GOV-21 staging once this tranche merges. Authoritative source for
  regeneration: the EffectiveSHA (this branch's merge into `main`).
- Root `execution/` remains outside the export allowlist (packet §4).

## Closure verdict and rerun requirements

- Verdict: implementation tranche COMPLETE as a candidate; closure occurs at
  the human-gated merge (EffectiveSHA).
- Verified in-tranche: G0 test suite 9/9 pass; live G0 run PASS (fence idle
  — no PKG-*/DEL-* children exist; packet §10 "nothing materializes at
  ruling" holds); practitioner-harness suite + self-check run pre-commit
  (results in the tranche's session evidence and CI).
- Rerun on any rebase: harness suite, self-check, G0 suite + live run,
  `validate_path_anchors.py`.
- Known accepted finding: self-check WARN `UNRESOLVED_SOURCE_REF` at
  `PACKET.md:356` — the packet's declined O-B option names
  `projects/chirality-root/`, which deliberately does not exist. The packet
  is the exact ruled candidate and must not be amended (amendment would void
  the AcceptedCandidateSHA); the WARN is non-gating and stands as recorded.

## Remaining blockers / downstream sequence (packet §6)

1. **Step 4 — root-loop reorientation** (obligation of the ruling, §7 class
   a): `execution/_Coordination/CURRENT_WORKPLAN.md` still targets a CLOSED
   workplan; reorient before root-PRD development begins. Separate tranche.
2. **Step 5 — candidate root PRD development** (authorized basis; adoption
   reserved, packet §11). After step 4; may parallel step 6.
3. **Step 6 — guard capability G1–G4** (validator code + CI wiring) before
   root Project Setup; G0 enforces the ordering. Preflight per §7: run the
   full harness/validation suites against a scratch root `PKG-*` skeleton
   before G1–G4 design.
4. **Steps 7–9** — PRD adoption (separate instrument), first root
   decomposition, Project Setup instantiating G2 register + first accepted
   work graph, then materialization with G0–G4 passing.
5. **Class b (independent, parallel):** historical receipt reconciliation
   (D-GOV-19/20 root receipts); K-WRITE-2 explanatory-gloss reconciliation.
6. **Class c (conditional):** root `chirality.project.json` +
   `instructionRoot = workingRoot = .` registry containment test before any
   runtime-backed root execution.
