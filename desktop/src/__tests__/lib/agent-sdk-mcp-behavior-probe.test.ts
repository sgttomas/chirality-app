import {
  query,
  type HookInput,
  type HookJSONOutput,
  type SpawnedProcess,
  type SpawnOptions
} from '@anthropic-ai/claude-agent-sdk';
import { EventEmitter } from 'node:events';
import { mkdtemp, mkdir, rm, writeFile } from 'node:fs/promises';
import os from 'node:os';
import path from 'node:path';
import { PassThrough, Writable } from 'node:stream';
import { afterEach, beforeEach, describe, expect, it } from 'vitest';
import { buildSdkOptions } from '../../lib/harness/sdk-options-builder';
import { replayHarnessEvents } from '../../lib/harness/session-events';
import type { ResolvedOpts, SessionRecord } from '@chirality/runtime-contracts/types';

const MCP_TOOL_NAME = 'mcp__chirality__status_read';
const SESSION_ID = 'sess_sdk_mcp_behavior_probe';
const SDK_SESSION_ID = 'sdk_mcp_behavior_probe_1';

const STATUS_DOCUMENT = `# Status: DEL-05-03 Lifecycle State Handling

**Current State:** INITIALIZED
**Last Updated:** 2026-02-22

## History
- 2026-02-22 - State set to INITIALIZED (4_DOCUMENTS)
`;

type FixtureContext = {
  tmpRoot: string;
  projectRoot: string;
  deliverablePath: string;
};

type JsonRecord = Record<string, unknown>;

type ControlResponseMessage = {
  type: 'control_response';
  response: {
    subtype: string;
    request_id: string;
    response?: JsonRecord;
    error?: string;
  };
};

type ProbeState = {
  projectRoot: string;
  deliverablePath: string;
  sentinelHookInputs: HookInput[];
};

let fixture: FixtureContext;

function isRecord(value: unknown): value is JsonRecord {
  return Boolean(value) && typeof value === 'object' && !Array.isArray(value);
}

function readString(value: unknown): string | undefined {
  return typeof value === 'string' ? value : undefined;
}

function readRecord(value: unknown): JsonRecord | undefined {
  return isRecord(value) ? value : undefined;
}

function readArray(value: unknown): unknown[] {
  return Array.isArray(value) ? value : [];
}

function initializationResponse(): JsonRecord {
  return {
    commands: [],
    agents: [],
    output_style: 'default',
    available_output_styles: ['default'],
    models: [],
    account: {
      apiKeySource: 'temporary',
      apiProvider: 'firstParty'
    }
  };
}

function sdkSystemInitMessage(projectRoot: string): JsonRecord {
  return {
    type: 'system',
    subtype: 'init',
    session_id: SDK_SESSION_ID,
    uuid: '00000000-0000-0000-0000-000000000301',
    apiKeySource: 'temporary',
    claude_code_version: '2.1.150',
    cwd: projectRoot,
    tools: [MCP_TOOL_NAME],
    mcp_servers: [{ name: 'chirality', status: 'connected' }],
    model: 'claude-test',
    permissionMode: 'acceptEdits',
    slash_commands: [],
    output_style: 'default',
    skills: [],
    plugins: []
  };
}

function sdkResultMessage(): JsonRecord {
  return {
    type: 'result',
    subtype: 'success',
    duration_ms: 10,
    duration_api_ms: 0,
    is_error: false,
    num_turns: 1,
    result: 'sdk MCP behavior probe complete',
    stop_reason: 'end_turn',
    total_cost_usd: 0,
    usage: {},
    modelUsage: {},
    permission_denials: [],
    uuid: '00000000-0000-0000-0000-000000000302',
    session_id: SDK_SESSION_ID
  };
}

function mcpInitializeMessage(): JsonRecord {
  return {
    jsonrpc: '2.0',
    id: 'mcp-init',
    method: 'initialize',
    params: {
      protocolVersion: '2025-03-26',
      capabilities: {},
      clientInfo: {
        name: 'chirality-agent-sdk-mcp-behavior-probe',
        version: '1.0.0'
      }
    }
  };
}

function mcpInitializedNotification(): JsonRecord {
  return {
    jsonrpc: '2.0',
    method: 'notifications/initialized'
  };
}

function mcpStatusReadCall(deliverablePath: string): JsonRecord {
  return {
    jsonrpc: '2.0',
    id: 'mcp-call-status',
    method: 'tools/call',
    params: {
      name: 'status_read',
      arguments: {
        deliverablePath
      }
    }
  };
}

function preToolUseHookInput(input: ProbeState): JsonRecord {
  return {
    session_id: SDK_SESSION_ID,
    transcript_path: path.join(input.projectRoot, '.probe-transcript.jsonl'),
    cwd: input.projectRoot,
    permission_mode: 'acceptEdits',
    hook_event_name: 'PreToolUse',
    tool_name: MCP_TOOL_NAME,
    tool_input: {
      deliverablePath: input.deliverablePath
    },
    tool_use_id: 'toolu_probe_hook'
  };
}

class SdkMcpBehaviorProbeProcess extends EventEmitter implements SpawnedProcess {
  readonly stdout = new PassThrough();
  readonly stdin: Writable;
  readonly controlResponses: ControlResponseMessage[] = [];
  readonly hostMessages: JsonRecord[] = [];

  killed = false;
  exitCode: number | null = null;
  initializeRequest: JsonRecord | undefined;
  sentinelHookCallbackId: string | undefined;

  private stdinBuffer = '';
  private completed = false;

  constructor(
    private readonly spawnOptions: SpawnOptions,
    private readonly probe: ProbeState
  ) {
    super();

    this.stdin = new Writable({
      write: (chunk, _encoding, callback): void => {
        try {
          this.consumeStdin(typeof chunk === 'string' ? chunk : chunk.toString('utf8'));
          callback();
        } catch (error) {
          callback(error instanceof Error ? error : new Error(String(error)));
        }
      }
    });

    this.spawnOptions.signal.addEventListener(
      'abort',
      () => {
        this.kill('SIGTERM');
      },
      { once: true }
    );
  }

  kill(signal: NodeJS.Signals): boolean {
    if (this.exitCode !== null) {
      return false;
    }
    this.killed = true;
    this.exitCode = signal === 'SIGTERM' || signal === 'SIGINT' ? 130 : 1;
    this.stdout.end();
    this.emit('exit', null, signal);
    return true;
  }

  private consumeStdin(raw: string): void {
    this.stdinBuffer += raw;
    for (;;) {
      const newlineIndex = this.stdinBuffer.indexOf('\n');
      if (newlineIndex < 0) {
        return;
      }
      const line = this.stdinBuffer.slice(0, newlineIndex).trim();
      this.stdinBuffer = this.stdinBuffer.slice(newlineIndex + 1);
      if (line.length === 0) {
        continue;
      }
      this.handleHostMessage(JSON.parse(line) as JsonRecord);
    }
  }

  private handleHostMessage(message: JsonRecord): void {
    this.hostMessages.push(message);
    if (message.type === 'control_request') {
      const request = readRecord(message.request);
      if (request?.subtype === 'initialize') {
        this.handleInitialize(message, request);
      }
      return;
    }

    if (message.type === 'control_response') {
      const response = readRecord(message.response);
      const requestId = readString(response?.request_id);
      if (!requestId || !response) {
        return;
      }
      const controlResponse = message as ControlResponseMessage;
      this.controlResponses.push(controlResponse);
      this.advanceAfterControlResponse(requestId);
    }
  }

  private handleInitialize(message: JsonRecord, request: JsonRecord): void {
    this.initializeRequest = request;
    this.sentinelHookCallbackId = this.readSentinelHookCallbackId(request);

    this.writeJson({
      type: 'control_response',
      response: {
        subtype: 'success',
        request_id: message.request_id,
        response: initializationResponse()
      }
    });
    this.writeJson(sdkSystemInitMessage(this.probe.projectRoot));
    setTimeout(() => {
      this.sendControlRequest('mcp_initialize', {
        subtype: 'mcp_message',
        server_name: 'chirality',
        message: mcpInitializeMessage()
      });
    }, 0);
  }

  private readSentinelHookCallbackId(request: JsonRecord): string | undefined {
    const hooks = readRecord(request.hooks);
    const preToolUseMatchers = readArray(hooks?.PreToolUse);
    const sentinelMatcher = preToolUseMatchers
      .map(readRecord)
      .find((matcher) => matcher?.matcher === MCP_TOOL_NAME);
    return readString(readArray(sentinelMatcher?.hookCallbackIds)[0]);
  }

  private advanceAfterControlResponse(requestId: string): void {
    if (requestId === 'mcp_initialize') {
      this.sendControlRequest('mcp_initialized_notification', {
        subtype: 'mcp_message',
        server_name: 'chirality',
        message: mcpInitializedNotification()
      });
      return;
    }

    if (requestId === 'mcp_initialized_notification') {
      this.sendControlRequest('mcp_call_status', {
        subtype: 'mcp_message',
        server_name: 'chirality',
        message: mcpStatusReadCall(this.probe.deliverablePath)
      });
      return;
    }

    if (requestId === 'mcp_call_status') {
      this.sendControlRequest('can_use_tool_status', {
        subtype: 'can_use_tool',
        tool_name: MCP_TOOL_NAME,
        input: {
          deliverablePath: this.probe.deliverablePath
        },
        tool_use_id: 'toolu_probe_permission'
      });
      return;
    }

    if (requestId === 'can_use_tool_status') {
      if (!this.sentinelHookCallbackId) {
        throw new Error('SDK initialize request did not include the sentinel hook callback ID.');
      }
      this.sendControlRequest('hook_callback_status', {
        subtype: 'hook_callback',
        callback_id: this.sentinelHookCallbackId,
        input: preToolUseHookInput(this.probe),
        tool_use_id: 'toolu_probe_hook'
      });
      return;
    }

    if (requestId === 'hook_callback_status') {
      this.finishSuccessfully();
    }
  }

  private sendControlRequest(requestId: string, request: JsonRecord): void {
    this.writeJson({
      type: 'control_request',
      request_id: requestId,
      request
    });
  }

  private writeJson(message: JsonRecord): void {
    if (this.exitCode !== null) {
      return;
    }
    this.stdout.write(`${JSON.stringify(message)}\n`);
  }

  private finishSuccessfully(): void {
    if (this.completed || this.exitCode !== null) {
      return;
    }
    this.completed = true;
    this.writeJson(sdkResultMessage());
    this.exitCode = 0;
    this.stdout.end();
    this.emit('exit', 0, null);
  }
}

function createSessionRecord(projectRoot: string): SessionRecord {
  return {
    sessionId: SESSION_ID,
    projectRoot,
    persona: 'WORKING_ITEMS',
    mode: 'workspaceWrite',
    createdAt: '2026-06-16T00:00:00.000Z',
    updatedAt: '2026-06-16T00:00:00.000Z'
  };
}

function createResolvedOpts(): ResolvedOpts {
  return {
    model: 'claude-test',
    tools: ['status_read'],
    maxTurns: 1,
    persona: 'WORKING_ITEMS',
    mode: 'workspaceWrite'
  };
}

function findControlSuccess(
  process: SdkMcpBehaviorProbeProcess,
  requestId: string
): JsonRecord {
  const response = process.controlResponses.find(
    (item) => item.response.request_id === requestId
  );
  expect(response?.response.subtype).toBe('success');
  return response?.response.response ?? {};
}

function extractMcpResponse(controlResponse: JsonRecord): JsonRecord {
  const mcpResponse = readRecord(controlResponse.mcp_response);
  expect(mcpResponse).toBeDefined();
  return mcpResponse ?? {};
}

function extractStatusText(mcpResponse: JsonRecord): string {
  const result = readRecord(mcpResponse.result);
  const content = readArray(result?.content);
  const firstContent = readRecord(content[0]);
  const text = readString(firstContent?.text);
  expect(text).toBeDefined();
  return text ?? '';
}

beforeEach(async () => {
  const tmpRoot = await mkdtemp(path.join(os.tmpdir(), 'chirality-agent-sdk-mcp-probe-'));
  const projectRoot = path.join(tmpRoot, 'project-root');
  const deliverablePath = path.join(
    projectRoot,
    'PKG-05_Filesystem_Execution_Model',
    '1_Working',
    'DEL-05-03_Lifecycle_State_Handling'
  );

  await mkdir(deliverablePath, { recursive: true });
  await writeFile(path.join(deliverablePath, '_STATUS.md'), STATUS_DOCUMENT, 'utf8');

  fixture = {
    tmpRoot,
    projectRoot,
    deliverablePath
  };
  process.env.CHIRALITY_SESSION_ROOT = path.join(tmpRoot, 'sessions');
});

afterEach(async () => {
  delete process.env.CHIRALITY_SESSION_ROOT;
  if (fixture?.tmpRoot) {
    await rm(fixture.tmpRoot, { recursive: true, force: true });
  }
});

describe('agentSdk MCP behavior probe', () => {
  it('shows SDK MCP messages do not automatically invoke permission or hook callbacks', async () => {
    const sentinelHookInputs: HookInput[] = [];
    const options = buildSdkOptions({
      session: createSessionRecord(fixture.projectRoot),
      opts: createResolvedOpts(),
      abortController: new AbortController(),
      systemPrompt: 'STAB-04 SDK MCP behavior probe'
    });

    options.hooks = {
      ...options.hooks,
      PreToolUse: [
        ...(options.hooks?.PreToolUse ?? []),
        {
          matcher: MCP_TOOL_NAME,
          hooks: [
            async (hookInput): Promise<HookJSONOutput> => {
              sentinelHookInputs.push(hookInput);
              return {
                continue: true,
                hookSpecificOutput: {
                  hookEventName: 'PreToolUse',
                  permissionDecision: 'allow'
                }
              };
            }
          ]
        }
      ]
    };

    let spawnedProcess: SdkMcpBehaviorProbeProcess | undefined;
    options.spawnClaudeCodeProcess = (spawnOptions): SpawnedProcess => {
      spawnedProcess = new SdkMcpBehaviorProbeProcess(spawnOptions, {
        projectRoot: fixture.projectRoot,
        deliverablePath: fixture.deliverablePath,
        sentinelHookInputs
      });
      return spawnedProcess;
    };

    const sdkMessages = [];
    for await (const message of query({
      prompt: 'Probe in-process MCP permission and hook behavior.',
      options
    })) {
      sdkMessages.push(message);
    }

    if (!spawnedProcess) {
      throw new Error('Expected SDK query to spawn the probe process.');
    }

    expect(sdkMessages.map((message) => message.type)).toContain('result');
    expect(spawnedProcess.initializeRequest).toMatchObject({
      subtype: 'initialize',
      sdkMcpServers: ['chirality']
    });
    expect(spawnedProcess.sentinelHookCallbackId).toMatch(/^hook_/);

    const mcpStatusResponse = extractMcpResponse(
      findControlSuccess(spawnedProcess, 'mcp_call_status')
    );
    expect(mcpStatusResponse).toMatchObject({
      jsonrpc: '2.0',
      id: 'mcp-call-status'
    });
    expect(JSON.parse(extractStatusText(mcpStatusResponse))).toMatchObject({
      status: {
        currentState: 'INITIALIZED'
      }
    });

    const permissionResponse = findControlSuccess(spawnedProcess, 'can_use_tool_status');
    expect(permissionResponse).toMatchObject({
      behavior: 'allow',
      toolUseID: 'toolu_probe_permission'
    });

    const hookResponse = findControlSuccess(spawnedProcess, 'hook_callback_status');
    expect(hookResponse).toMatchObject({
      continue: true,
      hookSpecificOutput: {
        hookEventName: 'PreToolUse',
        permissionDecision: 'allow'
      }
    });
    expect(sentinelHookInputs).toHaveLength(1);
    expect(sentinelHookInputs[0]).toMatchObject({
      hook_event_name: 'PreToolUse',
      tool_name: MCP_TOOL_NAME,
      tool_use_id: 'toolu_probe_hook'
    });

    const replay = await replayHarnessEvents(SESSION_ID);
    expect(replay.events.map((event) => event.type)).toEqual([
      'tool.started',
      'tool.completed',
      'tool.permission'
    ]);
    expect(replay.events[0].data).toMatchObject({
      source: 'chirality-mcp',
      toolName: 'status_read',
      adapterToolName: MCP_TOOL_NAME
    });
    expect(replay.events[2].data).toMatchObject({
      behavior: 'allow',
      source: 'sdk-callback',
      toolName: MCP_TOOL_NAME,
      toolUseId: 'toolu_probe_permission'
    });
  });
});
