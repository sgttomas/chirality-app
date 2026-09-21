import { createHash, randomUUID } from 'node:crypto';
import { constants, existsSync } from 'node:fs';
import { lstat, mkdir, open, realpath, rename, unlink, writeFile } from 'node:fs/promises';
import path from 'node:path';
import type { ProductInstructionsResult, ProductInstructionsState } from './product-instructions-ipc-contract';

const MAX_INSTRUCTION_BYTES = 1024 * 1024;
const digest = (bytes: Buffer): string => createHash('sha256').update(bytes).digest('hex');

/** Product defaults have different source and packaged layouts. */
export function resolveProductInstructionsDefault(options: {
  packaged: boolean;
  resourcesPath: string;
  frontendRoot: string;
  instructionRootOverride?: string;
}): string {
  if (options.packaged) return path.join(options.resourcesPath, 'instruction-root', 'AGENTS.md');
  const override = options.instructionRootOverride?.trim();
  if (override) {
    const root = path.resolve(override);
    const sourceProject = path.join(root, 'projects', 'chirality-app-dev');
    // An explicit source-root override still uses that checkout's product
    // default. A staged/custom instruction root already has the product layout.
    return existsSync(sourceProject)
      ? path.join(sourceProject, 'instructions', 'AGENTS.md')
      : path.join(root, 'AGENTS.md');
  }
  return path.resolve(options.frontendRoot, '..', 'instructions', 'AGENTS.md');
}

/** Fixed App-owned path, never a renderer-supplied destination or Codex-home file. */
export function createProductInstructionsStore(options: {
  userDataDirectory: string;
  defaultInstructionsPath: string;
}) {
  const directory = path.join(path.resolve(options.userDataDirectory), 'instructions');
  const instructionsPath = path.join(directory, 'AGENTS.md');

  const assertDirectory = async (): Promise<void> => {
    await mkdir(directory, { recursive: true });
    const value = await lstat(directory);
    if (!value.isDirectory() || value.isSymbolicLink() || await realpath(directory) !== directory) {
      throw new Error('The agent instructions folder must be a regular App-owned folder.');
    }
  };
  const read = async (file: string): Promise<Buffer> => {
    const handle = await open(file, constants.O_RDONLY | constants.O_NOFOLLOW);
    try {
      const before = await handle.stat({ bigint: true });
      if (!before.isFile() || before.size > BigInt(MAX_INSTRUCTION_BYTES)) {
        throw new Error('Agent instructions must be a regular file smaller than 1 MB.');
      }
      const bytes = await handle.readFile();
      const after = await handle.stat({ bigint: true });
      if (before.ino !== after.ino || before.size !== after.size || before.mtimeNs !== after.mtimeNs
        || before.ctimeNs !== after.ctimeNs || BigInt(bytes.length) !== after.size) {
        throw new Error('Agent instructions changed while being read. Try again.');
      }
      return bytes;
    } finally { await handle.close(); }
  };
  const get = async (): Promise<ProductInstructionsState> => {
    await assertDirectory();
    const [current, defaults] = await Promise.all([read(instructionsPath), read(options.defaultInstructionsPath)]);
    return { path: instructionsPath, modified: digest(current) !== digest(defaults) };
  };

  return {
    instructionsPath,
    async initialize(): Promise<ProductInstructionsState> {
      await assertDirectory();
      const defaults = await read(options.defaultInstructionsPath);
      try { await writeFile(instructionsPath, defaults, { flag: 'wx', mode: 0o600 }); }
      catch (error) { if ((error as NodeJS.ErrnoException).code !== 'EEXIST') throw error; }
      return get();
    },
    get,
    async restore(): Promise<ProductInstructionsState> {
      await assertDirectory();
      const [current, defaults] = await Promise.all([read(instructionsPath), read(options.defaultInstructionsPath)]);
      if (digest(current) === digest(defaults)) return get();
      // Keep the customization recoverable. The ordinary instruction basis also
      // preserves any previous content that reached an agent.
      await writeFile(path.join(directory, `AGENTS.backup-${randomUUID()}.md`), current, { flag: 'wx', mode: 0o600 });
      const pending = path.join(directory, `.AGENTS-${randomUUID()}.tmp`);
      try {
        await writeFile(pending, defaults, { flag: 'wx', mode: 0o600 });
        await rename(pending, instructionsPath);
      } finally { await unlink(pending).catch(() => undefined); }
      return get();
    }
  };
}

/** Small validated bridge; the renderer can operate only on this one known file. */
export function createProductInstructionsHandler<Event>(options: {
  authorized: (event: Event) => boolean;
  store: ReturnType<typeof createProductInstructionsStore>;
  open: (file: string) => Promise<string>;
  confirmRestore: () => Promise<boolean>;
}) {
  return async (event: Event, operation: unknown): Promise<ProductInstructionsResult> => {
    if (!options.authorized(event) || typeof operation !== 'string' || !['get', 'open', 'restore'].includes(operation)) {
      return { ok: false, error: 'The agent instructions request was denied.' };
    }
    try {
      const state = await options.store.get();
      if (operation === 'open') {
        const error = await options.open(state.path);
        if (error) return { ok: false, error: 'The agent instructions file could not be opened.' };
      }
      if (operation === 'restore' && state.modified) {
        if (!await options.confirmRestore()) return { ok: true, state, cancelled: true };
        return { ok: true, state: await options.store.restore() };
      }
      return { ok: true, state };
    } catch {
      return { ok: false, error: 'Agent instructions are unavailable. Check the App instructions folder and try again.' };
    }
  };
}
