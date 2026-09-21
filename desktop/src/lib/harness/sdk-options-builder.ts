import { createSdkMcpServer, tool, type McpServerConfig, type Options, type PermissionMode, type SettingSource } from '@anthropic-ai/claude-agent-sdk';
import { z } from 'zod/v4';
import { createChiralityToolHooks } from './chirality-hooks';
import { ContentBlock, ResolvedOpts, SessionRecord } from '@chirality/runtime-contracts/types';
import type { RuntimeToolDefinition } from '@chirality/runtime-contracts';
import {
  createHarnessCanUseTool,
  normalizeHarnessPermissionMode
} from './permission-overlay';
import { HarnessError } from '@chirality/runtime-contracts/errors';
import { getPermissionBroker } from './permission-broker';
import { getPermissionEventChannel } from './permission-event-channel';
import { resolveHarnessToolPool } from './tool-pool';
import {
  getHarnessToolDescriptor,
  type ClaudeAgentSdkToolName,
  type HarnessToolDescriptor
} from '@chirality/runtime-contracts/tool-descriptor';
import {
  createChiralityMcpServers,
  filterChiralityMcpAllowedToolNames
} from './mcp/read-tools';
import { createScriptedAgentSdkProofSpawn } from './scripted-agent-sdk-proof';
import { createExecutableSubagentBridge } from './subagent-bridge';

export type SdkProbeOptions = Options & {
  settingSources: SettingSource[];
};

function parseSettingSources(raw: string | undefined): SettingSource[] {
  if (!raw || raw.trim().length === 0) {
    return [];
  }

  const requested = raw
    .split(',')
    .map((item) => item.trim())
    .filter(Boolean);

  if (requested.length === 1 && requested[0] === 'project') {
    return ['project'];
  }

  return [];
}

function mapPermissionMode(mode: string): PermissionMode {
  const normalizedMode = normalizeHarnessPermissionMode(mode);
  if (normalizedMode === 'readOnly' || normalizedMode === 'dontAsk') {
    return 'dontAsk';
  }
  if (normalizedMode === 'workspaceWrite') {
    return 'acceptEdits';
  }
  if (
    normalizedMode === 'bypass' &&
    process.env.CHIRALITY_ALLOW_SDK_BYPASS === '1'
  ) {
    return 'bypassPermissions';
  }
  return 'default';
}

function contentBlocksToPrompt(message: string, contentBlocks?: ContentBlock[]): string {
  if (!contentBlocks || contentBlocks.length === 0) {
    return message;
  }

  const attachmentSummary = contentBlocks
    .map((block) => {
      if (block.type === 'text') {
        return block.text;
      }
      return `[Attachment: ${block.path} (${block.mimeType})]`;
    })
    .join('\n\n');

  return [message, attachmentSummary].filter((part) => part.trim().length > 0).join('\n\n');
}

export function buildSdkPrompt(message: string, contentBlocks?: ContentBlock[]): string {
  return contentBlocksToPrompt(message, contentBlocks);
}

function requestedAgentTool(toolNames: readonly string[]): boolean {
  return toolNames.some((toolName) => getHarnessToolDescriptor(toolName)?.name === 'agent');
}

function createRuntimeToolDescriptor(
  definition: RuntimeToolDefinition,
  sdkToolName: string
): HarnessToolDescriptor {
  const isSessionControl =
    definition.name === 'chirality_request_method_change' &&
    definition.permission.operation === 'control';
  return {
    name: definition.name,
    aliases: [sdkToolName],
    description: definition.description,
    surface: 'chirality-mcp',
    permissions: isSessionControl ? ['control'] : ['read'],
    pathScope: 'none',
    idempotence: isSessionControl ? 'input-dependent' : 'idempotent',
    concurrency: 'safe',
    interruptBehavior: 'cancel',
    resultBudget: { inlineByteLimit: 64 * 1024, artifactByteLimit: 0, overflow: 'deny' },
    provenance: {
      emits: ['tool.permission', 'tool.started', 'tool.completed', 'tool.failed'],
      storeInput: 'metadata',
      storeOutput: 'metadata',
      recordsDiff: false
    },
    humanGate: { required: false },
    adapter: { claudeAgentSdk: { toolName: sdkToolName as ClaudeAgentSdkToolName } },
    inputSchema: definition.inputSchema,
    runtime: {
      exposedToModel: true,
      reason: isSessionControl
        ? 'Exact Runtime session-control tool admitted by the frozen Runtime turn context.'
        : 'Admitted by the frozen Runtime turn context.'
    }
  };
}

export function buildSdkOptions(input: {
  session: SessionRecord;
  opts: ResolvedOpts;
  abortController: AbortController;
  systemPrompt: string;
  runtimeTools?: readonly RuntimeToolDefinition[];
}): SdkProbeOptions {
  const unsafeRuntimeTool = input.runtimeTools?.find((definition) => {
    if (definition.permission.effect !== 'allow') return true;
    if (definition.permission.operation === 'read') return false;
    return !(
      definition.name === 'chirality_request_method_change' &&
      definition.permission.operation === 'control'
    );
  });
  if (unsafeRuntimeTool !== undefined) {
    throw new HarnessError(
      'ENGINE_UNAVAILABLE',
      422,
      `Runtime tool '${unsafeRuntimeTool.name}' cannot be exposed by the Claude MCP bridge without an enforceable read-only permission.`
    );
  }
  const toolPool = resolveHarnessToolPool({
    sessionId: input.session.sessionId,
    requestedTools: input.opts.tools,
    mode: input.opts.mode
  });
  const subagentBridge = createExecutableSubagentBridge({
    session: input.session,
    opts: input.opts
  });
  const allowExecutableAgent = Boolean(subagentBridge && requestedAgentTool(input.opts.tools));
  const allowedToolNames = allowExecutableAgent
    ? [...toolPool.allowedToolNames, 'Agent' as const]
    : [...toolPool.allowedToolNames];
  const disallowedToolNames = allowExecutableAgent
    ? toolPool.disallowedToolNames.filter((toolName) => toolName !== 'Agent')
    : [...toolPool.disallowedToolNames];
  const allowedChiralityMcpToolNames = filterChiralityMcpAllowedToolNames(allowedToolNames);
  const scriptedAgentSdkProofSpawn = createScriptedAgentSdkProofSpawn();
  const runtimeToolNames = (input.runtimeTools ?? []).map((definition) =>
    `mcp__chirality_runtime__${definition.name}`
  );
  const runtimeDescriptors = new Map(
    (input.runtimeTools ?? []).map((definition) => {
      const sdkToolName = `mcp__chirality_runtime__${definition.name}`;
      return [sdkToolName, createRuntimeToolDescriptor(definition, sdkToolName)] as const;
    })
  );
  const admittedNativeDescriptors = new Map<string, HarnessToolDescriptor>(
    allowedToolNames.flatMap((toolName) => {
      const descriptor = getHarnessToolDescriptor(toolName);
      return descriptor === undefined ? [] : [[toolName, descriptor] as const];
    })
  );
  const resolveTurnToolDescriptor = (toolName: string): HarnessToolDescriptor | undefined =>
    runtimeDescriptors.get(toolName) ?? admittedNativeDescriptors.get(toolName);
  const runtimeMcpServers: Record<string, McpServerConfig> = input.runtimeTools?.length ? {
    chirality_runtime: createSdkMcpServer({
      name: 'chirality_runtime',
      version: '3',
      instructions: 'Runtime-admitted Chirality method discovery and context tools.',
      tools: input.runtimeTools.map((definition) => {
        const schema = z.fromJSONSchema(definition.inputSchema);
        if (!(schema instanceof z.ZodObject)) {
          throw new Error(`Runtime tool '${definition.name}' must use an object input schema.`);
        }
        return tool(definition.name, definition.description, schema.shape, async (args) => ({
          content: [{ type: 'text' as const, text: JSON.stringify(await definition.execute(args, input.abortController.signal)) }]
        }));
      })
    })
  } : {};

  return {
    abortController: input.abortController,
    agents: subagentBridge?.agents,
    cwd: input.session.projectRoot,
    model: input.opts.model,
    maxTurns: input.opts.maxTurns,
    permissionMode: mapPermissionMode(input.opts.mode),
    tools: [...allowedToolNames, ...runtimeToolNames],
    allowedTools: [...allowedToolNames, ...runtimeToolNames],
    disallowedTools: disallowedToolNames,
    canUseTool: createHarnessCanUseTool({
      sessionId: input.session.sessionId,
      mode: input.opts.mode,
      projectRoot: input.session.projectRoot,
      allowedReadScopes: input.session.declaredContext,
      allowedWriteTargets: input.session.allowedWriteTargets,
      delegatedSubagents: subagentBridge?.delegatedSubagents,
      resolveDescriptor: resolveTurnToolDescriptor,
      requestHumanDecision: ({ sessionId, toolUseId }) =>
        getPermissionBroker().request({
          sessionId,
          toolUseId,
          // The turn's AbortController is its identity, so teardown can scope the
          // clear to this turn and not deny a newer same-session turn's approvals.
          turnToken: input.abortController
        }).verdict,
      publishEvent: (event) =>
        getPermissionEventChannel().publish(input.session.sessionId, event)
    }),
    hooks: createChiralityToolHooks({
      sessionId: input.session.sessionId,
      projectRoot: input.session.projectRoot,
      allowedReadScopes: input.session.declaredContext,
      allowedWriteTargets: input.session.allowedWriteTargets,
      delegatedSubagents: subagentBridge?.delegatedSubagents,
      resolveDescriptor: resolveTurnToolDescriptor
    }),
    mcpServers: { ...createChiralityMcpServers({
      context: {
        projectRoot: input.session.projectRoot,
        sessionId: input.session.sessionId,
        persona: input.opts.persona,
        mode: input.opts.mode,
        tools: input.opts.tools
      },
      allowedToolNames: allowedChiralityMcpToolNames,
      mode: input.opts.mode
    }), ...runtimeMcpServers },
    resume: input.session.sdkSessionId,
    settingSources: parseSettingSources(process.env.CHIRALITY_SDK_SETTING_SOURCES),
    systemPrompt: {
      type: 'preset',
      preset: 'claude_code',
      append: input.systemPrompt
    },
    ...(scriptedAgentSdkProofSpawn
      ? { spawnClaudeCodeProcess: scriptedAgentSdkProofSpawn }
      : {})
  };
}
