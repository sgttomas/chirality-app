# RP-2 — repairs from V18 in C (DEL-03-01) and P (DEL-03-02)

Run `APP-V4-DESIGN-PASS-2-20260930`, node **RP-2**. Type 2 TASK executor
(Claude Code subagent, Claude Opus 5.5; no delegation). Date 2026-09-30
(local; the final rerun is stamped 2026-10-01 01:32 UTC). Working tree at
`ac8483633c` plus the parallel nodes' uncommitted edits. Resumed once after
a connection error. On resuming, the partial edits (`catalog.schema.json`,
`schema_subset.py`, `read_result.schema.json`, `catalog.example-invalid-3.json`)
were checked against HEAD with `git diff`. All four were correct and
complete, and they were kept.

**Inputs read:**
- BRIEFS.md (sha256 `e3f98d1c8449…`): "Common rules", "Wave B" and "RP", row RP-2.
- R14_RESOLUTIONS.md (`c6a603303693…`, binding), R13_RESOLUTIONS.md (`d0385313660e…`) and R12_RESOLUTIONS.md (`5cf5f574bd73…`).
- `comparisons/V18-1.md` (`fb07e07c66c1…`), `V18-2.md` (`0b00e79b161b…`), `V18-3.md` (`68a067e26af7…`) and `V18-4.md` (`078113d7055b…`).
- C and P whole, with their schemas, examples and prototypes.
- Sibling sections were read only to resolve citations: EXEC §2.4, §2.5 and §3.3; ACT §2.1; LOOP §6.2 and §7 MC-8; RS §4 R15, §5, §6.1 and §7; ADAPTER §4.6 OM-9; CA F-26; XT F-25 and §5.1.1.

**Constraints observed:** no git writes, no network, no package install.
Scratch and run output went under `$TMPDIR` (`rp2-base`, `rp2-sh1-run`,
`rp2-final-run`).

No version step. Each change is a row in the file's "Changes from v0.7"
table, keyed by R14 item or V18 finding.

## 1. Finding → fix → location

### C (DEL-03-01, C-v0.8)

| Finding | Fix | Location |
|---|---|---|
| **R14-7 / R13-1** (V18-3 M-3; V18-4 M-4) | §5.2 rule 1 now states the ruled exception: a read is citable only when the host declares it supplies no workspace identity or generation (in its basis profile or a host statement). The limit is "basis lineage not supplied", comparisons across lineages read *unknown (incomparable)*, and an *omitted* element (or any other missing one) stays *basis incomplete*. R8-12 item 6 sits inside the rule. This replaces "both texts stand until R13". CF-5 is restated, **U-C14 is closed**, and the `read_result.schema.json` `not_supplied` description states the rule. The §10.8 profile row and run-table row name R13-1 | §5.2; §2.3 CF-5; UNRESOLVED; schema; §10.8 |
| V18-3 n-5 | `run_fixture.py` classifies reads by the one ruled rule, replacing options A and B. A new check covers three reads (no-lineage → citable with limit; omitted on the full profile → basis incomplete; T3 → citable) | prototype; §10.8; VC-C-10 |
| V18-3 m-15, R-7, n-3 (C's schema) | `catalog.schema.json` now refuses a destination request entry that is exposed on H or X, or that has no `carried_call` argument. `contains` was added to the validator subset for this. **CX-1** is a conformance rule beyond the schema: a *from argument* declaration names an argument of its own entry. It is stated in §3.5 and checked by `validate_all.py`, which also reruns the three V18-3 mutations. New file: `catalog.example-invalid-3.json` | §3.4; §3.5; schema; `schema_subset.py`; `validate_all.py`; README |
| V18-3 n-2 (NOTE) | OP-C10's class has no form in the schema. This is recorded, not resolved | §3.5 |
| V18-4 m-10 | §10.8 "Does not implement" now lists the gaps CA F-26 and XT F-25 found. No profile was added | §10.8 |
| V18-1 m-1 | V-GR1 now reads "prior act not counted" | §10.4 |
| V18-1 m-5 | A15 is named (not checkpoint-requirable; no entry here performs it) | §0 |
| V18-1 m-8; V18-3 n-1 | §4.1: C-v0.8 and P-v0.8 rows are noted, and the two destination rows go to RS R15, not R7. EI-4 now cites EXEC-v0.6 / LOOP-v0.8, §6.2 cites RS-v0.8, and §0 cites EXEC-v0.6 §2.4–§2.5 | §0; §2.1; §4.1; §6.2 |
| V18-4 n-2 (NOTE) | §8 cites XT-v0.6 §5.1.1 | §8 |
| P join (R14-8 N-18; V18-3 M-1) | SH-1 now emits the explicit `item_left` event on each item that left, and `captured_at` on host-captured A5 and A10. The clock is not advanced, so all other values are unchanged | `simhost.py`; §10.8 |

### P (DEL-03-02, P-v0.8)

| Finding | Fix | Location |
|---|---|---|
| **R14-8 N-18** (V18-4 m-7 (a)) | Item-left events are explicit in `proposal_state.schema.json`. On the item, `item_left` {cause, time, evaluated basis} is required exactly when the item left (refused before any A5, withdrawn, or cleared), its cause must match the item's state, and it is refused on any other item (including PT-15). A standalone `item_left_event` document kind is added. `left_cause` has all five causes. New examples: `-valid-3` (an event) and `-invalid-2` (a refused item without its event). `proposal_states.py --check` verifies the events | §4.3; §4.6; DS-4; schema; prototype |
| **R14-8 N-18: the five contributions** | §13 lists each contribution with its text and schema locus: content identity (PM-6), dispositions, all-items-decided, item-left events, and resulting objects. **All five are offered.** | §13 |
| **R14-6**; V18-2 M-2; V18-4 m-8 | §9 "Tokens" maps each outcome to its `item_state` token (*applied (receipt)* → `applied`). Identity conflict and not known to host are document kinds. `applied_receipt` is not P's token | §9 |
| V18-3 M-1 / R14-4 (supplier side) | `act_ref.captured_at` is added: the host's capture time, absent meaning *not supplied by host*. §9 *accepted* and *rejected* say so | §9; schema; valid example |
| R14-8 N-21; V18-4 m-7 (c) | A resulting object without an identity has it *not supplied* | §9; schema description |
| V18-3 m-13 | §3.1 rule 5: the malformed-sibling part is ruled by R12-7 (LOOP MC-8). U-P9 is narrowed | §3.1; UNRESOLVED |
| V18-3 m-12 | §13 "Provide to DEL-05-02" adds the two v0.8 rows, DS-1…DS-5 and PM-1…PM-4 | §13 |
| V18-1 m-5 | A15 row added in §10; DEL-04-01 now provides A1–A15 | §10; §13 |
| V18-2 m-9 | `proposal.schema.json` workflow `origin` is limited to {project, user, bundled, host} | schema |
| V18-3 n-1 | Body citations of C now point to C-v0.8; §0 cites EXEC-v0.6 §2.4–§2.5 | body |

## 2. Prototype runs

All runs used `python3 -B` (3.13.7) and wrote output under `$TMPDIR`. The
final run directory is `$TMPDIR/rp2-final-run`. Every command exited 0.

| Command (cwd DEL-03-01 `Design/prototype/`) | Observed |
|---|---|
| `run_fixture.py --out $TMPDIR/rp2-final-run` | "22 of 22 checks passed; items recorded: 34; host documents: 30". The R13-1 printout gives one rule: no-lineage → "citable with limit 'basis lineage not supplied'…"; omitted → "basis incomplete: not citable"; T3 → "citable" |
| `validate_all.py --run …` | 8 schemas "subset ok"; 27 instances, all as expected (`catalog.example-invalid-3`: exposure.X, `contains`, CX-1); 3 mutations rejected; "30 validated", "6 validated"; "RESULT: all checks passed" |
| `…/DEL-03-03…/observe_map.py --run …` | "34 dispatch, 11 checkpoint observations, 14 channel statuses"; "RESULT: all checks passed" |
| `…/DEL-03-02…/proposal_states.py --check …` | 10 legal, 5 illegal and 5 item-left cases PASS; "8 recorded-state documents … 2 item-left events, each with cause and time … no other item carries one"; "RESULT: all checks passed" |

Evidence label: *test-double*. Nothing here is host or candidate evidence.

## 3. What other files must now say (returned)

- **ADAPTER (RP-1):**
  - RD-2, OM-9 and UNRESOLVED should state R13-1 as ruled, in the C §5.2 wording.
  - CO-4 should take the cause and time from P's `item_left`, not derive them from state.
  - CO-2 and CO-3 should map `act_ref.captured_at`, or record "not supplied by host" when it is absent (R14-4).
- **RS (RP-1):**
  - §5 should state that C §4.1's two destination rows are recorded under R15, not R7 (V18-1 m-8).
  - R11 should adopt P PM-5's "de-duplication scope exceeded" (R14-3).
- **EXEC (RP-1):**
  - `item_decision` *left* should carry P's `item_left` cause and time.
  - EXEC should cite P-v0.8 §4.3 and §13, and the schema elements (N-21).
- **WD (RP-3):**
  - Use `applied` (P §9 "Tokens").
  - Cite P-v0.8 §13's five-contribution row and `item_left` (N-18).
  - The `derived_from` tuple form (V18-2 m-9) remains WD's.
- **LOOP (RP-4):**
  - Name CI-4 and the held-edition states (V18-3 m-16).
  - Add P's two v0.8 rows (m-11).
- **PANEL (RP-4):** Take P §13's DEL-05-02 additions (m-12).
- **CA and XT (RP-4):**
  - The SH-1 limits are now listed in C §10.8 (F-26/F-25 answered as recorded, not as new profiles).
  - "21 of 21" for the B3 run stays true. The repair rerun is 22 of 22.

**Not done:**
- V18-2 n-1 (whether a workflow may require a destination request entry): this is a WD/EXEC question.
- New SH-1 profiles.
- The OP-C10 class form.

The SH-1 run steps keep the labels `R12-9-a` and `R12-9-b`.

## 4. Files (sha256, 12-char prefix)

C: `CATALOG_AND_READ_BASIS.md` a8c35d7aa637 · `catalog.schema.json` 24d7db75d66f · `read_result.schema.json` 5f71d7184bd3 · `catalog.example-invalid-3.json` (new) 9eea2e878d0d · `prototype/run_fixture.py` 88b8a5300320 · `simhost.py` 27693ccf00e0 · `schema_subset.py` d65b90796f13 · `validate_all.py` c8edbdfa66df · `README.md` 9d7fd8c12fcf.
P: `PROPOSAL_LIFECYCLE_AND_OUTCOMES.md` 2250f872125a · `proposal_state.schema.json` 222de733c7df · `proposal.schema.json` 48fbe625c517 · `proposal_state.example-valid.json` 6b369692c11c · `-valid-3.json` (new) e3ef15f7735f · `-invalid-2.json` (new) ff7e84851d3e · `prototype/proposal_states.py` 2b4ae190182b · `README.md` 7100eee8aa06.

`git status --short`: among the changes, only the files above are mine.
The others are the parallel nodes' (DEL-02-01, DEL-02-03, DEL-05-01).
