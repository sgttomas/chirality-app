# Stop diagnosis — no repair

Exact basis `cd79d9b477f7f33aa4d7a3683e26e6337039d412`, existing author checkout `/Users/ryan/.codex/worktrees/hosting-lt23/chirality`, branch `codex/hosting-stop-diagnosis`. Prior merged LT12 staged work preserved in stash `preserved-merged-lt12-before-stop-diagnosis`. The diagnosis skill and exact source origins are hashed in ORIGINS.json. All temporary cfg(test) instrumentation was removed; RESTORATION.json confirms original hashes and clean Git status. No production/contract edits or repair, new checkout/target, downloads, supplier/native App execution, credentials, qualification, or MEMORY.

## Reproduced findings

### D1 — no-child Stop uses the wrong transition and fabricated terminal path

The temporary seeded matrix calls the real stop_inner with no child/PID, null generation, and a named entry state. It establishes branch behavior, **not that all seeded combinations are natively reachable**.

| Entry | Observed result | Time | Tuple result |
|---|---|---:|---|
| absent / refused / stopped / stopping | rejected, no lifecycle rows | 0 ms | expected rejection / duplicate Stop rejection |
| ready | LT17 then LT23 | 3004 ms | tuple matches, but deliberately impossible seeded no-child readiness is not a valid operational witness |
| handshaking | LT18 then LT23 | 3095 ms | same seeded limit |
| spawning | LT19 then LT23 | 3077 ms | row tuple matches; no child guard exercised |
| verifying | LT19 then LT23 | 3001 ms | LT19 from-state mismatch; expected LT20 no-child direct stopped |
| restart-waiting | LT19 then LT23 | 3005 ms | LT19 mismatch; expected LT21 no-child direct stopped |
| halted-after-repeated-failure | LT19 then LT23 | 3014 ms | LT19 mismatch; expected LT22 no-child direct stopped |
| exited-unexpectedly | LT19 then LT23 | 3004 ms | LT19 mismatch; no existing direct Stop row in table |

These no-child accepted cases still wait for an exit journal fact, call close_generation, and emit LT23 with zero closed counts, null exit code/signal and `descendants.checked=true, surviving=0, handling=none surviving`. The empty journal and null generation are retained in OBSERVATIONS.json. This is not evidence that a tree was inspected. HOSTING §4.7 says LT20/21/22 are direct stopped transitions under no-child guards. The earliest divergence is stop_inner's wildcard `_ => LT-19`, coupled to one unconditional child-cleanup/EOF-wait/closure path rather than explicit no-child dispatch. LT19 is declared only for spawning.

### D2 — actual legacy Stop during verification can return stopped then launch

`verify-gate.log` uses a **fresh** Host with no prior H5/PID. The invented Python `--version` process signals entered and waits for an explicit fixture file. Test order is strict: await entered; assert verifying/no child; call Stop to completion; retain atStop snapshot; only then write release; join start. No timing race is inferred from sleeps.

- Legacy `cfg.distribution=None`: Stop returned `Ok(stopped)` after 3071 ms while probe remained blocked. After release, start returned Ok with state ready and child present. Its actual rows include LT19 verifying→stopping, LT23 stopped, then a late development-start transition and spawn/handshake. The test then called real Stop successfully to clean up the invented late child.
- Successor `cfg.distribution=Some(...)`: same schedule, Stop returned stopped after 3097 ms; release produced `stale start attempt; prospective generation or start attempt changed; no spawn`. Final state stopped, no child.

Earliest causal omission: start captures attempt before verification, but the final attempt/state/prospective check and attachment gate apply only when prepared/prospective are Some. The legacy verify return proceeds through the writer into verification-result mutation and spawn with no equivalent cancellation check. The App writer does not serialize Stop, so it cannot supply this missing source boundary. This is a reproduced late-launch defect, separate from incorrect Stop row selection. It is not evidence that successor has the same race. No unrelated or recycled PID was signalled in this control.

### D3 — actual EOF-first exit facts are lost by later Stop lookup

Actual invented-child controls exercise both orderings:

- Stop first: LT17 then stopping EOF journals exit facts; LT23 retains actual exitCode=0. Initial no-outstanding-request control completed in 60 ms.
- EOF first: child exits7 with no Stop, actual LT12 records exitCode=7. Later explicit Stop emits invalid-from-state LT19, waits for a journal fact that ready EOF did not append, then LT23 records exitCode=null/signal=null after 3008 ms (3002 ms in the nonzero-count variant).

Source cause: on_eof's ready branch stores facts only in LT12, while stop_inner only searches `journal.class == exit`; that journal entry is created in the stopping branch. The earlier actual fact is not absent from the source history, only absent from Stop's lookup. Do not repair by rewriting LT12, assuming success, or silently declaring its unexpected ending deliberate.

### D4 — ordinary Stop discards first actual closure totals

`closure-counts.log` adds one actual invented client request left unanswered and one actual supplier request left outstanding before either ending. The real protocol path records final client `unknown-no-response` and server `ended-unanswered` states.

- Stop first: on_eof closes both; actual LT23 reports `{unknownNoResponse:0, endedUnanswered:0}` despite those observed closures. ExitCode remains0; Stop took60 ms.
- EOF first: actual LT12 reports `{unknownNoResponse:1, endedUnanswered:1}` with exitCode7; subsequent Stop LT23 reports zero/zero and unknown exit facts.

Earliest divergence for ordinary Stop: on_eof calls close_generation and obtains the counts, then the stopping branch journals only exitFacts and discards counts. Stop calls close_generation again; pending registers have already been drained/closed, so it receives residual zeros. This is a closure-summary defect, not evidence of missing actual request closure or permission to repeat closure effects. REC facts and states remain primary. No totals were manufactured by instrumentation.

## Read-only retained-generation/PID concern

start clears successor references/status and version fields but leaves `i.generation` and `i.child_pid` until the actual spawn/custody assignment. A restarted Host can therefore be verifying with the previous generation/PID still present. stop_inner captures those fields and uses killpg/group_alive, journal lookup and close_generation without first distinguishing prospective no-child cancellation from prior-generation history. This is source-traced exposure, **not a reproduced stale-PID signalling exploit**. No arbitrary/live unrelated PID was seeded or signalled. A later regression should use genuine owned process handles/barriers or a harmless signal-observation seam, never an arbitrary PID. Whether a prior group still owns descendants must not be inferred solely from state or a cached numeric PID.

## Confidence, limits and repair choices

D1 branch mismatch, D2 late launch, D3 fact lookup loss and D4 residual-count loss are high-confidence reproduced source behavior. Seeded no-child states are deliberately labelled; restart-waiting/halted reachability and automatic restart policy were not implemented or tested. The actual verifying, ready Stop and exited-unexpectedly schedules are separate native Host executions against invented binaries. Passing diagnostic tests mean observations were collected, not product conformance.

Small bounded implementation corrections can explicitly dispatch existing rows and guard current child ownership, invalidate in-flight start and recheck attempt/state under the same spawn/Stop source gate on **both routes**, and retain the first source-bound exit/closure observation for later legitimate Stop reporting. Such retention needs REC concurrence on capture-once/conflicting-repeat semantics; do not duplicate close_generation side effects or reinterpret zero residuals as totals. No-child LT20–22 must not manufacture H5, exit, descendants or generation closure.

The exited-unexpectedly direct Stop case remains a **contract gap**. Existing options are to reject it pending proper exit-recorded LT13/14 processing (availability consequence: direct start also rejects), actually implement those broader restart/failure/descendant rules, or seek a named direct post-exit cleanup transition treatment. Do not rename LT19 or claim a full trace is valid. No option is selected here.

Affected surfaces: Host Stop/start/quit/restart, REC summaries, existing LT12/LT23 publication sequence and source references, established Runtime/native display, and Group B exact-source/row receipts. Any repair changes pinned producer sources and requires fresh receiving evidence; no downstream files were changed.

## Later regression checks required

- Explicit full state dispatch and actual no-child guards; no fabricated LT23/counts/descendant facts or needless EOF wait for LT20–22.
- Deterministic blocked version probe Stop-before-release on both routes, plus spawning/handshake boundary scheduling and refusal of late mutation/spawn.
- Genuine prior-generation handle/history during a new verification attempt; safe no-unrelated-signal proof; source replacement and repeated Stop/EOF.
- Both actual EOF/Stop orderings with nonzero client/server closures, capture-once exit/count preservation, unchanged REC effect/cause/no-resend semantics, unknown facts retained honestly.
- The separately selected treatment for post-LT12 Stop, with exact transition and consumer consequences.
- Existing terminal worker liveness/sequence/closing and same-H5 predecessor controls; fresh source receipts after any implementation change.

## Execution/evidence

Default only, bounded requested scope. Existing offline cache/target, CARGO_INCREMENTAL=0 and CHIRALITY_SKIP_CODEX=1. `diagnostic.log`: 2 diagnostic tests passed (initial state matrix and actual orderings). `verify-gate.log`: 1 test passed (two route cases). `closure-counts.log`: 1 test passed (two actual orderings with outstanding requests). No broad suite or production-feature claim. Temporary module and include patch are preserved as FINAL_INSTRUMENTATION.rs/INSTRUMENTATION.patch; initial log precedes the added gate/count variants. All raw STOP_DIAG observations are extracted losslessly into OBSERVATIONS.json. The production hosting.rs bytes were never edited. Shared target released after final test and exact source restoration.
