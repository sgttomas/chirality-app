# CCE-CALL-CUSTODY-01 — dormant original-call custody

PROPOSED SOURCE ADOPTION AND IMPLEMENTATION BRIEF; not accepted policy or code.
Basis: main `3cbfac7b8eb49aaee9ceb2068125319b1995f8aa`; reviewed route assessment
`27823310ce89f843382993f196deb3c85499ca5f` (PR #1189, independently READY).
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
    "claimIds": {"type": "array", "minItems": 1, "uniqueItems": true, "items": {"type": "string", "minLength": 1}}
  }
}
```

These are untrusted selectors, not accepted base identity, authority or a sealed
brief. Dormant handling performs schema validation only: no filesystem resolution,
base acceptance, writes or managed records. Later C3 resolution must reject escape,
staleness and missing claims under the associated project before sealing intent.
No role, permission, home, policy or output/write scope may be supplied as authority
through arguments. Existing transport limits continue to apply; this slice does
not invent new accepted project limits or silently truncate arguments.

## Offer and original-call lifecycle

The definition is offered only through a test-only activation on a fresh manager
start. Ordinary production construction cannot activate it and emits no new
`dynamicTools`. Bind an internal pending offer to the actual original start
SourceRequest, exact sent definition and common/role guidance identity, Host
instance, home and H5. Activate only after complete write, correlated schema-valid
start result and original admitted HELP_HUMAN/WORKING_ITEMS role chain all agree.
A role string, generic binding, caller JSON or historical receipt is insufficient.
If current role custody cannot prove original admission, stop at a narrower Host
custody test; do not introduce a fake manager credential to complete the slice.

The offer belongs only to the resulting thread and current source generation.
Failed/partial start, generation closure or loss of admitted manager continuity
invalidates it. Resume/fork does not copy the offer; the pinned generated resume
and fork shapes expose no dynamicTools field. No retroactive registration.

Mint a private non-deserializable incoming-call handle only at Host's original
received-frame boundary. Bind Host/home/H5, offer identity, thread, turn, callId,
RPC request ID, receipt position and exact tool/argument values. Preserve raw
received frame in existing journal; the private handle is not a client
SourceRequest, role lease or grant. Validate shape and the offered tool before
minting. Recheck current source and unsettled original request before reply;
never accept reconstructed handles or replayed evidence. Duplicate identities
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
through existing request settlement; no success, silent drop or outstanding
request is manufactured. Preserve complete journaling, reply-write and resolution
evidence; failed writes never imply delivery. No child launch or durable managed
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
- `projects/chirality-app-v4/app/src-tauri/src/hosting.rs`: `7b9f306d7c6fc9ceeeb4178003521afcdafe5981370f0fc87418fdf35e2644b9`
- `projects/chirality-app-v4/app/src-tauri/src/native_requests.rs`: `bb3317458e40ade1e623f86ed771c196a97e07ca7e4daa8a89931b3ea6ee6992`
- `projects/chirality-app-v4/app/src-tauri/src/runtime_session.rs`: `15425f6a48b31570447ab498b2a7c92f7870b2700d75fc9de1aef891af221f97`
- `projects/chirality-app-v4/app/src-tauri/src/role_lifecycle.rs`: `549fe28fe8155217ac961a29bf3dfe43b9103de12ccad585f609894e411bf7b3`
- `projects/chirality-app-v4/app/src-tauri/src/role_supply.rs`: `83e75542baa986924823ebdf7bcefa9d6761c623e536d92eb29fd2d603a81ec2`
- `projects/chirality-app-v4/execution/PKG-02_Workflow and role portability/1_Working/DEL-02-03_Workflow execution compatibility and round-trip support/Design/EXECUTION_COMPATIBILITY.md`: `a3001809efe5e749c158a9b33aa30180e53f0c42892a4bbb6251592b35f8c0e2`
- `projects/chirality-app-v4/execution/PKG-02_Workflow and role portability/1_Working/DEL-02-03_Workflow execution compatibility and round-trip support/Design/CCE_INITIATION_ORDERING_OPTIONS.md`: `76d00c47c4ce27979f2b038b378a28aa1c9a2c465e165bf7df053ad8fdea7a56`
- `projects/chirality-app-v4/execution/PKG-02_Workflow and role portability/1_Working/DEL-02-04_Additive role selection and supply/Design/ROLE_SUPPLY.md`: `b279a23a5c8d8b2170618a062b3a5ccc3ea07a1cecdfcec7c61d0320f6559ba9`
