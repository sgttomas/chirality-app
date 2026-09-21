import { readFile, writeFile } from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const scriptPath = fileURLToPath(import.meta.url);
const frontendRoot = path.resolve(path.dirname(scriptPath), '..');
const defaultLockPath = path.join(frontendRoot, 'package-lock.json');

export const PI_VERSION = '0.82.0';
export const PI_ROOT = 'node_modules/@earendil-works/pi-coding-agent';
export const PI_SIBLING_PACKAGES = [
  '@earendil-works/pi-agent-core',
  '@earendil-works/pi-ai',
  '@earendil-works/pi-tui'
];

function assertRegistryEntry(entry, packagePath) {
  if (entry?.version !== PI_VERSION) {
    throw new Error(`${packagePath} is not pinned to ${PI_VERSION}`);
  }
  if (!entry?.resolved?.startsWith('https://registry.npmjs.org/')) {
    throw new Error(`${packagePath} does not resolve from the approved HTTPS npm registry`);
  }
}

export function normalizePiLockIntegrity(lock) {
  const changes = [];

  for (const packageName of PI_SIBLING_PACKAGES) {
    const rootPath = `node_modules/${packageName}`;
    const nestedPath = `${PI_ROOT}/node_modules/${packageName}`;
    const rootEntry = lock.packages?.[rootPath];
    const nestedEntry = lock.packages?.[nestedPath];

    assertRegistryEntry(rootEntry, rootPath);
    assertRegistryEntry(nestedEntry, nestedPath);

    if (!rootEntry.integrity?.startsWith('sha512-')) {
      throw new Error(`${rootPath} has no lock-enforced SHA-512 integrity`);
    }
    if (nestedEntry.resolved !== rootEntry.resolved) {
      throw new Error(`${nestedPath} does not resolve to the exact root-pinned Pi artifact`);
    }
    if (nestedEntry.integrity && nestedEntry.integrity !== rootEntry.integrity) {
      throw new Error(`${nestedPath} has integrity that conflicts with the root-pinned artifact`);
    }
    if (nestedEntry.integrity !== rootEntry.integrity) {
      nestedEntry.integrity = rootEntry.integrity;
      changes.push(nestedPath);
    }
  }

  return changes;
}

export async function normalizePiLockFile(lockPath = defaultLockPath) {
  const lock = JSON.parse(await readFile(lockPath, 'utf8'));
  const changes = normalizePiLockIntegrity(lock);
  if (changes.length > 0) {
    await writeFile(lockPath, `${JSON.stringify(lock, null, 2)}\n`, 'utf8');
  }
  return changes;
}

if (process.argv[1] && path.resolve(process.argv[1]) === scriptPath) {
  const changes = await normalizePiLockFile();
  console.log(
    JSON.stringify(
      {
        status: 'PASS',
        changed: changes,
        integrity: 'sha512-enforced'
      },
      null,
      2
    )
  );
}
