# Placement decision preparation — Group A

Status: **PROPOSED; no owner placement decision recorded by this packet.**
Run: APP-V4-GROUP-A-20261004. TASK `/root/group_a_owner_choices`, delegated-harness-native child of HELP_HUMAN `/root`; user-selected gpt-6.1-sol / medium; no descendants. Read-only investigation; only this packet written. Execution manager `/root/group_a_execution` owns graph, Design and code integration. No downloads, network, credentials, product writes, acceptance, qualification or gate decision.

## Finding and point of need

**Placement does not block CI-1…CI-9 preparation/review, portable temp cleanup, dependency inventory, or contract-neutral hosting/recovery and workflow/role work.** OI-013 is principally the external host's construction decision, and the owner has deferred host joins. It must not be expanded into permission for Group A to build SWBPIPE's loop. OI-014 becomes immediate when production code allocates shared components or chooses the App record/capture stores. The graph's I3 explicitly waits for placement; RS U-05 says “Before writer implementation.” The existing skeleton already writes files, but its existence supplies evidence and a concrete option, not an owner ruling.

Do not leave I3 silently waiting behind one broad OI label. Bring the bounded App record-location/component-allocation choice when the reviewed CI repairs release I3. I1/I2 can proceed if they do not silently settle those stores or shared allocations. CI9's validator/checker choice is a distinct implementation/dependency issue; placement approval alone does not authorize its download or weaken RS W-1.

## What is already chosen, and what remains reserved

| Established basis | Standing and consequence |
|---|---|
| App hosts stock Codex; host uses its own minimal loop over Chat Completions | ARCH §4 V4-ARC-10 and pass-2 owner “keep Chat Completions for the host loop as recommended.” App runs no Chirality loop (LOOP §10.2). Choosing a common App/host loop would reopen this boundary. |
| Host network/credentials stay native; parsing/streaming do not block UI where needed | ARCH V4-ARC-12 and §4 properties. These are required outcomes; worker versus native placement is still host-selected. |
| Host owns loop construction, parsing, persistence, panel assembly | ARCH §4 final paragraphs; LOOP §10.1; PANEL §6. Group A defines/receives contracts; SWBPIPE implements externally. |
| Shared meaning does not prescribe executable service | ARCH V4-ARC-20. Compatible local implementations, a library and a service are alternatives with different costs; actual repeated responsibility must justify sharing. |
| Checkpoint agent asks; product records current-phase arrivals without holding | DECISION-K1 K1-1…3; no placement option creates a governance hold or changes reserved acts. |
| Rust host owns App process/request register/writing; interface composes/presents; native event captures | R17-5 is an **integrator proposal**, labelled OI-008 O-1 PROPOSED, implemented by skeleton. AAC P-2 native confirmation remains PROPOSED; P-3 per-act OS presence check was explicitly not adopted (DECISION-L L-5). Do not report Rust/native placement as an already accepted OI-013/014 decision. CI5 clarifies A16's native-confirmation behavior separately. |
| RS shared container and append-only writer/reader obligations | RS §§13–14; S-A is PROPOSED. Alternatives S-B/C/D remain described; S-B rewriting conflicts with OF-5. Serialization fixtures do not choose storage placement (RS §13 opening). |

Reserved: OI-013 loop placement, parsing, persistence and panel assembly at the shared/host boundary; OI-014 actual component/contract allocation before common implementation; RS U-05 App record location; ACT U-12 policy representation placement; AAC capture-store location (AAC §5.2). OI-008/native capture cannot be folded into these as a generic “approve.” The current Group A owner record authorizes development sign-in only, and explicitly lists placement as still needed.

## Concrete choices for the owner

These are agent recommendations for a bounded next allocation, not an attempt to close both OIs globally.

### A. App-local production first — recommended

Proposed decision text:

> For this Group A production slice, allocate App record writing, capture storage and policy consumption to App-local components. Use the shared Design schemas/contracts as their conformance basis; allocate no common executable service, host loop or reusable host panel yet. Keep SWBPIPE construction and persistence with its owner and its joins deferred. Implement App run records as append-only JSON Lines logs per run and writer, and a separate standing-act log per writer; A15 acts travel with their library. Prepare and review the exact paths and migration from the skeleton before production adoption. This does not close OI-013 or the remaining OI-014 candidates.

Consequence: I3 can proceed after the exact path choice below and the reviewed CI changes. App work can be examined independently; future shared reuse remains extractable. Cost: compatible host implementations may later duplicate small pieces and need conformance checks. Benefit: no unestablished cross-host service dependency.

### B. Small shared library now

Allocate only an identified repeated part with named consumers and an owner. Existing candidates: LOOP §10.2 parse completeness and catalog-schema argument checking (the latter may serve ADAPTER); PANEL §6 act/lapse/supersession, grant-state/scope, workflow-identity/required-tool presentation. None has current agreement. Proposal disposition needs an API, consumer adoption, versioning and independent review before common implementation. No whole loop, conversation renderer, tool-activity renderer or proposal queue is supported as common by the present evidence (PANEL §6).

Consequence: less eventual duplication if consumers truly share behavior; introduces library boundary/build/version work now. SWBPIPE receipt and actual use remain deferred. Recommendation: revisit catalog-schema checking first once both concrete consumers require it; don't commit all candidates as one library.

### C. Common executable service

ARCH V4-ARC-20 permits consideration but does not presume it. No present contract establishes a common execution responsibility (LOOP §10.2 expressly says none). Requires concrete consumers, service lifetime/failure/IPC authority, scope/ownership analysis and propagation before adoption. Recommendation: do not select for this slice; it adds an unsupported production dependency. It is not interchangeable with a schema library.

## Exact App record-location choice to present with A

Recommended proposal for reviewed Design adoption:

> Keep App-generated project run logs and capture files under the opened project's `.chirality/records/` and `.chirality/captures/`. Use `.chirality/records/runs/<opaque-run-storage-key>/<writer-storage-key>.jsonl` for per-run/per-writer logs, `.chirality/records/acts/<writer-storage-key>.jsonl` for standing acts, and `<library>/.chirality/records/acts.jsonl` for A15 library acts. Storage keys are safe path segments minted/mapped by the App, never interpreted as governed record identities. The capture resolver owns `.chirality/captures/` and resolves `cap:` references. Writable-target failure is reported and records/captures never silently relocate. Before adoption, review reader discovery, concurrent writer behavior, identity binding and migration of skeleton records; preserve old logs as history.

This is concrete **proposed text**, derived from RS S-A/OF-5/6 and the existing skeleton capture store, not a source requirement. Skeleton `recorder::LOG` is currently `records/coordination.rs.jsonl`, one coordination log; capture store is `.chirality/captures`. The proposed run layout must not be represented as already implemented. Library path is currently expressly a placeholder (RS U-05). Compare alternatives with the human: App user-data storage (central discovery, weaker portability), or explicit project-selected external root (flexibility, reference/discovery/move complexity). Confirm intended behavior when no writable project is attached, rather than inventing a fallback. Path migration and identity/canonicalization details are implementation work under review, not solved by this packet.

## OI-013 host options to preserve for the owning session

The already stated alternatives are interface thread, worker, or native layer (ARCH §4). Interface-thread execution is acceptable only if long parsing/streaming do not block host UI; worker needs controlled native network/capture/persistence bridges; native layer naturally owns those host resources but adds IPC/event ordering/recovery work. Recommend the host owner assess worker/native against actual host implementation. Group A may supply receiving fixtures and replay/failure expectations without selecting the host option, retention duration or host schema checker. LOOP §3.4 replay may truthfully report events not held; it does not select retention. Positive host-conformance evidence still waits for an identified candidate and owner-resumed joins.

## Scope and propagation

Affected Group A contracts: DEL-04-03 RS paths/discovery/writer-reader behavior; DEL-01-04 AAC capture store/resolver and NIR presentation; DEL-04-01 policy placement; DEL-02-02 library act log; DEL-02-03 recorder; DEL-03-01/03 and DEL-05-01/02 only if a shared checker/component is actually allocated. Group D consumers of App records/captures and Group B packaging may require notice through their work graphs when these exact allocations affect them. No finished downstream work is declared unaffected without comparison.

GC-7/8: internal details belong in Group A's graph; cross-group needs go in each affected loop's graph, and if absent remain in Group A until that loop starts. No new standing relationship list. GC-9: any agreed Design interface change is named, reviewed and propagated. Bring parent/human in immediately if allocation changes deliverables, reverses group order, creates a cross-group cycle or invalidates another group's completed work. No DAG reconstruction just to resolve these bounded internal choices.

## Retrieval and evidence limits

Read current entry instructions, AUM headings plus §13 and Field Book; targeted Design sections above and owner records. No ephemeral HANDOFF read. No full design reconstruction, no independent approval review, no code execution or product validation performed. OI-013/014 remain OPEN in Open_Issues.csv; this packet cannot close them. Parent should record actual human words/source/custody in OWNER_DECISIONS separately from these interpretations. Group graph seen during concurrent execution; hashes below bind bytes actually available at packet creation, not a final integrated candidate.

## Source manifest

Repository revision at read basis: `e916ad17892d24fc0d577fc62edd1be22d8d73b4`. Paths relative to Root. SHA-256 pins preserved for instructions and substantive evidence; only relevant sections were loaded unless stated above.

| Source | SHA-256 |
|---|---|
| `AGENTS.md` | `f96feb19d297c74e10048c506805b2fe3622c50cfefd6078f599724556113977` |
| `agents/AGENT_TASK.md` | `1a13a5b00b3ce01ff8519efe6b46bcbe0cd6a5b7985e24282fa7efa2c57c8fb7` |
| `projects/chirality-app-v4/loop/LOOP_INIT.md` | `45c23cf477e23aff1d0152189caf7e8ebfb53eca42e3a1fae87a06af8c197f28` |
| `docs/alignment-manual/README.md` | `31217d30b0d2743bef0d7c1a54bb9a81814d56b24ff0961cf01d9532952e305f` |
| `docs/alignment-manual/CHIRALITY_AGENT_USER_MANUAL_v3.md` | `08ca0e40cd5157574a011bac57d539e77e9007a0d46494785da8b92745391b1a` |
| `docs/alignment-manual/Project_Management_for_Human_Agent_Teams_Field_Book_v1.md` | `02d53a3966220001318aacf3f46e1b63b8695a098c81b20f4e3e1531b93024d3` |
| `projects/chirality-app-v4/docs/ARCHITECTURE.md` | `317d5789272c5206599936fa9b4e68551b30016d226b88039f0153afa02d828c` |
| `projects/chirality-app-v4/execution/_Decomposition/Open_Issues.csv` | `9c2d916c277f8ce4b847c9c532822d0566e59517ba9e0a86b650fe0450f3515d` |
| `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-GRAPH-CLOSURE-20261004/GROUPS.md` | `d96c399755fe2369cab96d29f73744834a98d70678f2f273f9ad01b0b129940f` |
| `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-GRAPH-CLOSURE-20261004/GC_RULINGS.md` | `22187acaffb9a0e2c5ef6ed415cce0c62c6e6db06361405cf8caf642b5a59a92` |
| `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-GRAPH-CLOSURE-20261004/OWNER_DECISIONS.md` | `9494d39b7405fc6342aea13e00073fbdebe21c5014e32620b752321fa1aa6136` |
| `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-GROUP-A-20261004/OWNER_DECISIONS.md` | `70d4ebe882ac67221afb05134a63d79b76f3e47dffe184253c09ad4be53f2744` |
| `projects/chirality-app-v4/execution/_Coordination/WorkGraphs/APP-V4-GROUP-A-20261004/WORK_GRAPH.md` | `921252cf288bcf4b49c0738f7276295fd46a2eda29d3c132d7f97c4e500dddea` |
| `projects/chirality-app-v4/app/CONTRACT_ISSUES.md` | `b34507c62daec69fe2ca7152757757a31d6429d7786c797c7097e693f2675639` |
| `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-FIRST-INCREMENT-20260928/OWNER_DECISIONS.md` | `a9869129753631b865cbbb00a138c0f497d5ac8a4b67f5746169d1f9a668ad2c` |
| `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-DESIGN-PASS-2-20260930/OWNER_DECISIONS.md` | `b2fa81871cbf44b978894c8d0512c66d55a66e3c50db21df56e00ddbf651e05b` |
| `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-DESIGN-PASS-3-20261001/OWNER_DECISIONS.md` | `8a5d11149045770dfcf1a19ebabb86bfe9f04cd3e65ed36166cb8593e2fe20ac` |
| `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-DESIGN-PASS-3-20261001/R17_RESOLUTIONS.md` | `b0af81bcbad9bc52fddc99119c42a19019a9b174677d5b92a0a2f5c8b4f8e198` |
| `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-DESIGN-PASS-4-20261003/OWNER_DECISIONS.md` | `e4350f61a93edf0d2d4bfc588fcaa17ae23981baa6059617dcc430cda3008cd8` |
| `projects/chirality-app-v4/execution/PKG-03_Host capability and operation contracts/1_Working/DEL-03-01_Capability catalog and read-basis contract/Design/CATALOG_AND_READ_BASIS.md` | `0e3ba39cd926a2063fc93621c17ed39d1fc8622b2256f08005d1286e99795294` |
| `projects/chirality-app-v4/execution/PKG-03_Host capability and operation contracts/1_Working/DEL-03-02_Proposal, validation and outcome contract/Design/PROPOSAL_LIFECYCLE_AND_OUTCOMES.md` | `ad6a3083e7b808e247562fa0cc3762192b121ff99e75e8ac8167ab25da555eb3` |
| `projects/chirality-app-v4/execution/PKG-03_Host capability and operation contracts/1_Working/DEL-03-03_Local external-agent receiving adapter/Design/ADAPTER_ENABLEMENT_AND_RECEIVING.md` | `eed1d912df333822c172593ea81a244661dab305b81c6295493802f252eda761` |
| `projects/chirality-app-v4/execution/PKG-03_Host capability and operation contracts/1_Working/DEL-03-04_Host boundary and integration guide/Design/HOST_INTEGRATION_GUIDE.md` | `5050658818c24a8600e53686d16a7f6ca6aba9724ee558ecc17d3d9a184b113b` |
| `projects/chirality-app-v4/execution/PKG-05_Embedded-host receiving integration/1_Working/DEL-05-01_Minimal-loop and model receiving contract/Design/LOOP_RECEIVING_CONTRACT.md` | `2bac33a883b176e24cd17e6fb78361efea63ce4c254810dcf8ab6e1d13cd7004` |
| `projects/chirality-app-v4/execution/PKG-05_Embedded-host receiving integration/1_Working/DEL-05-02_Host panel and shared interaction receiving/Design/PANEL_RECEIVING_CONTRACT.md` | `4898b6f80832b3baae9fd7e2e24e2fe6141a0d2b12359f1c0dce5647ccee6999` |
| `projects/chirality-app-v4/execution/PKG-04_Human acts, autonomy and run evidence/1_Working/DEL-04-03_Content-bound decisions and compact run records/Design/RECORD_SEMANTICS.md` | `a2c390b4641c47ae3150b52ff97365ccbff3dec08274fb2f3892d311e7c674b3` |
| `projects/chirality-app-v4/execution/PKG-04_Human acts, autonomy and run evidence/1_Working/DEL-04-01_Operation-policy and human-act distinctions/Design/ACT_AND_POLICY_CONTRACT.md` | `597f13bda1fe1c1fa97b9db8ebc92483c2b43ebcbdc784d91be1f57fa93df5f2` |
| `projects/chirality-app-v4/execution/PKG-01_Native App and third-party harness integration/1_Working/DEL-01-04_Native requests, outcomes and attachments/Design/APP_ACT_CONTROL.md` | `657659b8396f2c15a5a64035c1c3dd13826611812c776c4b1dbc4df9e144e348` |
| `projects/chirality-app-v4/execution/PKG-01_Native App and third-party harness integration/1_Working/DEL-01-04_Native requests, outcomes and attachments/Design/NATIVE_INTERACTION_RECEIVING.md` | `aca40c0e326dae03a06fe5767c2c2e81b79600286b393bfa0dee68cc819cc6cb` |
| `projects/chirality-app-v4/app/src-tauri/src/records.rs` | `9a7d2bf86679489868ea4b5bd2aeb3f3187a992bcfbd40c09384aa94bf99e7bc` |
| `projects/chirality-app-v4/app/src-tauri/src/recorder.rs` | `485987c3958dc4b3b6aefca3f9b429fbd914f5496d8a320e286533ce8c2e5bd6` |
| `projects/chirality-app-v4/app/src-tauri/src/act_control.rs` | `6a43e6eabf0de1a40ef0768ca1444fe46018c56aecaaad558dc3420743c81ac4` |
| `projects/chirality-app-v4/app/src-tauri/src/lib.rs` | `2995fc41188438c344f0dcd8c7a948e0b796703b6cb1a8a263bb176e176944e0` |

## Current reviewed recommendation — manager amendment

Write ownership transferred by parent after the TASK author completed. This supersedes the earlier proposal's incomplete library capture root and ambiguous standing-act duplication. RS and AAC current design owners examined it in their CC-R/CC-A returns; manager checked WR K-8, A15 ledger/identity and RS S-A. Recommendation remains PROPOSED until owner decision.

**Allocation and exact paths:** App-local Rust record writing, capture storage and policy consumption; shared Design schemas as conformance basis; no common executable service, host loop or panel implementation. Project run logs `.chirality/records/runs/<safe-run-storage-key>/<safe-writer-storage-key>.jsonl`; standing acts captured outside any run only in `.chirality/records/acts/<safe-writer-storage-key>.jsonl`. A15 library acts `<library>/.chirality/records/acts.jsonl` and their captures `<library>/.chirality/captures/`, so portability preserves resolvable evidence. Other project captures `.chirality/captures/`. Safe opaque storage keys remain separate from governed record/run identities.

**History and failures:** Reader discovers new roots plus explicitly registered legacy `records/coordination.rs.jsonl`. Preserve legacy bytes and identities; no implicit copying, recapture, new IDs or duplicate act. Recovery accounts for all discovered owning logs before replay. Unwritable targets refuse visibly; no silent relocation. A new path choice does not itself migrate old evidence. This bounded allocation leaves external OI-013 and other OI-014 work open.

**Consumer concurrence:** RS owner requires standing log to mean outside-run captures, not a duplicate index of all run acts; AAC owner requires library capture co-location and complete legacy-log recovery. WR's bound reviewed A15 and ledger keep the same act identity; current source definitions supply required input, product adoption still ahead. Downstream D views and B packaging must receive actual named adopted changes; no downstream finished work silently considered valid.

## Separate native-control implementation allocation question

R17-5/AAC P-2 remain recorded proposals; the60% grouping/gate is not unambiguous custody construction approval. Ask separately: approve the App Rust host as authoritative record writer and capture owner, with a host-owned native Decide/Cancel confirmation displaying the full immutable chosen act statement and consequences; only actual native confirmation captures, webview supplies presentation/selection only. Do not add per-act OS presence/password check (L-5 declined P-3). This decides implementation allocation, not authenticity qualification or proof that a human acted. Native script-isolation and durability witnesses remain implementation/qualification checks.
