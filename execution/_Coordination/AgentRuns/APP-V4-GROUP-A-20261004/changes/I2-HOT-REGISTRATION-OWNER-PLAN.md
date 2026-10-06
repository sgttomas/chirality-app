# I2 hot registration owner — private API handshake and transaction plan

2026-10-05. TASK `/root/group_a_execution/workflow_authority_route`, native descendant of WORKING_ITEMS `/root/group_a_execution`, no delegation/historical identity claim. Manager commissioned this next private proposal after preserving independently reviewed development catalog in checkpoint d546a2f316. This task does not inspect/operate Git or infer product acceptance from that parent-supplied checkpoint. No live product/resource/Design/schema/manifest/Cargo/Host/act_control/records/lib/runtime/App writes, native/auth/model/capture/network/seal operation. Sole durable write is this plan. Root/TASK/Loop/manual entry already recorded in I2-SELECTION-AUTHORITY-ROUTE applies; further readings below are section-bounded.

**Return:** a declaration-only private Rust seam and maintained test proposal. They are not compiled implementation, not an executing transaction and not receipt construction. The concrete AAC receipt edge must be supplied by its actual owner before production code can consume it. This is an ordinary owner/interface agreement, not a new human checkpoint.

Private files:

- `/private/tmp/chirality-i2-hot-registration-owner/workflow_library_api.rs`: private session/view/attempt/outcome fields and exact method/receipt signatures. Import `crate::act_control::HotA15Receipt` is intentionally unresolved pending AAC's owner; no fake stub, trait implementation, Bool or fabricated success replaces it.
- `/private/tmp/chirality-i2-hot-registration-owner/workflow_library_test_proposal.md`: eleven groups of concrete authority, freshness, commit, migration and failure checks. No suite execution claimed. These temporary proposal files are local recovery inputs for the next writer, not maintained-runtime dependencies.

## I2 owner session and AAC view

I2's owning library context fixes the actual absolute project/user root, origin and source-root identity once from the host's opened library context. Target paths come from that context: workflow-drafts/name or workflows/name, staging, immutable workflow-revisions/name/revision/name, workflow-registry.jsonl, workflow-unrecorded/name/content key. AAC act log/captures use **RS §13.7's accepted portable library allocation**, `storage::library_log(root)` → `.chirality/records/acts.jsonl` and `.chirality/captures/`. Do not reuse A16's current skeleton LOG for A15 or accept a renderer-selected output path. The future host binding is a needed receiving edge, not an implicit capability in a pathname.

`LibraryOwner::review_draft(name, observed_list_revision)` reads the contained real path, captures Snapshot, rereads live bytes, checks list/snapshot/live equality and hygiene/name, observes actual slot state, and retrieves App-kept base/lineage. It privately builds ReviewSession around Review; it accepts no caller Review/Snapshot/tuple/prior/base/descriptor as authority. Existing Review public mutable fields/descriptor remain data-facing and are not passed directly as AAC admission. Read App-kept draft-base/source records as actual observed source facts with their provenance limits; a derived_from tuple in draft files or a renderer DTO cannot create an App-kept base. Existing metadata may be disclosed and frozen without proof of an earlier native A15, while it cannot mint the earlier trusted RegisteredRevision/Selection. Preserve SP-3 lineage through round trips, not merely the current Review::open same-slot shortcut; the base and prior are different facts and stale-base review shows both.

`LibraryOwner::review_in_place(ordered_names)` observes only LS-2 entries genuinely lacking a registration record. A single entry uses the single registration route (DS-7); multiple entries use WR ME-1…5, one a15_multi_descriptor, in the original chosen order, prior none. Several separate drafts remain separate acts. Same-name known bundled development equality retains its distinct candidate standing rather than pretending an A15 occurred. Incomplete registration evidence remains LS-4/unknown, not silently reclassified as LS-2; WR LS-4 itself offers Review to register. A complete readable current ledger/slot claim can be shown/frozen as disclosed prior evidence for a NEW A15 even where its prior native custody is unknown. No accepted WR/RS/AAC clause was found requiring native-authenticated prior/base facts merely to present that new review. Any draft with an unrecorded same-name copy must match that copy for DS-7; otherwise K-6 name refusal stands.

`ReviewSession::current(&self)` rereads every live entry and actual slot/latest and returns a borrowed CurrentReviewView only if the whole descriptor is current. That view has private fields, no constructor/serde/Clone, and methods for actual review/descriptor IDs, owning library/act-log and ordered binding facts. Its descriptor JSON is presentation data. AAC may copy bound facts into an offer it owns, but callers cannot construct a view from those facts. Withdrawal/stale current() refuses; caller references cannot resurrect a withdrawn session. The production owner must retain sessions behind its own state, not a webview-selected serialized session.

AAC first composes from CurrentReviewView, presents its own native surface and freezes context/offer/ordered bindings. After the native event it reacquires/rechecks a current borrowed owner view before capture (AAC §4.2 steps4–5/AX-06). Changed live content or withdrawn descriptor/slot makes the whole offer stale, captures none, including multi-entry. No source-label enum or caller JSON says that a native event occurred.

## Concrete hot receipt contract requested from AAC

AAC supplies `HotA15Receipt` with private fields, no Clone/serde/public constructor/file loader or implementable receipt trait. It originates ONLY in the actual host-native A15 handler after original capture evidence and a durable matching A15 RS record. Pending capture/write is a distinct return, never this receipt. In-process recovery may mint/deliver the same original result after durable writing while custody survives; cold file loading cannot mint it.

Read-only getters required: review_ref; descriptor_id and descriptor_kind; library_root and act_log; record_id and capture_id; ordered_bindings. Each ordered binding exposes exact full subject tuple, content method/value, reviewed ID-3 plus content, and prior tuple/null. Required equality is entry count/order/full tuple/method/content/prior/review/descriptor/owning context, not just hash. Single persisted RS relations are reviewedDraft/priorRevision; multi persisted relations are registeredEntries in matching boundSubject/boundContent order. Map WD/WR snake_case to RS camelCase one-to-one. Derived-from remains in the tuple, not invented as an A15 relation. AAC retains its actual source/record/capture witness; getter equality is necessary consistency, not the origin warrant itself.

`ReviewSession::begin_hot_registration(self, receipt: HotA15Receipt)` consumes both move-only values into HotRegistrationAttempt only after G0 matching all entries/context. Rejection does not make a reusable receipt: report the captured act's no-effect outcome and retain the original act. The attempt owns the original receipt/session and progress; `advance(&mut self)` can only finish that attempt. No standalone DTO grants registration. Internal callbacks may retain attempt state across a temporary I2 receiving failure; cold reconstruction is held under SEAL-2. AAC must ensure one native act does not issue two consumable effect receipts.

## G0–G6 effects, locking and durability

- **G0:** bind actual AAC receipt to this exact frozen session/snapshot/entries/target/prior. Native live freshness was checked immediately before capture. **Draft mode RB-6:** a later draft edit does not change the frozen reviewed bytes to publish after slot recheck. **In-place mode ME-5:** the actual entry must still equal the bound bytes and still be unregistered at publication; changed entry is terminal NotCompleted, while the original A15 and unaffected entries stand. Do not generalize the draft exception to in-place entries. Never substitute newly read bytes. This is the precise reading of the manager's live/slot recheck requirement against AAC step4 and WR RB-6/G1.
- **G1:** acquire the library ledger/registration lock before reading latest, reserve/check each slot and keep serialization through G4. Another completed registration/empty→filled change refuses that entry with a not-completed outcome citing the original A15. A caller prior or a cached earlier lookup cannot pass this check. External agent writes are still possible under Codex permissions, so reobserve actual guarded files at the use points and keep limits truthful.
- **G2/G3:** create-if-absent revision reservation in the existing portable store, copy frozen regular files, fsync file/directory publication and recompute complete bytes/method. Existing exact content is idempotent only for the same attempt's actual receipt and intended transaction; a directory alone does not establish registration. Extra/missing/changed/nonregular bytes conflict. On failed verification remove only this attempt's uncommitted reservation; preserve existing content and all prior revisions.
- **G4:** append canonical WR library_entry under exclusive ledger lock. Validate against unchanged WR schema before write; use library ledger_seq and per-slot sequence, full tuple, prior, actual reviewed_draft or reviewed_entry, exact NEW hot act record/capture refs, store_path, written_at and evidence_limits. Durable ledger append is the commit point. Private RegisteredRevision construction is after durable matching G4 AND verified original store bytes/actual hot A15. Keep receipt-derived act_ref in the constructed value. A partial write/fsync uncertainty yields typed Pending/CommitUncertain, never a selectable success. Retain intended line and reread under the same hot attempt; if exact already-appended line and publication durability can be established, finish it without duplicate append. Unreadable/conflicting tail stays pending. This requires an I2-owned WR ledger append helper, not RS `human_act` append with an invented record kind or a new generic store.
- **G5:** stage exact convenience copy, preserve an externally changed/unrecorded copy in workflow-unrecorded before replacement, then rename and sync. Never delete the changed content to force success. Failure after G4 returns Registered plus RepairPending with cause; store-based selection remains available. It never becomes NotCompleted or rolls back committed ledger/store bytes. In-place registration first enforces ME-5 unchanged actual entry; on success it preserves already equal source bytes, leaving the published copy as it is.
- **G6:** report per-entry committed tuple/act/capture or no-effect/pending reason; emit existing draft transition fields and update App-kept base after success. A multi-entry act may have mixed post-capture outcomes; no rollback of already committed entries and no blank success for the batch. Any later retry of failed content requires a new review/act, except finishing the exact interrupted attempt permitted by SQ-X.

Maintain existing WR attempt/staging and outcome semantics; this proposal creates no new manifest/schema/registry/path class. Cold trustworthy restart completion/standing remains unfinished: do not reconstruct a hot attempt, trusted prior RegisteredRevision/Selection or original native receipt from caller/disk claims alone. Distinguish those authority values from observed prior/base/slot claims: schema-readable ledger and App-kept base records may be disclosed, frozen and checked under lock for a NEW genuine native A15. Their equality is freshness evidence, not replay proof. Unknown prior native custody alone does not veto that new hot effect. A malformed/unreadable/ambiguous ledger can still prevent a reliable prior/latest observation and needs its exact cause, not a SEAL-based blanket hold. Claim readability and unknown custody stay separately visible. Receipt provenance is not persisted trust by serialization. The same-process owner preserves new committed revisions/custody and observed bases. Selecting an older revision or replaying an old act still requires its source warrant; merely freezing that older tuple as an explicitly disclosed prior/base for a new act does not promote it.

## Review/receiving route and decision boundary

Manager sends this exact seam to AAC owner for its private concrete type/result fit. The sole shared receiver later owns host library context, session lookup/native command dispatch and user-facing review/transitions; those files are outside this task. I2 owns contained library review/session/store/WR-ledger and RegisteredRevision construction. AAC owns native event/offer/current-view checks, durable A15/capture provenance and move-only receipt. RS owns accepted record/capture format/writer semantics. Development catalog remains separate and unchanged. Freeze actual implementations before independent API/transaction review and affected offline tests; real native evidence follows its existing point-specific grant.

No new human-reserved architectural choice was found for this ordinary hot route. Existing exact owner decision K-8 governs product operation: registration is through the person's act control bound to the reviewed bytes; this is the eventual native product event, not a request for the human to approve this implementation plan. Owner's explicit “Keep SEAL-2 deferred; continue other work” remains binding on cold seal work. If concrete implementation would change a Design/schema or cross-group order, return that named issue rather than guessing a contract expansion.

## Relied-on pins

| Source (selective sections) | SHA-256 |
|---|---|
| `projects/chirality-app-v4/execution/PKG-02_Workflow and role portability/1_Working/DEL-02-02_Workflow-making workspace and registration/Design/WORKSPACE_AND_REGISTRATION.md` | `bd61f48ca97eba9c7665b31ff7506672f18152d57a20b0ffd361a168750af989` |
| `projects/chirality-app-v4/execution/PKG-01_Native App and third-party harness integration/1_Working/DEL-01-04_Native requests, outcomes and attachments/Design/APP_ACT_CONTROL.md` | `098875a39b33543adc8ac1d860840e7e841062ea513cbd60a601ca237ceb721b` |
| `projects/chirality-app-v4/execution/PKG-04_Human acts, autonomy and run evidence/1_Working/DEL-04-03_Content-bound decisions and compact run records/Design/RECORD_SEMANTICS.md` | `15266b5078ad1878dae20dc1fa2ef93723d187ce18d5fe780bd1af75c00d5f41` |
| `projects/chirality-app-v4/app/src-tauri/src/workflow_workspace.rs` | `15aefc71343ad5aa446b919f567f017fdf1d1477201f75b32d2b4e5c0993ffa5` |
| `projects/chirality-app-v4/app/src-tauri/src/storage.rs` | `ae8439c47b86a3225bf46e893bfa1159a2189d0cc8579692d468a78ea9267d77` |
| `projects/chirality-app-v4/app/src-tauri/src/records.rs` | `cc61f735ab8dfa987081b5f50d37bd0a8b93c340c80cc5bd72266a307c588fea` |
| `projects/chirality-app-v4/app/src-tauri/resources/workflow_role/workspace-registration.schema.json` | `cfd6d3e252b72247d8e1ad0ced3b43b119c5785935002d493407757bd57066e9` |
| `projects/chirality-app-v4/execution/PKG-02_Workflow and role portability/1_Working/DEL-02-02_Workflow-making workspace and registration/Design/prototype/wrproto.py` | `303474582a5192909b7f60e0108009d47efe77fd0477f1ec3c88f00b80fd9c62` |

| Private proposed output | SHA-256 |
|---|---|
| `/private/tmp/chirality-i2-hot-registration-owner/workflow_library_test_proposal.md` | `67504a6b6fa4065b7516f86f279b70e6b3bec71e194758523c749cf29fc5a060` |
| `/private/tmp/chirality-i2-hot-registration-owner/workflow_library_api.rs` | `914933fd69fec2d257bfc8b6cd26f4a2cadc87433e5c3e263eae4540c4ca653e` |

## Parent caution adopted — prior facts versus prior authority

The parent explicitly directed against extending the cold seal limitation to
ordinary current-slot review. **Source disposition:** WR RB-2 shows prior/base
and differences; RB-3/G1 compare actual latest; LS-1 requires ledger+A15+bytes
for runnable standing; LS-4 offers Review to register; AAC §4.2/RS HA-10 require
native capture for the NEW A15. None of these states that displayed/frozen prior
or App-kept base facts need a native-authenticated historical act first.
Accordingly the private SlotBinding now admits ObservedLatest with retained
ledger observation/evidence limits, alongside same-process HotRegistered.
It cannot construct the older registered/selection capability. New genuine
hot A15 and G4 registration remain viable on disclosed observed slot facts.
A draft-file base claim still does not establish an App-kept base (WR SP-3);
loss/ambiguity of that actual source remains its specific disposition cause.
No prior JSON, metadata label or new act rewrites history to say the old native
act occurred. This correction narrows an overbroad inference in the first plan;
it does not change WR/RS/AAC, cold replay obligations or the accepted catalog.

## Supplied AAC seam concurrence — concrete placement and borrowed getters

Read actual AAC plan b0cfa39cd7a04ce4c9ec63b8c2eefbf1405899539c4e6d764dd0e51b1653af10,
receipt API da34c687b90ce706c6c06b07ff87e023d3274e1ff8e65fed3e58b1396561bc70,
native capture delta bc9880bbf4a5e2f6d574df7e3c82eb9e6d45f17efd7f8ad3e1349a040b873ac3,
and Root event API0d297639ef761b274637233f0cdecad50339f19a8a9cd1d9273f81017b551056.
Concur their concrete move-only receipt/result, retained witness/once-only
transfer and original-library writer destination. Existing records helper takes
the owner-derived relative log; no records schema change is necessary.

**Selected I2 placement:** maintained `workflow_library.rs`, loaded solely by
`#[path = "workflow_library.rs"] pub(crate) mod registration;` in
workflow_workspace.rs. Thus AAC's `workflow_workspace::registration` import
resolves to the intended owner child and RegisteredRevision construction can
remain private. No declaration installed during this private refinement.

CurrentReviewView exact getter fit is now in the private proposed source:
`descriptor() -> &Value`, `descriptor_kind() -> &'static str`, `review_ref`,
`descriptor_id`, `library_root`, `act_log`, `review_presentation() -> &Value`, and
`ordered_bindings() -> impl ExactSizeIterator<Item=BorrowedReviewBinding<'_>>`.
SingleDraft/SingleInPlace kinds return a15_descriptor; MultipleInPlace returns
a15_multi_descriptor. BorrowedReviewBinding exposes subject, content_method,
content_value, reviewed_id3, reviewed_content_method, reviewed_content_value,
and prior, exactly matching AAC's A15Binding getters. All derive from private
owned entries and immutable review; neither borrowed view nor binding has a
caller constructor/serde/Clone. AAC copies read-only facts into its own offer,
without treating JSON equality or iterator values as native provenance.

**RB-2 presentation:** owner-composed display value includes target slot/library,
mode/disposition/message, exact tuple/content/method, complete per-file names,
sizes/digests and WORKFLOW.md; declared-part/hygiene findings; original App-kept
base and prior separately, lineage, stale-base explanation and differences
against each; same-name origins/holding locations/standings; source observation
limits; and the registration-is-availability-not-compatibility sentence. Optional
compatibility report is separately labelled. ME-2 in-place presentation has no
invented draft/base: every ordered entry gets its own snapshot/review package.
Unavailable comparison material is labelled unavailable rather than silently
shown as an empty diff. The frozen presentation is data held by ReviewSession,
not an extra act or a new canonical schema/record type.

**Precise remaining Root fact-access fit:** supplied A15OfferRef has private id
with no getter and confirmation_text returns String, yet ConfirmedA15Event
needs actual frozen offer ID/digest. AAC must expose read-only actual offer ID
and frozen offer digest after composition/freeze (for example offer.id() and
ActControl::a15_offer_digest(&offer)); descriptor_id must not substitute for
AAC's offer ID. These getter facts grant no native authority and cannot replace
the Root lexical native event constructor. Parent routed this narrow issue to
AAC; this plan does not edit another owner's proposed source or invent a Bool.
The concrete Root handler still owns actual review lookup/actor/home/library
rechecks and event construction. No other I2/AAC contract conflict found.

**Mode correction retained:** ME-4 invalidates whole multi offer before capture;
ME-5 evaluates each in-place entry at publication after capture; changed entries
are NotCompleted and their unchanged siblings can register. ME-6 forbids later
completion of finalized failed entries by reusing the same act, even if bytes
are restored. Draft RB-6 still publishes frozen reviewed bytes after a later
draft edit. Private API comments and test proposal now assert both modes. This
source distinction corrects the earlier general statement and changes no Design,
receipt/capture semantics or human gates. No live sources or Cargo executed.

## Actual first implementation and combined checking — 2026-10-05

Manager released actual implementation after private mutual fit; AAC published
its real counterpart, Root published actual same-crate declarations and froze
lib691b1ae1/runtime1fde/App28a83. This owner published workflow_library.rs,
workflow_library_tests.rs and workspace registration child wiring, with no
other-owner or Design/schema/manifest/dependency edits. This section supersedes
the earlier declaration-only status for the implemented first hot unit; the
private proposal remains historical.

Actual LibraryOwner reads contained draft/in-place packages and schema-readable
ledger observations, builds private ReviewSession and owner-held descriptor/RB2
presentation; current()/view.revalidate() check actual live bytes and slot.
Ordered borrowed getters bind AAC's real private receipt, never a DTO. Actual
receipt-consuming attempt locks the existing portable registration ledger,
reserves/verifies/syncs original store bytes, validates/appends canonical WR
library_entry, privately constructs RegisteredRevision after durable G4, and
reports typed per-entry Pending/NotCompleted/Registered+RepairPending. Original
hot intended ledger lines survive write uncertainty in memory and are reread
without duplicate append. G5 preserves externally changed copy bytes before
replacement. G6 updates same-owner App-kept draft-base memory after commit.
RB6 draft-later-edit and ME5 in-place-postcapture-refusal differ explicitly.
New registration does not authenticate a displayed old native act. No cold
receipt/registered-value loader exists.

This first unit has explicit receiving/continuity limits: Root native review/
selection/command state is the next owning consumer; comparison against other
libraries/collision inventory needs that owner's actual known library inputs
(the current presentation labels them not observed rather than inventing empty
coverage); old App-kept base persistence/recovery and trustworthy cold replay
remain unfinished. In-process base updates and ledger/store publication are
implemented; no durable native-trust journal/source promotion is claimed.
Development candidate selection remains its unchanged separate admission path.
No real human native A15, model operation, live run, shipping/acceptance or seal
qualification follows from the synthetic tests below.

**Retained tests routed into actual crate.** Existing workflow-role21,
workflow-receiving6 and workflow-catalog8 were source-included integration tests
for synthetic fixture access. Real crate-private AAC receipt cannot be swapped
for a foreign-crate DTO or hidden by cfg. With sole Root owner concurrence,
original test bodies were preserved verbatim after local source/utility preludes
in src/workflow_role_tests.rs, workflow_receiving_tests.rs and
workflow_catalog_tests.rs. Parent workspace cfgtest modules run them against
actual crate types; old integration target files truthfully document the routing
and contain zero tests. The actual commands below use --lib, never claim 21/6/8
passes for empty integration wrappers. Root added actual workflow_workspace,
workflow_declaration, execution_compatibility and a15_native declarations.

**First outcomes preserved.** Initial --lib --no-run session42581 exit101 had79
compiler diagnostics cascading from this owner's invalid three test-prelude
`use super as workflow_workspace` aliases. An intermediate rerun82810 exit101
repeated that source because the prelude-edit command used wrong cwd and failed;
its raw output is retained. Repair changed only those imports to
`use crate::workflow_workspace`; no criterion/authority API was weakened.
Corrected no-run session13356 exit0 PASS in5.77s with actual Root/I2/AAC types.

Initial workspace selector78578 exit101: retained35 PASS, all new12 FAIL in
fixture setup because std::env::temp_dir() traversed macOS /var symlink and the
unchanged storage guard refused it. Repair only canonicalized the synthetic
fixture parent to its actual real temp location. No production path guard change.
Repaired workspace selector28646 exit0: **47 passed,0 failed,0 ignored**,155
filtered,1.42s. Retained35 and new12 all executed. New tests exercise real owner
reads and the actual AAC synthetic native-event/capture/writer/HotA15Receipt
path: full snapshot freshness, ordered in-place review, original draft bytes,
ME5 terminal failure/sibling success, store conflict, G5 postcommit repair
pending, wrong-review refusal, malformed ledger, uncertain append/idempotence,
actual slot advancement, preserved outside copy and disclosed prior/new hot act.
These are synthetic event witnesses, not a native-human qualification.

Exact commands (app/src-tauri cwd), approved existing cache only:

```sh
CARGO_HOME=/tmp/chirality-app-v4-group-a-cargo-home CARGO_NET_OFFLINE=true CHIRALITY_SKIP_CODEX=1 cargo test --lib --no-run --offline --locked
CARGO_HOME=/tmp/chirality-app-v4-group-a-cargo-home CARGO_NET_OFFLINE=true CHIRALITY_SKIP_CODEX=1 cargo test --offline --locked --lib workflow_workspace::
```

Cargo lane released to manager immediately after47 PASS for AAC's next lane.
Unconsumed receiving/helper warnings remain truthful; no broad cleanup. Actual
source/transaction/ordinary-build authority review is still required before
READY. Manager owns independent commissioning, publication and subsequent
receiving work. No extra human gate is introduced.

### Exact initial tested source association

| Artifact | SHA-256 |
|---|---|
| `projects/chirality-app-v4/app/src-tauri/src/workflow_workspace.rs` | `9fe3ceb4e569208b059dc1a1695f7baa54c8b8919a5a01dd18e2c2f859853f5c` |
| `projects/chirality-app-v4/app/src-tauri/src/workflow_library.rs` | `a84c6c2cec713a2db99ddfe459ab449d2d3291d688f98a0ae721c8e720a88d02` |
| `projects/chirality-app-v4/app/src-tauri/src/workflow_library_tests.rs` | `60add871eb7fd8367dbac62501d64959eb9c492eb196e0984ba8fc3537280ed0` |
| `projects/chirality-app-v4/app/src-tauri/src/workflow_role_tests.rs` | `ceea521a535b71295f08db662311a9f91a7d660e96842a49840abcbb86c8a7f2` |
| `projects/chirality-app-v4/app/src-tauri/src/workflow_receiving_tests.rs` | `28efe9d77132f7770a16624061cf3a9231964e7f077e55186443f43ef1e8939b` |
| `projects/chirality-app-v4/app/src-tauri/src/workflow_catalog_tests.rs` | `f6c2ffd345e484566f41e090ed84d881d92f1e0e6722c38ab50dd2262a3dd556` |
| `projects/chirality-app-v4/app/src-tauri/tests/workflow_role.rs` | `8be606b3b4231d03c9ad1ad540e9ce37aa68dbd9dc541e968a27001d98b27859` |
| `projects/chirality-app-v4/app/src-tauri/tests/workflow_receiving.rs` | `b938c32b833efcc65ae657d3e9b13a73bae38737a49cd7963b22d366beeed78c` |
| `projects/chirality-app-v4/app/src-tauri/tests/workflow_catalog.rs` | `abc1b7dfb011bd1a43c439846033c94e236029f63b09dc51219e00f145270583` |
| `projects/chirality-app-v4/app/src-tauri/src/lib.rs` | `691b1ae102e2d0d804b3f039feb53ca804645795c15e0b3e3a6ec56aba429069` |
| `projects/chirality-app-v4/app/src-tauri/src/act_control.rs` | `32897881a2d7ee4740dd73dcbc3107e60b225df7f028ead3666edf82fa4a82a2` |
| `projects/chirality-app-v4/app/src-tauri/src/act_control_a15.rs` | `f7430bb6f54ecb1f4f18d220d34dbe5e970a621d8a35b70670505764dcc562fe` |
| `projects/chirality-app-v4/app/src-tauri/src/a15_native.rs` | `1f6c4df9b734fd6e6ddd7f43973b3097dc36a4d5346e0676805d24eb1168cfa8` |

Raw outputs remain local recovery evidence (not maintained test dependencies):

- `/private/tmp/chirality-i2-hot-registration-initial-compile.log` SHA-256 `386e3deb0a6f0777a15ec49b0d3c6388c3f67749a93e66b9b8201b8f8ea928d8`.
- `/private/tmp/chirality-i2-hot-registration-repaired-compile.log` SHA-256 `386e3deb0a6f0777a15ec49b0d3c6388c3f67749a93e66b9b8201b8f8ea928d8`.
- `/private/tmp/chirality-i2-hot-registration-corrected-compile.log` SHA-256 `352ac22b18d5a0635999a3a29c290323545841c8f03bfece8bf9684c59d85c7a`.
- `/private/tmp/chirality-i2-hot-registration-initial-tests.log` SHA-256 `0daa0faa70728558ab6b954c9a7e2909f3fa235f8fa9d846e90acb1fd0b2084f`.
- `/private/tmp/chirality-i2-hot-registration-canonical-fixture-tests.log` SHA-256 `4ddb94b169532274d8e10076ee74dde521ec0a9f5f1f099a9a0c1796a8cfba4d`.

Actual repaired result: `test result: ok. 47 passed; 0 failed; 0 ignored; 0 measured; 155 filtered out; finished in 1.42s`.

## HR-1 original defect, repair and actual affected validation

Original independent review V4-I2-HOT-REGISTRATION is **NOT READY** on
librarya84c/workspace9fe3/tests60add/author701. Report SHA-256
bf38f770afca726f9efea990d4a7c3e456321de55f52141ae02ed77602ebd728
and original47 PASS stay historical. Reviewer confirmed source HR-1: fresh
create_dir(store) created a link in store.parent, while sync_package established
only files/store durability. The later ledger parent sync is a different
directory and did not establish this store link before G4. This violates the
G2/G3 durable immutable publication needed before G4 and selectable result.

Manager released this owner's precise source/Cargo window after AAC completed
its affected checks. Published only the new regression against unchanged original
librarya84c first. Existing storage::fail_directory_for_test targets store.parent,
which is created and durably synchronized BEFORE injection, so prior
ensure_directory sync cannot mask the missing post-child-publication sync.
Actual session14312 exit101: **0 passed,1 failed**; injected parent sync failure
still returned Registered+Current. Raw source-specific first failure preserved.

Minimal repair adds sync_dir(store.parent) after sync_package and BEFORE intended
G4 line/ledger append. Registered intended-line retry also reestablishes package
and parent durability before commit completion. No record/schema/guard/native
receipt change. No weakened expected result. Same regression requires Pending,
no G4 record and no Registered while the fault is injected; the original frozen
snapshot store remains; clearing fault completes the SAME retained receipt
attempt and repeated progress still leaves exactly one ledger registration.
Actual focused session1887 exit0: **1 passed,0 failed**,0.53s. Actual full
workflow_workspace selector61137 exit0: **48 passed,0 failed,0 ignored**,156
filtered,1.47s. Original47 controls remain, plus the HR-1 regression. No real
native act, cold replay or qualification is claimed. Cargo lane released to
manager immediately after48 PASS; original reviewer affected backcheck is pending.

Commands, approved offline/locked existing cache only, app/src-tauri cwd:

```sh
CARGO_HOME=/tmp/chirality-app-v4-group-a-cargo-home CARGO_NET_OFFLINE=true CHIRALITY_SKIP_CODEX=1 cargo test --offline --locked --lib hr1_new_store_parent_sync_failure
CARGO_HOME=/tmp/chirality-app-v4-group-a-cargo-home CARGO_NET_OFFLINE=true CHIRALITY_SKIP_CODEX=1 cargo test --offline --locked --lib workflow_workspace::
```

### HR-1 repaired candidate association

| Artifact | SHA-256 |
|---|---|
| `projects/chirality-app-v4/app/src-tauri/src/workflow_library.rs` | `8504e62fc117ca5cde9bbed9b7d172504854eb6d89acc2e78cd2ddb172e08f01` |
| `projects/chirality-app-v4/app/src-tauri/src/workflow_library_tests.rs` | `3f1a29d9bdd664deec13c7e2ade4f56dec388cd14caa87dde26a19701a0db703` |
| `projects/chirality-app-v4/app/src-tauri/src/workflow_workspace.rs` | `9fe3ceb4e569208b059dc1a1695f7baa54c8b8919a5a01dd18e2c2f859853f5c` |

Raw original/repair/affected outputs (local recovery, not maintained-test inputs):

- `/private/tmp/chirality-i2-hr1-original-test.log` SHA-256 `2e024099482c6f41f98ed1b14cb48e066012f5136b58a2e29c25f13c29740bdf`.
- `/private/tmp/chirality-i2-hr1-repaired-test.log` SHA-256 `b1e1a2b157a8cdbd421e0e582f1e073fc555a17c563d788b6bfa42af5bde4f27`.
- `/private/tmp/chirality-i2-hr1-workspace48.log` SHA-256 `8a142dac8828ab37783c6a1fca65da52b18c8f34da4a000b5069d4f454b7f8de`.

## Actual Root list-revision receiving fit — bounded adapter

Parent resumed this owner after actual Root connected tests reached two review
flows that failed DS-6. The actual caller runtime_session.rs::begin_review used
opaque_id("workflow-list:") where review_draft requires the content revision
observed in the workspace list. That is a request reference, not package bytes;
DS-6 correctly refused. This is a receiving source-fit defect, not a reason to
weaken listed/snapshot/live equality or alter the reviewed native/ledger APIs.

Read actual runtime caller and WR D-2/RB-1/SQ-R/DS-6. Root owner concurred the
smallest actual owner-read getter `LibraryOwner::listed_draft_revision(name)`:
validate name, derive contained .chirality/workflow-drafts/name from opened owner
root, storage::check_path, Snapshot::capture and return its existing package
revision. Returned String is comparison data, not a source-authority marker or
review/capture/registration capability. Root holds the same owner mutex, observes
this digest and calls unchanged review_draft(name,&digest). Review still captures
and rereads bytes; edits between listing and review remain DS-6.

Root explicitly released compile/source window for this small owner delta.
Published getter and one new listing/stale/refresh/traversal control; prior G3
parent-directory sync repair is byte-preserved. No Root/Host/Design/schema/manifest/
dependency or AAC edit by this owner. Sole Root receiver owns actual caller
repair and test-native serialization correction; those are not author edits here.
No Cargo invoked by this owner; requested next Root consuming lane include the
focused new control. Prior review READY covers its exact old candidate; affected
source/getter test checking remains pending for this delta, without a human gate.

| Listing-fit output | SHA-256 |
|---|---|
| `projects/chirality-app-v4/app/src-tauri/src/workflow_library.rs` | `633fe20ae46b1842a7d94567a69c3fa999fbc9814c09410a7cd69296d3480c38` |
| `projects/chirality-app-v4/app/src-tauri/src/workflow_library_tests.rs` | `f98380037bc5e33581121349a0da8c23e3a62ee32414b505f23fdd46d3e8fb74` |
