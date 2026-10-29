# Supplemental hosted Windows process fixture lane

Status: **TWO NATIVE ATTEMPTS FAILED AT P02-A; OWNERSHIP DIAGNOSIS PENDING**. The
source-bound first attempt and partial observations are appended below; the
earlier preparation/checks retain their original scope. This is a separately
attributed disposable GitHub-hosted native-x64 P01/P02 lane. Parent
Agent 0 owns source integration/publication and later appending actual run
identity/results. No push, PR or remote execution is part of this local return.

## Profile and source basis

The source-only starting point is `de122cc4a768ea8ae5ebb9bbba11a169aad9d94e`.
At that initial source-only point, `ProcessFixture.cs` was unchanged (344 lines, SHA-256
`a587f4b5424b93b407bbbae671a4c1a1904bc005ed98115fbc31d0c1e096c646`),
as is `verify_results.py`. Prior harness scrutiny at `0e3db4a5` and the
unrun/held guest route remain documented in
[WINDOWS_PROCESS_FIXTURE_RESULTS.md](WINDOWS_PROCESS_FIXTURE_RESULTS.md).
The hosted adapter does not import or enable `run_fixture.py`/`Controller.ps1`.

The new profile is
`github-hosted-native-x64-trusted-checkout-process-only/v1`. It assumes trusted
checked-out sources and the provider-owned disposable runner namespace. It is
not a hostile-namespace guard, persistent/shared guest profile, compiler
bootstrap solution or arbitrary runner-death cleanup proof. Source-byte checks
are not continuous namespace retention. Provider provisioning/disposal is
provider-managed; compiler lifetime across arbitrary runner loss is unproven.
The two original guest-route blockers remain unresolved and unwaived.

The source entry points are
`.github/workflows/windows-process-fixtures.yml` and
`app/examination/windows_platform/run_hosted_fixture.py`. The workflow checks
out the actual PR head (or dispatch SHA), with read-only contents permission
and no persisted checkout credential. Checkout alone receives a command-scoped
`core.autocrlf=false` Git override so the workflow and `.gitattributes` also
retain their committed bytes; no repository/global settings or attributes are
changed. It runs independently of existing App
and governance workflows and adds no macOS gate or production policy.

## Preconditions and execution

Only `GITHUB_ACTIONS=true`, `RUNNER_ENVIRONMENT=github-hosted`, Windows/X64
runner metadata and 64-bit Windows Python are admitted. Before any subprocess
or scratch creation, `IsWow64Process2` must observe native AMD64 Python
(`processMachine=0`, `nativeMachine=0x8664`). Environment labels alone are
insufficient. The C# trace must independently report those machine values,
native system architecture 9 and pointer width 8 through its supported APIs.

Use the preinstalled Python >=3.9 (tested version/stdlib capability) and
`%SystemRoot%\Microsoft.NET\Framework64\v4.0.30319\csc.exe` plus the adjacent
`mscorlib.dll`, `System.dll`, `System.Core.dll`. Missing prerequisites fail;
there is no setup action, package/toolchain acquisition, installer or fallback.
Only the provider checkout/artifact actions acquire their own infrastructure.
No supplier/model, credentials, App, VM or private binding is accessed.

The adapter requires a full source SHA matching checkout HEAD. Before scratch,
all five inputs (workflow, adapter, C#, verifier, `.gitattributes`) must equal
their exact checked-out Git blobs. It records Git blob IDs, raw SHA-256 and
lengths, preserves LF/CRLF, copies the verified C# bytes and checks the copy.
It repeats checkout binding before launch and executes the verifier from bound
blob bytes. No expected-result/source-hash rewrite hides checkout conversion.

Fresh exclusive `RUNNER_TEMP` leaves hold source, output, TEMP, TMP and
CODEX_HOME. Compilation uses `/noconfig /nostdlib+ /platform:x64`, explicit
framework references and explicit output. The legacy compiler's supported
`/noconfig /help` probe retains the version banner and bounded raw help output;
compiler/reference hashes are retained. A successful original compiler exit is mandatory before
launch. Version/Git commands have 15-second response bounds; compilation 60
seconds; native supervisor 90 seconds; ordinary original-process teardown five
seconds. Combined stdout/stderr per command is capped at 128 KiB. Process
creation itself is not interruptible by the adapter deadline; the eight-minute
provider job timeout is the outer execution bound. No wait/context-manager
exit adds an unbounded process-exit wait. Timeout/output/teardown uncertainty
always fails, even if a later original process exit is observed.

`Popen.kill()` on Windows addresses its original process HANDLE, never a PID
lookup or process-name scan. Killing the supervisor is not recorded as observed
descendant cleanup. The retained native supervisor owns its creation-time safety
Job, non-inheritable last Job handle, original child handles, independent
80-second timer and ordinary cleanup observations. No breakaway/global kill or
Taskkill is used. Provider disposal is separate from harness evidence.

## Intended native evidence and artifact schema

The native suite must demonstrate P01 positive containment and deliberate
negative rejection using the retained actual descendant HANDLE, original-inner
exclusion and outer-safety inclusion. A delayed marker is insufficient. P02 A
separates EOF from leader exit, B separates leader exit from inherited pipe EOF,
and C observes signaled process HANDLE plus actual exit 259. Each case requires
retained-handle cleanup and the suite requires safety Job active zero. Refusal,
empty trace, unknown cleanup, wrong architecture, missing generation/suite,
nonzero exit, output overflow or timeout cannot produce a hosted pass.

The artifact `windows-process-fixture-<source SHA>` (14-day retention) contains:

- `result.json`: schema `chirality-hosted-process-fixture/v1`, profile, overall
  status, native execution state, source SHA/blob/hash/size map, Python/OS and
  observed architecture, compiler/reference hashes, compiler version, nonce,
  executable hash, command return/failure/teardown/elapsed metadata, raw-channel
  sizes/hashes, verified cases/native identity or explicit error.
- `compiler-version.stdout/.stderr`, `compile.stdout/.stderr`,
  `native.stdout/.stderr`: bounded raw bytes, including original line endings;
  files exist only for commands actually attempted.

A pre-admission/source/prerequisite failure may precede artifact creation and
must remain a failed job with its explicit console error. Artifact upload runs
on failure but missing evidence does not turn execution green. No raw executable,
owner home, private VM identity or complete environment dump is uploaded.

Actual run fields to append after parent publication: Git SHA, Actions run URL
and attempt, image version, artifact digest/identity, observed native identities,
compiler/runtime versions, five case results, cleanup evidence, and any error.
Those fields were initially NOT RUN. The actual first-attempt observations are
recorded in the follow-up below; they do not establish a passing full suite.

## Reconciliation and limits

This additive process-only examination supports the candidate P-01/P-02 probes
in [WINDOWS_PLATFORM_SERVICES.md](WINDOWS_PLATFORM_SERVICES.md). It does not
complete the broader P-01 failure injection/incompatible outer-Job suite or
P03/P04/P05. It supplies no Rust/App parity, production crash policy, supplier,
native-control, hostile-namespace, durable-file, SQLite, shared-guest or
compiler-bootstrap guarantee. DEL-01-02 ScopeOfWork and dependency conditions
remain unchanged; no commitment, acceptance, hold lifting or release is implied.

Focused host checks before source review: ten hosted regression methods pass
(including per-input newline conversion and compile-failure/timeout/overflow
preventing native launch); eight retained guest-driver regressions pass. The
actual Git/autocrlf regression passes: ten selected committed inputs convert
without attributes, zero with attributes, all eleven protected samples match
including intentional CRLF, and an unprotected control still converts. Python
AST parsing, workflow YAML parsing/read-only/native-image assertions,
`git diff --check` and the deliverables check pass (41 deliverables, no errors).
C# and verifier bytes match the starting commit and their recorded hashes.
Host-only results never replace native proof.

## Independent scrutiny and local repairs

[Independent review](t3-thread://v1/thread:delegated-task:command%3Amcp%3A2c97a15a-18fc-4e5c-899d-c6d1e85ed0e0%3Adelegate-task%3Ad99e6925-01c3-4385-93d9-4d0182857831)
examined exact commit `02a329835183a44288edb57c929e5b823678cc31`, all six changed
files and retained harness/contracts, using `codex-hub/gpt-6.1-sol`,
`reasoningEffort=medium`, `serviceTier=default` under the owner's updated
steering. Only one Type2 was active; no previous-setting reviewer was started.
The Type1 manager inspected the actual completed return.

The reviewer reproduced two unprotected bound inputs converting under
`core.autocrlf=true` (`.gitattributes` 393 to 404 bytes, original workflow
1,902 to 1,945 bytes). Strict source binding correctly refused them. The local
repair scopes `core.autocrlf=false` to the checkout action's Git processes;
it changes no existing shared file or expected source bytes. A new real Git
checkout-index regression now covers every bound input: the negative checkout
changes exactly those two inputs; the scoped override preserves all five.
Existing attributes and the original byte-conversion regression remain intact.

The reviewer also identified `/version` as incompatible with the legacy
Framework compiler (source compatibility finding, not a native reproduction).
The local repair uses `/noconfig /help`, requires a version banner and retains
the bounded raw response. The compiler-failure regression checks that exact
probe and still rejects nonzero, timeout or overflow before native launch.

The reviewer found the profile, architecture checks, original-HANDLE/Job
invariants, real descendant-membership requirement and false-pass protections
intact. Review initially required these repairs before publication. These are
small compatibility repairs inspected and checked by the Type1 owner; no
second independent review or observed Windows compiler success is implied.
Post-repair: eleven hosted regression methods pass, including actual Git
checkout coverage of all bound inputs; native execution remains NOT RUN.

## First native attempt and targeted fixture repair

[Actions run 40835385560](https://github.com/sgttomas/chirality-app/actions/runs/40835385560)
executed source `47edcee47eb04ec3d9b5a8445115e622e652fc16` on hosted
Windows Server 2022. The retained [result](hosted-windows-process-fixture-evidence/47edcee4/result.json)
and [raw native trace](hosted-windows-process-fixture-evidence/47edcee4/native.stdout)
are exact artifact bytes. Agent 0 compared all five recorded source SHA-256s
with that commit's blobs and both native-channel digests with the result.
Artifact ID was 12880158540; the upload reported ZIP digest
`d784d106dc6d93ec9f168d9401e2edfbacb469ea9d3386010039b3e76b9acf39`.
The digest is a provider report, not an independently hashed local ZIP.

Preinstalled Python 3.12.10 observed native AMD64 (processMachine 0,
nativeMachine 0x8664, pointer width 8); Framework C# compiler 4.8.9363.0
compiled successfully. The native trace independently reports the same ISA.
The managed Environment.OSVersion compatibility value is retained raw and
is not the OS-build authority. Actual observations:

- P01-positive emitted PASS with descendant inner/safety membership and
  observed case cleanup.
- P01-negative emitted REJECT with descendant outside the original inner Job
  but inside safety containment, followed by observed case cleanup.
- P02-A failed: leader still live, exit-code query 259 and pipe EOF false.
- P02-B and P02-C were not reached.
- The failure path observed every retained process HANDLE signaled and safety
  Job active zero. This is that attempt's cleanup, not runner-death proof.

The adapter correctly failed the suite on native exit 2; no partial trace is
accepted as a complete pass. The fixture assigns stdout and stderr to one
pipe, while A originally closed only stdout. The small root-owned repair
closes every distinct helper-side standard-output/error reference and logs
their identities before closure; the EOF/live-process assertion, original
deadline, membership verifier and cleanup requirements are unchanged. Its
C# SHA-256 is `77b7359bbc0f61c7a741d609a743028de2bfae929044248564808ea95276efaa`. This is a local
fixture repair, not a new independent review or a successful rerun.

Result-only documentation is removed from the supplemental workflow's path
triggers to avoid rerunning native cases solely to append their evidence.
Workflow/source/attribute changes still select the lane; required App/Mac
checks are unchanged. The exact repaired candidate must now run on Windows.

## Second native attempt: alias-close hypothesis not sufficient

[Actions run 40836454447](https://github.com/sgttomas/chirality-app/actions/runs/40836454447)
executed exact source `47953d358ce7448f10c12244fcb1402716bbe8b9`.
Agent 0 checked all five recorded source hashes against those Git blobs and
native-channel digests before preserving the [result](hosted-windows-process-fixture-evidence/47953d35/result.json)
and [trace](hosted-windows-process-fixture-evidence/47953d35/native.stdout).
Compilation succeeded. Both P01 controls and their cleanup were observed
again, but P02-A still refused with the leader live and EOF false. The new
diagnostic shows stdout and stderr had the same handle value, so closing a
distinct second output reference did not resolve this run. The remaining
writer ownership or EOF-observation cause is unestablished; the earlier alias
hypothesis must not be reported as a confirmed diagnosis or successful fix.
B/C were not reached. Safety cleanup again observed all retained handles
signaled and active zero; the overall suite remains FAILED. A focused
diagnosis must preserve the actual EOF/live-leader assertion and deadline.

## Bounded direct-read candidate: native NOT RUN

The next local candidate follows the independent source research on the two
exact failed traces. Neither an extra writer, a CLR duplicate nor a
`PeekNamedPipe` defect is established. The old Reader only reads when peek
reports available bytes. A now stops polling after validated ENTRY and an
empty pending buffer and starts exactly one background synchronous
`ReadFile` on `c.Output.Handle`, the existing leader stdout `CreatePipe`
read end, with one byte requested. P01/B/C retain their observation paths.

The helper attempts each distinct stdout/stderr close and captures its actual
Boolean and immediate Win32 error; successful calls' error values carry no
meaning. Equal stdout/stderr values designate a single close: stderr is
explicitly `attempted=False`, with no fabricated successful second close. QPC
is captured after these attempts. The helper exclusively creates
`P02-A-close.txt` under this profile's fresh validated Root using
`CreateNew`/`FileShare.None`, writes at most 512 ASCII bytes with a terminal
completion marker, flushes and closes. The supervisor requires an exclusive
completed-file read, exact size/field/generation/case/ENTRY-handle/alias/time
validation and successful distinct closes. Missing, malformed, stale or failed
confirmation cannot pass. No post-close exception is logged via closed stdout.
Validated metadata is included in native stdout; the raw metadata file is not
a separate uploaded artifact. This trusted-root diagnostic establishes no
hostile-namespace or durable-publication guarantee.

The worker captures return Boolean, byte count, immediate failure error,
completion QPC and elapsed milliseconds; successful `Thread.Join` supplies
completion evidence. A requires FALSE/109 with zero bytes before the existing
absolute eight-second deadline, valid post-close metadata, and the same original
leader HANDLE unsignaled with exit query259. A second QPC bound, also eight
seconds from before creation, only tightens the existing elapsed-time bound.
TRUE/positive output, TRUE/zero, other errors and pending/late completion refuse.
The exact required A observation remains
`leaderSignaled=False;exit=259;eof=True`. The verifier additionally requires
the close/read/deadline/original-HANDLE proof and joined-reader cleanup; no
historical source hash, trace or expectation is rewritten.

On refusal the failure precedes normal safety cleanup. The read HANDLE is kept
alive until the worker joins. Following all retained process HANDLE signaling
and safety Job active-zero proof, cleanup allows a join of at most two seconds
within its existing five-second absolute budget, records the result and whether
its QPC is at/after the recorded death proof. Completion earlier than that
proof does not establish its precise ordering against process death. EOF only
during cleanup cannot retroactively pass A or identify a retaining module.
Unjoined or otherwise unknown teardown records `CLEANUP_UNKNOWN` and terminates
only this fixture controller and its owned safety Job; it does not manually
close an outstanding synchronous-I/O HANDLE. The independent watchdog remains
armed on that path. No `CancelSynchronousIo`, cold thread lookup, global handle
enumeration, PID cleanup, replacement stdout or speculative native helper is
introduced. Helper sleep11s/timer12s and safety containment remain.

Falsifiable next native outcomes: live FALSE/109 with all other proof supports
this observer correction; pending at the original deadline followed by EOF
during writer termination rejects live EOF and supports further bounded
process-lifetime-associated retention investigation. Missing close metadata,
nonproof reads or unknown cleanup remain failures. No module or supplier cause
is inferred from any of those outcomes.

Host-only checks currently pass 17 hosted regression methods, including six new
parser-boundary methods for missing/duplicate proof, failed/stale/incomplete
close confirmation, zero-byte success, unexpected output, cancellation995,
other errors, late/unjoined completion, handle/deadline mismatch and unknown or
rewritten read cleanup. Invented parser units are not native traces. The
deliverables check reports 41 deliverables, no errors and the same six cycle
groups; `git diff --check` passes. No C# compiler/runtime or Windows execution
was used locally. Native CI for this candidate is NOT RUN and remains with
parent Agent 0 after independent source review and publication.

Reconciliation: this changes only the hosted diagnostic implementation and
its proof checks. DEL-01-02 ScopeOfWork/dependency conditions and the proposed
P-02 outcome in WINDOWS_PLATFORM_SERVICES remain unchanged. No production,
guest, compiler-safety, filesystem, policy, commitment, acceptance or release
claim follows; old evidence is preserved.

### Independent candidate review and local repair

[Independent Type2 review](t3-thread://v1/thread:delegated-task:command%3Amcp%3A68530ca1-6352-497f-b9d9-11162eb7140f%3Adelegate-task%3A024c7a6a-b065-4bcb-bd11-7ff99209dfdc)
examined saved candidate `63746e0d5dc88ec4d650caf015e361e889d89559`
using `codex-hub/gpt-6.1-sol`, `reasoningEffort=medium`,
`serviceTier=default`. One Type2 ran and did not delegate. The implementation
owner inspected the completed return and full saved report. The reviewer found
no P0/P1 or additional worker/handle/file/cleanup safety defect and identified
one P2 verifier gap: `removeprefix` permitted a suffix-only cleanup record
without the joined-worker result. The actual C# emitter included the result;
the missing-proof boundary still needed refusal.

The implementation owner reproduced that finding with a new suffix-only
negative subcase, then required the exact prior read-result prefix before
parsing cleanup metadata. All 17 hosted host-only methods pass after repair.
This small verifier repair was locally checked; it did not change the reviewed
C# worker, file or cleanup semantics and was not independently re-reviewed.
Both prior native channel hashes were rechecked against their result records;
the new verifier still refuses both failed traces. No native compilation or
execution was performed by either contributor.

Executable source identities for parent publication: `ProcessFixture.cs`
SHA-256 `0fe3a1d38c032655e9803c861eabf1bffb6ba11f0051c237f81889d1df4057b5`
(31,875 bytes); repaired `verify_results.py` SHA-256
`742241038b0f78871bc6fb308119356c857c7acba2d1da4b5f40cb899a6ef205`
(9,504 bytes). These are new candidate identities, not replacements for either
historical artifact's source hashes. Native CI remains NOT RUN.
