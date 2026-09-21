import { mkdir, mkdtemp, readFile, rm, writeFile } from 'node:fs/promises';
import os from 'node:os';
import path from 'node:path';
import { afterEach, describe, expect, it } from 'vitest';
import { createHarnessEvent } from '../../lib/harness/event-factory';
import { HARNESS_EVENT_TYPES } from '@chirality/runtime-contracts/event-schema';
import { appendHarnessEvent, replayHarnessEvents } from '../../lib/harness/session-events';

let tmpDir = '';

afterEach(async () => {
  delete process.env.CHIRALITY_SESSION_ROOT;
  delete process.env.CHIRALITY_ANTHROPIC_API_KEY;
  if (tmpDir) {
    await rm(tmpDir, { recursive: true, force: true });
    tmpDir = '';
  }
});

describe('session events', () => {
  it('keeps canonical HarnessEvent types provider-neutral', () => {
    expect(HARNESS_EVENT_TYPES.join(' ')).not.toMatch(/sdk|claude|anthropic/i);
    expect(HARNESS_EVENT_TYPES).toEqual(
      expect.arrayContaining([
        'message.completed',
        'tool.queued',
        'tool.started',
        'tool.progress',
        'tool.completed',
        'tool.failed',
        'hook.started',
        'hook.progress',
        'hook.completed',
        'queue.enqueued',
        'branch.summarized',
        'interruption.requested',
        'interruption.completed',
        'turn.interrupted',
        'context.compaction.started',
        'context.compacted',
        'subagent.started',
        'subagent.completed'
      ])
    );
  });

  it('persists and replays hook.progress payloads without dropping output fields', async () => {
    tmpDir = await mkdtemp(path.join(os.tmpdir(), 'chirality-session-events-'));
    process.env.CHIRALITY_SESSION_ROOT = path.join(tmpDir, 'sessions');
    await appendHarnessEvent(createHarnessEvent({
      sessionId: 'sess_hook',
      type: 'hook.progress',
      data: { hookId: 'hook_1', stdout: 'halfway', stderr: 'warning', output: '50%' }
    }));

    const replay = await replayHarnessEvents('sess_hook');
    expect(replay.summary.eventTypeCounts).toMatchObject({ 'hook.progress': 1 });
    expect(replay.events[0]).toMatchObject({
      type: 'hook.progress',
      data: { hookId: 'hook_1', stdout: 'halfway', stderr: 'warning', output: '50%' }
    });
  });

  it('appends and replays HarnessEvent JSONL records', async () => {
    tmpDir = await mkdtemp(path.join(os.tmpdir(), 'chirality-session-events-'));
    process.env.CHIRALITY_SESSION_ROOT = path.join(tmpDir, 'sessions');
    const event = createHarnessEvent({
      sessionId: 'sess_1',
      type: 'turn.accepted',
      data: {
        apiKey: 'not-a-real-key'
      }
    });

    const filePath = await appendHarnessEvent(event);
    const replay = await replayHarnessEvents('sess_1');

    expect(filePath).toContain(path.join('sessions', 'sess_1', 'events.jsonl'));
    expect(replay.malformedLineCount).toBe(0);
    expect(replay.summary).toMatchObject({
      eventCount: 1,
      malformedLineCount: 0,
      eventTypeCounts: {
        'turn.accepted': 1
      },
      firstTimestamp: expect.any(String),
      lastTimestamp: expect.any(String)
    });
    expect(replay.events).toHaveLength(1);
    expect(replay.events[0]).toMatchObject({
      schemaVersion: 1,
      sessionId: 'sess_1',
      type: 'turn.accepted'
    });
  });

  it('summarizes full replay coverage and preserves artifact references without raw secrets', async () => {
    tmpDir = await mkdtemp(path.join(os.tmpdir(), 'chirality-session-events-'));
    const sessionRoot = path.join(tmpDir, 'sessions');
    process.env.CHIRALITY_SESSION_ROOT = sessionRoot;
    process.env.CHIRALITY_ANTHROPIC_API_KEY = 'sk-test-secret';

    const sessionId = 'sess_full';
    const artifactPath = path.join(sessionRoot, sessionId, 'artifacts', 'tools', 'tool.json');
    await mkdir(path.dirname(artifactPath), { recursive: true });
    await writeFile(artifactPath, '{"redacted":true}\n', 'utf8');

    const events = [
      createHarnessEvent({
        sessionId,
        type: 'turn.accepted',
        data: { apiKey: 'sk-test-secret' }
      }),
      createHarnessEvent({
        sessionId,
        type: 'message.delta',
        data: { role: 'assistant', text: 'delta' }
      }),
      createHarnessEvent({
        sessionId,
        type: 'message.completed',
        data: { role: 'assistant', source: 'model' }
      }),
      createHarnessEvent({
        sessionId,
        type: 'tool.permission',
        data: { behavior: 'allow', toolName: 'Read' }
      }),
      createHarnessEvent({
        sessionId,
        type: 'tool.started',
        data: { toolName: 'Read' }
      }),
      createHarnessEvent({
        sessionId,
        type: 'tool.completed',
        data: {
          toolName: 'Read',
          resultMetadata: {
            outputPersisted: true,
            rawOutputPersisted: false
          },
          artifactMetadata: {
            artifactPath,
            redacted: true
          }
        }
      }),
      createHarnessEvent({
        sessionId,
        type: 'hook.completed',
        data: {
          hookName: 'chirality.write.post_tool_use',
          artifactMetadata: {
            artifactPath,
            redacted: true
          }
        }
      }),
      createHarnessEvent({
        sessionId,
        type: 'subagent.started',
        data: { childRunId: 'child_1', parentSessionId: sessionId }
      }),
      createHarnessEvent({
        sessionId,
        type: 'subagent.completed',
        data: {
          childRunId: 'child_1',
          parentSessionId: sessionId,
          outputArtifactPath: artifactPath
        }
      }),
      createHarnessEvent({
        sessionId,
        type: 'turn.completed',
        data: { totalCostUsd: 0 }
      }),
      createHarnessEvent({
        sessionId,
        type: 'turn.failed',
        data: { error: 'synthetic coverage failure branch' }
      })
    ];

    let eventFilePath = '';
    for (const event of events) {
      eventFilePath = await appendHarnessEvent(event);
    }
    await writeFile(eventFilePath, 'not-json\n', { encoding: 'utf8', flag: 'a' });

    const replay = await replayHarnessEvents(sessionId);

    expect(replay.malformedLineCount).toBe(1);
    expect(replay.summary).toMatchObject({
      eventCount: events.length,
      malformedLineCount: 1,
      eventTypeCounts: {
        'turn.accepted': 1,
        'message.delta': 1,
        'message.completed': 1,
        'tool.permission': 1,
        'tool.started': 1,
        'tool.completed': 1,
        'hook.completed': 1,
        'subagent.started': 1,
        'subagent.completed': 1,
        'turn.completed': 1,
        'turn.failed': 1
      },
      firstTimestamp: events[0].timestamp,
      lastTimestamp: events[events.length - 1].timestamp
    });
    expect(JSON.stringify(replay.events)).not.toContain('sk-test-secret');
    expect(JSON.stringify(replay.events)).toContain('[REDACTED_API_KEY]');
    await expect(readFile(artifactPath, 'utf8')).resolves.toContain('"redacted":true');
  });

  it('redacts raw imported JSONL records at replay time', async () => {
    tmpDir = await mkdtemp(path.join(os.tmpdir(), 'chirality-session-events-'));
    const sessionRoot = path.join(tmpDir, 'sessions');
    process.env.CHIRALITY_SESSION_ROOT = sessionRoot;
    process.env.CHIRALITY_ANTHROPIC_API_KEY = 'sk-test-secret';

    const sessionId = 'sess_imported';
    const eventsDir = path.join(sessionRoot, sessionId);
    await mkdir(eventsDir, { recursive: true });
    await writeFile(
      path.join(eventsDir, 'events.jsonl'),
      `${JSON.stringify({
        schemaVersion: 1,
        eventId: 'evt_imported',
        sessionId,
        timestamp: '2026-06-21T00:00:00.000Z',
        type: 'turn.accepted',
        data: {
          apiKey: 'sk-test-secret',
          nested: {
            Authorization: 'Bearer sk-test-secret'
          }
        }
      })}\n`,
      'utf8'
    );

    const replay = await replayHarnessEvents(sessionId);
    const serialized = JSON.stringify(replay.events);

    expect(serialized).not.toContain('sk-test-secret');
    expect(serialized).toContain('[REDACTED_API_KEY]');
  });

  it('replays interleaved tool artifact events in append order with checksum metadata', async () => {
    tmpDir = await mkdtemp(path.join(os.tmpdir(), 'chirality-session-events-'));
    const sessionRoot = path.join(tmpDir, 'sessions');
    process.env.CHIRALITY_SESSION_ROOT = sessionRoot;

    const sessionId = 'sess_interleaved';
    const events = [
      createHarnessEvent({
        sessionId,
        turnId: 'turn_1',
        type: 'tool.started',
        data: { toolUseId: 'tool_a', toolName: 'Read' }
      }),
      createHarnessEvent({
        sessionId,
        turnId: 'turn_1',
        type: 'tool.started',
        data: { toolUseId: 'tool_b', toolName: 'Write' }
      }),
      createHarnessEvent({
        sessionId,
        turnId: 'turn_1',
        type: 'tool.completed',
        data: {
          toolUseId: 'tool_b',
          toolName: 'Write',
          artifactMetadata: {
            artifactRelativePath: path.join(sessionId, 'artifacts', 'tools', 'tool_b-Write.json'),
            toolName: 'Write',
            turnId: 'turn_1',
            sha256: 'b'.repeat(64),
            retentionPolicy: 'session-lifetime',
            redacted: true,
            truncated: false
          }
        }
      }),
      createHarnessEvent({
        sessionId,
        turnId: 'turn_1',
        type: 'tool.completed',
        data: {
          toolUseId: 'tool_a',
          toolName: 'Read',
          artifactMetadata: {
            artifactRelativePath: path.join(sessionId, 'artifacts', 'tools', 'tool_a-Read.json'),
            toolName: 'Read',
            turnId: 'turn_1',
            sha256: 'a'.repeat(64),
            retentionPolicy: 'session-lifetime',
            redacted: true,
            truncated: false
          }
        }
      }),
      createHarnessEvent({
        sessionId,
        turnId: 'turn_1',
        type: 'turn.completed',
        data: { stopReason: 'end_turn' }
      })
    ];

    for (const event of events) {
      await appendHarnessEvent(event);
    }

    const replay = await replayHarnessEvents(sessionId);

    expect(replay.events.map((event) => event.eventId)).toEqual(
      events.map((event) => event.eventId)
    );
    expect(replay.events.map((event) => event.type)).toEqual([
      'tool.started',
      'tool.started',
      'tool.completed',
      'tool.completed',
      'turn.completed'
    ]);
    expect(replay.events[2].data.artifactMetadata).toMatchObject({
      toolName: 'Write',
      turnId: 'turn_1',
      sha256: 'b'.repeat(64),
      retentionPolicy: 'session-lifetime'
    });
    expect(replay.events[3].data.artifactMetadata).toMatchObject({
      toolName: 'Read',
      turnId: 'turn_1',
      sha256: 'a'.repeat(64),
      retentionPolicy: 'session-lifetime'
    });
  });
});
