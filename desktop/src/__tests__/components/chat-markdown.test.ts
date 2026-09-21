import { createElement } from 'react';
import { renderToStaticMarkup } from 'react-dom/server';
import { act, create } from 'react-test-renderer';
import { describe, expect, it } from 'vitest';
import { vi } from 'vitest';
import { ChatMarkdown, resolveCatalogFileLink } from '../../components/shell/chat-markdown';

describe('chat markdown rendering', () => {
  it('keeps inline code within its sentence and uses one pre only for fenced blocks', () => {
    const html = renderToStaticMarkup(createElement(ChatMarkdown, { source: 'Read `README.md` first.\n\n```txt\nreport\n```' }));
    expect(html).toContain('<p>Read <code>README.md</code> first.</p>');
    expect(html.match(/<pre/g)).toHaveLength(1);
  });
  it('renders core GFM structures for assistant messages', () => {
    const source = [
      '| Col A | Col B |',
      '| --- | --- |',
      '| 1 | 2 |',
      '',
      '- [x] done',
      '- [ ] todo',
      '',
      '~~deprecated~~',
      '',
      'Visit https://example.com',
      '',
      '```ts',
      'const value = 1;',
      '```'
    ].join('\n');

    const html = renderToStaticMarkup(createElement(ChatMarkdown, { source }));

    expect(html).toContain('<table>');
    expect(html).toContain('type="checkbox"');
    expect(html).toContain('<del>deprecated</del>');
    expect(html).toContain('href="https://example.com"');
    expect(html).toContain('language-ts');
    expect(html).toContain('const value = 1;');
  });

  it('uses ansi fallback rendering for terminal code blocks', () => {
    const source = ['```ansi', '\u001b[31mERR\u001b[0m', '```'].join('\n');
    const html = renderToStaticMarkup(createElement(ChatMarkdown, { source }));

    expect(html).toContain('chat-code-block--ansi');
    expect(html).toContain('ansi-red-fg');
    expect(html).toContain('ERR');
  });

  it.each([
    ['docs/SPEC.md', '/root/docs/SPEC.md'],
    ['./docs/SPEC.md', '/root/docs/SPEC.md'],
    ['/root/docs/SPEC.md', '/root/docs/SPEC.md'],
    ['docs/My%20File.md', '/root/docs/My File.md'],
    ['docs/SPEC.md#section', '/root/docs/SPEC.md'],
    ['docs/SPEC.md#section?display-only', '/root/docs/SPEC.md']
  ])('resolves exact current-root catalog links: %s', (href, expected) => {
    expect(resolveCatalogFileLink(href, '/root', ['/root/docs/SPEC.md', '/root/docs/My File.md'])).toBe(expected);
  });

  it.each([
    '', '#fragment', 'docs/SPEC.md?raw=1', 'docs/%ZZ.md', 'docs\\SPEC.md',
    'docs/%00SPEC.md', 'docs//SPEC.md', 'docs/../SPEC.md', 'docs/./SPEC.md',
    'https://example.com', 'mailto:test@example.com', '/root-other/docs/SPEC.md',
    '/root/docs/missing.md'
  ])('rejects unsafe, external, or non-catalog links: %s', (href) => {
    expect(resolveCatalogFileLink(href, '/root', ['/root/docs/SPEC.md'])).toBeNull();
  });

  it('rejects an ambiguous duplicate catalog entry', () => {
    expect(resolveCatalogFileLink('docs/SPEC.md', '/root', ['/root/docs/SPEC.md', '/root/docs/SPEC.md'])).toBeNull();
  });

  it('activates only cataloged local anchors and keeps external links unchanged', () => {
    const open = vi.fn();
    const tree = create(createElement(ChatMarkdown, {
      source: '[spec](docs/SPEC.md) [outside](docs/nope.md) [web](https://example.com) `docs/SPEC.md`',
      projectRoot: '/root', fileCatalog: ['/root/docs/SPEC.md'], onOpenFile: open
    }));
    const anchors = tree.root.findAllByType('a');
    expect(anchors).toHaveLength(3);
    expect(anchors[0].props.target).toBeUndefined();
    expect(anchors[1].props.target).toBe('_blank');
    expect(anchors[2].props).toMatchObject({ href: 'https://example.com', target: '_blank', rel: 'noreferrer noopener' });
    const preventDefault = vi.fn();
    act(() => anchors[0].props.onClick({ button: 0, metaKey: false, ctrlKey: false, shiftKey: false, altKey: false, preventDefault }));
    expect(preventDefault).toHaveBeenCalledOnce();
    expect(open).toHaveBeenCalledExactlyOnceWith('/root/docs/SPEC.md');
    act(() => anchors[0].props.onClick({ button: 0, metaKey: true, ctrlKey: false, shiftKey: false, altKey: false, preventDefault }));
    expect(open).toHaveBeenCalledTimes(1);
    expect(tree.root.findAllByType('code')).toHaveLength(1);
  });

  it('leaves plain paths, images, and rendering without a current catalog non-actionable', () => {
    const open = vi.fn();
    const html = renderToStaticMarkup(createElement(ChatMarkdown, {
      source: 'docs/SPEC.md ![spec](docs/SPEC.md) [spec](docs/SPEC.md)',
      projectRoot: '/other', fileCatalog: ['/root/docs/SPEC.md'], onOpenFile: open
    }));
    expect(html).toContain('docs/SPEC.md');
    expect(html).toContain('<img');
    expect(html).toContain('target="_blank"');
    expect(open).not.toHaveBeenCalled();
  });
});
