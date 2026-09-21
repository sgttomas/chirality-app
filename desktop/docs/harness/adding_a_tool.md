# Adding a Governed Tool

**Status:** Governance/runtime contributor guide
**Applies to:** local SDK built-ins and in-process Chirality MCP tools
**Primary sources:** `frontend/src/lib/harness/tool-descriptor.ts`,
`frontend/src/lib/harness/sdk-options-builder.ts`,
`frontend/src/lib/harness/mcp/tool-names.ts`,
`frontend/src/lib/harness/mcp/read-tools.ts`, and
`frontend/docs/harness/runtime_engine_contract.md`
**Amended:** D-GOV-43 (A2), 2026-09-12: Codex is the only engine and the adapter boundary is the Runtime service's socket API. Tool activity shown in the App comes from Codex's own tools and the user's MCP configuration (shared by reference through the effective Codex home) and is rendered through the normalized tool-activity view of the pass-through event representation. The Claude Agent SDK built-in path and `buildSdkOptions` sequence below are compatibility history; whether and how Chirality MCP tools are exposed to Codex is not established by this guide.

This guide describes how to add or change a governed tool without bypassing Chirality's
permission, hook, path, redaction, event, and human-gate policy. It does not approve a new
tool by itself. Remote MCP, plugins, broad tool search, network expansion, domain tools,
non-Anthropic providers, default-provider cutover, and release/professional claims remain
outside R6 unless a future human ruling authorizes them.

## Required Sequence

1. Update `HARNESS_TOOL_DESCRIPTORS` in
   `frontend/src/lib/harness/tool-descriptor.ts`.
2. For a Chirality MCP tool, update the typed name inventory in
   `frontend/src/lib/harness/mcp/tool-names.ts`.
3. Implement or update the handler registration in
   `frontend/src/lib/harness/mcp/read-tools.ts`.
4. Ensure SDK option resolution in `frontend/src/lib/harness/sdk-options-builder.ts`
   exposes the tool only after descriptor resolution, mode policy, and allow-list
   filtering.
5. Add or update focused tests for descriptor resolution, denial behavior, MCP server
   attachment, handler evidence, and any path or permission policy touched by the tool.
6. Regenerate the catalog with `npm run harness:generate-tool-catalog`.
7. Run the validation required by the active tranche. For tool-surface changes, the
   default minimum is `npm run test` and `npm run typecheck`.

## Descriptor Requirements

Every tool needs a descriptor before it can be considered for exposure. The descriptor
records:

- provider-neutral `name` and aliases;
- `adapter.claudeAgentSdk.toolName`, when the first adapter has a concrete name;
- surface: `claude-agent-sdk-builtin`, `chirality-mcp`, or `reserved`;
- permissions, path scope, idempotence, concurrency, interrupt behavior, result budget,
  provenance, human gate, input schema, and runtime exposure status.

The descriptor registry is collision-checked at import time. A new descriptor must not
claim a normalized name, alias, or adapter tool name already owned by another descriptor.
The descriptor tests also assert built-in SDK names remain disjoint from
`mcp__chirality__*` adapter names and that live Chirality MCP registrations match
descriptor metadata.

## Built-In SDK Tool Path

SDK built-ins such as `Read`, `Write`, `Edit`, and `Bash` are exposed through descriptor
resolution and `buildSdkOptions`.

The required enforcement path is:

1. `resolveHarnessToolPool` resolves requested names against the descriptor registry.
2. Current mode and permission overlay decide allow or deny.
3. Allowed names are passed to `tools` and `allowedTools`.
4. Denied or unrequested names remain in descriptor-derived `disallowedTools`.
5. `canUseTool` remains attached for explicit permission decisions.
6. `PreToolUse` and `PostToolUse` hooks enforce path, shell, redaction, evidence, and
   fail-closed behavior where applicable.

`allowedTools` alone is never a restriction boundary. A built-in tool that skips
descriptor resolution, `disallowedTools`, `canUseTool`, or required hooks is not governed
and must be rejected.

## In-Process Chirality MCP Path

Chirality MCP tools use the `mcp__chirality__*` adapter-name convention. Add the raw tool
name to the relevant registry list, then add the handler to `buildChiralityMcpTools` only
when the descriptor is meant to be exposed to the model.

Read-only MCP handlers must preserve project-root containment, result-budget handling,
redaction, and event logging. Mutating MCP handlers require a stricter path because the
SDK behavior probe showed raw in-process `mcp_message` calls do not automatically invoke
SDK `canUseTool` or hook callbacks.

For every mutating MCP tool, the handler itself must use the fail-closed
permission/evidence wrapper and must:

- require the appropriate mode, currently `workspaceWrite` for mutating tools;
- emit `tool.started`, `tool.permission`, and terminal `tool.completed` or `tool.failed`
  evidence;
- enforce project-root containment, instruction-root write blocking, and symlink target
  rejection;
- record bounded file metadata, result summaries, redacted errors, and diff metadata only;
- avoid storing raw protected file content, raw full diffs, raw SDK transcripts, or secrets
  in `HarnessEvent.data`.

An MCP tool that mutates project state without this handler-level wrapper is a K-MCP-1
bypass and must be rejected in review.

## Reserved Names

Current Chirality MCP adapter names are cataloged in
`frontend/docs/harness/tool_catalog.md`.

D-APP-50 tranche-1 exposes only the read-side domain transport wrappers
`mcp__chirality__domain_completeness_check` and
`mcp__chirality__domain_rule_check_run`. They must remain read-only DEC-041
in-process transport/evidence-envelope tools and must not claim a domain verdict,
live binding, professional conclusion, shell execution, network access, or piping write.
`mcp__chirality__domain_headless_preview_run` is the narrow D-APP-50 exception:
it is live only for `open_pipe_stress` through the final DEC-065 local
`openpipestress-runner solve` contract. Local configuration must provide an
absolute executable path in `CHIRALITY_OPEN_PIPE_STRESS_RUNNER_PATH` and exact
lowercase SHA-256 in `CHIRALITY_OPEN_PIPE_STRESS_RUNNER_SHA256`; the adapter verifies the
resolved regular executable immediately before direct foreground spawn, passes
the exact complete schema-first `runnerInputRef` bytes on stdin, and parses one
bounded stdout JSON result. It does not search PATH, invoke a shell, inherit the
ambient environment, use network/daemon/telemetry, name an output path, or expose
proposal/apply behavior. The former `modelInputPath` descriptor field was retired
because it described the provisional TP-RUNNER-014 model-only fixture, not the
final DEC-065 request envelope. Proposal/write names retain their separate profile
and transport rules.
Do not add placeholder domain handlers, broad tool search, remote MCP servers,
plugin marketplace hooks, remote execution, provider-network expansion, or apply-capable
domain tools as part of ordinary local tool work.

## Agent Tool Exception

`Agent` is special-cased outside ordinary descriptor exposure. Its descriptor remains not
exposed by default. `buildSdkOptions` may add `Agent` only when:

- the parent explicitly requested the agent tool;
- `createExecutableSubagentBridge` returns governed SDK agent definitions;
- delegated child names pass the Type 2 governance allowlist; and
- `Agent` is removed from `disallowedTools` only for that governed bridge path.

Child definitions do not inherit parent tools or capabilities. The Agent permission
callback and subagent hook re-check the delegated child name before execution.

## Catalog and Test Gates

After changing descriptors or MCP names, run:

```bash
npm run harness:generate-tool-catalog
npm run test -- --run src/__tests__/lib/tool-catalog.test.ts src/__tests__/lib/tool-descriptor.test.ts
```

The catalog test fails if `frontend/docs/harness/tool_catalog.md` drifts from
`HARNESS_TOOL_DESCRIPTORS`. Descriptor tests fail if a new descriptor collides with an
existing lookup key, a built-in shadows a Chirality MCP adapter name, or the live MCP
registration set no longer matches the descriptor set.

For runtime tool changes, also run the broader tranche-required checks, normally:

```bash
npm run test
npm run typecheck
```

Run `npm run harness:validate:premerge` when a change can affect exposed tool surface,
MCP server construction, or browser-visible harness workflow.
