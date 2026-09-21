#!/usr/bin/env node

import { execFileSync } from 'node:child_process';
import { createHash } from 'node:crypto';
import { existsSync } from 'node:fs';
import { mkdir, readdir, readFile, stat, writeFile } from 'node:fs/promises';
import path from 'node:path';

const FRONTEND_ROOT = path.resolve(path.dirname(new URL(import.meta.url).pathname), '..');
const DEFAULT_PROJECT_ROOT = path.resolve(FRONTEND_ROOT, '..');
const DEFAULT_OUTPUT_ROOT = path.resolve(
  FRONTEND_ROOT,
  'artifacts',
  'harness',
  'security',
  'latest'
);

const EXCLUDED_DIRECTORIES = new Set([
  '.git',
  '.next',
  'coverage',
  'dist',
  'dist-electron',
  'node_modules',
  'out'
]);

const TEXT_EXTENSIONS = new Set([
  '.cjs',
  '.csv',
  '.css',
  '.html',
  '.js',
  '.json',
  '.jsx',
  '.log',
  '.md',
  '.mjs',
  '.ndjson',
  '.sh',
  '.svg',
  '.ts',
  '.tsx',
  '.txt',
  '.yaml',
  '.yml'
]);

const ANTHROPIC_KEY_PATTERN = /sk-ant-[A-Za-z0-9._=/-]{8,}/g;
const URL_CREDENTIAL_PATTERN = /\bhttps?:\/\/[^\s/@:]+:[^\s/@]+@[^\s/]+/g;
const FIXTURE_MARKERS = [
  'ambient',
  'alias',
  'alt-key',
  'bridge',
  'dummy',
  'example',
  'fake',
  'fixture',
  'placeholder',
  'redaction',
  'test',
  'ui-key'
];

function nowIso() {
  return new Date().toISOString();
}

function printUsage() {
  console.log(`Usage: node ./scripts/scan-secret-evidence.mjs [options]

Options:
  --project-root <path>   Project root to scan (default: app-dev root)
  --output-root <path>    Output directory for secret-scan-summary.json
                          (default: artifacts/harness/security/latest)
  --help                  Show this message
`);
}

function readArgValue(argv, index, flagName) {
  const value = argv[index];
  if (!value || value.startsWith('--')) {
    throw new Error(`Missing value for ${flagName}`);
  }
  return value;
}

function parseArgs(argv) {
  const args = {};

  for (let index = 0; index < argv.length; index += 1) {
    const token = argv[index];

    if (token === '--help') {
      args.help = true;
      continue;
    }

    if (token === '--project-root') {
      args.projectRoot = readArgValue(argv, index + 1, token);
      index += 1;
      continue;
    }

    if (token === '--output-root') {
      args.outputRoot = readArgValue(argv, index + 1, token);
      index += 1;
      continue;
    }

    throw new Error(`Unknown argument: ${token}`);
  }

  return {
    help: args.help === true,
    projectRoot: path.resolve(args.projectRoot ?? DEFAULT_PROJECT_ROOT),
    outputRoot: path.resolve(args.outputRoot ?? DEFAULT_OUTPUT_ROOT)
  };
}

function toPosix(filePath) {
  return filePath.split(path.sep).join('/');
}

function isExcluded(relativePath) {
  return relativePath
    .split(path.sep)
    .some((part) => EXCLUDED_DIRECTORIES.has(part));
}

function isTextPath(filePath) {
  return TEXT_EXTENSIONS.has(path.extname(filePath).toLowerCase());
}

function sha256(value) {
  return createHash('sha256').update(value).digest('hex');
}

function isFixtureToken(value, relativePath) {
  const lowered = value.toLowerCase();
  if (FIXTURE_MARKERS.some((marker) => lowered.includes(marker))) {
    return true;
  }

  return relativePath.includes('__tests__') || relativePath.includes('/test/') || relativePath.includes('/tests/');
}

function lineColumnForIndex(text, index) {
  let line = 1;
  let column = 1;

  for (let cursor = 0; cursor < index; cursor += 1) {
    if (text[cursor] === '\n') {
      line += 1;
      column = 1;
    } else {
      column += 1;
    }
  }

  return { line, column };
}

function redactedFinding({ kind, value, relativePath, text, index, disposition, reason }) {
  const location = lineColumnForIndex(text, index);
  return {
    kind,
    path: toPosix(relativePath),
    line: location.line,
    column: location.column,
    valueSha256: sha256(value),
    valueLength: value.length,
    disposition,
    reason
  };
}

function collectEnvironmentSecrets() {
  const inputs = [];
  const names = [
    'ANTHROPIC_API_KEY',
    'CHIRALITY_ANTHROPIC_API_KEY',
    'CHIRALITY_OMLX_API_KEY'
  ];

  for (const name of names) {
    const value = process.env[name];
    const present = typeof value === 'string' && value.length > 0;
    const usable = present && value.length >= 8;
    inputs.push({
      name,
      present,
      scanned: usable,
      valueLength: present ? value.length : 0,
      valueSha256: usable ? sha256(value) : null,
      variants: usable
        ? [
            { kind: 'raw', value },
            { kind: 'url_encoded', value: encodeURIComponent(value) }
          ]
        : []
    });
  }

  return inputs;
}

function gitTrackedFiles(projectRoot) {
  try {
    const output = execFileSync('git', ['ls-files', '-z'], {
      cwd: projectRoot,
      encoding: 'utf8',
      stdio: ['ignore', 'pipe', 'ignore']
    });
    return output.split('\0').filter(Boolean);
  } catch {
    return [];
  }
}

function gitUntrackedFiles(projectRoot) {
  try {
    const output = execFileSync(
      'git',
      ['ls-files', '--others', '--exclude-standard', '-z'],
      {
        cwd: projectRoot,
        encoding: 'utf8',
        stdio: ['ignore', 'pipe', 'ignore']
      }
    );
    return output.split('\0').filter(Boolean);
  } catch {
    return [];
  }
}

async function walkFiles(root, baseRoot = root) {
  const results = [];
  const entries = await readdir(root, { withFileTypes: true }).catch(() => []);

  for (const entry of entries) {
    const absolutePath = path.join(root, entry.name);
    const relativePath = path.relative(baseRoot, absolutePath);

    if (entry.isDirectory()) {
      if (!isExcluded(relativePath)) {
        results.push(...(await walkFiles(absolutePath, baseRoot)));
      }
      continue;
    }

    if (entry.isFile()) {
      results.push(relativePath);
    }
  }

  return results;
}

async function candidateFiles(projectRoot) {
  const tracked = gitTrackedFiles(projectRoot);
  const trackedSet = new Set(tracked);
  const untracked = gitUntrackedFiles(projectRoot);
  const untrackedSet = new Set(untracked);
  const generatedRoots = [
    path.join(projectRoot, 'frontend', 'artifacts', 'harness')
  ];

  const generated = [];
  for (const root of generatedRoots) {
    if (!existsSync(root)) {
      continue;
    }
    for (const relativePath of await walkFiles(root, projectRoot)) {
      generated.push(relativePath);
    }
  }

  if (tracked.length > 0) {
    return {
      files: Array.from(new Set([...tracked, ...untracked, ...generated])).sort(),
      gitTrackedFileCount: trackedSet.size,
      gitUntrackedFileCount: untrackedSet.size,
      generatedArtifactFileCount: generated.length
    };
  }

  const fallbackFiles = await walkFiles(projectRoot, projectRoot);
  return {
    files: fallbackFiles.sort(),
    gitTrackedFileCount: 0,
    gitUntrackedFileCount: 0,
    generatedArtifactFileCount: generated.length
  };
}

async function scanFile({ projectRoot, relativePath, envSecrets }) {
  const absolutePath = path.join(projectRoot, relativePath);
  const fileStat = await stat(absolutePath).catch(() => null);
  if (!fileStat?.isFile()) {
    return { skipped: { path: toPosix(relativePath), reason: 'not_file' }, findings: [] };
  }
  if (fileStat.size > 5_000_000) {
    return { skipped: { path: toPosix(relativePath), reason: 'size_limit', sizeBytes: fileStat.size }, findings: [] };
  }
  if (!isTextPath(relativePath)) {
    return { skipped: { path: toPosix(relativePath), reason: 'extension', sizeBytes: fileStat.size }, findings: [] };
  }

  const buffer = await readFile(absolutePath);
  if (buffer.includes(0)) {
    return { skipped: { path: toPosix(relativePath), reason: 'binary', sizeBytes: fileStat.size }, findings: [] };
  }

  const text = buffer.toString('utf8');
  const findings = [];

  for (const secretInput of envSecrets) {
    for (const variant of secretInput.variants) {
      if (!variant.value) {
        continue;
      }

      let cursor = text.indexOf(variant.value);
      while (cursor !== -1) {
        findings.push(
          redactedFinding({
            kind: `env_${secretInput.name}_${variant.kind}`,
            value: variant.value,
            relativePath,
            text,
            index: cursor,
            disposition: 'blocked',
            reason: 'actual_environment_secret_value'
          })
        );
        cursor = text.indexOf(variant.value, cursor + variant.value.length);
      }
    }
  }

  for (const match of text.matchAll(ANTHROPIC_KEY_PATTERN)) {
    const value = match[0];
    const fixture = isFixtureToken(value, toPosix(relativePath));
    findings.push(
      redactedFinding({
        kind: 'anthropic_key_pattern',
        value,
        relativePath,
        text,
        index: match.index ?? 0,
        disposition: fixture ? 'allowed_fixture' : 'blocked',
        reason: fixture ? 'test_or_placeholder_key_material' : 'high_confidence_anthropic_key_pattern'
      })
    );
  }

  for (const match of text.matchAll(URL_CREDENTIAL_PATTERN)) {
    const value = match[0];
    const fixture = isFixtureToken(value, toPosix(relativePath));
    findings.push(
      redactedFinding({
        kind: 'url_credentials',
        value,
        relativePath,
        text,
        index: match.index ?? 0,
        disposition: fixture ? 'allowed_fixture' : 'blocked',
        reason: fixture ? 'test_or_placeholder_url_credentials' : 'url_embeds_credentials'
      })
    );
  }

  return {
    scanned: { path: toPosix(relativePath), sizeBytes: fileStat.size },
    findings
  };
}

async function main() {
  const args = parseArgs(process.argv.slice(2));
  if (args.help) {
    printUsage();
    return;
  }

  const envSecrets = collectEnvironmentSecrets();
  const candidates = await candidateFiles(args.projectRoot);
  const scannedFiles = [];
  const skippedFiles = [];
  const blockedFindings = [];
  const allowedFixtureFindings = [];

  for (const relativePath of candidates.files) {
    if (isExcluded(relativePath)) {
      skippedFiles.push({ path: toPosix(relativePath), reason: 'excluded_directory' });
      continue;
    }

    const result = await scanFile({
      projectRoot: args.projectRoot,
      relativePath,
      envSecrets
    });

    if (result.skipped) {
      skippedFiles.push(result.skipped);
      continue;
    }
    if (result.scanned) {
      scannedFiles.push(result.scanned);
    }

    for (const finding of result.findings) {
      if (finding.disposition === 'blocked') {
        blockedFindings.push(finding);
      } else {
        allowedFixtureFindings.push(finding);
      }
    }
  }

  const summary = {
    generatedAt: nowIso(),
    status: blockedFindings.length === 0 ? 'pass' : 'fail',
    projectRoot: args.projectRoot,
    scannedFileCount: scannedFiles.length,
    skippedFileCount: skippedFiles.length,
    gitTrackedFileCount: candidates.gitTrackedFileCount,
    gitUntrackedFileCount: candidates.gitUntrackedFileCount,
    generatedArtifactFileCount: candidates.generatedArtifactFileCount,
    scannedFilePaths: scannedFiles.map((entry) => entry.path),
    environmentSecretInputs: envSecrets.map(({ variants: _variants, ...entry }) => entry),
    blockedFindings,
    allowedFixtureFindingCount: allowedFixtureFindings.length,
    allowedFixtureFindings,
    skippedFiles,
    boundaries: {
      rawSecretValuesWritten: false,
      releaseReadinessClaim: false,
      networkExpansion: false
    }
  };

  await mkdir(args.outputRoot, { recursive: true });
  const summaryPath = path.join(args.outputRoot, 'secret-scan-summary.json');
  await writeFile(summaryPath, `${JSON.stringify(summary, null, 2)}\n`, 'utf8');

  console.log(`secret scan status: ${summary.status}`);
  console.log(`scanned files: ${summary.scannedFileCount}`);
  console.log(`blocked findings: ${summary.blockedFindings.length}`);
  console.log(`allowed fixture findings: ${summary.allowedFixtureFindingCount}`);
  console.log(`summary: ${summaryPath}`);

  if (summary.status !== 'pass') {
    process.exitCode = 1;
  }
}

main().catch((error) => {
  const message = error instanceof Error ? error.message : String(error);
  console.error(`secret scan failed: ${message}`);
  process.exitCode = 1;
});
