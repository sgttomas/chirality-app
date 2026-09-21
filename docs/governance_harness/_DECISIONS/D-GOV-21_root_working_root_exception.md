# D-GOV-21 — Root working-root exception and replacement containment contract

Status:       RULED
HumanRuling:  "I rule APPROVED for O-A against candidate SHA c038c493e871c95871823281b45890ba9404624b" (owner, 2026-07-25)
AcceptedCandidateSHA: c038c493e871c95871823281b45890ba9404624b
PublicationSHA: 75b7aa6d1fb019846ac76fb775df2fc1652ab8a8 (this record's publication commit; backfilled in the implementation tranche per the `f1549afb1` backfill precedent)
EffectiveSHA: ee42157290618e3f84be0e0b651c041387ad6ee0 (merge of PR #338 into `main`, 2026-07-25, performed at explicit owner direction; backfilled by the ROOT-LOOP-REORIENT-20260725 tranche per the `f1549afb1` backfill precedent)
Date:         2026-07-25
FramedBy:     Agent-drafted under owner direction, root-PRD inquiry session, 2026-07-25, with independent adversarial review by a second agent (two passes; dispositions in the packet §16)
AcceptedBasis: `main@1049e011c`
DecisionKey:  `root_working_root_exception`
RecordConvention: D-GOV-18/19 exact candidate-SHA ruling pattern; supersede-never-edit
CandidatePacket: `docs/governance_harness/_PROPOSALS/D-GOV-21_root-working-root-exception/PACKET.md` (Revision 3, committed at the AcceptedCandidateSHA; the packet file deliberately retains its internal `TBD` placeholders — amending it would change the ruled SHA)

## Status note

This record is RULED. The owner approved **O-A — Adopt as specified** against
the exact candidate commit `c038c493e871c95871823281b45890ba9404624b`, which
contains the full decision packet (options, supersession table, Annex A exact
candidate prose, containment contract, sequence, falsifiers). The packet at
that SHA is the substantive content of this decision; this record is its
ruling and publication surface. On any disagreement between this summary and
the packet at the AcceptedCandidateSHA, the packet governs.

The §1 owner-direction transcription block inside the candidate stood
uncorrected at ruling; the owner issued no correction, and the ruling
approves the exact candidate SHA containing that block. Any later correction
to the transcription is a superseding act, not an edit.

The ruling authorizes the packet's five §2 effects and its §14 implementation
mechanics. It does not itself materialize anything: root `execution/` becomes
**eligible** for `PKG-*`/`DEL-*` structure only after the packet's §5.3 gate
closes (guards G0–G4 registered and passing, root decomposition accepted from
an adopted root PRD). Nothing in this ruling adopts the root PRD, changes the
public-export boundary, extends the exception to any other working root, or
waives the decomposition pipeline (packet §4).

## Recorded ruling

The owner ruled in-session on 2026-07-25, binding the ruling to the exact
candidate commit:

<!-- BEGIN OWNER RULING VERBATIM -->
I rule APPROVED for O-A against candidate SHA c038c493e871c95871823281b45890ba9404624b
<!-- END OWNER RULING VERBATIM -->

## Effects (summary; packet governs)

1. **Root as working root (narrow exception).** The repository root is both
   the shared instruction root and the working root for development of the
   root product. No other working root gains this property.
2. **Root execution root.** Root `execution/` is the root product's lawful
   execution root, eligible for `PKG-*`/`DEL-*` after the packet's §6 gates
   close. Existing control-plane records remain valid historical state.
3. **Enumerated supersessions.** Normative clauses S1–S9 (DIRECTIVE §1/§2/§2.6/§5,
   SPEC §0.2.1–§0.3/§1, TYPES §1.4) are amended exactly per the packet's
   Annex A; S10 (`execution/_Coordination/LOOP_INIT.md`) is updated as an
   orientation surface. Anything not enumerated remains in force unchanged.
   D-GOV-09 remains the historical ratification act; this decision
   prospectively amends the S1–S9 clauses of the corpus it ratified.
4. **Replacement containment contract.** Mechanisms M1–M7 and deterministic
   guards G0–G4 are required, with the §5.3 gate ordering. G0 (the
   materialization fence) ships in the implementation tranche and is wired
   into governance-harness CI.
5. **PRD-development basis.** Development of the candidate root PRD is
   authorized on this basis; PRD adoption is a separate future act
   (packet §11).

## Implementation gates (from packet §14)

1. ~~Commit the exact candidate; record AcceptedCandidateSHA~~ — done,
   `c038c493e871c95871823281b45890ba9404624b`.
2. ~~Owner ruling recorded verbatim; record published in `_DECISIONS/`~~ —
   this record.
3. Implementation tranche applies Annex A per its stated application
   semantics, plus §3b propagation, the S10 LOOP_INIT rewrite, G0, and the
   register row. Any necessary deviation from Annex A prose returns for
   exact-prose re-acceptance before merge. The merged implementation commit
   is recorded as the EffectiveSHA; the merge is human-gated.

Adjacent obligations and their classes (root-loop reorientation before
root-PRD development; independent historical reconciliation; conditional
runtime work; the guard-design preflight) are enumerated in packet §7 and are
not restated here.
