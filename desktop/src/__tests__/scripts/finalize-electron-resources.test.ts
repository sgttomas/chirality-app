import { chmod, mkdir, mkdtemp, readFile, realpath, rm, symlink, writeFile } from 'node:fs/promises';
import os from 'node:os';
import path from 'node:path';
import { afterEach, describe, expect, it } from 'vitest';

import afterPack, {
  FORBIDDEN_RESOURCE_ENTRIES,
  INVENTORY_NAME,
  INVENTORY_SCHEMA,
  REQUIRED_RESOURCE_FILES,
  inspectPackagedResources,
  writePackagedResourcesInventory
} from '../../../scripts/finalize-electron-resources.mjs';

const cleanup: string[] = [];
afterEach(async () => {
  await Promise.all(cleanup.splice(0).map((entry) => rm(entry, { recursive: true, force: true })));
});

async function resourcesFixture() {
  const root = await realpath(await mkdtemp(path.join(os.tmpdir(), 'chirality-resources-')));
  cleanup.push(root);
  const appOutDir = path.join(root, 'mac-arm64');
  const resourcesRoot = path.join(appOutDir, 'Chirality.app', 'Contents', 'Resources');
  for (const relativePath of REQUIRED_RESOURCE_FILES) {
    await mkdir(path.dirname(path.join(resourcesRoot, relativePath)), { recursive: true });
    await writeFile(path.join(resourcesRoot, relativePath), relativePath);
  }
  await writeFile(path.join(resourcesRoot, 'codex', 'codex-package.json'), JSON.stringify({ version: '0.154.0', target: 'aarch64-apple-darwin', entrypoint: 'bin/codex' }));
  await chmod(path.join(resourcesRoot, 'codex', 'bin', 'codex'), 0o755);
  await chmod(path.join(resourcesRoot, 'codex', 'bin', 'codex-code-mode-host'), 0o755);
  return { root, appOutDir, resourcesRoot };
}

describe('packaged resources finalizer (A2 layout)', () => {
  it('accepts the App-owned layout and writes a plain inventory', async () => {
    const { appOutDir, resourcesRoot } = await resourcesFixture();
    const result = await afterPack({ electronPlatformName: 'darwin', appOutDir, packager: { appInfo: { productFilename: 'Chirality' } } });
    expect(result.inventoryPath).toBe(path.join(resourcesRoot, INVENTORY_NAME));
    const inventory = JSON.parse(await readFile(result.inventoryPath, 'utf8'));
    expect(inventory.schema).toBe(INVENTORY_SCHEMA);
    expect(inventory.codex).toEqual({ version: '0.154.0', target: 'aarch64-apple-darwin' });
    const paths = inventory.files.map((file: { relativePath: string }) => file.relativePath);
    for (const relativePath of REQUIRED_RESOURCE_FILES) expect(paths).toContain(relativePath);
    const codex = inventory.files.find((file: { relativePath: string }) => file.relativePath === 'codex/bin/codex');
    expect(codex).toMatchObject({ kind: 'file', mode: 0o755 });
    expect(codex.sha256).toMatch(/^[a-f0-9]{64}$/);
  });

  it('rejects missing resources, non-executable Codex binaries, symlinks and retired supply-model trees', async () => {
    const { resourcesRoot } = await resourcesFixture();
    await rm(path.join(resourcesRoot, 'runtime-service', 'standalone-bin.mjs'));
    await chmod(path.join(resourcesRoot, 'codex', 'bin', 'codex'), 0o644);
    await mkdir(path.join(resourcesRoot, 'supplier'));
    await mkdir(path.join(resourcesRoot, 'native'));
    await symlink(path.join(resourcesRoot, 'app.asar'), path.join(resourcesRoot, 'linked.asar'));
    const inspection = await inspectPackagedResources(resourcesRoot);
    expect(inspection.failures).toEqual(expect.arrayContaining([
      'missing packaged resource runtime-service/standalone-bin.mjs',
      'packaged resource is not executable: codex/bin/codex',
      'symlink inside packaged resources: linked.asar',
      'retired supply-model resource is present: supplier',
      'retired supply-model resource is present: native'
    ]));
    await expect(writePackagedResourcesInventory(resourcesRoot)).rejects.toThrow(/Packaged resources are incomplete/);
    expect([...FORBIDDEN_RESOURCE_ENTRIES]).toContain('runtime-artifact-inventory.json');
  });

  it('refuses non-macOS contexts and malformed product names', async () => {
    await expect(afterPack({ electronPlatformName: 'linux' })).rejects.toThrow(/only the macOS/);
    await expect(afterPack({ electronPlatformName: 'darwin', appOutDir: '/x', packager: { appInfo: { productFilename: ' ' } } })).rejects.toThrow(/productFilename/);
  });
});
