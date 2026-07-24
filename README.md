# Chirality

Chirality is a governed macOS application environment for agent-assisted,
deliverable-heavy professional work. It combines a desktop workspace, a
filesystem-native agent operating system, deterministic tools, explicit human
gates, and durable evidence so machine output is not confused with
professional authority.

> AI may extend reckoning; it must not inherit judgment.

## Download Chirality for macOS

Download the signed and notarized installer from the
[latest GitHub release](https://github.com/sgttomas/chirality-app/releases/latest).

System requirements:

- Apple Silicon (`arm64`)
- macOS 15 or newer

The release contains:

- `Chirality-<version>-arm64.dmg`
- `Chirality-<version>-arm64.dmg.sha256`

To verify the download, place both files in the same directory and run:

```sh
shasum -a 256 -c Chirality-*-arm64.dmg.sha256
```

Then open the DMG, drag Chirality to Applications, and launch it normally.
The installer is signed with a Developer ID certificate, accepted by Apple
notarization, and distributed with a stapled notarization ticket.

## What Chirality Does

Chirality is designed for work where outputs need scope, provenance,
coordination, review, and explicit human acceptance.

Its core ideas are:

- **Filesystem-native workspaces.** Project files remain the durable source of
  truth rather than chat history or model memory.
- **Governed agent roles.** Supervising, managing, and specialist agents work
  within declared authority, read/write boundaries, and acceptance checks.
- **Deterministic operations.** Repeatable tools perform mechanical work while
  semantic judgment remains visible and reviewable.
- **Human authority.** Agents can propose, draft, reconcile, validate, and
  report. Humans approve, accept risk, and issue work for reliance.
- **Provider-neutral runtime.** Desktop and CLI clients communicate with a
  local runtime over an authenticated Unix-domain socket. No TCP control
  listener is exposed.

## Repository Contents

This repository is the sanitized public Chirality source boundary.

| Path | Contents |
| --- | --- |
| `runtime/` | Shared runtime contracts, daemon, client, CLI, and safe engine adapters |
| `agents/` | Agent instruction contracts and role definitions |
| `skills/` | Reusable, bounded method packs |
| `tools/` | Deterministic utilities and validation tools |
| `docs/` | Architecture, governance, contracts, specifications, and roadmap |
| `init/` | Public session bootstrap guidance |

The desktop application source is not currently included in this public
export. The downloadable desktop application is produced from a separately
maintained app-development workspace and published here as a signed,
notarized release asset. The public repository does not contain credentials,
machine registration state, downloaded models, private project workspaces, or
local runtime data.

## Working with the Public Runtime

The shared runtime requires Node.js 22.19 or newer:

```sh
cd runtime
npm ci
npm run typecheck
npm test
npm run build
```

These commands validate and build the shared runtime. They do not build the
desktop application.

See [`runtime/README.md`](runtime/README.md) for runtime architecture and
development details. Start with [`AGENTS.md`](AGENTS.md) and
[`docs/DIRECTIVE.md`](docs/DIRECTIVE.md) for the agent and governance model.

## Professional and Security Boundary

Chirality does not transfer professional responsibility to an AI system.
Generated content must be reviewed against the governing project record,
applicable standards, and the responsible human's acceptance criteria.

Provider credentials, runtime sessions, machine paths, and model-residency
state are local operational data. They are not part of this repository and do
not replace versioned project authority.

## License

MIT License + Professional Engineering Clause. See [`LICENSE.md`](LICENSE.md).

Copyright (c) 2026 Ryan Tufts
