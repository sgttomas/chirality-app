import { createHash } from 'node:crypto';
import { createReadStream } from 'node:fs';
import { lstat, readFile, realpath } from 'node:fs/promises';
import os from 'node:os';
import path from 'node:path';
import { pathToFileURL } from 'node:url';

export const ELECTRON_SUPPLY_PIN = Object.freeze({
  version: '43.2.0',
  filename: 'electron-v43.2.0-darwin-arm64.zip',
  size: 122090802,
  sha256: 'ad4a0ae3c37ee05aa06c7e2ed0627608389790f0505a2b0d20319efbe33ffe28',
  officialLine:
    'ad4a0ae3c37ee05aa06c7e2ed0627608389790f0505a2b0d20319efbe33ffe28 *electron-v43.2.0-darwin-arm64.zip',
  sourceUrl: 'https://github.com/electron/electron/releases/download/v43.2.0/SHASUMS256.txt'
});

const SCRIPT_DIRECTORY = path.dirname(new URL(import.meta.url).pathname);
const FRONTEND_DIRECTORY = path.resolve(SCRIPT_DIRECTORY, '..');
const PACKAGE_JSON_PATH = path.join(FRONTEND_DIRECTORY, 'package.json');

function validateLiteralDirectory(directory) {
  if (typeof directory !== 'string' || directory.length === 0) {
    throw new Error('Electron distribution directory must be a non-empty absolute path');
  }
  if (directory.includes('\0')) {
    throw new Error('Electron distribution directory contains a NUL byte');
  }
  if (!path.isAbsolute(directory)) {
    throw new Error('Electron distribution directory must be absolute');
  }
  if (directory !== path.normalize(directory) || directory === path.parse(directory).root) {
    throw new Error('Electron distribution directory is malformed or unsafe');
  }
  return directory;
}

export function resolveElectronDistDirectory({
  env = process.env,
  homeDirectory = os.homedir()
} = {}) {
  if (Object.hasOwn(env, 'CHIRALITY_ELECTRON_DIST_DIR')) {
    return validateLiteralDirectory(env.CHIRALITY_ELECTRON_DIST_DIR);
  }
  return validateLiteralDirectory(
    path.join(homeDirectory, 'Library', 'Caches', 'chirality', 'electron-dist')
  );
}

export async function hashFileStreaming(filePath) {
  const hash = createHash('sha256');
  for await (const chunk of createReadStream(filePath)) {
    hash.update(chunk);
  }
  return hash.digest('hex');
}

export async function verifyElectronDist({
  directory = resolveElectronDistDirectory(),
  packageJsonPath = PACKAGE_JSON_PATH,
  hashArchive = hashFileStreaming
} = {}) {
  const resolvedDirectory = validateLiteralDirectory(directory);

  let packageJson;
  try {
    packageJson = JSON.parse(await readFile(packageJsonPath, 'utf8'));
  } catch (error) {
    throw new Error(`Unable to read frontend package.json: ${error.message}`);
  }
  if (packageJson.devDependencies?.electron !== ELECTRON_SUPPLY_PIN.version) {
    throw new Error(
      `Electron devDependency must equal ${ELECTRON_SUPPLY_PIN.version}`
    );
  }

  const directoryStat = await lstat(resolvedDirectory);
  if (!directoryStat.isDirectory() || directoryStat.isSymbolicLink()) {
    throw new Error('Electron distribution directory must be a non-symlink directory');
  }
  const canonicalDirectory = await realpath(resolvedDirectory);
  if (canonicalDirectory !== resolvedDirectory) {
    throw new Error('Electron distribution directory resolves through an unsafe path');
  }

  const archivePath = path.join(resolvedDirectory, ELECTRON_SUPPLY_PIN.filename);
  if (path.dirname(archivePath) !== resolvedDirectory) {
    throw new Error('Electron archive path escapes the distribution directory');
  }
  const archiveStat = await lstat(archivePath);
  if (!archiveStat.isFile() || archiveStat.isSymbolicLink()) {
    throw new Error('Electron archive must be a regular non-symlink file');
  }
  if (archiveStat.size !== ELECTRON_SUPPLY_PIN.size) {
    throw new Error(
      `Electron archive size mismatch: expected ${ELECTRON_SUPPLY_PIN.size}, received ${archiveStat.size}`
    );
  }
  const canonicalArchive = await realpath(archivePath);
  if (canonicalArchive !== path.join(canonicalDirectory, ELECTRON_SUPPLY_PIN.filename)) {
    throw new Error('Electron archive resolves outside the distribution directory');
  }

  const digest = await hashArchive(archivePath);
  if (digest !== ELECTRON_SUPPLY_PIN.sha256) {
    throw new Error('Electron archive SHA-256 mismatch');
  }

  return resolvedDirectory;
}

/**
 * @param {{
 *   argv?: string[],
 *   stdout?: { write(text: string): unknown },
 *   stderr?: { write(text: string): unknown },
 *   verify?: () => Promise<string>
 * }} options
 */
export async function runCli(options = {}) {
  const {
    argv = process.argv.slice(2),
    stdout = process.stdout,
    stderr = process.stderr,
    verify = verifyElectronDist
  } = options;
  try {
    if (argv.length !== 0) {
      throw new Error('verify-electron-dist does not accept command-line arguments');
    }
    const directory = await verify();
    stdout.write(`${directory}\n`);
    return 0;
  } catch (error) {
    stderr.write(`Electron supply verification failed: ${error.message}\n`);
    return 1;
  }
}

const isMain =
  process.argv[1] && pathToFileURL(path.resolve(process.argv[1])).href === import.meta.url;
if (isMain) {
  process.exitCode = await runCli();
}
