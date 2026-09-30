# Dispatch — APP-V4-SCA002-20260929

| Node | State |
|---|---|
| S0 | Graph and owner direction |
| CA1 | SCA-V4-001 closure audit, done after one resume following a connection error: verdict **OPEN**. 47/47 actions verified; no reruns needed. ASC-ISS-001 (11 supersession rows exist only in Notes) is provisional CRITICAL and needs an owner ruling; minor and observation findings ASC-ISS-002…009. Snapshot `_Evaluation/ScopeClosureAudit/ScopeClosure_SCA-V4-001_2026-09-29_1222/`. Fold-in gaps forwarded to P1 |
| P1 | SCA-V4-002 packet RETURNED after resumes following connection errors: 16 MODIFY; 26 SoW blocks in 9 SoWs, dry-run clean, 9/9 validate; all four arcs kept (+4 held, SCCs unchanged); 15 owner items; CA1 folded in. File hashes match the return. Fence verified |
| P3 | Pre-change baseline done after one resume following a connection error: 0 BLOCKER, 38 WARNING (all pre-existing), 101 INFO; scope PKG-01, 02, 03, 04, 05, 09, 10 (PKG-05 added for register row 16); expected source is GROUP3 as amended by SCA-V4-001. No finding changes the accepted packet. Fence verified |
| K1 | Accepted by the owner (DECISION-2, groups 1–2). The owner decided while P3 was still running; P3 then found nothing that changes the packet, so application proceeds |
| AK1 | Decision snapshots; apply basis, decomposition and record edits; post-change audit: ACTIVE |
