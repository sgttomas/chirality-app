# Local Responses fixture backend smoke (stock Codex 0.160)

## Purpose and standing

This is a parent-gated backend integration probe. It drives the **real** pinned
stock Codex 0.160 app-server through the App's production `Host` and
`RuntimeSession` path without any model, credential or owner Codex home. The model
side is a **deterministic loopback Responses fixture** that returns canned SSE; it
is not inference.

The probe checks that the supplier contract works end to end against an anonymous
local provider defined exactly as the App defines one (`provider_create.rs`:
`{name, base_url, wire_api = "responses", requires_openai_auth = false}`):
- startup;
- conversation start with role guidance;
- one send, reaching a completed turn with the exact reply;
- history read-back;
- normal stop and descendant cleanup.

It is **not** model, J1/J2, native GUI or release qualification, and it says
nothing about real model behaviour. The existing authenticated cloud test is a
separate gate and is unchanged in meaning.

## Invocation (opt-in only; CI never runs it)

`app/src-tauri/tests/native_backend_smoke.rs`, test
`parent_authorized_stock_native_local_responses_fixture`, which is `#[ignore]`.

- **Gate.** `CHIRALITY_RUN_NATIVE_BACKEND_SMOKE=parent-authorized-0160-local-responses-fixture`.
  It is distinct from the cloud gate `parent-authorized-0160-one-greeting`.
- **Input.** `CHIRALITY_NATIVE_SMOKE_BIN` is the absolute path to the stock Codex
  binary, pinned to SHA-256 `112fae7a…`. There is no auth-home, provider, model or
  credential input.
- **Codex home.** The test creates a fresh 0700 Codex home inside its own `0700`
  scratch root, with `config.toml` naming the invented model
  `chirality-fixture-model` and the provider `chirality-smoke-local`. The provider's
  `base_url` is the fixture on an ephemeral `127.0.0.1` port.
- **Environment.** Credential variables are stripped from the Codex child by the
  existing spawn (`CREDENTIAL_VARS`). Running the test binary under `env -i` keeps
  the parent environment out as well.
- **Network and owner data.** Run the test binary under a localhost-only
  `sandbox-exec` profile, `(deny network*)` plus loopback allows, also denying
  owner `~/.codex` reads and writes, with a bounded alarm, inside a `t3_slot`.

## What it asserts

The flow and checks are shared with the cloud test (`run_one_greeting`):
- the `codex-cli 0.160.0` label;
- a `configured` recovery startup;
- start-request binding of the dispatched guidance;
- the original role binding (`HELP_HUMAN`, adoption not established);
- the native-side prompt observation;
- strict refusal of foreign items or server requests;
- a `completed` terminal with the **byte-exact** reply (exact because the fixture
  is deterministic);
- exactly one `session_started` recovery entry with no prompt or reply text;
- normal stop with zero surviving descendants.

The local route adds:
- **Destination.** `thread/start` reports the fixture model and provider. Reasoning
  effort is recorded, not required.
- **History.** A read-back through the public path: `NativeHistory`
  list, select, turns and items, then `Host::history_dispatch` and `history_wait`,
  with the view's own `receive` validation. The checks are that the thread is
  listed, the turn is `completed`, and the turn's items contain the exact prompt
  `userMessage` and the reply `agentMessage`. Items arrive wrapped as
  `{item, turnId, …}`.
- **Fixture traffic.** At least one Responses request reached the fixture; every
  request was a parsed loopback request; every Responses request carried the
  fixture model, `stream: true` and an uncompressed complete body; and the prompt
  was present. Other requests are listed by method and path only.

The fixture keeps request facts only, never request bodies. A non-ignored unit test
(`local_responses_fixture_answers_canned_sse_and_records_request_facts`) covers the
fixture alone in CI.

## Shared-flow repair

The shared flow read the recovery ledger as `runtime/recovery.ledger.jsonl` bytes.
Current recovery storage is database-backed (`recovery::database_path`), so that
file is no longer written. Both routes now read the entries through the running
host's own handle, `Host::recorded_recovery_entries()`, with the same assertions.
The cloud test would have failed at this point against current source; its gate,
inputs and other assertions are unchanged.

## Observed run (2026-11-04)

- **Source.** Main `fe811788` plus this branch; stock binary `112fae7a…`.
- **Context.** Run under the localhost-only sandbox, `env -i`, a 180 s alarm and
  `t3_slot`; the result was `ok` in 3.6 s.
- **Supplier.** Supplier `codex-cli 0.160.0`; reported model and provider
  `chirality-fixture-model` / `chirality-smoke-local`; reported reasoning effort
  `null`; terminal `completed`; reply exact.
- **History.** Read-back found the thread listed, the turn completed, and 2 items:
  the prompt and the reply.
- **Fixture.** 1 Responses request, all from loopback, and no other requests.
- **Ledger.** 1 `session_started` entry with no conversation text.
- **Cleanup.** Normal stop with 0 surviving descendants. The scratch root was
  removed, and no Codex process remained.

## Later change

The fixture now lives in `app/src-tauri/tests/support/responses_fixture.rs`, so
that [LOCAL_RESPONSES_WORKFLOW_FIXTURE.md](LOCAL_RESPONSES_WORKFLOW_FIXTURE.md)
can share it. This route's script is its one canned message, and its prompt
fact is now read as `markers.prompt`. The route was re-run on 2026-11-04 on
`98722981` plus that branch: `ok`, 3.58 s.

## Limits

These are deterministic fixture results only. Compatibility with any real local
model server, actual model output, tool or approval behaviour, network behaviour
outside the sandbox, and GUI first-screen behaviour (see the separate dev-candidate
diagnosis) are not established. No endpoint, model, credential, signing identity or
owner state was used.
