import { readFile } from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const frontendRoot = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const packageJson = JSON.parse(await readFile(path.join(frontendRoot, 'package.json'), 'utf8'));
const lock = JSON.parse(await readFile(path.join(frontendRoot, 'package-lock.json'), 'utf8'));
const notice = await readFile(path.join(frontendRoot, 'THIRD_PARTY_NOTICES_PI.md'), 'utf8');
const piRoot = 'node_modules/@earendil-works/pi-coding-agent';
const expectedVersion = '0.82.0';
const piPackages = [
  '@earendil-works/pi-agent-core',
  '@earendil-works/pi-ai',
  '@earendil-works/pi-coding-agent',
  '@earendil-works/pi-tui'
];

function fail(message) {
  throw new Error(`[pi-supply-chain] ${message}`);
}

for (const packageName of piPackages) {
  if (packageJson.dependencies?.[packageName] !== expectedVersion) {
    fail(`${packageName} must be exactly pinned to ${expectedVersion}`);
  }

  const entry = lock.packages?.[`node_modules/${packageName}`];
  if (
    entry?.version !== expectedVersion ||
    !entry?.resolved?.startsWith('https://registry.npmjs.org/') ||
    !entry?.integrity?.startsWith('sha512-')
  ) {
    fail(`${packageName} is not protected by the expected registry SHA-512 lock`);
  }
}

const closure = Object.entries(lock.packages ?? {}).filter(
  ([name, entry]) =>
    (name === piRoot || name.startsWith(`${piRoot}/node_modules/`)) &&
    typeof entry?.resolved === 'string'
);
if (closure.length < 4) {
  fail('Pi dependency closure is absent or unexpectedly small');
}

for (const [name, entry] of closure) {
  if (!entry.resolved.startsWith('https://registry.npmjs.org/')) {
    fail(`${name} resolves outside the approved HTTPS npm registry`);
  }
  if (typeof entry.integrity !== 'string' || !entry.integrity.startsWith('sha512-')) {
    fail(`${name} has no lock-enforced SHA-512 integrity`);
  }
}

const installScriptPaths = closure
  .filter(([, entry]) => entry.hasInstallScript === true)
  .map(([name]) => name.slice(`${piRoot}/node_modules/`.length))
  .sort();
const expectedInstallScripts = ['@google/genai', 'protobufjs'];
if (JSON.stringify(installScriptPaths) !== JSON.stringify(expectedInstallScripts)) {
  fail(`install-script allowlist changed: ${installScriptPaths.join(', ') || 'none'}`);
}

const asarUnpack = packageJson.build?.asarUnpack ?? [];
for (const pattern of [
  'node_modules/@earendil-works/pi-coding-agent/node_modules/**/*.node',
  'node_modules/@earendil-works/pi-coding-agent/node_modules/**/*.wasm',
  'node_modules/@earendil-works/pi-tui/**/*.node',
  'node_modules/@mariozechner/clipboard-*/**/*.node',
  'node_modules/@silvia-odwyer/photon-node/**/*.wasm'
]) {
  if (!asarUnpack.includes(pattern)) {
    fail(`missing explicit packaged native/WASM policy: ${pattern}`);
  }
}

for (const required of [
  'Copyright (c) 2025 Mario Zechner',
  '@earendil-works/pi-coding-agent',
  '@earendil-works/pi-agent-core',
  '@earendil-works/pi-ai',
  '@earendil-works/pi-tui'
]) {
  if (!notice.includes(required)) {
    fail(`Pi third-party notice is missing: ${required}`);
  }
}

console.log(
  JSON.stringify(
    {
      status: 'PASS',
      package: `@earendil-works/pi-coding-agent@${expectedVersion}`,
      closureArtifacts: closure.length,
      installScriptAllowlist: installScriptPaths,
      integrity: 'sha512-enforced',
      nativeWasmPolicy: 'explicit-asar-unpack',
      notice: 'present'
    },
    null,
    2
  )
);
