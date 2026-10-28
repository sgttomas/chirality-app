# Review packet — DAG-004 candidate

Written before the owner's checkpoint, as project-dag method Stage 4 step 4 requires. It lists the SHA-256 of every file in the candidate as presented. At publication, `_DAG/DAG-004/` must contain these files byte for byte (method Stage 5 step 1), verified against this list.

- **Candidate:** staged at `_Coordination/AgentRuns/APP-V4-SCA003-20261002/DAG_PREP/DAG-004/` (execution-root relative), because the D1 brief fences writes out of `_DAG/`. Its method home before acceptance is `_DAG/_Candidates/DAG-004/`. Assembled on the frozen basis `75764184b99ab006cd46c1d1c328cf7d5c4d0c8d` (clean tree); 33 files, the same file set as the DAG-003 candidate.
- **Independent review:** not yet performed at the time of writing. A separate TASK instance that did not assemble the candidate must review it (method Stage 4 step 3) before the package is presented. Its `INDEPENDENT_REVIEW.md` is added to the candidate when returned. If any file listed below changes as a result, this packet is re-issued with the new hashes and the changed parts are re-presented.
- **Strict audit:** `python3 tools/coordination/audit_dag.py --dag-dir <candidate> --canonical --strict --json-out <candidate>/Evidence/dag_audit.json`, from the repository root: **exit 0** (`Evidence/Tool_Run.json`). 129 admitted edges, 41 nodes, 0 canonical findings, 0 SCCs, 0 duplicates, 0 bidirectional pairs.
- **Counts:** 41 nodes; 129 admitted, 83 held (all `SCC_UNRESOLVED`, six SCCs, membership unchanged), 355 excluded (208 NOT_TOPOLOGICAL, 145 MIRROR, 2 SAME_ARC) = 567 ACTIVE EXECUTION rows, none missing, none twice.
- **Scope of the acceptance:** checkpoints 1 and 2 may be decided in one sitting (no SCC needs a ruling; only the 10 added arcs and their consequences are reopened; everything else carries forward from DAG-003). If the owner decides them together, **the acceptance record must state that the decision covers both checkpoints.**
- **What acceptance decides:** the departure found by `CURRENCY_APP_V4_SCA003_2026-10-03_1937`: 10 arcs added (5 admitted: NR-05, NR-07, NR-01, NR-02, NR-04; 5 held: NR-08, NR-09, NR-4, R2-04-03-e, R20-10), none removed. It releases DEL-01-02, 01-03, 01-04, 01-05, 02-01, 02-02, 02-03, 02-04, 03-03, 04-02 and 04-03 from `DAG pending`.
- **Not in this candidate yet:** `INDEPENDENT_REVIEW.md` (from the reviewer), and the publication-time files `ACCEPTANCE_RECORD.md`, `HANDOFF_STATE.md`, `REVIEW_PACKET.md` (a copy of this file) and `MANIFEST.sha256`.
- **Reproduction:** rerunning `Evidence/assemble_graph.py` rewrites only the graph files and the Evidence files it generates; those reproduce byte for byte except `Evidence/Tool_Run.json` (`finished_at`) and possibly `Evidence/AssemblyChecks.json` (`protected_input_count`, which counts files in the protected folders). Publish the bytes listed here, not a rerun.

## Candidate files

| File | SHA-256 |
|---|---|
| `ASSEMBLY_RUN.md` | `566e31435761bb100864cb30b28ab2556efcacb734cc713d4838053b952e9d17` |
| `CandidateEdges.csv` | `2bfff10e3094d7fd86da563006c965694563ec10d0fc78e9b1d9958fefa42025` |
| `DeliverableNodes.csv` | `102eee1a6a409ae4babefa674546c5111848e90ba5fb7447dc5cc240a31b93e8` |
| `DependencyEdges.csv` | `c43033742df768a6fb493701d25b1d73240366172c05b1d0caa143650690966e` |
| `Evidence/Accounting.md` | `ab0eb7362347d07e22d32fb339c1a7898c79f7030767c7f3990afe04fa1760c5` |
| `Evidence/AssemblyChecks.json` | `008664463af6b971319891fb16f0fc7ec9293abb4a578a9d4bb4251b2fb7283d` |
| `Evidence/DepartureAccount.csv` | `9d2f7655d097bc5da2dbb6c6a1215db88676d51f24d90cd0998d5bb718ed6d86` |
| `Evidence/DepartureAccount.json` | `1c5357ab279b4a545b77ea1e2150cd4c9aabb3e49fd764aad3355b80285ea50f` |
| `Evidence/MirrorAssessment.csv` | `eb0df00a83d52fc94eb0670d7dfe82fed3735382c6bd93b1d0bad5606036cf84` |
| `Evidence/MirrorAssessment.md` | `23f586a9a4993ba8cd94f4181241def452b2ee9ef24e4e8f4451f1ee443180d1` |
| `Evidence/MirrorComparisons.csv` | `c19444eb4ed9e1a6a9a1e90ad563bf6ca7627bdaacbbb99a18f90cc602bf1266` |
| `Evidence/NonTopologicalInputs.csv` | `64dfaef3933ec769c922186212410959ec4c37dd2e1e63abb28e08a82cf46319` |
| `Evidence/RegisterAccounting.csv` | `2ed5a1e0e24eba2d105b6b84b2fa9456740799393a1006a78a3921f93386037b` |
| `Evidence/SCC_Accounting.json` | `7366f4b8118962e170a25bb96040eb5e2f4837c592df5a3824891ed281ce903a` |
| `Evidence/Tool_Run.json` | `6e50d38557a7ee8c326a0d28b113d1be7c772181f5a0c33ecf82024c3f2a3994` |
| `Evidence/admissible_audit.json` | `790d8f4defc749938b7c9dc116daa324c0edbf6fdfdf640e6a82eabf215091af` |
| `Evidence/admissible_audit.stderr.txt` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `Evidence/admissible_audit.stdout.txt` | `29dfe29aeb0af0a2ef51864e0d93137ffefb1dcfef4d71b67c200f0c87f86429` |
| `Evidence/admissible_edges.csv` | `22e5a26415d5b7932ceb9bce177959988816a42deab769a190c287bd6c1341fc` |
| `Evidence/all_execution_rows.csv` | `3c176baf9db2f717d357265e62230993b4839e131e8a774e9e37daa3c7e63704` |
| `Evidence/assemble_graph.py` | `008e9ed1c4b503faa1c474b21988add53e9d23851cb4c5a132a6ca3955af2d58` |
| `Evidence/candidate_audit.json` | `92d04dcb0ec74af2061b4493b3afa05098b1fe5361ac9adb17ee2d5c24123aef` |
| `Evidence/candidate_audit.stderr.txt` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `Evidence/candidate_audit.stdout.txt` | `7b81c829036db073a33cab123d9db152a9b3d6016911240c8612388307655f1a` |
| `Evidence/dag_audit.json` | `0f4fca923d18beb7a5889facd7108f587949b59a7e6c83c1821ce9d4d6d9ba22` |
| `Evidence/dag_audit.stderr.txt` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `Evidence/dag_audit.stdout.txt` | `1076b63bb6ef1dd86d093a7f32d509eafba1431dbd6aeb49a6db68235bdc8c3e` |
| `Evidence/successor_currency_precheck.json` | `0b515028383276c25dc2f7c08f4dde3d92d2636cc654e7f36aa8ca23cf9663f2` |
| `ExcludedRows.csv` | `45f55e76ecf7c9aac3bd923838eee8c302d6b2776e4fa3c221e51f9cf465664e` |
| `GRAPH_BASIS.md` | `21835c7be4b2d1c65f38dc492aee28f936a31bd5f58d7df9e3ba7cc48c1aad79` |
| `PROPOSED_LATEST.md` | `3634d4903d7eb32ba44fb9c22e9091f486b25bb605a81e4b829603f93bad4846` |
| `SOURCE_BASIS.json` | `2e8c8643b2514d5cdce8dad5702268cee43edf92b34ca64ad4d9a913454ef37c` |
| `SOURCE_MANIFEST.sha256` | `03aa668b88cb1cb32e1d26a15fb64afdf85e0af6fbb61ec89f833eaf5893a8ef` |

## Supporting records (not part of the graph version)

The closure and currency snapshots are staged beside the candidate for the same reason. At publication they are copied to `_Evaluation/DepClosure/` and `_Evaluation/DAGCurrency/` (and those pointers moved), verified against these hashes. `PROPOSED_LATEST.md` cites the currency snapshot by its `_Evaluation/DAGCurrency/` name; `GRAPH_BASIS.md`, `SOURCE_BASIS.json` and `ASSEMBLY_RUN.md` cite the staged `DAG_PREP/` paths and say where each goes. The CASE-002 draft is applied separately through `scc-resolution-case`; the candidate does not depend on it.

| File (under `DAG_PREP/`) | SHA-256 |
|---|---|
| `CLOSURE_APP_V4_SCA003_2026-10-03_1936/Dependency_Closure_Report.md` | `d2c9e44ca37f90e3c8ea0940544ad300f4058e44327af27ff363b1b607625742` |
| `CLOSURE_APP_V4_SCA003_2026-10-03_1936/Evidence/bidirectional_pairs.csv` | `0aed40f638a778fe3164ce3d91baca1c3a69ecb71e6d1f59950c00989c87b5f5` |
| `CLOSURE_APP_V4_SCA003_2026-10-03_1936/Evidence/closure_summary.json` | `406702089641db375ec72437c549df324ffc20db6c509f291f613771017ee8ca` |
| `CLOSURE_APP_V4_SCA003_2026-10-03_1936/Evidence/coverage.csv` | `d92adad795a2fcbf2c33e59da89caf2af825ee96a7fcaa26d31edfdb9c6dde9f` |
| `CLOSURE_APP_V4_SCA003_2026-10-03_1936/Evidence/cycles_sample.csv` | `baaf2e767196aa1fe71682967c9f517fd1a939e58c5cc74de9c509d805245f0b` |
| `CLOSURE_APP_V4_SCA003_2026-10-03_1936/Evidence/dag_pending.csv` | `976b5ee1b3b2d9d45ce403056e77d6ae57575ba295ea8387197e1b8f8bf3bd55` |
| `CLOSURE_APP_V4_SCA003_2026-10-03_1936/Evidence/declared_disagreements.csv` | `25f24f398fafb2796522f1c2e57ab4967d6bd0d2a74c7db097033a99a154db1e` |
| `CLOSURE_APP_V4_SCA003_2026-10-03_1936/Evidence/declared_only.csv` | `eda0dfdb6c8d836b12a62d0970fa69e5c55b4651f39f07ab849f707d2d1478d8` |
| `CLOSURE_APP_V4_SCA003_2026-10-03_1936/Evidence/declared_unread.csv` | `5a27b1a738093a62a08a6bd46feafba2cb88607673725e1dcb0d8fde47ddefb1` |
| `CLOSURE_APP_V4_SCA003_2026-10-03_1936/Evidence/hubs.csv` | `b5279432c61d478055b8482f6e9180c52d7a5eaac4efdb9bac857a367d15c4df` |
| `CLOSURE_APP_V4_SCA003_2026-10-03_1936/Evidence/id_normalization.csv` | `adfc7cb090f6d0e18c2474fe703c9081d5176ce88a5ac2ea7933c0439300841c` |
| `CLOSURE_APP_V4_SCA003_2026-10-03_1936/Evidence/isolated.csv` | `2f5dc27ce8e121fe54a0fbab33c2de421476e1adc67f8da7a11104e82b3410fa` |
| `CLOSURE_APP_V4_SCA003_2026-10-03_1936/Evidence/orphans.csv` | `c7249203528bf437056a6a103839fd2987671722a46f017f227ca1c12970b360` |
| `CLOSURE_APP_V4_SCA003_2026-10-03_1936/Evidence/outside_scope.csv` | `c7249203528bf437056a6a103839fd2987671722a46f017f227ca1c12970b360` |
| `CLOSURE_APP_V4_SCA003_2026-10-03_1936/Evidence/scc_summary.csv` | `d97c6415c304c7555806e2f3f5f8465bfecbcabdfbb539f74768a8999c36258d` |
| `CLOSURE_APP_V4_SCA003_2026-10-03_1936/Tool_Run.json` | `3b66740cc2a9545ffbc813977579a86aef7e99246cc1122e0b93cee2e4e70274` |
| `CURRENCY_APP_V4_SCA003_2026-10-03_1937/CURRENCY_REPORT.md` | `01aa86d761199588da568342d121bf993762d3dfb18d49ca6b3e196bad298a72` |
| `CURRENCY_APP_V4_SCA003_2026-10-03_1937/Evidence/added_arcs.csv` | `22f05000335086643e52bd3a1b53a17488425f2054c3815c565648963f48d1aa` |
| `CURRENCY_APP_V4_SCA003_2026-10-03_1937/Evidence/analyzer.exit` | `9a271f2a916b0b6ee6cecb2426f0b3206ef074578be55d9bc94f6f3fe3ab86aa` |
| `CURRENCY_APP_V4_SCA003_2026-10-03_1937/Evidence/analyzer.stderr.txt` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `CURRENCY_APP_V4_SCA003_2026-10-03_1937/Evidence/analyzer.stdout.json` | `5c741a0438d74d899e9b1a94e644215aead747fe5b2fd6fc2a210e5be55d9f08` |
| `CURRENCY_APP_V4_SCA003_2026-10-03_1937/Evidence/dag001_manifest.exit` | `9a271f2a916b0b6ee6cecb2426f0b3206ef074578be55d9bc94f6f3fe3ab86aa` |
| `CURRENCY_APP_V4_SCA003_2026-10-03_1937/Evidence/dag001_manifest.stderr.txt` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `CURRENCY_APP_V4_SCA003_2026-10-03_1937/Evidence/dag001_manifest.stdout.txt` | `1423d7f10876fd9306747b724bcb9e58dd025c7ca2b3d4d167e65f9b1933d08f` |
| `CURRENCY_APP_V4_SCA003_2026-10-03_1937/Evidence/dag002_manifest.exit` | `9a271f2a916b0b6ee6cecb2426f0b3206ef074578be55d9bc94f6f3fe3ab86aa` |
| `CURRENCY_APP_V4_SCA003_2026-10-03_1937/Evidence/dag002_manifest.stderr.txt` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `CURRENCY_APP_V4_SCA003_2026-10-03_1937/Evidence/dag002_manifest.stdout.txt` | `eb9f0f07e6721a79355d08d06d2b17a41f2f5292a52f93febb9632266936c615` |
| `CURRENCY_APP_V4_SCA003_2026-10-03_1937/Evidence/reapplication_result.json` | `f4a220cf6f0c5da6506769d8de4965ac4a525de450322a2df82af389f24d2db4` |
| `CURRENCY_APP_V4_SCA003_2026-10-03_1937/Evidence/reapply_selection.py` | `afb2d6de9f29385f33ad0eb3b0806c95bffa20acdc5fcaf8c72bd18db880184d` |
| `CURRENCY_APP_V4_SCA003_2026-10-03_1937/Evidence/scratch_admissible_audit.json` | `649fb0a4dd1662c23db3fd82deaabbacfb4e748dfd72d326d8aef4bf7012db4a` |
| `CURRENCY_APP_V4_SCA003_2026-10-03_1937/Evidence/scratch_admissible_audit.stderr.txt` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `CURRENCY_APP_V4_SCA003_2026-10-03_1937/Evidence/scratch_admissible_audit.stdout.txt` | `29dfe29aeb0af0a2ef51864e0d93137ffefb1dcfef4d71b67c200f0c87f86429` |
| `CURRENCY_APP_V4_SCA003_2026-10-03_1937/Evidence/scratch_admissible_edges.csv` | `089cda8d1aa693d8ba00858152e003284b502234a2f48c171c079babf63d7271` |
| `CURRENCY_APP_V4_SCA003_2026-10-03_1937/Evidence/snapshot_manifest.exit` | `9a271f2a916b0b6ee6cecb2426f0b3206ef074578be55d9bc94f6f3fe3ab86aa` |
| `CURRENCY_APP_V4_SCA003_2026-10-03_1937/Evidence/snapshot_manifest.stderr.txt` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `CURRENCY_APP_V4_SCA003_2026-10-03_1937/Evidence/snapshot_manifest.stdout.txt` | `b899657a6580956d9b56ce50f75493979cd1c5485fac61b0d37fdeb392c7d2aa` |
| `CURRENCY_APP_V4_SCA003_2026-10-03_1937/Evidence/source_manifest.exit` | `4355a46b19d348dc2f57c046f8ef63d4538ebb936000f3c9ee954a27460dd865` |
| `CURRENCY_APP_V4_SCA003_2026-10-03_1937/Evidence/source_manifest.stderr.txt` | `3ca31b15b6a0d6f2362130eceea693d867164ec22ae444e2ea01c1d4b1646483` |
| `CURRENCY_APP_V4_SCA003_2026-10-03_1937/Evidence/source_manifest.stdout.txt` | `25d00a90e23c92b13f46369cfa4c27e7232da65a506de0e3786cb4c103c6f95a` |
| `CURRENCY_APP_V4_SCA003_2026-10-03_1937/Tool_Run.json` | `f0dbd989802ef914b1dcdd30a000b835c5db5664e53999de069669ffa7620165` |
| `CASE-002_EVIDENCE_UPDATE.proposed.md` | `5cdf942f49b129f84579f276444781c9a235af99c1bb7728e31b9329fc973ce2` |
