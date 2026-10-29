# Supplemental hosted Windows process fixture lane

Status: **PENDING NATIVE CI — NOT RUN**. This record prepares a separately
attributed disposable GitHub-hosted native-x64 P01/P02 lane. No native outcome,
compiler success, cleanup observation or App qualification is claimed. Parent
Agent 0 owns source integration/publication and later appending actual run
identity/results. No push, PR or remote execution is part of this local return.

## Profile and source basis

The source-only starting point is `de122cc4a768ea8ae5ebb9bbba11a169aad9d94e`.
The retained `ProcessFixture.cs` is unchanged (344 lines, SHA-256
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
and no persisted checkout credential. It runs independently of existing App
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
framework references and explicit output. Compiler version and compiler/reference
hashes are retained. A successful original compiler exit is mandatory before
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
Until then all five cases and compiler/native cleanup observations are NOT RUN.

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
Host-only results never replace native proof. Independent source review remains
pending at this preparation point; its actual result will be appended before
local return.
