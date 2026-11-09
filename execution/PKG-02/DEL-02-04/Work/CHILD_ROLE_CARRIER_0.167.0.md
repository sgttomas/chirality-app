# Native child carrier — Codex 0.167.0 source compatibility

The supported source path is per-parent `thread/start.config`, with dotted
`agents.<ROLE>.description` and `agents.<ROLE>.config_file`. The child file is
the App's immutable, content-bound TOML envelope containing the complete
`developer_instructions`. There is no process-wide configuration fallback or
namespace-tool availability inference.

This account relies on official source commit
`086ccc833bc9cf01024ad2dd6af7dbd421b6bf9a` and the canonical acting distribution
identified by [the supplier integration account](../../../PKG-01/DEL-01-01/Work/CODEX_0.167_UPGRADE.md).
The main is `030316ecfbb41f4e7946e584b0063ef333b7a36cd312ba349f2f6869e39b62cc`;
its complete 42-file canonical manifest is
`158dd67072236253a694ca06d9bf7bfdebbe20d4a197bbf675433cbdddea7e7b`.
Source bodies were checked against that revision's immutable tree sizes and
Git blobs before interpretation. Matching version/main alone is not the
mechanism basis, and schema shapes are not runtime-child evidence.

## Source path and origin limits

- [Config manager](https://github.com/openai/codex/blob/086ccc833bc9cf01024ad2dd6af7dbd421b6bf9a/codex-rs/app-server/src/config_manager.rs)
  merges request configuration as JSON-to-TOML override pairs.
  [Dotted overrides](https://github.com/openai/codex/blob/086ccc833bc9cf01024ad2dd6af7dbd421b6bf9a/codex-rs/config/src/overrides.rs)
  expand `agents.<ROLE>.config_file` into the layer; the
  [typed role declaration](https://github.com/openai/codex/blob/086ccc833bc9cf01024ad2dd6af7dbd421b6bf9a/codex-rs/config/src/config_toml.rs)
  preserves its absolute/resolved file path.
- [Role loader](https://github.com/openai/codex/blob/086ccc833bc9cf01024ad2dd6af7dbd421b6bf9a/codex-rs/agent-roles/src/loader.rs)
  reads enabled layers low to high, with declared role files before same-layer
  standalone definitions. Higher layers replace lower roles while retaining
  missing fields. The
  [parser](https://github.com/openai/codex/blob/086ccc833bc9cf01024ad2dd6af7dbd421b6bf9a/codex-rs/agent-roles/src/agent_role_config.rs)
  takes a nonempty content `name` before the declaration hint.
  [Discovery](https://github.com/openai/codex/blob/086ccc833bc9cf01024ad2dd6af7dbd421b6bf9a/codex-rs/agent-roles/src/discovery.rs)
  recursively collects `.toml` files under a layer's `agents/` folder.
- [Layer state](https://github.com/openai/codex/blob/086ccc833bc9cf01024ad2dd6af7dbd421b6bf9a/codex-rs/config/src/state.rs)
  excludes disabled layers and gives discovery folders only to System, User
  and Project. Packaged defaults and managed/session layers have no standalone
  folder, although declarations can still exist in enabled configuration.
  [Config read](https://github.com/openai/codex/blob/086ccc833bc9cf01024ad2dd6af7dbd421b6bf9a/codex-rs/app-server/src/config_manager_service.rs)
  projects effective config/origins and optional layers, omitting packaged
  defaults. It does not resolve a complete standalone role namespace or lock
  source currency. App keeps conservative name unions, unknown-origin refusal,
  linked-input limits and before-dispatch source rechecks.

`AgentsToml` now uses `interrupt_message` and accepts raw-layer alias
`max_threads` for `max_concurrent_threads_per_session`. App recognizes these
controls without treating them as role names. Unknown scalar controls still
withhold. This is the concrete 0.167 parser repair; it grants no new config,
permission or origin coverage.

## Exact V1/V2 distinction and original association

| Supplier child path | Source-established carrier |
|---|---|
| V1 without full-history fork | Applies the selected role to the child configuration. It is not the supported V2 started-item association described below. |
| V1 full-history fork with explicit `agent_type` | Rejects the role override. No App role-supply success may be inferred. |
| V2 without full-history fork, explicit `agent_type` | Applies that role and its `developer_instructions`. |
| V2 full-history fork, explicit `agent_type` | Applies that role and its `developer_instructions`; parent text is only a fallback when no role developer instructions exist. |
| V2 full-history fork without explicit role | Does not establish App child role supply merely by inheriting history or parent settings. |

These branches are in
[child_config.rs](https://github.com/openai/codex/blob/086ccc833bc9cf01024ad2dd6af7dbd421b6bf9a/codex-rs/core/src/agent/child_config.rs)
(`prepare_agent_spawn_config`, `reject_full_fork_agent_type_override`).
[role.rs](https://github.com/openai/codex/blob/086ccc833bc9cf01024ad2dd6af7dbd421b6bf9a/codex-rs/core/src/agent/role.rs)
loads the referenced role envelope and assigns the child-only developer text.
The V2
[spawn handler](https://github.com/openai/codex/blob/086ccc833bc9cf01024ad2dd6af7dbd421b6bf9a/codex-rs/core/src/tools/handlers/multi_agents_v2/spawn.rs)
passes explicit role and fork mode through
[thread_spawn.rs](https://github.com/openai/codex/blob/086ccc833bc9cf01024ad2dd6af7dbd421b6bf9a/codex-rs/core/src/thread_spawn.rs),
which selects `SpawnConfigVersion::V2` and binds parent/role in `SessionSource::SubAgent`.

The V2 handler emits the `started` activity with actual child ID after successful spawn.
[multi_agents_v2.rs](https://github.com/openai/codex/blob/086ccc833bc9cf01024ad2dd6af7dbd421b6bf9a/codex-rs/core/src/tools/handlers/multi_agents_v2.rs)
emits both item lifecycle events;
[event mapping](https://github.com/openai/codex/blob/086ccc833bc9cf01024ad2dd6af7dbd421b6bf9a/codex-rs/app-server-protocol/src/protocol/event_mapping.rs)
keeps the original parent thread/turn in `item/completed`;
[item conversion](https://github.com/openai/codex/blob/086ccc833bc9cf01024ad2dd6af7dbd421b6bf9a/codex-rs/app-server-protocol/src/protocol/v2/item.rs)
preserves `subAgentActivity`, kind and `agentThreadId`.
[Thread read](https://github.com/openai/codex/blob/086ccc833bc9cf01024ad2dd6af7dbd421b6bf9a/codex-rs/app-server/src/request_processors/thread_processor.rs)
reads that child and projects parent ID and source role from stored/live metadata.

App's original completed event, same live generation, correlated `thread/read`,
correct `parentThreadId` and supplied `agentRole`, current original parent
carrier and unchanged role files remain jointly required. A V1 failed fork,
inherited parent role, unmatched read, history-only/fork/resume reference or
merely schema-valid started item supplies no child authority. The native access
owner owns the version-bound admission predicate and connecting positive/negative
fixtures; it must consume this mechanism basis rather than replace the old pin
predicate with a bare constant or discard the child requirement.

The historical [0.160.0 carrier account](CHILD_ROLE_CARRIER_0.160.0.md), including
12 cases/19 requests, retains exactly its original subject. No 0.167 supplier
session or child was run for this account. App fixture tests concern its guarded
preparation and association only. Actual native .167 carrier delivery, complete
prompt behavior, child nondelegation, supplier distribution/installed qualification,
provider uptake and adoption remain unestablished. TASK nondelegation remains
stated rather than enforced.
