# STOP-STATE-01 diagnostic repair proposal — not released

Basis cd79d9b477f7f33aa4d7a3683e26e6337039d412, after merged #1156. WORKING_ITEMS hosting runtime manager; software-defect-diagnosis selected. This proposal does not alter source or accepted contracts. The author packet /private/tmp/hosting-stop-diagnosis preserves temporary instrumentation, four diagnostic tests, observations and exact restoration; Host/RS and REC read-only assessments are separately supplied.

## Confirmed diagnosis

D1: verifying/restart-waiting/halted no-child Stop emits LT19 then LT23, waits about3 seconds and claims a checked empty descendant outcome. Existing HOSTING4.7 requires LT20/21/22 directly to stopped. The seeded state matrix demonstrates dispatch, not native reachability of every combination.

D2: actual fresh legacy verification was held behind an explicit invented version-probe gate. Stop returned stopped before release; releasing the gate produced ready with an owned invented child. The same successor schedule refused stale start and stayed stopped. Legacy lacks the successor route's final attempt/state gate. This is a whole-product lifecycle blocker, not fixed by relabeling events.

D3: actual unexpected exit7 is retained in LT12; later Stop waits for a stopping-only journal entry and emits unknown exit facts. D4: ordinary Stop with one unanswered client request and one outstanding supplier request closes both, but LT23 emits counts0/0 because on_eof discards its first1/1 closure counts and Stop repeats closure. These are reporting defects; actual REC closure is not shown missing.

Retained old H5/PID during subsequent verifying is a source-traced identity hazard, not a reproduced wrong-process signal. No unrelated PID was seeded or signalled.

## Recommended bounded sequence

1. **Admission and existing no-child rows first.** Prepare a precise implementation fence in hosting.rs/start/stop and maintained tests. Replace wildcard state dispatch with explicit accepted cases. For verifying/restart-waiting/halted, require actual current-attempt no-child ownership, record existing LT20/21/22 with actor/stop record, revoke pending start/restart admission, and return without process signalling, EOF wait, close_generation, new H5, descendant assertion or fabricated LT23. Unknown state refuses before mutation; duplicate stopping remains single-owner refusal. Child-ready/handshaking/spawning routes retain actual owned-child custody and existing row guards.

   Both legacy and successor paths must bind attempt/state through post-verification publication and actual spawn installation under the same Stop/source serialization boundary. No unlocked check followed by spawn, no late verification-failure/handshake result overwriting stopped or a newer attempt. Preserve lock order and keep probe/scanner/Store IO outside the short source critical section. Historical generation/PID is not current-attempt authority. A no-child assertion must be derived from explicit owned-child/attempt state, not just a cached PID/state string. If a real owned-child inconsistency appears, fail closed with truthful unavailable/diagnostic state rather than falsely recording a no-child row or killing an unowned group.

   This step does not select a new post-exit Stop row, implement automatic restart, or change survivor policy. The currently invalid exited-unexpectedly Stop path remains a named held residual until step3; no full Stop-conformance claim. It must not be silently converted to refusal, since that would withdraw the accepted broad Stop affordance and also strand current Stop-then-start recovery.

2. **First-observation custody for legitimate child Stop.** Separately review a private source-bound first exit/closure receipt with REC. Capture actual H5, owning attempt, observed exit facts and first closure counts once at the existing closure point; repeated EOF/Stop must neither repeat closure effects nor replace known facts with residual zeros. Define first-capture and conflicting/repeated-observation behavior, preserve original REC cause/no-resend and unknown facts. Stop may use those exact original facts for a legitimate child-stop envelope; it must distinguish earlier unexpected exit from later explicit cleanup. Keep terminal worker admission/liveness and same-H5 original LT09 capability intact. This does not authorize cold restart hydration or serialized capability restoration.

3. **Named source treatment for Stop after unexpected exit.** HOSTING4.6 broadly admits Stop, but4.7 supplies only LT13/14 exit-recorded follow-ons, not a direct stop-requested row. Do not invent LT19 semantics or pretend a valid isolated LT23 validates the trace. Recommend a concrete narrow technical proposal preserving the person's existing Stop and separate earlier exit cause, with exact no-child versus surviving-owned-descendant behavior, before implementation of that case. Alternative is to implement the actual LT13/14 failure/restart route, substantially broader. Interim refusal changes availability and is not selected here. A direct-row amendment requires versioned table/schema provenance and owning consumer adoption; historical rows/evidence remain unchanged.

## Regression acceptance before repair readiness

- Run the exact D2 held-probe schedule unchanged on both routes: Stop completes before release, late start returns stale/refused, no child and no later state/event/verification mutation. Add actual spawn and handshake barrier races and concurrent newer attempt.
- All existing entry states, exact accepted tuples, wrong no-child guard and unknown-state refusal. Fresh and prior-generation verifying cases must show no signalling of historical/unowned process, no invented generation/exit/closure/census, and no EOF wait on direct no-child rows. Use owned harmless processes or a signal-observation seam, never an arbitrary PID.
- Actual Stop-first and EOF-first with1/1 pending closures, first facts/counts immutable, repeated EOF/Stop no duplicate effect, zero/nonzero/unknown exit facts, full foreign home/session/H5 rejection. No change to first execution-loss cause, ended-unanswered, acknowledgment or no-resend semantics.
- Preserve prior LT12/LT23 worker busy/error/panic/closing/stale-generation/lateLT09 and original-predecessor controls; no Store IO under operational locks. Test both feature states. Validate each emitted transition and relevant actual trace sequence; present readers validate individual tuples, not universal whole-trace conformance.
- After source freeze, exact independent review, fresh committed/recompiled existing receiving cohorts and named B adoption. A new row/envelope needs a separate contract/reader/export decision; existing v1 formats must not silently expand.

## Authority and limits

Host/RS and REC source-owner assessments concur that shared admission revocation and existing no-child LT20–22 correction preserve accepted meaning. No new human-reserved choice is identified for those engineering repairs. Implementation is still not released by this diagnosis. Exact child-ownership and first-capture protocol needs bounded design review before coding.

The post-exit row gap requires a named technical source decision. A new human decision is required only if its chosen consequences change a reserved policy (automatic survivor termination, restart/confirmation, replay, authority or accepted scope); no such policy is selected or requested here. Preserve the existing U05/U16 ownership limits rather than treating uncertainty as blanket approval need.

#1156 remains a valid bounded LT12 contribution with its historical stated limits; this diagnosis does not retrofit closure. No S3/native/supplier/download/credential/SEAL2/hydration work or qualification follows. No production/contract changes; diagnosis instrumentation removed.
