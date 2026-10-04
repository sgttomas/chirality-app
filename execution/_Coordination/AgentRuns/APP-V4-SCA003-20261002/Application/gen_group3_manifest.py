#!/usr/bin/env python3
"""AK2 part 1: ACCEPTED_MANIFEST.csv of checkpoint_snapshots/SCA-V4-003_GROUP-3_2026-10-03/.
Binds the presented bytes: every row must equal its blob at the act commit 84b520742d (refuses otherwise).
Usage: gen_group3_manifest.py REPO
"""
import csv, hashlib, io, os, subprocess, sys
REPO = sys.argv[1]
ACT = "84b520742d"
E = "projects/chirality-app-v4/execution"
C = f"{E}/_ScopeChange/SCA-V4-003_2026-10-03_1827"
R = f"{E}/_Coordination/AgentRuns/APP-V4-SCA003-20261002"
G = f"{E}/_ScopeChange/checkpoint_snapshots"
pres = "presented bytes at 388fc730b9; hash at 84b520742d"
rows = [
 (f"{C}/Handoff_State.md", "group-3 presentation (candidate handoff state with the acceptance-time list F-1 to F-4 and H-1 to H-3, the date rule, the propagation table and the parsable closure verdict)", f"The handoff the owner accepted; finalized after this act by F-3 (accepted status lines only); {pres}"),
 (f"{C}/RUN_SUMMARY.md", "group-3 presentation (candidate run summary)", f"Accepted; finalized after this act by F-4 (accepted status lines only); {pres}"),
 (f"{C}/Decision_Log.md", "candidate decision log", f"Accepted; the group-3 standing lines, row and records are added after this act by F-2; {pres}"),
 (f"{C}/Amendment_Actions.csv", "action register", f"Bound at group 2 (SCA-V4-003_GROUP-2_2026-10-03); unchanged; {pres}"),
 (f"{C}/Supersession_Delta.csv", "accepted supersession delta (D-021)", f"Takes effect through Supersession_Map.csv when _LATEST.md names this snapshot; unchanged; {pres}"),
 (f"{C}/Supersession_Map.csv", "cumulative supersession map (30 rows)", f"Accepted; becomes active with _LATEST.md; unchanged; {pres}"),
 (f"{C}/Amendment_Preview.md", "accepted exact amendment (rendered; transcription after the group-2 act)", f"Unchanged; the bound packet governs; {pres}"),
 (f"{C}/Propagation_Plan.md", "accepted propagation plan (rendered; transcription after the group-2 act)", f"Unchanged; the bound packet governs; {pres}"),
 (f"{C}/Brief.md", "intake brief (transcription after the group-1 and group-2 act)", f"Keeps its candidate standing line; unchanged; {pres}"),
 (f"{C}/Intake_Actions.csv", "group-1 intake actions (transcription)", f"Unchanged; {pres}"),
 (f"{C}/Impact_Assessment.md", "group-1 impact assessment (byte copy of the packet file)", f"Unchanged; {pres}"),
 (f"{C}/Pre_Change_Coverage.json", "pre-change coverage baseline (copy of BASELINE/coverage_summary.json)", f"Unchanged; {pres}"),
 (f"{C}/Post_Change_Coverage.json", "post-change coverage (copy of POSTCHANGE/coverage_summary.json)", f"Execution evidence; unchanged; {pres}"),
 (f"{E}/_Decomposition/Open_Issues.csv", "accepted candidate companion register (B-02 option B, B-03)", f"Accepted as presented; unchanged after this act; {pres}"),
 (f"{E}/_ScopeChange/_PostAcceptanceValidation/SCA-V4-002_20261004T002903Z_EFFECTIVE_STATE/EFFECTIVE_STATE.md", "SCA-V4-002 effective-state note (C-02)", f"Append-only; cited by H-2; {pres}"),
 (f"{E}/_Decomposition/SOFTWARE_DECOMP.md", "decomposition document before H-1 (B-01 held)", f"Pre-act bytes; H-1 applied after this act with ACCEPT_DATE 2026-10-03 (expected result 983199cc...a70d); {pres}"),
 (f"{E}/_ScopeChange/_LATEST.md", "active pointer before this act (names SCA-V4-002)", f"Pre-act pointer; H-2 (C-01) rewrites it after this act; {pres}"),
 (f"{R}/AMENDMENT_PACKET/BASIS_AMENDMENT.md", "source of the acceptance-conditional text (B-01, C-01)", f"Bound at group 2; unchanged; {pres}"),
 (f"{R}/AMENDMENT_PACKET/SOW_REVISIONS_A.md", "source of 63 ScopeOfWork blocks (PKG-01)", f"Bound at group 2; applied only by scope-of-work REVISE after this act; {pres}"),
 (f"{R}/AMENDMENT_PACKET/SOW_REVISIONS_B.md", "source of 84 ScopeOfWork blocks (outside PKG-01)", f"Bound at group 2; applied only by scope-of-work REVISE after this act; {pres}"),
 (f"{R}/AMENDMENT_PACKET/ARC_EFFECT.md", "accepted arc effect and expected DAG-003 departure", f"Bound at groups 1 and 2; unchanged; {pres}"),
 (f"{R}/AMENDMENT_PACKET/IMPACT_ASSESSMENT.md", "accepted impact assessment and propagation outline", f"Bound at groups 1 and 2; unchanged; {pres}"),
 (f"{R}/AMENDMENT_PACKET/OWNER_ITEMS.md", "owner decision sheet (K1)", f"Bound at groups 1 and 2; unchanged; {pres}"),
 (f"{R}/reviews/V24.md", "independent group-3 review", f"READY FOR GROUP 3 after M-1 (fixed at 388fc730b9); no blocking finding; {pres}"),
 (f"{R}/POSTCHANGE/COMPARISON.md", "post-change audit evidence", f"Execution evidence; unchanged; {pres}"),
 (f"{R}/POSTCHANGE/coverage_summary.json", "post-change audit evidence", f"Execution evidence; unchanged; {pres}"),
 (f"{R}/POSTCHANGE/Decomp_Coverage_IssueLog.csv", "post-change audit evidence", f"Execution evidence; unchanged; {pres}"),
 (f"{R}/POSTCHANGE/Decomp_Coverage_Matrix.csv", "post-change audit evidence", f"Execution evidence; unchanged; {pres}"),
 (f"{R}/POSTCHANGE/RUN_SUMMARY.md", "post-change audit evidence", f"Execution evidence; unchanged; {pres}"),
 (f"{R}/POSTCHANGE/audit_checks.py", "post-change audit script (byte-identical to BASELINE)", f"Execution evidence; unchanged; {pres}"),
 (f"{R}/POSTCHANGE/INPUT_MANIFEST.sha256", "post-change audit input manifest", f"Execution evidence; unchanged; {pres}"),
 (f"{R}/Application/apply_sca003.py", "candidate application evidence", f"Execution evidence; unchanged; {pres}"),
 (f"{R}/Application/apply_log.json", "candidate application evidence", f"Execution evidence; unchanged; {pres}"),
 (f"{R}/Application/DAG_CURRENCY.txt", "candidate application evidence (DAG-003 130/130)", f"Execution evidence; unchanged; {pres}"),
 (f"{R}/Application/CANDIDATE_ARTIFACTS.sha256", "the 13 required artifacts at presentation", f"Execution evidence; 13/13 at the act; {pres}"),
 (f"{R}/Application/SIMULATED_POSTACCEPT.md", "simulated post-acceptance audit (0 BLOCKER) and H-1 expected results", f"Execution evidence; unchanged; {pres}"),
 (f"{R}/Application/simulated_postaccept.json", "simulated post-acceptance audit output", f"Execution evidence; unchanged; {pres}"),
 (f"{G}/SCA-V4-003_GROUP-1_2026-10-03/DECISION.md", "group-1 decision record", f"Written before this act; unchanged; {pres}"),
 (f"{G}/SCA-V4-003_GROUP-1_2026-10-03/ACCEPTED_MANIFEST.csv", "group-1 accepted manifest", f"Written before this act; unchanged; {pres}"),
 (f"{G}/SCA-V4-003_GROUP-2_2026-10-03/DECISION.md", "group-2 decision record", f"Written before this act; unchanged; {pres}"),
 (f"{G}/SCA-V4-003_GROUP-2_2026-10-03/ACCEPTED_MANIFEST.csv", "group-2 accepted manifest (binds the register)", f"Written before this act; unchanged; {pres}"),
 (f"{R}/OWNER_DECISIONS.md", "record of the owner's act (DECISION-2; commit 84b520742d)", "Custody record; the act is the quoted owner text only; hash at 84b520742d"),
]
out = io.StringIO(); w = csv.writer(out, lineterminator="\n")
w.writerow(["Path", "SHA256", "Role", "AcceptanceBoundary"])
bad = []
for p, role, b in rows:
    h = hashlib.sha256(open(os.path.join(REPO, p), "rb").read()).hexdigest()
    blob = subprocess.run(["git", "-C", REPO, "show", f"{ACT}:{p}"], capture_output=True, check=True).stdout
    if hashlib.sha256(blob).hexdigest() != h:
        bad.append(p)
    w.writerow([p, h, role, b])
if bad:
    raise SystemExit(f"FAIL: not the presented bytes: {bad}")
open(os.path.join(REPO, G, "SCA-V4-003_GROUP-3_2026-10-03/ACCEPTED_MANIFEST.csv"), "w", newline="").write(out.getvalue())
print(len(rows), "rows; all equal their blobs at", ACT)
