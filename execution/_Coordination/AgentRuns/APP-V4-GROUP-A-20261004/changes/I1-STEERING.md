# I1 native text steering transport — 2026-10-05

TASK `/root/group_a_execution/runtime_core_production`, parent `/root/group_a_execution`; native descendant, no delegation. Parent released this bounded production against accepted independent steering path. Writes only hosting.rs inline production/tests and this record. NativeHistory successor, shared lib/UI/runtime_session/lifecycle, Design/schemas and dependency manifests unchanged; no Git, actual supplier/model turn, credentials/auth/network/download or key action. Env-cleared /bin/cat is reaped after each actual pipe test.

## Frozen API and native basis

```rust
pub fn turn_steer_text(&self, generation: &Value, thread_id: &str,
    expected_live_turn: &str, text: &str) -> Result<Value, String>;
```

Maintained 0.160.0 `codex_app_server_protocol.schemas.json`, definitions/v2/TurnSteerParams requires threadId, expectedTurnId and input; expectedTurnId is the active-turn precondition. TurnSteerResponse requires turnId. The UserInput text variant carries unchanged text and text_elements. HOSTING HCG-B03 lists turn/steer as native turn control. The run ATTACHMENT_DECISION_PREPARATION.md independent steering paragraph preserves the required observed expectedTurnId and no fallback start; text-only steering has no attachment/lifetime prerequisite.

The exact outbound body is `{threadId,expectedTurnId,input:[{type:"text",text:<unchanged>,text_elements:[]}]}`. Empty identities/text refuse. No role/base/config/model/provider/approval/sandbox/collaboration override; selected native thread retains its settings. No renderer actor argument; existing fixed person-directed routing metadata is not identity verification or human_act evidence.

Full H5 generation is validated before scoped dispatch. Known current-generation/home thread and current live expected turn are checked under registration lock before actual source-pipe acquisition/write. TerminalEventObserved and observationEnded independently exclude an active-looking payload. Existing scoped sender binds the source pipe with registration, retaining write/wait/correlation uncertainty. There is no fallback turn/start and no automatic resend.

The live target is a source-bound reading of latest turn/started/completed frame plus memo lifecycle. Start responses record the receipt position preceding their actual dispatch; a delayed prior start response cannot displace a newer event target. A sole fresh response-only start can establish a target, including a distinct new turn after a completed event. Multiple ambiguous fresh response-only targets refuse. Raw native frames and memo inconsistency limits retain their original authority; no transcript cache or native evidence rewrite.

At wrapper consumption, full generation/open/ready and live expected target are rechecked. Native errors retain exact raw data. A reported turnId different from expected refuses without rebinding. A target changed/ended or tuple changed after receipt returns an explicit refusal with received native response/client correlation retained. Steering acknowledgment neither edits nativeTurn nor proves turn end, rollback, run end, model prediction or supplier qualification. Shared UI integration and actual supplier witness remain separate obligations.

## Actual checks

Manager granted exclusive Cargo slot; cwd app/src-tauri; `CARGO_HOME=/tmp/chirality-app-v4-group-a-cargo-home`.

| Command | Actual result |
| --- | --- |
| `cargo test --offline --locked --lib steering_` | exit0; 5 passed,0 failed,0 ignored;2.62s compile,0.07s tests |
| `cargo test --offline --locked --lib conversation_transport_tests` | exit0;14 passed,0 failed,0 ignored;0.06s tests |

Five new checks exercise actual ChildStdin/correlation: exact Unicode/newline body and unchanged generated params/response schema; live ack retaining native state/settings; stale expected/terminal marker/foreign full tuple/unknown thread/closed zero registration; native mismatch/error/data, failed write, wait and late response; changed target/terminal/session/home/counter between receipt and wrapper consumption; delayed prior start response versus newer native started target plus fresh distinct response-only start control. The prior nine conversation oracles are preserved and pass. No failed run or test weakening. Syntax-only rustfmt emit-to-stdout passed without rewriting source. Cargo released promptly after the two runs.

Source/API frozen for independent affected review before shared consumption. NativeHistory remains unchanged at its prior 63b735 successor. This is source/transport evidence, not actual stock/native/provider qualification or full NIR support.

## Frozen seals

| Subject | SHA-256 |
| --- | --- |
| `hosting.rs` | `d20d8ef399911f49f4604fa9530703c91a1f83cf0885e9609885dd12e39f6c75` |
| `conversation_transport_tests` | `00608f2f8d80a257f48fa32298e14693bff8a8ffab823c266a8ba14e006b28bf` |
| `conversation methods/helpers` | `44822287a8f472ac7db9cb42daf73a80cbb632838e95eada06b9f7031abcacbe` |
| `native_history.rs` | `63b7358679a14244e18125f52fcd0bcbe319240463a944219de9b5016c8fe613` |
| `native schema bundle` | `7243ba241962af92ca60581f1a81808ebda4212a800f8b205f54703bcfd508c5` |
