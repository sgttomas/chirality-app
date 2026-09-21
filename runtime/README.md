# Chirality Runtime

This workspace contains the Chirality Runtime service: the session store, turn
coordinator, delegated-runtime coordination, Codex supervisor and login
modules, the authenticated Unix-socket API, its typed Node client and the
`chirality` CLI.

Under D-GOV-43 (ruled 2026-09-11) and its topology A2 supplement (recorded
2026-09-12) the Runtime is an application-owned service. The Chirality App
starts, owns and stops it as a child process; the service owns the stock,
version-pinned `codex app-server` child. The App is the only production
consumer. The Runtime stays independent of Electron and Next so a later
Chirality application can run it as a sidecar. Piping integration and local
models are deferred.

## Architecture

- **One process.** The standalone entry `chirality-runtime-service` composes
  `RuntimeService`, `SessionStore`, `TurnCoordinator`, `DelegatedRuntime`,
  `CodexSupervisor` and `CodexLogin` in a single application-owned mode and
  prints a JSON ready line on stdout once the socket is listening. There is
  no supervisor job, second socket, admission step or native addon.
- **Socket API.** The service speaks its existing HTTP/1.1 and SSE API over a
  Unix domain socket. Client tokens are private to the owning application.
  No TCP or other network-exposed listener is introduced.
- **Stock Codex.** The service launches the official `@openai/codex`
  `codex app-server` over stdio, pinned by the package manifest and lockfile.
  Updating the pin is an ordinary dependency update with re-validation. No
  patched or privately extended supplier, admission, payload hashing or
  identity binding exists.
- **Effective Codex home.** Codex runs against a Chirality-owned effective
  home that shares the user's configuration and resources by reference
  (config, skills, plugins, MCP definitions, instruction caches, sessions)
  and keeps authentication private (`auth.json` and the models cache).
  Sign-in and sign-out use Codex's own account methods inside that home; the
  Runtime never reads, copies or relays credential material. There is no
  effective-configuration veto.
- **Faithful stream.** The complete App Server notification and
  server-request stream is carried through with upstream method names,
  identifiers and payloads preserved. Every server request receives a
  response; an unfamiliar request receives an explicit JSON-RPC error and a
  visible "unsupported request" outcome, never an implied approval.
- **Continuity.** The Runtime owns the active turn; a client subscription
  observes it. A closed client connection does not interrupt the turn.
  Explicit Stop is the interrupt endpoint. Thread persistence, resume, fork
  and compaction come from Codex; the service keeps its own session index.
- **Interruption versus retirement.** Interrupting a turn and finally
  retiring a worker are distinct operations. Both paths join one
  exact-generation retirement result, and foreign or stale generations are
  rejected. The interrupt-versus-retirement defect recorded in PR #767 is
  repaired in the lifecycle code with a deterministic regression.

## How the App owns the child

The App spawns `chirality-runtime-service` with a private configuration,
waits for the ready line, connects `RuntimeClient` with a per-launch token
kept under its user-data directory, restarts the service with backoff on
crash, and stops it deliberately on quit. Closing or hiding a window is not
quitting. Unexpected termination is never presented as completion; the
session store carries an honest continuation state for reopening.

## Application-owned tools

An owning application can register dynamic tool descriptions before a new
conversation starts, receive calls through the authenticated host API, and
return results. The catalog is immutable for that conversation; handlers
explicitly rebind after restart. Runtime supplies transport and lifecycle while
the application owns argument/domain validation, live state and human acceptance.
See [Application tools](docs/APPLICATION_TOOLS.md) for the interface and limits.
SWBPIPE client adoption and its live domain adapter remain separate work.

## Development

Requires Node.js 22.19 or newer.

```sh
npm ci
npm run typecheck
npm test
npm run build
```

The integration tests use temporary Unix-domain sockets. Sandboxed runners
must permit local socket creation. `software-workflow.json` registers
`npm run typecheck` and `npm test`. A test runs once per distinct condition.

## Packages

- `@chirality/runtime-contracts`: session, project, protocol and delegated
  types. The extensible event representation preserves upstream names and
  payloads with normalized views for known items.
- `@chirality/runtime-core`: `RuntimeService`, `SessionStore`,
  `TurnCoordinator`, `DelegatedRuntime`, process supervision and descendant
  tracking.
- `@chirality/runtime-daemon`: the socket server, `CodexSupervisor`,
  `CodexLogin`, the Codex session and the `chirality-runtime-service` entry.
- `@chirality/runtime-client`: typed Node client for the socket API.
- `@chirality/runtime-cli`: the `chirality` command surface, a client of the
  socket API.

PEC's integration opportunity through the client is preserved; its
compatibility is unverified and is not an MVP prerequisite.

## Retirement note (D-GOV-43, A2)

Retired from this workspace: the per-user LaunchAgent and installer, the
supervisor's second socket and job, hosted admission and identity binding,
packaged-basis hashing, the native admission addon, the host-account XPC
channel, restart admission, the exact-supply pin with drift refusal, the
supplier patch, build recipe and provenance, the conformance limbs, the nine
held release bindings, the configuration veto, the notification whitelist and
quarantine, the closed event union v2, the continuity gate on
`thread/resume`, the per-chat model and effort freeze, and local-model
residency. Nothing is re-created under another name; ordinary software
integrity (lockfile-pinned dependencies, application signing, request and
session correctness tests) replaces it.

`tools/codex-supplier/`, `tools/native-admission/` and
`tools/provision-hosted-release-anchor-v2.mjs` were deleted in the
application tranche. Their last commit in this repository is `e83cb1f47`.
`docs/CODEX_MVP_INTEGRATION.md` is superseded by the App's host design. The
historical run records under `execution/_Coordination/AgentRuns/RUNTIME_*`
are preserved unchanged.

## Reference

Prior local-model work is preserved as reference without release
obligations. Live local Pi validation completed actual
client-to-daemon-to-Pi-to-oMLX inference, a bounded read and the expected
final marker; both the pre-admitted child limb and the coordinator-created
child limb passed, the latter verifying durable parentage and required review
through an explicitly controlled manager port. That composition used the
`local-engine-only` configuration with Pi 0.82.0 against a loopback oMLX
endpoint and resident model; it did not load or unload models or choose a
fallback. When local models are taken up they will be reached through Codex
model providers; preserving these records creates no obligation to keep
unused implementations compiling.
