# Connector route-account placement CRP-v0.1

Named technical design selection: C3-PLACE-01. Status: proposed definition
pending DEL-06-01 concurrence and independent review. Prepared by DEL-07-02
source owner under WORKING_ITEMS; HELP_HUMAN identified O-D placement as a
technical selection within DEL-07-02/DEL-06-01 ownership, not a new human
gate. This document does not record a new owner act, consumer adoption,
implementation or permission to persist before those checks.

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

Resolve the project-root input once to a directory and retain that resolved
root as the operation's anchor. A symlink spelling of the selected project
root may resolve to its actual root; display/use that resolved identity and
keep it stable for the operation. Below that anchor, reject symlinks in every
`.chirality/records/connectors/route-accounts` component and in the target;
reject non-directory ancestors and non-regular account files. No account path
or recovered reference may escape the anchor by `..`, absolute path, links,
or equivalent platform syntax. Hard-linked pre-existing targets are never
write destinations; writes create new files only.

Use directory-handle-relative operations with no-follow/exclusive guarantees
(or a platform equivalent demonstrating the same behavior), not a separate
path-string check followed by an unprotected open. Check containment at use;
a changing ancestor or substituted directory must fail visibly rather than
redirect the operation. If the host cannot establish the guarantee, refuse
the write. Permissions are those enforced by the host; this design grants none.

## 3. Write-once commit and failure behavior

Validate the chosen schema version and semantic source-account invariants
before writing. Build complete UTF-8 JSON bytes before publication; record the
actual timestamp provenance, recorder and duty standing. Serialization or
validation failure leaves no published account.

Create a private temporary regular file exclusively inside the same anchored
account directory. Write the complete bytes, flush and sync them, then publish
the final basename atomically with a no-replace operation. Sync the directory
where supported/required for the promised durability. A successful return
requires publication and the host's durability steps to complete. An API that
can replace an existing target is not an acceptable no-replace substitute.
Readers never consume temporary names as accounts.

If the operation fails before publication, report the failure and remove only
its own temporary file where possible; a leftover temporary file is a visible
recovery issue, never an account. If publication may have occurred but a later
step fails, report an uncertain commit with the target and intended byte hash;
do not claim success or retry automatically. Recovery checks that exact file
and identity before a caller elects any next write. No published file is
silently modified, deleted, moved or replaced to repair an error.

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
substitution attempts; interruption before/after publication and uncertain
commit recovery; concurrent distinct writers and identical-target contention;
unchanged original bytes following failed or repeated writes. Verify visible
failure and absence of silent relocation on each applicable failure path.

These are future implementation checks, not claims that this definition ran
or that platform-specific atomicity has been proved. Final source adoption
requires DEL-06-01 concurrence and independent review of this exact amendment.
