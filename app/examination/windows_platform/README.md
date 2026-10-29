# Package-free Windows process fixtures

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

`run_fixture.py --inspect --source-commit <saved-revision>` only reads installed guest metadata via Windows
PowerShell `-NoProfile -NonInteractive -EncodedCommand`. It writes a bounded
raw response, source hashes, blockers and a fresh scratch CODEX_HOME on the host.
All four fixture files must match that saved revision before guest contact.
Both response channels together are capped at 32 KiB with a 25-second original
monotonic deadline. No guest TEMP/user-profile path is captured.
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
