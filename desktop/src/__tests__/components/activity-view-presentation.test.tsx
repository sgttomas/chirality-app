import React from 'react';
import { act, create, type ReactTestRenderer } from 'react-test-renderer';
import { afterEach, expect, it, vi } from 'vitest';
import type { HarnessEvent } from '@chirality/runtime-contracts/event-schema';

const state = vi.hoisted(() => ({ events: [] as HarnessEvent[] }));
vi.mock('../../components/workspace/harness-events-provider', () => ({ useHarnessEvents: () => ({ events: state.events }) }));
import { ActivityView } from '../../components/woven-dialogue/activity-shelf';
import { TranscriptStreamList } from '../../components/shell/transcript-stream-view';

const trees: ReactTestRenderer[] = [];
afterEach(() => { act(() => trees.splice(0).forEach(tree => tree.unmount())); });
function mount(events: HarnessEvent[]) {
  state.events = events;
  const tree = create(<ActivityView />);
  trees.push(tree);
  return tree;
}
function event(id: string, type: HarnessEvent['type'], data: Record<string, unknown> = {}, timestamp = '2026-09-06T01:02:03Z', sessionId = 'one'): HarnessEvent {
  return { schemaVersion: 1, eventId: id, sessionId, turnId: 'turn', timestamp, type, data };
}
function click(tree: ReactTestRenderer, label: string) {
  act(() => tree.root.findAllByType('button').find(button => button.children.includes(label))!.props.onClick());
}
function filter(tree: ReactTestRenderer, value: string) {
  act(() => tree.root.findByProps({ 'aria-label': 'Filter activity' }).props.onChange({ target: { value } }));
}
function rows(tree: ReactTestRenderer) {
  return tree.root.findAll(node => node.type === 'li' && typeof node.props.className === 'string' && node.props.className.startsWith('harness-stream-item '));
}
function names(tree: ReactTestRenderer) {
  return tree.root.findAllByProps({ className: 'harness-stream-name' }).map(node => node.children.join(''));
}

it('uses Actions, Events, and Tasks while preserving the existing Events renderer', () => {
  const tree = mount([event('action', 'tool.started', { toolName: 'read_file' }), event('task', 'subagent.started', { agentName: 'RESEARCHER' })]);
  expect(tree.root.findAllByType('button').map(button => button.children.join(''))).toEqual(['Actions', 'Events', 'Tasks', 'Codex', 'Clear view']);
  expect(names(tree)).toEqual(['Reading file']);
  expect(tree.root.findAllByType('h2')).toHaveLength(0);
  click(tree, 'Events');
  expect(tree.root.findAllByType(TranscriptStreamList)).toHaveLength(1);
  click(tree, 'Tasks');
  expect(names(tree)).toEqual(['Task running: Researcher']);
  expect(tree.root.findAllByType('h2')).toHaveLength(0);
  click(tree, 'Actions');
  expect(names(tree)).toEqual(['Reading file']);
});

it.each([
  ['tool.queued', 'Queued to read file', 'queued'],
  ['tool.permission', 'Permission check to read file', 'Permission check'],
  ['tool.started', 'Reading file', 'running'],
  ['tool.completed', 'Read action finished', 'completed'],
  ['tool.failed', 'Failed to read file', 'failed']
] as const)('presents truthful %s status for a known operation', (type, sentence, status) => {
  const tree = mount([event('action', type, { toolName: 'read_file' })]);
  expect(names(tree)).toEqual([sentence]);
  expect(tree.root.findAll(node => node.type === 'span' && node.props.className?.startsWith('harness-status-badge '))[0].children).toEqual([status]);
  expect(tree.root.findByProps({ title: 'read_file' }).children).toEqual([sentence]);
});

it.each([
  ['tool.queued', 'Action queued'], ['tool.permission', 'Action permission check'],
  ['tool.started', 'Action running'], ['tool.completed', 'Action completed'], ['tool.failed', 'Action failed']
] as const)('does not invent operation meaning for an unfamiliar %s row', (type, sentence) => {
  const tree = mount([event('unknown', type, { toolName: 'vendor_magic_42', input: { path: '/not-safe-to-surface', purpose: 'Publish everything' } })]);
  expect(names(tree)).toEqual([sentence]);
  expect(tree.root.findByProps({ title: 'vendor_magic_42' }).children).toEqual([sentence]);
  const rendered = JSON.stringify(tree.toJSON());
  expect(rendered).toContain('vendor_magic_42');
  expect(rendered).not.toContain('/not-safe-to-surface');
  expect(rendered).not.toContain('Publish everything');
});

it('keeps safe paths, event details and raw identifiers, with the recorded timestamp', () => {
  const timestamp = '2026-09-06T01:02:03Z';
  const tree = mount([event('write', 'tool.completed', {
    toolName: 'write_file', source: 'adapter', surface: 'safe-surface',
    inputMetadata: { pathFields: { file_path: 'Reports/Design basis.md', output: '[redacted]' } }
  }, timestamp)]);
  expect(names(tree)).toEqual(['Write action finished']);
  expect(tree.root.findByProps({ title: 'file_path: Reports/Design basis.md' }).findByProps({ className: 'harness-stream-path-value' }).children).toEqual(['Reports/Design basis.md']);
  const rendered = JSON.stringify(tree.toJSON());
  for (const value of ['[redacted]', 'adapter', 'safe-surface', 'tool.completed', '1 event', 'write_file']) expect(rendered).toContain(value);
  const time = tree.root.findByType('time');
  expect(time.props).toMatchObject({ dateTime: timestamp, title: timestamp });
  expect(time.children.join('')).toBe(new Date(timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' }));
  expect(rows(tree)[0].findAllByType('a')).toHaveLength(0);
  expect(rows(tree)[0].findAllByType('button')).toHaveLength(0);
});

it('honestly handles missing operation names and invalid or absent timestamps', () => {
  const tree = mount([event('missing', 'tool.failed', {}, 'not-a-time'), event('empty', 'tool.started', {}, '')]);
  expect(names(tree)).toEqual(['Action failed', 'Action running']);
  expect(tree.root.findAllByType('time')).toHaveLength(0);
  expect(JSON.stringify(tree.toJSON())).toContain('Tool name unavailable');
  expect(tree.root.findByProps({ title: 'not-a-time' }).children).toEqual(['Time unavailable']);
  expect(tree.root.findByProps({ title: 'No recorded timestamp' }).children).toEqual(['Time unavailable']);
  filter(tree, 'time unavailable'); expect(rows(tree)).toHaveLength(2);
  filter(tree, 'tool name unavailable'); expect(rows(tree)).toHaveLength(2);
});

it('searches friendly sentences and preserved raw row data without changing the buffer', () => {
  const events = [event('read', 'tool.started', { toolUseId: 'read', toolName: 'read_file', inputMetadata: { pathFields: { path: 'Reports/Basis.md' } } }), event('other', 'tool.failed', { toolName: 'vendor_magic' })];
  const original = JSON.stringify(events);
  const tree = mount(events);
  for (const query of ['Reading file', 'READ_FILE', 'Reports/Basis.md']) { filter(tree, query); expect(names(tree)).toEqual(['Reading file']); }
  filter(tree, 'vendor_magic'); expect(names(tree)).toEqual(['Action failed']);
  filter(tree, 'does not exist'); expect(rows(tree)).toHaveLength(0);
  expect(state.events).toBe(events); expect(JSON.stringify(events)).toBe(original);
});

it.each(['running', 'completed', 'failed'] as const)('presents %s tasks with recorded optional fields and searchable names', status => {
  const tree = mount([event('task', status === 'running' ? 'subagent.started' : `subagent.${status}`, {
    taskId: 'task', agentName: 'RESEARCHER', description: 'Check the bid curves', summary: 'Recorded result',
    lastToolName: 'read_file', outputArtifactPath: 'safe-marker'
  })]);
  click(tree, 'Tasks');
  expect(names(tree)).toEqual([`Task ${status}: Researcher`]);
  expect(tree.root.findByProps({ title: 'RESEARCHER' }).children).toEqual([`Task ${status}: Researcher`]);
  const rendered = JSON.stringify(tree.toJSON());
  for (const text of ['Check the bid curves', 'Recorded result', 'Last action: read_file', 'Recorded output path', `subagent.${status === 'running' ? 'started' : status}`]) expect(rendered).toContain(text);
  for (const query of [`Task ${status}: Researcher`, 'RESEARCHER', 'Recorded result', 'Recorded output path', 'safe-marker']) { filter(tree, query); expect(rows(tree)).toHaveLength(1); }
  expect(rows(tree)[0].findAllByType('a')).toHaveLength(0);
  expect(rows(tree)[0].findAllByType('button')).toHaveLength(0);
});

it('handles missing task metadata and displays the accepted Assistant label', () => {
  const tree = mount([event('missing', 'subagent.started', {}, 'bad-time'), event('assistant', 'subagent.failed', { agentName: 'HELP_HUMAN' })]);
  click(tree, 'Tasks');
  expect(names(tree)).toEqual(['Task running', 'Task failed: Assistant']);
  expect(JSON.stringify(tree.toJSON())).toContain('Agent name unavailable');
  expect(tree.root.findByProps({ title: 'bad-time' }).children).toEqual(['Time unavailable']);
  filter(tree, 'Assistant'); expect(names(tree)).toEqual(['Task failed: Assistant']);
  filter(tree, 'HELP_HUMAN'); expect(names(tree)).toEqual(['Task failed: Assistant']);
  filter(tree, 'Agent name unavailable'); expect(names(tree)).toEqual(['Task running']);
});

it('keeps same task IDs in separate sessions and resurfaces a later completion after Clear view', () => {
  const start = event('start', 'subagent.started', { taskId: 'same', agentName: 'RESEARCHER', description: 'Preserved purpose' });
  const second = event('start', 'subagent.started', { taskId: 'same', agentName: 'TASK' }, undefined, 'two');
  const tree = mount([start, second]);
  click(tree, 'Tasks'); expect(rows(tree)).toHaveLength(2);
  click(tree, 'Clear view'); expect(rows(tree)).toHaveLength(0);
  const end = event('end', 'subagent.completed', { taskId: 'same', summary: 'Finished review' });
  state.events = [start, second, end];
  act(() => tree.update(<ActivityView />));
  expect(names(tree)).toEqual(['Task completed: Researcher']);
  expect(JSON.stringify(tree.toJSON())).toContain('Preserved purpose');
  expect(JSON.stringify(tree.toJSON())).toContain('Finished review');
  expect(state.events).toEqual([start, second, end]);
});


it.each([
  ['read_file', 'Read action finished', 'Read file'],
  ['write_file', 'Write action finished', 'Wrote file']
] as const)('does not claim a file effect when a failed %s action is followed by summary completion', (toolName, sentence, effectClaim) => {
  const start = event('start', 'tool.started', { toolUseId: 'known-action', toolName });
  const failure = event('failure', 'tool.failed', { toolUseId: 'known-action' });
  const tree = mount([start, failure]);
  expect(rows(tree)[0].props.className).toContain('--failed');
  expect(names(tree)[0]).toMatch(/^Failed to /);
  const summary = event('summary', 'tool.completed', { precedingToolUseIds: ['known-action'] });
  state.events = [start, failure, summary];
  act(() => tree.update(<ActivityView />));
  // The unchanged projection overwrites the failure with completed. Presentation
  // reports that lifecycle status without upgrading it into a file-effect claim.
  expect(rows(tree)).toHaveLength(1);
  expect(rows(tree)[0].props.className).toContain('--completed');
  expect(names(tree)).toEqual([sentence]);
  expect(JSON.stringify(tree.toJSON())).not.toContain(effectClaim);
  for (const query of [sentence, toolName]) {
    filter(tree, query);
    expect(names(tree)).toEqual([sentence]);
  }
  expect(state.events).toEqual([start, failure, summary]);
});
