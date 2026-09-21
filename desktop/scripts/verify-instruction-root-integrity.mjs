#!/usr/bin/env node

import { execSync } from 'node:child_process';
import { createHash } from 'node:crypto';
import { existsSync } from 'node:fs';
import { mkdir, readdir, readFile, stat, writeFile } from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import {
  BUNDLE_MANIFEST,
  BUNDLED_SKILL_NAMES,
  DOC_FILES,
  SKILL_TOOL_CLOSURE,
  buildExpectedInstructionManifest
} from './prepare-packaged-instruction-root.mjs';

const scriptPath = fileURLToPath(import.meta.url);
export const ELECTRON_OUTPUT_DIRECTORY_ENV = 'CHIRALITY_ELECTRON_OUTPUT_DIRECTORY';

export function resolvePackagedInstructionRoot(env = process.env, cwd = process.cwd()) {
  let outputDirectory = path.join(cwd, 'dist');
  if (Object.prototype.hasOwnProperty.call(env, ELECTRON_OUTPUT_DIRECTORY_ENV)) {
    const candidate = env[ELECTRON_OUTPUT_DIRECTORY_ENV];
    if (typeof candidate !== 'string' || candidate.length === 0 || candidate.includes('\0')
      || !path.isAbsolute(candidate) || path.normalize(candidate) !== candidate) {
      throw new Error(`${ELECTRON_OUTPUT_DIRECTORY_ENV} must be a normalized absolute path`);
    }
    outputDirectory = candidate;
  }
  return path.join(outputDirectory, 'mac-arm64', 'Chirality.app', 'Contents', 'Resources', 'instruction-root');
}

const REQUIRED_ROOT_FILES = [
  'AGENTS.md',
  'CLAUDE.md',
  'README.md'
];

const REQUIRED_DOC_FILES = [
  'DIRECTIVE.md',
  'CONTRACT.md',
  'SPEC.md',
  'TYPES.md',
  'PLAN.md',
  'WHAT-IS-AN-AGENT.md'
];

const REQUIRED_UNPACKED_SDK_FILES = [
  'app.asar.unpacked/node_modules/@anthropic-ai/claude-agent-sdk/package.json',
  'app.asar.unpacked/node_modules/@anthropic-ai/claude-agent-sdk/sdk.mjs',
  'app.asar.unpacked/node_modules/@anthropic-ai/claude-agent-sdk/manifest.json'
];

const SOURCE_COMPLETENESS_CANDIDATE_PATHS = [
  {
    id: 'KG-001-tools-registry',
    path: 'tools/REGISTRY.md',
    description: 'PRD KG-001 candidate source registry asset'
  },
  {
    id: 'KG-001-examples',
    path: 'examples',
    description: 'PRD KG-001 candidate examples source asset'
  }
];

const SDK_PLATFORM_PACKAGE_BY_RUNTIME = new Map([
  ['darwin:arm64', '@anthropic-ai/claude-agent-sdk-darwin-arm64'],
  ['darwin:x64', '@anthropic-ai/claude-agent-sdk-darwin-x64'],
  ['linux:arm64', '@anthropic-ai/claude-agent-sdk-linux-arm64'],
  ['linux:x64', '@anthropic-ai/claude-agent-sdk-linux-x64'],
  ['win32:arm64', '@anthropic-ai/claude-agent-sdk-win32-arm64'],
  ['win32:x64', '@anthropic-ai/claude-agent-sdk-win32-x64']
]);

const RUNTIME_PROFILES = new Set(['codex-only', 'legacy-claude']);

function toPosix(relativePath) {
  return relativePath.split(path.sep).join('/');
}

function nowIso() {
  return new Date().toISOString();
}

function printUsage(log) {
  log(`Usage: node ./scripts/verify-instruction-root-integrity.mjs [options]

Options:
  --source-root <path>   Monolithic source instruction-root root
  --root-files-root <path>
                         Source root for AGENTS.md, CLAUDE.md, and README.md
                         (default: auto-detected monorepo root)
  --agents-root <path>   Source agents directory root (default: <root-files-root>/agents)
  --docs-root <path>     Source canonical docs directory root (default: <root-files-root>/docs)
  --bundle-root <path>   Packaged instruction root (default: packaged Resources/instruction-root)
  --output-root <path>   Output directory for manifest + summary (default: artifacts/harness/instruction-root-integrity/latest)
  --sdk-bundle-root <path>
                         Packaged Resources root containing app.asar.unpacked
                         (used only by --runtime-profile legacy-claude)
  --runtime-profile <profile>
                         Runtime supplier proof: codex-only (default) or legacy-claude
  --help                 Show this message
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
  const options = {};

  for (let index = 0; index < argv.length; index += 1) {
    const token = argv[index];

    if (token === '--help') {
      options.help = true;
      continue;
    }

    if (token === '--source-root') {
      options.sourceRoot = readArgValue(argv, index + 1, token);
      index += 1;
      continue;
    }

    if (token === '--root-files-root') {
      options.rootFilesRoot = readArgValue(argv, index + 1, token);
      index += 1;
      continue;
    }

    if (token === '--agents-root') {
      options.agentsRoot = readArgValue(argv, index + 1, token);
      index += 1;
      continue;
    }

    if (token === '--docs-root') {
      options.docsRoot = readArgValue(argv, index + 1, token);
      index += 1;
      continue;
    }

    if (token === '--bundle-root') {
      options.bundleRoot = readArgValue(argv, index + 1, token);
      index += 1;
      continue;
    }

    if (token === '--output-root') {
      options.outputRoot = readArgValue(argv, index + 1, token);
      index += 1;
      continue;
    }

    if (token === '--sdk-bundle-root') {
      options.sdkBundleRoot = readArgValue(argv, index + 1, token);
      index += 1;
      continue;
    }

    if (token === '--runtime-profile') {
      options.runtimeProfile = readArgValue(argv, index + 1, token);
      index += 1;
      continue;
    }

    throw new Error(`Unknown argument: ${token}`);
  }

  return options;
}

async function sha256ForFile(absolutePath) {
  const fileBuffer = await readFile(absolutePath);
  const fileStat = await stat(absolutePath);
  if (!fileStat.isFile()) {
    throw new Error(`Expected a file but found non-file entry: ${absolutePath}`);
  }
  return {
    sha256: createHash('sha256').update(fileBuffer).digest('hex'),
    sizeBytes: fileStat.size
  };
}

function readGitSha(sourceRoot) {
  try {
    return execSync('git rev-parse HEAD', {
      cwd: sourceRoot,
      stdio: ['ignore', 'pipe', 'ignore']
    })
      .toString('utf8')
      .trim();
  } catch {
    return null;
  }
}

function hasMonolithicInstructionRootShape(candidateRoot) {
  return (
    existsSync(path.join(candidateRoot, 'agents')) &&
    existsSync(path.join(candidateRoot, 'AGENTS.md')) &&
    existsSync(path.join(candidateRoot, 'docs', 'DIRECTIVE.md'))
  );
}

function hasSplitInstructionRootShape({ rootFilesRoot, agentsRoot, docsRoot }) {
  return (
    REQUIRED_ROOT_FILES.every((fileName) => existsSync(path.join(rootFilesRoot, fileName))) &&
    existsSync(agentsRoot) &&
    REQUIRED_DOC_FILES.every((fileName) => existsSync(path.join(docsRoot, fileName)))
  );
}

function resolveDefaultSourceRoots(cwd) {
  const envRoot = process.env.CHIRALITY_INSTRUCTION_ROOT
    ? path.resolve(process.env.CHIRALITY_INSTRUCTION_ROOT)
    : undefined;

  if (envRoot && hasMonolithicInstructionRootShape(envRoot)) {
    return {
      rootFilesRoot: envRoot,
      agentsRoot: path.join(envRoot, 'agents'),
      docsRoot: path.join(envRoot, 'docs'),
      sourceLayout: 'monolithic',
      sourceRoot: envRoot
    };
  }

  const monorepoRoot = path.resolve(cwd, '..', '..', '..');
  const splitCandidate = {
    rootFilesRoot: monorepoRoot,
    agentsRoot: path.join(monorepoRoot, 'agents'),
    docsRoot: path.join(monorepoRoot, 'docs'),
    sourceLayout: 'split'
  };

  if (hasSplitInstructionRootShape(splitCandidate)) {
    return splitCandidate;
  }

  const candidates = [
    envRoot,
    path.resolve(cwd, '..'),
    path.resolve(cwd, '..', '..', '..')
  ].filter(Boolean);

  const sourceRoot = candidates.find(hasMonolithicInstructionRootShape) ?? candidates[0];
  return {
    rootFilesRoot: sourceRoot,
    agentsRoot: path.join(sourceRoot, 'agents'),
    docsRoot: path.join(sourceRoot, 'docs'),
    sourceLayout: 'monolithic',
    sourceRoot
  };
}

function resolveSourceRoots(args, cwd) {
  if (args.sourceRoot) {
    const sourceRoot = path.resolve(args.sourceRoot);
    return {
      rootFilesRoot: sourceRoot,
      agentsRoot: path.join(sourceRoot, 'agents'),
      docsRoot: path.join(sourceRoot, 'docs'),
      sourceLayout: 'monolithic',
      sourceRoot
    };
  }

  const defaults = resolveDefaultSourceRoots(cwd);
  const rootFilesRoot = path.resolve(args.rootFilesRoot ?? defaults.rootFilesRoot);
  const agentsRoot = path.resolve(args.agentsRoot ?? defaults.agentsRoot);
  const docsRoot = path.resolve(args.docsRoot ?? defaults.docsRoot);
  const sourceLayout =
    rootFilesRoot === docsRoot && agentsRoot === path.join(rootFilesRoot, 'agents')
      ? 'monolithic'
      : 'split';

  return {
    rootFilesRoot,
    agentsRoot,
    docsRoot,
    sourceLayout,
    sourceRoot: sourceLayout === 'monolithic' ? rootFilesRoot : undefined
  };
}

async function listSourceAgentFiles(agentsRoot) {
  const entries = await readdir(agentsRoot, { withFileTypes: true });

  const agentFiles = entries
    .filter((entry) => entry.isFile() && /^AGENT_.*\.md$/.test(entry.name))
    .map((entry) => entry.name)
    .sort();

  if (agentFiles.length === 0) {
    throw new Error(`No AGENT_*.md files were found in ${agentsRoot}`);
  }

  return agentFiles;
}

async function listBundleAgentFiles(bundleRoot) {
  const agentsDirectory = path.join(bundleRoot, 'agents');
  let entries = [];
  try {
    entries = await readdir(agentsDirectory, { withFileTypes: true });
  } catch {
    return [];
  }

  return entries
    .filter((entry) => entry.isFile() && /^AGENT_.*\.md$/.test(entry.name))
    .map((entry) => toPosix(path.join('agents', entry.name)))
    .sort();
}

async function listBundleInstructionFiles(bundleRoot) {
  const files = [];
  async function visit(directory, prefix = '') {
    for (const entry of await readdir(directory, { withFileTypes: true })) {
      const relativePath = prefix ? `${prefix}/${entry.name}` : entry.name;
      if (entry.isDirectory()) await visit(path.join(directory, entry.name), relativePath);
      else files.push(toPosix(relativePath));
    }
  }
  await visit(bundleRoot);
  return files.sort();
}

async function buildSourceManifest({ rootFilesRoot, agentsRoot, docsRoot }, legacyFixture = false) {
  if (!legacyFixture) {
    const expected = await buildExpectedInstructionManifest({ rootFilesRoot, agentsRoot, docsRoot });
    const entries = [];
    for (const entry of expected.entries) {
      const digest = entry.expectedContent
        ? {
            sha256: createHash('sha256').update(entry.expectedContent).digest('hex'),
            sizeBytes: entry.expectedContent.length
          }
        : await sha256ForFile(entry.sourcePath);
      entries.push({
        path: entry.bundlePath,
        sourcePath: entry.sourcePath,
        sha256: digest.sha256,
        sizeBytes: digest.sizeBytes
      });
    }
    return entries;
  }
  const sourceAgentFiles = await listSourceAgentFiles(agentsRoot);
  const sourceEntries = [
    ...REQUIRED_ROOT_FILES.map((fileName) => ({
      bundlePath: fileName,
      sourcePath: path.join(rootFilesRoot, fileName)
    })),
    ...REQUIRED_DOC_FILES.map((fileName) => ({
      bundlePath: toPosix(path.join('docs', fileName)),
      sourcePath: path.join(docsRoot, fileName)
    })),
    ...sourceAgentFiles.map((fileName) => ({
      bundlePath: toPosix(path.join('agents', fileName)),
      sourcePath: path.join(agentsRoot, fileName)
    }))
  ];

  const entries = [];
  for (const entry of sourceEntries) {
    const digest = await sha256ForFile(entry.sourcePath);
    entries.push({
      path: entry.bundlePath,
      sourcePath: entry.sourcePath,
      sha256: digest.sha256,
      sizeBytes: digest.sizeBytes
    });
  }

  return entries;
}

async function verifyManifestAgainstBundle({ manifestEntries, bundleRoot, legacyFixture }) {
  const missingInBundle = [];
  const mismatchedFiles = [];
  const comparisons = [];

  for (const entry of manifestEntries) {
    const bundleFilePath = path.join(bundleRoot, entry.path);
    try {
      const bundleDigest = await sha256ForFile(bundleFilePath);
      const hashesMatch = bundleDigest.sha256 === entry.sha256;

      comparisons.push({
        path: entry.path,
        sourceSha256: entry.sha256,
        bundleSha256: bundleDigest.sha256,
        sourceSizeBytes: entry.sizeBytes,
        bundleSizeBytes: bundleDigest.sizeBytes,
        match: hashesMatch
      });

      if (!hashesMatch) {
        mismatchedFiles.push({
          path: entry.path,
          sourceSha256: entry.sha256,
          bundleSha256: bundleDigest.sha256
        });
      }
    } catch {
      missingInBundle.push(entry.path);
    }
  }

  const sourceAgentSet = new Set(
    manifestEntries.filter((entry) => entry.path.startsWith('agents/')).map((entry) => entry.path)
  );
  const bundleAgentFiles = await listBundleAgentFiles(bundleRoot);
  const unexpectedBundleAgentFiles = bundleAgentFiles.filter((entry) => !sourceAgentSet.has(entry));

  let unexpectedBundleFiles = [];
  let bundleManifestStatus = legacyFixture ? 'not-applicable' : 'missing';
  if (!legacyFixture) {
    const expectedSet = new Set([...manifestEntries.map((entry) => entry.path), BUNDLE_MANIFEST]);
    unexpectedBundleFiles = (await listBundleInstructionFiles(bundleRoot)).filter(
      (entry) => !expectedSet.has(entry)
    );
    try {
      const value = JSON.parse(await readFile(path.join(bundleRoot, BUNDLE_MANIFEST), 'utf8'));
      const expectedFiles = manifestEntries.map(({ path: filePath, sha256, sizeBytes }) => ({
        path: filePath,
        sizeBytes,
        sha256
      }));
      const skills = Array.isArray(value.skills) ? value.skills : [];
      const expectedSkills = [...BUNDLED_SKILL_NAMES].sort().map((name) => ({
        name,
        resources: expectedFiles.filter((entry) => entry.path.startsWith(`.agents/skills/${name}/`)).map((entry) => entry.path),
        toolMembers: (SKILL_TOOL_CLOSURE[name]?.toolMembers ?? []).map((entry) => `tools/${entry}`),
        externalPrerequisites: SKILL_TOOL_CLOSURE[name]?.externalPrerequisites ?? []
      }));
      bundleManifestStatus =
        value.schema === 'chirality-instruction-bundle-manifest/v2' &&
        value.sourceSchema === 'chirality-method-index/v1' &&
        JSON.stringify(value.files) === JSON.stringify(expectedFiles) &&
        JSON.stringify(value.excludedSkillNames) === JSON.stringify(['chirality-change']) &&
        value.toolMembersSemantics ===
          'packaged dependency bytes only; allowed capabilities and commands come from each skill execution.json and the outer policy intersection' &&
        JSON.stringify(value.documentationClosure) === JSON.stringify({
          rule: 'direct-root-doc-references-from-bundled-entry-roles-workflows-and-skills',
          files: DOC_FILES.map((entry) => `docs/${entry}`)
        }) &&
        JSON.stringify(skills) === JSON.stringify(expectedSkills)
          ? 'match'
          : 'mismatch';
    } catch {
      bundleManifestStatus = 'missing';
    }
  }

  return {
    missingInBundle,
    mismatchedFiles,
    unexpectedBundleAgentFiles,
    unexpectedBundleFiles,
    bundleManifestStatus,
    comparisons
  };
}

function resolveSdkPlatformPackageName() {
  return SDK_PLATFORM_PACKAGE_BY_RUNTIME.get(`${process.platform}:${process.arch}`) ?? null;
}

function buildRequiredUnpackedSdkFiles() {
  const platformPackageName = resolveSdkPlatformPackageName();
  const platformPackageCandidates = platformPackageName
    ? [
        `app.asar.unpacked/node_modules/${platformPackageName}`,
        `app.asar.unpacked/node_modules/@anthropic-ai/claude-agent-sdk/node_modules/${platformPackageName}`
      ]
    : [];

  return {
    platformPackageName,
    requiredFiles: [...REQUIRED_UNPACKED_SDK_FILES],
    platformPackageCandidates: platformPackageCandidates.map((root) => ({
      root,
      files: [`${root}/package.json`, `${root}/claude`]
    }))
  };
}

async function verifyUnpackedSdkBundle({ bundleRoot }) {
  const { platformPackageName, requiredFiles, platformPackageCandidates } =
    buildRequiredUnpackedSdkFiles();
  const missingFiles = [];
  const comparisons = [];

  for (const relativePath of requiredFiles) {
    const absolutePath = path.join(bundleRoot, relativePath);
    try {
      const fileStat = await stat(absolutePath);
      const isFile = fileStat.isFile();
      comparisons.push({
        path: relativePath,
        sizeBytes: isFile ? fileStat.size : null,
        present: isFile
      });
      if (!isFile) {
        missingFiles.push(relativePath);
      }
    } catch {
      comparisons.push({
        path: relativePath,
        sizeBytes: null,
        present: false
      });
      missingFiles.push(relativePath);
    }
  }

  const platformCandidateComparisons = [];
  let selectedPlatformPackageRoot = null;

  for (const candidate of platformPackageCandidates) {
    const candidateFiles = [];
    for (const relativePath of candidate.files) {
      const absolutePath = path.join(bundleRoot, relativePath);
      try {
        const fileStat = await stat(absolutePath);
        candidateFiles.push({
          path: relativePath,
          sizeBytes: fileStat.isFile() ? fileStat.size : null,
          present: fileStat.isFile()
        });
      } catch {
        candidateFiles.push({
          path: relativePath,
          sizeBytes: null,
          present: false
        });
      }
    }

    const found = candidateFiles.every((entry) => entry.present);
    platformCandidateComparisons.push({
      root: candidate.root,
      found,
      files: candidateFiles
    });

    if (found && !selectedPlatformPackageRoot) {
      selectedPlatformPackageRoot = candidate.root;
    }
  }

  if (platformPackageName && !selectedPlatformPackageRoot) {
    missingFiles.push(
      `one complete ${platformPackageName} unpacked package under ${platformPackageCandidates
        .map((candidate) => candidate.root)
        .join(' or ')}`
    );
  }

  return {
    platformPackageName,
    selectedPlatformPackageRoot,
    missingFiles,
    comparisons,
    platformPackageCandidates: platformCandidateComparisons
  };
}

function buildSourceCompletenessChecklist({ sourceRoots, manifestEntries, verification, legacyFixture }) {
  const bundleIssueCount =
    verification.missingInBundle.length +
    verification.mismatchedFiles.length +
    verification.unexpectedBundleAgentFiles.length +
    verification.unexpectedBundleFiles.length +
    (['missing', 'mismatch'].includes(verification.bundleManifestStatus) ? 1 : 0);

  const rows = [
    {
      id: 'SOW-073-OI-004-required-instruction-root-assets',
      source: 'SOW-073; OI-004; docs/PRD.md KG-001 under D-APP-38',
      description:
        'Required instruction-root source assets are complete enough for source-to-bundle comparison.',
      status: bundleIssueCount === 0 ? 'satisfied' : 'remediation_required',
      remediationStatus: bundleIssueCount === 0 ? 'not_required' : 'required',
      evidence: {
        checkedFileCount: manifestEntries.length,
        missingInBundle: verification.missingInBundle,
        mismatchedFiles: verification.mismatchedFiles.map((entry) => entry.path),
        unexpectedBundleAgentFiles: verification.unexpectedBundleAgentFiles,
        unexpectedBundleFiles: verification.unexpectedBundleFiles,
        bundleManifestStatus: verification.bundleManifestStatus
      }
    }
  ];

  for (const candidate of SOURCE_COMPLETENESS_CANDIDATE_PATHS) {
    const absolutePath = path.join(sourceRoots.rootFilesRoot, candidate.path);
    const sourcePresent = existsSync(absolutePath);
    const bundledPresent = manifestEntries.some(
      (entry) => entry.path === candidate.path || entry.path.startsWith(`${candidate.path}/`)
    );
    const satisfied = legacyFixture ? sourcePresent : sourcePresent && bundledPresent;
    rows.push({
      id: candidate.id,
      source: 'docs/PRD.md KG-001 under D-APP-38',
      description: candidate.description,
      path: candidate.path,
      absolutePath,
      status: satisfied ? 'satisfied' : 'remediation_required',
      remediationStatus: satisfied ? 'not_required' : 'required',
      evidence: {
        sourcePresent,
        bundledPresent,
        legacySourceOnlyCheck: legacyFixture
      }
    });
  }

  return {
    status: rows.some((row) => row.remediationStatus === 'required') ? 'needs_remediation' : 'pass',
    rows
  };
}

async function writeJson(filePath, value) {
  await writeFile(filePath, `${JSON.stringify(value, null, 2)}\n`, 'utf8');
}

/**
 * Runs the instruction-root integrity verification. Returns the process exit
 * code (0 pass, 1 fail). `opts.cwd` overrides the working directory and
 * `opts.log` / `opts.logError` override the output writers so tests can call
 * this in-process instead of spawning node.
 */
export async function run(argv = process.argv.slice(2), opts = {}) {
  const cwd = opts.cwd ?? process.cwd();
  const log = opts.log ?? ((line) => console.log(line));
  const logError = opts.logError ?? ((line) => console.error(line));

  try {
    return await runVerification(argv, {
      cwd,
      env: opts.env ?? process.env,
      log,
      logError,
      legacyFixture: opts.legacyFixture === true
    });
  } catch (error) {
    const message = error instanceof Error ? error.message : String(error);
    logError(`instruction-root integrity verification failed: ${message}`);
    return 1;
  }
}

async function runVerification(argv, { cwd, env, log, logError, legacyFixture }) {
  const args = parseArgs(argv);
  if (args.help) {
    printUsage(log);
    return 0;
  }

  const runtimeProfile = args.runtimeProfile ?? 'codex-only';
  if (!RUNTIME_PROFILES.has(runtimeProfile)) {
    throw new Error(`Unsupported runtime profile: ${runtimeProfile}`);
  }

  const sourceRoots = resolveSourceRoots(args, cwd);
  const bundleRoot = path.resolve(
    args.bundleRoot ?? resolvePackagedInstructionRoot(env, cwd)
  );
  const outputRoot = path.resolve(
    args.outputRoot ??
      path.join(cwd, 'artifacts', 'harness', 'instruction-root-integrity', 'latest')
  );

  await mkdir(outputRoot, { recursive: true });

  const manifestEntries = await buildSourceManifest(sourceRoots, legacyFixture);
  const verification = await verifyManifestAgainstBundle({
    manifestEntries,
    bundleRoot,
    legacyFixture
  });
  const sdkBundleRoot = path.resolve(
    args.sdkBundleRoot ?? (path.basename(bundleRoot) === 'instruction-root' ? path.dirname(bundleRoot) : bundleRoot)
  );
  const sdkBundleVerification =
    runtimeProfile === 'legacy-claude'
      ? await verifyUnpackedSdkBundle({ bundleRoot: sdkBundleRoot })
      : {
          platformPackageName: null,
          selectedPlatformPackageRoot: null,
          missingFiles: [],
          comparisons: [],
          platformPackageCandidates: []
        };
  const sourceCompleteness = buildSourceCompletenessChecklist({
    sourceRoots,
    manifestEntries,
    verification,
    legacyFixture
  });

  const status =
    verification.missingInBundle.length === 0 &&
    verification.mismatchedFiles.length === 0 &&
    verification.unexpectedBundleAgentFiles.length === 0 &&
    verification.unexpectedBundleFiles.length === 0 &&
    !['missing', 'mismatch'].includes(verification.bundleManifestStatus) &&
    sdkBundleVerification.missingFiles.length === 0
      ? 'pass'
      : 'fail';

  const gitSha = readGitSha(sourceRoots.rootFilesRoot);
  const manifest = {
    generatedAt: nowIso(),
    gitSha,
    sourceLayout: sourceRoots.sourceLayout,
    sourceRoot: sourceRoots.sourceRoot ?? null,
    sourceRoots: {
      rootFilesRoot: sourceRoots.rootFilesRoot,
      agentsRoot: sourceRoots.agentsRoot,
      docsRoot: sourceRoots.docsRoot
    },
    runtimeProfile,
    files: manifestEntries
  };

  const summary = {
    generatedAt: nowIso(),
    gitSha,
    runtimeProfile,
    sourceLayout: sourceRoots.sourceLayout,
    sourceRoot: sourceRoots.sourceRoot ?? null,
    sourceRoots: {
      rootFilesRoot: sourceRoots.rootFilesRoot,
      agentsRoot: sourceRoots.agentsRoot,
      docsRoot: sourceRoots.docsRoot
    },
    bundleRoot,
    checkedFileCount: manifestEntries.length,
    status,
    missingInBundle: verification.missingInBundle,
    mismatchedFiles: verification.mismatchedFiles,
    unexpectedBundleAgentFiles: verification.unexpectedBundleAgentFiles,
    unexpectedBundleFiles: verification.unexpectedBundleFiles,
    bundleManifestStatus: verification.bundleManifestStatus,
    comparisons: verification.comparisons,
    sourceCompleteness,
    sdkBundle: {
      status: runtimeProfile === 'legacy-claude' ? 'checked' : 'not-applicable',
      platformPackageName: sdkBundleVerification.platformPackageName,
      selectedPlatformPackageRoot: sdkBundleVerification.selectedPlatformPackageRoot,
      requiredFiles: sdkBundleVerification.comparisons,
      platformPackageCandidates: sdkBundleVerification.platformPackageCandidates,
      missingFiles: sdkBundleVerification.missingFiles
    }
  };

  await writeJson(path.join(outputRoot, 'manifest.json'), manifest);
  await writeJson(path.join(outputRoot, 'summary.json'), summary);

  log(`instruction-root integrity status: ${status}`);
  log(`checked files: ${manifestEntries.length}`);
  log(`source completeness status: ${sourceCompleteness.status}`);
  if (gitSha) {
    log(`git sha: ${gitSha}`);
  } else {
    log('git sha: unavailable');
  }
  log(`manifest: ${path.join(outputRoot, 'manifest.json')}`);
  log(`summary: ${path.join(outputRoot, 'summary.json')}`);

  if (status !== 'pass') {
    if (verification.missingInBundle.length > 0) {
      logError(`Missing in bundle (${verification.missingInBundle.length}):`);
      for (const filePath of verification.missingInBundle) {
        logError(`  - ${filePath}`);
      }
    }
    if (verification.mismatchedFiles.length > 0) {
      logError(`Hash mismatches (${verification.mismatchedFiles.length}):`);
      for (const entry of verification.mismatchedFiles) {
        logError(`  - ${entry.path}`);
      }
    }
    if (verification.unexpectedBundleAgentFiles.length > 0) {
      logError(`Unexpected bundled agent files (${verification.unexpectedBundleAgentFiles.length}):`);
      for (const filePath of verification.unexpectedBundleAgentFiles) {
        logError(`  - ${filePath}`);
      }
    }
    if (verification.unexpectedBundleFiles.length > 0) {
      logError(`Unexpected bundled instruction files (${verification.unexpectedBundleFiles.length}):`);
      for (const filePath of verification.unexpectedBundleFiles) logError(`  - ${filePath}`);
    }
    if (['missing', 'mismatch'].includes(verification.bundleManifestStatus)) {
      logError(`Instruction bundle manifest: ${verification.bundleManifestStatus}`);
    }
    if (runtimeProfile === 'legacy-claude' && sdkBundleVerification.missingFiles.length > 0) {
      logError(`Missing unpacked Claude Agent SDK files (${sdkBundleVerification.missingFiles.length}):`);
      for (const filePath of sdkBundleVerification.missingFiles) {
        logError(`  - ${filePath}`);
      }
    }

    return 1;
  }

  return 0;
}

if (process.argv[1] && path.resolve(process.argv[1]) === scriptPath) {
  process.exitCode = await run();
}
