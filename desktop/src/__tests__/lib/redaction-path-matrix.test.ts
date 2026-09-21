import { mkdtemp, readFile, rm } from 'node:fs/promises';
import os from 'node:os';
import path from 'node:path';
import { afterEach, describe, expect, it } from 'vitest';
import { harnessEventToUiEvent } from '../../lib/harness/harness-ui-bridge';
import { mapSdkMessageToHarness } from '../../lib/harness/sdk-message-mapper';
import { appendHarnessEvent, replayHarnessEvents } from '../../lib/harness/session-events';
import { summarizeToolError } from '../../lib/harness/tool-evidence';

let tmpDir = '';

afterEach(async () => {
  delete process.env.ANTHROPIC_API_KEY;
  delete process.env.CHIRALITY_ANTHROPIC_API_KEY;
  delete process.env.CHIRALITY_SESSION_ROOT;
  if (tmpDir) {
    await rm(tmpDir, { recursive: true, force: true });
    tmpDir = '';
  }
});

describe('runtime redaction-path matrix', () => {
  it('redacts SDK hook diagnostics before persistence, replay, and browser display', async () => {
    tmpDir = await mkdtemp(path.join(os.tmpdir(), 'chirality-redaction-matrix-'));
    process.env.CHIRALITY_SESSION_ROOT = path.join(tmpDir, 'sessions');
    const apiKey = 'sk-test-sdk-diagnostic-secret';
    process.env.CHIRALITY_ANTHROPIC_API_KEY = apiKey;

    const mapped = mapSdkMessageToHarness('sess_redaction_matrix', {
      type: 'system',
      subtype: 'hook_response',
      hook_id: 'hook_redaction',
      hook_name: 'PostToolUse',
      hook_event: 'PostToolUse',
      outcome: 'error',
      exit_code: 1,
      stdout: `stdout ${apiKey}`,
      stderr: `stderr ${apiKey}`,
      output: { message: `output ${apiKey}`, status: 500 },
      uuid: '00000000-0000-0000-0000-000000000111',
      session_id: 'sdk_redaction_matrix'
    } as never);

    expect(mapped.harnessEvents).toHaveLength(1);
    const diagnosticEvent = mapped.harnessEvents[0];
    expect(diagnosticEvent.type).toBe('hook.failed');
    expect(JSON.stringify(diagnosticEvent)).not.toContain(apiKey);
    expect(JSON.stringify(diagnosticEvent)).toContain('[REDACTED_API_KEY]');

    const eventPath = await appendHarnessEvent(diagnosticEvent);
    const persisted = await readFile(eventPath, 'utf8');
    expect(persisted).not.toContain(apiKey);
    expect(persisted).toContain('[REDACTED_API_KEY]');

    const replay = await replayHarnessEvents('sess_redaction_matrix');
    expect(JSON.stringify(replay.events)).not.toContain(apiKey);
    expect(JSON.stringify(replay.events)).toContain('[REDACTED_API_KEY]');

    const browserEvent = harnessEventToUiEvent(diagnosticEvent);
    expect(browserEvent?.type).toBe('harness:event');
    expect(JSON.stringify(browserEvent)).not.toContain(apiKey);
    expect(JSON.stringify(browserEvent)).toContain('[REDACTED_API_KEY]');
  });

  it('redacts tool-error messages while retaining typed diagnostic metadata', () => {
    const apiKey = 'sk-test-tool-error-secret';
    process.env.ANTHROPIC_API_KEY = apiKey;

    const summary = summarizeToolError({
      name: 'ToolExecutionError',
      message: `tool failed with ${apiKey}`,
      type: 'EXECUTION_FAILURE',
      status: 502,
      rawPayload: `must not be retained ${apiKey}`
    });

    expect(summary).toEqual({
      errorName: 'ToolExecutionError',
      message: 'tool failed with [REDACTED_API_KEY]',
      type: 'EXECUTION_FAILURE',
      status: 502
    });
    expect(JSON.stringify(summary)).not.toContain(apiKey);
    expect(summary).not.toHaveProperty('rawPayload');
  });
});
