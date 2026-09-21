import type { SDKMessage, SpawnedProcess, SpawnOptions } from '@anthropic-ai/claude-agent-sdk';
import { EventEmitter } from 'node:events';
import { mkdtemp, mkdir, rm, writeFile } from 'node:fs/promises';
import os from 'node:os';
import path from 'node:path';
import { PassThrough, Writable } from 'node:stream';
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';
import { replayHarnessEvents } from '../../../lib/harness/session-events';

type SessionRecord = {
  sessionId: string;
  projectRoot: string;
  persona: string;
  mode: string;
  createdAt: string;
  updatedAt: string;
  claudeSessionId?: string;
  sdkSessionId?: string;
  sdkPackageVersion?: string;
};

type RouteModules = {
  createRoute: typeof import('../../../app/api/harness/session/create/route');
  idRoute: typeof import('../../../app/api/harness/session/[id]/route');
  turnRoute: typeof import('../../../app/api/harness/turn/route');
  runtimeModule: typeof import('../../../lib/harness/runtime');
  daemonPortModule: typeof import('../../../lib/runtime-client/daemon-harness-port');
};

type SdkOptionsBuilderModule = typeof import('../../../lib/harness/sdk-options-builder');

type TestContext = {
  tmpRoot: string;
  projectRoot: string;
  instructionRoot: string;
};

type SpawnRecord = {
  command: string;
  args: string[];
  cwd?: string;
  anthropicApiKeyAtSpawn?: string;
};

const GLOBAL_API_KEY = '__CHIRALITY_UI_API_KEY__';
const apiKeyGlobal = globalThis as typeof globalThis & Record<typeof GLOBAL_API_KEY, string | undefined>;

let context: TestContext;
let spawnRecords: SpawnRecord[] = [];

class ScriptedSdkProcess extends EventEmitter implements SpawnedProcess {
  readonly stdout = new PassThrough();
  readonly stdin = new Writable({
    write(_chunk, _encoding, callback): void {
      callback();
    }
  });

  killed = false;
  exitCode: number | null = null;

  kill(signal: NodeJS.Signals): boolean {
    if (this.exitCode !== null) {
      return false;
    }
    this.killed = true;
    this.exitCode = 130;
    this.stdout.end();
    this.emit('exit', null, signal);
    return true;
  }

  writeMessage(message: SDKMessage): void {
    this.stdout.write(`${JSON.stringify(message)}\n`);
  }

  finish(): void {
    if (this.exitCode !== null) {
      return;
    }
    this.exitCode = 0;
    this.stdout.end();
    this.emit('exit', 0, null);
  }
}

function createScriptedSpawn(options: SpawnOptions): SpawnedProcess {
  spawnRecords.push({
    command: options.command,
    args: options.args,
    cwd: options.cwd,
    anthropicApiKeyAtSpawn: options.env.ANTHROPIC_API_KEY
  });

  const process = new ScriptedSdkProcess();
  queueMicrotask(() => {
    process.writeMessage({
      type: 'system',
      subtype: 'init',
      session_id: 'sdk_dev_turn_1',
      uuid: '00000000-0000-0000-0000-000000000101',
      apiKeySource: 'temporary',
      claude_code_version: '2.1.150',
      cwd: options.cwd ?? '',
      tools: [],
      mcp_servers: [],
      model: 'claude-test',
      permissionMode: 'default',
      slash_commands: [],
      output_style: 'default',
      skills: [],
      plugins: []
    });
    process.writeMessage({
      type: 'stream_event',
      event: {
        type: 'content_block_delta',
        index: 0,
        delta: {
          type: 'text_delta',
          text: 'scripted agentSdk dev turn'
        }
      },
      parent_tool_use_id: null,
      uuid: '00000000-0000-0000-0000-000000000102',
      session_id: 'sdk_dev_turn_1'
    });
    process.writeMessage({
      type: 'result',
      subtype: 'success',
      duration_ms: 10,
      duration_api_ms: 0,
      is_error: false,
      num_turns: 1,
      result: 'scripted agentSdk dev turn',
      stop_reason: 'end_turn',
      total_cost_usd: 0,
      usage: {} as never,
      modelUsage: {},
      permission_denials: [],
      uuid: '00000000-0000-0000-0000-000000000103',
      session_id: 'sdk_dev_turn_1'
    });
    process.finish();
  });

  return process;
}

function parseSse(raw: string): Array<{ type: string; data: Record<string, unknown> }> {
  return raw
    .split('\n\n')
    .map((segment) => segment.trim())
    .filter(Boolean)
    .map((segment) => {
      const lines = segment.split('\n');
      const type = lines
        .find((line) => line.startsWith('event:'))
        ?.slice('event:'.length)
        .trim();
      const data = lines
        .filter((line) => line.startsWith('data:'))
        .map((line) => line.slice('data:'.length).trim())
        .join('\n');
      return {
        type: type ?? '',
        data: data.length > 0 ? (JSON.parse(data) as Record<string, unknown>) : {}
      };
    });
}

async function importRouteModules(): Promise<RouteModules> {
  vi.resetModules();
  vi.doMock('../../../lib/harness/sdk-options-builder', async (importOriginal) => {
    const actual = await importOriginal<SdkOptionsBuilderModule>();
    return {
      ...actual,
      buildSdkOptions(input: Parameters<SdkOptionsBuilderModule['buildSdkOptions']>[0]) {
        return {
          ...actual.buildSdkOptions(input),
          spawnClaudeCodeProcess: createScriptedSpawn
        };
      }
    };
  });

  const [
    createRoute,
    idRoute,
    turnRoute,
    runtimeModule,
    daemonPortModule,
    fakeDaemonPortModule
  ] = await Promise.all([
    import('../../../app/api/harness/session/create/route'),
    import('../../../app/api/harness/session/[id]/route'),
    import('../../../app/api/harness/turn/route'),
    import('../../../lib/harness/runtime'),
    import('../../../lib/runtime-client/daemon-harness-port'),
    import('./fake-daemon-harness-port')
  ]);
  runtimeModule.resetHarnessRuntimeForTests();
  daemonPortModule.installDaemonHarnessPort(
    fakeDaemonPortModule.createFakeDaemonHarnessPort()
  );

  return {
    createRoute,
    idRoute,
    turnRoute,
    runtimeModule,
    daemonPortModule
  };
}

async function createSession(routes: RouteModules): Promise<SessionRecord> {
  const response = await routes.createRoute.POST(
    new Request('http://localhost/api/harness/session/create', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        projectRoot: context.projectRoot,
        persona: 'WORKING_ITEMS',
        mode: 'direct'
      })
    })
  );
  expect(response.status).toBe(200);
  const body = (await response.json()) as { session: SessionRecord };
  return body.session;
}

beforeEach(async () => {
  const tmpRoot = await mkdtemp(path.join(os.tmpdir(), 'chirality-agent-sdk-dev-turn-'));
  const projectRoot = path.join(tmpRoot, 'project-root');
  const instructionRoot = path.join(tmpRoot, 'instruction-root');
  const agentsDir = path.join(instructionRoot, 'agents');
  const docsDir = path.join(instructionRoot, 'docs');

  await mkdir(projectRoot, { recursive: true });
  await mkdir(agentsDir, { recursive: true });
  await mkdir(docsDir, { recursive: true });
  await writeFile(path.join(projectRoot, 'README.md'), '# scripted dev turn fixture\n', 'utf8');
  await writeFile(path.join(instructionRoot, 'AGENTS.md'), '# agents index\n', 'utf8');
  await writeFile(path.join(instructionRoot, 'README.md'), '# instruction root\n', 'utf8');
  await writeFile(path.join(agentsDir, 'AGENT_WORKING_ITEMS.md'), '# persona fixture\n', 'utf8');
  await writeFile(path.join(docsDir, 'DIRECTIVE.md'), '# directive\n', 'utf8');
  await writeFile(path.join(docsDir, 'CONTRACT.md'), '# contract\n', 'utf8');
  await writeFile(path.join(docsDir, 'SPEC.md'), '# spec\n', 'utf8');
  await writeFile(path.join(docsDir, 'TYPES.md'), '# types\n', 'utf8');
  await writeFile(path.join(docsDir, 'PLAN.md'), '# plan\n', 'utf8');

  context = { tmpRoot, projectRoot, instructionRoot };
  spawnRecords = [];
  process.env.CHIRALITY_HARNESS_PROVIDER = 'agentSdk';
  process.env.CHIRALITY_SESSION_ROOT = path.join(tmpRoot, '.chirality', 'sessions');
  process.env.CHIRALITY_INSTRUCTION_ROOT = instructionRoot;
});

afterEach(async () => {
  vi.doUnmock('../../../lib/harness/sdk-options-builder');
  vi.resetModules();
  delete apiKeyGlobal[GLOBAL_API_KEY];
  delete process.env.CHIRALITY_HARNESS_PROVIDER;
  delete process.env.CHIRALITY_SESSION_ROOT;
  delete process.env.CHIRALITY_INSTRUCTION_ROOT;
  delete process.env.ANTHROPIC_API_KEY;
  delete process.env.CHIRALITY_ANTHROPIC_API_KEY;
  if (context?.tmpRoot) {
    await rm(context.tmpRoot, { recursive: true, force: true });
  }
});

describe('agentSdk scripted dev turn validation', () => {
  it('runs the route-level agentSdk turn through real SDK query with an offline subprocess', async () => {
    const priorEnvKey = 'prior-agent-sdk-dev-env-key';
    const uiKey = 'ui-agent-sdk-dev-turn-key';
    process.env.ANTHROPIC_API_KEY = priorEnvKey;
    apiKeyGlobal[GLOBAL_API_KEY] = uiKey;
    const routes = await importRouteModules();
    const session = await createSession(routes);

    const turnResponse = await routes.turnRoute.POST(
      new Request('http://localhost/api/harness/turn', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          sessionId: session.sessionId,
          message: 'Run the STAB-02b scripted agentSdk dev turn.',
          opts: {
            persona: 'WORKING_ITEMS',
            mode: 'direct',
            model: 'claude-test',
            maxTurns: 1,
            tools: []
          },
          attachments: []
        })
      })
    );
    const rawSse = await turnResponse.text();
    const events = parseSse(rawSse);

    expect(turnResponse.status).toBe(200);
    // turn.accepted / turn.started bridge after session:init (D-APP-25), then the
    // model.completed / turn.completed evidence before the terminal uiEvents.
    expect(events[0]).toEqual({ type: 'transport:connected', data: {} });
    expect(events.map((event) => event.type)).toEqual([
      'transport:connected',
      'session:init',
      'harness:event',
      'harness:event',
      'chat:delta',
      'harness:event',
      'harness:event',
      'chat:complete',
      'session:complete',
      'process:exit'
    ]);
    expect(spawnRecords).toHaveLength(1);
    expect(spawnRecords[0]).toMatchObject({
      cwd: context.projectRoot,
      anthropicApiKeyAtSpawn: uiKey
    });
    expect(spawnRecords[0]?.command).toContain('@anthropic-ai/claude-agent-sdk');
    expect(spawnRecords[0]?.args).toEqual(
      expect.arrayContaining(['--output-format', 'stream-json', '--input-format', 'stream-json'])
    );
    expect(process.env.ANTHROPIC_API_KEY).toBe(priorEnvKey);

    const sessionResponse = await routes.idRoute.GET(new Request('http://localhost'), {
      params: Promise.resolve({ id: session.sessionId })
    });
    expect(sessionResponse.status).toBe(200);
    const sessionBody = (await sessionResponse.json()) as { session: SessionRecord };
    expect(sessionBody.session.sdkSessionId).toBe('sdk_dev_turn_1');
    expect(sessionBody.session.sdkPackageVersion).toBe('0.3.150');

    const replay = await replayHarnessEvents(session.sessionId);
    expect(replay.events.map((event) => event.type)).toEqual([
      'message.accepted',
      'turn.accepted',
      'turn.started',
      'adapter.initialized',
      'model.delta',
      'message.delta',
      'model.completed',
      'turn.completed'
    ]);
    expect(replay.events[0]).toMatchObject({
      type: 'message.accepted',
      data: { role: 'user' }
    });
    const serializedEvidence = JSON.stringify(replay.events);
    expect(rawSse).not.toContain(uiKey);
    expect(rawSse).not.toContain(priorEnvKey);
    expect(serializedEvidence).not.toContain(uiKey);
    expect(serializedEvidence).not.toContain(priorEnvKey);
  });
});
