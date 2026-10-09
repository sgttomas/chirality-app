# R2-PROOF-01 — proposed first current-status snapshot proof selection

SOURCE CANDIDATE ONLY; no implementation, contract adoption or owner decision
request. Basis current main3cbfac7b8eb49aaee9ceb2068125319b1995f8aa. OD-02
selects recoverable current status; the technical source target is R2-S, with
R2-L comparator. PR #1185 supplies the physical hypothesis, not a selected
production quota/placement/retirement policy. This proposal narrows the first
technical proof; it does not claim PM05 sufficiency.

## 1. Recommended bounded release after review

Select a **dormant private two-slot snapshot/descriptor proof core**, exercised
only by test-only activation against temporary constructed projects. Include
an exact-byte recovery-content envelope, bounded snapshot/descriptor codec,
inactive-slot commit/readback, interrupted-operation outcomes and evidence
survival checks. No App command, production opener/admission constructor,
startup recovery, supplier dispatch, actual CCE mint, graph writer or quota
setting becomes callable. No production directory name is selected.

This can proceed after owning/independent source review and a bounded technical
release without a new owner product choice: explicit test budgets parameterize
the mechanism, not the App. Missing production policy continues to refuse
production admission. Passing a two-slot test never authorizes real journal
creation, reuse or retirement. If code cannot enforce this reachability boundary,
return that concrete implementation issue rather than adding a temporary UI.

## 2. Recovery-critical content for the first proof

The internal test envelope carries journal/undertaking identity, revision and
predecessor descriptor hash; current state and explicit gaps; exact artifact
bytes/length/hash; original intended-request identity/text where supplied;
recorded observations and unresolved-attempt identities; final-account result
separate from journal result. Data are explicitly constructed or historical
claims. No field, valid checksum or successful commit authenticates native
emission, RoleSourceLease, permission, manager duty or human act.

For the first proof, **embed every required recovery-critical artifact**. No
external immutable store, mutable-slot hash reference, Host-memory handle or
network resolution. A required-artifact identity maps to one exact byte string;
same identity/different bytes refuses. Links between selected base, answer,
review, intent and outcome must resolve within the envelope, with required-set
membership and role/source limitations retained. Do not describe a constructed
answer/review as an observed live contribution.

Preserve the prior required artifact/unknown-attempt set when advancing. Additions
are allowed within test bounds; removal or implicit resolution of uncertainty
refuses. This deliberately conservative proof subset does not select a final
semantic retirement/replacement policy. Old complete stage snapshots may be
reused only after their critical artifacts survive in the new snapshot. Tests
must demonstrate that a third update overwrites an old disk slot while keeping
its still-required exact bytes/limits in the selected snapshot. Unbounded revision
history cannot fit; evidence growth must end in refusal, not truncation. A later
C3 schema/semantic owner may propose precise supersession/reconciliation without
silently inheriting this test subset as final product policy.

## 3. Test budgets versus unresolved policy

Production N/S/D/T/Q, metadata/reference/depth ceilings, placement and supported
filesystem/threat model remain unselected. The proof has an explicitly named
TestBudget with no production constructor or deserialization into an admitted
policy. Initial finite fixtures may use N=2, S=32768 bytes, D=4096 bytes,
T=0 (no terminal-marker admission/retirement) and Q=262144 logical file bytes,
with at most32 embedded artifacts,64 references,64 enumerated entries/issues,
512 JSON members, nesting depth16, identifier strings128 UTF8 bytes and each
artifact string16384 UTF8 bytes. These are **test constants**
chosen to fit the constructed evidence and exercise exact/one-over refusal;
they are not proposed product defaults or a promise that any workload fits.
Vary them downward to force independent N, S, D and Q refusal; do not just pass
one generous configuration. Absent, zero N/S/D/Q, arithmetic overflow or inconsistent budgets refuse;
T=0 is intentionally the no-retirement case, not invalid policy.

Q in these tests measures enumerated logical file bytes including both slots,
descriptor/temp and control metadata, not allocated disk blocks, filesystem
journal overhead or total device use. Physical Q accounting and platform overhead
are outstanding production proof, not hidden under this number. Bound unknown
entries and issue enumeration as well as records. Test counters never consume,
reserve, reset or release CAM identities; no test proves final CAM64 suitability.

One-full-payload/1MiB development envelope remains the outer constraint. Count
simultaneously retained raw, parsed, serialized and proof buffers; two disk slots
are not permission for two full resident payloads. Test S is below that envelope,
but small data alone does not prove ownership or peak bounds. Require a written
allocation/ownership account, bounded actual reads and no second full serialization
unless counted. Existing generic0.5 discovery's resource gap is unrelated and
must not be cited as a bounded R2 reader.

## 4. Transaction and cold meaning

Use opened-root/directory no-follow identity checks and one fixed descriptor
temporary. The writer owns the same cooperating exclusion through inspection,
quota admission and commit. Never hold CCE/role/Host locks across IO. Write and
sync inactive snapshot; validate raw bytes; write/sync descriptor temp; recheck
expected selected revision/root/lock; replace descriptor; sync directory; reread
exact selected pair before confirmed acknowledgment. Unsupported sync or identity
checks refuse confirmation. No current code is claimed to implement this protocol.

Before descriptor replacement, the old selected snapshot remains current and
inactive work is uncommitted. After replacement without confirmed durability/
readback, return uncertain original attempt; never automatically retry or erase
it. Cold reopen reports the exact descriptor-selected state and whether evidence
is complete, not that a caller received the prior acknowledgment. Missing/torn/
forked descriptor refuses current-state selection; old bytes may be shown only
as historical salvage. Do not choose a higher revision or newest timestamp.
No automatic rollback, repair or cleanup is part of the core.

First tests use actual files plus in-process fault injection at every named
boundary and a controlled storage adapter. Such faults model interruption; they
are not physical power-loss or OS-process-crash qualification. Independent-open
lock tests can establish local descriptor behavior, not cross-process exclusion
by themselves. Separate cooperating-process/platform tests remain required before
production activation; a later reviewed test plan may request appropriate process
fixtures, but none is authorized by this source packet.

Advisory lock cooperation is not exclusion of a same-user actor ignoring/replacing
locks. Observe substitutions and refuse; do not claim transient replace/restore
is excluded. Self-consistent rollback/copy has no external freshness anchor.
Those limitations remain explicit suitability inputs before production, rather
than newly requested owner decisions now.

## 5. W2 and final-account observations stay separate

Use constructed intent/effect/record schedules only; no actual supplier request
or graph edit. Confirmed intent followed by crash before possible dispatch and
post-effect/pre-record crash can have the same recovered snapshot. Outcome is
unknown, not no-write and not retry permission. Untracked ordinary work has no
fabricated write-ahead intent. Matching target bytes alone cannot establish
original request, exclusive causality or manager integration.

A confirmed final account retains its definite BoundReference in original live
custody if a journal update fails; only the journal result is failed/uncertain.
If that confirmation did not survive restart, matching final bytes are a new
observation, not reconstruction of acknowledgment or CAM token. Test these two
outcomes separately. No real CRP publication is invoked in this first slice;
its outcome inputs are explicitly injected facts, not producer qualification.
Journal identity is never a CAM identity. No final-account writer/version change.

## 6. Code fence and connected proof brief, after release only

Proposed owner: existing storage-capable TASK selected by WORKING_ITEMS/Host
owner, with independent reviewer separate; no new child is commissioned here.
Private module and maintained tests/fixtures only, with at most an additive module
declaration if needed. Production activation absent. No mutation of App startup,
recovery.rs ledger, connector writer/registry/view, role/Host capture, schemas,
user data, existing native witness artifacts or graphs. Temporary test files are
constructed by test setup only, never a migrated user project.

Source owners before release: C3 validates critical-set/state meaning and no
claim promotion; storage owner selects exact OS operation/error/lock/read-bound
mapping within the test hypothesis; RS receives identity/resolution semantics;
independent reviewer challenges code reachability, bounds and interrupted commits.
Existing R2 physical proposal is owning context, not automatic concurrence on
this narrowed core or a new carrier. Exact semantic/byte methods and test-only
budget type must be reviewed; no generic callback under source locks.

Required joined test: constructed base/answer/review/ordinary intent/unknown
outcome bytes → prepare current snapshot → commit through actual file operations
→ clear all core memory → reopen exact selected pair → compare required artifacts,
state and uncertainty → advance twice → reopen after old-slot reuse. No saved
record is treated as an actual authored answer. Designed cases in
C3_R2_FIRST_PROOF_CASES.json include refusal of disappearing critical bytes,
mutable-slot references, over-budget staging, torn/forked selection, lost ack,
no automatic external retry and final-account/journal distinction.

## 7. Decision-ready conclusion

**Yes, a private test-only proof core can proceed without a new owner choice**
after exact owning/independent review and technical release. Its result would
be bounded mechanism evidence, not a usable App recovery feature or PM05 pass.
**No, production recovery cannot be released from this brief:** numeric resource
policy, placement/support/threat model, semantic carrier/reference retention,
shared cross-process admission and retirement/product capacity remain unresolved.
Prepare evidence for those choices rather than asking the owner to guess them.
R2 does not reset final CAM64 or gate all answer/review development. No code,
journal, cleanup, new decision request or accepted-contract change occurs now.
