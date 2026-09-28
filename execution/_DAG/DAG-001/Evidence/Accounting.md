# Execution-row accounting

All 403 ACTIVE EXECUTION rows occur exactly once: **109 admitted + 52 candidate + 242 excluded = 403**. Exclusions are 202 NOT_TOPOLOGICAL, 38 MIRROR and 2 SAME_ARC. The 355 active ANCHOR rows and one RETIRED execution row remain in their local registers, outside this denominator. No row is missing or counted twice.

The 161 admitted/candidate representatives preserve all 29 core field values, including exact UTF-8 field bytes, from their source logical records; serialization/CSV quoting is not claimed identical. `all_execution_rows.csv` independently retains all 403 full core records, including every excluded obligation. Source file hashes and one-based logical record ordinals disambiguate locators. There are no duplicate source DependencyIDs.

The 130-entry source manifest matches working bytes and source commit 85dcc17c3fda4bce82332a40f27aa9b4e849653e. The original 79 presentation members match their own preserved commit 2a461a47adee03bb868e433a73048265cc0be808, not later decision-applied case bytes. All 268 protected source/CP1/case/status/closure inputs remain unchanged. The node file retains its original bytes and all 41 accepted identities/paths.

SCCs computed by the registered auditor on the 161 representative arcs match all six refreshed closure member sets exactly. The 52 held arcs represent 66 source rows, with 14 further intra-SCC mirrors/same-arc rows retained in exclusions. No type filter, SR-5 hold, cut, merge group or endpoint normalization is applied. Raw closure cyclicity remains expected.

| Register owner | Total source | Anchors | Retired | Active execution | Admitted | Candidate | Excluded |
|---|---:|---:|---:|---:|---:|---:|---:|
| DEL-01-01 | 24 | 15 | 0 | 9 | 0 | 1 | 8 |
| DEL-01-02 | 21 | 17 | 0 | 4 | 3 | 0 | 1 |
| DEL-01-03 | 18 | 10 | 0 | 8 | 2 | 0 | 6 |
| DEL-01-04 | 19 | 6 | 0 | 13 | 3 | 2 | 8 |
| DEL-01-05 | 16 | 11 | 0 | 5 | 1 | 1 | 3 |
| DEL-01-06 | 12 | 5 | 0 | 7 | 1 | 0 | 6 |
| DEL-02-01 | 24 | 16 | 0 | 8 | 1 | 4 | 3 |
| DEL-02-02 | 19 | 11 | 1 | 7 | 2 | 4 | 1 |
| DEL-02-03 | 21 | 8 | 0 | 13 | 1 | 4 | 8 |
| DEL-02-04 | 16 | 9 | 0 | 7 | 2 | 2 | 3 |
| DEL-03-01 | 30 | 21 | 0 | 9 | 1 | 2 | 6 |
| DEL-03-02 | 26 | 15 | 0 | 11 | 1 | 3 | 7 |
| DEL-03-03 | 12 | 5 | 0 | 7 | 1 | 2 | 4 |
| DEL-03-04 | 20 | 4 | 0 | 16 | 15 | 0 | 1 |
| DEL-04-01 | 21 | 11 | 0 | 10 | 1 | 0 | 9 |
| DEL-04-02 | 14 | 6 | 0 | 8 | 1 | 2 | 5 |
| DEL-04-03 | 20 | 10 | 0 | 10 | 0 | 0 | 10 |
| DEL-05-01 | 24 | 13 | 0 | 11 | 1 | 6 | 4 |
| DEL-05-02 | 18 | 4 | 0 | 14 | 1 | 5 | 8 |
| DEL-06-01 | 13 | 6 | 0 | 7 | 4 | 0 | 3 |
| DEL-06-02 | 16 | 7 | 0 | 9 | 3 | 0 | 6 |
| DEL-07-01 | 15 | 8 | 0 | 7 | 0 | 1 | 6 |
| DEL-07-02 | 15 | 9 | 0 | 6 | 1 | 2 | 3 |
| DEL-08-01 | 16 | 7 | 0 | 9 | 1 | 1 | 7 |
| DEL-08-02 | 12 | 4 | 0 | 8 | 2 | 0 | 6 |
| DEL-09-01 | 30 | 12 | 0 | 18 | 6 | 2 | 10 |
| DEL-09-02 | 31 | 8 | 0 | 23 | 12 | 0 | 11 |
| DEL-09-05 | 13 | 5 | 0 | 8 | 6 | 0 | 2 |
| DEL-09-06 | 24 | 11 | 0 | 13 | 4 | 0 | 9 |
| DEL-09-07 | 25 | 10 | 0 | 15 | 1 | 0 | 14 |
| DEL-09-09 | 20 | 6 | 0 | 14 | 2 | 4 | 8 |
| DEL-09-10 | 11 | 4 | 0 | 7 | 3 | 0 | 4 |
| DEL-09-11 | 10 | 4 | 0 | 6 | 2 | 0 | 4 |
| DEL-09-12 | 14 | 6 | 0 | 8 | 2 | 0 | 6 |
| DEL-10-01 | 22 | 11 | 0 | 11 | 1 | 0 | 10 |
| DEL-10-02 | 13 | 10 | 0 | 3 | 1 | 1 | 1 |
| DEL-10-03 | 20 | 7 | 0 | 13 | 10 | 0 | 3 |
| DEL-10-04 | 14 | 4 | 0 | 10 | 2 | 1 | 7 |
| DEL-11-01 | 12 | 7 | 0 | 5 | 3 | 0 | 2 |
| DEL-11-02 | 22 | 7 | 0 | 15 | 2 | 0 | 13 |
| DEL-11-03 | 16 | 5 | 0 | 11 | 3 | 2 | 6 |
| **Total** | **759** | **355** | **1** | **403** | **109** | **52** | **242** |

`RegisterAccounting.csv` adds full register paths. `AssemblyChecks.json`, `SCC_Accounting.json`, `Tool_Run.json`, and `ManifestCheck_Run.json` carry checks and exact invocation/fingerprint evidence. Strict admitted audit exits 0; this is an admitted-topology result only. No acceptance, readiness, lifecycle or input fulfilment follows.
