# C3-P bounded route-account persistence

TASK `/root/group_c_successor/route_persistence` returns the backend contribution
under WORKING_ITEMS `/root/group_c_successor`. Basis and exact source/output
hashes are in `C3_PERSISTENCE_BASIS.json`. The commit carrying this record is the
author candidate; the manager supplies independent review and integration.
No push or merge was performed by this child.

## Implemented boundary

`connector_route_store` accepts schema-valid caller accounts in format 0.1 or
0.2 through an explicit opened project. Exact maintained copies of the two
route schemas and standing dependency compile with external retrieval disabled;
a regression check compares their complete bytes to the maintained Design.
The caller's account fields, recorder/time provenance and duty standing survive
serialization. No source read, source truth, semantic reference validation,
performed duty or authority follows from this shape check.

New records use independently generated UUID-v4 names under
`.chirality/records/connectors/route-accounts/`. All descendants are opened
relative to retained directory handles with no-follow flags. Canonical root and
ancestor identities are compared before writing and after publication. Private
exclusive temporary files are written/flushed/synced; macOS additionally calls
`F_FULLFSYNC`. `linkat` publishes atomically without replacement, the private
name is removed and the directory synced. Readback checks regular-file identity,
exact byte hash, account ID and version. Collision is visible, with no retry.
A later failure exposes an uncertain attempt, target/hash and original directory
and file identities. Published targets are never silently repaired or removed.
Cleanup failure retains a separately visible temporary-file issue.

Cold discovery enumerates through an independent directory handle and preserves
malformed, unknown-version, noncanonical, symlink/nonregular/hard-link, temporary,
duplicate and unreadable conditions. Duplicate IDs retain all paths, with no
winner. Missing directories mean only that no accounts were found there;
incomplete discovery remains distinct. A held reference carries relative path,
account/version/hash and observed filesystem identities. Resolution refuses
changed bindings and duplicate identities; read-only reconciliation checks the
exact attempted binding without searching outside the selected project. An
explicit legacy relative binding uses the same anchored checks, without a crawl.
Whole-project relocation can retain the binding when directory/file identities
remain the same. Copying bytes into a distinct directory does not silently adopt
that new identity or transfer authority.

The public surface is a Rust library seam, not a Tauri command or UI. Full source
reconstruction, broader semantic checking, native presentation, provider joins
and consumer adoption remain C3/receiving-owner work. All fields required to
show account claims/gaps/duties remain in the returned account value.

## Executed checks

One private APFS copy-on-write clone of the inactive C1 Cargo target was used;
its existing objects are a local acceleration, not portable proof. Actual
candidate files were rebuilt and tested with the approved Group A offline
Cargo home, `CARGO_NET_OFFLINE=true` and `CHIRALITY_SKIP_CODEX=1`. No download,
supplier launch or native App launch occurred. Rust/Cargo 1.92.0; macOS 26.6.2
arm64. From `app/src-tauri`:

```text
cargo test --offline --locked connector_ --lib -- --nocapture
25 passed; 0 failed; 0 ignored; 423 filtered out
```

The 25 top-level checks comprise 18 route-store checks and 7 pre-existing
connector-standing checks. Two child processes additionally exit deliberately
with code 73 before/after publication; these are interruption observations,
not top-level passes or supplier executions.

| Requirement | Observed result |
|---|---|
| Exact 0.1/0.2 schema dispatch; CI-29; performed evidence-field presence | Both versions round-trip under distinct supplied IDs; source-free 0.1 and unsupported versions fail; invalid zero-read facts/support/gaps and unsupported performed-duty shape fail. A complete evidence-field claim remains unverified content. |
| Restart, project move, selected-root symlink | Cold resolve reproduces caller content and exact bytes; explicit relocated project resolves the same binding; stale old project path refuses. The initial root alias displays its resolved path. |
| UUID paths and input containment | Account ID is never the filename; malformed accounts leave no canonical store. Absolute/parent/backslash/empty-component reference paths refuse. |
| Collision and unchanged originals | Repeated identical-target writes fail with Collision, original bytes unchanged and no retained temporary. Eight distinct writers all succeed; eight same-target contenders yield exactly one success and seven collisions. |
| Cold malformed/unknown/duplicate/link/temp evidence | Issues are separate; duplicate IDs expose both paths and refuse reference reliance. Files, directories, links, FIFO and unreadable entries do not become accounts or an empty-success claim. |
| Permission and cleanup failure | Read-only directory refuses new publication; existing account remains. Failed temporary cleanup reports its name and cold discovery finds the leftover. An unreadable directory reports incomplete discovery. |
| Ancestor substitution | Each canonical ancestor as symlink/non-directory refuses. Outside replacement directory remains empty. |
| CRP-R1 rename race | Writer is paused after temporary sync/precheck; each root/ancestor/account directory is moved away and replaced. Publication follows the original capability only; replacement stays empty; postcheck returns uncertain location and no durable-success reference. Restoring the exact directory allows explicit cold reconciliation. No retry occurs. |
| Transient move and later mismatch | Move outside the current project tree, publish there, then restore before postcheck: success is an observed comparison only. Test explicitly observes the outside publication. A subsequent move/replacement refuses reference reliance. Continuous pathname containment is not claimed. |
| Interruption and tampering | Injected before/after-publication failures distinguish definite from uncertain outcomes. Abrupt process exit leaves visible private temporaries; after-publication exit also leaves the temporary hard link, so reading is held until explicit test-caller cleanup. Published byte and same-byte inode substitutions return uncertainty and fail reconciliation. |
| Explicit legacy read | Only a supplied relative binding resolves; discovery does not search historical paths elsewhere. |

Initial test result was 14 passed/1 failed: the version-roundtrip fixture used
the same account ID twice and correctly triggered duplicate refusal. Giving
those distinct version fixtures distinct IDs repaired the test; no duplicate
rule was weakened. Initial sandboxed compilation could not write Tauri's
worktree permission metadata; scoped host escalation enabled the authorized
offline build. No automatic approval rejection occurred.

`rustfmt` was applied to the two new Rust files; `git diff --check` passed.
The staged private-term validator with `--from-host` is run immediately before
the commit and its result returned with the exact candidate revision.

## Limits and return

macOS operations were exercised on real temporary directories. The Linux
implementation is present but not compiled/run here; other platforms refuse
opening the store. Successful sync calls are observed, but physical power-loss,
hardware durability and actual fsync failure injection were not witnessed.
Partial enumeration has errno-aware failure handling; an induced mid-stream
readdir failure was not witnessed. Controlled operation-boundary failures do
not pretend to be those unperformed platform qualifications.

Opened-directory containment does not guarantee continuously current pathname
membership against external renames. Pre/post checks cannot eliminate the
transient-move residual selected in CRP-v0.2. Cold observations likewise are
not a filesystem snapshot or a promise against changes after return.

This contribution does not change any Design/schema semantics, CI, instruction,
work graph, other runtime implementation, frontend or previously integrated
CI-29 source file. The maintained resource copies are exact. SEAL-2 remains
held. No credentials, sign-in, provider/person act, MEMORY write, external
owner work, new human decision, acceptance, qualification, release or 90% claim
was performed. Independent candidate review and manager integration remain.
