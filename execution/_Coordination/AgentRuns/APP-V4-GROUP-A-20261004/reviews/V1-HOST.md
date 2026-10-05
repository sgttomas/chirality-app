# V1-HOST — independent P0 hosting product review

2026-10-04. Independent TASK `/root/group_a_execution/hosting_contract_review` under WORKING_ITEMS `/root/group_a_execution`, delegated-harness-native, no descendants. Root `/Users/ryan/.codex/worktrees/077c/chirality`. Write boundary: this report only. Software-code-review skill loaded; retained Root/TASK/LOOP/CC-H/SUP1 authority basis from V0-H-R1 and V0-SUP1 applies.

## Disposition and exact basis

**Repair before existing-path fan-in. Two major blocking findings; no minor finding.** Reviewed frozen `changes/P0-HOST.md` SHA-256 `fe81fd5958f63414bf346e8a56f82b49f40d3e26b38ea40914db5eb6435ac9c9` and repaired `hosting.rs` SHA-256 `a7c1867acea11e4211f74f071b91a9529cbbfe56ead320845c4502790db1d8ac`. The record's earlier hosting hash is explicitly historical; all other five stated product output hashes matched when checked. Read full hosting source, bounded diff from `e916ad1789`, new hosting-contract and real handshake tests, resource identities, util entropy supplier and current host-related lib/UI/Node integration. ACT source is excluded from verdict; concurrent act repairs are not approved by this review.

Manager has restarted the author to repair the two early findings. This review remains against the sealed original above; no later edit is silently reviewed or accepted. Seal a successor and commission affected backcheck. No Cargo slot was used (ACT owns it), no dependencies downloaded, credentials/authentication/live model work or Git mutations.

## Major findings

### HOST-M1 — contradictory handshake loses held native frames (blocking)

Location: frozen `app/src-tauri/src/hosting.rs:390–399`, especially the return at 399. The new contradictory-userAgent branch kills the child, closes pending requests and emits LT-11, but never transfers `i.held` into the public journal. The normal initialize-error/timeout branch at 423–440 performs exactly that transfer and marks entries `generationNeverReady`.

Trigger: the current offline hosting-contract double emits `test/early` and then an initialize result whose userAgent is changed to `codex/0.159.0`. Both entries were held under the full generation by `on_line`; the latter also correlated the handshake response. The contradiction branch then returns. `snapshot()` exposes journal, not held, so neither native frame is surfaced. A later spawn clears held entirely. This is confirmed by source control flow and the double's written emission order, not a newly executed Host test.

Impact/claim: P0-HOST's statement that all handshake frames, including native initialize responses, are preserved in receipt order does not hold on its new mismatch path. HOSTING H4/H6 and §4.3 failure step 4 require held frames from a never-ready generation to be delivered with that status, never dropped. The user's refusal/diagnosis loses the very native response that explains the rejection.

Repair direction: use one handshake-failure cleanup path, transfer every held entry in original receipt order with the owning full generation and never-ready marker before closing/returning, and retain the contradictory native reported identity as observed rather than leave its versionIdentity report empty. The existing test should assert that both `test/early` and the actual initialize response survive unchanged and ordered with no LT-09, and that retry/stop does not erase or duplicate them. This preserves the refusal; it does not weaken verification or require restart completion.

### HOST-M2 — unavailable content masks an already known version mismatch (blocking)

Location: frozen `app/src-tauri/src/hosting.rs:240–253`, with development guard at 287–291. `verify()` reads the binary after observing the version label, returns `unverifiable` plus `Some(label)` on a read failure, and only then (on the readable branch) compares the observed label to the declared pin. `dev_ok` accepts that earlier unverifiable result whenever the explicit option is on and a label exists.

Trigger: version probe succeeds and outputs `codex-cli 0.159.0`, but a subsequent content read fails (unreadable executable, file replaced/deleted between operations, or equivalent failure). The candidate records `unverifiable(binary not readable)` and proceeds via LT-24 instead of refusing the known observed-version mismatch. Generated-output comparison is skipped by the same early return.

Independent bounded stimulus: a scratch local shell double printed `codex-cli 0.159.0`, exited 0, and removed its own file; the subsequent Python content read raised FileNotFoundError. This verifies the real precondition, not execution of Rust Host. A separate execute-only native-copy attempt was killed by the platform and yielded no useful version label; no conclusion relies on that attempt. No Codex or model ran in these stimuli.

Impact/claim: CC-H §7.2 and P0-HOST require every known mismatch to refuse even with development enabled. The product can emit LT-24 for a known wrong version and attempt a child spawn; a self-removed file eventually fails to spawn, but that later failure does not repair the false verification/lifecycle disposition. A still-executable unreadable binary could proceed further. This ordering was inherited from the skeleton but remains material to the expressly claimed CI-7 propagation.

Repair direction: evaluate observed-label and compiled generated-identity mismatches before an unverifiable-content fallback, preserve no-label/empty-label refusal, and ensure every available contradictory comparison dominates unavailable comparisons. Add negative coverage combining wrong label with content-read failure; assert LT-05 mismatch/refused and no LT-24/LT-06. Keep matching readable main hash unverifiable while qualified full distribution identity is absent.

## Supported behavior and test-corpus assessment

The resource mirrors exactly match reviewed SUP1 root/v2/manifest hashes. They are embedded and checked against complete constants; declaration is 0.160.0. Main-binary hash match no longer creates verified status, and explicit development choice maps to LT-24 with correct supported top-level lifecycle standing. With current absent qualified full distribution identity, LT-04 remains unreachable; no qualification is inferred from embedding or parent provider access.

Full generation objects flow through current records, journal, snapshots, threads and reader/stderr capture; foreign reader generation is checked before correlation. Typed request-id serialization prevents a string id from colliding with an integer id. Secure session creation uses fallible entropy and never a clock/counter fallback. The current single-host path is covered; per-home orchestration/restart remains I1 work, not completion implied by the test that changes homes on one Host.

Source traces show explicit native model/modelProvider fields from blank UI controls through the Tauri command to `thread_start_selected`; the legacy no-selection method truthfully refuses. Requested and reported destination facts remain separate at thread scope. Network snapshot retains expected-versus-observed standing, current child version, historical source version and sampling limitations without claiming socket contact or a model turn. UI identifies its list as expected contact. No user provider/configuration override or new default is introduced by these changed paths; analytics remains an App-child session flag.

The author reports 2 identity/resource unit passes, four offline hosting-contract passes, one real local-provider 0.160.0 handshake pass, and connected Node 3/3 after strict metadata repair. These results are **author evidence**, not this reviewer's reruns. Read assertions independently: they cover matching development hash remaining unverified, mismatch on readable binary, explicit-option absence, healthy early frame preservation/order, full identity separation and contradictory handshake not becoming ready. They do **not** check failed-handshake frame retention or known-label-mismatch plus content-read failure; increasing happy-path counts or rerunning existing tests cannot dispose HOST-M1/M2.

The Node runner registers declared canonical schema IDs without rewriting and directly validates emitted lifecycle/client records. Its hosting portion remains contingent on an actual supplier path and does not validate a server-request register/access network record that this existing path does not yet implement. No server-register/restart completion or supplier qualification is established. The real handshake test's single sampled socket check is bounded evidence only, and the record correctly retains that limitation; its comment's broad no-outside-connection wording is not used as a universal guarantee in this verdict.

`git diff --check` passed for hosting source/tests/resources at inspection. No new tests requiring the occupied Cargo slot were run; the two findings have precise source evidence and require affected successor tests when the author receives the slot.

## Return boundary and recheck

CC-H/SUP1 readiness is unchanged; two implementation defects prevent P0 existing-path fan-in. Author repairs should preserve strict schema metadata, full objects/native frames, development standing and explicit provider selection. Manager lib/UI/Node wiring remains subject to combined-candidate checking after repair. Act/capture/recording changes, request register, restart policy, configuration linking and broader Group A production remain their own owners/nodes. No acceptance, gate or release follows from this review.

Immediate reading identities for the frozen material are the hashes in P0-HOST and the superseding hosting hash above. The reviewed dependency suppliers are the already sealed CC-H b5b454… and SUP1 103606… with their independent reviews. Actual origin of the selected review skill is `.agents/skills/software-code-review/SKILL.md`; no additional role body/workflow was activated.
