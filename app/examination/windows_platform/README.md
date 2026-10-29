# Package-free Windows process fixtures

## Supplemental hosted profile

`run_hosted_fixture.py` is a separate, additive process-only adapter for
disposable GitHub-hosted native-x64 Windows, with trusted checkout/namespace and
preinstalled Python/Framework compiler. It refuses other contexts before source
reads, subprocesses or scratch. The independent workflow
`.github/workflows/windows-process-fixtures.yml` binds actual PR-head Git blobs,
preserves raw bytes and retains bounded compiler/native traces. It does not
enable the guest route or claim hostile-namespace/compiler parent-death safety.
Native execution is pending parent publication; see
`execution/PKG-01/DEL-01-02/Design/HOSTED_WINDOWS_PROCESS_FIXTURE_RESULTS.md`
for prerequisites, boundaries and artifact schema. Host-only checks:
`python3 -B app/examination/windows_platform/test_hosted_fixture.py`.

## Held guest profile

**Guest access is held.** The former target is the owner's CAEPIPE VM and is
permanently off-limits. All guest modes refuse before binding, contact or scratch.
A separate owner-authorized build guest (at most 16 GiB RAM) must first be
created and privately bound, with exclusive-window scheduling respected. No VM
identifier is committed. A ready/unlocked legacy guest is not execution authority.
The older observations below describe historical preparation, not a current route.

This examination harness exercises invented P01/P02 process semantics only.
It neither runs App/suppliers/models nor selects production Job/crash policy.
The owning design and results are in
`execution/PKG-01/DEL-01-02/Design/WINDOWS_PROCESS_FIXTURE_RESULTS.md`.

**Native execution is withheld.** Independent scrutiny of `0e3db4a5`
found two blocking driver safety gaps: no continuously retained namespace guards
through scratch use/compilation, and no compiler lifetime guard surviving loss
of the host command. The original executable driver is preserved in Git history
for review evidence. Its write/compile/run route has been removed from the current
source rather than left available behind a warning. `--run` hard-refuses before
any guest operation. The source harness has not been compiled or executed.

The guarded-bootstrap follow-up adds `Controller.ps1` as an exact-byte **inline
source asset**, never a script loaded from disk. It emits PInvoke definitions,
validates 64-bit sequential structure sizes/offsets, and prepares a dedicated
managed watchdog thread without PowerShell callbacks. The controller's source
uses a creation-time Job list, retained original process/Job handles and one
original guest deadline. Deadline expiry terminates its own controller root;
closing the last non-inherited Job handle then requests descendant cleanup.
That timeout path provides no observed-cleanup result. Ordinary cleanup requires
original process signaling and Job active zero before stopping/joining the
watchdog and closing handles. After a stop wake the watchdog checks the original
deadline before accepting cancellation. The controller lifecycle has not been invoked.
Its future fixture integration still needs bounded stdout capture.

The proposed sharing-only namespace guard has a specific documented conflict:
CreateFile share modes do not restrict attribute/EA access, while MS-FSA
2.1.5.10.37 permits setting reparse data with FILE_WRITE_ATTRIBUTES. Denying
write sharing therefore does not itself prevent reparse mutation; permitting
write sharing for pathname-based compiler output does not repair that gap.
This rejects that guard, not every possible package-free implementation.
See the owning results for exact citations, qualifications and remaining work.

`run_fixture.py --bootstrap-check --source-commit <full-40-digit-commit>` makes
one bounded in-memory attempt: it checks the exact transported source hash,
emits/validates the API types and queries its own machine types through
IsWow64Process2. It checks just the two known Roslyn stream-emitter assembly
names beside the installed framework compiler; absence there is not a global
inventory or proof of absence elsewhere. It invokes no compiler or controller
lifecycle, creates no guest file, Job or fixture process, and leaves execution
policy unchanged. The driver still refuses `--run` before guest contact.
Gzip/base64 transport checks a 16 KiB compressed bound, exact decompressed
length (at most 96 KiB), SHA-256 and strict UTF-8 before ScriptBlock creation.
The encoded command stays below the Windows command-line bound.
Command construction uses the verified Git-blob bytes without reopening the
controller pathname. Keep the invocation unchanged; recorded execution uses a
Python loader that executes the driver bytes from the exact saved Git revision.

`run_fixture.py --inspect --source-commit <saved-revision>` only reads installed guest metadata via Windows
PowerShell `-NoProfile -NonInteractive -EncodedCommand`. It writes a bounded
raw response, source hashes, blockers and a fresh scratch CODEX_HOME on the host.
All six source files (C# harness, Python driver/verifier/regressions, this README
and Controller.ps1) must match that saved full commit before guest contact, and
the required input ebf71ce7 must be its ancestor.
Both response channels together are capped at 32 KiB with a 25-second original
host response deadline, followed by an attempted local-client kill and five-second
exit wait. Exceptional teardown remains reported as unknown, with no implicit
unbounded Popen-context wait.
Process creation itself is not interrupted by that deadline. A host timeout
leaves guest PowerShell completion UNKNOWN; it proves no guest termination.
No guest TEMP/user-profile path is captured.
The existing Restricted policy stays unchanged; individual inline metadata
commands load no `.ps1` file and invoke no compiler. No guest fixture scratch,
source, compiler temporary files, binaries or logs are created by this route.
Normal builds/tests do not invoke it. No binary is committed.

The following describes the saved **unrun** C# fixture design. Before any future
native attempt, independently review the repaired bootstrap/driver and bind all
source/driver/verifier identities to that exact revision. Establish continuously
held, no-follow namespace guards from exclusive guest-local NTFS scratch
creation through all source/output/temp operations. Establish a supported
compiler/launch lifetime guard independent of host callback survival. Do not
weaken policy, use breakaway, install prerequisites, or treat command timeout as
cleanup. If either guard cannot be established, stop with a precise refusal.

Every leader is born suspended into a distinct unnamed safety Job through
`PROC_THREAD_ATTRIBUTE_JOB_LIST`. Its last handle is non-inheritable and held
only by the supervisor, with `JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE`. Descendants
inherit Job membership at creation; no breakaway flags are used. A separate
inner Job is the P01 subject. The deliberately broken negative leader runs and
creates its descendant before assignment to that inner Job. That descendant
stays in the safety Job. Explicit standard input/output handle lists confer no
Job authority. The supervisor duplicates the actual child HANDLE from its
original leader HANDLE, using a private source-bound handle value, never a PID.

Intended helper entry, pre-creation private acknowledgment, actual returned creation
HANDLE, first nonce effect, inner/safety membership and delayed final marker
are separate observations. `verify_results.py` refuses missing/unknown evidence
and requires rejection of the broken launch. P02 covers stdout closure with
leader live, leader exit with descendant stdout live, and real exit code 259.
Process HANDLE signaling is observed independently of EOF and exit-code query.

Helpers self-expire at 12 seconds. Each operation retains an original monotonic
deadline. The supervisor has an 80-second independent timer which terminates
only its original safety Job then exits; host callback failure cannot disable
that timer, and supervisor death closes the last safety handle. Timer expiration
is cleanup **unobserved**, never success. Ordinary cleanup observes all retained
process HANDLEs signaled and authoritative Job active zero before reporting it.
An invocation timeout or absent cleanup output requires stopping and reporting
unknown; no PID/name cleanup is permitted. At most one leader and one descendant
run concurrently. No crash/last-close experiment is included in this tranche.

P01 setup/assignment/resume failure injection, incompatible outer Job testing,
P03 full-generation Stop, and P04/P05 remain unrun. The invented generation is
an ordered fixture binding record, not the production Rust custody capability.
S01/sidecars/durability, App native controls and supplier evidence remain deferred.
The installed managed runtime's actual machine/native machine and pointer width
are logged; ARM64/AnyCPU evidence does not establish Windows-x64 App execution.
