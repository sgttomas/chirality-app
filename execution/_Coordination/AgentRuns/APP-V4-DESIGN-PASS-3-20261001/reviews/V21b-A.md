# V21b-A — recheck of V21-A after the repairs RV21-A and RP-final

- Reviewer: the V21-A reviewer, rechecking as V21b-A at HELP_HUMAN's request.
  Type 2 TASK, Claude Opus 5.5. Read-only on the repository except this file.
- Candidate: branch head `65f1d36f5a` ("RP-final: CA examples, GUIDE
  re-pinned 25/25"). It contains RV21-B (`dc61150559`), RV21-A (`31d65b0be3`)
  and RP-final.
- Read: `F/RV21-A.md`; `F/F-E2.md` § "RP-final"; R21-1…R21-4 at the end of
  `R20_RESOLUTIONS.md`; the OWNER_DECISIONS and ASSESSMENT_SIWC diffs; and
  `git diff aa12160bfa 65f1d36f5a` of every file in the six new Design
  folders (word diff, read whole).
- My earlier findings: `reviews/V21-A.md`.

Design files at the candidate (sha256):

| File | sha256 |
|---|---|
| RECOVERY | `678042beae0327e6fcbabb99eaea746d46c843198238ac4dfc67690ea26149c1` |
| NPTD | `6eed39dcee4acf4b8b986cdd9e09c460a8fa53571973cb5c826acce37d644a72` |
| NIR | `7144aebd4a72522d156ea6bae21db78da9343565d68f3f5688a46b35a2f50576` |
| AAC | `062ce28c8a4ec0bc79fc6b6c421245057a59815df14b88fa779b61eeb98be7d7` |
| ACCESS | `929bd07b32f40fc6f65b6df6ce5b7aebe6cd91a89866525a981e5cbe11c4ffa0` |
| ACCOUNT-HOME-RECORD | `f77f87927558ca73ab862fbe1452eaf5a0c47b6bb53b89c1419e2324ec4dad5d` (unchanged) |
| WR | `5b522ce626dcaadd73e5abb46b9db1303d45a9cf2307feface5920d831d056dd` |
| ROLE | `45a748697cf8fca8625a6927417647a30f90e60e0c3020f93fd22bcfc4cd2f3a` (unchanged) |

The six changed files equal GUIDE's RP-final pins; the account-home record
and ROLE are unchanged since V21-A.

## Verdict

**MERGE AS DRAFTS.**

- Both V21-A MAJOR findings and all 14 MINOR findings are fixed. MINOR 12 is
  fixed with one change-table row (V2-6) left as history.
- No new BLOCKING or MAJOR finding.
- Two new MINOR findings: N-1 and N-2 below.

## Status of the V21-A findings

| Finding | Status | Evidence |
|---|---|---|
| **M-1** L-4 multi-entry through the act control | **Fixed** (R21-3) | See "M-1 evidence" below |
| **M-2** attachments rest on `mention` | **Fixed** (R21-2) | See "M-2 evidence" below |
| 1 AAC A15 ordering | Fixed | AI-7 now reads "After capture, for every kind including A15 (AK-f; R18-1 C-22)". §4.4 now reads "for every kind including A15 (AK-e, AK-f)". Rerun: K-15 recovers a capture without an exception |
| 2 AAC entry count | Fixed | §5.3 and VC-AAC-12 say 11 entries; the rerun's K-16 says "all 11 RS entries … are valid" |
| 3 AAC "RS-v0.9 in progress" | Fixed | §4.2 step 6 and §5.3 cite RS-v0.9 as current |
| 4 Stop Codex label | Fixed | NIR TO-4 adds "interrupted by Stop Codex" (cause *codex-stop*). §5.2 uses RECOVERY's labels, and §5.1 cites RECOVERY-v0.2 §3.4 `outcomeLabel`. New check O-3a passes |
| 5 IF-13 wording | Fixed | IF-13 now says "no model selected"; R18-2's wording is left to ST-3, matching NPTD §5.4 |
| 6 TC-2 run-end line | Fixed | TC-2 places R20-3's run-end line first when no run starts. O-8a passes. O-9 validates the composed `turn/start` against `TurnStartParams` |
| 7 RN-2 and VC-NIR-23 | Fixed | RN-2 follows R20-1 and R20-11 (1). VC-NIR-23 expects "End ‹A› and start ‹B›" to be enabled during a run |
| 8 "End run" owner | Fixed | §5.2 reads "DEL-02-03's run end, EXEC; DEL-01-02 DEF-4 defines … and neither performs nor records it" |
| 9 CA-3 and K-3 | Fixed | CA-3 offers "the project's last explicit choice … exactly as ST-2"; the source conversation's model is not offered as such |
| 10 ACCESS live work (C-23) | Fixed | ACCESS §1, AE-12, KE-13 and Q-5 use RECOVERY's `assess live work` and list live turns, outstanding requests and active children |
| 11 resume override | Fixed | RECOVERY §4.1 and §4.2 drop the resume model override. ACCESS Q-11 states the same rule, and ROLE §5.5 already did. A model change is per turn (CS-18). The prototype's resume already sends the thread id only |
| 12 H-probe citation; Continue-as vs fork | Fixed (V2-6 kept as history) | §1 now cites ACCESS §3. CV-21: "'Continue as ‹role›' is a new conversation by `thread/start` … a fork is the person's same-role copy by `thread/fork`". The V2-6 change-table row is left as history, and the RV21 row says it is read with this correction. Acceptable |
| 13 WR §7 and §8 | Fixed | §7's DEL-01-03 row: "only the plan-mode element (choosing Plan) needs Codex's experimental opt-in (K-5 as narrowed by R18-1 C-05)". §8's paragraph now describes RS-v0.9's form and P-36's refusal of `derivedFrom` |
| 14 NPTD `$id`s; optional third-party checks | Fixed | `npt.item-anchor` and `npt.delegation-export` `$id`s are now `…:v0.2`. `npt.plan-revision`, which did not change, stays v0.1. NIR §13.2, the README and the check lines label S-4 and O-9 "optional third-party cross-check" |

**M-1 evidence.**

- **Schemas:** AAC offer and capture schemas 0.3 compose from one descriptor
  per act (`descriptorId`, `descriptorKind`), with the entries inside it.
- **Pattern:** reviewed content now matches `^(draft|entry):(project|user):[^@]+@.+$`.
- **Wording:** the enum adds "register workflow revisions".
- **Rules enforced** (invalid cases INV-OF-10…16 and INV-CE-10…12):
  - an `a15_descriptor` has exactly one `draft:` entry and the singular wording;
  - an `a15_multi_descriptor` has two or more `entry:` entries, no prior
    revision, and the plural wording.
- **Withdrawn reading:** AAC's earlier "several reviewed drafts" reading is
  withdrawn (§1.2, §4.2; several drafts are several acts, AK-d).
- **My independent check:** I copied WR's own `a15_multi_descriptor` example
  (`a15m-rv-9`, `entry:` strings, plural wording, "make them available …")
  into AAC's offer shape. It validates. The singular wording and a `draft:`
  entry under the multi descriptor are both rejected.
- **Prototype:** K-17 (WR's examples run through offer, capture and the RS
  writer) and K-17b (RS act-log record 4) pass.
- **WR side:** RB-4a's stale sentence is replaced, and ME-3 cites AAC.

**M-2 evidence.**

- **NIR §6 rewritten:**
  - It cites OBS-3 W-3 ("nothing reached the model"), W-1 and W-4.
  - Three carriers:
    - `text-element`: supplied;
    - `localImage` / `image-url` / `image-fileId`: supplied, with the read
      "not observed";
    - `path-named`: "named; read only if a tool item shows it", with
      `toolReads`.
  - `mention`, `skill` and the audio inputs are not used.
- **Schema 0.2:** `supplierRead` is set per form; `mention` and `skill` are
  refused as forms (INV-AT-5, INV-AT-6). The `mention` example is replaced.
- **AT-8 (K-7 trial):** follows the same carriers and drops `draft-package`
  (INV-AT-11).
- **Prototype:** A-1…A-8 pass.

## New findings

### BLOCKING

None.

### MAJOR

None.

### MINOR

**N-1. ACCESS §20 still states the owner's acceptance as fact, against the
corrected owner record.**

- **Where:** ACCESS-v0.2 §20 "Decision record" (l.945–949): "HELP_HUMAN's
  recommendation (no pressing need; DEL-01-05 records it as an alternative
  considered, with its triggers; the host-billing point goes on the
  next-relay list) was accepted with L-1 and L-6".
- **The corrected record:** after V21-B m-3, OWNER_DECISIONS says this
  arrangement "is HELP_HUMAN's recommendation, which the owner did not
  separately answer and did not object to". It labels the L-1/L-6 acceptance
  as "Reading (HELP_HUMAN, not owner text)". ACCESS was not in RV21-B's list,
  and RV21-A did not pick it up.
- **Why it matters:** check (1) asks that owner decisions be carried exactly.
  The substance is unaffected ("Not adopted"), but the attribution now
  contradicts the run's owner record.
- **Fix:** replace "was accepted with L-1 and L-6" with "was not separately
  answered by the owner and not objected to; L-1 and L-6 were answered A
  (HELP_HUMAN's reading; OWNER_DECISIONS)".

**N-2. WR TT-3 and NIR AT-8 describe the draft-trial carrier differently.**

- **WR TT-3** (unchanged): "The App pre-fills … a message naming the draft's
  path and content identity". Under R21-2 that is a named path, "named; read
  only if a tool item shows it".
- **NIR AT-8** (RV21) and prototype A-8: the draft's `WORKFLOW.md` and other
  text files "go as text elements (AT-9)", which makes them "supplied".
- **Why it matters:** both routes are allowed by K-7 and R21-2, and either
  is truthful if recorded as what it is. The two files nonetheless describe
  "Try in a conversation" with different carriers and standings.
- **Fix:** WR TT-3 says the pre-fill attaches the draft's text files as text
  elements (AT-9) and names the rest (AT-10), or NIR AT-8 says that TT-3's
  pre-fill names the path. Then cite one from the other.

## Reruns and scripts

**Setup.** `git archive 65f1d36f5a projects/chirality-app-v4 agents tools`
into `$TMPDIR/v21b`; Python 3.13.7, `-B`, `PYTHONDONTWRITEBYTECODE=1`. The
worktree was unchanged afterwards.

**Prototypes.**

| Prototype | V21-A | Now |
|---|---|---|
| RECOVERY `run_cases.py` | 16/16 | 16/16, exit 0 |
| NPTD `run_cases.py` | 18/18 | 18/18, exit 0 (PC-16 per R21-1, 64 combinations; `fixtures/native/*.jsonl` byte-identical to the committed ones) |
| NIR/AAC `run_cases.py` | 120 | 151 checks, 0 failed, exit 0 |
| ACCESS `run_cases.py` | 9/0 | 9/0, exit 0 |
| WR `wrproto.py` | 98/98 | 99/99, exit 0 (P-50a: `thread/items/list` pages valid against the generated types) |
| ROLE `run_cases.py` | 36/0 | 36/0, exit 0 |

**Recorded results.** The result lines of the NPTD and NIR
`RUN_2026-10-02_RV21.txt` files equal my rerun after normalising times and
temporary paths: 0 differing lines.

**Independent schema check.** `v21b_schemas.py`, the V21-A script extended to
read the new `instances` and `case` layouts, run with `jsonschema` 4.26.0
(Draft 2020-12) and a registry of every `$id`:

- all 18 schemas are valid;
- 129 instance checks behaved as stated, with 0 unexpected;
- AAC offer: 3 valid / 16 invalid; capture: 2 / 12; NIR attachment: 4 / 11.

**SCC and guard.** `v21a_scc.py` was rerun unchanged. DAG-003's edge files and
every `Dependencies.csv` are unchanged since `aa12160bfa` (empty `git diff`).

- The SCCs are the same: sizes 2, 2, 2, 2, 3 and 13.
- Every proposed row leaves the SCC set unchanged, singly and pairwise.
- DEL-01-02 and DEL-01-03 reach no guarded deliverable.
- RV21 proposes no new row.

**Breakage search in scope.**

- I read every changed line in the six folders.
- Joins rechecked:
  - NIR IF-5 ↔ AAC ↔ WR descriptors;
  - NIR TC-2 ↔ WR TX-5;
  - NIR ↔ RECOVERY labels;
  - ACCESS ↔ RECOVERY `assess live work`;
  - RECOVERY ↔ ACCESS ↔ ROLE resume;
  - NPTD §7.1 ↔ ROLE B-9 (ROLE states the C-04 signals without an order;
    no conflict);
  - WR SC-3 ↔ RECOVERY's history-read guidance.
- Nothing broken beyond N-1 and N-2.
