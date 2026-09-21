import React from 'react';
import { renderToStaticMarkup } from 'react-dom/server';
import { describe, expect, it, vi } from 'vitest';
import { ActivityShelf } from '../../components/woven-dialogue/activity-shelf';
import { CoordinationPanel } from '../../components/woven-dialogue/coordination-panel';

vi.mock('../../components/shell/tool-stream-view', () => ({
  ToolStreamView: () => <div>Tools projection</div>
}));
vi.mock('../../components/shell/transcript-stream-view', () => ({
  TranscriptStreamView: () => <div>Events projection</div>
}));
vi.mock('../../components/shell/subagent-stream-view', () => ({
  SubagentStreamView: () => <div>Children projection</div>
}));

describe('Woven Dialogue view controls', () => {
  it('uses ordinary pressed buttons rather than incomplete ARIA tab widgets', () => {
    const coordination = renderToStaticMarkup(
      <CoordinationPanel
        activeView="session"
        replaySlot={<div>Selected replay</div>}
        hierarchy={{
          roots: [],
          detached: [],
          childrenByParentSessionId: {},
          unresolvedParentSessionIds: [],
          diagnostics: []
        }}
        sessionsLoading={false}
        sessionsError={null}
        selectionDisabled={false}
        onSelectView={vi.fn()}
        onRefreshSessions={vi.fn()}
        onSelectSession={vi.fn()}
      />
    );
    const activity = renderToStaticMarkup(
      <ActivityShelf collapsed={false} onToggleCollapsed={vi.fn()} />
    );

    expect(coordination).toContain('aria-pressed="true"');
    expect(coordination).toContain('Session</button>');
    expect(coordination).toContain('Agents</button>');
    expect(coordination).toContain('Selected replay');
    expect(coordination).not.toContain('Work</button>');
    expect(activity).toContain('aria-pressed="true"');
    expect(coordination).not.toContain('role="tab"');
    expect(activity).not.toContain('role="tab"');
    expect(activity).toContain('Live runtime projection');
  });
});
