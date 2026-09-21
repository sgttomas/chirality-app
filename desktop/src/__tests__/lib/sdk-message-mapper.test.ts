import { mkdtemp, readFile, rm } from 'node:fs/promises';
import os from 'node:os';
import path from 'node:path';
import { afterEach, describe, expect, it } from 'vitest';
import {
  createSdkToolEvidenceState,
  mapSdkMessageToHarness,
  mapSdkMessageToHarnessWithArtifacts
} from '../../lib/harness/sdk-message-mapper';
import { deriveSubagentActivity } from '../../lib/shell/harness-event-views';

let tmpDir = '';

afterEach(async () => {
  delete process.env.CHIRALITY_SESSION_ROOT;
  delete process.env.CHIRALITY_ANTHROPIC_API_KEY;
  if (tmpDir) {
    await rm(tmpDir, { recursive: true, force: true });
    tmpDir = '';
  }
});

describe('mapSdkMessageToHarness', () => {
  it('maps SDK init metadata to stable session:init UI event and HarnessEvent evidence', () => {
    const mapped = mapSdkMessageToHarness('sess_1', {
      type: 'system',
      subtype: 'init',
      session_id: 'sdk_1',
      uuid: '00000000-0000-0000-0000-000000000001',
      apiKeySource: 'temporary',
      claude_code_version: '1.2.3',
      cwd: '/tmp/project',
      tools: [],
      mcp_servers: [],
      model: 'claude-test',
      permissionMode: 'default',
      slash_commands: [],
      output_style: 'default',
      skills: [],
      plugins: []
    });

    expect(mapped.sdkSessionId).toBe('sdk_1');
    expect(mapped.sdkClaudeCodeVersion).toBe('1.2.3');
    expect(mapped.uiEvents).toEqual([
      {
        type: 'session:init',
        data: {
          engineSessionId: 'sdk_1',
          adapterId: 'claude-agent-sdk',
          providerId: 'anthropic',
          claudeSessionId: 'sdk_1',
          model: 'claude-test'
        }
      }
    ]);
    expect(mapped.harnessEvents[0]).toMatchObject({
      schemaVersion: 1,
      sessionId: 'sess_1',
      type: 'adapter.initialized'
    });
    expect(mapped.harnessEvents[0].data).toMatchObject({
      adapterName: 'claude-agent-sdk',
      adapterSessionId: 'sdk_1',
      sdkSessionId: 'sdk_1'
    });
  });

  it('maps stream text and terminal result without changing UI event names', () => {
    const delta = mapSdkMessageToHarness('sess_1', {
      type: 'stream_event',
      event: {
        type: 'content_block_delta',
        index: 0,
        delta: { type: 'text_delta', text: 'Hello' }
      },
      parent_tool_use_id: null,
      uuid: '00000000-0000-0000-0000-000000000002',
      session_id: 'sdk_1'
    });
    expect(delta.uiEvents).toEqual([{ type: 'chat:delta', data: { text: 'Hello' } }]);
    expect(delta.harnessEvents.map((event) => event.type)).toEqual([
      'model.delta',
      'message.delta'
    ]);

    const terminal = mapSdkMessageToHarness('sess_1', {
      type: 'result',
      subtype: 'success',
      duration_ms: 10,
      duration_api_ms: 9,
      is_error: false,
      num_turns: 1,
      result: 'Hello',
      stop_reason: 'end_turn',
      total_cost_usd: 0,
      usage: {} as never,
      modelUsage: {},
      permission_denials: [],
      uuid: '00000000-0000-0000-0000-000000000003',
      session_id: 'sdk_1'
    });

    expect(terminal.uiEvents.map((event) => event.type)).toEqual([
      'chat:complete',
      'session:complete',
      'process:exit'
    ]);
    expect(terminal.harnessEvents.map((event) => event.type)).toEqual([
      'model.completed',
      'turn.completed'
    ]);
  });

  it('maps SDK-only system messages into provider-neutral HarnessEvent types', () => {
    const permission = mapSdkMessageToHarness('sess_1', {
      type: 'system',
      subtype: 'permission_denied',
      uuid: '00000000-0000-0000-0000-000000000004',
      session_id: 'sdk_1',
      tool_name: 'Write',
      decision_reason: 'read-only mode',
      decision_reason_type: 'policy',
      message: 'permission denied'
    } as never);
    const compact = mapSdkMessageToHarness('sess_1', {
      type: 'system',
      subtype: 'compact_boundary',
      uuid: '00000000-0000-0000-0000-000000000005',
      session_id: 'sdk_1',
      compact_metadata: { preservedTurns: 3 }
    } as never);
    const mirror = mapSdkMessageToHarness('sess_1', {
      type: 'system',
      subtype: 'mirror_error',
      uuid: '00000000-0000-0000-0000-000000000006',
      session_id: 'sdk_1',
      error: 'mirror failed',
      key: 'transcript-key'
    } as never);

    expect([
      permission.harnessEvents[0].type,
      compact.harnessEvents[0].type,
      mirror.harnessEvents[0].type
    ]).toEqual(['tool.permission', 'context.compacted', 'runtime.mirror.error']);
    expect(permission.harnessEvents.map((event) => event.type)).toEqual([
      'tool.permission',
      'tool.failed'
    ]);
    expect(permission.harnessEvents[0].data).toMatchObject({
      behavior: 'deny',
      source: 'adapter',
      adapterToolName: 'Write'
    });
  });

  it('emits hook.progress and preserves progress output fields', () => {
    const mapped = mapSdkMessageToHarness('sess_1', {
      type: 'system',
      subtype: 'hook_progress',
      hook_id: 'hook_1',
      hook_name: 'PostToolUse',
      hook_event: 'after-write',
      stdout: 'halfway',
      stderr: 'warning',
      output: '50%',
      uuid: '00000000-0000-0000-0000-000000000099',
      session_id: 'sdk_1'
    } as never);

    expect(mapped.harnessEvents).toHaveLength(1);
    expect(mapped.harnessEvents[0]).toMatchObject({
      sessionId: 'sess_1',
      type: 'hook.progress',
      data: {
        hookId: 'hook_1',
        hookName: 'PostToolUse',
        hookEvent: 'after-write',
        stdout: 'halfway',
        stderr: 'warning',
        output: '50%'
      }
    });
  });

  it('maps assistant tool use and queued user messages into Chirality lifecycle events', () => {
    const assistant = mapSdkMessageToHarness('sess_1', {
      type: 'assistant',
      message: {
        role: 'assistant',
        content: [
          { type: 'text', text: 'I will inspect the file.' },
          { type: 'tool_use', id: 'toolu_1', name: 'Read', input: { file_path: 'README.md' } }
        ]
      },
      parent_tool_use_id: null,
      uuid: '00000000-0000-0000-0000-000000000007',
      session_id: 'sdk_1'
    } as never);
    expect(assistant.uiEvents).toEqual([
      { type: 'chat:delta', data: { text: 'I will inspect the file.' } }
    ]);
    expect(assistant.harnessEvents.map((event) => event.type)).toEqual([
      'model.delta',
      'message.completed',
      'tool.queued'
    ]);
    expect(assistant.harnessEvents[2].data).toMatchObject({
      source: 'model',
      toolUseId: 'toolu_1',
      toolName: 'Read',
      descriptorName: 'read_file',
      inputMetadata: {
        inputKeys: ['file_path'],
        pathFields: {
          file_path: 'README.md'
        }
      }
    });
    expect(assistant.harnessEvents[2].data).not.toHaveProperty('input');

    const queuedUser = mapSdkMessageToHarness('sess_1', {
      type: 'user',
      message: {
        role: 'user',
        content: 'follow up later'
      },
      parent_tool_use_id: null,
      isSynthetic: false,
      priority: 'later',
      shouldQuery: false,
      uuid: '00000000-0000-0000-0000-000000000008',
      session_id: 'sdk_1'
    } as never);
    expect(queuedUser.harnessEvents.map((event) => event.type)).toEqual([
      'message.completed',
      'queue.enqueued'
    ]);
  });

  it('emits SDK read built-in lifecycle evidence from queued tool use results', () => {
    const state = createSdkToolEvidenceState();
    mapSdkMessageToHarness(
      'sess_1',
      {
        type: 'assistant',
        message: {
          role: 'assistant',
          content: [
            { type: 'tool_use', id: 'toolu_read', name: 'Read', input: { file_path: 'README.md' } }
          ]
        },
        parent_tool_use_id: null,
        uuid: '00000000-0000-0000-0000-000000000014',
        session_id: 'sdk_1'
      } as never,
      state
    );

    const userResult = mapSdkMessageToHarness(
      'sess_1',
      {
        type: 'user',
        message: {
          role: 'user',
          content: []
        },
        parent_tool_use_id: 'toolu_read',
        tool_use_result: {
          type: 'tool_result',
          tool_use_id: 'toolu_read',
          content: 'raw file contents'
        },
        uuid: '00000000-0000-0000-0000-000000000015',
        session_id: 'sdk_1'
      } as never,
      state
    );

    expect(userResult.harnessEvents.map((event) => event.type)).toEqual([
      'tool.started',
      'tool.completed',
      'message.completed'
    ]);
    expect(userResult.harnessEvents[1].data).toMatchObject({
      source: 'adapter',
      toolUseId: 'toolu_read',
      toolName: 'Read',
      descriptorName: 'read_file',
      resultMetadata: {
        resultByteLength: expect.any(Number),
        inlineByteLimit: 65536,
        artifactByteLimit: 2097152,
        overflowPolicy: 'artifact',
        budgetClass: 'within-inline-budget',
        rawOutputPersisted: false
      }
    });
    expect(JSON.stringify(userResult.harnessEvents[1].data)).not.toContain('raw file contents');
  });

  it('emits SDK write built-in lifecycle evidence from queued tool use results', () => {
    const state = createSdkToolEvidenceState();
    mapSdkMessageToHarness(
      'sess_1',
      {
        type: 'assistant',
        message: {
          role: 'assistant',
          content: [
            {
              type: 'tool_use',
              id: 'toolu_write',
              name: 'Write',
              input: { file_path: 'notes.md', content: 'raw changed content' }
            }
          ]
        },
        parent_tool_use_id: null,
        uuid: '00000000-0000-0000-0000-000000000019',
        session_id: 'sdk_1'
      } as never,
      state
    );

    const userResult = mapSdkMessageToHarness(
      'sess_1',
      {
        type: 'user',
        message: {
          role: 'user',
          content: []
        },
        parent_tool_use_id: 'toolu_write',
        tool_use_result: {
          type: 'tool_result',
          tool_use_id: 'toolu_write',
          content: 'updated notes.md'
        },
        uuid: '00000000-0000-0000-0000-000000000020',
        session_id: 'sdk_1'
      } as never,
      state
    );

    expect(userResult.harnessEvents.map((event) => event.type)).toEqual([
      'tool.started',
      'tool.completed',
      'message.completed'
    ]);
    expect(userResult.harnessEvents[1].data).toMatchObject({
      source: 'adapter',
      toolUseId: 'toolu_write',
      toolName: 'Write',
      descriptorName: 'write_file',
      resultMetadata: {
        resultByteLength: expect.any(Number),
        inlineByteLimit: 16384,
        artifactByteLimit: 524288,
        overflowPolicy: 'artifact',
        rawOutputPersisted: false
      }
    });
    expect(JSON.stringify(userResult.harnessEvents[1].data)).not.toContain('updated notes.md');
  });

  it('emits SDK Bash lifecycle evidence with stdout and stderr metadata only', () => {
    const state = createSdkToolEvidenceState();
    mapSdkMessageToHarness(
      'sess_1',
      {
        type: 'assistant',
        message: {
          role: 'assistant',
          content: [
            {
              type: 'tool_use',
              id: 'toolu_bash',
              name: 'Bash',
              input: { command: 'npm test', timeout: 120000 }
            }
          ]
        },
        parent_tool_use_id: null,
        uuid: '00000000-0000-0000-0000-000000000021',
        session_id: 'sdk_1'
      } as never,
      state
    );

    const userResult = mapSdkMessageToHarness(
      'sess_1',
      {
        type: 'user',
        message: {
          role: 'user',
          content: []
        },
        parent_tool_use_id: 'toolu_bash',
        tool_use_result: {
          type: 'tool_result',
          tool_use_id: 'toolu_bash',
          stdout: 'test output',
          stderr: 'warn',
          interrupted: false
        },
        uuid: '00000000-0000-0000-0000-000000000022',
        session_id: 'sdk_1'
      } as never,
      state
    );

    expect(userResult.harnessEvents.map((event) => event.type)).toEqual([
      'tool.started',
      'tool.completed',
      'message.completed'
    ]);
    expect(userResult.harnessEvents[1].data).toMatchObject({
      source: 'adapter',
      toolUseId: 'toolu_bash',
      toolName: 'Bash',
      descriptorName: 'shell',
      resultMetadata: {
        inlineByteLimit: 16384,
        artifactByteLimit: 2097152,
        overflowPolicy: 'artifact',
        rawOutputPersisted: false
      },
      shellResultMetadata: {
        stdoutPresent: true,
        stderrPresent: true,
        stdoutByteLength: 11,
        stderrByteLength: 4,
        interrupted: false
      }
    });
    expect(JSON.stringify(userResult.harnessEvents[1].data)).not.toContain('test output');
  });

  it('maps interrupted SDK Bash results to failed evidence with stream metadata', () => {
    const state = createSdkToolEvidenceState();
    mapSdkMessageToHarness(
      'sess_1',
      {
        type: 'assistant',
        message: {
          role: 'assistant',
          content: [
            {
              type: 'tool_use',
              id: 'toolu_bash_interrupted',
              name: 'Bash',
              input: { command: 'sleep 60', timeout: 120000 }
            }
          ]
        },
        parent_tool_use_id: null,
        uuid: '00000000-0000-0000-0000-000000000033',
        session_id: 'sdk_1'
      } as never,
      state
    );

    const userResult = mapSdkMessageToHarness(
      'sess_1',
      {
        type: 'user',
        message: {
          role: 'user',
          content: []
        },
        parent_tool_use_id: 'toolu_bash_interrupted',
        tool_use_result: {
          type: 'tool_result',
          tool_use_id: 'toolu_bash_interrupted',
          stdout: 'partial output',
          stderr: 'Interrupted',
          interrupted: true
        },
        uuid: '00000000-0000-0000-0000-000000000034',
        session_id: 'sdk_1'
      } as never,
      state
    );

    expect(userResult.harnessEvents.map((event) => event.type)).toEqual([
      'tool.started',
      'tool.failed',
      'message.completed'
    ]);
    expect(userResult.harnessEvents[1].data).toMatchObject({
      source: 'adapter',
      toolUseId: 'toolu_bash_interrupted',
      toolName: 'Bash',
      descriptorName: 'shell',
      failureSource: 'tool_use_result',
      shellResultMetadata: {
        stdoutPresent: true,
        stderrPresent: true,
        stdoutByteLength: 14,
        stderrByteLength: 11,
        interrupted: true
      }
    });
    expect(JSON.stringify(userResult.harnessEvents[1].data)).not.toContain('partial output');
    expect(JSON.stringify(userResult.harnessEvents[1].data)).not.toContain('Interrupted');
  });

  it('persists SDK built-in overflow results through the async mapper path', async () => {
    tmpDir = await mkdtemp(path.join(os.tmpdir(), 'chirality-sdk-mapper-'));
    process.env.CHIRALITY_SESSION_ROOT = path.join(tmpDir, 'sessions');
    process.env.CHIRALITY_ANTHROPIC_API_KEY = 'sk-test-secret';
    const state = createSdkToolEvidenceState();
    mapSdkMessageToHarness(
      'sess_1',
      {
        type: 'assistant',
        message: {
          role: 'assistant',
          content: [
            { type: 'tool_use', id: 'toolu_read', name: 'Read', input: { file_path: 'README.md' } }
          ]
        },
        parent_tool_use_id: null,
        uuid: '00000000-0000-0000-0000-000000000023',
        session_id: 'sdk_1'
      } as never,
      state
    );

    const userResult = await mapSdkMessageToHarnessWithArtifacts(
      'sess_1',
      {
        type: 'user',
        message: {
          role: 'user',
          content: []
        },
        parent_tool_use_id: 'toolu_read',
        tool_use_result: {
          type: 'tool_result',
          tool_use_id: 'toolu_read',
          content: `${'x'.repeat(70 * 1024)} sk-test-secret`
        },
        uuid: '00000000-0000-0000-0000-000000000024',
        session_id: 'sdk_1'
      } as never,
      state
    );

    expect(userResult.harnessEvents.map((event) => event.type)).toEqual([
      'tool.started',
      'tool.completed',
      'message.completed'
    ]);
    expect(userResult.harnessEvents[1].data).toMatchObject({
      resultMetadata: {
        budgetClass: 'requires-artifact-overflow',
        outputPersisted: true,
        rawOutputPersisted: false
      },
      artifactMetadata: {
        artifactPath: expect.any(String),
        sha256: expect.stringMatching(/^[a-f0-9]{64}$/),
        toolName: 'Read',
        retentionPolicy: 'session-lifetime',
        redacted: true,
        truncated: false
      }
    });
    expect(JSON.stringify(userResult.harnessEvents[1].data)).not.toContain('sk-test-secret');
    expect(JSON.stringify(userResult.harnessEvents[1].data)).not.toContain('x'.repeat(128));
    const artifactPath = (userResult.harnessEvents[1].data.artifactMetadata as {
      artifactPath: string;
    }).artifactPath;
    const artifact = await readFile(artifactPath, 'utf8');
    expect(artifact).not.toContain('sk-test-secret');
    expect(artifact).toContain('[REDACTED_API_KEY]');
  });

  it('maps SDK read tool error results to failed evidence and skips duplicate MCP completions', () => {
    const state = createSdkToolEvidenceState();
    mapSdkMessageToHarness(
      'sess_1',
      {
        type: 'assistant',
        message: {
          role: 'assistant',
          content: [
            { type: 'tool_use', id: 'toolu_grep', name: 'Grep', input: { pattern: 'needle' } },
            {
              type: 'tool_use',
              id: 'toolu_mcp',
              name: 'mcp__chirality__status_read',
              input: { deliverablePath: 'PKG/DEL' }
            }
          ]
        },
        parent_tool_use_id: null,
        uuid: '00000000-0000-0000-0000-000000000016',
        session_id: 'sdk_1'
      } as never,
      state
    );

    const failedRead = mapSdkMessageToHarness(
      'sess_1',
      {
        type: 'user',
        message: {
          role: 'user',
          content: []
        },
        parent_tool_use_id: 'toolu_grep',
        tool_use_result: {
          type: 'tool_result',
          tool_use_id: 'toolu_grep',
          is_error: true,
          content: 'grep failed'
        },
        uuid: '00000000-0000-0000-0000-000000000017',
        session_id: 'sdk_1'
      } as never,
      state
    );
    const mcpResult = mapSdkMessageToHarness(
      'sess_1',
      {
        type: 'user',
        message: {
          role: 'user',
          content: []
        },
        parent_tool_use_id: 'toolu_mcp',
        tool_use_result: {
          type: 'tool_result',
          tool_use_id: 'toolu_mcp',
          content: 'mcp result body'
        },
        uuid: '00000000-0000-0000-0000-000000000018',
        session_id: 'sdk_1'
      } as never,
      state
    );

    expect(failedRead.harnessEvents.map((event) => event.type)).toEqual([
      'tool.started',
      'tool.failed',
      'message.completed'
    ]);
    expect(failedRead.harnessEvents[1].data).toMatchObject({
      failureSource: 'tool_use_result',
      resultMetadata: {
        rawOutputPersisted: false
      }
    });
    expect(JSON.stringify(failedRead.harnessEvents[1].data)).not.toContain('grep failed');
    expect(mcpResult.harnessEvents.map((event) => event.type)).toEqual(['message.completed']);
  });

  it('maps SDK tool, hook, status, and subagent messages into expanded HarnessEvent categories', () => {
    const toolProgress = mapSdkMessageToHarness('sess_1', {
      type: 'tool_progress',
      tool_use_id: 'toolu_1',
      tool_name: 'Read',
      parent_tool_use_id: null,
      elapsed_time_seconds: 1.5,
      uuid: '00000000-0000-0000-0000-000000000009',
      session_id: 'sdk_1'
    } as never);
    const hookStarted = mapSdkMessageToHarness('sess_1', {
      type: 'system',
      subtype: 'hook_started',
      hook_id: 'hook_1',
      hook_name: 'PreToolUse',
      hook_event: 'PreToolUse',
      uuid: '00000000-0000-0000-0000-000000000010',
      session_id: 'sdk_1'
    } as never);
    const hookFailed = mapSdkMessageToHarness('sess_1', {
      type: 'system',
      subtype: 'hook_response',
      hook_id: 'hook_1',
      hook_name: 'PreToolUse',
      hook_event: 'PreToolUse',
      output: 'denied',
      stdout: '',
      stderr: 'blocked',
      exit_code: 1,
      outcome: 'error',
      uuid: '00000000-0000-0000-0000-000000000011',
      session_id: 'sdk_1'
    } as never);
    const status = mapSdkMessageToHarness('sess_1', {
      type: 'system',
      subtype: 'status',
      status: 'compacting',
      permissionMode: 'default',
      uuid: '00000000-0000-0000-0000-000000000012',
      session_id: 'sdk_1'
    } as never);
    const task = mapSdkMessageToHarness('sess_1', {
      type: 'system',
      subtype: 'task_started',
      task_id: 'task_1',
      tool_use_id: 'toolu_2',
      description: 'Run bounded task',
      subagent_type: 'TASK',
      uuid: '00000000-0000-0000-0000-000000000013',
      session_id: 'sdk_1'
    } as never);
    const notification = mapSdkMessageToHarness('sess_1', {
      type: 'system',
      subtype: 'task_notification',
      task_id: 'task_1',
      tool_use_id: 'toolu_2',
      status: 'completed',
      output_file: '/tmp/chirality-child-output.json',
      summary: 'child done',
      usage: {},
      skip_transcript: true,
      uuid: '00000000-0000-0000-0000-000000000014',
      session_id: 'sdk_1'
    } as never);

    expect([
      toolProgress.harnessEvents[0].type,
      hookStarted.harnessEvents[0].type,
      hookFailed.harnessEvents[0].type,
      status.harnessEvents[0].type,
      task.harnessEvents[0].type,
      notification.harnessEvents[0].type
    ]).toEqual([
      'tool.progress',
      'hook.started',
      'hook.failed',
      'context.compaction.started',
      'subagent.started',
      'subagent.completed'
    ]);
    expect(notification.harnessEvents[0].data).toMatchObject({
      taskId: 'task_1',
      toolUseId: 'toolu_2',
      outputFile: '/tmp/chirality-child-output.json',
      summary: 'child done'
    });
  });

  it('maps compaction and terminal result messages as lifecycle boundary evidence', () => {
    const compacting = mapSdkMessageToHarness('sess_1', {
      type: 'system',
      subtype: 'status',
      status: 'compacting',
      permissionMode: 'default',
      uuid: '00000000-0000-0000-0000-000000000035',
      session_id: 'sdk_1'
    } as never);
    const compacted = mapSdkMessageToHarness('sess_1', {
      type: 'system',
      subtype: 'status',
      status: 'ready',
      compact_result: 'success',
      uuid: '00000000-0000-0000-0000-000000000036',
      session_id: 'sdk_1'
    } as never);
    const compactFailed = mapSdkMessageToHarness('sess_1', {
      type: 'system',
      subtype: 'status',
      status: 'ready',
      compact_result: 'failed',
      compact_error: 'compaction failed',
      uuid: '00000000-0000-0000-0000-000000000037',
      session_id: 'sdk_1'
    } as never);
    const completed = mapSdkMessageToHarness('sess_1', {
      type: 'result',
      subtype: 'success',
      duration_ms: 10,
      duration_api_ms: 9,
      is_error: false,
      num_turns: 1,
      result: 'done',
      stop_reason: 'end_turn',
      total_cost_usd: 0,
      usage: {} as never,
      modelUsage: {},
      permission_denials: [],
      uuid: '00000000-0000-0000-0000-000000000038',
      session_id: 'sdk_1'
    });
    const failed = mapSdkMessageToHarness('sess_1', {
      type: 'result',
      subtype: 'error',
      duration_ms: 10,
      duration_api_ms: 9,
      is_error: true,
      num_turns: 1,
      result: '',
      stop_reason: 'error',
      terminal_reason: 'adapter_error',
      total_cost_usd: 0,
      usage: {} as never,
      modelUsage: {},
      permission_denials: [],
      errors: ['adapter failed'],
      uuid: '00000000-0000-0000-0000-000000000039',
      session_id: 'sdk_1'
    } as never);

    expect(compacting.harnessEvents.map((event) => event.type)).toEqual([
      'context.compaction.started'
    ]);
    expect(compacted.harnessEvents.map((event) => event.type)).toEqual(['context.compacted']);
    expect(compacted.harnessEvents[0].data).toMatchObject({
      compactResult: 'success',
      replayImplication: 'sdk_transcript_linkage_required'
    });
    expect(compactFailed.harnessEvents.map((event) => event.type)).toEqual([
      'context.compaction.failed'
    ]);
    expect(compactFailed.harnessEvents[0].data).toMatchObject({
      compactResult: 'failed',
      compactError: 'compaction failed'
    });
    expect(completed.harnessEvents.map((event) => event.type)).toEqual([
      'model.completed',
      'turn.completed'
    ]);
    expect(failed.harnessEvents.map((event) => event.type)).toEqual(['turn.failed']);
    expect(failed.harnessEvents[0].data).toMatchObject({
      subtype: 'error',
      terminalReason: 'adapter_error'
    });
  });

  it('embeds adapter-observed child-run records in SDK task lifecycle events', () => {
    const state = createSdkToolEvidenceState({
      parentPersona: 'WORKING_ITEMS',
      projectRoot: '/tmp/chirality-project',
      mode: 'workspaceWrite',
      parentTurnId: 'turn_1'
    });
    const started = mapSdkMessageToHarness(
      'sess_parent',
      {
        type: 'system',
        subtype: 'task_started',
        task_id: 'task_1',
        tool_use_id: 'toolu_agent',
        description: 'Run bounded task',
        subagent_type: 'TASK',
        task_type: 'agent',
        workflow_name: 'bounded-task',
        skip_transcript: true,
        uuid: '00000000-0000-0000-0000-000000000025',
        session_id: 'sdk_1'
      } as never,
      state
    );
    const completed = mapSdkMessageToHarness(
      'sess_parent',
      {
        type: 'system',
        subtype: 'task_notification',
        task_id: 'task_1',
        tool_use_id: 'toolu_agent',
        status: 'completed',
        output_file: '/tmp/chirality-child-output.json',
        summary: 'child done',
        usage: {},
        skip_transcript: true,
        uuid: '00000000-0000-0000-0000-000000000026',
        session_id: 'sdk_1'
      } as never,
      state
    );

    expect(started.harnessEvents[0].data).toMatchObject({
      childRunId: expect.stringMatching(/^child_/),
      parentSessionId: 'sess_parent',
      parentTurnId: 'turn_1',
      parentPersona: 'WORKING_ITEMS',
      agentName: 'TASK',
      projectRoot: '/tmp/chirality-project',
      mode: 'workspaceWrite',
      status: 'running',
      capabilityPolicy: {
        inheritParentCapabilities: false,
        allowedToolNames: [],
        deniedCapabilities: ['read', 'write', 'shell', 'mcp', 'network', 'subagent']
      },
      governance: {
        state: 'adapter-observed'
      },
      adapter: {
        adapterName: 'claude-agent-sdk',
        adapterSessionId: 'sdk_1',
        adapterTaskId: 'task_1',
        adapterToolUseId: 'toolu_agent'
      }
    });
    expect(completed.harnessEvents[0].data).toMatchObject({
      childRunId: started.harnessEvents[0].data.childRunId,
      status: 'completed',
      outputArtifactPath: '/tmp/chirality-child-output.json',
      adapter: {
        adapterTaskId: 'task_1'
      }
    });
  });

  it('materializes over-inline child output summaries as redacted session artifacts', async () => {
    tmpDir = await mkdtemp(path.join(os.tmpdir(), 'chirality-child-output-artifacts-'));
    process.env.CHIRALITY_SESSION_ROOT = path.join(tmpDir, 'sessions');
    process.env.CHIRALITY_ANTHROPIC_API_KEY = 'sk-test-secret';

    const state = createSdkToolEvidenceState({
      parentPersona: 'WORKING_ITEMS',
      projectRoot: '/tmp/chirality-project',
      mode: 'workspaceWrite',
      parentTurnId: 'turn_1'
    });
    const started = await mapSdkMessageToHarnessWithArtifacts(
      'sess_parent',
      {
        type: 'system',
        subtype: 'task_started',
        task_id: 'task_1',
        tool_use_id: 'toolu_agent',
        description: 'Run bounded task',
        subagent_type: 'TASK',
        task_type: 'agent',
        workflow_name: 'bounded-task',
        skip_transcript: true,
        uuid: '00000000-0000-0000-0000-000000000040',
        session_id: 'sdk_1'
      } as never,
      state
    );
    const completed = await mapSdkMessageToHarnessWithArtifacts(
      'sess_parent',
      {
        type: 'system',
        subtype: 'task_notification',
        task_id: 'task_1',
        tool_use_id: 'toolu_agent',
        status: 'completed',
        output_file: '/tmp/chirality-child-output.json',
        summary: `${'child output '.repeat(1800)} sk-test-secret`,
        usage: {
          total_tokens: 25,
          tool_uses: 2,
          duration_ms: 50
        },
        skip_transcript: true,
        uuid: '00000000-0000-0000-0000-000000000041',
        session_id: 'sdk_1'
      } as never,
      state
    );

    const completedEvent = completed.harnessEvents[0];
    expect(completedEvent.data).toMatchObject({
      childRunId: started.harnessEvents[0].data.childRunId,
      status: 'completed',
      outputArtifactPath: path.join(
        'sess_parent',
        'artifacts',
        'subagents',
        'task_1-TASK.json'
      ),
      childOutputArtifactMetadata: {
        artifactPath: expect.any(String),
        artifactRelativePath: path.join(
          'sess_parent',
          'artifacts',
          'subagents',
          'task_1-TASK.json'
        ),
        artifactByteLength: expect.any(Number),
        originalByteLength: expect.any(Number),
        sha256: expect.stringMatching(/^[a-f0-9]{64}$/),
        toolName: 'Agent',
        turnId: 'turn_1',
        taskId: 'task_1',
        childRunId: started.harnessEvents[0].data.childRunId,
        toolUseId: 'toolu_agent',
        sourceOutputFile: '/tmp/chirality-child-output.json',
        redacted: true,
        truncated: false,
        retentionPolicy: 'session-lifetime'
      }
    });

    expect(JSON.stringify(completedEvent.data)).not.toContain('sk-test-secret');
    const artifactPath = (
      completedEvent.data.childOutputArtifactMetadata as {
        artifactPath: string;
      }
    ).artifactPath;
    const artifact = await readFile(artifactPath, 'utf8');
    expect(artifact).not.toContain('sk-test-secret');
    expect(artifact).toContain('[REDACTED_API_KEY]');
    expect(artifact).toContain('"toolName": "Agent"');
    expect(artifact).toContain('"turnId": "turn_1"');

    const rows = deriveSubagentActivity([
      started.harnessEvents[0],
      completed.harnessEvents[0]
    ]);
    expect(rows).toHaveLength(1);
    expect(rows[0]).toMatchObject({
      key: 'task_1',
      agentName: 'TASK',
      status: 'completed',
      outputArtifactPath: path.join(
        'sess_parent',
        'artifacts',
        'subagents',
        'task_1-TASK.json'
      ),
      eventCount: 2
    });
  });
});
