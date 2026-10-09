# Connector exact Git observation CGP-v0.1

Named technical proposal C3-S3-GIT-01. Source owner DEL-07-02. Status: PROPOSED,
independent source review and manager selection pending. Extends CSP-v0.1 §6
with a separate transient Git observation; preserves CSP local-read meaning,
CFB-v0.3, CRP-v0.3, persisted schemas and saved-account reader unchanged.
No source/account materialization, actor act, provider reliance or native
witness follows from this definition.

## 1. Concrete contribution and supplied identity

Given a current host-private CSP session and selected observation/path, read
the exact regular Git blob at an explicitly supplied full commit object ID.
Optionally repeat at a full since-commit ID for the same exact path. Return
separately bound object observations and excerpts beside the original local
snapshot, with independent gaps. No recursive search, automatic rename
tracking, branch selection, checkout or reconstructed fact/conclusion is done.

The renderer passes session/generation/observation reference and commit strings;
it cannot pass a root, Git directory, object directory, path or source DTO.
The host derives the exact project-relative path from the private selection,
not its display spelling. CSP must retain this private path at selection;
its current Observation cannot be rebuilt from the public preview. Extending
that private state is part of the bounded implementation, not permission for
arbitrary path RPC. A stale or cancelled historical observation is not usable
as current selection; explicit new selection or current reference is required.

This slice requires the explicit App project root to be the repository's
worktree root. A project subdirectory, nested repository, bare repository or
unestablished association yields a scope gap; do not walk upward or silently
switch repositories. This is a bounded initial adapter limitation, not a
change to general App project policy. Missing local historical files cannot
be chosen through this selector; later historical-path intake needs separate
technical treatment. Read-only Git history need not equal the live local file.

## 2. Revision grammar and exact resolution

Accept only lowercase full hexadecimal object IDs of the identified repository
object format: 40 characters for SHA-1, 64 for SHA-256. No trimming or Unicode
normalization; reject whitespace, abbreviations, uppercase, refs, HEAD, tags,
reflogs, revision operators, ranges, options or commit:path expressions.
Wrong format/length is an explicit input gap. A full ID still requires actual
object lookup and type verification: a tag/tree/blob ID is not a commit and
must not be peeled or reinterpreted. No ambiguity fallback exists.

Bind each result to the exact requested and read commit ID, commit raw bytes
and their identity, root tree ID, traversed tree identities/modes and final
blob ID. Verify Git object identity using the repository hash format over the
raw object header/type/length and bytes; a SHA-256 content hash over blob bytes
is recorded separately. If integrity cannot be established, do not use the
label Git-object-verified. Object identity establishes graph membership and
bytes, not trustworthy authorship, signatures, source truth or acceptance.
No claim is made that a supplied commit belongs to HEAD's ancestry or an
accepted branch; full object availability alone does not establish that.

## 3. Repository and linked-worktree association

Read the explicit root's `.git` entry as metadata under host control. Support
an ordinary `.git` directory or a linked-worktree `.git` file whose `gitdir:`
points to its administrative directory. Resolve the linked administrative
`commondir` and validate its backlink `gitdir` to the selected root's `.git`
file. Retain resolved path identities and exact metadata bytes/hashes, including
object-format declaration. Refuse malformed, cyclic, missing or inconsistent
association and unknown repository-format extensions instead of guessing.
Do not accept renderer-supplied metadata destinations.

Linked administrative/common/object directories can legitimately lie outside
the project root. This adapter reads only the metadata/object-store association
derived from that explicit worktree and makes that external location visible;
it must not describe it as project-contained. This is a bounded repository
association read, not arbitrary outside-file approval, source selection or
permission expansion. Actual host permissions still govern. Separate git-dir
layouts lacking the linked-worktree backlink are outside this first slice.

Reject symlink indirection in association entries/object storage paths for the
initial implementation; do not rewrite or repair repositories to satisfy it.
Alternates (including environment alternates and object-store alternates files)
are unsupported initially and produce a gap. Common Git object storage for a
validated linked worktree is not an alternate. No submodule metadata traversal
is allowed. Detect/recheck association changes around the read; fail observed
change rather than rebind to another repository.

These checks observe a filesystem association; they do not prove an adversarial
same-user process never changed metadata between checks. Preserve the existing
opened-identity/pathname distinction. Report that residual. Rehash each returned
object to its requested identity and retain original association observations;
never represent matching pre/post observations as continuous exclusion.
The pathname-based Git subprocess does not inherit CSP directory-handle
no-follow guarantees for every object-store descendant. Initial symlink checks
and rechecks do not exclude a concurrent replacement; state that mechanism
limit explicitly alongside the integrity and association observations. If
host permissions or supported mechanisms cannot honor the bounded read, refuse.

## 4. Literal tree path and object reading

Split the retained relative path into exact components. Reject absolute paths,
empty/dot/dot-dot components, NUL and separators masquerading as components;
never normalize case or Unicode, interpret a glob/pathspec, or interpolate a
revision:path string. Use raw tree entries matched byte-for-byte. Non-UTF-8
native components may be compared as bytes; display is explicitly lossy where
needed, never used for lookup. A platform unable to preserve bytes refuses.

Read raw commit object, extract its exact root tree identity, then walk each
raw tree's exact component. Intermediate nodes must be trees. Final entry
must be a regular blob with mode 100644 or 100755. Symlink mode 120000,
gitlink/submodule mode 160000, directory, absent path, malformed/duplicate tree
entry, wrong object type or unavailable object is a gap. Never dereference
symlinks, load submodules, consult index or substitute working-tree bytes.
Read the blob without smudge/textconv/EOL filters or mailmap transformation.

Bound accepted blob bytes to CSP's 262144-byte UTF-8/no-NUL limit. Bound commit
and each tree raw payload to 1 MiB, traversal to 128 components, total object
payload per side to 8 MiB, and one request to 10 seconds with bounded stderr
(16 KiB). These are explicit technical limits, not source invalidity claims.
Refuse truncation, over-limit declared/actual lengths, framing mismatch, stalled
read, invalid UTF-8 or NUL-bearing blob; do not hash a truncated buffer as a
complete source. Apply the side-local versus whole-request rules below. Parsing consumes only
successfully bounded raw payloads; incomplete bytes never become an observation.

## 5. Offline implementation mechanism and qualification boundary

Existing App code supplies private CSP session, project Root checks, bounded
text/excerpt routines and SHA-256; it has no Git provenance engine. Cargo.toml
has no Git object library. The available development host reports Git 2.54.0
(Apple Git-157); this is an observation, not an App dependency guarantee or
qualification across machines. Do not download an engine or dependency.

Preferred bounded implementation: a known absolute Git executable, invoked as
a subprocess by an explicit argv vector, never a shell. Restrict operations to
raw `cat-file` object queries and the CGP-R1 nonwriting recomputation below;
full object IDs are supplied as data. Tree walks
are parsed by the host, not revision expressions or pathspecs. Before release,
verify the actual executable/version supports the required switches and test
its complete command/environment envelope; unsupported installations refuse.
Use `--no-lazy-fetch`, `--no-replace-objects`, `--no-optional-locks`, no pager,
no filters/textconv/mailmap and no symlink-follow mode. Set a deny-all
transport/protocol policy as defense in depth; qualification must show that
unsupported controls fail rather than silently relying on ignored variables. Missing promised objects
stay missing; no fetch, remote helper, hook or credential program may run.

Do not launch Git against unfiltered user/repository configuration. Construct
a private transient minimal administrative directory containing only the
validated object format and a host-selected object-store association; expose
only the validated object directory for raw reads. Exclude all inherited Git
path/config/alternate/namespace/trace/command overrides; disable system/global
configuration and terminal prompts. Do not copy repository remotes, includes,
aliases, extensions or helper/hook/filter configuration into that directory.
Reject unsupported source extensions/alternates before use. On a child/payload cap failure terminate and reap the affected child and
boundedly drain/close its pipes; that side fails under §6. Whole-request
deadline or cancellation terminates all request children and follows the
request-abort rule in §6. Incomplete object bytes are never successful evidence.
No Git operation writes to original worktree, repository metadata or object store. Temporary
helper metadata is session-owned, not persistent authority or a new service.

The process boundary must prevent object misses/configuration from causing
network or external-helper activity; demonstrate this with hostile-config,
promisor-object and process/transport sentinel fixtures. Git option support is
not inferred from silent acceptance of an unknown environment variable. An
available host network-denial boundary may strengthen tests; do not claim OS
sandbox enforcement where none exists. If the restricted built-in operation
and sanitized configuration cannot establish the stated no-helper/no-network
behavior on the actual host, refuse and return the mechanism gap for technical
review rather than weakening it. A different object library/engine is a named
reviewed alternative, not an implicit dependency addition.

### CGP-R1: concrete object-ID recomputation, no new dependency

The approved offline Cargo cache has no `sha1` archive/extracted source; sparse
index metadata alone is not build availability. Existing Cargo.lock has no
sha1 crate. No dependency download, manifest change or custom cryptographic
implementation is selected. Extend the restricted Git operation allowlist
explicitly with this fixed nonwriting command in the same sanitized helper:

`hash-object -t <type> --stdin --no-filters`

`<type>` is a host enum limited to `commit`, `tree`, or `blob`, matching the
validated raw object's reported type. Pass the already bounded, fully read
object payload as raw stdin bytes, with no pathname, transformations or shell.
The helper's validated repository object format chooses SHA-1 or SHA-256; an
unsupported format/capability refuses. Never pass `-w`, `--path`, `--stdin-paths`,
`--literally`, a file argument or caller-selected extra option. No object is
created. Existing object-byte/side-total limits apply to the buffer; hashing
cannot extend the whole request's remaining 10-second deadline. Terminate/reap
on failure using the same supervisor and result-publication rules.

Accept exactly one lowercase full-length object ID followed by one LF on
stdout, zero exit status and no framing excess (stdout capped at 65 bytes).
Compare with the requested commit/tree/blob ID. This recomputes identity from
type and the returned raw bytes, rather than trusting `cat-file`'s ID echo.
Mismatch or type/framing/command failure yields a side-local integrity gap,
unless the failure is whole-request deadline/cancellation/supervision failure.
Compute blob content SHA-256 separately with existing `sha2`.

Both reads and recomputation use the same qualified Git executable. This is
an independently invoked calculation over the received buffer, **not an
independent cryptographic implementation or protection from a compromised Git
binary**. Its warrant is byte/type/object-ID consistency under that identified
implementation. Qualification must include fixed independently known SHA-1
and SHA-256 commit/tree/blob vectors, corrupted payload/type negatives,
nonwriting/source-object-store invariance and hostile configuration tests.
Do not count a Git-generated expectation checked only by the same Git as an
independent oracle. Actual host invocation support remains to be demonstrated
by implementation evidence; the source definition itself is not that evidence.

## 6. Frozen observations, excerpts and comparison

Keep source local snapshot, caller revision assertions, located revision text
and Git object observation as distinct objects with fresh opaque references.
A verified Git read never relabels local snapshot bytes as committed, even if
their content hashes coincide. Record the observed repository/worktree/metadata
association, requested full commit, raw commit/tree/blob identities, regular
mode, exact path bytes, blob SHA-256/length, read time and mechanism standing.
Bounded raw bytes remain in host session memory; exported DTOs cannot recreate
read capabilities. Cancellation/stale completion preserves previous observations
as historical and produces no new successful Git observation. Project/session
change invalidates capabilities; process loss loses previews.

For each side use CSP's exact zero-based half-open UTF-8 byte intervals and
one-based complete-line excerpts including retained LF/CRLF. Excerpts bind to
that side's blob hash and opaque observation, never a local file/other commit
anchor. At/since same path may yield different content, one missing side, or
identical content in different commits. Show these facts mechanically; do not
infer semantic change, rename history, contradiction resolution or authority.
One successful side plus one gap is partial, never a verified comparison.

**Request publication rule.** Prepare results privately, then publish one new
request result only after both requested sides finish and session/generation
checks pass. With no since input, completion applies to the at side only.
Side-local failure means missing/nonregular object/path, invalid or oversized
payload, decoding/integrity failure, or that side's 8 MiB payload budget. Retain
a completed verified other side as a current **partial** result with the failed
side's explicit gap; discard incomplete object buffers on the failed side.
Neither side can consume the other's budget. Two failed sides publish gaps
only, not a successful Git observation. Input grammar/association/capability
failure before sides begin yields request failure with no new object result.

Whole-request failure means the 10-second overall deadline, user cancellation,
stale session/generation, changed project/repository association, or process
supervision failure that prevents establishing isolation/completion. Abort the
entire new result, including any internally completed side; do not publish a
new current partial observation. Keep only the previously published request
result as explicitly historical, with the latest operation failed/cancelled.
A previously published result is never silently relabelled as this request.

Examples: at verified, then since exceeds its blob or side-total limit → new
partial result containing at plus since gap. At verified, then since consumes
the remaining overall deadline → aborted request, no new at result; previous
published result historical. At verified, then user cancels or generation
changes → same abort rule. At and since verified before deadline but session
check fails → abort. At missing and since verified → current partial since
plus at gap. These rules concern presentation/result custody, not changes to
actual bytes that may already have been read in private request memory.


No route source entry/account is emitted. Even commit/blob verification leaves
source role, factual interpretation, reliance and actor evidence unestablished.
Materialization requires a later named treatment preserving those distinctions;
existing source schema's revision string alone is not a provenance receipt.

## 7. Failure and consumer treatment

Show same-question gaps with reason, affected side/path/revision and caller's
responsibility assignment or explicitly unassigned status. Separate invalid
request, association failure, unsupported capability/layout, missing object,
nonregular path, over-limit/encoding problem, integrity mismatch, cancellation
and partial comparison. Neither absent object nor connector implies no work.
No provider term, fleet prerequisite, native act, source truth, performed
locate/compare, manager integration or person coordination is promoted.

Only CSP preview gets a new separate Git observation panel/control. Existing
saved-account view and CRP writer are unchanged; no historic anchor opens a
file or triggers Git. C1 connector standing remains independent input; current
preview triggers remain constructed. PEC/Domains/fleet consumers receive no new
record format or automatic adoption. Actual native witness remains point-held.

## 8. Required offline verification before code readiness

Use local scratch repositories and injected native selection, preserving no
native-witness claim. Tests cover ordinary and linked worktrees with metadata
outside project; wrong backlink, nested/subdirectory/bare refusal, symlink and
alternate refusal, metadata change, unknown format and host capability failure.
Use full SHA-1 and SHA-256 IDs if supported, wrong lengths/case/ref/operators,
full noncommit IDs, missing/ambiguous-input refusal and replacement-ref traps.

Read same exact path at two commits with dirty worktree and moved HEAD; verify
commit/tree/blob identities and content hashes by an independent raw-object
oracle. Exercise same-content/different-commit, absent one/both sides, unusual
literal names, Unicode/non-UTF-8 paths where host supports them, symlink/gitlink,
malformed trees and all payload/time limits. No shell/pathspec/filter expansion.

Sentinel configs/hooks/helpers/credential/transport and promised missing-object
cases must prove no invocation/network attempt, no lazy fetch and no original
repository writes. Verify sanitized helper cleanup does not affect source
metadata. Inject stale session, cancel, association replacement, truncated/
corrupted object framing and differing hashes. Exact excerpts use the same
CSP examples at each blob pin. No source/account/save/send/duty call occurs.
A source definition or installed Git version is not a pass for these tests.

## 9. Decisions and available boundary

Technical proposal within DEL-07-02: full-ID-only grammar, root/worktree
association support, explicit external metadata observation, literal object
walk, limits, private helper mechanism, transient preview and test matrix.
Independent review/manager selection precedes implementation release; no new
human gate is created. Actual platform qualification and source materialization
remain required work. Any broader filesystem authority, new dependency download,
external source policy, changed persisted meaning, network exception, provider
or D prerequisite returns to HELP_HUMAN before adoption.

Technical references consulted (upstream mutable manuals, not qualified runtime
pins): [Git object read](https://git-scm.com/docs/git-cat-file),
[Git controls](https://git-scm.com/docs/git), and
[repository layout](https://git-scm.com/docs/gitrepository-layout), and
[nonwriting object hash](https://git-scm.com/docs/git-hash-object).
