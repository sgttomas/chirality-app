# Chirality App v4

Chirality makes a general agent act within and for a host application. Its
workflow-authoring App is the exemplar. [App v4 thesis](docs/thesis/README.md)
develops the reasons for its form; product commitments are in the [PRD](docs/PRD.md),
its companions and the deliverable Scopes of Work and Designs.

Development enters through the [App v4 loop](loop/LOOP_INIT.md). Deliverables live
in `execution/PKG-nn/DEL-nn-nn/`: `ScopeOfWork.md` holds commitments and acceptance
criteria, `Design/` holds contracts and open implementation conditions, and
`deliverable.yaml` states needs and code/check pointers. Query their inputs and
consumers with the [deliverables tools](../../tools/deliverables/README.md).
The [App README](app/README.md) describes the current product path and checks.

The [current manual selection](execution/_Coordination/CURRENT_EXECUTION_BASIS.md)
applies to forward development. The [SWB/Domain interface basis](execution/_Coordination/HANDOFF_SWBPIPE_DOMAINS.md)
retains its undelivered and unadopted standing. New contract gaps belong in their
owning Design; PR descriptions carry the history of their fixes.

## Basis and history

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

## Layout

| Path | Contents |
|---|---|
| [docs/](docs/) | PRD, architecture, host integration, examination and operating method |
| [app/](app/) | Rust host, web view and maintained product checks |
| [execution/](execution/) | Deliverable contracts, Designs and dependency conditions |
| [conceptual/](conceptual/) | Source interpretation and the original conceptual choices |
| [reference/](reference/) | Identified source revisions and inventories |
| [foundation/](foundation/) | Preserved thesis and its transfer account |
