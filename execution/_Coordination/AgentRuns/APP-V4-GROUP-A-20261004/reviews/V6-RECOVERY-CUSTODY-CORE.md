# V6 recovery custody core — independent source review

2026-10-05 original review. **NOT READY for fan-in: three blocking source findings.** No Cargo, compiler, tests, native supplier, network, credentials, Git or source edits performed. This is source readiness review, not a test-pass or final product verdict.

TASK `/root/group_a_execution_astra/recovery_custody_review`, parent `/root/group_a_execution_astra`, delegated-harness-native child, no descendants. Sole write: this report. Applied software-code-review. Inspected private `/tmp/chirality-rec-custody-astra.bo0pfG/app`, patch, manifest, baseline and parser evidence, I1-RECOVERY-CUSTODY-ASTRA/NEXT-ASTRA, actual owning source/queue and selective REC contract/schema. No repository software-workflow profile exists; bounded scope inspected directly from patch. Prior queue, conversation, RT and startup reviews were consulted as scoped historical evidence, not rerun or generalized approval.

## Findings

### RC-1 — blocking P2: known item pointers disappear from durable projection without a turn-start observation

`src-tauri/src/execution_custody.rs:70–73` writes openItems only inside `Some(row.turn)` and filters to that one turn. `item` at 51–59 accepts and retains full native thread/turn/item references independently of any turn-start observation, but never sets row.turn. Therefore an admitted indexed thread receiving item/started(u,i) without an observed turn/started(u), followed by generation close, emits i in live observation_lost.inFlightItems while its successfully written index omits i completely. The queue is empty afterward, so no persistence limit explains the loss; relaunch cannot recover that pointer. The same loss occurs for known open items belonging to another turn than the latest row.turn. This is a deterministic source path, not a claim of having observed a stock supplier reorder.

The assigned source-fit contract explicitly requires started-not-completed references to survive through the actual ledger; the accepted ledger schema permits openItems independently of liveTurn. Retain all warranted item references under a truthful incomplete-turn observation, or explicitly represent the schema's correlation limit rather than silently dropping known facts. Do not infer a live turn or invent native outcome just to fit the reducer. Add actual Host→ledger→reopen controls for item-only and missing/competing turn-observation sequences, with no UI polling.

### RC-2 — blocking P2: legitimate metadata rows are discarded as session/generation mismatches

`src-tauri/src/recovery.rs:975` rejects every conversation_index whose row.session differs from lastLoadedGeneration.appSession. That is not an invariant of the existing owning writer: `hosting.rs:624` appends an attachment-context tag with the CURRENT session and preserves the original index's lastLoadedGeneration and execution fields. This is intentional historical-context preservation. On a new App session, an already indexed conversation may be admitted and receive a durable context tag before another execution observation; bind at execution_custody.rs:32–33 does not set an observation timestamp, so rows skips it at 68. The valid newer tag row is consequently classified as mismatched and omitted from historicalConversations, leaving an older index without that tag (or no row if no earlier usable index is supplied). Its persisted context is still in the ledger, but this new API misstates the selected historical account.

Separate row-append provenance from execution-observation generation. Preserve the latest legitimate metadata/tags/fork account while ranking execution observations with their actual full-generation source; do not rewrite an old observation's generation to today's generation merely to satisfy the new reader. Add a source-connected cross-session existing-index→actual bind_attachment_context→RecoveryCustodyView control. This is an affected owning-writer compatibility defect, not a request to reopen unrelated context logic.

### RC-3 — blocking P2: custody ignores the Host's terminal-event fact

`hosting.rs:1634–1638` sets terminalEventObserved when source is turn/completed, then passes only native status to ExecutionCustody::turn. `execution_custody.rs:35–47` treats any status inProgress as live. A first turn/completed frame for u with status inProgress (or that frame after a prior nonterminal start) therefore leaves Host's operational guard correctly non-live, but marks custody live and fails to install its terminal guard. Subsequent item/started(u,i) is accepted into custody and generation close/reopen can advertise u as live-at-loss/restart. The source already recognizes this contradictory-event class and preserves raw evidence; the custody projection must honor the same terminal fact rather than deriving a stronger live claim. Later active-like notifications may be refused upstream, leaving the wrong custody standing unchanged.

Pass the source terminal marker into the custody reducer or consume the guarded Host state, preserving contradictory native bytes and an explicit limitation. Add an actual Host control where the first terminal event has active-like status, then a late item/start and generation close; neither liveTurns nor restart interruption should revive the terminal tuple. Existing conversation tests cover other prior-terminal contradictions; the six new custody tests use only ordinary completed statuses and do not cover this case.

## Other assessed boundaries and missing verification

The design is otherwise coherent at source level: Host on_line and remember_turn produce pointer observations without renderer polling; close snapshots requests before closing the register; full generation keys and completed-item sets protect ordinary late/foreign receipts; original index cloning retains project/tags/fork fields in normal same-generation execution updates. Immutable values enter the existing captured queue before writer IO, and the prior strong queue lifetime mechanism remains unchanged. RecoveryCustodyView has no public constructor/Deserialize or authority import; snapshot is read-only and does not flush. Missing-index paths do not manufacture project rows. Restart derivation distinguishes missing session end from observed system termination, and refuses to infer quit-with-live-work solely from a clean end. Native history and automatic resume remain separate.

The six authored tests and parser success are source/evidence inspected only. They do not establish compilation, schema execution, concurrent writer behavior or regression passes on this candidate. After repair, retain first failures and run the permitted lane's six expanded custody controls plus affected queue/retirement, context, conversation and recovery checks. Source cases for actual stop cause, clean versus missing session end, unknown/malformed history, fork metadata, and multi-home generation isolation need corresponding evidence. Root consumer is absent by declared division of work; final UI/native-history separation and native quit/relaunch remain Parent-owned. No extra human checkpoint is created by this review.

## Source identity and reading provenance

Private source hashes independently matched the author's seal. Paths below are relative to private app unless repository qualified. Reading provenance is actual consulted origin, not acceptance. Root user-supplied instruction body, TASK, v4 LOOP, skill, manual index/headings and full Field Book were read; Group A graph was consulted selectively for scope, not reconstructed. REC contract reads were selective (CV, ledger/context, custody schema and verification clauses); no other full role body was loaded.

- `/Users/ryan/.codex/worktrees/077c/chirality/AGENTS.md` — `f96feb19d297c74e10048c506805b2fe3622c50cfefd6078f599724556113977`
- `/Users/ryan/.codex/worktrees/077c/chirality/agents/AGENT_TASK.md` — `1a13a5b00b3ce01ff8519efe6b46bcbe0cd6a5b7985e24282fa7efa2c57c8fb7`
- `/Users/ryan/.codex/worktrees/077c/chirality/.agents/skills/software-code-review/SKILL.md` — `ee085d589c44f912d11a59eead8edac214f0343761d26b0d33e886a979888bca`
- `/Users/ryan/.codex/worktrees/077c/chirality/projects/chirality-app-v4/loop/LOOP_INIT.md` — `c2e88f81439ed03578fee13fd7563082fefdfe11096d9134a59531eba3b985bd`
- `/Users/ryan/.codex/worktrees/077c/chirality/docs/alignment-manual/README.md` — `5eee30d902c57a251bf885f91bfa0481a7834ec6945c3382baf15d2e2980c63d`
- `/Users/ryan/.codex/worktrees/077c/chirality/docs/alignment-manual/CHIRALITY_AGENT_USER_MANUAL_v3.md` — `2535efe547f2368e06d965d189efc47c7c46f28c2d6fd4777b0b8cece9003fa7`
- `/Users/ryan/.codex/worktrees/077c/chirality/docs/alignment-manual/Project_Management_for_Human_Agent_Teams_Field_Book_v1.md` — `02d53a3966220001318aacf3f46e1b63b8695a098c81b20f4e3e1531b93024d3`
- `/Users/ryan/.codex/worktrees/077c/chirality/projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-GROUP-A-20261004/changes/I1-RECOVERY-CUSTODY-ASTRA.md` — `9e20b2cea6d25a79821b67deefe03d0035c34251ba5824def31673c3e189c9eb`
- `/Users/ryan/.codex/worktrees/077c/chirality/projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-GROUP-A-20261004/changes/I1-RECOVERY-CUSTODY-NEXT-ASTRA.md` — `073710657bf0ebcc583565a88e876dac30f2506ceca3c7f43c33ecd900043d9c`
- `/tmp/chirality-rec-custody-astra.bo0pfG/app/src-tauri/src/hosting.rs` — `412a6f8b70c5ff6279d65f12c9ae56e63eb39489dc2de64ad19de451e0e13563`
- `/tmp/chirality-rec-custody-astra.bo0pfG/app/src-tauri/src/recovery.rs` — `271fa3d80aac4f010026bc9073e018ca11c74e47493d34e7037d9a5cce9e3429`
- `/tmp/chirality-rec-custody-astra.bo0pfG/app/src-tauri/src/execution_custody.rs` — `a03a27517a804b577ab8f077728c82bfc3cf1f26a295adb9df956bf173f5bf7b`
- `/tmp/chirality-rec-custody-astra.bo0pfG/app/src-tauri/src/execution_custody_tests.rs` — `0586ca2b71af09584fa4cfb04da8e55951953c990f4412e8487d763b1659e7ed`
- `/tmp/chirality-rec-custody-astra.bo0pfG/app/src-tauri/resources/runtime_core/recovery.custody-event.schema.json` — `033398508abc813e90aee0a074a18cb91bd59be88b6991111504ae5662653773`
- `/tmp/chirality-rec-custody-astra.bo0pfG/recovery-custody.patch` — `e59c64fd2c0892b2aea46debfb8b663923ae117538deca5952ed99ff35a921a4`


# V6-R1 — actual independent successor backcheck and cold-correlation source fit

2026-10-05. Same independent TASK and sole report write. **Bounded repairs are verified; whole recovery core remains NOT READY for closure because RC1-COLD is unresolved.** RC2 and RC3 close on this successor. RC1's silent loss of item IDs/types is repaired, but its native item-to-turn association requirement remains open. This is permission to retain a clearly partial contribution, not acceptance of a reduced recovery criterion or a new human gate.

Parent expressly granted direct retained-binary checking without Cargo. No source/schema/Git/Cargo/native supplier/network/auth action occurred. The exact retained binary was executed with 11 custody controls and the single actual cross-session writer control; both returned exit0, **12/12 independent passes**, respectively 3.46s and 0.13s reported test duration. Commands:

```text
/tmp/chirality-rec-custody-astra.bo0pfG/checked-lib-tests execution_custody_tests --test-threads=1
/tmp/chirality-rec-custody-astra.bo0pfG/checked-lib-tests recovery_custody_rc2 --test-threads=1
```

The binary is the author's retained actual build artifact, not an independently rebuilt binary. Its SHA and all five repaired source hashes match repaired-manifest.json. Every listed evidence-log hash matches. Original-vectors RC1, RC2 and RC3 function bodies are byte-identical to the current test bodies; original failure logs contain actual 6-pass/2-fail RC1+RC3 and 0-pass/1-fail RC2 outcomes. Those author executions are retained history, not falsely attributed as reviewer executions. The author's other 27 affected checks were read as evidence and not repeated. No broader/native qualification follows.

| Repaired source / artifact | SHA-256 |
|---|---|
| hosting.rs | `45bd26eb798db9df04a639213de7702bedad4ef89c962d521b146ab92cc2406f` |
| recovery.rs | `47b271401eccc1775ee3137c0b9d4faa31e163356d1ff63d49713b1825842c6f` |
| execution_custody.rs | `457b46849f2bd6aa21c10252799f5998e8936b2a710fca0775dc9a70aaf275fa` |
| execution_custody_tests.rs | `52f2cd75128143393d71f2336ba8d1fd78c1df308ec2e5f31464baf2b4a1e855` |
| exact custody schema resource | `033398508abc813e90aee0a074a18cb91bd59be88b6991111504ae5662653773` |
| checked-lib-tests | `96f0ce63c28ffdb3c8daa3a1f0c64ff07c2ae88cc9535a60f969d71310223c50` |

## Repair assessment

RC1 now writes every retained open item ID/type without the row.turn filter. The original item-only and competing-turn vectors pass, and the reader expressly refuses to infer membership in liveTurn. This is a truthful partial improvement. The passing test asserts presence of an ID, not preservation of its native turn relation; it therefore cannot close the fuller requirement.

RC2 ranks execution by the session/counter carried in the actual lastLoadedGeneration, while metadataIndex separately ranks append provenance. The new reader accepts the legitimate actual context-writer case without retagging historical P as Q or rebinding execution to the current session. Both original rows are offered, not silently spliced into a fabricated ledger row. The actual writer control passes unchanged, and the older-generation ordering control also passes. Root must consume both provenance fields rather than assuming index.session is the execution session.

RC3 passes the source turn/completed marker into the helper. It marks the tuple terminal even for contradictory inProgress content, clears its item pointers, and provides a contradiction limit while preserving raw source. The first-terminal-active-status vector no longer emits liveTurns/inFlightItems or a restart interruption. Existing source/closed-generation boundaries remain intact.

The API remains read-only, without authority import or automatic resume. Queue lifetime and immutable facts are reused unchanged. Additional checked controls exercise actual stop entry/cause versus a clean session end, unavailable history, fork metadata and distinct home references; their synthetic/constructed scope remains explicit.

## RC1-COLD — blocking source-fit gap, not repaired by a disclaimer

The helper retains each open item as `(turnId,itemId) → itemType`. Repaired execution_custody.rs still serializes only itemId/itemType in rows, erasing turnId. Two histories with the same thread/generation and item ID/type but different observed turns can therefore produce identical cold rows. Once the Host is gone, neither the ledger nor RecoveryCustodyView can recover the original association. A blanket correlation warning accurately reports that loss but does not supply the promised custody.

The source obligation is not merely external PI-6 mapping: REC §7's conversation_index records the live/lost turn and items open at that moment; §3.4 G-4 and SQ-R R-5 require truthful per-turn item settlement/display after recovery. §8.2 supplies inFlightItems to present display and later receivers, and the exact custody schema requires threadId, turnId, itemId and itemType for those references. The authorized NEXT-ASTRA assignment expressly called for full native thread/turn/item capture and preservation into actual pointer history. The restart-event schema itself has no item array, so **this does not require inventing a new restart-event member or replaying an observation_lost event as newly observed after relaunch**. It requires retaining already observed pointer associations so the cold account can preserve them with its original standing. External native-item→proposal binding remains separately unfulfilled.

An item/started event supplies an observed item-to-turn association. It does not, by itself, establish the conversation's one current live turn at the later loss. Completion/start frames can be absent or contradictory; competing-turn references are precisely the counterexample. Putting its turnId into liveTurn would conflate correlation with lifecycle state, and still fail for several open turns. No native history lookup is a reliable substitute: REC's own observed basis explicitly notes unfinished items absent from supplier history.

**Minimal faithful proposed fit, requiring named source/schema review before code adoption:** extend only each conversation_index.lastObservedExecution.openItems entry with an optional nonempty opaque `turnId`, preserving existing itemId/itemType and all existing required fields. New own-source writes retain the actual observed turnId; absence on legacy rows means correlation unknown, never reconstructed from liveTurn, tags, current selection or native ID spelling. Enclosing thread/home/full lastLoadedGeneration remain the rest of the scope. Retain `(turnId,itemId)` identity so same item labels in different turns do not collapse. This adds pointer metadata, not native item content or an authority capability.

Because the current item object is closed (`additionalProperties:false`), this requires an explicit ledger schema/source amendment and synchronized product resource/validator adoption. Existing binaries will reject new rows under the old closed schema: state the compatibility/version/adoption boundary in the named change, rather than calling optionality universal backward compatibility. New-reader/old-row compatibility is straightforward; old-reader/new-row compatibility is not. Do not hide the relation in opaque receiver tags or add an unreviewed sidecar/ledger kind.

Required successor controls: unchanged item-only/competing-turn repros plus exact cold turn association; same item label under distinct turns; legacy rows without turnId stay readable with explicit unknown correlation; no liveTurn or restart live-work invented by item-only evidence; terminal completion removes only its matching open tuples; schema accepts new pointers and refuses raw native payload; existing metadata/tags/fork and retired immutable queue behavior retain their standing. Root must show known/unknown correlation faithfully. Schema/source review and code backcheck precede closing RC1-COLD and whole core; actual consumer integration remains outstanding.


# V6-S1 — independent CC-REC-ITEM-TURN-CUSTODY source-fit review

2026-10-05. **READY for bounded technical owning adoption of the exact proposed source amendment. No actionable source/schema finding. RC1-COLD remains OPEN until actual implementation and independent backcheck.** This verdict neither adopts maintained bytes nor closes the recovery core, Root consumer, external PI-6 or native evidence obligations.

Same independent TASK, parent and report-only write. Read the separate fresh owner's CC-REC-ITEM-TURN-CUSTODY-ASTRA report and full proposed §7.2/schema delta, examples, manifest and patch. No Cargo, product execution, source/schema edits, Git, supplier/network/auth operation. This is a separate source-fit review after V6-R1, not a retrospective approval of the incomplete code.

Private candidate `/var/folders/0s/50y7rb796d1bqdxmpcz6qg800000gn/T/chirality-rec-item-turn-design.rb2i2q3l`:

| Artifact | SHA-256 |
|---|---|
| source-amendment.patch | `2549bd3d1d1c146c0bab83291df0db9bbc5f24ad738df86b1cf96934aca8f7f8` |
| proposed EXECUTION_AND_RECOVERY.md | `088cb70f9124e09845b27dad785009fca56674e276f11dd32ae650622bdb1856` |
| proposed current ledger schema 0.3 | `8a400991244e6dc389f4159bafb65f6486d4b2609ba0a92d030469c434e0a81b` |
| preserved ledger schema 0.2 | `3f1d7f27f68a523c459ebcb9ce3dcd40a5de54fc4b9b16d20fd4e6b4c3f05c67` |

Independent pure-schema checks returned exit0: every manifest hash matches; the archived0.2 bytes equal the actual current owning schema; both schemas pass Draft202012Validator.check_schema; all six new examples and six existing ledger/custody/stop examples have their stated validity. Known correlated rows pass0.3 and fail0.2; the legacy-unknown example passes both. Empty/null turn references and payload fields fail. No dependency installation or network resolution occurred. These are 12 format outcomes, not runtime tests or new execution coverage.

The schema delta is exactly the distinct0.3 $id plus optional nonempty opaque turnId under the existing closed openItems item object. Existing required members, row kinds and all other definitions are unchanged. The source's mandatory new-writer retention rule is stronger than structural optionality: optionality permits old/unknown historical rows, not dropping an available native association. The implementation must enforce and test that rule.

§7.2 faithfully resolves RC1-COLD's representation gap without manufacturing lifecycle evidence: new native item tuples preserve actual turnId alongside itemId/type under enclosing thread/home/full generation; same labels in distinct turns remain distinct; an item start alone establishes no liveTurn; completion matches the tuple and terminal settlement only its turn. Per-item absent correlation remains unknown even beside a liveTurn. Cold rows preserve original observation provenance; neither current selection nor supplier history backfills missing historical evidence. No new event shape, store, record kind, tag convention, authority import, operation/run mapping or automatic resume is introduced.

Compatibility is explicit and accurate. Schema IDs identify validator versions rather than row versions. New readers accept unchanged legacy rows and mixed ledgers; old closed-schema readers reject correlated rows. The amendment requires coordinated writer/resource/validator/reader and Root consumer adoption, keeps0.2's identity recoverable, preserves bytes on rollback and forbids stripping pointers to downgrade. It does not pretend that schema optionality makes old binaries compatible or supplies automatic version negotiation. Parent must carry this restriction with the candidate/downgrade account and assess actual pinned downstream consumers before releasing it.

The propagation plan covers owning Design, exact product schema resource, validator and prototype/example checks, source capture/immutable queue, cold reader, Root presentation, contract issue/work graph and actual downstream REC consumers. Existing custody-event0.2 remains unchanged: hot loss tuples retain complete source references, while restart events keep their existing conversation/live-work shape and cold item associations are supplied separately. No contradiction with the bounded accepted REC ledger/custody contract was found; this closes the representation design question only.

Next required evidence is actual writer→queued/durable ledger→reopen/consumer behavior on the adopted0.3 source, including item-only, competing turns, duplicate item labels across turns, legacy unknowns, terminal/late frames, persistence failures and retired queue lifetime. Preserve all original failing vectors and V6-R1 partial evidence. Recheck exact cold turn associations and no invented live/restart work; do not close RC1-COLD from these schema passes alone. Named technical owning adoption can proceed under the reviewed interface-change route; no acceptance/release or stage-gate decision is asserted here.


# V6-R2 — independent implemented ledger0.3 cold-custody backcheck

2026-10-05. **READY for bounded recovery core fan-in at the exact frozen candidate below. RC1-COLD is repaired; RC1, RC2 and RC3 have no remaining actionable finding in this core scope.** This supersedes the earlier NOT READY implementation verdict for these bytes only. Root recovery consumer integration, actual native quit/relaunch, wider DEL-01-02 production and external PI-6 remain unfinished. The older-reader incompatibility is retained, not waived.

Same independent TASK and sole maintained report write. Parent authorized bounded immutable-binary controls; no Cargo/shared target, source/schema/Git, supplier/native/network/auth operation. Reviewed updated implementation return, frozen `cold03-checked/app`, CHECKED.json, source-adoption.json, inventory and patch. The source-adoption record binds the separately reviewed V6-S1 exact source patch to Parent's technical owning adoption; historical parser-only fields embedded in CHECKED.json are retained draft history, while its enclosing actual run record supplies subsequent checks.

Independent exact retained-binary execution, all exit0:

```text
/tmp/chirality-rec-custody-astra.bo0pfG/cold03-checked-lib-tests execution_custody_tests --test-threads=1
  15 passed, 0 failed (3.66s test time)
/tmp/chirality-rec-custody-astra.bo0pfG/cold03-checked-lib-tests recovery_custody_rc2 --test-threads=1
  1 passed, 0 failed (0.13s)
/tmp/chirality-rec-custody-astra.bo0pfG/cold03-checked-lib-tests app_custody --test-threads=1
  7 passed, 0 failed (1.10s)
```

**23 distinct independent passes.** This is the retained author-built binary, not an independent rebuild. Author's other20 passes are inspected evidence only, not added to this count. All declared source and log hashes match CHECKED.json; runtime resource manifest pins match actual resource bytes. Original RC1/RC2/RC3 regression function bodies remain byte-identical to original-vectors. Original failures and0.2 partial repair evidence remain in prior report sections/artifacts. Binary hash was unchanged after checking.

| Candidate artifact | SHA-256 |
|---|---|
| hosting.rs | `45bd26eb798db9df04a639213de7702bedad4ef89c962d521b146ab92cc2406f` |
| recovery.rs | `2e3c52c8fbc02b92067310a2a9caca9bfbd241ac99c79d49e1285c766014687f` |
| execution_custody.rs | `a9d95f8fb19efe5072a07fd090f34e2f2d90444e3838fbc47594d8ac637bbffd` |
| execution_custody_tests.rs | `976844fa75577ab919b80def97f9622c9ce476fb26e36fddece58d6a5da28257` |
| current schema0.3 | `8a400991244e6dc389f4159bafb65f6486d4b2609ba0a92d030469c434e0a81b` |
| archived schema0.2 | `3f1d7f27f68a523c459ebcb9ce3dcd40a5de54fc4b9b16d20fd4e6b4c3f05c67` |
| unchanged custody-event0.2 | `033398508abc813e90aee0a074a18cb91bd59be88b6991111504ae5662653773` |
| cold03-checked-lib-tests | `3239f1a96bdc94be14ac2d6cbc73be0303397fbf88ccbf74d6d28a8b7f4681f2` |


The source producer now writes the actual turn key from each retained `(turnId,itemId)` into the existing immutable pointer snapshot. It does not obtain that association from row.turn, current selection, a receiver tag or imported native history. Both competing associations survive identical item labels. Item completion and turn terminal handling remove only matching tuples; late starts cannot revive completed entries. This fixes the information loss identified in RC1-COLD rather than hiding it behind a warning.

Actual ledger append/open uses the exact reviewed0.3 resource through the existing production validator. Archived0.2 remains byte-exact, and checked examples confirm new correlated rows are rejected by the old schema while legacy absent-turn rows are accepted by the new one. No historical row is migrated or backfilled. The full source→ledger→close→reopen tests inspect the original full generation, owning home, thread, per-item turn and item references, with item-only and competing-live-turn cases. Item-only evidence creates no liveTurn or restart-live-work event. The independently checked legacy/mixed-row control retains unknown per-item turn/fullTuple even next to a liveTurn and verifies prior file bytes stay a prefix after normal append.

RecoveryCustodyView now supplies openItemAssociations with per-item known/unknown correlation and a fullTuple only when an actual persisted turn exists. Its standing remains historical App metadata, not current liveness, native content or authority. Execution-generation and metadata-append provenance remain separate under RC2; the actual cross-session context writer control passes. RC3 terminal-source handling and its original contradiction control still pass. Read-only view has no flush/append/send or public source-mint path.

Queue/source guards are unchanged from the reviewed successor Host hash. Independent affected checks exercise actual retired Host drop/recreation, IO failure/restoration without end replay, paused writer/source order/Stop, shared context and unavailable original ledger/no relocation. Custody checks additionally exercise queued versus persisted views, retained context/fork metadata, separate homes, close idempotence, truthful stop/quit versus missing/clean end and unchanged custody-event schemas. These tests establish owned synthetic fixture behavior only; physical storage/power-loss or supplier operation is not inferred.

Manager may fan in these exact core/source/resource bytes with the reviewed source amendment and carry the0.3 older-reader/downgrade restriction. Before closing the present recovery undertaking, integrate and independently inspect the actual current HomeSession consumer, render openItemAssociations known/unknown and metadataIndex/executionGeneration distinctly beside native History, retain pending/error/unknown limits, and complete required propagation notices/records. Core READY does not supply those missing consumer or native witnesses.
