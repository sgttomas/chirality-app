# C3 critical-set reference carrier — technical proposal v0.1

DRAFT for Group C, Host, storage and CRP owning review. Exact read basis
fef109a510dafa400c2f1e839e21cdbd3c84d5f8. No code, schema adoption, production
carrier, source mint, role capability, product envelope or accepted 0.6 is
created here. Existing formats0.1–0.4, proposed0.5, message0.1/0.2 and their
readers remain unchanged. Actual DEL-04-03 owner concurrence is NOT available
for this new carrier; prior reference-separation concurrence is not adoption.

## 1. Proposed technical cut and dispatch

A separate proposed carrier identity `chirality.c3.critical-set.proposal`, version
`0.1`, named C3-CS-R0.1, denotes only this reviewable definition. It is NOT a
route-account version and is never dispatched as connector.route-account0.6.
A later adopting reader must use exact format/version pair, closed fields and
explicit owner validator dispatch. Unknown/missing/mixed version, duplicate keys
or malformed types refuse; no nearest-version fallback or shape-only adoption.
Existing production readers must reject this unadopted carrier. All proposed
parser/resource bounds require a reviewed envelope; no N/S/D/T/Q is selected.

The technical cut uses an exact-reference manifest for ALL recovery-critical
artifacts, plus a retained raw-artifact closure. This is a proposal to test, not
selection against inline/hybrid. Raw artifacts still count fully toward retention
and quota; a small manifest does not make referenced bytes free. The previous
constructed comparison omitted genuine Host/role/request/target/attempt evidence;
this definition inventories those missing slots rather than inventing values.
No immutable store, path placement or persistence primitive is claimed to exist.

## 2. Complete semantic inventory

Every named slot exists, even when unavailable. No null implies success. Each
slot carries state, reason code/detail, responsible party as actually known or
explicitly unassigned, evidence refs and an observation boundary. Collections
carry stable member identity and completeness state; an empty collection alone
cannot mean no relevant evidence exists. Same question refers to exact base
question identity and original raw base bytes; no retargeting to latest.

| Slot | Meaning and exact required bindings when recorded |
|---|---|
| undertaking | Original undertaking identity/association and same opened project root observation; project path is a locator, not owner authority |
| base | Exact original route-account0.4 bytes, canonical CRP reference/account ID/hash/byte length; owning schema AND semantic validation; full question and claim/fact/comparison/contradiction/gap identities |
| answer_request | Original supplied request text, purpose and base/question/selected support bindings; original SourceRequest/complete-write/result refs and actual dispatch standing; absent structured producer remains unavailable |
| answer | Exact decoded UTF-8 emitted message bytes, message schema version, original final-item/terminal/generation/role supply joins and limits; source loss before mint cannot become historical mint |
| review_request | Original request bound to exact answer bytes/hash and base; genuinely distinct manager-role/request source, not role label; same dispatch distinctions |
| content_review | Exact message0.2 content-only review bytes when selected, complete answer-claim findings and carried gaps/conflicts; reviewed_content_only never means integration or acceptance |
| ordinary_request_intent | Actual intended ordinary W2 request text and supplied target/basis where known; journal intent commit evidence separate from actual request dispatch; untracked work has explicit not-supplied intent |
| ordinary_request_outcome | Original supplier request/write/result/terminal and tool items actually observed; event-before-response allowed; successful tool report not exclusive causality or full integration |
| target_observations | Independently observed preimage, postimage and reread, each exact path/root/file identity/method/byte refs and observation time/order where actually known; absent preimage is explicit, never reconstructed |
| manager_reconciliation | Separately observed actual manager contribution bound to exact answer, review, ordinary outcome and target observations; mere statement or a content-only review cannot fill it |
| attempts | Distinct original supplier, journal and final-account attempts, original outcomes/uncertainty and later reconciliation links; never collapse attempt identity or overwrite original uncertain result |
| prior_journal_results | Exact prior committed receipt/attempt states actually available when preparing this manifest; prior descriptor/snapshot identity and byte refs only. Current commit identity/bytes/confirmation belong to the external storage/reader envelope, not this manifest |
| final_account | Exact declared version/account ID/bytes/reference plus publication attempt and original confirmation state; unsupported final representation is unavailable, not fake0.5 |
| responsibility | Agent/manager/human duty standing and gaps, actor versus recorder, unverified identity; evidence presence never performs duty, acceptance or reliance |
| limitations | Complete unresolved missing/stale/conflicting sources, unknown effects, source/producer/representation absence and retention-resolution limits; no silent pruning |

Additional request/output identities must not be invented to fill the table.
Only the existing actually admitted source can warrant an observation. Host's
merged dormant original-call/unavailable-response seam includes a test-only
successful manager-insertion handoff. It is not a production CCE RoleSourceLease
issuer, TASK service, authored answer or joined complete critical-set mint.
This carrier introduces none. Cold records describe recorded evidence, not new
source capabilities; all actual producer availability remains an owning review.

## 3. Closed observation and resolution states

Slot state is exactly one of: `recorded`, `not_requested`, `unknown`, `missing`,
`unavailable`, `stale`, `conflicting`, `not_applicable`. These proposed states are
not accepted schema enums. `recorded` means an attributed observation is present,
not truth, acceptance or current live custody. `not_requested` requires an
explicit observation boundary; absence from a file defaults to unknown, not
never occurred. `missing` names an expected ref whose bytes cannot be resolved;
`unavailable` names an absent producer or unsupported representation; `stale`
names the changed dependent identity; `conflicting` retains all relevant competing
refs; `not_applicable` requires source-grounded reason, not convenient omission.

Raw artifact current-resolution state is separately `resolved`, `not_supplied`,
`missing`, `changed`, `unreadable`, `conflicting` or `not_checked`. Every source
ref records resolution_at_write; each cold read produces resolution_at_read,
never overwrites the historical write observation. Cold read result is a derived
view, not a rewrite of original artifact bytes. Source liveness is separately
`recorded_current_at_observation`, `historical_after_source_close` or `unknown`;
no cold read produces current live custody. Changing one domain must not silently
change another. Matching bytes after source closure do not restore liveness.

Attempt outcome is separately `not_dispatched_observed`, `dispatch_unknown`,
`in_flight_observed`, `terminal_failure_observed`, `terminal_success_observed`,
`write_uncertain`, `refused_before_write_observed`, or `confirmation_unavailable`.
Only original owning evidence can support negative-effect claims. Successful
supplier terminal and journal commit are different outcomes with separate refs.
Closure/cancellation cannot erase an observed attempt; later reconciliation adds
an observation linked to it, never rewrites uncertainty into fictitious success.
No aggregate boolean `complete`, `authorized`, `accepted` or `ready` is inferred.

## 4. Exact bytes, source identity and immutable-reference closure

Every artifact entry has a carrier-local artifact key, semantic kind, raw
byte length and SHA256, exact byte-method designation, and immutable-content
reference. Text artifacts use exact UTF-8 of the original decoded text, including
whitespace. Base account uses exact original file bytes. JSON parse/reserialize
is not the same artifact. Raw file targets may be nontext; do not claim UTF-8 or
line anchors without an applicable source method. Excerpts cite exact source
artifact plus explicit byte interval/line convention from its owning contract.

Host parsed frames use its named pinned parsed-Value serialization method, not
original wire bytes. Retain original decoded request/message text separately.
Source-reference fields are mandatory: kind; claimed identity; identity method;
source owner/namespace/root association; generation and receipt-position scope
where applicable; observed source custody identity; resolution_at_write. Actual
method and root come from the source, not whichever project is currently open.
A byte digest is not a source custody identity. Equal bytes from another Host,
RoleBinding, request, generation, root, target inode or retained source cannot
silently replace the original observation. The carrier stores evidence projection
only; no source capability is serializable or reproducible by these fields.

Immutable reference means exact bytes must remain independently recoverable
through snapshot replacement and any selected retirement, under a separately
reviewed bounded store/retention contract. A digest alone, arbitrary URI, mutable
slot/current path, in-memory Host pointer or future store promise is insufficient.
The manifest names its retained artifact inventory and closure completeness;
reference source/digest/size mismatch is changed or conflicting, not same-name
fallback. An independently stored copy may preserve raw bytes but does not acquire
the original custody or source status; these are separate explicit facts.

Required recovery artifacts may not be replaced by prose summaries or dropped
because a later state seems successful. Recording an explicit gap is permitted with incomplete closure; destructive
replacement, a complete-closure claim or retirement must refuse when required
evidence would be lost or unresolved dependencies are being treated as complete. Numeric limits and
retention allocation remain unselected; overflow must not be repaired by truncating
uncertainty. Recursive refs, cycles, duplicate keys, conflicting identical IDs,
unsupported identity methods and unresolved required dependencies refuse a
complete-closure result. A self-consistent forged closure remains recorded claims,
never authenticity proof. Parser and traversal bounds must precede reader code.

## 5. W2 ordering and final-account separation

W2 is ordinary supplier file work: no controlled writer, App operation-class
policy gate or scope-grant requirement is reintroduced. For newly App-initiated
tracked requests, durable intent confirmation precedes dispatch under actual
current Host permissions/custody. It is not a veto on unrelated Codex operations.
Untracked observations retain their missing-intent limit. Crash after intent but
before dispatch and after dispatch before outcome recording remain unknown; no
automatic replay, retry, rollback, graph write or source mint follows recovery.

A current matching target may corroborate current bytes, never exclusive writer
causality. A separately observed manager reconciliation remains distinct from
content review and supplier outcome. If unavailable, responsibility stays
outstanding/unknown rather than inventing integrated standing.

ONLY for a future carrier-linked final-account/reference path, after separate
explicit adoption, that new path must bind exact pre-final committed journal/
outcome evidence whose raw bytes survive slot reuse. Existing0.1–0.4 CRP/CAM
publication and selected read-only0.5 behavior remain unchanged. R2 is not a
blanket publication prerequisite: ordinary supported incremental publication
requires no new journal gate. Current final-account schemas do not automatically
carry message0.2 or this carrier; adoption needs a separate explicit decision.
Later journal revision may reference exact final account, avoiding a hash cycle.
Account confirmed + journal-update failed retains account confirmation in original
custody and a separate journal attempt. After restart, lost durable confirmation
is unknown even if matching account bytes are found. Journal success never means
account publication; account existence never proves original acknowledgement.
CAM tokens remain consumed; no cold revival or retirement/reset choice here.

## 6. Owning review and remaining gap

Host review: actual source methods/roots/custody, request/result/terminal timing,
closed-source handling and exact unavailable producer states; no role credential
from an ordinary call. Storage review: bounded immutable retention closure,
replacement/read acquisition, total accounting, failures/orphans and method
qualification; no claim small refs imply small retention. CRP/CAM review: final
publication and attempts/version dispatch, no hot restoration. Group C review:
semantic completeness, supports/actor/manager distinctions and W2 meaning.
DEL-04-03 actual owning concurrence is absent for this draft and must be obtained
or recorded as unresolved before adoption; no self-concurrence. Existing RS §9
informs the proposed identity/method/resolution fields but supplies no new grant,
act, run format or carrier approval.

The supplied cases are negative-definition vectors with expected outcomes, not
executed production tests. A later selected demonstrator must validate owning
schemas/semantics, exact source/custody joins and storage closure separately.
No arbitrary N/S/D/T/Q, threshold, carrier-final choice, implementation release,
product suitability, PM05 completion or whole-product90 claim follows.

### Replacement and CRP/CAM receiving constraints

Current selected content and older historical observations are separately named.
Changing the selected answer/review does not relabel old facts as current or drop
an unresolved attempt. Byte storage may deduplicate identical raw artifacts, but
source identities/custody and their different observation standings must remain
separate. Every retained required artifact must survive old snapshot replacement;
this does not require preserving every obsolete full snapshot. Never discard
uncertainty to implement the owner-selected current-status retention direction.

CRP/CAM implementation-owner receiving input for exact review (not historical
design-owner concurrence): final publication binds
exact prepared bytes and same opened root; path, account ID, declared version,
raw hash and physical storage identity remain independent checks. A bare ID or
matching cold bytes is not a publication receipt. Duplicate/missing/mismatch
refuses a unique binding; no winner, relocation or automatic retry. Confirmed
BoundReference, original Attempt and later reconciliation remain distinct.
CAM retains64 lifetime identities, one payload, no reset, second registry or cold
token hydration. This carrier cannot allocate a new hidden authority registry.
The current0.5 known-reference/base reader is narrowly bounded at1MiB plus sentinel;
that does not repair generic unknown-version acquisition. Shared production
writer supports0.1–0.4 only. This draft expands neither writer dispatch nor limits.
Actual carrier/immutable-artifact acquisition needs a separate bounded reader
contract before code; no unbounded bootstrap or resource-safety claim follows.

### Current commit envelope — self-reference prohibition

The manifest cannot contain its own raw snapshot hash, a descriptor hash that
includes that snapshot hash, or original confirmation of its own publication.
At preparation it may record only prior committed receipts and attempts already
observed, and their exact evidence. Its intended journal identity/revision may
be supplied as non-confirming selectors, never a claim of committed current state.

The storage owner computes current raw snapshot bytes/hash and descriptor binding
outside the manifest. The external reader/storage envelope names the observed
current journal/revision, descriptor identity, selected snapshot raw hash/size and
current read resolution. A live storage return may separately attest its actual
original confirmation; a cold envelope reports observed descriptor/bytes only,
never recreates that acknowledgement. This envelope is not a serializable hot
capability or new accepted carrier; its exact source-owned shape remains for
storage review.

A later manifest can record the prior publication result once actually observed,
including a definite receipt or an unresolved attempt. It cannot retrospectively
write a confirmation into the bytes whose publication is being confirmed. If
account publication succeeds but current journal update fails, keep the original
account BoundReference and separate journal attempt in live custody; do not edit
the attempted manifest to pretend it recorded its own failure. A later successful
record or cold gap must preserve the actual temporal boundary. Self-reference or
current-publication acknowledgement inside the manifest refuses the proposed
semantic contract, even if caller fields or a hash fixed-point claim are supplied.

### Gap recording is not complete closure

A new durable manifest may truthfully record unavailable producer, missing ref,
unknown dispatch, stale input or conflict without fabricating a corresponding
artifact. Such recording is useful recovery state, not successful complete
critical closure. Replacement must preserve all previously required available
critical bytes, original unresolved attempts and their exact bindings. It may
add a newly discovered resolution gap while retaining the old historical
observation. It must not discard bytes still retained merely because a source
is now unavailable, or delete uncertainty to make the state appear complete.

If an external artifact has actually disappeared, record that loss and the exact
historical binding; do not pretend the new snapshot preserved missing bytes.
Durable loss reporting remains permitted. Completion/retirement or replacement
that itself destroys retained required evidence refuses. These distinctions
apply to the proposed semantic contract independently of storage write failure
or an unselected resource cap; no successful persistence is assumed here.

### RS resolution mapping remains unadopted

RS §9 uses write-resolution literals `resolved`, `unresolvable`, `not supplied`
and independently reports resolution at read. The richer carrier resolution
states in §3 are proposed diagnostic refinements, NOT accepted RS enum values.
Their exact mapping/representation is an explicit owning-review gap; this draft
must not emit them as valid RS literals, rewrite historical RS records or claim
RS-schema compatibility. Referenced RS evidence keeps its actual recorded literal
and source meaning separately from the carrier's diagnostic state. Actual RS
owner concurrence remains absent.

### Prior results are not an all-snapshot dependency chain

Each prior-result reference must declare its use: `historical_subject_identity`
or `required_recovery_dependency`. A historical subject identity records the
original journal/revision/hash and bounded receipt/outcome observation. It does
not require resolving the entire old snapshot merely to preserve that historical
identity. If those old bytes are absent, show not-retained/not-resolved in the
carrier diagnostic view without pretending current resolution or deleting the
original observation. This proposed distinction does not assign an RS enum.

A required recovery dependency, by contrast, must retain the exact critical
artifact bytes and evidence necessary for current recovery. It cannot be relabeled
historical to evade retention. Original unresolved attempts and their actual
recovery-critical evidence remain required; a required pre-final account binding
must survive exactly as its future adopted contract requires. Referencing a prior
commit does not transitively make every prior full snapshot required: the current
manifest identifies the finite required artifact closure explicitly. The closure
must not depend on recursively traversing all previous snapshot manifests.

After repeated commits, retain current selected exact artifacts and all still-
required historical critical evidence/attempts through stable references or exact
embedded material; keep bounded prior receipt/subject metadata only to the extent
needed to explain current status. Older full snapshots may be replaced under the
selected current-status retention direction once required bytes survive. No new
count, expiry or deletion policy is selected here. If required critical evidence
cannot fit the later reviewed bound, refuse destructive advancement rather than
silently dropping it or requiring an unbounded all-history store.
