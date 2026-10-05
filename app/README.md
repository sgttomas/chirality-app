# Chirality App v4 — runtime contract development

Run `APP-V4-GROUP-A-20261004` repairs and extends the walking skeleton from
`APP-V4-GRAPH-CLOSURE-20261004`. The current path hosts stock Codex 0.160.0,
supplies reviewed v4 common/role guidance, receives native requests and activity,
loads external observations, records decision packages, confirms A16 through the
host-native control, and reads recorded decisions with their limits. Group A development remains active;
packaging, supplier qualification and the owner's stage gate are separate work.

Tests use the maintained invented `tests/fixtures/FX-DP1` content. Native
confirmation tests are explicit stand-ins; they do not establish that a person
performed an act.

## Current path

1. The Rust host starts the stock App Server, completes its handshake and keeps
   native frames with full `{appSession, home, spawnCounter}` generation identity.
2. The person chooses a primary role (or none) and explicitly enters a model
   and a configured Codex provider for a new thread. Codex retains its own configuration and permissions. The view
   discloses expected model contact at thread start, before a turn; it does not
   represent that notice as measured socket traffic. Reviewed v4 guidance seeds
   an editable App instruction copy without overwriting edits; new conversations
   read current bytes. Native child roles remain not supplied.
3. The recorder validates package files, records source-faithful requests and
   separately states when the requester identity is unestablished.
4. The host freezes the chosen alternative and all its consequences before
   native Decide/Cancel confirmation. Absent or empty package scope is shown as
   `not named by the package`; a nonempty scope stays unchanged.
5. Capture publication is atomic and durable before the writer prepares a
   record. The writer validates complete entries against embedded JSON Schema
   2020-12 resources before append. New App record IDs are secure UUIDv4 opaque
   tokens. Delayed trusted entries retain their facts, ID and original time.
6. Backlink failure leaves a recorded act with its link pending. Trusted pending
   captures flush before newer confirmations or recorder appends. Cold unverified
   files cannot create a new human act; existing recorded claims keep provenance
   limits when a backlink is repaired.

7. Native request controls keep the full generation and source identity; question
   answers may be partial, form aliases validate their content, and changed
   confirmation context refuses. User-verification acceptance remains unsupported
   under CI-11. Ended/replaced observations keep explicit checklist/history limits.
8. The person can select catalog/read JSON and an optional counterpart through
   native selectors. Rust retains exact bytes in memory; the panel shows complete
   reported content, unverified host origin and comparison/path-display limits.
9. Current native threads accept unchanged text input; live turns can receive an
   explicit interrupt request. Native acknowledgment is separate from turn end or
   rollback. Contradictory late starts cannot revive a completed tuple.
10. An App-owned pointer-only recovery ledger initializes before supplier startup
   at the App user-data `runtime/recovery.ledger.jsonl` path. Initialization errors
   remain visible without blocking native protocol processing or relocating data.

11. Stored native history is read without making a thread operational. Explicit
    Continue uses the latest validated native response and current generation.
    Original role guidance is retained in memory for threads started here; missing
    original guidance is shown as Unknown, independent of native role hints.

## Modules

| Module | Contribution |
|---|---|
| `src-tauri/src/hosting.rs` | HOSTING/ACCESS lifecycle, generation, request correlation, ordered native journal, development verification and network disclosure; reviewed 0.160.0 protocol resources in `resources/supplier/` |
| `native_requests.rs`, `recovery.rs`, `native_items.rs`, `access.rs` | Typed native request custody, pointer ledger, scoped live/ended activity and reported account/destination observations |
| `role_supply.rs`, `runtime_session.rs`, `resources/instructions/` | Reviewed v4 defaults, fixed composition bytes, seeding and generation-bound receiving/startup; supplier/model adoption remains a separate warrant |
| `catalog.rs`, `proposal.rs`, `external_adapter.rs`, `receiving.rs`, `external_observation.rs` | Reviewed receiving contracts and exact person-selected observation custody; no external host dispatch or origin verification implied |
| `src-tauri/src/schema_validation.rs`, `schemas/` | W-1 plus complete package/offer/capture checks; declared-ID registry with external retrieval disabled; embedded resources checked by `schemas/sync.py` |
| `src-tauri/src/records.rs` | Validated append, UUID identities, sequence/read completeness, serialization and ordered capture late-write accounting |
| `src-tauri/src/storage.rs` | Selected project/run/writer and library paths, legacy discovery, atomic capture persistence and locking |
| `src-tauri/src/recorder.rs` | Package byte snapshot and request/provenance-limit mapping |
| `src-tauri/src/act_control.rs`, `canonical.rs` | A16 offer/native binding, capture, trusted retry/backlink recovery and the designated offer digest |
| `src-tauri/src/decision_view.rs`, `act_policy.rs`, `standing.rs` | Decision projection, A16 method-aware standing and provenance limits; recorded claims do not establish native act admission |
| `attachments.rs`, `resources/attachments/` | Tested Unix text-source producer and immutable metadata list; durable pre-send transport and native picker are not yet connected |
| `native_history.rs`, `role_lifecycle.rs` | Read-only native history, scoped Continue receiving and immutable original guidance bindings; cold role-source custody remains unfinished |
| `src-tauri/src/lib.rs`, `src/App.tsx` | Native command boundary and presentation; the webview cannot confirm a capture itself |

## Offline build and checks

Use Rust 1.92, Node 24 and prepared Cargo/npm caches. Set `CARGO_HOME` if the
approved dependency cache is isolated; its machine-local recovery path is in
this run's evidence. Package downloads require the owner's authorization.

```sh
npm install --offline --no-audit --no-fund --ignore-scripts
npm run build
(cd src-tauri && cargo build --offline --locked)
(cd src-tauri && python3 schemas/sync.py)
```

From `app/`, set the supplier path to run the real offline handshake:

```sh
export CHIRALITY_CODEX_BIN=<stock codex 0.160.0 vendor binary>
export CHIRALITY_CODEX_EXPECTED_SHA256=112fae7a5a1223e673c8a1791d32338f37df8b527ff1159bb8adac6c4dbf1b4b
npm test
(cd src-tauri && cargo test --offline --locked)
```

`npm test` validates actual Rust outputs against canonical Design schemas,
without reference rewrites. Rust tests also check runtime refusal, capture
failure/recovery, ordering, namespace and provenance negatives. With no supplier
binary, set `CHIRALITY_SKIP_CODEX=1` explicitly for Rust checks; the Node hosting
check then reports its skip. Skipped checks establish no supplier result.

The handshake uses its own unique system-temp home, a local provider at
127.0.0.1 port 9, plugins off and analytics off. It starts no model turn, supplies
no credential, and checks its sampled process-group sockets. Test-owned scratch
files are cleaned after consumers finish.

## Run the development App

Set `CHIRALITY_WORKSPACE`, `CHIRALITY_CODEX_BIN` and a scratch
`CHIRALITY_CODEX_HOME`; never use `~/.codex` for development. A matching binary
hash is a development assertion. Full qualified distribution identity is absent,
so the development run requires `CHIRALITY_ALLOW_UNVERIFIED=1` and is labelled
`unverified-development` (LT-24); mismatches still refuse.

Make the workspace and Codex home with `mktemp -d`, and use their physical paths
(`cd <directory> && pwd -P`) because protected store paths reject symlink
ancestry. Put this stand-in configuration in the scratch home's `config.toml`:

```toml
model_provider = "skeleton_local"
model = "skeleton-no-model"
[model_providers.skeleton_local]
name = "Offline development stand-in"
base_url = "http://127.0.0.1:9/v1"
wire_api = "responses"
[features]
plugins = false
[analytics]
enabled = false
```

Copy the maintained `tests/fixtures/FX-DP1/project/decisions` files into the
scratch workspace's `project/decisions/`, then run `npx --offline tauri dev`.
For the offline thread exercise, enter model `skeleton-no-model` and provider
`skeleton_local` explicitly. These are test choices, not product defaults.
Open a package, choose an alternative and confirm its full native text.
Authenticated/live model work remains coordinated with the owner.

For stored history, choose **Read stored conversations**, then select a received
conversation. **Read metadata**, **Read turns**, **Read goal**, and per-turn item
controls read disposable native pages; opaque page cursors belong to their
received stream. **Continue selected conversation** separately requests native
resume before permitting operational text input. It keeps the conversation’s
existing guidance/settings and does not resend automatically. Original App role
evidence is shown only when retained in this process; a cold restart shows
Unknown. Reading child metadata does not supply a child role.

The decision view reads recorded claims without writing. Use **Continue pending
recording and record new requests** for explicit writer continuation; startup
also invokes that separate writer responsibility. Incomparable current claims,
conflicting record IDs and incomplete lapse histories remain visible, with each
source and time preserved. Reading a claim does not verify its native origin.

## Storage and remaining work

Project run logs use `.chirality/records/runs/<safe-run-key>/<safe-writer-key>.jsonl`;
outside-run acts use `.chirality/records/acts/<safe-writer-key>.jsonl` with captures
in `.chirality/captures/`. Library A15 allocation uses the library's
`.chirality/records/acts.jsonl` and `.chirality/captures/`; the A15 product journey
remains later Group A work. Storage keys are separate from governed identities.
Explicitly discovered legacy `records/coordination.rs.jsonl` stays intact.
Unwritable or incomplete targets report limits without silent relocation.

Trustworthy persistent cold replay and SEAL-2 remain unfinished under CI-10 and
I3-CUST. Current code refuses unverified replay while preserving evidence.
Native authenticity, real process-kill/fsync failure witnesses, durable history
rebuild and cold role-source reconciliation, child role supply, per-home configuration linking, other
act kinds and actual policy/standing control/reader joins remain in the Group A
graph. Full workflow parsing awaits the exact CommonMark dependency decision;
the handwritten subset is not production-complete. External dispatch and host
qualification remain unsupplied. Native text-turn and interrupt controls use the selected native thread and
retain generation/terminal limits. Transport and receiving tests do not prove a
provider prediction. A separately frozen controlled live backend greeting passed;
its exact source pins and limits are recorded in the run. Physical App UI/IPC
smoke remains a separate unfinished witness. Host joins stay deferred to their owning sessions.

See `CONTRACT_ISSUES.md`, `EVIDENCE.md` and the current Group A `WORK_GRAPH.md`.
