# C3 critical-set grammar G0.1 — proposed external carrier

DRAFT source grammar, not JSON Schema adoption, production reader, source mint or
resource policy. Basis3e8e1afc71e55abf88bada6e4ac0f6a7dbcb3b7a, reviewed reference
proposal49ba1d89. This refines that proposal for owning review; it changes no
account0.1–0.5 or message0.1/0.2 meaning and does not invent account0.6.

## 1. Grammar conventions and dispatch

Notation `T{a:A,b:B}` is a JSON object with EXACTLY the listed keys, all required.
`[T]` is an array; `T|null` explicitly permits JSON null. No omitted-field default,
coercion, unknown field, duplicate object key, trailing text, nonfinite number or
ill-formed UTF-8. Strings are Unicode scalar sequences: reject unpaired surrogates
and embedded NUL. `ID` is nonempty ASCII matching `[A-Za-z0-9][A-Za-z0-9._:-]*`.
`Text` is a string (empty permitted); `Nonempty` is nonempty Text. `Digest` is
64 lowercase hexadecimal characters. `Nat` is a canonical decimal STRING matching
`0|[1-9][0-9]*`, compared mathematically, not through floating point. No arbitrary
maximum is selected here; bounded acquisition/integer/string/array/depth budgets
must be selected and proved before a reader implementation. Empty arrays are
permitted only subject to rules below, never shorthand for unknown.

Manifest dispatch is exact pair (`chirality.c3.critical-set.proposal`, `0.1`).
This is an unadopted external format, not a new RS record or route account.
Future production readers must refuse it until explicitly adopted. No validator
retry until something accepts. Message version is selected by an explicit ref
field; message payload itself remains its unchanged source-defined shape.

## 2. Root, inventories and required slots

Manifest = {format:literal above, version:"0.1", manifest_id:ID,
undertaking_id:ID, recorder:Recorder, context:Context, local_order:Nat,
artifacts:[Artifact], sources:[Source], records:[Record], slots:Slots,
closure:Closure, limitations:[Limitation]}

Recorder = {kind:"app"|"agent"|"person"|"unknown", identity:Nonempty|null,
source_ref:ID|null, identity_verified:false}
Context = {project_source_ref:ID|null, project_state:"recorded"|"unknown"|"conflicting",
association_note:Nonempty}
`local_order` is only the manifest's producer-reported journal-local order; not
wall-clock time, human-performance order, cross-stream sequence or proof of freshness.
No governed run, human act or verified person identity is introduced.

Slots has EXACTLY these keys, each a Slot: base, answer_request, answer,
review_request, content_review, ordinary_intent, ordinary_outcome,
target_observations, manager_reconciliation, attempts, prior_journal_results,
final_account, responsibilities. All must be present.
Slot = {state:State, reason:Nonempty, record_ids:[ID], evidence_refs:[ID],
responsible:Responsibility, observation_boundary:Nonempty}
State = recorded|not_requested|unknown|missing|unavailable|stale|conflicting|not_applicable.
Responsibility = {kind:"named"|"unassigned"|"unknown", identity:Nonempty|null}
Named requires identity; other kinds require null. A duty assignment is not
performance. `recorded` requires one or more matching records; other states may
retain historical records, but may not label them current by implication.
`not_requested` and `not_applicable` require at least one source evidence ref
supporting that explicit boundary; lack of records alone yields unknown.
`conflicting` requires at least two distinct evidence or record refs and reason.
`unavailable` can have no record when a producer is absent; do not fabricate one.

Closure = {claim:"complete_recorded_closure"|"incomplete",
required_artifact_ids:[ID], historical_artifact_ids:[ID], gaps:[Limitation]}
Limitation = {id:ID, kind:"missing"|"unknown"|"unavailable"|"stale"|"conflicting"|
"representation"|"custody"|"retention", subjects:[SubjectRef], detail:Nonempty,
responsible:Responsibility}
SubjectRef = {inventory:"artifact"|"source"|"record", id:ID}.
All IDs unique within their inventory; limitation IDs unique across root and
closure. References resolve by inventory type, never search another namespace.
Root limitations and closure gaps are distinct entries; duplicate subject facts
must remain consistent. `complete_recorded_closure` concerns required recorded
bytes/references only, never truth, source authenticity or whole undertaking
completion. An unavailable producer may coexist with complete closure of the
recorded subset only if explicitly excluded from that subset and named in root
limitations; it must not imply a complete critical set for that undertaking.
Missing/changed/conflicting REQUIRED artifact or source resolution forces incomplete.

## 3. Artifacts and source references

Artifact = {id:ID, kind:ArtifactKind, bytes_method:BytesMethod, sha256:Digest,
byte_length:Nat, ref:ArtifactRef, retention_refs:[ID]}
ArtifactKind = base_account|answer_message|review_message|request_text|parsed_frame|
role_guidance|target_bytes|manager_message|attempt_evidence|prior_commit_evidence|
final_account|other_source_evidence.
BytesMethod = raw_file_bytes_sha256|decoded_utf8_sha256|
host_parsed_value_json_utf8_sha256|role_guidance_utf8_sha256.
ArtifactRef = {namespace:"c3-critical-artifact-proposed", key:Digest}
Ref key MUST equal sha256. This illustrative content-address namespace does NOT
select a filesystem path/store or promise immutability. Unknown method refuses;
`other_source_evidence` must still use one named exact method and retain actual
source kind. It is not permission to transform unknown source bytes. Artifacts
are all raw referenced bytes, not inline JSON text in this grammar. Their bytes
and storage overhead remain chargeable; no resource threshold is selected.

Source = {id:ID, evidence_kind:Nonempty, claimed_identity:Nonempty|null,
identity_method:SourceMethod|null, owner:Nonempty|null, namespace:Nonempty|null,
recording_context:Nonempty, expected_routing:Nonempty|null,
root_identity:Nonempty|null, custody_identity:Nonempty|null,
generation:Generation|null, receipt_position:Nat|null,
request_attempt_position:Nat|null, artifact_id:ID|null,
rs_resolution_at_write:"resolved"|"unresolvable"|"not supplied",
liveness:"recorded_current_at_observation"|"historical_after_source_close"|"unknown"}
Generation = {app_session:Nonempty, home:Nonempty, spawn:Nat}; spawn>0.
SourceMethod = raw_file_bytes_sha256|decoded_utf8_sha256|
host_parsed_value_json_utf8_sha256|role_guidance_utf8_sha256|
original_host_request_identity|original_host_event_identity|
original_role_supply_identity|filesystem_object_identity|original_attempt_identity|
original_commit_receipt_identity.
Resolved Host request/event sources require artifact_id retaining the actual
selected parsed frame or exact source-owned evidence projection. Its original
RPC/thread/turn/item identities and projection/redaction limits must be checked
by the owning method; opaque claimed_identity text cannot replace those joins.
Absent original metadata stays unavailable and cannot be fabricated.
These method names are proposed explicit design tags requiring source-owner
mapping, not asserted existing supplier/RS values. The raw method must match
Artifact.bytes_method when the source identity is defined by that artifact hash.
Unknown/unmapped method refuses a supported observation claim; retain unavailable
diagnostic rather than guessing. Actual source evidence kind is preserved as
supplied, never relabeled generic carriage manifest to hide distinctions.

Resolved requires claimed_identity and identity_method. Not supplied requires
both null, artifact_id null and liveness unknown. Unresolvable retains known
claimed identity/method if available, never manufactures them. Host event methods require Generation, receipt_position and custody_identity.
Host request identity requires Generation and custody_identity, not a received
event/reply position: receipt_position must be null for request identity.
request_attempt_position may be null when no actual attempt position is available;
when supplied it must be the source-owned send/attempt position, not a fabricated
receipt cut. Event identity requires request_attempt_position=null; role supply
requires custody_identity and root association; filesystem identity requires root
and custody identity. None of these declarative values proves actual custody.
Byte equality from another source never substitutes for the original identity.
Source `resolved` means only recorded source resolution, not more than source says.

## 4. Typed records (closed alternatives)

Every Record is {id:ID, kind:K, source_refs:[ID], historical:boolean, data:D}.
Choose EXACTLY the data definition matching K; no extra fields. Every record
has at least one source_ref except absent/unavailable slots, which contain no
invented record. Every artifact/ref field below resolves to the named inventory.

base / Base = {artifact:ID, account_format:"chirality.connector.route-account",
account_version:"0.4", account_id:Nonempty, crp_source:ID, question_id:Nonempty}.
Owning0.4 schema+semantic validation on exact raw bytes; account ID/question must
match; canonical CRP path/root/physical identity are source checks, not inferred
from raw hash. Exact claim/fact/comparison/gap/contradiction IDs remain source-owned.

answer_request or review_request or ordinary_intent / Request = {
request_text:ID, base_record:ID, answer_record:ID|null,
request_source:ID|null, purpose:"answer"|"content_review"|"ordinary_operation",
dispatch:"not_dispatched_observed"|"unknown"|"written_observed",
intent_commit_source:ID|null, tracked:boolean, intended_target_sources:[ID]}.
Kind fixes matching purpose. review_request requires answer_record; answer_request
requires null; ordinary_intent may cite known answer or null. `written_observed`
requires actual request_source; not-dispatched requires source_refs supporting
that negative. Unknown may retain incomplete request source. Tracked intent is
not proof of dispatch. Untracked has null intent_commit_source and explicit limit.

answer or content_review or manager_reconciliation / Contribution = {
message_artifact:ID, message_format:"contribution-message"|"manager-reconciliation-proposed",
message_version:"0.1"|"0.2"|"unadopted", base_record:ID,
answer_record:ID|null, review_record:ID|null, request_record:ID,
role_source:ID, final_item_source:ID, terminal_source:ID,
related_outcome_records:[ID], related_target_records:[ID]}.
Answer selects contribution-message0.1 or0.2 explicitly, owner answer schema and
exact support rules; answer_record/review_record null. Content review selects
message0.2 and reviewed_content_only, exact answer required, review_record null,
related outcome/target arrays empty. Manager reconciliation is unadopted proposed
message format/version ONLY; its producer/content validator is absent, so no
supported recorded reconciliation until separately reviewed. Keep its slot
unavailable rather than accepting arbitrary text as a completed contribution.
Actual joins require original request/role/item/terminal and distinct manager
conversation. Declarative records alone cannot mint them.

ordinary_outcome / Outcome = {request_record:ID, terminal_source:ID|null,
tool_sources:[ID], standing:"unknown"|"terminal_failure_observed"|
"terminal_success_observed"|"tool_completion_observed", target_record_ids:[ID]}.
Terminal standing requires terminal_source; tool-completion requires nonempty
tool_sources. No outcome stands for independent target observation or manager act.

target_observation / Target = {phase:"preimage"|"postimage"|"reread",
path_text:Nonempty, project_source:ID, file_source:ID, artifact:ID,
request_record:ID|null, byte_start:Nat|null, byte_end:Nat|null}.
Both offsets null for whole bytes; otherwise both supplied with start<=end<=raw
artifact length; range is zero-based half-open. Path is a recorded locator,
not path authority; NUL already forbidden. Each observation independent; matching
hash cannot substitute root/file/custody identity. No invented preimage.

attempt / Attempt = {domain:"supplier"|"journal"|"final_account",
original_source:ID, subject_record:ID|null, intended_subject:AttemptSubject, outcome:AttemptState,
reconciliation_sources:[ID], unresolved:boolean}.
AttemptState = not_dispatched_observed|dispatch_unknown|in_flight_observed|
terminal_failure_observed|terminal_success_observed|write_uncertain|
refused_before_write_observed|confirmation_unavailable.
Unknown/inflight/write_uncertain/confirmation_unavailable requires unresolved=true.
Reconciliation adds observations; it never changes original outcome. Resolved
later state may be described through reconciliation without deleting this record.

prior_journal_result / Prior = {journal_id:ID, revision:Nat,
subject_sha256:Digest|null, receipt_source:ID|null, attempt_record:ID|null,
use:"historical_subject_identity"|"required_recovery_dependency", artifacts:[ID]}.
At least receipt_source or attempt_record required. Required dependency requires
nonempty artifacts. Historical identity need not retain entire prior snapshot;
no recursive all-snapshot chain. Subject hash is prior content, never current
manifest self-hash or future confirmation. Unresolved attempt cannot be demoted
to historical-only to discard its required evidence.

final_account / Final = {format:"chirality.connector.route-account", version:"0.1"|"0.2"|"0.3"|"0.4"|"0.5",
artifact:ID|null, account_id:Nonempty|null, publication_source:ID|null,
attempt_record:ID|null, outcome:"confirmed_original"|"uncertain"|"refused"|
"not_attempted_observed"|"unknown", prefinal_prior_record:ID|null, intended_subject:AccountSubject,
confirmed_binding:ConfirmedBinding|null}.
Declared version dispatch is explicit source-owned version only:0.1/0.2 owning
shape rules,0.3/0.4 owning semantic rules,0.5 selected read-only semantic rules.
Unknown version has no Final record and remains unavailable diagnostic, never
permissive parse.0.5 cannot claim a supported current publication producer or
confirmed_original through the existing shared writer. Confirmed_original
requires artifact/account_id/publication_source whose original evidence includes
full definite BoundReference. Uncertain requires final-account Attempt. Existing
0.1–0.4 publication needs no prefinal_prior_record; read-only0.5 unchanged. ONLY a
future separately adopted carrier-linked path may require prefinal binding.
Journal failure cannot overwrite confirmed account source. Cold matching bytes
cannot synthesize publication_source or confirmed_original.

responsibility / Duty = {duty:Nonempty, responsible:Responsibility,
standing:"outstanding"|"unknown"|"reported"|"not_required",
contribution_records:[ID], explanation:Nonempty}.
No performed/accepted/waived enum; reported contribution is not verified duty.
Not_required needs source-grounded reason; unknown cannot become unassigned by
inference. Human acceptance/reliance/coordination remain actual owner obligations.

Slots constrain kinds: single selected base/answer/content_review/final_account
when recorded; answer_request/review_request each selected single request;
ordinary_intent/outcome,target_observations,attempts,prior_journal_results and
responsibilities collections; manager_reconciliation unavailable pending source.
Stale/conflicting slots may retain multiple historical candidates, never choose
latest. Each record ID can appear only in its matching slot. Record edges form a
DAG with base→request→contribution→later request/outcome relations; forward file
order has no meaning. No dependency cycle or unknown referenced ID is accepted.

## 5. External current envelope and cold read result

Current storage envelope is a separate proposed object, never embedded inside
its own manifest bytes:
Envelope = {format:"chirality.c3.critical-set-envelope.proposal", version:"0.1",
journal_id:ID, revision:Nat, manifest_id:ID, snapshot_sha256:Digest,
snapshot_byte_length:Nat, descriptor_source:ID|null,
observation:"current_bytes_observed"|"unavailable"|"conflicting",
original_confirmation_source:ID|null, external_sources:[Source],
external_artifacts:[Artifact]}.
Here source IDs refer to EXTERNAL storage-owner observation inventory supplied
with the read/return in external_sources/external_artifacts, not the manifest
being hashed. Its Source.artifact_id resolves only to external_artifacts and
Artifact.retention_refs only to external_sources. No envelope artifact can be
inserted into that same manifest to create a cycle. Cold input MUST have
original_confirmation_source=null; an original live return may supply it only
under storage owner custody, not from deserialized envelope JSON. This is a
source constraint, not a property enforceable by a string field. Current raw
hash/length are recomputed externally. An observed descriptor is not proof of
caller acknowledgement, dispatch, current authority or rollback resistance.
Manifest prior_journal_results contains only receipts/attempts already available
at preparation. A later manifest may record an earlier result, never its own
successful/failing acknowledgement before that result exists.

ColdResult = {format:"chirality.c3.critical-set-read.proposal", version:"0.1",
manifest_id:ID, snapshot_sha256:Digest, diagnostics:[Diagnostic],
closure:"resolved_recorded_subset"|"incomplete"|"conflicting",
source_authenticity:"not_established_by_cold_bytes",
live_authority:"not_restored", unsupported_producers:[Nonempty]}.
Diagnostic = {subject_kind:"artifact"|"source"|"record", subject_id:ID,
read_state:"resolved"|"not_supplied"|"missing"|"changed"|"unreadable"|
"conflicting"|"not_checked", detail:Nonempty}.
Exactly one diagnostic per inventoried artifact/source/record, no unknown IDs.
`resolved` artifact means read original bytes match method/hash/length; it says
nothing about actual source custody. Record resolved means its referenced
recorded content passed specified consistency checks, not real performance.
Conflict relationships are explicit even if each competing artifact individually
resolves. Source closure or stale relationship does not turn intact historical
bytes into missing/changed bytes. Not_checked is no assessment, not unresolvable.
A manifest's own complete claim is not trusted: result derives from actual
bounded resolution and owning validators. EVERY required artifact and source dependency must have actual read diagnostic
resolved for resolved_recorded_subset/complete recorded closure. ALL other read
states, including not_supplied and not_checked, prevent it. Historical write-time
resolved claims alone do not establish read resolution. An unavailable producer
slot with no fabricated/rooted dependency may be recorded, but the undertaking
remains incomplete; historical-only artifacts retain their separate exception.

Relayed distribution-manager RS receiving guidance (not historical RS-owner
concurrence/adoption): preserve original rs_resolution_at_write literal unchanged
and report the separate carrier Diagnostic. NO automatic diagnostic→RS coarse
projection in this first grammar. Existing RS read resolution belongs to its
owning reader. Never overwrite write-time observation or emit richer states as
accepted RS literals. The new format is external; no RS kind/field/order/capture
meaning changes are authorized. Calling this a carriage manifest is conditional
on later carrier selection, not permission to relabel original evidence kinds.
The full receiving note was subsequently read at merged8a057f7d6c72eb3f8ab33cda8b51e66d78438cc4,
SHA51921d9d54a4bf26d2d2303284482ecfd08625b6fec5452dd7e43fe692a3e14e.
It is a new attributed distribution receiving assessment with independent review,
not historical RS-owner concurrence or format adoption.

## 6. Required cross-record and cold invariants

- Resolve base0.4 through exact owner validation, then enforce answer support IDs,
  all carried base gaps/contradictions, and content-review exact answer hash and
  claim coverage using explicitly selected message validator. Unknown schema or
  absent proposed reconciliation validator yields unavailable, not acceptance.
- Check ArtifactKind/method against use: base/final raw_file_bytes; answer/review/
  request/manager message decoded_utf8; parsed_frame uses named parsed method;
  role guidance uses role method; target bytes raw_file_bytes. Unknown methods
  or same-byte different semantic kind cannot bypass selected owner rules.
- Check original source tuple separately from raw hashes. Host request/result/
  item/terminal generation/position relations must use their owning source rules;
  same stream same position cannot have conflicting identities. Numerically
  ordering unrelated streams is forbidden. Distinct manager source is required
  for actual review claim; role JSON is not a capability. Absent producer cannot
  be repaired by internally consistent asserted fields.
- No bare hash/mutable slot is a required immutable-retention warrant. Storage
  owner must independently guarantee required raw artifact survival across
  replacement. Historical subject identity does not recursively retain every
  old snapshot. Required pre-final evidence and unresolved attempts remain exact
  required dependencies; relabeling them historical to delete them refuses.
- Permit durable truthful gap/unavailable/loss reporting. Do not fabricate the
  missing artifact. Preserve previously retained critical bytes and original
  unresolved attempts. Replacement that destroys those bytes, or completion/
  retirement based on unresolved dependencies, refuses. External actual loss
  can be reported without pretending it was prevented.
- Preserve attempt domain and original outcome. Later observation is additive.
  Definite final BoundReference plus failed journal update remains two outcomes;
  matching cold account bytes never create original confirmation or hot token.
- Existing0.1–0.4 CRP/CAM incremental publication remains ungated by this carrier;
  selected read-only0.5 unchanged. Future carrier-linked final account needs its
  own adoption before requiring exact surviving pre-final journal references.
- W2 ordinary observation only: no controlled writer, per-edit policy classifier,
  A5/A12 reinterpretation, hidden supplier veto or new global dispatch permission.
  Tracked intent precedes newly initiated request only under actual Host route;
  untracked supplier work gets no invented intent. Current file equality is not
  exclusive causality or manager reconciliation.
- No source-producer proof, verified actor identity, performed duty, acceptance,
  reliance, whole-product readiness or live permission from declarative records.
  Shape/semantic consistency and actual producer/storage qualification remain
  distinct. Unsupported new format cannot enter existing production paths.

## 7. Exact gaps and review boundary

This is sufficient to review proposed structural vocabulary and conditional
relations, not a release-ready parser. Still required: source-owner mapping of
new method tags to actual methods, exact Host/role/currentness joins, unavailable
producer handling, final-account owner validation/version qualification, complete fixed
parser/traversal/acquisition resource envelope, real immutable-reference/store
retention coupling and reader dispatch adoption. Final carrier selection and
N/S/D/T/Q remain open; no implicit maximum from these arrays/strings is a promise
of unbounded implementation. No implementation checker or schema was written.

Cases accompany this grammar as designed definition vectors. Host, CRP/storage,
Group C and RS receiving review must assess the exact frozen draft. No new RS
schema is needed merely to use an external RS-style reference proposal if actual
RS fields/readers/meaning remain unchanged; if that condition fails, return for
an explicit RS amendment. Actual historical RS-owner concurrence is not claimed.

## 8. Complete ID lookup table and computed closure

No ID-field lookup searches multiple inventories. Same lexical ID in different
inventories is permitted but never aliases. A wrong-domain or wrong-record-kind
lookup refuses even if another inventory contains that text.

| Field | Sole lookup domain / meaning |
|---|---|
| Manifest.manifest_id, undertaking_id; Recorder.identity; Responsibility.identity; Context.association_note | Declared identities/text, not inventory lookups or authority |
| Recorder.source_ref, Context.project_source_ref | manifest sources (nullable only as declared) |
| Slot.record_ids | manifest records, exact slot-kind rules |
| Slot.evidence_refs, Record.source_refs | manifest sources |
| Limitation.subjects | SubjectRef explicitly tags artifact/source/record inventory |
| Closure.required_artifact_ids, historical_artifact_ids | manifest artifacts |
| Artifact.retention_refs | manifest sources; external artifact uses external_sources only |
| Source.artifact_id | manifest artifacts; external source uses external_artifacts only |
| Source.claimed_identity/root_identity/custody_identity/generation/receipt_position/request_attempt_position | Original source metadata, never local-ID lookup |
| Base.artifact | artifacts of kind base_account |
| Base.crp_source | sources |
| Request.request_text | artifacts of kind request_text |
| Request.base_record | records of kind base |
| Request.answer_record | records of kind answer |
| Request.request_source, intent_commit_source, intended_target_sources | sources |
| Contribution.message_artifact | artifacts: answer_message/review_message/manager_message matching record kind |
| Contribution.base_record/answer_record/review_record/request_record | records: base/answer/content_review and matching answer_request/review_request; reconciliation request producer unavailable |
| Contribution.role_source/final_item_source/terminal_source | sources |
| Contribution.related_outcome_records/related_target_records | records: ordinary_outcome/target_observation |
| Outcome.request_record/target_record_ids | records: ordinary_intent/target_observation |
| Outcome.terminal_source/tool_sources | sources |
| Target.project_source/file_source | sources |
| Target.artifact | artifacts of kind target_bytes |
| Target.request_record | records of kind ordinary_intent |
| Attempt.original_source/reconciliation_sources | sources |
| Attempt.subject_record | records: matching request kind for supplier, prior_journal_result for journal, final_account for final_account; null permitted when no independently existing subject record; no cycle allowed |
| Prior.receipt_source | sources |
| Prior.attempt_record | records of kind attempt, domain journal |
| Prior.artifacts | artifacts; use flag distinguishes historical from required dependencies |
| Final.artifact | artifacts of kind final_account |
| Final.publication_source | sources |
| Final.attempt_record | records of kind attempt, domain final_account |
| Final.prefinal_prior_record | records of kind prior_journal_result, required dependency if future adopted path requires it |
| Duty.contribution_records | records of kind answer/content_review/manager_reconciliation |
| Envelope.manifest_id/journal_id/revision | external subject identities; manifest_id must equal decoded manifest, not a source lookup |
| Envelope.descriptor_source/original_confirmation_source | envelope external_sources ONLY |
| Diagnostic.subject_id | inventory named by Diagnostic.subject_kind in manifest ONLY |

Record.kind is exactly one of the data alternatives in §4; slot mapping is exact:
base→base, answer_request→answer_request, answer→answer,
review_request→review_request, content_review→content_review,
ordinary_intent→ordinary_intent, ordinary_outcome→ordinary_outcome,
target_observations→target_observation, manager_reconciliation→manager_reconciliation,
attempts→attempt, prior_journal_results→prior_journal_result,
final_account→final_account, responsibilities→responsibility.
Every record must appear exactly once in its matching slot. No hidden/orphan
record; all retained attempts, including unresolved historical attempts, occur
in attempts. A selected predecessor cannot vanish by simply omitting its ID:
replacement validation must compare prior state's required critical set/attempts
and preserve or explicitly account for actual external loss, never destructively
drop retained evidence. With no prior state available, cold validation reports
replacement-preservation unassessed, not proven.

Required closure is computed, not chosen by the declared list. Roots are ALL
Slot.record_ids, Slot.evidence_refs, Recorder.source_ref and Context.project_source_ref
when nonnull. Traverse every mapped record/source/artifact edge in the table,
including artifact retention_refs. All reached artifacts are required EXCEPT
Prior.artifacts reached solely through a Prior marked historical_subject_identity;
those edges preserve historical subject bytes optionally. Prior receipt/attempt
and unresolved attempts still traverse normally as required. If any artifact is
reached both ways, REQUIRED wins. A future required prefinal binding must use
required_recovery_dependency, never this exception.

Closure.required_artifact_ids must equal the computed required artifact set,
without duplicates. Closure.historical_artifact_ids must equal the computed
historical-only artifact set, disjoint from required. Every Artifact/Source must
be reachable under this traversal; an orphan refuses rather than hiding an
unbounded evidence stash. Cycles through any dependency edge refuse, regardless
of declaration or traversal order. Known source resolution cannot be inferred
from presence of an ID; unresolved or not-supplied edges retain gaps. Explicitly
unavailable producer slots without fabricated records are permitted and remain
undertaking limitations; computed closure is only the recorded subset.

A missing external raw artifact does not delete its manifest node or identity.
The immutable ref can remain with read missing and incomplete closure. No list
edit can exclude an artifact required by a selected record or unresolved attempt.
Historical-only absence is reported separately and is not silently upgraded to
resolved; it does not force retention of every obsolete full snapshot. Bounded
traversal and prior-state acquisition are still implementation holds.

For Envelope external inventories, apply the same unique-ID, typed-lookup,
method, no-orphan and no-cycle rules with descriptor_source and (live only)
original_confirmation_source as roots. These external observations do not add
self-edges into manifest closure. All Limitation SubjectRefs must resolve in
the declared inventory even when not traversal roots; an unknown external subject
may be described in detail with an empty subjects array, never fake an ID lookup.

## 9. Combined review repairs and exact publication binding

Source.owner and namespace are null when actual ownership/namespace is unknown.
recording_context names the actual recorder's known context, never an invented
source owner. expected_routing is a separately labelled expectation or null;
it cannot fill actual owner/root/custody. For not supplied, unknown actual values
remain null. Known expected routing does not establish source resolution. Existing
required method/custody conditions apply only when claiming a resolved supported
source; incomplete metadata permits gap reporting, not fabricated provenance.

AccountSubject = {account_id:Nonempty, version:"0.1"|"0.2"|"0.3"|"0.4"|"0.5",
raw_sha256:Digest, raw_byte_length:Nat, canonical_relative_path:Nonempty,
root_identity:PhysicalIdentity, directory_identities:[PhysicalIdentity]}.
PhysicalIdentity = {device:Nat,inode:Nat}.
ConfirmedBinding = {subject:AccountSubject, file_identity:PhysicalIdentity,
receipt_source:ID}.
AttemptSubject is a closed tagged union:
{domain:"final_account",account:AccountSubject,created_file_identity:PhysicalIdentity|null}
or {domain:"journal",journal_id:ID,revision:Nat,prepared_sha256:Digest|null}
or {domain:"supplier",request_source:ID|null,request_record:ID|null}.
Attempt.domain must equal intended_subject.domain. Final-domain intended subject
is exact prepared identity, not a bare account ID; absent producer/tuple means
slot unavailable or unknown without fabricated Final/Attempt data.

Final.confirmed_original requires nonnull confirmed_binding and publication_source;
other outcomes require confirmed_binding=null. Final.account_id/version and the
actual resolved artifact hash/length must equal every corresponding field of
Final.intended_subject and confirmed_binding.subject. receipt_source must equal
publication_source and independently resolve the ORIGINAL definite BoundReference:
canonical path, root, ordered directory chain, file identity, account ID/version
and raw hash must match. Byte length is verified from original exact prepared/
resolved bytes; do not invent a native BoundReference length field. Apply owning
version validation to those same bytes. Valid account A plus receipt B refuses,
even if each separately validates. A caller-constructed binding object alone is
not an original receipt. Physical identities and logical content checks remain
separate; no arbitrary path authority or relocation follows.

Canonical relative path follows the actual CRP owning reference rules, not this
proposal's invented path parser. Directory identities preserve original traversal
order including the root as supplied by the owning source; compare the entire
chain, and require its root identity equals AccountSubject.root_identity.
Final.intended_subject.version equals Final.version in every outcome. With an
artifact present, its account ID/hash/size/version must match intended_subject
also for uncertain outcomes. No existing writer or read-only0.5 scope expands.

Final.uncertain requires attempt_record of domain final_account, whose exact
AccountSubject equals Final.intended_subject, and whose ORIGINAL outcome is
write_uncertain or confirmation_unavailable. A terminal-success attempt or
foreign account/root/path/hash cannot supply uncertainty. Unknown or never-
attempted records use their separate Final outcomes; do not coerce them into
uncertain. Later reconciliation may resolve observed bytes but does not rewrite
the original uncertain attempt or create original acknowledgement.

Acyclic normal form: a Prior or Final may point to its original Attempt while
that Attempt.subject_record is null; its intended_subject retains exact identity.
This is the normal positive representation, not lost subject metadata. Never
point that Attempt back at the same enclosing Prior/Final. An independently
existing EARLIER subject record may be referenced only if identity-consistent
and the whole graph stays acyclic; file order or local_order alone cannot prove
it is earlier. A Prior→Attempt→samePrior or Final→Attempt→sameFinal cycle refuses.
Prior journal_id/revision must match referenced journal AttemptSubject. Hash,
when supplied on both prior subject and prepared attempt, must agree.

New lookup fields: ConfirmedBinding.receipt_source and supplier AttemptSubject.
request_source resolve manifest sources; supplier AttemptSubject.request_record
resolves answer_request/review_request/ordinary_intent records as applicable.
AccountSubject physical/path/digest fields and journal AttemptSubject identities
are source subject metadata, not inventory references. All new source/record refs
participate in computed closure and cycle checking under §8. No implied lookup
in external envelope inventories.

Actual definition check performed during this repair: unchanged message0.2
Draft202012 schema accepts the existing constructed answer fixture, kind answer;
this is shape compatibility only, not0.5 semantic consumer expansion or actual
emission. All grammar vectors remain designed, not executed parser tests.

## 10. Host request positions and classified dependency traversal

A genuinely registered original request may have no send attempt yet; an actually
written request may still have no reply or received-event receipt position. Keep
its original SourceRequest evidence and actual send/attempt status as supplied.
No reply, terminal or invented receipt_position is required merely to record that
request source. Authored answer/review joins still require their separate actual
completion evidence under the owning contract; recording a request alone never
completes authorship. Do not compare request-attempt positions with received-event
positions unless the Host owner expressly defines a common ordering domain.
Missing position is explicit null, not zero or a guessed latest event position.

Closure traversal assigns REQUIRED or HISTORICAL_ONLY to BOTH artifact and source
nodes/edges. Ordinary roots and ordinary dependencies are REQUIRED. The special
Prior.artifacts edges of historical_subject_identity introduce HISTORICAL_ONLY;
that classification propagates through the artifact's retention_refs and source
artifact_id dependencies, recursively, rather than resetting those sources to
required. A node reached through ANY independent required path is REQUIRED,
which then propagates to its dependencies. REQUIRED wins over historical-only.
Original unresolved attempts and all their sources remain REQUIRED; no historical
edge can demote them. Prior receipt/attempt metadata remains required as already
specified, separately from optionally retained old subject bytes.

A missing retention source reached ONLY from an optional historical subject
artifact produces historical diagnostic missing, without blocking resolved
recorded-subset closure of required dependencies. If that same source is reached
from selected current evidence or an unresolved attempt, it is REQUIRED and any
non-resolved diagnostic blocks closure. Required/historical artifact lists must
match the resulting fixed classification; source classification is derived and
used for the all-required-resolved rule. ColdResult still reports every source
and artifact, including historical-only missing references; nothing becomes
resolved merely because it is optional. No unbounded traversal or storage
implementation is authorized by this graph definition.
