import React from 'react';
import { renderToStaticMarkup } from 'react-dom/server';
import { act, create, type ReactTestRenderer } from 'react-test-renderer';
import { describe, expect, it, vi } from 'vitest';
import { AgentsProjection } from '../../components/woven-dialogue/agents-projection';
import { buildRecordedAgentHierarchy } from '../../lib/woven-dialogue/recorded-agent-hierarchy';

const removedMetadata = [
  'pi',
  'omlx',
  'local-model',
  'Currency:',
  'session:root-session',
  '2026-07-23T10:00:00Z',
  'artifact:return',
  'approval:record',
  'status unknown',
  'INVALID_CURRENCY',
  'missing-parent',
  'root-session',
  'child-session'
];

function fullHierarchy() {
  return buildRecordedAgentHierarchy([
    {
      sessionId: 'supervisor-session',
      sourceReference: 'session:supervisor-session',
      observedAt: '2026-07-23T09:59:00Z',
      persona: 'HELP_HUMAN',
      role: 'agent0'
    },
    {
      sessionId: 'root-session',
      sourceReference: 'session:root-session',
      observedAt: '2026-07-23T10:00:00Z',
      currency: 'CURRENT',
      persona: 'WORKING_ITEMS',
      role: 'agent1',
      status: 'running',
      engineSelection: { adapterId: 'pi', providerId: 'omlx', model: 'local-model' },
      outputArtifact: 'artifact:return',
      approvalRef: 'approval:record'
    },
    {
      sessionId: 'child-session',
      parentSessionId: 'root-session',
      sourceReference: 'session:child-session',
      observedAt: '2026-07-23T10:01:00Z',
      persona: 'TASK',
      role: 'agent2'
    },
    {
      sessionId: 'unknown-session',
      sourceReference: 'session:unknown-session',
      observedAt: '2026-07-23T10:02:00Z',
      currency: 'invalid'
    },
    {
      sessionId: 'detached-session',
      parentSessionId: 'missing-parent',
      sourceReference: 'session:detached-session',
      observedAt: '2026-07-23T10:03:00Z',
      persona: 'RESEARCH',
      role: 'agent1'
    }
  ]);
}

function renderProjection(
  overrides: Partial<React.ComponentProps<typeof AgentsProjection>> = {}
): string {
  return renderToStaticMarkup(
    <AgentsProjection
      hierarchy={fullHierarchy()}
      loading={false}
      error={null}
      selectionDisabled={false}
      onRefresh={vi.fn()}
      onSelectSession={vi.fn()}
      {...overrides}
    />
  );
}

describe('Agents projection minimal presentation', () => {
  it('shows recorded agent type, persona, and human-readable tree relationships', () => {
    const html = renderProjection();

    expect(html).toContain('<strong>Type 1</strong><span>Role: WORKING_ITEMS</span>');
    expect(html).toContain('<strong>Type 2</strong><span>Role: TASK</span>');
    expect(html).toContain('<strong>Type 0</strong><span>Role: HELP_HUMAN</span>');
    expect(html).toContain('Top-level');
    expect(html).toContain('Parent: WORKING_ITEMS');
    expect(html).toContain('Agents reporting to WORKING_ITEMS');
  });

  it('omits unknown type and persona without inferring either', () => {
    const html = renderProjection();
    const unknownRoot = html.match(/<button[^>]*><small>Top-level<\/small><\/button>/g);

    expect(unknownRoot).toHaveLength(1);
    expect(html).not.toContain('Role not recorded');
    expect(html).not.toContain('Agent type unknown');
  });

  it('uses plain relationship-unavailable language for detached agents', () => {
    const html = renderProjection();

    expect(html).toContain('<h3>Parent relationship unavailable</h3>');
    expect(html).toContain('<strong>Type 1</strong><span>Role: RESEARCH</span>');
    expect(html.match(/Parent relationship unavailable/g)).toHaveLength(2);
    expect(html).not.toContain('unresolved');
    expect(html).not.toContain('conflicting');
  });

  it('does not expose runtime, provenance, identifier, evidence, or diagnostic metadata', () => {
    const html = renderProjection();

    for (const text of removedMetadata) {
      expect(html).not.toContain(text);
    }
  });

  it('keeps refresh and error access, including the loading guard', () => {
    const refresh = vi.fn();
    let tree: ReactTestRenderer;

    act(() => {
      tree = create(
        <AgentsProjection
          hierarchy={fullHierarchy()}
          loading={false}
          error="Agents could not be refreshed."
          selectionDisabled={false}
          onRefresh={refresh}
          onSelectSession={vi.fn()}
        />
      );
    });
    const refreshButton = tree!.root.findAllByType('button')[0];
    act(() => refreshButton.props.onClick());
    expect(refresh).toHaveBeenCalledTimes(1);
    expect(tree!.root.findByProps({ role: 'alert' }).children.join('')).toBe(
      'Agents could not be refreshed.'
    );

    act(() => {
      tree!.update(
        <AgentsProjection
          hierarchy={fullHierarchy()}
          loading
          error={null}
          selectionDisabled={false}
          onRefresh={refresh}
          onSelectSession={vi.fn()}
        />
      );
    });
    expect(tree!.root.findAllByType('button')[0].props.disabled).toBe(true);
    expect(tree!.root.findAllByType('button')[0].children.join('')).toBe('Refreshing…');
  });

  it('preserves selected and disabled session selection with the recorded session id internally', () => {
    const selectSession = vi.fn();
    let tree: ReactTestRenderer;

    act(() => {
      tree = create(
        <AgentsProjection
          hierarchy={fullHierarchy()}
          loading={false}
          error={null}
          selectedSessionId="child-session"
          selectionDisabled={false}
          onRefresh={vi.fn()}
          onSelectSession={selectSession}
        />
      );
    });
    const agentButtons = tree!.root.findAllByType('button').slice(1);
    const selected = agentButtons.find((button) => button.props['aria-pressed'] === true);
    expect(selected?.props.className).toContain('woven-agent-card--selected');
    act(() => selected?.props.onClick());
    expect(selectSession).toHaveBeenCalledWith('child-session');

    act(() => {
      tree!.update(
        <AgentsProjection
          hierarchy={fullHierarchy()}
          loading={false}
          error={null}
          selectionDisabled
          onRefresh={vi.fn()}
          onSelectSession={selectSession}
        />
      );
    });
    expect(tree!.root.findAllByType('button').slice(1).every((button) => button.props.disabled)).toBe(
      true
    );
    expect(tree!.root.findByProps({ role: 'status' }).children.join('')).toContain(
      'Agent selection is paused'
    );
  });
});
