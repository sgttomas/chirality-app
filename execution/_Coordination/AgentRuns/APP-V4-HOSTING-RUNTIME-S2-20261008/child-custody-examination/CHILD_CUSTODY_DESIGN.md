# Child custody Step 1 — source-only design for review

Basis: `bf795b99d1f7093178b41ca93e638450eca2d8e0` (merged PR 1158). Status: conditional protocol and concrete availability decision; **not implementation-ready and not permission to run process probes**. No product bytes, contracts, builds, processes or signals were changed/executed for this assessment. The existing author checkout and all earlier evidence remain preserved. Step 2 first closure/exit summaries, Step 3 restart, and Step 4 receiving are excluded.

## Recommendation and unresolved decision

Use one private, source-owned Child custody cell for every actual child, including unpublished launch failures and successor label probes. Serialize observation, signals and final reap within that cell; a generation/attempt token alone is never OS authority. Prefer nonreaping exit observation only on an independently accepted macOS support basis. The evidence below supports a candidate mechanism, but does not yet establish the mechanism on the running kernel or a complete descendant census.

Do not release a production implementation on the claim that a mutex or retained Child alone solves Stop. There are three independent obligations: (a) prevent targeting a recycled group; (b) establish which descendants remain; (c) choose the irreversible final reap point. This proposal supplies an exact conditional protocol for (a), preserves uncertainty for (b), and exposes the availability cost of (c).

Recommended next decision: authorize only the described isolated synthetic mechanism examination after independent design review, while production reliance remains unavailable. To enable production thereafter, accept a platform-support basis and an explicit cleanup completion method. If these cannot be supplied, choose protective unavailability: refuse fresh spawning before creating a child; for an already-created source retain cleanup responsibility, emit no fabricated LT23/stopped/census, and deny replacement/restart. That is a material availability change requiring parent/source-owner disposition, not an implementation detail silently selected here. The current code remains unchanged meanwhile.

## Current platform evidence and limits

Read-only host metadata: macOS 26.6.2, build 25G83; Darwin 25.6.0; kernel build `xnu-12377.161.14~5/RELEASE_ARM64_T8122`. No hostname or process inventory was collected.

* Local CommandLineTools SDK `sys/wait.h` declares waitid and WNOWAIT; WNOWAIT is documented in the header as leaving the process waitable. This establishes compilation availability only. SDK man page `wait.2` documents waitpid/WNOHANG, not the required nonreaping contract.
* [Apple wait documentation](https://developer.apple.com/library/archive/documentation/System/Conceptual/ManPages_iPhoneOS/man2/wait.2.html) describes consuming child status; [Rust Child documentation](https://doc.rust-lang.org/std/process/struct.Child.html) expressly says try_wait reaps a terminated Unix child. Therefore neither try_wait nor wait is an observation-only replacement.
* Pinned Apple OSS release [xnu-12377.121.6, commit ac9718fb1af618d5ce8678d0dc6e8a58f252216f](https://github.com/apple-oss-distributions/xnu/commit/ac9718fb1af618d5ce8678d0dc6e8a58f252216f), [kern_exit.c](https://raw.githubusercontent.com/apple-oss-distributions/xnu/ac9718fb1af618d5ce8678d0dc6e8a58f252216f/bsd/kern/kern_exit.c): waitid skips reap_child_locked under WNOWAIT (tag lines 3149–3154); reap removes group membership and process hash (2737 onward). WNOHANG's no-event path may leave output untouched (3244 onward); zero-initialize siginfo before each call. The same source has a wait-collision sleep before the no-event path, so WNOHANG is not an unconditional wall-clock bound under foreign concurrent waiters. This release is **not** the running 12377.161.14 kernel. No exact matching published source or current Apple support guarantee was established in this assessment. Mutable main was discovery only, not the pinned proof basis.
* [POSIX definitions](https://pubs.opengroup.org/onlinepubs/9799919799/basedefs/V1_chap03.html) distinguish process lifetime, zombies and group lifetime; [identifier reuse](https://pubs.opengroup.org/onlinepubs/9799919799/basedefs/V1_chap04.html) constrains reuse while the corresponding lifetime continues. These are normative concepts, not evidence that the running macOS binary meets this particular custody argument. Direct Open Group retrieval was intermittently unavailable; indexed primary-source extracts were also consulted.
* [Apple killpg](https://developer.apple.com/library/archive/documentation/System/Conceptual/ManPages_iPhoneOS/man2/killpg.2.html) targets a numeric group. Signal zero is a point observation, not a group handle or descendant count. [Apple sigaction](https://developer.apple.com/library/archive/documentation/System/Conceptual/ManPages_iPhoneOS/man2/sigaction.2.html) documents SA_NOCLDWAIT suppressing zombies. A momentary disposition check does not exclude a concurrent library changing it.

Proof prerequisites, all required before group signalling: accepted platform behavior; no automatic child reaping; exclusive control of every wait/reap of this child; source-created group association; retained child lifetime through the actual signal syscall; and warranted continuity of that group identity. Merely querying getpgid or killpg(0), comparing a numeric PID, having a Rust Arc, or passing one synthetic test does not discharge these prerequisites. Group migration/escape and same-session membership changes must remain outside any whole-descendant claim. This proposal makes no retained-zombie PGID proof for the current machine.

## Existing calls that must be covered together

All paths are in `projects/chirality-app-v4/app/src-tauri/src/`, at the basis above.

| Callsite | Existing risk / exact proposed fence |
|---|---|
| hosting.rs start, approximately 1035–1085 | process_group(0), local child cleanup, self.child installation, H5 allocation. Construct private custody immediately after spawn and before any fallible handoff. Publish its native identity with H5/attempt under the existing final admission gate. No plain Child alias escapes. An unpublished failed allocation retains the same custody responsibility, not a fabricated H5. |
| hosting.rs successor_handshake_failed, 1138 onward | Numeric killpg while source gate/Inner held. Capture source-scoped cleanup authorization there; perform owner operation only after releasing global/source locks; re-enter to settle only the same attempt/H5. Never signal a newer slot by looking up child_pid later. |
| hosting.rs on_eof, 2195 onward | Currently holds child mutex through blocking wait. Replace only the process observation segment with custody observation; no wait/reap under Inner or attachment gate. Preserve REC ordering and actual lifecycle-event ownership; do not repair first-summary loss in Step 1. |
| hosting.rs kill_group/group_alive, 2234–2245; stop_inner, 2301 onward | Remove all unowned numeric action entry points. Capture immutable source custody when Stop is accepted, release source gate before OS operations. LT20 remains process-action-free. Existence checks also require the owner protocol. Existing LT23 completion logic cannot remain a success fallback when cleanup is unavailable. |
| hosting_successor.rs terminate/probe, 168–270 | Already uses waitid/WNOWAIT, then unconditional group kill/Child kill/wait, including observation-error paths. Apply the same support/error/owner protocol; an ECHILD/unsupported observation must never flow into numeric terminate. Local probe custody is not a Host generation. |
| lib.rs Exit, 1292–1296 | Currently calls Stop and ignores errors. Closing must prevent new admissions; unresolved cleanup must not become a successful cleanup claim. Do not add a blocking shutdown join. Changing App exit prevention/owner recovery policy needs explicit disposition beyond this source protocol. |

The legacy version probe and any library-owned child APIs must be inventoried during implementation review before claiming all-child coverage. The bounded proposed module is hosting_child_custody.rs, hosted privately by hosting.rs and hosting_successor.rs, plus narrow tests and module inclusion. No REC schema, lifecycle row, restart mechanism, supplier wrapper/session change, UI, B pins, S3 or SEAL2 change is authorized.

## Exact conditional owner protocol

Each admitted home has at most one unresolved installed source; a failed unpublished launch prevents another launch for that home until resolved. No retirement list accumulating children, no per-poll threads, no detached blocking reaper, and no rehydration from JSON. A local probe must settle or retain a blocking unresolved association before another probe for that home. The necessary App-lifetime retention location for a dropped/reopened Host must be reviewed with the owner; dropping a Rust Child does not discharge responsibility.

The custody cell owns Child and immutable native-source identity. Its mutex protects `OwnedUnreaped`, `ExitedUnreaped(first exact status)`, `Reaped(status)`, or `OwnershipUnavailable(reason)`, plus an irreversible `signals_revoked` bit. Identity/attempt/H5 are attribution fields, not substitutes for this state. No other caller can access Child, call wait/try_wait, invoke kill, or extract the handle. Poison/unwind fails closed: revoke operations and retain the cell; do not recover poison and signal speculatively.

1. Observation takes only the custody mutex (prefer try_lock with explicit busy return). Under the accepted platform contract call waitid(P_PID, exact owned PID, zeroed siginfo, WEXITED|WNOHANG|WNOWAIT). Zero si_pid is no observed exit, not proof of life; nonzero must match exact child and an allowed terminal code. Store the first exact status. Contradictory repeats become unavailable. EINTR gives interrupted/no action and returns without an unbounded retry; ECHILD, unsupported options or other errors invalidate signalling eligibility. No consuming API is used here.
2. Signal takes that same mutex and checks source authorization, support and unreaped state; it keeps the guard through the actual group signal. No check-unlock-signal interval and no callback, logging I/O or source lock is allowed inside. A concurrent owner reaper cannot pass the guard. Success records only signal submission; ESRCH is not a whole-tree conclusion; EPERM/other errors retain uncertainty. Signal-zero is governed identically and is not used as a count.
3. Final reap is a separate explicit one-way operation, not a side effect of observation or EOF. Under the owner mutex, revoke all future numeric group operations **before** a single waitpid(exact PID, WNOHANG) consuming call. It is permitted only after terminal status is observed and an accepted policy has decided no more group action is required. Match the returned identity/status; any unexpected zero/error leaves unavailable standing, never re-enables signals. Do not call Child.wait afterwards or allow Drop to signal. The Child value can be dropped after exact successful reap, with historical custody retained.
4. The caller copies the result, releases custody, then reacquires source gate→Inner to install only against captured source/attempt/state. A stale result may settle its own custody history; it cannot mutate a later source. Explicit cleanup authorization is bound to the old source, so slot replacement cannot retarget it. Replacement is itself prohibited while prior cleanup remains unresolved.

These are finite syscall attempts, not a hard real-time promise. No blocking Child.wait is used. Any grace polling sleeps outside every lock and obeys a cancellation/closing token; expiration returns cleanup unavailable, not LT23 or success. Closing stops admissions and polling; it does not cancel an in-progress kernel operation, destroy the owner, prove death or authorize a post-reap signal. No shutdown join is introduced.

## Lock graph

Existing initial admission: attachment gate→Inner. Existing final spawn admission: REC writer→attachment gate→Inner. Existing writes: frame_write→source-file lock→attachment gate→Inner. Keep these existing edges.

Custody mutex is an isolated leaf protocol: acquire it only after dropping REC writer, namespace operation guards, frame_write, source-file lock, attachment gate and Inner; never acquire any of those while custody is held. Source transitions capture an immutable reference/authorization under attachment gate→Inner and then release. Observation/cleanup runs; settlement later rechecks under attachment gate→Inner. The source cannot be released for replacement while cleanup is in flight/unresolved. New custody construction before publication is private and uncontended; installation moves the reference, not a locked cell. Publication worker/controller locks never participate. No wait on custody while source gate is held, and no OS wait while any global lock is held.

## Availability and final-reap decision table

| Situation | Required result absent additional proof |
|---|---|
| Ordinary Stop, unreaped source and accepted signal prerequisites | May close its bound input and submit authorized signal; no automatic tree-ended conclusion. Without accepted descendant completion proof, return explicit cleanup-unavailable and retain stopping/source responsibility; no LT23, no new start. |
| Handshake failure | Preserve scoped failure evidence; cleanup availability is separate. No automatic retry/replacement while unresolved, even if LT11 is already recorded. |
| EOF/actual LT12 with exit observed but not reaped | Preserve actual exit/REC event semantics; ownership retained. LT12 does not establish clean descendants or authorize reaping. Later cleanup remains a separate operation. Direct post-LT12 Stop row mapping remains held. |
| Leader already reaped, absent handle, foreign wait suspected or ownership unknown | No numeric group probe or signal. Return cleanup-unavailable, retain unresolved source association. No fabricated zero census, no successful cleanup, no restart release. Repeated Stop cannot cure absent authority. |
| New verification / LT20 cancellation | Touch only the current unspawned attempt. Prior source custody and cause remain unchanged. New actual spawn blocked by unresolved prior custody. |
| App closing / grace expires | Stop polling and new admissions; expose unresolved cleanup. No thread join, false stopped state or implicit transfer to OS supervision. Whether App exit is prevented or permitted with unresolved responsibility is a parent availability decision. |

Keeping the zombie indefinitely would preserve at most a conditional reservation and leak resources; reaping and then probing the old numeric group loses authority. Neither is an acceptable hidden completion policy. A separate warranted containment/census mechanism or explicit unavailable mode is required. No numeric timeout resolves this conflict. This is why the complete production route remains NOT READY despite a concrete sole-owner algorithm.

## Deterministic examination plan after release only

Use private invented children and explicit pipes/barriers; never arbitrary PIDs or the supplier. No natural PID reuse stress, system process enumeration, sleeps-as-ordering, or native App execution. Test-only operation traces must capture every observation/signal/reap attempt and source association.

1. Signal-first: pause inside owner guard immediately before syscall; competing EOF/reap operation is busy and cannot consume status. Resume one signal, then reap; prove zero later group calls. Reverse ordering: final reap first, then Stop/handshake cleanup produces no group call and explicit unavailable. Use an inert backend for intentionally reused numeric identifiers; do not signal a recycled OS ID.
2. Nonreaping contract experiment on the exact recorded platform: invented child exits; observe twice with WNOWAIT; consuming wait once returns matching child/status; subsequent wait reports no child. Keep this as observed behavior, not universal OS proof. Separate leader-plus-descendant fixture checks reservation assumptions, without treating killpg(0) as census.
3. Duplicate EOF, Stop and handshake failure racing; source replacement attempted while custody unresolved; local postspawn allocation failure; cancellation and closing during grace; no global lock held during custody operations. Assert no stale settlement into a successor and no replacement release.
4. ECHILD, EINTR, EINVAL, permission errors, unexpected/mismatched status, poison and panic seams: no fallback numeric termination, no cleared responsibility, no repeated consuming wait, no automatic retry loop. Test auto-reap disposition only in an isolated test subprocess, never alter the harness/App's SIGCHLD globally.
5. Process-group escape/migration fixture demonstrates that group targeting is not a descendant census. Missing proof must refuse completion rather than manufacture zero survivors. Keep old H5/PID verifying LT20 no-action regression unchanged.
6. Both feature states and connecting Host Stop/EOF/handshake/probe tests after exact implementation release. Existing actual REC-count failures remain named Step 2 residuals; no whole-trace or full-Stop conformance claim. Export/pin renewal is later receiving work, not a test for custody safety.

Independent design review must close platform support, all-waiter exclusion, conditional PGID continuity, final-reap/census policy, lifetime retention and App closing consequence before production implementation is called ready. If those cannot be closed within Step 1, return the unavailable alternative for a concrete owner decision; do not broaden into a wrapper, supervisor or different supplier launch contract automatically.

## Exact consulted local source identities

Repository paths below are relative to basis bf795b99d1f7093178b41ca93e638450eca2d8e0, not mutable checkout claims.

| Source | SHA-256 |
|---|---|
| AGENTS.md | f96feb19d297c74e10048c506805b2fe3622c50cfefd6078f599724556113977 |
| agents/AGENT_TASK.md | 1a13a5b00b3ce01ff8519efe6b46bcbe0cd6a5b7985e24282fa7efa2c57c8fb7 |
| .agents/skills/chirality-change/SKILL.md | 1a2b056263ec77e4104efdf99afe3fe76dda792334a243fb2f21c60bc9c81450 |
| projects/chirality-app-v4/loop/LOOP_INIT.md | c2e88f81439ed03578fee13fd7563082fefdfe11096d9134a59531eba3b985bd |
| hosting.rs | 7b9f306d7c6fc9ceeeb4178003521afcdafe5981370f0fc87418fdf35e2644b9 |
| hosting_successor.rs | 81996c7b8def7717aca5183c565b02b82de2985a7305d95c95d34dd3c7693c9a |
| lib.rs | 068c3039d446b8d341c8c3e5dac60937b7cc11b0746276da6babd751b90872f2 |

SDK root `/Library/Developer/CommandLineTools/SDKs/MacOSX.sdk`:

| Relative source | SHA-256 |
|---|---|
| usr/include/sys/wait.h | 59742f1ebee76c58ce7c36a44f4ee7cbf4faa6edfaad7a32208190e193d76bf6 |
| usr/share/man/man2/wait.2 | 2178648ce5091cba439ca601216ec3f368ed64487f91385f68b65e7b5e5e5409 |
| usr/share/man/man2/setpgid.2 | c0266df5531a862435f68e669f307f5fa0f37c9df5ab740fce37cd4ecb59fbe4 |
| usr/share/man/man2/sigaction.2 | a903e2842957c58bcd3c974c39ca0899d07b0b4c4b65c3e73d136687cceefafc |
| usr/share/man/man2/killpg.2 | fec81b2fbda8ffab3f17575a90623c8f98b52f52caf6e8a2fab9748b769791da |

Prior held review `/private/tmp/STOP_PART1_INDEPENDENT_REVIEW.md` was deliberately consulted to avoid repeating its ownership/availability omissions. Root and TASK are supplied role context; no other full role was loaded. Project manual entry/Field Book and Agent User Manual headings were refreshed; manager retains the active graph and prior diagnosis. No new graph, MEMORY, accepted contract or instruction was authored.
