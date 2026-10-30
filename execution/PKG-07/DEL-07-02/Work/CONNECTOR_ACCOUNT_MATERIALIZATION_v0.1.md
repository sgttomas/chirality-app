# Source-evidence draft materialization CAM-v0.1

Named proposal C3-S4-MAT-01. PROPOSED source/schema successor for review and
manager technical selection before implementation. Format 0.3 is explicitly
**source_evidence_draft**, not a completed reconstruction account. It permits
source evidence and unreviewed caller interpretations only: facts and supported
conclusions are empty, no performed/not-required duty is emitted. Older 0.1/0.2,
CFB-v0.3, CRP-v0.3, CSP-v0.1 and CGP-v0.1 bytes remain unchanged. This named
successor releases only the mapping described here after review, not broad
changes to their meanings or adoption by another loop.

## 1. One concrete connected contribution

Current private CSP selection → completed eligible CGP observation → explicit
source/anchor selection and attributed caller interpretations → host-prepared
immutable format 0.3 draft → explicit once-only CRP publication → cold read of
recorded evidence/claims. Implement/test this through injected native selection
and actual local Git/file operations now; actual App launch/person selection
witness remains point-held. No provider, fleet software or external authority
is necessary for the synthetic connected check. Full factual reconstruction,
manager review/integration and native witness remain required future work.

## 2. Eligibility, question and literal identity

Prepare from the host's current session/generation, current local selection,
completed CGP result and host-checked side/anchor references. The renderer may
choose those opaque references, but cannot supply paths, bytes, hashes, object
IDs, excerpts, receipt metadata or a preassembled account. Cancelled, failed,
pending, historical, stale project/selection or replaced generation refuses.
A completed partial/gaps-only CGP result is eligible with all failed-side gaps
preserved; no successful side can be invented. Never compose from a cold record.

Question ID/text/asked/since are copied from the frozen session. Asked revision
must exactly equal the CGP at full commit; since must be absent on both or equal
the exact CGP since commit. Mismatch refuses preparation and displays both
inputs; user can start an explicitly new preparation, not silently rewrite the
question or label a different commit as its answer. Current question revisions
remain caller requests; matching verified Git evidence does not prove authority.

Only successfully observed at/since sides can become sources. Each selected
side appears once with a distinct host-minted source_id, even when both have
identical bytes. The selected host path must be losslessly representable as
UTF-8 project-relative text with no invalid components. Non-UTF-8 paths remain
valid CGP observations but cannot materialize in this first string-path schema;
refuse the draft explicitly, never use lossy display or omit that side silently.
Project_display is also exact UTF-8; refuse unsupported project spelling rather
than corrupt provenance. This is a bounded materialization limitation only.

## 3. Exact schema mapping and proof limits

Use `connector.route-account.v0.3.schema.json`, unique ID/version 0.3. Copy
source.path from private exact relative path; revision from readCommit; sha256
from exact blob bytes; source_id is host minted. Caller must supply a nonempty
source role, recorded with role_standing caller_assertion. It describes intended
use, not observed authority. No role or source scope is guessed.

Each source has provenance: at/since side, repository object format, commit,
root tree, blob, regular mode, raw commit SHA-256, traversal SHA-256, original
observation time/provenance, opaque reference and explicit same-engine limit.
Traversal digest is SHA-256 over exact UTF-8 JSON bytes of the frozen CGP
`traversed` value serialized by the host at prepare. Shared evidence similarly
hashes frozen CGP association and engine JSON bytes; it records project device/
inode as decimal strings, exact display path and CGP requested commits. These
are compact identified observations, not complete replay bundles. Do not copy
raw commit/tree receipts, config contents, admin paths or full blob text.
Receipt digests cannot independently reconstruct/prove omitted bytes after
restart. Cold readers show that limit and do not regenerate trusted custody.

Selected excerpts copy host-checked exact text, byte interval, source-bound
anchor and SHA-256 from frozen Git bytes. Preserve CSP zero-based half-open
UTF-8 offsets including final selected LF/CRLF. Copy no local snapshot excerpt
into a Git source. Each excerpt gets a unique host-minted ID. SHA-256 must
match exact excerpt UTF-8; interval length must match bytes; source commit/blob
and side references must match the same retained observation. After cold read,
these remain recorded observations, not newly verified source contents.

Caller-authored statements are `interpretations`, separately attributed by
caller-supplied asserted_by identity, explicitly unverified attribution and
unreviewed interpretation. References identify existing selected source/excerpt
IDs. Do not put them in facts, supported conclusions or provenance. Empty
interpretations is allowed; the producer never manufactures a paraphrase.

Schema validation plus producer semantic checks must enforce unique source,
excerpt and interpretation IDs; valid references; exactly one of each of the
three existing duties; source revision==provenance.commit==requested side;
object ID length matches format; at/since selection uniqueness; exact question
binding; source SHA/excerpts match retained buffers; receipt hashes match the
frozen values; constructed trigger matches session; account shape/size. Schema
alone cannot validate these cross-field/source relationships. Cold validation
can check internal consistency/references but cannot claim buffer/provenance
verification without original custody. Reject inconsistent format 0.3 claims;
retain old-version validation unchanged.

## 4. Gaps, connector labels and actor claims

Copy every CGP failed-side condition into a gap with requested revision/side
and its actual reason/effect. Every gap has typed origin observed_git_failure, caller_reported or
producer_limit and context side/requested_commit/path. Failed-side context
matches the frozen request and exact path; general limitations use general
and null where not applicable. Explicit additional caller gaps have caller
origin and do not masquerade as observed failures. Required responsibility is typed:
caller_assigned plus explicit supplied identity, or genuinely unassigned plus
null. No guessed actor or string pretending unassigned is a named person.
Unassigned gaps do not block honest persistence; they remain visibly unresolved.
At least one unsupported conclusion identifies that factual reconstruction and
reliance are not established by this draft; caller may supply additional
unsupported statements. This limitation is a producer fact about its bounded
output, not a fabricated answer. Always preserve existing prohibited values.

Selection mechanism in the evidence receipt comes from the actual host entry
point: injected test callback is synthetic_test_callback, never inferred from
a renderer flag or the generic preview label. Native picker callback identifies
mechanism only, not witnessed human intent or authority.

Trigger connector is explicitly caller-selected pec/domains, reason preserves
the session's constructed absent/stale/partial/failing label; standing is
constructed. Receiving_records stays empty in this first producer. No actual
provider response or adopted/current standing is inferred.

For each locate_compare, review_integrate and cross_undertaking_coordination,
require the caller to supply prepared or outstanding plus an explicit reason;
no prefilled standing is silently accepted. These are reported unverified
statuses, not authenticated actor acts. Prepared means prepared work only.
No performed or not_required value is allowed by this first format/producer.
Do not require a human duty to be performed merely to save a draft. Necessary
future decisions/acts remain with their owners; no universal acceptance gate
is invented. Recorder is the App instance that materializes the draft, never
the caller's asserted identity promoted to person/agent. Record an opaque App
instance identifier, actual observed-clock prepare time and separate caller
interpretation attribution. Save success establishes no recorder duty beyond
writing these bytes.

## 5. Bounds and adoption

At most two sources, sixteen excerpts per source, thirty-two interpretations
and thirty-two gaps. Blob/excerpt limits inherit CGP/CSP; all serialized account
bytes must fit **1 MiB UTF-8 JSON** using the exact serialization frozen for
publication. Count escaped/encoded bytes, not character lengths. Oversize
refuses without truncation, omitted evidence or automatic splitting. Caller
can explicitly select fewer excerpts/start a new draft. No raw object bundle
or full blob duplication is required.

Current CRP implementation has no account-byte cap; this is a named composer
limit, not an existing guarantee. Format 0.3 cold validation refuses serialized
records above the cap once identified, but generic existing discovery reads
bytes before knowing their format. This does NOT promise bounded pre-read
allocation. A reader-wide bounded acquisition policy would affect older
versions and needs separate technical review; do not silently cap 0.1/0.2.
Schema maxLength is character-based; byte limit needs a deterministic check.

Store schema registry must explicitly add 0.3 and tests before writing it.
Cold reader must show draft standing, provenance/excerpt receipt limits,
interpretations/attribution and typed responsibility alongside existing fields.
Unknown versions still refuse, never downgrade or project 0.3 into 0.2.
Existing old records keep their own schema and views. CRP path, no-replace
publication, identity/ref resolution and uncertainty behavior remain unchanged.

## 6. Prepare, publish, cancel and uncertain custody

Prepare performs no filesystem publication. Mint unique account_id `ra:<uuid>`,
draft reference and exact bytes once; keep immutable host-private draft state.
Caller edits replace/invalidate that preparation explicitly and produce a new
draft identity; no hidden mutation of a frozen draft. Before publication,
recheck session/selection/CGP and project eligibility. An explicit publish action
carries only draft token/generation, not account JSON. Cancellation before
publish invalidates it and writes nothing. Only one publication attempt can
consume a draft token; concurrent/repeated submission refuses or returns its
already recorded attempt/result without invoking another write.

The CRP writer must use the **same opened project directory identity** observed
by the source session, not just a path with matching spelling. Bind device/
inode at preparation and compare opened writer root before publication, while
preserving CSP/CGP/CRP mutable-path limitations. Retain/open a writer capability
and verify against the source root; if bridging APIs do not expose sufficient
identity, add that narrow interface rather than infer equality from display.
Observed root/association change refuses; never save into a newly substituted
project. Rechecks cannot promise continuous membership during concurrent rename.

Before publish, detect existing account_id via discovery and fail on duplicates
or incomplete discovery. Host-minted unique identity plus one-use draft reduces
accidental duplication, not a cross-process uniqueness guarantee. Concurrent
foreign writers may still introduce the same ID; cold discovery must report
ambiguity, never pick a winner. Do not invent a global lock or overwrite policy.

Once publication starts, cancellation is not a guarantee of rollback. Record
and display the actual CRP result even if UI/session changes: success returns
its exact BoundReference; uncertain returns its Attempt without successful
binding; definite refusal preserves its failure/recovery issues. Do not suppress
a completed/uncertain write as 'cancelled, nothing saved'. No automatic retry,
rollback or unlink. An uncertain token remains consumed; reconciliation may
resolve that exact Attempt, not publish a replacement. A later genuinely new
draft requires explicit user intent and must not be disguised as retry of the
uncertain draft. Published bytes are immutable; corrections are new identities.
Cold records neither revive draft tokens nor establish a successful prior write.

### CAM-R1: bounded App-instance draft/outcome registry

Named technical amendment, pending exact independent review and parent
technical confirmation. The registry belongs to the App instance, independently
of source sessions. Keep at most **64 materialization identities** for that
instance. A successfully validated/frozen preparation reserves one slot;
preflight, stale-input or capacity refusal reserves/exposes no draft identity
or registry slot and does not
silently invalidate an existing draft. Consumed/cancelled/superseded entries
continue to count. At capacity, refuse new preparation visibly; never reuse
a slot, evict an outcome, clear the registry or restart automatically.

Retain at most one full immutable account payload, of at most the existing
1 MiB serialized cap, across prepared and in-flight states. An explicit new
preparation may replace the prior unconsumed draft only after its own preflight
and capacity checks pass; atomically install the new identity and convert the
previous draft into a superseded, unpublishable tombstone without its payload.
Explicit prepublish cancel likewise drops payload and retains a cancelled,
consumed tombstone. Neither cancellation nor supersession releases its slot.
Internal discarded candidate/placeholder IDs used to validate serialized size
are not exposed identities. Mint final IDs and revalidate the exact final
bytes before freezing/reserving a slot; RNG or final validation failure exposes
no draft and leaves the prior entry intact. There is no silent forgetting of
a formerly usable token. A failed replacement
request leaves the old registry status unchanged, though source changes may
independently make that old draft ineligible to publish.

When publication starts, mark its identity consumed/in-flight immediately and
hold its sole payload until the writer returns. Refuse new preparation during
that interval; do not release/reuse memory required by the write. Cancellation
or source-session changes do not evict the entry, undo publication or manufacture
a cancellation outcome. Retain the actual result when returned, then release
the full account payload. Keep the token tombstone, identity, status and exact
BoundReference for success, Attempt for uncertainty, or failure/recovery outcome
for definite refusal. Do not keep another account copy inside diagnostic text.
The count/payload limits do not claim an exact global memory-byte bound for
all metadata/diagnostics; retain compact structured outcome fields and existing
bounded diagnostic mechanisms without truncating a recovery-critical binding.

Repeated token operations report that retained state without invoking another
write. An unresolved Attempt remains present until explicitly reconciled; a
reconciliation result is added to that same entry, preserving the original
Attempt/outcome rather than replacing uncertainty with fictitious prior success.
Reconciliation never frees its slot or revives publication capability. Success,
definite refusal, cancellation and supersession are likewise retained for the
instance lifetime. No source-session reset is a registry reset.

Process exit/restart loses this transient registry and hot tokens, as already
stated for CSP/CGP capabilities; this is a limit, not an automatic recovery step
or direction to restart. Cold records cannot revive tokens or prove a prior
publication result. Existing explicit cold CRP inspection/reconciliation remains
available where its required evidence exists. On capacity exhaustion, show the
limit and retained outcomes so the caller can inspect/reconcile; do not promise
that retrying or restarting recovers uncertainty. Adding durable outcome storage
or a reset/eviction operation is outside this amendment.

Required implementation checks: exactly 64 successful preparations consume
64 slots even if each is cancelled/superseded; the next refuses without clearing
history. Failed preflights reserve/expose none. At most one full payload during edit,
cancel and publication; new prepare during write refuses. Source-session change
retains actual started-write result. Repeated publish/cancel/reconcile cannot
write again or reclaim slots; original uncertain Attempt survives reconciliation
and capacity pressure. New process has no restored hot tokens. This amendment
changes no account schema, persisted meaning or external consumer contract.

## 7. Required checks and retained obligations

Maintain schema positive/negative tests for the distinct format and no facts/
support/performed claims. Producer tests must use real scratch repository reads
through injected selection, at/since and partial/gaps-only results, matching
question/refuse mismatch, precise UTF-8 excerpts, stale/cancel/current states,
forged DTO/IDs, unknown role, assigned/unassigned gaps and explicit duty inputs.
Verify receipt hashes, object lengths/ref consistency and 1 MiB serialization.

Connected implementation check: selection injection → real Git bytes → chosen
anchors → draft → CRP save → restart/cold display retaining all limits. Include
same-root replacement, one-use/concurrent publish, duplicate/incomplete scan,
prepublish cancel, post-start cancel, edits/concurrent reread/stale completion
between prepare and publish, uncertain publication/reconciliation, cold hostile
text/large numeric strings and oversize escaping including metadata/excerpts. Current code is not claimed to implement these checks.
Actual native selection and full reconstruction/agent comparison, manager review,
human coordination and joined connector witness remain independently necessary.

## 8. Consumer consequences and authority

PEC PRC §8 must distinguish draft evidence/interpretation from a file-derived
answer; no new provider contract or pin adoption. Domains likewise preserves
admission/query boundaries and existing CFB pins. Fleet DEL-06-01/02 may link
this draft only after deliberate receiving adoption; it satisfies no need,
readiness or performed-duty inference. DEL-09-10 must examine this as draft
production evidence, not an answered-question or qualified connector witness.
Later research-to-design pin/activation stays unchanged. Notifications belong
with the manager; external loops decide adoption. No D production prerequisite.

The source/schema change is explicit: new format, typed responsibility,
provenance and interpretations, restricted draft standing. These are proposed
technical representations of existing evidence/actor distinctions, not weakened
accepted outcomes. Full reconstruction is still IN. Review may reject a mapping
that changes meaning; consequential scope/order/owner-reserved choices return
through HELP_HUMAN. No new human gate is invented for technical source selection.
