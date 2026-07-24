import {
  HARNESS_TOOL_REGISTRY_VERSION,
  listHarnessToolDescriptors,
  type HarnessToolDescriptor
} from './tool-descriptor.js';

const CATALOG_PATH = 'frontend/docs/harness/tool_catalog.md';

function escapeMarkdownTableCell(value: string): string {
  return value.replace(/\|/g, '\\|').replace(/\n/g, '<br>');
}

function joinValues(values: readonly string[]): string {
  return values.length > 0 ? values.join(', ') : 'none';
}

function humanGateSummary(descriptor: HarnessToolDescriptor): string {
  if (!descriptor.humanGate.required) {
    return 'none';
  }
  return `${descriptor.humanGate.gate}: ${descriptor.humanGate.reason}`;
}

function exposedSummary(descriptor: HarnessToolDescriptor): string {
  return `${descriptor.runtime.exposedToModel ? 'yes' : 'no'}: ${descriptor.runtime.reason}`;
}

function modeSummary(descriptor: HarnessToolDescriptor): string {
  if (descriptor.surface === 'reserved') {
    return 'reserved / future policy';
  }
  if (descriptor.name === 'agent') {
    return 'subagent bridge gate';
  }
  if (
    descriptor.permissions.includes('workspace-write') ||
    descriptor.permissions.includes('shell') ||
    descriptor.permissions.includes('coordination')
  ) {
    return 'workspaceWrite';
  }
  return 'readOnly, workspaceWrite';
}

function hookRequirementSummary(descriptor: HarnessToolDescriptor): string {
  if (descriptor.surface === 'chirality-mcp') {
    if (descriptor.permissions.includes('workspace-write')) {
      return 'Handler-level permission/evidence wrapper; project-root path policy; redaction; event logging. SDK canUseTool and hooks do not auto-fire for raw in-process MCP calls.';
    }
    return 'Descriptor allow-list; project-root containment in handler; result budget; redaction; event logging.';
  }

  if (descriptor.surface === 'reserved') {
    return 'Not exposed; future policy must define permission, hook, path, redaction, and event requirements before activation.';
  }

  if (descriptor.name === 'agent') {
    return 'Special case: descriptor remains not exposed by default; buildSdkOptions may add Agent only when the governed subagent bridge allows it.';
  }

  if (descriptor.permissions.includes('shell')) {
    return 'canUseTool permission overlay; PreToolUse and PostToolUse hooks; shell timeout/no-network policy; redaction; event logging.';
  }

  if (descriptor.permissions.includes('workspace-write')) {
    return 'canUseTool permission overlay; PreToolUse and PostToolUse hooks; project-root path policy; redaction; diff/evidence logging.';
  }

  return 'canUseTool permission overlay; PreToolUse and PostToolUse evidence hooks; project-root read policy; result budget.';
}

function adapterName(descriptor: HarnessToolDescriptor): string {
  return descriptor.adapter.claudeAgentSdk?.toolName ?? 'none';
}

function renderDescriptorRow(descriptor: HarnessToolDescriptor): string {
  const values = [
    descriptor.name,
    adapterName(descriptor),
    descriptor.description,
    descriptor.surface,
    joinValues(descriptor.permissions),
    descriptor.pathScope,
    modeSummary(descriptor),
    descriptor.idempotence,
    descriptor.concurrency,
    humanGateSummary(descriptor),
    hookRequirementSummary(descriptor),
    exposedSummary(descriptor)
  ];
  return `| ${values.map(escapeMarkdownTableCell).join(' | ')} |`;
}

export function renderHarnessToolCatalog(): string {
  const descriptors = listHarnessToolDescriptors();
  const rows = descriptors.map(renderDescriptorRow).join('\n');
  return `# Harness Tool Catalog

**Status:** Generated governance/runtime support artifact
**Registry version:** \`${HARNESS_TOOL_REGISTRY_VERSION}\`
**Source:** \`frontend/packages/harness-contract/src/tool-descriptor.ts\`
**Regenerate:** \`npm run harness:generate-tool-catalog\`

This catalog is generated from \`HARNESS_TOOL_DESCRIPTORS\`. Do not edit
\`${CATALOG_PATH}\` by hand; update the descriptor registry and regenerate it. It is
derivative documentation for the local/in-process tool boundary and does not expose new
capability, change provider scope, or create release/professional approval.

## Naming Boundary

Chirality-owned in-process MCP tools use \`mcp__chirality__*\` adapter names.
A closed, ruled two-entry domain profile registry (D-APP-51) gates the
read-side domain transport wrappers
\`mcp__chirality__domain_completeness_check\` and
\`mcp__chirality__domain_rule_check_run\` for exactly the registered profileIds
\`open_pipe_stress\` (D-APP-50 tranche-1) and \`pec\` (D-APP-51 P1); registering
any further profileId requires its own D-APP ruling (no filesystem discovery,
no dynamic registration). Their handlers return live DEC-041 in-process
read-transport evidence envelopes only: no domain verdict, no live-binding
claim, no professional conclusion, and no piping write.
\`mcp__chirality__domain_headless_preview_run\` is live only for
\`open_pipe_stress\` under D-APP-50 using the final DEC-065 local
\`openpipestress-runner solve\` transport. The caller must configure an absolute
runner path in \`CHIRALITY_OPEN_PIPE_STRESS_RUNNER_PATH\` plus its exact lowercase
SHA-256 in \`CHIRALITY_OPEN_PIPE_STRESS_RUNNER_SHA256\`; the adapter resolves and verifies
the executable immediately before one foreground spawn, passes the exact bytes
of a project-root-contained \`runnerInputRef\` on stdin, and accepts structured
JSON only from bounded stdout. It performs no PATH lookup, shell invocation,
network access, daemon work, telemetry, output-path write, proposal, acceptance,
or apply operation. The provisional \`modelInputPath\` concept is retired because
DEC-065 requires the complete schema-first request envelope rather than the
TP-RUNNER-014 model-only fixture.
\`mcp__chirality__domain_propose_operation\` and
\`mcp__chirality__domain_proposal_validate\` are live pec-scoped exposures per
D-APP-52: both handlers resolve only the registry's \`pec\` entry and ride a
loopback-only (127.0.0.1) endpoint-allowlisted HTTP transport to the local pec
engine seam (login, propose, refresh, get-proposal — no generic request
surface; credentials from the local environment, never in results). Proposal
refresh mutates and rides the workspace-write \`domain_propose_operation\`
tool; \`domain_proposal_validate\` is read-only and never recomputes.
Acceptance and application remain human acts in pec behind admin-only RBAC;
no accept/apply/force tool is registered or exposed.

SDK built-in tool names and Chirality MCP adapter names are collision-checked by the
descriptor registry tests. Unknown tools remain rejected before streaming.

## Exposure Note

\`Agent\` is a special case: the descriptor remains not exposed by default, and
\`buildSdkOptions\` may add the SDK \`Agent\` tool only when the governed subagent bridge is
present and explicitly allows executable delegation.

## Catalog

| Name | Adapter name | Description | Surface | Permissions | Path scope | Modes | Idempotence | Concurrency | Human gate | Hook requirements | Exposed to model |
|---|---|---|---|---|---|---|---|---|---|---|---|
${rows}
`;
}
