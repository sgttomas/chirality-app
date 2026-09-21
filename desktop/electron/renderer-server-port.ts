import { constants, type Stats } from 'node:fs';
import { link, lstat, open, unlink } from 'node:fs/promises';
import path from 'node:path';
import { randomUUID } from 'node:crypto';

export const RENDERER_PORT_RECORD_SCHEMA = 'chirality.renderer-port/v1';
export const RENDERER_PORT_RECORD_FILENAME = 'renderer-port.json';
const MAX_RECORD_BYTES = 256;

export type RendererPortRecord = {
  schema: typeof RENDERER_PORT_RECORD_SCHEMA;
  host: '127.0.0.1';
  port: number;
};

export type BoundRendererServer = {
  port: number;
  close: () => Promise<void>;
};

type StableRendererServerOptions = {
  userDataDirectory: string;
  bind: (port: number) => Promise<BoundRendererServer>;
};

function recordPath(userDataDirectory: string): string {
  return path.join(userDataDirectory, RENDERER_PORT_RECORD_FILENAME);
}

function validateRecord(value: unknown): RendererPortRecord {
  if (!value || typeof value !== 'object' || Array.isArray(value)) {
    throw new Error('renderer port record is not an object');
  }
  const record = value as Record<string, unknown>;
  const fields = Object.keys(record).sort();
  if (
    fields.length !== 3 ||
    fields[0] !== 'host' ||
    fields[1] !== 'port' ||
    fields[2] !== 'schema' ||
    record.schema !== RENDERER_PORT_RECORD_SCHEMA ||
    record.host !== '127.0.0.1' ||
    !Number.isSafeInteger(record.port) ||
    (record.port as number) < 1024 ||
    (record.port as number) > 65535
  ) {
    throw new Error('renderer port record has invalid fields');
  }
  return record as RendererPortRecord;
}

function validateRecordFile(entry: Stats): void {
  if (!entry.isFile() || entry.isSymbolicLink()) {
    throw new Error('renderer port record must be a regular non-symlink file');
  }
  if (entry.size <= 0 || entry.size > MAX_RECORD_BYTES) {
    throw new Error('renderer port record has an invalid size');
  }
  if (process.platform !== 'win32') {
    if ((entry.mode & 0o077) !== 0) {
      throw new Error('renderer port record permissions must be owner-only');
    }
    if (typeof process.getuid === 'function' && entry.uid !== process.getuid()) {
      throw new Error('renderer port record must be owned by the current user');
    }
  }
}

/** Absolute path of the renderer port record for a userData directory. */
export function rendererPortRecordPath(userDataDirectory: string): string {
  return recordPath(userDataDirectory);
}

/**
 * The validated saved record, `null` when none exists. Throws on any record
 * that fails validation. Shared with the daemon's activate guard, which uses
 * the saved port as its evidence of a running GUI.
 */
export async function readRendererPortRecord(filePath: string): Promise<RendererPortRecord | null> {
  let entry;
  try {
    entry = await lstat(filePath);
  } catch (error) {
    if ((error as NodeJS.ErrnoException).code === 'ENOENT') return null;
    throw error;
  }
  validateRecordFile(entry);

  const noFollow = typeof constants.O_NOFOLLOW === 'number' ? constants.O_NOFOLLOW : 0;
  const handle = await open(filePath, constants.O_RDONLY | noFollow);
  try {
    const opened = await handle.stat();
    validateRecordFile(opened);
    if (opened.dev !== entry.dev || opened.ino !== entry.ino || opened.size !== entry.size) {
      throw new Error('renderer port record changed while it was being read');
    }
    return validateRecord(JSON.parse(await handle.readFile('utf8')));
  } catch (error) {
    if (error instanceof SyntaxError) {
      throw new Error('renderer port record is not valid JSON');
    }
    throw error;
  } finally {
    await handle.close();
  }
}

async function persistRendererPortRecord(
  filePath: string,
  record: RendererPortRecord
): Promise<void> {
  const temporary = `${filePath}.${process.pid}.${randomUUID()}.tmp`;
  const handle = await open(temporary, 'wx', 0o600);
  try {
    await handle.writeFile(`${JSON.stringify(record)}\n`, 'utf8');
    await handle.sync();
  } finally {
    await handle.close();
  }

  try {
    // A hard link is an atomic create-if-absent operation. It prevents two GUI
    // processes that start against a fresh userData directory from silently
    // choosing different persistent origins.
    await link(temporary, filePath);
  } catch (error) {
    if ((error as NodeJS.ErrnoException).code !== 'EEXIST') throw error;
    const winner = await readRendererPortRecord(filePath);
    if (!winner || winner.port !== record.port) {
      throw new Error('another GUI process selected a different renderer port');
    }
  } finally {
    await unlink(temporary).catch(() => undefined);
  }
}

function bindingFailure(port: number, error: unknown): Error {
  const cause = error instanceof Error ? error : new Error(String(error));
  const code = (error as NodeJS.ErrnoException | undefined)?.code;
  return new Error(
    code === 'EADDRINUSE'
      ? `Saved renderer port ${port} is already occupied; refusing to change renderer origin`
      : `Unable to bind saved renderer port ${port}: ${cause.message}`,
    { cause }
  );
}

export async function bindStableRendererServer(
  options: StableRendererServerOptions
): Promise<BoundRendererServer> {
  const filePath = recordPath(options.userDataDirectory);
  let saved: RendererPortRecord | null;
  try {
    saved = await readRendererPortRecord(filePath);
  } catch (error) {
    throw new Error(
      `Invalid renderer port record at ${filePath}: ${error instanceof Error ? error.message : String(error)}`,
      { cause: error }
    );
  }

  if (saved) {
    try {
      return await options.bind(saved.port);
    } catch (error) {
      throw bindingFailure(saved.port, error);
    }
  }

  const server = await options.bind(0);
  try {
    await persistRendererPortRecord(filePath, {
      schema: RENDERER_PORT_RECORD_SCHEMA,
      host: '127.0.0.1',
      port: server.port
    });
    return server;
  } catch (error) {
    await server.close().catch(() => undefined);
    throw new Error(
      `Unable to persist stable renderer port at ${filePath}: ${error instanceof Error ? error.message : String(error)}`,
      { cause: error }
    );
  }
}
