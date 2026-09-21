import { mkdtemp, mkdir, readFile, realpath, rm, writeFile } from 'node:fs/promises';
import os from 'node:os';
import path from 'node:path';
import { afterEach, beforeEach, describe, expect, it } from 'vitest';

import {
  resolvePackagedInstructionRoot,
  run
} from '../../../scripts/verify-instruction-root-integrity.mjs';
import { preparePackagedInstructionRoot } from '../../../scripts/prepare-packaged-instruction-root.mjs';


const BASE_FIXTURE_FILES: Record<string, string> = {
  'AGENTS.md': '# agents index\n',
  'CLAUDE.md': '@AGENTS.md\n',
  'README.md': '# readme\n',
  'docs/WHAT-IS-AN-AGENT.md': '# what is an agent\n',
  'docs/DIRECTIVE.md': '# directive\n',
  'docs/CONTRACT.md': '# contract\n',
  'docs/SPEC.md': '# spec\n',
  'docs/TYPES.md': '# types\n',
  'docs/PLAN.md': '# plan\n',
  'agents/AGENT_WORKING_ITEMS.md': '# working items persona\n',
  'agents/AGENT_TASK.md': '# task persona\n'
};

const SDK_PLATFORM_PACKAGE_BY_RUNTIME: Record<string, string> = {
  'darwin:arm64': '@anthropic-ai/claude-agent-sdk-darwin-arm64',
  'darwin:x64': '@anthropic-ai/claude-agent-sdk-darwin-x64',
  'linux:arm64': '@anthropic-ai/claude-agent-sdk-linux-arm64',
  'linux:x64': '@anthropic-ai/claude-agent-sdk-linux-x64',
  'win32:arm64': '@anthropic-ai/claude-agent-sdk-win32-arm64',
  'win32:x64': '@anthropic-ai/claude-agent-sdk-win32-x64'
};

type ScriptResult = {
  code: number;
  stdout: string;
  stderr: string;
};

let tmpRoot = '';

async function writeFixture(root: string, overrides?: Record<string, string>): Promise<void> {
  const files = {
    ...BASE_FIXTURE_FILES,
    ...(overrides ?? {})
  };

  for (const [relativePath, content] of Object.entries(files)) {
    const absolutePath = path.join(root, relativePath);
    await mkdir(path.dirname(absolutePath), { recursive: true });
    await writeFile(absolutePath, content, 'utf8');
  }
}

async function writeSdkBundleFixture(bundleRoot: string): Promise<void> {
  const files: Record<string, string> = {
    'app.asar.unpacked/node_modules/@anthropic-ai/claude-agent-sdk/package.json':
      '{"name":"@anthropic-ai/claude-agent-sdk"}\n',
    'app.asar.unpacked/node_modules/@anthropic-ai/claude-agent-sdk/sdk.mjs': 'export {};\n',
    'app.asar.unpacked/node_modules/@anthropic-ai/claude-agent-sdk/manifest.json': '{}\n'
  };
  const platformPackageName =
    SDK_PLATFORM_PACKAGE_BY_RUNTIME[`${process.platform}:${process.arch}`];
  if (platformPackageName) {
    const platformPackageRoot = `app.asar.unpacked/node_modules/@anthropic-ai/claude-agent-sdk/node_modules/${platformPackageName}`;
    files[`${platformPackageRoot}/package.json`] = `{"name":"${platformPackageName}"}\n`;
    files[`${platformPackageRoot}/claude`] = '#!/bin/sh\n';
  }

  await writeFixtureFiles(bundleRoot, files);
}

async function writeFixtureFiles(root: string, files: Record<string, string>): Promise<void> {
  for (const [relativePath, content] of Object.entries(files)) {
    const absolutePath = path.join(root, relativePath);
    await mkdir(path.dirname(absolutePath), { recursive: true });
    await writeFile(absolutePath, content, 'utf8');
  }
}

async function runIntegrityScript(args: string[], cwd = process.cwd()): Promise<ScriptResult> {
  const stdout: string[] = [];
  const stderr: string[] = [];
  const code = await run(args, {
    cwd,
    legacyFixture: true,
    log: (line: string) => stdout.push(line),
    logError: (line: string) => stderr.push(line)
  });
  return { code, stdout: stdout.join('\n'), stderr: stderr.join('\n') };
}

async function runV3IntegrityScript(args: string[], cwd = process.cwd()): Promise<ScriptResult> {
  const stdout: string[] = [];
  const stderr: string[] = [];
  const code = await run(args, {
    cwd,
    log: (line: string) => stdout.push(line),
    logError: (line: string) => stderr.push(line)
  });
  return { code, stdout: stdout.join('\n'), stderr: stderr.join('\n') };
}

let previousInstructionRootEnv: string | undefined;

beforeEach(async () => {
  tmpRoot = await mkdtemp(path.join(os.tmpdir(), 'chirality-integrity-script-'));
  // The in-process runner shares this worker's environment; the script's
  // default source-root resolution consults CHIRALITY_INSTRUCTION_ROOT, so
  // shield these tests from ambient/leaked values.
  previousInstructionRootEnv = process.env.CHIRALITY_INSTRUCTION_ROOT;
  delete process.env.CHIRALITY_INSTRUCTION_ROOT;
});

afterEach(async () => {
  if (previousInstructionRootEnv === undefined) {
    delete process.env.CHIRALITY_INSTRUCTION_ROOT;
  } else {
    process.env.CHIRALITY_INSTRUCTION_ROOT = previousInstructionRootEnv;
  }
  if (tmpRoot) {
    await rm(tmpRoot, { recursive: true, force: true });
  }
  tmpRoot = '';
});

describe('verify-instruction-root-integrity script', () => {
  it('resolves the integrity check from the shared explicit candidate output', () => {
    expect(resolvePackagedInstructionRoot(
      { NODE_ENV: 'test', CHIRALITY_ELECTRON_OUTPUT_DIRECTORY: '/private/tmp/chirality candidate' },
      '/frontend'
    )).toBe('/private/tmp/chirality candidate/mac-arm64/Chirality.app/Contents/Resources/instruction-root');
    expect(() => resolvePackagedInstructionRoot(
      { NODE_ENV: 'test', CHIRALITY_ELECTRON_OUTPUT_DIRECTORY: '' },
      '/frontend'
    )).toThrow('must be a normalized absolute path');
  });

  // Full-library filesystem checks measure correctness, not a five-second latency budget.
  it('validates the complete v3 bundle and rejects omissions and unexpected files', async () => {
    const repoRoot = path.resolve(process.cwd(), '..', '..', '..');
    const resourcesRoot = path.join(tmpRoot, 'resources');
    const bundleRoot = path.join(resourcesRoot, 'instruction-root');
    await preparePackagedInstructionRoot({
      sourceRoot: repoRoot,
      docsRoot: path.join(repoRoot, 'docs'),
      outputRoot: bundleRoot
    });
    await writeSdkBundleFixture(resourcesRoot);
    const args = [
      '--source-root', repoRoot,
      '--bundle-root', bundleRoot,
      '--sdk-bundle-root', resourcesRoot,
      '--output-root', path.join(tmpRoot, 'v3-output')
    ];
    const initial = await runV3IntegrityScript(args);
    expect(initial, initial.stderr).toMatchObject({ code: 0 });
    const v3Summary = JSON.parse(await readFile(path.join(tmpRoot, 'v3-output', 'summary.json'), 'utf8'));
    expect(v3Summary.sourceCompleteness.status).toBe('needs_remediation');
    expect(v3Summary.sourceCompleteness.rows).toEqual(
      expect.arrayContaining([
        expect.objectContaining({ id: 'KG-001-tools-registry', status: 'remediation_required' }),
        expect.objectContaining({ id: 'KG-001-examples', status: 'remediation_required' })
      ])
    );

    await writeFixtureFiles(bundleRoot, { 'workflows/unexpected.txt': 'unexpected\n' });
    const unexpected = await runV3IntegrityScript(args);
    expect(unexpected.code).toBe(1);
    expect(unexpected.stderr).toContain('Unexpected bundled instruction files');
    await rm(path.join(bundleRoot, 'workflows/unexpected.txt'));

    await rm(path.join(bundleRoot, 'agents/AGENT_TASK.md'));
    const omitted = await runV3IntegrityScript(args);
    expect(omitted.code).toBe(1);
    expect(omitted.stderr).toContain('Missing in bundle');
  }, 15_000);

  it('passes when bundled files match source hashes', async () => {
    const sourceRoot = path.join(tmpRoot, 'source-root');
    const bundleRoot = path.join(tmpRoot, 'bundle-root');
    const outputRoot = path.join(tmpRoot, 'output');

    await writeFixture(sourceRoot);
    await writeFixture(bundleRoot);
    await writeSdkBundleFixture(bundleRoot);

    const result = await runIntegrityScript([
      '--source-root',
      sourceRoot,
      '--bundle-root',
      bundleRoot,
      '--output-root',
      outputRoot
    ]);

    expect(result.code).toBe(0);
    expect(result.stdout).toContain('instruction-root integrity status: pass');

    const summaryRaw = await readFile(path.join(outputRoot, 'summary.json'), 'utf8');
    const summary = JSON.parse(summaryRaw) as {
      status: string;
      checkedFileCount: number;
      missingInBundle: string[];
      mismatchedFiles: Array<{ path: string }>;
      unexpectedBundleAgentFiles: string[];
      sourceCompleteness: {
        status: string;
        rows: Array<{
          id: string;
          status: string;
          remediationStatus: string;
        }>;
      };
      sdkBundle: {
        missingFiles: string[];
        selectedPlatformPackageRoot: string | null;
      };
    };

    expect(summary.status).toBe('pass');
    expect(summary.checkedFileCount).toBe(11);
    expect(summary.missingInBundle).toHaveLength(0);
    expect(summary.mismatchedFiles).toHaveLength(0);
    expect(summary.unexpectedBundleAgentFiles).toHaveLength(0);
    expect(summary.sourceCompleteness.status).toBe('needs_remediation');
    expect(summary.sourceCompleteness.rows).toEqual(
      expect.arrayContaining([
        expect.objectContaining({
          id: 'SOW-073-OI-004-required-instruction-root-assets',
          status: 'satisfied',
          remediationStatus: 'not_required'
        }),
        expect.objectContaining({
          id: 'KG-001-tools-registry',
          status: 'remediation_required',
          remediationStatus: 'required'
        }),
        expect.objectContaining({
          id: 'KG-001-examples',
          status: 'remediation_required',
          remediationStatus: 'required'
        })
      ])
    );
    expect(summary.sdkBundle).toMatchObject({ status: 'not-applicable', missingFiles: [] });
  });

  it('fails when bundled content diverges from source', async () => {
    const sourceRoot = path.join(tmpRoot, 'source-root');
    const bundleRoot = path.join(tmpRoot, 'bundle-root');
    const outputRoot = path.join(tmpRoot, 'output');

    await writeFixture(sourceRoot);
    await writeFixture(bundleRoot, {
      'agents/AGENT_TASK.md': '# task persona (modified)\n'
    });
    await writeSdkBundleFixture(bundleRoot);

    const result = await runIntegrityScript([
      '--source-root',
      sourceRoot,
      '--bundle-root',
      bundleRoot,
      '--output-root',
      outputRoot
    ]);

    expect(result.code).toBe(1);
    expect(result.stdout).toContain('instruction-root integrity status: fail');

    const summaryRaw = await readFile(path.join(outputRoot, 'summary.json'), 'utf8');
    const summary = JSON.parse(summaryRaw) as {
      status: string;
      mismatchedFiles: Array<{ path: string }>;
    };

    expect(summary.status).toBe('fail');
    expect(summary.mismatchedFiles).toEqual(
      expect.arrayContaining([
        expect.objectContaining({
          path: 'agents/AGENT_TASK.md'
        })
      ])
    );
  });

  it('reports source-completeness remediation state for SOW-073 and OI-004 candidates', async () => {
    const sourceRoot = path.join(tmpRoot, 'source-root');
    const bundleRoot = path.join(tmpRoot, 'bundle-root');
    const outputRoot = path.join(tmpRoot, 'output');

    await writeFixture(sourceRoot, {
      'tools/REGISTRY.md': '# registry\n',
      'examples/README.md': '# examples\n'
    });
    await writeFixture(bundleRoot);
    await writeSdkBundleFixture(bundleRoot);

    const result = await runIntegrityScript([
      '--source-root',
      sourceRoot,
      '--bundle-root',
      bundleRoot,
      '--output-root',
      outputRoot
    ]);

    expect(result.code).toBe(0);
    expect(result.stdout).toContain('source completeness status: pass');

    const summaryRaw = await readFile(path.join(outputRoot, 'summary.json'), 'utf8');
    const summary = JSON.parse(summaryRaw) as {
      sourceCompleteness: {
        status: string;
        rows: Array<{
          id: string;
          status: string;
          remediationStatus: string;
        }>;
      };
    };

    expect(summary.sourceCompleteness.status).toBe('pass');
    expect(summary.sourceCompleteness.rows).toEqual(
      expect.arrayContaining([
        expect.objectContaining({
          id: 'SOW-073-OI-004-required-instruction-root-assets',
          status: 'satisfied',
          remediationStatus: 'not_required'
        }),
        expect.objectContaining({
          id: 'KG-001-tools-registry',
          status: 'satisfied',
          remediationStatus: 'not_required'
        }),
        expect.objectContaining({
          id: 'KG-001-examples',
          status: 'satisfied',
          remediationStatus: 'not_required'
        })
      ])
    );
  });

  it('preserves the explicit historical Claude SDK proof path', async () => {
    const sourceRoot = path.join(tmpRoot, 'source-root');
    const bundleRoot = path.join(tmpRoot, 'bundle-root');
    const outputRoot = path.join(tmpRoot, 'output');

    await writeFixture(sourceRoot);
    await writeFixture(bundleRoot);

    const result = await runIntegrityScript([
      '--source-root',
      sourceRoot,
      '--bundle-root',
      bundleRoot,
      '--output-root',
      outputRoot,
      '--runtime-profile',
      'legacy-claude'
    ]);

    expect(result.code).toBe(1);
    expect(result.stderr).toContain('Missing unpacked Claude Agent SDK files');

    const summaryRaw = await readFile(path.join(outputRoot, 'summary.json'), 'utf8');
    const summary = JSON.parse(summaryRaw) as {
      status: string;
      runtimeProfile: string;
      sdkBundle: {
        status: string;
        missingFiles: string[];
      };
    };

    expect(summary.status).toBe('fail');
    expect(summary.runtimeProfile).toBe('legacy-claude');
    expect(summary.sdkBundle.status).toBe('checked');
    expect(summary.sdkBundle.missingFiles).toEqual(
      expect.arrayContaining([
        'app.asar.unpacked/node_modules/@anthropic-ai/claude-agent-sdk/package.json',
        'app.asar.unpacked/node_modules/@anthropic-ai/claude-agent-sdk/sdk.mjs'
      ])
    );
  });

  it('supports split source roots for monorepo instruction packages', async () => {
    const rootFilesRoot = path.join(tmpRoot, 'monorepo-root');
    const agentsRoot = path.join(rootFilesRoot, 'agents');
    const docsRoot = path.join(tmpRoot, 'app-dev', 'docs');
    const bundleRoot = path.join(tmpRoot, 'bundle-root');
    const outputRoot = path.join(tmpRoot, 'output');

    await writeFixtureFiles(rootFilesRoot, {
      'AGENTS.md': BASE_FIXTURE_FILES['AGENTS.md'],
      'CLAUDE.md': BASE_FIXTURE_FILES['CLAUDE.md'],
      'README.md': BASE_FIXTURE_FILES['README.md']
    });
    await writeFixtureFiles(agentsRoot, {
      'AGENT_WORKING_ITEMS.md': BASE_FIXTURE_FILES['agents/AGENT_WORKING_ITEMS.md'],
      'AGENT_TASK.md': BASE_FIXTURE_FILES['agents/AGENT_TASK.md']
    });
    await writeFixtureFiles(docsRoot, {
      'WHAT-IS-AN-AGENT.md': BASE_FIXTURE_FILES['docs/WHAT-IS-AN-AGENT.md'],
      'DIRECTIVE.md': BASE_FIXTURE_FILES['docs/DIRECTIVE.md'],
      'CONTRACT.md': BASE_FIXTURE_FILES['docs/CONTRACT.md'],
      'SPEC.md': BASE_FIXTURE_FILES['docs/SPEC.md'],
      'TYPES.md': BASE_FIXTURE_FILES['docs/TYPES.md'],
      'PLAN.md': BASE_FIXTURE_FILES['docs/PLAN.md']
    });
    await writeFixture(bundleRoot);
    await writeSdkBundleFixture(bundleRoot);

    const result = await runIntegrityScript([
      '--root-files-root',
      rootFilesRoot,
      '--agents-root',
      agentsRoot,
      '--docs-root',
      docsRoot,
      '--bundle-root',
      bundleRoot,
      '--output-root',
      outputRoot
    ]);

    expect(result.code).toBe(0);
    expect(result.stdout).toContain('instruction-root integrity status: pass');

    const summaryRaw = await readFile(path.join(outputRoot, 'summary.json'), 'utf8');
    const summary = JSON.parse(summaryRaw) as {
      sourceLayout: string;
      sourceRoot: string | null;
      sourceRoots: {
        rootFilesRoot: string;
        agentsRoot: string;
        docsRoot: string;
      };
      status: string;
      checkedFileCount: number;
    };

    expect(summary.status).toBe('pass');
    expect(summary.sourceLayout).toBe('split');
    expect(summary.sourceRoot).toBeNull();
    expect(summary.sourceRoots).toEqual({
      rootFilesRoot: path.resolve(rootFilesRoot),
      agentsRoot: path.resolve(agentsRoot),
      docsRoot: path.resolve(docsRoot)
    });
    expect(summary.checkedFileCount).toBe(11);
  });

  it('auto-detects split source roots from the app-dev frontend workspace', async () => {
    const monorepoRoot = path.join(tmpRoot, 'monorepo-root');
    const agentsRoot = path.join(monorepoRoot, 'agents');
    const appDevRoot = path.join(monorepoRoot, 'projects', 'chirality-app-dev');
    const frontendCwd = path.join(appDevRoot, 'frontend');
    const docsRoot = path.join(monorepoRoot, 'docs');
    const bundleRoot = path.join(tmpRoot, 'bundle-root');
    const outputRoot = path.join(tmpRoot, 'output');

    await mkdir(frontendCwd, { recursive: true });
    await writeFixtureFiles(monorepoRoot, {
      'AGENTS.md': BASE_FIXTURE_FILES['AGENTS.md'],
      'CLAUDE.md': BASE_FIXTURE_FILES['CLAUDE.md'],
      'README.md': BASE_FIXTURE_FILES['README.md']
    });
    await writeFixtureFiles(agentsRoot, {
      'AGENT_WORKING_ITEMS.md': BASE_FIXTURE_FILES['agents/AGENT_WORKING_ITEMS.md'],
      'AGENT_TASK.md': BASE_FIXTURE_FILES['agents/AGENT_TASK.md']
    });
    await writeFixtureFiles(docsRoot, {
      'WHAT-IS-AN-AGENT.md': BASE_FIXTURE_FILES['docs/WHAT-IS-AN-AGENT.md'],
      'DIRECTIVE.md': BASE_FIXTURE_FILES['docs/DIRECTIVE.md'],
      'CONTRACT.md': BASE_FIXTURE_FILES['docs/CONTRACT.md'],
      'SPEC.md': BASE_FIXTURE_FILES['docs/SPEC.md'],
      'TYPES.md': BASE_FIXTURE_FILES['docs/TYPES.md'],
      'PLAN.md': BASE_FIXTURE_FILES['docs/PLAN.md']
    });
    await writeFixture(bundleRoot);
    await writeSdkBundleFixture(bundleRoot);

    // The spawned script's process.cwd() was realpath-normalized by the OS;
    // the in-process runner receives cwd verbatim, so normalize it here to
    // keep the realpath-based expectations below.
    const result = await runIntegrityScript(
      ['--bundle-root', bundleRoot, '--output-root', outputRoot],
      await realpath(frontendCwd)
    );

    expect(result.code).toBe(0);
    expect(result.stdout).toContain('instruction-root integrity status: pass');

    const summaryRaw = await readFile(path.join(outputRoot, 'summary.json'), 'utf8');
    const summary = JSON.parse(summaryRaw) as {
      sourceLayout: string;
      sourceRoot: string | null;
      sourceRoots: {
        rootFilesRoot: string;
        agentsRoot: string;
        docsRoot: string;
      };
      status: string;
    };

    expect(summary.status).toBe('pass');
    expect(summary.sourceLayout).toBe('split');
    expect(summary.sourceRoot).toBeNull();
    expect(summary.sourceRoots).toEqual({
      rootFilesRoot: await realpath(monorepoRoot),
      agentsRoot: await realpath(agentsRoot),
      docsRoot: await realpath(docsRoot)
    });
  });
});
