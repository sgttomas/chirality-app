import React from 'react';
import { act, create } from 'react-test-renderer';
import { expect, it, vi } from 'vitest';
import type { HarnessEvent } from '@chirality/runtime-contracts/event-schema';
const state = vi.hoisted(() => ({ events: [] as HarnessEvent[] }));
vi.mock('../../components/workspace/harness-events-provider', () => ({ useHarnessEvents: () => ({ events: state.events }) }));
import { ActivityView, ActivityStrip } from '../../components/woven-dialogue/activity-shelf';
function actionRows(tree: ReturnType<typeof create>) {
  const list = tree.root.findAllByProps({ 'aria-label': 'Actions' })[0];
  return list ? list.findAll(node => node.type === 'li' && typeof node.props.className === 'string' && node.props.className.startsWith('harness-stream-item ')) : [];
}
function event(eventId: string, type: HarnessEvent['type'], data: Record<string, unknown>, sessionId = 'one'): HarnessEvent {
  return { schemaVersion: 1, eventId, sessionId, turnId: 'turn', timestamp: '2026-09-06T01:00:00Z', type, data };
}
it('filters completed projections and clears only observed versions without changing the shared event buffer', () => {
  state.events = [event('start', 'tool.started', { toolUseId: 'tool', toolName: 'read_file' }), event('end', 'tool.completed', { toolUseId: 'tool' })];
  const original = JSON.stringify(state.events);
  const tree = create(<ActivityView />);
  act(() => tree.root.findByProps({ 'aria-label': 'Filter activity' }).props.onChange({ target: { value: 'read_file' } }));
  expect(actionRows(tree)).toHaveLength(1);
  expect(actionRows(tree)[0].props.className).toContain('--completed');
  expect(actionRows(tree)[0].findByProps({ title: 'read_file' }).children).toEqual(['Read action finished']);
  act(() => tree.root.findAllByType('button').find(button => button.children.includes('Clear view'))!.props.onClick());
  expect(actionRows(tree)).toHaveLength(0);
  expect(JSON.stringify(state.events)).toBe(original);
  act(() => tree.root.findByProps({ 'aria-label': 'Filter activity' }).props.onChange({ target: { value: '' } }));
  state.events = [...state.events, event('start', 'tool.started', { toolUseId: 'tool', toolName: 'write_file' }, 'two')];
  act(() => tree.update(<ActivityView />));
  expect(actionRows(tree)).toHaveLength(1);
  expect(actionRows(tree)[0].props.className).toContain('--running');
  expect(actionRows(tree)[0].findByProps({ title: 'write_file' }).children).toEqual(['Writing file']);
  state.events = [event('start', 'tool.started', { toolUseId: 'tool', toolName: 'updated_tool' }), ...state.events.slice(1)];
  act(() => tree.update(<ActivityView />));
  expect(actionRows(tree)[0].props.className).toContain('--completed');
  expect(actionRows(tree).map(row => row.findByProps({ className: 'harness-stream-name' }).props.title)).toEqual(['updated_tool', 'write_file']);
  act(() => tree.unmount());
});

it('keeps matching tool IDs in different sessions distinct and reveals a later completion after clear', () => {
  state.events = [event('start', 'tool.started', { toolUseId: 'same', toolName: 'read_file' }, 'one'), event('start', 'tool.started', { toolUseId: 'same', toolName: 'read_file' }, 'two')];
  const tree = create(<ActivityView />);
  expect(actionRows(tree)).toHaveLength(2);
  const strip = create(<ActivityStrip events={state.events} running onOpenDetails={() => {}} />);
  expect(JSON.stringify(strip.toJSON())).not.toContain('Primary turn activity unavailable');
  expect(JSON.stringify(strip.toJSON())).not.toContain('2 actions');
  act(() => tree.root.findAllByType('button').find(button => button.children.includes('Clear view'))!.props.onClick());
  expect(actionRows(tree)).toHaveLength(0);
  const completion = event('end', 'tool.completed', { toolUseId: 'same' }, 'one');
  state.events = [...state.events, completion];
  act(() => tree.update(<ActivityView />));
  expect(actionRows(tree)).toHaveLength(1);
  expect(actionRows(tree)[0].props.className).toContain('--completed');
  expect(state.events).toHaveLength(3); expect(state.events[2]).toBe(completion);
  act(() => { tree.unmount(); strip.unmount(); });
});


it('distinguishes absent recorded actions from filtering and clearing a recorded view', () => {
  state.events = [];
  const tree = create(<ActivityView />);
  expect(JSON.stringify(tree.toJSON())).toContain('No recorded actions.');
  act(() => tree.root.findByProps({ 'aria-label': 'Filter activity' }).props.onChange({ target: { value: 'missing' } }));
  expect(JSON.stringify(tree.toJSON())).toContain('No matching actions.');
  act(() => tree.root.findByProps({ 'aria-label': 'Filter activity' }).props.onChange({ target: { value: '' } }));
  state.events = [event('recorded', 'tool.started', { toolUseId: 'tool', toolName: 'read_file' })];
  act(() => tree.update(<ActivityView />));
  expect(actionRows(tree)).toHaveLength(1);
  act(() => tree.root.findAllByType('button').find(button => button.children.includes('Clear view'))!.props.onClick());
  expect(JSON.stringify(tree.toJSON())).toContain('No actions in this view.');
  expect(JSON.stringify(tree.toJSON())).not.toContain('No recorded actions.');
  expect(state.events).toHaveLength(1);
  act(() => tree.unmount());
});
