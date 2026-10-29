# Windows platform services: proposed contracts and probe gates

Development design, 2026-10-28. **Proposed, unimplemented, unrun on Windows.**
This does not select Windows shipping/support, change a guarantee, qualify a
supplier, record acceptance or authorize provisioning/execution. macOS remains
independently finishable. No production behavior changes accompany this document.

## Basis, ownership and affected consumers

App source basis throughout: `79315c26b104b534a89ed8e9b1e716f3da3440d0`
(including first feasibility `716a8e795968b82c42f84cf67f26ad817d64bdfe`).
Paths below are relative to this App repository at that revision unless qualified.
Selected instruction library: `/Users/ryan/dev/chirality`, revision
`1560bbf7f7add4637a20572a2b0d404ef121af63`, WORKING_ITEMS and
`workflows/coordinated-knowledge-work/WORKFLOW.md`. Consultation does not adopt
new packaged roles/workflows. The App's current supplier definition is 0.160.0;
older observations at 0.158.0 remain older observations.

Owning contracts are DEL-01-01 `HOSTING_BOUNDARY.md` H5/H10/H11, §§4.2–4.5;
DEL-01-02 `EXECUTION_AND_RECOVERY.md` DEF-1…7, §5 SQ-Q, §6 U-16 and §7;
DEL-01-04 `APP_ACT_CONTROL.md` and `NATIVE_INTERACTION_RECEIVING.md`;
DEL-01-05 `ACCOUNT_AND_PROVIDER_ACCESS.md` §3 and CR custody rules. ACT is
DEL-04-01 `Design/ACT_AND_POLICY_CONTRACT.md` where applicable. File/record consumers
include `act_control_file.rs`, `attachments.rs`, `attachment_custody.rs`,
`records_store.rs`, `records_retention.rs`, `record_lines.rs`,
`distribution_store.rs`, `instruction_store.rs` and workflow library publishers.
These consumers have different authorities; a low-level service cannot grant
permission, turn an agent claim into a human act, or turn native completion into
durable recording. DEL-02-03, DEL-03-03 and DEL-04-03 receive custody/outcome
facts, not new authority. Native confirmation remains Rust-owned under OI-008.

The contracts below specify one common semantic boundary with platform-specific
mechanisms. They are probe targets, not a request for a broad production refactor.
Existing Unix guards remain. Unsupported Windows branches must refuse explicitly.
Owning ScopeOfWork and dependency conditions stay unchanged: this investigation
does not satisfy their execution/qualification/acceptance conditions.

## P: actual-spawn process custody

### Existing App behavior, including limits

| Event | Source-bound behavior to preserve |
|---|---|
| Window close/hide/reload | No supplier stop or request answer. `app_quit.rs` window rules and RECOVERY DEF-1/SQ-W keep work alive. |
| EOF while ready | `hosting.rs:3857` `on_eof_process` waits for the **original leader's observed exit** before LT-12 and closure. EOF alone is not exit; a leader can close stdout and remain alive. After exit, survivors are observed/retained, not killed by the EOF rule. |
| EOF before ready / failed startup | Same function can kill the captured original group during handshake; startup abort also uses `OwnedProcess::abort_spawn`. It must not publish a ready generation after failed admission. This differs from ready EOF. |
| Leader exit with pipe still open in descendant | Reader-triggered EOF processing can be delayed by inherited stdout. The platform observer must expose leader exit separately; it must not claim the current reader-driven lifecycle already closes promptly in this case. |
| Stop / Restart Codex | `hosting.rs:3974` `stop_inner` checks the full target tuple under the source gate, records Stop, closes stdin, waits a 3 s test-value grace, forces the original group if needed, then observes again. LT-23/state `stopped` can carry null exit fields or unknown/surviving descendants. The state label is not an all-exited receipt. |
| Normal App quit | `app_quit.rs` `quit_sequence` and `finish_exit:422`, `lib.rs:2789–2807`: native confirmation when live/unknown work warrants it, reassessment, close new-turn admission, recorded interrupt requests, bounded wait, then each home's process Stop, then session end. No run is ended and no outstanding request is answered by that sequence. |
| System termination with callback time | `finish_exit` first attempts `session_ended(system-terminated)`, then best-effort Stop of each home. The early marker does not prove later cleanup completed. |
| App crash / hard termination without callback | No `Drop` parent-death killer, death signal or equivalent in `process_group_custody.rs`. Kernel closure of App pipe ends may lead to supplier EOF; descendant copies and supplier behavior prevent an exit guarantee. A missing end record remains unknown on reopen. No source-backed promise that every supplier descendant dies on App death. |

`process_group_custody.rs` mints custody only inside actual spawn, binds once to
`{appSession, home, spawnCounter}`, keeps the original child unreaped with
`waitid(WNOWAIT)`, and serializes census/signal/retirement. A complete empty
group observation plus original leader exit permits retirement/reap. Lost or
unavailable observation is not empty. The macOS census covers the reserved
group only; detached/escaped descendants are explicitly unobserved. RECOVERY
U-16's overlap policy is still a proposal: record survivors after unexpected
exit, show them with a person's termination action, permit a successor after a
test-value overlap wait. No stronger implemented descendant UI is inferred.

### Proposed capability and outcomes

`SpawnCustody` is an in-memory, non-deserializable capability created by one
successful owned launch; bind it exactly once to the complete generation.
Acquire an operation lease before checking source currency, then retain the
captured capability through blocking work. A successor never replaces its
target. Persisted PID, Job name, JSON generation or exit code is evidence only.

Suggested operations (names are specifications, not existing APIs):

| Operation | Required evidence / refusal |
|---|---|
| `spawn_contained(launch, generation)` | Returns original process/Job ownership only after safe assignment and binding; otherwise startup refused, child kept suspended until termination/exit observation or explicitly retained cleanup-unknown custody. |
| `observe_leader()` | `running`, `exited(code, observedAt)`, or `unknown(api,error)` from the original process HANDLE. `WaitForSingleObject(handle,0)==WAIT_OBJECT_0` establishes termination; only then query `GetExitCodeProcess`. `STILL_ACTIVE`/259 by itself is ambiguous with a real exit code of 259. |
| `observe_members()` | Contained active count with time, query completeness and scope, or unknown. No global name/PID search and no invented zero on denied query, buffer limit or churn. A populated PID list is diagnostic, not termination authority. |
| `request_stop(expectedGeneration,cause)` | Full-generation check and stop observation before closing this source's stdin; after grace use owned `TerminateJobObject`. Record attempted/succeeded/error separately. API success is a request result, not confirmed exit. |
| `retire()` | Serialize with stop and observation. Only retire as confirmed empty after original leader termination and authoritative Job active-zero observation with no external assignment authority. Unknown custody remains retained/marked unavailable. Closing handles never becomes a later numeric action. |

Job Objects are a **candidate containment mechanism**, not an adopted policy.
Use unnamed `CreateJobObjectW`, `SetInformationJobObject` and non-inheritable
Job/process handles. Initial candidate uses `CreateProcessW(CREATE_SUSPENDED |
EXTENDED_STARTUPINFO_PRESENT)` with explicit executable, properly encoded
arguments, environment/cwd and `STARTUPINFOEX` handle allowlist; inherit only
intended stdio handles. Close App copies of child-side pipe handles. Assign
the suspended process with `AssignProcessToJobObject`, bind source custody,
then `ResumeThread`; never spawn-running-then-assign. Closing the primary
thread HANDLE is not resume. On any assignment/resume/publication failure,
terminate the original suspended process (or assigned Job), wait/observe its
exit and retain error/unknown facts; no runnable uncontained fallback.

This prevents **child code** escaping before assignment. Suspended creation
alone leaves an App-crash window between creation and assignment. Probe a
creation-time `PROC_THREAD_ATTRIBUTE_JOB_LIST` variant on the selected Windows
11 target before choosing a production launch mechanism; it can establish Job
membership during creation, but does not settle crash cleanup policy. A crash
with kill-on-close off may still leave a suspended child. That is a reserved
policy/launch-safety issue, not permission to claim leak-free creation.

Windows 8+ supports nested jobs subject to hierarchy/limit restrictions. Detect
the parent's actual Job situation (`IsProcessInJob`); test nested assignment in
the intended launcher/CI context. Do not set `CREATE_BREAKAWAY_FROM_JOB`,
`JOB_OBJECT_LIMIT_BREAKAWAY_OK` or `SILENT_BREAKAWAY_OK` as a workaround.
Refuse incompatible nesting; do not escape another host's constraints. Ensure
supplier descendants inherit containment in the fixture. Services, brokers and
preexisting processes outside this Job are not thereby contained.

Keep process HANDLEs until exit evidence is captured and Job HANDLEs until
retirement or explicitly reported observation loss. No child receives a Job
HANDLE or a way to assign unrelated processes. Job activity queries include
descendants in their stated hierarchy; use documented accounting active count
for zero, and bounded `JobObjectBasicProcessIdList` queries for diagnostics,
retrying `ERROR_MORE_DATA` within a fixed budget. Completion-port messages may
trigger re-query; do not rely on notification delivery alone as complete exit
proof. A live Job with no breakaway/external assignment and authoritative active
zero cannot later sprout a child. If those assumptions are unestablished,
report unknown, retain handles and refuse confirmed retirement.

**Reserved P1 — App hard-death policy.** Recommend initially preserving the
current App distinction: kill-on-close **off**, explicit Stop on normal quit,
ready-exit survivors recorded. Consequence: hard App death can leave children
and can lose observation/control of a Job; never reacquire custody from a
recorded PID/Job name after restart. This recommendation leaves the suspended
creation crash window unresolved until the creation-time-assignment probe and
owner decision. If the owner wants mandatory death of all contained suppliers
on App death, adopt `JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE` explicitly and prove
last-handle ownership; closing a Job on retirement/error then becomes
destructive. It also kills recorded survivors if the App dies. This would add
a guarantee/policy and cannot be borrowed from SWB. Stronger no-breakaway
containment also changes the scope of explicit Stop relative to Unix escaped
descendants; present that consequence for owner disposition before adoption.

## F: namespace, identity, locks and publication

### Existing behavior and proposed Windows boundary

`storage.rs:116` checks owning paths for symlinks; its lock functions use Unix
`flock` and hold the `Ownership` file plus admission lease for its lifetime.
`sync_dir`, `sync_publication` and `publish_json_observed` flush file and folder
ancestry; create-once uses same-directory temporary + hard link without
replacement, mutable metadata uses rename. A failure after publication was
attempted is uncertain even when the final file is readable.
`act_control_file.rs:127` reads the **opened** non-followed subject, compares
handle metadata before/after with the named object and freezes content for the
native act. `attachment_custody.rs` and `recovery.rs` impose regular/single-link
and native-namespace constraints beyond a path check. Preserve those distinctions.

Proposed `OpenedIdentity` contains a live HANDLE plus `FILE_ID_INFO`
`{VolumeSerialNumber, FileId[16]}`, object kind, attributes/reparse tag,
link-count evidence, final volume path and access/share mode. Use
`CreateFileW`, `GetFileType`, `GetFileInformationByHandleEx(FileIdInfo,
FileAttributeTagInfo, FileStandardInfo)` and, where needed,
`GetFileInformationByHandle`/`GetFinalPathNameByHandleW`. An unavailable identity
refuses the owning operation; file ID is volume-scoped and reusable after
deletion, so it is no durable authority without retained handles/content basis.
Never compare two pathname stats as proof of the object actually read/written.

Initial **recommended probe envelope**, not a new supported-filesystem promise:

- Fixed, guest-local NTFS volume; fully qualified drive path resolved to its
  actual volume. Reject UNC/SMB, mapped network drives, removable/non-NTFS,
  drive-relative `C:foo`, relative/root-relative paths, arbitrary device paths,
  ADS (`:` inside a component), reserved names and ambiguous trailing dots or
  spaces. Refuse unsupported names visibly. Internal volume-GUID/extended paths
  require controlled normalization; do not accept arbitrary `GLOBALROOT` or
  pipe/device names. SUBST/mount/drive alias handling needs verified final-volume
  binding; initially refuse aliases rather than treating drive letters as IDs.
- Open root and each existing component with `FILE_FLAG_OPEN_REPARSE_POINT`
  and directories with `FILE_FLAG_BACKUP_SEMANTICS`; reject **all** unexpected
  reparse tags (junctions, mount points, symlinks, cloud placeholders), not just
  symlink tags. That flag protects only the final component of each open.
  Hold a chain of namespace guard handles that deny delete/rename and reparse
  mutation through their sharing/access combination; a candidate omits
  `FILE_SHARE_DELETE` and `FILE_SHARE_WRITE` on directory guards. Prove compatible
  child creation/SQLite operation and resistance to already-open writers in
  F-01 before relying on it. Win32 absolute-path component checking alone is
  not `openat` or an atomic ancestor guard. If the chain cannot be pinned with
  supported APIs, refuse the affected operation; a custom VFS or different
  root-relative primitive is a later scoped design question.
- Owning metadata, DB, sidecars, locks and evidence leaves must be regular
  disk files, no unexpected reparse point and single-link where the consumer
  currently requires it. Query actual handle link count; do not broaden a
  consumer that currently permits multiple links by imposing another's rule.
  Publisher-owned temporary/final hard-link pair is a narrow, lock-held
  exception until cleanup; not permission to accept arbitrary hard aliases.
- Native path bytes/UTF-16 identity is distinct from lossy display. Case-folded
  strings or prefix matching do not prove containment; handle/volume IDs and
  component boundaries do. Read handles must preserve source attribution if
  a pathname later changes; stale native-act offers fail before capture.

**Access exception:** App homes intentionally link `config.toml`, `AGENTS.md`
and `skills/` to explicitly selected shared resources (`home_resources.rs`,
AAC §3). The non-Unix setup branch currently refuses link creation. Do not
silently copy these resources or permit arbitrary reparse traversal. A future
Windows home service must separately validate the exact declared link, target,
namespace lease and generation; inability to create/verify it is an explicit
setup blocker. No Developer Mode, privilege, DACL or global setting change is
authorized. Probe invented nonsecret home/profile files only. Windows access
security needs actual token/DACL evidence; Unix mode bits/read-only attributes
are not ACL parity. Supplier owns credentials; the platform service must not
read or relocate them. No sign-in/key entry is part of these probes.

### Lifetime lock contract

Candidate sentinel lock: stable regular single-link file opened once with
`OPEN_ALWAYS`, read/write access, share read/write but **no share delete**, and
validated handle identity; never delete/recreate the sentinel to unlock.
`LockFileEx` a fixed range `[0,1)` with independent open HANDLE per owner:
exclusive or shared; add `LOCKFILE_FAIL_IMMEDIATELY` for try-lock. Only a real
lock-conflict error maps to busy; denied/invalid/IO errors remain unavailable.
Use synchronous handles or correctly complete/wait/cancel OVERLAPPED locking;
`ERROR_IO_PENDING` is not acquired. Owner Drop uses `UnlockFileEx` on the same
range then closes the HANDLE. No lock HANDLE inheritance; OS crash cleanup
must be observed before another owner is admitted. Preserve records-retention
shared admission leases and nonblocking removal exclusion; SQLite's own locks
do not replace these locks, and these locks do not replace SQLite transactions.
These are cooperating App locks, not protection against administrators or
arbitrary malicious same-user memory writers.

### Publication result contract

Represent independent facts: `not_attempted`, `attempted(outcome_unknown)`,
`visible(identity,exactBytes)`, and `durability_confirmed(profile,evidence)`.
Record the irreversible boundary **before** making the namespace syscall;
failures after that point default unknown unless a documented error and
revalidated namespace prove nonpublication. A reader finding expected bytes
can establish visibility/reconciliation, not retroactive flush success or a
new human act. No automatic resubmission of an uncertain capture/operation.

Candidate sequence: same-directory `CREATE_NEW` random temporary; complete
write; `FlushFileBuffers` the actual writable HANDLE; while holding owning
locks and namespace leases, publish with no overwrite for create-once.
`CreateHardLinkW` is the closest source-preserving candidate (then remove only
the owned temporary name), or probe same-volume `MoveFileExW` without
`MOVEFILE_REPLACE_EXISTING`/`COPY_ALLOWED`. Existing final name must win unchanged.
For explicitly mutable metadata only, probe `ReplaceFileW` (existing target)
or `MoveFileExW(MOVEFILE_REPLACE_EXISTING | MOVEFILE_WRITE_THROUGH)` with no
cross-volume copy; preserve the required ACL/attributes/content facts. Never
implement replacement as delete-then-create. Sharing violations are failures,
not reason to weaken identity or sharing guards. Probe reader visibility,
replacement errors and cleanup interference; do not assume every failure
left both names unchanged. `ReplaceFileW` documents partial failure states
and **does not support `REPLACEFILE_WRITE_THROUGH`**.

**Reserved F1 — namespace durability.** File flush success, NTFS journaling,
successful link/rename, re-open and process-crash recovery do not establish the
current `storage::sync_publication` ancestry flush guarantee. Microsoft documents
`MOVEFILE_WRITE_THROUGH` flush behavior for copy/delete moves; it is not proof
of every same-volume link/rename and parent-creation barrier. A directory HANDLE
opened with BACKUP_SEMANTICS is not automatically a supported `fsync` equivalent.
Volume flush requires additional authority and is not proposed. Recommend keep
Windows durable capture/record publication **unavailable/unknown** until a
documented, measured durability profile is reviewed and any changed guarantee
is owner-approved. That restricts the first connected slice until resolved;
do not relabel visible fixtures as confirmed durable to finish it.

## S: pinned SQLite actual-opened-file binding and durability

`Cargo.lock` pins rusqlite 0.32.1 and libsqlite3-sys 0.30.1 (`bundled` in
Cargo.toml). The latter's bundled `sqlite3/sqlite3.h:149` is **3.46.0**.
Existing `recovery_store.rs:652` proves actual `main` descriptor identity on
Unix through version-checked `FILE_POINTER`/`VFS_POINTER` and a Unix-only layout;
it cannot be copied to Windows or replaced with before/after path stats.

### Supported Windows API, verified in the local pinned dependency

The documented `SQLITE_FCNTL_WIN32_GET_HANDLE` is **available in this pin**:

| Pinned bundled source | Checked fact |
|---|---|
| `sqlite3.h:1082–1086`, `:1233` | Documents native file HANDLE output through pointer-to-HANDLE; opcode 29. |
| `sqlite3.c:50169`, `:50236–50240` `winFileControl` | `LPHANDLE phFile = (LPHANDLE)pArg; *phFile = pFile->h; return SQLITE_OK;` outside `SQLITE_TEST`. The adjacent SET_HANDLE is test-only; GET_HANDLE is not. |
| `sqlite3/bindgen_bundled_version.rs:211` | ffi exports `SQLITE_FCNTL_WIN32_GET_HANDLE: i32 = 29`. No internal `winFile` prefix inspection is necessary. |
| `sqlite3.c:51800–51888` `winOpen` | Writable main opens with `CreateFileW`, ordinary flags and `FILE_SHARE_READ | FILE_SHARE_WRITE`, omitting share-delete. No general reparse refusal is added here. |
| `sqlite3.c:52248–52439`, `:61875` | Windows full-path processing does not report `SQLITE_OK_SYMLINK`; generic NOFOLLOW handling only acts when VFS does. Keeping `SQLITE_OPEN_NOFOLLOW` is necessary but **not sufficient proof of Windows reparse rejection**. |

Local dependency source was read under the existing Cargo registry cache,
not downloaded or executed. Its file digests and lock/archive identity appear
in the adjacent `windows-platform-evidence.json`. They establish this inspected
source, not the eventual Windows executable's VFS/runtime identity.

Probe algorithm, under exclusive ownership of the live rusqlite connection:

1. Require `sqlite3_libversion_number()==3046000`, record `sqlite3_sourceid`,
   compile options and `SQLITE_FCNTL_VFS_POINTER`/VFS name. Use the stock locking
   Windows VFS, not `win32-none` or an unverified shim. Verify no `NO_SYNC` build.
2. Initialize a native `HANDLE` variable to null; call
   `sqlite3_file_control(db, "main", SQLITE_FCNTL_WIN32_GET_HANDLE, &handle)`.
   Require `SQLITE_OK`, neither NULL nor `INVALID_HANDLE_VALUE`, `FILE_TYPE_DISK`,
   then query identity/kind/reparse/link metadata **on that returned HANDLE**.
   It is borrowed from SQLite: do not close it, wrap it in owning Rust `File`,
   change its position, or use it after connection close. A duplicated HANDLE,
   if needed for ownership, must be non-inheritable and scoped separately.
3. Independently open the guarded namespace leaf without following reparse,
   compare its volume/file ID to the SQLite HANDLE and the retained expected
   binding; revalidate the pinned component chain. Before schema/import/write,
   require regular/single-link source and source-current namespace lease.
   Failure to obtain or compare actual handle identity refuses the open/write.
4. Retain the connection, directory leases and leaf binding through transactions;
   recheck before writes. SQLite's omitted share-delete helps keep an opened
   main file from replacement, but does not protect all ancestors, prevent hard
   links or pin the sidecars. It is not the entire namespace guard.

Important limit: public GET_HANDLE binds **main**, not every journal/sidecar.
Preflighting `-journal/-wal/-shm` paths alone cannot prove the journal SQLite
will subsequently open. Main's VFS `winOpen` can also create before a post-open
identity check, and opening a hot journal can cause recovery writes before
the App's guard runs. First probes must use an already created, pinned,
invented DB and protected namespace; no write into an unproved path. S-02 must
challenge sidecar and open-time races. If directory pins and access policy
cannot prevent those races for every SQLite open, refuse production open and
scope a supported VFS wrapper for all `xOpen` paths before implementation.
Do not infer that GET_HANDLE solves the entire security boundary.

### What Windows durability can honestly establish

Keep the current rollback `journal_mode=DELETE`, `synchronous=EXTRA` checks as
the comparison basis; do not silently switch to WAL/PERSIST to avoid a barrier.
The pin's `winSync:49649–49730` calls `FlushFileBuffers` (also `FlushViewOfFile`
if mapped), returns `SQLITE_IOERR_FSYNC` on failure; `SQLITE_NO_SYNC` makes it a
no-op. `winDelete:51996–52014` expressly ignores `syncDir`. Consequently EXTRA's
requested journal-unlink directory sync does **not** establish such a barrier
on this VFS. `fullfsync` and `checkpoint_fullfsync` PRAGMA readbacks do not turn
Windows into macOS `F_FULLFSYNC`; stock Windows sync ignores that distinction.
The current App's extra `storage::sync_dir(folder)` confirmation condition is
still unresolved on Windows. A successful SQLite COMMIT can have landed while
the App reports unknown/not confirmed; never retry that batch blindly.

Within a declared tested OS/VFS/NTFS/storage profile, probes can establish
transaction atomicity, append ordering, rejection behavior, explicit API flush
results and **process-crash** reopen behavior. They cannot prove universal
power-loss survival, drive-cache honesty, hypervisor/host flush propagation or
namespace ordering for all media. No VM reset/power-off fault test is authorized.
Recommend S1: preserve unknown durability when the namespace barrier cannot be
established, and request a scoped owner decision on an honest Windows profile
before promising confirmed durable reopen. Choosing a different journal/VFS
would need its own reviewed design and regression work.

## Isolated probe and regression specification

Everything below is **not run**. Execute only after exact owner authorization
and prerequisites; no current supplier/guest/package operations are implied.
Use an invented local NTFS directory, fresh scratch CODEX_HOME, no credentials,
no private files, offline fixtures, explicit cleanup and separately attributed
native-x64 versus ARM guest/emulated-x64 evidence. No global path/permission
changes. First implement tiny standalone probe binaries, not production services.

Each result must capture source/build hashes, OS/architecture/VFS, exact APIs,
flags/rights/share modes, monotonic event order, generation, errors, returned
observations and limitations. Record attempted actions before calls. Timeouts
produce unknown/refusal, never success; fixed test deadlines are not support
guarantees. Helpers self-report through private fixture pipes/files, not process
name searches. The harness retains original process HANDLEs for cleanup proof.

P-01 must expose early execution even if a later marker is delayed. Use an
ordered private fixture trace: record successful leader assignment and full
generation binding before the harness calls resume; the helper's first fixture
action reports entry, then reports/acknowledges the child-creation attempt
**before** calling `CreateProcessW`. Capture the creation result and the child's
first observable nonce-bearing effect separately. Transfer a non-inheritable
duplicate of the actual returned child process HANDLE to the harness, with only
the query/wait/cleanup rights needed; do not reopen by PID. Keep the child alive
until the harness checks `IsProcessInJob(childHandle, originalJob)` and captures
the result, or report membership unavailable. A final helper marker cannot
substitute for those events or prove the earlier creation order.

Include a deliberately broken **running-before-assignment negative control**:
allow the helper to create its child and require the child's first effect and
retained HANDLE before assigning the leader; delay the helper's final marker
until after assignment/binding. The checker must reject this run despite that
late marker, establish that the preexisting child is outside the original Job,
and clean it up through its retained HANDLE with exit observation. Failure to
observe the negative control's ordering/membership is an inconclusive probe,
never a passing launch contract. The positive runs require assignment/bind
before helper entry/creation attempt, every created descendant in the original
Job, and explicit ordering/observation of its first effect. The test harness's
extra control handles are fixture-only and confer no production Job authority.

| ID | Setup and falsifiable operation | Pass / required refusal |
|---|---|---|
| P-01 assignment | Use the ordered entry/creation-attempt/child-effect trace and retained descendant HANDLE above. Exercise suspended assign/resume and creation-time Job list; inject Job setup/assignment/resume failures and incompatible outer job; run the deliberate early-escape negative control. | Positive assignment/bind precedes helper execution/creation attempt; actual descendant membership established. Negative control rejected even with delayed final marker. Failure child never resumed; original exit observed or cleanup explicitly unknown. No running-then-assign or breakaway production fallback. Record parent-crash window separately. |
| P-02 independent observations | Helper A closes stdout then waits; B exits while descendant holds stdout; C exits with code 259. | A: EOF but leader running; B: leader exited independent of EOF, descendant live; C: signaled handle plus 259 means exited. None implies empty Job or observed supplier result. |
| P-03 Stop/generation | Helper descendant survives stdin EOF; Stop after recorded cause/grace. Replace current Host slot with g+1 while g Stop waits; attempt second bind, serialized PID input and stale-generation Stop. | Only g's Job terminated; g+1 untouched; no second bind/cold authority; termination success alone not confirmed exit. Observe original leader and Job zero before confirmed retirement. |
| P-04 custody/unknown | Deny/inject query error; force PID-list buffer overflow/churn; delay completion messages; cancel cleanup; attempt inherited/duplicate Job handle and descendant breakaway. | Unknown never zero, no released authority reused; no Job handle in child; no breakaway. Confirm retirement only with authoritative zero/leader proof; fail safely on nesting restriction. |
| P-05 quit/death | Two invented homes: cancel quit, confirm quit, callback system exit, hard-kill a fixture parent. Separately test P1 candidate modes, including a parent killed between creation and assignment and while descendants survive leader exit. | Cancel has no interrupt/Stop; normal quit records before effects and stops each original home; hard death reported under the actual selected mode, never an invented session-end/exit. Handles stay owned until proof or explicit loss. No SWB policy imported. |
| F-01 namespaces | Ordinary path then junction/symlink/unknown reparse at every ancestor/leaf; hard-link metadata leaf; rename ancestor, mutate reparse target and replace leaf between validation/open/use, including preexisting mutation HANDLEs. Test declared App-home links separately. | Actual opened identity matches retained root/leaf under pinned chain; attacks refused before effect or operation unavailable. Wrong target unchanged. Intended home links accepted only by explicit verified exception, otherwise setup unavailable. |
| F-02 path/access | UNC/network/mapped/SUBST, another volume, device/ADS, drive-relative, case aliases, non-ASCII UTF-16 and extended names; distinct scratch-user token only if separately authorized. | Unsupported envelope refused, aliases never independent authority. No ACL parity claim from attributes. No privilege/config/credential changes. |
| F-03 lock lifetime | Two processes plus two independently opened same-process handles, shared/shared, shared/exclusive, try-lock, denied open; kill one holder, then retry; attempt sentinel rename/hard alias. | Shared compatibility and exclusivity hold; busy distinct from unavailable; after OS releases dead holder lock new acquisition succeeds; sentinel identity stable. Removal cannot bypass live retention lease. |
| F-04 publication | Competing create-once publishers with different bytes; truncate/fail temp write; collision; concurrent readers during replacement; sharing interference; injected failures before syscall, immediately after namespace effect, after file flush and during cleanup. | One complete create winner, old final never overwritten by loser; replacement readers see complete old/new or explicit unavailable. Attempted/unknown kept when final landed; no false durable receipt or automatic retry. Verify link-count exception is only owned temp/final pair. |
| S-01 main identity | Pinned bundled SQLite opens guarded DB; GET_HANDLE identity compared with independent guarded leaf. Negative shim returns NOTFOUND/NULL/invalid handle; wrong VFS/version; race path swap. | Supported stock VFS exposes actual `main`; unsupported/invalid proof refuses before App writes. Two path stats cannot pass. Borrowed HANDLE not closed; connection still works after query. |
| S-02 sidecar/open | Hot-journal reopen and first-create fixtures; inject ancestor/reparse/sidecar swaps at SQLite xOpen boundaries through an isolated instrumented VFS forwarding to stock Windows VFS. | No unintended target written/recovered; if pins cannot exclude race, production open is refused and wrapper work remains prerequisite. Main GET_HANDLE alone cannot pass this case. Instrumented fixture is not evidence the uninstrumented production guard exists. |
| S-03 atomicity/history | Existing `recovery_store_tests.rs` cases: batch rollback, append-only triggers, exact JSON/index agreement, commit ordering, import-once, changed/invalid legacy input, torn final line, missing/locked DB. Reexpress OS-specific fixtures without reducing invariants. | Exact previous-or-whole-batch history, never partial; no duplicate landed-but-unconfirmed start, no fallback ledger/import rewrite, explicit limits. Index queries do not silently repair corrupt source. |
| S-04 flush/crash | Log stock VFS sync/delete returns and App post-commit barrier. Fixture child commits then is terminated at deterministic precommit/postcommit/postflush boundaries; reopen without killing VM/host. Inject `FlushFileBuffers` failure and post-COMMIT barrier failure. | SQL atomicity/reopen observed separately from namespace confirmation. Landed commit with failed barrier is unknown, not resent. Passing process-crash cases never declared universal power-loss proof. |
| N-01 connected slice | Only after P/F/S choices and regressions: standalone App launch, fully identified stock Windows 0.160.0 package, initialize/initialized, controlled stop, invented fixture publication/reopen and a real native control. Outbound denial must be established first. | Exact supplier distribution/preflight and fresh home/config; zero login/thread/model requests. Native capture and durable record receipts retain separate outcomes. Failure/unavailable branch remains visible. Stand-ins cannot satisfy stock supplier/native witness; no SWB dependency. |

Existing regressions worth porting include `hosting_process_group_custody_tests.rs`,
`hosting_startup_refusal_tests.rs`, `hosting_stop_admission_tests.rs`,
`app_quit_tests.rs`, `codex_stop_tests.rs`, `recovery_store_tests.rs`,
`records_store_publication_tests.rs`, `namespace_admission_tests.rs`,
`file_act_tests.rs` and `attachment_outcome_tests.rs`. Do not delete Unix tests,
remove `cfg` guards, replace expected refusal with success, or run a fixture
instead of a supplier and call it qualification.

## Peer constraint and next buildable slice

Read-only SWB basis: `/Users/ryan/.t3/worktrees/chirality/t3-514d37a1`,
production `1560bbf7f7add4637a20572a2b0d404ef121af63`; Windows candidate
`b78b0feac0aa1e6bbc4606597e10accc54b7eb51`. Its
`projects/chirality-piping/execution/PKG-04/DEL-04-07/Design/memory-budget-decision.md`
and `apps/desktop/src-tauri/src/solve_worker.rs:72–96` require workers to die on
App death. That is SWB's policy, not App adoption. Its manager's subsequent
source-qualified input distinguishes allocation-request gating before allocation
from polling a running mutator's footprint: pause-event delivery cannot prove
stopped excess. Its exact 2 s original-deadline/headroom commitment remains;
commit/working-set, counted grant and fresh headroom are distinct. A planned
generation-bound safe-point fixture (including uncheckpointed page-touch
negative case) remains peer-specific and does not prove real solver coverage.
This App has no corresponding worker/headroom admission contract to replace.
Job memory limits or cooperative events are therefore not an App/SWB shared
solution. Agent 0 carries consequential alignment; no peer source is changed.

After owner-authorized acquisition/tooling and a policy decision, the next
buildable work is **isolated P-01/P-02/P-03 and S-01/F-01 probes**, with original
HANDLE custody and invented SQLite DB. They can fail/refuse usefully without
whole-App compilation or supplier execution. Then resolve P1/F1/S1 using actual
evidence; implement one platform service at a time behind the unchanged semantic
boundary, port the named regressions, independently scrutinize persistence and
process effects, and only then attempt N-01. The producer/consumer gaps for a
later App↔SWB journey are traced separately in
[`WINDOWS_APP_SWB_TRACE.md`](../../../PKG-03/DEL-03-03/Design/WINDOWS_APP_SWB_TRACE.md).

## Official API basis and evidence limits

Checked official Microsoft API documentation includes [Job Objects](https://learn.microsoft.com/en-us/windows/win32/procthread/job-objects),
[CreateProcessW](https://learn.microsoft.com/en-us/windows/win32/api/processthreadsapi/nf-processthreadsapi-createprocessw),
[UpdateProcThreadAttribute / Job list](https://learn.microsoft.com/en-us/windows/win32/api/processthreadsapi/nf-processthreadsapi-updateprocthreadattribute),
[AssignProcessToJobObject](https://learn.microsoft.com/en-us/windows/win32/api/jobapi2/nf-jobapi2-assignprocesstojobobject),
[QueryInformationJobObject](https://learn.microsoft.com/en-us/windows/win32/api/jobapi2/nf-jobapi2-queryinformationjobobject),
[CreateFileW](https://learn.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-createfilew),
[GetFileInformationByHandleEx](https://learn.microsoft.com/en-us/windows/win32/api/winbase/nf-winbase-getfileinformationbyhandleex),
[LockFileEx](https://learn.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-lockfileex),
[FlushFileBuffers](https://learn.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-flushfilebuffers),
[MoveFileExW](https://learn.microsoft.com/en-us/windows/win32/api/winbase/nf-winbase-movefileexw)
and [ReplaceFileW](https://learn.microsoft.com/en-us/windows/win32/api/winbase/nf-winbase-replacefilew).
SQLite API authority for this pin is its bundled public header and implementation
cited above; the current [file-control documentation](https://sqlite.org/c3ref/c_fcntl_begin_atomic_write.html)
is supplementary, not a replacement pin. Additional APIs named as probe
candidates must be checked against the installed SDK/runtime during the probe.

Only source investigation, official API-document reads, path census and local
graph/representation checks are evidence from this tranche. No Windows code,
supplier, model, native control, crash test, payload or signature verification
ran. Prior Mac/build/34-fixture checks remain attributed to first feasibility;
they are not repeated or upgraded here. VS acquisition integrity remains held;
Agent 0's independent metadata follow-up does not resolve it. No new downloads,
guest mutations, publishing or owner acceptance follow from this proposal.

Local validation before independent review: `tools.deliverables check` reports
41 deliverables, no errors and the same six declared cycle groups;
`neighborhood DEL-01-02`, `neighborhood DEL-03-03` and `impact DEL-01-02`
report no errors. New-document relative Markdown links resolve, evidence JSON
parses, and `git diff --check` passes. The three inspected SQLite files were
compared byte-for-byte with the cached `.crate` archive whose SHA-256 matches
the App Cargo lock. ScopeOfWork/dependency reconciliation: hosting, recovery,
adapter and their consumers keep existing requirements and conditions; these
proposals supply no completion or qualification witness. No production tests
were added or rerun for this documentation-only tranche.

Independent scrutiny reviewed saved revision
`13c1206311aa8d527ec57e96e53858b79b251b9c` with
`codex-hub/gpt-6.1-terra`, `reasoningEffort=xhigh`, `serviceTier=priority`.
It found no critical/high issue and one medium: the former P-01 final-marker
condition could miss a child created before assignment but reported afterward.
The WORKING_ITEMS owner repaired that specification with ordered pre-creation
instrumentation, actual descendant HANDLE/Job membership and the deliberately
broken negative control above. This narrow repair was locally inspected and
representation-checked, not independently re-reviewed or executed on Windows.
The reviewer independently traced process/SQLite/App-peer claims and reproduced
the path census; no build, Windows, supplier or live probe was run. Review and
repair establish no owner acceptance or production adoption.
