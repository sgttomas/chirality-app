# SCA-V4-001 post-acceptance validation

Owner act: DECISION-8, 2026-09-29 ("Accept (Recommended)"; `checkpoint_snapshots/SCA-V4-001_GROUP-3_2026-09-29/`). Accepted basis `3d006a909` (candidate `230bf1e64`, presentation `9ae24fc0f`). Applied state: uncommitted working tree over `3d006a909`. Record `SCA-V4-001_20260929T132946Z`. Written by `verify_post_acceptance.py`, which recomputes the applied bytes from the accepted basis independently of `apply_group3_edits.py`. The candidate evidence reviewed at group 3 (POSTCHANGE/, V11) is not modified.

| Check | Result | Detail |
|---|---|---|
| 1a group-3 DECISION.md first line is the accepted heading (check_amendment_reopen.py form) | PASS | # SCA-V4-001 checkpoint group 3 — accepted audited poststate |
| 1b DECISION-8 labels quoted verbatim in DECISION.md and present in OWNER_DECISIONS.md | PASS | 3/3 labels |
| 1c OWNER_DECISIONS.md custody hash equals the cited hash and its blob at 3d006a909 | PASS | 752876c16f7f96ef5d63609d995596f1ac838152b561bc7b9c0b2aa6e3ddea10 |
| 1d group-3 ACCEPTED_MANIFEST.csv binds the presented bytes (every row equals its blob at 3d006a909) | PASS | 36 rows; mismatches [] |
| 1e group-3 folder holds DECISION.md, ACCEPTED_MANIFEST.csv, Handoff_State.md | PASS | ['ACCEPTED_MANIFEST.csv', 'DECISION.md', 'Handoff_State.md'] |
| 2a BASIS_AMENDMENT.md is the accepted bytes | PASS | 04bdc91622223510870ac8fe3994d708641c5e07a7853c5abc75ac59c0ed24cf |
| 2b A07 pair 1: filled old block occurs exactly once in the accepted candidate | PASS | projects/chirality-app-v4/docs/PRD.md count 1 |
| 2b A07 pair 2: filled old block occurs exactly once in the accepted candidate | PASS | projects/chirality-app-v4/docs/PRD.md count 1 |
| 2b A07 pair 3: filled old block occurs exactly once in the accepted candidate | PASS | projects/chirality-app-v4/docs/PRD.md count 1 |
| 2b A17a pair 1: filled old block occurs exactly once in the accepted candidate | PASS | projects/chirality-app-v4/docs/ARCHITECTURE.md count 1 |
| 2b A17b pair 1: filled old block occurs exactly once in the accepted candidate | PASS | projects/chirality-app-v4/docs/HOST_INTEGRATION.md count 1 |
| 2b A17c pair 1: filled old block occurs exactly once in the accepted candidate | PASS | projects/chirality-app-v4/docs/EXAMINATION.md count 1 |
| 2b D-15 pair 1: filled old block occurs exactly once in the accepted candidate | PASS | projects/chirality-app-v4/execution/_Decomposition/SOFTWARE_DECOMP.md count 1 |
| 2c seven held pairs found (A07 x3, A17a, A17b, A17c, D-15) | PASS | 7 |
| 2d projects/chirality-app-v4/docs/PRD.md equals accepted candidate + filled edits | PASS | bb6e786f7a6c01dc5ce2f16f58e6c600989a12808ff47ce4fd87924bcc6c49bd |
| 2e projects/chirality-app-v4/docs/PRD.md carries no unfilled token | PASS |  |
| 2d projects/chirality-app-v4/docs/ARCHITECTURE.md equals accepted candidate + filled edits | PASS | 317d5789272c5206599936fa9b4e68551b30016d226b88039f0153afa02d828c |
| 2e projects/chirality-app-v4/docs/ARCHITECTURE.md carries no unfilled token | PASS |  |
| 2d projects/chirality-app-v4/docs/HOST_INTEGRATION.md equals accepted candidate + filled edits | PASS | 6c6854f941c714d8287bf799e1427bd4d99450847341bdf885ce4158d77eb122 |
| 2e projects/chirality-app-v4/docs/HOST_INTEGRATION.md carries no unfilled token | PASS |  |
| 2d projects/chirality-app-v4/docs/EXAMINATION.md equals accepted candidate + filled edits | PASS | 471798bc2f2dc0202ae40d9d5cf033a22ae41af2a0afdf58032cf37a687957d0 |
| 2e projects/chirality-app-v4/docs/EXAMINATION.md carries no unfilled token | PASS |  |
| 2d projects/chirality-app-v4/execution/_Decomposition/SOFTWARE_DECOMP.md equals accepted candidate + filled edits | PASS | 7434058164f9e53f146793b85c38845a562fbc9ffd46f2b97de18e8d597e5747 |
| 2e projects/chirality-app-v4/execution/_Decomposition/SOFTWARE_DECOMP.md carries no unfilled token | PASS |  |
| 3a Consolidated_Coverage.csv equals the B8 rule applied to the accepted candidate and the applied documents | PASS | 4eee4bcb1cb296a9e96f9c44f934f19913dd827b43666475505e684a646a8db1 |
| 3b only SHA256, ReadSnapshot and SourceLine changed; 126 rows recomputed, 18 other rows untouched | PASS | cols ['ReadSnapshot', 'SHA256', 'SourceLine']; 126/18 |
| 3c Standing: nine rows end 'amended by SCA-V4-001', none doubled | PASS | 9; doubled 0 |
| 4a every changed path is inside the post-acceptance write boundary | PASS | 31 paths; outside [] |
| 4b no ScopeOfWork.md, Dependencies.csv, _DEPENDENCIES.md, _DAG, _STATUS.md or Coverage_Telemetry.json changed | PASS | [] |
| 4c nothing outside projects/chirality-app-v4 changed | PASS | [] |
| 5 GROUP-1_2026-09-28 ACCEPTED_MANIFEST.csv rows still match the working tree (append-only custody record checked at f4ba34c2c) | PASS | 8 rows; mismatches []; append-only since binding ['OWNER_DECISIONS.md'] |
| 5 GROUP-2_2026-09-28 ACCEPTED_MANIFEST.csv rows still match the working tree (append-only custody record checked at f4ba34c2c) | PASS | 9 rows; mismatches []; append-only since binding ['OWNER_DECISIONS.md'] |
| 6a _LATEST.md names exactly one active snapshot, the accepted SCA-V4-001 folder | PASS | ['execution/_ScopeChange/SCA-V4-001_2026-09-28_2155/'] |
| 6b active snapshot holds every required PROJECT/SOFTWARE artifact | PASS | missing [] |
| 6c accepted Handoff_State.md names snapshot, derivative status, verdict, next workflows, residuals, crosswalk, F3 | PASS | missing [] |
| 6d exactly one SCA-* amendment snapshot folder exists | PASS | ['SCA-V4-001_2026-09-28_2155'] |
| 7a audit-decomp rerun: 0 BLOCKER | PASS | 0/38/94 |
| 7b Change Register binds ('Decision Log', rank exact); the COV-131 Change Register part is closed | PASS | [{"target": "Decision Log", "rank": "exact", "hit": "Decision Log", "ambiguous": []}, {"target": "Revision History", "rank": null, "hit": null, "ambiguous": []}] |
| 7c Check 10 active snapshot and handoff state PASS | PASS | PASS/PASS |
| 7d topology unchanged (11 packages, 41 deliverables, 10 objectives, 262 scope items) | PASS | {"packages": 11, "deliverables": 41, "objectives": 10, "scope_items": 262, "ledger_rows": 262} |
| 8 accumulate_supersession_map.py --check-map on the active snapshot | PASS | Wrote supersession map: <scratch>/Supersession_Map.regen.csv Rows: 11 Findings: 0 total, 0 blocking |
| 9a DAG-001 currency (run from the execution root) | PASS | 130/130 OK, exit 0 |
| 9b no deliverable is ISSUED (the ISSUED-reopen rule does not apply) | PASS | {"IN_PROGRESS": 14, "INITIALIZED": 27} |

## Applied and finalized files (sha256)

| File | sha256 |
|---|---|
| `projects/chirality-app-v4/docs/ARCHITECTURE.md` | `317d5789272c5206599936fa9b4e68551b30016d226b88039f0153afa02d828c` |
| `projects/chirality-app-v4/docs/EXAMINATION.md` | `471798bc2f2dc0202ae40d9d5cf033a22ae41af2a0afdf58032cf37a687957d0` |
| `projects/chirality-app-v4/docs/HOST_INTEGRATION.md` | `6c6854f941c714d8287bf799e1427bd4d99450847341bdf885ce4158d77eb122` |
| `projects/chirality-app-v4/docs/PRD.md` | `bb6e786f7a6c01dc5ce2f16f58e6c600989a12808ff47ce4fd87924bcc6c49bd` |
| `projects/chirality-app-v4/execution/_Decomposition/Consolidated_Coverage.csv` | `4eee4bcb1cb296a9e96f9c44f934f19913dd827b43666475505e684a646a8db1` |
| `projects/chirality-app-v4/execution/_Decomposition/SOFTWARE_DECOMP.md` | `7434058164f9e53f146793b85c38845a562fbc9ffd46f2b97de18e8d597e5747` |
| `projects/chirality-app-v4/execution/_ScopeChange/SCA-V4-001_2026-09-28_2155/Decision_Log.md` | `59c72a170a33c7d862fb9975ff2f0fde910aef0d1f1bc5b2775bdefaa275e80b` |
| `projects/chirality-app-v4/execution/_ScopeChange/SCA-V4-001_2026-09-28_2155/Handoff_State.md` | `ef587eddd15deea6ee22f0800f2efc7dfb6209e193a16ffae2f0284987a1ef79` |
| `projects/chirality-app-v4/execution/_ScopeChange/SCA-V4-001_2026-09-28_2155/RUN_SUMMARY.md` | `851fce50b4edce9c0bcbf2ed87e5b9b8c9070e46743a57ea32f4d6f7ddd97d1e` |
| `projects/chirality-app-v4/execution/_ScopeChange/_LATEST.md` | `a9a7cdc8c50a36fbdd25fc53c72322972ba4f9b4d301d811e1a9c1381966339d` |
| `projects/chirality-app-v4/execution/_ScopeChange/checkpoint_snapshots/SCA-V4-001_GROUP-3_2026-09-29/ACCEPTED_MANIFEST.csv` | `2c8c89053d793552a15bd5bbcb428fd7d6d0c96c02c2347baa00098657993274` |
| `projects/chirality-app-v4/execution/_ScopeChange/checkpoint_snapshots/SCA-V4-001_GROUP-3_2026-09-29/DECISION.md` | `640f0fe3fbbfd37eca28f1b53ceea0f7751220244658e415102b07f4bdf17d3d` |
| `projects/chirality-app-v4/execution/_ScopeChange/checkpoint_snapshots/SCA-V4-001_GROUP-3_2026-09-29/Handoff_State.md` | `0b61c6ae3cfd2c7ebe6495be3791b2715d1d0f49ee455bc5566382b357192f65` |

Result: PASS
