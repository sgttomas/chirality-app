# Decomposition coverage report — pre-change baseline for SCA-V4-003 (proposed)

- **Run:** `APP_V4_SCA_V4_003_PRECHANGE`, 2026-10-03T02:46:41Z, basis commit `897a107cc`.
- **Variant:** SOFTWARE.
- **Subject:** the working package in `projects/chirality-app-v4/execution/_Decomposition/` and the 32 scoped
  deliverable folders. This is the SCA-V4-002 accepted poststate with its completed propagation: 148/148 checked
  files equal their accepted bytes (Decision_Log D-2).
- **Expected source:** `_ScopeChange/SCA-V4-002_2026-09-29_1901/`, the active accepted amendment named by
  `_ScopeChange/_LATEST.md` (predecessor SCA-V4-001), over `_Decomposition/checkpoint_snapshots/GROUP3-20260928T001055Z`.
- **Scope:** PKG-01, 02, 03, 04, 05, 09 and 10 (32 deliverables), the SCA-V4-002 audits' scope. It covers the six
  packages the SCA-V4-003 proposal records target (Decision_Log D-3). Repository: 11 packages, 41 deliverables,
  10 objectives, 262 ledger rows.

**Overall status: WARNINGS. Closure readiness: WARN.** 0 BLOCKER, 35 WARNING, 93 INFO, 0 EXPECTED_CONSEQUENCE.
Every WARNING was already present in the SCA-V4-002 post-acceptance audit (0 / 38 / 100); `COMPARISON.md`
attributes each difference.

This report is derivative evidence for the scope-change pre-change comparison (method step 5), not decomposition
truth. The TASK moved no pointer and applied nothing.

## Summary of the 12 checks

| # | Check | Verdict | Key result |
|---|---|---|---|
| 1 | Forward coverage: Packages | PASS | 7/7 scoped packages have folders; all 11 exist repository-wide |
| 2 | Forward coverage: Deliverables | PASS | 32/32 scoped (41/41 repository-wide) have exactly one folder, in `1_Working` |
| 3 | Reverse coverage: Folders | PASS | No undeclared DEL or PKG folder; 100 % |
| 4 | ID consistency | PASS | All IDs and parents match. One INFO label difference (COV-001, DEL-01-05 `/` → `-`) |
| 5 | Context fidelity | PASS | 32/32 `_CONTEXT.md` MATCH on the 15 compared fields; SoW frontmatter identity and refs match the registers. The 32 INFO rows are the duplicated `PackageID` bullet (COV-002…033) |
| 6 | Artifact presence | WARN | All 32 units SOW_V1 and valid. Heuristic presence 20/102 (19.61 %). 34 WARNINGs (absences at IN_PROGRESS in 14 units) and 48 INFOs (absences at INITIALIZED), COV-034…115. The 9 newly matched artifacts are Design documents and prototypes (D-6) |
| 7 | Objective mapping | PASS | 10/10 objectives have active support; `Objectives.csv`, the ledger and the telemetry objective counts agree. Integrity PASS |
| 8 | Ledger integrity | PASS | 262 rows (234 IN / 15 OUT / 13 TBD), reciprocal mappings, 0 unmapped. Scoped: 193 IN / 14 OUT / 9 TBD |
| 9 | Derivative package parity | SKIPPED | Not variant-owned. 11 derivative-currency INFOs (below) |
| 9b | Package-shape conformance | WARN | Companion inventory complete. COV-127: Ledger, Objectives, Partitions and Production Units headings do not bind; the Change Register binds to `## Decision Log` (exact) |
| 10 | Active snapshot and handoff state | PASS | `_ScopeChange/_LATEST.md` names exactly one active snapshot (SCA-V4-002) holding all 13 required artifacts; state fields admissible and agreeing; verdict `OPEN_PENDING_DERIVATIVE_CLOSURE`; SCA-V4-001's folder complete (no residue). The registered parser resolves the pointer (`pointer_matches_active` True) |
| 11 | Lifecycle distribution | INFO | Scoped: INITIALIZED 18, IN_PROGRESS 14. Repository: INITIALIZED 27, IN_PROGRESS 14. None CHECKING, ISSUED or RETIRED. COV-128: missing workspace tool roots |
| 12 | Comparison mode | not requested | This run is the "pre" side for the SCA-V4-003 post-change audit; `COMPARISON.md` sets it against POSTACCEPT |

## Key figures (`coverage_summary.json`)

| Measure | Value |
|---|---|
| Packages declared / found | 7 / 7 (100 %) |
| Deliverables declared / found | 32 / 32 (100 %) |
| Reverse coverage | 100 % |
| Context fidelity | 100 % |
| Artifact presence (heuristic) | 19.61 % (20/102) |
| Objective coverage | 100 % |
| Deliverables / IN ledger rows without an objective | 0 / 0 |
| Package shape | WARN |
| Active snapshot / handoff state | PASS / PASS |
| Objective-evidence integrity | PASS |

## Findings that bear on SCA-V4-003

1. **The proposal records were written against the current bytes.** For all 20 target deliverables, the
   `ScopeOfWork.md` and `Dependencies.csv` hashes the records cite (pass-2 C1-A/B/C, pass-3 C1-A/B input tables)
   equal the pre-change bytes below (20/20 and 20/20), so no old → new block rests on superseded text. One
   transcription slip: pass-3 C1-A records DEL-01-04 `_STATUS.md` as `12de2a18b4016880`; the file, unchanged since
   `ddd721a90` (2026-09-27), is `12de2a18b401688c…`. Any R22-5 status edit should bind the actual hash.

2. **R22-5 (the six deliverables' lifecycle) moves Check 6 severities.** DEL-01-02, 01-03, 01-04, 01-05, 02-02 and
   02-04 are INITIALIZED, so their 16 missing-artifact rows are INFO here (DEL-01-02 4, 01-04 4, 02-02 3, 01-03 2,
   01-05 2, 02-04 1). If the owner moves them to IN_PROGRESS, the post-change audit will show those 16 as WARNINGs
   (35 → 51, INFO 93 → 77) with no other change. The comparison should attribute them to R22-5, not count them as
   regressions. The SCA-V4-002 propagation used `scope-of-work` REVISE with `NO_STATUS_TOUCH`; a status change needs
   its own authorized step.

3. **DAG-003 binds every target file.** At the subject `_DAG/DAG-003/SOURCE_MANIFEST.sha256` passes 130/130 and
   `MANIFEST.sha256` 37/37. Every `ScopeOfWork.md` or `Dependencies.csv` edit will make the source manifest fail on
   that file, as SCA-V4-002's did to DAG-002. Pass-3 F0 §3 records NR-01…NR-07 as new admitted arcs (each a DAG
   departure) and NR-08…NR-10 as held inside SCC-002. A `project-dag` currency check and DAG-004 should be expected.

4. **Check 5 is MATCH for all 32.** No record proposes a `Deliverables.csv`, `Packages.csv` or `_CONTEXT.md` edit
   (pass-2 C1-A and pass-3 C1-A note the missing "as amended" sentence in three `_CONTEXT.md` files and propose no
   change). If P1's BASIS_AMENDMENT adds one, the `_CONTEXT.md` mirror must change byte-consistently, as SCA-V4-002
   row 14 did.

5. **Open_Issues edits change Check 9 wording only.** OI-009, OI-010 and OI-018 are OPEN; 23 issues are OPEN. An
   OI-009 text amendment changes `Open_Issues.csv` (COV-121's hash and attribution). A status change would also move
   COV-116's counts, because `Coverage_Telemetry.json` stays `STALE_REBUILD_REQUIRED` (owner-deferred; SCA-V4-002
   EFFECTIVE_STATE).

6. **Closed since POSTACCEPT.** POSTACCEPT COV-127 (ASC-ISS-006) is gone: `_LATEST_ACCEPTED.md` carries the B-06a
   reading rule. Its base script still emits the old, now false description; this run's change (h) handles it. The
   inherited (f)/(g) pointer limits also remain. Both are tooling work outside this amendment.

7. **Carried, not SCA-V4-003 effects.** COV-116 and COV-117 (stale telemetry), COV-127 (heading bindings), the 34
   absence WARNINGs at IN_PROGRESS, COV-126 (frozen Objectives label) and COV-128 (tool roots). The post-change
   comparison should treat them as pre-existing.

## Pre-change hashes of the SCA-V4-003 target files

Paths under `execution/`; the full list is in `INPUT_MANIFEST.sha256`. "R22-5" marks the six deliverables whose
lifecycle goes to the owner. `_Decomposition/Open_Issues.csv` is
`a11782181531ce77e564b774787537d3e11cc1d4304123cba0d83f539bb280f0`.

| DEL | `ScopeOfWork.md` | `Dependencies.csv` | `_STATUS.md` (state) |
|---|---|---|---|
| DEL-01-01 | `9945e72b04b4f45c4c641a5248cca8bc2ac40bf4897d1018c5ab59eba307cc75` | `9fdb3ce3d8c180f58bf64d9fcf3476e3835dd6c8641bf4f4f203bc10f1f13d08` | `477c9a576400caf4…` (IN_PROGRESS) |
| DEL-01-02 | `057ae2fdf4c3e98c961214739d2170a7c8ab29a530208f0c476af15125d6c6b4` | `84451e124cf2718581a4e86c97e62d4598838ac202ec371ddc12f2e4ebc55948` | `76353a510b0de5d5…` (INITIALIZED) R22-5 |
| DEL-01-03 | `b5d533cb3dbea97b37950792ad2c68f42bf6023effa4ac894209a1ef3fc605f2` | `9ac820166dd07dde8bbad59ba1c2b0818ab7f4ff4b435c6991cc2d887ddeedf4` | `52ea2e2fa6506ad3…` (INITIALIZED) R22-5 |
| DEL-01-04 | `0cdb44e297010b70deb479ab647a165023846aa0943c3f9fc200407c708469cd` | `20ce3808597bf2833bba6c488ae3770c3b93260d4be229b6f89cedecdb0d5eaa` | `12de2a18b401688c…` (INITIALIZED) R22-5 |
| DEL-01-05 | `baf68c79b5b8fdf01300fc255d7cf8e433975e6275daadf67b914b4e51eca4a6` | `3b038c98f97cd6855b42b10e1602a24c34152f3defa582c037d6ee642f4796a6` | `fdd04e5ef2ed0353…` (INITIALIZED) R22-5 |
| DEL-02-01 | `ef360edf28f5f463ae961495e04e566ab9ec9d56c0a4fd4f35e67b87adb82f17` | `d3946a9e0c2bd7b37cb18355abc3b2a2f563ef0b886b500162b550d6ac1db10a` | `9e05735edd3c742d…` (IN_PROGRESS) |
| DEL-02-02 | `5814116909db8120c1fe888ba021ca60ad139ea0b36cc89fe7e93ed00235924a` | `be14a079c872695ee6720c75bfe96b91dbac6ad4c228fb577ee044f1e32f7e0a` | `a4efafd9d06802f6…` (INITIALIZED) R22-5 |
| DEL-02-03 | `0006521b9bd96ea7ec98ecc5d9e6db794ecb331440c276006b444e7ee319726d` | `f1a81f854d5923dd450a6eb709bfc623b3f778651787e6f4a09d0d48d5110f7e` | `237e0982346f75a9…` (IN_PROGRESS) |
| DEL-02-04 | `3acfaa62a3bbf0038d4f3c94416925bf5ff940bb8771b5454ff1ea80e6e16601` | `0cb255b3270dfe616f434e8974795eb6b9a9e37aceb5da9972823d5a3cf0a267` | `c38a7fdb81047d9c…` (INITIALIZED) R22-5 |
| DEL-03-01 | `9ada531b59a6efc007c273f131a8d51df390994ef5f379b1d523d635d3849449` | `930796b5f1b82537ca24fc061b71b0947e5f7db3ab6e3f8552f5d4f05491407e` | `8f5e07e85e379cb2…` (IN_PROGRESS) |
| DEL-03-02 | `3560915142ebfbf3fa7197008ea3b0660584665c9d86260b22b550c5c2354d0f` | `226380332f36b03d4140d59927d1e68b157b02155313bbed2fc8f06e92e53a87` | `9d86523da17f33b3…` (IN_PROGRESS) |
| DEL-03-03 | `93faf918ce5d2d4eb14f0ecd1b20831a164a8c55a8b47cad26880818251b1a93` | `be53fc728070902e916a7e5321a1054746b25f721aa5a9c50daec3faf7ec2620` | `94239785ea511273…` (IN_PROGRESS) |
| DEL-03-04 | `895f004e4d0f133798f461d8157ac63fff880da09f471be9bae885fe0cfb7c28` | `977d8712e02b4e22eb1191da82013fc974aedf76fc482e63302c5f6512bee32b` | `5c304d62f1619fce…` (IN_PROGRESS) |
| DEL-04-01 | `ac043e54e396f9155e3d1b02d61ca7333350a812c7db3d5bb26c80d6fc3bb875` | `d3892649dbc008d81b9a183d34c44cf68e0765d886a04dce924e69f456c5c9c1` | `4cd05ed56d087a33…` (IN_PROGRESS) |
| DEL-04-02 | `f16ffa8a33cbfb2e78a8e916e90aff9fb44ad20adf94fe61a559a213f5564460` | `05ffc9c7b274b464ed26709e1c54f536c65704ce7c0b9f6febe2c399a47bcb44` | `b429eebf9e8962c6…` (IN_PROGRESS) |
| DEL-04-03 | `ceecddbb67a86f744b413bb08b08c27017a82ebee8500f7600faf8d880fbaa47` | `f40bc8889830c6f67b048851ecf4b6e0425f9db154b8756d48a85c9130ce70cf` | `5bb717f95917a574…` (IN_PROGRESS) |
| DEL-05-01 | `9b2379a14e2c9da4310f62e72d83a6e7506ef37f70c4a38b41d76908bca985ed` | `6c86f2263ea36a87f58024a85ecdeebcf5c13088503a2478aa92dcb6de5f03e6` | `d54d031271457d4e…` (IN_PROGRESS) |
| DEL-05-02 | `beb9c66c38161cbb00d1040e294aa9dfd04af953f9bf539121fcda44356dc82c` | `2889aa5f910b1123347d821f27a7e609d5a9a8f8dc7fe6c6825813bef1900568` | `ddaaff1f2c68fe51…` (IN_PROGRESS) |
| DEL-09-06 | `287d47a1260e7433c3f16578c67345d067472165421c65848bd15e44d92a7923` | `0f8ecad83cca72f7c65786ff0cd0252a2b7664c145a6e39193cff332a639f2f6` | `c2eb59adeab32c7a…` (IN_PROGRESS) |
| DEL-09-09 | `e887a579f75335aa91b59ae195053eabae81ce031fe91136df5c81df2297e53a` | `e0e3297adb7350c58694aae88062d1bb35778c4440a5e91374f3d8c7c9663bb8` | `82eba88d08f10cc7…` (IN_PROGRESS) |

## Other derivative-currency observations (Check 9, all variants)

| Issue | Severity | Surface | Observation |
|---|---|---|---|
| COV-116 | INFO | `Coverage_Telemetry.json` | Open-issue counts stale against `Open_Issues.csv` (ASC-ISS-004; rebuild owner-deferred) |
| COV-117 | INFO | `Coverage_Telemetry.json` | Candidate-era standing and a "no folders or SoWs" check; 41 SoW folders exist |
| COV-118, 119, 121, 123 | INFO | four working files | Differ from GROUP3 canonical; named by SCA-V4-001 and SCA-V4-002 `AffectedFiles` |
| COV-122, 124, 125 | INFO | three working files | Differ from GROUP3 canonical; named by SCA-V4-001 `AffectedFiles` |
| COV-120 | INFO | `External_Dependencies.csv` | Differs from GROUP3; named by neither amendment (pre-amendment standing update, `ddd721a90`) |
| COV-126 | INFO | `Objectives.csv` | Notes keep the frozen label "final Group3 acceptance remains pending" |

## What to fix for a cleaner rerun (not in this TASK's authority)

- Correct the DEL-01-04 `_STATUS.md` prefix where the packet cites it (finding 1).
- Decide R22-5 before the post-change audit, so its severity shift is classified (finding 2).
- The telemetry rebuild (COV-116/117), the heading bindings (COV-127) and a repaired base audit script stay outside
  SCA-V4-003 unless the owner adds them.
