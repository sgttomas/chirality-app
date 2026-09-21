# D-GOV-43 supplement — host topology selected: A2, application-owned Runtime service

Status: `RECORDED 2026-09-12` — supplements `D-GOV-43_codex_host_replatform.md`
(ruled 2026-09-11); that record is not edited

Date: `2026-09-12` (America/Edmonton)

Basis: the ruled record; `projects/chirality-app-dev/execution/_Coordination/AgentRuns/APP_V3_CODEX_HOST_REPLATFORM_20260912/TOPOLOGY_COMPARISON.md`
(source comparison of three topologies, with its section 8 addendum and
corrections); two rounds of the independent reviewer's feedback relayed by
the owner on 2026-09-12.

## What was reopened and why

After ruling, the owner reopened ruling items 1 (hosting) and 7 (daemon
retirement) on the independent reviewer's counter-proposal, which showed
that the observed failures established defects in Chirality's Codex
integration and transport, not that a host service, adapter or normalized
event model is inherently wrong. The owner added that the same agents and
agent host are intended for embedding in later Chirality applications
(first Chirality Piping, a Tauri application) with local models, deferred.

## Owner decision (verbatim)

Owner Ryan Tufts, 2026-09-12 (America/Edmonton), after the comparison and
the reviewer's concurrence:

> We are all in agreement this is the path forward. You will be handing
> this off so a third agent can begin implementation.

The path is topology **A2** of the comparison: the Runtime host is retained
as a simplified service that the Chirality App starts, owns and stops as a
child process, speaking the existing socket API; the private Codex
integration is replaced with stock Codex; the admission, supplier and
launchd machinery is retired.

## Effect on the ruled items

- **Item 1 (Hosting)** is re-expressed: the App owns a Runtime service child
  process, and that service owns the stock, version-pinned `codex app-server`
  child. Everything else in item 1 stands (lockfile pin, no patched
  supplier, ordinary software integrity, no admission re-created).
- **Item 7 (Daemon retirement)** is re-expressed: retired are the LaunchAgent
  and its installer, the supervisor's second socket and job, hosted admission
  and identity binding, packaged-basis hashing, the native admission addon,
  the host-account XPC channel and restart admission. Retained are the
  Runtime service composition (core services, Codex session, supervisor and
  login modules), its Unix-socket API with client tokens private to the
  application, and the client, port and routes, all repaired per the
  comparison. No network-exposed listener is introduced.
- **Item 2 (Faithful transport)** is read to its purpose rather than its
  Electron-specific wording: one long-lived channel with validated shapes,
  `contextIsolation`, no credential material in the renderer, and no idle
  timeout that ends a turn. The App's renderer channel is loopback HTTP and
  SSE through the in-process Next server; the service's public face is the
  socket API. The notification and server-request rules of item 2 stand.
- **Item 13 (Local models)** is refined: Codex reaches local models through
  model providers; what later applications would share is an inference
  server, a separate per-user concern from the Codex host, subject to memory
  and capability qualification when taken up. Prior Pi and oMLX work is
  preserved in history and reference; preserving it creates no obligation to
  keep unused implementations compiling.
- Items 3 to 6, 8 to 12 and 14 stand as ruled, including the post-build
  minimum-not-ceiling clarification. The `AGENTS.proposed.patch` wording
  "owned by the App's own host process" is read as the application-owned
  Runtime service.

## Cross-product constraint recorded now

> Keep the Runtime host independent of Electron and Next and consumable as an
> application-owned service. Chirality App is the only implementation and
> qualification target for this tranche; Piping integration and local-model
> management remain deferred.

## Implementation clarifications carried into the handoff

1. Retaining the contracts package does not retain its restrictive event
   vocabulary: an extensible representation preserving upstream method
   names, identifiers and payloads, normalized views for known items,
   unfamiliar notifications inspectable, unfamiliar server requests answered
   explicitly without implying approval.
2. Execution is separate from observation: the Runtime owns the active turn;
   a browser subscription observes it; reopening after a renderer disconnect
   recovers current state, missed activity and outstanding decisions without
   re-sending the prompt or executing twice; a renderer disconnect during
   tool work is a continuity check.
3. Application shutdown is explicit: closing or hiding a window differs from
   quitting; quit stops the owned Runtime and Codex processes deliberately
   with an accurate continuation record; unexpected termination is never
   presented as completion; no unattended execution after quit is promised.

Reuse is assessed by behaviour, not line counts; "A2 needs less new code"
is an estimate. PEC's integration opportunity is preserved, its
compatibility unverified and not an MVP prerequisite.

## Application boundary

Unchanged from the ruled record except as re-expressed above. The
coordinated application tranche, the functional spike against the eight
checks, independent source review before one consolidated signed build, and
the owner's native verification proceed on this basis. No release,
publishing, Piping integration or local-model work is authorized.
