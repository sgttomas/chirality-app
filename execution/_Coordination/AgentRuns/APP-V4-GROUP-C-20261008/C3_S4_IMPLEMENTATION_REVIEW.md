# C3-S4 independent implementation review

**READY for bounded manager fan-in** at exact candidate `3909ebc2a49fe99c6a1974444c5f81a2232b13fa`, receiving `f25ba6887d85904ebef2a6321c222809d47cfabd`. No blocking findings. This is independent review, not CI completion, native qualification, full reconstruction or acceptance.

Reviewer: TASK `/root/group_c_successor/cfb_design_review`, parent `/root/group_c_successor`, delegated-harness-native execution, separate managed review branch `codex/group-c-s4-code-review`; no delegation. The authorized write is this report only. Instruction fences and actual host permissions apply; no per-file enforcement is claimed. Applied software-code-review to the full 24-path diff, production callers, registry, filesystem writer, schema/cold reader, actual renderer handlers and retained tests. No production repairs were made.

## Exact basis

Selected CAM-v0.1 plus CAM-R1 source `e87321bae2d782ae6a2d2cfaff3ba0b647398358` and technical releases are retained in C3_S4_TECHNICAL_SELECTION.md. Independently recomputed all three selected-source hashes and all fourteen implementation-file hashes in C3_S4_IMPLEMENTATION_BASIS.json; all matched. Design and embedded schema bytes match. Old 0.1/0.2 schema bytes are unchanged.

| Actual origin | SHA-256 |
|---|---|
| DEL-07-02 Design/CONNECTOR_ACCOUNT_MATERIALIZATION_v0.1.md | `627581f503ebf8f7752d8f099215f73f25358e8b7ecef4702186125640e8f4aa` |
| DEL-07-02 Design/connector.route-account.v0.3.schema.json and matching embedded resource | `f220695f8f8f28651508ae9f5a471c35aa37f26a55d287eb05ebe90af93fe50b` |
| C3_S4_TECHNICAL_SELECTION.md | `6df69e8bf2946461ba832ab922a82c416d9303b7c0f84a2937d5dd5faf3fcd62` |
| Root AGENTS.md, continued supplied role context | `f96feb19d297c74e10048c506805b2fe3622c50cfefd6078f599724556113977` |
| agents/AGENT_TASK.md, continued supplied role context | `1a13a5b00b3ce01ff8519efe6b46bcbe0cd6a5b7985e24282fa7efa2c57c8fb7` |
| projects/chirality-app-v4/loop/LOOP_INIT.md, continued selected loop entry | `c2e88f81439ed03578fee13fd7563082fefdfe11096d9134a59531eba3b985bd` |
| .agents/skills/software-code-review/SKILL.md, reread for this return | `ee085d589c44f912d11a59eead8edac214f0343761d26b0d33e886a979888bca` |

Prior source review and its semantic-check gates remain in C3_S4_SOURCE_REVIEW.md. The source's historical proposal/confirmation wording is interpreted through the explicit technical selection, not silently rewritten as human acceptance.

## Independent execution

Used the exact candidate export, existing private serial target and approved offline dependency cache, with CARGO_INCREMENTAL=0, CARGO_NET_OFFLINE=true and CHIRALITY_SKIP_CODEX=1. No clone, download, supplier/native launch, credentials or MEMORY act. Local permission covered the inherited passive loopback sentinel, not an external network qualification. Disk pressure paused additional work; only the reviewer's own quiescent stale incremental cache was removed. Checks resumed after manager capacity coordination.

- Exact-candidate `connector_` Rust library checks: **70 passed** with default features; **70 passed** with `distribution-successor`. This includes ten materialization tests, existing hostile Git/source/store tests and abrupt-exit child witnesses.
- One additional disposable independent distribution-feature test passed; production bytes were unchanged. Its two sequences are specified below.
- Full maintained `npm test`: **23 passed, one supplier handshake skipped** because no supplier binary was selected. Nested decision-flow Rust tests: **4 passed**. The maintained source/route component and actual-handler checks are included, not merely static source matching.
- Production frontend build passed. Full candidate diff whitespace check passed. Existing compiler warnings were not represented as new defects.

The additional `connector_materialization_independent_uncertain_session_and_failed_replacement` probe first prepared a valid draft, then cancelled source selection inside the final-freeze test hook of a replacement preparation. The replacement failed and the complete registry view equaled its previous value: original draft, one slot, no exposed replacement. It then used a fresh constructed repository to prepare and invoke the real writer's post-publication error hook. After that actual rename/error, but before returning the writer result, it cancelled the draft and created a new source session. The registry still reported uncertain, with the original injected-error/Attempt text. Two reconciliation calls each observed the exact saved account while preserving that original text and uncertain status. Repeated publication used a panic-on-write closure, which was never invoked; one slot and no full payload remained, and cold discovery found exactly one account. This is a synthetic adversarial sequence, not an actual native user operation.

## Contract and scope assessment

Schema-only duplicate-duty, mismatched-revision, dangling-reference and altered-excerpt-digest fixtures are first shown schema-valid and then rejected by semantic validation. Producer mapping binds current private source/Git references, question pins, side/anchor identity and exact bytes; partial/gaps-only failure conditions remain explicit. Caller interpretations, duties and responsibility are separately attributed. No facts, supported conclusions, performed/not-required duty or authority is manufactured.

The retained opened source root and writer root compare device/inode; root and Git association checks occur before freeze and publication. Final source eligibility is held under the source lock through registry reservation. Failed preflight leaves prior state intact. Capacity tests cover 64 consumed identities, refusal of 65, cancellation/supersession tombstones, one retained payload, no preparation during write and no token revival in a new instance. Publication passes only opaque token/generation and preserves actual started outcomes across source changes. The early retained-result lookup precedes fresh project admission for already consumed tokens, without authorizing a new write.

The 1 MiB producer boundary counts serialized UTF-8 including escapes; exact-boundary publication/readback and padded original-byte cold refusal pass. Identified 0.3 validation occurs after acquisition, so it is explicitly not a preallocation bound. Legacy 0.2 padded records retain their old behavior; mislabeled 0.2-as-0.3 and unknown 0.4 refuse. Cold presentation exposes draft standing, receipt limits, excerpts, caller interpretations and typed responsibility without restoring source custody or implying prior successful publication. Host namespace/receiving-base additions remain intact; the shared lib changes add only required state, commands and test initialization.

## Remaining limits

Real constructed Git repositories, filesystem operations and mocked renderer transport establish the bounded connected mechanisms. They do not establish actual native selection, user-project provenance, independent cold source verification, factual reconstruction, manager/person duties, external consumer adoption or 90% completion. Existing CGP same-engine consistency and process/path residuals and CRP late-rename/uncertain outcomes remain. macOS was executed; Linux/unsupported-platform behavior was inspected, not qualified here. Power loss and actual filesystem durability failure were not newly witnessed. The 64-entry development bound is not a final product capacity decision. C3-S4-R, point-held native witness, receiving-owner decisions and SEAL-2 remain as recorded.
