#!/usr/bin/env python3
"""AK2 part 1: F-3 and F-4, the accepted status lines of the SCA-V4-003 snapshot's Handoff_State.md and RUN_SUMMARY.md.
Each replacement is exact, from the presented list (Handoff_State F-3/F-4 rows); each old text must occur once and the
file must equal its blob at the act commit 84b520742d before editing. Usage: finalize_status.py REPO LOG.json
"""
import hashlib, json, os, subprocess, sys
REPO, LOG = sys.argv[1:3]
ACT = "84b520742d"
C = "projects/chirality-app-v4/execution/_ScopeChange/SCA-V4-003_2026-10-03_1827"
PAV = "_ScopeChange/_PostAcceptanceValidation/SCA-V4-003_20261004T005706Z"
sha = lambda b: hashlib.sha256(b).hexdigest()
HS_STATUS_OLD = """**Status.** Candidate awaiting the owner's checkpoint group 3. Groups 1 and 2
are accepted (DECISION-1 of run `APP-V4-SCA003-20261002`, 2026-10-03). Group 3
is **not accepted**: no accepted-state marker exists, and
`_ScopeChange/_LATEST.md` still names `SCA-V4-002_2026-09-29_1901`.
"""
HS_STATUS_NEW = """**Status.** Accepted. The owner accepted checkpoint group 3 on 2026-10-03
(DECISION-2 of run `APP-V4-SCA003-20261002`: "I accept the audited result.";
`checkpoint_snapshots/SCA-V4-003_GROUP-3_2026-10-03/`). This folder is the
immutable accepted amendment snapshot, and `_ScopeChange/_LATEST.md` names it
in SPEC §11.2 form. Node AK2 (part 1) applied F-1…F-4 and H-1…H-3 after the
act ("Applied after the act", below). The candidate version of this file as
presented is sha256 `4f3f31b971a8a7c817a32604a22b99697731cd18283f72de4e443d6e099ec167`,
bound in the group-3 manifest. Sections written before the act (the
acceptance-time list, "Remaining human decisions", "Next owning workflows")
are kept as presented; group 3 and steps 1–2 of the next workflows are now
done.
"""
HS_APPLIED = f"""## Applied after the act (DECISION-2, node AK2 part 1)

| # | Target | Result |
|---|---|---|
| F-1 | `checkpoint_snapshots/SCA-V4-003_GROUP-3_2026-10-03/` (`DECISION.md`, `ACCEPTED_MANIFEST.csv` with 42 rows equal to their blobs at `84b520742d`, `Handoff_State.md`) | written; hashes in `{PAV}/POST_ACCEPTANCE_VALIDATION.md` |
| H-1 | `_Decomposition/SOFTWARE_DECOMP.md`: B-01 with `{{ACCEPT_DATE}}` = `2026-10-03`, `{{AMENDMENT_SNAPSHOT}}` = `SCA-V4-003_2026-10-03_1827` | `ea3388bc…d7d5` → `983199cc22c84398000612cd95308c840ad011d302fe31ca110a5aa97e64a70d`, the expected result |
| H-2 | `_ScopeChange/_LATEST.md`: C-01, `{{UTC}}` = `20261004T005706Z` | `2b7938bc…c2e1` → `19cf31f14da259d64c52b33f52598dbe66381f0a887b34a13d3eccce9388e657`; registered parser target `SCA-V4-003_2026-10-03_1827`, match True |
| F-2…F-4 | this folder's `Decision_Log.md`, `Handoff_State.md`, `RUN_SUMMARY.md` | accepted status lines only |
| H-3 | `{PAV}/` and `RUN/POSTACCEPT/` | post-acceptance validation; the unchanged baseline script; result in `POST_ACCEPTANCE_VALIDATION.md` there |

"""
edits = {
 f"{C}/Handoff_State.md": [
  ("# Handoff state — SCA-V4-003 (CANDIDATE, before group 3)\n", "# Handoff state — SCA-V4-003 (ACCEPTED, active snapshot)\n"),
  (HS_STATUS_OLD, HS_STATUS_NEW),
  ("**Closure verdict:** `OPEN_PENDING_DERIVATIVE_CLOSURE` (proposed, for the owner's acceptance at group 3)\n", "**Closure verdict:** `OPEN_PENDING_DERIVATIVE_CLOSURE`\n"),
  ("| `DecompositionTruthState` | `INCOMPLETE` |\n", "| `DecompositionTruthState` | `COMPLETE` |\n"),
  ("| `DownstreamRerunState` | `FROZEN` |\n", "| `DownstreamRerunState` | `IN_PROGRESS` |\n"),
  ("`DecompositionTruthState` is INCOMPLETE because B-02 and B-03 are applied\nand B-01 waits for group 3. `DownstreamRerunState` stays FROZEN until group\n3.\n",
   "`DecompositionTruthState` is COMPLETE: B-02 and B-03 in the candidate, B-01\nby H-1 after the act. `DownstreamRerunState` is IN_PROGRESS: DECISION-2\nauthorizes the propagation, and no rerun had completed at this record. The\naudit states above are confirmed by the H-3 rerun.\n"),
  ("## Post-change validation\n", HS_APPLIED + "## Post-change validation\n"),
 ],
 f"{C}/RUN_SUMMARY.md": [
  ("# Run summary — SCA-V4-003 (CANDIDATE, before group 3)\n", "# Run summary — SCA-V4-003 (ACCEPTED, active snapshot)\n"),
  ("- Group 3 is not yet presented.\n", "- DECISION-2, group 3, \"I accept the audited result.\" (2026-10-03).\n"),
  ("- **Pointer:** `_ScopeChange/_LATEST.md` still names SCA-V4-002 (unchanged).\n", "- **Pointer:** `_ScopeChange/_LATEST.md` names this folder (`Latest: SCA-V4-003_2026-10-03_1827`).\n"),
  ("**Closure verdict:** `OPEN_PENDING_DERIVATIVE_CLOSURE` (proposed, for the owner's acceptance at group 3)\n", "**Closure verdict:** `OPEN_PENDING_DERIVATIVE_CLOSURE`\n"),
  ("| `DecompositionTruthState` | `INCOMPLETE` |\n", "| `DecompositionTruthState` | `COMPLETE` |\n"),
  ("| `DownstreamRerunState` | `FROZEN` |\n", "| `DownstreamRerunState` | `IN_PROGRESS` |\n"),
 ],
}
log = {}
for p, reps in edits.items():
    b = open(os.path.join(REPO, p), "rb").read()
    if b != subprocess.run(["git", "-C", REPO, "show", f"{ACT}:{p}"], capture_output=True, check=True).stdout:
        raise SystemExit(f"FAIL: {p} differs from its blob at {ACT}")
    t = b.decode()
    for o, n in reps:
        if t.count(o) != 1:
            raise SystemExit(f"FAIL: {p}: old text occurs {t.count(o)} times: {o[:60]!r}")
        t = t.replace(o, n, 1)
    log[p] = {"before": sha(b), "after": sha(t.encode()), "replacements": len(reps)}
for p in edits:
    pass
# write only after every check passed
for p, reps in edits.items():
    t = open(os.path.join(REPO, p), "rb").read().decode()
    for o, n in reps:
        t = t.replace(o, n, 1)
    open(os.path.join(REPO, p), "wb").write(t.encode())
json.dump(log, open(LOG, "w"), indent=2)
print(json.dumps(log, indent=1))
