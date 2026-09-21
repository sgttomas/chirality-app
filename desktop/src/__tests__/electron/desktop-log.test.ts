import { mkdtemp, readFile, rm, stat, writeFile } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { afterEach, describe, expect, it } from 'vitest';
import { createDesktopLogger, createNoopDesktopLogger, redactAccountEmails } from '../../../electron/desktop-log';

const temporaryDirectories: string[] = [];

afterEach(async () => {
  while (temporaryDirectories.length > 0) {
    const directory = temporaryDirectories.pop();
    if (directory) {
      await rm(directory, { recursive: true, force: true });
    }
  }
});

async function temporaryDirectory(): Promise<string> {
  const root = await mkdtemp(join(tmpdir(), 'chirality-desktop-log-'));
  temporaryDirectories.push(root);
  return root;
}

describe('createDesktopLogger', () => {
  it('creates the log directory and appends one timestamped line per event', async () => {
    const root = await temporaryDirectory();
    const directory = join(root, 'logs');
    const logger = createDesktopLogger({
      directory,
      mirrorToConsole: false,
      now: () => new Date('2026-07-25T12:00:00.000Z')
    });

    logger.info('runtime.connectivity.bound', { priorFailedAttempts: 2 });
    logger.warn('runtime.connectivity.lost');
    logger.error('runtime.connectivity.bind_failed', new Error('socket refused'));

    const contents = await readFile(logger.filePath, 'utf8');
    const lines = contents.trimEnd().split('\n');
    expect(logger.filePath).toBe(join(directory, 'desktop-main.log'));
    expect(lines).toEqual([
      '2026-07-25T12:00:00.000Z [info] runtime.connectivity.bound {"priorFailedAttempts":2}',
      '2026-07-25T12:00:00.000Z [warn] runtime.connectivity.lost',
      '2026-07-25T12:00:00.000Z [error] runtime.connectivity.bind_failed {"error":"socket refused"}'
    ]);
  });

  it('appends to an existing file rather than truncating it', async () => {
    const root = await temporaryDirectory();
    const logger = createDesktopLogger({ directory: root, mirrorToConsole: false });

    logger.info('first');
    const firstLogger = createDesktopLogger({ directory: root, mirrorToConsole: false });
    firstLogger.info('second');

    const contents = await readFile(logger.filePath, 'utf8');
    expect(contents).toContain('first');
    expect(contents).toContain('second');
  });

  it('writes the log file with owner-only permissions', async () => {
    const root = await temporaryDirectory();
    const logger = createDesktopLogger({ directory: root, mirrorToConsole: false });
    logger.info('permission-check');
    const metadata = await stat(logger.filePath);
    expect(metadata.mode & 0o777).toBe(0o600);
  });

  it('rotates once past the size ceiling so the file cannot grow without bound', async () => {
    const root = await temporaryDirectory();
    const logger = createDesktopLogger({
      directory: root,
      mirrorToConsole: false,
      maxBytes: 64
    });

    await writeFile(logger.filePath, 'x'.repeat(200), 'utf8');
    logger.info('after-rotation');

    const rotated = await readFile(`${logger.filePath}.1`, 'utf8');
    const active = await readFile(logger.filePath, 'utf8');
    expect(rotated).toHaveLength(200);
    expect(active).toContain('after-rotation');
    expect(active).not.toContain('xxxx');
  });

  it('never throws when the target directory cannot be used', async () => {
    const root = await temporaryDirectory();
    // A file where the directory should be makes both mkdir and append fail.
    const blocked = join(root, 'blocked');
    await writeFile(blocked, 'not-a-directory', 'utf8');
    const logger = createDesktopLogger({ directory: blocked, mirrorToConsole: false });

    expect(() => logger.error('should-not-throw', { detail: 1 })).not.toThrow();
  });

  it('serialises non-JSON-safe details without throwing', async () => {
    const root = await temporaryDirectory();
    const logger = createDesktopLogger({ directory: root, mirrorToConsole: false });
    const cyclic: Record<string, unknown> = {};
    cyclic.self = cyclic;

    expect(() => logger.info('cyclic', cyclic)).not.toThrow();
    logger.info('bigint', { value: 1n } as unknown);
    logger.info('plain-string', 'a message');

    const contents = await readFile(logger.filePath, 'utf8');
    expect(contents).toContain('cyclic');
    expect(contents).toContain('plain-string a message');
  });

  it('omits the detail segment when no detail is supplied', async () => {
    const root = await temporaryDirectory();
    const logger = createDesktopLogger({
      directory: root,
      mirrorToConsole: false,
      now: () => new Date('2026-07-25T00:00:00.000Z')
    });
    logger.info('bare');
    const contents = await readFile(logger.filePath, 'utf8');
    expect(contents).toBe('2026-07-25T00:00:00.000Z [info] bare\n');
  });
});

describe('account e-mail redaction at the writer', () => {
  it('scrubs addresses from events and details but leaves scoped package names alone', async () => {
    const root = await temporaryDirectory();
    const logger = createDesktopLogger({ directory: root, mirrorToConsole: false });
    logger.info('runtime.service.stderr', 'account/read owner.name+tag@example.co.uk plan pro');
    logger.warn('runtime.service.stderr', { message: 'login as second@example.org failed', package: '@chirality/runtime-core' });
    logger.error('owner@example.com');
    const contents = await readFile(logger.filePath, 'utf8');
    expect(contents).toContain('account/read [redacted-email] plan pro');
    expect(contents).toContain('"message":"login as [redacted-email] failed"');
    expect(contents).toContain('"package":"@chirality/runtime-core"');
    expect(contents).toContain('[error] [redacted-email]');
    expect(contents).not.toMatch(/example\.(com|org|co\.uk)/u);
    expect(redactAccountEmails('a@b.io and @chirality/x')).toBe('[redacted-email] and @chirality/x');
  });
});

describe('createNoopDesktopLogger', () => {
  it('accepts every call and writes nothing', () => {
    const logger = createNoopDesktopLogger();
    expect(logger.filePath).toBe('');
    expect(() => {
      logger.info('a');
      logger.warn('b');
      logger.error('c');
      logger.log('info', 'd', { e: 1 });
    }).not.toThrow();
  });
});
