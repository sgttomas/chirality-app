import { mkdir, mkdtemp, readFile, readdir, rm, stat } from 'node:fs/promises';
import os from 'node:os';
import path from 'node:path';
import { afterEach, beforeEach, describe, expect, it } from 'vitest';
import { writeTextFileAtomically } from '../../lib/atomic-write';

let tmpRoot: string;

async function tempEntriesFor(filePath: string): Promise<string[]> {
  const directory = path.dirname(filePath);
  const baseName = path.basename(filePath);
  return (await readdir(directory)).filter(
    (entry) => entry.startsWith(`.${baseName}.`) && entry.endsWith('.tmp')
  );
}

beforeEach(async () => {
  tmpRoot = await mkdtemp(path.join(os.tmpdir(), 'chirality-atomic-write-'));
});

afterEach(async () => {
  await rm(tmpRoot, { recursive: true, force: true });
});

describe('writeTextFileAtomically', () => {
  it('replaces file content through a same-directory temp file and cleans up the temp path', async () => {
    const filePath = path.join(tmpRoot, 'record.md');

    const result = await writeTextFileAtomically(filePath, 'first\n');
    expect(result.strategy).toBe('same-directory-rename');
    expect(path.dirname(result.tempFilePath)).toBe(tmpRoot);

    await writeTextFileAtomically(filePath, 'second\n');

    await expect(readFile(filePath, 'utf8')).resolves.toBe('second\n');
    await expect(tempEntriesFor(filePath)).resolves.toEqual([]);
  });

  it('removes the temp file when the final rename cannot replace the target path', async () => {
    const targetPath = path.join(tmpRoot, 'target-directory');
    await mkdir(targetPath);

    await expect(writeTextFileAtomically(targetPath, 'content\n')).rejects.toBeTruthy();

    expect((await stat(targetPath)).isDirectory()).toBe(true);
    await expect(tempEntriesFor(targetPath)).resolves.toEqual([]);
  });
});
