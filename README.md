# Chirality

Chirality gives project teams a disciplined way to use AI for real production
work without giving up the controls that make professional work reviewable,
coordinated, and defensible.

It is a macOS workspace for delegating structured knowledge work to AI agents.
An agent is best understood as a capable but unfamiliar team member: it can
follow instructions, read assigned material, use permitted tools, and return
work, but it needs a clear brief, defined authority, and competent review.

Chirality provides that working environment. It connects conversation to
project files, organizes agents into supervised roles, limits what they can
access and change, and keeps a record of how work was produced. Agents do the
legwork. People decide what can be relied upon.

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

## Getting Started

Full interactive agent work currently requires an Anthropic API key supplied
by the user. The credential is application state and is not written into the
selected project folder. Model usage remains under the user's provider
account.

For a first working session:

1. Open **Runtime & credentials** and enter the Anthropic API key.
2. Select a **Working Root**: the project folder Chirality may use for the
   session.
3. Select the supervising or managing agent appropriate to the assignment.
4. Begin with a brief that identifies the objective, available information,
   constraints, required return, and intended reviewer.

The quality of the delegation still matters. A short, well-bounded assignment
with known inputs and a reviewable output is a better starting point than an
open-ended instruction to take over an entire project.

## From a Brief to Reviewable Work

Consider a familiar assignment: a package of work has a defined objective,
reference material, interfaces with other work, required outputs, and a
reviewer who remains accountable for the result.

In Chirality, you can approach that assignment much as you would with a human
team:

1. You state the objective, governing information, constraints, and required
   return.
2. A supervising or managing agent organizes the work and delegates bounded
   assignments where appropriate.
3. Specialist agents research, compare, draft, check, or reconcile within
   their assigned scope.
4. Their outputs return with the available evidence and execution record.
5. You review the work, resolve matters requiring judgment, and accept,
   revise, or reject the result.

The value is not simply that several agents can work at once. The value is
that delegation remains traceable: who did what, against which brief, with
what access, producing which return, for whose review.

## Familiar Responsibilities, New Participants

The agent roles in Chirality resemble a project organization, but they do not
inherit human accountability.

| Familiar responsibility | Chirality counterpart |
| --- | --- |
| Accountable project or professional lead | The human who sets direction, reviews evidence, accepts risk, and authorizes reliance |
| Project coordinator or supervising lead | A supervising agent that aligns the objective and coordinates managers |
| Package, discipline, or functional manager | A manager agent that plans bounded work, briefs specialists, and integrates their returns |
| Analyst, researcher, drafter, or checker | A specialist agent that executes one defined assignment |
| Standard procedure, calculation routine, or checklist | A reusable agent method or repeatable tool |
| Controlled project record | The project files and version history selected by the user |

Agents may prepare and propose. They do not become the project authority,
discipline lead, engineer of record, approver, or issuer.

## Work Chirality Is Designed For

Chirality is intended for deliverable-heavy work in which outputs must remain
connected to scope, sources, dependencies, review, and decisions. Depending on
the agents and methods selected, it can help teams:

- break a scope into packages, deliverables, and bounded assignments;
- organize a working folder and prepare repeatable document structures;
- research source material and produce evidence-linked findings;
- draft specifications, reports, procedures, registers, and other working
  documents;
- identify missing inputs, unresolved interfaces, contradictions, and
  dependencies;
- compare and reconcile information across related deliverables;
- support estimating, scheduling, review, and change-impact work; and
- run repeatable checks and mechanical transformations with tools.

These are production and decision-support activities. Chirality does not
certify compliance, authenticate professional judgment, or issue work for
reliance.

## A Workroom, Not a Chatbot

Dialogue is where people establish intent, explain context, test an approach,
and exercise judgment. Chirality keeps that dialogue central while separating
it from the durable project record.

- **Dialogue** records the working conversation.
- **Runtime history** records what agents and tools did.
- **Project files** contain the work and decisions the team intends to carry
  forward.

The distinction matters. A persuasive answer in a chat window is not the same
thing as reviewed project work. When information matters for later reliance,
it should be placed in the appropriate project file and accepted through the
team's review process.

The desktop workspace brings the live dialogue together with project files,
recorded work, agent relationships, tool activity, and read-only replay of
past sessions. These views help the user inspect the work; they do not silently
create plans, approve changes, or convert an agent's conclusion into project
truth.

## What Remains Under Human Control

Chirality is built around several practical controls:

- **Defined scope.** Agents work from instructions, declared context, and
  checkable outputs rather than unrestricted mandates.
- **Controlled access.** Read, write, tool, shell, network, and delegation
  capabilities are governed separately and can be denied.
- **Visible basis.** Sources, assumptions, unknowns, conflicts, and produced
  artifacts can remain available for review.
- **Reviewable changes.** Project work stays in ordinary files that can be
  inspected, compared, archived, and recovered.
- **Recorded execution.** Sessions can record accepted turns, tool use,
  permission decisions, interruptions, failures, and delegated work.
- **Human acceptance.** Agents cannot make their own drafts authoritative or
  approve consequential actions on a person's behalf.

Project truth remains in user-selected files with a reviewable version history,
rather than in model memory, application caches, or a vendor-hosted project
database. The working record therefore remains inspectable outside Chirality.

## Models and Local Operation

Chirality keeps its project, permission, session, and governance rules separate
from the company or local server supplying the AI model.

In the current release, Anthropic is the primary provider for full interactive
agent work. The local Pi/oMLX path is an opt-in, deliberately bounded
capability for one supervised, read-only specialist assignment. It does not
currently offer the same capabilities as the Anthropic path and is not an
automatic fallback.

The application runtime operates locally on the Mac. Provider requests leave
the machine when a cloud model is used. The supported local-model connection
is restricted to an authenticated oMLX service running on the same Mac.

## Professional Boundary

Chirality does not transfer professional responsibility to an AI system.
Generated material must be reviewed against the governing project record,
applicable requirements, and the responsible human's acceptance criteria.

The user remains responsible for:

- selecting the governing basis and appropriate source material;
- deciding whether an agent is suitable for the assignment;
- reviewing work to a standard appropriate for its intended use;
- resolving conflicts, uncertainty, and matters requiring professional
  judgment; and
- approving, issuing, or relying upon project work.

Chirality is useful when the person delegating the work is capable of
reviewing the return.

## Repository Contents

This repository contains the Chirality files approved for public distribution
and hosts the downloadable desktop releases.

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

Provider credentials, runtime sessions, machine paths, and model-residency
state are local operational data. They are not part of this repository and do
not replace versioned project authority.

## License

MIT License + Professional Engineering Clause. See [`LICENSE.md`](LICENSE.md).

Copyright (c) 2026 Ryan Tufts
