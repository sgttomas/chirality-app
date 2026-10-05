# Independent Unit A credential RPC review — 2026-10-05

**NOT READY for the original Unit A source: AUTH-1 is one major blocking privacy/typed-projection defect.** The original5 passing canaries do not cover unsafe values in purported nominal safe fields. This report binds the original frozen source below; evolving owner repair is not approved.

TASK `/root/group_a_execution/hosting_contract_review`, parent `/root/group_a_execution`; no delegation. Software-code-review applied against admitted basis4314747e. Only this report written. Parent granted one focused synthetic exact-source inclusion repro lane after Unit B release; lane immediately released after result. No product/Design/Git/auth/native/model/network/download mutation or operation. Source inclusion used rustc and existing compiled serde_json library, not a Cargo/full-suite replay. Owned scratch removed.

| Original exact snapshot | SHA-256 |
| --- | --- |
| hosting.rs | `3661f2d91867d5e937c9906ed5fa46a696bba5650e7adccaea9f0341fb4fc592` |
| physical sibling src/auth_rpc.rs (hosting::auth_rpc) | `fd13952e9c3b2c254fb8975ff54fe95aff57599820edb86cdbdc079ea052c74f` |
| changes/I1-CREDENTIAL-RPC.md | `cc604029e165f65d411708394da742f28c5be78b044a7ef8ea6b72c51030da10` |
| admitted source basis review | `4314747e1479ecedd8321488b9144874d7a2694faed6cd82d9c23442d9294ed1` |

Actual module origin is the sibling path declared by hosting.rs `#[path="auth_rpc.rs"]`, not a nonexistent hosting/ subdirectory. Original source hash independently confirmed in the included repro. Preserved Root/TASK/project/skill/native0.160/ACCESS origins remain; no other role activated.

## AUTH-1 — nominal fields retain arbitrary sensitive values

**Major, blocking.** auth_rpc.rs `project_frame` login result projection copies `type` and `loginId` through `fields(v,false)` without categorical/branch/shape admission. Primitive strings are cloned unchanged. A malformed type can therefore carry the synthetic key into retained SourceEvidence/journal; an API-key result can add an unexpected loginId carrying the key, despite its Unit A safe native response being type-only. `typed_observation` also returns arbitrary nativeType and does not independently validate the categorical result before public observation. A field name alone is not evidence that its value is safe typed metadata.

Independent exact-source inclusion: compile original fd139 module unchanged using rustc --test, linked only existing serde_json artifacts. Three synthetic tests, no Host/native process or real credential:

1. `project_frame({id:1,result:{type:CANARY}}, Some("account/login/start"))` must not retain CANARY. **FAIL**: projected result retains `type:"SYNTHETIC_REVIEW_KEY_CANARY_not_real"`; typed_observation has the same untrusted nativeType path.
2. `project_frame({id:1,result:{type:"apiKey",loginId:CANARY}}, Some("account/login/start"))` must not retain CANARY. **FAIL**: projected result retains loginId and apiKey type.
3. Literal valid `{type:"apiKey"}` presence control and well-formed unrelated notification identity control **PASS**.

Actual compile exit0; test **exit101,1 passed/2 failed**,0.00s test. No Host/native or real credential operation occurred; owned scratch was removed after preserving these results. This is the same declared retained-surface privacy oracle as author's original canaries, applied to omitted nominal-field vectors; no matcher/erasure or universal DLP criterion was added. I do not claim execution of SourceEvidence/journal leaks: their inclusion is directly traced from on_line passing this projected frame to source/channel/journal retention.

Repair: project only genuinely admitted literal categories and applicable safe fields for the actual method/mode. API-key response admits its type-only branch; unexpected loginId/type/shape must become explicit unavailable/redacted/unknown facts rather than an echo channel. Preserving arbitrary strings because the name is nominally allowed is insufficient. Validate source-envelope/mode/type and typed read/logout/policy standings as applicable before claiming safe typed facts; schema validation alone does not authorize unknown additional fields. Keep actual integer error code, full namespace/RPC/response occurrence/write/uncertainty and unrelated notifications, with explicit projection/not-original limits. Do not retain key for matching, hash it, silently discard the source observation or fabricate RPC settlement.

The exact two negatives and literal valid/unrelated controls must rerun on frozen repaired code. Actual receiving canaries must additionally exercise bad nominal values and wrong-mode/branch after transient release, late/closed/unadmitted response routing. GetAccountResponse bool/optional/null versus malformed account fields and LogoutAccountResponse object acknowledgment must not be inferred from arbitrary projected strings/nulls; native policy unknown/exclusion remains distinct. These are the existing safe-typed-observation requirements, not an authorized expansion to real authentication or a blanket notification filter.

## Other inspected paths and truthful original history

TransientApiKey has no Clone/Debug/Deserialize/public real-entry factory; synthetic constructor is cfg(test). Input moves into bounded serialization; raw frame is dropped after building transient bytes and only projected SourceRequest.frame retained. Wire bytes drop after actual attempt/refusal and before wait. Sensitive queue uses20s try-lock/source checks to release on queued loss/limit; it is an implementation queue bound, not physical erasure/global write/filesystem deadline. Bounded raw serialization copies are not a long-lived matcher. No actual secure-entry UI is implemented/qualified.

Generic account credential/external-token bypass and forced refresh/include-token guard refuse before send. Private route uses full-generation source/actual policy receipt, no model/config/provider/role override. Full-frame writer/source duplicate/Stop/ledger/nonattempt/actual failure/late facts follow the retained source machinery. Account scope retains nonsecret full generations beyond key release; original/closed frames project before closed-generation early return. Unparseable diagnostics from known account source become explicitly unattributed withheld evidence, while unrelated valid notification control remains byte-value identical. stderr retains count only. No saved key matcher or generic transcript scan is introduced. AUTH-1 limits the completeness of these otherwise useful targeted projections.

Author reports original **5/5 credential canaries** and **53/53 affected Host**, with ignored watchdog helper actually invoked. I read their assertions/record, not a reviewer whole-suite rerun. The initial fifth test exit101 incorrectly demanded late error admission after an actual EPIPE removed pending correlation. Existing removal was correct; corrected oracle requires unadmitted but safely projected journal/code/diagnostic occurrence and SourceEvidence.response null. This is a truthful test-expectation correction, **not** a product repair or permission to invent settlement. Original failed expectation is preserved separately from the newly confirmed AUTH-1 failures.

Return AUTH-1 to original owner, preserving this original source/reproduction and successful source predicates. Unit B actual H-key descriptors/bootstrap/config/resources, real secure-entry origin/field lifetime/UI, real credentials/Codex custody/native access remain unqualified. No source-only, synthetic pipe or current account observation establishes key validity/person identity/removal/history deletion, model/provider execution or full access completion. Same-reviewer bounded backcheck will use actual repaired seals and relevant controls, not original5/53 alone.
