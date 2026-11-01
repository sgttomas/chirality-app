# j58087z7 activation refusal: bounded offline assessment

## Actual outcome and comparison

This attempt remains FAILED. Candidate1f67d3822b-8c83d74ae3ce/source1f67d382 is
unchanged; no reset, rebuild or new launch was made for this assessment.
Helper001 passed the repaired admission parser and produced the verified owned
`window-001.png`, SHA256
`89d8a522f36c207e4ab2cc8419576bfd7c88166671a4af385b19e16650d6f5a7`.
I inspected that exact retained image offline: it shows a rendered Desktop
setup page, “Current launch: setup-required” and “No explicit desktop request
saved”, with blank source fields. It is not a supplier-ready or AX-readiness
observation. No desktop/foreign image was read or captured.

| Retained observation | 095p183p | j58087z7 |
| --- | --- | --- |
| Subject | historical fdcf successor, saved-request B | current1f67 candidate, setup-required A |
| First helper focus read after recorded App start |41.699871s |2.018223s |
| Initial AXFrontmost |false |false |
| Actual receiver policy/options |0 /0 |0 /0 |
| activateWithOptions return, recorded as request_sent |true |false |
| Subsequent frontmost observations |false, then true |none; helper refused immediately |
| Focus result receipt |success at21:43:32.302867UTC |absent after Python refusal |

The `activate_original_app` function AST is identical in the two frozen helper
copies. This compares the actual selected function, not a claim that every
helper/controller/candidate byte or surrounding OS state is identical.

j580 helper002 has a complete focus trace: receiver77302, regular policy0,
options0, request_sent=false, and the Python error “owned App activation request
refused”. Its traceback is at the explicit false-return gate, after the
NSRunningApplication lookup, receiver/policy checks and actual method call.
This is **an attempted activation returning NO**, not a no-op, missing attempt,
missing trace, helper timeout or native abort. No second activation occurred.
The initial App remained the retained live Child until the owner's normal Quit.

Local SDK NSRunningApplication.h documents YES as request successfully sent,
NO as not sent (with examples, not an exhaustive reason). The helper's return
name follows that contract; neither value alone establishes foreground effect.
For this false return, no post-call AXFrontmost sample was taken. A no-op instead
has activation:null plus one true observation and a successful result. Missing
trace/native abort is unknown; neither applies to this recorded Python refusal.
Existing focused tests already distinguish those cases; no duplicate activation
framework or broader API probe is needed.

## What the evidence does not determine

The earlier success happened substantially later in startup, but that correlation
does not prove a startup race. Rendering a WebKit page and having a regular
activation policy do not prove NSApplicationDidFinishLaunching or complete AX
availability. `isFinishedLaunching` was not recorded. The SDK says some apps
never report that property, so making it an unconditional gate without product
support would itself risk permanent refusal.

macOS cooperative foreground policy is another plausible factor, but the trace
does not identify the system's reason. The background helper's method once
succeeded in095; that does not establish a durable foreground entitlement.
Do not label this “foreground policy denied” or “too early” as a proven cause.
No ignoring-other-apps flag, yield, alternate transport, repeat request or delay
increase is justified by the false return.

Cleanup's “distinct owned main AXWindow unavailable” means the filtered lookup
found no unique role/title match. Possible observations include no roots,
unsupported/timed-out attribute, app self-reference, or unmatched role/title.
The current run retained **no AX root observation file** at that refusal. The
root/attribute observations existed only in the now-ended controller object,
so the exact reason cannot be recovered offline. It would be false to infer
AX absence, WebKit failure or a specific label mismatch from the error alone.

A minimal evidence repair now logs only the root/attribute facts already read
when cleanup lookup fails, without any additional native call. It clears stale
root observations before the lookup and labels failures before a lookup as
unobserved. Three focused fixtures verify original exception preservation,
backend/library cleanup and no stale data presented as current. This changes
failure evidence only, not any action/acceptance boundary.

## Practical next method (subsequently selected for offline preparation)

**Selected offline approach: use an explicitly attended owner-foreground start, then a
read-only readiness/recovery gate before setup input.** Prebrief the owner to
bring only the exact new App window to the foreground when each incarnation
appears. Verify actual original App AXFrontmost, a distinct AX main mapped to
the retained WindowServer ID, absence of blocking modal, and the unique enabled
owned-menu Quit/AXPress route before proceeding. An owner report alone is not
focus or window-binding proof; retain actual observations and actor limits.

This removes dependence on an early background activateWithOptions request
instead of trying another flag or repeating it. The selected path must not
silently fall back to automatic activation if the read-only gate fails. It
requires a concrete source change and independent scrutiny before any live use;
this assessment does not implement or authorize that new action/handoff scope.
No product human-reading timeout or PR69 activation is proposed.

The normal-Quit recovery route must be established **at this startup stage**,
not first attempted after an activation failure. If actual AX/main/menu proof
is unavailable, stop before setup and immediately request owner normal Quit
of Chirality App v4(development gvpud8q). That attended fallback actually closed
both failed starts; it is not claimed to be an agent-accessible menu in the
missing-AX state. Do not weaken the distinct-main/modal checks to invent that
capability. Keep original custody and the existing exact exit/reap rules.

Account for both foreground handoffs/readiness observations, A setup/exit,
fresh admission and B readiness within the existing160s pre-Stop allowance;
retain135s at Stop entry and295s total. The current early2s and historical42s
activation times are not proposed waits or latency bounds. If the full method
cannot credibly fit after concrete implementation/fixture accounting, return
that timing conflict rather than launch another trial. Owner attention must be
freshly coordinated; no request to focus or launch is made now.

Classification: **unresolved early-startup activation-dispatch refusal, with a
separate missing AX observation**. Startup readiness and foreground policy are
hypotheses; the proposed owner-foreground/read-only recovery preflight is the
smallest practical method change that avoids relying on the failed request.

## Closure and retained evidence

Only A launched. No setup action, B, Stop, Cancel or LT23 followed. Owner reported
normal Quit; original Child77302 was observed CLD_EXITED/status0, exact admission-
bound administrative wait returned0, helpers settled, controllerrc1/slot2 ended
17:45:12UTC. Elapsed56.973087s, no overrun, known App/controller/slot/lockf absent
and run.77254 absent. File publication timestamps are retained separately from
exit observations; no exhaustive supplier settlement is inferred.

Private source evidence remains in j58087z7/A helper001 request/image,
helper002 request/focus trace/stderr, initial-window records, final result and
resource-closure-corroboration.json. The095 comparison uses its original helper003
trace/result and native_B_started record. All prior used preparations, state and
failures remain unchanged. This is DEL-09-02 diagnosis under the existing scope,
not new native qualification, release or signing evidence.
