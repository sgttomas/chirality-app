# V1 — REC attachment project-context definition review

2026-10-05. **Original frozen definition/prototype packet NOT READY: one blocking model-warrant gap REC-PC1. Source contract otherwise compatible.** This is bounded REC/NIR/ACCESS definition/source review, not production code or checkpoint14849 qualification. TASK `/root/group_a_execution/contract_reviewer`, parent WORKING_ITEMS `/root/group_a_execution`, delegated-harness-native, gpt-6.1-sol/medium; no delegation/model-diversity claim. Parent resumed the original owner for repair; a repaired successor must be separately sealed/backchecked rather than silently replacing this association.

## Original exact source association

| Subject | SHA-256 |
|---|---|
| changes/CC-REC-ATTACHMENT-PROJECT-CONTEXT.md | 0193263c25fb2077da7b0f9a0abe661e71c001ae2c24aedc5d6df17c36c33f31 |
| DEL-01-02 Design/EXECUTION_AND_RECOVERY.md | bdd358607c5b957c3f3a8b440680b614d56404bee459060574db0e465aebee44 |
| recovery.app-ledger-entry.schema.json | 3f1d7f27f68a523c459ebcb9ce3dcd40a5de54fc4b9b16d20fd4e6b4c3f05c67 |
| prototype/project_context.py | ac2bd0d1be1bb9653485434edeaddd7c5dd782deb7abcb71f54c943f064f1829 |
| prototype/check_project_context.py | fe2388ffc60ecf87c83c44f9334615ee6018548b0c03c5e3ce3e961c1f77866d |
| V0-NIR-REC-PROJECT-CONTEXT.md | b6bcd36c0a621e6a0902b92c29897ce6d1d60d491f9703650e23896a3fed368e |
| V0-ACCESS-REC-PROJECT-CONTEXT.md | 72e972ae52a2c6dd71153c8fe23fcebca6d86227eb78eabfacf6c778d5b7414e |

All independently hashed. Historical nullable proposal is not this candidate and is not adopted. Current production checkpoint explicitly excludes this definition WIP; no product or other review hold is inferred from REC-PC1.

## REC-PC1 — known index ignores existing hot-only submission binding

`project_context.py::bind_context` selects `index["tags"]` whenever an index exists and only uses memory_tags when index is absent. REC §4.1 permits a tag write failure to leave a tag in memory; a previously known historical index P may still exist. With known P lacking the failed durable tag, hot submission S→Q must therefore constrain a later same-S attempt just as it does when no index row exists. The prototype has no stated/enforced complete-hot-index precondition and ignores the explicit supplied memory tag in that case.

Independent offline pure Python control, no files/native/Cargo operation:

```python
index = {"kind":"conversation_index", "session":"synthetic", "at":"observation",
         "threadId":"synthetic:thread", "home":"H-acct", "project":"P", "tags":[],
         "lastObservedExecution":{"state":"loaded-idle","at":"observation"}}
hot = bind_context(index, "submission:fixed", "Q")["tag"]
bind_context(index, "submission:fixed", "R", (hot,))
```

Actual result: currentSubmissionProject R, idempotent false, new tag `["submission:fixed","R"]` seq1. The corresponding no-index call with the same hot tag correctly refuses `immutable submission context conflicts; no retag/transfer`. Thus the new definition's immutable same-token rule is not established across this actual known-index/hot failure representation by the model controls. This is a scripted model defect, not an observed native metadata write failure or private Root enforcement failure.

Required bounded repair: check all supplied relevant durable/hot bindings, or explicitly enforce a source-complete hot snapshot precondition that cannot ignore contradictory supplied memory metadata. Same token/different binding must refuse or expose ambiguity; same binding must be idempotent; known historical P/old rows remain unchanged. Preserve raw conflicting tags, no latest/path/time winner and no forged durable claim. Focused known-P + hot S→Q + new R refusal, same-Q idempotence and both absent/known index controls are required without changing this oracle. No new schema field/kind/service/human gate/product policy is necessary.

## Preserved source-definition assessment

REC §7.1/§4.1 receiver extension names NIR DEL-01-04 and opaque compact UTF8 JSON pair of immutable submission token with independently supplied nonempty App project reference or null absence. REC preserves value/order and does not interpret run/current native state. Null is inside a nonempty tag string only; conversation_index.project remains required/nonempty0.2. Independent structural JSON comparison to the maintained runtime0.2 schema is identical after removing only schema annotations, preserving property/definition maps and all ID/const/enum/default/shape data. No nullable/index successor or fake unknown value is admitted.

Known historical association P remains P; explicit current submission Q/absence is separately reported same/different/unbound, not transfer/backfill or changed model/home/role/run. Unknown historical association has no fabricated row; hot memory-only/no cold lookup is an explicit missing durability limitation, not complete recovery by omission. A genuinely new current App association may index actual known Q as its own observation, never retroactively relabel earlier native history. Actual successful owning metadata is necessary for a durable context claim.

Configured/opened App directory may be a legitimate reference when furnished by actual Root/shared source with lossless identity. Coincidentally matching native cwd/temp/home/projectId, WR run or renderer assertion supplies no such warrant. Freeze Q/absence before asynchronous preparation and bind the actual returned immutable submission token; do not reread a changed selection after await. Tags do not hydrate SourceRequest/native thread/full generation, infer pipe/receipt/adoption/cold readiness, insert guidance/caption into native input or impose file containment in Q.

NIR concurrence preserves complete ordered supply/HOST prewrite barriers and trial WR draft/source handles, not a universal Root/WR gate. Ordinary text/attachments are not blanket-held by missing historical index/context; actual project/run-scoped effects wait only at their own point of need. Opaque historical unrecognized values are preserved without source reactivation or current-run inference.

ACCESS concurrence is precise: existing ACCESS0.2 requires nonempty project and cannot represent unknown new selection/view with null/temp/cwd/fake ID. Its owning native unknown-selection/view source path remains a real open dependency before claiming that consumer complete. It neither supplies default model/provider nor silently retargets old selection/model/home, and creates no conversation-wide veto or new human approval checkpoint. Current lib cwd bridge is not the required independent Root reference. REC/NIR compatibility does not close this ACCESS source gap.

## Method, limits and return

Applied software-code-review skill ee085d589c44f912d11a59eead8edac214f0343761d26b0d33e886a979888bca; Root/TASK/v4-loop origins/hashes retained in earlier run reviews. Read current source packet/REC amendments/schema/prototype, actual NIR/ACCESS concurrence and focused relevant receiving meanings. Only read-only Python/stdlib source controls and structural comparison executed; author controls/16 existing cases remain separately attributed, not rerun or native enforcement proof. No production/shared/Cargo/Git/auth/model/nativeUI/dependency/network write/operation or delegation; only this assigned review written. W1/AK-e/record custody and production14849 separation preserved. Original owner repair and successor independent backcheck remain required for this bounded model warrant; wider private-context/index/tag/cold/ACCESS/source readiness remains production work, not acceptance from definition.

## R1 successor — independent same-reviewer backcheck (2026-10-05)

**READY for bounded REC source-definition/prototype fan-in. REC-PC1 repaired; no remaining blocking, major or minor finding in this affected scope.** The original019/ac2 NOT READY association and its exact unchanged oracle above remain historical. No production/shared implementation or checkpoint14849 adoption/witness is granted.

| Frozen successor | SHA-256 |
|---|---|
| changes/CC-REC-ATTACHMENT-PROJECT-CONTEXT.md | ef5039ee3a27e9723c626e8bd0401cdcc6adad71e418c5116497a5a922353b5e |
| REC Design/EXECUTION_AND_RECOVERY.md | e78b9ead452b0a1adb20cf07493a1eccbd2ee651e68d4f75772c440a6a228056 |
| prototype/project_context.py | f6fb259360d685632d3f54263818fa58224e26575e28f8a717056efe9c42b1f9 |
| prototype/check_project_context.py | 1ba99c0b8a750ba3a2467d78561940b6e2ed24dae27b9f61af46d4687fb7c929 |
| recovery.app-ledger-entry.schema.json — unchanged | 3f1d7f27f68a523c459ebcb9ce3dcd40a5de54fc4b9b16d20fd4e6b4c3f05c67 |

All independently verified before and after source/control assessment. The original review prefix before this append is SHA04c41f59264428862cf329b98c5b83225d1f8c3b081a411dca23144cc4eb88cd. NIR/ACCESS earlier concurrence hashes retain their historical source association; this affected hot-source repair does not silently adopt the later ACCESS unknown-selection definition.

Source now combines index tags and supplied memory tags even when historical project P is known. Identical tag objects are not duplicated in its working collection; no durable-first or hot-first fallback masks different recognized bindings. Resolution checks every recognized same-token binding before returning any result. A differing current target or durable/hot disagreement refuses; cold combined lookup stays ambiguous. Unknown tags/source input lists remain untouched. Exact same binding is idempotent, and a known index lacking that hot-only binding reports memory-only/cold lookup unavailable rather than deriving durability from P's existence. REC §7.1 expressly carries both-source checking including failed tag writes alongside a known index. Actual implementation must furnish complete actual hot metadata; these scripted labels remain no private Root capability or native proof.

Independent `python3 -B` stdin controls imported only the actual frozen prototype; no fixtures/source patched, no filesystem/Cargo/native operation. Original exact known-P/index-without-durable-tag plus hot S→Q/newR input above is unchanged. Actual results:

- Original known-P/hot-Q/new-R refuses `immutable submission context conflicts; no retag/transfer`.
- Original absent-index/hot-Q/new-R still refuses with the same error.
- Known-P/hot-only same-Q is idempotent, returns unchanged P snapshot/exact hot tag and limit `known project index lacks this hot binding: tag memory-only; cold lookup unavailable`.
- Identical durable/hot repeat is idempotent with unchanged snapshot and no missing-durable-binding limit.
- Durable-Q/hot-R/current-Q refuses; combined-source lookup is ambiguous rather than choosing a winner.
- Explicit hot absence is idempotent with no row/cold limit; changing that same token to Q refuses, including beside known P.
- A new token bound to R preserves historical P, original Q tag and source input object, reports different/no transfer.

All assertions passed, exit0. These are direct focused semantic controls, not native persistence/privacy/cold replay or Root-source enforcement witnesses. Author controls/16 existing REC cases remain separately attributed; no blanket repeat. Unchanged schema retains original0.2 no-row/null-inside-tag rule and prior independent structural comparison. Source contract's P/Q, lossless explicit App directory reference, no cwd/home/WR/native project inference, no raw tag capability hydration, ordinary-input/no-blanket-hold and NIR/HOST prewrite barriers retain their valid assessment.

ACCESS unknown NEW selection/view source handling remains an actual owning dependency pending its separately frozen source review/implementation; this backcheck neither closes it nor invents a model/provider default, broad input hold or fresh human gate. Actual private Root source freezing before prepare, returned submission binding, REC index/tag write/read/cold limits and complete known-hot source tests remain product work with their owners. No full Group A acceptance/release/qualification or unrelated production hold follows.

Only this assigned report appended; no product/shared/Design/schema/Cargo/Git/auth/model/nativeUI/network/dependency write/operation or delegation. Prior skill/role provenance and record custody preserved. Return final bounded definition/model READY at the exact successor above.
