# Bounded package-free Windows process fixture return

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
