# Bounded package-free Windows process fixture return

The historical return below remains intact. The later guarded-bootstrap attempt
and its actual guest-session obstacle are recorded in the appended follow-up.

2026-10-28 local undertaking (raw review timestamps are 2026-10-29 UTC).
**Source prepared and independently scrutinized; native execution withheld.**
No P01/P02 case, compiler, supplier, App or model was run. This return establishes
an exact bootstrap safety blocker, not an unavailable Windows API or compiler.
It does not change commitments, acceptance, shipping architecture or App crash
policy. Agent 0 retains integration and reserved choices.

## Source and instruction identity

Host-created worktree: `/Users/ryan/.t3/worktrees/chirality-app/t3-9009de90`.
Local branch: `t3/windows-fixture-process-probes`.
Required input/base: `ec66648b36023c27f2c0e3dc3c1f655a71ca076f`, an ancestor.
No additional checkout, push, PR, merge, release or permission change occurred.

- Harness/initial driver reviewed at `0e3db4a52474ee67259d57537b739af3370012aa`.
- Unsafe executable driver removed at `8ece3a63f166fe76944b8c8f2408199f92cff5c5`;
  independent recheck inspected that revision and unchanged C# source.
- Small metadata/refusal repairs and actual read-only capture source:
  `da0a2802a87ff3f4d71fbc816c93526801eefafd`.
- Source files: `app/examination/windows_platform/ProcessFixture.cs`,
  `run_fixture.py`, `verify_results.py`, `README.md`.
  Exact SHA-256 identities are in [readiness.json](windows_process_fixture_evidence/readiness.json).
  C# source remained byte-identical through both reviews and the return.

Selected shared instruction library: `/Users/ryan/dev/chirality` at
`1560bbf7f7add4637a20572a2b0d404ef121af63`; active `AGENT_WORKING_ITEMS.md`
and `workflows/coordinated-knowledge-work/WORKFLOW.md`. Reviewers read
`AGENT_TASK.md` from that same library. This consultation neither updates
packaged product instructions nor adds a build dependency. Both Type2 reviews
used `codex-hub/gpt-6.1-terra`, `reasoningEffort=xhigh`, `serviceTier=priority`,
with at most one active reviewer and no TASK delegation.

## Exact blocking safety prerequisites

1. The initial driver checked attributes and an ownership sentinel by pathname,
   but did not retain namespace guards from exclusive scratch creation through
   all source, compiler output and compiler temporary-file opens. A reparse or
   replacement race could redirect later access outside task scratch. The nonce
   and sentinel alone do not prove confinement.
2. The initial driver bounded only the host `prlctl` call. Its guest compiler
   had no independent lifetime guard covering loss/failure of that host call.
   The C# supervisor's 80-second timer starts after compilation, so cannot
   cover this gap. Host timeout cannot establish compiler cleanup.

These findings are unresolved, not waived. The current `--run` path hard-refuses
before guest contact or host scratch creation. The former guest write/compile/run
route is removed, preserved only in historical commit `0e3db4a5`. No unsafe
"try anyway" or weakening of execution policy was used. Windows support for a
suitable bootstrap has not been disproved; a reviewed implementation is missing.

The next minimal slice is a bounded bootstrap that continuously pins exclusive
NTFS scratch and all compiler source/output/temp paths, and establishes
compiler/launch lifetime containment independent of host callback survival.
It must preserve Restricted policy, existing launcher Job constraints, original
HANDLE authority and no-breakaway rules. Independently scrutinize that actual
saved revision before guest writes or compiler/fixture execution. Then attempt
the already saved P01/P02 suite once; do not expand to storage or provisioning.

## Actual environment and bounded observation

The selected running peer is Parallels VM
`2944eb77-696f-41ad-97e2-142ba0489535` (`Windows 11`), via installed
`/usr/local/bin/prlctl`; earlier authorized inventory identifies Parallels
27.0.2 and Windows 11 Pro ARM64, 32 GiB. This tranche read only VM list/status
and installed PowerShell/.NET metadata; it did not independently remeasure RAM,
Windows edition or Parallels version.

The saved [raw readiness response](windows_process_fixture_evidence/readiness.json)
records return code 0, empty stderr, exact command, source revision/hashes and:

| Observed metadata | Actual value |
|---|---|
| OSVersion | Microsoft Windows NT 10.0.26200.0 |
| PowerShell | 5.1.26100.9457, FullLanguage |
| Effective execution policy | Restricted; unchanged |
| Process environment architecture / pointer bytes | ARM64 / 8 |
| Runtime directory | `C:\Windows\Microsoft.NET\FrameworkArm64\v4.0.30319\` |
| CLR runtime version | 4.0.30319.42000 |
| Installed CLR file version | 4.8.9363.0, NET481REL1LAST_25H2_B |
| Installed compiler | `csc.exe`, 2,841,096 bytes, version 4.8.9221.0, NET481REL1LAST_25H2 |

Compiler presence/version is metadata, not a successful compile. `IsWow64Process2`
and `GetNativeSystemInfo` calls are in the unrun harness; actual native/process
machine values from those APIs remain **not observed**. Environment architecture,
runtime path and pointer width are supporting metadata only. There is no
managed-fixture, emulated-x64 or Windows-x64 App execution evidence.

The read-only capture used source commit `da0a2802`, with all four files compared
byte-for-byte to that saved revision before guest contact. It loads no `.ps1`,
uses no `-ExecutionPolicy` option, and changes no guest environment or settings.
The current capture omits guest TEMP/user-profile paths, caps stdout+stderr at
32 KiB, and uses one original 25-second monotonic deadline. Earlier read-only
metadata showed system TEMP `C:\WINDOWS\TEMP` and `Add-Type` availability; no
compiler or Add-Type compilation was invoked. One initial plain-Command metadata
request failed with a PowerShell parse error because prlctl removed quoting;
subsequent EncodedCommand calls preserve literals. That failure created no fixture.

## Native cases and cleanup

| Case | Saved source intent | Actual outcome |
|---|---|---|
| P01 positive | Suspended CreateProcessW with creation-time safety Job; original inner assignment/full invented generation bind before resume; ordered private entry/PRE acknowledgment; actual child creation HANDLE and first nonce effect separately; live retained descendant HANDLE queried for inner/safety membership | NOT RUN; no pass |
| P01 broken negative | Run leader, observe descendant creation/effect and retain actual HANDLE before inner assignment; delayed final marker; outside inner but inside safety Job; checker requires REJECT | NOT RUN; no observed negative rejection |
| P02 A | EOF while original process HANDLE remains unsignaled | NOT RUN |
| P02 B | Original leader HANDLE signaled while descendant keeps stdout open; live descendant observation | NOT RUN |
| P02 C | Actual exit 259 with signaled original HANDLE; 259 alone never exit | NOT RUN |
| P01 failure injection / incompatible outer Job | Setup/assignment/resume refusals and launcher constraints | NOT IMPLEMENTED/NOT RUN |
| P03/P04/P05 | Full-generation Stop and broader custody/death/crash probes | DEFERRED |

The C# source proposes a distinct non-inheritable kill-on-last-close safety Job,
creation-time `PROC_THREAD_ATTRIBUTE_JOB_LIST` for every leader and inherited
safety membership at descendant creation. Helpers inherit only explicit intended
stdio, and the supervisor uses the original leader HANDLE as DuplicateHandle's
source. No PID/name search, numeric-PID reopening or breakaway is present. The
inner Job is separate; its deliberate negative descendant stays safety-contained
by construction in the source. Entry, PRE acknowledgment, creation result/HANDLE,
first effect, membership and late final marker are separate records. Helpers
self-expire at 12 seconds, operations retain monotonic deadlines, and the
supervisor has an 80-second timer. The verifier refuses missing/unknown evidence.
These are reviewed design/implementation intentions, not native proof.

**Cleanup facts:** no guest fixture root/sentinel/artifacts were created, no
compiler or fixture-owned process/Job HANDLE was created, and no termination
operation was attempted. Thus no fixture cleanup was required. No all-exited,
Job-empty, last-close or crash-cleanup observation is claimed. The read-only
metadata invocation exited with code 0. Existing guest processes were untouched.

## Scrutiny, repairs and focused checks

[Initial independent review](windows_process_fixture_evidence/review1Summary.md)
identified the two high blockers above and a medium missing reviewed-source
binding. [Independent recheck](windows_process_fixture_evidence/review2Summary.md)
confirmed native execution withholding and the unchanged harness, then found
metadata TEMP exposure, response byte bounds, missing saved-revision binding,
and the not-yet-created results pointer. Ordinary local repairs at `da0a2802`
removed TEMP capture, added combined-channel byte/deadline bounds, required
`--source-commit` with exact file equality, and this return supplies the results
pointer. Those small metadata-only repairs were inspected by the Type1 owner;
no third independent review or native authorization is implied. The two high
bootstrap blockers remain open.

Focused host checks: Python syntax compilation, refusal of `--run` and mixed
`--run --inspect`/missing-mode inputs before guest or scratch effects, source/hash
identity preservation, evidence JSON parsing, `git diff --check`, and repository
`python3 -m tools.deliverables --project . check`. The independent recheck also
performed host-only syntax/refusal checks. No invented passing native trace was
used to stand in for a valid run or the deliberate native negative. Ordinary
App build/tests were not run because no production source changed.

Host artifacts remain at
`/tmp/chirality-app-win-process.FctUv4yh` (fresh `codex-home`, check/refusal outputs)
and `/var/folders/96/1_3ww0012pv5ptwwsd1990yw0000gn/T/chirality-app-process-readiness-mxwmesxf`
(raw readiness report and fresh `CODEX_HOME`). Governing source and durable
readiness/review evidence are committed here; scratch is not an instruction source.

ScopeOfWork REQ-008/VER-008 and dependency conditions remain unchanged: this
fixture preparation/refusal supplies no supplier/candidate qualification,
completion or acceptance. S01 exact SQLite 3.46.0, sidecar/open recovery,
namespace durability, native-control, supplier, production adapter and App/x64
checks remain deferred. No system SQLite substitution or VS catalog retry,
repin, installer/download or provisioning was performed.

## Guarded-bootstrap follow-up — 2026-10-29

**One independently reviewed in-memory bootstrap attempt failed at guest-session
admission. No compiler or P01/P02 case ran.** `prlctl` returned 255 with empty
stdout and:

```
PrlVmGuest_RunProgram: Unable to open new session in this virtual machine.
Make sure your virtual machine has finished booting, runs the latest version
of Parallels Tools, and is not isolated from the host OS.
```

The exact stderr, source hashes and full guest command are preserved in
[guarded_bootstrap_attempt.json](windows_process_fixture_evidence/guarded_bootstrap_attempt.json).
[Outcome interpretation](windows_process_fixture_evidence/guarded_bootstrap_outcome.json)
keeps that transport failure separate from compiler, fixture and cleanup facts.
No retry, inventory repetition, guest repair, settings change, installation or
workaround followed it. The VM was not stopped, reset or reconfigured. This is
an actual execution-prerequisite obstacle, not an inferred missing compiler.

### Local source, exact attempt and independent scrutiny

Host-created worktree: `/Users/ryan/.t3/worktrees/chirality-app/t3-0721d905`.
Branch: `t3/windows-fixture-guarded-bootstrap`. Required input
`ebf71ce713e4d71a2b32193fd360cfda3cd1dab9` remains an ancestor. All work and
commits are local; no push, PR change, merge or permission/release action occurred.
Shared instructions retain the source identity already recorded above; no
shared-library or packaged-asset write occurred.

The source family is now six files under `app/examination/windows_platform/`:
the unchanged `ProcessFixture.cs` and `verify_results.py`, repaired
`run_fixture.py`, new `Controller.ps1` and `test_driver.py`, and `README.md`.
The source asset ending `.ps1` is transported as exact bytes and evaluated only
in memory; execution never loads a `.ps1` file or overrides Restricted policy.

- Initial executable-source review examined
  `21f35b693eb13f2eed4abb836da2494166a0bb16`. Its
  [actual return](windows_process_fixture_evidence/guarded_bootstrap_review1.json)
  found a late controller reread after source checking, unsigned-exit conversion,
  cleanup settlement after the original deadline, and imprecise host-timeout
  wording. The manager fixed these ordinarily and obtained a new review.
- The [second actual return](windows_process_fixture_evidence/guarded_bootstrap_review2.json)
  examined `c5e01df9d4a06fa6184841cb30d22ec539e30590` and found no source blocker
  to the one zero-file bootstrap attempt under its stated controlled-invocation
  conditions. It retained two limitations: exceptional local teardown could
  escape the normal unknown report, and the dormant watchdog could accept a
  stop event without checking time after that wake. It expressly did not endorse
  the dormant controller for execution.
- The actual attempt used that exact reviewed `c5e01df9` source. An inline Python
  loader fetched the driver from that Git blob and executed it with the actual
  worktree `__file__`, `__name__='__main__'`, `--bootstrap-check` and the full
  `--source-commit`. The driver compared all six files to that commit and built
  transport from retained verified Git bytes without reopening Controller.ps1.
  The compressed payload was also compared locally with that saved Git blob.
- Subsequent local source at
  `c91621e09d118c001439d65d4425062bb856a913` repairs the two remaining findings:
  exceptional local kill/wait failure retains UNKNOWN without a Popen-context
  implicit wait; the emitted watchdog checks time after every wake, including
  stop, before accepting cancellation. This source has not reached the guest.
  Its final independent source scrutiny is retained separately with the return.
- The [third actual return](windows_process_fixture_evidence/guarded_bootstrap_review3.json)
  reviewed `c91621e0`, independently reproduced all six attempted source hashes,
  the command hash and decompressed controller Git-blob equality, and confirmed
  the failed-session/native-NOT-RUN account. It found one small remaining host
  reporting bug: selector/pipe close exceptions could discard the prepared
  UNKNOWN result. The manager repaired those closes and added a focused
  regression. This final small driver/test delta was checked by the manager;
  it was not independently re-reviewed or used for another guest attempt.

All Type2 tasks used `codex-hub/gpt-6.1-terra`, xhigh/priority, at most one active
at a time and no TASK delegation. Their actual returns were inspected; a
preparatory contributor's incomplete launch refusal was repaired by the manager,
not treated as proof of API impossibility.

The attempted guest command SHA-256 is
`f34d8a3142a14fcce05a1fb2984ad1e763a63ad08b4c05c2ed4e8db8fa156a33`.
Its 19,218-byte controller source SHA-256 is
`f4e5fb24a59ba81fb1c90d5259a4d8a8bc1345f47fa1b1b163b5cbbae32cb498`.
These identify the attempted source, not later local source or actual guest
copies. No guest hash response was received. The other five files were checked
on the host, not staged to guest disk. The raw record retains every source hash.

### Repairs and the remaining namespace gate

Reflection.Emit now prepares documented 64-bit layouts and PInvoke types in
memory, with sizes and offsets validated before use. Controller source starts
a dedicated emitted-IL watchdog thread before native Job/process setup; it
requires a distinct non-inheritable kill-on-close safety Job in the process's
creation-time Job list, uses no breakaway or Job-handle duplication, and retains
original process/thread/Job handles. It preserves true unsigned exit codes and
requires process signaling plus Job active zero within the original deadline.
After observed cleanup the watchdog accepts cancellation only after its own
time check; handle disposal follows watchdog join. Deadline/unknown paths
terminate only the controller root, whose last Job close requests cleanup.
That path never claims observed cleanup. This is **source preparation**, not a
runtime result or completed B integration; fixture stdout capture and actual
compiler/launch/watchdog validation remain owed.

The [API basis](windows_process_fixture_evidence/guarded_bootstrap_api_basis.md)
records why the considered sharing-only A guard is insufficient: CreateFile
share restrictions exclude attribute/EA access, and MS-FSA's reparse-setting
access test accepts FILE_WRITE_ATTRIBUTES. A file-ID check does not prohibit
metadata mutation on the same object. Denying FILE_SHARE_WRITE also conflicts
with pathname-based output writes; enabling it supplies no unique writer or
reparse exclusion. Other tag/size/privilege checks still apply. This is a
documented proof gap for this guard, not a demonstrated guest exploit or a
universal package-free impossibility claim. No continuously safe compiler
namespace is implemented or admitted, and `--run` still refuses before contact.

A caller-owned-stream compiler API is a candidate alternative. The attempted
bootstrap would have checked only `Microsoft.CodeAnalysis.dll` and
`Microsoft.CodeAnalysis.CSharp.dll` beside the framework compiler. Those checks
were **not reached**. No global absence, assembly compatibility, compiler
temporary behavior or availability of that alternative is claimed.

### Observations, limits and next step

The guest remains pinned to VM `2944eb77-696f-41ad-97e2-142ba0489535` via
`prlctl exec`. Readiness at `da0a2802` remains historical metadata: Windows 11
build 26200, PowerShell 5.1 FullLanguage/Restricted, ARM64 environment, 8-byte
pointers, and installed FrameworkArm64 .NET 4.8.1 compiler. The failed session
produced no new runtime, layout or `IsWow64Process2` process/native machine
observation. No ARM managed fixture or native-x64 App evidence exists.

P01-positive, the deliberate P01-negative and P02 A/B/C are all **NOT RUN**.
There is no observed late-marker rejection, inner-Job exclusion, outer-safety
inclusion, EOF/process-signaling distinction or true-exit259 result. Compiler,
controller lifecycle, timeout observation, host-loss/crash and last-close
experiments also remain unrun. The attempted route requested no guest fixture
file, compiler, helper or Job creation, so no fixture-owned cleanup was required;
no retained-HANDLE/Job-empty cleanup observation is invented. Guest PowerShell
completion was not observed through the failed session.

Host-only regression checks cover refusal/source binding, exact-byte bounded
gzip transport, overflow/timeout UNKNOWN and failed local teardown reporting.
The unchanged native verifier rejects an empty trace. Schema/hash checks and
the Git checkout-byte regression pass; deliverable consistency is checked with
the repository tool. Fresh mktemp CODEX_HOME directories were used. No App,
supplier, peer or model execution, downloads or provisioning occurred.

The next small step is restoring the authorized `prlctl` guest-session
prerequisite without assuming permission for VM/tool/settings repair. Before
any compiler or case attempt, independently establish A across every compiler
open and integrate/validate B with bounded fixture-output capture. ScopeOfWork
REQ-008/VER-008 and all dependency conditions remain unchanged; the new host
regression is added only as a check pointer. This supplies no acceptance,
production-policy decision, supplier qualification, storage/durability evidence
or release advancement.
