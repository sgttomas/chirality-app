# Chirality App

Start a conversation with Help Human, the assistant in Chirality App. Work out
what you need, make a plan when it helps, and carry out the work together. Turn
a useful plan into a workflow for next time.

[Download v3.0.1](https://github.com/sgttomas/chirality-app/releases/tag/v3.0.1) · [Website](https://chirality.ai) · [Release announcement](https://chirality.ai/announcements)

The download is **v3.0.1**. This repository’s `main` branch develops **v4**,
which is not yet released.

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
- **v3.0.1 requirements:** an Apple Silicon Mac with macOS 15 or newer, and a ChatGPT
  account. v3.0.1 uses Codex through your account and does not offer local-model
  support.
- **Your data in v3.0.1:** saved plans, workflows, references, and outputs are ordinary
  files in your folders. Plans stay in conversation history unless you choose
  to save them to a file. You can keep and use them outside the App. Task
  content needed by the model is sent to OpenAI using your account; Chirality
  AI Ltd does not proxy or retain that content. See
  [installation and data handling](https://chirality.ai/app#install).
- **Issues:** [report an App issue](https://github.com/sgttomas/chirality-app/issues/new).

The [released v3.0.1 desktop source](https://github.com/sgttomas/chirality/tree/485051eac923c759238948a54cd7bb094eee4899/projects/chirality-app-dev/frontend)
is identified by the release notes. GitHub’s automatic source archives for that
release contain the release repository’s framework snapshot, not the desktop
application source.

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
its companions and the deliverable Scopes of Work and `Work/` material.

Development enters through the [App v4 loop](loop/LOOP_INIT.md). Deliverables live
in `execution/PKG-nn/DEL-nn-nn/`: `ScopeOfWork.md` holds commitments and acceptance
criteria, `Work/` holds contracts and open implementation conditions, and
`deliverable.yaml` states needs and code/check pointers. Query their inputs and
consumers with the [deliverables tools](tools/deliverables/README.md).
For the toolchain, build and launch instructions, start with the
[App developer start](app/README.md#developer-start). The rest of that README
describes the current product path, checks and remaining qualification limits.

The [current manual selection](execution/_Coordination/CURRENT_EXECUTION_BASIS.md)
applies to forward development. The [current SWBPIPE receiving account](execution/PKG-09/DEL-09-06/Work/SWBPIPE_RECEIVING_BINDING.md)
identifies the selected integration sources and evidence limits. The
[historical SWB/Domain interface basis](execution/_Coordination/HANDOFF_SWBPIPE_DOMAINS.md)
retains the dated relay and adoption record. New contract gaps belong in their
owning deliverable's `Work/`; PR descriptions carry the history of their fixes.

### User documentation

The [App v4 User Manual](docs/user-manual/README.md) is a working draft focused
on completing tasks and using, testing and improving workflows. Its procedures
need verification against the release candidate before publication.

### Basis and history

The [execution basis and retained history](execution/_Coordination/CURRENT_EXECUTION_BASIS.md)
identify the accepted project basis, current release obligations and historical
source selections. Earlier acceptance gates apply to their recorded subjects;
v4 publication and replacement of v3.0.1 remain separate decisions.

<details>
<summary>Historical source recovery</summary>

The [accepted decomposition](execution/_Decomposition/checkpoint_snapshots/_LATEST_ACCEPTED.md)
and [project DAG](execution/_DAG/_LATEST.md) retain their original decision records.
Old setup logs, handoffs and acceptance packets are recoverable in the
[pre-contract-register-retirement archive](https://github.com/sgttomas/chirality/tree/archive%2Fapp-v4-pre-contract-register-retirement-20261011/projects/chirality-app-v4).
Earlier AgentRuns are in the
[pre-efficiency-cleanup archive](https://github.com/sgttomas/chirality/tree/archive%2Fpre-efficiency-cleanup-2026-10-09/projects/chirality-app-v4/execution/_Coordination/AgentRuns).
These sources preserve history; they do not define a standing development backlog.

</details>

### Layout

| Path | Contents |
|---|---|
| [docs/](docs/) | PRD, architecture, host integration, examination and operating method |
| [app/](app/) | Rust host, web view and maintained product checks |
| [execution/](execution/) | Deliverable contracts, `Work/` material and dependency conditions |
| [conceptual/](conceptual/) | Source interpretation and the original conceptual choices |
| [reference/](reference/) | Identified source revisions and inventories |
| [foundation/](foundation/) | Preserved thesis and its transfer account |

## License

Repository code is available under the [MIT License](LICENSE.md). Bundled
third-party components retain their own licenses, terms and notices; the
repository license does not replace them.
