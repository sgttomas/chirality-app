# Chirality App

Start a conversation with Help Human, the assistant in Chirality App. Work out
what you need, make a plan when it helps, and carry out the work together. Turn
a useful plan into a workflow for next time.

[Download Chirality App](https://github.com/sgttomas/chirality-app/releases/latest) · [Website](https://chirality.ai) · [Release announcement](https://chirality.ai/announcements)

## Use the App

Bring a task such as a monthly update, a proposal, an investigation, or a review.
Help Human can organize references, prepare work, and help you check it. You can
select a workflow from the library or ask it to turn your plan into one. Return
to the conversation to reuse and refine the method as your work changes.

You direct the work and decide what is ready to rely on. Use review appropriate
to its consequences.

## Get the App

- **Current release:** [v3.0.1](https://github.com/sgttomas/chirality-app/releases/tag/v3.0.1),
  published 2026-09-20 as `Chirality-3.0.1-arm64.dmg` with its SHA-256 checksum.
  App v4 is [in development](#develop-the-app) and does not replace v3.0.1
  until a separate release decision.
- **Requirements:** an Apple Silicon Mac with macOS 15 or newer, and a ChatGPT
  account. The App uses Codex through your account. Local-model support is
  planned for a later release.
- **Your data:** saved plans, workflows, references, and outputs are ordinary
  files in your folders. Plans stay in conversation history unless you choose
  to save them to a file. You can keep and use them outside the App. Task
  content needed by the model is sent to OpenAI using your account; Chirality
  AI Ltd does not proxy or retain that content. See
  [installation and data handling](https://chirality.ai/deployment).
- **Issues:** [report an App issue](https://github.com/sgttomas/chirality-app/issues/new).

App v3 is frozen and no longer developed or verified;
[Frozen products](https://github.com/sgttomas/chirality/blob/main/projects/FROZEN.md)
explains source recovery.

Built on [Chirality](https://github.com/sgttomas/chirality)'s principles, roles
and workflows.

## Develop the App

**Development resumed by owner direction on 2026-10-28.** App v4 has moved here
from Chirality. The migration does not publish or qualify a v4 release; the
existing v3.0.1 release remains the fallback.

The [current release pathway](execution/_Coordination/CURRENT_EXECUTION_BASIS.md#current-release-pathway)
targets the full public v4 release with the live embedded SWBPIPE journey.
It identifies delivery owners, next results and the evidence still needed.

Chirality makes a general agent act within and for a host application. Its
workflow-authoring App is the exemplar. [Chirality thesis](https://github.com/sgttomas/chirality/blob/main/docs/thesis/README.md)
develops the reasons for its form; product commitments are in the [PRD](docs/PRD.md),
its companions and the deliverable Scopes of Work and Designs.

Development enters through the [App v4 loop](loop/LOOP_INIT.md). Deliverables live
in `execution/PKG-nn/DEL-nn-nn/`: `ScopeOfWork.md` holds commitments and acceptance
criteria, `Design/` holds contracts and open implementation conditions, and
`deliverable.yaml` states needs and code/check pointers. Query their inputs and
consumers with the [deliverables tools](tools/deliverables/README.md).
For the toolchain, build and launch instructions, start with the
[App developer start](app/README.md#developer-start). The rest of that README
describes the current product path, checks and remaining qualification limits.

The [current manual selection](execution/_Coordination/CURRENT_EXECUTION_BASIS.md)
applies to forward development. The [SWB/Domain interface basis](execution/_Coordination/HANDOFF_SWBPIPE_DOMAINS.md)
retains its undelivered and unadopted standing. New contract gaps belong in their
owning Design; PR descriptions carry the history of their fixes.

### User documentation

The [App v4 User Manual](docs/user-manual/README.md) is a working draft focused
on completing tasks and using, testing and improving workflows. Its procedures
need verification against the release candidate before publication.

### Basis and history

The owner accepted the revised composite basis on 2026-09-26, including its open
matters and external dependencies, and accepted the 60% gate on 2026-10-04. The
[composite acceptance](https://github.com/sgttomas/chirality/blob/archive%2Fapp-v4-pre-contract-register-retirement-20261011/projects/chirality-app-v4/execution/_Coordination/Acceptances/APP-V4-BASIS-20260926/ACCEPTANCE.md),
[Group1](execution/_Decomposition/checkpoint_snapshots/_LATEST_GROUP1.md),
[Group2](execution/_Decomposition/checkpoint_snapshots/_LATEST_GROUP2.md),
[final decomposition](execution/_Decomposition/checkpoint_snapshots/_LATEST_ACCEPTED.md),
[project DAG](execution/_DAG/_LATEST.md) and
[gate decision](https://github.com/sgttomas/chirality/blob/archive%2Fpre-efficiency-cleanup-2026-10-09/projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-GRAPH-CLOSURE-20261004/OWNER_DECISIONS.md)
identify those acts and their subjects. The published fallback remains v3.0.1
until the separate replacement decision.

Old setup logs, handoffs, work graphs, acceptance packets and implementation
register history are recoverable at
[`archive/app-v4-pre-contract-register-retirement-20261011`](https://github.com/sgttomas/chirality/tree/archive%2Fapp-v4-pre-contract-register-retirement-20261011/projects/chirality-app-v4).
Earlier AgentRuns are in
[`archive/pre-efficiency-cleanup-2026-10-09`](https://github.com/sgttomas/chirality/tree/archive%2Fpre-efficiency-cleanup-2026-10-09/projects/chirality-app-v4/execution/_Coordination/AgentRuns).
These are historical sources, not a standing development backlog.

### Layout

| Path | Contents |
|---|---|
| [docs/](docs/) | PRD, architecture, host integration, examination and operating method |
| [app/](app/) | Rust host, web view and maintained product checks |
| [execution/](execution/) | Deliverable contracts, Designs and dependency conditions |
| [conceptual/](conceptual/) | Source interpretation and the original conceptual choices |
| [reference/](reference/) | Identified source revisions and inventories |
| [foundation/](foundation/) | Preserved thesis and its transfer account |
