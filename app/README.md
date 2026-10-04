# Chirality App v4: walking skeleton

Run `APP-V4-GRAPH-CLOSURE-20261004`. Built by a Type 2 TASK (SK) for HELP_HUMAN,
on the owner's direction to build a walking skeleton through the contract core.

This is one thin path, built as code against the frozen Design files. It is not
a candidate, it is not qualified, and nothing here is accepted. The content is
the Pass 4 fixture FX-DP1
(`../execution/_Coordination/AgentRuns/APP-V4-DESIGN-PASS-4-20261003/E/`). It is
invented, and no person performed any of its acts.

## The path

1. **Host Codex.** The Tauri 2 Rust main process starts the stock Codex 0.158.0
   App Server as a child process. It verifies the binary, then sends
   `initialize` and `initialized` over stdio JSON-RPC. It then sends
   `thread/start` and shows the connection and thread state in the window.
2. **Decide.** The person opens the App act control on a pending decision
   package and chooses an alternative. They confirm in a native dialog that the
   host owns and fills in. This is A16 "decide".
3. **Record.** The capture evidence is written first. The RS `human_act` is then
   appended to `records/coordination.rs.jsonl`. The test validates it against
   `RS_RECORD.schema.json`.
4. **View.** The decision view is derived from the files. It shows the package
   as *decided*, with the alternative, the person, the recorder and the lapse
   state.

## Modules and the contract sections they implement

| Module | Implements |
|---|---|
| `src-tauri/src/hosting.rs` | DEL-01-01 `HOSTING_BOUNDARY.md` v0.9. Covered: §3 invariants H2, H4, H5, H6, H7, H10 and H11; §4.1 states; §4.2 start steps 1–5; §4.5 deliberate stop; §4.7 rows LT-01…LT-06, LT-08, LT-09, LT-11, LT-12, LT-17…LT-19 and LT-23; §5 framing and classification; §5.1/§5.2 client-request records; §7.1/§7.2 version identity and verification. Its records follow `hosting.lifecycle-event.schema.json` and `hosting.client-request-record.schema.json`. The protocol shapes are those of 0.158.0 (`Design/generated/0.158.0`, PIN_SPIKE §5) |
| `src-tauri/src/act_control.rs` | DEL-01-04 `APP_ACT_CONTROL.md` AAC-v0.3. Covered: §1.2 A16 row; §2 AI-1 and AI-9; §3 rows AX-01…AX-06, AX-08, AX-12 and AX-13, plus the refusals listed under the table; §4.1 steps 2–7; AK-c and AK-e; §5.1 offer; §5.2 capture evidence; §5.3 RS entry; §6.1 NA-3 and NA-4; §7 identity. It also follows DEL-04-03 `RECORD_SEMANTICS.md` §6.1 (A16 rows) and HA-11, and DEL-04-01 `ACT_AND_POLICY_CONTRACT.md` §2.1 (A16 row) |
| `src-tauri/src/canonical.rs` | AAC §5.1 offer digest `aac-offer-digest/0.1`, written from the text |
| `src-tauri/src/records.rs` | RS §13.1 S-A (JSON Lines log), §13.2 entry header, §14.1 W-0/W-1, §14.2 R-2 |
| `src-tauri/src/recorder.rs` | RS §13.6 decision packages, with the file → `act_request` mapping (R23-24). The body is DEL-02-03 `checkpoint-record-entries.schema.json` `$defs/actRequest` (CE-4) and the file shape is `$defs/decisionPackageFile` |
| `src-tauri/src/decision_view.rs` | DEL-06-02 `DECISION_VIEW.md` §3 DV-1…DV-9, §4 row states and §6 failure behaviour (a port of Pass 4 `decision_view.py`) |
| `src-tauri/src/lib.rs` | The Tauri commands. The webview reads snapshots and asks the host to act. `decide` presents the AAC §6.2 P-2 native confirmation through `tauri-plugin-dialog`, and only that confirmation captures |
| `src/App.tsx` | The interface. It shows host state, threads, lifecycle events, the decision rows (DECISION_VIEW §4) and the act control's offer. It holds no pipe and captures nothing |

## Build, test and run (offline only)

You need Rust 1.92, Node 24, the cargo registry cache and the npm cache already
on this machine. Nothing is downloaded.

```sh
cd projects/chirality-app-v4/app
npm install --offline                    # from the npm cache
(cd src-tauri && cargo build --offline)  # Rust main process
npm run build                            # tsc + Vite build into dist/
```

### Tests

Run these from `app/`:

```sh
export CHIRALITY_CODEX_BIN=<path to the stock codex 0.158.0 vendor binary>
# optional: the expected sha-256 of that binary; without it the run is the
# U-06 development case, labelled unverifiable
export CHIRALITY_CODEX_EXPECTED_SHA256=<hex>
npm test     # runs the Rust tests, then validates what they wrote with Ajv
```

- `npm test` runs `tests/validate-records.test.mjs`. That test runs
  `cargo test --offline --test decide_flow` and `--test handshake`. It then
  validates what they wrote against the Design schemas, as they are:
  - the RS entries;
  - the AAC offer and capture;
  - the package file;
  - the hosting lifecycle and client-request records.
- `cargo test --offline` in `src-tauri/` runs the unit tests and both
  integration tests on their own.
- The handshake test fails if `CHIRALITY_CODEX_BIN` is unset, unless you set
  `CHIRALITY_SKIP_CODEX=1` explicitly. Without the variable, the node test marks
  the hosting-records check as skipped.
- The handshake test makes its own scratch home with
  `mktemp -d /private/tmp/cxh.XXXXXX`. It writes a `config.toml` there that
  stands in for the person's configuration. That file sets plugins off,
  analytics off, and a model provider at 127.0.0.1 port 9, where no server
  runs. It never uses `~/.codex`, never signs in and supplies no credential. It
  checks that the Codex process group holds no internet socket after
  `thread/start`.
- No model turn is started.

### Run the App

All of these are environment variables. No path is built into the code.

| Variable | Meaning |
|---|---|
| `CHIRALITY_CODEX_BIN` | The stock Codex binary (required for hosting) |
| `CHIRALITY_CODEX_HOME` | The App-owned Codex home. Use a scratch directory made with `mktemp -d /private/tmp/cxh.XXXXXX`, never a real Codex home. A `config.toml` placed there stands in for the person's configuration |
| `CHIRALITY_CODEX_EXPECTED_SHA256` | The expected distribution identity. If it is absent, the start is refused unless `CHIRALITY_ALLOW_UNVERIFIED=1` |
| `CHIRALITY_ALLOW_UNVERIFIED` | `1` runs an unverified distribution for development (U-06), labelled as such |
| `CHIRALITY_WORKSPACE` | The project folder. It holds `project/decisions/*.json`. The App writes `records/coordination.rs.jsonl` and `.chirality/captures/` there |

Seed a workspace with the fixture's two package files, then start the App:

```sh
WS=$(mktemp -d /private/tmp/cxws.XXXXXX); mkdir -p "$WS/project/decisions"
cp ../execution/_Coordination/AgentRuns/APP-V4-DESIGN-PASS-4-20261003/E/fixtures/FX-DP1/project/decisions/PKG-*.json "$WS/project/decisions/"
CHIRALITY_WORKSPACE=$WS CHIRALITY_CODEX_HOME=$(mktemp -d /private/tmp/cxh.XXXXXX) \
CHIRALITY_CODEX_BIN=... CHIRALITY_ALLOW_UNVERIFIED=1 npx --offline tauri dev
# or: npx --offline tauri build --no-bundle -- --offline, then run src-tauri/target/release/chirality-app-v4
```

In the window:

1. Press "Start thread".
2. Set your name.
3. Press "Open act control (decide)" on a pending package.
4. Choose an alternative and press "Decide…".
5. Confirm in the native dialog.

The row then shows *decided*.

## Skeleton choices and limits (not contract changes)

- The places where records and captures are kept are unselected (OI-014, U-05).
  The skeleton uses `records/coordination.rs.jsonl`, as the fixture does, and
  `.chirality/captures/`.
- Times are RFC 3339 UTC strings. The representation is unselected.
- Record ids take the form `rec:app:coord:NNNN`. Minting is unselected.
- Not built:
  - restart rules (§4.4);
  - the server-request register (§6);
  - re-attach journal replay;
  - the per-home config link (§4.2 step 3, option C);
  - SEAL-2 (AAC §6.3);
  - W-0 repair and W-2 late write;
  - relaunch recovery (AC-R1);
  - Codex account read (AAC §7: absent, never guessed).
- The writer does not run the W-1 schema check, because no JSON Schema crate is
  in the offline cargo cache. The test validates every entry the skeleton
  writes. See EVIDENCE.md.
- Ending the App with a signal skips the stop record. Codex still ends when its
  input closes, but the App records nothing for that stop.

See `CONTRACT_ISSUES.md` for points where the contracts are ambiguous or could
not be implemented as written, and `EVIDENCE.md` for what was run.
