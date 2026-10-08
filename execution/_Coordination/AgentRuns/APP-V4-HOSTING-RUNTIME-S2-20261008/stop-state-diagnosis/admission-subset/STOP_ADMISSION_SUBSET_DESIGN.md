# STOP-ADMISSION-01 — narrow proposed safe subset, source review required

Basis cd79d9b477f7f33aa4d7a3683e26e6337039d412. Supersedes the broader Part1 implementation selection for this next increment only; STOP_PART1_DESIGN remains a held proposal. Parent selects the reproduced verifying Stop→late-ready correction plus exact current-attempt LT20 cancellation. All process signalling/reaping/cleanup redesign, LT23 exit/count repair, LT21/22 correction, post-LT12 mapping and Part2 restart work remain held. No full Stop conformance or proof of process-group ownership is claimed. No code, build or further process research in this revision.

## Bounded state and source fence

Production fence: hosting.rs admission/start/Stop and scoped post-start settlement only. Tests in a small Host/successor test module plus documentation. No InstalledSource abstraction, Child extraction/wait rewrite, REC source/schema, Store/reader/schema, lib/UI, Group B or canonical changes.

Add a private current-start admission record in Inner: checked immutable attempt number and `NotSpawned / Installed(full H5)` marker. It is not a process capability or descendant census. Set NotSpawned only when an existing accepted start state transitions to verifying; record Installed only after actual successful spawn/H5 publication for that same attempt. All transitions of this record occur under attachment_gate→Inner. A failed local spawn remains uninstalled. Clear/revoke the current admission on direct LT20; do not clear historical child, generation, PID, journal, exit facts or REC custody merely to make this marker true.

The marker is trustworthy for the narrow question “has this attempt installed a child?” because BOTH start routes must own the same attachment gate from final admission check through spawn/custody publication. Stop cannot run in the spawned-but-unpublished interval. Historical Inner.generation/child_pid/self.child are not evidence of a current-attempt spawn and are not used by the LT20 branch. Conversely a missing marker, mismatched attempt or Installed marker while state says verifying is an inconsistent condition: refuse before mutation. Never infer NotSpawned from a missing PID alone.

## Initial and final start boundaries

Initial start admission takes attachment_gate then Inner, validates existing absent/stopped/refused states, computes checked next attempt before mutation, installs its NotSpawned admission and records existing LT01/02/03. Release locks before probe, inventory, Store or other preparation IO. No new accepted start states.

After verification and final successor audit, acquire the existing REC writer then attachment gate for BOTH routes, then Inner. Retain successor try-lock behavior; legacy may retain existing writer wait but must check source after waiting. Require exact captured attempt, admission NotSpawned and verifying state before any shared verification/status/identity/lifecycle write. Successor also keeps its exact prospective tuple/counter and App-end checks. Do not perform a check, release gate and then spawn. Hold writer+attachment gate through spawn and successful custody/H5/LT06 publication. Mark Installed for the captured attempt atomically with that existing publication. No early H5 allocation, counter reset/rollback, probe/hash/Store IO under the gate, or new spawn cleanup semantics.

Route every preparation error/refusal through a scoped check: if the attempt was cancelled/superseded or is no longer verifying, return stale/cancelled without LT05 or any verification/identity mutation. This applies to legacy verification failure as well as success, successor preparation/Store/audit errors, writer/gate admission failures, counter/session checks and spawn-result mutation. A local spawn failure can emit the existing failure row only while the held gate still proves its attempt. Existing local allocation-failure cleanup is unchanged and remains a separately held ownership concern; this subset does not claim to repair it.

## LT20 only: cancellation without touching historical processes

In stop_inner, under attachment_gate→Inner and after existing scoped-target validation, add one explicit verifying branch. Require current admission matching start_attempt and NotSpawned. Compute checked revocation before mutation; invalidate the attempt (advance checked attempt plus remove its pending admission, or equivalent exact monotonic token revocation). Record actual actor/stop record and existing LT20 verifying/stop-requested/stopped. Advance/clear only in-flight successor publication state belonging to this cancelled attempt so late results cannot install. Return stopped directly after releasing locks.

This branch does not close stdin, inspect/signal/probe any PID/group, wait for EOF, call close_generation, allocate H5, emit LT23, create closure/exit observations or assert descendants checked/none surviving. It does not consult a retained prior generation to authorize action. The legacy shape may retain historical generation metadata; that is not a new live H5 or a closure claim. No terminal artifact is invented for LT20 in this slice.

Scope is cancellation of the CURRENT verifying attempt. It does not establish that a prior generation has no surviving descendants, discharge prior cleanup, or authorize new overlap. Existing accepted start/descendant-policy limitations remain explicit; the correction prevents cancellation itself from signalling an old numeric PID. No auto-restart/survivor policy is added. Other stop_inner state branches remain unchanged and retain their known defects/availability, rather than silently implementing LT21/22 or changing post-LT12 behavior.

## Later start barriers and source writes

The final gate fixes the reproduced pre-spawn resurrection but is not permission for late handshake settlement to mutate a stopped/new source. Apply the existing successor generation+attempt+handshaking checks to legacy post-spawn settlement, preserving route-specific output and verification semantics. Before declared capabilities, response identity, held-frame delivery and LT09/LT11 mutations, require captured attempt, admission Installed with exact captured H5, current H5 and handshaking state under attachment_gate→Inner. A stale success/error/contradiction returns without mutation. Native initialize/initialized dispatch uses existing scoped-generation request/write entry points; each write keeps its existing final source/pipe check, not a stale prior check.

No response wait under source gate. Do not acquire frame_write while holding source gate: dispatch retains existing frame_write→source gate→Inner order. Failure handling must check captured source under the gate before reaching the existing signalling/closure path, so a stale failure cannot target a later source. This is admission suppression of stale work, not a new signal/reap proof: do not change which signal, grace, wait, reap, PID/group mechanism or closure summary the still-current failure path uses. If preserving this fence requires a new process-ownership mechanism, stop and return that exact call site instead of broadening the subset.

After admission publication, readers continue their current captured-H5 behavior. This subset does not add a new child token, historical index or change on_eof. Existing successor LT09 artifact installation retains its controller/attempt/H5/sequence/closing checks outside operational locks. Legacy does not gain successor artifacts.

## Lock table

| Operation | Order and boundary |
|---|---|
| Initial accepted start | attachment_gate → Inner; release before all preparation IO |
| Final admission/custody publication | REC writer → attachment_gate → Inner; no release of gate between check and spawn/install |
| LT20 cancellation | attachment_gate → Inner; no Child/stdin/group/REC-writer/Store access |
| Post-spawn state settlement | attachment_gate → Inner; response wait and artifact IO outside |
| Native writes | existing frame_write → source-file lock where applicable → attachment_gate → Inner |
| Successor artifact installation | existing controller → Inner; no operational gate/Store inversion |

No new global lock, blocking Child lock, worker, queue, deadline or automatic retry. Legacy version probe may continue until it returns; the promise is irrevocable launch/state admission cancellation, not probe-process cancellation. Initial and final attempt increment overflow refuse before mutation.

## Exact discriminatory tests after release

1. Original D2 fixture unchanged: block actual invented --version; assert verifying/current attempt uninstalled; real Stop returns LT20/stopped BEFORE release; release probe; both legacy and successor return stale/cancelled with no child or later event/verification mutation. Repeat with failed version probe and successor preparation failure.
2. Fresh and prior-generation verifying cancellation. Retain historical H5/PID metadata and use an inert signal observation seam; assert no signal/group probe/stdin close/EOF wait/closure call/counter allocation. No arbitrary live PID. LT20 has no exit/count/descendant fields and no LT23 artifact. This demonstrates current-attempt cancellation, not prior-tree extinction.
3. Final gate race both routes: Stop wins before final gate → no spawn; start wins and publishes custody → Stop sees handshaking/ready installed child on existing route. Pause after final check to prove Stop cannot complete across an unlocked spawn window. Preserve original H5 counter and child cleanup controls.
4. Cancelled attempt then newer explicit attempt: release old successful/failed verification; no mutation of new source. Checked attempt exhaustion and inconsistent verifying/Installed marker refuse before mutation.
5. Actual delayed handshake success/error/contradiction against Stop and newer start on both routes; no late LT09/LT11/identity/held-frame mutation or stale failure signalling. Existing same-source handshake behavior stays intact. Test scoped initialize/initialized writes with source replacement.
6. Affected existing successor/legacy admission, LT12/LT23 publication, root/namespace and connector coexistence controls in both feature states, without claiming known other Stop defects repaired. Independent exact-source review and B fresh cohorts/pin adoption after commit remain required.

## Held findings and concrete release limit

D1 for restart-waiting/halted, D3 missing exit facts, D4 discarded first counts, post-LT12 invalid row, numeric group reuse after reap, allocation-failure cleanup and restart completeness remain held. No LT23/stopped/no-survivor claim is newly justified by a deadline in this subset; existing defective branches are not certified. Primary-source process-lifetime research does not release broader cleanup. Parent must separately settle the exclusive wait/reap/signal mechanism and its availability consequences before that repair. This subset is review requested, not self-accepted or code-authorized.
