import { mkdir, mkdtemp, rm } from 'node:fs/promises';
import os from 'node:os';
import path from 'node:path';
import { afterEach, describe, expect, it, vi } from 'vitest';
import { buildSdkOptions } from '../../lib/harness/sdk-options-builder';
import {
  getPermissionBroker,
  resetPermissionBrokerForTests
} from '../../lib/harness/permission-broker';
import type { ResolvedOpts, SessionRecord } from '@chirality/runtime-contracts/types';

const session: SessionRecord = {
  sessionId: 'sess_1',
  projectRoot: '/tmp/project',
  persona: 'WORKING_ITEMS',
  mode: 'direct',
  createdAt: '2026-02-23T00:00:00.000Z',
  updatedAt: '2026-02-23T00:00:00.000Z',
  sdkSessionId: 'sdk_resume'
};

const opts: ResolvedOpts = {
  model: 'claude-test',
  tools: ['read', 'write', 'bash'],
  maxTurns: 3,
  persona: 'WORKING_ITEMS',
  mode: 'direct'
};

const LIVE_DOMAIN_MCP_TOOL_NAMES = [
  'mcp__chirality__domain_completeness_check',
  'mcp__chirality__domain_rule_check_run',
  'mcp__chirality__domain_headless_preview_run'
] as const;

// D-APP-52: live pec-scoped proposal tools (write + read grades).
const PEC_PROPOSAL_DOMAIN_MCP_TOOL_NAMES = [
  'mcp__chirality__domain_propose_operation',
  'mcp__chirality__domain_proposal_validate'
] as const;

const DOMAIN_MCP_TOOL_NAMES = [
  ...LIVE_DOMAIN_MCP_TOOL_NAMES,
  ...PEC_PROPOSAL_DOMAIN_MCP_TOOL_NAMES
] as const;

let tmpDir = '';

afterEach(async () => {
  vi.unstubAllEnvs();
  resetPermissionBrokerForTests();
  delete process.env.CHIRALITY_SDK_SETTING_SOURCES;
  delete process.env.CHIRALITY_ALLOW_SDK_BYPASS;
  delete process.env.CHIRALITY_INSTRUCTION_ROOT;
  delete process.env.CHIRALITY_AGENTSDK_SCRIPTED_PROOF;
  if (tmpDir) {
    await rm(tmpDir, { recursive: true, force: true });
    tmpDir = '';
  }
});

describe('buildSdkOptions', () => {
  it('admits only the exact Runtime read tool through permission, hooks, and its MCP callback', async () => {
    tmpDir = await mkdtemp(path.join(os.tmpdir(), 'chirality-runtime-tool-'));
    const execute = vi.fn(async (args: unknown) => ({ echoed: args }));
    const options = buildSdkOptions({
      session: { ...session, projectRoot: tmpDir },
      opts: { ...opts, mode: 'readOnly' },
      abortController: new AbortController(),
      systemPrompt: 'runtime prompt',
      runtimeTools: [{
        name: 'chirality_list_methods', description: 'List admitted methods',
        inputSchema: { type: 'object', properties: { query: { type: 'string' } }, additionalProperties: false },
        permission: { effect: 'allow', operation: 'read' }, execute
      }]
    });
    const toolName = 'mcp__chirality_runtime__chirality_list_methods';

    await expect(options.canUseTool?.(
      toolName,
      { query: 'central' },
      { signal: new AbortController().signal, toolUseID: 'runtime-read' }
    )).resolves.toMatchObject({ behavior: 'allow', toolUseID: 'runtime-read' });
    await expect(options.canUseTool?.(
      'mcp__chirality_runtime__not_admitted',
      {},
      { signal: new AbortController().signal, toolUseID: 'runtime-unknown' }
    )).resolves.toMatchObject({ behavior: 'deny', message: expect.stringContaining('Unknown harness tool') });

    const preToolUse = options.hooks?.PreToolUse?.[0]?.hooks[0];
    await expect(preToolUse?.({
      hook_event_name: 'PreToolUse', tool_name: toolName,
      tool_input: { query: 'central' }, tool_use_id: 'runtime-read'
    } as never, 'runtime-read', { signal: new AbortController().signal })).resolves.toMatchObject({ continue: true });

    const server = options.mcpServers?.chirality_runtime as unknown as {
      instance: { _registeredTools: Record<string, { handler: (args: unknown) => Promise<unknown> }> };
    };
    await expect(server.instance._registeredTools.chirality_list_methods.handler({ query: 'central' }))
      .resolves.toEqual({ content: [{ type: 'text', text: JSON.stringify({ echoed: { query: 'central' } }) }] });
    expect(execute).toHaveBeenCalledWith({ query: 'central' }, expect.any(AbortSignal));
  });

  it('fails closed before a Runtime write tool can enter the Claude MCP bridge', () => {
    expect(() => buildSdkOptions({
      session,
      opts: { ...opts, mode: 'readOnly' },
      abortController: new AbortController(),
      systemPrompt: 'runtime prompt',
      runtimeTools: [{
        name: 'unexpected_write', description: 'write', inputSchema: { type: 'object' },
        permission: { effect: 'allow', operation: 'write' },
        execute: async () => ({ ok: true })
      }]
    })).toThrowError(expect.objectContaining({ type: 'ENGINE_UNAVAILABLE', status: 422 }));
  });

  it('admits only the exact Runtime method-change control tool without filesystem capability', async () => {
    const execute = vi.fn(async () => ({ requested: true }));
    const options = buildSdkOptions({
      session: { ...session, declaredContext: [], allowedWriteTargets: [] },
      opts: { ...opts, mode: 'readOnly', tools: [] },
      abortController: new AbortController(),
      systemPrompt: 'runtime prompt',
      runtimeTools: [{
        name: 'chirality_request_method_change',
        description: 'Request a method change at the turn boundary',
        inputSchema: { type: 'object', properties: {}, additionalProperties: false },
        permission: { effect: 'allow', operation: 'control' },
        execute
      }]
    });
    const toolName = 'mcp__chirality_runtime__chirality_request_method_change';

    expect(options.tools).toEqual([toolName]);
    expect(options.allowedTools).toEqual([toolName]);
    expect(options.disallowedTools).toContain('Write');
    expect(options.disallowedTools).toContain('Bash');
    await expect(options.canUseTool?.(
      toolName,
      {},
      { signal: new AbortController().signal, toolUseID: 'runtime-control' }
    )).resolves.toMatchObject({ behavior: 'allow', toolUseID: 'runtime-control' });
    await expect(options.hooks?.PreToolUse?.[0]?.hooks[0]?.({
      hook_event_name: 'PreToolUse', tool_name: toolName,
      tool_input: {}, tool_use_id: 'runtime-control'
    } as never, 'runtime-control', { signal: new AbortController().signal }))
      .resolves.toMatchObject({ continue: true });

    expect(() => buildSdkOptions({
      session,
      opts: { ...opts, mode: 'readOnly' },
      abortController: new AbortController(),
      systemPrompt: 'runtime prompt',
      runtimeTools: [{
        name: 'unrecognized_control', description: 'control', inputSchema: { type: 'object' },
        permission: { effect: 'allow', operation: 'control' }, execute
      }]
    })).toThrowError(expect.objectContaining({ type: 'ENGINE_UNAVAILABLE', status: 422 }));
  });

  it('defaults to SDK settings isolation and exposes only requested read-class tools', () => {
    const options = buildSdkOptions({
      session,
      opts,
      abortController: new AbortController(),
      systemPrompt: 'persona prompt'
    });

    expect(options.settingSources).toEqual([]);
    expect(options.tools).toEqual(['Read']);
    expect(options.allowedTools).toEqual(['Read']);
    expect(options.disallowedTools).not.toContain('Read');
    expect(options.disallowedTools).toContain('LS');
    expect(options.disallowedTools).toContain('Bash');
    expect(options.disallowedTools).toContain('Write');
    expect(options.disallowedTools).toContain('Edit');
    expect(options.disallowedTools).toContain('Agent');
    expect(options.tools).not.toContain('Agent');
    expect(options.allowedTools).not.toContain('Agent');
    expect(options.agents).toBeUndefined();
    expect(options.disallowedTools).toContain('mcp__chirality__status_read');
    expect(options.disallowedTools).toEqual(expect.arrayContaining([...DOMAIN_MCP_TOOL_NAMES]));
    expect(options.mcpServers).toEqual({});
    expect(options.hooks?.PreToolUse?.[0]?.hooks[0]).toBeTypeOf('function');
    expect(options.hooks?.PostToolUse?.[0]?.hooks[0]).toBeTypeOf('function');
    expect(options.resume).toBe('sdk_resume');
    expect(options.model).toBe('claude-test');
    expect(options.maxTurns).toBe(3);
    expect(options.permissionMode).toBe('default');
    expect(options.canUseTool).toBeTypeOf('function');
    expect(options.spawnClaudeCodeProcess).toBeUndefined();
  });

  it('fails closed when a provider callback or hook names a tool omitted from the admitted turn set', async () => {
    tmpDir = await mkdtemp(path.join(os.tmpdir(), 'chirality-sdk-admitted-tools-'));
    const projectRoot = path.join(tmpDir, 'project');
    await mkdir(projectRoot, { recursive: true });
    const options = buildSdkOptions({
      session: { ...session, projectRoot },
      opts: { ...opts, mode: 'workspaceWrite', tools: ['read'] },
      abortController: new AbortController(),
      systemPrompt: 'persona prompt'
    });
    const sdkOptions = (toolUseID: string) => ({
      signal: new AbortController().signal,
      toolUseID
    });
    const preToolUse = options.hooks?.PreToolUse?.[0]?.hooks[0];

    await expect(
      options.canUseTool?.('Read', { file_path: 'README.md' }, sdkOptions('admitted-read'))
    ).resolves.toMatchObject({ behavior: 'allow' });
    await expect(
      options.canUseTool?.('Bash', { command: 'npm test' }, sdkOptions('omitted-bash'))
    ).resolves.toMatchObject({
      behavior: 'deny',
      message: expect.stringContaining("Unknown harness tool 'Bash'")
    });
    await expect(
      preToolUse?.({
        hook_event_name: 'PreToolUse',
        tool_name: 'Bash',
        tool_input: { command: 'npm test' },
        tool_use_id: 'omitted-bash-hook'
      } as never, 'omitted-bash-hook', { signal: new AbortController().signal })
    ).resolves.toMatchObject({
      continue: false,
      decision: 'block',
      hookSpecificOutput: { permissionDecision: 'deny' }
    });
    await expect(
      options.canUseTool?.(
        'mcp__chirality__status_read',
        {},
        sdkOptions('omitted-known-mcp')
      )
    ).resolves.toMatchObject({ behavior: 'deny' });
    await expect(
      preToolUse?.({
        hook_event_name: 'PreToolUse',
        tool_name: 'mcp__unknown__tool',
        tool_input: {},
        tool_use_id: 'unknown-mcp-hook'
      } as never, 'unknown-mcp-hook', { signal: new AbortController().signal })
    ).resolves.toMatchObject({ continue: false, decision: 'block' });
  });

  it('exposes the full requested read set and keeps unrequested or denied tools disallowed', () => {
    const options = buildSdkOptions({
      session,
      opts: { ...opts, tools: ['read', 'Glob', 'grep', 'LS'] },
      abortController: new AbortController(),
      systemPrompt: 'persona prompt'
    });

    expect(options.tools).toEqual(['Read', 'Glob', 'Grep', 'LS']);
    expect(options.allowedTools).toEqual(['Read', 'Glob', 'Grep', 'LS']);
    expect(options.disallowedTools).toEqual([
      'mcp__chirality__status_read',
      'mcp__chirality__deps_read',
      'mcp__chirality__scope_scan',
      'mcp__chirality__scaffold_preview',
      'mcp__chirality__delegate_agent',
      'mcp__chirality__report_coordination_notice',
      'mcp__chirality__send_agent_update',
      'mcp__chirality__ack_agent_update',
      'mcp__chirality__status_transition',
      'mcp__chirality__deps_write',
      ...DOMAIN_MCP_TOOL_NAMES,
      'Write',
      'Edit',
      'MultiEdit',
      'NotebookEdit',
      'Bash',
      'WebFetch',
      'WebSearch',
      'Agent'
    ]);
  });

  it('attaches the read-only Chirality MCP server when MCP descriptors are requested', () => {
    const options = buildSdkOptions({
      session,
      opts: { ...opts, tools: ['status_read', 'deps_read'] },
      abortController: new AbortController(),
      systemPrompt: 'persona prompt'
    });

    expect(options.tools).toEqual([
      'mcp__chirality__status_read',
      'mcp__chirality__deps_read'
    ]);
    expect(options.allowedTools).toEqual([
      'mcp__chirality__status_read',
      'mcp__chirality__deps_read'
    ]);
    expect(options.disallowedTools).not.toContain('mcp__chirality__status_read');
    expect(options.disallowedTools).not.toContain('mcp__chirality__deps_read');
    expect(options.disallowedTools).toContain('mcp__chirality__scope_scan');
    expect(options.disallowedTools).toContain('Bash');
    expect(options.disallowedTools).toContain('Write');
    expect(options.disallowedTools).toContain('mcp__chirality__status_transition');
    expect(options.disallowedTools).toEqual(expect.arrayContaining([...DOMAIN_MCP_TOOL_NAMES]));
    expect(options.mcpServers).toMatchObject({
      chirality: {
        type: 'sdk',
        name: 'chirality'
      }
    });
  });

  it('attaches mutating Chirality MCP tools only when requested in workspaceWrite mode', () => {
    const workspaceWrite = buildSdkOptions({
      session,
      opts: {
        ...opts,
        mode: 'workspaceWrite',
        tools: ['status_transition', 'deps_write']
      },
      abortController: new AbortController(),
      systemPrompt: 'persona prompt'
    });

    expect(workspaceWrite.tools).toEqual([
      'mcp__chirality__status_transition',
      'mcp__chirality__deps_write'
    ]);
    expect(workspaceWrite.allowedTools).toEqual([
      'mcp__chirality__status_transition',
      'mcp__chirality__deps_write'
    ]);
    expect(workspaceWrite.disallowedTools).not.toContain('mcp__chirality__status_transition');
    expect(workspaceWrite.disallowedTools).not.toContain('mcp__chirality__deps_write');
    expect(workspaceWrite.mcpServers).toMatchObject({
      chirality: {
        type: 'sdk',
        name: 'chirality'
      }
    });

    const readOnly = buildSdkOptions({
      session,
      opts: {
        ...opts,
        mode: 'readOnly',
        tools: ['status_transition', 'deps_write']
      },
      abortController: new AbortController(),
      systemPrompt: 'persona prompt'
    });

    expect(readOnly.tools).toEqual([]);
    expect(readOnly.allowedTools).toEqual([]);
    expect(readOnly.disallowedTools).toContain('mcp__chirality__status_transition');
    expect(readOnly.disallowedTools).toContain('mcp__chirality__deps_write');
    expect(readOnly.mcpServers).toEqual({});
  });

  it('attaches D-APP-50 tranche-1 read-side domain MCP tools when explicitly requested', () => {
    const options = buildSdkOptions({
      session,
      opts: {
        ...opts,
        mode: 'readOnly',
        tools: ['domain_completeness_check', 'domain_rule_check_run']
      },
      abortController: new AbortController(),
      systemPrompt: 'persona prompt'
    });

    expect(options.tools).toEqual(LIVE_DOMAIN_MCP_TOOL_NAMES.slice(0, 2));
    expect(options.allowedTools).toEqual(LIVE_DOMAIN_MCP_TOOL_NAMES.slice(0, 2));
    expect(options.disallowedTools).not.toContain('mcp__chirality__domain_completeness_check');
    expect(options.disallowedTools).not.toContain('mcp__chirality__domain_rule_check_run');
    expect(options.mcpServers).toMatchObject({
      chirality: {
        type: 'sdk',
        name: 'chirality'
      }
    });
  });

  it('attaches the DEC-065 headless domain tool in readOnly mode when explicitly requested', () => {
    const options = buildSdkOptions({
      session,
      opts: {
        ...opts,
        mode: 'readOnly',
        tools: ['domain_headless_preview_run']
      },
      abortController: new AbortController(),
      systemPrompt: 'persona prompt'
    });

    expect(options.tools).toEqual(['mcp__chirality__domain_headless_preview_run']);
    expect(options.allowedTools).toEqual(['mcp__chirality__domain_headless_preview_run']);
    expect(options.disallowedTools).not.toContain('mcp__chirality__domain_headless_preview_run');
    expect(options.mcpServers).toMatchObject({ chirality: { type: 'sdk', name: 'chirality' } });
  });

  it('attaches the D-APP-52 pec proposal tools in workspaceWrite mode when explicitly requested', () => {
    const options = buildSdkOptions({
      session,
      opts: {
        ...opts,
        mode: 'workspaceWrite',
        tools: ['domain_propose_operation', 'domain_proposal_validate']
      },
      abortController: new AbortController(),
      systemPrompt: 'persona prompt'
    });

    expect(options.tools).toEqual([...PEC_PROPOSAL_DOMAIN_MCP_TOOL_NAMES]);
    expect(options.allowedTools).toEqual([...PEC_PROPOSAL_DOMAIN_MCP_TOOL_NAMES]);
    expect(options.disallowedTools).not.toContain('mcp__chirality__domain_propose_operation');
    expect(options.disallowedTools).not.toContain('mcp__chirality__domain_proposal_validate');
    expect(options.mcpServers).toMatchObject({
      chirality: {
        type: 'sdk',
        name: 'chirality'
      }
    });
  });

  it('keeps the write-graded pec proposal tool denied in readOnly mode while validate attaches', () => {
    const options = buildSdkOptions({
      session,
      opts: {
        ...opts,
        mode: 'readOnly',
        tools: ['domain_propose_operation', 'domain_proposal_validate']
      },
      abortController: new AbortController(),
      systemPrompt: 'persona prompt'
    });

    expect(options.tools).toEqual(['mcp__chirality__domain_proposal_validate']);
    expect(options.allowedTools).toEqual(['mcp__chirality__domain_proposal_validate']);
    expect(options.disallowedTools).toContain('mcp__chirality__domain_propose_operation');
    expect(options.mcpServers).toMatchObject({
      chirality: {
        type: 'sdk',
        name: 'chirality'
      }
    });
  });

  it('allows only explicit project settings and never user or local sources', () => {
    process.env.CHIRALITY_SDK_SETTING_SOURCES = 'user,local,project';

    const rejected = buildSdkOptions({
      session,
      opts,
      abortController: new AbortController(),
      systemPrompt: 'persona prompt'
    });
    expect(rejected.settingSources).toEqual([]);

    process.env.CHIRALITY_SDK_SETTING_SOURCES = 'project';
    const projectOnly = buildSdkOptions({
      session,
      opts,
      abortController: new AbortController(),
      systemPrompt: 'persona prompt'
    });
    expect(projectOnly.settingSources).toEqual(['project']);
  });

  it('attaches the scripted SDK subprocess only for explicit development or test proof runs', () => {
    vi.stubEnv('CHIRALITY_AGENTSDK_SCRIPTED_PROOF', '1');
    vi.stubEnv('NODE_ENV', 'test');

    const proofOptions = buildSdkOptions({
      session,
      opts,
      abortController: new AbortController(),
      systemPrompt: 'persona prompt'
    });
    expect(proofOptions.spawnClaudeCodeProcess).toBeTypeOf('function');

    vi.stubEnv('NODE_ENV', 'development');
    const developmentOptions = buildSdkOptions({
      session,
      opts,
      abortController: new AbortController(),
      systemPrompt: 'persona prompt'
    });
    expect(developmentOptions.spawnClaudeCodeProcess).toBeTypeOf('function');

    vi.stubEnv('NODE_ENV', '');
    const unsetOptions = buildSdkOptions({
      session,
      opts,
      abortController: new AbortController(),
      systemPrompt: 'persona prompt'
    });
    expect(unsetOptions.spawnClaudeCodeProcess).toBeUndefined();

    vi.stubEnv('NODE_ENV', 'production');
    const productionOptions = buildSdkOptions({
      session,
      opts,
      abortController: new AbortController(),
      systemPrompt: 'persona prompt'
    });
    expect(productionOptions.spawnClaudeCodeProcess).toBeUndefined();
  });

  it('maps Chirality modes to SDK permission posture without premature write auto-acceptance', () => {
    const readOnly = buildSdkOptions({
      session,
      opts: { ...opts, mode: 'readOnly' },
      abortController: new AbortController(),
      systemPrompt: 'persona prompt'
    });
    expect(readOnly.permissionMode).toBe('dontAsk');

    const workspaceWrite = buildSdkOptions({
      session,
      opts: { ...opts, mode: 'workspaceWrite' },
      abortController: new AbortController(),
      systemPrompt: 'persona prompt'
    });
    expect(workspaceWrite.permissionMode).toBe('acceptEdits');

    const bypassWithoutGate = buildSdkOptions({
      session,
      opts: { ...opts, mode: 'bypass' },
      abortController: new AbortController(),
      systemPrompt: 'persona prompt'
    });
    expect(bypassWithoutGate.permissionMode).toBe('default');

    process.env.CHIRALITY_ALLOW_SDK_BYPASS = '1';
    const bypassWithGate = buildSdkOptions({
      session,
      opts: { ...opts, mode: 'bypass' },
      abortController: new AbortController(),
      systemPrompt: 'persona prompt'
    });
    expect(bypassWithGate.permissionMode).toBe('bypassPermissions');
  });

  it('exposes requested Write/Edit/Bash only in workspaceWrite mode', () => {
    const workspaceWrite = buildSdkOptions({
      session,
      opts: { ...opts, mode: 'workspaceWrite', tools: ['read', 'write', 'Edit', 'bash'] },
      abortController: new AbortController(),
      systemPrompt: 'persona prompt'
    });

    expect(workspaceWrite.tools).toEqual(['Read', 'Write', 'Edit', 'Bash']);
    expect(workspaceWrite.allowedTools).toEqual(['Read', 'Write', 'Edit', 'Bash']);
    expect(workspaceWrite.disallowedTools).not.toContain('Write');
    expect(workspaceWrite.disallowedTools).not.toContain('Edit');
    expect(workspaceWrite.disallowedTools).not.toContain('Bash');
    expect(workspaceWrite.disallowedTools).toContain('MultiEdit');
    expect(workspaceWrite.permissionMode).toBe('acceptEdits');

    const askMode = buildSdkOptions({
      session,
      opts: { ...opts, mode: 'ask', tools: ['write', 'Edit'] },
      abortController: new AbortController(),
      systemPrompt: 'persona prompt'
    });

    expect(askMode.tools).toEqual([]);
    expect(askMode.allowedTools).toEqual([]);
    expect(askMode.disallowedTools).toContain('Write');
    expect(askMode.disallowedTools).toContain('Edit');
    expect(askMode.disallowedTools).toContain('Bash');
    expect(askMode.permissionMode).toBe('default');
  });

  it('does not attach or expose the retired SDK Agent bridge', () => {
    const options = buildSdkOptions({
      session,
      opts: {
        ...opts,
        delegatedSubagents: ['TASK'],
        mode: 'workspaceWrite',
        tools: ['read', 'Agent']
      },
      abortController: new AbortController(),
      systemPrompt: 'persona prompt'
    });

    expect(options.agents).toBeUndefined();
    expect(options.tools).toEqual(['Read']);
    expect(options.allowedTools).toEqual(['Read']);
    expect(options.disallowedTools).toContain('Agent');

    const noDelegation = buildSdkOptions({
      session,
      opts: {
        ...opts,
        tools: ['read', 'Agent']
      },
      abortController: new AbortController(),
      systemPrompt: 'persona prompt'
    });
    expect(noDelegation.tools).toEqual(['Read']);
    expect(noDelegation.allowedTools).toEqual(['Read']);
    expect(noDelegation.disallowedTools).toContain('Agent');
  });

  it('attaches a canUseTool callback backed by Chirality permission decisions', async () => {
    tmpDir = await mkdtemp(path.join(os.tmpdir(), 'chirality-sdk-options-'));
    const writableProjectRoot = path.join(tmpDir, 'project');
    const instructionRoot = path.join(tmpDir, 'instruction-root');
    await mkdir(writableProjectRoot, { recursive: true });
    await mkdir(instructionRoot, { recursive: true });
    process.env.CHIRALITY_INSTRUCTION_ROOT = instructionRoot;
    const callbackSession = { ...session, projectRoot: writableProjectRoot };

    const askOptions = buildSdkOptions({
      session: callbackSession,
      opts: { ...opts, mode: 'ask' },
      abortController: new AbortController(),
      systemPrompt: 'persona prompt'
    });

    await expect(
      askOptions.canUseTool?.(
        'Read',
        { file_path: 'README.md' },
        {
          signal: new AbortController().signal,
          toolUseID: 'tool_read'
        }
      )
    ).resolves.toMatchObject({
      behavior: 'allow',
      toolUseID: 'tool_read'
    });

    // Ask-class tools are omitted from this provider turn, so a direct
    // callback cannot bypass the exact admitted descriptor set.
    await expect(askOptions.canUseTool?.(
      'Write',
      { file_path: 'README.md', content: 'changed' },
      {
        signal: new AbortController().signal,
        toolUseID: 'tool_write'
      }
    )).resolves.toMatchObject({
      behavior: 'deny',
      message: expect.stringContaining("Unknown harness tool 'Write'")
    });

    const workspaceWriteOptions = buildSdkOptions({
      session: callbackSession,
      opts: { ...opts, mode: 'workspaceWrite' },
      abortController: new AbortController(),
      systemPrompt: 'persona prompt'
    });

    await expect(
      workspaceWriteOptions.canUseTool?.(
        'Write',
        { file_path: 'README.md', content: 'changed' },
        {
          signal: new AbortController().signal,
          toolUseID: 'tool_write_allowed'
        }
      )
    ).resolves.toMatchObject({
      behavior: 'allow',
      toolUseID: 'tool_write_allowed'
    });

    await expect(
      workspaceWriteOptions.canUseTool?.(
        'Bash',
        { command: 'npm test' },
        {
          signal: new AbortController().signal,
          toolUseID: 'tool_bash_allowed'
        }
      )
    ).resolves.toMatchObject({
      behavior: 'allow',
      toolUseID: 'tool_bash_allowed'
    });

    await expect(askOptions.canUseTool?.(
      'Bash',
      { command: 'npm test' },
      {
        signal: new AbortController().signal,
        toolUseID: 'tool_bash_ask'
      }
    )).resolves.toMatchObject({
      behavior: 'deny',
      message: expect.stringContaining("Unknown harness tool 'Bash'")
    });

    await expect(
      askOptions.canUseTool?.(
        'mystery',
        {},
        {
          signal: new AbortController().signal,
          toolUseID: 'tool_unknown'
        }
      )
    ).resolves.toMatchObject({
      behavior: 'deny',
      message: expect.stringContaining("Unknown harness tool 'mystery'"),
      toolUseID: 'tool_unknown'
    });

    // A gated ask with no addressable toolUseID must not register an unreachable
    // pending entry; it denies immediately instead of suspending.
    await expect(
      askOptions.canUseTool?.(
        'Write',
        { file_path: 'README.md', content: 'changed' },
        {
          signal: new AbortController().signal,
          toolUseID: ''
        }
      )
    ).resolves.toMatchObject({ behavior: 'deny' });
    expect(getPermissionBroker().pendingCount(callbackSession.sessionId)).toBe(0);
  });

  it('keeps inherited, deny-all, and bounded session brief scopes distinct in callbacks and hooks', async () => {
    tmpDir = await mkdtemp(path.join(os.tmpdir(), 'chirality-sdk-brief-scope-'));
    const projectRoot = path.join(tmpDir, 'project');
    const packageRoot = path.join(projectRoot, 'execution', 'PKG-01');
    await mkdir(packageRoot, { recursive: true });
    const makeOptions = (scope: Pick<SessionRecord, 'declaredContext' | 'allowedWriteTargets'>) =>
      buildSdkOptions({
        session: { ...session, projectRoot, ...scope },
        opts: { ...opts, mode: 'workspaceWrite', tools: ['read', 'write', 'bash'] },
        abortController: new AbortController(),
        systemPrompt: 'persona prompt'
      });
    const sdkCallOptions = (toolUseID: string) => ({
      signal: new AbortController().signal,
      toolUseID
    });
    const hookInput = (toolUseId: string, filePath: string) => ({
      hook_event_name: 'PreToolUse',
      tool_name: 'Write',
      tool_input: { file_path: filePath, content: 'changed' },
      tool_use_id: toolUseId
    } as never);

    const inherited = makeOptions({});
    await expect(
      inherited.canUseTool?.(
        'Write',
        { file_path: 'outside-package.md', content: 'changed' },
        sdkCallOptions('inherited-callback')
      )
    ).resolves.toMatchObject({ behavior: 'allow' });
    await expect(
      inherited.hooks?.PreToolUse?.[0]?.hooks[0]?.(
        hookInput('inherited-hook', 'outside-package.md'),
        'inherited-hook',
        { signal: new AbortController().signal }
      )
    ).resolves.toMatchObject({ continue: true });

    const denyAll = makeOptions({ declaredContext: [], allowedWriteTargets: [] });
    await expect(
      denyAll.canUseTool?.(
        'Write',
        { file_path: 'execution/PKG-01/output.md', content: 'changed' },
        sdkCallOptions('deny-all-callback')
      )
    ).resolves.toMatchObject({
      behavior: 'deny',
      message: expect.stringContaining('declared write targets')
    });
    await expect(
      denyAll.hooks?.PreToolUse?.[0]?.hooks[0]?.(
        hookInput('deny-all-hook', 'execution/PKG-01/output.md'),
        'deny-all-hook',
        { signal: new AbortController().signal }
      )
    ).resolves.toMatchObject({
      continue: false,
      decision: 'block',
      hookSpecificOutput: { permissionDecision: 'deny' }
    });

    const bounded = makeOptions({
      declaredContext: [packageRoot],
      allowedWriteTargets: [packageRoot]
    });
    await expect(
      bounded.canUseTool?.(
        'Write',
        { file_path: 'execution/PKG-01/output.md', content: 'changed' },
        sdkCallOptions('bounded-inside-callback')
      )
    ).resolves.toMatchObject({ behavior: 'allow' });
    await expect(
      bounded.canUseTool?.(
        'Write',
        { file_path: 'outside-package.md', content: 'changed' },
        sdkCallOptions('bounded-outside-callback')
      )
    ).resolves.toMatchObject({ behavior: 'deny' });
    await expect(
      bounded.hooks?.PreToolUse?.[0]?.hooks[0]?.(
        hookInput('bounded-outside-hook', 'outside-package.md'),
        'bounded-outside-hook',
        { signal: new AbortController().signal }
      )
    ).resolves.toMatchObject({ continue: false, decision: 'block' });
    await expect(
      bounded.canUseTool?.(
        'Bash',
        { command: 'npm test' },
        sdkCallOptions('bounded-shell-callback')
      )
    ).resolves.toMatchObject({ behavior: 'deny' });

    const readOnlyToolSet = buildSdkOptions({
      session: {
        ...session,
        projectRoot,
        declaredContext: [packageRoot],
        allowedWriteTargets: [packageRoot]
      },
      opts: { ...opts, mode: 'workspaceWrite', tools: ['read'] },
      abortController: new AbortController(),
      systemPrompt: 'persona prompt'
    });
    expect(readOnlyToolSet.tools).toEqual(['Read']);
    expect(readOnlyToolSet.disallowedTools).toContain('Write');
    expect(readOnlyToolSet.disallowedTools).toContain('Bash');
  });

  it('denies legacy Agent permission callbacks even for formerly eligible children', async () => {
    tmpDir = await mkdtemp(path.join(os.tmpdir(), 'chirality-sdk-agent-options-'));
    const writableProjectRoot = path.join(tmpDir, 'project');
    await mkdir(writableProjectRoot, { recursive: true });

    const options = buildSdkOptions({
      session: { ...session, projectRoot: writableProjectRoot },
      opts: {
        ...opts,
        mode: 'workspaceWrite',
        delegatedSubagents: ['TASK'],
        tools: ['Agent']
      },
      abortController: new AbortController(),
      systemPrompt: 'persona prompt'
    });

    await expect(
      options.canUseTool?.(
        'Agent',
        { agent: 'TASK', prompt: 'run this' },
        {
          signal: new AbortController().signal,
          toolUseID: 'tool_agent'
        }
      )
    ).resolves.toMatchObject({
      behavior: 'deny',
      message: expect.stringContaining("Unknown harness tool 'Agent'")
    });

    await expect(
      options.canUseTool?.(
        'Agent',
        { agent: 'UNKNOWN', prompt: 'run this' },
        {
          signal: new AbortController().signal,
          toolUseID: 'tool_agent_unknown'
        }
      )
    ).resolves.toMatchObject({
      behavior: 'deny',
      message: expect.stringContaining("Unknown harness tool 'Agent'")
    });
  });
});
