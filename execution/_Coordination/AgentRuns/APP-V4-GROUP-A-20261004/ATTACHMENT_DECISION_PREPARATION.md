# Attachment preparation — exact text bound and pre-send identity

2026-10-05; TASK `/root/group_a_execution/design_aac`, parent WORKING_ITEMS
`/root/group_a_execution`; native descendant, no delegation. **Implementation disposition authorized by Root; DEL-01-05 source concurrence
received; joined independent review pending.** Only this preparation and
`changes/CC-NIR-ATTACHMENT-REF.md` are written. No governing Design/product,
network/auth/native/model/API/Git changes or execution.

## Bound choice assigned to the App implementation owner

NIR §6 AT-9/U-NIR-10 proposes a 256 KiB bound but does not adopt it. Recommend
**262,144 bytes inclusive, measured on the original file bytes** before adding
the App naming line. This is a per-file text-carrier threshold, not a whole
turn, model-token or provider limit. The wrapper's UTF-8 bytes do not count in
that threshold; the transport retains any actual independent payload limit and
reports its refusal without truncating or splitting the person's content.

Exact implementation disposition for named adoption:

> Use 262,144 original-file bytes inclusive as the App text-attachment carrier
> bound. A file within the bound that decodes as UTF-8 and contains no NUL is
> carried as one native text input, with its bytes preserved after the naming
> line. Other files use the existing NIR named-path/image carrier rules; this
> is not an upload rejection or a supplier/context limit. Show the selected
> carrier and file identity before sending, and hold changed/missing content
> for explicit confirmation or removal. Do not silently adopt a different
> bound or trim/truncate content.

Alternative choice: bound the complete wrapped element instead. That makes
carrier eligibility vary with path/name/wrapper length for identical file bytes;
it requires explaining that behavior and a different AT-9 definition. Original
file bytes are recommended because they are the stable file property stated by
AT-9 and used for selected/submitted content identity. No supplier evidence
establishes 256 KiB as a context limit or guarantees suitability for every
provider. This is an App implementation-owner choice within authorized scope, not a
discovered supplier default or a reserved human act.

Eligibility and failure behavior under the recommendation:

| Case | Action |
| --- | --- |
| UTF-8/no NUL, file byteLength ≤262144 | Native `text` element; retain BOM, CRLF, trailing whitespace and final-newline state exactly. |
| File >262144, non-UTF-8 or NUL-bearing non-image | Existing `path-named`; describe as named, not supplied bytes. The text factory returns carrier-needed rather than deleting/rejecting the attachment. |
| Image | Existing image carrier; image read/provider adoption remain unobserved without actual evidence. No generic upload is introduced. |
| Picker dismissed or item removed before send | No dispatch. Any prepared evidence remains marked not sent by correlation, never counted as supplied. |
| Changed/missing/unreadable at submission | Hold the whole pending submission; no native request. Show cause; confirmation reselects/identifies current bytes, removal is the other choice. Reread at actual dispatch again. |
| Supply evidence persistence or correlation persistence fails | No dispatch. Preserve any partial preparation as not sent; no best-effort send. |
| Native write/result uncertain, supplier refusal, cancellation after send | Preserve the actual request outcome/unknown; no automatic retry. Subsequent person's send is a new submission reference. |

Use the same byte buffer for submission file identity, UTF-8 decoding and element
composition; never hash one read and parse another. Element identity covers the
whole wrapped UTF-8 element separately from file identity. AT-9's naming line is
naming-only; its resolved wording/escaping belongs to the reviewed factory (names
and paths with line feeds/quotes must not inject extra framing). No new cached
file copy or attachment lifetime is required for text bytes in the native input.
AT-6 later checks remain separate from immutable selection/submission facts.

## Ordinary technical design: pre-send reference

AT-3/SQ-A requires a supply record before send, but `turn/start` does not provide
its native turn ID until its response. Recommend the named change packet's
explicit App-owned submission reference and later native correlation. It uses
the existing schema's string field without inventing a native ID or weakening
record-before-send. **String validity alone is not adoption:** the field meaning,
prepared/sent distinction and consumer correlation require named review.

One reference per complete pending submission/ordered input list, minted by the
host before evidence persistence: `submission:<opaque UUID>`. Each attachment has
its own attachmentId and immutable record with that same turnRef. The resolver
maps to the existing HOSTING client request full generation/request ID/method/
thread, then its observed response/native turn. It records no transcript copy
or new RS event kind. REC/RS source owner has confirmed the source fit and need for explicit
submission/thread pointer association absent from current HOSTING client schema;
see the named packet's recorded return. Exact metadata placement/API and HOSTING
integration still need common reviewed terms before connected dispatch; no
implemented binding or independent approval is claimed.

## Disjoint work and connected point of need

Ready factory work is selection/submission byte snapshots, carrier eligibility
against an explicit chosen bound, input ordering, native UserInput composition,
immutable supply evidence and unknown/failure outputs. The factory must use the named implementation-disposed bound after the
required model-context concurrence; no arbitrary or supplier-derived default
is inferred. A metadata receiver/resolver
can be built against the named proposed contract after independent review.
Shared transport/UI integration waits for receiving owner concurrence and repaired
history/ROLE reviews, then reuses their custody and journal. It may not add role
instructions, a model default or a parallel transcript.

WR TT-2/TT-3 and NIR AT-8 permit draft trial composer prefill only; no send before
the person's action, no run, no registered workflow guidance, no A15 evidence.
NIR §7 consumes WR draft transitions/ledger outcomes and does not invent them.
Registered-run start/end text comes from WR TX-1…TX-5 and is placed as TC-2 defines;
ROLE remains fixed-lifetime conversation guidance.

Steering remains an independent native transport path: maintained TurnSteerParams
requires threadId, input and observed expectedTurnId; mismatch is refused with
no fallback start. Text-only steering does not depend on file-carrier bound,
attachment persistence or this reference choice. Interrupt remains RECOVERY
DEF-3, distinct from run-end/process-stop. No attachment/lifetime blanket hold.

## Examination and ownership

Before adoption: independent contract review, boundary 262143/262144/262145-byte
cases, wrapper-overhead cases, changed/missing/same-name files, record/correlation
persistence failure, pre-dispatch cancel, uncertain native write and late response
with no duplicate send. Candidate-native witness observes actual selected-file
input and request correlation; provider adoption remains unobserved. Model/
schema pass alone cannot establish native send or provider receipt.

App implementation owner with DEL-01-05 model context disposes bound; NIR
owner owns carrier/view; HOSTING owns request identity,
write/outcome evidence; RECOVERY owns session/observer history; RS owns cited
content/evidence interface, not invented attachment event kinds; WR owns draft/
trial outcomes; ROLE owns fixed guidance. Parent integrates named consumer changes.
Unsupported verification and act controls are separate unchanged work.

## Exact local source hashes

- `projects/chirality-app-v4/execution/PKG-01_Native App and third-party harness integration/1_Working/DEL-01-04_Native requests, outcomes and attachments/Design/NATIVE_INTERACTION_RECEIVING.md`: `f9794dcc24d55b813b760daa0f120d9fc53c4893282e907b550e60cdb085ab7a`
- `projects/chirality-app-v4/execution/PKG-01_Native App and third-party harness integration/1_Working/DEL-01-04_Native requests, outcomes and attachments/Design/nir.attachment-supply-record.schema.json`: `eb9e965df9f5c562b000991aaf23f2e8541f47d33d38c37910a13e95daa87850`
- `projects/chirality-app-v4/execution/PKG-01_Native App and third-party harness integration/1_Working/DEL-01-04_Native requests, outcomes and attachments/ScopeOfWork.md`: `8434cc47ec28e1397e7dae548183543567f0b5fcfdefaebc0b44bc1f709aacf3`
- `projects/chirality-app-v4/execution/PKG-01_Native App and third-party harness integration/1_Working/DEL-01-02_Durable execution and request recovery/Design/EXECUTION_AND_RECOVERY.md`: `9b443fbc5e7fc617e51e18c4cb8aec7af0d429bc7fefe3e0ec9e52f968aa79d1`
- `projects/chirality-app-v4/execution/PKG-01_Native App and third-party harness integration/1_Working/DEL-01-01_Stock Codex hosting and supplier contract/Design/HOSTING_BOUNDARY.md`: `47b8f1c6fb01e1f495099b06cd3fc10e95d03c032e8d122ede4378f28e194087`
- `projects/chirality-app-v4/execution/PKG-02_Workflow and role portability/1_Working/DEL-02-02_Workflow-making workspace and registration/Design/WORKSPACE_AND_REGISTRATION.md`: `5ed5da8842b32b87ae68db3476192a55fc8ff151802684b10bdca16eaa8b8d8b`
- `projects/chirality-app-v4/execution/PKG-02_Workflow and role portability/1_Working/DEL-02-04_Additive role selection and supply/Design/ROLE_SUPPLY.md`: `b279a23a5c8d8b2170618a062b3a5ccc3ea07a1cecdfcec7c61d0320f6559ba9`
- `projects/chirality-app-v4/app/src-tauri/resources/supplier/0.160.0/codex_app_server_protocol.v2.schemas.json`: `e77b7d1436a78f431a74b2cb263a862e92ae40d70411bc63835b47ab2168827c`

## Authority correction — 2026-10-05

Earlier packet SHA-256 `f060685296a9b54f4d9b5676072425c022d0dece54bf04898fdd30070b4d7102` described the threshold as human/owner
reserved. That was this TASK's mistaken interpretation, not an accepted ruling
or an actual human checkpoint. Exact NIR UNRESOLVED U-NIR-10 owner column is
**"App implementation owner with DEL-01-05 (model context)"**, point of need
**"Before attachment implementation"**. AT-9 labels256KiB proposed but reserves
no human decision. Root's source finding and parent launch authorize ordinary
262144 original-file bytes inclusive, UTF-8/no-NUL, existing named/image fallback
in this scope. No superseding human reservation was found in the loaded clauses.
DEL-01-05 concurrence is requested through parent; image/provider observations
remain open. Earlier proposed reasoning is retained above; active authority
disposition is corrected here, without inventing human approval.

## Current joined candidate preparation

DEL-01-05 model-context concurrence received2026-10-05 from
`/root/group_a_execution/design_hosting_access`: ordinary per-file262144 bound
with UTF-8/noNUL and existing carriers fits; not supplier/provider context
limit, image/provider witnesses remain open. Owning NIR-v0.4 prose/schema
descriptions/example and prototype candidates prepared. The lean HOSTINGv0.10
submissionAssociation with ordered supplyRefs supersedes the earlier proposed
NIR companion; no companion schema/store was created. Existing custody outer
fields own fullgen/RPC/method, NIR owns per-attachment refs and immutable token.
Native-path identity must remain lossless, distinct from display; no lossy
path dispatch, file-copy/cache, new transcript or RS kind is selected.

Local model checks29/29 plus existing162/162 pass; full canonical output in
DEL-01-04 Design/prototype/results/RUN_2026-10-05_ATTACHMENT_SUBMISSION.txt.
Joined actual HOSTING schema validation/source-owner review remains pending
before product adoption. Steering remains independent.
