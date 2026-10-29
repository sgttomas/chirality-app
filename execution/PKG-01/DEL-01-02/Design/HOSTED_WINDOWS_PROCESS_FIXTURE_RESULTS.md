# Supplemental hosted Windows process fixture lane

Status: **CONTROLLED STDOUT PROFILE PASSED ALL FIVE CASES ON HOSTED NATIVE-X64
WINDOWS**, run `40845322580` at exact source `d26ecdae630b07b94b4331e4041fdce18861edcb`.
The final section records the inspected native evidence. The three earlier
attempts remain FAILED at P02-A, and all earlier preparation/checks retain
their original scope. This is separately attributed disposable GitHub-hosted
P01/P02 fixture evidence, not Windows App or shared-guest qualification.

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

## Direct-read native result

[Actions run 40841278555](https://github.com/sgttomas/chirality-app/actions/runs/40841278555)
executed exact source `91b80351c30beb2c502fc4c77125f0b74bf097aa`.
The [result](hosted-windows-process-fixture-evidence/91b80351/result.json) and
[raw trace](hosted-windows-process-fixture-evidence/91b80351/native.stdout)
are exact source/channel-verified artifact bytes. Compilation and both P01
controls completed again; the overall native suite remains FAILED.

A confirmed successful output close, then its actual synchronous read stayed
pending through the original deadline while the original leader remained live.
After safety termination began, the read completed FALSE/109, and bounded
worker join plus process-HANDLE/Job-empty cleanup were observed. Read completion
was after termination request but before the later all-exited proof: the raw
`eofAfterDeathProof=False` is not evidence of live EOF. Original acceptance
deadlines were already exceeded. B/C were not reached.

This run rejects a missed-peek-only explanation for its observation and supports
process-lifetime-associated retention, without identifying any module, duplicate
handle or universal CLR/kernel defect. Existing failed records remain intact.
A next controlled fixture may create its test pipe inside the helper after
managed startup, transfer the read HANDLE through its original owned process,
and explicitly bind/verify the write end as actual STD_OUTPUT_HANDLE. That must
be source-reviewed and prove parent/child pipe correspondence, real current
stdout binding, live original leader, FALSE/109 within eight seconds, and cleanup.
An unrelated private pipe or an EOF after death cannot satisfy A. This is a
controlled-stimulus refinement, not a production fix or guarantee.


## Controlled current-stdout candidate: native NOT RUN

The next A-only implementation uses setup identity
`post-managed-start-stdout/v1`. This is an explicit controlled-stimulus change,
not evidence that the startup stdout pipe has been fixed. The three historical
native failures and their exact source/artifact bytes remain unchanged.
The required P-02 A observation remains actual intended stdout FALSE/109 while
the same retained original leader PROCESS HANDLE is nonsignaled with query259,
within the original eight seconds starting before leader creation. Neither
absence of data nor EOF after process death qualifies.

After managed startup and existing root/nonce/environment validation, the A
helper creates a fresh anonymous pipe with noninheritable ends, checks both
PIPE types and rejects equality with any startup standard handle. It sends a
strict bounded generation/case control frame over startup stdout naming the
pair and startup handles. The parent duplicates only the read end from the
actual retained original leader PROCESS HANDLE, with SAME_ACCESS and
noninheritance; it owns and type-checks the copy before private acknowledgment.
No PID lookup, writer duplication, A descendant or new inheritance is added.
The helper closes its source read end only after that acknowledgment, calls
supported `SetStdHandle(-11, freshWriter)`, checks `GetStdHandle(-11)` equals
that writer and is PIPE, then raw-writes ENTRY through a newly queried actual
stdout. Only ENTRY received on the transferred corresponding reader can bind
the test stream. Source/observer QPC order covers control, transfer, ack,
source-reader close, stdout bind, ENTRY, close attempt/return and direct read.

The startup reader remains in owned IO with no further/concurrent reads, and
startup stdout/stderr remain control references until helper death. The new
writer closes exactly once. No claim is made about old-pipe EOF, all runtime
copies, .NET `Console.Out` caches or startup-stdio root cause. The bounded
exclusive metadata file now carries the setup identity, generation, source
pair, bind/ENTRY/close timestamps and close result; it never supplies EOF.
The verifier refuses missing/duplicate/mismatched binding and reader evidence,
failed/missing close proof, zero-byte success, other read errors, unknown or
late worker completion and dead original leaders. Read completion can race
with CloseHandle return timestamping: close-attempt QPC must precede the read
completion, while post-close QPC is separately bounded and ordered.

The existing one-read background worker, original deadline, original leader
HANDLE authority, helper sleep11s/watchdog12s, joined-reader cleanup,
creation-time safety Job/HANDLE_LIST/four arguments, no-breakaway and all
retained-HANDLE/Job-zero invariants remain. P01/B/C launch/observation behavior
is unchanged. No read HANDLE is manually closed while its ReadFile is pending;
unknown teardown still fails and exits only the fixture controller/owned Job.

Reconciliation: this refines only the existing hosted P-02 A stimulus and its
source-bound verification. WINDOWS_PLATFORM_SERVICES P-02 expected observation,
DEL-01-02 ScopeOfWork and deliverable.yaml dependency conditions remain
unchanged. The trusted disposable hosted namespace/profile remains the limit;
no hostile namespace, durability, SQLite, shared/protected guest, supplier,
App, production policy, commitment, acceptance or release result follows.
Native compilation/CI/execution for this setup is NOT RUN until parent
integration/publication. Historical B/C observations remain NOT REACHED.

Host-only verification on this candidate: 18 hosted test methods and eight
retained guest-driver refusal tests pass using a fresh scratch CODEX_HOME.
Mutation units explicitly labelled invented cover missing/duplicate setup,
wrong source leader/read/write/observer HANDLE, inherited endpoints, absent or
failed SetStdHandle/GetStdHandle proof, unknown setup/type, impossible source
ordering, stale/mismatched metadata, nonproof/late/unjoined reads, dead leader
and rewritten/unknown cleanup. They do not generate a native success trace.
The deliverables check reports 41 deliverables, no errors and the same six
cycle groups; `git diff --check` passes. Independent source review and final placement checks are recorded below.


### Independent controlled-stdout source review

[Independent Type2 source review](t3-thread://v1/thread:delegated-task:command%3Amcp%3A7fdf66b7-ae31-457d-bed4-1dafe1c8294f%3Adelegate-task%3Aef2a79dc-893e-445d-b194-c4ec0acbe7f0)
examined exact saved commit `44f209a34ca42f00401597496483090acc9b596e`
with required ancestor `59a33c990f28d3a1847446574cff8353b4e56ea5`, using
`codex-hub/gpt-6.1-sol`, `reasoningEffort=medium`, `serviceTier=default`.
One Type2 ran and did not delegate. The implementation owner inspected its
actual completed return through the host completion mechanism.

The reviewer identified no blocking findings or ordinary repairs. It judged
that the actual source ties the transferred reader to current Win32 stdout,
retains the original live-EOF counterexample and expressly changes the stimulus
rather than weakening the outcome. It found no new ownership/cleanup or
Framework 4.8 source/ABI compatibility defect by inspection. Native compilation
remains unverified. The reviewer independently ran the 18 hosted tests, eight
held-driver refusal tests, deliverables check (41/no errors/six cycle groups)
and whitespace check, with fresh scratch CODEX_HOME and no repository edits.

The final review-record commit changes only this owning result document;
the four reviewed implementation/test/README files are byte-identical to the
reviewed candidate. Current C# is 36,844 bytes, SHA-256
`161b054e890e7f233fbf5194a826ba1d42538f344baec478bf2e446b9f27d43c`;
verifier is 12,057 bytes, SHA-256
`808e99df691a286c1f662d0d726330e43e2b6fb2739936ff37325befd983ca56`.
These are new candidate identities, not edits to historical expected hashes.
All three retained native channel pairs still match their result.json hashes,
all three old failed traces remain refused by the new verifier, and their
artifact directory has zero diff from the required ancestor. No fake native
success trace was generated. Native compile/CI/execution remain NOT RUN;
parent Agent 0 owns integration/publication and actual outcome recording.

### Agent 0 integration correction: Win32 pipe type

Before publication, Agent 0 found that the reviewed candidate used file type
`2` for pipes. Win32 defines `FILE_TYPE_CHAR=2` and `FILE_TYPE_PIPE=3`, also
confirmed in the cached Microsoft `windows-sys 0.61.2` FileSystem bindings.
The source review above retains its actual no-findings outcome; this defect
was caught during integration and does not change any historical run record.

The integrated C# now uses named `FILE_TYPE_PIPE=3`, checks the observed types
of both fresh endpoints, the duplicated reader and current stdout, and logs
the actual API values. The verifier requires type 3 in each correspondence
record. Invented parser units use type 3 and reject both character type 2 and
disk type 1 at every such record. This is a focused API-constant/logging
repair, locally checked by Agent 0 without another independent review.

All 18 hosted methods and eight retained held-driver methods pass. The graph
still has 41 deliverables, zero errors and six declared cycle groups. The
three retained native channel pairs match their saved hashes, their failed
traces remain refused, and their artifact directory is unchanged from
`59a33c990f28d3a1847446574cff8353b4e56ea5`. Whitespace checks pass.

Corrected C# is 37,157 bytes, SHA-256
`e605e4a2c454655cadc176d3693547ddf5b3beeed1e62d305ace20faac4084ff`;
verifier is 12,093 bytes, SHA-256
`5048582b2be3e27ae690affaa2a97a66feebb056bc48816f3aaae7b52b8f1162`.
These identities supersede only the unrun candidate above. Native compilation
and execution of this corrected setup remain NOT RUN pending publication.
P01/B/C, live-leader/deadline/cleanup requirements and the existing scope and
dependency conditions are unchanged. No VM was accessed.

## Controlled-stdout native result

[Actions run 40845322580](https://github.com/sgttomas/chirality-app/actions/runs/40845322580)
compiled and executed exact source
`d26ecdae630b07b94b4331e4041fdce18861edcb` successfully. Agent 0 inspected
the actual [result.json](hosted-windows-process-fixture-evidence/d26ecdae/result.json)
and [raw trace](hosted-windows-process-fixture-evidence/d26ecdae/native.stdout),
verified all five source identities against committed Git blobs, checked every
compiler/native channel length and SHA-256, and independently reapplied the
bound verifier to the saved raw bytes. All seven downloaded artifact files are
preserved byte-for-byte. No success trace was synthesized.

This was disposable GitHub `windows-2022`, image `20261026.347.1`, host build
20348, native AMD64 (`processMachine=0`, `nativeMachine=0x8664`), with 8-byte
pointers. The preinstalled C# compiler reported `4.8.9363.0` and the native
fixture reported CLR `4.0.30319.42000`. The CLR's compatibility OS string is
preserved in the raw identity; it does not change the separately observed host
build. This is not Windows 11 or Parallels execution.

- P01-positive observed the descendant inside the original inner and safety
  Jobs after safety assignment at creation and inner assignment before resume,
  then observed cleanup.
- P01-negative observed the deliberately escaped descendant outside the late
  inner Job but inside safety containment, rejected the broken launch and
  observed its termination through the retained descendant HANDLE.
- P02-A verified fresh type-3 pipe/reader correspondence and current Win32
  stdout binding. The joined one-byte read returned FALSE/109 while the same
  original leader HANDLE remained nonsignaled with exit query 259, inside the
  original eight-second deadline and before any termination request. Successful
  writer close metadata matched that binding; EOF was not inferred from it.
- P02-B observed leader exit 0 while the retained descendant remained live and
  the inherited stdout pipe had no EOF.
- P02-C observed a signaled original process HANDLE and actual exit code 259.

Every case recorded its required retained-process/inner-Job cleanup. Final
safety cleanup observed all retained process HANDLEs signaled and active Job
count zero; the A reader was joined and its earlier result remained unchanged.
Compiler/native commands exited 0 without response-limit, deadline or teardown
uncertainty. The bound verifier and adapter both returned PASS.

This establishes those fixture observations under the declared trusted hosted
profile. The controlled fresh-stdout stimulus does not repair or explain the
three failed startup-stdout attempts. Production Rust/App process policy,
supplier behavior, full-generation Stop, crash/hostile-namespace bootstrap,
SQLite and durability remain outside this evidence. The protected CAEPIPE VM
was not accessed; the separate build VM remains stopped without Windows media.
DEL-01-02 commitments and dependency conditions remain unchanged; no owner
acceptance or release qualification is implied.
