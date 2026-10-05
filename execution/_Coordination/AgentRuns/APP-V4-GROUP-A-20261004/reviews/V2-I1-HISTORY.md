# V2-I1-HISTORY — independent history query/receiving review

2026-10-05. Independent TASK `/root/group_a_execution/hosting_contract_review` under `/root/group_a_execution`, delegated-harness-native; no descendants. Own repository write: this report only. Retained Root/TASK/LOOP/manual/software-code-review basis; maintained0.160 native schema, RECOVERY history/recovery clauses, NPTD history/child sequences and ROLE continuation/child provenance consulted. No dispatch, supplier/Host/UI/model, network/auth/download, product/Design/Git or delegation operations.

## Exact original candidate and disposition

**Repair before fan-in: three major blocking findings.** Original `changes/I1-HISTORY.md` seal `50739c01c25feb8cf9958f164fdf2539fb4c9d45726f8c030fc362d2b6285a29`; `native_history.rs` `c65fd6598d0d37cbeb175cb11c8f79b02ca5f3598c021115d524e2600910a9fe`; test `9d538238851293f76a5451511d951d74636b5e5fc8b3d98b0d8ec56b73972174`. Seals matched at entry, and original source was copied/verified before independent execution. Native schema root remains `7243ba241962af92ca60581f1a81808ebda4212a800f8b205f54703bcfd508c5`.

Original owner has begun repairs; source later observed e2609ad… is **not reviewed by this verdict**. Preserve original failure evidence; freeze actual successor and backcheck affected cases. Existing published checkpoint/other source is untouched. No active binding, provider execution, durable transcript/recovery, qualification or owner acceptance is inferred.

## HIST-M1 — old resume stays eligible after newer thread-state facts (blocking)

Locations: original `issue` stream revision handling; Metadata receive at572–575; resumed_thread at638–654. Pending callbacks are revision-checked, but accepted `selection.resume` stores only the old native result without its accepted query revision/epoch eligibility. New Continue/thread-state reads do not invalidate it.

Independent valid sequence: select indexed thread; explicit Continue query→matching idle resume with canAcceptDirectInput=true; initial resumed_thread is Some (positive control). Then new matching metadata read returns same thread id with notLoaded and canAcceptDirectInput=false. Metadata correctly changes, but resumed_thread still returns old idle/true candidate. Independent None assertion **fails**. A new Continue pending/timeout similarly leaves old success accessible by source inspection.

Impact: the candidate is no longer justified by the current thread-state query/read, contrary to the unit's revision/current-context claim and RECOVERY recovering/read-completed/read-failed distinctions. “Active owner must recheck” remains a separate required guard; it does not make this helper's obsolete eligibility current. History read-only status cannot be promoted to loaded/live by cached prior success.

Repair: bind accepted resume eligibility to actual accepted query/selection epoch/thread-state revision, withhold it under newer pending/refused/unavailable or contradictory metadata, and retain old response only as clearly historical evidence. New valid matching current Continue response can restore candidate eligibility; never treat query preparation as success. Test newer Continue pending/error/timeout, metadata notLoaded/directInput:false, selection change and fresh successful response. Resume body must remain ID-only and original role unknown absent trusted evidence.

## HIST-M2 — one error slot cannot reconcile independent streams (blocking)

Locations: original receive_error483–494, unconditional error clear in Metadata/Turns/Items572–604, missing reconciliation in Goal/Child606–614, selected snapshot state657.

Two independent reproductions:

- Goal read fails with native error “goal unavailable”; selected state unavailable (positive control). Later same-stream successful goal:null read updates goal but leaves old error/state unavailable. Expected indexed-read-only state fails.
- Goal read fails; unrelated successful metadata read then clears the singular error entirely. Snapshot no longer contains “goal unavailable”. Expected preservation of that independent failure evidence fails.

Child success has the same missing-clear path by source. The error slot also means other success paths can hide failures in independent streams. NPTD SQ-1 requires read error/unavailability to remain explicit rather than imply empty/no-data or successful history. A successful current read must reconcile that stream without erasing unrelated/historical evidence or allowing old failures to masquerade as current failure.

Repair: track current result/error standing by the same logical stream/query revision used for receiving. Clear current failure on its successful same-stream response; preserve prior native error/query evidence separately, and keep unrelated stream errors visible. Derive selected/page/goal/child availability from those actual facts, not a global bool. Add goal and child error→same-stream success plus error→unrelated success controls, including selection/generation closure and stale callback refusal.

## HIST-M3 — arbitrary collab receivers become newly known children (blocking)

Location: original Items receive590–598. Every collabAgentToolCall receiverThreadIds creates knownChildren with senderThreadId labelled parent, without checking tool spawnAgent and completed status. A sendInput/wait receiver, pending spawn or failed call therefore establishes a new child relationship/read-child eligibility from address alone.

Warrant: ROLE CR-5/SQ-4 learns a child from a completed spawnAgent receiver list; NPTD SQ-8 says spawn call→node at completion. Its broad DS-1 update row does not adopt a different creation proof or erase that condition. Manager confirms existing condition governs this repair; no new human decision or scope narrowing is needed.

Repair: new collab-derived child knowledge requires completed spawn with actual parent/receiver provenance. Other calls may update/reference an already known child but cannot invent a new parent-child relation. Keep all raw native call fields; explicitly sourced subAgentActivity inference remains distinct. Check sendInput/wait/pending/failed unknown receivers are not admitted, completed spawn is, and metadata/parent discrepancies do not silently rebind known provenance or assign App role. This finding is source-confirmed; no additional test execution or actual child was performed by this reviewer.

## Independent evidence and test-corpus assessment

With manager-granted serialized slot, created a unique scratch Cargo package containing **byte-identical original module/test/schema** and three independent public-API regressions. Source was not edited/reimplemented. Approved isolated CARGO_HOME; scratch lock resolved offline, exact jsonschema0.58.5. `cargo test --offline --locked --test native_history independent_ -- --nocapture`: successful9.42s compile, 0.21s run; **3/3 negative assertions fail**, exit101; original eight tests filtered. Positive initial resume/error controls passed inside those cases. No real query or transport dispatch occurred. Slot immediately released. Scratch inputs/failures are preserved in this report; the machine-local copied-source tree is retained temporarily for the commissioned same-case backcheck, then removed. It contains invented fixtures/schema/source only.

Author's8/8 remains evidence of its identified cases, not of these uncovered combinations. Those tests correctly check full tuple/epoch/factory refusal, immutable query params, atomic schema/identity rejection, exact native cursor values/directions, nullable availability and basic read-only/Continue standing. They do not check accepted old resume versus a newer query/read or reconcile errors between independent streams. Existing spawn fixture is completed spawn only, so it cannot establish the broad collab receiver rule.

Source check confirms schemas are complete native local Draft7 definitions with offline retrieval and no rewriting. Actual0.160 list/turn/item backwardsCursor descriptions support reversing sortDirection; next/backwards values remain opaque and stream/direction checked. Goal absent/null/value distinctions, summary/notLoaded/inProgress fields and native extras are preserved, not interpreted as absence. Relational IDs are checked before view mutation. Epoch/latest pending revision and private factory nonce correctly reject older selection, superseded pending callback, foreign factory and full session/home/counter/scalar mismatch.

## Supported seams and remaining production

Query creation is not dispatch or a person's reserved act. Source home/full generation must still be bound to the actual current ready Host by the future dispatcher, with actual RPC ID/reference kept separately. Private HistoryQuery fields are immutable and not deserialized from renderer assertions. This module never inserts an active Host register row; snapshot activeBindingPerformed=false is accurate.

Explicit Continue emits exactly threadId; no role/base/config/model/provider/policy/history/path overrides. Native agentRole, current configuration, instruction paths, fork relation or a record's existence do not establish original App role. That unknown remains correctly labelled until original request-bound trusted RoleBindings evidence is supplied; provider/guidance/base behavior still needs actual candidate witnesses.

Transient page/metadata views are not durable transcript storage. Closing generation clears selection/index/pages and rejects callbacks; checklist updates are explicitly unrecoverable from supplier history. Child/parent status is not return, review or integration. Raw history with active status is not live App custody. These preserved boundaries do not close the three stale/error/provenance defects above.

After a sealed repair, recheck these exact combinations and any changed schema/receiving outputs, then release the bounded seam for actual selected-home list→metadata/turn/item/goal/child→explicit Continue integration. Actual stock history/resume, cold relaunch/same-home recovery, role source persistence/lifetime, native UI, provider/supplier qualification and other production remain their existing owners' work. No blanket readiness or new acceptance ceremony is created.

Reading origins: retained Root/TASK/LOOP/skill/manual; actual new module/test/record; maintained generated0.160 schema; RECOVERY §3.2/CV/history reads, NPTD RV-4/SQ-1/SQ-4/SQ-8/child sequence and ROLE §5.3 CR-5/continuation/SQ-4. No other role instruction activated, product/Design/shared artifact changes or model-diversity claim.
