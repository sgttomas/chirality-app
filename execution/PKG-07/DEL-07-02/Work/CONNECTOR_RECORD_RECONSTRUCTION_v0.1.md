# Bounded record reconstruction CRR-v0.1

C3-S4-R1, PROPOSED technical source candidate; independent source review and
manager selection precede implementation. This contribution supplies a bounded
record comparison, not full C3 closure or accepted factual reconstruction.
Unique route-account format **0.4**, schema ID
`urn:chirality:app-v4:del-07-02:route-account:0.4`. Formats 0.1/0.2/0.3 and their
sources remain byte-for-byte unchanged. Never upgrade a cold account implicitly.

## 1. Concrete increment and relation to accepted sources

One frozen question, one host-selected ordinary project record at two explicitly
requested Git commits, checked excerpts, substantive attributed claims about
those records, explicit contradictions/gaps and distinct agent/manager/person
contribution accounting. A selected record may be a graph or decision document;
no fleet implementation, PEC or Domains completion is a prerequisite.

CFB-v0.3 means historical CONNECTOR_FALLBACK.md plus its named v0.3 amendment.
CFB §§3–7 still govern missing inputs, source facts, unsupported conclusions,
prohibitions and actual duties. This additive format narrows its factual warrant
to **what bytes the selected record contains**. It does not redefine CFB's
performed duty or solve authority by calling a claim supported. CAM-v0.1/R1
remains the format0.3 source-evidence draft definition. CRR borrows its private
custody, exact source mapping, failure lifecycle and bounds, while explicitly
adding record observations/comparison and contribution-report fields in 0.4.
CRP-v0.3 placement and publication are unchanged; registry/schema dispatch must
explicitly admit 0.4 after review. A source-only check is no persistence release.

The useful result distinguishes (a) checked excerpt inclusion and equality,
(b) a contributor's cited interpretation of recorded meaning, and (c) unresolved
performance/reliance. For example: a graph's earlier row reports CI pending and
its later row reports integrated; those are record claims even if a Git merge
was already present at the earlier pin. Never repair a recorded claim silently
using external merge knowledge. Any discovered inconsistency is a gap/claim
with its provenance and consequence, not a rewritten source.

## 2. Frozen input, custody and partial results

Require CSP-v0.1 current host-private selected path, CGP-v0.1 completed current
result and at plus since full pins matching the frozen question exactly. Both requested pins must have the same object-ID length/format for one
repository, even with partial or zero-source results. Both
pins address the same literal UTF-8 project-relative path. Copy that private
path into evidence.selected_path even when both sides fail; every source and
failed-side gap must match it. Paths are nonempty, NUL-free relative UTF-8
with no empty, dot or parent components and no leading slash. Commit identity,
full file SHA-256, blob identity, path and every selected anchor remain distinct.
No HEAD/worktree coincidence, caller bytes, attachment supply, arbitrary path,
source-stated revision or cold record becomes a private Git result.

CAM §2 eligibility and mapping still apply: a completed partial/gaps-only
result may be saved but no failed side becomes a source. Preserve every failed
side as a gap with its requested pin, literal path, cause, effect and explicit
responsibility (including genuinely unassigned). Source absence means no facts
for that side and no two-sided comparison. Zero sources means no facts,
comparisons, claims, contradictions, contribution reports or supported results;
gaps/unsupported remain nonempty. Full-question answer is unsupported where
needed evidence is absent. Do not discard a successful side to fabricate a
symmetric answer. Since is required in 0.4; use 0.3 for the single-pin draft.

Snapshot/hash/anchor limits and Git same-engine verification remain those of
CSP/CGP. Caller-selected excerpts may omit other relevant record text; preserve
a producer-limit gap and unsupported conclusion for record completeness,
semantic truth, actual duties and authority. No automated completeness or
contradiction detector is claimed. A changed excerpt need not be a substantive
change; equal excerpts do not prove the full file/question unchanged. Different
full-file hashes with equal excerpts must remain visible.

## 3. Observations, checked comparisons and attributed claims

`facts` in 0.4 are narrowly typed **observed_record_excerpt_only**. The host
creates one fact per selected excerpt, binding fact_id, source_id, excerpt_id
and exact anchor. Its statement is exactly `Observed excerpt {excerpt_id} at
{source.revision}; content SHA-256 {excerpt.sha256}.` The content is already in
the source excerpt; do not duplicate the blob or accept caller-authored fact
statements. This is an observation about a record, not its truth or authority.

`comparisons` are explicit user-selected pairs: one since fact and one at fact
from this selected record. The host computes `same_excerpt_bytes` or
`different_excerpt_bytes` from their exact UTF-8 bytes. It does not choose
semantically equivalent sections, infer status transitions or compare only
hashes. One pair appears once; refs and IDs must be unique and resolvable.
Unpaired excerpts are still useful observations. Relation scope is exactly the
selected intervals, including LF/CRLF, never the entire record.

`conclusions.supported` contains only host-generated mechanical observations:
one per fact and comparison, basis `source_route`, exactly one ref. A fact's
supported statement equals its fact statement. A comparison's statement is
exactly `Selected excerpts {since_fact_id} and {at_fact_id}: {relation}; no
whole-record or substantive-change conclusion.` No caller conclusion or claim
can enter this list. Missing observations cannot support a conclusion. The
bounded basis does not satisfy a connector need or authorize work.

`claims` are the actual contributor-authored answer/analysis, with explicit
asserted_by, asserted_role and caller_asserted_identity, and scope
record_contents or record_change. Each cites existing fact/comparison IDs.
A record_change claim requires at least one checked pair; record_contents may
cite facts alone. Citation support means the author points to checked record evidence; the host
validates the links, **not entailment, truth, sufficiency or authorship**. Display
claims as attributed record claims, not as the mechanical supported list. The
schema's `attributed_record_claim_not_verified_truth` must accompany every claim.
The author may say “the row records COMPLETE”; neither host nor reader turns
that into “the work is complete.” Source validity cannot certify arbitrary
natural-language claims; no keyword filter can substitute for review.

`contradictions` records explicit unresolved disagreement between at least two
claims, their IDs, description, effect and responsibility. `[]` means none
reported, not absence proven. No automatic adjudication or resolved value in
this first increment. Every contradiction generates a gap (origin
caller_reported, general context) with its exact description/effect/responsibility
and an unsupported conclusion `Contradiction {id} resolved` with why=effect.
Preserve both claims and citations. Byte equality/difference can remain supported
while conflicting substantive conclusions remain unresolved. Reports of stale
or inconsistent records are claims/gaps, not source edits or provider standing.

## 4. Duties and contribution reports; no shared act format

Retain exactly the three CFB duties with their proper roles. Their `standing`
remains explicitly caller-reported **prepared** or **outstanding**, with reason;
0.4 does not emit actual performed or not_required. This is separate from the
contribution report and must not be set automatically by an excerpt, operation,
save, report or reviewer-looking identity. Prepared means prepared work only.
An actual performed-duty conclusion remains unestablished in this producer.

`contribution_reports` lets the route account preserve what is reported for
agent locate_compare, manager review_integrate and person coordination, without
making a new act record. A report carries the duty-matched actor_role, reported_by, reported_actor (nullable
when unknown), reported_status prepared/performed/outstanding/not_required,
reason and cited fact IDs. `reported_status=performed` requires non-null actor
and at least one ordinary-record fact citation. Every report is
unverified_contribution_report with performance_verification=not_established.
This field can faithfully preserve “the graph reports that review happened”;
it does **not** set duties.standing=performed. Missing reports mean no report,
not an outstanding or performed act inferred by default. Opposing reports stay
visible; turn a claimed conflict into an explicit contradiction/gap through
claims, not a last-writer-wins report. Reports and duty reasons are inert text.

This first increment **does not consume typed RS act/run references**. It
accepts only local fact IDs identifying checked ordinary-record excerpts;
strings naming a run or act inside those excerpts are quoted content, not
resolved references. No shared capture/record format, act ID dereference,
checkpoint satisfaction, direct capture, faithful-recording certification or
verified identity is produced. Generic citation is not adoption of
DEL-04-03 RECORD_SEMANTICS.md / RS-v0.10 §6.1–6.2 HA-1/HA-2 and §13/14: those
require actual capture evidence and retain identity-not-verified. If a later
slice consumes those typed records, obtain DEL-04-03 concurrence through the
manager on that exact interface before adoption. This source does not create
that dependency or claim to satisfy it with ordinary report text.

No genuinely reserved human meaning choice is needed for this bounded record
reporting proposal. Two concrete future alternatives remain outside it:
(1) leave actual performance unestablished with reports visible; or
(2) consume identified act/run/capture interfaces under their owners' concurrence
and applicable actual human acts. Select neither verified identity nor automatic
performed-duty inference as a shortcut. Any request to use a reported human act
as permission or acceptance returns to its governing owner before implementation.

## 5. Validation and lifecycle

Beyond JSON shape, validate exact pins/source-side mapping, at most one source
per side, same literal path, full object-ID lengths, globally unique source/excerpt/fact/pair/claim/
contradiction/report IDs, no dangling or repeated refs, one fact per excerpt,
anchor/byte/hash/source matching, and each pair's since/at orientation/relation.
Generate and compare the exact complete supported list; no claim/report IDs may
appear there. Validate duties once each, role mapping, responsibility and every
failed-side/contradiction gap and unsupported effect. Preserve all caller gaps.

Hot preparation additionally checks original private buffers/anchors, CGP
association/engine receipt digests, source eligibility and same opened root.
Cold validation checks internal citation/equality consistency, excerpt hashes
and deterministic statements. Excerpts are nonempty bytes. Parse line anchors with first <= last; exact
selected-line count is LF count plus one only for a final unterminated line.
L1 starts at byte zero; a later first line starts no earlier than first-1 bytes.
Cold data cannot prove exact offsets of unseen preceding bytes; hot buffers
check those. Reject observed_git_failure gaps on a successful/general side;
each absent side requires exactly one matching pin/path failure gap, never a
duplicate or substituted failure. The cold validator has no original whole-file
or object buffers; these internal checks remain limited.
Thus a self-consistent forged cold account cannot establish provenance. Show
recorded observations/claims/reports and the compact receipt limits; never
rehydrate source custody or infer prior publication. Present arbitrary strings
as inert escaped text and preserve host-parsed numeric limitations.

Inherit CAM's exact 1 MiB serialized UTF-8 cap (including escaping/metadata),
max2 sources/max16 excerpts per side/max32 gaps, at most32 facts/claims/reports/
contradictions and16 pairs. Required generated gaps that exceed a bound refuse
preparation, never truncate. CAM-R1's 64 lifetime identities, one payload and
capacity refusal are unchanged development bounds, not sufficient product
capacity. No source-session reset or version switch frees a slot. Generic cold
pre-read allocation remains unbounded by version-specific identification; do
not claim a composer cap fixes it or change old-version resource policy.

Every edit (claim, citation, contradiction, report or duty), reread, changed pin,
cancel or stale completion invalidates/replaces preparation under CAM §6/R1;
no mutation of frozen bytes. Preserve eligibility check immediately before
publish, same opened root identity, once-only token, duplicate/incomplete
discovery refusal, actual started/uncertain outcome retention, no retry/rollback/
unlink, and cold restart limits. CRP's identity-anchored rename race residual is
unchanged. Explicit format0.4 reader/validator/producer adoption is required;
unknown versions refuse. No App code is changed by this source candidate.

## 6. Concrete ordinary-record question and consumer impact

Question: “How does the Group C work graph's recorded C3-S3-P state differ
between 7fd670cc061a564d9a1c3a8cc3e85a4f870cf418 and
3d73db745edd3378e0bb254a1b263215ef0861e9, and what reconstruction/native work
does the later graph still record as unfinished or held?” Select
`projects/chirality-app-v4/execution/_Coordination/WorkGraphs/APP-V4-GROUP-C-20261008/WORK_GRAPH.md`.
Exact full-file hashes and selected line/byte excerpts are retained in
C3_S4_RECONSTRUCTION_BASIS.json. Since L110 reports S3-P READY with CI pending;
at L108 reports it COMPLETE/merged. At L106 and L111 preserve native HELD and
full reconstruction UNFINISHED. These are the graph's claims; even known Git
merge facts do not repair stale recorded text. The run basis retains the actual
source-owner locate/compare activity as task evidence; fixture account reports
remain constructed and cannot stand in for that activity, manager integration
or the human's cross-undertaking work.

PEC/DEL-07-01 and Domains/DEL-08-01 retain standing/admission/coverage semantics
and old pins; no receiving adoption is implied. Fleet DEL-06-01/02 can later
consume a deliberately adopted account reference with explicit record-versus-
claim labels; it may not infer readiness, need satisfaction, performed duties
or a new source dependency. DEL-09-10 must separately examine this bounded
question/unsupported effects and actual actor evidence; save/read success is
not its historical “question answered” or full C3 pass. DEL-09-11/DEL-04-03
receive no new act/run format. Native witness remains point-held; no provider,
fleet or group-order reversal is introduced.

Run `python3 check_record_reconstruction_v04.py` for offline schema/semantic
fixture checks. These are maintained definition checks, not production code,
source truth verification, native witness, duty performance or acceptance.

Future implementation acceptance (not executed by definition checks): exercise
the joined current private source → pairs/claims/reports → frozen 0.4 → CRP →
cold view path, including edit/cancel/reread races before publish, stale completion,
same-root substitution refusal, duplicate/incomplete discovery, started/uncertain
outcome retained across UI changes, version refusal and no cold-token revival.
Check rendered claims/reports cannot be mistaken for mechanical support or
performed duties. Required actual-native examination stays separately held.
