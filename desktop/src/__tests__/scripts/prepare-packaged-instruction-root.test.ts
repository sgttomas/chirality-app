import { cp, mkdtemp, mkdir, readFile, rm, symlink, writeFile } from 'node:fs/promises';
import os from 'node:os';
import path from 'node:path';
import { afterEach, beforeEach, describe, expect, it } from 'vitest';

import {
  BUNDLE_MANIFEST,
  DOC_FILES,
  PRODUCT_AGENTS_SOURCE,
  ROLE_IDS,
  preparePackagedInstructionRoot
} from '../../../scripts/prepare-packaged-instruction-root.mjs';

const REPO_ROOT = path.resolve(process.cwd(), '..', '..', '..');
let temporaryRoot = '';

beforeEach(async () => {
  temporaryRoot = await mkdtemp(path.join(os.tmpdir(), 'chirality-packaged-instructions-'));
});

afterEach(async () => {
  await rm(temporaryRoot, { recursive: true, force: true });
});

describe('prepare packaged instruction root', () => {
  // Full-library filesystem checks measure correctness, not a five-second latency budget.
  it('stages the exact four-role, workflow, skill, compatibility, and tool closure', async () => {
    const outputRoot = path.join(temporaryRoot, 'instruction-root');
    await preparePackagedInstructionRoot({
      sourceRoot: REPO_ROOT,
      docsRoot: path.join(REPO_ROOT, 'docs'),
      outputRoot
    });

    const registry = JSON.parse(await readFile(path.join(outputRoot, 'agents/registry.json'), 'utf8'));
    const productGuidance = await readFile(path.join(REPO_ROOT, PRODUCT_AGENTS_SOURCE), 'utf8');
    expect(await readFile(path.join(outputRoot, 'AGENTS.md'), 'utf8')).toBe(productGuidance);
    expect(productGuidance).not.toBe(await readFile(path.join(REPO_ROOT, 'AGENTS.md'), 'utf8'));
    expect(Object.keys(registry.roles).sort()).toEqual([...ROLE_IDS].sort());
    for (const roleId of ROLE_IDS) {
      expect(await readFile(path.join(outputRoot, `agents/AGENT_${roleId}.md`), 'utf8')).toBe(
        await readFile(path.join(REPO_ROOT, `agents/AGENT_${roleId}.md`), 'utf8')
      );
    }
    for (const doc of DOC_FILES) {
      expect(await readFile(path.join(outputRoot, 'docs', doc), 'utf8')).toBe(
        await readFile(path.join(REPO_ROOT, 'docs', doc), 'utf8')
      );
    }

    const index = JSON.parse(await readFile(path.join(outputRoot, 'workflows/index.json'), 'utf8'));
    expect(index.schema).toBe('chirality-method-index/v1');
    expect(index.methods).not.toEqual(
      expect.arrayContaining([expect.objectContaining({ kind: 'skill', name: 'chirality-change' })])
    );
    expect(await readFile(path.join(outputRoot, 'workflows/legacy-agents.json'), 'utf8')).toBeTruthy();
    expect(await readFile(path.join(outputRoot, 'workflows/legacy-methods.json'), 'utf8')).toBeTruthy();
    await expect(readFile(path.join(outputRoot, '.agents/skills/chirality-change/SKILL.md'), 'utf8')).rejects.toThrow();

    const manifest = JSON.parse(await readFile(path.join(outputRoot, BUNDLE_MANIFEST), 'utf8'));
    expect(manifest.schema).toBe('chirality-instruction-bundle-manifest/v2');
    expect(manifest.documentationClosure).toEqual({
      rule: 'direct-root-doc-references-from-bundled-entry-roles-workflows-and-skills',
      files: DOC_FILES.map((entry) => `docs/${entry}`)
    });
    expect(manifest.toolMembersSemantics).toContain('packaged dependency bytes only');
    expect(manifest.skills).toEqual(
      expect.arrayContaining([
        expect.objectContaining({
          name: 'researcher',
          toolMembers: expect.arrayContaining([
            'tools/retrieval/query_source_index.py',
            'tools/source_catalog/source_database.py'
          ]),
          externalPrerequisites: expect.arrayContaining([
            { name: 'python3', condition: 'required' },
            { name: 'numpy', condition: 'required by query_source_index.py' }
          ])
        }),
        expect.objectContaining({
          name: 'preparation',
          externalPrerequisites: expect.arrayContaining([
            { name: 'zsh', condition: 'required by the packaged scaffolding and validation shell helpers' },
            { name: 'git', condition: 'required by write_status.sh for governed transitions inside a Git repository' },
            { name: 'PyYAML', condition: 'required by write_status.sh when checking Root execution policy' }
          ])
        }),
        expect.objectContaining({
          name: 'software-code-review',
          toolMembers: [
            'tools/software_workflow/select_affected_checks.py',
            'tools/software_workflow/software_workflow_common.py',
            'tools/software_workflow/validate_change_scope.py',
            'tools/software_workflow/compare_structured.py',
            'tools/software_workflow/verify_generated_manifest.py'
          ],
          externalPrerequisites: expect.arrayContaining([
            { name: 'git', condition: 'required by validate_change_scope.py when changed paths are not supplied explicitly' }
          ])
        }),
        expect.objectContaining({
          name: 'software-defect-diagnosis',
          toolMembers: [
            'tools/software_workflow/discover_repository.py',
            'tools/software_workflow/select_affected_checks.py',
            'tools/software_workflow/software_workflow_common.py',
            'tools/software_workflow/run_registered_checks.py'
          ],
          externalPrerequisites: expect.arrayContaining([
            {
              name: 'project-registered check toolchains',
              condition: 'required only for commands selected and executed by run_registered_checks.py'
            }
          ])
        })
      ])
    );
    for (const file of manifest.files) {
      await expect(readFile(path.join(outputRoot, file.path))).resolves.toBeTruthy();
    }
  }, 15_000);

  it('clears stale files before rebuilding', async () => {
    const outputRoot = path.join(temporaryRoot, 'instruction-root');
    await mkdir(outputRoot, { recursive: true });
    await writeFile(path.join(outputRoot, 'stale.txt'), 'stale\n');
    await preparePackagedInstructionRoot({
      sourceRoot: REPO_ROOT,
      docsRoot: path.join(REPO_ROOT, 'docs'),
      outputRoot
    });
    await expect(readFile(path.join(outputRoot, 'stale.txt'), 'utf8')).rejects.toThrow();
  });

  it('rejects destructive output overlap and symlinked canonical members', async () => {
    await expect(
      preparePackagedInstructionRoot({
        sourceRoot: REPO_ROOT,
        docsRoot: path.join(REPO_ROOT, 'docs'),
        outputRoot: REPO_ROOT
      })
    ).rejects.toThrow('must not equal or contain source-root');

    const sourceRoot = path.join(temporaryRoot, 'source');
    await cp(REPO_ROOT, sourceRoot, {
      recursive: true,
      filter: (source) => {
        const relative = path.relative(REPO_ROOT, source);
        return !relative || ['AGENTS.md', 'CLAUDE.md', 'README.md', 'agents', 'docs', 'workflows', '.agents', 'tools'].includes(relative.split(path.sep)[0])
          || relative === 'projects' || relative === path.join('projects', 'chirality-app-dev')
          || relative === path.join('projects', 'chirality-app-dev', 'instructions')
          || relative.startsWith(path.join('projects', 'chirality-app-dev', 'instructions') + path.sep);
      }
    });
    for (const protectedDirectory of ['agents', 'workflows']) {
      const sentinel = path.join(sourceRoot, protectedDirectory, 'preserved-source.txt');
      await writeFile(sentinel, 'preserve\n');
      await expect(
        preparePackagedInstructionRoot({
          sourceRoot,
          docsRoot: path.join(sourceRoot, 'docs'),
          outputRoot: path.join(sourceRoot, protectedDirectory, 'generated-bundle')
        })
      ).rejects.toThrow('must not overlap a canonical instruction source root');
      await expect(readFile(sentinel, 'utf8')).resolves.toBe('preserve\n');
    }
    await expect(
      preparePackagedInstructionRoot({
        sourceRoot,
        docsRoot: path.join(sourceRoot, 'docs'),
        outputRoot: path.join(sourceRoot, 'node_modules', '.cache', 'instruction-root')
      })
    ).resolves.toBeTruthy();

    const sourceAlias = path.join(temporaryRoot, 'source-alias');
    await symlink(sourceRoot, sourceAlias, 'dir');
    await expect(
      preparePackagedInstructionRoot({
        sourceRoot: sourceAlias,
        docsRoot: path.join(sourceAlias, 'docs'),
        outputRoot: path.join(temporaryRoot, 'source-alias-output')
      })
    ).rejects.toThrow('source root must not be a symlink');

    const externalAgents = path.join(temporaryRoot, 'external-agents');
    await cp(path.join(sourceRoot, 'agents'), externalAgents, { recursive: true });
    const externalAgentBytes = await readFile(path.join(externalAgents, 'AGENT_TASK.md'), 'utf8');
    await rm(path.join(sourceRoot, 'agents'), { recursive: true });
    await symlink(externalAgents, path.join(sourceRoot, 'agents'), 'dir');
    await expect(
      preparePackagedInstructionRoot({
        sourceRoot,
        docsRoot: path.join(sourceRoot, 'docs'),
        outputRoot: path.join(temporaryRoot, 'directory-root-output')
      })
    ).rejects.toThrow('agents source root must not traverse a symlink');
    await expect(readFile(path.join(externalAgents, 'AGENT_TASK.md'), 'utf8')).resolves.toBe(externalAgentBytes);
    await rm(path.join(sourceRoot, 'agents'));
    await cp(externalAgents, path.join(sourceRoot, 'agents'), { recursive: true });

    const softwareRoot = path.join(sourceRoot, 'tools', 'software_workflow');
    const externalSoftwareRoot = path.join(temporaryRoot, 'external-software-workflow');
    await cp(softwareRoot, externalSoftwareRoot, { recursive: true });
    await rm(softwareRoot, { recursive: true });
    await symlink(externalSoftwareRoot, softwareRoot, 'dir');
    await expect(
      preparePackagedInstructionRoot({
        sourceRoot,
        docsRoot: path.join(sourceRoot, 'docs'),
        outputRoot: path.join(temporaryRoot, 'intermediate-link-output')
      })
    ).rejects.toThrow('Instruction resource must not traverse a symlink');
    await rm(softwareRoot);
    await cp(externalSoftwareRoot, softwareRoot, { recursive: true });

    const outputAlias = path.join(temporaryRoot, 'output-alias');
    await symlink(path.join(sourceRoot, 'agents'), outputAlias, 'dir');
    await expect(
      preparePackagedInstructionRoot({
        sourceRoot,
        docsRoot: path.join(sourceRoot, 'docs'),
        outputRoot: outputAlias
      })
    ).rejects.toThrow('must not overlap a canonical instruction source root');
    await expect(readFile(path.join(sourceRoot, 'agents', 'AGENT_TASK.md'), 'utf8')).resolves.toBe(externalAgentBytes);

    const unexpectedSkill = path.join(sourceRoot, '.agents', 'skills', 'unexpected-skill');
    await mkdir(unexpectedSkill, { recursive: true });
    await writeFile(path.join(unexpectedSkill, 'SKILL.md'), '# unexpected\n');
    await expect(
      preparePackagedInstructionRoot({
        sourceRoot,
        docsRoot: path.join(sourceRoot, 'docs'),
        outputRoot: path.join(temporaryRoot, 'unexpected-output')
      })
    ).rejects.toThrow('Canonical skill membership mismatch');
    await rm(unexpectedSkill, { recursive: true });

    const missingSkill = path.join(sourceRoot, '.agents', 'skills', 'proposal-format');
    await rm(missingSkill, { recursive: true });
    await expect(
      preparePackagedInstructionRoot({
        sourceRoot,
        docsRoot: path.join(sourceRoot, 'docs'),
        outputRoot: path.join(temporaryRoot, 'missing-output')
      })
    ).rejects.toThrow('Canonical skill membership mismatch');
    await cp(path.join(REPO_ROOT, '.agents', 'skills', 'proposal-format'), missingSkill, { recursive: true });

    const target = path.join(sourceRoot, 'agents', 'AGENT_TASK.md');
    await rm(target);
    await symlink(path.join(REPO_ROOT, 'agents', 'AGENT_TASK.md'), target);
    await expect(
      preparePackagedInstructionRoot({
        sourceRoot,
        docsRoot: path.join(sourceRoot, 'docs'),
        outputRoot: path.join(temporaryRoot, 'symlink-output')
      })
    ).rejects.toThrow('must not traverse a symlink');
  });
});
