#!/usr/bin/env python3
"""AK2 part 1: F-2, the SCA-V4-003 snapshot Decision_Log.md group-3 standing lines, row and execution records.
Exact replacements per the presented F-2 row; the file must equal its blob at 84b520742d. Usage: finalize_decision_log.py REPO LOG.json
"""
import hashlib, json, os, subprocess, sys
REPO, LOG = sys.argv[1:3]
P = "projects/chirality-app-v4/execution/_ScopeChange/SCA-V4-003_2026-10-03_1827/Decision_Log.md"
b = open(os.path.join(REPO, P), "rb").read()
if b != subprocess.run(["git", "-C", REPO, "show", f"84b520742d:{P}"], capture_output=True, check=True).stdout:
    raise SystemExit("FAIL: Decision_Log.md differs from its blob at 84b520742d")
t = b.decode()
STAND_OLD = "**Standing: CANDIDATE amendment folder (posture `ACCEPTED_PREDECESSOR`);\ncheckpoint group 3 not yet presented.** Human decisions are quoted exactly;\n"
STAND_NEW = "**Standing: ACCEPTED amendment snapshot (posture `ACCEPTED_PREDECESSOR`);\ncheckpoint group 3 accepted by DECISION-2 on 2026-10-03.** Human decisions are quoted exactly;\n"
ROW_ANCHOR = "and `SCA-V4-003_GROUP-2_2026-10-03/` (`ec267bdb9f`) |\n"
ROW = ("| DECISION-2 | 2026-10-03 | K2: scope-change group 3 | \"I accept the audited result.\" | same file (sha256 `29c0a07b…8c2e`), "
       "added by `84b520742d` (local time America/Denver, MDT, as recorded). Recorded in `checkpoint_snapshots/SCA-V4-003_GROUP-3_2026-10-03/`. "
       "The package presented was this candidate at `fa16393978` with its records at `388fc730b9` and review V24 |\n")
SECTION = """
## Execution-stage records (node AK2 part 1, after DECISION-2)

- **E-13 · F-1, the group-3 decision snapshot.**
  `checkpoint_snapshots/SCA-V4-003_GROUP-3_2026-10-03/` was transcribed from
  DECISION-2. It holds:
  - `DECISION.md` (`b6e90900…af60`), whose first line is the accepted heading;
  - `ACCEPTED_MANIFEST.csv` (`b3651c16…a847`), 42 rows, each equal to its
    blob at `84b520742d`; the 13 artifacts are at their presented hashes
    (`RUN/Application/CANDIDATE_ARTIFACTS.sha256`, 13/13);
  - `Handoff_State.md` (`07a2f0f0…fe01`).

  It is written before every other post-act edit; the manifest binds the
  pre-act bytes (`RUN/Application/gen_group3_manifest.py`).
- **E-14 · H-1 applied (B-01).**
  - Slots: `{ACCEPT_DATE}` = `2026-10-03` and `{AMENDMENT_SNAPSHOT}` =
    `SCA-V4-003_2026-10-03_1827`. The four clause slots are filled with the
    group-2 values (no item was declined).
  - The old block occurred once; the new block occurred zero times before
    and once after; exactly two lines were added.
  - `SOFTWARE_DECOMP.md`: `ea3388bc…d7d5` → `983199cc…a70d`, equal to the
    expected result in `RUN/Application/SIMULATED_POSTACCEPT.md`.
  - A dry run to scratch first gave identical bytes.
  - Script and log: `_PostAcceptanceValidation/SCA-V4-003_20261004T005706Z/apply_group3_edits.py`
    and its `apply_log.json`.
- **E-15 · H-2 applied (C-01).** `_ScopeChange/_LATEST.md` was rewritten
  from the C-01 text.
  - Slots: `{CLOSURE_VERDICT}` = `OPEN_PENDING_DERIVATIVE_CLOSURE`;
    `{G1_DATE}` = `{G2_DATE}` = `2026-10-03`; `{C02_UTC}` =
    `20261004T002903Z`; `{UTC}` = `20261004T005706Z`.
  - Hash: `2b7938bc…c2e1` → `19cf31f1…e657`.
  - The registered parser `_latest_pointer_target` returns
    `SCA-V4-003_2026-10-03_1827`, and `_pointer_matches` is True.
  - Every path the pointer names exists.
- **E-16 · F-2…F-4.** Only the accepted status lines were changed, exactly
  as the presented list gives them:
  - this log's standing lines and the DECISION-2 row, plus this section;
  - `Handoff_State.md`: title, status paragraph, verdict line, two state
    fields, an "Applied after the act" table. `4f3f31b9…c167` →
    `775fb93f…38f8`;
  - `RUN_SUMMARY.md`: title, two bullets, verdict line, two state fields.
    `9478bd5f…e7f2` → `e864fd27…ccd0`.

  Script and log: `RUN/Application/finalize_status.py`,
  `finalize_status_log.json` and `finalize_decision_log.py`. The other ten
  artifacts are unchanged.
- **E-17 · H-3, the post-acceptance validation.**
  - Record: `_PostAcceptanceValidation/SCA-V4-003_20261004T005706Z/`.
  - Audit (`RUN/POSTACCEPT/`): the baseline `audit_checks.py`, unchanged,
    over PKG-01, 02, 03, 04, 05, 09 and 10.
  - Result: **0 BLOCKER, 51 WARNING, 77 INFO**. Check 10 is PASS/PASS with
    active snapshot SCA-V4-003, and the parser matches.
  - The IssueLog and Matrix are byte-identical to the simulation
    (`RUN/Application/SIMULATED_POSTACCEPT.md`).
  - Against POSTCHANGE: COV-129 is absent and COV-123 carries the H-1 hash.
  - The script's known wording limits are disclosed (Handoff_State, H-3).
"""
for o, n in ((STAND_OLD, STAND_NEW), (ROW_ANCHOR, ROW_ANCHOR + ROW)):
    if t.count(o) != 1:
        raise SystemExit(f"FAIL: anchor count {t.count(o)}: {o[:50]!r}")
    t = t.replace(o, n, 1)
t = t + SECTION
open(os.path.join(REPO, P), "wb").write(t.encode())
json.dump({"path": P, "before": hashlib.sha256(b).hexdigest(), "after": hashlib.sha256(t.encode()).hexdigest()}, open(LOG, "w"), indent=2)
print(hashlib.sha256(t.encode()).hexdigest())
