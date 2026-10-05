# V2-I1-REC-RT — independent product mapping adoption review

2026-10-05. **READY for bounded later-error reducer/ledger adoption and its released Host test consequence. No blocking, major or minor finding.** This resolves the specific missing mapping retained in V2-I1-R1; full recovery/native/App production and qualification remain unclaimed.

Independent TASK `/root/group_a_execution/aac_contract_review`, delegated-harness-native child of WORKING_ITEMS `/root/group_a_execution`, no delegation. Same contract reviewer; did not implement this adoption. Applied previously read software-code-review skill. Read final named return, native_requests/recovery mapping and affected tests, reviewed HOSTING RT14/15 and RECOVERY receiving sources, and the single released Host test change. Only this report written; no product/Design/Git edits, network/auth/credentials/model/supplier execution. Manager explicitly granted the Cargo slot; it was released immediately after the three focused regressions completed.

## Exact candidate

Final `changes/I1-REC-RT-ADOPTION.md` SHA `27ff8c18392d714de91181ee625a8198719851d8f451213df472139760dd5850` includes historical old Host failure and the named test-only successor. Frozen scoped bytes match before/after independent checking:

| File, relative to app/src-tauri/src | SHA-256 |
|---|---|
| native_requests.rs | 5879e6d034820e5d26c6dea1a4947ab851a39c0598aa675753ab6948e3030dbe |
| recovery.rs | 4aefbdc26f4956a50788a21089c650ce80a4509727105485ce91d036396d49d0 |
| hosting.rs whole successor | 71ec04b2a67893e133d94c756a3bada17eedcc783ea82d0ffd9d16f44d1ca97a |

READY source inputs remain V0-H-RT-LATE and V0-REC-RT-LINK, binding HOSTING `47b8f1c6…` and RECOVERY `9b443fbc…`. No schema/resource shape or ID was changed to make this adoption pass.

## Mapping assessment

prepare_error sets the private laterProtocolError marker only after origin/native/state validation for the admitted outstanding operation. Incoming nativeParameters cannot set it. written now distinguishes later failed errors (RT09 settle-write-failed/write-failed) from receipt error failures (RT02/03 errored/write-failed). A written marked later error is RT14 errored/written; exact native error and actual named/boundary origin remain intact, without human_act or person content-answer attribution.

resolved uses full generation/request lookup, thread correlation and closed-generation refusal. It acknowledges only a written answer/decline or a written marked later error (RT15), retaining the actual source generation/native request envelope privately. Failed writes retain separately sourced supplier resolution without inventing an acknowledgment or changing uncertainty. Public schema-shaped records omit private operational markers.

request_summary maps RT14 to RQ03 closed/errored/written and later RT09 to RQ03 closed/settle-write-failed/write-failed/not-observed. Receipt errors remain RQ08. RQ09 requires written RT12/13/15 state, matching acknowledgment tuple/request/thread and same-generation request history. New acknowledgment after source/durable closure refuses with unchanged bytes; already durably observed pre-closure acknowledgment can remain unchanged during later summary replay. Written/no-ack closure is RQ05; unanswered closure is RQ04. The mapper validates later-error origin/native error rather than accepting an arbitrary marked errored object. Full H5 remains object at the boundary and tagged lossless reference only in the ledger.

Native MCP turnId:null remains unchanged in nativeParameters and is omitted from the ledger's optional string pointer, without guessing a turn or widening the schema. The connected tests assert both halves. This preserves absent native correlation rather than silently changing native payload.

## Evidence and Host test consequence

Independent command from repository root:

```sh
CARGO_HOME=/tmp/chirality-app-v4-group-a-cargo-home CHIRALITY_SKIP_CODEX=1 cargo test --offline --locked --manifest-path projects/chirality-app-v4/app/src-tauri/Cargo.toml --lib reviewed_later_error_adoption_tests
```

Exit 0; **3/3 pass**, 46 filtered, 0 failures/ignored. The groups exercise actual reducer→ledger success/ack/failure/closure with foreign/post-close negatives, receipt RQ08 and refused submissions, forged acknowledgment shapes with unchanged file bytes, exact generation/origin and null-turn omission. No broader passing suite was substituted for these missing claims. Author evidence additionally records native_requests 10/10 and recovery 10/10 on their frozen scoped bytes.

The original Host oracle actually failed **exit101, 0/1**, unwrapping an absent recoveryPersistenceError because its formerly held mapping was now supplied. That failure is retained rather than erased. Parent subsequently released only the old missing_custody_mapping_tests block after its Host production review. The renamed successor uses an env-cleared /bin/cat echo-only pipe, asserts the exact outgoing error, written/error/native origin/full tuple, no acknowledgment invented, no recoveryPersistenceError, RQ01 then RQ03, no RQ08/human_act and no guessed turn. This is governed source-adoption oracle maintenance with stronger connected transport evidence, not tolerance of an unexplained error.

Owner's exact successor Host test reports **exit0, 1/1**, 0.07s; this reviewer read the test and did not independently rerun that one test. Independently recomputed seals match the named preservation evidence: production prefix `43fc53d79b07a70374d8c902882d9f53a7e3524f986a49601a102946d1838b59`, bytes outside the released block `c6f18156164bd08aea4460a91e082da446f790e701180e5ed28fcb1390266f70`, released block `09bb27e154ed118f3a6a2fc50e60718cc5258ccf5dd0226b153740eaa54d6b99`. The before/after equality claim is preserved with the owner/manager evidence; no new Host production behavior or another test change is certified as part of this test-only consequence.

## Return

The specific later-error source/receiver/code mapping is ready for manager fan-in at these hashes. Its prior no-adopted-RQ gap is no longer a reason to strand summaries on this operation; broader storage errors still require truthful pending/incomplete behavior. Combined readiness can now include the named Host test successor rather than the old failing expectation, with its bounded evidence stated above.

Actual native cards, supplier acknowledgment behavior, application reconnect/cold relaunch, ledger publication/directory durability and failed-write recovery, complete runtime-session/UI/multi-home/account/guidance/A15 integration and qualification remain separately unfinished. No general I1 completion, reserved act, stronger account identity or supplier qualification follows from this narrow adoption verdict.
