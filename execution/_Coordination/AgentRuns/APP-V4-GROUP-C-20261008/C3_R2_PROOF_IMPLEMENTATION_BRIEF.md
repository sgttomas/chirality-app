# R2-PROOF-01-B2 — exact dormant snapshot implementation brief

PROPOSED brief awaiting independent review. Parent technically releases only
after this exact brief is frozen/reviewed. Source selection76071c0038 merged
PR #1191 at04b06eb2f781a8344bc0582ea0dbd190f441dcce. Storage owner concurrence
is retained byte-exact in C3_R2_PROOF_STORAGE_CONCURRENCE.md. RS receiving
assessment is conditional and not source-owner adoption; no typed RS record is
created. No code has started under this brief.

## Code and activation fence

Implement a private `src/r2_snapshot_proof.rs` included only by a dedicated
`tests/r2_snapshot_proof.rs` integration-test binary using a path module. Do not
add it to production lib.rs or any App opener/command/startup. No Cargo feature
or runtime environment flag activates it. This also avoids a second global
allocator colliding with AA-CAP's existing lib-test allocator. No changes to
Host/AA-CAP, role/WR, recovery.rs, connector writer/registry/view, production
schemas, Cargo dependencies or actual project journal directory. Existing
storage-capable route_persistence may execute only after independent review;
reviewer remains separate. No new children or worktrees.

Use existing serde/serde_json/sha2/libc only. MacOS/Linux Unix test targets;
unsupported platform/filesystem operations refuse. Files live under an owned
constructed temporary root, with fixed fixture-only names and no production
placement default. No process spawn, native App, supplier or real CRP publication.
Test teardown can remove only that test's owned root after observations; the
core itself performs no automatic cleanup/retirement. Preserve existing witness
artifacts/App-data/locks and other sessions' scratch.

## Closed fixture codec and identity

All bytes UTF8 JSON, exact method `sha256:original_r2_proof_fixture_bytes_v1`.
Serialize typed structs in declared field order, compact serde_json::to_writer,
no newline; hash bytes actually written/read, never claim cross-library canonical
JSON. Use lowercase64hex SHA256; u64 revisions with checked increments. Exact
raw previous-descriptor SHA binds predecessor; no hash cycle. Prefix formats
are `chirality.r2.proof-control`, `chirality.r2.proof-descriptor` and
`chirality.r2.proof-snapshot`, version `test-1`; NOT a production record format.

Control: test namespace identity, exact TestBudget/policy digest. Journal admission:
unique fixture journal and undertaking IDs, revision0/no selected snapshot and
reservation. Descriptor: namespace/journal identity, revision, slot A/B, snapshot
raw length/hash, predecessor descriptor hash or null for first commit, policy
identity. Snapshot: same identities/revision/predecessor, constructed status/gaps,
artifacts (unique ID, kind, exact text, raw UTF8 length/hash), required IDs,
unresolved attempt IDs, separately labeled injected intent/outcome/account facts.
Use closed typed fields; no arbitrary recursive JSON metadata or executable values.
Kinds and status labels describe constructed/recorded data, never live capabilities.
Same artifact ID with different bytes refuses; all required IDs resolve internally.
Old required IDs and unresolved attempts must remain in successor, byte-identical
where identity persists. No resolver, blob store, slot-reference or implicit
uncertainty resolution. No retirement/ID reuse or conversion to a CAM token.

Parser: actual bounded read at S+1 or D+1; sentinel refuses before full parsing.
A nonallocating full-buffer structural scan bounds nesting16 and total object
members512 by counting each structural colon outside quoted/escaped strings,
including the first member (not commas/n-minus-one). This is not a prefix
classifier; serde still validates the whole JSON syntax and trailing EOF. Typed
Deserialize with deny_unknown_fields rejects duplicate/unknown fields; bounded
sequence visitors stop before item33 for artifacts and65 for references/issues.
Explicit duplicate artifact/required/attempt IDs refuse. Maintained tests must
actually reject duplicate keys in control, admission, descriptor and snapshot,
not rely on a serde comment; scanner tests count a single member as1 and exercise
exact512/513 plus punctuation inside escaped strings. Decoded IDs ≤128 UTF8
bytes, artifact strings ≤16384; string decoding may temporarily use the already
bounded input size, counted by allocation instrumentation, not falsely claimed
pre-allocation per-string rejection. Other text fields obey named identifier or
artifact bounds, not unbounded generic strings. Invalid UTF8/number/type, u64
overflow and incomplete/trailing JSON refuse without salvage-as-current.

TestBudget exactly initial N2/S32768/D4096/T0/Q262144 logical file bytes,
32artifacts/64refs/64enumerated entries-or-issues/512members/depth16/ID128/text16384.
Vary downward independently in tests. No Default, production deserialization or
production policy constructor. T0 forbids marker/retirement; zero N/S/D/Q and
checked-arithmetic overflow refuse. These are test parameters, not owner policy.

## OS protocol and error standing

Open root and child directories by descriptor; fixed single components only.
Use openat with O_NOFOLLOW/O_CLOEXEC and regular-file fstat/single-link checks;
directories checked as directories, not required to have nlink1. Mode0700 dirs,
0600 test files. Stable lock object created exclusively on initialization and
never normally deleted/replaced. Each session independently opens and uses
flock(LOCK_EX|LOCK_NB); EWOULDBLOCK/EAGAIN means Busy, unsupported/error refuses.
No duplicated fd masquerades as independent acquisition, PID-stale override or
upgrade. Reader and writer use the same exclusive lock protocol. Recheck lock,
root/entry and control identity around operations; no continuous-path or hostile
same-user replace/restore protection claimed.

### Bootstrap and admission, before first snapshot

Test setup owns a fresh temporary root; the core must not interpret a pre-existing
partial namespace as empty. Under its opened-root capability, initialization
exclusively mkdirat's the fixed fixture namespace, opens/rechecks it no-follow,
and fsyncs the root that names it. Create stable lock via exclusive openat,
fstat regular/single-link, acquire exclusive nonblocking flock on that open,
fsync lock then namespace directory. Create control exclusively, write bounded
exact namespace/policy bytes, fsync control and namespace, then reopen/read strict
exact bytes/identity. Recheck opened root, namespace and lock entry. Only after
all sync/readback checks return a new NamespaceConfirmed receipt. A competing
existing namespace or lock is not permission to initialize/replace it.

Before journal admission, hold that same lock, inspect bounded namespace state,
check N and worst-case Q reservation and uniqueness. Select a never-used fixed
slot index in0..N (not an argument-derived path). Exclusively mkdirat journal
slot; fsync naming namespace. Create immutable admission metadata exclusively
with namespace/journal/undertaking ID, policy and reserved slot identity, bounded
by D; fsync metadata. Create A and B placeholders exclusively, verify regular
single-link identity, fsync each; descriptor and temp must be absent for revision0.
Fsync journal directory then namespace; reopen/read admission and verify the
complete expected initial set, identities and zero-length placeholders. Return
AdmissionConfirmed only then. First commit refuses without current confirmed
namespace/admission and the held lock. No journal ID escapes as admitted earlier.

Before any filesystem mutation attempt, refusal reports no bootstrap/admission
attempt. Once creation/write is attempted, failure reports IncompleteOrUncertain
bootstrap/admission with original attempt and observed created entries; it never
claims nothing was created or gives back the slot. Partial, missing, conflicting
or unacknowledged state counts as occupied/reserved or blocks the whole namespace
when identity/accounting cannot be resolved. Never silently treat it empty,
reinitialize, delete or reuse quota. Error standing is distinct from a later
snapshot NotCommitted/Uncertain result. No snapshot can claim successful state
merely because a control/admission file is visible.

Cold inspection independently opens/rechecks all control/admission/lock paths and
reports observed state, not original initialization acknowledgment. The first
proof permits an explicit test-only confirm-existing step under the same lock:
only a complete identity/policy-consistent expected set may be resynchronized,
reopened and rechecked, issuing a new current confirmation, never reconstructing
the old acknowledgment. It creates/replaces/deletes no entries. An incomplete
bootstrap/admission still refuses; there is no repair fallback. Existing selected
snapshot/descriptor and uncertainty are preserved, not reset to revision0. This
lets a fresh test session continue from complete observed state without claiming
old hot custody. All prior attempts/outcome distinctions remain historical data.

Inject cuts before/after namespace mkdir/root sync; lock create/sync/directory
sync; control create/write/sync/directory sync/readback; journal mkdir/parent sync;
admission create/write/sync; each placeholder create/sync; journal/parent sync;
and final admission readback/acknowledgment. Assert incomplete states consume
reservation or block, repeat initialization/admission cannot reuse them, no first
commit follows failure, and explicit confirmation of complete existing state
neither recreates original ack nor silently discards an unknown attempt.

Select only descriptor's active slot. Open validated inactive slot, truncate/write
only it, enforce S during streaming serialization/hash, fsync file and bounded
readback. Create one exclusive descriptor.tmp, stream within D, fsync, recheck
expected old descriptor/root/lock, renameat descriptor.tmp→descriptor atomically,
fsync containing directory, reopen/read exact descriptor+selected snapshot under
same lock before confirmed acknowledgment. No F_FULLFSYNC or physical power-loss
assurance is claimed by this first `test-fsync-v1` protocol. Unsupported/failed
file or directory fsync refuses confirmation; no weaker fallback. Platform proof
and stricter device ordering remain production work.

Before descriptor replacement is attempted, failure is NotCommitted for the new
revision (old committed selection retained), with actual partial inactive/temp
leftovers reported. Once replacement is attempted, ambiguous syscall/fault,
directory-sync or post-check failure is Uncertain with original attempt identity;
do not automatically retry, roll back, unlink or reuse the old active slot.
Only all selected checks completed gives Confirmed. Reader reopened after dropping
all live handles returns SelectedStateObserved, never proof of prior acknowledgment.
Corrupt/missing/forked descriptors refuse current selection; prior snapshots are
only historical salvage if explicitly requested by test inspection, never winner.
Keep confirmed injected account BoundReference separate from journal failure;
missing historical acknowledgment after reopen is unknown, not a revived token.

## Reservation, quota and reader budget

Under same lock, bound enumeration and validate known fixed entries. Unknown,
orphan, invalid or ambiguous entries count conservatively and can block admission;
never accumulate unbounded issue vectors or ignore leftovers. For each admitted
journal reserve both S slots plus descriptor D and descriptor-temp D and its
admission metadata maximum D; project control+lock overhead reserves2D. Compute
`N*(2*S+3*D)+2*D` with checked arithmetic and require ≤Q before admission; exact
actual logical bytes/entry budget is also checked. No double-counting a leftover
inside an already reserved maximum, but unexpected extra files must not get a
free allowance. Unknown file larger than remaining budget refuses by metadata
plus actual bounded inspection where needed; never read it unboundedly. No quota
counter separate from reserved namespace state and no release on error/cancel.
This is logical byte accounting, not physical blocks/filesystem journal/device Q.

Read selected snapshot only, never both slots as full payloads. After clearing
memory, independently open root/lock/control and reacquire exclusion before
resolving exact descriptor; do not reuse old fds/capabilities as cold recovery.
Known per-file caps and stream growth after stat are tested. One test-owned
state may hold raw/parsed/new bytes only if every simultaneous allocation is
accounted within existing1MiB envelope; no hidden second full serialized cache.

Use a System-backed allocator meter only in the dedicated test binary, enabled
for the test thread. Measure cumulative allocation requests during each bounded
operation; add capacities of retained inputs/handles allocated before measurement.
That conservative measured total upper-bounds live peak, rather than asserting
it equals peak or bounds OS/RSS. Include parser, serializer, artifact clones and
hash work; no unmetered warm-up that hides required allocation. Assert the bound
≤1MiB for boundary fixtures and report observed upper bounds. If this overestimate
cannot fit, improve ownership/streaming or return the exact gap; never silently
change the envelope. Existing AA-CAP allocator and tests remain untouched.

## Required connected tests and release checks

Execute the21 selected designed cases with actual test files and deterministic
fault cuts before/after inactive write/sync, descriptor temp/sync, replace,
directory sync and readback. Retain first failing results. In-process cuts are
not OS crash/power-loss evidence. Independent-open flock tests are not cross-
process qualification; no child-process helper or supplier is used.

Required positive: embed constructed0.4/answer/review/intent/unknown outcome;
commit, drop all core state, reopen exact bytes; advance twice and prove old-slot
reuse preserves all required artifacts/unknown attempts. Cases include every
budget boundary, duplicate/unknown fields, syntax/depth/member/string limits,
identity/predecessor/revision changes, missing critical bytes, corrupt/forked
selection, growth-after-stat, lock Busy/substitution, retained temp/staging costs,
no auto-retry and final-account/journal distinction. Assert no production entry
exists and default App/library builds do not compile/activate this test module.
Run focused tests under default and distribution-successor features serially,
plus a production library check. No broad unrelated suite, frontend/native build,
new target or dependency acquisition unless an actual changed concern warrants it.

Storage owner and independent reviewer must backcheck exact choices above before
code; parent conditional technical release then applies. Source contradiction,
needed production activation, shared allocator edit, unknown quota accounting,
unsafe lock/IO order or inability to bound allocations returns before widening.
No accepted contract, RS typed record, CAM64 policy, retirement, real journal or
PM05/90% claim is authorized by this brief.
