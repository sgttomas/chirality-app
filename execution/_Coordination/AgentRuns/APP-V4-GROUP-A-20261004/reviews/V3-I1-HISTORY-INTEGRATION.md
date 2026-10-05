# V3 — I1 shared history/ROLE integration: original candidate

Disposition: **NOT READY**, one blocking correctness finding. Independent TASK review, 2026-10-05, delegated-harness-native child of `/root/group_a_execution`; gpt-6.1-sol/medium. No delegation or model-diversity claim. This records the original candidate inspected before its authorized successor repair; it does not describe current source as unchanged.

## Candidate association

Original author record `changes/I1-HISTORY-INTEGRATION.md`: SHA-256 `0f3a912d77a206bde29894e7952edfb3d73e5c9225e9c51e14680be60738d763` before the R1 append.

| Original source under app/ | SHA-256 |
|---|---|
| src-tauri/src/lib.rs | fede9e6bf692aa03da108d31ef2244f6c0588c09e633589e3a7b60235d94ee99 |
| src-tauri/src/runtime_session.rs | 33d3e69db61b5fcfa570a422ac71b3f178822cbc8ec651263ce4d52af0b01099 |
| src-tauri/tests/history_integration.rs | d59503c08589ec1040c9e7d16ebd97c20b93e928c9b1c382d9f9e95aa6f039ba |
| src/App.tsx | 316cd7b31c5d8b8857380779a02936e766c71374eebb12d406baebca2f4e1d4a |

## HJ-1 — blocking: fallible start work escapes the claimed state

In original `lib.rs::thread_start`, after access selection and role-supply status become Starting, supply-reference generation through `opaque_id("sup:")?`, `HistorySession::start_dispatched(...)?`, and final `ConversationSelection::started(...)?` can return before failure cleanup. An entropy/preparation failure or refused/malformed lifecycle result therefore leaves the shared selection Starting. The next explicit start is rejected as already in progress. This is a source-confirmed control-flow finding; no original dynamic reproduction is claimed.

Required repair: finish no-effect fallible preparation before claiming, capture every postclaim error, and finalize selection/status on all paths. Preserve genuine private dispatch receipt and actual write/response uncertainty after a sent request; do not report it as not sent or automatically resend. Cleanup must match original attempt identity and complete owning generation, so a late failure cannot overwrite a newer claim. Focused regressions must cover preclaim failure, postclaim preparation/result refusal, replacement attempt and generation controls, and genuine dispatched receipt retention without binding/admission.

The author's original passing history/affected/bridge checks did not cover these escapes. The original Host mixed-result/error finding belongs to its separate owner/review and is not certified by this review.

## Preserved review warrants and limits

Read source supports separation of local history query IDs from actual supplier RPC identity/reference, private-source correlation, complete-generation/selection/stream guards, read-only history, and explicit latest-candidate Continue admission. New role binding derives from immutable original composition and actual private sent-frame/result context; native role hints/current selectors/imported records do not substitute. Resume does not invent current role guidance. Existing text/interrupt/request/ledger/observation/I3 paths remain represented. UI displays null/empty/pending/error and original-role Unknown limitations separately.

These are source findings, not a physical UI, supplier lifetime, changed-source native smoke, cold persistent-role provenance, child-role supply, qualification or whole Group A completion warrant. README step11 exists; an earlier reviewer lookup omission was corrected and is not a missing-step finding. Concrete Run operator guidance was subsequently supplied by the manager and is checked in R1.

## Method and custody

Selected `software-code-review` skill at `.agents/skills/software-code-review/SKILL.md`, SHA-256 `ee085d589c44f912d11a59eead8edac214f0343761d26b0d33e886a979888bca`. Root AGENTS SHA-256 `f96feb19d297c74e10048c506805b2fe3622c50cfefd6078f599724556113977`; TASK `agents/AGENT_TASK.md` SHA-256 `1a13a5b00b3ce01ff8519efe6b46bcbe0cd6a5b7985e24282fa7efa2c57c8fb7`. Prior reviewed NativeHistory/RoleLifecycle and run review basis remain referenced by the author record. No product/Design/Git mutation, native supplier/model/auth/network operation, transcript cache, or new instruction adoption. Authorized original-owner repair is assessed separately in `V3-I1-HISTORY-INTEGRATION-R1.md`; this NOT READY history is retained.
