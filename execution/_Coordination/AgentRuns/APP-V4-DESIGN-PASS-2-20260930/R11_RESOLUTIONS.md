# R11 rulings — repairs from review V17

Integrator: HELP_HUMAN. Inputs: [reviews/V17-A.md](reviews/V17-A.md) and
[reviews/V17-B.md](reviews/V17-B.md), both HOLD at `764e599ee7`. R9 (as
corrected by R10-1) and R10 stand. Every finding is dispositioned below.

## Blocking

**R11-1 (V17-A B-1). ACT AP-5 says recording is required where observed.**
Reword AP-5 so that a checkpoint's arrival, the request where it can be
identified, and the act that answers it are recorded where the arrival is
observed, and that this is required, not optional (R9-1; EXEC PH-6; SoW
DEL-02-03 REQ-002). Recording is observation, not enforcement.

**R11-2 (V17-B B-1). EXEC CH-20 gets its own binding.** CH-20 exists to show
an earlier act counting for part of a checkpoint's subject and a new act
answering the rest (K1-2 with JA-1). Give it its own local variant,
`L-EXEC-n` (next free number), with `CP-review` binding S-2 and S-3 and T2's
A4 on S-2 before the arrival at T4. Its result stands as recomputed at A3.
Stop citing WD-EX R-9b / L-WDEX-7 as CH-20's input; cite it as the related
single-support case, whose result (*performed* by T2's A4) is consistent
with CH-20 under K1-2. The integrator has corrected DISPATCH's A3 row.

## Major

**R11-3 (V17-A M-1; V17-B M-1). Header pins to run records.** In every
Design file header that pins a run record of this run, pin the final bytes of
R9_RESOLUTIONS.md, R10_RESOLUTIONS.md, R11_RESOLUTIONS.md (this file) and
OWNER_DECISIONS.md, and of `_Coordination/HANDOFF_SWBPIPE_DOMAINS.md` where a
file pins it. The integrator will not edit those five files again before
PR-1. Compute each value with `shasum -a 256` at the start of the repair and
verify at the end. GUIDE's 18-row table is re-verified afterwards by script
(18/18); GUIDE's own header gets the same treatment.

**R11-4 (V17-B M-2; V17-A m-1). Change-table closing sentences.** Where a
Wave A change table's preamble or closing sentence says no rule, disposition,
case result or standing changed (WD, WD-EX, EXEC; C, P), mark that sentence
"at A1" and add one sentence stating what A3 changed (DECISION-K1: SP-6 is
the SETTLED earlier-act rule for the current phase, the R4-5 rule is kept as
SP-6F, a governance-phase option; JA-1 added; the listed cases recomputed).
In C also name the SP-6-cost row closed at A3.

**R11-5 (V17-B M-3). LOOP labels.** NW-5: label DERIVED from V4-HOST-01
("the person chooses", no default) and the always-off item in V4-HOST-02 and
ARCHITECTURE §4 ("a silent switch … unless the person turns it on"); SETTLED
only for "no silent switch unless the person turns it on". The §5.1.1
enforcement bullet: SETTLED by V4-ARC-12 for recording every destination
contacted; "records the refusal" is PROPOSED (V4-EXM-23 says a declined
request is reported to the agent; no accepted text says the refusal is
recorded).

## Minor

**R11-6 (V17-A m-2).** RS E10 (i) and VC-17 add the governance-phase reading
under SP-6F, as the reviewer proposes.

**R11-7 (V17-A m-3).** ACT AP-12: "Its request is an A8 (§2.1; DERIVED)".

**R11-8 (V17-B m-2).** PANEL PC-19b and PC-21i: drop "Phase 1 reads …" from
the SP-6F clause.

**R11-9 (V17-B m-3).** CA §12.9 F-23: annotate that after K1-2 CH-20 shows an
earlier act counting; W14-05's "prior act not counted" negative now needs a
case where the earlier act's content is no longer current or its kind
differs. If an existing EXEC case shows that in the current phase, cite it;
otherwise return it for node B7 and say so in F-23.

**R11-10 (V17-B m-1, m-4).** Records only; done by the integrator
(DISPATCH, graph, BRIEFS note; OWNER_DECISIONS now cites the page's wording
and quotes the executor-model direction).

## Notes

- **V17-A N-1:** add "SETTLED by DECISION-K1 K1-1" beside the "(R9-1)"
  requester citations in C FXA-5 and V-GR1, P §4.4, ADAPTER §5.3 and §7.7.
- **V17-A N-2:** ACT §4.5 cites EXEC §5 (CAP-1…CAP-9) instead of the closed
  WD U-25.
- **V17-A N-3, N-4, N-5; V17-B n-1…n-4:** no change. N-4 (three wordings of
  "prior act not counted") is left to Wave B, where the record labels are
  fixed (node B4).
- **V17-B n-5** ("otherwise reacts" versus "records what it observes"):
  carried to node B2, which will say that recording is not a reaction to the
  arrival.
