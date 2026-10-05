# P2-INTEGRATION — immutable staged successor preservation/glue review

2026-10-05. **NOT READY at staged tree `e6cd6b0356762ca133855f772b212b7fe213f34a`: one precise native form-alias backend gap remains.** Other preservation/manager-scope checks below stand. This is not another whole-unit review, a whole Group A 90% claim, final test/CI verdict, product qualification or release.

Independent TASK `/root/group_a_execution/aac_contract_review`, delegated-harness-native child of WORKING_ITEMS `/root/group_a_execution`; no delegation. Applied retained repository software-code-review skill to staged preservation and unreviewed manager README/CONTRACT_ISSUES/graph/schema visibility. Reused actual substantive source reviews rather than repeating generated fixture review. Read only staged diff inventory and archive bytes at `/private/var/folders/0s/50y7rb796d1bqdxmpcz6qg800000gn/T/tmp.JcIirKW82W/source/projects/chirality-app-v4/` for product/Design analysis; evolving working-copy I3/parser work is excluded.

Execution provenance: the initial inventory mistakenly included `git write-tree`; the sandbox refused index.lock (exit128), so no Git write occurred. No escalation/retry; subsequent Git calls were read-only diff/rev-parse/show. Only this report was written. No Cargo/build/native/model/auth/network/credentials/download or delegation. Final candidate build/tests are separately planned against the archive; none is claimed by this review.

## Blocking staged gap

**P2-1 [P1] Form aliases are not validated at the actual request reducer boundary.** Archive locations: `app/src-tauri/src/native_requests.rs`, validate_answer's MCP requestedSchema branch; `app/README.md` current-path item 7.

The staged App card recognizes `form`, `openai/form` and `openaiForm`, and runtime_session.answer_preview normalizes an alias in a temporary validation copy. The actual RequestRegister/Host answer operation still applies requestedSchema only when nativeParameters.mode equals literal `form`. A direct valid-origin alias-mode accept therefore passes the generated response-shape validator without applying that request's form schema. Temporary preview validation is useful but cannot supply the underlying operation's complete answer validation contract for every receiving caller. The README's “form aliases validate their content” exceeds the staged backend guarantee.

Independent installed-schema counterexample: an accept response with content `{choice:"no"}` validates against the maintained 0.160.0 McpServerElicitationRequestResponse; a supplied object schema requiring `choice == "yes"` rejects that content. The staged alias branch omits this second check. This is source/schema evidence, **not** an independently executed Rust reproduction or a claim that the currently guarded App button bypasses its preview.

The manager confirmed this is a real staged gap and dispatched the original module owner to repair only alias recognition/direct valid+invalid requestedSchema tests. Existing Core R1 transport review does not cover this branch; no phantom review is relied on. Repair the actual reducer while retaining nativeParameters and origin/full tuple semantics; run focused direct-boundary positives/negatives for both aliases and literal form; freeze a named successor and backcheck it before successor readiness. Removing only the README claim would not satisfy the backend obligation.

## Preservation and manager scope supported at this tree

Nine directly inspected archive files were independently compared with their immutable Git-tree blobs and match exactly. The tree identity is verified with read-only rev-parse, not inferred from the mutable index. Staged path inventory has no new decision_view/util/I3 admission-export or held workflow-parser source: baseline files may exist, but their evolving changes are not part of this candidate and are not reviewed here.

Latest V3-I1-CONVERSATION-INTEGRATION seals exactly match staged lib/runtime_session/App, hosting and the four connecting test files. That review's source-preservation chain covers the earlier READY ledger startup and I4 native-observation glue. Staged native_requests/recovery/native_items/access remain the reviewed I1-R1/REC-RT bytes. I4 observation/catalog/receiving sources and unchanged integration tests match V3-I4 seals. First pure I3 act_policy/standing/test hashes match V2-I3-POLICY-R1; they remain a bounded unit, not the unstaged A16/admission/reader join. No pure-unit readiness is promoted to a completed control path.

Schema visibility: staged schema_validation differs from merged HEAD only by crate-local visibility of compile_targets and formatting/optional trailing commas. Independent lexical comparison preserving string literals confirms no other token change. The helper remains limited to supplied declared-ID resources, rejecting retrieval, dialect/resource/setup errors with eager compilation and no unchecked fallback. It is needed by already reviewed catalog/policy consumers and adds no protocol/schema/record meaning or global callable interface. Archive builds still must exercise the assembled consumers; token preservation is not that test pass.

README and CONTRACT_ISSUES otherwise keep source behavior and evidence standing separate: expected network traffic is not measured traffic; selected model/provider and Codex settings are retained; child roles are not supplied; external observations preserve unverified origin/currency and display limits; interrupt acknowledgment is not native turn end; native-authenticity/SEAL-2 cold replay, userVerification positive capability, full history/recovery, other act kinds, actual policy/standing joins, external dispatch and qualification remain open. CI10/CI11 keep exact unmet obligations with their existing owners. The held CommonMark dependency/parser is correctly identified as unfinished rather than production-complete.

The graph retains active I1/I2/I3/I4, planned I5 and closeout, blocked custody/held supplier prerequisites and receiving-loop pin obligations. It distinguishes bounded READY units from the whole group, preserves original review failures and the project-order constraints, and records the conditional Group B signing input without transferring A's replay obligation or inventing acceptance. Historical “executing/dispatched” observation paragraphs remain history beside the current completed unit rows; they supply no new completion warrant.

## Proof and final-test boundary

Reused ROLE supplier-capture/pin and instruction-tranche reviews support exact sampled primary composition carriage and unchanged compared provider input/native template at their declared exclusions. They explicitly retain original UNKNOWN/exit1 probe evidence, unknown model adoption, other-role/child/lifetime limits and no supplier qualification. Runtime instruction seeding and editable/current-copy behavior have their actual later glue review; no instruction origin is silently rebound to Root defaults.

Root-owned result/structure JSONs are not in this staged archive and remain awaiting custody release. No raw prompt/provider payload was inspected/copied into this report. The existing accepted metadata/source reviews can be cited at their bounded standing, but this tree is not a complete newly published/recoverable probe-result packet. Manager/Root must retain or release the nonsecret identified records through their owning custody before relying on their presence in a published package; no authorization to copy raw prompts is inferred.

EVIDENCE.md is inherited P0 evidence identifying P0 ACT/HOST checked source and its historical combined checks. It is not evidence that this expanded staged tree has already passed final-source tests. The forthcoming archived Rust/Node/frontend/source-sync/build results must be bound to their actual candidate, particularly after P2-1 repair, and preserved separately. A new passing run alone cannot cure the known alias defect without its targeted source repair/regressions.

## Exact staged identities and return

| Staged path | SHA-256 |
|---|---|
| `app/README.md` | `6b219f7f950b546a9bace569626d9d371236a4ee900f334124dd491ba05cfde3` |
| `app/CONTRACT_ISSUES.md` | `6b373904f3d3c8a04add025c599f296dd6142156751e2e80a98dff15da5a25bd` |
| `app/src-tauri/src/schema_validation.rs` | `42545d9d544f0a8ac7be84814bc9285d987888e6c7ef2ca0201041458c2eb3a9` |
| `app/src-tauri/src/lib.rs` | `e88f133c46805d9085c496d966d23ff411f70ac303b2f81df1a387b01270e2cd` |
| `app/src-tauri/src/runtime_session.rs` | `c96db03894b242f78a7029b5e04063f639fb02dc13b0c8de59de4b3e9e0e88b9` |
| `app/src/App.tsx` | `3e509ea07de283fc4dfd9ca8ea67d1196457a165bbc3e247990fb02dcec3f672` |
| `app/src-tauri/src/hosting.rs` | `fbe61326d878fc92d7301773e38e0781dbaca6f98eb46ba87df06b80b6991510` |
| `app/src-tauri/src/native_requests.rs` | `5879e6d034820e5d26c6dea1a4947ab851a39c0598aa675753ab6948e3030dbe` |
| `app/src-tauri/src/recovery.rs` | `4aefbdc26f4956a50788a21089c650ce80a4509727105485ce91d036396d49d0` |
| `execution/_Coordination/WorkGraphs/APP-V4-GROUP-A-20261004/WORK_GRAPH.md` | `3fc899826781934354fcf2ebf3543c361bafa4dafde2a4a6dcf8f9a5c7940772` |

Return: preserve this exact-tree review and its P2-1 finding; integrate the separately reviewed alias successor and rerun only affected/required candidate checks before a successor P2 disposition. No broad substantive redo is needed for unchanged reviewed modules. Root proof custody and final archive checks remain explicit packet/integration requirements. Existing unresolved Group A production, downstream adoption and native/qualification work stays in its current graph, not silently completed by this staged slice.
