import { mkdtemp, readFile, rm } from 'node:fs/promises';
import { createHash } from 'node:crypto';
import os from 'node:os';
import path from 'node:path';
import { afterEach, beforeEach, describe, expect, it } from 'vitest';
import {
  persistChildOutputArtifact,
  persistToolResultArtifact
} from '../../lib/harness/tool-result-artifacts';
import { getHarnessToolDescriptor } from '@chirality/runtime-contracts/tool-descriptor';

let tmpDir = '';

beforeEach(async () => {
  tmpDir = await mkdtemp(path.join(os.tmpdir(), 'chirality-tool-artifacts-'));
  process.env.CHIRALITY_SESSION_ROOT = path.join(tmpDir, 'sessions');
});

afterEach(async () => {
  delete process.env.CHIRALITY_SESSION_ROOT;
  delete process.env.CHIRALITY_ANTHROPIC_API_KEY;
  if (tmpDir) {
    await rm(tmpDir, { recursive: true, force: true });
    tmpDir = '';
  }
});

function sha256Hex(value: string): string {
  return createHash('sha256').update(value, 'utf8').digest('hex');
}

describe('tool result artifacts', () => {
  it('skips persistence for inline-sized results', async () => {
    await expect(
      persistToolResultArtifact({
        sessionId: 'sess_artifact',
        toolUseId: 'tool_read',
        toolName: 'Read',
        descriptor: getHarnessToolDescriptor('Read'),
        result: {
          content: [{ type: 'text', text: 'small result' }]
        }
      })
    ).resolves.toBeUndefined();
  });

  it('persists over-inline results as redacted artifact files', async () => {
    process.env.CHIRALITY_ANTHROPIC_API_KEY = 'sk-test-secret';

    const metadata = await persistToolResultArtifact({
      sessionId: 'sess_artifact',
      turnId: 'turn_1',
      toolUseId: 'tool_read',
      toolName: 'Read',
      descriptor: getHarnessToolDescriptor('Read'),
      result: {
        content: [{ type: 'text', text: `${'x'.repeat(70 * 1024)} sk-test-secret` }]
      }
    });

    expect(metadata).toMatchObject({
      artifactRelativePath: path.join('sess_artifact', 'artifacts', 'tools', 'tool_read-Read.json'),
      redacted: true,
      truncated: false,
      toolName: 'Read',
      turnId: 'turn_1',
      retentionPolicy: 'session-lifetime',
      sha256: expect.stringMatching(/^[a-f0-9]{64}$/),
      originalByteLength: expect.any(Number),
      artifactByteLength: expect.any(Number)
    });

    const artifact = await readFile(metadata?.artifactPath as string, 'utf8');
    expect(metadata?.sha256).toBe(sha256Hex(artifact));
    expect(artifact).not.toContain('sk-test-secret');
    expect(artifact).toContain('[REDACTED_API_KEY]');
    expect(artifact).toContain('"toolName": "Read"');
    expect(artifact).toContain('"turnId": "turn_1"');
  });

  it('truncates results that exceed the artifact budget', async () => {
    const metadata = await persistToolResultArtifact({
      sessionId: 'sess_artifact',
      toolUseId: 'tool_huge',
      toolName: 'Read',
      descriptor: getHarnessToolDescriptor('Read'),
      result: {
        content: [{ type: 'text', text: 'x'.repeat(3 * 1024 * 1024) }]
      }
    });

    expect(metadata).toMatchObject({
      redacted: true,
      truncated: true,
      retentionPolicy: 'session-lifetime',
      sha256: expect.stringMatching(/^[a-f0-9]{64}$/)
    });
    const artifact = await readFile(metadata?.artifactPath as string, 'utf8');
    expect(metadata?.sha256).toBe(sha256Hex(artifact));
    expect(artifact).toContain('"truncated": true');
    expect(artifact.length).toBeLessThan(128 * 1024);
  });
});

describe('child output artifacts', () => {
  it('skips persistence for inline-sized child output summaries', async () => {
    await expect(
      persistChildOutputArtifact({
        sessionId: 'sess_child',
        turnId: 'turn_1',
        taskId: 'task_1',
        childRunId: 'child_1',
        toolUseId: 'toolu_agent',
        agentName: 'TASK',
        status: 'completed',
        outputFile: '/tmp/child-output.json',
        summary: 'small child output'
      })
    ).resolves.toBeUndefined();
  });

  it('persists over-inline child output summaries with redacted linkage metadata', async () => {
    process.env.CHIRALITY_ANTHROPIC_API_KEY = 'sk-test-secret';

    const metadata = await persistChildOutputArtifact({
      sessionId: 'sess_child',
      turnId: 'turn_1',
      taskId: 'task_1',
      childRunId: 'child_1',
      toolUseId: 'toolu_agent',
      agentName: 'TASK',
      status: 'completed',
      outputFile: '/tmp/child-output.json',
      summary: `${'x'.repeat(20 * 1024)} sk-test-secret`,
      usage: {
        total_tokens: 12,
        tool_uses: 1,
        duration_ms: 34
      }
    });

    expect(metadata).toMatchObject({
      artifactRelativePath: path.join('sess_child', 'artifacts', 'subagents', 'task_1-TASK.json'),
      redacted: true,
      truncated: false,
      toolName: 'Agent',
      turnId: 'turn_1',
      taskId: 'task_1',
      childRunId: 'child_1',
      toolUseId: 'toolu_agent',
      sourceOutputFile: '/tmp/child-output.json',
      retentionPolicy: 'session-lifetime',
      sha256: expect.stringMatching(/^[a-f0-9]{64}$/),
      originalByteLength: expect.any(Number),
      artifactByteLength: expect.any(Number)
    });

    const artifact = await readFile(metadata?.artifactPath as string, 'utf8');
    expect(metadata?.sha256).toBe(sha256Hex(artifact));
    expect(artifact).not.toContain('sk-test-secret');
    expect(artifact).toContain('[REDACTED_API_KEY]');
    expect(artifact).toContain('"toolName": "Agent"');
    expect(artifact).toContain('"turnId": "turn_1"');
    expect(artifact).toContain('"taskId": "task_1"');
  });

  it('truncates child output summaries that exceed the artifact budget', async () => {
    const metadata = await persistChildOutputArtifact({
      sessionId: 'sess_child',
      taskId: 'task_huge',
      agentName: 'TASK',
      status: 'completed',
      outputFile: '/tmp/huge-child-output.json',
      summary: 'x'.repeat(800 * 1024)
    });

    expect(metadata).toMatchObject({
      redacted: true,
      truncated: true,
      toolName: 'Agent',
      retentionPolicy: 'session-lifetime',
      sha256: expect.stringMatching(/^[a-f0-9]{64}$/)
    });
    const artifact = await readFile(metadata?.artifactPath as string, 'utf8');
    expect(metadata?.sha256).toBe(sha256Hex(artifact));
    expect(artifact).toContain('"truncated": true');
    expect(artifact.length).toBeLessThan(64 * 1024);
  });
});
