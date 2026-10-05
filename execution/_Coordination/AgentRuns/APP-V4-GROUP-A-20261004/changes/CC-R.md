# CC-R — RS/EXEC contract clarification and repair

Run `APP-V4-GROUP-A-20261004`. Author TASK `/root/group_a_execution/design_records_exec`, delegated-harness-native child of WORKING_ITEMS `/root/group_a_execution`; model gpt-6.1-sol, medium. No delegation. Working root resolved from active checkout `/Users/ryan/.codex/worktrees/077c/chirality`. Supplied basis and scope: parent launch message plus Root/project entry and TASK guidance below. Writes confined to DEL-04-03 and DEL-02-03 Design and this change record. No application code, shared graph, issues, MEMORY, download, network, credentials, live turn or Git mutation.

Status: PROPOSED/APPLIED FOR INDEPENDENT REVIEW; consumer propagation not authorized by this record. CI-4 owner choice applied to handoff; CI-9 implementation remains held.

## Proposed changes and rationale

- **CI-1:** Replace exactly 19 file-relative RS schema refs with EXEC's existing absolute `$id` `chirality:del-02-03/exec-checkpoint-entry-bodies/proposed-0.7` plus the same JSON Pointer fragments. RS's URN base no longer needs a loader rewrite. Both local prototype loaders register EXEC by ID; kind coverage checks the actual ID. Inventory behavior, schema IDs and format remain unchanged.
- **CI-3:** RS §13.6 permits requester identity only when an observed source links the writer to the package path and identified bytes. The source reference is optional `requester.evidence` in EXEC's CE-4; the file remains CE-4's own `evidence`. Without writer observation, record `{kind: agent}` without identity and separate RS `evidence_limit` label `requester identity not established`, referring to the request. No author is inferred from the folder, filename, reader thread or recorder. Fixture identity removed; local RS conversion exercises the request and separate limit. The optional evidence field and added label clarify a proposed format; they do not establish supplier observation or verified identity.
- **CI-4 (owner-selected handoff):** OWNER_DECISIONS.md records the actual parent-relayed human answer “Use the explicit absence label (recommended)”. Retain optional package scope and use the faithful offer/capture/human-act wording `not named by the package` when omitted or empty; preserve the package bytes and copy present nonempty scope. Do not insert inferred subject/purpose wording. AAC owner applies the coordinated concrete wording; RS §13.6 states that request scope stays source-faithful (absent/empty/present), and offer/capture/human-act scope follows the displayed label. A required/nonempty package scope would reject previously valid 0.1 files and engage RS §13.4's rule for newly required elements. Package schema and source mapping remain unchanged; the capture-scope helper/check covers all three cases without rewriting package bytes.
- **CI-9:** Preserve W-1 host writer validation of each complete entry before append against RS and registered ACT/AS/EXEC schemas. Unavailable validation refuses append. A later checker is insufficient. Required dependency: owner-approved Rust JSON Schema 2020-12 validator plus transitive dependencies and schema registry, with no network retrieval. Exact file/source/size inventory and download approval belong to manager/dependency owner. No crate chosen or downloaded here. Skeleton unchecked writes remain nonconforming until host implementation and refusal tests pass; local prototype and standard validator do not close CI-9.
- **D07:** RT-11 carries EXEC's supplier inventory and names DEL-09-06 as receiver/joined-witness owner. W14 ← EXEC mapping remains in CA §8.2 under R10-11; the supplier no longer imports the receiver's case list as its definition. No case content or joined witness changes. Receiver consumer list remains authoritative.
- **U08:** RS R11 drops its circular CAF-24 citation and cites R14-3/EXEC A-7/HA-1. R14-3 is the adopted origin; CAF-24 is a consumer. No vocabulary or act standing changes.

## Verification

Offline Python 3.13; no packages installed. `python3 -B Design/prototype/run_all.py --write-examples` (EXEC): exit 0, `ALL CHECKS HOLD: 0 failure(s)`. Regenerated examples account for the absent requester identity. `python3 -B Design/prototype/run_prototype.py` (RS; scratch outside repository): exit 0, `RESULT: all expectations held`; EXEC valid example 12/12 RS entries, other CH runs/samples plus decision package 43/43. Decision-package case writes its two CE bodies plus the explicit missing-identity RS limit.

`python3 -B Design/prototype/check_cc_r.py` (RS) uses already installed jsonschema/referencing: all four schemas structurally valid; 66 valid RS entries validate, 28 negatives reject, solely registering declared IDs with no retrieval/rewrite. Missing package scope still validates, confirming optional file scope remains intact; the owner-selected capture helper maps absent/empty to the label and nonempty unchanged. Absent requester identity, an optional sourced identity shape (scripted test values), and the separate missing-identity limit validate. Schema shape checks cannot establish real requester provenance. An initial scratch check mistakenly validated a detached `$defs` body without its root; corrected to use absolute schema-ID refs before the final passing run.

Independent review has not been performed by this author. Manager must commission fresh review of these exact hashes, then propagate and test against actual consumers. No required CI/build or host-code validation was run.

## Outside consumers and required action

- `app/tests/validate-records.test.mjs`: remove in-memory schema rewrite after reviewed adoption; register EXEC directly.
- `app/src-tauri/src/records.rs`: implement W-1 host validation/refusal; CI-9 dependency blocks compliance.
- `app/src-tauri/src/recorder.rs`: requester provenance and missing-identity limit; coordinated CI-4 package scope mapping under the owner decision.
- `app/README.md`, `app/EVIDENCE.md`, `app/CONTRACT_ISSUES.md`: manager updates compliance/account only after actual adoption and execution.
- DEL-01-04 AAC/prototype: coordinated package scope offer/capture rule, provenance shown with absence; independent owner review underway.
- DEL-06-02 DECISION_VIEW: package source/record meaning and absent author limit; no writer identity inferred.
- DEL-09-06 CA/W14 rehearsal: retains its own mapping; receives source-clarified RS label. D07/U08 remove reverse reading only; joined witness remains receiver-owned.
- DEL-03-04 GUIDE: reviewed source pin/citation reconciliation after adoption.
- DEL-02-01, DEL-02-02, DEL-02-04, DEL-04-01, DEL-04-02, DEL-03-03, DEL-05-01/02, DEL-09-09, DEL-09-05, DEL-09-11: shared RS/EXEC semantic/schema consumers; manager assesses affected pins, validators and prototype registries. No automatic claim of updated adoption.

No outside consumers were edited. Source search locates candidate consumers; reliance/required changes are checked at their owner, not inferred solely from mentions.

## Input origins and hashes

Entry reading: Agent User Manual headings through level 3; Field Book full; Root/TASK/loop full; bounded SoW/MEMORY and Design; prior rulings R23-24, R10-11 and R14-3; GROUP_SORT D07/U08. No other full role instructions, workflow or skill bodies selected.

| Supplied/read source | SHA-256 |
|---|---|
| `AGENTS.md` | `f96feb19d297c74e10048c506805b2fe3622c50cfefd6078f599724556113977` |
| `agents/AGENT_TASK.md` | `1a13a5b00b3ce01ff8519efe6b46bcbe0cd6a5b7985e24282fa7efa2c57c8fb7` |
| `projects/chirality-app-v4/loop/LOOP_INIT.md` | `45c23cf477e23aff1d0152189caf7e8ebfb53eca42e3a1fae87a06af8c197f28` |
| `docs/alignment-manual/README.md` | `31217d30b0d2743bef0d7c1a54bb9a81814d56b24ff0961cf01d9532952e305f` |
| `docs/alignment-manual/CHIRALITY_AGENT_USER_MANUAL_v3.md` | `08ca0e40cd5157574a011bac57d539e77e9007a0d46494785da8b92745391b1a` |
| `docs/alignment-manual/Project_Management_for_Human_Agent_Teams_Field_Book_v1.md` | `02d53a3966220001318aacf3f46e1b63b8695a098c81b20f4e3e1531b93024d3` |
| `projects/chirality-app-v4/execution/_Coordination/WorkGraphs/APP-V4-GROUP-A-20261004/WORK_GRAPH.md` | `aab07f4d85f15557393cae9d7fe1007bcddfcd14abbdbdb4927c73495d49ff63` |
| `projects/chirality-app-v4/app/CONTRACT_ISSUES.md` | `b34507c62daec69fe2ca7152757757a31d6429d7786c797c7097e693f2675639` |
| `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-GRAPH-CLOSURE-20261004/SURVEY/GROUP_SORT.md` | `fc455c4d85a1925da7c141ed4a6d3c585759dd61991bf9faa7c48fb1979cf001` |
| `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-DESIGN-PASS-4-20261003/R23_RESOLUTIONS.md` | `21b2ccfa0f63d61671eddcebe5c2a41dccd2fc5f901e529808605bd017b3fc11` |
| `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-DESIGN-PASS-2-20260930/R10_RESOLUTIONS.md` | `ad3b6caa4a12660db77abc51b5c02ba70519ee46d55b40d21ee76eb3ca561796` |
| `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-DESIGN-PASS-2-20260930/R14_RESOLUTIONS.md` | `c6a603303693f50e24ea27fcbc9f381a297434e4182f023fbcee941073623576` |
| `projects/chirality-app-v4/execution/PKG-04_Human acts, autonomy and run evidence/1_Working/DEL-04-03_Content-bound decisions and compact run records/ScopeOfWork.md` | `b8b58d674e3ac2d86c53005951ca7182dcdeb810964901191afe14cec07afc66` |
| `projects/chirality-app-v4/execution/PKG-04_Human acts, autonomy and run evidence/1_Working/DEL-04-03_Content-bound decisions and compact run records/MEMORY.md` | `004aef6087bd4d6770c99ad861d9bfee389ca0b3fd85fe7a33d83348ec951203` |
| `projects/chirality-app-v4/execution/PKG-02_Workflow and role portability/1_Working/DEL-02-03_Workflow execution compatibility and round-trip support/ScopeOfWork.md` | `625b299ec1d48de1b80dff74796774cc95ee466870bec06a196e16b840af6e5f` |
| `projects/chirality-app-v4/execution/PKG-02_Workflow and role portability/1_Working/DEL-02-03_Workflow execution compatibility and round-trip support/MEMORY.md` | `73fa90d980f79a40e13310cb79aebc445e6ce7f4e43de140118c43b1091918d2` |

Outside consumer registry requirement: AAC `prototype/run_cases.py` loads ACT/AS/RS only; its owner must register EXEC explicitly by declared ID. An observed K4 unresolved-ref regression is returned for that bounded repair. RS local loaders already register EXEC; no path-based fallback is added.

Owner decision source read for CI-4: `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-GROUP-A-20261004/OWNER_DECISIONS.md` SHA-256 `ef8563a292f745a89173b529ec841458d6d67415732b5a2d6895f003f9520d41`.

## Returned candidate files

| File | SHA-256 |
|---|---|
| `projects/chirality-app-v4/execution/PKG-04_Human acts, autonomy and run evidence/1_Working/DEL-04-03_Content-bound decisions and compact run records/Design/RECORD_SEMANTICS.md` | `0cbf416d3740955971a1c94b92416b0d78936ea462231882b232e8671854b5f3` |
| `projects/chirality-app-v4/execution/PKG-04_Human acts, autonomy and run evidence/1_Working/DEL-04-03_Content-bound decisions and compact run records/Design/RS_RECORD.schema.json` | `c94dbd441388f52de4dbce5b79859abf2a07223bf236f209eedcb6aee548e3e6` |
| `projects/chirality-app-v4/execution/PKG-04_Human acts, autonomy and run evidence/1_Working/DEL-04-03_Content-bound decisions and compact run records/Design/prototype/run_prototype.py` | `a812d7aac7d8daee2a964d20cca933d614a950e8b9e2022b4285ef18a76197b1` |
| `projects/chirality-app-v4/execution/PKG-04_Human acts, autonomy and run evidence/1_Working/DEL-04-03_Content-bound decisions and compact run records/Design/prototype/exec_to_rs.py` | `bef73d225d32eae10693281fb8d05a07102d37d7444a8b18ff8e02d586dc7e62` |
| `projects/chirality-app-v4/execution/PKG-04_Human acts, autonomy and run evidence/1_Working/DEL-04-03_Content-bound decisions and compact run records/Design/prototype/check_cc_r.py` | `a097e09084b05cdea0c228f26ab45943b14b83c902334456e8d9899125c7173b` |
| `projects/chirality-app-v4/execution/PKG-04_Human acts, autonomy and run evidence/1_Working/DEL-04-03_Content-bound decisions and compact run records/Design/prototype/README.md` | `5d92a03051fd25e80b37d524af995d768b22034bf7a9978d0dd09e34a33ededd` |
| `projects/chirality-app-v4/execution/PKG-02_Workflow and role portability/1_Working/DEL-02-03_Workflow execution compatibility and round-trip support/Design/EXECUTION_COMPATIBILITY.md` | `982761a8ad29ee315e41553691ec10281dd8636d14f6f7651f3570d6d7489361` |
| `projects/chirality-app-v4/execution/PKG-02_Workflow and role portability/1_Working/DEL-02-03_Workflow execution compatibility and round-trip support/Design/checkpoint-record-entries.schema.json` | `00d5203a2fa9d099b25f2f8da5732f2d869a18fd0846ebe33d25c9ae2ae135d3` |
| `projects/chirality-app-v4/execution/PKG-02_Workflow and role portability/1_Working/DEL-02-03_Workflow execution compatibility and round-trip support/Design/prototype/run_all.py` | `5f22b059324ead5cdeace994fd79a256bd88034fdccf2ed2a14d5b1c9f911120` |
| `projects/chirality-app-v4/execution/PKG-02_Workflow and role portability/1_Working/DEL-02-03_Workflow execution compatibility and round-trip support/Design/checkpoint-record-entries.example.decision-package.valid.json` | `034734224cd9e73e19d884d783f3dbb02e875658166d4653694e7d6fd3ff2fb2` |
| `projects/chirality-app-v4/execution/PKG-02_Workflow and role portability/1_Working/DEL-02-03_Workflow execution compatibility and round-trip support/Design/checkpoint-record-entries.example.invalid.json` | `6668dccda600c4082c8b473a914c6790f05ed1a53f6a1b1c021b284450f21fe4` |
| `projects/chirality-app-v4/execution/PKG-02_Workflow and role portability/1_Working/DEL-02-03_Workflow execution compatibility and round-trip support/Design/decision-package-file.example.invalid.json` | `e60ce94b96566aade5a697cc0f8623ec314b38f3e47d3023eb92d4e12149392e` |

## Read-only placement consumer check for I3

`PLACEMENT_DECISION_PREPARATION.md` option A aligns with RS S-A/W-0…W-3 and OF-5/6 if its phrase “standing-act log” means **acts captured outside any run**, not a second copy of every run act. Run acts stay in their per-run/per-writer log; standing view discovers and joins run and outside-run logs by governed record/capture identity. A15 uses the library log and travels with that library. The proposal's safe storage keys are path mappings, not governed identities. `.chirality/captures/` resolution must retain the native capture identity and serve the same evidence after reopen, without silent relocation on failure.

Smallest concrete owner allocation to release I3 (PROPOSED; requires fresh consumer review before presentation):

> For this Group A slice use App-local components, `.chirality/records/runs/<safe-run-key>/<safe-writer-key>.jsonl` for run/writer logs, `.chirality/records/acts/<safe-writer-key>.jsonl` solely for acts captured outside runs, and `<library>/.chirality/records/acts.jsonl` for A15 library acts. Use `.chirality/captures/` for the App capture resolver. Discover/join these logs without treating storage keys or a view as authority; preserve record IDs, capture IDs, writer-local sequence, corrections and content-bound scope. Keep the skeleton's `records/coordination.rs.jsonl` readable as legacy history; do not rewrite its contents, fabricate a run assignment, or append the same act as a new capture during migration. New writes use the selected layout. Missing/non-writable targets report failure without silently relocating. Prepare a versioned legacy-discovery/mapping record and exercise duplicate/disagreement, reopen and torn-write cases before claiming migration. Allocate no common service; host construction/persistence and OI-013 remain with their owner.

Needed consumer review: RS log discovery/merge/W-0 recovery; AAC durable `cap:` resolution; WR library A15 path and travel; AS standing over multiple logs; EXEC run/outside-run association. A single coordination log cannot be declared S-A-conformant merely by changing its path. No placement code or Design choice was applied by this check.

OI-008/native capture is separate: recovered R17-5 explicitly remains integrator PROPOSED O-1, and DECISION-L L-5 already selects no OS password/Touch ID per act. Do not reopen that resolved L-5 choice. This author found no broader OI-008 acceptance in the two read owner records; parent should recover any other existing owner act before requesting one. These facts do not close OI-014 globally.

Placement-check source `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-GROUP-A-20261004/PLACEMENT_DECISION_PREPARATION.md` SHA-256 `c7db441de1ec7cbb658ad48a4475e5857bf6d7975a9575992f610c3542e65ee0` (bounded relevant loci; preparation full).

Placement-check source `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-DESIGN-PASS-3-20261001/R17_RESOLUTIONS.md` SHA-256 `b0af81bcbad9bc52fddc99119c42a19019a9b174677d5b92a0a2f5c8b4f8e198` (bounded relevant loci; preparation full).

Placement-check source `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-DESIGN-PASS-3-20261001/OWNER_DECISIONS.md` SHA-256 `8a5d11149045770dfcf1a19ebabb86bfe9f04cd3e65ed36166cb8593e2fe20ac` (bounded relevant loci; preparation full).

Placement-check source `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-DESIGN-PASS-4-20261003/OWNER_DECISIONS.md` SHA-256 `e4350f61a93edf0d2d4bfc588fcaa17ae23981baa6059617dcc430cda3008cd8` (bounded relevant loci; preparation full).
