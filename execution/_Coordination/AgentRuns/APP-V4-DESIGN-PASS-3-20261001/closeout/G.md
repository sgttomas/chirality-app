# G — items the closeout returned to the graph (closeout, design pass 3)

Executor: Type 2 TASK (Claude Opus 5.5), dispatched by HELP_HUMAN. Brief:
`BRIEFS.md` "Closeout (after PR #1072)" → "G". Worktree base `0089d583bc`
(clean at start). Read-only git (`git show 63a6e0fa47:…` only); no commit,
stash, checkout or reset; no network; no Codex or model run. Executed
2026-10-02 local time (final rerun 2026-10-03 02:47 UTC).

## 1. Basis read (sha256, `shasum -a 256`, at the start)

| File | sha256 |
|---|---|
| `BRIEFS.md` (common rules; "G") | `11c9c91bfcb4d10c93615828c1a24d176177ca8cad3df3fcfec5071345a43dba` |
| `R22_RESOLUTIONS.md` (R22-1…R22-3) | `2acc830206bd40b30318f0d5f8db0fcb033a77d7297edd78ec737c85b25ec526` |
| `closeout/C1-A.md` (G-A1, G-A2) | `0c2a44af8c09ce32827ae14365a7a6c6f9a0fcc925f70f18453445acf09475d0` |
| `closeout/C1-B.md` (§3.3, §3.4, §7 items 1–2) | `b2b8bfad297f91258bbab45408b0db833b2704c15c665f25cf1157367abe391a` |
| ROLE-v0.1 at `63a6e0fa47` (`git show`) | `692873d1d025b4ab0bc3d741a19bf1facad5d39b875e58ac1f0127042059b644` (equals the hash ROLE-v0.2's header records) |
| RS-v0.9 `RECORD_SEMANTICS.md` (§3 run-ended row; §10 DEL-01-02 row) | `a91882e74064495c5758110deae4cbc7280f3b2a12d0df8592f5238d1afd16e5` |

Also read: D/D3.md §R2.5 (D3 NR-4), the three Design files whole or in the
sections touched, the three prototypes' READMEs and RECOVERY's C-10 table
check.

## 2. Edits (in place, no version steps; a "G" row in each change table)

| File | Items | sha256 before → after |
|---|---|---|
| ROLE-v0.2 `ROLE_SUPPLY.md` (DEL-02-04) | R22-1, R22-2 | `45a748697cf8fca8625a6927417647a30f90e60e0c3020f93fd22bcfc4cd2f3a` → `92bb421b7bccee9a02d33a037736a97bb4d4b1e2136246fa83f75c49291c7e2a` |
| RECOVERY-v0.2 `EXECUTION_AND_RECOVERY.md` (DEL-01-02) | R22-3; G-A1, G-A2 | `678042beae0327e6fcbabb99eaea746d46c843198238ac4dfc67690ea26149c1` → `d84c7e26f4342d261f385877ddea78a9c935c5f561b5b91602d93d9db49fe2cb` |
| NIR-v0.2 `NATIVE_INTERACTION_RECEIVING.md` (DEL-01-04) | R22-3 | `7144aebd4a72522d156ea6bae21db78da9343565d68f3f5688a46b35a2f50576` → `49e180907d39db3d5e6c7fedfaadf9d964aba57b328d84cca1f58fb1aec38ca0` |

No schema, example, prototype or result file was changed.

### 2.1 R22-1 (ROLE)

- §7.2 O-8 now names the role list with its preselection, the fixed-role
  display with "Continue as", and the "guidance changed" notice. It cites
  **D3 NR-4** (DEL-01-04 consumes DEL-02-04; D3 R2.5, NIR IF-15), adopted by
  R22-1 as a held arc inside SCC-002 with no SCC change, and notes that it is
  proposed but not yet in a register.
- §7.3 adds an "Adopted (R22-1)" bullet with the same content. It names
  C1-B's R3-02-04-c as the DEL-02-04 mirror and says R22-1 replaces v0.2's
  runtime-value reading.
- The header's binding line adds R22-1 and R22-2.

### 2.2 R22-2 (ROLE): what was written out, and where it differs from v0.1

Every "as v0.1" deferral is written out from `63a6e0fa47`:

- the input table and the ScopeOfWork reading (header);
- §4.1;
- §4.2 preface, GS-1…GS-6 and T-1;
- CO-1, CO-2, CO-5 and CO-6, with CO-3/CO-4 kept as withdrawn (§5.1);
- the §6.4 table, §8 and §9's reuse table with its closing paragraph;
- F-R1…F-R8 (§13) and §15.

A grep finds no remaining "as v0.1", "as in v0.1" or "unchanged from v0.1"
deferral, except T-1's lead-in, which now reads "v0.1's table, changed where
marked".

The text is v0.1's. It differs only where v0.2's rulings had already changed
it, and each difference is marked "(v0.2)" in place:

| Where | v0.1 → as written | v0.2 basis |
|---|---|---|
| §4.1, GS-5, T-1 missing row | "supply" → "start" | L-2; v0.2 §4.1/§4.2 summaries ("every start is refused", "refuses the start") |
| GS-4 | "at a supply point (§5.4)" → "at a conversation start (§5.1)" | L-2; §5.4 withdrawn |
| GS-6; T-1 rows 7–8; the paragraph after T-1 | "next idle point" / "only through §5.4" → new conversations only, open ones flagged (§4.4) | v0.2 GS-6 and T-1 note (L-2) |
| T-1 restore row | "change cause `guidance-restored`" → `guidance-restored` as the store's result, no longer a supply-record cause | schema 0.2 has no `changeCause` (checked: 0 occurrences) |
| CO-5 | `developerInstructions` → `developerInstructions` on `thread/start` | v0.2 §5.2 (B-8, B-16) |
| §6.4 Supply row | adds "(a same-role fork: `inherited`, §6.1)" | v0.2 §6.1 |
| §9 first row | "the 0.158.0 mechanism check (B-15)" → mechanism observed through an adapter (B-15), carrier open (CR-1a) | v0.2 B-15, CR-1a |
| F-R1, F-R3, F-R8 | v0.2's stated amendments appended | v0.2 §13 |
| F-R7 | "so IP-1 rests on…" → the status reading rests on…, now serving "one start in flight" and relaunch | IP-1 withdrawn (§5.4) |
| F-R1, F-R2, F-R4 | "HOSTING S-6/§8.4", "RS R3" → "HOSTING-v0.8 …", "(RS-v0.8)", in the past tense | version labels only: the findings were written against the v0.8 files v0.1 read |
| §15 | v0.1's list, with v0.2's "adding" sentence merged into it | v0.2 §15 |
| Header | v0.1 input table carried as recorded; the v0.2 line's newer `BRIEFS.md`/`OWNER_DECISIONS.md` hashes said to take precedence | — |

One judgment, flagged for the integrator. v0.2 gave T-1's last two rows the
effect "reaches new conversations; open ones are flagged". For the last row
(a modified copy kept at a new release), the copy does not change, so GC-1
flags nothing. That row now says nothing reaches a conversation until the
person restores or edits the copy. This follows v0.2's meaning (L-2, GC-1),
not its literal wording.

Not adjusted, and reported only: node F has since applied the joins of F-R1,
F-R2 and F-R4 (HOSTING-v0.9 FH-36 and FH-33; RS-v0.9 R3 now carries the
parts). The findings stay as v0.1 findings with version labels, because
recording node F's results in them would go beyond "no meaning change".

### 2.3 R22-3, G-A1, G-A2 (RECOVERY and NIR)

**RECOVERY changes:**
- §3.3 gains "Several windows on one conversation":
  - each window is an observer and shows the interrupt control;
  - the first press writes the one stop request (SR-01);
  - another window's press is refused, `stop-already-requested` (SR-11) or `no-live-turn` after the turn ended (§4.1);
  - that window's control then shows the turn's state from the same stop request, as NIR WI-4 does for cards.
- SR-11's "Recorded / told" cell says the same for another window. The From, Event and To cells are unchanged, so RECOVERY's C-10 table check still holds.
- §8.2's stop-request row now cites RS-v0.9 §10 (DEL-01-02 row: "a turn interrupt is not recorded in format 0.1") and RS-v0.9 §3's run-ended row.
- U-R5 and U-R6 are marked closed in place.

**NIR changes:**
- §4.8 gains **WI-5** beside WI-4: the stop control's behaviour with two windows, with the same rule and refusal reasons, citing RECOVERY-v0.2 §3.3, §3.4 and §4.1.
- §5.2's "Interrupt a turn" row points to WI-5.
- A G row was added to "Changes from v0.1" and a G bullet to "Changes".
- NIR's `prototype/` is outside this node's fence, so WI-5 is designed, not prototyped.
- RECOVERY's model needed no change: SR-11 already refuses a second press, whichever window it comes from.

## 3. Prototype reruns

**Method** (C0's): `cp -R projects/chirality-app-v4` to
`$TMPDIR/g-closeout/{base,after}`, before and after the edits. Runs used Python
3.13.7 with `-B` and `PYTHONDONTWRITEBYTECODE=1`, no record or
example-writing flags. Afterwards, `diff -rq` of the worktree's
`projects/chirality-app-v4` against each scratch copy (excluding
`__pycache__`) found no difference, so no committed output changed.

| Prototype | Before | After |
|---|---|---|
| DEL-01-02 RECOVERY `run_cases.py` | 16 results, 16 as expected; exit 0 | **16/16 as expected**, exit 0; C-10 "58 rows in five tables compared with the model: equal"; C-17 58/58 |
| DEL-01-04 NIR/AAC `run_cases.py` | 151 checks, 0 failed; exit 0 | **151 checks, 0 failed**, exit 0 |
| DEL-02-04 ROLE `run_cases.py` | pass=36 fail=0; exit 0 | **pass=36 fail=0**, exit 0 |

The before and after outputs are identical, once timestamps and scratch-folder
names are masked. The only remaining difference is ROLE's random scratch
suffix.

## 4. Other checks

- **GUIDE pins.** B8's `pins.py`, check-only (`$TMPDIR/c0/pins.py`, sha256
  `b943319d…5423`, unchanged), gave 25/25 before the edits and **22/25**
  after. The three that differ are RECOVERY, NIR and ROLE, as expected.
  **A GUIDE re-pin is needed and is outside G's fence.**
- **DAG-003.** `SOURCE_MANIFEST.sha256` is 130/130 OK and `MANIFEST.sha256`
  is 37/37 OK. G touched no ScopeOfWork, register, `_STATUS.md`, DAG, basis,
  `OBS_*`, `PIN_SPIKE_*`, `generated/` or SWBPIPE file.
- **`git status`.** It shows the three edited Design files and this record.
  Untracked files that other sessions are writing are also present and were
  not touched:
  - `closeout/CLOSEOUT_ACCOUNT.md`;
  - `_Coordination/AgentRuns/APP-V4-SCA003-20261002/BASELINE/*`.

## 5. Notes for the integrator

1. **Re-pin the GUIDE** (22/25 now): RECOVERY, NIR and ROLE.
2. **An ID collision to keep apart.**
   - R22-1's "NR-4" is **D3 NR-4**: DEL-01-04 → DEL-02-04, held.
   - R22-4's "NR-01…NR-04" are **F0's** rows into DEL-01-02.
   - NIR also has a rule NR-4, "Truthful origin".
   - ROLE now writes "D3 NR-4", as C1-A does.
3. **WI-5 has no prototype case.** NIR's prototype is outside G's fence. If
   one is wanted, it can be added at NIR's next touch, beside R-4.
4. **The T-1 last-row reading** (§2.2) is the one place where the meaning
   was made precise rather than copied.

## 6. Return

- **R22-1:** ROLE §7.2 O-8 and §7.3 cite D3 NR-4, adopted as a held arc
  inside SCC-002 with no SCC change.
- **R22-2:** ROLE-v0.2 is now self-contained. Every "as v0.1" section is
  written out from `63a6e0fa47`, and each adjustment v0.2 had already made is
  marked "(v0.2)" in place (§2.2).
- **R22-3:**
  - RECOVERY §3.3 and SR-11 state the two-window stop-control rule.
  - U-R5 is closed.
  - U-R6 is closed by RS-v0.9 §10, which §8.2 now cites.
  - NIR §4.8 WI-5 states the same rule beside WI-4, and §5.2 points to it.
- **Reruns:** RECOVERY 16/16, NIR 151/0 and ROLE 36/0, all exit 0 and
  identical to before.
- **Files written:**
  - `PKG-02_Workflow and role portability/1_Working/DEL-02-04_Additive role selection and supply/Design/ROLE_SUPPLY.md`
  - `PKG-01_Native App and third-party harness integration/1_Working/DEL-01-02_Durable execution and request recovery/Design/EXECUTION_AND_RECOVERY.md`
  - `PKG-01_Native App and third-party harness integration/1_Working/DEL-01-04_Native requests, outcomes and attachments/Design/NATIVE_INTERACTION_RECEIVING.md`
  - `_Coordination/AgentRuns/APP-V4-DESIGN-PASS-3-20261001/closeout/G.md` (this file)
- **Scratch:** under `$TMPDIR/g-closeout/`, plus `$TMPDIR/role_v01.md`.
