# Decomposition coverage report — pre-change baseline for SCA-V4-002 (proposed)

- **Run:** `APP_V4_SCA_V4_002_PRECHANGE`, 2026-09-30T00:52:43Z, basis commit `f05bd1bbd`.
- **Variant:** SOFTWARE.
- **Subject:** the working package in `projects/chirality-app-v4/execution/_Decomposition/` and its deliverable
  folders. This is the SCA-V4-001 accepted poststate: 22/22 checked files equal their accepted bytes.
- **Expected source:** `_ScopeChange/SCA-V4-001_2026-09-28_2155/`, the active accepted amendment named by
  `_ScopeChange/_LATEST.md`, applied over `_Decomposition/checkpoint_snapshots/GROUP3-20260928T001055Z`
  (Decision_Log D-2).
- **Scope:** PKG-01, 02, 03, 04, 05, 09 and 10, which hold 32 deliverables. It is derived from, and checked against,
  the SCA-V4-002 proposed register (Decision_Log D-3). The whole repository has 11 packages, 41 deliverables,
  10 objectives and 262 ledger rows.

**Overall status: WARNINGS. Closure readiness: WARN.** The run found 0 BLOCKER, 38 WARNING, 101 INFO and
0 EXPECTED_CONSEQUENCE. Every WARNING was already present in the POSTACCEPT audit of SCA-V4-001.

This report is derivative evidence for the scope-change pre-change comparison (method step 5), not decomposition
truth. The TASK moved no pointer.

## Summary of the 12 checks

| # | Check | Verdict | Key result |
|---|---|---|---|
| 1 | Forward coverage: Packages | PASS | 7/7 scoped packages have folders; all 11 exist repository-wide |
| 2 | Forward coverage: Deliverables | PASS | 32/32 scoped deliverables (41/41 repository-wide) have exactly one folder, in `1_Working` |
| 3 | Reverse coverage: Folders | PASS | No undeclared DEL or PKG folder; 100 % |
| 4 | ID consistency | PASS | All IDs and parents match. One INFO label difference (COV-001, DEL-01-05 `/` → `-`) |
| 5 | Context fidelity | PASS | 32/32 `_CONTEXT.md` MATCH on the 15 compared fields. SoW frontmatter identity and refs match the registers. The 32 INFO rows are the duplicated `PackageID` bullet (COV-002…033) |
| 6 | Artifact presence | WARN | All 32 units are SOW_V1 and valid. Heuristic presence is 11/102 (10.78 %). There are 37 WARNINGs (absences at IN_PROGRESS in 14 units) and 54 INFOs (absences at INITIALIZED) |
| 7 | Objective mapping | PASS | 10/10 objectives have active support. `Objectives.csv` and the ledger `ObjectiveIDs` agree, and the telemetry objective counts agree. Integrity: PASS |
| 8 | Ledger integrity | PASS | 262 rows (234 IN / 15 OUT / 13 TBD) with reciprocal mappings and 0 unmapped. Scoped: 193 IN / 14 OUT / 9 TBD |
| 9 | Derivative package parity | SKIPPED | Not variant-owned. There are 12 derivative-currency INFOs (below) |
| 9b | Package-shape conformance | WARN | The companion inventory is complete. COV-137: the Ledger, Objectives, Partitions and Production Units headings do not bind. The Change Register binds to `## Decision Log` (exact) |
| 10 | Active snapshot and handoff state | PASS | `_ScopeChange/_LATEST.md` names exactly one active snapshot (SCA-V4-001), which holds all 13 required artifacts. State fields are admissible and agree; the verdict is `OPEN_PENDING_DERIVATIVE_CLOSURE`. COV-139 INFO: the registered parser returns `None` |
| 11 | Lifecycle distribution | INFO | Scoped: INITIALIZED 18, IN_PROGRESS 14. Repository-wide: INITIALIZED 27, IN_PROGRESS 14. None is CHECKING, ISSUED or RETIRED |
| 12 | Comparison mode | not requested | This run is the "pre" side for the SCA-V4-002 post-change audit |

## Key figures (`coverage_summary.json`)

| Measure | Value |
|---|---|
| Packages declared / found | 7 / 7 (100 %) |
| Deliverables declared / found | 32 / 32 (100 %) |
| Reverse coverage | 100 % |
| Context fidelity | 100 % |
| Artifact presence (heuristic) | 10.78 % (11/102) |
| Objective coverage | 100 % |
| Deliverables / IN ledger rows without an objective | 0 / 0 |
| Package shape | WARN |
| Active snapshot / handoff state | PASS / PASS |
| Objective-evidence integrity | PASS |

## Findings that bear on SCA-V4-002

1. **The scope needs PKG-05.** IMPACT_ASSESSMENT §4 ("Pre-change baseline") names PKG-01, 02, 03, 04, 09 and 10.
   Register row 16 (B-06c, Q-12) edits the `_CONTEXT.md` files of DEL-05-01 and DEL-05-02, which are in PKG-05. This
   baseline therefore uses seven packages, and the post-change audit should use the same seven. The §4 sentence and
   any group-1 presentation that repeats it should add PKG-05.

2. **The facts behind the validation hold at `f05bd1bbd`:**
   - All 16 register rows' `AffectedFiles` exist (V-1).
   - Lifecycle states (V-2):
     - IN_PROGRESS: DEL-01-01, 02-01, 02-03, 03-03, 04-01, 04-02, 05-01 and 05-02;
     - INITIALIZED: DEL-01-04, 02-02, 09-07 and 10-03;
     - none CHECKING or ISSUED, so no reopening is needed.
   - OI-001, OI-002, OI-012 and OI-021 are all OPEN, consistent with Q-5 option A.
   - `Consolidated_Coverage.csv` has 31 HOST_INTEGRATION rows, the count that row 11 recomputes.
   - Topology is 11 / 41 / 10 / 262. The amendment should leave it unchanged.

3. **Check 5 is currently MATCH for DEL-04-01.** Register row 14 changes the `Deliverables.csv` Description.
   - The `_CONTEXT.md` `- **Description:**` bullet mirrors it exactly and must change byte-consistently, or the
     post-change audit will raise a Check 5 WARNING.
   - Row 16's reading-rule notes go beside the non-bullet `Accepted basis:` lines. If they stay out of
     `- **Field:**` bullet form, Check 5 is unaffected. A bullet that repeats a compared field would add findings.

4. **COV-139 (INFO, Check 10) confirms V13 F2 and item 5a.**
   - The registered `_latest_pointer_target` returns `None` for `_ScopeChange/_LATEST.md`, and `_pointer_matches` is
     False.
   - The audit-decomp Step 10 reading passes.
   - The post-change audit should still show COV-139, because C-01 lands at group 3. The post-acceptance audit should
     not.

5. **COV-127 (INFO) confirms ASC-ISS-006, which Q-12 addresses.**
   - `_Decomposition/_LATEST.md` reads `Latest: (none)`.
   - `_LATEST_ACCEPTED.md` names GROUP3 without saying that SCA-V4-001 amends it.
   - Row 15's pre-change hashes are `8eb05194…` for `_LATEST.md` and `d5d873b3…` for `_LATEST_ACCEPTED.md`.

6. **Carried items, not SCA-V4-002 effects.**
   - COV-125 and COV-126: `Coverage_Telemetry.json` is `STALE_REBUILD_REQUIRED` (ASC-ISS-004). It has 24 active
     issues against 23 OPEN, and a candidate-era standing.
   - COV-137: the four register headings do not bind.
   - COV-034…124: 37 absence WARNINGs at IN_PROGRESS.
   - COV-138: missing workspace tool roots.

   The post-change comparison should treat these as pre-existing.

7. **Minor.** Register row 10's EntityID `docs/HOST_INTEGRATION.md#status` names the `**Status:**` paragraph on
   line 3. That paragraph is not a heading, so `#status` does not resolve as a Markdown anchor. The A17b join is at
   line 11. This is a label question only.

## Pre-change hashes of the SCA-V4-002 targets

Paths are under `execution/`. The full list is in `INPUT_MANIFEST.sha256`.

| Register row | File | sha256 |
|---|---|---|
| 1 | DEL-10-03 `ScopeOfWork.md` | `4e16817e71f1df39afd3e3dd8175a04e9d4cc2384bf42065e91e16a5452b5f92` |
| 2 | DEL-02-01 `ScopeOfWork.md` | `6ccc860ba48aee9392fbf90fef323577c7599655164442e6f3fb0b78fe36f0dc` |
| 3 | DEL-02-03 `ScopeOfWork.md` | `a4ffcd8711ad0ee50d9ca6876d0b19972f9f3ba9a7a129578068c4a918c24c0e` |
| 4 | DEL-09-07 `ScopeOfWork.md` | `53b51d309d060089a6a88dae565867a92348789ee01430927e7464c7c2d3cba0` |
| 5 | DEL-01-04 `ScopeOfWork.md` | `7261a58f93d4531ca080c16d7fe088818871c3444085bade2eb2350ace94e60a` |
| 6 | DEL-02-02 `ScopeOfWork.md` | `b0a1a8a4aa6f53057c8db4bb33c65c5e697f45ae509088a570a70ff8cee295ec` |
| 7 | DEL-03-03 `ScopeOfWork.md` | `fdd22e25a0a43c55d31ca38f3fcb44931af8ebee6d34da62ff1f214013fb2881` |
| 8 | DEL-04-02 `ScopeOfWork.md` | `e077f20a95efc193e4de5489824e84278449b64dda615fb913c9dbd6070122f9` |
| 9 | DEL-01-01 `ScopeOfWork.md` | `f65dc666708dc06fbff046cf293ff529024ad9487829d2c105b3678c86a8acc9` |
| 10 | `docs/HOST_INTEGRATION.md` | `6c6854f941c714d8287bf799e1427bd4d99450847341bdf885ce4158d77eb122` |
| 11 | `_Decomposition/Consolidated_Coverage.csv` | `4eee4bcb1cb296a9e96f9c44f934f19913dd827b43666475505e684a646a8db1` |
| 12 | `_Decomposition/Open_Issues.csv` | `f6b92362c4f334ffe65522557acb515d247ba67133403cc6c805f1c5c4182bf7` |
| 13 | `_Decomposition/SOFTWARE_DECOMP.md` | `7434058164f9e53f146793b85c38845a562fbc9ffd46f2b97de18e8d597e5747` |
| 14 | `_Decomposition/Deliverables.csv`; DEL-04-01 `_CONTEXT.md` | `2480cbef8f597c76482dda22c652e182d3dcfa2a9a1eb07621ca6bda7fe06f44`; `3f981bd6036744b524cbc67e257cdbc3821d10d829492660e4640f76386e0abd` |
| 15 | `_Decomposition/checkpoint_snapshots/_LATEST_ACCEPTED.md`; `_Decomposition/_LATEST.md` | `d5d873b3b918fd508685871abf177e90104b98524c5cea52944dfa2f5a695ead`; `8eb0519416e80c1016cf464efb86624a42eaa94c867fe2b46ead7e5b80c9bb91` |
| 16 | `_CONTEXT.md` of DEL-02-03, 05-01, 05-02, 09-07 (and 04-01, above) | `d8cfefa0…b148`, `58f0bc84…89a1`, `e889d2b7…4f4c`, `8f7927ff…e78f` |

## Other derivative-currency observations (Check 9, all variants)

| Issue | Severity | Surface | Observation |
|---|---|---|---|
| COV-125 | INFO | `Coverage_Telemetry.json` | Open-issue counts are stale against `Open_Issues.csv` (ASC-ISS-004) |
| COV-126 | INFO | `Coverage_Telemetry.json` | Candidate-era standing and a "no folders or SoWs" check; 41 SoW folders exist |
| COV-127 | INFO | `_Decomposition/_LATEST.md` | The pointer reading gap (finding 5) |
| COV-128, 129, 131–135 | INFO | seven working files | Differ from GROUP3 canonical; each is named in SCA-V4-001 `AffectedFiles` |
| COV-130 | INFO | `External_Dependencies.csv` | Differs from GROUP3; not named by SCA-V4-001 (pre-amendment standing update, `ddd721a90`) |
| COV-136 | INFO | `Objectives.csv` | The Notes keep the frozen label "final Group3 acceptance remains pending" |

## What to fix for a cleaner rerun (not in this TASK's authority)

- Add PKG-05 to the stated baseline scope in IMPACT_ASSESSMENT §4 (finding 1).
- Apply row 14 to `Deliverables.csv` and the DEL-04-01 `_CONTEXT.md` together (finding 3).
- C-01 (the `Latest:` line in `_ScopeChange/_LATEST.md`) and B-06a/b/c close COV-139 and COV-127 after group 3.
- The telemetry rebuild (COV-125/126) and the heading bindings (COV-137) stay outside SCA-V4-002, as the impact
  assessment sequences them.
