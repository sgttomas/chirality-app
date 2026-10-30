# Phase B relaunch preflight

Phase B has **not run**. The 2026-10-30 preflight found that the proposed
extension of the A sandbox cannot both admit supplier startup and prevent
uncovered helper creation. This is a controller-design result, not a failed
native supplier handshake or an App qualification result. Candidate
`795362874d-a391547a5c5d` and the successful A state remain unchanged.

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
