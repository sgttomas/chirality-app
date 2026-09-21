import { createElement } from 'react';
import { renderToStaticMarkup } from 'react-dom/server';
import { describe, expect, it } from 'vitest';
import type { HarnessEvent, HarnessEventType } from '@chirality/runtime-contracts/event-schema';
import {
  deriveSubagentActivity,
  deriveToolActivity
} from '../../lib/shell/harness-event-views';
import { SessionListPanel } from '../../components/shell/session-list-view';
import { SubagentStreamList } from '../../components/shell/subagent-stream-view';
import { ToolStreamList } from '../../components/shell/tool-stream-view';
import { TranscriptStreamList } from '../../components/shell/transcript-stream-view';
import { deriveTranscriptView } from '@chirality/runtime-contracts/transcript-replay';
import type { SessionRecord } from '@chirality/runtime-contracts/types';

let counter = 0;

function event(type: HarnessEventType, data: Record<string, unknown>): HarnessEvent {
  counter += 1;
  return {
    schemaVersion: 1,
    eventId: `evt_${counter}`,
    sessionId: 'sess_test',
    timestamp: '2026-06-18T00:00:00.000Z',
    type,
    data
  };
}

describe('ToolStreamList rendering', () => {
  it('shows an empty hint when there is no tool activity', () => {
    const html = renderToStaticMarkup(createElement(ToolStreamList, { rows: [] }));
    expect(html).toContain('No tool activity yet');
  });

  it('renders a row with tool name, status badge, and path field', () => {
    const events = [
      event('tool.queued', {
        toolUseId: 't1',
        toolName: 'Read',
        source: 'model',
        inputMetadata: { pathFields: { file_path: '/a/b.ts' } }
      }),
      event('tool.completed', { toolUseId: 't1', toolName: 'Read' })
    ];

    const html = renderToStaticMarkup(
      createElement(ToolStreamList, { rows: deriveToolActivity(events) })
    );

    expect(html).toContain('Read');
    expect(html).toContain('harness-status-badge--completed');
    expect(html).toContain('/a/b.ts');
  });
});

describe('SubagentStreamList rendering', () => {
  it('shows an empty hint when there is no subagent activity', () => {
    const html = renderToStaticMarkup(createElement(SubagentStreamList, { rows: [] }));
    expect(html).toContain('No subagent activity yet');
  });

  it('renders a row with agent name, description, and status badge', () => {
    const events = [
      event('subagent.started', {
        taskId: 'task-1',
        childRunId: 'c1',
        agentName: 'TASK',
        description: 'Investigate the failing import'
      }),
      event('subagent.completed', { taskId: 'task-1', childRunId: 'c1', outputArtifactPath: '/runs/c1.md' })
    ];

    const html = renderToStaticMarkup(
      createElement(SubagentStreamList, { rows: deriveSubagentActivity(events) })
    );

    expect(html).toContain('TASK');
    expect(html).toContain('Investigate the failing import');
    expect(html).toContain('harness-status-badge--completed');
  });
});

describe('TranscriptStreamList rendering', () => {
  it('shows an empty hint when no transcript events are loaded', () => {
    const html = renderToStaticMarkup(createElement(TranscriptStreamList, { items: [] }));
    expect(html).toContain('No transcript events loaded');
  });

  it('renders assistant messages, tool artifacts, and terminal status', () => {
    const events = [
      event('message.completed', {
        role: 'assistant',
        text: 'Created the patch.'
      }),
      event('tool.completed', {
        toolName: 'Write',
        resultMetadata: {
          contentItemCount: 1,
          contentTypes: ['text'],
          resultByteLength: 42,
          outputPersisted: true
        },
        artifactMetadata: {
          artifactRelativePath: 'artifacts/tools/write.json',
          artifactByteLength: 42,
          truncated: false
        }
      }),
      event('turn.interrupted', {
        terminalReason: 'user interrupt'
      })
    ];

    const html = renderToStaticMarkup(
      createElement(TranscriptStreamList, { items: deriveTranscriptView(events).items })
    );

    expect(html).toContain('Created the patch.');
    expect(html).toContain('Write');
    expect(html).toContain('artifacts/tools/write.json');
    expect(html).toContain('Turn interrupted');
    expect(html).toContain('harness-status-badge--failed');
  });
});

describe('SessionListPanel rendering', () => {
  const sampleSessions: SessionRecord[] = [
    {
      sessionId: 'sess_1',
      projectRoot: '/tmp/project',
      persona: 'WORKING_ITEMS',
      mode: 'CHAT',
      createdAt: '2026-06-18T00:00:00.000Z',
      updatedAt: '2026-06-18T00:00:00.000Z'
    }
  ];

  const baseProps = {
    hasProjectRoot: true,
    sessions: sampleSessions,
    loading: false,
    error: null,
    notice: null,
    openingId: null,
    streaming: false,
    onRefresh: () => {},
    onOpen: () => {}
  };

  it('prompts for a Working Root when none is selected', () => {
    const html = renderToStaticMarkup(
      createElement(SessionListPanel, { ...baseProps, hasProjectRoot: false })
    );
    expect(html).toContain('Select a Working Root');
  });

  it('renders an enabled Open button per session when idle', () => {
    const html = renderToStaticMarkup(createElement(SessionListPanel, baseProps));
    expect(html).toContain('WORKING_ITEMS');
    expect(html).toContain('>Open<');
    expect(html).not.toContain('disabled=""');
  });

  it('disables Open and warns while a turn is streaming', () => {
    const html = renderToStaticMarkup(
      createElement(SessionListPanel, { ...baseProps, streaming: true })
    );
    expect(html).toContain('A turn is running');
    // The Open button must be disabled so a mid-turn hydrate cannot replace the
    // live buffer (D-APP-22 "no same-turn mix").
    expect(html).toContain('disabled=""');
  });

  it('shows the open-result notice when not streaming', () => {
    const html = renderToStaticMarkup(
      createElement(SessionListPanel, {
        ...baseProps,
        notice: 'Loaded 3 events. View them in the Transcript / Tools / Subagents tabs.'
      })
    );
    expect(html).toContain('Loaded 3 events');
    expect(html).toContain('Transcript / Tools / Subagents');
  });
});
