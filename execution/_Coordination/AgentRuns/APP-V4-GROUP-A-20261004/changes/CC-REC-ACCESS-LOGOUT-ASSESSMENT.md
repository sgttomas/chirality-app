# CC-REC-ACCESS-LOGOUT-ASSESSMENT — observed live-work consequence

2026-10-05. TASK `/root/group_a_execution/design_records_exec`, parent WORKING_ITEMS `/root/group_a_execution`; no delegation. Read-only source assessment; only this packet written. PROPOSED recipient interface/interpretation for named source review before product adoption, no Design/product/Git/Cargo/auth/native/model/network/credential action or new human gate.

## Exact governing clauses

ACCESS AE-12 asks first when H-acct has live work, listing live turns, outstanding requests and active delegated children (REC assess-live-work/K4); Q-5 and RV21 MINOR10 require all THREE lists. KE-13/Q-7 applies the same pattern to the key home. ACCESS I1/AE14 treats missing/error response as unknown and re-reads; CR1/2/4 preserve native credential custody/redaction, CR5 forbids token-refresh reads by App rule, CR6 forbids automatic credential replay, CR10 carries the user's store mode unchanged.

RECOVERY §4.1 assess-live-work returns the same three lists for homes actually named (all by default), runtime only: nothing recorded/changed. Its descendants row explicitly says **none observed is “none observed”, never “none”**. §3.4/I6 preserves descendant observations and never infers their stop from parent outcome; U-R1/O4 native child interrupt/cascade coverage remains open. REC/RS preserve actual unknown/observer/source/time, separate interrupt/run-end/process-stop and actual act from operation success. No clause supplies an omniscient active-child census or permits an all-safe inference from an empty observed list.

## Concrete least scope-preserving consumer

Implement the existing REC assessment facade over actual selected-home/full-generation sources, returning one read-only snapshot: selected home, full H5 generation, source/receipt references and observation times; observed live-turn IDs/status, outstanding received-request IDs/method/status, observed active-child IDs/status; per-list coverage/availability and explicit child-visibility/completeness unknown plus known-child history whose current activity is unknown. No payload/credential copy, new row/kind/store or native-control capability follows from this runtime value.

Host currently exposes conversationTurns/serverRequests/nativeItems and known-child history; these are inputs, not a complete assess-live-work API. Each item must have current source/generation warrant. Surrounding current snapshot G cannot silently retag stale child/history into G. History-only child is unknown activity, not active or stopped. Window/renderer cache never substitutes for the main source. Include the whole selected home’s observed work, not only the current window/thread. Missing visibility produces a limit, not an empty complete census. Do not claim complete native coverage until actual source proves it.

For native logout confirmation, list all three observed sets with timestamps/source limits and clear “child visibility/completeness not established; additional work may exist.” Always-confirm on this unknown boundary is an ordinary implementation of existing ask-first/explicit-person intent, not an extra governance approval. Empty observed lists never mean all safe/no work. If the selected home/account/full generation itself cannot be established, report unavailable/refuse the scoped route until that source is established; do not route through the current window/default/other home.

Bind the person’s native confirmation to that immutable source snapshot/target. Before actual account_logout_scoped, recheck full generation/home/current reported account and material live IDs/status/availability/coverage. Changed meaningful context refreshes the warning/confirmation or cancels; timestamp passage alone is not a new state/warrant. No scope switch after an await; no Host Inner/Stop-critical lock held through a dialog or blocking native IO. Native Cancel writes no logout/removal request. Preserve original observations rather than rewrite them as current after recheck.

Logout send/write/result/account-observation are separate facts. ACCESS AE13 may show Codex-reported typed logout success; that is not a credential-store inspection/proof, turn end, child stop, run end, history deletion or grant/reliance act. Unknown/error stays unknown with its cause, followed only by existing allowed source read; no automatic resend/removal or provider/home switch. Follow CR redaction/no credential read/copy/cache; no claim another home or all accounts were affected. Provider/model defaults are untouched.

## Source ambiguity and owner disposition

No accepted complete-census promise found: the explicit REC none-observed and descendant limits qualify what assessment knows. But the required **three-list assessment** is a real runtime prerequisite and today’s disconnected snapshots do not establish it delivered. Least change is the actual REC-owned aggregate facade + explicit per-source limits, then ACCESS native confirmation/recheck; a completeness boolean invented by UI cannot replace it. If an owner requires bypassing confirmation on no-work, that path must first establish negative completeness—it is NOT warranted today. This bounded interpretation requires REC/ACCESS source agreement/independent checking before product claims; no SoW narrowing or human checkpoint inferred.

ACCESS owner design_hosting_access was actually consulted and source-CONCURS the observed-list/unknown/always-confirm fit, selected full-home namespace and material recheck; if assessing the home itself is unavailable, no current-window/default fallback. This is source-fit concurrence, not actual consumer/auth/native qualification. Recipient implementation owners: REC/shared facade and ACCESS/history_product_join native flow, Core scoped logout/receipt. Parent routes exact named review; actual native UI/account removal witness remains separate.

## Required controls before adoption

Observed active work in each of the three lists is shown; no children observed with unknown visibility still warns/asks. History-only/stale generation child does not become current or absent. Two homes/current-window switching cannot retarget logout. Generation/account/new turn/request/child or coverage change during confirmation refreshes/cancels before write. Cancel writes nothing; unavailable assessment sends nothing through guessed scope. Typed error/no response remains unknown; native success does not end turns/delete history or inspect credentials. Mandatory supplier replies/Stop liveness continue during assessment/dialog; no quiet snapshot is construed as approval. Tests/native/auth were not run by this source-only task.

## Exact input source hashes

| Source | SHA-256 |
|---|---|
| `projects/chirality-app-v4/execution/PKG-01_Native App and third-party harness integration/1_Working/DEL-01-05_Native OAuth-sign-in, API-key and local-provider access/Design/ACCOUNT_AND_PROVIDER_ACCESS.md` | `5067ed0b64b0a7787d33809b542c1cbadd02793e136b136e330bb933d5f8a203` |
| `projects/chirality-app-v4/execution/PKG-01_Native App and third-party harness integration/1_Working/DEL-01-02_Durable execution and request recovery/Design/EXECUTION_AND_RECOVERY.md` | `e78b9ead452b0a1adb20cf07493a1eccbd2ee651e68d4f75772c440a6a228056` |
| `projects/chirality-app-v4/execution/PKG-04_Human acts, autonomy and run evidence/1_Working/DEL-04-03_Content-bound decisions and compact run records/Design/RECORD_SEMANTICS.md` | `15266b5078ad1878dae20dc1fa2ef93723d187ce18d5fe780bd1af75c00d5f41` |
| `projects/chirality-app-v4/app/src-tauri/src/hosting.rs` | `533ba07c51e356a43ad7b0aac422b95031b568e2c6083d5389eb02e000a3ab04` |
| `projects/chirality-app-v4/app/src-tauri/src/runtime_session.rs` | `d965de4e36be243968a422b00b71736d3ef4857ca97f648ec92eb611d4b21d6f` |

## Actual REC recipient facade concurrence — source implementation handoff

Parent commissioned actual REC source concurrence after independent READY of original1d3f packet (V0-REC-ACCESS-LOGOUT-ASSESSMENT007178). Shared history_product_join actually returned this consuming plan and REC owner CONCURS its source meaning; no disconnected snapshots are declared delivered. The receiver facade is owned by selected HomeSession/runtime and returns one immutable read-only assessment object: actual home/fullG/account-scope observation/revision, original source cursors/times, observedLiveTurns, observedOutstandingRequests, observedActiveChildren, knownChildActivityUnknown, per-source coverage/availability/limits. No persistent row/type or native capability follows from this runtime interface.

Gather from that SAME HomeSession Host observation plus RuntimeSession receiving state. Turn/status and received outstanding request must have actual current-G source; descendant data uses original NativeView G, not surrounding current snapshot. Native agentsStates running/pendingInit may be reported as observed activity under that original G; other/known-history child remains unknown current activity. Explicit child completeness/visibility unknown and none-observed/not-none remain, even when all observed lists empty. Runtime/context availability itself must be established; no window/default/home fallback.

Native confirmation shows all three sets and limits. Re-assess the SAME private lane before logout and compare meaningful fullG/home/account namespace revision and material native IDs/status/availability/coverage. Source cursors/receipt positions/time are provenance; unrelated receipt-counter increments or timestamp passage are NOT blanket stale-confirmation veto. Changed meaningful target/work requires refreshed warning/confirmation or cancel; no all-safe/child absence/process stop/native removal proof. Mandatory supplier replies and Stop remain live during aggregation/dialog. This is the exact existing REC assess-live-work runtime facade recipient basis, not a new claim the code exists or native effect is qualified.

Owning ACCESS concurrence to actual1d3f is recorded in adopted OAuth packet8efa; current ACCESS/HOST OAuth custody amendments preserve AE12/Q5/KE13 assessment separately. REC OAuth recipient source review below is independent of actual logout code release. Original source assessment1d3f remains its READY association; this append narrows implementation handoff/provenance, not an accepted promise change or new human gate. Parent source reviewer received this exact source-fit interface before code adoption.

Prior logout packet SHA-256 `1d3f300b0ffc0b0099ec9ccdde9a074357ec34447cf5118e308b8f99e3f505ba` preserved. Fresh receiving source pins:

`projects/chirality-app-v4/execution/PKG-01_Native App and third-party harness integration/1_Working/DEL-01-02_Durable execution and request recovery/Design/EXECUTION_AND_RECOVERY.md` SHA-256 `e78b9ead452b0a1adb20cf07493a1eccbd2ee651e68d4f75772c440a6a228056`.

`projects/chirality-app-v4/execution/PKG-01_Native App and third-party harness integration/1_Working/DEL-01-05_Native OAuth-sign-in, API-key and local-provider access/Design/ACCOUNT_AND_PROVIDER_ACCESS.md` SHA-256 `26659864fd1b720d51bc5bf8038311238e9d6b1775f62a4e08fd2917dba4f9ec`.

`projects/chirality-app-v4/execution/PKG-01_Native App and third-party harness integration/1_Working/DEL-01-01_Stock Codex hosting and supplier contract/Design/HOSTING_BOUNDARY.md` SHA-256 `9839cb38310ff55045657e51f7bb7dcfcb2024eb43ec3bab364959e33e5c1e85`.

`projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-GROUP-A-20261004/changes/CC-ACCESS-OAUTH-CONTROL-CUSTODY.md` SHA-256 `8efa4401058a74d03cd57177699e463798cff5e78d123e7b8d5f6a7642fb36a4`.

`projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-GROUP-A-20261004/reviews/V0-REC-OAUTH-CONTROL-CUSTODY.md` SHA-256 `690accb9e829f4226724bee797602bc25f8cb9320afc3942f8b6517f421ee6f0`.
