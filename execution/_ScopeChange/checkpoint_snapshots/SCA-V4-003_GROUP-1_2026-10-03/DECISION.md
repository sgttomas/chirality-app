# SCA-V4-003 checkpoint group 1 — accepted proposed change and impact

Recorded 2026-10-03 by node AK1 (stage 1), a Type 2 TASK (Claude Code
subagent; no delegation) dispatched by the HELP_HUMAN session of run
`APP-V4-SCA003-20261002`, which presented checkpoint K1 to the owner. This
record transcribes the owner's act as it is recorded in the run's
`OWNER_DECISIONS.md`. It is not a new request for the same decision, and it
claims no inspection the owner did not perform.

## Custody of the act

| Item | Value |
|---|---|
| Record | `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-SCA003-20261002/OWNER_DECISIONS.md`, section "DECISION-1 — Checkpoint K1: SCA-V4-003 scope-change groups 1 and 2 (owner, exact, 2026-10-03)" |
| Record sha256 at transcription | `59b20bb025d01fd2607d8b0824f507f3310a4b5255a6bf49943e14be18cdf919` (equal to the bytes at the commit below; the file has not changed since) |
| Commit that added DECISION-1 | `5b16bb683192298fb89f2ed733f12b06dd21921f` ("docs(app-v4): SCA-V4-003 checkpoint K1 accepted (groups 1-2), DECISION-1", 2026-10-03 18:17:56 -0600; it changes only that file) |
| Channel | The owner's chat message to HELP_HUMAN, recorded verbatim in the record above. AK1 did not observe the chat; it relies on that record |
| Earlier directions | "Direction to prepare" (same record), quoting run `APP-V4-DESIGN-PASS-3-20261001`: "Proceed as recommended." (2026-10-01) and "yes, run the closeout." (2026-10-02). They started the undertaking and accepted neither group |

## What the owner had in front of them

As the record states: the package was presented as
`AMENDMENT_PACKET/OWNER_ITEMS.md` (recorded prefix `72c53db208ff42cc`,
committed at `60359d7372`), with the packet files it cites, reviewed by V23
and V23b, and as the review page
https://claude.ai/artifact/A8XbVqJPNoWCHK3RM7YaYJ (Version 1). The record
itself says it "is not a claim that the owner reviewed any file"; this
snapshot makes no such claim either. The page is not a repository file; AK1
has not read it. `DISPATCH.md` row "K1 package" says the page was built from
OWNER_ITEMS.md Q-1…Q-17, with the drafted criteria.

The packet files at `60359d7372` and at this transcription are byte-identical
(each hashed at both; `git diff 60359d7372 HEAD` touches only `BRIEFS.md`,
`DISPATCH.md` and `OWNER_DECISIONS.md` in the run folder):

| Packet file (`AMENDMENT_PACKET/`) | Full sha256 |
|---|---|
| `OWNER_ITEMS.md` | `72c53db208ff42cce271816df9b22898405ff53ca8e5618a1216c21e3877db86` |
| `IMPACT_ASSESSMENT.md` | `46ea15e5b2930c66d97bdc9d10ed5224633e946ba47eb2b2b30897c05f5435f3` |
| `LEDGER.csv` | `e28661cdf3375e156c44dad50c98c6413d56376fa9e0f961e2295472a8a35f12` |
| `LEDGER.md` | `d0d860c88d78322d3af5f7a1c6b52556466d3c4854af0b287997dda81904a0b2` |
| `ARC_EFFECT.md` | `25073317e9cde08ea38d90a37be8823c74bcf32d00d4490fffe9e743320894e7` |
| `BASIS_AMENDMENT.md` | `151bc6fffcac482f6f8e77bf3d7b2822ec65f94012e0b66720f14644efbe35bf` |
| `Amendment_Actions.draft.csv` | `9b7c2ce8fbf97ec0cf829c5024e03d19b4117c1ca50abaea4ec0b2c340346d1c` |
| `SOW_REVISIONS_A.md` | `42c9167aadf8f0f88cc42b6e746af221140c2b7a00b7feaca552692e0cc7fc07` |
| `SOW_REVISIONS_B.md` | `d7b5cb2422cfdc69755e582b920351dccfced4d8871dc722f87ada48cfbb94df` |

For group 1 the subject is the proposed change and its impact:
IMPACT_ASSESSMENT §§1–9 and 11, the ledger (216 rows; 191 INCLUDE, 10
DEFER, 15 DROP), ARC_EFFECT §§1–3, and the OWNER_ITEMS items listed below.
The last four files of the table are group 2's subject
(`../SCA-V4-003_GROUP-2_2026-10-03/`).

## Timing

The pre-change baseline (node P3, method step 5) completed and was committed
at `eaa6a37730` (2026-10-02 20:55:48 -0600), before the packet was repaired
(`a534a7c36e`), rechecked (`60359d7372`) and presented, and before the act
(`5b16bb6831`, 2026-10-03). Its result: 0 BLOCKER, 35 WARNING, 93 INFO, over
PKG-01, 02, 03, 04, 05, 09 and 10 (32 deliverables). Unlike SCA-V4-002, no
timing disclosure is needed.

## The owner's act (verbatim)

> accept the remaining items as recommended

No correction, exception or rewording was recorded.

## Interpretation (recording role's reading, not owner text)

The record reads "remaining" as all seventeen items, since none had been
answered, and lists the effects as each item's recommendation in OWNER_ITEMS'
quick answer sheet. OWNER_ITEMS itself labels only Q-2 (group 1) and Q-3
(group 2); which other items belong to group 1 is AK1's reading, following
SCA-V4-002's split (scope and dispositions here; exact bytes, route and
register in group 2). For checkpoint group 1 the act accepts:

| Item | Effect |
|---|---|
| Q-1 | Amendment ID `SCA-V4-003`; posture `ACCEPTED_PREDECESSOR` (SCA-V4-002); `_ScopeChange/_LATEST.md` keeps naming `SCA-V4-002_2026-09-29_1901` until group 3 |
| Q-2 | The scope: the ledger's 191 INCLUDE rows (102 ScopeOfWork items in 19 deliverables; 86 register items: 10 new links, 35 mirror groups with 96 rows, 41 statement and notes items; 2 Open_Issues edits; the Change Register entry). All `MODIFY`; nothing added, removed, reclassified, merged or split; no decomposition ID changes |
| Q-4 | The 10 new links (5 held inside SCC-002, 5 admitted); NR-01, NR-02 and NR-04 kept with their sentences; NR-03 (and its mirror R3-01-02-g) dropped |
| Q-5 | The App act control in DEL-01-04 (SC3-01-04-1, replacing SC2-01-04-1), with REQ-008 as adjusted and the drafted OUT-005, AC-008 and VER-008 |
| Q-6 | S-01-2 and S-01-3 included (DEL-03-01 scope additions) |
| Q-7 | S-01-4 held (DEFER) |
| Q-8 | DEL-03-01 keeps custody of FX-PIPE-01 and SH-1; S-01-5 included |
| Q-9 | The four A12-mapping rows held: SC2-04-01-2, R2-04-01-b, S-0502-1, R-0502-2 |
| Q-10 | OI-009 option B: status `RESOLVED_BY_OWNER_DECISION`, with supersession row D-021 |
| Q-11 | The optional items included (SC2-04-01-4, S-02-2, R-02-3, S-03-3, R-03-4, S-03-4, S-04-3, S-11-1, SC3-01-02-10, SC3-01-02-11, SC3-01-05-13, the OI-018 pointer, R3-01-02-d, R3-01-03-f); SC3-02-02-5 and S-0906-4 dropped |
| Q-12 | No basis change: three basis items held, three not needed |
| Q-14 | R-02-4 held (register owners' pass) |
| Q-15 | The receivers sentences P1-06…P1-10, and R22-7's DEL-04-03 sentence and row (R22-7-SoW, R22-7-reg); R22-7-open held with DEL-11-02's owner |
| Q-16 | The SCA-V4-002 effective-state note (BASIS_AMENDMENT C-02), written after this group-1 acceptance |
| Q-17 | The 15 further mirror rows (RP1-MX-0201, -0203, -0403, -0401) |

Check made for this record (script over `LEDGER.csv`): the 191 INCLUDE rows
are exactly the dispositions DECISION-1 accepts. Every DEFER row belongs to a
held item (Q-7, Q-9, Q-12, Q-14, R22-7-open under Q-15), and every DROP row is
one the recommendations drop. No row changes disposition under the act.

**Q-13 is not part of the amendment.** DECISION-1 accepts it "as a separate
act": DEL-01-02, 01-03, 01-04, 01-05, 02-02 and 02-04 move INITIALIZED →
IN_PROGRESS. HELP_HUMAN recorded it in the six `_STATUS.md` files at
`baa6e618d70b229e38a8365786a7818e4a6b9b3f` (after the act, before this
snapshot). It is neither a register action nor bound here; the post-change
audit attributes its effect (16 Check 6 INFO rows → WARNING) to it.

## What this acceptance authorizes and does not authorize

It authorizes group-2 preparation from this snapshot, and the SCA-V4-002
effective-state note (Q-16; BASIS_AMENDMENT C-02). Because the same act also
accepted group 2 (`../SCA-V4-003_GROUP-2_2026-10-03/`), no separate group-2
preparation step follows.

On its own it applies no change to any basis document, the decomposition
package, `Open_Issues.csv`, any `ScopeOfWork.md`, `_CONTEXT.md`, `_STATUS.md`,
`Dependencies.csv`, `_DEPENDENCIES.md` or `_DAG` file, and it does not move
`_ScopeChange/_LATEST.md`.

## Basis

At the transcription (`HEAD` `7fea17baaf1c182a49c11cab458503ab532c9063`,
working tree clean before this node's writes):
- the accepted decomposition
  `_Decomposition/checkpoint_snapshots/GROUP3-20260928T001055Z`, as amended
  by SCA-V4-001 and the accepted predecessor
  `_ScopeChange/SCA-V4-002_2026-09-29_1901/` (named by `_ScopeChange/_LATEST.md`,
  sha256 `2b7938bc82aa9b08a2bd26d7f2c0169c538edb1e6ae5423d5757def968f0c2e1`);
- the accepted graph DAG-003 (`_DAG/_LATEST.md`);
- the pre-change baseline `RUN/BASELINE/` (P3; input manifest
  `INPUT_MANIFEST.sha256`). Since that baseline, the only changes to its
  audited surfaces are the six `_STATUS.md` files of the Q-13 act and one
  Design file outside the baseline's input manifest (DEL-03-04
  `Design/HOST_INTEGRATION_GUIDE.md`, pass-3 closeout commit `a68a9e06e2`);
  no `ScopeOfWork.md`, `Dependencies.csv`, `_DEPENDENCIES.md`, `_Decomposition/`,
  `_DAG/`, `_ScopeChange/` or basis file changed (`git diff --name-only
  eaa6a37730 HEAD`).

Every file this snapshot binds was written before any SCA-V4-003 edit was
applied, and none of them describes a post-application state.
