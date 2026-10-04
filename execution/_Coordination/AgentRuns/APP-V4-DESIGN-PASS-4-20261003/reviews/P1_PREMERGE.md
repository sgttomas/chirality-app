# P1 — independent pre-merge review, design pass 4, tranche 1

- **Reviewer:** P1. Type 2 TASK (Claude Opus 5.5), dispatched by HELP_HUMAN
  for run `APP-V4-DESIGN-PASS-4-20261003`. No delegation.
- **Candidate:** commit `d150856784` on `claude/app-v4-design-pass-4`. Its
  merge base with `origin/main` is `13b07065e1`, which is also `origin/main`.
- **Method:** `coordinated-knowledge-work` §3 and §6. I checked only what was
  still unestablished, and did not re-review units that RV or RV2 have
  already confirmed READY.
- **Tools and limits:** read-only git, no network, scratch under
  `$TMPDIR/p1`. Paths below are relative to `projects/chirality-app-v4/execution`
  (E), with `PKG-*/1_Working/` dropped.
- **Write record:** this file only.

## Verdict: **MERGE**

There are no BLOCKING and no MAJOR findings. There are 2 MINOR findings and
5 NOTEs.

Every difference between a unit file at `d150856784` and its last confirmed
bytes is one of the following:

- a recorded closeout pin line;
- one of HELP_HUMAN's three cascade re-pins;
- O-C's ISO-8601 change;
- O-B's last minors;
- or, in one case, the U-EXP-1 closure (P1-F1), which I checked here.

In addition:

- GUIDE-v0.7's A16 rows agree with ACT-v0.10, RS-v0.10 and AAC-v0.3, and the
  GUIDE pin check gives 25/25.
- The fences hold.
- Every prototype reproduces its expected count.

## Findings

### P1-F1 — MINOR (record) — the EXP U-EXP-1 closure is a post-confirmation change that is not in the brief's list of expected differences

- **Claim.** The brief lists four kinds of expected difference: (a) closeout
  pin lines, (b) the cascade re-pins, (c) O-C's ISO-8601 change and (d) O-B's
  last minors. DEL-09-01 `EXAMINATION_PROTOCOL.md` also differs from its last
  confirmed bytes in a fifth way: the U-EXP-1 closure.
- **Evidence.**
  - **What RV confirmed.** RV confirmed EXP-v0.2 at
    `fc5b8230ec2ab81a…` (`RV-EXP-U1.md`, repair confirmation). Those are the
    bytes in `09ca67d094`.
  - **The diff.** A token diff from `09ca67d094` to `d150856784` shows two
    groups of change:
    - O-B's U-EXP-1 closure: L6–7 (header), L47 (`HEAD` → `31d65b0be3`), L57
      (adds R23-22), L660 (the U-EXP-1 row) and L696 (a change-table row);
    - C1's three pin lines: L34, L39 and L43.
  - **Who has already looked at it.**
    - DISPATCH sent the closure "to RV2 for confirmation". RV2's PKG/SQ
      confirmation does not cover EXP.
    - RV-EP checked its scope only: "U-EXP-1 closure only … no rule, schema
      or example".
- **My check.**
  - The L660 text matches R23-22 items 1 and 2.
  - `codex_pin` exists as a change kind in `exam.change-impact.schema.json`,
    as §6.2 requires.
  - `31d65b0be3` holds AAC at `062ce28c…`.
  - All 13 other EXP files equal the hashes that RV-EXP-U1 confirmed.
  - `check_exp.py` gives 77/0.
- **Consequence.** The content is sound and nothing needs to change in it.
  Only the record has a gap: no standing reviewer has stated a confirmation of
  `1371ddb2…`, the bytes the closure produced. HELP_HUMAN may cite this
  finding as that confirmation.

### P1-F2 — MINOR (O-C) — the ISO-8601 change covers the traffic record, but TOP §7's cross-record time comparisons are not stated on instants

- **Claim.** O-C's change answers RV's note in full for `top_check.py`, but it
  leaves one comparison in TOP §7 without a stated time basis.
  - **Answered:** RV's note concerned `top_check.py` comparing interval times
    as strings. The change fixes one time form in the traffic record (TOP §6
    L101), enforces it in the schema, and makes `top_check.py` compare instants.
  - **Not covered:** TOP §7 also orders contact times against times held in
    other records.
- **Evidence.**
  - TOP §7 compares each contact's time with entries from other records:
    - "Allowed set at time t … the A12 records of grants … applied in time
      order";
    - "its allowing entry is in force at t";
    - "any subject contact to a declined destination after the decline".
  - Those grant and decline times come from RS records. In
    `RS_RECORD.schema.json`, `destinationGrant.time`, `actDeclined.time`,
    `humanAct.captureTime` and `entry.writtenAt` are unconstrained strings.
    RECORD_SEMANTICS states no time form.
- **Consequence.** An implementer could order a traffic-record time (`…Z`)
  against an RS time in another form by string order, and so misclassify a
  contact as allowed or not allowed. This is a design gap only: nothing is
  built, and no example is affected.
- **Repair (suggested).** Add one sentence to TOP §7: every time comparison,
  including one against an RS record time, is made on instants. A record time
  that has no UTC offset makes the affected comparison *inconclusive*.
  Alternatively, carry the point to RS at its next touch.

### P1-N1 — NOTE — edge cases in `top_check.py` and the time pattern

- **The pattern admits impossible dates.** The pattern
  `^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}(\.[0-9]+)?Z$`
  accepts values such as month 13 or hour 25.
- **Refusals are not distinguishable.** On such a value, or on a time without
  an offset, `top_check.py` stops with an uncaught `ValueError` and exits 1. A
  run that finds mis-tagged contacts also exits 1. I checked this on a scratch
  record.
- **Fraction digits.** `datetime.fromisoformat` truncates fractions beyond 6
  digits (Python 3.13.7). Two times less than 1 µs apart can therefore compare
  as equal.
- **Leniency.** `top_check.py` accepts non-`Z` offsets that the schema rejects.
- **Effect.** None on the examples.

### P1-N2 — NOTE — the cascade re-pin annotations name C1/C2, and no record gives the resulting hashes

- **The annotations.** TOP L7, DOS L9 and RRM L15 read "(C1/C2 re-pin,
  R23-21 item 4)". HELP_HUMAN made these three re-pins with a script.
- **The records.** The DISPATCH C2 row names HELP_HUMAN as the actor but gives
  no before or after hashes.
- **What this review establishes.** At `d150856784` the files are:
  - TOP `f82a58f6…`;
  - DOS `b2ffba7135652c9e…`;
  - RRM `fcaa65443712…`.

  Each one reverses exactly to its confirmed bytes (P1-C1 below).

### P1-N3 — NOTE — merge with a merge commit

- **The citations.** Some files cite bytes "committed at `09ca67d094`":
  - DEL-09-05 DAC L18 (EXP `fc5b8230…`, a deliberate pin under R23-21
    item 3);
  - GUIDE L2.

  Run records also cite `09ca67d094` and `e4a0c2c4c3`.
- **Why the merge method matters.** A squash or rebase merge would make those
  commits unreachable from `main`. The repository's convention is a merge
  commit (`13b07065e1`, `714199f7be`), which keeps them reachable.

### P1-N4 — NOTE — `VC.md` L9 still pins VA `30f4eae2…`

- VA is now `0dee021d…`.
- `VC.md` is a dated return record, and C2 §3 item 1 already lists this.
- No Design file pins an old VA. The pins of GUIDE `8ca61f2d…`/`3a4f07af…`
  and of ACCESS `7a2ad8e4…` survive only in VA's dated §7.1 inventory and in
  GUIDE's own history line (grep over `E/PKG-*`).

### P1-N5 — NOTE — uncommitted run records at review time

- **What was uncommitted.** During this review the working tree held
  uncommitted edits to three files:
  - `DISPATCH.md`, one row;
  - `reviews/RV2-PKG-U2.md` and `reviews/RV2-SQ-U3.md`, RV2's separate
    confirmation of item (d).
- **Effect on this review.** None. They are not part of the candidate, and no
  prototype reads them. All other files equal `d150856784` (`git diff --stat
  HEAD`).
- **Effect on the merge.** A commit that adds them and this file changes run
  records only.

## What I checked, and how

### C1 — unit files compared with their last confirmed bytes (brief item 1)

**Method.**

- For each of the 177 files under `E/PKG-*` that changed against `13b07065e1`,
  excluding `_STATUS.md`, I took the sha256 at `d150856784`.
- I compared it with the hashes that the reviews and `OWNERS/*.md` confirm,
  and with C1's pre-edit list (`$TMPDIR/c1/design_pre.sha256`).
- **How I obtained the confirmed bytes:**
  - from git where they were committed (`09ca67d094`);
  - from C2's pre-edit copies (`$TMPDIR/c2/orig/`, whose hashes equal C2's
    "before" column);
  - otherwise by **reversing** the recorded pin substitutions in the
    candidate file and checking that the result hashes to the confirmed
    value.
- I also searched every git blob by sha256, and it holds none of the
  CB-1-confirmed DEL-09-07 bytes.

**Files at their confirmed bytes.**

- **Current hash named in a review:**
  - all E-1 and E-2 files;
  - DAC, `fw04_check.py` and its examiner observation;
  - RRM's schemas, `rrm_compare.py` and `run_standing_check.py`, and the
    accounts and judgments;
  - the LHQ-U2 schemas and the valid and CB-1 examples.
- **Current hash in an owner table that a review states it confirmed whole:**
  - O-A "E-1 repairs" (RV-E1: "every file in the CURRENT table");
  - O-B "U1 repair", 14 files (RV-EXP-U1);
  - O-B "U2/U3 repaired", the terms files, `read_tree.py` and the SQ schema
    and invalid set (RV2);
  - O-C "LHQ-U2 — frozen", the CIR examples (RV-LHQ-U2, "All 11 files").
- **Fixtures:**
  - FX-FL1 `MANIFEST.sha256`, 10/10 OK, with the manifest at `0489bc61…` as
    confirmed;
  - RR-E input against `E/RR-E/SUPPLIED.sha256`, 9/9 OK;
  - IS-FX-DP1-3 input against `IS-FX-DP1-3.input-set.json` (`18b9e49b…`,
    confirmed), 7/7, and against RR-F's `SUPPLIED.sha256` (the schema from
    `Design/`);
  - FX-DP1 `MANIFEST.sha256`, 6/6 OK;
  - the `E/` files equal O-A's CURRENT table.
- **Unchanged since `09ca67d094`:** the remaining standing-check fixtures,
  which every later EP confirmation ran on.

**Files that differ from their confirmed bytes, and why.**

| File | Confirmed → now | Difference, as established |
|---|---|---|
| LHQ | `4ee7de26…` (RV) = `09ca67d094` → `20361a0b…` | L10 only: seven pins (CA, C, P, AS, LOOP, HOSTING from C1; GUIDE from C2). (a) |
| EXEC | `3add943d…` (RV-E1) = `09ca67d094` → `138b04eb…` | L6 only: the SoW pin (C1). (a) |
| EXP | `fc5b8230…` (RV) → `ff0187da…` | U-EXP-1 closure (P1-F1), plus L34/L39/L43 (C1). (a) + P1-F1 |
| DOS | `83101523…` (RV) → `b2ffba71…` | Reversing L8 (EXP, C1) and L9 (LHQ, C1, then the cascade) gives `83101523d9c16d0a…` exactly. (a)+(b) |
| RRM | `3a4a1462…` (RV-EP) → `fcaa6544…` | Reversing L15 (DOS, C1, then the cascade) gives `3a4a1462285fc91a…` exactly. (a)+(b) |
| TOP | `a4cd945f…` (RV, CB-1) → O-C ISO `5d147be4…` → `f82a58f6…` | Reversing L7 (LHQ, LOOP, AS) gives `5d147be4c0b441b3…` exactly, the hash O-C records for its ISO version. The CB-1 → ISO step is (c), below. (a)+(b)+(c) |
| traffic schema, invalid examples, `top_check.py` | `25afd32d…`, `829bc8d6…`, `c767c3fa…` → `b7401e1f…`, `0a651f0f…`, `cf128073…` | Equal to O-C's ISO record ("Time form"). (c) |
| PKG | `44c0ac88…` (RV2) → O-B `95722979…` → `0d8d14d2…` | C2 orig (`33aa12a5…`) → now changes only L51 (ACCESS). Reversing C1's L30/L37/L42/L45 gives `95722979a8fe9637…` exactly. (d)+(a) |
| SQ | `f18f26c5…` (RV2) → O-B `a2ad48cf…` → `3e5d0f12…` | C2 orig → now changes only L50. Reversing L36/L38/L54/L56/L67/L69 gives `a2ad48cf6803c9e9…` exactly. (d)+(a) |
| pkg identity schema and 3 example sets, `check_pkg.py`; `sq.step-map.json`, SQ valid and rule-violation examples, `check_sq.py` | RV2 hashes → O-B "in place" table (O-B.md L640–644, L667–670) | (d), listed only: RV2 is confirming separately |

**Review of the (c) content.**

- **Correct.**
  - TOP §6 L101 lists the time fields as window, calibration interval,
    contacts, annex entries and privilege grant.
  - The schema has exactly seven time-valued fields, all
    `$ref: #/$defs/utcTime`: `privilege.granted_at`, `window.start` and
    `window.end`, `system_unattributed[].time`,
    `calibration_setup.interval.start` and `.end`, and `contact.first_seen`
    and `last_seen`.
  - `check_schema` (jsonschema 4.26.0, Draft 2020-12) passes.
  - The valid example (1/1) and the CB-1 examples (2/2) remain valid.
  - All 12 invalid examples are rejected under both jsonschema and DEL-01-01's
    `jsonschema_subset`.
  - The new `INVALID-time-form` fails on exactly one error, the pattern at
    `contacts[0].first_seen`. None of the other 11 invalid examples raises a
    pattern error, so none has its intended reason masked.
  - `top_check.py` compares instants and refuses a time with no offset (I
    checked this).
  - TOP L121 pins `top_check.py` at the current `cf128073…`.
  - The changes-table row L153 matches.
- **Complete:** for the traffic record and `top_check.py`, yes. For TOP §7's
  cross-record comparisons, not quite (P1-F2).
- **Edge cases:** P1-N1.

### C2 — GUIDE-v0.7 (brief item 2)

- **The diff.** I diffed C2's pre-edit copy (`3a4f07af…`) against the
  candidate (`a656682e…`). The changed lines are exactly those that C2 §1
  lists: L2–3, L19–21, L26, L28, L44–45, L335–336, L447, L449, L451 and
  L939–941. Nothing else changed.
- **C1's GUIDE edit.** From `13b07065e1` to `3a4f07af…`, C1 changed L9 and 17
  table rows: C, P, ADAPTER, AS, WD, WD-EX, EXEC, LOOP, HOSTING, CA, RELAY,
  XT, RECOVERY, NPTD, NIR, WR and ROLE. PANEL is untouched, as C1 states.
- **The A16 additions, against their sources:**
  - **§0.** "A1–A16 … A16 *decide*, R23-8, … neither of which a checkpoint may
    require … ACT-v0.10 §4.1" agrees with ACT §4.1 L795–797.
  - **M5.1.** Every element agrees with ACT §2.1 A16 (L342), §2.4 (L413),
    §2.5 (L451) and §4.1, and with RS §6.1 (L520–532) and HA-11 (L587–602):
    - the choice of one alternative;
    - an A8 recorded as an R16 `act_request` with alternatives and
      consequences;
    - binding to the package file's content identity;
    - the request relation and the *alternative chosen*;
    - the App act control;
    - not D2-reserved, and no agent performs it;
    - a package naming another kind (A4–A7, A10, A12, A13, A15) is decided by
      that kind;
    - not checkpoint-requirable.
  - **M5.3.** "A runtime value when the person opens it from DEL-06-02's
    decision view, with no decline" agrees with AAC §1.2 (L98: "No"
    act-declined event; runtime value; R23-2) and §2 AI-9 (L123).
  - **M5.5.** Agrees with ACT §2.5 L451 and with RS §7 L-0 (the A16 sentence),
    L-1 and HA-11:
    - binds to the package file's identity;
    - lapses as an App file;
    - a revised package needs a new A16;
    - a later A16 on the same unchanged package supersedes the earlier one
      for current standing;
    - both stay recorded.
- **Nothing else changed in meaning.**
  - M5.2, M5.4 and M5.8 list no act kinds; I read them.
  - `git diff --word-diff=porcelain 13b07065e1` of ACT, RS and AAC removes
    only label tokens and list tokens that are extended in place: "A1–A15;",
    "purpose" (A8 extended), "(A15)", "R12-5)", "A15)," and the version
    labels.
  - So the v0.9/v0.2 citations that GUIDE keeps still rest on unchanged text.
- **Pin check.** B8's `pins.py` (`$TMPDIR/b8/pins.py`, sha256
  `b943319dc4a00bd7…5423`), run in check mode on the candidate tree, gives
  **match 25/25**.

### C3 — ACCESS §13 row, ScopeOfWork re-pin and the VA note (brief item 3)

- **ACCESS diff from `13b07065e1`:** three changes and no others.
  - new L8, the header line;
  - L28–29, the basis SoW pin;
  - new L773, the §13 row.
- **Register.**
  - The §13 row agrees with DEL-01-05 `Dependencies.csv` (`7100a2e6…bbca`,
    data row 17): DEP-01-05-017, DOWNSTREAM HANDOVER to DEL-09-02, with the
    same statement, citing CLM-004 / G-0105-02 and SC3-01-05-12.
  - DAG-004 `ExcludedRows.csv` L47 gives it disposition MIRROR, SR-6,
    represented by `DEP-09-02-013@13`.
  - LEDGER `R3-01-05-b` is a "new DOWNSTREAM HANDOVER row (mirror of
    DEP-09-02-013)".
  - G-0105-02 appends exactly the CLM-004 sentence.
  - R22-7 and V22 m-7 exist in the pass-3 records.
- **ScopeOfWork re-pin.** The ScopeOfWork changed once, in `2d5e6845c5`, from
  `baf68c79…a4a6` (the parent) to `2e134b57…f3d3`, which is the current hash.
  Blocks G-0105-01…16 exist (16).
- **Reliance untouched.** The three changed regions are outside the parts
  that the dependents cite:
  - PKG relies on §0 and §20;
  - SQ relies on §0 and VC-A01…A13;
  - GUIDE relies on §2, §3, §11 CH-8 and §20.
- **DEL-01-05 `run_cases.py`:** TOTAL 9, FAIL 0.
- **VA.** `diff` against C2's pre-edit copy gives `181a182`: one note line.
  I checked its claim myself. Over every version in `git log --all`, the six
  named hashes (AAC `eca9a079`, ACT `e5bf830c`, RS `1068e295`, EXP
  `dc6b6a0c`, LHQ `2668d955`, TOP `cf0b65f2`) match no commit.

### C4 — closeout re-pins (brief item 4)

**All new pins resolve.** This is a full check, not a sample. In every line
that C1, C2 or the cascade changed, I took each 64-hex value that the line
newly introduced and looked it up among the current files.

- 53 resolve to a current file, and in each case it is the file the label
  names.
- 3 do not, and all three are history: ACCESS's "was `baf68c79…`" and GUIDE's
  `3a4f07af…` and `8ca61f2d…` in its "supersedes" line.
- The 16-hex SoW pins also resolve to their current ScopeOfWork hash: WR
  `fe9f9bd923f94ed3` and ROLE `2327508f2290e7cf`.

**Sibling re-pins sampled (12 of 40).** For each one I checked by diff that
the pinned file changed only outside what is relied on.

| Pin | Pinned file's change | Reliance |
|---|---|---|
| GUIDE EXEC row | EXEC L3 and L6 only | GUIDE cites EXEC §2–§6 |
| GUIDE NIR row | NIR changed only in its header and §5.1, at new L407 and L421 | GUIDE cites §4, §5.2 and §9 PD-5 |
| GUIDE ROLE row | ROLE L47 only | Header |
| DOS L8 EXP | U-EXP-1 lines and pins; the schemas are unchanged | `parts_not_applicable`, `case_definition` |
| PKG L37 EXP | Same | EXP §3.1, §6.1, §8, F-5 |
| SQ L36 RECOVERY | RECOVERY L8 only | Header |
| EXP L39 CA | CA L8 only | Header |
| LHQ L10 HOSTING | HOSTING L8 only | Header |
| LHQ L10 GUIDE (C2) | GUIDE edits at the lines in C2 above | HC-7.3 and HC-7.9 (§3 checklist, around L800) untouched |
| TOP L7 LHQ (cascade) | LHQ L10 only | — |
| RRM L15 DOS (cascade) | DOS L8–L9 only | — |
| PKG L51 and SQ L50 ACCESS (C2) | ACCESS L8, L28–29, L773 | §0, §20 and VC-A rows untouched |

**ScopeOfWork re-pins sampled (6 of 17):** EXEC, ROLE, WR, CA, RELAY and LOOP,
with RECOVERY's diff also read.

- **Each is one pin line,** as the token diff from `13b07065e1` shows.
- **The hashes.** The old hash is the ScopeOfWork's bytes at `2d5e6845c5^`,
  and the new hash is the current bytes. Each ScopeOfWork changed only in
  `2d5e6845c5` since `40e04273da`. The abbreviated "was" values match the full
  old hashes, for example ROLE `…6601` and WR `…924a`.
- **The stated block ranges** exist with the stated counts for all 16
  deliverables in `SOW_REVISIONS_A.md` and `_B.md` (`42c9167a…` and
  `d7b5cb24…`).
- **"None requiring a change".** I read G-0304-01…04 and G-0906-01…05 in
  full. Each traces to text that the design file already states. I spot-checked
  this:
  - GUIDE L5 states the requested and recorded-when-performed rule;
  - CA names DEL-09-01 eight times;
  - CA cites `w14-result-record.schema.json`.

**W14 examples.** Only L31 changed in each example: the run_all sha, now the
current `0bc95d07…`. `run_w14_rehearsals.py --out $TMPDIR/…` gives 44 PASS,
0 FAIL, "ALL CHECKS HOLD".

### C5 — lifecycle (brief item 5)

- **The transitions.** Exactly eight `_STATUS.md` files changed: DEL-01-06,
  06-01, 06-02, 09-01, 09-02, 09-05, 09-07 and 09-11. Each made the same
  three changes:
  - `INITIALIZED` → `IN_PROGRESS`;
  - the date to 2026-10-03;
  - one history line citing R23-28.
- **The tool.** I replayed `tools/scaffolding/write_status.sh` on a scratch
  copy of DEL-01-06's base `_STATUS.md`, with the recorded actor string. The
  output is byte-identical to the candidate's file apart from the date. This
  is consistent with the tool, but it is not proof that the tool was used.
- **R23-28 against root `docs/SPEC.md` §3.3.**
  - The quoted row ("`INITIALIZED → IN_PROGRESS` | Human, WORKING_ITEMS (when
    semantic step is skipped)") is accurate.
  - The semantic step was skipped: all eight `_SEMANTIC.md` files are
    `PLACEHOLDER` ("No semantic-lensing pipeline selected").
  - The WORKING_ITEMS consultation is recorded in BRIEFS.md L5 as
    `9ae4bea25bd9`. That equals the sha256 of `agents/AGENT_WORKING_ITEMS.md`,
    which is unchanged on the branch.

### C6 — fences on the whole branch against `13b07065e1` (brief item 6)

- **Scope.** 200 files changed. None is outside `projects/chirality-app-v4/`,
  and none is outside `execution/`.
- **Governed records.** No ScopeOfWork, `Dependencies.csv`, `_DEPENDENCIES`,
  `_DAG/`, `_ScopeChange`, `_Decomposition` or Open_Issues file changed (a
  path grep returns 0).
- **Home paths.** I scanned the full content of all 200 files at
  `d150856784` for `/Users/<letter>` and `-Users-<letter>`: 0 files.
- **D-GOV-52.** No commit in `git log --all` touches
  `docs/governance_harness/_PROPOSALS/D-GOV-52*`, and none of its files is in
  the index. It remains untracked.
- **Root instructions.** `AGENTS.md`, `CLAUDE.md`, `agents/` and `docs/` are
  unchanged.

### C7 — prototypes, rerun once at the candidate (brief item 7)

- **Conditions.** Each check ran from its folder with
  `PYTHONDONTWRITEBYTECODE=1`, with `TMPDIR` and all outputs under
  `$TMPDIR/p1`. `git status` was identical before and after, and no
  `__pycache__` was left.
- **Not run:** anything in DEL-01-01 `prototype/version_advance/`.

| Check | Result |
|---|---|
| DEL-04-03 `run_prototype.py` | 67 PASS, "all expectations held" |
| DEL-02-03 `run_all.py` | 126 ok, "ALL CHECKS HOLD: 0 failure(s)" |
| DEL-01-04 `run_cases.py` | 159 checks, 0 failed |
| DEL-04-01 `validate_policy.py` | 6 PASS, all held |
| `E/run_e.py` | 56/56 |
| DEL-06-01 `run_fleet.py` | 34/34 (the committed FX-FL1 equals the one rebuilt) |
| DEL-06-02 `run_views.py` | 23/23 |
| DEL-09-01 `check_exp.py` | TOTAL 77, FAIL 0 |
| DEL-01-06 `check_pkg.py --tree` (VC's 0.160.0 vendor tree in the session scratchpad; present) | TOTAL 66, FAIL 0. Without `--tree`: 59/0. I checked the code: tree mode runs only `/usr/bin/codesign -d` and hashing, and its probe trees go to `TMPDIR` |
| DEL-09-02 `check_sq.py` | TOTAL 114, FAIL 0 (65 citations) |
| DEL-09-05 `fw04_check.py` (C1's documented command) | 22 expectations, 0 failed |
| DEL-09-11 `run_standing_check.py` | 19 cases, 0 unexpected |
| DEL-09-07 `top_check.py` | Valid example OK, 4 of 5 compared, exit 0. CB-1 examples: both MIS-TAGGED, exit 1, as designed |
| DEL-09-06 `run_w14_rehearsals.py` | 44 PASS, 0 FAIL |
| Added: DEL-01-05 `run_cases.py` | TOTAL 9, FAIL 0 |
| Added: GUIDE `pins.py` | 25/25 |

### C8 — the older pins in RELAY, ADAPTER and LOOP (brief item 8)

Each of these pins was already present on `origin/main` (`13b07065e1`), on an
identical line, so none is a regression:

- **RELAY** L11 and L23 pin GUIDE-v0.1 `fc96d285…`, whose bytes are first
  found at `cc58211c58`.
- **ADAPTER** L8 and **LOOP** L11 pin ACCESS-v0.1 `8cc7a60f…`, first found at
  `2728ec405e`.

C1 changed ADAPTER L6 and LOOP L9 only.

## What I did not check

- **O-B's last minors (d).** I listed them and did not review them. RV2's
  confirmation was uncommitted in the working tree during this review (P1-N5),
  and I did not rely on it.
- **Units already confirmed READY.** I did not re-review their content.
- **The CB-1-confirmed bytes of TOP, the traffic schema, its invalid examples
  and `top_check.py`.** They are in no git object and no scratch copy. The
  CB-1 → ISO delta is therefore established from the current content and
  O-C's record, not by a byte diff. The ISO version of TOP itself was
  reconstructed exactly.
- **The full counts.** I did not recount C1's 40 sibling re-pins and 17
  ScopeOfWork re-pins one by one. Instead, every newly introduced 64-hex pin
  was checked to resolve (C4). The reliance check was sampled (12 sibling, 6
  ScopeOfWork).
- **The SCA-V4-003 blocks.** I did not read them in full beyond G-0304,
  G-0906 and G-0105-02.
- **The W14 rehearsals.** I did not check their semantics beyond the 44/0
  run.
- **The run records.** I did not check the run-folder records beyond those
  cited above.
