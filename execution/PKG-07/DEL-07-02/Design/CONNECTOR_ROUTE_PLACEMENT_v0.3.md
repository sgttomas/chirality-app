# Connector route-account placement CRP-v0.3

Named technical design selection: C3-PLACE-01; proposed repair CRP-R2.
This successor preserves CRP-v0.2 unchanged. WORKING_ITEMS relays HELP_HUMAN's
selection of exclusive-rename publication as a bounded technical repair;
this is not a new human act, product acceptance or consumer adoption.
Status: source successor pending independent backcheck and affected fleet
concurrence; code is NOT READY on the strength of this definition. Supersedes
v0.2 only upon the applicable reviewed selection. The source-name substitution
consequence is explicit below; it is not a same-user exclusion guarantee.

## 1. Scope and selection

Accounts live in the opened user's project at
`.chirality/records/connectors/route-accounts/<storage-key>.json`.
This selects connector account location only, resolving the CFB §9 placement
question when concurrence and review are complete. It does not select fleet
paths, act logs, captures, provider storage, a common service or host allocation.
CFB account format and authority meanings are unchanged. Format 0.1 and 0.2
remain distinct; readers dispatch by declared format/version and validate
against the matching schema, never reinterpret unsupported versions.

Group A's bounded App-local allocation supplies a recovery precedent only.
The project root is an explicit opened-project input, never inferred from
process working directory. No unwritable-project fallback selects user data,
an external directory, another project or an external provider.

## 2. Safe storage identity and containment

The writer mints a lowercase canonical UUID v4 as `storage-key`, independently
of `account_id`, question, connector label and user strings. The basename is
exactly `<uuid>.json`; governed IDs are data, never path segments. A collision
causes a visible failure; it does not overwrite, reuse or silently rename an
existing record. Retry is a new explicit write attempt with its own key.

Resolve the project-root input once to a directory and retain that opened
directory's identity as the operation anchor. A symlink spelling of the
selected project root may resolve to its actual root; show that resolved
location. Record filesystem identity for the opened root and each opened
ancestor used by the operation. Below the root, reject symlinks in every
`.chirality/records/connectors/route-accounts` component and in the target;
reject non-directory ancestors and non-regular account files. Reject `..`,
absolute paths and equivalent platform escape syntax. Hard-linked
pre-existing targets are never write destinations; writes create new files.

**Containment guarantee: opened directory identities, not continuously
current pathname membership.** Open each child relative to its verified
parent handle with no-follow behavior, retaining handles through publication.
Create/publish only relative to the resulting account-directory handle, with
exclusive/no-replace operations. Unsupported platforms must refuse rather
than fall back to a path check followed by an unprotected open. Permissions
are those enforced by the host; this definition grants none.

This prevents path substitution from redirecting an operation to an unrelated
replacement directory. It does **not** prevent another process from renaming
an already opened root or descendant, including moving it outside the root's
current pathname tree. Handles follow the original directory identity. No
claim is made that its current path remains under the selected project at
every instant; pre/post comparisons cannot close the final-check-to-write
race. No enforceable exclusion of external renames is assumed.

Before writing and after publication, resolve the canonical relative chain
again without following links and compare it to the retained identities. A
pre-write mismatch aborts visibly. A detected post-write mismatch or failed
comparison reports an uncertain-location commit, never success at the old
relative reference. Do not retry, relocate or delete published bytes
implicitly. If a rename occurs between checks, bytes can have been published
in the original opened directory while its current location differed; even a
successful post-check proves only the observed identity comparison, not the
absence of transient moves. This residual is explicitly part of this proposed
technical selection and requires affected review/concurrence.

Recovery reports the originally bound root/directory identities, intended
relative reference, account identity and byte hash, plus which comparisons
failed or were unavailable. Reinspect the canonical path under the explicit
project root before accepting a reference. If it no longer locates the
published identity, report unresolved location and request explicit location
reconciliation by the caller; no search outside the project, silent adoption
of replacement directory, or claim that the account is absent everywhere.
If the intended product instead requires continuously-current-path containment
against concurrent renames, this design is insufficient: hold implementation
until an enforceable exclusion mechanism and its examination are selected.

## 3. Write-once commit and failure behavior

Validate the declared account against its exact 0.1 or 0.2 schema before
writing. Format 0.2's CI-29 rule is checkable: no source reads requires no
facts or supported conclusions, and nonempty gaps/unsupported conclusions.
The matching schema also checks required identity fields, prohibited values
and performed-duty evidence-field presence. This placement writer does not
add new cross-reference rules or claim to validate reference truth: any
broader referential/semantic checks belong to a separately specified recovery
contribution. The caller supplies the account, recorder, timestamp provenance
and duties; the writer preserves them and does not invent a missing value.
Schema/shape checks do not verify source truth, source custody, completeness,
actual duty performance or authority. The bounded persistence seam accepts a
schema-valid caller account; actual source recovery and semantic verification
remain C3 work. Build complete UTF-8 JSON bytes before publication; preserve
the caller's timestamp provenance, recorder and duty standing. Serialization or
validation failure leaves no published account.

Create a private temporary regular file exclusively inside the same anchored
account directory. Retain its open file descriptor and filesystem identity;
write the complete intended bytes, flush and sync them. Immediately before
publication, inspect its pathname without following links: require a regular
file with the retained device/inode identity and exact intended bytes/hash.
Observed substitution or disappearance refuses publication; no automatic
pathname unlink occurs, including on errors or collisions.

On macOS, publish with directory-relative
`renameatx_np(account_dir_fd, temporary_name, account_dir_fd, final_name,
RENAME_EXCL)`. Require the actual platform/filesystem to support atomic
no-replace rename; an unsupported flag/filesystem or ambiguous failure fails
closed. Do not fall back to ordinary replacing rename, link-plus-unlink, or
check-then-replacing rename. A destination collision preserves the existing
target and reports failure. In ordinary success, rename consumes the temporary
name as part of publication, leaving no extra hard-link alias or separate
cleanup step. No pathname unlink is performed automatically on any path in
this seam. Retained temporary entries are reported for explicit reconciliation;
this preserves v0.2's remove-only-own requirement by not attempting removal
where ownership cannot be guaranteed atomically.

**Source-name race remains.** Exclusive rename resolves the source name at
its execution; it does not consume the retained file descriptor. A same-user
process can replace the temporary name after the final precheck. Publication
can then move the foreign entry to the previously absent final name, removing
its temporary name while preserving its underlying bytes. This can affect a
foreign regular file or another entry type. The foreign entry's original
pathname may be disrupted; the record must not describe this as no mutation
or merely an extra alias. Prechecks, random names, mode bits and advisory
locks do not establish exclusion of this race. The original intended file
may remain moved aside, or reachable only through its retained descriptor.

After rename, read back relative to the retained directory handle without
following links. Require the final entry to be a regular file whose identity
matches the original retained temporary descriptor, whose exact bytes/hash,
account_id and formatVersion match the intended account. Complete the existing
root/path identity comparisons and durability steps. A successful binding
requires every check to pass; it attests those observations, not immunity from
transient changes or later modification. Comparison of hash alone is not
sufficient when a foreign inode contains identical bytes.

On mismatch, uncertain publication/durability outcome or failed path check,
report an uncertain/tampered commit, not a successful durable binding. Include
the intended target, intended account identity/version/hash and original file
identity; describe observed final identity/type/hash only where safely read,
and mark absent/unreadable observations explicitly. Preserve all entries.
Do not unlink, rename back, move elsewhere or retry automatically: such a
repair could mutate a further replacement. A successful syscall alone is not
a successful account commit. Where rename reports a definite pre-publication
failure, report that failure and any retained temporary recovery issue; do
not claim publication without evidence.

Recovery inspects the canonical target and any explicitly known original
location under the same containment rules, compares intended and observed
bindings, and reports missing/mismatched identities for explicit reconciliation.
It does not guess where a displaced original went or search outside the
project. A schema-valid foreign file may exist at the final name: cold
discovery alone does not prove that this writer successfully published it.
The existing reader binding checks must refuse reliance on an intended
reference whose observed bytes/identity binding differs. An unbound discovered
record remains an inspected file with its own claimed content, not evidence
of a successful writer operation, source truth or actual recorder duty.

Corrections and later connector recovery create separate accounts with new
storage keys and distinct account identities supplied by the recorder; prior
accounts remain evidence of their original state. This placement amendment
adds no supersession field or automatic authority precedence. A later timestamp
alone does not resolve contradictory accounts.

## 4. Durable references and cold recovery

After successful publication, return the project-relative path, account_id,
formatVersion and SHA-256 of the exact published bytes. A consumer keeps that
binding in its own existing reference mechanism; a bare `ra:` identity remains
an identity, not a path. No receiving contract is silently extended here.
Consumers that cannot preserve/resolve the binding require a reviewed adoption
treatment before relying on it. Project relocation preserves relative paths;
copying bytes into another project does not transfer authority automatically.

Cold recovery enumerates the canonical account directory without following
links, considers only canonical UUID `.json` regular files, validates supported
formats, and recomputes hashes. Build an in-memory account_id-to-path index;
no authoritative side index or fleet service is required. Duplicate account
identities, malformed bytes, unknown format versions, hash disagreement with a
held reference, missing targets and temporary leftovers are shown separately
as unresolved recovery conditions. Never pick one conflicting account by
filename, timestamp, enumeration order or last-writer-wins.

Absent directory means no route accounts were found at this location, not no
work or no outstanding need. Partial enumeration or unreadable entries means
incomplete discovery, not an empty result. Historical accounts elsewhere stay
in place; only an explicitly supplied legacy reference is inspected under the
same project containment and identity checks. No broad filesystem crawl,
implicit migration, copying or reassignment of old identities is authorized.

## 5. Visibility, consumers and production order

Show the bound project, relative target, record identity/version, source-route
standing and recorded gaps/duties. A zero-read account displays unsupported
answers and gaps, never an answer purportedly derived from files. Show storage,
validation and discovery failures with their actual affected reference; do not
promote a saved record into evidence of source truth, performed duty, readiness,
need satisfaction or acceptance. Sensitive source content follows the governing
account/host rules; directory placement supplies no new disclosure authority.

DEL-06-01 may later choose a separate descendant of `.chirality/records/` and
reference these accounts as files. DEL-06-02 may present the reference and
waiting cause after adoption. Neither must implement fleet software, choose
its own descendant, or share a writer before C implements this definition.
Concurrence covers namespace/reference compatibility only. Any actual D-first
prerequisite, cycle, invalidated completed work, or owner-reserved allocation
conflict returns through WORKING_ITEMS/HELP_HUMAN under GC-7.

## 6. Required implementation examination

Before persistence is considered complete, examine real file operations for:
round-trip/restart discovery and bound-reference resolution; whole-project
move; each supported account version; source-free gaps; collision refusal;
malformed/unknown/duplicate records; unwritable directory; link and ancestor
substitution attempts, concurrent ancestor/root rename and uncertain-location
recovery (including a move between checks, whose absence cannot be proved); interruption before/after publication and uncertain
commit recovery; concurrent distinct writers and identical-target contention;
unchanged original bytes following failed or repeated writes. Verify visible
failure and absence of silent relocation on each applicable failure path.

These are future implementation checks, not claims that this definition ran
or that platform-specific atomicity has been proved. Final source adoption
requires DEL-06-01 concurrence and independent review of this exact amendment.

### CRP-R1 required rename-race case

Pause a real writer after it has opened the verified account-directory
capability but before publication. Rename that directory or an ancestor away
and put a distinct replacement at the former pathname; resume the writer.
Verify it never writes into the replacement, that any publication occurs only
through the original capability, and that the post-path comparison reports
uncertain location without a successful durable reference or automatic retry.
Inspect original and replacement bytes and recover the original identity
explicitly. Also exercise a rename restored before the post-check: the test
must preserve the stated transient-move limitation rather than assert that
pre/post checks prove continuous membership. A later discovery mismatch must
refuse reference reliance and require reconciliation. These are required
implementation observations; none is reported performed by this definition.

### CRP-R2 required temporary-substitution cases

Exercise macOS exclusive rename on the actual tested filesystem: ordinary
success consumes the temporary name and preserves intended inode/bytes;
collision retains both entries and returns no binding; unsupported operation
fails closed without fallback. Preserve all error-path temporary entries and
report them as recovery issues.

Inject source-name substitution both after temporary sync and **after the
final prepublication check, immediately before rename**. The first must refuse
observed substitution. The latter must expose the actual residual: foreign
entry moves to final name, original moved-aside entry remains, postcheck
rejects the foreign inode and returns uncertain commit with no successful
binding. Test a foreign schema-valid account, identical bytes in a foreign
inode, symlink/non-regular substitutions, and existing destination collision.
Inspect original, replacement and target after failure; no automatic unlink,
rollback or retry may conceal or further mutate the race outcome. Cold
recovery must not relabel foreign discovery as a successful publication.
These tests are future required evidence, not performed by this document.

Technical API basis: Apple's XNU `bsd/man/man2/rename.2` documents
name-based relative-directory rename and `RENAME_EXCL` destination refusal:
https://raw.githubusercontent.com/apple-oss-distributions/xnu/main/bsd/man/man2/rename.2
The documentation does not qualify a particular runtime/filesystem. Actual
platform support and the injection cases require implementation evidence.
