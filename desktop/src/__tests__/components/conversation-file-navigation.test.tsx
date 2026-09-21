import React from 'react';
import { act, create, type ReactTestRenderer } from 'react-test-renderer';
import { afterEach, expect, it, vi } from 'vitest';
import { useConversationFileCatalog } from '../../lib/workspace/use-conversation-file-catalog';
import { ChatMarkdown } from '../../components/shell/chat-markdown';

afterEach(() => vi.unstubAllGlobals());
const reply = (root: string, files = ['README.md']) => ({ ok: true, json: async () => ({ root: {
  path: root, kind: 'directory', children: files.map(name => ({ path: `${root}/${name}`, name, kind: 'file' }))
} }) });
function Conversation({ root, streaming = false, open }: { root: string; streaming?: boolean; open: (path: string) => void }) {
  const catalog = useConversationFileCatalog(root, streaming, 0);
  return <ChatMarkdown source="[Read](README.md)" projectRoot={root} fileCatalog={catalog.paths} onOpenFile={open} />;
}

it('opens a contained file without mounting the Files panel and refreshes after work', async () => {
  const fetch = vi.fn(async () => reply('/trial'));
  vi.stubGlobal('fetch', fetch);
  const open = vi.fn(); let view!: ReactTestRenderer;
  await act(async () => { view = create(<Conversation root="/trial" open={open} />); });
  act(() => view.root.findByType('a').props.onClick({ button: 0, preventDefault: vi.fn() }));
  expect(open).toHaveBeenCalledWith('/trial/README.md');
  await act(async () => view.update(<Conversation root="/trial" streaming open={open} />));
  expect(fetch).toHaveBeenCalledTimes(1);
  await act(async () => view.update(<Conversation root="/trial" open={open} />));
  expect(fetch).toHaveBeenCalledTimes(2);
  act(() => view.unmount());
});

it('cannot use a late old-root catalog or a failed new-root read', async () => {
  let resolveOld!: (value: ReturnType<typeof reply>) => void;
  const pending = new Promise<ReturnType<typeof reply>>(resolve => { resolveOld = resolve; });
  vi.stubGlobal('fetch', vi.fn().mockReturnValueOnce(pending).mockResolvedValueOnce({ ok: false, json: async () => ({}) }));
  const open = vi.fn(); let view!: ReactTestRenderer;
  await act(async () => { view = create(<Conversation root="/old" open={open} />); });
  await act(async () => view.update(<Conversation root="/new" open={open} />));
  await act(async () => resolveOld(reply('/old')));
  expect(view.root.findByType('a').props.onClick).toBeUndefined();
  expect(open).not.toHaveBeenCalled();
  act(() => view.unmount());
});

it('hands out one stable empty catalog while no tree is available, so consumers do not re-derive per render', async () => {
  vi.stubGlobal('fetch', vi.fn(async () => ({ ok: false, json: async () => ({}) })));
  const seen: Array<readonly string[]> = [];
  function Probe({ root, tick }: { root: string; tick: number }) {
    const catalog = useConversationFileCatalog(root, false, 0);
    seen.push(catalog.paths);
    return <span data-tick={tick} />;
  }
  let view!: ReactTestRenderer;
  await act(async () => { view = create(<Probe root="/trial" tick={0} />); });
  await act(async () => view.update(<Probe root="/trial" tick={1} />));
  await act(async () => view.update(<Probe root="/other" tick={2} />));
  expect(seen.length).toBeGreaterThanOrEqual(3);
  expect(seen.every(paths => paths === seen[0] && paths.length === 0)).toBe(true);
  act(() => view.unmount());
});
