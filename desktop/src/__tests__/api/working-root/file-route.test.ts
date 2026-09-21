import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';
import { mkdir, mkdtemp, writeFile, symlink, rm, open, utimes } from 'node:fs/promises';
import path from 'node:path';
import { tmpdir } from 'node:os';
import { PDF_CONTENT_SECURITY_POLICY, RESPONSE_CLASS_HEADER } from '../../../../electron/renderer-window-policy';
const policy = vi.hoisted(() => ({ instruction: '' }));
const routeHandle = vi.hoisted(() => ({
  target: '', closeCalls: 0,
  read: undefined as undefined | ((handle: any, args: any[]) => Promise<any>),
  stat: undefined as undefined | ((handle: any, args: any[]) => Promise<any>)
}));
vi.mock('node:fs/promises', async importOriginal => {
  const actual = await importOriginal<any>();
  return {
    ...actual,
    open: async (...args: any[]) => {
      const handle = await actual.open(...args);
      if (!routeHandle.target || !String(args[0]).endsWith(routeHandle.target)) return handle;
      return new Proxy(handle, {
        get(target, property) {
          if (property === 'close') return async () => { routeHandle.closeCalls += 1; return target.close(); };
          if (property === 'read' && routeHandle.read) return (...readArgs: any[]) => routeHandle.read!(target, readArgs);
          if (property === 'stat' && routeHandle.stat) return (...statArgs: any[]) => routeHandle.stat!(target, statArgs);
          const value = Reflect.get(target, property, target);
          return typeof value === 'function' ? value.bind(target) : value;
        }
      });
    }
  };
});
vi.mock('../../../lib/harness/session-manager', () => ({ assertProjectRootAccessible: async (root: string) => { if (!path.isAbsolute(root)) throw { type: 'INVALID_REQUEST', status: 400, message: 'Root must be absolute.' }; return root; } }));
vi.mock('../../../lib/harness/instruction-root', () => ({ resolveInstructionRootPath: () => policy.instruction }));
import { GET } from '../../../app/api/working-root/file/route';
import { TEXT_LIMIT, openDocument } from '../../../app/api/working-root/file/file-policy';
let base: string, root: string;
const fixtureBase = path.join(tmpdir(), 'chirality-d121-file-route-tests');
beforeEach(async () => {
  routeHandle.target = ''; routeHandle.closeCalls = 0; routeHandle.read = undefined; routeHandle.stat = undefined;
  await mkdir(fixtureBase, { recursive: true }); base = await mkdtemp(path.join(fixtureBase, 'route-')); root = path.join(base, 'root'); policy.instruction = path.join(base, 'instruction');
  await Promise.all([mkdir(root), mkdir(policy.instruction)]);
});
afterEach(async () => { vi.restoreAllMocks(); await rm(base, { recursive: true, force: true }); });
const get = (target: string, extra = '', projectRoot = root) => GET(new Request(`http://localhost/api/working-root/file?projectRoot=${encodeURIComponent(projectRoot)}&target=${encodeURIComponent(target)}${extra}`));
describe('bounded document endpoint', () => {
  it('returns safe text metadata, including literal HTML, without executing it', async () => {
    await writeFile(path.join(root, 'view.html'), '<script>alert(1)</script>');
    const response = await get('view.html'); expect(response.status).toBe(200);
    expect(response.headers.get('x-content-type-options')).toBe('nosniff');
    expect(await response.json()).toMatchObject({ kind: 'text', content: '<script>alert(1)</script>', size: 25 });
  });
  it('reads text through exactly 10MiB and hands larger text off with its actual size', async () => {
    await writeFile(path.join(root, 'cap.txt'), 'x'.repeat(TEXT_LIMIT));
    expect((await (await get('cap.txt')).json()).content.length).toBe(TEXT_LIMIT);
    const handle = await open(path.join(root, 'cap.txt'), 'r+'); await handle.truncate(TEXT_LIMIT + 1); await handle.close();
    expect(await (await get('cap.txt')).json()).toMatchObject({ size: TEXT_LIMIT + 1, tooLarge: true });
    expect((await (await get('cap.txt')).json()).content).toBeNull();
  });
  it('streams PDFs above the text cap and keeps Office previews uncapped', async () => {
    const content = Buffer.alloc(TEXT_LIMIT + 2, 32); content.write('%PDF-1.7');
    await writeFile(path.join(root, 'large.pdf'), content);
    const response = await get('large.pdf', '&content=pdf');
    expect(response.status).toBe(200); expect(response.headers.get('content-type')).toBe('application/pdf');
    expect(response.headers.get('content-security-policy')).toBe(PDF_CONTENT_SECURITY_POLICY);
    expect(response.headers.get(RESPONSE_CLASS_HEADER)).toBe('eligible-pdf-v1');
    expect(response.headers.get('accept-ranges')).toBeNull(); expect(response.headers.get('content-range')).toBeNull();
    expect((await response.arrayBuffer()).byteLength).toBe(content.length);
    await writeFile(path.join(root, 'large.docx'), content);
    expect(await (await get('large.docx')).json()).toMatchObject({ kind: 'office', tooLarge: false, size: content.length });
  });
  it('ignores Range and If-Range and returns the complete eligible PDF', async () => {
    const bytes = Buffer.from('%PDF-1.7\ncomplete'); await writeFile(path.join(root, 'range.pdf'), bytes);
    const response = await GET(new Request(`http://localhost/api/working-root/file?projectRoot=${encodeURIComponent(root)}&target=range.pdf&content=pdf`, { headers: { Range: 'bytes=2-5', 'If-Range': 'stale' } }));
    expect(response.status).toBe(200); expect(response.headers.get('content-length')).toBe(String(bytes.length));
    expect(response.headers.get('accept-ranges')).toBeNull(); expect(response.headers.get('content-range')).toBeNull();
    expect(Buffer.from(await response.arrayBuffer())).toEqual(bytes);
  });
  it('rejects empty, wrong-signature, mismatched and duplicate PDF selectors before emitting trust', async () => {
    await writeFile(path.join(root, 'empty.pdf'), ''); await writeFile(path.join(root, 'fake.pdf'), 'plain text');
    for (const response of [
      await get('empty.pdf', '&content=pdf'), await get('fake.pdf', '&content=pdf'),
      await GET(new Request(`http://localhost/api/working-root/file?projectRoot=${encodeURIComponent(root)}&projectRoot=${encodeURIComponent(root)}&target=fake.pdf&content=pdf`)),
      await GET(new Request(`http://localhost/api/working-root/file?projectRoot=${encodeURIComponent(root)}&target=fake.pdf&target=fake.pdf&content=pdf`)),
      await GET(new Request(`http://localhost/api/working-root/file?projectRoot=${encodeURIComponent(root)}&path=fake.pdf&target=fake.pdf&content=pdf`)),
      await GET(new Request(`http://localhost/api/working-root/file?projectRoot=${encodeURIComponent(root)}&target=fake.pdf&content=pdf&unknown=1`))
    ]) {
      expect(response.status).not.toBe(200); expect(response.headers.get(RESPONSE_CLASS_HEADER)).toBeNull();
      expect(response.headers.get('content-security-policy')).toBeNull();
    }
  });
  it('returns typed non-PDF JSON when the signature read fails and closes exactly once', async () => {
    const file = path.join(root, 'read-failure.pdf'); await writeFile(file, '%PDF-1.7\nbody');
    routeHandle.target = path.basename(file);
    routeHandle.read = async () => { throw Object.assign(new Error('read failed'), { code: 'EIO' }); };
    const response = await get('read-failure.pdf', '&content=pdf');
    expect(response.status).toBe(500); expect(response.headers.get(RESPONSE_CLASS_HEADER)).toBeNull();
    expect(await response.json()).toMatchObject({ error: { code: 'FILE_READ_FAILED' } });
    expect(routeHandle.closeCalls).toBe(1);
  });

  it('closes the route-owned descriptor exactly once after normal stream completion', async () => {
    const file = path.join(root, 'complete.pdf'); const bytes = Buffer.from('%PDF-1.7\ncomplete'); await writeFile(file, bytes);
    routeHandle.target = path.basename(file);
    const response = await get('complete.pdf', '&content=pdf');
    expect(Buffer.from(await response.arrayBuffer())).toEqual(bytes);
    expect(routeHandle.closeCalls).toBe(1);
  });

  it.each(['size', 'mtime'] as const)('aborts on observable %s mutation and closes exactly once', async (mutation) => {
    const file = path.join(root, `changed-${mutation}.pdf`); const bytes = Buffer.from('%PDF-1.7\nmutable'); await writeFile(file, bytes);
    routeHandle.target = path.basename(file);
    let statCalls = 0, releaseStat!: () => void;
    const streamStatGate = new Promise<void>(resolve => { releaseStat = resolve; });
    routeHandle.stat = async (handle, args) => {
      statCalls += 1;
      if (statCalls === 3) await streamStatGate;
      return handle.stat(...args);
    };
    const response = await get(`changed-${mutation}.pdf`, '&content=pdf');
    if (mutation === 'size') await writeFile(file, Buffer.concat([bytes, Buffer.from('!')]));
    else {
      const future = new Date(Date.now() + 60_000);
      await utimes(file, future, future);
    }
    // Size and mtime are the accepted observable guards. This does not claim snapshot isolation.
    releaseStat();
    await expect(response.arrayBuffer()).rejects.toMatchObject({ code: 'FILE_CHANGED' });
    expect(response.status).toBe(200);
    expect(response.headers.get('content-type')).toBe('application/pdf');
    expect(routeHandle.closeCalls).toBe(1);
  });

  it('aborts a postcommit stream on truncation without appending JSON and closes exactly once', async () => {
    const file = path.join(root, 'truncated.pdf'); await writeFile(file, '%PDF-1.7\nbody');
    routeHandle.target = path.basename(file);
    let readCalls = 0;
    routeHandle.read = async (handle, args) => {
      readCalls += 1;
      if (readCalls === 2) return { bytesRead: 0, buffer: args[0] };
      return handle.read(...args);
    };
    const response = await get('truncated.pdf', '&content=pdf');
    expect(response.status).toBe(200); expect(response.headers.get(RESPONSE_CLASS_HEADER)).toBe('eligible-pdf-v1');
    await expect(response.arrayBuffer()).rejects.toMatchObject({ code: 'FILE_CHANGED' });
    expect(response.headers.get('content-type')).toBe('application/pdf');
    expect(routeHandle.closeCalls).toBe(1);
  });

  it('aborts on descriptor read failure after response construction without appending JSON', async () => {
    const file = path.join(root, 'stream-read-failure.pdf'); await writeFile(file, '%PDF-1.7\nbody');
    routeHandle.target = path.basename(file);
    let readCalls = 0;
    const failure = Object.assign(new Error('descriptor read failed'), { code: 'EIO' });
    routeHandle.read = async (handle, args) => {
      readCalls += 1;
      if (readCalls === 2) throw failure;
      return handle.read(...args);
    };
    const response = await get('stream-read-failure.pdf', '&content=pdf');
    expect(response.status).toBe(200); expect(response.headers.get('content-type')).toBe('application/pdf');
    await expect(response.arrayBuffer()).rejects.toBe(failure);
    expect(response.headers.get(RESPONSE_CLASS_HEADER)).toBe('eligible-pdf-v1');
    expect(routeHandle.closeCalls).toBe(1);
  });

  it('treats consumer cancellation as disconnect-equivalent and closes exactly once', async () => {
    const file = path.join(root, 'cancelled.pdf'); await writeFile(file, Buffer.concat([Buffer.from('%PDF-'), Buffer.alloc(128 * 1024)]));
    routeHandle.target = path.basename(file);
    const response = await get('cancelled.pdf', '&content=pdf');
    await response.body!.cancel('client disconnected');
    expect(routeHandle.closeCalls).toBe(1);
  });
  it('reports unsupported and missing files truthfully', async () => {
    await writeFile(path.join(root, 'a.bin'), 'hello');
    expect(await (await get('a.bin')).json()).toMatchObject({ kind: 'unsupported' });
    expect((await get('missing.txt')).status).toBe(404);
    expect((await get('a.bin', '&content=pdf')).status).toBe(415);
    await mkdir(path.join(root, 'folder')); expect((await get('folder')).status).toBe(400);
  });
  it('refuses traversal, symlink escape, instruction aliases and .git but allows .chirality', async () => {
    await writeFile(path.join(base, 'secret.txt'), 'private');
    await symlink(path.join(base, 'secret.txt'), path.join(root, 'escape.txt'));
    for (const target of ['../secret.txt', '/etc/passwd', 'a/../secret.txt', 'a\\b']) expect((await get(target)).status).toBe(400);
    expect((await get('escape.txt')).status).toBe(403);
    await writeFile(path.join(policy.instruction, 'secret.txt'), 'instruction');
    await symlink(policy.instruction, path.join(root, 'instructions'));
    expect((await get('instructions/secret.txt')).status).toBe(403);
    await symlink(policy.instruction, path.join(base, 'root-alias'));
    expect((await get('secret.txt', '', path.join(base, 'root-alias'))).status).toBe(409);
    await mkdir(path.join(root, '.git')); await writeFile(path.join(root, '.git/config'), 'git');
    expect((await get('.git/config')).status).toBe(403);
    await mkdir(path.join(root, '.chirality')); await writeFile(path.join(root, '.chirality/workflow.md'), '# Workflow');
    expect((await get('.chirality/workflow.md')).status).toBe(200);
  });
  it('keeps an already-open descriptor bound when its name is replaced', async () => {
    const file = path.join(root, 'race.txt'); await writeFile(file, 'original');
    const opened = await openDocument({ projectRoot: root, target: 'race.txt' }, policy.instruction);
    await rm(file); await writeFile(path.join(base, 'outside.txt'), 'outside'); await symlink(path.join(base, 'outside.txt'), file);
    expect(await opened.handle.readFile('utf8')).toBe('original'); await opened.handle.close();
    expect((await get('race.txt')).status).toBe(403);
  });
});

it('preserves the existing root error status/type and supports the planned path parameter', async () => {
  const error = await get('x', '', 'relative'); expect(error.status).toBe(400); expect(await error.json()).toMatchObject({ error: { code: 'INVALID_REQUEST' } });
  await writeFile(path.join(root, 'alias.md'), '# Title');
  const response = await GET(new Request(`http://localhost/api/working-root/file?projectRoot=${encodeURIComponent(root)}&path=alias.md`));
  expect(await response.json()).toMatchObject({ path: 'alias.md', mimeType: 'text/markdown', content: '# Title' });
});

it('streams bounded image MIME downloads without overriding the existing host policy', async () => {
  const svg = '<svg xmlns="http://www.w3.org/2000/svg"><script>alert(1)</script><image href="https://example.invalid/track"/><rect width="1" height="1"/></svg>';
  await writeFile(path.join(root, 'hostile.svg'), svg);
  const response = await get('hostile.svg', '&content=image');
  expect(response.headers.get('content-type')).toBe('image/svg+xml'); expect(response.headers.get('content-disposition')).toBe("attachment; filename*=UTF-8''hostile.svg");
  expect(response.headers.get('content-security-policy')).toBeNull(); // Existing Electron policy remains the owner; browser img-only behavior needs real proof.
  expect(await response.text()).toBe(svg);
  const raster = Buffer.from('iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAwMCAO+jf9sAAAAASUVORK5CYII=', 'base64');
  await writeFile(path.join(root, 'pixel.png'), raster);
  expect(await (await get('pixel.png')).json()).toMatchObject({ kind: 'image', mimeType: 'image/png', size: raster.length, tooLarge: false, reason: 'IMAGE_VIEWER' });
  expect(Buffer.from(await (await get('pixel.png', '&content=image')).arrayBuffer())).toEqual(raster);
  expect((await get('pixel.png', '&content=pdf')).status).toBe(415);
});
it('keeps the image engineering limit separate from text and refuses over-limit binary reads', async () => {
  await writeFile(path.join(root, 'large.png'), Buffer.alloc(2 * 1024 * 1024 + 1));
  expect(await (await get('large.png')).json()).toMatchObject({ tooLarge: true, reason: 'IMAGE_LIMIT_EXCEEDED', kind: 'image' });
  expect((await get('large.png', '&content=image')).status).toBe(413);
  await writeFile(path.join(root, 'large.txt'), 'x'.repeat(2 * 1024 * 1024 + 1));
  expect(await (await get('large.txt')).json()).toMatchObject({ tooLarge: false, kind: 'text' });
  await writeFile(path.join(root, 'pretend.png'), '<html><script>evil()</script></html>');
  const invalid = await get('pretend.png', '&content=image');
  expect(invalid.headers.get('content-type')).toBe('image/png'); expect(invalid.headers.get('x-content-type-options')).toBe('nosniff');
  expect(await invalid.text()).toContain('<html>'); // Bytes are never reinterpreted as executable HTML; decoder rejection is a renderer check.
});
