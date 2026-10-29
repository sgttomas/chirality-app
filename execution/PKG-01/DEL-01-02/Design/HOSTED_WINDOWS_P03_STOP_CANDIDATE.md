# Hosted P-03 generation-bound Stop candidate

2026-10-29: **all three required hosted native-AMD64 scenarios completed** at
source `0aec700dd15f961d358f9bcd9d6e1760905b20dd`, run `40922543448`.
The final section records inspected native results. Earlier candidate/review
accounts below retain their original unrun scope. Agent0 owns integration.
No App Windows compile/launch, supplier, crash, durability or production policy
qualification follows from this synthetic probe. The P-01/P-02 pass at
`d26ecdae` and all three earlier failures retain their original bytes and limits
in `HOSTED_WINDOWS_PROCESS_FIXTURE_RESULTS.md` and its raw artifacts.

## Basis and receiving scope

The owning design's P-03 row specifies a descendant surviving stdin EOF, a
pending Stop bound to full generation g through replacement by g+1, admission
refusals, and process/Job observations before retirement. This separate harness
implements that synthetic mechanism probe. It does not select an App Job policy
or implement the proposed Rust capability. ScopeOfWork OUT-003/REQ-008/VER-008
still require actual candidate-bound native evidence; existing product
commitments, acceptance conditions, dependency conditions and lifecycle standing
are unchanged. `deliverable.yaml` gains check pointers only. No other consumer
interface changes and no supplier, resources or production implementation changes.

Inputs: clean isolated baseline `735f65d3ef58f65b6f2ed066d97de34d2ff48cb5`,
read-only fetched main `c5b33e37832364eaa04360540ea5e31bc08a9168`, merged with
both parents at `eb603aa30ba09a3ce8cdf0de4cc008c8c0362aa8`. Selected shared
role/method source: `/Users/ryan/dev/chirality` at
`1560bbf7f7add4637a20572a2b0d404ef121af63`,
`agents/AGENT_WORKING_ITEMS.md`, `agents/AGENT_TASK.md`, and
`workflows/coordinated-knowledge-work/WORKFLOW.md`. Consultation changes no
packaged App instructions or shared-library files.

## Separate stimulus and authority

`P03Fixture.cs` uses an external fixture supervisor holding the sole unnamed,
non-inheritable safety Job handle. It creates the controller suspended with a
creation-time JOB_LIST containing that Job, verifies membership, then resumes.
The controller creates actors suspended, inheriting that external safety Job
without breakaway, assigns their inner generation Jobs and verifies membership
before binding/resuming. A leader's descendant inherits both Jobs. Inner Jobs
have kill-on-close **off**. The safety Job's kill-on-close is fixture cleanup
only; this probe supplies no parent-death or all-descendant App guarantee.

The leader creates one descendant and sends its process HANDLE value over a
private inherited allowlisted pipe. The controller duplicates it directly from
the retained original leader process HANDLE while the leader still owns it,
checks non-inheritance, original Job membership and liveness. This is a live
source-owned handle transfer, not a PID lookup. There is no OpenProcess,
process/name scan, cold adoption, identity reuse, named Job or global kill.
Generation Jobs and creation process handles stay in private in-memory objects.

The complete generation is `appSession=<launch nonce>`, `home=fixture-home`,
`spawnCounter=1`. A second bind, numeric PID, serialized PID and mismatching
session, home or counter cannot start custody/Stop. A current Stop records its
explicit fixture cause before closing stdin and captures an immutable original
capability/generation before waiting. The leader acknowledges EOF then exits;
after a 150 ms **fixture test value**, its retained HANDLE must signal, while
the descendant remains live and authoritative original Job active count is one.
The controller logs the pending captured generation, starts the one-actor
successor with counter 2, and replaces the current slot. A fresh stale-g Stop
against the successor is refused. The pending operation uses the captured
original Job, never the current slot. This deterministic pending continuation
tests replacement across blocking work; it is not a concurrent App lock test.

TerminateJobObject attempt, success/error and retirement are separate events.
Success never supplies exit evidence. Confirmed retirement requires the original
leader HANDLE signaled and authoritative original Job active zero; this probe
also observes the retained original descendant HANDLE signaled. The successor
must still be live with active count one before fixture cleanup begins.

## Falsifiable controls and bounded failure

Three serial fresh-nonce launches are required for the supplemental lane:

- `positive`: original Job emptied, successor untouched, retirement confirmed.
- `wrong-slot`: deliberately targets the successor Job. It must actually show
  successor signaled/active zero and original descendant live/active one;
  retirement stays unknown. Its trace is rejected as a positive result.
- `missing-observation`: after successful original termination, deliberately
  withholds the authoritative Job-query observation from Stop. Retirement stays
  unknown and custody remains held until separately logged fixture cleanup.
  This is injected observation unavailability, not a claimed OS API fault.

The three refusal combinations success-alone, leader-only and zero-only cannot
confirm retirement. A source-bound verifier requires exact event order, full
generation, native AMD64 identity, original observations, controls, original
deadlines, cause/grace and cleanup. Missing/extra events, unknown cleanup,
nonzero return, timeout, output overflow or unexpected stderr fail the lane.
Only `positive` carries `mechanism_pass=true`; the lane's eventual PASS would
mean the positive probe and required negative/partial-failure controls completed.

No more than four child actors are possible concurrently: controller, original
leader, original descendant and successor (the leader actually exits before
successor creation). The supervisor is outside its own safety Job. Safety and
inner Jobs cap active processes at four, process memory at 128 MiB and Job memory
at 384 MiB. Each scenario starts one absolute QPC experiment deadline at 12 s
and cleanup deadline at 18 s. Actors use that original experiment deadline;
cleanup gets no renewed wait. Controller cleanup reserves the last three seconds
for the external safety owner, including suspended inner-assignment failures.
The supervisor separately has a 25 s fail-only timer. Its expiration/last-close
is never observed cleanup or a pass. The Python wrapper's original capture
deadline is 35 s plus at most 5 s original-handle termination observation; raw
stdout/stderr share a 128 KiB bound. Private pipes have 4 KiB bounds and only
fixed small fixture messages. No unbounded wait, thread join or capture exists.
The supervisor requires its retained controller HANDLE signaled plus safety Job
active zero. Controller cleanup separately requires every retained actor HANDLE
signaled and every original inner Job active zero. Uncertainty fails; cleanup
never rewrites an earlier unknown Stop to confirmed retirement.

## Hosted binding and pending native claims

`run_hosted_p03.py` reuses unchanged hosted admission, bounded capture and Git
binding helpers from `run_hosted_fixture.py`, with a separate exact input set:
attributes, supplemental Stop workflow, both runner sources, P-03 C# source and
P-03 verifier. HEAD must equal the requested full commit; every checkout input
must match its Git blob, SHA-1 object identity and recorded SHA-256. Source copy
bytes are rechecked, and all bound inputs are rechecked immediately before
launch. Profile: `github-hosted-native-amd64-p03-synthetic-stop/v1`, trusted
checkout/runner namespace; no claim to exclude adversarial namespace races.

Admission requires disposable GitHub-owned Windows/X64, native AMD64 64-bit
Python >=3.9 and IsWow64Process2 evidence. Only preinstalled Framework64 compiler
and explicit framework references may compile `/platform:x64 /nostdlib+`.
Compiler banner/file hashes, executable hash, source/blob hashes, original argv,
bounded raw compile/native stdout/stderr and command outcomes are retained in
`windows-stop-fixture-evidence/result.json` and sibling raw channels. Fresh owned
scratch TEMP/TMP/CODEX_HOME and exclusive artifact creation prevent stale reuse.
There is no package/tool acquisition, guest adapter or live supplier call.

The additive `windows-stop-fixtures.yml` runs only the separate synthetic lane;
the P-01/P-02 workflow and checked stimulus are unchanged. Actual Framework64
compilation, native Job nesting/assignment, EOF survival, generation isolation,
both controls and cleanup remain **NOT RUN** until Agent0 publishes/runs the
reviewed candidate. Host parser tests establish none of those native claims.

## Host verification and independent scrutiny

Eight P-03 host unit methods pass: admission before execution/scratch, exact
bound verifier bytes, three distinct invented outcomes, required/unique events,
generation/architecture/process/Job/cleanup mutations, negative-control promotion,
deadline/grace bounds and raw channel/nonce refusals. Their invented traces are
ephemeral test inputs and are never saved as purported native evidence.

Actual independent Type 2 source scrutiny completed on exact commit
`5be2c733c513a9da700b66464730ffda5f4d1f2c`, via host-managed isolated worktree,
using `codex-hub/gpt-6.1-sol`, `reasoningEffort=medium`, `serviceTier=default`.
The reviewer compared all nine changed files to committed blobs, inspected the
actual original HANDLE/Job and generation paths, negative controls, observation
rules, old-C# source/ABI plausibility, containment, deadlines and cleanup. It
reported **no substantive findings or must-fix publication blockers**. No repair
was required. It independently ran the eight host units, deliverable graph check
(41 deliverables, zero errors, six existing cycle groups), committed-byte
comparison and whitespace check. No native compilation/execution, guest work,
download or remote operation was performed by that reviewer.

Manager checks used a fresh `tempfile.TemporaryDirectory` CODEX_HOME and
`PYTHONDONTWRITEBYTECODE=1`; no supplier or Codex process was launched:

```text
python3 -B -m unittest discover -s app/examination/windows_platform -p test_p03.py -v
python3 -B -m tools.deliverables --project . check
git diff --check
```

All pass (eight unit methods; graph errors empty). Calling the actual hosted
`bind_sources` helper against committed `5be2c733` on the host verified all six
inputs against exact Git blobs and SHA-256. The reviewed native source blob is
`d4f46f4c5728a3d299e5696e67c28cf9d2454f0c`, SHA-256
`9a3fa9a65138d2e28366610adaa422f6e26f661650048fcd6ed17c52c640f962`.
The review-record follow-up changes only this document; runtime inputs and tests
remain the independently checked bytes. P-01/P-02 implementation, verifier,
runner, workflow, host tests, result narrative and raw evidence compare
byte-identical to baseline `735f65d3`; their unchanged parser units were not
repeated or presented as native requalification. Both baseline and fetched main
are committed ancestors. No push, PR or hosted run was performed by this manager.

## Agent 0: inspected hosted native result

[Actions run 40922543448](https://github.com/sgttomas/chirality-app/actions/runs/40922543448)
compiled and ran exact integrated source
`0aec700dd15f961d358f9bcd9d6e1760905b20dd` on disposable hosted
`windows-2022`, image `20261026.347.1`, OS build 20348. Supported machine APIs
observed native AMD64 (process machine 0, native machine 34404, 8-byte pointers).
The preinstalled Framework64 compiler reported `4.8.9363.0`; Python was 3.12.10.
This is not Windows 11, Parallels or production App execution.

Agent 0 inspected [the exact result](hosted-windows-p03-evidence/0aec700d/result.json)
and all three raw traces, verified all six source blob identities/lengths/SHA-256
against the committed source, checked every compiler/native channel hash and
length, and reapplied the bound verifier to the raw native bytes. All 19 artifact
files are preserved byte-for-byte; no executable binary is committed.

- [Positive](hosted-windows-p03-evidence/0aec700d/positive-native.stdout): the
  original leader exited after stdin closed, its descendant remained live
  through the fixture grace, and the current slot changed to g+1. Stop acted
  on captured g; original leader/descendant HANDLEs signaled and original Job
  active count reached zero while g+1 remained live with active count one.
  Retirement was CONFIRMED only after those observations.
- [Wrong-slot control](hosted-windows-p03-evidence/0aec700d/wrong-slot-native.stdout):
  deliberately terminating g+1 left g's descendant live/active one and killed
  the successor. Retirement remained UNKNOWN; mechanism_pass was false.
- [Missing-observation control](hosted-windows-p03-evidence/0aec700d/missing-observation-native.stdout):
  termination API success did not establish retirement when the authoritative
  Job observation was withheld. Custody remained held and retirement UNKNOWN
  until separately logged fixture cleanup; cleanup did not rewrite the outcome.

Each trace rejected second binding, numeric/serialized PID authority and stale
session/home/counter/generation admission, plus success-only/leader-only/zero-only
retirement. Both control traces also reject when presented to the positive
verifier. All three observed retained-actor exit/inner-Job-zero cleanup followed
by retained controller exit/external safety-Job active zero within original
deadlines. Compiler/native commands returned 0, with no stderr, timeout,
response-bound or teardown uncertainty. The lane PASS means this positive
synthetic mechanism and its required controls completed; neither control is a
successful Stop result.

No production App adapter, concurrent App source-gate race, crash policy,
supplier, hostile namespace, SQLite/durability or owner qualification is
established. The owner superseded the second-local-VM route: no further media,
setup, boot or provisioning is planned/authorized under it. Dormant hardware
is preserved without contact; CAEPIPE stays excluded. Current hosted work needs
neither local media nor cloud provisioning. Commitments/dependencies are unchanged.
