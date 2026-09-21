# D-GOV-23 — Exact-prose supersession of the DIRECTIVE §1 genus clause

Status:       RULED
HumanRuling:  "I rule APPROVED for O-A against candidate SHA 65bb96378428a86ed8ab8581149ead056d756789" (owner, 2026-07-25)
AcceptedCandidateSHA: 65bb96378428a86ed8ab8581149ead056d756789
PublicationSHA: 9a28c8d378e8d0c949f2426b5c50c97366268b60 (this record's publication commit, which also applies Annex A; backfilled by the obligations-(b)/(c) tranche per the `f1549afb1` precedent)
EffectiveSHA: b6ae1d5d879a1205179ecedc71c8eecac333443e (merge of PR #342 into `main`, 2026-07-25, performed at explicit owner direction; backfilled by the same tranche)
Date:         2026-07-25
FramedBy:     Agent-drafted (Agent 0, `HELP_HUMAN` posture) executing D-GOV-22 packet §5 item 3 at explicit owner direction ("proceed with obligation (a)", 2026-07-25, in-session)
AcceptedBasis: `main@08f526277` (the D-GOV-22 EffectiveSHA; Annex A.1 verified byte-exact against that state)
DecisionKey:  `directive_genus_supersession`
RecordConvention: D-GOV-18/19/21/22 exact candidate-SHA ruling pattern; supersede-never-edit
CandidatePacket: `docs/governance_harness/_PROPOSALS/D-GOV-23_directive_genus_supersession/PACKET.md` (committed at the AcceptedCandidateSHA)

## Status note

This record is RULED. The owner approved **O-A — SUPERSEDE** against the
exact candidate commit `65bb96378428a86ed8ab8581149ead056d756789`. The
packet at that SHA is the substantive content of this decision; on any
disagreement between this summary and the packet, the packet governs.

The Annex A.2 replacement prose was applied to `docs/DIRECTIVE.md` §1 in
this record's publication commit, **extracted programmatically from the
ruled packet** (not retyped) after verifying the A.1 current text still
occurred exactly once in the live file. The application is byte-faithful to
the ruled candidate; no deviation occurred, so no re-approval round was
required (packet §6).

**C-1 is CLOSED.** The ratified DIRECTIVE §1 genus clause now carries the
RD-1 ruled two-level formulation verbatim (with the provenance
parenthetical the candidate specified). The single DIVERGENT pair in the
D-GOV-22 Annex A concordance map is concordant; the adopted PRD's §1.2
"ruled, concordance pending" state is satisfied by events — the adopted PRD
bytes are not edited (RD-4; any future PRD amendment is an M2 tranche).
Falsifier F5's watched condition (divergence becoming permanent and
unrecorded) is discharged for this pair.

## Recorded ruling

The owner ruled in-session on 2026-07-25, binding the ruling to the exact
candidate commit:

<!-- BEGIN OWNER RULING VERBATIM -->
I rule APPROVED for O-A against candidate SHA 65bb96378428a86ed8ab8581149ead056d756789
<!-- END OWNER RULING VERBATIM -->

## Scope applied (packet §3 governs)

Exactly one paragraph — the §1 opening paragraph of `docs/DIRECTIVE.md`.
Expressly untouched: the DIRECTIVE preamble sentence and all other
"operating system" prose (obligation (c), propagation survey);
`README.md` (obligation (b)); the instruction-surface description
"a release-managed agent operating system" retained verbatim inside the
replacement (the contained level under the ruled formulation); the adopted
PRD, its candidates, and prior decision records.

## Downstream coordination (M6)

`projects/chirality-app-dev` pins `docs/DIRECTIVE.md` by sha256 in
`execution/_Reconciliation/References/AUTHORITY_CORPUS.json`; that pin was
already stale relative to the D-GOV-21 S-clause amendments and this change
moves the live hash again. Routed change notices ship in this tranche to
`projects/chirality-app-dev` and `domains/chirality` coordination surfaces
(D-GOV-21 notice precedent); the receiving loops adopt, amend, or decline
under their own instruments and cadence. Detection does not depend on the
notices: corpus-drift checks remain the deterministic path.
