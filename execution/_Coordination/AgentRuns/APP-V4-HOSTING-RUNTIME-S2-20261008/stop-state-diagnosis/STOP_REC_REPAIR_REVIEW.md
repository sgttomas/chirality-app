# STOP-STATE-01 — REC repair source review

**CONCUR with part 1 and with part 2 subject to the precise first-capture refinements below. Part 3 remains a named source-contract treatment, not an implementation-ready row choice.** This is REC technical concurrence, not independent code review or implementation release.

TASK `/root/hosting_runtime_manager/attachment_namespace_owner` under WORKING_ITEMS `/root/hosting_runtime_manager`, parent HELP_HUMAN `/root`; harness-native read-only assignment, no delegation. Source basis `cd79d9b477f7f33aa4d7a3683e26e6337039d412`. Read the exact proposal and diagnostic report identified below, with prior source assessment carried forward. No code/contract edit, test, build, native action or new checkout. Only this report written.

## Evidence reading

D1 is deliberately seeded dispatch evidence, not proof of native reachability for every combination. D2 establishes the fresh legacy late-launch defect while the successor control refuses; both still misreport no-child Stop. D3 establishes that exit7 survives in actual LT12 but is lost by later Stop's journal-only lookup. D4 establishes that requests actually close while repeated close returns residual zero counts. These diagnostic passes establish observations, not successful repair. I read the manager's report and previously read verify-gate.log; I did not execute or independently rerun the instrumentation. No stale-PID wrong-process exploit is established.

## Part 1 — existing rows and admission

Shared attempt/state checks under the same Stop/source-gate final admission boundary, for both startup paths, preserve REC meaning and are concurred. Existing no-child LT20–22 must return without generation closure, signal/census, EOF wait or H5 allocation. Historical H5/PID is not current-attempt ownership. Late verification/handshake success or error must not mutate stopped or a newer attempt. Actual child admission winning the boundary must leave coherent ownership for the existing child-stop route. Preserve current counter history and actual request facts, never invent a generation to fit a lifecycle row. No reserved human choice is identified for these repairs.

## Part 2 — required first-capture definition

The proposed private receipt is appropriate, but “first exit/closure receipt” needs this exact distinction before coding: **the first closure result and the first observed process exit are different observations and may occur at different times**. Store a source-bound aggregate with independently once-set components, or an equivalent representation; do not freeze missing exit information forever merely because closure happened first. A Stop deadline can close custody before EOF yields an exit status. That source must retain the original unknown exit observation as unknown, and a later genuine EOF may be retained as a separate later observation; it must not silently rewrite the already-published Stop event. The producer must state which actual observation each emitted envelope used.

Bind receipt authority to the actual installed child's full H5 and owning spawn/start identity, acquired at installation. A retained prior generation during a new verification attempt must never become the new attempt's receipt. Do not derive ownership from the current mutable attempt number at late EOF capture or from a PID alone. No-child cancellation creates neither component and does not reuse a historical one as current.

At the existing source-serialized closure point, perform close_generation effects at most once for that actual source and capture its actual counts/cause together. Later EOF/Stop reads those first closure facts rather than calling close_generation again to obtain “totals.” Preserve REC's first loss cause, ended-unanswered state, acknowledgment limits and no-resend semantics. A later explicit Stop is a later action; it cannot change supplier-exit into supplier-stop. Zero newly ended entries on a repeat is not the original closure total.

Capture actual exit facts when observed for the same owning child; retain exact null/unknown values rather than inventing successful exit. Exact duplicate observations are idempotent. Conflicting repeats must preserve the first observation and a truthful conflict/limit; they must not overwrite it, sum counts, reinterpret a late completion, or substitute successor facts. The chosen conflict storage must remain bounded and cannot become a second transcript/history index. A first-capture receipt carries no new REC schema, hot capability or persisted replay authority.

For ordinary Stop where EOF already captured 1/1 counts and actual exit0, LT23 should use those exact captured facts rather than residual0/0. That is the D4 reporting repair. If Stop wins the closure point before exit is observed, record the real available facts and preserve uncertainty; do not wait indefinitely just to fill a receipt. This distinction needs a negative scheduling test, not only the two successful EOF-order controls.

## Part 3 — explicit Stop after LT12 constraints

No direct post-exit row is selected or accepted here. A concrete Host proposal must preserve three separate facts: earlier unexpected exit and its source cause/counts; later person's explicit Stop/cleanup request; any actual handling or observation of surviving **owned** descendants. A known reaped parent is not proof that its process group is empty. Conversely, no owned surviving descendant may be invented to justify a tree-ending row. A cached numeric PID is insufficient renewed authority over a potentially reused group.

With genuinely established no remaining owned child/tree, record the person's requested transition using the separately agreed source mapping without creating another process exit, REC closure, descendant census or acknowledgment. With proven owned survivors, use only the already warranted explicit Stop handling and retain its actual outcomes separately from prior parent exit. Unknown ownership cannot become “none surviving” or permission to signal an unrelated group. The named proposal must state its refusal/unavailable consequences while preserving the broad accepted Stop/restart affordance; neither automatic survivor handling nor automatic restart is selected by this review.

An eventual terminal representation may carry original closure facts with clear provenance, but cannot pretend those counts were newly caused by later cleanup. Do not reopen closed journals to reconstruct authority or rewrite LT12 into deliberate termination. Existing immutable LT12 receipt remains historical; explicit later actions must preserve publication sequencing/original LT09 capability and cannot let stale completion overwrite them. Changing canonical transition rows/reader or exporter acceptance requires named provenance and consumer adoption; a valid isolated LT23 is not proof of a valid complete trace.

## Required refinements and return

Before part 2 implementation release, put the independent closure/exit capture points, owning child identity, late-EOF-after-Stop handling and duplicate/conflict behavior into the bounded implementation fence. These are technical clarifications within preserved REC semantics, not a new human gate. Retain exact original D2/D4 regression vectors and add Stop-deadline-before-EOF, repeated EOF after source reaping, prior-H5/new-attempt, conflicting duplicate and successor races. Confirm no duplicated REC effect, unchanged first cause/counts, actual unknown exit preserved, and no-child omission of generation-required facts. Preserve terminal worker liveness and no Store IO under lifecycle locks.

No new reserved human choice is identified in parts 1–2 with these refinements. Part 3's source row and descendant-ownership treatment remain for Host/parent; only a consequence that changes a reserved policy or accepted scope would require the corresponding human decision. This review does not silently choose that consequence. Existing merged LT12 work and its stated limitations remain intact.

## Input hashes

- `/private/tmp/STOP_REPAIR_PROPOSAL.md` — `8675c10d2e669f992b327bea292982fd050fc372882c73ede63a8efbb670c4c8`
- `/private/tmp/hosting-stop-diagnosis/REPORT.md` — `be374152c5eaf6957439763899935c985f4dbbe795e8f523ba6fabe3f49e6381`
- `/private/tmp/STOP_REC_SOURCE_ASSESSMENT.md` — `4d85a3ffe78274cc70699c330afa234104039a3607d40985e04b08145b37b01b`

## Revised two-part package — exact backcheck

Read revised `/private/tmp/STOP_REPAIR_PROPOSAL.md`, SHA-256 `0b7e1b906e5c354ed0823b86f356548c784c9704924bec3366a52d1e2e05a971`. **CONCUR for parent assessment, not code release.** Earlier preliminary review remains preserved; its part numbers refer to the earlier three-step version. The revised Part1 now includes admission/no-child corrections and independently once-set first closure/exit components; revised Part2 contains the unselected post-exit alternatives.

The revision incorporates the requested REC constraints: installed-child H5/owning identity; separate closure and exit capture; first cause/counts/effect standing retained; no persistence guarantee or replay; deadline-before-EOF uncertainty and immutable earlier events; idempotent duplicates and bounded conflict marker; no-child creates neither component; no historical-source borrowing. These resolve the specific source-contract refinements identified in the preceding review. Exact implementation ownership/locking and failure protocol still need their bounded review and original-vector backchecks.

The A/B/C comparison properly distinguishes completing the existing failure/restart route from a new direct cleanup amendment and from an availability-reducing refusal. REC concurrence does not select any route, allocate LT25, waive automatic-restart obligations or settle descendant overlap. A must preserve original closure facts/no resend while implementing real source-owned failure/restart behavior. B must retain earlier unexpected exit separately from later owned cleanup and must not attribute descendant force to the already-exited child; any new typed fields or transition require named consumer adoption. C cannot be represented as complete recovery. The remaining U16/descendant standing and selected policy consequences stay with the parent and owning source review.

No additional reserved human act is identified merely by the revised Part1 engineering scope. Parent must assess actual chosen Part2 consequences against accepted policy; the comparison itself grants no implementation, native, qualification or canonical-change authority. No tests or other files were changed in this backcheck.
