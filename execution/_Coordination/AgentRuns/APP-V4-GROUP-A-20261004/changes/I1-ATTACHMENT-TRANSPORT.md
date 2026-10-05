# I1 attachment durability and scoped transport — 2026-10-05

TASK `/root/group_a_execution/runtime_core_production`, parent `/root/group_a_execution`; no delegation. Released owning allocation CC-H-ATTACHMENT-PERSISTENCE-ALLOCATION (NIR/REC concurrence), reviewed producer77791e9 and HOSTING0.10/NIR0.4. Original parent candidate95a4/PR1087 remains historical; this successor lives on the parent-managed attachment transport branch. Author writes only hosting.rs, new attachment_custody.rs, exact canonical hosting schema/manifest, tests/attachment_transport.rs and this record. No lib/App/runtime_session/producer/records/storage/Design/Git or dependency edits. No stock/model/auth/credentials/network/download execution; actual env-cleared /bin/cat fixtures are own-code and reaped.

## Frozen interface and physical sources

One canonical module: `hosting::attachment_custody` declared as hosting.rs sibling module; no crate-root duplicate or lib export. `AttachmentCustody::open(&Path app_data,&Path codex_home)` validates explicit absolute nontraversing root, canonical separation and symlink redirection, then establishes runtime directory with existing storage durability primitives. There is no memory/project/RS/Codex fallback. Shared integrating native host supplies the App path; renderer strings do not mint a source owner/picker capability.

```rust
Host::prepare_attachment_turn(Arc<AttachmentCustody>, &Value generation,
    &str thread, Option<&str> expected_turn, &str text,
    &[SelectedTextAttachment]) -> Result<PreparedAttachmentDispatch,String>
Host::dispatch_attachment_turn(&PreparedAttachmentDispatch) -> Result<SourceRequest,String>
Host::attachment_wait(&SourceRequest,Duration) -> Result<Value,String>
Host::persist_attachment_observation(&SourceRequest) -> Result<Value,String>
Host::resolve_attachment_submission(&Arc<AttachmentCustody>, &str submission_ref) -> Value
```

PreparedAttachmentDispatch has no Clone/Deserialize. Accessors submission_ref/source/supply_records/state; cancel() returns true only before commit (prepared/validating). Its private source receipt uses the actual reserved never-reused RPC and existing genuine SourceRequest evidence/wait/status. Cancellation/refusal/attempt makes this packet one-shot. Explicit later send prepares a NEW token; no retry on wait/view/relaunch. Empty ordinary text permits attachment-only input; otherwise exact person text is first, followed by exact producer inputs in original order. Method is turn/start or turn/steer with required observed expectedTurnId; no role/base/config/model/provider/policy/approval/sandbox override or fallback start.

Actual create-once owning NIR array is `<App-data>/runtime/nir/attachment-supplies/<submissionhash>.json`; actual existing0.10 client object is `<App-data>/runtime/hosting/client-requests/<fullGhash>/<typedRPChash>.json`. NIR members retain unchanged0.2 canonical fields/values. Array stores no wrapper/new kind, file body or native input. Client uses original full H5/RPC/method/initiator/pointer-only submissionAssociation and permitted outcome/write/send/wait/receipt/error metadata. Typed integer1/string"1" key preimages differ; full tuple generation_ref preserves Unicode and all fields without normalization; fields inside records remain authority. No RS/REC kind, transcript/base/config/native params/result cache or correlation database is added. Existing hot SourceRequest/native journal evidence remains ephemeral process evidence, never serialized into these sources.

## Actual preparation, dispatch and observation

prepare performs final producer preparation, native params validation and current ready/open full-generation/known-thread/live expected target checks. It captures actual pipe descriptor identity plus source-owner pipe epoch, reserves a real RPC, and records prepared-not-sent/not-attempted WITHOUT sendPosition. Outside Inner it publishes the COMPLETE ordered metadata array then exact client object with file/directory durability; regular-descriptor nonblocking source readback validates all schema fields, unique IDs, ordered refs/same token and exact complete equality with private producer/client values. Partial/file/sync/readback/conflict failure returns no send, retaining available facts and consuming its RPC.

Dispatch revalidates original selected source bytes through the reviewed producer, discarding fresh revalidation IDs rather than rewriting original records; mismatched input/source holds. It retains the existing owning flock through final exact readback and pipe commit. Lock order is source ownership → attachment dispatch gate → Inner → source pipe. Disk IO occurs outside Inner. Final gate checks cancellation/full tuple/current ready/open known thread/live target and actual pipe identity/epoch. Only an actual attempt increments sendPosition and installs pending/write account. Source pipe retained while Inner is released for write; pipe and owning lock are released before state update/durable observation. Deliberate stop and source spawn/replacement honor the gate; source EOF closes under the gate. No broad generic sender rewrite; original text/history/steering/interrupt/request/ledger behavior remains covered by affected tests. An unexpected write/OS failure is uncertain, not retrospective cancellation/rollback.

Actual write confirmation sets sentFrame; broken pipe stays write-failed/unknown. Outcome metadata is atomically replaced in the SAME owning client record, with original identity/association immutable and stale unsettled state unable to overwrite settled state. Correlated native on_line journals raw source first, then releases Inner before persisting attachment metadata. attachment_wait persists actual wait/result observation; postwrite metadata failure becomes a visible hot custody limit, never no-send or resend. File reads reject FIFO/special descriptors after nonblocking open on Unix and reject malformed/unreadable/partial sources. Metadata read bound is a visible64MiB storage limit, not partial-list acceptance or supplier context qualification.

Error projection retains only actual validated integer code and fixed `[attachment custody: native error text withheld; original source may be unavailable]`; error.data is absent. Storage boundary rejects nonredacted error message/data even when canonical schema alone would accept them. Missing/malformed code/message/envelope yields unknown cause, never invented0 or definite native error. Raw delivered native error/result remains unchanged in hot evidence. Client schema copied byte-exact with provenance manifest; no retrieval or schema shape change.

## Hot versus cold resolver

Resolver reads the owning source schemas/typed path keys and exact association/order/token. Hot source additionally requires SAME private root-owner Arc plus genuine Host generation/RPC/original association/list binding and actual successful owning write. Only its first correlated response envelope (no method/error, exact RPC, full native result schema) can establish native turn: start result.turn.id with original thread context and refusal of reported contradictory thread; steer result.turnId must equal original expectedTurnId. Missing/null/malformed/error/foreign/repeated/target conflict stays unknown with cause. Repeated native reply remains uncorrelated raw journal and cannot replace first source. No latest-turn/text/thread-only/counter inference; separate tokens can refer to one observed native turn without merging NIR identities.

Cold resolver labels all disk outcome claims UNVERIFIED App metadata and returns nativeTurnRef:null/no private receipt/no active admission. Prepared-only can have been written before a crash; written/result/receipt position alone cannot restore native proof. Root-owner reopening does not import the old hot capability. Unavailable/corrupt/conflicting metadata returns explicit limits and no fallback/retry. Actual hot evidence is still retained when later metadata publication fails; if owning resolver source itself is unavailable its join remains unknown rather than manufactured. Retention/deletion, arbitrary-filesystem deadlines, non-Unix open qualification, native picker origin/UI/source dispatch, named/image carrier and actual supplier/provider witnesses remain separate obligations.

## Actual checks and failures

Manager-exclusive Cargo slot; approved CARGO_HOME=/tmp/chirality-app-v4-group-a-cargo-home, cwd app/src-tauri, offline/locked. Initial `--lib attachment_host_` compile exited101: Vec<Value> compared directly with JSON Value in resolver. Repaired comparison to typed as_array, removed unused File import; no criterion relaxed. No runtime test failure.

First repaired source passed five Host tests and four custody tests. Source was then tightened to retain owning lock through final readback/pipe, exercise real replacement cat pipe rather than epoch-only mutation, preserve two submissions resolving one native turn distinctly, and reject raw error message/data at the public storage boundary. Final exact source results:

| Command | Actual result |
| --- | --- |
| `cargo test --offline --locked --lib attachment_host_` | exit0;5 passed,0 failed;1.63s compile,1.32s run |
| `cargo test --offline --locked --test attachment_transport` | exit0;4 passed,0 failed;3.95s compile,0.21s run |
| `cargo test --offline --locked --lib hosting::` | exit0;36 passed,0 failed;1.29s run |

Actual disk/cat checks cover complete immutable ordered array/client before outbound, reserved RPC/no sendPosition, exact ordinary+attachment input/order/hashes/no metadata wire field, timeout+hot late response+cold owner/no retry, two independent submissions to one native turn, actual partial publication and directory sync failure with zero cat bytes, cancellation/real content drift/full session/home/counter/actual pipe replacement/terminal steer target/corrupt metadata with zero cat bytes, real broken pipe, later client source failure with raw outcome retained, exact steer target mismatch/native errors/redaction/missing code/null/repeated reply, typedRPC/path mismatch/cold limits/immutable source/root rejection and actual FIFO descriptor refusal. FIFO test directly exercises selected Unix nonblocking regular-descriptor code; no hard-deadline/general filesystem or non-Unix claim. Previous31 Host controls remain unchanged and pass. New module/test formatted in own fence; source-only rustfmt parser check does not rewrite old Host formatting.

Cargo RELEASED after these results. Source/API frozen for independent review before actual native picker/shared send consumption. Shared owner must create the explicit owner from validated App data, retain private selections/prepared packet, route explicit person send/cancel, consume genuine SourceRequest via attachment_wait and expose resolver uncertainty. Do not export a separate root module with duplicate types, supply a renderer path factory, turn the cold reader into an active binder or cache payloads to fill evidence gaps. No status-only pipeline qualification claimed.

## Frozen source seals

| Subject | SHA-256 |
| --- | --- |
| `app/src-tauri/src/hosting.rs` | `262b241ec324e19442d0b3a9f06ec34014663e2f12a5e96962e243702f67bb2d` |
| `app/src-tauri/src/attachment_custody.rs` | `d3c244c3a138871e4682219cba3ebf19766d9aaf4ef3969e9ea474c64ab9fc29` |
| `app/src-tauri/tests/attachment_transport.rs` | `3a9c814731ce2f767dcef8a0323cbca236e74a1ed16a8bc1f3343f2377ea0b10` |
| `app/src-tauri/resources/hosting/hosting.client-request-record.schema.json` | `3264b5b31514f1477b48560d232f50edc3c00db5207b97557a0d4e7e0b9fa5a5` |
| `app/src-tauri/resources/hosting/manifest.json` | `b025c3d783b99266ba2826c4a03a1b5fddf8b495f34eb4ddf5c805c024648096` |
| `app/src-tauri/src/attachments.rs` | `77791e9bb62dd994ff7f0fa12a04acb667834ca3d5132f2a3d7284b308ffa0a5` |
| `conversation_transport_tests block` | `05c0e56e44a2e7a406a29a87baaa060915cd637800b550cf030234590ee171db` |

## ATT-T1…5 original-owner successor — 2026-10-05

Original contribution262b/d3c/record4fe7 is NOTREADY, not requalified by its45 earlier passing checks. Independent V2-ATTACHMENT-TRANSPORT.md original report/addendum is currently21e81b027dbc8f8a400c690caacaebdc14706089b63fbfd9802d0a5e17f009e1: ATT-T1 stale EOF can close successor after gate; ATT-T2 owning leaves/lock hardaliases accepted; ATT-T3 wrong allocation codec; ATT-T4 blocked write prevents Stop deadline; ATT-T5 premature public written observation. Original facts/source seals and failed new oracle remain historical. Parent expanded only necessary Host same-source complete-frame/reply/Stop boundaries; no native_requests/schema/actor policy, shared sources or new logical record kind changes.

Software-defect-diagnosis skill actually read at `.agents/skills/software-defect-diagnosis/SKILL.md`, SHA7e423dfd24132c33d3aa8fe6994bf17a1def966c396723f6bd72ac8d2442112b. It guided bounded own-process reproduction; no diagnosis authority was used to expand scope. Owning HOSTING append-only timing/generic/frame clarification and Parent released scoped repair; current allocation packet0c2c3bcc015249114124372f55ffe592b5eaa5b649735f5956ea69c167683e33. No additional human checkpoint inferred.

### Actual blocked-write diagnosis

The exact run before Stop/timing repair used Host68dfa781bc78b8a0bbe8a18954af026b60a3ed9855854d905a64c91cf1085c60, custody02c562fc (earlier EOF/hardalias/codec edits already staged). Writer/Stop clauses still matched original262b; this is NOT a whole262b executable replay. Command: `cargo test --offline --locked --lib attachment_host_nonreader_stop_and_midwrite_status_actual_bounded_watchdog -- --exact hosting::conversation_transport_tests::attachment_host_nonreader_stop_and_midwrite_status_actual_bounded_watchdog`, approved isolated cache/cwd. Compile5.89s; exit101,0pass/1fail,7.03s watchdog.

Owned env-cleared /bin/sleep60 separate group never read stdin; valid4MiB ordinary native text plus actual prepared attachments blocked write. Stop was called, helper had not returned by seven seconds. External supervisor killed/reaped owned helper group and killed owned sleep group from its freshly recorded PID; audit scratch removed. Midwrite facts: canonical client pending/writeResultwritten/sendPosition1 while private source sentFrame absent/write-in-progress. Audit held only pointer/status facts, not source text. Full execution output is in the author tool turn and independently attributed in original review addendum; reviewer did not run this Cargo. Causal chain: writer held lifecycle gate/original stdin across blocking write, so Stop could not reach its close/kill route. Prior source-only lock assessment did not establish liveness.

### Scoped source repairs

EOF captures original child PID, waits/reaps only that captured child, then rechecks FULL generation after source gate and Inner acquisition before any closure/state mutation. Superseded EOF contributes old-generation journal fact only. Deterministic test parks actual on_eof before gate, installs successor/full namespace, actual private pending request through a new cat source and live turn, then releases old observer; successor tuple/state/request/turn remains unchanged across session/home/counter variants.

Owned metadata regular leaf descriptors now require nlink1; lock is custody-local nonblocking/no-follow regular descriptor with nlink1 checked before/after flock. Read-only cold resolver uses existing safe shared lock; no missing-lock creation/fallback. Ordinary directories' link counts are untouched. Actual supply/client/lock hardlink negatives/readback/cold limits and explicitly selected hardlinked user-file positive pass. No new veto on user source/config/home policy. storage.rs unchanged.

Path keys now EXACT allocation compact UTF8 JSON: SHA([session,home,counter] ordered array) and SHA(actual typed RPC scalar), no normalization/global content canonicalization. Independent literal vectors computed separately cover1 versus"1", Unicode full tuple, changed session/counter. Wrong-placement/old codec sources stay conflict/unavailable, not auto-relocated or imported.

A Host complete-frame mutex serializes ALL client/initialized/manual/automatic reply frames. FD dup captures actual source under short gate/Inner/stdin access. Frame waiting and native blocking IO hold none of those lifecycle/state/original-pipe locks. Final after-queue check binds full generation/pipe epoch/descriptor and current conversation/pending reply eligibility; Stop does not acquire frame mutex. Original FD is never looked up again for actual write and dup is dropped after attempt. One-shot remains; queued source drift/native resolution denies reply without sending, origin/answer/secret redaction rules unchanged. Automatic receipt raw frames journal before Inner release/IO; manual reply races are conservative raw/unknown, not an invented acknowledgment. Final postwrite only source-bound old facts, no reopened closed generation/successor mutation.

Canonical attachment row remains explicitly LAST prewrite observation until actual write completion; effective hot SourceRequest/snapshot/resolver separately exposes writeAttemptInProgress/unknown and sentFrame absent. Resolver is readable while blocked: owning metadata lock is released after final validated scope/FD commit, before blocking IO, while full-frame serialization remains. It never reads historical not-attempted as current no-send during an active attempt or after failure. Success→written only at completion, pending only if still open/no first reply; failure→failed/unknown only when no admitted matching reply. Known reply plus failed write stays combined private facts, canonical current projection unavailable/last observation; raw reply never discarded or false no-response invented. Actual pressure case injects a synthetic matching source reply during the genuine blocked IO, then actual Stop/EPIPE proves combined facts retained with no native-turn acceptance. This is own-code/source-bound testing, not actual supplier qualification.

Generic private full-generation/RPC/method/initiator slot is installed BEFORE pipe, even when no valid canonical prewrite object exists. Canonical generic row is published only at actual completion; SourceRequest/end-wait/fast first reply/raw scope remains available independent of row. Source snapshot exposes reserved/attempt facts and last-observation limits; public client_requests returns actual canonical objects only. Fast matched response is immediately projected after complete write, never overwritten pending; malformed source keeps raw classification+projection unavailable rather than fabricated error code. Failure+known reply combination cannot fit forced v0.10 write-failed→unknown-no-response and is explicitly unprojectable. No new schema/kind/cache/wire field. Deferred turn memo correlation retains its map until actual first response and preserves terminal non-revival; duplicate interrupt recheck excludes its OWN RPC while preventing any other queued/pending duplicate.

Stop pins accepted target fullG/PID across all waits/kill/final accounting, signals captured group, rejects repeated Stop while stopping, consumes only target-generation exit facts and freezes returned state under target accounting lock. Replaced target returns explicit old-source journal/limit, never closes/stops successor. Missing target exit cannot borrow an older generation exit. No interrupt acknowledgment is treated as end/rollback/run acceptance.

### Real run history and final checks

All Cargo uses manager slot/approved cache/offline/locked. Intermediate repair compile exit101 duplicated an already-existing snapshot_inner helper; redundant helper removed, no contract change. First repaired original watchdog passed1/1 in3.77s after3.75s compile. During broad affected checks two runs were explicitly interrupted(exit130) after test-fixture reentrant gate hangs and asynchronous source regressions were exposed. EOF fixture now releases its test-owned gate before real new dispatch and uses a second deterministic rendezvous; Stop fixture asserts original state-only return API plus target lifecycle rather than a nonexistent response generation. No old source oracle was weakened. Source regressions fixed: late turn map removed before reply, queued interrupt duplicate predicate counted its own registered RPC, malformed-envelope private observation hidden behind historical pending. Isolated mixed-envelope test exited101(pending vs observedresult); source projection now retains raw observation classification with canonical projection-unavailable while original no-admission/error-envelope criterion remains. H5 identity fixture now carries complete canonical required fields/actual RPC rather than an invalid minimal record; identical foreign session/home/counter denial oracle retained.

| Final command | Actual result |
| --- | --- |
| `cargo test --offline --locked --lib attachment_host_` | exit0;10 passed,0failed,1ignored helper;1.60s compile,7.46s tests |
| `cargo test --offline --locked --test attachment_transport` | exit0;6 passed,0failed;6.70s compile,0.28s tests; module unchanged after this run |
| `cargo test --offline --locked --lib hosting::` | exit0;41 passed,0failed,1ignored helper;1.18s compile,7.48s tests |

Ignored helper is invoked explicitly by real watchdog supervisor twice (plain blocked write and combined reply/failure), not counted as a passive qualification check. Actual >PIPEBUF ordinary client/manual large error/automatic required error frames parse as three whole independent native lines through cat, no interleaving. Queued replies after source close/resolution send zero bytes. Original durability/failure/cold/one-shot and all previous31 Host controls remain and pass. No new tests beyond changed source/reply/frame/Stop/known warrants. Cargo RELEASED; source frozen for same-reviewer backcheck and shared affected checks.

App project association, native thread.cwd/projectId, Codex home and WR run are distinct. This Core path binds native generation/thread and explicit App-data source, never derives App project/run from cwd. Existing canonical shapes have no invented project/run fields; accepted explicit conversation_index/project join and WR-owned prefix interface require their own actual consuming seam. Current ordinary text+ordered attachment path has NO TC2 run prefix support claim, no blanket hold from an unrelated parser. Picker/shared receiver and actual native/provider qualification remain open as above.

| Successor source | SHA-256 |
| --- | --- |
| `hosting.rs` | `a8f4595647ec992594adf40a30b6e3e374af100f8b57084ae5f76d30be557618` |
| `attachment_custody.rs` | `02c562fcf2bc6d7805052fdb387e454516de1a5f4d280f0e3d2b56cab235eaf8` |
| `tests/attachment_transport.rs` | `99df63749a5c310685221800c4b94b3610b6cb7e37ae71d034e8ddf3b434f9be` |
| `conversation_transport_tests block` | `290bccf3aed436201d59b0dfab478b337ae92cc80fc761dc6ede23a7d1815cbd` |
| `canonical client schema (unchanged)` | `3264b5b31514f1477b48560d232f50edc3c00db5207b97557a0d4e7e0b9fa5a5` |
| `producer (unchanged)` | `77791e9bb62dd994ff7f0fa12a04acb667834ca3d5132f2a3d7284b308ffa0a5` |

### Residual R3 no-attempt successor

Same-reviewer backcheck of a8f459 identified an exact residual: generic Err from capture/check_bound/no-longer-pending before attempt_position was set still recorded write-failed. a8f/record1f584 therefore remained NOTREADY; previous41pass did not establish that R3 fixed. Parent released only this residual while shared52 checks/source reservation had finished. No original report overwritten or actual original-version replay claimed.

The generic Err path now differentiates the actual pipe-commit attempt_position. None means private allocated fullG/RPC/ref remains with explicit noAttemptCause and no canonical generic failure/prepared/null-ref fabrication; pending and turn-frame mapping cleaned, first matching raw reply retained, sendPosition remains0. SourceRequest/status exposes actualWriteAttemptObserved false/current projection unavailable, and waiting returns explicit before-actual-attempt refusal rather than misleading write failure/waiting. Some position still means actual attempted IO: genuine EPIPE/failure projection unchanged, including combined observed reply/private unavailable projection rule. No schema/kind/policy/actor changes.

Actual queued thread/read fixture holds real frame mutex, obtains real private receipt through source_request BEFORE pipe, then closes/replaces fullG before releasing queue; actual cat receives zero bytes. Both no-reply and matching-raw-reply-before-close controls retain same allocated reference, explicit cause and raw first reply; no failed canonical row or fake attachment prepared/null identity appears. Existing write-failure tests previously used absent stdin (now correctly no attempt); their fixtures now use an actual killed/reaped cat pipe, causing a real IO attempt/EPIPE while retaining the identical write-failed/unknown/native-nonadmission assertions. This strengthens actual failure warrant rather than weakening oracle. One first affected run exited101(41pass/1fail) because the history failure fixture still had absent stdin; updated that same fixture to actual broken pipe and reran all affected tests.

| Command | Actual result |
| --- | --- |
| `cargo test --offline --locked --lib attachment_host_queued_generic_noattempt_retains_real_source_without_failed_projection` | exit0;1passed;5.94s compile,0.02s test |
| First `cargo test --offline --locked --lib hosting::` | exit101;41pass/1fail/1ignored;history failure fixture expected write-failed from no pipe |
| Final `cargo test --offline --locked --lib hosting::` | exit0;42pass/0fail/1ignored helper;1.43s compile,7.56s tests |

Custody02c562fc and six public source tests99df637 are unchanged from their passing checks. Same approved cache/offline/locked/cwd. No native/model/auth/network/Git/shared source action. Cargo RELEASED; source/API immediately frozen for same-reviewer residual backcheck. Prior actual failures/interruptions and five source findings remain above; no broad extra tests or status-only readiness substituted.

Frozen Host SHA `26c3cf979c5cc69db8433571e34cb1e12af8d8d3edfe472cd0b955ae855fa8dd`; conversation testblock `9039e5b4200acadae4111923fa9ffe9db0ca863724d30d28eef54cbc121028b0`.

### Private-slot wait-fact successor

Reviewer independently passed no-attempt/EPIPE2 checks at26c3 but found another source residual: SourceRequest.evidence read waitingEnded only from canonical row while generic Null slot's real timeout fact was stored in observation_base. Original26c/R2 therefore remained NOTREADY despite its42 author tests/2 reviewer checks; no whole original executable repro claimed for this source-found wait bug. Parent released only Host/record and exact actual private wait regression after source reservation.

Effective waitingEnded now falls back to observation_base when canonical field is absent. Reserved snapshot exposes that same actual fact. No missing-row false-wait/reset/no-response inference, new canonical state, resend, schema or actor policy. Exact genuine source_request getter under a held frame mutex invokes real10ms source_request_wait before IO/canonical publication, verifies status and reserved snapshot waitingEnded true with no canonical row/actual attempt. Source completion through actual cat retains waiting fact in pending canonical row and after matching late raw reply; source close/replacement before actual IO retains wait fact in private no-attempt source with zero bytes/no canonical row. Original identity/ref/raw response and source generation behavior unchanged.

| Command | Actual result |
| --- | --- |
| `cargo test --offline --locked --lib attachment_host_private_wait_fact_visible_before_canonical_completion_and_close` | exit0;1passed;2.92s compile,0.05s test |
| `cargo test --offline --locked --lib hosting::` | exit0;43passed,0failed,1ignored actual-supervised probe helper;7.53s test |

No failed run or oracle change on this successor. Same approved isolated cache/offline/locked/cwd; Cargo RELEASED. No shared/module/schema/dependency/Git/native/model/auth changes. Custody02c/test99 unchanged from actual six passing source checks. Source immediately frozen for same-reviewer wait residual backcheck; prior findings/failures remain historical above.

Frozen Host SHA `5a5261bdf8973284712d12fb68241d2c484b6faa8012b0aa3d52d4f70415840e`; conversation testblock `a53c53395370c37a98dfd7894a721116e00c85af088077edf0e5c41f3284ce0c`.
