# D-GOV-22 — Adoption of the Chirality Root PRD

Status:       RULED
HumanRuling:  "I rule APPROVED for O-A against candidate SHA 90fae458bf485412e9c3a6295df193eb323c9774" (owner, 2026-07-25)
AcceptedCandidateSHA: 90fae458bf485412e9c3a6295df193eb323c9774
CandidateSubjectSHA: d9ea86f88504cb8d859a4cf3f042bac00d38fe57 (the commit containing the adopted Rev 5 PRD bytes; sha256 pins in the packet header)
PR340MergeSHA: d0f128647b9fa1800a2d6eda09084f17bfa97d49 (merge of PR #340 into `main`, 2026-07-25, performed at explicit owner direction immediately before the ruling took effect on publication)
PublicationSHA: c800631d59606e7b80c0c9f247ab867057ac543b (this record's publication commit; backfilled by the obligation-(a) tranche per the `f1549afb1` backfill precedent)
EffectiveSHA: 08f52627718e8ad12b0e7eb5567adc8e60899229 (merge of PR #341 into `main`, 2026-07-25, performed at explicit owner direction; backfilled by the same tranche)
Date:         2026-07-25
FramedBy:     Agent-drafted (Agent 0, `HELP_HUMAN` posture) under the owner's Lane A direction, root-PRD inquiry session, 2026-07-25, after four adversarial-review cycles by an independent second agent and five in-session owner rulings (RD-1..RD-5); run record `execution/_Coordination/AgentRuns/ROOT-PRD-LANE-A-20260725/`
AcceptedBasis: `d9ea86f88` (packet citations verified against that state)
DecisionKey:  `root_prd_adoption`
RecordConvention: D-GOV-18/19/21 exact candidate-SHA ruling pattern; supersede-never-edit
CandidatePacket: `docs/governance_harness/_PROPOSALS/D-GOV-22_root_prd_adoption/PACKET.md` (committed at the AcceptedCandidateSHA; carries the sha256-pinned candidate subject and the bidirectional PRD ↔ DIRECTIVE §1 concordance map as Annex A)

## Status note

This record is RULED. The owner approved **O-A — ADOPT** against the exact
candidate commit `90fae458bf485412e9c3a6295df193eb323c9774`, which contains
the full instrument packet: the sha256-pinned candidate subject (the Rev 5
adoption-ready root PRD and its concordance-annex evidence companion at
`d9ea86f88`), the effects and scope limits, the implementation tranche, the
items expressly put to the owner, and the Annex A concordance map. The packet
at that SHA is the substantive content of this decision; this record is its
ruling and publication surface. On any disagreement between this summary and
the packet at the AcceptedCandidateSHA, the packet governs.

**The Chirality Root PRD is adopted.** Per the PRD's own status model
(PRD §10.3), the adopted status is carried by **this record**, not by the PRD
file: the PRD banner points at the instrument, and this is that instrument.

## Recorded ruling

The owner ruled in-session on 2026-07-25, binding the ruling to the exact
candidate commit:

<!-- BEGIN OWNER RULING VERBATIM -->
I rule APPROVED for O-A against candidate SHA 90fae458bf485412e9c3a6295df193eb323c9774
<!-- END OWNER RULING VERBATIM -->

## Items put to the owner at ruling (packet §6) — both resolved

**C-3 — pre-repo lineage (ID-3 owner testimony): CONFIRMED.** The owner
stated in the same ruling message, verbatim:

<!-- BEGIN OWNER STATEMENT VERBATIM (C-3) -->
the "roughly three years" lingo is true but it was such a throwaway comment I find it hilarious and depressing that it's still getting mentioned all this time later.  Chirality has been in development for some time preceding the first commit evidence available.  Move on.
<!-- END OWNER STATEMENT VERBATIM (C-3) -->

Disposition: ID-3's testimony is confirmed as true — Chirality's development
precedes the first in-repo commit evidence (`7bee9ae41`, 2026-05-18). **C-3 is
CLOSED.** The confirmed claim carries the weight the owner gave it: a passing
characterization, true, and not load-bearing for any commitment. ID-3
(testimony) and ID-4 (git fact) remain stated separately in the adopted PRD;
no further recitation of the lineage estimate is warranted in future
instruments.

**ID-1 / ID-2 / ID-3 synthesis confirmation (packet §6.2): CONFIRMED.** The
owner ruled O-A with a correction to none of the three Agent 0-synthesized
identity claims (and expressly confirmed ID-3's substance above). Per the
packet's stated mechanics, the O-A ruling confirms them as accurate
syntheses.

## Effects (summary; packet §3 governs)

1. **The 17 PROPOSED items take effect as accepted commitments**: the v1
   boundary (PRD §3); OBJ-1..OBJ-7; D-13, D-14, D-15, D-16; the §7.2
   governed-promotion relationship; §8.3 release authority; falsifiers F4,
   F5, F6. TRANSCRIBED and CLARIFIED items continue to carry their own
   upstream authority.
2. **All five RD rulings (RD-1..RD-5) are SHA-bound** at this record's
   publication (K-AUTH-2), completing the in-session rulings recorded
   verbatim in PRD §9 and Loop Receipts 37–38.
3. **The Annex A concordance map is the recorded divergence state** between
   the adopted PRD and `docs/DIRECTIVE.md` §1: one DIVERGENT pair (the RD-1
   genus). C-1 remains `RESOLVED-IN-PRINCIPLE — concordance pending` until
   obligation (a) lands. The ratified DIRECTIVE §1 clause remains in force
   as written until that separate act.
4. **The implementation tranche (packet §5) is authorized**: publication
   mechanics, the RD-4-D adopted-copy placement in root `docs/` with
   pointer, obligations (a)/(b)/(c) presented as separately gated follow-ons,
   and the C-2/C-4 correction proposals.

## What this ruling does not do (packet §4 governs)

No root `execution/` materialization (`PKG-*`/`DEL-*` stay behind the
D-GOV-21 §5.3 gate; G0 enforcing); no root decomposition created or accepted
(D-GOV-21 §6 step 8 is its own future act); no public-export boundary change
(none needed for RD-4-D); no amendment of the ratified DIRECTIVE §1 genus
clause (obligation (a), separately gated); C-2 and C-4 remain open with
routed correction proposals.

## Implementation tranche state

Performed in this publication commit: this record; the `_REGISTER.md` row;
the RD-4-D placement (`docs/PRD_ROOT.md`, pointer block + adopted bytes);
Loop Receipt 39. Remaining, each separately gated: obligation (a) exact-prose
DIRECTIVE §1 supersession candidate (closes C-1); obligation (b) `README.md`
genus reword; obligation (c) SPEC/TYPES/AGENTS.md propagation survey; C-2
(CONTRACT §1 invariant-index arithmetic) and C-4 (README export description)
correction proposals. D-GOV-21 §6 step 5 (Lane A) is CLOSED by this ruling;
step 6 (Lane B, guard capability G1–G4) is the next open root-loop lane.
