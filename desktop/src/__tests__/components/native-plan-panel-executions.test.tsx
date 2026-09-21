import React from 'react';
import { act, create, type ReactTestRenderer } from 'react-test-renderer';
import { afterEach, describe, expect, it, vi } from 'vitest';
import type { NativePlanRevision } from '@chirality/runtime-contracts';
import type { PlanExecutionRecord } from '../../lib/harness/plan-executions';

vi.mock('../../components/shell/chat-markdown', () => ({ ChatMarkdown: (props: { source: string }) => <p>{props.source}</p> }));

import { NativePlanPanel, type NativePlanPanelModel } from '../../components/shell/native-plan-panel';

/**
 * Item 16: every plan revision keeps its identity and its execution history.
 * The panel reports not executed, running, completed, interrupted or failed
 * per revision and attempt; an executed revision offers Run again rather than
 * reading as awaiting first execution; earlier revisions stay executable.
 */
const revision = (number: number): NativePlanRevision => ({ revision: number, sourceEvent: { plan: `Plan text ${number}` } } as unknown as NativePlanRevision);
function model(overrides: Partial<NativePlanPanelModel> = {}): NativePlanPanelModel {
  return { revisions: [revision(1), revision(2)], clarifications: [], active: true, refreshing: false, fileCatalog: [], actionsDisabled: false,
    onRefresh: vi.fn(), onRevise: vi.fn(), onSave: vi.fn(), onExecute: vi.fn(), onSaveAsWorkflow: vi.fn(), onReplyClarification: vi.fn(), ...overrides };
}
let tree: ReactTestRenderer | undefined;
afterEach(() => { if (tree) act(() => tree!.unmount()); tree = undefined; });
const render = (value: NativePlanPanelModel) => { act(() => { tree = create(<NativePlanPanel model={value} />); }); };
const statusOf = (rev: number) => tree!.root.findByProps({ 'data-plan-revision': rev, className: 'native-plan-execution' });
const buttons = () => tree!.root.findAllByType('button').map(node => ({ label: node.children.join(''), disabled: Boolean(node.props.disabled) }));

describe('plan execution lifecycle', () => {
  it('reads every revision as not executed before any execution, and as prepared while the request sits in the composer', () => {
    render(model());
    expect(statusOf(2).props['data-execution-status']).toBe('none');
    expect(statusOf(2).children.join('')).toBe('Not executed');
    expect(statusOf(1).props['data-execution-status']).toBe('none');
    expect(buttons().find(button => button.label === 'Execute plan')).toEqual({ label: 'Execute plan', disabled: false });
    expect(buttons().find(button => button.label === 'Execute this revision')).toEqual({ label: 'Execute this revision', disabled: false });

    render(model({ preparedRevision: 2 }));
    expect(statusOf(2).props['data-execution-status']).toBe('prepared');
    expect(statusOf(2).children.join('')).toContain('send it to run this revision');
  });

  it('shows running with the attempt, disables re-execution of a running revision, and keeps the other revision independent', () => {
    const executions: PlanExecutionRecord[] = [
      { revision: 2, attempt: 1, startedAt: '2026-09-12T10:05:00.000Z', status: 'failed', endedAt: '2026-09-12T10:06:00.000Z' },
      { revision: 2, attempt: 2, startedAt: '2026-09-12T10:07:00.000Z', status: 'running', turnId: 'turn-2' }
    ];
    render(model({ executions }));
    expect(statusOf(2).props['data-execution-status']).toBe('running');
    expect(statusOf(2).children.join('')).toContain('Running · attempt 2 of 2');
    expect(buttons().find(button => button.label === 'Run again')).toEqual({ label: 'Run again', disabled: true });
    expect(statusOf(1).props['data-execution-status']).toBe('none');
    expect(buttons().find(button => button.label === 'Execute this revision')).toEqual({ label: 'Execute this revision', disabled: false });
  });

  it('keeps each outcome per revision and attempt and offers a deliberate Run again after execution', () => {
    const executions: PlanExecutionRecord[] = [
      { revision: 1, attempt: 1, startedAt: '2026-09-12T10:02:00.000Z', status: 'interrupted', endedAt: '2026-09-12T10:03:00.000Z' },
      { revision: 2, attempt: 1, startedAt: '2026-09-12T10:05:00.000Z', status: 'completed', endedAt: '2026-09-12T10:06:00.000Z' }
    ];
    const value = model({ executions });
    render(value);
    expect(statusOf(2).props['data-execution-status']).toBe('completed');
    expect(statusOf(2).children.join('')).toMatch(/^Completed /);
    expect(statusOf(2).children.join('')).not.toContain('Not executed');
    expect(statusOf(1).props['data-execution-status']).toBe('interrupted');
    expect(statusOf(1).children.join('')).toMatch(/^Stopped /);
    const again = buttons().filter(button => button.label === 'Run again');
    expect(again).toEqual([{ label: 'Run again', disabled: false }, { label: 'Run again', disabled: false }]);
    // Run again on the current revision prepares a request for that same revision; nothing is sent by the panel.
    act(() => { tree!.root.findAllByType('button').find(node => node.children.join('') === 'Run again')!.props.onClick(); });
    expect(value.onExecute).toHaveBeenCalledWith(expect.objectContaining({ revision: 2 }));

    render(model({ executions: [{ revision: 2, attempt: 1, startedAt: '2026-09-12T10:05:00.000Z', status: 'unknown', endedAt: '2026-09-12T10:06:00.000Z' }] }));
    expect(statusOf(2).props['data-execution-status']).toBe('unknown');
    expect(statusOf(2).children.join('')).toMatch(/^Outcome unknown/);
  });
});
