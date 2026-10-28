# SCA-V4-002 — Amendment preview (exact amendment, rendered)

**Standing: accepted at checkpoint group 2 (owner DECISION-2 of run
`APP-V4-SCA002-20260929`, 2026-09-29), as transcribed after the act.** The
owner reviewed the packet itself; this file renders its exact text for the
scope-change layout. Where this file and the packet differ, the packet
governs:

| Accepted source | sha256 |
|---|---|
| `AMENDMENT_PACKET/BASIS_AMENDMENT.md` (Parts A to D: the basis document, the decomposition package, the `_CONTEXT.md` edits, the pointer and effective-state record, the supersession rows) | `091871fd90283b27b2d067c1eeb3137e3cf8f9d50dab87ad92a9b871cc634238` |
| `AMENDMENT_PACKET/SOW_REVISIONS.md` (nine ScopeOfWork contracts, 26 F-blocks) | `440d4d50abd4d6bd2a639cfb2bcaa8bcc83a6c94061a27f9fc91e67c6a12d00d` |
| `AMENDMENT_PACKET/ARC_EFFECT.md` (the four consumption sentences and the SCC computation) | `4b3aeec0f041266dce0e2fae754c129d4473ff8c3268c0b5c638529c6951ddc0` |

This file was written before any SCA-V4-002 edit was applied. Everything
below the rule is BASIS_AMENDMENT.md from "## Part A" to its end, byte for
byte. Its phrases "PROPOSED", "conditional", "recommended" and "if the owner
chooses" are the packet's words at presentation; the owner's answers are in
"Owner answers" below.

## Owner answers that fix the conditional edits

| Item | Answer (DECISION-2: "accept the remaining items as recommended") | Effect on the text below |
|---|---|---|
| Q-5 | Option A: OI-001/OI-002 stay OPEN | B-03: no edit. The option-B text is not applied |
| Q-6 | Included | `{Q6_CLAUSE}` = `, DEL-04-02 and DEL-01-01`; SOW_REVISIONS F-0402 and F-0101 stand |
| Q-7 | Included | B-02 applies; `{Q7_CLAUSE}` = `; the OI-012 pointer in Open_Issues.csv` |
| Q-8 | Line break | A-01 applies in its recommended form; the blank-line alternative is not applied |
| Q-10 | Option (a) | Part D: all 17 `DL-` rows and D-014; `{Q10_CLAUSE}` = `; and path-level Supersession_Delta rows for SCA-V4-001 actions 18–25, 36, 42 and 46` |
| Q-11 | Included | B-05a and B-05b apply; `{Q11_CLAUSE}` = `; Deliverables DEL-04-01 (checkpoint clause) with its _CONTEXT.md mirror` |
| Q-12 | Option (a) | B-06a, B-06b and B-06c apply, at the times below; `{Q12_CLAUSE}` = `; a reading-rule note ("GROUP3 as amended by the active _ScopeChange/_LATEST.md") on _LATEST.md, checkpoint_snapshots/_LATEST_ACCEPTED.md and five _CONTEXT.md basis lines` |
| Q-13 | Accepted | C-02 is written after group 1 |

The clause values are copied from the B-04 "Slot rules" table below.

## Token fill

- `{AMENDMENT_ID}` = `SCA-V4-002` (owner item Q-1, accepted).
- `{D_SEQ_DEL0401}` = `D-014` (Part D).
- `{AMENDMENT_SNAPSHOT}` = the accepted group-3 snapshot folder under
  `execution/_ScopeChange/`. The current candidate is
  `SCA-V4-002_2026-09-29_1901`; the value is fixed only by the group-3 act.
- `{ACCEPT_DATE}` = the date of the owner's group-3 act.
- `{CLOSURE_VERDICT}`, `{GROUP12_REFS}`, `{SCA001_CLOSURE}`,
  `{ARC_LIST}`, `{OPEN_LIST}` and `{UTC}` (C-01) are filled at the
  pointer move, by the C-01 slot rules below.

## Application classes

| Class | Edits | When |
|---|---|---|
| After group-1 acceptance | C-02: the SCA-V4-001 effective-state record (new file; no existing byte changes) | Written after the group-1 decision snapshot |
| Candidate edits (no acceptance token) | A-01; B-01 (RECOMPUTE, 31 rows); B-02 (Q-7); B-05a and B-05b (Q-11); B-06b; B-06c (five `_CONTEXT.md` files); Part D (`Supersession_Delta.csv`, then `Supersession_Map.csv` by the accumulator) | Written into the candidate poststate after group 2 |
| No edit | B-03 (Q-5 option A) | — |
| **Acceptance-conditional** (carry `{ACCEPT_DATE}` and/or `{AMENDMENT_SNAPSHOT}`) | B-04 (the `## Decision Log` entry in SOFTWARE_DECOMP.md); C-01 (`_ScopeChange/_LATEST.md` in SPEC §11.2 form) | Only after group-3 acceptance, with the tokens filled from the accepted record |
| **Timed with the SoW REVISEs** (no token; the file is bound in `_DAG/DAG-002/SOURCE_MANIFEST.sha256`) | B-06a (`_Decomposition/checkpoint_snapshots/_LATEST_ACCEPTED.md`) | After group-3 acceptance, with the SoW REVISEs, so that the one DAG-003 currency audit takes it up (B-06 "Timing of B-06a"; IMPACT_ASSESSMENT §7 step 5) |
| ScopeOfWork edits (SOW_REVISIONS.md) | Register rows 1–9, nine contracts, 26 blocks | After group-3 acceptance, by `scope-of-work` MODE=REVISE, one brief per deliverable, closing with MODE=VERIFY, `STATUS_POLICY=NO_STATUS_TOUCH` (Q-3) |

Every candidate "old" block or value was checked, before application, to
occur exactly once in its target at commit `39c97257b`
(`apply_sca002.py`, dry run). The B-04 and B-06a "old" blocks also occur
exactly once there.

---

## Part A — Accepted basis documents

### A-01 · HOST_INTEGRATION.md status paragraph — the A17b line join

Target: `projects/chirality-app-v4/docs/HOST_INTEGRATION.md` (sha256 now
`6c6854f9…c49bd`, as H-2 left it)

**What happened.** SCA-V4-001 A17b expected "are retained." to end a line. In
this file it did not: the original line 10 read "are retained. **Open
detail** marks an unruled policy or interface point,". Applying A17b
verbatim therefore left the amendment sentence and "**Open detail** marks …"
on one long line (current line 11). The words are correct. Only the line
layout is off.

**A correction to the brief's wording.** The brief says "restore the
paragraph break". At `9ae24fc0f`, before A17b, "**Open detail** marks …"
was inside the status paragraph, on the same line as "are retained.", so
there was no paragraph break to restore. The recommended fix restores the
line break that A17b's new block implied. It keeps the paragraph as it
was. The alternative, a blank line, would make "**Open detail**" its own
paragraph (Q-8).

```old
2026-09-29, for owner decisions DEC-4 and DEC-5 (PRD §0). **Open detail** marks an unruled policy or interface point,
```
```new
2026-09-29, for owner decisions DEC-4 and DEC-5 (PRD §0).
**Open detail** marks an unruled policy or interface point,
```

- **Check:** the old block occurs once.
- **Result:** sha256 `d4331c39db7f452cd3ba72fdfa4bad540a6053931218359a93646971acb28d9f`;
  git blob `f4a5281e8f9bd6b1425a872fa3da3c674e8d079f`; 274 lines, one more
  than today.
- **Alternative (Q-8, blank line):** result sha256
  `78f7e4c2070676381b8794f0d864a42a54575a391863f3c6e19850d5d5b4ec94`, with
  two more lines, so B-01 would shift every SourceLine by 2.
- **Rendering:** Markdown renders the recommended form the same as today,
  so this is a source-layout fix only.
- **No amendment note** is added to the status paragraph. The edit changes
  no meaning. The Change Register entry (B-04) records it.

---

## Part B — Decomposition package (`execution/_Decomposition/`)

### B-01 · Consolidated_Coverage.csv — RECOMPUTE for the 31 HOST_INTEGRATION rows

This is the same recompute as SCA-V4-001 B8/H-4, limited to the rows of the
one changed document. For each row whose `Document` is
`projects/chirality-app-v4/docs/HOST_INTEGRATION.md`:

| Column | Old | New |
|---|---|---|
| `SHA256` | `6c6854f941c714d8287bf799e1427bd4d99450847341bdf885ce4158d77eb122` | `d4331c39db7f452cd3ba72fdfa4bad540a6053931218359a93646971acb28d9f` |
| `ReadSnapshot` | `git-blob:8edbfa40f4a40828e188c31729d9a771763155f6` | `git-blob:f4a5281e8f9bd6b1425a872fa3da3c674e8d079f` |
| `SourceLine` | n (all 31 rows have n ≥ 40) | n + 1 |

- **Check:** `basis_dryrun.py` recomputed each row's line in the revised
  file. The "n + 1" rule puts each ID on a line that contains it, 31/31.
- **Unchanged:** every other column and every other row, including the
  `Standing` text.
- **Tooling:** use the SCA-V4-001 recompute script
  (`_PostAcceptanceValidation/SCA-V4-001_20260929T132946Z/apply_group3_edits.py`
  pattern) or an equivalent. Do not hand-edit.

### B-02 · Open_Issues.csv — OI-012 `Consequence` pointer — conditional (Q-7)

This mirrors SCA-V4-001 O-17 (the OI-001/OI-002 pointers). The row stays
**OPEN**. The SoW texts that F-0104-05 and F-0202-02 revise will cite D4,
while this row does not mention it.

| Row · column | Old field value (whole) | New field value (whole) |
|---|---|---|
| OI-012 · `Consequence` | `Historical version examples are not adopted version pins. Required associated definition/receiving work is IN; this issue holds the unresolved detail, not the existence of the required result.` | `Historical version examples are not adopted version pins. Required associated definition/receiving work is IN; this issue holds the unresolved detail, not the existence of the required result. APP-V4-FIRST-INCREMENT-20260928-DECISION-1 D4 selected Codex 0.158.0 as the definition and generation pin for the first undertaking (carried by DEL-01-01); re-examination before implementation and the pin used for qualification remain under this issue.` |

- **Check:** the edit is row-scoped. The closing sentence also occurs in 7
  other rows, so it is not usable as a file-wide anchor. The OI-012 field
  equals the old value exactly.
- **CSV quoting:** the field is already quoted.
- **Tooling:** apply with a CSV reader and writer that keep the file's
  quoting and line endings (SCA-V4-001 D-14a/b pattern).
- **Counts:** unchanged (23 OPEN).

### B-03 · Open_Issues.csv — OI-001/OI-002 `Status` — owner item Q-5

**Recommended option A: no edit.** The rows stay OPEN, with the D2/D3
pointers SCA-V4-001 put in `Consequence`.

**If the owner chooses option B**, apply these edits. Both follow the OI-017
precedent (`RESOLVED_FOR_CURRENT_DEFINITION_RUN`).

| Row · column | Old | New |
|---|---|---|
| OI-001 · `Status` | `OPEN` | `RESOLVED_FOR_FIRST_INCREMENT` |
| OI-002 · `Status` | `OPEN` | `RESOLVED_FOR_FIRST_INCREMENT` |
| OI-001 · `Consequence` (append) | `False attribution is already prohibited.` | `False attribution is already prohibited. Frozen Group3 retains the historical OPEN row; the product-level list (PRD OQ-02) is not resolved by this status.` |

Option B also needs:
- **A SoW sweep.** Eight later-undertaking SoWs still say that OI-001/OI-002
  "remain OPEN" (IMPACT §4, V-4). They would need a follow-on sweep.
- **Counts and telemetry.** The OPEN count changes from 23 to 21. The
  already-stale Coverage_Telemetry (`ActiveOpenIssueCount`,
  `ResolvedIssueIDs`) would carry a further delta at its rebuild.

### B-04 · SOFTWARE_DECOMP.md — Change Register entry — acceptance-conditional

Insert after the SCA-V4-001 entry of `## Decision Log`:

```old
Snapshot: `../_ScopeChange/SCA-V4-001_2026-09-28_2155`.

## Checkpoint and next stage
```
```new
Snapshot: `../_ScopeChange/SCA-V4-001_2026-09-28_2155`.

- SCA-V4-002 ({ACCEPT_DATE}), requested by the owner (run APP-V4-BASIS-ALIGN-20260928 DECISION-8 and DECISION-10; run APP-V4-SCA002-20260929): MODIFY only. ScopeOfWork text of DEL-10-03, DEL-02-01, DEL-02-03, DEL-09-07, DEL-01-04, DEL-02-02 and DEL-03-03{Q6_CLAUSE}; a line-layout correction in HOST_INTEGRATION.md's status paragraph, with the Consolidated_Coverage recompute{Q7_CLAUSE}{Q11_CLAUSE}{Q12_CLAUSE}{Q10_CLAUSE}. No ID was added, retired, renumbered or moved; 11 Packages, 41 Deliverables and 262 scope IDs are unchanged. Snapshot: `../_ScopeChange/{AMENDMENT_SNAPSHOT}`.

## Checkpoint and next stage
```

**Slot rules.** They are fixed by the group-2 decision, so that no "where
accepted" text is applied (V11 F7):

| Slot | Filled with | If not accepted |
|---|---|---|
| `{ACCEPT_DATE}` | the group-3 acceptance date | — |
| `{AMENDMENT_SNAPSHOT}` | the accepted snapshot folder name | — |
| `{Q6_CLAUSE}` | `, DEL-04-02 and DEL-01-01` if Q-6 is accepted | the empty string |
| `{Q7_CLAUSE}` | `; the OI-012 pointer in Open_Issues.csv` if Q-7 is accepted | the empty string |
| `{Q11_CLAUSE}` | `; Deliverables DEL-04-01 (checkpoint clause) with its _CONTEXT.md mirror` if Q-11 is accepted | the empty string |
| `{Q12_CLAUSE}` | `; a reading-rule note ("GROUP3 as amended by the active _ScopeChange/_LATEST.md") on _LATEST.md, checkpoint_snapshots/_LATEST_ACCEPTED.md and five _CONTEXT.md basis lines` if Q-12 option (a) is accepted | the empty string |
| `{Q10_CLAUSE}` | `; and path-level Supersession_Delta rows for SCA-V4-001 actions 18–25, 36, 42 and 46` if Q-10 option (a) is accepted | the empty string |

If Q-5 option B is chosen, append `; OI-001/OI-002 Status` before the
`{Q10_CLAUSE}` slot.

**Check.** The old block occurs once (`## Checkpoint and next stage` follows
the Decision Log directly).

### B-05 · Deliverables.csv DEL-04-01 `Description`, with its `_CONTEXT.md` mirror — conditional (Q-11; ASC-ISS-002)

**Why.** DEL-04-01's description still says "PKG-02 checkpoints override
autonomy". SCA-V4-001 superseded that meaning:
- in V4-HI-42 (D-012);
- in the parallel DEL-09-07 phrase (D-12b).

DEL-04-01's own SoW no longer carries it. The fix uses D-12b's wording.

| # | Row · column | Old substring | New substring | Decision |
|---|---|---|---|---|
| B-05a | `Deliverables.csv` DEL-04-01 · `Description` | `PKG-02 checkpoints override autonomy;` | `PKG-02 checkpoint acts are never substituted by autonomy (holds only in the governance phase);` | SI DECISION-4 D4-1 |
| B-05b | `PKG-04_Human acts, autonomy and run evidence/1_Working/DEL-04-01_Operation-policy and human-act distinctions/_CONTEXT.md`, line 13 (`**Description:**`) | same | same | mirror (SCA-V4-001 B7 pattern) |

- **Check:** each old substring occurs once in its file. The GROUP3
  canonical row carries the same text; D-014 (Part D) binds it.
- **Left unchanged:** the same description's closing clause, "a concrete
  unruled operation waits for OI-001/OI-002 before dependent
  implementation". It is consistent with Q-5 option A (rows stay OPEN).
- **No DAG effect:** DEL-04-01's `_CONTEXT.md` and `Deliverables.csv` are
  not in DAG-002's source manifest. DEL-04-01's SoW does not change.

### B-06 · Reading-rule note on the accepted-decomposition pointers — conditional (Q-12; ASC-ISS-006)

**Why.** Supersession is reachable today only through
`_ScopeChange/_LATEST.md`. `_COORDINATION.md` tells readers to resolve
`checkpoint_snapshots/_LATEST_ACCEPTED.md`, which names GROUP3 alone. The
41 `_CONTEXT.md` "Accepted basis" lines also name GROUP3 alone. A reader
following either route never learns that some canonical rows are
superseded.

**Recommended option (a): add one reading-rule sentence.** Option (b), which
extends O-22 to these surfaces, is in OWNER_ITEMS Q-12.

#### B-06a · `_Decomposition/checkpoint_snapshots/_LATEST_ACCEPTED.md` (append after the last sentence)
```old
Future coordination, dependency/DAG and lifecycle decisions are not inferred.
```
```new
Future coordination, dependency/DAG and lifecycle decisions are not inferred.

Reading rule: read this snapshot as amended by the active scope-change snapshot named in [../../_ScopeChange/_LATEST.md](../../_ScopeChange/_LATEST.md). Where an accepted amendment changed a canonical row, the working file in `_Decomposition/` and that snapshot's `Supersession_Map.csv` govern; the canonical row is kept as the superseded original.
```

#### B-06b · `_Decomposition/_LATEST.md`
```old
Latest: (none)
```
```new
Latest: (none)

The accepted decomposition is `checkpoint_snapshots/GROUP3-20260928T001055Z` (see `checkpoint_snapshots/_LATEST_ACCEPTED.md`), read as amended by the active scope-change snapshot named in `../_ScopeChange/_LATEST.md`.
```

#### B-06c · `_CONTEXT.md` line 3 in DEL-02-03, DEL-05-01, DEL-05-02, DEL-09-07 and DEL-04-01 (the files that carry amended text)
```old
see `ACCEPTED_MANIFEST.csv` and `DECISION.md`. No production completion or external contribution is inferred.
```
```new
see `ACCEPTED_MANIFEST.csv` and `DECISION.md`. Read it as amended by the active scope-change snapshot named in `projects/chirality-app-v4/execution/_ScopeChange/_LATEST.md`. No production completion or external contribution is inferred.
```

- **Check:** each old string occurs once in each target file.
- **B-06b parser safety:** the parser reads "Latest: (none)" as before. The
  added prose has no `Latest:` line.
- **Timing of B-06a.** The file is bound in DAG-002 `SOURCE_MANIFEST.sha256`,
  so any edit to it is a DAG departure. Apply it with the SoW REVISEs, so
  that the one DAG-003 currency audit takes it up (ARC_EFFECT §4).
- **Timing of B-06b and B-06c:** apply in the candidate. They are not
  manifest-bound.
- **The other 36 `_CONTEXT.md` lines are left alone.** They carry no amended
  text, and the rule in `_LATEST_ACCEPTED.md` covers them.

---

## Part C — `_ScopeChange/_LATEST.md` (acceptance-conditional; V13 F2)

**What is wrong with the current pointer (V13 F2).** It uses the prose form
`**Active snapshot:** \`…\``. The registered parser
(`validate_domain_decomposition_integrity._latest_pointer_target`) returns
`None` for it. A scratch parser check (P1-002) confirms this at
`102f09c1a`.

**The fix.** At SCA-V4-002's group-3 pointer move, write the file in SPEC
§11.2 form: `Latest:` and `Updated:` as the first two lines, then field
lines, then prose.
- **Parser test:** a scratch copy of the form below was parsed by the
  registered function. It returns the snapshot name, and `_pointer_matches`
  is True.
- **Field lines:** none of them matches the parser's other patterns
  (`Latest snapshot:`, `| Snapshot |`).

Proposed bytes (tokens filled at the act):

```text
Latest: {AMENDMENT_SNAPSHOT}
Updated: {ACCEPT_DATE}
Amendment: {AMENDMENT_ID}
Accepted predecessor: SCA-V4-001_2026-09-28_2155
Closure: {CLOSURE_VERDICT}

# Active SCOPE_CHANGE Snapshot

**Status:** `{CLOSURE_VERDICT}`
**Active snapshot:** `execution/_ScopeChange/{AMENDMENT_SNAPSHOT}/`
**Amendment:** `{AMENDMENT_ID}`, the App v4 follow-on alignment (run `APP-V4-SCA002-20260929`)
**Accepted:** checkpoint group 3 on {ACCEPT_DATE} (`execution/_ScopeChange/checkpoint_snapshots/{AMENDMENT_ID}_GROUP-3_{ACCEPT_DATE}/`); groups 1 and 2 ({GROUP12_REFS})
**Accepted predecessor:** `execution/_ScopeChange/SCA-V4-001_2026-09-28_2155/` (closure verdict: {SCA001_CLOSURE})
**Post-acceptance validation:** `execution/_ScopeChange/_PostAcceptanceValidation/{AMENDMENT_ID}_{UTC}/`

{AMENDMENT_ID} makes MODIFY actions only: DEL-10-03 REQ-005 ("local-first"
aligned with DECISION-4 D4-3); the consumption sentences behind arcs
{ARC_LIST}; OI-001/002/012 text in DEL-09-07, DEL-01-04 and DEL-02-02; the
DEL-03-03 CLM-002 tail; and the HOST_INTEGRATION line layout. Topology is
unchanged: 11 packages, 41 deliverables and 262 scope IDs.

Open, separately governed: {OPEN_LIST}.

It makes no release, publication or reliance claim.
```

**Slot rules:**

| Slot | Filled with |
|---|---|
| `{CLOSURE_VERDICT}` | the group-3 Handoff_State verdict (expected `OPEN_PENDING_DERIVATIVE_CLOSURE`, because the SoW REVISEs, the registers and DAG-003 follow acceptance) |
| `{GROUP12_REFS}` | the actual decision folders |
| `{SCA001_CLOSURE}` | SCA-V4-001's closure verdict at the time of the write, from the CA1 audit's accepted record, or `OPEN_PENDING_DERIVATIVE_CLOSURE` if it is unchanged |
| `{ARC_LIST}` | the arcs kept at Q-4 |
| `{OPEN_LIST}` | the open items in the group-3 Handoff_State. They include the SCA-V4-001 items still open, so moving the pointer does not hide them |

**One-active-snapshot rule.** After the move, `_LATEST.md` names only
SCA-V4-002. SCA-V4-001 stays an accepted, immutable snapshot. Its open items
are carried in SCA-V4-002's Handoff_State "carried from predecessor"
section.

**Also, at each checkpoint:** the group-1, group-2 and group-3 decision
snapshots and the two `SCA-V4-002_GROUP-{1,2}_AUTHORIZED.md` pointers. Each
snapshot is committed before the next stage consumes it (V11 F3 lesson;
Q-14).

### C-02 · SCA-V4-001 effective-state record — Q-13 (ASC-ISS-003)

**Why.** SCA-V4-001's `_LATEST.md`, `Handoff_State.md` and `RUN_SUMMARY.md`
still list as open three things that are now done: the 16 SoW REVISEs, the
18 registers, and DAG-002 (accepted under DECISION-10). These records
understate progress; they do not over-claim (V13 N2). Their bytes are
group-bound, so they are not edited.

**Proposal.** Write one new append-only record:
`execution/_ScopeChange/_PostAcceptanceValidation/SCA-V4-001_{UTC}_EFFECTIVE_STATE/EFFECTIVE_STATE.md`.
This uses the contract's append-only post-acceptance folder; no new layout
is invented. It states:
- **Complete**, each with evidence commits: the 16 REVISEs (`e9dc4633b`),
  the 18 registers, and DAG-002 accepted and published (`87813431d`,
  `6dca88de7`).
- **Open:**
  - `Coverage_Telemetry.json`;
  - the 17 Design re-pins;
  - ASC-ISS-001, and its disposition (Q-10).
- **Closure verdict:** `OPEN_PENDING_DERIVATIVE_CLOSURE`, citing the CA1
  audit snapshot `_Evaluation/ScopeClosureAudit/ScopeClosure_SCA-V4-001_2026-09-29_1222/`.
- **Pointer:** it names neither a new pointer nor a different active
  snapshot.

**Timing.** Write it after group-1 acceptance, when the owner has ruled on
ASC-ISS-001. At SCA-V4-002's group-3 pointer move (C-01), the new
`_LATEST.md` cites it in `{SCA001_CLOSURE}` and `{OPEN_LIST}`. This combines
the V13 F2 pointer fix with the effective state, as CA1 asked, without
touching `_LATEST.md` during SCA-V4-002's candidate stage. The contract
says to keep the pointer unchanged in the `ACCEPTED_PREDECESSOR` posture.

---

## Part D — Supersession_Delta rows (Q-10 option (a); ASC-ISS-001, ASC-ISS-002)

**What CA1 found (ASC-ISS-001).** Eleven SCA-V4-001 actions (18–25, 36, 42
and 46) declare `SupersessionBindingPresent = YES`, but have no delta row of
their own. Their coverage is only in the Notes of D-001, D-002, D-003, D-009,
D-015 and D-016, and no row names the GROUP3 canonical `ScopeLedger.csv` or
`Deliverables.csv` as the superseded authority.

**Option (a), recommended.** SCA-V4-002's `Supersession_Delta.csv` binds them
at path level, without rewriting SCA-V4-001's immutable delta, map or
register:
- **One row per superseded fact:** 8 ledger statements, and 9 description or
  artifact substrings (D-10a/b, D-11a–d, D-12a–c). That makes 17 rows.
- **DecisionID `DL-SCA-V4-001-A{NN}[-D-xx]`.** This is the contract's
  decision-log-only form. The rows bind no SCA-V4-002 action, and audit Pass
  6 accepts `DL-` rows. SCA-V4-002's `Decision_Log.md` records the owner's
  Q-10 ruling as their decision-log reference.
- **One `D-014` row** binds B-05, the new SCA-V4-002 action 14 (IMPACT §3).

**Checks** (`delta_draft.py`, scratch `P1-002/`):
- Each `SupersededFactTextOrValue` equals, or is a substring of, the GROUP3
  canonical value: 18/18.
- Each replacement equals, or is a substring of, the current working value:
  17/17. D-014 is to be applied.
- **Accumulation:** `tools/coordination/accumulate_supersession_map.py
  --prior-map _ScopeChange/SCA-V4-001_2026-09-28_2155/Supersession_Map.csv
  --delta <this block, tokens filled> --output-map <scratch>` exits 0 with 29
  rows (11 + 18) and 0 findings.
- **Draft bytes:** `Supersession_Delta.draft.csv` sha256 `a14c4dd1…04e`.

**Tokens:** `{AMENDMENT_ID}` = `SCA-V4-002`; `{D_SEQ_DEL0401}` = `D-014`.
If Q-11 is declined, drop the last row. If option (b) is chosen, drop the 17
DL rows. The delta then holds only D-014, or nothing, and the map is carried
forward with no `--delta` (or with `--allow-empty` semantics as the tool
requires).

```csv
AmendmentID,DecisionID,SupersededAuthorityRole,SupersededAuthorityPath,SupersededAuthorityRef,SupersededFactKey,SupersededFactTextOrValue,OverrideType,ReplacementFactTextOrValue,AppliesToRoots,AppliesToFacilities,AppliesToSections,Notes
{AMENDMENT_ID},DL-SCA-V4-001-A18,OTHER,projects/chirality-app-v4/execution/_Decomposition/checkpoint_snapshots/GROUP3-20260928T001055Z/canonical/ScopeLedger.csv,"ScopeItemID SOW-015, column ScopeItemStatement",SCOPELEDGER_SOW_015_STATEMENT,The shared host integration contract defaults embedded agents to a user-controlled local model server.,SUPERSESSION,"The shared host integration contract offers embedded agents a user-controlled local model server as one of the model options the person chooses among, with no default.",,,,"Path-level binding for SCA-V4-001 action 18 (D-01; APP-V4-SWBPIPE-INTAKE-20260928-DECISION-4 D4-3), which the SCA-V4-001 delta covered only in the Notes of D-002 (ASC-ISS-001, option a). The override was accepted and applied under SCA-V4-001 (DECISION-7, DECISION-8); this row adds no new override. The SourceRef and DecisionRef columns of the row are not superseded facts."
{AMENDMENT_ID},DL-SCA-V4-001-A19,OTHER,projects/chirality-app-v4/execution/_Decomposition/checkpoint_snapshots/GROUP3-20260928T001055Z/canonical/ScopeLedger.csv,"ScopeItemID SOW-016, column ScopeItemStatement",SCOPELEDGER_SOW_016_STATEMENT,The shared host integration contract permits cloud models only when the person chooses one and supplies an API key.,SUPERSESSION,"The shared host integration contract permits a cloud model when the person chooses one, reached by OAuth sign-in or an API key.",,,,"Path-level binding for SCA-V4-001 action 19 (D-02; APP-V4-SWBPIPE-INTAKE-20260928-DECISION-4 D4-3), which the SCA-V4-001 delta covered only in the Notes of D-002 (ASC-ISS-001, option a). The override was accepted and applied under SCA-V4-001 (DECISION-7, DECISION-8); this row adds no new override. The SourceRef and DecisionRef columns of the row are not superseded facts."
{AMENDMENT_ID},DL-SCA-V4-001-A20,OTHER,projects/chirality-app-v4/execution/_Decomposition/checkpoint_snapshots/GROUP3-20260928T001055Z/canonical/ScopeLedger.csv,"ScopeItemID SOW-017, column ScopeItemStatement",SCOPELEDGER_SOW_017_STATEMENT,In local operation the host contract permits agent data transmission only to the configured model server.,SUPERSESSION,"The host contract permits agent data transmission only to the model service the person selected and to destinations the person has allowed, in advance or when the agent asks during its work; every destination contacted is recorded and shown.",,,,"Path-level binding for SCA-V4-001 action 20 (D-03; APP-V4-SWBPIPE-INTAKE-20260928-DECISION-5), which the SCA-V4-001 delta covered only in the Notes of D-003 (ASC-ISS-001, option a). The override was accepted and applied under SCA-V4-001 (DECISION-7, DECISION-8); this row adds no new override. The SourceRef and DecisionRef columns of the row are not superseded facts."
{AMENDMENT_ID},DL-SCA-V4-001-A21,OTHER,projects/chirality-app-v4/execution/_Decomposition/checkpoint_snapshots/GROUP3-20260928T001055Z/canonical/ScopeLedger.csv,"ScopeItemID SOW-052, column ScopeItemStatement",SCOPELEDGER_SOW_052_STATEMENT,At declared workflow checkpoints request the required human act and wait even when operation autonomy otherwise permits direct application.,SUPERSESSION,At declared workflow checkpoints request the required human act even when operation autonomy otherwise permits direct application; in the current phase the checkpoint is plan guidance and the run does not wait; waiting until the act is performed is phased to the governance layer for workflows that need it.,,,,"Path-level binding for SCA-V4-001 action 21 (D-04; APP-V4-SWBPIPE-INTAKE-20260928-DECISION-4 D4-1), which the SCA-V4-001 delta covered only in the Notes of D-001 (ASC-ISS-001, option a). The override was accepted and applied under SCA-V4-001 (DECISION-7, DECISION-8); this row adds no new override. The SourceRef and DecisionRef columns of the row are not superseded facts."
{AMENDMENT_ID},DL-SCA-V4-001-A22,OTHER,projects/chirality-app-v4/execution/_Decomposition/checkpoint_snapshots/GROUP3-20260928T001055Z/canonical/ScopeLedger.csv,"ScopeItemID SOW-137, column ScopeItemStatement",SCOPELEDGER_SOW_137_STATEMENT,The embedded-loop integration contract routes network requests through the host native layer enforcing the configured endpoint.,SUPERSESSION,"The embedded-loop integration contract routes network requests through the host native layer, which allows only the selected model service and the destinations the person has allowed and records every destination contacted.",,,,"Path-level binding for SCA-V4-001 action 22 (D-05; APP-V4-SWBPIPE-INTAKE-20260928-DECISION-5), which the SCA-V4-001 delta covered only in the Notes of D-009 (ASC-ISS-001, option a). The override was accepted and applied under SCA-V4-001 (DECISION-7, DECISION-8); this row adds no new override. The SourceRef and DecisionRef columns of the row are not superseded facts."
{AMENDMENT_ID},DL-SCA-V4-001-A23,OTHER,projects/chirality-app-v4/execution/_Decomposition/checkpoint_snapshots/GROUP3-20260928T001055Z/canonical/ScopeLedger.csv,"ScopeItemID SOW-138, column ScopeItemStatement",SCOPELEDGER_SOW_138_STATEMENT,Keep host API keys outside interface scripts.,SUPERSESSION,Keep host API keys and sign-in credentials outside interface scripts.,,,,"Path-level binding for SCA-V4-001 action 23 (D-06; APP-V4-SWBPIPE-INTAKE-20260928-DECISION-4 D4-3), which the SCA-V4-001 delta covered only in the Notes of D-009 (ASC-ISS-001, option a). The override was accepted and applied under SCA-V4-001 (DECISION-7, DECISION-8); this row adds no new override. The SourceRef and DecisionRef columns of the row are not superseded facts."
{AMENDMENT_ID},DL-SCA-V4-001-A24,OTHER,projects/chirality-app-v4/execution/_Decomposition/checkpoint_snapshots/GROUP3-20260928T001055Z/canonical/ScopeLedger.csv,"ScopeItemID SOW-201, column ScopeItemStatement",SCOPELEDGER_SOW_201_STATEMENT,"Examine direct low-consequence application with origin/undo, geometry proposals and a human checkpoint overriding autonomy.",SUPERSESSION,"Examine direct low-consequence application with origin/undo, geometry proposals and a human checkpoint whose act autonomy never substitutes, holding the run only in the governance phase.",,,,"Path-level binding for SCA-V4-001 action 24 (D-07; APP-V4-SWBPIPE-INTAKE-20260928-DECISION-4 D4-1), which the SCA-V4-001 delta covered only in the Notes of D-015 (ASC-ISS-001, option a). The override was accepted and applied under SCA-V4-001 (DECISION-7, DECISION-8); this row adds no new override. The SourceRef and DecisionRef columns of the row are not superseded facts."
{AMENDMENT_ID},DL-SCA-V4-001-A25,OTHER,projects/chirality-app-v4/execution/_Decomposition/checkpoint_snapshots/GROUP3-20260928T001055Z/canonical/ScopeLedger.csv,"ScopeItemID SOW-202, column ScopeItemStatement",SCOPELEDGER_SOW_202_STATEMENT,Coordinate observation of all host network traffic during the local-model journey to check endpoint-only transmission.,SUPERSESSION,"Coordinate observation of all host network traffic during the local-model journey to check transmission only to the selected model service and person-allowed destinations, each recorded and shown.",,,,"Path-level binding for SCA-V4-001 action 25 (D-08; APP-V4-SWBPIPE-INTAKE-20260928-DECISION-5), which the SCA-V4-001 delta covered only in the Notes of D-016 (ASC-ISS-001, option a). The override was accepted and applied under SCA-V4-001 (DECISION-7, DECISION-8); this row adds no new override. The SourceRef and DecisionRef columns of the row are not superseded facts."
{AMENDMENT_ID},DL-SCA-V4-001-A36-D-10a,OTHER,projects/chirality-app-v4/execution/_Decomposition/checkpoint_snapshots/GROUP3-20260928T001055Z/canonical/Deliverables.csv,"DeliverableID DEL-02-03, column Description, substring (D-10a)",DELIVERABLES_DEL_02_03_DESCRIPTION_D_10a,checkpoint requests wait regardless of direct autonomy;,SUPERSESSION,"checkpoint acts are requested and recorded only when performed, regardless of direct autonomy (holds are governance phase);",,,,"Path-level binding for SCA-V4-001 action 36 (D-10a; APP-V4-SWBPIPE-INTAKE-20260928-DECISION-4 D4-1), which the SCA-V4-001 delta covered only in the Notes of D-001 (ASC-ISS-001, option a). The override was accepted and applied under SCA-V4-001 (DECISION-7, DECISION-8); this row adds no new override."
{AMENDMENT_ID},DL-SCA-V4-001-A36-D-10b,OTHER,projects/chirality-app-v4/execution/_Decomposition/checkpoint_snapshots/GROUP3-20260928T001055Z/canonical/Deliverables.csv,"DeliverableID DEL-02-03, column AnticipatedArtifacts, substring (D-10b)",DELIVERABLES_DEL_02_03_ANTICIPATEDARTIFACTS_D_10b,"TEST: missing-tool, checkpoint hold and source-preserving round-trip fixtures",SUPERSESSION,"TEST: missing-tool, checkpoint recording (governance-phase hold retained) and source-preserving round-trip fixtures",,,,"Path-level binding for SCA-V4-001 action 36 (D-10b; APP-V4-SWBPIPE-INTAKE-20260928-DECISION-4 D4-1), which the SCA-V4-001 delta covered only in the Notes of D-001 (ASC-ISS-001, option a). The override was accepted and applied under SCA-V4-001 (DECISION-7, DECISION-8); this row adds no new override."
{AMENDMENT_ID},DL-SCA-V4-001-A42-D-11a,OTHER,projects/chirality-app-v4/execution/_Decomposition/checkpoint_snapshots/GROUP3-20260928T001055Z/canonical/Deliverables.csv,"DeliverableID DEL-05-01, column Description, substring (D-11a)",DELIVERABLES_DEL_05_01_DESCRIPTION_D_11a,the minimal local-first Chat Completions loop,SUPERSESSION,the minimal Chat Completions loop on a local or cloud model the person chooses,,,,"Path-level binding for SCA-V4-001 action 42 (D-11a; APP-V4-SWBPIPE-INTAKE-20260928-DECISION-4 D4-3), which the SCA-V4-001 delta covered only in the Notes of D-002 (ASC-ISS-001, option a). The override was accepted and applied under SCA-V4-001 (DECISION-7, DECISION-8); this row adds no new override."
{AMENDMENT_ID},DL-SCA-V4-001-A42-D-11b,OTHER,projects/chirality-app-v4/execution/_Decomposition/checkpoint_snapshots/GROUP3-20260928T001055Z/canonical/Deliverables.csv,"DeliverableID DEL-05-01, column Description, substring (D-11b)",DELIVERABLES_DEL_05_01_DESCRIPTION_D_11b,host owner selects internals and enforces endpoint/key boundaries;,SUPERSESSION,host owner selects internals and enforces destination and key/credential boundaries;,,,,"Path-level binding for SCA-V4-001 action 42 (D-11b; APP-V4-SWBPIPE-INTAKE-20260928-DECISION-4 D4-3; APP-V4-SWBPIPE-INTAKE-20260928-DECISION-5), which the SCA-V4-001 delta covered only in the Notes of D-002; D-003 (ASC-ISS-001, option a). The override was accepted and applied under SCA-V4-001 (DECISION-7, DECISION-8); this row adds no new override."
{AMENDMENT_ID},DL-SCA-V4-001-A42-D-11c,OTHER,projects/chirality-app-v4/execution/_Decomposition/checkpoint_snapshots/GROUP3-20260928T001055Z/canonical/Deliverables.csv,"DeliverableID DEL-05-01, column Description, substring (D-11c)",DELIVERABLES_DEL_05_01_DESCRIPTION_D_11c,constrain local traffic,SUPERSESSION,limit traffic to the selected model service and allowed destinations,,,,"Path-level binding for SCA-V4-001 action 42 (D-11c; APP-V4-SWBPIPE-INTAKE-20260928-DECISION-5), which the SCA-V4-001 delta covered only in the Notes of D-003 (ASC-ISS-001, option a). The override was accepted and applied under SCA-V4-001 (DECISION-7, DECISION-8); this row adds no new override."
{AMENDMENT_ID},DL-SCA-V4-001-A42-D-11d,OTHER,projects/chirality-app-v4/execution/_Decomposition/checkpoint_snapshots/GROUP3-20260928T001055Z/canonical/Deliverables.csv,"DeliverableID DEL-05-01, column AnticipatedArtifacts, substring (D-11d)",DELIVERABLES_DEL_05_01_ANTICIPATEDARTIFACTS_D_11d,"TEST: malformed-call, endpoint and responsiveness conformance cases",SUPERSESSION,"TEST: malformed-call, destination and responsiveness conformance cases",,,,"Path-level binding for SCA-V4-001 action 42 (D-11d; APP-V4-SWBPIPE-INTAKE-20260928-DECISION-5), which the SCA-V4-001 delta covered only in the Notes of D-003 (ASC-ISS-001, option a). The override was accepted and applied under SCA-V4-001 (DECISION-7, DECISION-8); this row adds no new override."
{AMENDMENT_ID},DL-SCA-V4-001-A46-D-12a,OTHER,projects/chirality-app-v4/execution/_Decomposition/checkpoint_snapshots/GROUP3-20260928T001055Z/canonical/Deliverables.csv,"DeliverableID DEL-09-07, column Description, substring (D-12a)",DELIVERABLES_DEL_09_07_DESCRIPTION_D_12a,actual human acts and endpoint-only operation.,SUPERSESSION,actual human acts and host-agent traffic only to the selected model service and allowed destinations.,,,,"Path-level binding for SCA-V4-001 action 46 (D-12a; APP-V4-SWBPIPE-INTAKE-20260928-DECISION-5), which the SCA-V4-001 delta covered only in the Notes of D-003 (ASC-ISS-001, option a). The override was accepted and applied under SCA-V4-001 (DECISION-7, DECISION-8); this row adds no new override."
{AMENDMENT_ID},DL-SCA-V4-001-A46-D-12b,OTHER,projects/chirality-app-v4/execution/_Decomposition/checkpoint_snapshots/GROUP3-20260928T001055Z/canonical/Deliverables.csv,"DeliverableID DEL-09-07, column Description, substring (D-12b)",DELIVERABLES_DEL_09_07_DESCRIPTION_D_12b,human checkpoints override autonomy;,SUPERSESSION,human checkpoint acts are never substituted by autonomy (holds only in the governance phase);,,,,"Path-level binding for SCA-V4-001 action 46 (D-12b; APP-V4-SWBPIPE-INTAKE-20260928-DECISION-4 D4-1), which the SCA-V4-001 delta covered only in the Notes of D-015 (ASC-ISS-001, option a). The override was accepted and applied under SCA-V4-001 (DECISION-7, DECISION-8); this row adds no new override."
{AMENDMENT_ID},DL-SCA-V4-001-A46-D-12c,OTHER,projects/chirality-app-v4/execution/_Decomposition/checkpoint_snapshots/GROUP3-20260928T001055Z/canonical/Deliverables.csv,"DeliverableID DEL-09-07, column Description, substring (D-12c)",DELIVERABLES_DEL_09_07_DESCRIPTION_D_12c,all local traffic stays on the configured endpoint.,SUPERSESSION,"all host traffic goes only to the selected model service and person-allowed destinations, each recorded.",,,,"Path-level binding for SCA-V4-001 action 46 (D-12c; APP-V4-SWBPIPE-INTAKE-20260928-DECISION-5), which the SCA-V4-001 delta covered only in the Notes of D-003 (ASC-ISS-001, option a). The override was accepted and applied under SCA-V4-001 (DECISION-7, DECISION-8); this row adds no new override."
{AMENDMENT_ID},{D_SEQ_DEL0401},OTHER,projects/chirality-app-v4/execution/_Decomposition/checkpoint_snapshots/GROUP3-20260928T001055Z/canonical/Deliverables.csv,"DeliverableID DEL-04-01, column Description, substring",DELIVERABLES_DEL_04_01_DESCRIPTION_CHECKPOINT_OVERRIDE,PKG-02 checkpoints override autonomy;,SUPERSESSION,PKG-02 checkpoint acts are never substituted by autonomy (holds only in the governance phase);,,,,"APP-V4-SWBPIPE-INTAKE-20260928-DECISION-4 D4-1, parallel to SCA-V4-001 D-12b (DEL-09-07). ASC-ISS-002. Mirrored in the DEL-04-01 _CONTEXT.md Description line."
```

---

## Record fixes carried (V13)

- **F2** is fixed by Part C.
- **F1 is disclosed, not rewritten.** The SCA-V4-001 group-3
  `ACCEPTED_MANIFEST.csv` gives the `OWNER_DECISIONS.md` row the boundary
  text "hash at 3d006a909 (= presented bytes at 230bf1e64/9ae24fc0f)". That
  equality is false for this one row:
  - the file is `cdc486801ae6315a…` at `9ae24fc0f`, and `752876c16f7f96ef…`
    at `3d006a909`;
  - DECISION-8 was appended after the presentation;
  - the hash in the manifest (`752876c1…`) and its Role column ("commit
    3d006a909") are correct.

  The snapshot is immutable. SCA-V4-002's `Brief.md` records this correction
  where it cites the SCA-V4-001 basis. Re-verified here with `git show` at
  both commits.
