# Package-free Windows process fixtures

This examination harness exercises invented P01/P02 process semantics only.
It neither runs App/suppliers/models nor selects production Job/crash policy.
The owning design and results are in
`execution/PKG-01/DEL-01-02/Design/WINDOWS_PROCESS_FIXTURE_RESULTS.md`.

`run_fixture.py --run` is an explicit, offline, single-run driver for the
already selected running guest. It uses Python on the host, Windows PowerShell
`-NoProfile -NonInteractive -EncodedCommand` for individual commands, and the
existing ARM64 .NET Framework C# compiler. It does not load `.ps1` files,
override execution policy, use profiles, provision packages or contact a model.
Restricted policy permits individual commands and native executable invocation;
if existing language/application controls refuse commands/compiler/fixture,
stop rather than weaken them. This driver is not a portable guest selector.

Do not run before independent scrutiny of the actual saved revision. No run is
implicit in normal builds/tests. The source and all compiler/output/temp files
are copied into fresh `C:\Windows\TEMP\chirality-app-process-fixture-<nonce>`
on fixed local NTFS. An ownership sentinel precedes artifacts. No guest directory
is enumerated. Host command responses and hashes are saved in a fresh host
scratch directory, printed before execution. A failed/timed-out invocation stops
further commands; its raw response is retained. No compiled binary is committed.

Every leader is born suspended into a distinct unnamed safety Job through
`PROC_THREAD_ATTRIBUTE_JOB_LIST`. Its last handle is non-inheritable and held
only by the supervisor, with `JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE`. Descendants
inherit Job membership at creation; no breakaway flags are used. A separate
inner Job is the P01 subject. The deliberately broken negative leader runs and
creates its descendant before assignment to that inner Job. That descendant
stays in the safety Job. Explicit standard input/output handle lists confer no
Job authority. The supervisor duplicates the actual child HANDLE from its
original leader HANDLE, using a private source-bound handle value, never a PID.

Helper entry, pre-creation private acknowledgment, actual returned creation
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
