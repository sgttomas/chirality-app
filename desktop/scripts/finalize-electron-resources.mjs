import { createHash } from 'node:crypto';
import { createReadStream } from 'node:fs';
import { lstat, readdir, readFile, writeFile } from 'node:fs/promises';
import path from 'node:path';

/**
 * electron-builder `afterPack` hook for the App-owned Runtime layout
 * (D-GOV-43, A2).
 *
 * Checks that `Contents/Resources` carries exactly the resources the App
 * launches against (the stock Codex platform tree, the Runtime service and
 * CLI bundles, the instruction root) and none of the retired supply-model
 * trees, then records a plain inventory of every packaged resource file for
 * the run record. Nothing here is consumed by the Runtime at startup.
 */

export const INVENTORY_NAME = 'packaged-resources-inventory.json';
export const INVENTORY_SCHEMA = 'chirality-packaged-resources-inventory/v1';

export const REQUIRED_RESOURCE_FILES = Object.freeze([
  'app.asar',
  'codex/bin/codex',
  'codex/bin/codex-code-mode-host',
  'codex/codex-package.json',
  'runtime-service/standalone-bin.mjs',
  'runtime-service/standalone-bin.mjs.map',
  'runtime-cli/chirality-cli.mjs',
  'runtime-cli/chirality-cli.mjs.map',
  'instruction-root/instruction-bundle-manifest.json'
]);

export const REQUIRED_EXECUTABLES = Object.freeze([
  'codex/bin/codex',
  'codex/bin/codex-code-mode-host'
]);

/** Supply-model residues that must not travel with an A2 build. */
export const FORBIDDEN_RESOURCE_ENTRIES = Object.freeze([
  'supplier',
  'native',
  'runtime-governance',
  'runtime-contracts',
  'runtime-artifact-inventory.json',
  'runtime-artifact-inventory-v2.json',
  'runtime-payload-manifest.json',
  'host-account-signing-predicate.json'
]);

const MAX_ENTRIES = 50_000;

async function hashFile(filePath) {
  const hash = createHash('sha256');
  let size = 0;
  for await (const chunk of createReadStream(filePath)) {
    hash.update(chunk);
    size += chunk.length;
  }
  return { sha256: hash.digest('hex'), size };
}

async function walk(root, relativeDirectory, records, failures) {
  const directory = path.join(root, relativeDirectory);
  for (const name of (await readdir(directory)).sort()) {
    const relativePath = relativeDirectory ? path.posix.join(relativeDirectory, name) : name;
    if (relativePath === 'app.asar.unpacked') {
      // Native modules unpacked by electron-builder; inventoried by name only.
      records.push({ relativePath, kind: 'directory' });
      continue;
    }
    const absolutePath = path.join(directory, name);
    const info = await lstat(absolutePath);
    if (info.isSymbolicLink()) {
      failures.push(`symlink inside packaged resources: ${relativePath}`);
      continue;
    }
    if (info.isDirectory()) {
      await walk(root, relativePath, records, failures);
      continue;
    }
    if (!info.isFile()) {
      failures.push(`unsupported entry inside packaged resources: ${relativePath}`);
      continue;
    }
    if (records.length > MAX_ENTRIES) throw new Error('Packaged resources exceed the inventory bound');
    const { sha256, size } = await hashFile(absolutePath);
    records.push({ relativePath, kind: 'file', size, sha256, mode: info.mode & 0o777 });
  }
}

export async function inspectPackagedResources(resourcesRoot) {
  const root = path.resolve(resourcesRoot);
  const failures = [];
  const files = [];
  const rootInfo = await lstat(root).catch(() => undefined);
  if (!rootInfo?.isDirectory()) {
    return { resourcesRoot: root, failures: [`Resources root is not a directory: ${root}`], files };
  }
  await walk(root, '', files, failures);
  const byPath = new Map(files.map((record) => [record.relativePath, record]));
  for (const relativePath of REQUIRED_RESOURCE_FILES) {
    const record = byPath.get(relativePath);
    if (!record || record.kind !== 'file') failures.push(`missing packaged resource ${relativePath}`);
  }
  for (const relativePath of REQUIRED_EXECUTABLES) {
    const record = byPath.get(relativePath);
    if (record?.kind === 'file' && (record.mode & 0o111) === 0) failures.push(`packaged resource is not executable: ${relativePath}`);
  }
  for (const entry of FORBIDDEN_RESOURCE_ENTRIES) {
    if (await lstat(path.join(root, entry)).then(() => true, () => false)) {
      failures.push(`retired supply-model resource is present: ${entry}`);
    }
  }
  let codex = null;
  try {
    const manifest = JSON.parse(await readFile(path.join(root, 'codex', 'codex-package.json'), 'utf8'));
    codex = { version: manifest.version ?? null, target: manifest.target ?? null };
  } catch {
    failures.push('codex/codex-package.json is missing or unreadable');
  }
  return { resourcesRoot: root, failures, files, codex };
}

export async function writePackagedResourcesInventory(resourcesRoot, { now = () => new Date() } = {}) {
  const inspection = await inspectPackagedResources(resourcesRoot);
  if (inspection.failures.length > 0) {
    throw new Error(`Packaged resources are incomplete: ${inspection.failures.join('; ')}`);
  }
  const inventoryPath = path.join(inspection.resourcesRoot, INVENTORY_NAME);
  const inventory = {
    schema: INVENTORY_SCHEMA,
    generatedAt: now().toISOString(),
    codex: inspection.codex,
    files: inspection.files
  };
  await writeFile(inventoryPath, `${JSON.stringify(inventory, null, 2)}\n`, { encoding: 'utf8', mode: 0o644 });
  return { inventoryPath, inventory };
}

export default async function afterPack(context) {
  if (context?.electronPlatformName !== 'darwin') {
    throw new Error('Packaged resources inventory currently supports only the macOS Electron package');
  }
  const productFilename = context?.packager?.appInfo?.productFilename;
  if (typeof productFilename !== 'string' || productFilename.trim() !== productFilename || productFilename.length === 0) {
    throw new Error('Electron afterPack context is missing productFilename');
  }
  const resourcesRoot = path.resolve(context.appOutDir, `${productFilename}.app`, 'Contents', 'Resources');
  return writePackagedResourcesInventory(resourcesRoot);
}
