# C3-U read-only route-account presentation

Candidate: code and maintained fixture in this commit, based on `412cf7fa012f400043182e4c9e8ea0e1725c843f`. Implementation author: TASK `/root/group_c_successor/route_persistence`, delegated by WORKING_ITEMS `/root/group_c_successor`. Independent code review remains required. This is a bounded presentation contribution, not completion of C3 or Group C.

## Selected basis and behavior

C3-U-READ-01 is selected from the unchanged source-owner `C3_SOURCE_WALK.md` at `e24bd8a5a2`, independently reviewed in `b6dfaf7bc3` and integrated by the manager as `ae061bd` / `4b392582ba`. The exact account is copied into maintained `app/tests/fixtures/connector-route-source-walk.json`; its immutable origin and hashes are in `C3_PRESENTATION_BASIS.json`. Tests do not depend on a dated run directory. Its source pins and contradictory historical status statements remain literal. The source owner performed the manual walk; the App view does not perform it.

The new host command accepts no renderer root or reference. It requires the host workspace, known explicit project reference, no association error, and an exact match using the existing lossless path identity encoding. Unknown, absent, invalid, mismatched, and project-open failure states remain distinct. No cwd, home, thread, normalization, or renderer fallback is used. A lightweight availability snapshot does no filesystem discovery. Reading is manual and read-only through existing `ProjectRouteStore::discover`.

The panel presents recorded question, gaps/effects/responsible parties and recorded duties directly. All question/trigger/source revision/hash/role/fact/anchor/conclusion/recorder/time fields remain available as host-produced parsed JSON text. The full parsed account and cold binding are also available. Arbitrary numeric fact data and u64 binding identities avoid JavaScript number conversion; this does not add arbitrary precision beyond the existing Rust JSON reader. Literal source paths, anchors and evidence are escaped text, not links or instructions. Missing metadata remains missing. Zero-source accounts cannot imply an answer from files.

Discovery issues, duplicate IDs and all matching cards, absent directory, complete empty directory and incomplete enumeration remain distinct. No duplicate winner is chosen. Refresh clears prior results before reading and leaves no old success after failure. Cold observation does not establish publication success, source truth, actor performance, continuous pathname identity, or resolution against a separately held prior reference. There is no prior-reference action in this slice. Existing CRP-v0.3 resolve semantics are unchanged.

## Actual checks

- Offline frontend build (`npm run build`): passed TypeScript and Vite compilation.
- Maintained frontend presentation tests: 10 passed, including six new actual React server-render/state tests. The exact manual walk and four constructed trigger variants retain the same question/facts; recorded fields, conflicting claims, duties, zero sources, missing metadata, duplicate cards, discovery issues, incomplete/empty/absent/error states, escaped text, large-number text and failed refresh are covered.
- Focused Rust view tests: four passed. Guard refusals, non-Unicode association identity, actual missing-project failure, absent-directory no creation, valid duplicate accounts, malformed/unknown formats, full account/large integer retention and unchanged on-disk bytes are exercised. Incomplete discovery projection is injected explicitly; no filesystem fault is falsely claimed.
- Full maintained `npm test`, with approved offline Cargo environment: 12 passed, one supplier-handshake check explicitly skipped. Its Rust decide-flow dependency passed four tests. No supplier was launched.
- Combined offline connector regressions (`cargo test --offline --lib connector_`): 35 passed, zero failed; includes persistence and standing alongside the four new view tests.
- `git diff --check`: passed before staging. Staged host-private-term validation is required immediately before commit.

An initial full npm invocation from the wrong working directory failed before tests. A subsequent invocation from the App without the approved Cargo environment failed its pre-existing Rust fixture dependency; after supplying the documented environment, the full entrypoint passed. An initial Rust projection syntax error was repaired before the passing checks. These are preparation failures, not passing evidence.

## Environment and remaining limits

Dependencies were installed with offline/no-audit/no-fund/ignore-scripts flags from existing cache. Rust used the approved Group A Cargo home, `CARGO_NET_OFFLINE=true`, `CHIRALITY_SKIP_CODEX=1`, and one private copy-on-write target cloned from the earlier quiescent persistence target. Only checks actually executed in the private target support this return; reused artifacts are local acceleration, not portable evidence. No downloads, native App launch, supplier handshake, provider input, credentials, person act, save/import/send, source picker, graph/instruction/schema semantic changes, or source-file reconstruction were performed.

macOS was tested. Browser/native visual interaction and other operating systems were not exercised. Tests render the actual component and compile actual command registration; they are not a native IPC witness. The read-only reader inherits existing store capability/containment and uncertainty semantics. Manager integration, exact-head independent review and required CI remain separate.

## Independent fidelity repair

Independent review `814c5eadd95fdb7b3024f364fe9e305851409b5f` found a P2 visible overclaim on integrated candidate `9d8baf3da6cf52aa5e8cedbe1723670c80efda15`. Its executed serde_json probe showed `18446744073709551617` becoming `1.8446744073709552e+19` and `0.12345678901234567890123456789` becoming `0.12345678901234568`. The probe passed its assertion of differing representations; the candidate failed the visible fidelity requirement. Host text avoids subsequent JavaScript rounding but is not an original-byte or arbitrary-precision representation.

The repair labels sections and full account as host-parsed, visibly discloses formatting normalization and possible integer/decimal rounding, and states that display cannot recover precision already lost. The binding hash remains a host observation of bytes, not frontend verification or parsed-value certification. No schema, store semantics, or accepted source meanings changed. Existing u64/text fidelity coverage remains. A new actual component-render test checks the labels and limitation at the point of viewing. Earlier check counts above remain historical.

Repair checks: frontend TypeScript/Vite build passed. Full maintained offline npm entrypoint passed 13 checks (including all seven new presentation checks), zero failed, one explicit supplier-handshake skip; its Rust decide-flow dependency passed four checks. No backend source changed, so the earlier 35 connector passes remain applicable. Diff check passed. Independent exact repair backcheck remains required.
