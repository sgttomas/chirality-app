import React from 'react';
import { act, create, type ReactTestRenderer } from 'react-test-renderer';
import { renderToStaticMarkup } from 'react-dom/server';
import { afterEach, expect, it, vi } from 'vitest';
import { DocumentView, previewCsv, buildJsonPreview, resolveLocalDocumentLink } from '../../components/shell/document-view';
vi.mock('../../components/workspace/workspace-provider', () => ({ useWorkspace: () => ({ projectRoot: '/root' }) }));
afterEach(() => vi.unstubAllGlobals());
it('parses quoted CSV and caps logical rows', () => {
  expect(previewCsv('a,"b,c"\n"d\ne",f')).toEqual([['a', 'b,c'], ['d\ne', 'f']]);
  expect(previewCsv('a\n'.repeat(600))).toHaveLength(500);
});
it('retains the legacy deliverable viewer when no target is supplied', () => {
  expect(renderToStaticMarkup(<DocumentView />)).toContain('Document');
});
it('escapes HTML text, reports metadata and invokes only the explicit handoff bridge', async () => {
  vi.stubGlobal('fetch', vi.fn(async () => ({ ok: true, json: async () => ({ name: 'a.html', target: 'a.html', kind: 'text', tooLarge: false, size: 8, modifiedAt: '2026-09-05', content: '<script>bad()</script>' }) })));
  const handoff = vi.fn(async () => ({ ok: true })); vi.stubGlobal('window', { chirality: { document: { handoff } } });
  let tree!: ReactTestRenderer; await act(async () => { tree = create(<DocumentView target="a.html" />); });
  expect(tree.root.findAllByType('script')).toHaveLength(0); expect(tree.root.findByType('pre').children).toEqual(['<script>bad()</script>']);
  await act(async () => { await tree.root.findAllByType('button').find(x => x.children.includes('Open in default app'))!.props.onClick(); });
  expect(handoff).toHaveBeenCalledWith({ projectRoot: '/root', target: 'a.html', action: 'open' }); act(() => tree.unmount());
});
it('ignores stale asynchronous results after changing files', async () => {
  let finish!: (value: unknown) => void;
  vi.stubGlobal('fetch', vi.fn((url: string) => url.includes('first') ? new Promise(resolve => { finish = resolve; }) : Promise.resolve({ ok: true, json: async () => ({ name: 'second.txt', kind: 'text', content: 'second', size: 6, modifiedAt: 'today' }) })));
  let tree!: ReactTestRenderer; await act(async () => { tree = create(<DocumentView target="first.txt" />); });
  await act(async () => { tree.update(<DocumentView target="second.txt" />); });
  await act(async () => finish({ ok: true, json: async () => ({ content: 'first' }) }));
  expect(tree.root.findByType('pre').children).toEqual(['second']); act(() => tree.unmount());
});
it.each([
  { kind: 'office', tooLarge: false, name: 'a.docx', text: 'Preview this Office document with Quick Look.' },
  { kind: 'text', tooLarge: true, name: 'a.txt', text: 'This file exceeds the 10 MB text preview limit.' },
  { kind: 'unsupported', tooLarge: false, name: 'a.bin', text: 'This format is available in its default app.' }
])('renders a truthful handoff card for $name', async preview => {
  vi.stubGlobal('fetch', vi.fn(async () => ({ ok: true, json: async () => ({ ...preview, size: 12000000, modifiedAt: 'today' }) })));
  let tree!: ReactTestRenderer; await act(async () => { tree = create(<DocumentView target={preview.name} />); });
  expect(tree.root.findAllByType('p').some(x => x.children.includes(preview.text))).toBe(true);
  expect(tree.root.findAllByType('button').find(x => x.children.includes('Open in default app'))!.props.disabled).toBe(true);
  act(() => tree.unmount());
});
it('uses a same-origin bounded URL for the built-in PDF viewer', async () => {
  vi.stubGlobal('fetch', vi.fn(async () => ({ ok: true, json: async () => ({ name: 'a.pdf', kind: 'pdf', size: 12000000, modifiedAt: 'today' }) })));
  let tree!: ReactTestRenderer; await act(async () => { tree = create(<DocumentView target="a.pdf" />); });
  expect(tree.root.findByType('iframe').props.src).toBe('/api/working-root/file?projectRoot=%2Froot&target=a.pdf&content=pdf');
  act(() => tree.unmount());
});
it('renders markdown without raw HTML or script links becoming executable nodes', async () => {
  vi.stubGlobal('fetch', vi.fn(async () => ({ ok: true, json: async () => ({ name: 'a.md', kind: 'text', content: '# Safe\n<script>evil()</script>\n[bad](javascript:alert(1))', size: 70, modifiedAt: 'today' }) })));
  let tree!: ReactTestRenderer; await act(async () => { tree = create(<DocumentView target="a.md" />); });
  expect(tree.root.findByType('h1').children).toEqual(['Safe']); expect(tree.root.findAllByType('script')).toHaveLength(0);
  expect(tree.root.findAllByType('a').every(x => !x.props.href?.startsWith('javascript:'))).toBe(true);
  act(() => tree.unmount());
});
it('continues loading canonical deliverable documents for legacy consumers', async () => {
  const fetcher = vi.fn(async (url: string) => ({ ok: true, json: async () => url.includes('/deliverables?') ? { deliverables: [{ id: 'DEL-01', path: '/root/DEL-01', name: 'Legacy', pkg: 'PKG', status: 'WORKING' }], deliverableContracts: [{ path: '/root/DEL-01', selectedProductionDocuments: [{ fileName: 'Spec.md' }] }] } : { content: '# Existing document' } }));
  vi.stubGlobal('fetch', fetcher);
  let tree!: ReactTestRenderer; await act(async () => { tree = create(<DocumentView />); });
  expect(tree.root.findByType('h1').children).toEqual(['Existing document']);
  expect(tree.root.findAllByType('option').some(x => x.children.includes('Spec.md'))).toBe(true);
  expect(fetcher.mock.calls.some(([url]) => url.includes('/deliverable/content?'))).toBe(true); act(() => tree.unmount());
});

it('honors Electron inline-PDF capability and sends the actual default-app request', async () => {
  const handoff = vi.fn(async () => ({ ok: true }));
  vi.stubGlobal('window', { chirality: { document: { inlinePdfPreview: false, handoff } } });
  vi.stubGlobal('fetch', vi.fn(async () => ({ ok: true, json: async () => ({ name: 'a.pdf', kind: 'pdf', size: 12000000, modifiedAt: 'today' }) })));
  let tree!: ReactTestRenderer; await act(async () => { tree = create(<DocumentView target="a.pdf" />); });
  expect(tree.root.findAllByType('iframe')).toHaveLength(0);
  expect(tree.root.findAllByType('p').some(x => x.children.includes('PDF preview is unavailable here. Open this file in its default app.'))).toBe(true);
  await act(async () => { await tree.root.findAllByType('button').find(x => x.children.includes('Open in default app'))!.props.onClick(); });
  expect(handoff).toHaveBeenCalledWith({ projectRoot: '/root', target: 'a.pdf', action: 'open' }); act(() => tree.unmount());
});

it('uses the candidate desktop capability but treats iframe failure as unavailable and retryable', async () => {
  const handoff = vi.fn(async () => ({ ok: true }));
  vi.stubGlobal('window', { chirality: { document: { inlinePdfPreview: true, handoff } } });
  vi.stubGlobal('fetch', vi.fn(async () => ({ ok: true, json: async () => ({ name: 'a.pdf', kind: 'pdf', size: 12, modifiedAt: 'today' }) })));
  let tree!: ReactTestRenderer; await act(async () => { tree = create(<DocumentView target="a.pdf" />); });
  expect(tree.root.findByType('iframe').props.src).toBe('/api/working-root/file?projectRoot=%2Froot&target=a.pdf&content=pdf');
  await act(async () => { tree.root.findByType('iframe').props.onError(); });
  expect(tree.root.findAllByType('iframe')).toHaveLength(0);
  expect(tree.root.findAllByType('p').some(x => x.children.includes('PDF preview is unavailable here. Open this file in its default app.'))).toBe(true);
  await act(async () => { tree.root.findAllByType('button').find(x => x.children.includes('Retry PDF preview'))!.props.onClick(); });
  expect(tree.root.findByType('iframe')).toBeTruthy(); act(() => tree.unmount());
});

it('resolves only safe relative Markdown paths', () => {
  expect(resolveLocalDocumentLink('docs/readme.md', './next.md')).toBe('docs/next.md');
  for (const value of ['../secret', '%2e%2e/secret', '/etc/passwd', '//example.com/x', 'javascript:alert(1)', 'x?target=secret', 'a\\b']) expect(resolveLocalDocumentLink('docs/readme.md', value)).toBeNull();
});
it('renders unique actual headings, ignores fences, navigates TOC and uses bounded local links', async () => {
  vi.stubGlobal('fetch', vi.fn(async () => ({ ok: true, json: async () => ({ name: 'readme.md', kind: 'text', size: 100, modifiedAt: 'today', content: '# Same\n## Same\n```md\n# Fenced\n```\n[next](next.md) [outside](https://example.com) [unsafe](../secret)' }) })));
  const onOpenDocument = vi.fn(); let tree!: ReactTestRenderer;
  const nodes = new Map<string, { id: string; textContent: string; tagName: string; scrollIntoView: ReturnType<typeof vi.fn>; focus: ReturnType<typeof vi.fn> }>();
  const actualHeadings = () => tree.root.findByProps({ className: 'chat-markdown' }).findAll(node => typeof node.type === 'string' && /^h[1-6]$/.test(node.type)).map(node => {
    if (!nodes.has(node.props.id)) nodes.set(node.props.id, { id: node.props.id, textContent: node.children.join(''), tagName: String(node.type).toUpperCase(), scrollIntoView: vi.fn(), focus: vi.fn() });
    return nodes.get(node.props.id)!;
  });
  await act(async () => { tree = create(<DocumentView target="docs/readme.md" onOpenDocument={onOpenDocument} expanded />, { createNodeMock: element => element.type === 'div' && ['chat-markdown', 'panel-body document-view-body'].includes(element.props.className) ? { querySelectorAll: actualHeadings } : null }); });
  const headings = actualHeadings(); expect(headings.map(x => x.textContent)).toEqual(['Same', 'Same']); expect(new Set(headings.map(x => x.id)).size).toBe(2);
  const toc = tree.root.findByProps({ 'aria-label': 'Document headings' }); act(() => toc.findAllByType('button')[1].props.onClick()); expect(headings[1].scrollIntoView).toHaveBeenCalled(); expect(headings[1].focus).toHaveBeenCalled();
  expect(tree.root.findAllByType('h2').some(x => x.children.includes('Same'))).toBe(true);
  const local = tree.root.findAllByType('a').find(x => x.children.includes('next'))!;
  act(() => local.props.onClick({ preventDefault: vi.fn() })); expect(onOpenDocument).toHaveBeenCalledWith('docs/next.md');
  expect(tree.root.findAllByType('a').find(x => x.children.includes('outside'))!.props.target).toBe('_blank');
  expect(tree.root.findAllByType('a').some(x => x.children.includes('unsafe'))).toBe(false);
  expect(tree.root.findByProps({ className: 'panel-body document-view-body' }).props.style.maxWidth).toBe(640); act(() => tree.unmount());
});
it('bounds folded JSON depth and width without changing opaque keys', async () => {
  const value = JSON.parse('{"__proto__":{"safe":true},"constructor":"literal"}');
  expect(buildJsonPreview(value).children?.map(x => x.label)).toEqual(['__proto__', 'constructor']);
  const wide = Object.fromEntries(Array.from({ length: 300 }, (_, i) => [String(i), i])); expect(buildJsonPreview(wide).children).toHaveLength(200); expect(buildJsonPreview(wide).disclosure).toBe('Showing 200 of 300 entries.');
  let deep: unknown = 1; for (let i = 0; i < 20; i++) deep = { next: deep }; expect(JSON.stringify(buildJsonPreview(deep))).toContain('Depth limit reached.');
  vi.stubGlobal('fetch', vi.fn(async () => ({ ok: true, json: async () => ({ name: 'a.json', kind: 'text', content: JSON.stringify(value), size: 30, modifiedAt: 'today' }) })));
  let tree!: ReactTestRenderer; await act(async () => { tree = create(<DocumentView target="a.json" />); });
  expect(tree.root.findByProps({ 'aria-label': 'JSON tree' }).findAllByType('details').length).toBeGreaterThan(1); act(() => tree.unmount());
});
it('shows malformed JSON as truthful raw text and associates hover with original source lines', async () => {
  vi.stubGlobal('fetch', vi.fn(async () => ({ ok: true, json: async () => ({ name: 'a.json', kind: 'text', content: '{\nbroken', size: 8, modifiedAt: 'today' }) })));
  const container = {}, setEnd = vi.fn();
  vi.stubGlobal('document', { caretRangeFromPoint: () => ({ startContainer: container, startOffset: 2 }), createRange: () => ({ selectNodeContents: vi.fn(), setEnd, toString: () => '{\nbr' }) });
  let tree!: ReactTestRenderer; await act(async () => { tree = create(<DocumentView target="a.json" />); });
  expect(tree.root.findByProps({ role: 'alert' }).children).toEqual(['Invalid JSON. Showing the original text.']);
  act(() => tree.root.findByType('pre').props.onMouseMove({ clientX: 1, clientY: 2, currentTarget: { contains: () => true } }));
  expect(setEnd).toHaveBeenCalledWith(container, 2); expect(tree.root.findByProps({ 'aria-label': 'Source line' }).children).toEqual(['Line ', '2']); act(() => tree.unmount());
});
it('uses img-only decoding, toggles natural size and reports decoder failures', async () => {
  vi.stubGlobal('fetch', vi.fn(async () => ({ ok: true, json: async () => ({ name: 'hostile.svg', kind: 'image', tooLarge: false, size: 100, modifiedAt: 'today' }) })));
  let tree!: ReactTestRenderer; await act(async () => { tree = create(<DocumentView target="hostile.svg" />); });
  const image = () => tree.root.findByType('img'); expect(image().props.src).toContain('&content=image'); expect(image().props.style.maxWidth).toBe('100%');
  expect(tree.root.findAllByType('svg')).toHaveLength(0); expect(tree.root.findAllByType('script')).toHaveLength(0); expect(tree.root.findAllByType('iframe')).toHaveLength(0);
  act(() => tree.root.findByProps({ 'aria-label': 'Show image at natural size' }).props.onClick()); expect(image().props.style.maxWidth).toBe('none');
  act(() => image().props.onError()); expect(tree.root.findByProps({ role: 'alert' }).children).toEqual(['Unable to decode this image. Open it in its default app.']); act(() => tree.unmount());
});
