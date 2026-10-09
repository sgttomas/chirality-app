# CCE-CALL-CUSTODY-01 — dormant original-call custody

PROPOSED SOURCE ADOPTION AND IMPLEMENTATION BRIEF; not accepted policy or code.
Basis: main `27c88451e66c3825e9a8c11327f4c22d7cd48bbb`; reviewed route assessment
`27823310ce89f843382993f196deb3c85499ca5f` (PR #1189, independently READY, merged `11f3a4abbc5e6353d802d00b011bc62cabb73d6e`).
This record proposes the bounded source change needed before a dormant code
slice. Merge alone does not adopt it or authorize production registration.
No managed service, RoleSourceLease producer, supplier qualification, TASK
execution, native launch or user-config change is established here.

## Proposed contract and precise boundary

One experimental function definition, `chirality_c3_request_answer_v1`, described
as “Request one bounded C3 answer from the App managed-session service; unavailable
when that service is absent.” No namespace, deferred loading or status tool is
introduced in this slice. Its `inputSchema` is exactly:

```json
{
  "type": "object",
  "additionalProperties": false,
  "required": ["base", "question", "claimIds"],
  "properties": {
    "base": {
      "type": "object",
      "additionalProperties": false,
      "required": ["path", "id", "byteLength", "sha256"],
      "properties": {
        "path": {"type": "string", "minLength": 1},
        "id": {"type": "string", "minLength": 1},
        "byteLength": {"type": "integer", "minimum": 0},
        "sha256": {"type": "string", "minLength": 64, "maxLength": 64, "pattern": "^[0-9a-f]{64}$"}
      }
    },
    "question": {"type": "string", "minLength": 1},
    "claimIds": {"type": "array", "uniqueItems": true, "items": {"type": "string", "minLength": 1}}
  }
}
```

`question` is the exact selected base.question.id, not new question text.
`claimIds` selects IDs from that same base; an empty selection is valid, including
valid bases with claims=[]. Later resolution freezes the full base question bytes
and rejects unknown/mismatched question or claim IDs without fabricating claims.
These are untrusted selectors, not accepted base identity, authority or a sealed
brief. Dormant handling performs schema validation only: no filesystem resolution,
base acceptance, writes or managed records. Later C3 resolution must reject escape,
staleness and missing claims under the associated project before sealing intent.
No role, permission, home, policy or output/write scope may be supplied as authority
through arguments. Existing transport limits continue to apply; this slice does
not invent new accepted project limits or silently truncate arguments. Before
code release, specify bounded validation/allocation and outstanding-call caps
with boundary vectors; no unbounded retained request queue is allowed.

## Offer and original-call lifecycle

The definition is offered only through a test-only activation on a fresh manager
start. Ordinary production construction cannot activate it and emits no new
`dynamicTools`. Bind an internal pending offer to the actual original start
SourceRequest, exact sent definition and common/role guidance identity, Host
instance, home and H5. Activate only after complete write, correlated schema-valid
start result and original admitted HELP_HUMAN/WORKING_ITEMS role chain all agree.
A role string, generic binding, caller JSON or historical receipt is insufficient.
Issue only after successful role-map insertion with the exact original binding:
current reconciliation sets activeAdmission before insertion can fail, so neither
that flag nor start_admitted alone is a credential. PreparedStart observation
alone accepts supplied values and is not proof of Host custody.
If current role custody cannot prove original admission, stop at a narrower Host
custody test; do not introduce a fake manager credential to complete the slice.

The offer belongs only to the resulting thread and current source generation.
Failed/partial start, generation closure or loss of admitted manager continuity
invalidates it. Resume/fork does not copy the offer; the pinned generated resume
and fork shapes expose no dynamicTools field. No retroactive registration.

Mint a private non-deserializable incoming-call handle only at Host's original
received-frame boundary. Bind Host/home/H5, offer identity, thread, turn, callId,
RPC request ID, receipt position and exact tool/argument values. Preserve the original parsed-frame
value and receipt in the existing journal, respecting existing sensitive-source
projection limits; this is not a claim to preserve original wire bytes; the private handle is not a client
SourceRequest, role lease or grant. Validate shape and the offered tool before
minting. Recheck current source and unsettled original request before reply;
never accept reconstructed handles or replayed evidence. Classify private offers
before the default automatic error; preserve ordinary unoffered classification. Duplicate identities
and supplier resolution retain existing request lifecycle behavior.

## Response and refusal

Without activation, retain current `known-app-unsupported` / no-dynamic-tools
behavior byte-for-byte. In the test-only offered path, a schema-valid call returns
exact DynamicToolCallResponse content:

```json
{"success":false,"contentItems":[{"type":"inputText","text":"managed-service-unavailable: no TASK session was created"}]}
```

The pinned `v2.DynamicToolCallOutputContentItem` declares this inputText
variant; this is declaration checking only, not runtime qualification.
Malformed arguments receive an explicit invalid-params RPC error, no handle.
Unoffered, foreign or stale calls receive an explicit unsupported/refusal error
only while their original request is unsettled and reply-eligible. Closed or
superseded generations, duplicates and supplier-resolved calls retain existing
refusal/resolution evidence without a new reply, retargeting or delivery claim.
No success or outstanding request is manufactured. Preserve complete journaling, reply-write and resolution
evidence; failed writes never imply delivery. Check final reply eligibility
at the existing serialized prewrite cut: earlier closure/resolution refuses;
after that cut or during IO bytes cannot be unsent. Preserve actual write and
resolution order without acknowledgment, retry or delivery inference. No child launch or durable managed
session is created even when a schema-valid call is received.

## Ownership and adoption gates

| Owner | Bounded source/implementation fence and concurrence question |
|---|---|
| Group A Host | HOSTING/ADAPTER familiar-tool and server-request classification exceptions must be named for test-only offered path. `hosting.rs`: pending offer/start receipts, incoming handle custody, closure and serialized reply, maintained synthetic transport tests. Can this reuse existing locks without reverse edges or callbacks under Inner? |
| Group A native requests / EXEC | `native_requests.rs`: scoped test-only offered-call classification/settlement; a maintained small definition module and lib module declaration if needed. Adopt tool/schema and unavailable semantics; preserve all ordinary classifications and record contracts. Do not repin consumers without adoption. |
| Group A ROLE | `runtime_session.rs` / `role_lifecycle.rs` only if required to expose private original manager admission. Confirm real source chain can be proven; no generic RoleBinding/serialized evidence issuer, resupply or adoption claim. |
| Group C receiver | Confirm base/question/claims selector shape and explicit unavailable result. No producer, publish, request-status service or managed storage enters this slice. |

Source-owner concurrence and independent review precede technical selection/code.
Current HOSTING §6.1/§6.8 and ADAPTER F-9 no-tools limitation remains true in
production. Proposed exception is test-only and must not be labeled adopted
until owning source changes are explicitly selected. The later live managed
service, SL-4, TASK full-guidance admission, combined WR/role/Host cut and reverse
lock proof remain separate missing inputs. No production wrapper calls this
seam; no renderer command or Cargo feature exposes activation.

## Current-main Host integration constraint

PR #1190 merged dormant AA-CAP at the selected basis. Its Core is Inner-owned;
registration, prewrite, settlement and on_line observation are already hooked.
Ordinary callers pass no capture reservation. This proposal neither activates
that Core nor treats its readout as incoming-call custody or role admission.
Preserve frame_write → source gate → Inner ordering and release owner/source
locks before pipe IO. Do not invoke ROLE/EXEC/C3 callbacks or acquire their locks
from an Inner-held receive hook. Resolve manager admission through a reviewed
private handoff with recheck; if this requires a reverse edge, stop and revise
the source brief before implementation. Host concurrence must assess this
revised basis, not the pre-1190 hosting.rs hash.

## First proof and required negatives

Use maintained synthetic transport through the real Host start/receive/reply
path: exact offer in actual start frame, successful correlated result, actual
manager admission, original incoming call, one unavailable response, zero child
start and zero managed-session records. Also prove ordinary start has no offer
and ordinary item/tool/call remains unsupported. Test fixtures do not create a
managed session by writing records.

Reject: unoffered/wrong tool; invalid/additional arguments; digest trailing LF;
copied frame/handle; wrong role/thread/home/H5; generic bind/history-only role;
partial/failed or mismatched start; duplicate call/RPC identity; generation
closure; resume/fork with copied offer; substituted arguments; supplier resolution
before reply; failed reply write. Race checks prove invalidation before settlement
and no double reply. Later WR notice races are not “passed” by this refusing seam:
there is no TASK dispatch cut here. A later executable producer must independently
prove pending-before/preparation/prewrite/post-cut semantics after source selection.

## Consequence assessment and return

This is additive unfinished Group A-to-C connecting work under GC-8, not a claim
that completed Group A already supplied tools or managed delegation. Do not edit
its closeout. No Group D prerequisite, native Fleet dispatch claim, graph approval
UI, instruction amendment or new delegation class is proposed. A GC-7 owner
question arises only if source concurrence finds an actual contradiction requiring
reopening accepted Group A truth/group order; technical missing implementation
alone does not trigger it. Stop rather than silently relax original-role custody.

Generated experimental 0.160 declarations establish candidate shapes, not stock
runtime/model qualification. V3 launcher code is reuse evidence, not v4 adoption.
D-GOV-35 permits a class; it does not establish an executed session. No runtime
proof has been performed for this source proposal. Owner no-memory direction
supersedes memory conventions. Review returns belong in one concise run record.

## Exact basis identities (SHA-256)

- `AGENTS.md`: `f96feb19d297c74e10048c506805b2fe3622c50cfefd6078f599724556113977`
- `docs/governance_harness/_DECISIONS/D-GOV-35_delegated_harness_native_class.md`: `e7c1e532a9d46cdc27957c85003515c46b5193e21438c905cf1cfb4e56433efa`
- `projects/chirality-app-v4/app/src-tauri/resources/supplier/0.160.0/codex_app_server_protocol.schemas.json`: `7243ba241962af92ca60581f1a81808ebda4212a800f8b205f54703bcfd508c5`
- `projects/chirality-app-v4/app/src-tauri/src/hosting.rs`: `5c989bb4264ca3430040cbe05e2353c3305902d4b88f12034c92c292ee9af08d`
- `projects/chirality-app-v4/app/src-tauri/src/native_requests.rs`: `bb3317458e40ade1e623f86ed771c196a97e07ca7e4daa8a89931b3ea6ee6992`
- `projects/chirality-app-v4/app/src-tauri/src/runtime_session.rs`: `15425f6a48b31570447ab498b2a7c92f7870b2700d75fc9de1aef891af221f97`
- `projects/chirality-app-v4/app/src-tauri/src/role_lifecycle.rs`: `549fe28fe8155217ac961a29bf3dfe43b9103de12ccad585f609894e411bf7b3`
- `projects/chirality-app-v4/app/src-tauri/src/role_supply.rs`: `83e75542baa986924823ebdf7bcefa9d6761c623e536d92eb29fd2d603a81ec2`
- `projects/chirality-app-v4/execution/PKG-02_Workflow and role portability/1_Working/DEL-02-03_Workflow execution compatibility and round-trip support/Design/EXECUTION_COMPATIBILITY.md`: `a3001809efe5e749c158a9b33aa30180e53f0c42892a4bbb6251592b35f8c0e2`
- `projects/chirality-app-v4/execution/PKG-02_Workflow and role portability/1_Working/DEL-02-03_Workflow execution compatibility and round-trip support/Design/CCE_INITIATION_ORDERING_OPTIONS.md`: `76d00c47c4ce27979f2b038b378a28aa1c9a2c465e165bf7df053ad8fdea7a56`
- `projects/chirality-app-v4/execution/PKG-02_Workflow and role portability/1_Working/DEL-02-04_Additive role selection and supply/Design/ROLE_SUPPLY.md`: `b279a23a5c8d8b2170618a062b3a5ccc3ea07a1cecdfcec7c61d0320f6559ba9`
- `projects/chirality-app-v4/app/src-tauri/src/hosting_request_event_join.rs`: `9cb103da8e730be0f04cca554537acf4e2f221125e4318acf8edb58ba36276fc`
- `projects/chirality-app-v4/app/src-tauri/resources/distribution-successor/AA_CAP_CORE.md`: `be2dc9d8da83c041e57e5782946e748869211b132332761606ef87737573b477`
