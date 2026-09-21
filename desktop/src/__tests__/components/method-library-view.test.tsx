import React from 'react';
import { act, create, type ReactTestRenderer } from 'react-test-renderer';
import { beforeEach, expect, it, vi } from 'vitest';
import type { MethodNavigation } from '@chirality/runtime-contracts/v3';

vi.mock('../../components/woven-dialogue/workflow-draft-review', () => ({ WorkflowDraftReview: () => null }));

const mocks = vi.hoisted(() => ({ list: vi.fn(), inspect: vi.fn() }));
vi.mock('../../lib/harness/method-selection-client', async importOriginal => ({
  ...await importOriginal<typeof import('../../lib/harness/method-selection-client')>(),
  listMethods: mocks.list,
  inspectMethod: mocks.inspect
}));
vi.mock('../../components/shell/runtime-connectivity-provider', () => ({ useRuntimeEpoch: () => 0 }));
import { MethodLibraryView } from '../../components/woven-dialogue/method-library-view';

const descriptor = (name: string, sourceRootId: string, input: Partial<{ source: 'project' | 'user' | 'bundled'; kind: 'skill' | 'workflow'; central: boolean; compatibility: 'canonical' | 'legacy'; metadata: Readonly<Record<string, unknown>>; navigation: MethodNavigation }> = {}) => ({
  qualifiedId: `${sourceRootId}/${input.kind ?? 'workflow'}/${name}`,
  sourceRootId,
  source: input.source ?? 'project' as const,
  kind: input.kind ?? 'workflow' as const,
  name,
  description: `${name} description`,
  central: input.central ?? false,
  compatibility: input.compatibility ?? 'canonical' as const,
  executionRoleIds: ['TASK'] as const,
  resources: [],
  ...(input.metadata ? { metadata: input.metadata } : {}),
  ...(input.navigation ? { navigation: input.navigation } : {})
});
const response = (methods: ReturnType<typeof descriptor>[]) => ({ schemaVersion: 'chirality.methods/v3' as const, methods, malformedPackages: [] });
const textOf = (node: { children: unknown[] }): string => node.children.map(child => typeof child === 'string' ? child : child && typeof child === 'object' && 'children' in child ? textOf(child as { children: unknown[] }) : '').join('');
function deferred<T>() { let resolve!: (value: T) => void; const promise = new Promise<T>(done => { resolve = done; }); return { promise, resolve }; }
const core = (name: string, order: number, displayName?: string) => descriptor(name, 'bundled', { source: 'bundled', central: order < 6, navigation: { category: 'core', tier: 'primary', order, ...(displayName ? { displayName } : {}) } });
const specialist = (name: string, group: { key: string; label: string; order: number }, order: number, tier: 'primary' | 'supporting' = 'primary') => descriptor(name, 'bundled', { source: 'bundled', navigation: { category: 'specialist', tier, order, group } });

beforeEach(() => vi.clearAllMocks());

async function render(view: 'workflows' | 'skills' = 'workflows', onSelectedChange = vi.fn()): Promise<ReactTestRenderer> {
  let tree!: ReactTestRenderer;
  await act(async () => { tree = create(<MethodLibraryView projectRoot="/project" selected={[]} onSelectedChange={onSelectedChange} view={view} />); });
  await act(async () => { await new Promise(resolve => setTimeout(resolve, 0)); });
  return tree;
}

it('does not let an aborted project catalog overwrite the current project', async () => {
  const oldResult = deferred<ReturnType<typeof response>>();
  const nextResult = deferred<ReturnType<typeof response>>();
  mocks.list.mockImplementation((root: string) => root === '/old' ? oldResult.promise : nextResult.promise);
  let tree!: ReactTestRenderer;
  await act(async () => { tree = create(<MethodLibraryView projectRoot="/old" selected={[]} onSelectedChange={() => {}} />); });
  await act(async () => { await new Promise(resolve => setTimeout(resolve, 0)); });
  await act(async () => { tree.update(<MethodLibraryView projectRoot="/next" selected={[]} onSelectedChange={() => {}} />); });
  await act(async () => { await new Promise(resolve => setTimeout(resolve, 0)); });
  await act(async () => nextResult.resolve(response([descriptor('current-method', 'next-root')])));
  await act(async () => oldResult.resolve(response([descriptor('stale-method', 'old-root')])));
  const text = JSON.stringify(tree.toJSON());
  expect(text).toContain('current-method');
  expect(text).not.toContain('stale-method');
  expect(tree.root.findAllByProps({ role: 'alert' })).toHaveLength(0);
});

it('presents Core in catalog order with display names, Specialist by intent group with supporting steps disclosed, Project Specific and personal workflows by source, and superseded workflows with their replacement', async () => {
  const plan = { key: 'plan-organize', label: 'Plan & organize', order: 0 };
  const extract = { key: 'extract-documents', label: 'Extract from documents', order: 2 };
  mocks.list.mockResolvedValue(response([
    specialist('pdf2md-page-full', extract, 2, 'supporting'),
    specialist('pdf2md', extract, 0),
    descriptor('pdf2md-page', 'bundled', { source: 'bundled', compatibility: 'legacy', navigation: { category: 'superseded', tier: 'primary', order: 0, supersededBy: 'pdf2md-page-full' } }),
    descriptor('my-saved-plan', 'project', { metadata: { purpose: 'Prepare a release', applicability: ['App work', 'Runtime work'] } }),
    descriptor('personal-flow', 'user', { source: 'user' }),
    specialist('preparation', plan, 0),
    core('reconciliation', 8, 'Check project status'),
    core('project-setup', 0),
    core('task-management', 6, 'Manage tasks')
  ]));
  const tree = await render();
  const text = JSON.stringify(tree.toJSON());
  const headings = tree.root.findAllByType('h3').map(node => node.children.join(''));
  expect(headings).toEqual(['Core', 'Specialist', 'Project Specific', 'Your workflows']);
  const coreNames = tree.root.findAll(node => node.props.className === 'method-card' || node.props.className === 'method-card method-card--central').slice(0, 3).map(node => node.findByType('strong').children.join(''));
  expect(coreNames).toEqual(['project-setup', 'Manage tasks', 'Check project status']);
  expect(text).toContain('task-management');
  expect(tree.root.findAllByType('h4').map(node => node.children.join(''))).toEqual(['Plan & organize', 'Extract from documents']);
  // Specialist categories list their name and count only until expanded; a search opens them so matches are visible.
  const categories = tree.root.findAll(node => node.type === 'details' && node.props.className === 'method-library-subgroup');
  expect(categories.map(node => [node.props['data-method-category'], node.props.open, node.findByProps({ className: 'method-library-count' }).children.join('')])).toEqual([['plan-organize', undefined, '1'], ['extract-documents', undefined, '2']]);
  act(() => { tree.root.findByProps({ className: 'method-library-search' }).props.onChange({ target: { value: 'pdf' } }); });
  await act(async () => { await new Promise(resolve => setTimeout(resolve, 200)); });
  expect(tree.root.findAll(node => node.type === 'details' && node.props.className === 'method-library-subgroup').map(node => node.props.open)).toEqual([true]);
  const supporting = tree.root.findByProps({ className: 'method-library-supporting' });
  expect(supporting.type).toBe('details');
  expect(supporting.props.open).toBeUndefined();
  expect(supporting.findByType('summary').children.join('')).toBe('Supporting steps (1)');
  expect(text).toContain('Prepare a release');
  expect(text).toContain('App work, Runtime work');
  expect(text.indexOf('Project Specific')).toBeLessThan(text.indexOf('Your workflows'));
  const superseded = tree.root.findByProps({ className: 'method-library-superseded' });
  expect(superseded.props.open).toBeUndefined();
  const supersededNote = superseded.findByProps({ className: 'method-card-meta method-card-superseded' });
  expect(textOf(supersededNote)).toBe('Superseded · replaced by pdf2md-page-full');
  expect(text).not.toContain('Legacy methods');
  expect(text).not.toContain('Start here');
  expect(tree.root.findAllByType('input').map(node => node.props['aria-label'])).toEqual(['Search workflows']);
  expect(tree.root.findAllByType('label')).toHaveLength(0);
});

it('lets a superseded workflow still be selected deliberately and searched for', async () => {
  const retired = descriptor('retired-flow', 'bundled', { source: 'bundled', compatibility: 'legacy', navigation: { category: 'superseded', tier: 'primary', order: 0, supersededBy: 'current-flow' } });
  mocks.list.mockResolvedValue(response([core('current-flow', 0), retired]));
  const change = vi.fn();
  const tree = await render('workflows', change);
  await act(async () => tree.root.findByProps({ className: 'method-library-superseded' }).findAllByType('button').find(button => button.children.includes('Use in message'))!.props.onClick());
  expect(change).toHaveBeenCalledWith([{ kind: 'workflow', name: retired.name, source: retired.source, sourceRootId: retired.sourceRootId }]);
  await act(async () => tree.root.findByProps({ 'aria-label': 'Search workflows' }).props.onChange({ target: { value: 'retired' } }));
  await act(async () => { await new Promise(resolve => setTimeout(resolve, 200)); });
  const text = JSON.stringify(tree.toJSON());
  expect(text).toContain('retired-flow');
  // The Core card is filtered out; only the superseded card (which names its replacement) remains.
  expect(tree.root.findAllByType('h3').map(node => node.children.join(''))).not.toContain('Core');
  expect(tree.root.findAll(node => node.props['data-method-kind'] === 'workflow')).toHaveLength(1);
  act(() => tree.unmount());
});

it('redirects the legacy Skills view to workflows without exposing skill cards', async () => {
  mocks.list.mockResolvedValue(response([
    descriptor('trusted-check', 'bundled', { source: 'bundled', kind: 'skill' }),
    descriptor('project-skill', 'project', { kind: 'skill' }), core('project-setup', 0)
  ]));
  const tree = await render('skills');
  const text = JSON.stringify(tree.toJSON());
  expect(text).not.toContain('trusted-check');
  expect(text).not.toContain('project-skill');
  expect(text).toContain('project-setup');
  expect(tree.root.findByProps({ 'aria-label': 'Search workflows' })).toBeDefined();
  act(() => tree.unmount());
});

it('keeps only the newest inspection result', async () => {
  const a = descriptor('method-a', 'root-a');
  const b = descriptor('method-b', 'root-b');
  mocks.list.mockResolvedValue(response([a, b]));
  const inspectA = deferred<any>(); const inspectB = deferred<any>();
  mocks.inspect.mockImplementation((_root: string, method: { name: string }) => method.name === 'method-a' ? inspectA.promise : inspectB.promise);
  let tree!: ReactTestRenderer;
  await act(async () => { tree = create(<MethodLibraryView projectRoot="/project" selected={[]} onSelectedChange={() => {}} />); });
  await act(async () => { await new Promise(resolve => setTimeout(resolve, 0)); });
  const inspectButtons = tree.root.findAllByType('button').filter(button => button.children.includes('Inspect'));
  await act(async () => inspectButtons[0].props.onClick());
  await act(async () => inspectButtons[1].props.onClick());
  await act(async () => inspectB.resolve({ schemaVersion: 'chirality.method-inspection/v3', method: b, entrypoint: { content: 'B instructions', sha256: 'b'.repeat(64) }, resources: [] }));
  await act(async () => inspectA.resolve({ schemaVersion: 'chirality.method-inspection/v3', method: a, entrypoint: { content: 'A instructions', sha256: 'a'.repeat(64) }, resources: [] }));
  const text = JSON.stringify(tree.toJSON());
  expect(text).toContain('B instructions');
  expect(text).not.toContain('A instructions');
  expect(text).toContain('Identifier');
});

it('reloads the catalog when the panel requests a refresh', async () => {
  mocks.list.mockRejectedValueOnce(new Error('Daemon was unavailable'))
    .mockResolvedValue(response([descriptor('available-again', 'project-root')]));
  let tree!: ReactTestRenderer;
  await act(async () => { tree = create(<MethodLibraryView projectRoot="/project" selected={[]} onSelectedChange={() => {}} refresh={0} />); });
  await act(async () => { await new Promise(resolve => setTimeout(resolve, 0)); });
  expect(JSON.stringify(tree.toJSON())).toContain('Daemon was unavailable');
  await act(async () => { tree.update(<MethodLibraryView projectRoot="/project" selected={[]} onSelectedChange={() => {}} refresh={1} />); });
  await act(async () => { await new Promise(resolve => setTimeout(resolve, 0)); });
  expect(mocks.list).toHaveBeenCalledTimes(2);
  expect(JSON.stringify(tree.toJSON())).toContain('available-again');
});

it('keeps inspection and selected methods during same-scope refresh, including catalog failure', async () => {
  const item = descriptor('saved-flow', 'project');
  const pending = deferred<ReturnType<typeof response>>();
  mocks.list.mockResolvedValueOnce(response([item])).mockImplementationOnce(() => pending.promise)
    .mockRejectedValueOnce(new Error('Refresh unavailable'));
  mocks.inspect.mockResolvedValue({ method: item, entrypoint: { content: 'Saved workflow instructions', sha256: 'a'.repeat(64) }, resources: [] });
  const selected = [{ kind: item.kind, source: item.source, name: item.name, sourceRootId: item.sourceRootId }];
  const change = vi.fn();
  const props = { projectRoot: '/project', selected, onSelectedChange: change };
  let tree!: ReactTestRenderer;
  await act(async () => { tree = create(<MethodLibraryView {...props} />); });
  await act(async () => { await new Promise(resolve => setTimeout(resolve, 0)); });
  await act(async () => tree.root.findAllByType('button').find(node => node.children.includes('Inspect'))!.props.onClick());
  await act(async () => tree.update(<MethodLibraryView {...props} refresh={1} />));
  await act(async () => { await new Promise(resolve => setTimeout(resolve, 0)); });
  expect(JSON.stringify(tree.toJSON())).toContain('Saved workflow instructions');
  expect(JSON.stringify(tree.toJSON())).not.toContain('Loading…');
  expect(tree.root.findByProps({ 'aria-label': 'Search workflows' }).props.value).toBe('');
  await act(async () => pending.resolve(response([item, descriptor('new-flow', 'project')])));
  expect(JSON.stringify(tree.toJSON())).toContain('Saved workflow instructions');
  await act(async () => tree.update(<MethodLibraryView {...props} refresh={2} />));
  await act(async () => { await new Promise(resolve => setTimeout(resolve, 0)); });
  expect(JSON.stringify(tree.toJSON())).toContain('Refresh unavailable');
  expect(JSON.stringify(tree.toJSON())).toContain('Saved workflow instructions');
  await act(async () => tree.root.findAllByType('button').find(button => button.children.includes('‹ Workflows'))!.props.onClick());
  expect(JSON.stringify(tree.toJSON())).toContain('new-flow');
  expect(change).not.toHaveBeenCalled();
  act(() => tree.unmount());
});


it('opens inspection as the visible focused detail view with a route back to the full library', async () => {
  const method = descriptor('inspect-me', 'project');
  mocks.list.mockResolvedValue(response([method, ...Array.from({length: 20}, (_, index) => descriptor(`other-${index}`, 'project'))]));
  mocks.inspect.mockResolvedValue({ method, entrypoint: { content: '# Read this method', sha256: 'a'.repeat(64) }, resources: [] });
  const tree = await render();
  await act(async () => tree.root.findAllByType('button').find(button => button.children.includes('Inspect'))!.props.onClick());
  const details = tree.root.findByProps({ 'aria-label': 'inspect-me method details' });
  expect(details.props.tabIndex).toBe(-1);
  expect(details.findAllByType('details').find(node => node.findByType('summary').children.includes('Read instructions'))!.props.open).toBe(true);
  expect(tree.root.findAllByProps({ 'data-method-kind': 'workflow' })).toHaveLength(0);
  await act(async () => details.findByType('button').props.onClick());
  expect(tree.root.findAllByProps({ 'data-method-kind': 'workflow' })).toHaveLength(21);
  act(() => tree.unmount());
});
