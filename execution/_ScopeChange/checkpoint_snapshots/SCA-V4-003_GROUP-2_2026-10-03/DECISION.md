# SCA-V4-003 checkpoint group 2 — accepted exact amendment and propagation plan

Recorded 2026-10-03 by node AK1 (stage 1), a Type 2 TASK (Claude Code
subagent; no delegation) dispatched by the HELP_HUMAN session of run
`APP-V4-SCA003-20261002`, which presented checkpoint K1. This record
transcribes the same owner act as the group-1 snapshot. One reply addressed
both subjects; it is recorded in two snapshots, as for SCA-V4-001 and
SCA-V4-002. It claims no inspection the owner did not perform.

## Custody of the act

Identical to `../SCA-V4-003_GROUP-1_2026-10-03/DECISION.md` "Custody of the
act": `AgentRuns/APP-V4-SCA003-20261002/OWNER_DECISIONS.md` (sha256
`59b20bb025d01fd2607d8b0824f507f3310a4b5255a6bf49943e14be18cdf919`), section
"DECISION-1 — Checkpoint K1: SCA-V4-003 scope-change groups 1 and 2 (owner,
exact, 2026-10-03)", added by commit
`5b16bb683192298fb89f2ed733f12b06dd21921f`; the owner's chat message was
recorded verbatim there by HELP_HUMAN.

## What the owner had in front of them

As the record states: `AMENDMENT_PACKET/OWNER_ITEMS.md` (committed at
`60359d7372`) with the packet files it cites, and the review page
https://claude.ai/artifact/A8XbVqJPNoWCHK3RM7YaYJ (Version 1). AK1 has not
read the page and does not claim the owner read any file. For group 2 the
subject is the exact amendment, the route and the register:

- `AMENDMENT_PACKET/Amendment_Actions.draft.csv` (sha256
  `9b7c2ce8fbf97ec0cf829c5024e03d19b4117c1ca50abaea4ec0b2c340346d1c`): the
  proposed register, 23 rows, written for the recommended options;
- `AMENDMENT_PACKET/BASIS_AMENDMENT.md` (sha256
  `151bc6fffcac482f6f8e77bf3d7b2822ec65f94012e0b66720f14644efbe35bf`): no
  basis change (Part A); the exact old → new bytes of B-01 (Change Register
  entry), B-02 (OI-009) and B-03 (OI-018); C-01 (`_LATEST.md`) and C-02 (the
  SCA-V4-002 effective-state note); the Part D supersession row D-021; with
  the slot rules for the acceptance-conditional edits;
- `AMENDMENT_PACKET/SOW_REVISIONS_A.md` (sha256
  `42c9167aadf8f0f88cc42b6e746af221140c2b7a00b7feaca552692e0cc7fc07`): 63
  exact ScopeOfWork blocks for DEL-01-01…01-05;
- `AMENDMENT_PACKET/SOW_REVISIONS_B.md` (sha256
  `d7b5cb2422cfdc69755e582b920351dccfced4d8871dc722f87ada48cfbb94df`): 84
  exact ScopeOfWork blocks for the 14 deliverables outside PKG-01;
- `AMENDMENT_PACKET/IMPACT_ASSESSMENT.md` (sha256
  `46ea15e5b2930c66d97bdc9d10ed5224633e946ba47eb2b2b30897c05f5435f3`) §3 (the
  register proposal), §6 (package roles), §7 (supersession), §10 (write
  boundary and propagation outline) and §11 (derivative status);
- `AMENDMENT_PACKET/ARC_EFFECT.md` (sha256
  `25073317e9cde08ea38d90a37be8823c74bcf32d00d4490fffe9e743320894e7`) §4 (the
  expected DAG-003 departure);
- `AMENDMENT_PACKET/OWNER_ITEMS.md` (sha256
  `72c53db208ff42cce271816df9b22898405ff53ca8e5618a1216c21e3877db86`) Q-3,
  Q-16, the exact text behind Q-4, Q-5, Q-6, Q-8, Q-10, Q-11, Q-15 and Q-17,
  and "Drafted text for your review".

Each file was hashed at `60359d7372` and at this transcription; the bytes are
identical.

## The owner's act (verbatim)

> accept the remaining items as recommended

No correction, exception or rewording was recorded. OWNER_ITEMS says
"Accepting 'as recommended' accepts this wording; you may ask for any of it
to be reworded before group 2 is recorded"; no rewording was asked for.

## Interpretation (recording role's reading, not owner text)

| Item | Effect |
|---|---|
| Q-3 | Write boundary: direct candidate writes are `_Decomposition/Open_Issues.csv` (B-02, B-03) and the SCA-V4-003 snapshot folders under `_ScopeChange/`; after group 3, the Change Register entry (B-01) and the pointer (C-01); nothing else. Route: the 19 ScopeOfWork files change only after group 3, by `scope-of-work` `MODE=REVISE`, one per brief, `STATUS_POLICY=NO_STATUS_TOUCH`, then `MODE=VERIFY`; then `dependency-extract` UPDATE for 20 registers (with DEL-04-03's `_DEPENDENCIES.md`), the `project-dag` currency audit and DAG-004 for the owner. The disclosed wording conventions (deliverable IDs without backticks in four requirements; "in the format of DEL-04-03"; "outside this undertaking" dropped for every receiver) are accepted |
| Register | The 23-row register as drafted: all `MODIFY`; `ScopeChanging` `YES` on actions 2, 3, 4, 5, 7, 8, 9 and 10 (DEL-01-02, 01-03, 01-04, 01-05, 02-02, 02-03, 02-04, 03-01), `NO` on the other 15; `SupersessionBindingPresent` `YES` on action 21 only |
| Q-4 | The grounding sentences P1-01, P1-02, P1-03 and P1-05 as drafted in SOW_REVISIONS_B; no block for NR-03 |
| Q-5 | SOW_REVISIONS_A blocks G-0104-01…14 as written: REQ-008 as adjusted (G-0104-09), and the drafted OUT-005, AC-008, VER-008, matrix row and claim sentences |
| Q-6, Q-8 | SOW_REVISIONS_B's DEL-03-01 blocks for S-01-2, S-01-3 and S-01-5, as written |
| Q-7, Q-9, Q-14 | No block and no register row for the held items (SOW_REVISIONS_B "Not written") |
| Q-10 | Option B: B-02 with `Status` `RESOLVED_BY_OWNER_DECISION` and the option-B `Consequence`; the D-021 row of BASIS_AMENDMENT Part D, exactly; action 21 `SupersessionBindingPresent` `YES` |
| Q-11 | B-03 (the OI-018 pointer) and the optional blocks as written (G-0401-02 with "captured through DEL-01-04's App act control", S-02-2, S-03-3, S-03-4, S-04-3, S-11-1, SC3-01-02-10, -11, SC3-01-05-13) |
| Q-15, Q-17 | The receivers sentences P1-06…P1-10 and G-0403-03 (R22-7-SoW) as written; their mirror rows, including the 15 RP1-MX rows, are carried by register actions 6, 8, 14 and 16 |
| Q-16 | Each decision snapshot is committed before the next stage uses it; C-02 is written after group 1 |
| Drafted text | The agent-drafted wording listed in OWNER_ITEMS "Drafted text for your review" is accepted as worded |

**The register.** The authoritative register is `Amendment_Actions.csv` in
this folder (sha256
`9b7c2ce8fbf97ec0cf829c5024e03d19b4117c1ca50abaea4ec0b2c340346d1c`), bound in
`ACCEPTED_MANIFEST.csv` with the role `action register`. It is a byte copy of
`Amendment_Actions.draft.csv` (`cmp` equal). No change was needed: the draft
was written for the recommended options, the owner accepted every
recommendation, so no item was declined, no row is dropped or renumbered, and
no Description loses an ID. The draft carries no unfilled token
(`AmendmentID` is `SCA-V4-003` on every row). Checks made for this record, by
script: 23 rows; every value free of leading and trailing spaces; every
`AffectedFiles` path exists; every INCLUDE row of `LEDGER.csv` is named in a
Description, and no DEFER or DROP row is.

**Acceptance-conditional edits and their slots, as fixed by this act.**

| Edit | When | Slots |
|---|---|---|
| B-01 Change Register entry (DC-01) | After group-3 acceptance | `{ACCEPT_DATE}` = group-3 acceptance date; `{AMENDMENT_SNAPSHOT}` = accepted snapshot folder name; `{Q5_CLAUSE}` = `, including the App act control in DEL-01-04`; `{OI009_CLAUSE}` = `Open_Issues OI-009 Status (RESOLVED_BY_OWNER_DECISION) and Consequence`; `{OI018_CLAUSE}` = ` and the OI-018 Consequence pointer`; `{D021_CLAUSE}` = `; and a Supersession_Delta row binding the GROUP3 OI-009 Status` |
| C-01 `_ScopeChange/_LATEST.md` | After group-3 acceptance | `{AMENDMENT_SNAPSHOT}`, `{ACCEPT_DATE}`, `{CLOSURE_VERDICT}`, `{G1_DATE}` = `2026-10-03`, `{G2_DATE}` = `2026-10-03`, `{C02_UTC}`, `{UTC}` per BASIS_AMENDMENT C-01 |
| ScopeOfWork AX lines | At REVISE, after group 3 | `{AMENDMENT_ID}` = `SCA-V4-003`; `{AMENDMENT_SNAPSHOT}` = accepted snapshot folder name |

**Candidate writes fixed by this act.** B-02 (option B) and B-03 together;
BASIS_AMENDMENT gives the expected `Open_Issues.csv` result sha256
`9c2d916c277f8ce4b847c9c532822d0566e59517ba9e0a86b650fe0450f3515d` (OPEN
count 22) from the current file `a11782181531ce77e564b774787537d3e11cc1d4304123cba0d83f539bb280f0`
(the current hash checked at this record; V23b reproduced the result hash).
`Supersession_Delta.csv` is the BASIS_AMENDMENT Part D block exactly (header
and the D-021 row; no token to fill). `Supersession_Map.csv` is accumulated
from SCA-V4-002's map (sha256 `45502bf5…eb93`, 29 rows) with
`tools/coordination/accumulate_supersession_map.py` (expected 30 rows).

No affected deliverable is CHECKING or ISSUED (all 20 targets are
IN_PROGRESS at this record, after the Q-13 act), so no register row
authorizes a reopening.

## What this acceptance authorizes and does not authorize

It authorizes checkpoint-group-3 preparation from this snapshot
(`ACCEPTED_GROUP2_DECISION_SNAPSHOT`), in posture `ACCEPTED_PREDECESSOR`:
- writing the candidate poststate: B-02 and B-03 in `Open_Issues.csv`;
- the candidate `Supersession_Delta.csv` (D-021) and the accumulated
  `Supersession_Map.csv`;
- the post-change audit over the baseline's scope (PKG-01, 02, 03, 04, 05, 09,
  10) and its comparison with the baseline, and the independent review.

It does not authorize, before group-3 acceptance:
- B-01 or C-01;
- any `ScopeOfWork.md` edit (REVISE waits for group 3), or any
  `Dependencies.csv`, `_DEPENDENCIES.md` or `_DAG` change;
- any basis document, other decomposition file, `_CONTEXT.md`, `_STATUS.md`
  or `Coverage_Telemetry.json` write;
- moving `_LATEST.md` or marking an accepted `SCA-*` snapshot.

## Basis

At the transcription (`HEAD` `7fea17baaf1c182a49c11cab458503ab532c9063`):
the accepted decomposition GROUP3 as amended by SCA-V4-001 and the accepted
predecessor `_ScopeChange/SCA-V4-002_2026-09-29_1901/`; the group-1 snapshot
`../SCA-V4-003_GROUP-1_2026-10-03/` (recorded from the same act). No
SCA-V4-003 edit had been applied when this snapshot was written.

Group-3 pointer posture: `ACCEPTED_PREDECESSOR`.
