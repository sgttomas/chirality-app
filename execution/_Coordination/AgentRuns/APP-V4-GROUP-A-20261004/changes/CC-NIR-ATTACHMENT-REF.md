# CC-NIR-ATTACHMENT-REF — proposed submission reference and native correlation

2026-10-05; TASK `/root/group_a_execution/design_aac`, parent WORKING_ITEMS
`/root/group_a_execution`. **Named technical proposal, independent-review ready;
not adopted or applied.** Write only this record and ATTACHMENT_DECISION_PREPARATION.
No governing Design/schema/product/Git/network/auth/native changes. Bound choice
is implementation-owned with DEL-01-05 model-context concurrence; reference
design is an ordinary technical join
requiring supplier/receiver concurrence, not another fabricated human-act gate.

## Exact proposed contract wording

> An attachment supply record's turnRef may be a native turn reference already
> observed for this submission, or `submission:<opaque UUID>` minted by the App
> host before an ordered input list is dispatched. The latter is explicitly an
> App-owned submission reference and is never presented as a supplier turn ID.
> All attachments in that one dispatch cite the same submission reference; each
> retains its distinct attachmentId/content identity. The original reference and
> selection/submission/element identities are immutable after preparation.
>
> Before sending, persist all supply records and the submission correlation
> binding to the owning conversation and complete ready generation. Bind the
> native client RPC identity in that same pre-dispatch transaction. Failure to
> preserve either evidence or binding sends nothing. The native frame contains
> the ordinary documented params only; submissionRef is not an invented wire
> field. No future supplier turn ID is fabricated or reserved.
>
> The receiving resolver reports preparation, dispatched/unknown, native refusal
> and native-turn correlation from existing client-request custody and observed
> frames. A prepared supply record alone proves the exact prepared input/carrier,
> not dispatch, receipt or provider adoption. Its supplyStanding identifies the
> carrier (bytes-in-text versus named-path); display it as prepared/not sent
> until the corresponding native write is observed. A written frame is sent,
> not proof of supplier acceptance or provider adoption. A failed/uncertain write
> stays not-sent/unknown as actually observed; never upgrade it by file text.
>
> On turn/start response, correlate using that exact full generation and RPC ID,
> confirm thread context, and attach only the returned native turn identity.
> A notification or history turn is not attributed by proximity or matching
> text. With turn/steer, use the observed expectedTurnId as the precondition;
> accept correlation only to the corresponding response turnId. Conflicting,
> missing or uncorrelated results preserve unknown with their cause. Correlation
> does not overwrite original turnRef or content identity.
>
> Cancellation before dispatch marks not sent and sends no request. Cancellation
> or interrupt after dispatch follows the existing request/turn operation and
> makes no rollback claim. Closing a view or ending a wait cannot resend input.
> Unknown/error outcomes are never retried automatically; an explicit new send
> receives a new submission reference, with prior uncertain delivery visible.
>
> On reload, use existing receiving custody/history for actual correlation;
> absent evidence remains unavailable/unknown. This join adds no transcript,
> content cache, automatic copy, upload or retention promise. Native replies are
> kept in the existing hosting evidence stream, not duplicated into supply
> records. Role guidance, workflow trial/run meaning and model choice are
> unchanged.

The persisted prepared-state interpretation must be stated in NIR §6 AT-3/SQ-A
and supply-schema descriptions together before adoption; current descriptions
say content actually put in a turn and cannot silently acquire this new meaning.
Schema 0.2's minLength string turnRef can represent the token, but structural
validity does not settle semantics or receiving persistence/API. No schema union,
new persisted correlation field or RS kind is proposed here. If owners cannot
supply a durable existing-custody binding, that precise interface remains a
point-of-use dependency; the App must not send first and backfill evidence later.

## Proposed public receiving contract

`resolve_submission(submissionRef)` returns an App-owned observation:
`{submissionRef, conversation, generation, clientRequestRef?, dispatchStatus,
 nativeTurnRef?, observationLimit?}`. This is a receiver API description, not a
new persisted schema or second authoritative store. NativeTurnRef absent before
observed correlation; references point into existing custody. A replayed/cold
reference without retained correlation does not permit native retry or claim
sent. Require explicit ownership of the existing custody binding and source
reader before production use.

## Native payload and failure preservation

For the first attachment unit, TurnStartParams carries `threadId` and the ordered
native UserInput list; other existing selected fields remain supplied by their
owners. Text attachment input is `{type:"text",text:<AT-9 line+LF+exact decoded
file bytes>,text_elements:[]}`. No generic file property, file upload, turn ID,
submission token, role instruction or model default is added to wire params.
TC-2 puts existing WR start/end text first, then person text, then attachments.
A draft retains AT-8/WR TT-3's explicit trial standing, never workflow guidance.
All changed-file/read/record failures hold before dispatch; original unknowns
and selected context stay visible. Supplier acceptance/model adoption are
independent observations, never inferred from a returned client token.

## Consumers, comparison and checks before adoption

- NIR supply factory/view/schema descriptions: explicit reference namespace,
  prepared-versus-sent meaning, immutable facts, missing correlation limits.
- HOSTING request writer and RECOVERY receiver: reserve/bind actual client RPC
  identity before dispatch, full-generation correlation and durable observation
  reader without a parallel transcript; retain late/uncorrelated responses.
- RS evidence readers: resolve the original content/supply reference with its
  actual dispatch/correlation limits; no fabricated R3 guidance/human-act kind.
- WR trial view/pointer: retain draft identity and ordinary conversation meaning;
  ROLE and history consumers preserve fixed guidance/native event custody.

Source consistency: turnRef currently is required nonempty string; UserInput
text and turn/start list types are present in maintained0.160.0; turn/steer requires
expectedTurnId; HOSTING §5 correlates full generation/client request identity,
H10 ends waiting without proving outcome; RECOVERY §4.1 observe supplies gaps
and snapshot/history limits. NIR AT-2/AT-3/SQ-A prohibits send-before-evidence.
Negative examination: successful supply preparation with failed binding sends
nothing; native error/unknown doesn't look supplied/accepted; late response joins
only its own RPC/generation; changed bytes never masquerade as selected bytes;
pre-send cancel and view reload never dispatch/retry; ordinary text steering is
not held by this attachment choice. Full connected/native checks remain to run.

REC/RS source owner `/root/group_a_execution/design_records_exec` returned a
bounded source-fit assessment by native coordination message on 2026-10-05:
turnRef string permits an App token only with named meaning; one token binds the
immutable list; current HOSTING client schema lacks thread/submission association,
so retain explicit pointer correlation at the send seam without native payload
copy, and match actual response/explicit steer target, never temporal adjacency.
No new RS kind/auto resend. This is source concurrence, not independent review
or an implemented API; sibling proposed `CC-ATTACHMENT-CORRELATION` is prepared
by that owner. Parent coordinates exact common terms and HOSTING implementation.
Named review must cover adopted descriptions and the actual receiving binding,
then parent propagates to factory, transport and view consumers.
No existing capability or acceptance criterion is narrowed by this proposal.

Source bytes and proposed bound rationale are pinned in the companion packet.

## Authority correction — 2026-10-05

Earlier packet SHA-256 `156ddc59fa012d6d42277113f0610b8fcf5b78b6a9f132490dbd5db7a638e575` incorrectly described the text threshold
as human-reserved. NIR U-NIR-10 assigns App implementation owner with DEL-01-05
(model context), before attachment implementation; AT-9 creates no human
reservation. Root authorized ordinary262144 original-file-byte disposition
within scope. No actual human approval is claimed. Reference meaning still
requires named supplier/receiver review; no Design/product change occurred in
this correction. Image/provider read/adoption observations remain open.

## Prepared owning Design update — not product adoption

Root's corrected ordinary bound disposition now has DEL-01-05 model-context
source concurrence (native message from design_hosting_access,2026-10-05):
262144 original-file bytes inclusive is a per-file carrier threshold only;
UTF-8/no-NUL and existing named/image rules fit; image/provider read/adoption
witnesses remain open. No human approval is claimed.

Latest parent direction supersedes my earlier proposed NIR-owned companion
correlation schema/store before any such file was created. It is withdrawn:
use existing HOSTING optional submissionAssociation with ordered unique supplyRefs,
outer fullgen/RPC/method and distinct prepared-not-sent/not-attempted. HOSTING
source owner supplied exact proposed successor ID
`urn:chirality:del-01-01:hosting-boundary:v0.10:client-request-record`. NIR refs
are `attachment:<existing opaque attachmentId>` resolved under owning supply
custody, all sharing the immutable submission token. No outer-field duplication,
newRS/RECkind, parallel store/transcript, nativeTID invention or automatic retry.
Prepared-only evidence after crash cannot prove no pipewrite: source unknown
remains unknown/unavailable.

NIR §6/§6.1 and U-NIR-10 now carry this named candidate; existing supply schema
shape/ID0.2 stays intact with source/ref/standing descriptions clarified.
Prototype textbound is the ordinary selected value; supply with App submission
ref reports prepared/not-sent while historical actual-turn fixtures retain
sent standing. Native path representation must be lossless, separate from display;
no lossy path dispatch or copied file cache is selected. File digest/decoding
use the same snapshot. Joined independent review with actual HOSTING successor
and REC/RS concurrence precedes product adoption. These files are prepared
contract candidates, not claims of implemented send/custody/native witnesses.

Source candidate bytes before this update:

- `projects/chirality-app-v4/execution/PKG-01_Native App and third-party harness integration/1_Working/DEL-01-04_Native requests, outcomes and attachments/Design/NATIVE_INTERACTION_RECEIVING.md`: `f9794dcc24d55b813b760daa0f120d9fc53c4893282e907b550e60cdb085ab7a`
- `projects/chirality-app-v4/execution/PKG-01_Native App and third-party harness integration/1_Working/DEL-01-04_Native requests, outcomes and attachments/Design/nir.attachment-supply-record.schema.json`: `eb9e965df9f5c562b000991aaf23f2e8541f47d33d38c37910a13e95daa87850`
- `projects/chirality-app-v4/execution/PKG-01_Native App and third-party harness integration/1_Working/DEL-01-04_Native requests, outcomes and attachments/Design/prototype/nir_model.py`: `8541651a4f90e6b1b7c7d0a529382d5941012f5d3d1603bbd928fb2498b22c8f`

## Current model check and consumer distinction

29/29 standalone attachment-submission model cases and162/162 existing
combined cases pass (exit0). Full command/cwd/environment/version and
stdout/stderr retained in owning Design result. Model assumes persistence
callbacks and actual host-writer events; it does not establish filesystem
durability, native send, image/provider adoption or joined HOSTING schema
validation. Text-size/file eligibility tests are ordinary implementation
checks, not evidence of a model context limit or human bound approval.

The owning source candidate changes NIR prose, unchanged-shape0.2 supply-schema
descriptions, one illustrative prepared-record example, prototype carrier
comment/prepared output and the new local submission model. Only existing
HOSTINGv0.10 client-custody extension owns submissionAssociation/prepared state.
Exact schema field handoff was received from HOSTING/ACCESS source owner,
with REC/RS source concurrence; actual successor schema/joined independent
review/adoption are still pending. No new NIR correlation schema or store.
Prepared candidate source/record refs are not an adopted contract/product claim.

Current owning output hashes:

- `projects/chirality-app-v4/execution/PKG-01_Native App and third-party harness integration/1_Working/DEL-01-04_Native requests, outcomes and attachments/Design/NATIVE_INTERACTION_RECEIVING.md`: `385294cc3f082dd2b890d1e2051225261887cb0ce66229b6c87ce975e9a3e08b`
- `projects/chirality-app-v4/execution/PKG-01_Native App and third-party harness integration/1_Working/DEL-01-04_Native requests, outcomes and attachments/Design/nir.attachment-supply-record.schema.json`: `6562b8efacb75a3814f59b5918cdac9210e968f008059544864fa234e550a8c1`
- `projects/chirality-app-v4/execution/PKG-01_Native App and third-party harness integration/1_Working/DEL-01-04_Native requests, outcomes and attachments/Design/nir.attachment-supply-record.example.valid.json`: `ac5f161cf90a3d890dcc9dd49574b65ec8f793b3fb7a7dba99b42a78e948bbe3`
- `projects/chirality-app-v4/execution/PKG-01_Native App and third-party harness integration/1_Working/DEL-01-04_Native requests, outcomes and attachments/Design/prototype/nir_model.py`: `e36dfc3ff4038c574c9265bbe65ccc8ac824a113f4db15c64992485a0993a843`
- `projects/chirality-app-v4/execution/PKG-01_Native App and third-party harness integration/1_Working/DEL-01-04_Native requests, outcomes and attachments/Design/prototype/attachment_submission.py`: `fca046e15803e3505dafafe2bfd14f7dffa33d5c4a1635593428ab62018de139`
- `projects/chirality-app-v4/execution/PKG-01_Native App and third-party harness integration/1_Working/DEL-01-04_Native requests, outcomes and attachments/Design/prototype/README.md`: `9f6d59448756376362e4c5b5a3be1057b7923a4574d3220f42108dbfda8849d4`
- `projects/chirality-app-v4/execution/PKG-01_Native App and third-party harness integration/1_Working/DEL-01-04_Native requests, outcomes and attachments/Design/prototype/results/RUN_2026-10-05_ATTACHMENT_SUBMISSION.txt`: `2f3c629fc431ff6bd462334091865d0bc21dc75e10caf562c8d87129958581f1`

## Joined-review repair — actual findings retained

Reviewer `/root/group_a_execution/aac_contract_review` supplied exact current
model reproductions, confirmed independently in owning offline model:
1. written submission with matchinggeneration/RPC but result.threadId=foreign
   admitted foreign-native-turn;
2. result.turn=null raised AttributeError;
3. second conflicting sameRPC reply overwrote first native turn.
Original source hash and observed outputs retained in
`Design/prototype/results/RUN_2026-10-05_ATTACHMENT_REVIEW_REPRO.json`.
These are actual defects, not hypothetical checks, and previous29-case pass
did not cover them. Bound/carrier/source choices are unchanged.

Repair follows actual HOSTING pending-only result/source behavior: only exact
fullgen/RPC written-pending source admits reply; reported thread must match
(bound context applies when absent); safe malformed/null turn handling leaves
native turn unknown and preserves source; actual native error stays refusal;
unsent/error/failed-write sources cannot gain native turn; first settled source,
receipt and native identity are preserved against sameRPC repeats. Uncorrelated
repeat retains visible cause. The model's source reference points to the original
HOSTING frame and is not serialized/copied into client custody or a new store.
NIR §6.1 states these matched-reply/first-settled constraints explicitly.

Wrong-target steer reply now settles its owning RPC as HOSTING does. The
positive target case uses a fresh owning pending RPC; a new negative asserts
that later correct sameRPC result cannot replace first wrong-target source.
This restores the agreed criterion rather than weakening a check.

Focused54/54 plus existing162/162 pass, exit0; full canonical output in
`Design/prototype/results/RUN_2026-10-05_ATTACHMENT_SUBMISSION_REPAIR.txt`.
The focused model uses actual HOSTING successor IDv0.10 and its validator
for9 source states. This repairs the earlier pending joined-schema check;
independent reviewer backcheck/adoption/product/native witnesses remain pending.
No HOSTING/shared/product/schema/Git/network/auth edits were performed here.

Frozen repair/source outputs:

- `projects/chirality-app-v4/execution/PKG-01_Native App and third-party harness integration/1_Working/DEL-01-04_Native requests, outcomes and attachments/Design/NATIVE_INTERACTION_RECEIVING.md`: `7d96396172af4e444654809bc6946acd350477faf51eaa5afc1905259cd1c7f4`
- `projects/chirality-app-v4/execution/PKG-01_Native App and third-party harness integration/1_Working/DEL-01-04_Native requests, outcomes and attachments/Design/prototype/attachment_submission.py`: `0d32ef8abfcd32837138b486e790f205c249b419020d39a6396065ee39cb871d`
- `projects/chirality-app-v4/execution/PKG-01_Native App and third-party harness integration/1_Working/DEL-01-04_Native requests, outcomes and attachments/Design/prototype/README.md`: `f07f68c3a946aa6ef3f81508ee5b48226bf47f69a48585fb9f452bd16cd8d5e1`
- `projects/chirality-app-v4/execution/PKG-01_Native App and third-party harness integration/1_Working/DEL-01-04_Native requests, outcomes and attachments/Design/prototype/results/RUN_2026-10-05_ATTACHMENT_REVIEW_REPRO.json`: `ccc288c41829ca52770f7831a3a624727d9fd2ad3abd5bfbc7dfd176384b5a5c`
- `projects/chirality-app-v4/execution/PKG-01_Native App and third-party harness integration/1_Working/DEL-01-04_Native requests, outcomes and attachments/Design/prototype/results/RUN_2026-10-05_ATTACHMENT_SUBMISSION_REPAIR.txt`: `b7f3f36ef5c8154959f54ec7b6208a4b938b031aaf7b6814dcdb0b9e80419840`
- `projects/chirality-app-v4/execution/PKG-01_Native App and third-party harness integration/1_Working/DEL-01-01_Stock Codex hosting and supplier contract/Design/hosting.client-request-record.schema.json`: `3264b5b31514f1477b48560d232f50edc3c00db5207b97557a0d4e7e0b9fa5a5`
- `projects/chirality-app-v4/execution/PKG-01_Native App and third-party harness integration/1_Working/DEL-01-01_Stock Codex hosting and supplier contract/Design/prototype/jsonschema_subset.py`: `486e9286e5aa56888b5473f1c08493a115591255685a8a7bb88b93ff2cacffc0`
- `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-GROUP-A-20261004/changes/CC-H-ATTACHMENT-CORRELATION.md`: `b3ea05c61edb99afad1b55b57ea967ae7cb30172c128debeaa6bdcec3e43724d`
- `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-GROUP-A-20261004/changes/CC-ATTACHMENT-CORRELATION.md`: `11dced0cbbea19043eeb84422a1673d9944e845380d09aa406dd1c4a24abca10`
