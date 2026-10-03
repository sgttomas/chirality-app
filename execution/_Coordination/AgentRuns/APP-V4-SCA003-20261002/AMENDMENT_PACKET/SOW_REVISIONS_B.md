# SoW revisions B — SCA-V4-003, node P2-B (PKG-02 … PKG-10)

**Status: PROPOSED (scope-change checkpoint-group-2 preparation). Nothing here
is applied.** Every edit is an exact old → new replacement in one
`ScopeOfWork.md`. It is applied after the owner accepts the amendment, by
`scope-of-work` `MODE=REVISE`, one deliverable per brief, closing with
`MODE=VERIFY` (the route of SCA-V4-001 and SCA-V4-002). PKG-01's blocks
(DEL-01-01 … DEL-01-05) are node P2-A's, in `SOW_REVISIONS_A.md`.

- **Basis:** HEAD `40e04273da` (branch `claude/chirality-app-v4-60-percent-a41fd5`).
  Every "old" block was checked against the current SoW bytes; each prior hash
  in the Summary equals the bytes P1's packet and P3's baseline read
  (`git diff 897a107cc9 40e04273da` touches no `ScopeOfWork.md`). See
  "Mechanical checks" at the end.
- **Scope:** every INCLUDE ScopeOfWork row of [LEDGER.csv](LEDGER.csv) whose
  deliverable is outside PKG-01, including the P1 grounding sentences P1-01,
  P1-02, P1-03 (R22-4 for NR-01, NR-02, NR-04), P1-05 (R20-10), P1-06, P1-07,
  P1-08 and P1-10; plus one block HELP_HUMAN added under design pass 3's R22-7
  (G-0403-03, not in P1's ledger; see "For the ledger"; added to the ledger
  at RP1 as R22-7-SoW, R22-7-reg, R22-7-open).
- **Lifecycle:** DEL-02-02 and DEL-02-04 are INITIALIZED; the other twelve are
  IN_PROGRESS. REVISE admits both; none is CHECKING or ISSUED, so no
  reopening is involved. REVISE runs `STATUS_POLICY=NO_STATUS_TOUCH`; the
  R22-5 lifecycle move (Q-13) is a separate act.
- **Companion files:** [IMPACT_ASSESSMENT.md](IMPACT_ASSESSMENT.md),
  [ARC_EFFECT.md](ARC_EFFECT.md), [OWNER_ITEMS.md](OWNER_ITEMS.md),
  [LEDGER.md](LEDGER.md).

## Reading this file

The conventions are those of SCA-V4-002's `SOW_REVISIONS.md`, which the owner
accepted:

- **Edit IDs** are `G-<deliverable>-<nn>` (the "G" series follows SCA-V4-001's
  `E-` and SCA-V4-002's `F-`). Apply each deliverable's edits in the listed
  order. Within one deliverable no two "old" blocks overlap, and no "old"
  block contains text another block adds.
- **Tokens.** `{AMENDMENT_ID}` is the accepted amendment ID (recommended
  `SCA-V4-003`, Q-1). `{AMENDMENT_SNAPSHOT}` is the accepted group-3 snapshot
  folder name under `projects/chirality-app-v4/execution/_ScopeChange/`. Both
  are filled at application from the accepted records.
- **Amendment reference.** Each revised SoW gains one Axiology `AX-*` line
  naming the amendment, its snapshot, the decisions applied, and the revised,
  added and removed IDs (REVISE step 4). It is the deliverable's last block.
- **No new OUT, AC, VER, REQ or CLM IDs.** One new TBD (DEL-04-01 TBD-005,
  SC2-04-01-3). Nothing is renumbered or removed. No matrix row changes (the
  validator accepts the new TBD unreferenced, as it accepted DEL-04-01
  TBD-004 under SCA-V4-001).
- **Frontmatter is unchanged** in every SoW.
- **Upstream local IDs** are written in the qualified form (`DEL-02-02/REQ-002`),
  as the scope-of-work workflow requires.
- **Conditional.** A block marked with an owner item depends on it. If the
  owner declines the item, drop that block (or the named clause) and the
  matching words of the deliverable's AX line. Blocks for DEFER rows are not
  written (see "Not written").
- **"Outside this undertaking".** Pass-2 wording that named DEL-02-02 and
  DEL-02-04 as "outside this undertaking" is reworded, as the ledger asks
  (SC2-02-01-2, SC2-02-03-6, SC2-04-03-1): both now have Design files (pass 3).
  The phrase is dropped for every receiver, because a contract should not
  carry a statement about which design pass has reached which deliverable.

Decision identities used in the new text:

| Short form here | Full identity in the SoW text | Record |
|---|---|---|
| K1 (K1-1 … K1-4) | `APP-V4-DESIGN-PASS-2-20260930-DECISION-K1` | `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-DESIGN-PASS-2-20260930/OWNER_DECISIONS.md` |
| K3 revised (K-6 … K-10) | `APP-V4-DESIGN-PASS-3-20261001-DECISION-K3` (as revised by the owner the same day) | `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-DESIGN-PASS-3-20261001/OWNER_DECISIONS.md` |
| L (L-2, L-4) | `APP-V4-DESIGN-PASS-3-20261001-DECISION-L` | same record |
| FI DECISION-1 (D2, D3, D4) | `APP-V4-FIRST-INCREMENT-20260928-DECISION-1` | `…/APP-V4-FIRST-INCREMENT-20260928/OWNER_DECISIONS.md` |
| SI DECISION-5 | `APP-V4-SWBPIPE-INTAKE-20260928-DECISION-5` | `…/APP-V4-SWBPIPE-INTAKE-20260928/OWNER_DECISIONS.md` |
| Integrator rulings | "integrator ruling R12-8 of `APP-V4-DESIGN-PASS-2-20260930`"; R18-1, R18-4, R19-7, R20-3 of `APP-V4-DESIGN-PASS-3-20261001` | each run's `R*_RESOLUTIONS.md` |

The pass-2 and pass-3 records use "DECISION-K1", "DECISION-K3" and
"DECISION-L" without a run prefix; the full form follows the pattern the
earlier records use (`APP-V4-FIRST-INCREMENT-20260928-DECISION-1`), and pass-2
C1-B already wrote `APP-V4-DESIGN-PASS-2-20260930-DECISION-K1` in its proposed
text. Each AX line also cites the record path.

## Summary

| Deliverable | Prior SoW sha256 | Lifecycle | Blocks (incl. AX) | Ledger rows carried | Conditional |
|---|---|---|---|---|---|
| DEL-02-01 | `ef360edf28f5f463ae961495e04e566ab9ec9d56c0a4fd4f35e67b87adb82f17` | IN_PROGRESS | 3 | SC2-02-01-1, -2 | — |
| DEL-02-02 | `5814116909db8120c1fe888ba021ca60ad139ea0b36cc89fe7e93ed00235924a` | INITIALIZED | 9 | SC3-02-02-1, -2, -3, -4, -10, -11, -12; P1-03 | P1-03 clause: Q-4 |
| DEL-02-03 | `0006521b9bd96ea7ec98ecc5d9e6db794ecb331440c276006b444e7ee319726d` | IN_PROGRESS | 13 | SC2-02-03-1 … -6; P1-01 | P1-01: Q-4 |
| DEL-02-04 | `3acfaa62a3bbf0038d4f3c94416925bf5ff940bb8771b5454ff1ea80e6e16601` | INITIALIZED | 13 | SC3-02-04-1, -2, -4, -5, -6, -7, -9 | DEL-01-04 clause of -9: Q-4 (NR-4) |
| DEL-03-01 | `9ada531b59a6efc007c273f131a8d51df390994ef5f379b1d523d635d3849449` | IN_PROGRESS | 8 | S-01-1, -2, -3, -5; P1-06 | S-01-2, -3: Q-6; S-01-5: Q-8; P1-06: Q-15 |
| DEL-03-02 | `3560915142ebfbf3fa7197008ea3b0660584665c9d86260b22b550c5c2354d0f` | IN_PROGRESS | 4 | S-02-1, S-02-2; P1-07 | S-02-2: Q-11; P1-07: Q-15 |
| DEL-03-03 | `93faf918ce5d2d4eb14f0ecd1b20831a164a8c55a8b47cad26880818251b1a93` | IN_PROGRESS | 5 | S-03-1 … -5; P1-02, P1-08 | per clause (Q-4, Q-11, Q-15) |
| DEL-03-04 | `895f004e4d0f133798f461d8157ac63fff880da09f471be9bae885fe0cfb7c28` | IN_PROGRESS | 4 | S-04-1, -2, -3 | S-04-3: Q-11 |
| DEL-04-01 | `ac043e54e396f9155e3d1b02d61ca7333350a812c7db3d5bb26c80d6fc3bb875` | IN_PROGRESS | 4 | SC2-04-01-1, -3, -4 | -4: Q-11 |
| DEL-04-02 | `f16ffa8a33cbfb2e78a8e916e90aff9fb44ad20adf94fe61a559a213f5564460` | IN_PROGRESS | 2 | SC2-04-02-1 | — |
| DEL-04-03 | `ceecddbb67a86f744b413bb08b08c27017a82ebee8500f7600faf8d880fbaa47` | IN_PROGRESS | 6 | SC2-04-03-1, -2, -3; P1-05; R22-7 (added) | P1-05: Q-4; R22-7: owner, new item |
| DEL-05-01 | `9b2379a14e2c9da4310f62e72d83a6e7506ef37f70c4a38b41d76908bca985ed` | IN_PROGRESS | 4 | S-0501-1; P1-10 | P1-10: Q-15 |
| DEL-09-06 | `287d47a1260e7433c3f16578c67345d067472165421c65848bd15e44d92a7923` | IN_PROGRESS | 5 | S-0906-1, -2, -3 | — |
| DEL-09-09 | `e887a579f75335aa91b59ae195053eabae81ce031fe91136df5c81df2297e53a` | IN_PROGRESS | 4 | S-0909-1, -2 | — |
| **Total** | | | **84** | **57 ledger rows + 1 R22-7 item** | |

The 84 blocks include 14 amendment-reference AX lines. DEL-05-02 has a
register change only (R-0502-1) and no block; its SoW item S-0502-1 is DEFER
(Q-9).

---

## DEL-02-01 — Portable workflow contract and shared allocation

REVISION_SCOPE: CLM-002 (DEL-01-01 clause; one appended sentence); new AX-007.

#### G-0201-01 · CLM-002, DEL-01-01 clause · SC2-02-01-1
Target: DEL-02-01
Trace: pass-2 C1-A SC2-02-01-1 (text as proposed); WD §4.2.5 HC-7; R14-5; still accurate after pass 3 (HOSTING-v0.9 §8.4; R21-1 availability reading, per LEDGER). Pairs register item R2-02-01-g.
```old
`DEL-01-01` supplies the harness capability inventory and supplied-guidance identity evidence;
```
```new
`DEL-01-01` supplies the harness capability inventory, the capability-group meanings and availability signals to which harness-capability requirements resolve, and supplied-guidance identity evidence; this contract names those requirements;
```

#### G-0201-02 · CLM-002, receivers sentence · SC2-02-01-2
Target: DEL-02-01
Trace: pass-2 C1-A SC2-02-01-2, kept by pass-3 C1-B §5; "outside this undertaking" dropped (see "Reading this file"). Each receiver's own register declares DEL-02-01 upstream (checked by script over the ACTIVE rows): DEP-02-02-014, DEP-02-03-009, DEP-02-04-011, DEP-03-02-027, DEP-03-04-008, DEP-05-01-016, DEP-05-02-005, DEP-08-02-006, DEP-09-02-015, DEP-09-06-025, DEP-10-03-008. Grounds R2-02-01-a…f (six mirrors); the other five are the "outside mirrors noted, not proposed" of pass-2 C1-A (see "Extraction guards").
```old
this contract does not define them. Source: Accepted decomposition, Deliverables.csv corresponding rows, Packages.csv PKG-02 through PKG-05 and Open_Issues.csv OI-001/OI-002.
```
```new
this contract does not define them. This contract is received by `DEL-02-02`, `DEL-02-03`, `DEL-02-04`, `DEL-03-02`, `DEL-03-04`, `DEL-05-01`, `DEL-05-02`, `DEL-08-02`, `DEL-09-02`, `DEL-09-06` and `DEL-10-03`, each of which declares it upstream in its own register. Source: Accepted decomposition, Deliverables.csv corresponding rows, Packages.csv PKG-02 through PKG-05 and Open_Issues.csv OI-001/OI-002.
```

#### G-0201-03 · new AX-007 (amendment reference) · acceptance-conditional
Target: DEL-02-01
```old
Revised: CLM-002. Added: AX-006. Removed: none.
```
```new
Revised: CLM-002. Added: AX-006. Removed: none.
- **AX-007** — Revised under scope-change amendment `{AMENDMENT_ID}` (accepted snapshot `projects/chirality-app-v4/execution/_ScopeChange/{AMENDMENT_SNAPSHOT}`), which carries the contract proposals of the App v4 design passes `APP-V4-DESIGN-PASS-2-20260930` and `APP-V4-DESIGN-PASS-3-20261001` (closeout records under `projects/chirality-app-v4/execution/_Coordination/AgentRuns/`): the harness-capability supply from `DEL-01-01` and the receivers of this contract. Revised: CLM-002. Added: AX-007. Removed: none.
```

---

## DEL-02-02 — Workflow-making workspace and registration

REVISION_SCOPE: CLM-002; CLM-003 (appended sentence); REQ-001 (three
appended sentences); REQ-002 (two added sentences); REQ-003 (last sentence);
REQ-008 (one clause); new AX-005.

#### G-0202-01 · CLM-002, DEL-01-04 sentence · SC3-02-02-4 (part 1)
Target: DEL-02-02
Trace: pass-3 D5 §4 SC3-02-02-4 (text as proposed); K3 K-8; pairs SC3-01-04-2 (P2-A) and register item SC3-02-02-6. Same held arc DEL-02-02 → DEL-01-04 (DEP-02-02-013); no topology change.
```old
and native requests, outcomes, attachments and the draft-UI receiving interface belong to `DEL-01-04`;
```
```new
and native requests, outcomes, attachments, the draft-UI receiving interface and the App act control that captures registration belong to `DEL-01-04`;
```

#### G-0202-02 · CLM-003, appended sentence · SC3-02-02-12
Target: DEL-02-02
Trace: pass-3 C1-B §4.1 SC3-02-02-12 (text as proposed), with "and the run-end line" added: R20-3 makes DEL-02-02 the author of the App-written run-end line "beside its run-start framing, in the same schema" (WR-v0.2 §16.2; RS-v0.9 §4 R3 (c)). Rulings R19-7, R20-3, R20-10, R21-4 (`thread/items/list`, read as "Codex's history", R21-6). Grounds SC3-02-02-9, R3-02-02-a…d and the supplier side of R20-10. Receivers checked: DEP-02-03-010, DEP-01-04-009, DEP-09-06-026 exist; DEL-04-03's row is R20-10 (new held arc, proposed).
```old
while this deliverable owns their standalone workspace join. [B2] rows DEL-02-01 and DEL-02-03.
```
```new
while this deliverable owns their standalone workspace join. For each run `DEL-02-03` starts, this workspace composes the run-start text from the selected registered revision, and the App-written run-end line when a run ends and no run starts with the next turn, records each text's content identity and checks it against Codex's history; the run text and its supply-check record are received by `DEL-02-03`, `DEL-01-04` (turn composition) and `DEL-04-03` (supplied-workflow evidence), and the workspace's draft, registration and selection contract by `DEL-01-04`, `DEL-02-03` and `DEL-09-06`, each of which declares it upstream in its own register. [B2] rows DEL-02-01 and DEL-02-03; integrator rulings R19-7 and R20-3 of `APP-V4-DESIGN-PASS-3-20261001`.
```

#### G-0202-03 · REQ-001, trial sentence · SC3-02-02-1
Target: DEL-02-02
Trace: pass-3 D5 §4 SC3-02-02-1 (text as proposed); K3 K-7 (owner's alternative); WR §4.2; R21-5.
```old
reuse on new inputs, and further refinement. Native inputs remain recognizable
```
```new
reuse on new inputs, and further refinement. A draft is tried out in an ordinary conversation, which is not a run of any workflow identity; only registered revisions run (`APP-V4-DESIGN-PASS-3-20261001-DECISION-K3` K-7). Native inputs remain recognizable
```

#### G-0202-04 · REQ-001, chaining sentence · SC3-02-02-10, P1-03 (second sentence conditional, Q-4)
Target: DEL-02-02
Trace: SC3-02-02-10: pass-3 D5 R2.4 (text as proposed); L L-2; R19-2. P1-03 (R22-4 for NR-04, drafted here): RECOVERY-v0.2 §2 DEF-4 ("End a run", R17-3 operation 2); WR-v0.2 §6 SQ-X ("reconcile at App start … the turns themselves are DEL-01-02's, R17-3"), §16.3 CH-2; R19-2 (a); R20-1. DEL-02-02's SoW names DEL-01-02 0 times today (P1 check); the second sentence grounds NR-04 (new admitted arc DEL-02-02 → DEL-01-02, SCC-free, ARC_EFFECT §1.1). **If the owner drops NR-04 at Q-4, delete the second sentence ("A run in the chain ends … does not define them.") and nothing else.**
```old
and the workflow declaration remains available in the journey. [CLM-001; CLM-002; CLM-003; P1 §§2.1 and 4.1; E1 V4-EXM-10]
```
```new
and the workflow declaration remains available in the journey. Workflows are chained within one conversation, one run at a time: sequentially, the person starting the next after one ends, or on the agent's proposal with the person confirming (`APP-V4-DESIGN-PASS-3-20261001-DECISION-L` L-2). A run in the chain ends only as `DEL-01-02` defines ending a run, distinct from interrupting a turn or stopping Codex, and a registration attempt interrupted by a quit or a loss of the App process is reconciled at App start; this workspace consumes those definitions and that App-start event and does not define them. [CLM-001; CLM-002; CLM-003; P1 §§2.1 and 4.1; E1 V4-EXM-10]
```

#### G-0202-05 · REQ-002, shipped and library workflows · SC3-02-02-11
Target: DEL-02-02
Trace: pass-3 C1-B §4.1 SC3-02-02-11 (text as proposed); L L-4 A (clarified); R19-4; WR §4.6, §4.7. Placed after REQ-002's first sentence so that the rule it qualifies ("a new or changed workflow shall remain a draft…") reads with it. Basis V4-WF-02 is not contradicted (pass-3 C1-B §4.4).
```old
A new or changed workflow shall remain a draft until the person reviews the identified content and explicitly registers it.
```
```new
A new or changed workflow shall remain a draft until the person reviews the identified content and explicitly registers it. Workflows shipped with an App release are registered by the release (origin bundled); a library entry byte-equal to a shipped revision is recognized as that revision; other library content without a registration record is registered in place by the person's act, several entries per act allowed, each entry's bytes bound (`APP-V4-DESIGN-PASS-3-20261001-DECISION-L` L-4).
```

#### G-0202-06 · REQ-002, capture sentence · SC3-02-02-3
Target: DEL-02-02
Trace: pass-3 D5 §4 SC3-02-02-3 (text as proposed); K3 K-8; R17-2; WR §4.3.
```old
Draft creation, successful trial execution or an agent's recommendation shall not stand in for either actual review or explicit registration.
```
```new
Draft creation, successful trial execution or an agent's recommendation shall not stand in for either actual review or explicit registration. Explicit registration is performed by the person through the App act control of `DEL-01-04` and is bound to the exact reviewed content; a draft changed after review needs a new review (`APP-V4-DESIGN-PASS-3-20261001-DECISION-K3` K-8).
```

#### G-0202-07 · REQ-003, last sentence · SC3-02-02-2
Target: DEL-02-02
Trace: pass-3 D5 §4 SC3-02-02-2 (text as proposed); K3 K-6 selected the slot policy the sentence withheld; WR §4.1.
```old
preserve existing content unless the actual disposition authorizes its change; this contract does not select a new overwrite policy.
```
```new
preserve existing content unless the actual disposition authorizes its change. A draft made from a registered workflow registers as a new revision of it; earlier revisions are kept and every run cites the revision it used; a same-name draft with no such origin is refused with a request for a new name; nothing is overwritten (`APP-V4-DESIGN-PASS-3-20261001-DECISION-K3` K-6).
```

#### G-0202-08 · REQ-008, last clause on review/registration · SC3-02-02-4 (part 2)
Target: DEL-02-02
Trace: pass-3 D5 §4 SC3-02-02-4 (text as proposed); REQ-008 must not read as DEL-02-02 constructing the control. The boundary-owner check still resolves: REQ-008 names CLM-004, and DEL-01-04 is named in CLM-002 (G-0202-01).
```old
actual review/registration remains the person's act under CLM-004.
```
```new
actual review/registration remains the person's act under CLM-004, captured by `DEL-01-04`'s App act control (CLM-002).
```

#### G-0202-09 · new AX-005 (amendment reference) · acceptance-conditional
Target: DEL-02-02
```old
Revised: TBD-001 and TBD-002. Added: AX-004. Removed: none.
```
```new
Revised: TBD-001 and TBD-002. Added: AX-004. Removed: none.
- **AX-005** — Revised under scope-change amendment `{AMENDMENT_ID}` (accepted snapshot `projects/chirality-app-v4/execution/_ScopeChange/{AMENDMENT_SNAPSHOT}`), applying `APP-V4-DESIGN-PASS-3-20261001-DECISION-K3` K-6, K-7 and K-8 (as revised by the owner) and `APP-V4-DESIGN-PASS-3-20261001-DECISION-L` L-2 and L-4 (record `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-DESIGN-PASS-3-20261001/OWNER_DECISIONS.md`), with that run's integrator rulings R19-7 and R20-3 on run-start and run-end text. Revised: CLM-002, CLM-003, REQ-001, REQ-002, REQ-003 and REQ-008. Added: AX-005. Removed: none.
```

---

## DEL-02-03 — Workflow execution compatibility and round-trip support

REVISION_SCOPE: Purpose (first sentence); SOW-052 traceability row (local
contribution); CLM-002 (consumption list); CLM-003 (appended sentence);
REQ-002; REQ-007; AC-002; VER-002; VER-006; TBD-006 (appended); new AX-006.

#### G-0203-01 · Purpose, first sentence · SC2-02-03-2 (1 of 5)
Target: DEL-02-03
Trace: pass-2 C1-A SC2-02-03-2 (text as proposed); K1 K1-1. The condition A1-A set ("if the owner confirms R9-1's reading") is met by K1-1 (LEDGER).
```old
makes selected workflow requirements actionable in the current host, requests the human acts its declared checkpoints require and records them only when performed
```
```new
makes selected workflow requirements actionable in the current host, sees that the human acts its declared checkpoints require are requested, and records them only when performed
```

#### G-0203-02 · SOW-052 traceability row, local contribution · SC2-02-03-2 (2 of 5)
Target: DEL-02-03
Trace: as G-0203-01. The ScopeLedger row SOW-052 itself is unchanged (it has no subject; pass-2 C1-A "Basis items").
```old
| SOW-052 | Request each declared checkpoint act despite direct-operation autonomy;
```
```new
| SOW-052 | Each declared checkpoint act is requested despite direct-operation autonomy (in the current phase by the agent, `APP-V4-DESIGN-PASS-2-20260930-DECISION-K1` K1-1);
```

#### G-0203-03 · CLM-002, start of the consumption list · P1-01 · conditional (Q-4, NR-01)
Target: DEL-02-03
Trace: P1-01 (R22-4 for NR-01, drafted here). EXEC-v0.7 §2.7 (run reference tag and look-up, RECOVERY-v0.2 §4.1), AE-6 (DEL-01-02's custody events `observation_lost` / `observation_recovered`, RECOVERY-v0.2 §8.2), RE-4 (recovery as the same run), A-2, A-4; EXEC §9.1 row "Stop operations, observation custody and the run reference tag across restart — DEL-01-02". DEL-02-03's SoW names DEL-01-02 0 times today. Grounds NR-01 (new admitted arc DEL-02-03 → DEL-01-02, SCC-free; ARC_EFFECT §1.1). If the owner drops NR-01, drop this block and "the DEL-01-02 custody inputs" from AX-006.
```old
This slice consumes, and does not define: `DEL-03-02`'s
```
```new
This slice consumes, and does not define: `DEL-01-02`'s custody events (observation lost and recovered, App-restart interruption) and its run-reference tag and look-up, so that a run interrupted by a Codex stop or an App relaunch is recovered as the same run and its checkpoint history is preserved (REQ-002); `DEL-03-02`'s
```

#### G-0203-04 · CLM-002, grant display states · SC2-02-03-3
Target: DEL-02-03
Trace: pass-2 C1-A SC2-02-03-3 (text as proposed); EXEC §4.10, §9.1; AS §12.1. Consumer side of the existing held arc DEL-02-03 → DEL-04-02 (supplier row DEP-04-02-023); grounds R2-02-03-a.
```old
on the external channel, which this slice records (REQ-002, REQ-003);
```
```new
on the external channel, which this slice records (REQ-002, REQ-003); `DEL-04-02`'s grant display states (including *set by person, not yet confirmed*, *unconfirmed* and *refused*), for recording A12 checkpoints (REQ-002, REQ-003);
```

#### G-0203-05 · CLM-002, DEL-01-04 clause · SC2-02-03-5
Target: DEL-02-03
Trace: pass-2 C1-A SC2-02-03-5 (text as proposed); K1 K1-4; made true by SC3-01-04-1 (P2-A). Pairs register item R2-02-03-j. "which await that later undertaking" is kept: the control is designed (pass 3) but not built.
```old
and `DEL-01-04`'s App act control and person identity, for the App-side positive capture fixtures
```
```new
and `DEL-01-04`'s App act control, which records the person's identity as `APP-V4-DESIGN-PASS-2-20260930-DECISION-K1` K1-4 sets it, for the App-side positive capture fixtures
```

#### G-0203-06 · CLM-003, receivers sentence · SC2-02-03-6
Target: DEL-02-03
Trace: pass-2 C1-A SC2-02-03-6, kept by pass-3 C1-B §5; "outside this undertaking" dropped. Each receiver declares DEL-02-03 upstream (checked): DEP-02-01-026, DEP-02-02-015, DEP-03-03-014, DEP-03-04-009, DEP-04-02-017, DEP-04-03-025, DEP-05-01-017, DEP-05-02-020, DEP-09-02-017, DEP-09-06-013, DEP-09-09-023, DEP-10-03-009. Grounds R2-02-03-b…i. DEL-09-06 is added to pass 2's list: it consumes this slice (DEP-09-06-013) and CLM-003 already names it as owner of the joined witness.
```old
Workflow compatibility supplies neither another App engine nor a presumed common service. Source: G3 Deliverables.csv DEL-05-01/DEL-09-06;
```
```new
Workflow compatibility supplies neither another App engine nor a presumed common service. This slice's report, recording meanings and transfer contract are received by `DEL-02-01`, `DEL-02-02`, `DEL-03-03`, `DEL-03-04`, `DEL-04-02`, `DEL-04-03`, `DEL-05-01`, `DEL-05-02`, `DEL-09-02`, `DEL-09-06`, `DEL-09-09` and `DEL-10-03`, each of which declares it upstream in its own register. Source: G3 Deliverables.csv DEL-05-01/DEL-09-06;
```

#### G-0203-07 · REQ-002 · SC2-02-03-2 (3 of 5)
Target: DEL-02-03
Trace: pass-2 C1-A SC2-02-03-2 (text as proposed); K1 K1-1; EXEC RC-1…RC-6; R18-5 (the person opening the act control from an arrival row is not the product reacting).
```old
At a declared checkpoint, request the required human act and record it as done only when the person performs it, even where the applicable operation autonomy otherwise allows direct application.
```
```new
At a declared checkpoint, the required human act is requested and is recorded as done only when the person performs it, even where the applicable operation autonomy otherwise allows direct application. In the current phase the agent carrying out the workflow requests the act; the App and a host's embedded loop give the agent the checkpoint, offer the means to act and record the arrival, the request where it can be identified and the act, and neither requests in the agent's place nor otherwise reacts to the arrival (`APP-V4-DESIGN-PASS-2-20260930-DECISION-K1` K1-1).
```

#### G-0203-08 · REQ-007 · SC2-02-03-1 (1 of 2)
Target: DEL-02-03
Trace: pass-2 C1-A SC2-02-03-1; TBD-006 was added by SCA-V4-001.
```old
Carry open decisions at their separate points of need in TBD-001 through TBD-005.
```
```new
Carry open decisions at their separate points of need in TBD-001 through TBD-006.
```

#### G-0203-09 · AC-002 · SC2-02-03-2 (4 of 5)
Target: DEL-02-03
```old
- **AC-002** — A declared checkpoint requests its named human act, and
```
```new
- **AC-002** — A declared checkpoint's named human act is requested, and
```

#### G-0203-10 · VER-002 · SC2-02-03-2 (5 of 5)
Target: DEL-02-03
```old
Inspect the request, the recorded act state and the later act evidence;
```
```new
Inspect the request where it can be identified, the recorded act state and the later act evidence;
```

#### G-0203-11 · VER-006 · SC2-02-03-1 (2 of 2)
Target: DEL-02-03
```old
compare TBD-001 through TBD-005 and DEP-001
```
```new
compare TBD-001 through TBD-006 and DEP-001
```

#### G-0203-12 · TBD-006, appended · SC2-02-03-4
Target: DEL-02-03
Trace: pass-2 C1-A SC2-02-03-4 (text as proposed); K1 K1-2, K1-3; EXEC SP-6, SP-6F, JA-1; WD FA-1. `DEL-02-01` is already a named supplier of this slice (CLM-001; DEP-02-03-009): no new arc.
```old
with SWBPIPE's answer to relay SQ-02 (no host-held route planned) as an input.
```
```new
with SWBPIPE's answer to relay SQ-02 (no host-held route planned) as an input. In the current phase an earlier act of the required kind whose content is still current counts toward an arrival and is cited with its time, and several acts may answer one arrival together (`APP-V4-DESIGN-PASS-2-20260930-DECISION-K1` K1-2, K1-3). A workflow that takes up the governance phase may require a fresh act instead, declared through the portable declaration (`DEL-02-01`).
```

#### G-0203-13 · new AX-006 (amendment reference) · acceptance-conditional
Target: DEL-02-03
```old
inputs it consumes to this amendment. Revised: CLM-002. Added: AX-005. Removed: none.
```
```new
inputs it consumes to this amendment. Revised: CLM-002. Added: AX-005. Removed: none.
- **AX-006** — Revised under scope-change amendment `{AMENDMENT_ID}` (accepted snapshot `projects/chirality-app-v4/execution/_ScopeChange/{AMENDMENT_SNAPSHOT}`), applying `APP-V4-DESIGN-PASS-2-20260930-DECISION-K1` K1-1 to K1-4 (record `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-DESIGN-PASS-2-20260930/OWNER_DECISIONS.md`), with the grant-display, DEL-01-02 custody and receiver statements of the design passes' closeouts. Revised: the Purpose first sentence, the SOW-052 traceability row, CLM-002, CLM-003, REQ-002, REQ-007, AC-002, VER-002, VER-006 and TBD-006. Added: AX-006. Removed: none.
```

---

## DEL-02-04 — Additive role selection and supply

REVISION_SCOPE: CLM-002 (appended sentence); REQ-001; REQ-002; REQ-003;
AC-001; AC-003; Axiology open-matter table rows OI-001, OI-002, OI-012,
OI-017, OI-018; TBD-001; new AX-005.

#### G-0204-01 · CLM-002, receivers sentence · SC3-02-04-9 (DEL-01-04 clause conditional, Q-4 NR-4)
Target: DEL-02-04
Trace: pass-3 C1-B §4.1 SC3-02-04-9; the bracketed clause is included because R22-1 adopted NR-4 (LEDGER). Receivers: DEP-03-04-010, DEP-10-03-010 (checked); DEL-01-04's row is NR-4 (new held arc, proposed). Grounds R3-02-04-a…c. If the owner drops NR-4, delete ", and its role list and guidance-changed signal by `DEL-01-04`".
```old
this deliverable supplies their role-specific evidence rather than owning those acts or systems.
```
```new
this deliverable supplies their role-specific evidence rather than owning those acts or systems. Its role-guidance semantics are received by `DEL-03-04`, its supply obligations by `DEL-10-03`, and its role list and guidance-changed signal by `DEL-01-04`, each of which declares it upstream in its own register.
```

#### G-0204-02 · REQ-001, no-role and fixed-role sentences · SC3-02-04-5 (1 of 2)
Target: DEL-02-04
Trace: pass-3 D6 §5 SC3-02-04-5 as extended at D6 R2.3 (text as proposed); R17-9; L L-2; R19-3.
```old
a domain-specific expression such as SWB Piping Designer does not create a fifth durable role.
```
```new
a domain-specific expression such as SWB Piping Designer does not create a fifth durable role. A conversation may also run with no role; this is not a fifth role. A new conversation's preselection follows the App role set's default as data, shown and clearable. A conversation's role is fixed for its life; another role is a new conversation (`APP-V4-DESIGN-PASS-3-20261001-DECISION-L` L-2).
```

#### G-0204-03 · REQ-002, child roles · SC3-02-04-6
Target: DEL-02-04
Trace: pass-3 D6 §5 SC3-02-04-6 as changed at D6 R2.3 (text as proposed); R17-9 as amended by R18-4 (OBS-2 O-4a). REQ-002 rather than CLM-004 because it is a supply obligation.
```old
Retain the required role-configuration behavior without substituting a historical Root product default, old packaging location or prior implementation as present v4 authority.
```
```new
Retain the required role-configuration behavior without substituting a historical Root product default, old packaging location or prior implementation as present v4 authority. Delegated children receive the product guidance and their role through the supplier's native agent-role configuration where the supplier supports it, added without replacing the person's own definitions; a child spawned without a role type has unknown guidance, and the account says so (integrator ruling R18-4 of `APP-V4-DESIGN-PASS-3-20261001`).
```

#### G-0204-04 · REQ-003, K-10 · SC3-02-04-4 (1 of 2)
Target: DEL-02-04
Trace: pass-3 D6 §5 SC3-02-04-4 (text as proposed); K3 K-10 as revised (the owner withdrew the override alternative). Duplicate in substance of SC3-01-03-5 in DEL-01-03 (P2-A); both are kept (LEDGER).
```old
Preserve the required native delegation capability for roles whose applicable boundaries permit it.
```
```new
Preserve the required native delegation capability for roles whose applicable boundaries permit it. The task role's guidance states that a task agent does not delegate, presented as "stated, not enforced"; any delegation a task agent makes is recorded and shown; the App does not override the person's Codex configuration to enforce it (`APP-V4-DESIGN-PASS-3-20261001-DECISION-K3` K-10).
```

#### G-0204-05 · AC-001 · SC3-02-04-5 (2 of 2)
Target: DEL-02-04
```old
A domain-specific agent expression retains the applicable standing role instead of adding another. Verify with VER-001.
```
```new
A domain-specific agent expression retains the applicable standing role instead of adding another. A conversation with no role is offered and is not a fifth role; the preselection is shown and clearable; the role stays fixed for the conversation's life. Verify with VER-001.
```

#### G-0204-06 · AC-003 · SC3-02-04-4 (2 of 2)
Target: DEL-02-04
```old
The role restriction does not remove authorized native delegation from the other roles. Verify with VER-003.
```
```new
The role restriction does not remove authorized native delegation from the other roles. The task limit is presented as "stated, not enforced", any delegation a task agent makes is recorded and shown, and the person's Codex configuration is not overridden to enforce it. Verify with VER-003.
```

#### G-0204-07 · open-matter table, OI-001 row · SC3-02-04-1 (1 of 4)
Target: DEL-02-04
Trace: pass-3 D6 §5 SC3-02-04-1; FI DECISION-1 D2/D3 (S1-C §B.1; S1-F §4.2). Owner column unchanged.
```old
| Role selection/supply does not decide an always-reserved act list; policy is carried through App DEL-04-01. |
```
```new
| Role selection/supply does not decide an always-reserved act list; policy is carried through App DEL-04-01. Ruled for the App's contracts by `APP-V4-FIRST-INCREMENT-20260928-DECISION-1` D2; operation-specific additions remain open (OI-021). |
```

#### G-0204-08 · open-matter table, OI-002 row · SC3-02-04-1 (2 of 4)
Target: DEL-02-04
```old
| No historical App/host classifier default is adopted through role configuration. |
```
```new
| No historical App/host classifier default is adopted through role configuration. Ruled by `APP-V4-FIRST-INCREMENT-20260928-DECISION-1` D3: in the App, routine tool-permission and sandbox modes remain the user's own Codex setting. |
```

#### G-0204-09 · open-matter table, OI-012 row · SC3-02-04-1 (3 of 4)
Target: DEL-02-04
Trace: FI DECISION-1 D4; DEL-01-01 HOSTING U-01 (qualification separate), as D6 states.
```old
| Use the identified supplier contract when exercising actual supply; historical version examples are not v4 pins. |
```
```new
| `APP-V4-FIRST-INCREMENT-20260928-DECISION-1` D4 selected Codex 0.158.0 as the definition and generation pin; the pin used for qualification is separate (App DEL-01-01). Historical version examples are not v4 pins. |
```

#### G-0204-10 · open-matter table, OI-017 row · SC3-02-04-1 (4 of 4)
Target: DEL-02-04
Trace: `_Decomposition/Open_Issues.csv` OI-017 Status `RESOLVED_FOR_CURRENT_DEFINITION_RUN`, source `_Coordination/CURRENT_EXECUTION_BASIS.md` (checked).
```old
| Reading a manual or this contract does not perform project adoption. |
```
```new
| Resolved for the current definition run (`projects/chirality-app-v4/execution/_Coordination/CURRENT_EXECUTION_BASIS.md`); reading a manual or this contract does not perform project adoption. |
```

#### G-0204-11 · open-matter table, OI-018 row · SC3-02-04-2
Target: DEL-02-04
Trace: pass-3 D6 §5 SC3-02-04-2 as changed at D6 R2.3 (text as proposed); K3 K-9 as amended by L L-2 (R19-3); pairs register item R3-02-04-d and the optional OI-018 pointer (OI-018-ptr). OI-018 stays OPEN for hosts.
```old
| Preserve source/supply evidence without inventing a new precedence tree or distributing changed instructions prematurely. |
```
```new
| Answered for the App by `APP-V4-DESIGN-PASS-3-20261001-DECISION-K3` K-9 as amended by `APP-V4-DESIGN-PASS-3-20261001-DECISION-L` L-2: the App ships default role guidance, seeds an editable copy in its own data folder, applies a change to new conversations (an open conversation shows that its role's guidance changed), and records the guidance by content. Host distribution remains open with the same owners; preserve source/supply evidence without inventing a new precedence tree. |
```

#### G-0204-12 · TBD-001, appended · SC3-02-04-7
Target: DEL-02-04
Trace: pass-3 D6 §5 SC3-02-04-7 as amended for L-2 (C1-B); SCA-V4-002 precedent (DEL-02-02 TBD-002).
```old
receiving owners decide and evidence adoption through PKG-11. [G; A App DEL-11-02; E decision 07]
```
```new
receiving owners decide and evidence adoption through PKG-11. OI-018 is answered for the App by `APP-V4-DESIGN-PASS-3-20261001-DECISION-K3` K-9 as amended by `APP-V4-DESIGN-PASS-3-20261001-DECISION-L` L-2 and stays open for hosts; for OI-012, Codex 0.158.0 is the definition and generation pin (`APP-V4-FIRST-INCREMENT-20260928-DECISION-1` D4). [G; A App DEL-11-02; E decision 07]
```

#### G-0204-13 · new AX-005 (amendment reference) · acceptance-conditional
Target: DEL-02-04
```old
PKG-04 owns the applicable act/policy contract. [C V4-AUT-03/04; CLM-002]
```
```new
PKG-04 owns the applicable act/policy contract. [C V4-AUT-03/04; CLM-002]
- **AX-005** — Revised under scope-change amendment `{AMENDMENT_ID}` (accepted snapshot `projects/chirality-app-v4/execution/_ScopeChange/{AMENDMENT_SNAPSHOT}`), applying `APP-V4-DESIGN-PASS-3-20261001-DECISION-K3` K-9 and K-10 (as revised by the owner) and `APP-V4-DESIGN-PASS-3-20261001-DECISION-L` L-2 (record `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-DESIGN-PASS-3-20261001/OWNER_DECISIONS.md`), that run's integrator ruling R18-4, and `APP-V4-FIRST-INCREMENT-20260928-DECISION-1` D2, D3 and D4 (record `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-FIRST-INCREMENT-20260928/OWNER_DECISIONS.md`). Revised: CLM-002, REQ-001, REQ-002, REQ-003, AC-001, AC-003, the open-matter table rows OI-001, OI-002, OI-012, OI-017 and OI-018, and TBD-001. Added: AX-005. Removed: none.
```

---

## DEL-03-01 — Capability catalog and read-basis contract

REVISION_SCOPE: CLM-002 (appended receivers sentence); OUT-001 (opening,
element list, last sentence); OUT-003 (appended sentence); REQ-001
(appended sentence); REQ-002 (element list and sources); new AX-005.

#### G-0301-01 · CLM-002, receivers sentence · P1-06 · conditional (Q-15)
Target: DEL-03-01
Trace: P1-06 (drafted here). The eleven consumers whose UPSTREAM rows target DEL-03-01 (R-01-1; pass-2 C1-B §1.5), each checked ACTIVE: DEP-02-01-017, DEP-02-03-011, DEP-03-03-006, DEP-03-04-005, DEP-04-02-016, DEP-04-03-023, DEP-05-01-014, DEP-05-02-006, DEP-09-06-027, DEP-09-09-007, DEP-10-03-011. What each receives is taken from its row's Statement. `DEL-03-02` is already named as a receiver in CLM-002.
```old
(human-act evidence and lapse state). Sources: D named Deliverables.csv rows;
```
```new
(human-act evidence and lapse state). This contract is also received by App v4 `DEL-02-01` (tool descriptors for required-tool declarations), `DEL-02-03` (capability semantics for required-tool checks), `DEL-03-03` and `DEL-03-04` (catalog/read-basis definitions), `DEL-04-02` (read-basis and standing facets), `DEL-04-03` (subject content identities and method designations), `DEL-05-01` (schemas and catalog identity for loop validation), `DEL-05-02` (panel receiving), `DEL-09-06` (the connected activity), `DEL-09-09` (the external trace) and `DEL-10-03` (the shared account), each of which declares it upstream in its own register. Sources: D named Deliverables.csv rows;
```

#### G-0301-02 · OUT-001, opening · S-01-3 (1 of 2) · conditional (Q-6)
Target: DEL-03-01
Trace: pass-2 C1-B S-01-3 (text as proposed); C §2.1 EI-1…EI-5, CI-4; DEP-05-01-014 "catalog identity". Scope addition by owning decision (Q-6).
```old
- **OUT-001** — CONFIG: catalog and read-basis schemas expressing stable operation identity/version,
```
```new
- **OUT-001** — CONFIG: catalog and read-basis schemas expressing the identity of the catalog edition a consumer discovered and the event by which a host reports a new edition, stable operation identity/version,
```

#### G-0301-03 · OUT-001, element list · S-01-2 (1 of 2) · conditional (Q-6)
Target: DEL-03-01
Trace: pass-2 C1-B S-01-2 ("OUT-001 gains the same two items" as REQ-002); C §3.4, §4.1; LOOP §5.3. Scope addition by owning decision (Q-6).
```old
meaningful errors and adopted human-act/autonomy class; every read describes
```
```new
meaningful errors and adopted human-act/autonomy class, and, for an entry through which a host's embedded agent reaches a network destination, the host-declared external-contact declaration (destination category and form), with the host's destination-request entry and its non-success results for a destination that is not allowed; every read describes
```

#### G-0301-04 · OUT-001, last sentence · S-01-1
Target: DEL-03-01
Trace: pass-2 C1-B S-01-1 (text as proposed); R12-2. Clarification, no scope change.
```old
The schema contract supplies the later-action basis reference meaning without choosing an unsupported wire representation.
```
```new
The schema contract supplies the later-action basis reference meaning without choosing an unsupported wire representation. Schemas may be written as conformance fixtures of these meanings (for example JSON Schema with valid and invalid instances); such a fixture selects no host or supplier wire field, transport, identity algorithm or placement (TBD-003; OI-014).
```

#### G-0301-05 · OUT-003, appended sentence · S-01-5 · conditional (Q-8)
Target: DEL-03-01
Trace: pass-2 C1-B S-01-5 (wording as proposed, set as its own sentence); C §10 (FX-PIPE-01), §10.8 (SH-1); R12-4. Applies only if the owner keeps custody with DEL-03-01 (Q-8, recommended); otherwise drop.
```old
label contract evidence separately from a host-supplied integrated witness.
```
```new
label contract evidence separately from a host-supplied integrated witness. The fixtures include the shared fixture catalogue FX-PIPE-01 and the simulated host SH-1 that other deliverables cite (an integration assignment); their results are test-double evidence.
```

#### G-0301-06 · REQ-001, appended sentence · S-01-3 (2 of 2) · conditional (Q-6)
Target: DEL-03-01
```old
Equal UI gestures are unnecessary. Sources: SOW-018/SOW-067/SOW-068;
```
```new
Equal UI gestures are unnecessary. Consumers resolve operation references against an identified catalog edition. Sources: SOW-018/SOW-067/SOW-068;
```

#### G-0301-07 · REQ-002, element list and sources · S-01-2 (2 of 2) · conditional (Q-6)
Target: DEL-03-01
Trace: pass-2 C1-B S-01-2 (REQ-002 text as proposed); SI DECISION-5; PRD V4-HOST-02 and ARCHITECTURE V4-ARC-12 as amended by SCA-V4-001 (both checked to state the allowed-destinations rule). The source citation is added to REQ-002's Sources and to AX-005 (S-01-2's "new AX entry").
```old
human-act/autonomy class drawn from the adopted operation policy; and host-declared exposure per consumer surface, independent of class.
```
```new
human-act/autonomy class drawn from the adopted operation policy; host-declared exposure per consumer surface, independent of class; and, for an entry through which a host's embedded agent reaches a network destination, a host-declared external-contact declaration (destination category and form). The catalog also carries the host's destination-request entry, through which its agent asks the person for a destination, and the non-success results for a destination that is not allowed (`APP-V4-SWBPIPE-INTAKE-20260928-DECISION-5`; P V4-HOST-02 and A V4-ARC-12 as amended by `SCA-V4-001`).
```

#### G-0301-08 · new AX-005 (amendment reference) · acceptance-conditional
Target: DEL-03-01
Trace: if Q-6 is declined, remove `APP-V4-SWBPIPE-INTAKE-20260928-DECISION-5`'s clause, OUT-001's opening and REQ-001/REQ-002 from the lists; if Q-8 is declined, OUT-003; if Q-15 is declined, CLM-002.
```old
Revised: OUT-001, CLM-002, REQ-002, REQ-004, VER-004 and TBD-001. Added: AX-004. Removed: none.
```
```new
Revised: OUT-001, CLM-002, REQ-002, REQ-004, VER-004 and TBD-001. Added: AX-004. Removed: none.
- **AX-005** — Revised under scope-change amendment `{AMENDMENT_ID}` (accepted snapshot `projects/chirality-app-v4/execution/_ScopeChange/{AMENDMENT_SNAPSHOT}`), applying `APP-V4-SWBPIPE-INTAKE-20260928-DECISION-5` (record `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-SWBPIPE-INTAKE-20260928/OWNER_DECISIONS.md`) with PRD V4-HOST-02 and ARCHITECTURE V4-ARC-12 as amended by `SCA-V4-001` (destination elements), the catalog-edition identity, the owner's custody of the shared fixtures, the conformance-fixture clarification of integrator ruling R12-2 of `APP-V4-DESIGN-PASS-2-20260930`, and the receivers of this contract. Revised: CLM-002, OUT-001, OUT-003, REQ-001 and REQ-002. Added: AX-005. Removed: none.
```

---

## DEL-03-02 — Proposal, validation and outcome contract

REVISION_SCOPE: OUT-001 (last sentence); CLM-004 (two appended sentences);
new AX-005.

#### G-0302-01 · OUT-001, last sentence · S-02-1
Target: DEL-03-02
Trace: pass-2 C1-B S-02-1 (text as proposed); R12-2.
```old
do not select unagreed wire formats or storage topology.
```
```new
do not select unagreed wire formats or storage topology. Schemas may be written as conformance fixtures of these meanings; such a fixture selects no wire format, storage topology or placement (TBD-002; OI-014).
```

#### G-0302-02 · CLM-004, receivers sentence · P1-07 · conditional (Q-15)
Target: DEL-03-02
Trace: P1-07 (drafted here). Consumers checked ACTIVE: DEP-02-01-029, DEP-02-03-025, DEP-05-01-015, DEP-05-02-007, DEP-09-06-028, DEP-10-03-012 (R-02-2). `DEL-02-01` was already named (CLM-002 or CLM-003 by pass 2's count, "names 1 of 6"); it is listed for completeness of the sentence. Grounds R-02-2.
```old
This contract supplies proposal origin, basis and outcome semantics to those interfaces.
```
```new
This contract supplies proposal origin, basis and outcome semantics to those interfaces. Its proposal, validation and outcome meanings are also received by `DEL-02-01` and `DEL-02-03` (item dispositions and content identities for checkpoint subjects), `DEL-05-01` (the loop boundary), `DEL-05-02` (panel receiving), `DEL-09-06` (the connected activity) and `DEL-10-03` (the shared account), each of which declares it upstream in its own register.
```

#### G-0302-03 · CLM-004, consumption of DEL-04-02 · S-02-2 · conditional (Q-11)
Target: DEL-03-02
Trace: pass-2 C1-B S-02-2 (text as proposed); P §3.3, §13; consumer side of the held arc DEL-03-02 → DEL-04-02 (supplier row DEP-04-02-021); grounds R-02-3. No topology change.
```old
Sources: DELIVERABLES rows DEL-04-01, DEL-04-02 and DEL-04-03; ISSUES OI-001/OI-002;
```
```new
It consumes `DEL-04-02`'s visible autonomy state (grant display states, grant value and scope, settings version identities) for origin and standing at drafting. Sources: DELIVERABLES rows DEL-04-01, DEL-04-02 and DEL-04-03; ISSUES OI-001/OI-002;
```

#### G-0302-04 · new AX-005 (amendment reference) · acceptance-conditional
Target: DEL-03-02
```old
Revised: OUT-001, CLM-003, REQ-004, REQ-008, REQ-012, AC-009, AC-013 and TBD-001. Added: AX-004. Removed: none.
```
```new
Revised: OUT-001, CLM-003, REQ-004, REQ-008, REQ-012, AC-009, AC-013 and TBD-001. Added: AX-004. Removed: none.
- **AX-005** — Revised under scope-change amendment `{AMENDMENT_ID}` (accepted snapshot `projects/chirality-app-v4/execution/_ScopeChange/{AMENDMENT_SNAPSHOT}`), applying the conformance-fixture clarification of integrator ruling R12-2 of `APP-V4-DESIGN-PASS-2-20260930` (record `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-DESIGN-PASS-2-20260930/R12_RESOLUTIONS.md`), with the visible-autonomy input and the receivers of this contract from that run's closeout. Revised: OUT-001 and CLM-004. Added: AX-005. Removed: none.
```

---

## DEL-03-03 — Local external-agent receiving adapter

REVISION_SCOPE: CLM-002 (consumption sentence); CLM-003 (appended
receivers sentence); REQ-003 (current-phase sentence); VER-002 (second
sentence); new AX-006.

#### G-0303-01 · CLM-002, consumption sentence · S-03-2, S-03-3, S-03-5, P1-02 (clauses conditional)
Target: DEL-03-03
Trace: one block because the four items edit one sentence. Clauses: (a) **P1-02** (R22-4 for NR-02, drafted here; conditional Q-4): ADAPTER-v0.7 PI-6 (App restart during a submission: in-flight items *outcome unknown*, limit "App-restart interruption", from RECOVERY-v0.2 `observation_lost` and `app_restart_interruption`, §8.2), CT-9, CT-10, XF-41; ADAPTER §1 row "custody of execution and requests across a stop, a supplier exit or a relaunch is DEL-01-02's". DEL-03-03's SoW names DEL-01-02 0 times; grounds NR-02 (new admitted arc DEL-03-03 → DEL-01-02, SCC-free). (b) **S-03-3** (optional, Q-11): pass-2 C1-B text; consumer side of held arcs (supplier rows DEP-04-02-022, DEP-02-01-027); grounds R-03-4. (c) **S-03-5**: pass-2 C1-B text; ADAPTER §3.5, R12-4; pairs R-03-6. (d) **S-03-2**: pass-2 C1-B text; EXEC PH-3 (the required-tool check is in force in both phases); pairs R-03-3. If an item is declined, delete only its clause.
```old
This adapter consumes these definitions with adopted PKG-04 operation-policy distinctions, App `DEL-01-01`'s supplier MCP/dynamic-tool surfaces and channel-status facts at the definition pin 0.158.0 (`APP-V4-FIRST-INCREMENT-20260928-DECISION-1` D4), and App `DEL-02-03`'s checkpoint statement for the current phase and, for the governance phase, its hold machine, hold-support values and required-tool check;
```
```new
This adapter consumes these definitions with adopted PKG-04 operation-policy distinctions, App `DEL-04-02`'s visible autonomy state (grant display states and settings references) and, for the governance phase, App `DEL-02-01`'s declared checkpoint constraints, App `DEL-01-02`'s in-flight item state and relaunch fact for an external request whose Codex process stopped or whose App relaunched during submission, App `DEL-01-01`'s supplier MCP, dynamic-tool and command-execution surfaces and channel-status facts at the definition pin 0.158.0 (`APP-V4-FIRST-INCREMENT-20260928-DECISION-1` D4), and App `DEL-02-03`'s checkpoint statement and required-tool check for the current phase and, for the governance phase, its hold machine and hold-support values;
```

#### G-0303-02 · CLM-003, receivers sentence · P1-08 · conditional (Q-15)
Target: DEL-03-03
Trace: P1-08 (drafted here). Consumers checked ACTIVE: DEP-03-04-007, DEP-04-03-026, DEP-09-06-029 (R-03-1); DEL-02-03 (DEP-02-03-026) is already named in CLM-002 through its checkpoint statement and is not repeated. Grounds R-03-1.
```old
A host-owned acceptance surface is not the actor of the person's acceptance.
```
```new
A host-owned acceptance surface is not the actor of the person's acceptance. This adapter's external-agent receiving definition and evidence limits are received by App `DEL-03-04` (the integration guide), its external dispatch entries by `DEL-04-03`, and its external-receiving meanings by `DEL-09-06`, each of which declares it upstream in its own register.
```

#### G-0303-03 · REQ-003, current-phase sentence · S-03-4 · conditional (Q-11)
Target: DEL-03-03
Trace: pass-2 C1-B S-03-4 (text as proposed); amended V4-HI-42; K1 K1-1; ADAPTER §7.7.
```old
In the current phase a checkpoint on this channel is plan guidance: its act is recorded only when the person performs it and the App claims no hold (`APP-V4-SWBPIPE-INTAKE-20260928-DECISION-4` D4-1);
```
```new
In the current phase a checkpoint on this channel is plan guidance: the agent carrying out the workflow requests its act, the App records the request where it can identify it and the act only when the person performs it, and the App claims no hold (`APP-V4-SWBPIPE-INTAKE-20260928-DECISION-4` D4-1; `APP-V4-DESIGN-PASS-2-20260930-DECISION-K1` K1-1);
```

#### G-0303-04 · VER-002, second sentence · S-03-1
Target: DEL-03-03
Trace: pass-2 C1-B S-03-1 (text as proposed); aligns VER-002 with AC-002 as revised under SCA-V4-001.
```old
Confirm no host call while disabled, truthful unavailability and no implicit remote/data/autonomy expansion.
```
```new
Confirm no App-originated host request while disabled, that the host's refusal is recorded as the authoritative off for agent-originated requests, truthful unavailability and no implicit remote/data/autonomy expansion.
```

#### G-0303-05 · new AX-006 (amendment reference) · acceptance-conditional
Target: DEL-03-03
```old
Revised: CLM-002 and REQ-005. Added: AX-005. Removed: none.
```
```new
Revised: CLM-002 and REQ-005. Added: AX-005. Removed: none.
- **AX-006** — Revised under scope-change amendment `{AMENDMENT_ID}` (accepted snapshot `projects/chirality-app-v4/execution/_ScopeChange/{AMENDMENT_SNAPSHOT}`), applying `APP-V4-DESIGN-PASS-2-20260930-DECISION-K1` K1-1 (record `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-DESIGN-PASS-2-20260930/OWNER_DECISIONS.md`), with the consumption, correction and receiver statements of the design passes' closeouts. Revised: CLM-002, CLM-003, REQ-003 and VER-002. Added: AX-006. Removed: none.
```

---

## DEL-03-04 — Host boundary and integration guide

REVISION_SCOPE: CLM-003 (last sentence, two parts); receiving map row
"Autonomy", column 4; new AX-005.

#### G-0304-01 · CLM-003, DEL-01-01 part · S-04-1
Target: DEL-03-04
Trace: pass-2 C1-B S-04-1; GUIDE §2.11. "rows 5, 6 and 8" of the source text is rendered as the guide entries the register statement R-04-1 names (human-act, autonomy and host-method entries), because the SoW does not number the guide's rows. Same admitted arc N-B9.
```old
supplier boundary (native surfaces for optional external access),
```
```new
supplier boundary (native surfaces for optional external access, and the supplier facts on run holds, supplied guidance and model destination that the guide's human-act, autonomy and host-method entries cite),
```

#### G-0304-02 · CLM-003, DEL-09-06 part · S-04-2
Target: DEL-03-04
Trace: pass-2 C1-B S-04-2 (text as proposed). Same admitted arc N-B10; the DAG-003 guard against DEL-09-06 → DEL-03-04 is unaffected.
```old
recorded SWBPIPE answers (the host-contribution column)
```
```new
recorded SWBPIPE answers (the host-contribution column) and its connected-activity contract (step map, staging and evidence ladder)
```

#### G-0304-03 · receiving map, row "Autonomy", column 4 · S-04-3 · conditional (Q-11)
Target: DEL-03-04
Trace: pass-2 C1-B S-04-3 (text as proposed, with the K1 citation it names); GUIDE §0 already states it.
```old
their acts are recorded only when performed and no hold is claimed — and hold only for a workflow that takes up the governance phase (`APP-V4-SWBPIPE-INTAKE-20260928-DECISION-4` D4-1);
```
```new
their acts are requested by the agent carrying out the workflow and recorded only when performed, and no hold is claimed — and hold only for a workflow that takes up the governance phase (`APP-V4-SWBPIPE-INTAKE-20260928-DECISION-4` D4-1; `APP-V4-DESIGN-PASS-2-20260930-DECISION-K1` K1-1);
```

#### G-0304-04 · new AX-005 (amendment reference) · acceptance-conditional
Target: DEL-03-04
```old
REQ-005, TBD-001 and TBD-002. Added: AX-004. Removed: none.
```
```new
REQ-005, TBD-001 and TBD-002. Added: AX-004. Removed: none.
- **AX-005** — Revised under scope-change amendment `{AMENDMENT_ID}` (accepted snapshot `projects/chirality-app-v4/execution/_ScopeChange/{AMENDMENT_SNAPSHOT}`), applying `APP-V4-DESIGN-PASS-2-20260930-DECISION-K1` K1-1 (record `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-DESIGN-PASS-2-20260930/OWNER_DECISIONS.md`), with the supplier-input corrections of that run's closeout. Revised: CLM-003 and the receiving-map row "Autonomy". Added: AX-005. Removed: none.
```

---

## DEL-04-01 — Operation-policy and human-act distinctions

REVISION_SCOPE: CLM-002 (last sentence); REQ-002 (two added sentences); new
TBD-005; new AX-006.

#### G-0401-01 · CLM-002, last sentence · SC2-04-01-1
Target: DEL-04-01
Trace: pass-2 C1-A SC2-04-01-1 (text as proposed); DEP-09-06-030 (checked ACTIVE). Grounds R2-04-01-a. Supplier-side wording only: DEL-04-01 gains no supplier (guard).
```old
`DEL-05-01`, `DEL-05-02` and `DEL-09-09`, each of which declares it upstream in its own register.
```
```new
`DEL-05-01`, `DEL-05-02`, `DEL-09-06` and `DEL-09-09`, each of which declares it upstream in its own register.
```

#### G-0401-02 · REQ-002, after the first sentence · SC2-04-01-4 · conditional (Q-11)
Target: DEL-04-01
Trace: pass-2 C1-A SC2-04-01-4 with the optional addition pass-3 C1-B §5 recommends ("captured through DEL-01-04's App act control (K-8)"), worded here. R12-5 (A15). The upstream IDs are written in the qualified form. **Guard:** the sentence states that this contract *supplies* the distinction to DEL-02-02 and DEL-01-04 (both declare DEL-04-01 upstream: DEP-02-02-016, DEP-01-04-011, checked) and consumes nothing from them, so extraction must not read it as DEL-04-01 consuming either (DEL-04-01 gains no supplier).
```old
human marking checked, accepting an edit, engineering approval and professional reliance.
```
```new
human marking checked, accepting an edit, engineering approval and professional reliance. Registering a workflow revision (A15) is likewise a person's act with its own actor, subject (the revision) and evidence. This contract supplies that distinction to App v4 `DEL-02-02`, whose registration it governs (`DEL-02-02/REQ-002`, `DEL-02-02/AC-006`), and to `DEL-01-04`, whose App act control captures it (`APP-V4-DESIGN-PASS-3-20261001-DECISION-K3` K-8); it consumes nothing from either.
```

#### G-0401-03 · new TBD-005 · SC2-04-01-3
Target: DEL-04-01
Trace: pass-2 C1-A SC2-04-01-3 (text as proposed); ACT U-02, §8.5; ACT-v0.9 still lists U-02 open (P1 check). Records an open item; decides nothing. Pairs register item R2-04-01-c (EXTERNAL constraint row).
```old
This limits the VER-001 and VER-006 checkpoint cases to recording in the current phase; it does not change the policy meaning.
```
```new
This limits the VER-001 and VER-006 checkpoint cases to recording in the current phase; it does not change the policy meaning.
- **TBD-005** — The consequence dimension of operation classes (REQ-001, OUT-002) has no adopted vocabulary. A PROPOSED draft over the four dimensions of S/DECISION_BRIEF.html#d3 is prepared for the owner's phase review; until one is adopted no policy value assigns a consequence and the grant's consequence dimension stays a slot. **Owner:** the owner with the host policy owner. **Point of need:** before class assignment in `DEL-03-01`.
```

#### G-0401-04 · new AX-006 (amendment reference) · acceptance-conditional
Target: DEL-04-01
```old
Added: TBD-004 and AX-005. Removed: none.
```
```new
Added: TBD-004 and AX-005. Removed: none.
- **AX-006** — Revised under scope-change amendment `{AMENDMENT_ID}` (accepted snapshot `projects/chirality-app-v4/execution/_ScopeChange/{AMENDMENT_SNAPSHOT}`), applying integrator ruling R12-5 of `APP-V4-DESIGN-PASS-2-20260930` (A15; record `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-DESIGN-PASS-2-20260930/R12_RESOLUTIONS.md`) and `APP-V4-DESIGN-PASS-3-20261001-DECISION-K3` K-8 (record `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-DESIGN-PASS-3-20261001/OWNER_DECISIONS.md`), and recording the open consequence vocabulary. Revised: CLM-002 and REQ-002. Added: TBD-005 and AX-006. Removed: none.
```

---

## DEL-04-02 — Visible autonomy and result standing

REVISION_SCOPE: CLM-002 (receivers sentence); new AX-006.

#### G-0402-01 · CLM-002, receivers sentence · SC2-04-02-1
Target: DEL-04-02
Trace: pass-2 C1-A SC2-04-02-1 (text as proposed); DEP-03-04-012, DEP-09-06-031, DEP-09-09-022 (checked). Grounds R2-04-02-a…c. **Not added:** DEL-01-04 (NR-08 consumes DEL-04-02; AS-v0.9 §12 names it): naming it here is optional and would need a mirror row no source proposes (LEDGER note).
```old
Its visible autonomy state is received by `DEL-05-01`, `DEL-05-02`, `DEL-03-02`, `DEL-03-03` and `DEL-02-03`.
```
```new
Its visible autonomy state is received by `DEL-05-01`, `DEL-05-02`, `DEL-03-02`, `DEL-03-03` and `DEL-02-03`. `DEL-03-04`, `DEL-09-06` and `DEL-09-09` also declare it upstream in their own registers.
```

#### G-0402-02 · new AX-006 (amendment reference) · acceptance-conditional
Target: DEL-04-02
```old
Revised: CLM-004. Added: AX-005. Removed: none.
```
```new
Revised: CLM-004. Added: AX-005. Removed: none.
- **AX-006** — Revised under scope-change amendment `{AMENDMENT_ID}` (accepted snapshot `projects/chirality-app-v4/execution/_ScopeChange/{AMENDMENT_SNAPSHOT}`), recording the further receivers of this deliverable's visible autonomy state named by the closeout of `APP-V4-DESIGN-PASS-2-20260930`. Revised: CLM-002. Added: AX-006. Removed: none.
```

---

## DEL-04-03 — Content-bound decisions and compact run records

REVISION_SCOPE: CLM-004 (supplier list, three insertions); REQ-003
(appended sentence); REQ-005 (inserted sentence); new AX-005.

#### G-0403-01 · CLM-004, DEL-02-03 and DEL-02-01 items · SC2-04-03-2
Target: DEL-04-03
Trace: pass-2 C1-A SC2-04-03-2 (text as proposed); K1 K1-1; R14-1; ARC_ANALYSIS K-8. Grounds R2-04-03-e (new held arc DEL-04-03 → DEL-02-01, both in SCC-002) and R2-04-03-f.
```old
checkpoint arrival, act and lapse events (with hold events retained for the governance phase) and compatibility reports from `DEL-02-03`,
```
```new
checkpoint arrival, act request (where it can be identified), act and lapse events (with hold events retained for the governance phase) and compatibility reports from `DEL-02-03`, the workflow identity tuple and the checkpoint disposition vocabulary from `DEL-02-01`,
```

#### G-0403-02 · CLM-004, DEL-02-02 item · P1-05 · conditional (Q-4, R20-10)
Target: DEL-04-03
Trace: P1-05 (drafted here; no source proposes the consumer sentence). RS-v0.9 §4 R3 (b) and (c) ("each citing DEL-02-02's `run_text` record … with … the state of DEL-02-02's `supply_check`"), §6.2 HA-10 (A15 composed from DEL-02-02's A15 descriptor), §10 rows "DEL-02-02 (WR-v0.2; v0.9)" and "no register row yet; proposed in the F-C return"; WR-v0.2 §7, §16; R19-7, R20-3, R20-10. Grounds R20-10 (new held arc DEL-04-03 → DEL-02-02, SCC-neutral).
```old
external dispatch entries from `DEL-03-03`,
```
```new
external dispatch entries from `DEL-03-03`, the per-run run-start text and run-end line with their content identity and supply-check record, the selection record and the A15 descriptor's reviewed-content and prior-revision relations from `DEL-02-02`,
```

#### G-0403-03 · CLM-004, DEL-02-04 item · added under R22-7 (not in P1's ledger) · owner item (new; recommended include)
Target: DEL-04-03
Trace: design pass 3 R22-7 (`R22_RESOLUTIONS.md`): DEP-02-04-012 (DEL-02-04 DOWNSTREAM HANDOVER to DEL-04-03: "Provide the role-specific source identity, actual supplied bytes and enforcement-limit evidence to the content-bound run-record owner") has no supplier-side counterpart because this SoW names no DEL-02-04 input. RS-v0.9 §4 R3 (a) and R5a (DEL-02-04's supply record 0.2, limit account, `role_limit_observation`), §10 row "DEL-02-04 (ROLE-v0.2; v0.9) … DEP-02-04-012". Arc DEL-04-03 → DEL-02-04 exists today (through DEP-02-04-012; held, both in SCC-002): mirror only, no topology change. Grounds a new register mirror row in DEL-04-03 (UPSTREAM INTERFACE → DEL-02-04), to be added to the ledger (see "For the ledger"). DEP-02-04-013 (DEL-11-02) is not addressed here: it stays open with DEL-11-02's owner (R22-7).
```old
tool-permission settlements) from `DEL-01-01`, and a host agent's
```
```new
tool-permission settlements) from `DEL-01-01`, role-supply records (the role guidance supplied at conversation start or a fork, with its source and content identity, the limit account and observations that a stated limit was not kept) from `DEL-02-04`, and a host agent's
```

#### G-0403-04 · REQ-003, appended sentence · SC2-04-03-3
Target: DEL-04-03
Trace: pass-2 C1-A SC2-04-03-3 (text as proposed), with the Codex-account form of integrator ruling R18-1 C-10 of pass 3 (LEDGER note: "reported email, or 'ChatGPT account (no email reported)'; plan type not recorded"). K1 K1-4. No supplier is named for the Codex account, so no arc toward DEL-01-05 is implied (none is proposed).
```old
Recording shall preserve the actual human actor and scope of a performed act separately from its recorder and the recorder's available evidence.
```
```new
Recording shall preserve the actual human actor and scope of a performed act separately from its recorder and the recorder's available evidence. For an act captured in the App, the actor is recorded from what the App can observe — the name the person set in the App, the operating-system account and the Codex account when Codex reports one (its reported email, or "ChatGPT account (no email reported)"; the plan type is not recorded) — marked *identity not verified* (`APP-V4-DESIGN-PASS-2-20260930-DECISION-K1` K1-4); a verified identity is governance-phase work.
```

#### G-0403-05 · REQ-005, after the first sentence · SC2-04-03-1
Target: DEL-04-03
Trace: pass-2 C1-A SC2-04-03-1, kept by pass-3 C1-A and C1-B; "outside this undertaking" dropped (see "Reading this file"). Consumers checked ACTIVE: DEP-02-01-019, DEP-02-03-013, DEP-03-01-031, DEP-03-04-013, DEP-01-04-012, DEP-02-02-017, DEP-09-02-019, DEP-09-05-010, DEP-10-03-014. Grounds R2-04-03-a…d. RS §10 lists the same set (with DEL-06-01, DEL-06-02, which the pass-2 sentence did not name and this block does not add).
```old
how host-agent runs use it with receipt references. App `DEL-04-02` receives
```
```new
how host-agent runs use it with receipt references. App v4 `DEL-02-01`, `DEL-02-03` and `DEL-03-01` consume it at deliverable level, `DEL-03-04` (integration guide) declares it upstream, and `DEL-01-04`, `DEL-02-02`, `DEL-09-02`, `DEL-09-05` and `DEL-10-03` do so in their own registers. App `DEL-04-02` receives
```

#### G-0403-06 · new AX-005 (amendment reference) · acceptance-conditional
Target: DEL-04-03
```old
REQ-002, REQ-005 and TBD-001. Added: AX-004. Removed: none.
```
```new
REQ-002, REQ-005 and TBD-001. Added: AX-004. Removed: none.
- **AX-005** — Revised under scope-change amendment `{AMENDMENT_ID}` (accepted snapshot `projects/chirality-app-v4/execution/_ScopeChange/{AMENDMENT_SNAPSHOT}`), applying `APP-V4-DESIGN-PASS-2-20260930-DECISION-K1` K1-1 and K1-4 (record `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-DESIGN-PASS-2-20260930/OWNER_DECISIONS.md`) and the integrator rulings R18-1 (C-10), R19-7, R20-3, R20-10 and R22-7 of `APP-V4-DESIGN-PASS-3-20261001` (records `R18_RESOLUTIONS.md` … `R22_RESOLUTIONS.md` in that run's folder). Revised: CLM-004, REQ-003 and REQ-005. Added: AX-005. Removed: none.
```

Note: the edit IDs of this deliverable are numbered in application order;
the R22-7 block is G-0403-03.

---

## DEL-05-01 — Minimal-loop and model receiving contract

REVISION_SCOPE: OUT-002 (basis sentence); CLM-002 (appended sentence);
TBD-003 (inserted sentences); new AX-005.

#### G-0501-01 · OUT-002, basis sentence · S-0501-1 (part 2)
Target: DEL-05-01
Trace: pass-2 C1-C S-0501-1 optional second part (text as proposed); the LEDGER includes both parts ("without the OUT-002 edit the fixtures cannot satisfy OUT-002 as written; no requirement relaxed").
```old
Fixtures identify their adopted catalog and model-interface basis;
```
```new
Fixtures identify their adopted catalog basis and their model-interface basis (adopted, or until one is adopted a named fixture basis);
```

#### G-0501-02 · CLM-002, DEL-01-05 sentence · P1-10 · conditional (Q-15)
Target: DEL-05-01
Trace: P1-10 (drafted here). DEP-01-05-014 (DEL-01-05 DOWNSTREAM HANDOVER: "applicable local-server capability requirements and qualification limits … preserving App-provider versus host-model interface distinctions"); ACCESS-v0.2 §11 CH-1…CH-8 (interface I-8); LOOP-v0.9 §10.3 FL-01 ("read here as information with no requirement taken from it, each item's bearing stated"). DEL-05-01's SoW names DEL-01-05 0 times. Grounds R-0501-4 (mirror of an admitted arc DEL-05-01 → DEL-01-05).
```old
This deliverable consumes their meanings at the loop boundary.
```
```new
This deliverable consumes their meanings at the loop boundary. It also receives App v4 `DEL-01-05`'s local-server capability requirements and qualification limits (its capability handoff) as information, keeping the App's provider interface distinct from a host's model interface; no requirement of this contract is taken from them.
```

#### G-0501-03 · TBD-003, fixture basis · S-0501-1 (part 1)
Target: DEL-05-01
Trace: pass-2 C1-C S-0501-1 (text as proposed); R12-8; LOOP §4.1 (FB-CC-1; heading checked). Pairs R-0501-1.
```old
SWBPIPE has none selected, so that basis stays UNKNOWN.
```
```new
SWBPIPE has none selected, so that basis stays UNKNOWN. For its own fixtures this deliverable writes against a published Chat Completions reference that it names as a fixture basis, not a product selection (Design `LOOP_RECEIVING_CONTRACT.md` §4.1, FB-CC-1; integrator ruling R12-8 of `APP-V4-DESIGN-PASS-2-20260930`). That names no adopted basis for any host, and DEP-05-01-024 stays open.
```

#### G-0501-04 · new AX-005 (amendment reference) · acceptance-conditional
Target: DEL-05-01
```old
VER-001, VER-002 and TBD-003. Added: AX-004. Removed: none.
```
```new
VER-001, VER-002 and TBD-003. Added: AX-004. Removed: none.
- **AX-005** — Revised under scope-change amendment `{AMENDMENT_ID}` (accepted snapshot `projects/chirality-app-v4/execution/_ScopeChange/{AMENDMENT_SNAPSHOT}`), applying integrator ruling R12-8 of `APP-V4-DESIGN-PASS-2-20260930` (record `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-DESIGN-PASS-2-20260930/R12_RESOLUTIONS.md`), and recording the `DEL-01-05` capability handoff this contract receives. Revised: OUT-002, CLM-002 and TBD-003. Added: AX-005. Removed: none.
```

---

## DEL-09-06 — Connected activity contract and workflow round trip

REVISION_SCOPE: CLM-003 (appended sentence); OUT-003 (appended sentence);
REQ-008 (one exclusion clause); TBD-003 (c) (appended); new AX-005.

#### G-0906-01 · CLM-003, DEL-09-01 sentence · S-0906-3 (1 of 2)
Target: DEL-09-06
Trace: pass-2 C1-C S-0906-3 (text as proposed); DEP-09-01-024 (DEL-09-01 DOWNSTREAM HANDOVER to DEL-09-06, checked); CA §6 ST-1, §11.1. Grounds R-0906-3 (consumer row on the admitted arc DEL-09-06 → DEL-09-01). DEL-09-06's SoW names DEL-09-01 0 times today (checked).
```old
App DEL-05-01 owns loop/model receiving requirements and App DEL-05-02 panel receiving requirements.
```
```new
App DEL-05-01 owns loop/model receiving requirements and App DEL-05-02 panel receiving requirements. App DEL-09-01 supplies reusable candidate-examination support and the evidence protocol (candidate, date and configuration identification; outcome states; replay, browser and native marking) that the joined witness uses.
```

#### G-0906-02 · OUT-003, appended sentence · S-0906-2
Target: DEL-09-06
Trace: pass-2 C1-C S-0906-2 (text as proposed); R12-1, R12-2; CA §8.4; `Design/w14-result-record.schema.json` exists (checked).
```old
with the actual execution record and received host evidence.
```
```new
with the actual execution record and received host evidence. The per-case result record is drafted as a PROPOSED JSON Schema (`Design/w14-result-record.schema.json`) with conformance examples; it fixes meaning, not a selected form, and no rehearsal record counts toward this output.
```

#### G-0906-03 · REQ-008, exclusion clause · S-0906-3 (2 of 2)
Target: DEL-09-06
Trace: as G-0906-01. The clause binds DEL-09-01 to CLM-003, which G-0906-01 makes name it, so the boundary-owner check resolves.
```old
and supplier observation belongs to App DEL-01-01 (CLM-003);
```
```new
and supplier observation belongs to App DEL-01-01 and reusable candidate-examination support and evidence-protocol construction to App DEL-09-01 (CLM-003);
```

#### G-0906-04 · TBD-003 (c), appended · S-0906-1
Target: DEL-09-06
Trace: pass-2 C1-C S-0906-1 (text as proposed); CA §2.6 (heading checked), F-25, §8.1. A pointer; no criterion changes; the point of need is unchanged.
```old
OUT-003's joined witness cannot complete before then.
```
```new
OUT-003's joined witness cannot complete before then. SWBPIPE's answers of 2026-09-28 (`Design/RELAY_ANSWERS_SWBPIPE.md`; answers about its current state, not commitments) show that resumption alone does not make it completable. Set against those answers, no step of the designed activity is examinable against SWBPIPE (`Design/CONNECTED_ACTIVITY_CONTRACT.md` §2.6), whatever operation is selected under TBD-001. The joined witness also needs an identified host candidate, a host workflow library or work item to receive App workflows, a host act facility with a capture-evidence reference, and, on the external channel, an A13 enablement facility (on the embedded surface, a host loop). Each is a SWBPIPE owner decision.
```

#### G-0906-05 · new AX-005 (amendment reference) · acceptance-conditional
Target: DEL-09-06
```old
the REQ-003/AC-004 matrix evidence cell and TBD-002. Added: TBD-003 and AX-004. Removed: none.
```
```new
the REQ-003/AC-004 matrix evidence cell and TBD-002. Added: TBD-003 and AX-004. Removed: none.
- **AX-005** — Revised under scope-change amendment `{AMENDMENT_ID}` (accepted snapshot `projects/chirality-app-v4/execution/_ScopeChange/{AMENDMENT_SNAPSHOT}`), recording the closeout findings of `APP-V4-DESIGN-PASS-2-20260930` (record `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-DESIGN-PASS-2-20260930/closeout/C1-C.md`): the option-sheet consequence for the joined witness, the PROPOSED result-record schema (integrator rulings R12-1 and R12-2 of that run) and the examination-support supplier. Revised: CLM-003, OUT-003, REQ-008 and TBD-003. Added: AX-005. Removed: none.
```

---

## DEL-09-09 — External control and catalog-extension trace

REVISION_SCOPE: OUT-001 (appended sentence); OUT-003 (appended sentences);
REQ-001 (TBD range); new AX-006.

#### G-0909-01 · OUT-001, appended sentence · S-0909-2 (1 of 2)
Target: DEL-09-09
Trace: pass-2 C1-C S-0909-2 (text as proposed); R12-1, R12-2; `Design/xt-result-record.schema.json` exists (checked).
```old
including intervening edit and lost acknowledgment/interruption.
```
```new
including intervening edit and lost acknowledgment/interruption. Its per-case result record is drafted as a PROPOSED JSON Schema (`Design/xt-result-record.schema.json`) with conformance examples.
```

#### G-0909-02 · OUT-003, appended sentences · S-0909-2 (2 of 2)
Target: DEL-09-09
Trace: as G-0909-01; `Design/xt-work-account.schema.json` exists (checked).
```old
and preserves either the unresolved promise or the actual retain/narrow/defer decision and its consequences.
```
```new
and preserves either the unresolved promise or the actual retain/narrow/defer decision and its consequences. The work account is drafted as a PROPOSED JSON Schema (`Design/xt-work-account.schema.json`). Each fixes meaning, not a selected form; no rehearsal record counts toward the witness.
```

#### G-0909-03 · REQ-001, TBD range · S-0909-1
Target: DEL-09-09
Trace: pass-2 C1-C S-0909-1; TBD-005 was added by SCA-V4-001 (AX-005).
```old
Carry unresolved details at TBD-001 through TBD-004;
```
```new
Carry unresolved details at TBD-001 through TBD-005;
```

#### G-0909-04 · new AX-006 (amendment reference) · acceptance-conditional
Target: DEL-09-09
```old
REQ-004, REQ-009 and TBD-002. Added: TBD-005 and AX-005. Removed: none.
```
```new
REQ-004, REQ-009 and TBD-002. Added: TBD-005 and AX-005. Removed: none.
- **AX-006** — Revised under scope-change amendment `{AMENDMENT_ID}` (accepted snapshot `projects/chirality-app-v4/execution/_ScopeChange/{AMENDMENT_SNAPSHOT}`), recording the PROPOSED result-record and work-account schemas (integrator rulings R12-1 and R12-2 of `APP-V4-DESIGN-PASS-2-20260930`; record `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-DESIGN-PASS-2-20260930/R12_RESOLUTIONS.md`) and correcting REQ-001's pointer to TBD-005. Revised: OUT-001, OUT-003 and REQ-001. Added: AX-006. Removed: none.
```

---

## Not written (DEFER or DROP rows; no block)

| Ledger row | Why no block | Where the source text is, if the owner includes it |
|---|---|---|
| S-01-4 (DEL-03-01 REQ-004/AC-004) | DEFER, Q-7 (protected criterion; V4-HI-11) | pass-2 `closeout/C1-B.md` §1.4 S-01-4 |
| SC2-04-01-2 (DEL-04-01 AC-007/VER-007, new AX) | DEFER, Q-9 (A12 mapping not confirmed) | pass-2 `closeout/C1-A.md`, "Proposed ScopeOfWork items" |
| S-0502-1 (DEL-05-02 CLM-002, OUT-001; option A) | DEFER, Q-9; option B (no change) stands | pass-2 `closeout/C1-C.md` §2.5 |
| SC3-02-02-5 (DEL-02-02 "host-supplied") | DROP (basis V4-WF-03's own word) | — |
| SC3-02-04-3 (DEL-02-04 REQ-002 workflow supply) | DROP (withdrawn under R19-7) | — |
| S-0906-4 (DEL-09-06 REQ-007) | DROP (source finds option (b), no change, supportable) | — |

If the owner confirms the A12 mapping (Q-9) or includes S-01-4 (Q-7), those
blocks are drafted from the cited source text, dry-run the same way, and added
to the AX lines of DEL-04-01, DEL-05-02 and DEL-03-01.

## For the ledger (added under R22-7; not in P1's LEDGER)

| Proposed ID | Kind | Deliverable | Location | Change | Disp. | Source |
|---|---|---|---|---|---|---|
| R22-7-SoW | ScopeOfWork | DEL-04-03 | CLM-004 supplier list | Add DEL-02-04's role-supply records (supply record, limit account, limit observations; RS R3 (a), R5a) as received input (G-0403-03) | INCLUDE (recommended) | pass-3 `R22_RESOLUTIONS.md` R22-7; RS-v0.9 §4, §10 |
| R22-7-reg | register | DEL-04-03 | new UPSTREAM INTERFACE row → DEL-02-04 | Mirror of DEP-02-04-012 (arc DEL-04-03 → DEL-02-04 exists, held in SCC-002; mirror only) | INCLUDE (recommended) | same |
| R22-7-open | — | DEL-11-02 | DEP-02-04-013 supplier side | Stays open with DEL-11-02's owner (outside the design passes); no block | — | same |

With these, the ledger would read 211 rows (187 INCLUDE); ARC_EFFECT's mirror
count gains one item, one row; the arc and SCC results are unchanged (mirror
only). The owner's item for it would sit with Q-15 (receivers sentences).

## Extraction guards (for the `dependency-extract` UPDATE briefs)

- **New arcs these blocks are meant to yield (consumer → supplier):**
  DEL-02-03 → DEL-01-02 (G-0203-03, NR-01), DEL-03-03 → DEL-01-02 (G-0303-01
  clause a, NR-02), DEL-02-02 → DEL-01-02 (G-0202-04 second sentence, NR-04),
  DEL-04-03 → DEL-02-01 (G-0403-01, R2-04-03-e), DEL-04-03 → DEL-02-02
  (G-0403-02, R20-10). The other five of ARC_EFFECT §1.1 come from P2-A's
  DEL-01-04 blocks.
- **Mirror-only sentences.** The receivers sentences (G-0201-02, G-0203-06,
  G-0204-01, G-0301-01, G-0302-02, G-0303-02, G-0401-01, G-0402-01, G-0403-05,
  G-0202-02's second half) are written "received by … each of which declares it
  upstream", the form extraction reads as DOWNSTREAM rows. Every named
  receiver already has an UPSTREAM row toward the supplier (checked), except
  DEL-01-04 in G-0204-01 (NR-4) and DEL-04-03 in G-0202-02 (R20-10), which
  are proposed new arcs. Some named receivers are beyond the ledger's mirror
  groups (DEL-02-01's DEL-02-02, 02-04, 08-02, 09-02, 10-03; DEL-02-03's
  DEL-02-02, 09-02, 10-03; DEL-04-03's DEL-01-04, 02-02, 09-02, 09-05, 10-03;
  DEL-04-01's DEL-01-04 and DEL-02-02 from G-0401-02): 15 DOWNSTREAM mirrors,
  each mirror-only on an existing arc. *Corrected at RP1 (V23 m-1):* DEL-02-03's
  DEL-09-06 was listed here in error (its mirror exists, DEP-02-03-014), and
  DEL-04-01's two were missing. The 15 rows are ledger RP1-MX-0201, -0203,
  -0403 and -0401, put to the owner as OWNER_ITEMS Q-17 (recommended include).
- **Consumer-side sentences on existing arcs:** G-0203-04 (→ DEL-04-02),
  G-0302-03 (→ DEL-04-02), G-0303-01 clause b (→ DEL-04-02, → DEL-02-01),
  G-0403-03 (→ DEL-02-04, R22-7), G-0501-02 (→ DEL-01-05), G-0906-01
  (→ DEL-09-01). No topology change.
- **DEL-04-01 gains no supplier.** G-0401-01 and G-0401-02 name DEL-09-06,
  DEL-02-02 and DEL-01-04 only as receivers of this contract ("supplies …;
  consumes nothing from either"). TBD-005 names DEL-03-01 as the point of
  need, not as a supplier.
- **DEL-09-06 guard.** No block makes an SCC-002 member consume DEL-09-06:
  DEL-09-06 is named only as a receiver (G-0201-02, G-0202-02, G-0203-06,
  G-0301-01, G-0302-02, G-0303-02, G-0401-01, G-0402-01) and in its own SoW.
- **R17-10 guard.** No block makes DEL-01-02 or DEL-01-03 a consumer of
  anything: DEL-01-02 appears only as a supplier.
- **NR-03 is not grounded:** no block in DEL-09-09 names DEL-01-02.
- **No block names DEL-11-02.**

## Mechanical checks performed

Run 2026-10-02 by node P2-B, Python 3, on copies in scratch
(`$TMPDIR/p2b/`, not in the repository). `dryrun.py` parsed this file (blocks
under `#### G-…` headings with their `Target:` line and `old`/`new` fences),
applied each deliverable's blocks in order to a copy of the SoW at HEAD
`40e04273da`, filled `{AMENDMENT_ID}` = `SCA-V4-003` and a dummy snapshot
name, and ran on each revised copy, and on each unrevised copy for
comparison, the validators the scope-of-work workflow names
(`resources/tools.md` steps 6, 7 and 9):

```
python3 tools/scope_of_work/validate_scope_of_work.py <copy>/ScopeOfWork.md
python3 tools/scope_of_work/derive_review_checklist.py <copy>/ScopeOfWork.md --output <copy>/checklist.json
python3 tools/scope_of_work/check_boundary_owner_resolution.py <copy>/ScopeOfWork.md --json <copy>/boundary.json
```

| Check | Result |
|---|---|
| Blocks parsed / `####` headings | 84 / 84 |
| Prior-contract sha256 equals the Summary table | 14/14 |
| Each "old" block occurs exactly once in the original file, and once again when applied in order | 84/84 |
| "Old" spans overlapping within one file; an "old" block found inside another block's "new" text | 0; 0 (every block is independent of the others) |
| Unfilled tokens after filling | 0 |
| Frontmatter unchanged | 14/14 |
| `validate_scope_of_work.py` on each revised copy | 14/14 `PASS format=SOW_V1` (prior copies 14/14 PASS) |
| `derive_review_checklist.py` on each revised copy | 14/14 exit 0 |
| `check_boundary_owner_resolution.py` on each revised copy | 14/14 exit 0, status OK, 0 findings; JSON equal to the prior copy's in all 14 (DEL-09-06 REQ-008 still resolves through CLM-003) |
| Same three tools with the 15 wholly conditional blocks dropped (G-0203-03, G-0301-01/-02/-03/-05/-06/-07, G-0302-02/-03, G-0303-03, G-0304-03, G-0401-02, G-0403-02/-03, G-0501-02) | 14/14 PASS, exit 0, exit 0 |
| New deliverable IDs the revised text names beyond the prior file | as listed in "Extraction guards"; every one is a receiver with an existing UPSTREAM row toward the supplier, a supplier on an existing or ledger-proposed arc, or DEL-04-01's point-of-need mention of DEL-03-01; none is DEL-11-02 |

Clause-level conditions inside G-0202-04, G-0204-01 and G-0303-01 were not
dropped mechanically; each is a whole clause, removable without touching the
rest of the block.

These are checks of the proposal before application. They are not the REVISE
runs or their `MODE=VERIFY`.
