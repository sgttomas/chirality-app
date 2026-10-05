# CC-H-ATTACHMENT-CORRELATION — lean prewrite attachment pointer custody

2026-10-05. PROPOSED applied HOSTING/ACCESS Design amendment after NIR and REC/RS source concurrence; fresh joined independent review before product adoption. TASK `/root/group_a_execution/design_hosting_access` under WORKING_ITEMS `/root/group_a_execution`, no descendants. Only own HOSTING/ACCESS prose/client schema/prototype and this record changed. No app, other Design, new RS/REC kind, companion correlation store/schema, transcript/base cache, product/native/model/auth/network/download/Cargo/Git/SoW/register/MEMORY changes.

## Source concurrence and model-context choice

Actual NIR U-NIR-10 assigns text bound to App implementation owner with DEL-01-05 model-context input, before attachment implementation. It does not itself reserve another human act. Earlier preparation packets describe a human bound gate; current Root/manager ordinary technical scope disposition and NIR/ACCESS concurrence correct that interpretation without rewriting historical packets or inventing human approval. ACCESS concurs with 262144 original raw-file bytes inclusive, valid UTF-8/no NUL; preserve BOM/CRLF/whitespace/final newline. Wrapper overhead is excluded from this per-file carrier threshold, not from native element identity. Existing named-path/image rules remain; above threshold is named-path, not generic upload rejection/truncation. This is an App carrier allocation, **not** a measured provider context/payload limit or image-read/provider-adoption witness. Actual native/provider refusals remain visible with no silent splitting, truncation, model substitution or user Codex policy veto. NIR owns carrier factory/threshold; ACCESS supplies this model-context concurrence. Actual factory boundary witnesses belong to NIR and actual provider/image witnesses remain open.

Native coordination source concurrence: `/root/group_a_execution/design_aac` agrees exact lean association and immutable ordered owning supplyRefs; `/root/group_a_execution/design_records_exec` confirms pointer custody, no new RS/REC kind/store, complete same-token records and cold-crash ambiguity (successor CC-ATTACHMENT-CORRELATION hash below). Manager selects this existing HOSTING client-custody extension. These are technical source returns, not independent review, native implementation or human acceptance.

## Exact source contract and representation

Successor client schema `$id`:
`urn:chirality:del-01-01:hosting-boundary:v0.10:client-request-record`.
Legacy generic client records retain meaning and remain valid. Optional field:

```text
submissionAssociation {
  submissionRef: App-only submission:<opaque unique token>,
  threadId: original native request thread,
  supplyRefs: immutable ordered unique list of owning NIR per-attachment record references,
  expectedTurnId?: present exactly for turn/steer, actual observed target actually submitted
}
```

Each owning record must resolve with its original turnRef equal to submissionRef; exact list/order/unique membership must equal the full prepared NIR list. Token alone cannot enumerate it. Missing, extra, reordered, duplicate, unreadable or wrong-token references prevent dispatch. Native complete input order/composition remains NIR/TC-2's; metadata does not copy message/attachment payloads or rebuild a transcript. Full H5 generation, RPC requestIdentity and method come from the containing client record, with no duplicated outer fields. Native params never receive submissionRef/association/guessed turn IDs. AttachmentId/supply reference namespace remains NIR-owned; minting primitive is implementation-owned, operational identity distinct from governed content digest.

After all NIR supply records are durably preserved, reserve native RPC ID and preserve this pointer in **existing client-request custody before actual scoped pipewrite**. New outcome `prepared-not-sent` with `not-attempted`, nonnull full generation/RPC and no send position represents the prewrite observation; source CR09. Successful actual write becomes existing pending/written (CR10); actual failed write becomes unknown-no-response/write-failed (CR11). Failed preparation/binding, cancellation or changed ready session/home/counter/pipe before write sends nothing (CR12). Partial/unreadable persistence sends nothing, not best-effort. IDs are consumed, never reused/reserved as future native turns. The existing request/journal source owns subsequent write/response/cancellation facts and durable publication; no new parallel source is selected here.

Prepared-only durable metadata is **not** proof a crash preceded pipewrite. After loss/reload, unavailable later evidence yields unknown/unavailable dispatch; observed noattempt/cancel or exact matched native evidence can establish only their actual facts. No automatic resend, retry on reload/view/wait loss, rollback after sent cancellation, or inferred native acceptance. Explicit new send uses new submission/attachment evidence with prior uncertainty visible.

Resolver is a read-only view of existing sources, not a persisted schema/store: association, original complete full-generation/RPC/method/thread pointer, write/outcome/limits and nativeTurnRef only from matched observed result. `turn/start` uses its actual `result.turn.id`; thread context is the bound request (maintained 0.160.0 TurnStartResponse contains turn only, no required thread field). An actually reported contradictory thread rejects correlation. `turn/steer` uses `result.turnId` only when it matches actual expectedTurnId. Missing/malformed/error/conflicting/unavailable result, foreign namespace/RPC or nearby/history/text-only evidence cannot manufacture a turn. Keep multiple submissions to the same native turn distinct. Correlation does not mutate NIR turnRef, content identity, association or ordered refs, and implies neither provider adoption nor human act.

## Prototype and focused examination

The model accepts optional association/preserve/cancel hooks only for the lean associated path. Preservation hook is a **stand-in** for the owning complete-list source validation plus durable client custody receipt. It receives pointer metadata only, never native params/text. Same transient native composition is written only after True receipt and rechecked original full generation/pipe; callback failure/exception/cancel/drift sends nothing. No generic credential-path copy or extra native field. Internal captured namespace is exported as the original full H5 object, even on scope drift; matching responses cannot use foreign same-counter custody. Derived resolver uses existing native result source; if absent, no native turn is guessed. Model does not implement actual persistence/source-reader durability or claim source readiness solely from a callback Boolean.

`python3 -B prototype/check_attachment_correlation.py`: **six focused groups pass**. Cases include before-write pointer preservation, exact input/no wire token, complete ordered list and owning token validation, missing/reordered/extra/duplicate refs, persistence failure/no send, cancel and session/home/counter/pipe drift, failed-write uncertainty/no resend, cold prepared snapshot/foreign same-counter response, concurrent out-of-order RPCs, strict turn-start result shape (not steer turnId fallback), steer target/thread/missing-result limits, independent plain-text steering, schema positives/reason-specific negatives. All exported associated/generic records validate. Uniqueness/full owning-source consistency is the preparation/reader semantic barrier, not inferred from JSON structural validity alone.

Legacy client-request fixtures retain expected results; lifecycle/register table equality 24/15 passes. Existing later-error focused controls rerun pass, preserving RT14/15 and receipt RT02/03 behavior. `git diff --check` passes in owned fences. Initial local positive prepared-schema check exposed a conditional inserted at initiator scope; condition moved to record scope before freeze, original positive control retained and all negative oracles unchanged. No hidden weakening or full network/native suite claim.

```text
PASS before-write persistence/full namespace/ordered pointers, original native input and later exact RPC native turn; no synthetic wire field or immutable-ref rewrite
PASS incomplete/reordered/extra owning list or failed/partial association persistence sends nothing
PASS pre-send cancel and session/home/counter/pipe drift send nothing and preserve original namespace
PASS failed-write uncertainty, duplicate token no-resend and cold prepared crash gap/foreign same-counter response
PASS out-of-order RPC response correlation; steer exact target/thread/missing-result checks; plain text steer independent
PASS all exported associated/generic records and prepared control validate; incomplete/null/pending/guessed-target negative cases rejected
client-request-record.missing-session.invalid.json $.generation: missing required appSession
client-request-record.counter-only.invalid.json $.generation: type object/null expected
client-request-record.invalid.json $.initiator: missing required name
client-request-record.valid.json expected valid
VC-27 (tables in HOSTING) | pass (model) | HOSTING §4.7 (24 rows) and §6.2.1 (15 rows) equal the model's tables
```

## Receiving adoption and actual point-of-use dependencies

- NIR owner: AT-3/SQ-A/schema v0.4 and factory/store/view keep prepared carrier/content facts immutable; exact ordered supplyRefs resolve by original token; show prepared/not-established versus actual written/native correlation separately. Existing carrier/fallback/image/read/adoption semantics stay. Common field source ownership remains HOSTING/NIR, not consumer-invented shape.
- RECOVERY owner: §4.1 observe/§7 source-standing must say client preparation is last App observation, not delivery proof; after loss/relaunch unresolved dispatch unknown/unavailable unless exact namespace/request source proves noattempt/cancel or matched native observation; never resend. No ledger schema/kind addition presently warranted. Existing source/journal readability/retention/durability limits apply. Do not reuse server-request ledger state as client submission proof.
- RS owner: use existing reference/evidence interfaces to point into owning supply/client/native sources with actual limits; no attachment R3 guidance/human_act/new event kind or stronger accepted/adopted claim. Resolve each reference, not an unordered filename reconstruction. Original capture/content facts remain immutable.
- I1 writer/custody implementation: native thread ownership/full generation/RPC reservation; admitted complete-list validation; actual durable pointer append before scoped pipewrite; no-write on failed/partial/unreadable record/binding; subsequent write/outcome evidence, raw late/uncorrelated replies and reader resolution through existing sources. The real prewrite storage adapter/source reader is still required and must be identified/reviewed before connected send; this model does not assert it already exists or fsync occurred. If the receiving source cannot supply the barrier, hold dispatch at that precise seam rather than add a transcript/store or send then backfill.
- NIR/I1 factory/transport/view integration: canceled-before-send, write/ack loss, cold reload crash gap, scope changes, out-of-order/foreign response and expected-steer mismatch; ordinary text steering independent. Do not silently remint/reorder metadata or auto resend. BODY/native event custody remains existing HOSTING/RECOVERY; WR trial is ordinary draft conversation, not workflow run/A15; registered start/end text and ROLE fixed guidance remain their owners' input.
- ACCESS view/docs: per-file threshold/context distinction and selected provider preserved. Actual provider/image/native/factory witnesses remain assigned, not erased by schema/model passes.

## Reserved/open matters and limits

Fresh joined independent review of the exact HOSTING/NIR/REC/RS source candidates before product mapping. Actual custody persistence durability/readability and native write/correlation/receiver tests remain implementation work; supplier/provider/image adoption requires separate witnesses. This choice adds no human approval gate, global retention/cache policy, host one-effect, user configuration veto, new model default or scope narrowing. Native generation/client request identities remain their actual source, not offer/test digests or fabricated future turns. HOSTING file is a successor snapshot after CC-H-RT-LATE; that earlier source hash remains its original candidate association, not a claim of current bytes.

## Read origins / SHA-256

Root/TASK/loop previously read; actual U-NIR10/AT9/AT1–6/SQ-A, three preparation/technical packets, HOSTING §5/H5/H10/client schema, ACCESS model/provider context and native 0.160.0 response/steer required fields selectively read. REC/RS technical packet provides their source fit; no historical worker identity or actual native/model test borrowed.

- `AGENTS.md` — `f96feb19d297c74e10048c506805b2fe3622c50cfefd6078f599724556113977`
- `agents/AGENT_TASK.md` — `1a13a5b00b3ce01ff8519efe6b46bcbe0cd6a5b7985e24282fa7efa2c57c8fb7`
- `projects/chirality-app-v4/loop/LOOP_INIT.md` — `45c23cf477e23aff1d0152189caf7e8ebfb53eca42e3a1fae87a06af8c197f28`
- `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-GROUP-A-20261004/ATTACHMENT_DECISION_PREPARATION.md` — `24c2908fd651cca447f88e50030202a04c26560e6012673ab086f0d8ad763299`
- `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-GROUP-A-20261004/changes/CC-NIR-ATTACHMENT-REF.md` — `98646f43879a45b76c5256cdc07d04fead2fdff51d071d7bd190b630161aaac7`
- `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-GROUP-A-20261004/changes/CC-ATTACHMENT-CORRELATION.md` — `11dced0cbbea19043eeb84422a1673d9944e845380d09aa406dd1c4a24abca10`
- `projects/chirality-app-v4/execution/PKG-01_Native App and third-party harness integration/1_Working/DEL-01-04_Native requests, outcomes and attachments/Design/NATIVE_INTERACTION_RECEIVING.md` — `385294cc3f082dd2b890d1e2051225261887cb0ce66229b6c87ce975e9a3e08b`
- `projects/chirality-app-v4/execution/PKG-01_Native App and third-party harness integration/1_Working/DEL-01-04_Native requests, outcomes and attachments/Design/nir.attachment-supply-record.schema.json` — `6562b8efacb75a3814f59b5918cdac9210e968f008059544864fa234e550a8c1`
- `projects/chirality-app-v4/execution/PKG-01_Native App and third-party harness integration/1_Working/DEL-01-02_Durable execution and request recovery/Design/EXECUTION_AND_RECOVERY.md` — `9b443fbc5e7fc617e51e18c4cb8aec7af0d429bc7fefe3e0ec9e52f968aa79d1`
- `projects/chirality-app-v4/execution/PKG-04_Human acts, autonomy and run evidence/1_Working/DEL-04-03_Content-bound decisions and compact run records/Design/RECORD_SEMANTICS.md` — `afcba32a9971f495163487064b7cc2afecf66daeb3d2837a304a6714a7b9ffbd`
- `projects/chirality-app-v4/execution/PKG-01_Native App and third-party harness integration/1_Working/DEL-01-01_Stock Codex hosting and supplier contract/Design/generated/0.160.0/json-schema/experimental/codex_app_server_protocol.v2.schemas.json` — `e77b7d1436a78f431a74b2cb263a862e92ae40d70411bc63835b47ab2168827c`
- `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-GROUP-A-20261004/changes/CC-H-RT-LATE.md` — `ad2a8d0fc4c9d32b1cd7754d255e0abe7a0f59657b0fd63620d1bce50ff4a654`

## Captured pre-amendment identities

- `projects/chirality-app-v4/execution/PKG-01_Native App and third-party harness integration/1_Working/DEL-01-01_Stock Codex hosting and supplier contract/Design/hosting.client-request-record.schema.json` — `becf45fd51b5ce02f5c4b937c2259f07046c44055757ed01bd23b2f7f7d614d4`
- `projects/chirality-app-v4/execution/PKG-01_Native App and third-party harness integration/1_Working/DEL-01-01_Stock Codex hosting and supplier contract/Design/HOSTING_BOUNDARY.md` — `47b8f1c6fb01e1f495099b06cd3fc10e95d03c032e8d122ede4378f28e194087`
- `projects/chirality-app-v4/execution/PKG-01_Native App and third-party harness integration/1_Working/DEL-01-05_Native OAuth-sign-in, API-key and local-provider access/Design/ACCOUNT_AND_PROVIDER_ACCESS.md` — `0f177361460a30c52615607457289c1fe275f55264cbe0d95f9c6d4e0ed0ed57`
- `projects/chirality-app-v4/execution/PKG-01_Native App and third-party harness integration/1_Working/DEL-01-01_Stock Codex hosting and supplier contract/Design/prototype/boundary_model.py` — `1cdffd0c0eec01e5e8864f9984332615828204a53f77edbd37902f6522d2b632`

## Candidate outputs / SHA-256 (record self-hash returned separately)

- `projects/chirality-app-v4/execution/PKG-01_Native App and third-party harness integration/1_Working/DEL-01-01_Stock Codex hosting and supplier contract/Design/HOSTING_BOUNDARY.md` — `5b67393fd2cf2e45c51b72b1110a1dc1bce4ad7e0f3f3749e8940270975437b0`
- `projects/chirality-app-v4/execution/PKG-01_Native App and third-party harness integration/1_Working/DEL-01-01_Stock Codex hosting and supplier contract/Design/hosting.client-request-record.schema.json` — `3264b5b31514f1477b48560d232f50edc3c00db5207b97557a0d4e7e0b9fa5a5`
- `projects/chirality-app-v4/execution/PKG-01_Native App and third-party harness integration/1_Working/DEL-01-01_Stock Codex hosting and supplier contract/Design/prototype/boundary_model.py` — `dff501d0a82a2d16c9745079217f972e0f742acd91089416e54e54552141b873`
- `projects/chirality-app-v4/execution/PKG-01_Native App and third-party harness integration/1_Working/DEL-01-01_Stock Codex hosting and supplier contract/Design/prototype/check_attachment_correlation.py` — `77f8935a5a65986048793d9ec365953f99e4ad2c1efb67e47beb82bde994916b`
- `projects/chirality-app-v4/execution/PKG-01_Native App and third-party harness integration/1_Working/DEL-01-05_Native OAuth-sign-in, API-key and local-provider access/Design/ACCOUNT_AND_PROVIDER_ACCESS.md` — `1ede1195bec56e211a8950fdc607748980c576209605f5c4ae8060443b59aedc`
