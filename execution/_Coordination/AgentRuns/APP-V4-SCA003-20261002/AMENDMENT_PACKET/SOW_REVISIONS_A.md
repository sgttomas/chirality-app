# SoW revisions, part A (PKG-01) — SCA-V4-003, node P2-A

**Status: PROPOSED (scope-change checkpoint-group-2 preparation). Nothing here
is applied.** Every edit is an exact old → new replacement in one
`ScopeOfWork.md`. It is applied after the owner accepts the amendment, by
`scope-of-work` `MODE=REVISE`, one deliverable per brief,
`STATUS_POLICY=NO_STATUS_TOUCH`, closing with `MODE=VERIFY` (the route of
SCA-V4-001 and SCA-V4-002; IMPACT_ASSESSMENT §10).

- **Scope of this file:** the INCLUDE ScopeOfWork rows of [LEDGER.csv](LEDGER.csv)
  whose target is a PKG-01 deliverable: 44 rows in DEL-01-01…DEL-01-05,
  including P1-09 (the only P1 grounding sentence in PKG-01). DEL-01-06 has no
  ledger row of any kind (checked by script over LEDGER.csv) and no block.
  The other packages are in `SOW_REVISIONS_B.md` (node P2-B).
- **Basis:** HEAD `40e04273da`. Every "old" block was copied from the current
  SoW bytes, whose sha256 equal the C1 records' inputs and P3's baseline
  (Summary). Each occurs exactly once when applied in the listed order, and
  the blocks do not overlap. See "Mechanical checks" at the end.
- **Lifecycle:** DEL-01-01 is IN_PROGRESS; DEL-01-02, 01-03, 01-04 and 01-05
  are INITIALIZED (each `**Current State:**` line read). REVISE admits both.
  None is CHECKING or ISSUED. R22-5 (Q-13) is a separate act and changes
  nothing here.
- **Model:** SCA-V4-002's `AMENDMENT_PACKET/SOW_REVISIONS.md` (accepted
  conventions; read whole). Sources of the wording: `P3RUN/closeout/C1-A.md`
  "Proposed ScopeOfWork items" (DEL-01-02…01-04, with its full text of
  SC3-01-04-1), `P3RUN/closeout/C1-B.md` §4.1 with `P3RUN/D/D4.md` P-1…P-10
  and R2.4 (DEL-01-05), `P2RUN/closeout/C1-B.md` §5.4 (DEL-01-01). `P2RUN` =
  `E/_Coordination/AgentRuns/APP-V4-DESIGN-PASS-2-20260930`, `P3RUN` =
  `…/APP-V4-DESIGN-PASS-3-20261001`, `E` = `projects/chirality-app-v4/execution`.

## Reading this file

- **Edit IDs** are `G-<deliverable>-<nn>`. The "G" series keeps them distinct
  from SCA-V4-001's `E-` and SCA-V4-002's `F-` IDs; part B uses the same
  series for other deliverables, so no ID can collide. Apply each
  deliverable's edits in the listed order.
- **Tokens.** `{AMENDMENT_ID}` is the accepted amendment ID (recommended
  `SCA-V4-003`, Q-1). `{AMENDMENT_SNAPSHOT}` is the accepted group-3 snapshot
  folder name under `projects/chirality-app-v4/execution/_ScopeChange/`. Both
  are filled at application from the accepted records. No other byte depends
  on the acceptance act.
- **Amendment reference.** Each revised SoW gains one Axiology `AX-*` line
  naming the amendment, its snapshot, the decisions and rulings applied, and
  the revised, added and removed IDs (REVISE step 4).
- **New IDs.** Unlike SCA-V4-002, two contracts gain new local IDs, as the
  ledger rows require: DEL-01-04 gains OUT-005, REQ-008, AC-008, VER-008 and
  one matrix row (SC3-01-04-1, the App act control); DEL-01-05 gains REQ-010,
  AC-011, VER-011 and one matrix row (SC3-01-05-5). Each takes the next free
  number; nothing is renumbered, reused or removed.
- **Frontmatter is unchanged** in every SoW (no scope or objective reference
  changes; the new outputs map to references already in the frontmatter).
- **Owner dependency.** Every block depends on the owner item named in its
  heading (OWNER_ITEMS.md; none is answered yet). Each block is written for
  the recommended option. If the owner declines an item, drop the blocks or
  the clauses named under "If declined" and remove the dropped IDs from the
  AX line's Revised/Added list.
- **Wording.** Source wording is used verbatim where the source gives it.
  Where the source gives only a substance ("full text at source", "matching
  OUT, AC, VER") or the ledger leaves the wording to P2 (P1-09), the text is
  drafted here from the cited Design sections and marked **drafted (P2-A)**.
  One source sentence is adjusted to respect an amendment guard and is marked
  **adjusted (P2-A)**, with the source wording kept as the alternative.
- **Backticks.** In four requirements (DEL-01-02 REQ-004 and REQ-006;
  DEL-01-04 REQ-002 and REQ-008) the new text writes deliverable IDs without
  backticks. `check_boundary_owner_resolution.py` reads a backticked ID in a
  requirement that also contains "owner", "boundary" or a possessive as a
  per-act exclusion and reports it `NOT_CHECKABLE`; these sentences exclude no
  act (the named deliverables are suppliers or receivers), and with backticks
  the four would each add a manual QA item 21 finding. The IDs and meaning
  are unchanged; extraction reads either form.

Decision identities used in the new text:

| Short form here | Full identity in the SoW text | Record |
|---|---|---|
| FI DECISION-1 (D2, D3, D4) | `APP-V4-FIRST-INCREMENT-20260928-DECISION-1` | `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-FIRST-INCREMENT-20260928/OWNER_DECISIONS.md` |
| DECISION-K1 (K1-1…K1-4) | `APP-V4-DESIGN-PASS-2-20260930-DECISION-K1` | `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-DESIGN-PASS-2-20260930/OWNER_DECISIONS.md` |
| DECISION-K3 as revised (K-1, K-3, K-4, K-5, K-8, K-10, K-12) | `APP-V4-DESIGN-PASS-3-20261001-DECISION-K3` | `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-DESIGN-PASS-3-20261001/OWNER_DECISIONS.md` ("DECISION-K3" and "DECISION-K3, revised") |
| DECISION-L (L-1, L-2, L-3, L-4, L-6, L-7) | `APP-V4-DESIGN-PASS-3-20261001-DECISION-L` | same record |
| Rulings R17…R22 | named by number in the AX lines only | `P3RUN/R17_RESOLUTIONS.md`, `R18_…`, `R19_…`, `R20_RESOLUTIONS.md` (also holds R21-1…R21-6), `R22_RESOLUTIONS.md` |

The pass-2 and pass-3 records label their decisions "DECISION-K1",
"DECISION-K3" and "DECISION-L" without a run prefix. The full form follows the
pattern the earlier records use (as SCA-V4-002 did for BA DECISION-8), and
each AX line also cites the record path. Rulings are the design passes'
recorded integrator rulings, not owner decisions; the AX lines say so.

## Summary

| Deliverable | Prior SoW sha256 | Lifecycle | Blocks | Ledger rows carried | Owner items |
|---|---|---|---:|---|---|
| DEL-01-01 | `9945e72b04b4f45c4c641a5248cca8bc2ac40bf4897d1018c5ab59eba307cc75` | IN_PROGRESS | 4 | S-11-1, S-11-2, P1-09 | Q-2, Q-11, Q-15 |
| DEL-01-02 | `057ae2fdf4c3e98c961214739d2170a7c8ab29a530208f0c476af15125d6c6b4` | INITIALIZED | 18 | SC3-01-02-1…11 | Q-2, Q-4, Q-11 |
| DEL-01-03 | `b5d533cb3dbea97b37950792ad2c68f42bf6023effa4ac894209a1ef3fc605f2` | INITIALIZED | 11 | SC3-01-03-1…8 | Q-2 |
| DEL-01-04 | `0cdb44e297010b70deb479ab647a165023846aa0943c3f9fc200407c708469cd` | INITIALIZED | 14 | SC3-01-04-1…8, -10…13 | Q-2, Q-4, Q-5 |
| DEL-01-05 | `baf68c79b5b8fdf01300fc255d7cf8e433975e6275daadf67b914b4e51eca4a6` | INITIALIZED | 16 | SC3-01-05-1…7, -10, -12, -13 | Q-2, Q-11 |
| DEL-01-06 | `08e30b97baeb06ae57b6166d6358f5c68ad1d934102df7ea094ce6cc57abd795` | INITIALIZED | 0 | none in the ledger | — |
| **Total** | | | **63** | **44 rows** (every one appears in a block heading; checked by script) | |

The 63 blocks include 5 amendment-reference AX lines and 2 new matrix rows.
The DROP rows naming PKG-01 (SC2-01-04-1, C1-B X-1, SC3-02-02-8,
SC3-01-05-11) have no block. The non-ScopeOfWork rows (registers, OI-009) are
not in this file; the "Extraction guards" section states what the registers
should extract from these blocks.

---

## DEL-01-01 — Stock Codex hosting and supplier contract

REVISION_SCOPE: CLM-004 (one appended sentence); CLM-005 (one appended
sentence); TBD-002 (first sentence); new AX-007. ScopeChanging: NO.

#### G-0101-01 · CLM-005, new last sentence · S-11-2 · Q-2
Target: DEL-01-01
Trace: P2RUN C1-B §5.4 S-11-2 (wording verbatim); HOSTING-v0.9 §8.4 (harness-capability account at 0.158.0, arc N-16); DEP-02-01-025 ("Receive the harness capability meaning supplied through DEL-01-01"). Coordinated with SC2-02-01-1 on DEL-02-01's side (part B). Mirror: one of R-11-1's rows (DEL-02-01). REQ-008 cites CLM-005 for its owners; the sentence adds no excluded act.
```old
No record implementation performs a person's act. [D; R sections 4.5 and 4.7; K]
```
```new
No record implementation performs a person's act. [D; R sections 4.5 and 4.7; K] This deliverable supplies the harness-capability meaning of the selected pin (the supplier's item kinds, server requests and client methods grouped by capability, with their standing) to `DEL-02-01`, which owns the portable capability names that resolve to it.
```

#### G-0101-02 · CLM-004, new last sentence · P1-09 · Q-15 · drafted (P2-A)
Target: DEL-01-01
Trace: ledger P1-09 ("Name DEL-02-03, 03-03, 03-04, 09-06, 06-01, 09-01, 09-02"; wording left to P2). Each parenthesis restates the consuming row's own Statement: DEP-02-03-023, DEP-03-03-013, DEP-03-04-021, DEP-09-06-032, DEP-06-01-013, DEP-09-01-019, DEP-09-02-009 (read from each `Dependencies.csv`; all seven arcs are admitted in DAG-003). Placed in CLM-004, whose last sentence already says which deliverables "consume this supplier boundary", so the block is independent of G-0101-01. REQ-007 cites CLM-004; it names none of these seven, so the boundary check is unaffected. Grounds 7 of R-11-1's 10 mirror rows; DEL-02-04 and DEL-04-03 are already named in CLM-005 and DEL-02-01 by G-0101-01.
If declined (Q-15): drop this block and remove CLM-004 from AX-007's Revised list; the seven rows are then declared by hand in `_DEPENDENCIES.md` or not made.
```old
These accepted [D] rows consume this supplier boundary; their production acts are not transferred here.
```
```new
These accepted [D] rows consume this supplier boundary; their production acts are not transferred here. Within project **chirality-app-v4**, the boundary is also received by `DEL-02-03` (observed supplier facts, as capability information for App-side execution compatibility), `DEL-03-03` (supplier MCP/dynamic-tool surfaces and channel-status facts at the definition pin), `DEL-03-04` (native surfaces for optional external access), `DEL-09-06` (App-side supplied-guidance and model-destination evidence), `DEL-06-01` and `DEL-09-01` (the selected Codex pin, before protocol generation and qualification) and `DEL-09-02` (the hosting/protocol contribution and scoped feature checks, before its joined native/protocol witness); each declares it upstream in its own register, and none of their acts is transferred here.
```

#### G-0101-03 · TBD-002, first sentence · S-11-1 · Q-11 (optional)
Target: DEL-01-01
Trace: P2RUN C1-B §5.4 S-11-1 (OBS-1 pointer), extended as the ledger allows: `Design/OBS_2_0.158.0.md` and `Design/OBS_3_0.158.0.md` exist in DEL-01-01's Design folder (checked with `ls`), and each record's header calls itself a dated observation at one version, "Not qualification" (read). All three ran against a local LM Studio model.
If declined: drop this block and remove TBD-002 from AX-007's Revised list.
```old
observations recorded in `Design/PIN_SPIKE_0.158.0.md`.
```
```new
observations recorded in `Design/PIN_SPIKE_0.158.0.md` and, as dated observations at 0.158.0 against a local LM Studio model (not qualification), in `Design/OBS_1_0.158.0.md` (OBS-1, OBS-1b), `Design/OBS_2_0.158.0.md` (OBS-2) and `Design/OBS_3_0.158.0.md` (OBS-3).
```

#### G-0101-04 · new AX-007 (amendment reference) · acceptance-conditional
Target: DEL-01-01
```old
Revised: the [N] source line. Added: AX-006. Removed: none.
```
```new
Revised: the [N] source line. Added: AX-006. Removed: none.
- **AX-007** — Revised under scope-change amendment `{AMENDMENT_ID}` (accepted snapshot `projects/chirality-app-v4/execution/_ScopeChange/{AMENDMENT_SNAPSHOT}`). No owner decision changes this contract's scope: the revision names the receivers of this supplier boundary that their own registers already declare, states the harness-capability supply that `DEL-02-01` already receives, and points to the dated observation records. Revised: CLM-004, CLM-005 and TBD-002. Added: AX-007. Removed: none.
```

---

## DEL-01-02 — Durable execution and request recovery

REVISION_SCOPE: CLM-001 (interfaces sentence); CLM-002 (first sentence);
CLM-004 (last sentence); OUT-004 (last sentence); REQ-001 (first sentence);
REQ-002 (first sentence); REQ-003 (last sentence); REQ-004 (after the first
sentence); REQ-005 (after the second sentence); REQ-006 (first sentence);
AC-002; AC-006; VER-002; VER-006; TBD-001; TBD-003; new AX-004.
ScopeChanging: YES (K-4 quit; R17-3 three operations; L-1 one child per home).

Not changed, and still true under the revision: the Purpose table's "explicit
stop act", CLM-001's "explicit stop", OUT-002's "explicit stopping" and
REQ-009. Read with the revised REQ-002 they mean the person's turn interrupt
(RECOVERY-v0.2 §2 DEF-3); the ledger proposes no change there, so REVISE
leaves them.

#### G-0102-01 · CLM-001, interfaces sentence · SC3-01-02-8 with its C1-A completion · Q-4 (per clause)
Target: DEL-01-02
Trace: P3RUN C1-A SC3-01-02-8, verbatim, with the completion clause for the adopted F0 rows NR-01, NR-02, NR-04 (ledger: INCLUDE) and without DEL-09-09 (NR-03 DROP, R22-4). The bracket texts come from C1-A (DEL-02-03, DEL-03-03) and from the NR-04 row ("stop and run-end definitions; App-start reconciliation"; ARC_EFFECT §1.1). Grounds the mirrors R3-01-02-a, -b (admitted arcs DEP-01-03-012, DEP-09-02-010) and R3-01-02-e, -f, -h (mirrors of the new admitted arcs NR-01, NR-02, NR-04). R17-10 guard: every name added here is a receiver; DEL-01-02 consumes none of them.
If declined (Q-4, per arc): delete the `DEL-02-03`, `DEL-03-03` or `DEL-02-02` clause of a dropped arc and adjust the list.
```old
Its interfaces consume App-v4 `DEL-01-01`, serve App-v4 `DEL-01-04`, and hand compact evidence to PKG-04 without making a transcript copy authoritative.
```
```new
Its interfaces consume App-v4 `DEL-01-01`, serve App-v4 `DEL-01-04`, `DEL-01-03` and `DEL-09-02`, and also `DEL-02-03` (run tags and custody events), `DEL-03-03` (in-flight items and the relaunch fact) and `DEL-02-02` (the definitions of a turn interrupt, a run end and a Codex stop, and App-start reconciliation), each of which declares it upstream in its own register, and hand compact evidence to PKG-04 without making a transcript copy authoritative.
```

#### G-0102-02 · CLM-002, first sentence · SC3-01-02-9 · Q-2
Target: DEL-01-02
Trace: DECISION-L L-1 (one Codex process per App home); R19-4. Verbatim.
```old
Main-process ownership of the Codex child, protocol session and outstanding-request register is fixed.
```
```new
Main-process ownership of each Codex child (one per App-owned Codex home), its protocol session and outstanding-request register is fixed.
```

#### G-0102-03 · CLM-004, last sentence · SC3-01-02-5 · Q-2
Target: DEL-01-02
Trace: FI DECISION-1 D2/D3; ACT-v0.9 §10.1 V-21 (DEL-04-01 carries them; DEP-01-02-021); SCA-V4-002 IMPACT V-4 (overtaken). C1-A's text with the full decision identity, plus "OI-001/OI-002 stay open beyond this scope" so that CLM-004 and TBD-003 read alike. `DEL-04-01` is already a supplier (DEP-01-02-021, admitted). REQ-009 cites CLM-004; no owner it names is removed.
```old
Professional reliance remains the human's act, and no blanket reserved-act/classifier policy has been settled.
```
```new
Professional reliance remains the human's act. For this scope the reserved acts (`APP-V4-FIRST-INCREMENT-20260928-DECISION-1` D2) and the person's own tool-permission and sandbox modes (D3) are adopted and carried by App-v4 `DEL-04-01`; no App rule answers a tool-permission request affirmatively, and OI-001/OI-002 stay open beyond this scope.
```

#### G-0102-04 · OUT-004, last sentence · SC3-01-02-7 (output half) · Q-2 · drafted (P2-A)
Target: DEL-01-02
Trace: ledger locus "REQ-006; OUT-004". The full source sentence goes into REQ-006 (G-0102-11); OUT-004 gets its output-side half, so the sentence is not stated twice. Grounds: R9-7; R17-4; RECOVERY-v0.2 §8.2 ("DEL-01-02 writes nothing in DEL-04-03's format (R17-10 …)"; "Settlements by the person, by App rules and by the supplier stay DEL-01-01 → DEL-04-03 directly (R9-7)"). Both names are existing neighbours (DEP-01-02-018, DEP-01-02-020).
```old
it creates no competing authoritative transcript or new human-act schema.
```
```new
it creates no competing authoritative transcript or new human-act schema. Supplier facts reach `DEL-04-03` directly from `DEL-01-01`; this slice hands over only its own custody observations, in its own format.
```

#### G-0102-05 · REQ-001, first sentence · SC3-01-02-9 · Q-2
Target: DEL-01-02
Trace: as G-0102-02 ("REQ-001 likewise").
```old
- **REQ-001** — Keep the Codex child, protocol session and outstanding-request register in the main process.
```
```new
- **REQ-001** — Keep each Codex child (one per App-owned Codex home), its protocol session and outstanding-request register in the main process.
```

#### G-0102-06 · REQ-002, first sentence · SC3-01-02-1 · Q-2
Target: DEL-01-02
Trace: R17-3; R20-1; RECOVERY-v0.2 §2 DEF-3…DEF-6. Verbatim. Pairs SC3-01-04-7 (G-0104-06).
```old
- **REQ-002** — Support native interruption as an explicit act and preserve its actual observed result.
```
```new
- **REQ-002** — Support the person's interruption of a turn as an explicit act and preserve its actual observed result. Interrupting a turn, ending a workflow run and stopping the Codex process are distinct operations; an interrupt, a quit or a supplier exit never ends a run.
```

#### G-0102-07 · REQ-002, after G-0102-06's sentence · SC3-01-02-10 · Q-11 (optional)
Target: DEL-01-02
Trace: R18-1 C-13; R18-7 G-4; RECOVERY-v0.2 §2 DEF-3 (cause *cancel-answer*), §8.1 (`itemsNotCompleted`). Verbatim. Anchored on the sentence that follows, so it is independent of G-0102-06.
If declined: drop this block.
```old
A stop request, its transmission and an observed interruption are distinguishable;
```
```new
A turn ended by Codex after the person's cancel answer to a tool-permission request is recorded with that cause; items a turn opened and did not complete are stated as not completed. A stop request, its transmission and an observed interruption are distinguishable;
```

#### G-0102-08 · REQ-003, last sentence · SC3-01-02-4 · Q-2
Target: DEL-01-02
Trace: R17-9; RECOVERY-v0.2 §6, §2 DEF-5 (`request_ended_unanswered`). Verbatim. Pairs SC3-01-04-3 (G-0104-05).
```old
silence, timeout, reconnection and restart shall never grant approval. Sources: SOW-063, SOW-064, SOW-122; CLM-002 and CLM-004.
```
```new
silence, timeout, reconnection and restart shall never grant approval. No pending request is declined automatically after a period; a request still pending when the Codex process stops ends unanswered and is never answered afterwards. Sources: SOW-063, SOW-064, SOW-122; CLM-002 and CLM-004.
```

#### G-0102-09 · REQ-004, after the first sentence · SC3-01-02-11 · Q-11 (optional)
Target: DEL-01-02
Trace: RECOVERY-v0.2 §1; HOSTING-v0.9 §6.5; pass-2 C1-B §5.1 (U-14). Verbatim. A clarification: no requirement is weakened (OUT-001 still lists "unknown-request errors" among the custody code's handling).
If declined: drop this block and remove REQ-004 from AX-004's Revised list.
```old
- **REQ-004** — Return an explicit error for an unknown server request using the supplied protocol boundary.
```
```new
- **REQ-004** — Return an explicit error for an unknown server request using the supplied protocol boundary. The explicit error is written at receipt by the boundary of App-v4 DEL-01-01; this slice records its result and keeps it in custody across observation loss and relaunch.
```

#### G-0102-10 · REQ-005, after the second sentence · SC3-01-02-3 with its C1-A completion · Q-2
Target: DEL-01-02
Trace: DECISION-K3 K-4; R18-1 C-12; RECOVERY-v0.2 §2 DEF-5a, DEF-6. Verbatim, with the completion clause C1-A recommends (pairs SC3-01-04-7's Stop Codex / Restart Codex clause).
```old
support continuation of the conversation with access to what happened previously.
```
```new
support continuation of the conversation with access to what happened previously. When the person quits with live turns or pending requests, the App asks first and lists them; on confirmation the live turns are interrupted and recorded as interrupted by quit, and after relaunch they are shown with an offer to resume. The same applies when the person stops or restarts Codex from the App.
```

#### G-0102-11 · REQ-006, first sentence · SC3-01-02-7 · Q-2
Target: DEL-01-02
Trace: R9-7; R17-4; RECOVERY-v0.2 §7, §8.2. Verbatim. R17-10 guard: `DEL-04-03` is named as the receiver of supplier facts from `DEL-01-01`; DEL-01-02 consumes nothing from it (DEP-01-02-020 is DOWNSTREAM).
```old
- **REQ-006** — Supply observed events and explicitly unknown outcomes to the receiving UI and compact-evidence interface.
```
```new
- **REQ-006** — Supply observed events and explicitly unknown outcomes to the receiving UI and compact-evidence interface. Supplier facts (supplied guidance, model destination, tool-permission settlements) reach App-v4 DEL-04-03 directly from App-v4 DEL-01-01; this slice hands its own custody observations in its own format and keeps across relaunch only references and App-observed facts, never a copy of conversation content.
```

#### G-0102-12 · AC-002, first sentence · SC3-01-02-2 · Q-2
Target: DEL-01-02
Trace: R17-3. Verbatim.
```old
- **AC-002** — An explicit native stop is distinguishable from observation loss, and
```
```new
- **AC-002** — An explicit turn interrupt is distinguishable from observation loss and from a run end, and
```

#### G-0102-13 · AC-006 · SC3-01-02-3 · Q-2
Target: DEL-01-02
Trace: DECISION-K3 K-4. Verbatim.
```old
while recovered, currently outstanding and unavailable facts remain distinguishable. Verify the continuation part of REQ-005 with VER-006.
```
```new
while recovered, currently outstanding and unavailable facts remain distinguishable, including turns interrupted by a confirmed quit. Verify the continuation part of REQ-005 with VER-006.
```

#### G-0102-14 · VER-002, first sentence · SC3-01-02-2 · Q-2
Target: DEL-01-02
Trace: R17-3. Verbatim.
```old
- **VER-002** — Invoke native stop deliberately and trace the request and observed provider result.
```
```new
- **VER-002** — Interrupt a turn deliberately and trace the request and observed provider result.
```

#### G-0102-15 · VER-006, first sentence · SC3-01-02-3 · Q-2
Target: DEL-01-02
Trace: DECISION-K3 K-4. Verbatim.
```old
- **VER-006** — Quit and relaunch the identified native App, then continue the conversation
```
```new
- **VER-006** — Quit with live work, confirm the question, relaunch the identified native App, then continue the conversation
```

#### G-0102-16 · new AX-004 (amendment reference) · acceptance-conditional
Target: DEL-01-02
```old
Sources: CLM-005; [Operating method][operating] V4-OPS-31…34.
```
```new
Sources: CLM-005; [Operating method][operating] V4-OPS-31…34.
- **AX-004** — Revised under scope-change amendment `{AMENDMENT_ID}` (accepted snapshot `projects/chirality-app-v4/execution/_ScopeChange/{AMENDMENT_SNAPSHOT}`), applying `APP-V4-FIRST-INCREMENT-20260928-DECISION-1` D2, D3 and D4 (record `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-FIRST-INCREMENT-20260928/OWNER_DECISIONS.md`) and `APP-V4-DESIGN-PASS-3-20261001-DECISION-K3` K-4 and `APP-V4-DESIGN-PASS-3-20261001-DECISION-L` L-1 and L-7 (record `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-DESIGN-PASS-3-20261001/OWNER_DECISIONS.md`), with that design pass's recorded integrator rulings R17-3, R17-4, R17-5, R17-9, R18-1, R18-7 and R22-4 (`R17_RESOLUTIONS.md`, `R18_RESOLUTIONS.md` and `R22_RESOLUTIONS.md` in the same run folder). Revised: CLM-001, CLM-002, CLM-004, OUT-004, REQ-001, REQ-002, REQ-003, REQ-004, REQ-005, REQ-006, AC-002, AC-006, VER-002, VER-006, TBD-001 and TBD-003. Added: AX-004. Removed: none.
```

#### G-0102-17 · TBD-001 (OI-012 sentence) · SC3-01-02-6 with its C1-A completion · Q-2
Target: DEL-01-02
Trace: FI DECISION-1 D4; DECISION-L L-7; R17-5 (OI-008 option O-1, PROPOSED; HOSTING-v0.9 §12 "Nothing here is selected", read). The source says "Append"; the OI-012 sentence it would follow ("leaves the supplier pin to that owner before protocol generation/qualification") is overtaken by D4 for generation, so it is replaced rather than left beside the new text, as SCA-V4-002 did for DEL-01-04 TBD-004. One wording across the D4-pin class (SC3-01-03-1, SC3-01-05-3). "That owner" is the App implementation owner of the preceding OI-008 sentence.
```old
OI-012 leaves the supplier pin to that owner before protocol generation/qualification.
```
```new
For OI-012, owner decision `APP-V4-FIRST-INCREMENT-20260928-DECISION-1` D4 selected Codex 0.158.0 as the definition and generation pin, not a qualification; the pin used for qualification remains with that owner before qualification, and the Owner is also the App implementation owner (`APP-V4-DESIGN-PASS-3-20261001-DECISION-L` L-7). OI-008's main-process division is proposed as option O-1 in App-v4 DEL-01-01's hosting design (HOSTING §12), not selected.
```

#### G-0102-18 · TBD-003, first sentence · SC3-01-02-5 · Q-2
Target: DEL-01-02
Trace: FI DECISION-1 D2/D3; ACT-v0.9 §10.1 V-21. Enables R3-01-02-c. The remaining sentences of TBD-003 stay true ("This contract neither adopts an always-reserved list nor a classifier mode": the adoption is the owner's).
```old
- **TBD-003** — OI-001/OI-002 remain with the owner and App/SWB contract owners at the operation-policy/permission-implementation point of need.
```
```new
- **TBD-003** — OI-001/OI-002: for this scope, owner decisions `APP-V4-FIRST-INCREMENT-20260928-DECISION-1` D2 (reserved acts) and D3 (the person's own tool-permission and sandbox modes) apply, as App-v4 DEL-04-01's operation-policy contract carries them (ACT §10.1 V-21); beyond this scope OI-001/OI-002 stay open with the owner and App/SWB contract owners at the operation-policy/permission-implementation point of need.
```

---

## DEL-01-03 — Native plans, tools and delegation views

REVISION_SCOPE: CLM-003 (receivers sentence appended); CLM-004 (last
sentence); REQ-001; REQ-003; REQ-004; REQ-005; AC-001; AX-002; TBD-001;
TBD-003; new AX-004. ScopeChanging: YES (K-5 usable without experimental
surfaces; K-10 display). REQ-007 ("decide the unresolved reserved-act/classifier
policy") stays: the residue beyond this scope is still unresolved.

#### G-0103-01 · CLM-003, after "…decision views." · SC3-01-03-8 · Q-2
Target: DEL-01-03
Trace: P3RUN C1-A SC3-01-03-8, verbatim; NPTD-v0.2 §10.2, §16.3; F0 §3 NR-05, M-3. Grounds R3-01-03-a…c (mirrors of DEP-06-01-007, DEP-09-02-011, DEP-09-05-008, admitted) and R3-01-03-d (mirror of the new admitted arc NR-05, DEL-01-04 → DEL-01-03). R17-10 guard: DEL-01-04 and DEL-06-01 are named as receivers only; DEL-01-03 consumes neither. REQ-007 cites CLM-003; it names neither DEL-06-01 nor DEL-09-0x, and its existing owners stay named.
```old
it owns work-graph, return, waiting and decision views.
```
```new
it owns work-graph, return, waiting and decision views. This slice's plan-mode element, item anchors and delegation availability are received by App `DEL-01-04`, which composes turns and request cards from them; its delegation identities are received by App `DEL-06-01`; and its views and checks are received by `DEL-09-02` and `DEL-09-05` before their witnesses. Each declares it upstream in its own register.
```

#### G-0103-02 · CLM-004, last sentence · SC3-01-03-2 · Q-2
Target: DEL-01-03
Trace: FI DECISION-1 D2/D3 (overtaken). C1-A gives the substance ("decided for this scope by owner decisions D2 (reserved acts) and D3 (routine tool permission is the person's Codex setting); the rows stay OPEN for wider scope"); the sentence keeps CLM-004's owner for the residue, which REQ-007 and TBD-003 still cite.
```old
Exact always-reserved classes and classifier policy remain decisions of the owner with affected App/host contract owners, not decisions made by this presentation slice.
```
```new
For this scope the owner decided them by `APP-V4-FIRST-INCREMENT-20260928-DECISION-1` D2 (reserved acts) and D3 (routine tool permission is the person's own Codex setting); any always-reserved class or classifier matter beyond that ruling remains a decision of the owner with affected App/host contract owners, not a decision made by this presentation slice.
```

#### G-0103-03 · REQ-001, appended · SC3-01-03-4 · Q-2
Target: DEL-01-03
Trace: R17-4; R18-1 C-03; NPTD-v0.2 RV-4, CL-06/07. Verbatim.
```old
preserving the required plan behavior while leaving registry storage and implementation open. Sources:
```
```new
preserving the required plan behavior while leaving registry storage and implementation open. Plan revisions Codex does not keep in its history are not copied; after a relaunch or a supplier restart they are shown as not recoverable, while plan items are recovered from Codex history. Sources:
```

#### G-0103-04 · REQ-003, appended · SC3-01-03-5 · Q-2
Target: DEL-01-03
Trace: DECISION-K3 K-10 as revised ("stated, not enforced"; "the App does not override the user's Codex configuration"); NPTD-v0.2 DR-4. Verbatim. Same substance as SC3-02-04-4 in DEL-02-04 (part B); one wording in each SoW, as the ledger recommends.
```old
A completed primary turn shall not imply that active descendants completed, returned, were reviewed or were integrated. Sources:
```
```new
A completed primary turn shall not imply that active descendants completed, returned, were reviewed or were integrated. Delegation by a task agent is recorded and shown, labelled "stated, not enforced"; the App does not override the person's Codex configuration to prevent it. Sources:
```

#### G-0103-05 · REQ-004, appended · SC3-01-03-6 · Q-2
Target: DEL-01-03
Trace: DECISION-K3 K-5 as narrowed by R18-1 C-05 (only plan mode is labelled experimental). Verbatim; placed in REQ-004 (the ledger's first option), whose subject is the supplier basis the views use.
```old
it does not select a pin or prescribe a checker. Sources:
```
```new
it does not select a pin or prescribe a checker. Experimental supplier surfaces the views use (at 0.158.0, plan mode) are labelled "experimental" where they appear; the App remains fully usable without them, the corresponding views being absent. Sources:
```

#### G-0103-06 · REQ-005, appended · SC3-01-03-3 and SC3-01-03-7 · Q-2
Target: DEL-01-03
Trace: DECISION-K1 K1-4 (NPTD §9 TA-4); R17-9 (NPTD §5.5). Both verbatim.
```old
No universal ordering requiring proposal acceptance before another independently evidenced act is imposed. Sources: P V4-AUT-01…05 and V4-REC-03/05; H decision 03; I V4-HI-30…33.
```
```new
No universal ordering requiring proposal acceptance before another independently evidenced act is imposed. An act the App captures names the person as observed, marked "identity not verified". An instruction to carry out a plan is ordinary conversation input, not a reserved act, unless a workflow checkpoint names an act. Sources: P V4-AUT-01…05 and V4-REC-03/05; H decision 03; I V4-HI-30…33.
```

#### G-0103-07 · AC-001 · SC3-01-03-4 · Q-2 · drafted (P2-A)
Target: DEL-01-03
Trace: ledger locus "REQ-001; AC-001"; the source gives one sentence for both. The criterion form restates it observably.
```old
with the required behavior preserved irrespective of the assessed registry implementation. Verify using VER-001.
```
```new
with the required behavior preserved irrespective of the assessed registry implementation. After a relaunch or a supplier restart, plan revisions Codex did not keep are shown as not recoverable and plan items are recovered from Codex history. Verify using VER-001.
```

#### G-0103-08 · AX-002, third sentence · SC3-01-03-2 · Q-2
Target: DEL-01-03
Trace: FI DECISION-1 D2/D3.
```old
OI-001/002 remain open; carrying policy or records does not make this deliverable the policy decision actor.
```
```new
OI-001/002 are decided for this scope by owner decisions D2 and D3 of `APP-V4-FIRST-INCREMENT-20260928-DECISION-1` and stay open for wider scope; carrying policy or records does not make this deliverable the policy decision actor.
```

#### G-0103-09 · new AX-004 (amendment reference) · acceptance-conditional
Target: DEL-01-03
```old
Actual product input, candidate examination, owner validation and any later lifecycle act need their own evidence. Sources: M approved setup; E §1.
```
```new
Actual product input, candidate examination, owner validation and any later lifecycle act need their own evidence. Sources: M approved setup; E §1.
- **AX-004** — Revised under scope-change amendment `{AMENDMENT_ID}` (accepted snapshot `projects/chirality-app-v4/execution/_ScopeChange/{AMENDMENT_SNAPSHOT}`), applying `APP-V4-FIRST-INCREMENT-20260928-DECISION-1` D2, D3 and D4 (record `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-FIRST-INCREMENT-20260928/OWNER_DECISIONS.md`), `APP-V4-DESIGN-PASS-2-20260930-DECISION-K1` K1-4 (record `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-DESIGN-PASS-2-20260930/OWNER_DECISIONS.md`) and `APP-V4-DESIGN-PASS-3-20261001-DECISION-K3` K-5 and K-10 as revised and `APP-V4-DESIGN-PASS-3-20261001-DECISION-L` L-7 (record `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-DESIGN-PASS-3-20261001/OWNER_DECISIONS.md`), with that design pass's recorded integrator rulings R17-4, R17-9 and R18-1 (`R17_RESOLUTIONS.md` and `R18_RESOLUTIONS.md` in the same run folder). Revised: CLM-003, CLM-004, REQ-001, REQ-003, REQ-004, REQ-005, AC-001, AX-002, TBD-001 and TBD-003. Added: AX-004. Removed: none.
```

#### G-0103-10 · TBD-001, appended after the first sentence · SC3-01-03-1 · Q-2
Target: DEL-01-03
Trace: FI DECISION-1 D4; DECISION-L L-7; P3RUN D2 §6 and R2.4. Verbatim, with the full decision identities. Enables R3-01-03-f.
```old
supplied through App DEL-01-01 before protocol generation and qualification.
```
```new
supplied through App DEL-01-01 before protocol generation and qualification. Owner decision `APP-V4-FIRST-INCREMENT-20260928-DECISION-1` D4 selected Codex 0.158.0 as the definition and generation pin, not a qualification; qualification remains with the Owner, who is also the App implementation owner (`APP-V4-DESIGN-PASS-3-20261001-DECISION-L` L-7), through DEL-01-01 (OI-012).
```

#### G-0103-11 · TBD-003, first sentence · SC3-01-03-2 · Q-2
Target: DEL-01-03
Trace: FI DECISION-1 D2/D3. Enables R3-01-03-e (DEP-01-03-017 refreshed to the OI-001 residue).
```old
- **TBD-003** — Exact always-reserved acts and classifier permissions remain with the owner and affected App/SWB contract owners (OI-001/002), before the affected operation-policy contract or permission implementation.
```
```new
- **TBD-003** — For this scope, always-reserved acts and classifier permissions are decided by owner decisions D2 (reserved acts) and D3 (routine tool permission is the person's own Codex setting) of `APP-V4-FIRST-INCREMENT-20260928-DECISION-1`; beyond this scope they remain with the owner and affected App/SWB contract owners (OI-001/002, whose rows stay OPEN), before the affected operation-policy contract or permission implementation.
```

---

## DEL-01-04 — Native requests, outcomes and attachments

REVISION_SCOPE: CLM-001 (two appended sentences); CLM-004 (one appended
sentence); OUT-002 (appended clause); REQ-001, REQ-002, REQ-005 (appended
sentences); REQ-006 (the `DEL-02-02` clause); VER-005 (positive case); new
OUT-005, REQ-008, AC-008, VER-008 and one matrix row; new AX-005.
ScopeChanging: **YES** (the App act control, K1-4 and K-8).

#### G-0104-01 · CLM-001, after "…assigned to App `DEL-01-03`." · SC3-01-04-13 and SC3-01-04-5 (claim half) · Q-2, Q-4
Target: DEL-01-04
Trace: SC3-01-04-13 verbatim (DEP-09-02-012 has no mirror; grounds R3-01-04-b). SC3-01-04-5's ledger locus is "OUT-002; CLM-001": the full clause goes into OUT-002 (G-0104-03); CLM-001 gets a short pointing sentence, **drafted (P2-A)**. R17-7; NIR-v0.2 §9. Grounds NR-08 (DEL-01-04 → DEL-04-02) and NR-09 (DEL-01-04 → DEL-02-03), both new held arcs inside SCC-002.
If declined (Q-4, NR-08 or NR-09): delete the second sentence here and the OUT-002 clause of G-0104-03 (or only the dropped deliverable's name).
```old
with the plan/tool/delegation contribution assigned to App `DEL-01-03`.
```
```new
with the plan/tool/delegation contribution assigned to App `DEL-01-03`. This slice's native interaction view and scoped request/outcome checks are received by App `DEL-09-02` before its joined request witness, as `DEL-09-02` declares in its own register. In the App, this slice also places the checkpoint and standing display that App `DEL-04-02` and App `DEL-02-03` define (OUT-002).
```

#### G-0104-02 · CLM-004, appended · SC3-01-04-2 (claim half) · Q-2
Target: DEL-01-04
Trace: DECISION-K3 K-8; AAC-v0.2 §4.2 and AK-f ("the registration that follows is DEL-02-02's operation"). Ledger locus "REQ-006 DEL-02-02 clause; CLM-004"; C1-A gives the REQ-006 text (G-0104-08); this CLM-004 sentence is its claim-side statement, **drafted (P2-A)**. Pairs SC3-02-02-4 (part B). Names no new deliverable.
If Q-5 is declined: drop this block (it presupposes the act control).
```old
This slice supplies native attachment and draft-transition receiving interactions to that owner.
```
```new
This slice supplies native attachment and draft-transition receiving interactions to that owner. The person's act registering a reviewed revision (A15) is captured through this slice's App act control; the registration that follows is App `DEL-02-02`'s operation.
```

#### G-0104-03 · OUT-002, appended clause · SC3-01-04-5 · Q-4
Target: DEL-01-04
Trace: R17-7; NIR-v0.2 §9. C1-A's text, verbatim. Grounds NR-08 and NR-09.
If declined (Q-4): as G-0104-01.
```old
including the local attachment/draft transition surface used by the workflow workspace. Scope: SOW-129.
```
```new
including the local attachment/draft transition surface used by the workflow workspace, and the App's placement of the checkpoint overlay and standing facets defined by App `DEL-04-02`, with the checkpoint display meanings of App `DEL-02-03`, whose behaviour in the App this slice owns. Scope: SOW-129.
```

#### G-0104-04 · new OUT-005 · SC3-01-04-1 · Q-5 · drafted (P2-A)
Target: DEL-01-04
Trace: SC3-01-04-1 asks for the new REQ "with matching OUT, AC, VER" (P3RUN C1-A; pass-2 C1-A SC2-01-04-1). The output follows the anticipated-artifact form of OUT-001…OUT-004 and AAC-v0.2 §0, §5. Scope: SOW-129 ("draft … interactions under the accepted contract"), the reference the act control's A15 case and act presentation (REQ-005) already serve; the frontmatter is unchanged. Basis: CLM-004 (A15 registration, G-0104-02) and CLM-005 (act distinctions and the record owner).
```old
This is the native contribution to the full workflow workspace owned by App DEL-02-02.
```
```new
This is the native contribution to the full workflow workspace owned by App DEL-02-02.
- **OUT-005** — CODE: The App act control of REQ-008, with its offer, capture evidence and direct-capture record written through the evidence-record owner's writer, and the person's identity as the App observes it. Scope: SOW-129. Objectives: OBJ-001, OBJ-002. Basis: CLM-004, CLM-005; H and W; `APP-V4-DESIGN-PASS-2-20260930-DECISION-K1` K1-4 and `APP-V4-DESIGN-PASS-3-20261001-DECISION-K3` K-8.
```

#### G-0104-05 · REQ-001, appended · SC3-01-04-3, SC3-01-04-12, SC3-01-04-10 · Q-2, Q-4
Target: DEL-01-04
Trace: SC3-01-04-3 verbatim (R17-9; NIR §4.2–§4.4; pairs SC3-01-02-4). SC3-01-04-12 verbatim (R18-1 C-24; NIR §4.8). SC3-01-04-10 verbatim (R18-1 C-06; R19-7; NIR §5.6), plus "and run-end line", which C1-A asks P2 to consider: NIR §5.6 TC-2 places "DEL-02-02's run-end line" in the composed turn (R20-3; WR-v0.2 §16.2 TX-5), and the ledger's R3-01-04-a refreshes DEP-01-04-009 with "the run-start text and run-end line". Ledger locus "OUT-001 / REQ-001": REQ-001 taken. Grounds NR-05 (DEL-01-04 → DEL-01-03, new admitted); `DEL-02-02` is the existing held arc DEP-01-04-009.
If declined (Q-4, NR-05): delete "the collaboration mode supplied by App `DEL-01-03` (sent explicitly after plan mode was used) and".
```old
A translated Chirality event vocabulary shall not replace native requests. Basis: SOW-005/SOW-014; N, R; CLM-002 and CLM-003.
```
```new
A translated Chirality event vocabulary shall not replace native requests. Where a request lists the answer forms it accepts, only those are offered. The explicit decline is the request's own negative form or, for a kind that has none, the native empty answer this slice's design names. No App rule declines a waiting request after any period, and a request the supplier resolves itself is shown as resolved by the supplier, never as an answer. The App shows how many requests wait for the person's answer, also when no conversation window is open. This slice composes the turns it sends, including the collaboration mode supplied by App `DEL-01-03` (sent explicitly after plan mode was used) and the run-start text and run-end line supplied by App `DEL-02-02`. Basis: SOW-005/SOW-014; N, R; CLM-002 and CLM-003.
```

#### G-0104-06 · REQ-002, appended · SC3-01-04-7, SC3-01-04-6, SC3-01-04-11 · Q-2, Q-4
Target: DEL-01-04
Trace: SC3-01-04-7 verbatim with C1-A's optional clause (R17-3; R18-1 C-12; NIR §5.2; pairs the SC3-01-02-3 completion). SC3-01-04-6 as amended at C1-A, verbatim (DECISION-K3 K-3; R18-2's two wordings; K1-4; NIR §5.4, IF-10; AAC §7). SC3-01-04-11 as amended at C1-A, verbatim (DECISION-L L-2; R19-2, R19-3; R20-1, R20-9; NIR §5.4, §5.7, §5.8; adopted by R22-1). Grounds NR-07 (DEL-01-04 → DEL-01-05, new admitted) and NR-4 (DEL-01-04 → DEL-02-04, new held). `DEL-01-02` is the existing admitted arc DEP-01-04-008.
If declined (Q-4): NR-07 — delete ", from the selection state App DEL-01-05 reports" and the sentence "The Codex account App DEL-01-05 reports …"; NR-4 — replace "the roles App DEL-02-04 lists, with the registry's default" by "the roles available, with the default".
```old
without synthesizing completion or interruption. Basis: SOW-129; R; CLM-003.
```
```new
without synthesizing completion or interruption. Interrupting a turn, ending a run and stopping the Codex process are shown as distinct, as App DEL-01-02 defines them; an interrupted turn is never shown as an ended run. The App offers Stop Codex and Restart Codex, each asking first when work is live. A new conversation shows that no model is selected until the person chooses one, from the selection state App DEL-01-05 reports; the person's last explicit choice for the project may be offered, and is never applied without the person's choice. A workflow run that cannot start for want of a model reads "run not started — no model selected"; an ordinary conversation reads "not started — no model selected". The Codex account App DEL-01-05 reports is the one used for the person's identity at act capture. A new conversation offers the roles App DEL-02-04 lists, with the registry's default preselected and clearable and no role allowed; the role is fixed for the conversation, and a different role opens a new conversation with a handoff summary the person can edit. An agent's proposal of the next workflow is offered for the person to confirm and starts nothing by itself. An agent's report that the workflow finished is offered as the person's "End run" and ends nothing by itself. Basis: SOW-129; R; CLM-003.
```

#### G-0104-07 · REQ-005, appended · SC3-01-04-4 · Q-2
Target: DEL-01-04
Trace: DECISION-K1 K1-1, K1-2, K1-3, K1-4; NIR §8, §9; AAC AK-a, AK-b. Verbatim.
```old
Where bound content changes, display the lapsed standing supplied by the evidence interface. Basis:
```
```new
Where bound content changes, display the lapsed standing supplied by the evidence interface. The agent carrying out a workflow asks the person for a checkpoint's act; this slice offers the means to act as a standing facility and raises nothing because an arrival was recorded. An earlier act of the required kind on still-current content is shown as counting, with its time, and several acts may answer one arrival together. The person who acted is shown as the App observes them, marked identity not verified. Basis:
```

#### G-0104-08 · REQ-006, `DEL-02-02` clause · SC3-01-04-2 · Q-2
Target: DEL-01-04
Trace: DECISION-K3 K-8; AAC §4.2. C1-A's text verbatim, with "; the person's registration act …" joined by "while" because the clause sits inside REQ-006's semicolon list. Boundary check: no owner token is added or removed (`DEL-02-02` still resolves to CLM-004).
If Q-5 is declined: keep the first change ("the registration of a reviewed revision into the library") and delete the "while …" clause.
```old
the complete workflow-making workspace, reviewed registration and catalog selection belong to App `DEL-02-02` in CLM-004;
```
```new
the complete workflow-making workspace, the registration of a reviewed revision into the library and catalog selection belong to App `DEL-02-02` in CLM-004, while the person's registration act (A15) is captured by this slice's App act control;
```

#### G-0104-09 · new REQ-008 (the App act control) · SC3-01-04-1 · Q-5 · one sentence adjusted (P2-A)
Target: DEL-01-04
Trace: P3RUN C1-A "SC3-01-04-1, full text as amended here", verbatim except the "Consumers:" sentence, and with the closing OI-008 sentence that C1-A states after the quotation, written as part of the requirement. Grounds: DECISION-K1 K1-4; DECISION-K3 K-8; R17-2, R17-6; R21-3 (one act from one descriptor; several drafts are several acts); AAC-v0.2 §0, §1, AI-2, AK-d. Supersedes pass-2 SC2-01-04-1 (DROP).
**Adjusted (P2-A):** the source ends "Consumers: `DEL-02-02` (A15), `DEL-02-03` (App-side positive capture fixtures), `DEL-04-03`, `DEL-04-01`." AAC-v0.2 §2 shows DEL-04-01 and DEL-04-03 as *suppliers* to the control (AI-4: act wording, record kinds and act class "DEL-04-01 → the control (DEP-01-04-011, admitted)"; AI-7: "The control → DEL-04-03's writer (DEP-01-04-012, held)"), and SC2-04-03-1 (part B) names DEL-01-04 among DEL-04-03's consumers. DAG-003 has DEL-01-04 → DEL-04-01 and DEL-01-04 → DEL-04-03 and no arc the other way (checked in both edge files). Extracted as written, "consumers" would yield DOWNSTREAM rows DEL-04-01 → DEL-01-04 (against the guard "DEL-04-01 gains no supplier", and a new cycle pulling DEL-04-01 into SCC-002) and DEL-04-03 → DEL-01-04 (a held arc ARC_EFFECT does not count). The adjusted sentence keeps DEL-02-02 and DEL-02-03 as users (mirrors of DEP-02-02-013 and DEP-02-03-027; the latter is R2-01-04-a) and states the two supplier relations the design records. **Alternative (source wording):** replace the adjusted sentence by the source sentence above and add an extraction guard that `DEL-04-03` and `DEL-04-01` yield no DOWNSTREAM row. The owner chooses at Q-5.
If declined (Q-5): drop G-0104-04, -09, -10, -12 and -14, and the dependent clauses named under G-0104-02 and G-0104-08; G-0104-11's "through the App act control" stays only if another construction is named; remove the new IDs from AX-005.
```old
It shall not claim an adopted pin, fulfilled input, agreed common component or implemented capability solely from this definition. Basis: C; CLM-006; O.
```
```new
It shall not claim an adopted pin, fulfilled input, agreed common component or implemented capability solely from this definition. Basis: C; CLM-006; O.
- **REQ-008** — Provide the App act control: a dedicated control that only the person can operate — no agent tool, MCP operation, App rule, supplier request or interface script can operate it or produce its record — for one act kind at a time on App content. It covers App files and outputs, and A12 where an App control establishes the setting. It also covers A15 (register workflow revision), either on one reviewed workflow draft or on two or more library entries registered in place in one act. A15 is presented from one descriptor of the workflow workspace and bound to the exact reviewed content of each entry, so that a draft or entry changed after review needs a new review. The control shows the act kind in its canonical wording, the bound subject with its content identity, the declared scope and purpose, the actor requirement and the arrival it answers. It offers the decline where an act-declined event exists. Operating it produces capture evidence and a direct-capture human-act record in the format of DEL-04-03. It is a standing facility, available whether or not an arrival has been recorded, and no arrival raises it. It records the person's identity from what the App can observe (the name set in the App, the operating-system account, and the Codex account when Codex reports one), marked *identity not verified*. Presenting or operating it answers no pending supplier request. It is used by DEL-02-02 (A15) and DEL-02-03 (App-side positive capture fixtures), each of which declares it upstream in its own register; it takes its act wording and kinds from DEL-04-01 and writes its records through the writer of DEL-04-03, as CLM-005 states. The process placement that makes "not operable by automation" true stays with OI-008 (TBD-003). Basis: SOW-129 as qualified by the assigned PKG-04 interface; H; CLM-004, CLM-005; `APP-V4-DESIGN-PASS-2-20260930-DECISION-K1` K1-4; `APP-V4-DESIGN-PASS-3-20261001-DECISION-K3` K-8.
```

#### G-0104-10 · new AC-008 · SC3-01-04-1 · Q-5 · drafted (P2-A)
Target: DEL-01-04
Trace: the criterion form of REQ-008, in the AC-001…AC-007 pattern ("Verify by …. Grounds: …"). Its cases are AAC-v0.2 §8 VC-AAC-01, -03, -04, -05, -06, -07, -08, -09b, -12 (kinds, automation refused, positive capture, presenting answers nothing, decline, stale binding, A15 single and multi-entry, record conformance).
```old
Verify by VER-007. Grounds: OUT-003; D, R and W.
```
```new
Verify by VER-007. Grounds: OUT-003; D, R and W.
- **AC-008** — On the identified candidate, the App act control is offered for the act kinds that have App content and for A15 on one reviewed draft or on several library entries in one act, showing the canonical wording, bound subject and content identity, scope, purpose, actor requirement and any arrival. Only the person's confirmation captures an act: operation from an agent tool, MCP operation, App rule, supplier request or interface script captures nothing, and content changed after the offer captures nothing. The decline is offered only where an act-declined event exists. Each capture yields capture evidence and a direct-capture record valid in the evidence-record format, with the person's identity marked identity not verified. No arrival raises the control, and presenting or operating it leaves every pending supplier request pending. Verify by VER-008. Grounds: REQ-008; H and CLM-005.
```

#### G-0104-11 · VER-005, positive case · SC3-01-04-8 · Q-2
Target: DEL-01-04
Trace: AAC; EXEC CH-23. Verbatim.
```old
the person actually performs the act on identified content and a separate recorder preserves it;
```
```new
the person actually performs the act on identified App content through the App act control and a separate recorder preserves it;
```

#### G-0104-12 · new VER-008 · SC3-01-04-1 · Q-5 · drafted (P2-A)
Target: DEL-01-04
Trace: AAC-v0.2 §8 (cases and their "Needs": model, candidate, person); VC-AAC-13 (native confirmation) and VC-AAC-14 (provenance) are candidate-only and not run. In the VER-001…VER-007 pattern ("Checks AC-00n only.").
```old
The fixtures substantiate this slice and do not qualify the full V4-EXM-10/V4-EXM-11 journeys alone. Checks AC-007 only.
```
```new
The fixtures substantiate this slice and do not qualify the full V4-EXM-10/V4-EXM-11 journeys alone. Checks AC-007 only.
- **VER-008** — On an identified App candidate, open the act control from the act log, a file or output view, a draft under review and an arrival row. Have the person confirm an act on an App file, an A15 act on one reviewed draft and an A15 act on two library entries in one act, and decline where an act-declined event exists. Attempt operation from an agent tool, an MCP operation, an App rule, a supplier request and an interface script; change the bound content after the offer; leave a question waiting while acting. Compare captures and records with the evidence-record format, the identity marking and the pending request register, and record which cases ran on a model and which on the candidate. A model check does not stand in for the person's confirmation on the candidate. Checks AC-008 only.
```

#### G-0104-13 · new AX-005 (amendment reference) · acceptance-conditional
Target: DEL-01-04
```old
Revised: CLM-005, VER-005, TBD-001, TBD-002 and TBD-004. Added: AX-004. Removed: none.
```
```new
Revised: CLM-005, VER-005, TBD-001, TBD-002 and TBD-004. Added: AX-004. Removed: none.
- **AX-005** — Revised under scope-change amendment `{AMENDMENT_ID}` (accepted snapshot `projects/chirality-app-v4/execution/_ScopeChange/{AMENDMENT_SNAPSHOT}`), applying `APP-V4-DESIGN-PASS-2-20260930-DECISION-K1` K1-1, K1-2, K1-3 and K1-4 (record `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-DESIGN-PASS-2-20260930/OWNER_DECISIONS.md`) and `APP-V4-DESIGN-PASS-3-20261001-DECISION-K3` K-3 and K-8 and `APP-V4-DESIGN-PASS-3-20261001-DECISION-L` L-2 and L-4 (record `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-DESIGN-PASS-3-20261001/OWNER_DECISIONS.md`), with that design pass's recorded integrator rulings R17-3, R17-6, R17-7, R17-9, R18-1, R18-2, R19-2, R19-3, R19-7, R20-1, R20-3, R20-9, R21-3 and R22-1 (`R17_RESOLUTIONS.md`, `R18_RESOLUTIONS.md`, `R19_RESOLUTIONS.md`, `R20_RESOLUTIONS.md` and `R22_RESOLUTIONS.md` in the same run folder). Revised: CLM-001, CLM-004, OUT-002, REQ-001, REQ-002, REQ-005, REQ-006 and VER-005. Added: OUT-005, REQ-008, AC-008, VER-008, the OUT-005 matrix row and AX-005. Removed: none.
```

#### G-0104-14 · new matrix row for OUT-005 · SC3-01-04-1 · Q-5
Target: DEL-01-04
Trace: one row per acceptance criterion, as the existing matrix; AC-008 is verified only by VER-008 (QA item 20).
```old
| OUT-003 | OBJ-001, OBJ-002 | CLM-001, REQ-001, REQ-002, REQ-003, REQ-004, REQ-005 | AC-007 | VER-007 | Delivered and executed interaction fixtures with candidate/basis identity, coverage and truthful limits. |
```
```new
| OUT-003 | OBJ-001, OBJ-002 | CLM-001, REQ-001, REQ-002, REQ-003, REQ-004, REQ-005 | AC-007 | VER-007 | Delivered and executed interaction fixtures with candidate/basis identity, coverage and truthful limits. |
| OUT-005 | OBJ-001, OBJ-002 | REQ-008, CLM-004, CLM-005 | AC-008 | VER-008 | Person-only capture on the candidate: served kinds, A15 single and multi-entry acts, automation and stale-content refusals, decline, records in the evidence-record format, identity not verified, pending requests untouched. |
```

---

## DEL-01-05 — Native OAuth/sign-in, API-key and local-provider access

REVISION_SCOPE: CLM-001 (last sentence); CLM-004 (appended sentence);
OUT-002 (appended text); REQ-002; REQ-004; REQ-005; TBD-001; TBD-002;
TBD-003; AC-004; VER-004; new REQ-010, AC-011, VER-011 and one matrix row;
new AX-006. ScopeChanging: **YES** (new REQ-010 start-up traffic; Codex-account
supply; API key in a second home).

#### G-0105-01 · CLM-001, last sentence · SC3-01-05-2 · Q-2
Target: DEL-01-05
Trace: D4 P-2, verbatim; follows G-0105-08.
```old
This does not choose a v4 account home.
```
```new
The account home is chosen under TBD-001.
```

#### G-0105-02 · CLM-004, appended · SC3-01-05-12 · Q-2
Target: DEL-01-05
Trace: C1-B §4.1 SC3-01-05-12, verbatim; ACCESS I-9, §13; DEP-09-02-013 (admitted). Grounds R3-01-05-b. REQ-009 cites CLM-004; it names no `DEL-09-02`.
```old
shared construction requires separately agreed repeated responsibility and is not assigned by this interface. [S2: DEL-01-05 and DEL-05-01; S4: DEP-001 and clarification]
```
```new
shared construction requires separately agreed repeated responsibility and is not assigned by this interface. [S2: DEL-01-05 and DEL-05-01; S4: DEP-001 and clarification] `DEL-09-02` receives the account/provider inputs and the focused sign-in and concurrent-mode checks for V4-EXM-12 and declares them upstream in its own register.
```

#### G-0105-03 · OUT-002, appended · SC3-01-05-6 and a pointer to REQ-010 · Q-2
Target: DEL-01-05
Trace: SC3-01-05-6 at "OUT-002 or new REQ-011": OUT-002 taken (D4 P-6's first option; no new ID). Wording: D4 P-6 with the C-10 form (R18-1 C-10: "the reported email or 'ChatGPT account (no email reported)'; plan type is not recorded"); DECISION-K1 K1-4; ACCESS §8. It names no deliverable, so it grounds no register row (the ledger has none for it; NR-07 is grounded on DEL-01-04's side). The clause "with the start-up traffic settings, network view and record of REQ-010" is **drafted (P2-A)** and consequential: REQ-010's matrix row (G-0105-16) maps to OUT-002, which should name what it then delivers. No AC covers the account supply; the ledger's alternative (a new REQ-011 with its own AC and VER) would add one, and is not taken.
```old
keeping account, API-key and local-server configuration together and exposing per-conversation choice. Scope: SOW-011, SOW-012.
```
```new
keeping account, API-key and local-server configuration together and exposing per-conversation choice, with the start-up traffic settings, network view and record of REQ-010. It also supplies the Codex account as Codex reports it (the reported email, or "ChatGPT account (no email reported)"; the plan type is not recorded) for the person-identity element of App-captured acts, marked identity not verified. Scope: SOW-011, SOW-012.
```

#### G-0105-04 · REQ-002, appended · SC3-01-05-7 · Q-2
Target: DEL-01-05
Trace: D4 P-7 as made unconditional in R2.4 (K2-1 adopted by DECISION-L L-1 A: "a second App-owned Codex home for API-key conversations, sharing the person's settings"); ACCESS §4. "May be held" becomes "is held" because L-1 adopted it; "that shares the person's settings" is L-1's own text.
```old
using the supported behavior defined under REQ-006. Basis: CLM-001, SOW-010.
```
```new
using the supported behavior defined under REQ-006. Where the pinned protocol keeps one account per Codex home, the API key is held by Codex in a separate App-owned Codex home that shares the person's settings (`APP-V4-DESIGN-PASS-3-20261001-DECISION-L` L-1). Basis: CLM-001, SOW-010.
```

#### G-0105-05 · REQ-004, appended · SC3-01-05-4 · Q-2
Target: DEL-01-05
Trace: D4 P-4 (DECISION-K3 K-3), with R18-2's two refusal wordings as C1-B amends it ("keep, amended (two wordings)"). Supplier side of SC3-01-04-6 (G-0104-06).
```old
Selecting one mode shall preserve the configuration needed to choose the other modes for subsequent conversations. Basis: CLM-001, SOW-012.
```
```new
Selecting one mode shall preserve the configuration needed to choose the other modes for subsequent conversations. No access mode or model is applied to a new conversation until the person chooses; the App may offer the person's last explicit choice for that project, shown as such and never applied silently. A conversation that cannot start for want of a model reads "not started — no model selected", and a workflow run that cannot start reads "run not started — no model selected". Basis: CLM-001, SOW-012; `APP-V4-DESIGN-PASS-3-20261001-DECISION-K3` K-3.
```

#### G-0105-06 · REQ-005, responsible participants · SC3-01-05-10 · Q-2
Target: DEL-01-05
Trace: D4 R2.4 P-10, verbatim; DECISION-L L-7; R19-4. The REQ-005 sentence "Until that choice exists, the record shall explicitly retain OI-009 as open" stays: it still states the obligation's condition, now met (TBD-001).
```old
record the choice made by the Owner with the App implementation owner before account integration depends on it.
```
```new
record the choice made by the Owner, who is also the App implementation owner (`APP-V4-DESIGN-PASS-3-20261001-DECISION-L` L-7), before account integration depends on it.
```

#### G-0105-07 · new REQ-010 (start-up traffic) · SC3-01-05-5 · Q-2
Target: DEL-01-05
Trace: D4 P-5 as reworded in R2.4 ("turns off the start-up traffic Codex's settings allow, except that plugin traffic follows the person's own plugin setting (DECISION-L L-3); shows and records the rest, naming which is which per supplier version"), with P-5's network view from round 1. DECISION-K3 K-12 as revised; R18-3 (only what the settings allow; the internal variable is not used). Supersedes pass-2 basis item C1-B B-1 (DROP). C1-B's optional addition (the identifiers and time zone Codex sends to the chosen provider) is not included: no ledger row carries it.
```old
These exclusions preserve DEL-01-05's account/provider integration, local-server qualification and capability-requirement handoff. [S2, S4]
```
```new
These exclusions preserve DEL-01-05's account/provider integration, local-server qualification and capability-requirement handoff. [S2, S4]
- **REQ-010** — The App shall turn off the start-up traffic of its Codex that Codex's settings allow, except that plugin traffic follows the person's own plugin setting. It shall show the remaining start-up connections in a network view and record them, naming for each supplier version which connections an App setting stops and which remain. Basis: `APP-V4-DESIGN-PASS-3-20261001-DECISION-K3` K-12 as revised; `APP-V4-DESIGN-PASS-3-20261001-DECISION-L` L-3; CLM-001.
```

#### G-0105-08 · TBD-001 · SC3-01-05-1 and SC3-01-05-10 · Q-2 (status word: Q-10)
Target: DEL-01-05
Trace: D4 P-1 with its R2.4 additions (observed at 0.158.0; the Owner who is also the App implementation owner), C1-B §4.1 ("keep, amended"), SC3-01-05-10 extended to TBD-001 by C1-B. Facts checked: `Design/ACCOUNT_HOME_DECISION_RECORD.md` header reads "OBSERVED TO WORK AT CODEX 0.158.0 without a credential (OBS-2 O-6 M1)"; DECISION-L L-6 deferred any sign-in or API-key observation. Independent of Q-10: the TBD states the decision; whether OI-009's register row says OPEN or a decided value is Q-10's.
```old
- **TBD-001** — OI-009 remains OPEN: separated or shared account home. Responsible participants: Owner with App implementation owner. Point of need: before account integration. Historical v3 overlay or Root authentication separation does not decide this v4 product choice. [S4]
```
```new
- **TBD-001** — OI-009, separated or shared account home, decided at choice level by `APP-V4-DESIGN-PASS-3-20261001-DECISION-K3` K-1 (record `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-DESIGN-PASS-3-20261001/OWNER_DECISIONS.md`): shared Codex settings, providers and MCP servers, with a separate sign-in custodied by Codex in an App-owned Codex home. Responsible participants: the Owner, who is also the App implementation owner (`APP-V4-DESIGN-PASS-3-20261001-DECISION-L` L-7). Point of need: before account integration. The mechanism was observed to work at Codex 0.158.0 without a credential (OBS-2 O-6; decision record `Design/ACCOUNT_HOME_DECISION_RECORD.md`); separation with a real credential was not observed (L-6). It is confirmed on the pinned version before account integration; if a pinned Codex cannot share settings this way, the App keeps its own settings (a separated home) and says so. Historical v3 overlay or Root authentication separation did not decide this v4 product choice. [S4]
```

#### G-0105-09 · TBD-002, appended · SC3-01-05-13 · Q-11 (optional)
Target: DEL-01-05
Trace: C1-B §4.1 SC3-01-05-13, verbatim, with the file name: `Design/ACCOUNT_AND_PROVIDER_ACCESS.md` §10 "API-key definition record (OUT-003, REQ-006; OI-010 stays OPEN)" (heading read). DECISION-L L-6.
If declined: drop this block and remove TBD-002 from AX-006's Revised list.
```old
Required access modes remain IN. [S4]
```
```new
Required access modes remain IN. The definition record is `Design/ACCOUNT_AND_PROVIDER_ACCESS.md` §10 (draft); OI-010 stays open until supported behaviour is observed (deferred by the owner, `APP-V4-DESIGN-PASS-3-20261001-DECISION-L` L-6). [S4]
```

#### G-0105-10 · TBD-003, first two sentences · SC3-01-05-3 · Q-2
Target: DEL-01-05
Trace: D4 P-3 (FI DECISION-1 D4; OI-012 consequence column). One wording across the D4-pin class. The remaining TBD-003 sentences stay ("DEL-01-05 then establishes …"; "No historical version … is adopted or certified here").
```old
- **TBD-003** — OI-012 and DEP-005 retain the unidentified supplier pin, published protocol and configured model-endpoint capability evidence. The App implementation owner selects the pin through the DEL-01-01 contribution before protocol generation/qualification.
```
```new
- **TBD-003** — Codex 0.158.0 is the definition and generation pin (`APP-V4-FIRST-INCREMENT-20260928-DECISION-1` D4); OI-012 and DEP-005 retain the qualification pin, published protocol and configured model-endpoint capability evidence. The App implementation owner selects the qualification pin through the DEL-01-01 contribution before qualification.
```

#### G-0105-11 · AC-004 · SC3-01-05-4 · Q-2
Target: DEL-01-05
Trace: D4 P-4 ("and shows that a new conversation starts with no model chosen and that an offered last choice is not applied without the person's act").
```old
and preserves the other modes' configuration for subsequent selection. Verifies REQ-004 by VER-004.
```
```new
and preserves the other modes' configuration for subsequent selection; a new conversation starts with no model chosen, and an offered last choice is not applied without the person's act. Verifies REQ-004 by VER-004.
```

#### G-0105-12 · new AC-011 · SC3-01-05-5 · Q-2
Target: DEL-01-05
Trace: D4 P-5 round 1 AC ("the view and record identify, per pinned version, each start-up connection and whether an App setting stops it"), with L-3's plugin clause.
```old
The delivery boundary assigns every act enumerated by REQ-009 to its cited contribution and retains this deliverable's own integration, qualification and handoff work. Verifies REQ-009 by VER-010.
```
```new
The delivery boundary assigns every act enumerated by REQ-009 to its cited contribution and retains this deliverable's own integration, qualification and handoff work. Verifies REQ-009 by VER-010.
- **AC-011** — For the pinned version, the network view and the record identify each start-up connection of the App's Codex and whether an App setting stops it; the connections Codex's settings allow to be stopped are off, and plugin traffic follows the person's plugin setting. Verifies REQ-010 by VER-011.
```

#### G-0105-13 · VER-004, appended · SC3-01-05-4 · Q-2
Target: DEL-01-05
Trace: D4 P-4 (VER side), with R18-2's wordings.
```old
select and start each mode and inspect retained configuration and subsequent availability of the other modes.
```
```new
select and start each mode and inspect retained configuration and subsequent availability of the other modes. Start a new conversation and confirm that no access mode or model is applied until the person chooses; with the person's last explicit choice offered, confirm it is shown as such and not applied without the person's act, and check both refusal wordings.
```

#### G-0105-14 · new VER-011 · SC3-01-05-5 · Q-2
Target: DEL-01-05
Trace: D4 P-5 round 1 VER ("observe the App's Codex start-up with and without the settings and compare with the view and record"), with L-3's plugin case.
```old
checking each act's owner and the retained DEL-01-05 contribution one for one.
```
```new
checking each act's owner and the retained DEL-01-05 contribution one for one.
- **VER-011** — On an identified candidate and supplier version, observe the App's Codex start-up with and without the settings, and with the person's plugin setting on and off; compare the observed connections with the network view and the record.
```

#### G-0105-15 · new AX-006 (amendment reference) · acceptance-conditional
Target: DEL-01-05
```old
this contract makes no legal conclusion. [S1; S5; S3 §6]
```
```new
this contract makes no legal conclusion. [S1; S5; S3 §6]
- **AX-006** — Revised under scope-change amendment `{AMENDMENT_ID}` (accepted snapshot `projects/chirality-app-v4/execution/_ScopeChange/{AMENDMENT_SNAPSHOT}`), applying `APP-V4-FIRST-INCREMENT-20260928-DECISION-1` D4 (record `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-FIRST-INCREMENT-20260928/OWNER_DECISIONS.md`), `APP-V4-DESIGN-PASS-2-20260930-DECISION-K1` K1-4 (record `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-DESIGN-PASS-2-20260930/OWNER_DECISIONS.md`) and `APP-V4-DESIGN-PASS-3-20261001-DECISION-K3` K-1, K-3 and K-12 as revised and `APP-V4-DESIGN-PASS-3-20261001-DECISION-L` L-1, L-3, L-6 and L-7 (record `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-DESIGN-PASS-3-20261001/OWNER_DECISIONS.md`), with that design pass's recorded integrator rulings R18-1, R18-2, R18-3 and R19-4 (`R18_RESOLUTIONS.md` and `R19_RESOLUTIONS.md` in the same run folder). Revised: CLM-001, CLM-004, OUT-002, REQ-002, REQ-004, REQ-005, AC-004, VER-004, TBD-001, TBD-002 and TBD-003. Added: REQ-010, AC-011, VER-011, the REQ-010 matrix row and AX-006. Removed: none.
```

#### G-0105-16 · new matrix row for REQ-010 · SC3-01-05-5 · Q-2
Target: DEL-01-05
Trace: one row per acceptance criterion; AC-011 is verified only by VER-011. OUT-002 per G-0105-03.
```old
| OUT-004 | OBJ-002, OBJ-004 | REQ-009, CLM-003, CLM-004 | AC-010 | VER-010 | One-for-one boundary/owner comparison against accepted contributions |
```
```new
| OUT-004 | OBJ-002, OBJ-004 | REQ-009, CLM-003, CLM-004 | AC-010 | VER-010 | One-for-one boundary/owner comparison against accepted contributions |
| OUT-002 | OBJ-002 | REQ-010, CLM-001 | AC-011 | VER-011 | Per-version start-up connection observations with and without the settings and plugin setting, compared with the network view and record |
```

---

## Extraction guards

For the `dependency-extract` UPDATE briefs that follow REVISE (IMPACT §10).
"New name" means a deliverable ID the revised SoW names and the prior SoW did
not (computed by the dry-run script).

| SoW | New names (script) | Expected rows | Must not yield |
|---|---|---|---|
| DEL-01-01 | DEL-02-03, DEL-03-03, DEL-03-04, DEL-06-01, DEL-09-01, DEL-09-02, DEL-09-06 | R-11-1: 10 DOWNSTREAM mirror rows (all admitted arcs; DEL-02-01, DEL-02-04 and DEL-04-03 were already named) | any UPSTREAM row |
| DEL-01-02 | DEL-01-03, DEL-02-02, DEL-02-03, DEL-03-03, DEL-09-02 | R3-01-02-a, -b (mirrors); -e, -f, -h (mirrors of NR-01, NR-02, NR-04) | an UPSTREAM row to DEL-01-04, 02-02, 02-03, 04-02, 04-03 or 06-01 (R17-10); any row to DEL-09-09 (NR-03 DROP) |
| DEL-01-03 | DEL-06-01, DEL-09-02, DEL-09-05 (DEL-01-04 was already named) | R3-01-03-a…c (mirrors); R3-01-03-d (mirror of NR-05) | an UPSTREAM row to DEL-01-04 or DEL-06-01 (R17-10) |
| DEL-01-04 | DEL-01-05, DEL-02-03, DEL-02-04, DEL-04-02, DEL-09-02 | NR-05, NR-07 (new admitted); NR-08, NR-09, NR-4 (new held); R2-01-04-a (mirror of DEP-02-03-027); R3-01-04-b (mirror of DEP-09-02-012); a DOWNSTREAM mirror of DEP-02-02-013 (held) from REQ-008 | a DOWNSTREAM row to DEL-04-01 or DEL-04-03 (see G-0104-09) |
| DEL-01-05 | DEL-09-02 | R3-01-05-b (mirror of DEP-09-02-013) | a row naming DEL-01-04 (none is proposed on this side) |

Notes:

- **The ten new arcs.** The PKG-01 blocks ground five of them: NR-05, NR-07
  (G-0104-05, G-0104-06), NR-08, NR-09 (G-0104-01, G-0104-03) and NR-4
  (G-0104-06). The other five (NR-01, NR-02, NR-04, R2-04-03-e, R20-10) are
  grounded on the consumer side in part B (P1-01, P1-02, P1-03, SC2-04-03-2,
  P1-05); G-0102-01 carries only their DEL-01-02-side mirrors.
- **DOWNSTREAM mirror of DEP-02-02-013.** REQ-008's "used by `DEL-02-02`"
  mirrors the existing held arc DEL-02-02 → DEL-01-04. ARC_EFFECT §1.2 lists
  no DEL-01-04 row for it; it changes no topology. The extractor may emit it
  or leave it, as the register owner prefers; it is noted so that its
  appearance is not read as a departure.
- **R-11-1 in DEL-01-01.** The script's new-name list for DEL-01-01 is
  exactly the seven P1-09 names, none of them named before (the ledger's
  "names 3 of 10" is confirmed), so the R-11-1 rows the SoW grounds rise
  from 3 of 10 to 10 of 10.
- **Rows whose quoted text changes.** Rows that quote replaced text (for
  example DEP-01-03-017 quoting TBD-003; DEP-01-02-021 quoting CLM-004 or
  TBD-003; DEP-01-05-012, -015, -016 quoting TBD-003, TBD-001, TBD-002) are
  re-quoted or retired `source_revised` with the successor named, as
  SCA-V4-002 did; the ledger's R3-01-02-c, R3-01-03-e, R3-01-05-c…e cover
  their statements.

## Mechanical checks performed

`sow_dryrun.py` (scratch `$TMPDIR/sca003-p2a/`, sha256 `d40d95a9…61a2b3`,
not in the repository) parsed this file: 63 `#### G-` headings, 63 old → new
pairs, in 5 deliverables. For each deliverable it read the SoW at HEAD
`40e04273da`, applied the blocks in order to a scratch copy, filled
`{AMENDMENT_ID}` = `SCA-V4-003` and a dummy snapshot name, and ran the tools
the `scope-of-work` workflow names (`resources/tools.md` steps 6, 7 and 9).
Command, per variant:
`python3 $TMPDIR/sca003-p2a/sow_dryrun.py <repo> <this file> $TMPDIR/sca003-p2a/out <variant>`.
The unrevised copies were checked first: 5/5 PASS `SOW_V1`, boundary check
exit 0, no `NOT_CHECKABLE`.

| Check | Result |
|---|---|
| Prior-contract sha256 equals the Summary table | 5/5 |
| Each "old" block occurs exactly once when applied | 63/63 |
| Unfilled tokens after filling | 0 |
| Frontmatter unchanged | 5/5 |
| `tools/scope_of_work/validate_scope_of_work.py` on each revised copy | 5/5 PASS (`SOW_V1`), no issues |
| `tools/scope_of_work/check_boundary_owner_resolution.py --json` | 5/5 exit 0, status OK; no `UNRESOLVED_OWNER`, `UNDEFINED_CLAIM` or `NO_CITED_CLAIM`; 0 `NOT_CHECKABLE` (2 each in DEL-01-02 and DEL-01-04 before the backtick note above; none in the unrevised files) |
| `tools/scope_of_work/derive_review_checklist.py`, run twice | 5/5 exit 0, byte-identical; items 7, 9, 7, 8, 11 (DEL-01-04 +1 AC-008; DEL-01-05 +1 AC-011) |
| Changed definitions equal the AX line's Revised list; added definitions equal its Added list; no definition removed; no line outside a definition changed except the two new matrix rows | 5/5 (script comparison of definition lines) |
| New deliverable names per SoW | as the "Extraction guards" table (script) |
| Repeat run gives the same revised bytes | yes (revised sha256: DEL-01-01 `3712a6e1…`, 01-02 `4a8f17d0…`, 01-03 `dd5cad51…`, 01-04 `1d038a80…`, 01-05 `e5169de4…`) |
| Variant without the Q-11 optional blocks (G-0101-03, G-0102-07, G-0102-09, G-0105-09) | 5/5 PASS, all checks as above |
| Variant without P1-09 (G-0101-02, Q-15) | 5/5 PASS; DEL-01-01 then names no new deliverable |
| Variant without the Q-5 blocks (G-0104-04, -09, -10, -12, -14; AX-005's Added list and G-0104-02's clause adjusted as stated) | 5/5 PASS; DEL-01-04 checklist 7 items |

These are checks of the proposal before application. They are not the
REVISE run or its `MODE=VERIFY`, which bind the accepted amendment, the
action register hash and each prior contract hash at application. The Q-4
per-clause removals are text edits inside combined blocks and were not run
as variants; each removes a clause and names no new ID, so it cannot add a
validation issue, but the REVISE run checks the actual result.

Scope of what was not checked here: whether the extractor yields exactly the
rows in "Extraction guards" (that is `dependency-extract`'s run); the
semantic one-for-one review of QA item 21 (the tool reports no per-act
exclusion to route to it); and part B's blocks.
