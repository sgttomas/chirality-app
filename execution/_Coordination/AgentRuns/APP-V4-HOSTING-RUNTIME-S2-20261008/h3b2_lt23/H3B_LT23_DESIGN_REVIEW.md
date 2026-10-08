# LT23 bounded design/readiness review

Verdict: LT23 is a suitable next real implementation slice, but the proposed synchronous Stop-return path is NOT READY for code release without a concrete liveness refinement. No schema or reference-meaning blocker found. This is read-only design assessment at f25ba6887d85904ebef2a6321c222809d47cfabd, not implementation review or tested behavior.

## Required consequential choice: Stop completion must not wait for artifact IO

The proposal correctly keeps artifact work after input closure, grace/kill, EOF handling and actual LT23 emission and outside source/REC guards. That protects the process-ending critical path, but not Stop's return. Store publication performs namespace read-lock acquisition, selected-source resolution/hashing, copying, sync_all, rename and multiple readback scans. Bounded byte/member counts do not impose a wall-clock bound on those operations. Slow/stalled filesystem IO or exclusive namespace ownership can therefore leave the explicit Stop command pending after the process has stopped. Merely releasing locks does not close this new availability consequence.

The existing R2 source-owner rule explicitly protects Stop/EOF bookkeeping and forced termination from blocked metadata/writer paths; it does not claim arbitrary filesystem hard deadlines. Do not infer from that caveat that adding unbounded persistence to Stop return is accepted. Current stop_inner has finite process grace/EOF loops then best-effort recovery flush; the proposed new synchronous closure cost is a separate behavior needing a concrete decision.

Recommended refinement: after actual LT23, atomically capture an eligible native-held publication job/token and mark terminal evidence pending; return operational Stop success independently. One narrowly owned worker/task performs the existing complete Store checks, and installs success/unavailable only through the captured source token. Its pending/failure status must be native-held, bounded in number, non-retrying, and unable to block Stop, restart, mandatory replies or shutdown. Define job ownership/disposal and no-wait shutdown before code; a timeout around synchronous IO without controlling the leftover worker is insufficient. This is still the actual Host→Store→read slice, not a preparation-only layer. Alternatively, a synchronous choice requires an explicit accepted completion-latency policy and enforceable implementation limits; no such policy/bound is supplied here. This review does not select a new arbitrary numeric deadline.

## Accepted S1/RS mapping and ordering fence

Actual Stop source emits LT23 after cleanup with unchanged exitFacts, descendants and closedGeneration. Do not infer all descendants ended merely from stopped state: the event can honestly record survivors. The closed S1 envelope and current semantic reader allow same-H5 LT23 to reference unchanged pre-spawn observation; no terminal re-probe, renewed integrity, installed custody or phase rewrite follows. Restrict the producer to native actual LT23 after a successfully installed same-source LT09, and exact same observation/reference lineage. General JSON event callers cannot manufacture that eligibility. RS/source-owner concurrence must confirm this precise new producer support; keep source identity and Group B named adoption separate from canonical schemas.

Reserve the publication ordering token at actual event emission under Inner, not after IO. Capture attempt, full H5, actual lifecycle sequence, predecessor reference and exact event together. Both success and error installation must compare that token and current source eligibility. Mark an actual later terminal event even when LT09 is still pending: an ineligible stop must not let a late LT09 look like terminal success. Concurrent Stop, late LT09 success/error, restart, EOF and repeat Stop must neither regress selected receipt nor poison a newer source. Same attempt/H5 alone is insufficient. On failed terminal evidence, retain previous receipt internally but expose terminal unavailable; never label old LT09 as LT23. Stopped readback remains available through existing native reference/namespace/descriptor/closure guards.

Single-event fresh immutable closure is appropriate: preserve prior LT09 artifacts and original observation bytes, expose only the current successful reference, and explicitly disclaim public history index/discovery/restart hydration. Generalizing publish_lt09 should retain a closed supported-row set and exact event/ref/generation checks. Update producer-support/unsupported-row text and dependency identity coherently; do not change historical legacy bytes or silently repin B.

## Minimum discriminating evidence

Actual synthetic ready→Stop event equality and same observation bytes; graceful and forced termination, including honest surviving/unknown facts; native stopped read; original LT09 immutability; wrong event/sequence/H5/reference and tampered closure refusal. Block artifact IO deterministically after cleanup and prove Stop returns with truthful pending/unavailable evidence and no live-process/custody regression. Then release/fail IO and check exact token installation. Cover late LT09 success and error after terminal capture, restart during terminal publication, unsupported handshaking/pre-spawn stop, active namespace admission/rebind, substituted root, repeated Stop, and worker lifetime/shutdown if asynchronous. Existing descriptor-regression and namespace liveness controls remain required.

No code/build/tests/native supplier/download/MEMORY operations performed. Continuing independent delegated-harness-native TASK, software-code-review applied proportionately; no delegation. Parent retains release. Ready to recheck a concrete revised producer/liveness fence and RS concurrence rather than author implementation against the current unresolved synchronous choice.

## Exact read basis

Assessment SHA-256 eae4395d7495f5bb0980c6c3b91744f0f5a68cf12be82542b0147311fb773cfb. Source retrieved from exact Git objects; targeted Stop/schema/reader and accepted liveness passages inspected, earlier reader/store review retained.

- `projects/chirality-app-v4/app/src-tauri/src/hosting.rs`: `2952406eeab874252de18fe3a263bd77c6e70f808d91c6cefdf2df4e4ee1cf52`
- `projects/chirality-app-v4/app/src-tauri/src/distribution_store_s1.rs`: `e78664f9b422344f246099062c9247e484277095d8df2e570f247a02d469c8de`
- `projects/chirality-app-v4/app/src-tauri/src/distribution_s1.rs`: `408302b9942b1a2eec8e08ab8f81f28700d4e40f69a049dba08ede62f1198ad1`
- `projects/chirality-app-v4/app/src-tauri/resources/distribution-successor/lifecycle-event.s1.schema.json`: `e5713e88c720b2c4a2a1463923596e18b53302e3fae9195d433190ed098d0181`
- `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-GROUP-A-20261004/changes/CC-H-ATTACHMENT-PERSISTENCE-ALLOCATION.md`: `0c2c3bcc015249114124372f55ffe592b5eaa5b649735f5956ea69c167683e33`
