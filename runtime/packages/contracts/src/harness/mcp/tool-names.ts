export const CHIRALITY_MCP_SERVER_NAME = 'chirality';
export const CHIRALITY_MCP_SERVER_VERSION = '2.0.0';

export const CHIRALITY_MCP_READ_TOOL_NAMES = [
  'status_read',
  'deps_read',
  'scope_scan',
  'scaffold_preview'
] as const;

export const CHIRALITY_MCP_MUTATING_TOOL_NAMES = [
  'status_transition',
  'deps_write'
] as const;

export const CHIRALITY_MCP_DOMAIN_TOOL_NAMES = [
  'domain_completeness_check',
  'domain_rule_check_run',
  'domain_headless_preview_run',
  'domain_propose_operation',
  'domain_proposal_validate'
] as const;

export const CHIRALITY_MCP_COORDINATION_TOOL_NAMES = [
  'delegate_agent',
  'report_coordination_notice',
  'send_agent_update',
  'ack_agent_update'
] as const;

export type ChiralityMcpReadToolName = (typeof CHIRALITY_MCP_READ_TOOL_NAMES)[number];
export type ChiralityMcpMutatingToolName = (typeof CHIRALITY_MCP_MUTATING_TOOL_NAMES)[number];
export type ChiralityMcpDomainToolName = (typeof CHIRALITY_MCP_DOMAIN_TOOL_NAMES)[number];
export type ChiralityMcpCoordinationToolName =
  (typeof CHIRALITY_MCP_COORDINATION_TOOL_NAMES)[number];
export type ChiralityMcpToolName =
  | ChiralityMcpReadToolName
  | ChiralityMcpMutatingToolName
  | ChiralityMcpDomainToolName
  | ChiralityMcpCoordinationToolName;

export type ChiralityMcpAllowedToolName =
  `mcp__${typeof CHIRALITY_MCP_SERVER_NAME}__${ChiralityMcpToolName}`;

export const CHIRALITY_MCP_TOOL_NAMES = [
  ...CHIRALITY_MCP_READ_TOOL_NAMES,
  ...CHIRALITY_MCP_MUTATING_TOOL_NAMES,
  ...CHIRALITY_MCP_DOMAIN_TOOL_NAMES,
  ...CHIRALITY_MCP_COORDINATION_TOOL_NAMES
] as const satisfies readonly ChiralityMcpToolName[];

export const CHIRALITY_MCP_ALLOWED_TOOL_NAMES = CHIRALITY_MCP_TOOL_NAMES.map(
  (toolName) => `mcp__${CHIRALITY_MCP_SERVER_NAME}__${toolName}` as ChiralityMcpAllowedToolName
) as readonly ChiralityMcpAllowedToolName[];

const CHIRALITY_MCP_ALLOWED_TOOL_NAME_SET = new Set<string>(
  CHIRALITY_MCP_ALLOWED_TOOL_NAMES
);

export function toChiralityMcpAllowedToolName(
  toolName: ChiralityMcpToolName
): ChiralityMcpAllowedToolName {
  return `mcp__${CHIRALITY_MCP_SERVER_NAME}__${toolName}`;
}

export function isChiralityMcpAllowedToolName(
  toolName: string
): toolName is ChiralityMcpAllowedToolName {
  return CHIRALITY_MCP_ALLOWED_TOOL_NAME_SET.has(toolName);
}
