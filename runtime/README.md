# Chirality Shared Runtime

This workspace contains Chirality's provider-neutral runtime contracts,
orchestration core, headless daemon, authenticated Unix-socket client, CLI, and
safe engine adapters.

The daemon is the sole owner of engines, credentials, sessions, delegation,
turn locks, interruption, tools, and local-model residency. Desktop, CLI, and
project integrations are clients. Runtime state is operational and
non-authoritative; project manifests and governed execution records remain in
their registered repositories.

## Development

Requires Node.js 22.19 or newer.

```sh
npm ci
npm run typecheck
npm test
npm run build
```

The integration tests use temporary Unix-domain sockets. Sandboxed runners
must permit local socket creation; no TCP control listener is used.

## Packages

- `@chirality/runtime-contracts`: public events, sessions, projects, residency,
  and protocol types.
- `@chirality/runtime-core`: project/session registries, turn coordination,
  governed delegation, and residency control.
- `@chirality/runtime-daemon`: authenticated HTTP/1.1 and SSE over a Unix
  socket.
- `@chirality/runtime-client`: typed Node client for that Unix socket.
- `@chirality/runtime-cli`: the `chirality` command surface.
- `@chirality/engine-claude` and `@chirality/engine-pi-omlx`: host-injected
  engine adapters. Pi/oMLX is loopback-only and accepts no ambient Pi
  configuration.

The Electron composition root supplies encrypted provider credentials and the
concrete embedded engines when it starts with `--runtime-daemon`.
