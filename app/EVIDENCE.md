# Current Group A code-path evidence

Run `APP-V4-GROUP-A-20261004`. Current code uses stock Codex 0.160.0 for
development; it remains unqualified. Independent source reviews and repairs are
in `../execution/_Coordination/AgentRuns/APP-V4-GROUP-A-20261004/reviews/`.
P0-ACT-R2 and P0-HOST-R2 identify the checked production sources and residuals.

Combined final-source checks passed: offline locked Rust suite with the real
0.160.0 scratch-home handshake; Node schema suite 3/3 without ref rewriting;
TypeScript/Vite build; six embedded schema source/hash/ID checks. Raw stdout is
in that run's `validation/`. The initial unsupported schema-sync --check
invocation failed; the documented default invocation passed. Test cases and
exports use maintained invented fixtures, with native confirmation stand-ins.
No authenticated model turn occurred in these product checks. Parent supplier
provider probes are separate evidence.

CI-1…CI-9 changed through named reviewed Design control and tested consumer
adoption. CI-10 preserves unverified cold captures without creating acts;
trustworthy cold replay, signing/provenance and broader Group A work remain open.
The historical walking-skeleton evidence below retains its original scope and
0.158.0 observations; its old gaps describe that earlier source, not current code.

---

# Evidence: walking skeleton build

Run `APP-V4-GRAPH-CLOSURE-20261004`, 2026-10-04, macOS 26.6.2 arm64. Toolchain:
rustc and cargo 1.92.0, Node v24.5.0, npm 11.5.2. Executor: Type 2 TASK (SK),
Claude Opus 5.5, for HELP_HUMAN.

## Elapsed time

| Moment | Time (MDT) | Elapsed |
|---|---|---|
| Start (first command) | 15:47:55 | 0 |
| Step 1 test passes (Codex `initialize` + `thread/start` from Rust) | 15:59:38 | 11 min 43 s |
| First full end-to-end pass: `npm test` covering all four steps plus schema validation | 16:01:39 | 13 min 44 s |

## Which steps run as tested code

| Step | Tested by | Result |
|---|---|---|
| 1 Host Codex | `src-tauri/tests/handshake.rs` (real stock 0.158.0 binary, scratch home); hosting records validated by `tests/validate-records.test.mjs` | Pass |
| 2 Decide (A16 through the act control) | `src-tauri/tests/decide_flow.rs` `person_decides_a_package_and_the_view_shows_it` | Pass. The native dialog itself is not pressed by the test (see below) |
| 3 Record written and valid | The same test writes the record. `validate-records.test.mjs` validates it against `RS_RECORD.schema.json`, and validates the AAC offer and capture and the package file | Pass |
| 4 View shows the decision | `decide_flow.rs`: view model after the decision, and `view_model_reads_the_pass4_fixture` | Pass |

Not exercised:

- **A model turn.** No local model server is running, and none was attempted.
- **A click on the native confirmation** (AAC VC-AAC-13). A test cannot press
  the host's native dialog. The test calls the control's `confirm` with
  `HostNativeConfirmation` as a stand-in for the person's click. The App
  exposes no such path.
- **The UI through a real click on "Decide".** The release build was launched
  and observed (below), but nobody operated it.

## Commands and results

All builds ran offline. Nothing was downloaded.

```text
cargo generate-lockfile --offline        (src-tauri/) -> Locking 446 packages; tauri 2.11.1, tauri-build 2.6.1,
                                           tauri-plugin-dialog 2.7.2, wry 0.55.1, tao 0.35.2, rfd 0.16.0, sha2 0.10.9
cargo build --offline                    -> Finished `dev` profile (first build ~29 s); no warnings
npm install --offline --no-audit --no-fund -> added 136 packages in 2s
npm run build  (tsc --noEmit && vite build) -> vite v7.3.6; 30 modules; dist/assets/index-*.js 197.47 kB; built in 342ms
npx --offline tauri build --no-bundle -- --offline
                                         -> Finished `release` profile [optimized] in 1m 01s;
                                            Built application at src-tauri/target/release/chirality-app-v4
cargo test --offline --lib --test decide_flow -> 3 + 3 passed
CHIRALITY_CODEX_BIN=<scratch>/…/codex npm test -> 3/3 pass (output below)
```

### Final `npm test` (16:04:19), U-06 development case (no expected identity given)

```text
> node --test tests/validate-records.test.mjs
     Running tests/decide_flow.rs
test offer_digest_matches_pass4_fixture ... ok
test view_model_reads_the_pass4_fixture ... ok
test person_decides_a_package_and_the_view_shows_it ... ok
test result: ok. 3 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.03s
     Running tests/handshake.rs
test hosts_codex_initialize_then_thread_start ... ok
test result: ok. 1 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.63s
✔ Rust decide flow runs and produces outputs (202.650083ms)
✔ decision record and act-control objects validate against the Design schemas (115.458292ms)
✔ hosting lifecycle events and client-request records validate (878.280583ms)
ℹ tests 3  ℹ pass 3  ℹ fail 0  ℹ skipped 0
```

Lifecycle of that run, by transition and verification result:

- LT-01;
- LT-04, `unverifiable`, with the U-06 reason;
- LT-06, LT-09, LT-17 and LT-23.

Start to thread took 554 ms. No internet socket was found after `thread/start`.

### Verified case (16:02:15)

The same run with `CHIRALITY_CODEX_EXPECTED_SHA256=788a818f…ba35c8` passed 3/3,
with LT-04 `{"result": "verified"}`. That value is the spike-observed sha-256
of `bin/codex` (HOSTING §7.1). I recomputed it here with `shasum -a 256` on the
scratch binary and got the same value. It is not a qualification of the pin.

### What the step-1 test checks

- A request before ready is refused and not sent (CR-03).
- `start` reaches `ready` at generation 1.
- The observed label is `codex-cli 0.158.0`.
- The handshake is consistent: `userAgent` carries 0.158.0.
- The reported `codexHome` is the scratch home.
- The declared capabilities are `{experimentalApi: true, requestAttestation: false, explicitGatewayOauth: true}`.
- `remoteControl/status/changed` arrived with the `initialize` response. It was
  held and then delivered with ready, unchanged, with `emittedAtMs` (H4, H6).
- `thread/start` returns a thread id, and `thread/started` follows in the same
  generation.
- `lsof -a -i -g <pgid>` finds no internet socket.
- `initialize` and `thread/start` records show `response-observed-result`, and
  `thread/start` is `person-directed`.
- The stop gives LT-17 then LT-23, with 0 surviving descendants. A request after
  the stop is refused.

### What the decide-flow test checks

- The recorder writes two `act_request` entries from the fixture's package
  files. Their bodies equal Pass 4's apart from `time` and `requester`
  (CONTRACT_ISSUES CI-3). The same bytes are not requested twice.
- The composed A16 offer equals Pass 4's `offer-PKG-1.json` apart from
  `offerId`, `composedAt` and the digest. The digest recomputes under
  `aac-offer-digest/0.1`.
- The Rust digest of the Pass 4 offer file equals its recorded value,
  `f0d82571…`. That offer carries ü, ≈ and U+2028.
- Refusals that capture nothing:
  - a webview script, an agent tool or an App rule (AX-04);
  - a capture before present;
  - an alternative the package does not name;
  - a second capture from one offer.
- The positive capture:
  - writes the capture, then the record (`human_act`, seq 3, A16, ALT-2);
  - gives a body equal to Pass 4's `human_act` apart from the capture
    reference and time;
  - uses the same recorder.
- The view shows PKG-1 *decided*:
  - ALT-2 with its statement;
  - "Engineer A / enga (identity not verified)";
  - direct capture, not lapsed.

  PKG-2 stays *pending*.
- The view writes nothing: the input hashes are the same before and after
  (DV-9).
- If PKG-2 changes after its offer is shown, the offer goes stale and no record
  is written (AK-c, AX-06).
- If PKG-1 changes after the decision, the row shows *lapsed*, and the decision
  is still shown (DV-7).
- `view_model_reads_the_pass4_fixture` reproduces Pass 4's view of FX-DP1:
  PKG-1 decided ALT-2, not lapsed; PKG-2 pending, although the agent message
  claims a decision.

### Schema test

- Ajv 8.20.0 (draft 2020-12, `strict: false`) compiles:
  - RS, with CI-1's in-memory ref rewrite;
  - the DEL-02-03 checkpoint schema 0.7;
  - DEL-04-02 settings-in;
  - AAC offer 0.3 and capture 0.3;
  - the hosting lifecycle and client-request schemas (v0.8).
- Every written RS entry is valid.
- Negative controls fail as they should:
  - an A16 without `requestRef`;
  - act kind `A9`;
  - a decision-package `act_request` without `alternatives`. This shows the CE-4
    reference resolves.

## Observations

- **N-1 Network contact at `thread/start` (CONTRACT_ISSUES CI-8).** Before
  writing the tests, I ran a probe (`$SCRATCH/sk/probe.py`) against the stock
  binary. It had a fresh scratch home, `-c features.plugins=false` and
  `-c analytics.enabled=false`, and no model provider configured. `thread/start`
  made Codex open `wss://api.openai.com/v1/responses`. Its diagnostic output
  read `failed to connect to websocket: HTTP error: 401 Unauthorized`. No
  credential existed or was sent by me. That was one outside contact made by
  Codex during this run. All later runs configured a provider at
  127.0.0.1:9. A second probe and every test run saw no internet socket.
- **N-2 Release build launched.** `src-tauri/target/release/chirality-app-v4`
  was started for about 6 s with a scratch home, a scratch workspace seeded with
  PKG-1 and PKG-2, and the expected identity set.
  - The App ran.
  - Its only child was `codex -c analytics.enabled=false app-server`, as a
    process-group leader (pgid = pid; H11).
  - The webview called `decision_view`, so `records/coordination.rs.jsonl` was
    created in the workspace.
  - On SIGTERM the App exited (rc -15). The Codex child was gone within 1.5 s
    because its input closed. No App stop record was written, because a signal
    is not a confirmed quit (README limits).
- **N-3 Stray directory, outside the write fence.** While checking ignore rules
  I ran `mkdir -p $W/../x`. That created an empty directory
  `.claude/worktrees/x` beside the worktree. I removed it at once with `rmdir`
  (it was empty). It is no longer present.
- **N-4 Scratch left in place.** I created scratch homes, probe homes,
  workspaces and cwd folders with `mktemp` under the macOS system temporary
  directory. Their names
  are `cxh.*`, `cxp.*`, `cxw.*` and `cxws.*`. The test runs, the probes and the
  launch create these and leave them. None is a real Codex home.
- **Design files** were only read. `git status` shows only `projects/chirality-app-v4/app/` as new from this task. An untracked file elsewhere in the worktree,
  `docs/alignment-manual/…`, is not this task's.
- **Build outputs are ignored.** `git check-ignore` shows:
  - `app/node_modules/`, `app/dist/` and `app/src-tauri/target/` are ignored by
    the root `.gitignore`;
  - `app/src-tauri/gen/` is ignored by `app/.gitignore`, which I added.

## Blocked or missing offline

- **A JSON Schema validator crate for Rust is missing.** It is needed for RS
  §14.1 W-1 in the writer (CI-9). The cargo cache at
  `~/.cargo/registry/cache/index.crates.io-1949cf8c6b5b557f/` holds no
  `jsonschema`, `boon` or `valico` crate. Candidates are `jsonschema` (crates.io)
  and `boon` (crates.io; draft 2020-12, few dependencies). I did not look up
  their versions or sizes, because that needs the network. Nothing else was
  missing:
  - the Tauri 2 crates and `tauri-plugin-dialog` 2.7.2 (with `rfd` 0.16) came
    from the cache;
  - every npm package came from the cache.
- **The Tauri bundle (.app/.dmg) was not built.** `bundle.active` is false and
  `tauri build --no-bundle` succeeded. Whether bundling needs anything outside
  the caches was not tested.


## Group A portable temporary-directory repair (2026-10-04)

Run `APP-V4-GROUP-A-20261004`, T0, supersedes the test scratch behavior in
historical N-4 above. Rust integration tests now discover the system temp root
with `std::env::temp_dir()` and invoke `mktemp -d` with unique templates there.
Owned scratch homes, probes and workspaces are removed at test exit, including
assertion unwinding. The Node schema runner keeps one unique `os.tmpdir()`
evidence directory alive through its schema assertions and then removes it;
standalone Cargo runs retain their exports under Cargo's test output root.
The local unavailable provider, plugins/analytics settings and the assertion
that Codex holds no internet socket after thread/start are preserved.

Exact candidate hashes, commands, results and remaining platform limits are
recorded in
`../execution/_Coordination/AgentRuns/APP-V4-GROUP-A-20261004/changes/T0.md`.
This repair makes temp allocation portable; it does not qualify the App or
its process-group/socket checks on an additional operating system.
