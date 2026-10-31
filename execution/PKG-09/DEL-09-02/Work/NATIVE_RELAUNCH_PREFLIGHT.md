# Phase B relaunch preflight

The first successor B attempt has now **FAILED** before source/generation
observation. [Its failed-run and cleanup account](FAILED_B_20261031.md) is the
current outcome; preparation/review stages below retain their historical heads
and limits. No B pass or supplier settlement follows from administrative cleanup.

At the 2026-10-30 preflight below, phase B had not run. It found that the proposed
extension of the A sandbox cannot both admit supplier startup and prevent
uncovered helper creation. This is a controller-design result, not a failed
native supplier handshake or an App qualification result. Candidate
`795362874d-a391547a5c5d` and the successful A state remain unchanged.

The next live B input is now the repaired successor
`fdcf608fb5-23c6c3f22f5e`, whose A succeeded at 22:28:05–22:28:16 UTC on
2026-10-30. Its saved request digest is
`ef606ee5cf6dfe3bcd9b6c2b150a89e7a2710c6289c56d180c8e6ea5dd7705de`;
the exact bindings and private-metadata checks are in
`../Evidence/EXP/fdcf608fb5-23c6c3f22f5e/native-A-20261030T222805Z/`.
The retained native root is
`/Users/ryan/dev/chirality-t3/scratch/app-successor-native-A-irf2swd9/`.
B must consume that state without rerunning A, rewriting the request or
resetting any namespace. The original candidate's A tuple below is historical
and remains preserved, not substituted for the successor's input.

After this preflight, App Agent 0 selected a focused startup/shutdown custody
repair and a successor development candidate before live B. The original
candidate and A state stay retained; successor results will have their own
identity and namespace. B's explicitly admitted forks and exact-executable,
network-denied profile are a bounded execution arrangement, not proof of
exhaustive descendant containment. The repair must settle owned probes and
app-server groups, retain supervision on unavailable settlement and report
detached-helper observation limits. No universal adversarial fork/setsid
cleanup requirement is added. This supersedes treating that exhaustive proof
as a prerequisite to B, without changing the isolated policy observations below.

## Examined route and actual checks

The proposed route was exact saved-request relaunch, native diagnostics,
generation-bound Stop, verified settlement, then native Quit. Independent
read-only Type 2 scrutiny used codex-hub `gpt-6.1-sol`, reasoning effort `xhigh`,
service tier `priority`. It identified these source limits:

- `app/src-tauri/src/desktop_startup.rs` selects legacy `HostConfig` for this
  development launch. `Host::verify` in `hosting.rs` calls blocking `.output()`
  for `--version` before the app-server's generation custody. A hung probe
  cannot be stopped through a generation that does not yet exist. The bounded
  successor probe is a different route.
- `process_group_custody.rs` reserves the original supplier group; its census
  explicitly excludes detached/escaped descendants. App `finish_exit` in
  `app_quit.rs` ignores Stop errors. App exit alone cannot prove supplier
  settlement.
- The A controller's `poll()`, terminate and kill fallback would release App
  custody and may abandon supplier work. It must not be reused for B.
- `App.tsx` renders state/generation as text. The lifecycle JSON contains
  `lifecycle` and `clientRequests`, not a full state/generation snapshot. The
  retained raw B parser is inapplicable.

The maintained [isolated policy checks](test_native_relaunch_policy.py) passed
three tests on this macOS host on 2026-10-30, using Python 3.13.14. No App,
supplier, model, credential or actual A state was used:

| Fixture | Actual observation | Consequence |
| --- | --- | --- |
| Exact executable allowlist plus `deny process-fork` | `posix_spawn` of allowlisted `/usr/bin/true` refused with EPERM, including `setpgroup=0` and `setsid=True` | A's fork restriction cannot simply remain while admitting normal supplier spawn. |
| Same allowlist with fork allowed | Invented child forked without exec, called `setsid`, exited normally and was waited by its creator | An executable allowlist does not prevent group escape without exec. |
| Same allowlist with fork allowed | An allowlisted Python child spawned the same binary in a new session, exited normally and was waited by its creator | Same-binary helpers are also admitted. |

The first exploratory probe is retained in
`/Users/ryan/dev/chirality-t3/scratch/app-B-spawn-policy-l1psblkl/`, including
policy, script and result. The maintained tests reproduce and extend that
observation with fresh temporary homes and fixed environments. All fixture
children settled. These checks demonstrate specific policy limitations, not
that stock Codex actually takes either escape route. A scoped executable
census could corroborate a run but cannot replace ownership or prove exhaustive
fork/escape coverage.

## Required B observations and settlement order

Admission must validate A's exact request digest
`556a3b9ec7d1efce8b14bbc76e31637db40f6f866cb12f2f2c633dc751e9c547`, private
file/parent metadata, full native reference tuple and shared links; check the
complete candidate inventory; and use a fresh fallback home/tmp with the fixed
environment. Do not create a replacement request, rerun A or remove App data.
Keep network and personal-home denials. Validate recovery input state before
startup; existing recovery targets must not silently cause prohibited requests.

The native record must bind the saved-request launch to the actual executable,
full `{appSession, home, spawnCounter}`, observed `codex-cli 0.160.0`, initialize
response and LT-09. Preserve `unverified-development` standing. Legacy startup
ignores an `initialized` write failure: LT-09 alone does not prove delivery of
that notification. Read actual rendered sections and native envelopes; never
synthesize a ready snapshot. Inspect requests for prohibited model, auth,
thread, turn or tool activity.

Capture the generation before native Stop and its exact confirmation. A
`stopped` state alone is insufficient: its LT-23 must name that same generation,
contain observed leader exit facts, and report `descendants.checked == true`
and `surviving == 0`. Record any App-owned forced termination. Separate helper
escape accounting is still needed; this group result cannot establish it.
Only after the required settlement facts may the controller request Quit.

Retain the original App child without polling/reaping, using
`waitid(P_PID, pid, WEXITED | WNOHANG | WNOWAIT)` for observation. Never signal
a sampled supplier PID or group. Observation errors, cancellation, refusal,
generation drift, missing/unknown settlement, or early App exit must leave
supervision and resource accounting active and preserve live/unknown standing.
An App zombie reserves only the App PID, not the supplier's. Do not destroy
the observer or turn an overrun into a clean result. Native Stop is disabled
after `stopped`; a second click is not a guaranteed cleanup route.

Before execution, a separately reviewed route must resolve helper accounting
and failure supervision. Guaranteed cancellable legacy-probe cleanup or
custody surviving App death requires additional implementation/candidate work;
it is not supplied by the proposed controller. App Agent 0 owns substantive
shared design/candidate decisions. No changed criterion or weaker containment
has been adopted. The manager continues preparation and returns that precise
obstacle through the assigned session.

The confirmed resource profile permits concurrent slot/memguard execution of
one retained App, version probes and app-server initialization, with a 4 GiB
planning allowance (not measured peak), at most 180 seconds work plus cleanup
and a five-minute target. No model/oMLX/network/auth or performance measurement
is included. No clearance/START/END handshake is needed. Overrun or resident
processes must be reported; resource coordination does not resolve containment.

ScopeOfWork and dependency conditions are unchanged. This preflight supplies
no V4-EXM-10/11/12 pass, personal human act, supplier qualification-pin decision,
acceptance or release. Preserve all candidate, A-state and named recovery inputs.

## Repair verification before a successor build

The prepared Rust repair reuses actual `OwnedProcess` custody for both label
probe routes, retains unknown reservations, cancels by start attempt, and gates
ordinary Quit on actual owned-process settlement before its session-end record.
DEL-01-01's `HOSTING_BOUNDARY.md`, DEL-01-02's
`EXECUTION_AND_RECOVERY.md`, and DEL-01-04's `NATIVE_QUIT_SETTLEMENT.md`
carry the changed implementation meaning. Their ScopeOfWork commitments and
dependency conditions are unchanged. The preflight evidence review at
`e4a16bdbb89895b4324ef51dfa06643260d0c9b9` found no issues and independently
reproduced all three policy checks using the previously selected reviewer;
subsequent repair scrutiny uses the owner's updated reviewer selection.

Focused offline Rust 1.97.1 checks use a fresh scratch Codex home and cloned
prepared cache under
`/Users/ryan/dev/chirality-t3/scratch/app-native-custody-xwl7wbmc/`, slot admission,
memguard and two build jobs. Five probe tests, 36 Quit-filter tests and the
system-termination test passed; 12 process-group custody tests also passed.
The successor suite passed 97 tests with four
explicit exporter/stock-supplier cases ignored. Its first run exposed an
existing test polling past the transient `stopping` state; synchronization at
the existing cleanup hook repairs the test without removing its invalidation
assertions. Logs retain the initial failure and successful recheck. The first
probe run also retained an expected-diagnostic assertion failure at a 200 ms
fixture budget; that assertion omitted the actual error, so its precise cause
was not established. With failure diagnostics improved and a 500 ms fixture
budget, the bounded hang/noisy-output cases passed with the same
under-three-second upper bound. These are source/fixture results only;
no successor bundle or native A/B result is claimed here.

Retain this repair scratch and its check logs through review/integration in
addition to the original candidate/A inputs. Do not reuse the original bundle
identifier or namespace for the successor, or relabel historical A evidence.

### Independent repair review and disposition

Claude Opus 5.5 at high effort (fast mode off) reviewed
`fa69b98cbe007196608adb54b5fdad6c25abe9ab`. It found the retained custody,
cancellation, unknown handling, home enrollment and Q-7/AS-10 mechanics sound,
but identified four findings. That head's CI failed; it is not a passing basis.

- CI exposed slow legacy fixture startup exceeding the reused two-second
  handshake timeout. Probe waiting now has a separate budget, defaulting to
  and capped at 20 seconds; handshake/request limits are unchanged. A real
  label-probe regression verifies independence from a zero handshake budget.
  Hang/noisy fixtures explicitly set their shorter probe budget.
- The added receiving paragraph changed a frozen examination source digest.
  `NATIVE_INTERACTION_RECEIVING.md` is restored byte-for-byte to main
  `b20a0c37`; the implementation note lives in the companion
  `NATIVE_QUIT_SETTLEMENT.md`. No examination pin or adopted source is changed.
- A probe could publish refusal between Quit's state observation and Stop.
  The repair judges a raced idle-state Stop refusal after actual retained
  process settlement. Unknown custody still fails; a deterministic hook test
  exercises that interleaving without requiring a spurious Quit retry.
- PR CI now includes the probe, Quit, Codex Stop, LT-12 and stalled-probe
  regressions. The real-host Quit tests again assert the specific closed-turn
  refusal between confirmation and settlement, before checking final exit
  permission. The reviewer found the LT-12 hook synchronization sound.

The manager repairs these bounded findings directly. The earlier review's
actual model, head and limits remain preserved; no clean review is claimed for
the failed head. Updated checks and hosted CI must establish the repaired
head's standing before a ready integration return.

Post-repair local checks passed: seven probe cases, 37 Codex Stop cases,
18 App Quit cases, 15 LT-12 cases, 21 conversation-role cases, the stalled
probe case and all nine access-integration cases. The complete CI pinned-source
pytest group passed 106 tests and 382 subtests after the byte-exact restoration;
62 CI-selection tests and deliverable validation also passed. These checks
use the retained repair scratch, offline caches and serial Rust test execution.
Hosted CI on the new head remains separate from these local results.

## Successor B controller prepared, not executed

`native_successor_relaunch.py` is a standalone B controller; it does not inherit
A's emergency termination/reaping. It validates the successful successor A
result, exact saved request/private metadata/shared links and unchanged invented
inputs. Admission refuses unexpected account files, additional homes or prior
runtime/recovery data without reading credential contents. It rechecks the
complete bundle inventory, fixed launch environment, explicit two-executable
sandbox and namespace metadata before launch, with noninteractive AX-trust and
WNOWAIT availability checks. The sandbox admits forks and only the exact App
and stock Codex executable; network and personal Codex-home denials remain.
Path-scoped process observations corroborate activity and conservatively refuse
overlapping launch; they never supply signalling authority or exhaustive
descendant absence.

The original App remains a strongly held, unreaped child. Ready observation
requires rendered state/version/full generation, same-source LT-09, actual
launcher/content identity and a correlated native initialize response. The
generation's home must equal the source implementation's hash of the validated
saved account path. Any observed request other than this initialize makes the
witness fail; the controller initiates none. The actual UI header and lifecycle/envelope JSON are read
separately; no full snapshot or injected ready value is invented. LT-09 alone
does not establish delivery of the `initialized` notification.

Native Stop's exact question binds the observed source. LT-23 must retain
known leader exit and complete empty original-group census before native Quit
and original App reap. App-owned forced supplier termination, if observed,
remains explicit. Work/guard/log failures permit a bounded normal cleanup
attempt using those same gates; they never become a passing result. Unknown
cleanup keeps the supervisor, guard, slot and original reservation alive and
reports `held-unknown`, including any resource overrun. It never signals cached
App/supplier numbers or kills App to abandon supplier work.

A held observer accepts at most one validated operator request file in its own
attempt directory, `retry-native-cleanup.json`, containing only
`{"action":"retry-native-cleanup","candidate":"fdcf608fb5-23c6c3f22f5e"}`.
It reobserves the same source and gives native cleanup 45 seconds; it accepts no
PID, command or code input and does not silently repeat attempted UI presses.
The original failure remains failed even if this cleanup succeeds. Permanent
AX/parser loss cannot be repaired inside the frozen controller; it remains an
explicit held limitation requiring a concrete recovery disposition, not a
manufactured clean result. OS-forced observer/App death remains outside this
supervision claim.

Eleven invented-fixture tests passed, including actual nonreaping observation
of a tiny owned child, source/response/settlement rejection, Stop–Quit–reap order,
guard-expiry cleanup, safe lost stdout and bounded log-error retention. A
read-only check of the actual successor A input passed. These tests neither
launch the App nor exercise its native B diagnostic shape. Independent
pre-execution scrutiny remains required; B has not been prepared or launched.

### B review disposition and selected failure behavior

Independent Claude Opus 5.5/high review at `37c985b6` found two high controller
defects: normal App exit could race an AX traversal after Quit, and witness-pass
checks incorrectly blocked safe same-source cleanup. It found no issue with
the actual successor A evidence: all 24 digests and retained-root copies matched.
That A evidence does not need another review merely because B is repaired.

The repaired Quit wait accepts exit during AX search only after supplier
settlement and native Quit request. It stops searching once the Quit question
is confirmed, and a cleanup retry after Quit only waits for exit. Early exit
without those gates remains unknown. Cleanup now has a separate source gate:
the held, inventoried App, saved account hash, actual same-generation LT-06
spawn event and matching native Stop question bind the target. LT-06 is emitted
by the checked Host only after actual spawn of the admitted bundled executable;
the exact two-executable policy and saved startup choice constrain that route.
Any available LT-09 launcher must corroborate the same executable. A mismatched
or unbound source is never targeted. Expected requests, successful handshake
identity/version and qualification are not cleanup prerequisites; their failures
remain failed witness results after successful cleanup.

App Agent 0 explicitly selected native Stop for captured, bound generations in
handshaking, halted and unexpected-exit states as permitted by the existing
contract. This B version has **no pre-generation Quit-only route**. Absent or
missing generation remains supervised-held with the original App reservation,
guard and slot, requiring immediate root reporting of resident/overrun state.
No retry spawn, cold numeric signal, discarded reservation or fabricated LT-23
is authorized. This is bounded selected failure behavior, not an exhaustive
cleanup guarantee.

Result records now carry supplier exit/force facts, descendant observations and
observed cleanup-limit journal entries (or unavailable standing), rather than
leaving force implicit in a success boolean. Admission compares current
namespaces to A's write-once post-settlement record. Reporting after reap uses
the safe reporting path. SIGINT, SIGTERM and SIGHUP request failure/cleanup;
OS-forced death or an external harness kill cannot be prevented by this observer.

**Remaining native observation risk:** the inherited AX traversals still cover
the main window, with limits of 900 nodes and depth 20. A had 386–416 nodes with
diagnostics closed; B's expanded tree and traversal time have not been measured
or observed. Exceeding those limits can prevent source observation/cleanup and
leave a supervised-held result. These limits are not raised or passed off as
native evidence. Fifteen focused tests now pass, including exit during Quit
search, no repeated confirmed question, failed-request cleanup, pre-ready
source binding and force/limit result preservation. Actual A namespace/request
read-only validation still passes. B remains unrun pending focused scrutiny of
the materially changed cleanup gates and exact-head checks.

Focused independent review at `aa6e011a` confirmed both high findings fixed and
the bound-source cleanup route sufficient, including before LT-09. It found
one medium interpretation issue and two low test/latency observations. The
manager's disposition uses the existing HOSTING/RECOVERY Q-6 Stop contract:
App-owned force after grace can still count as **observed owned-group
settlement** when the leader exit is known and the original-group census is
complete and empty. Earlier reported cleanup limits likewise do not erase
those later observed facts; all limits remain in the result. B's `success`
means its bounded initialize/ready, settlement and normal App Quit observations
were obtained without witness/guard/log failure. It is explicitly **not** a
graceful or error-free supplier claim, a full candidate qualification or a
changed acceptance criterion. `success_scope` states this in the result itself.
A's `forced == false` requirement concerned emergency controller termination
of the App, a different operation that B never performs.

Eighteen tests now pass. Added negatives cover missing, duplicate and foreign
LT-06 events, disallowed states and missing generation leading to held evidence
without Quit/reap. A clearly permanent failure on a bound source (unexpected
request or halted/ended state) exits the ready wait immediately and proceeds
to the same cleanup path; incomplete observations remain bounded waits.
Unavailable settlement results now retain the same nullable field names.
These are bounded review dispositions, not a new design or another native
result. A evidence remains unchanged; B is still UNRUN. Exact-head CI remains
the outstanding integration check.
