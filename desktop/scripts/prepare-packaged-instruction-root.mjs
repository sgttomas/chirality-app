#!/usr/bin/env node

import { createHash } from 'node:crypto';
import { cp, lstat, mkdir, readdir, readFile, realpath, rm, stat, writeFile } from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const scriptPath = fileURLToPath(import.meta.url);

export const ROLE_IDS = ['HELP_HUMAN', 'HELPS_HUMANS', 'WORKING_ITEMS', 'TASK'];
export const ROOT_FILES = ['AGENTS.md', 'CLAUDE.md', 'README.md'];
export const PRODUCT_AGENTS_SOURCE = 'projects/chirality-app-dev/instructions/AGENTS.md';
export const DOC_FILES = [
  'DIRECTIVE.md',
  'CONTRACT.md',
  'SPEC.md',
  'TYPES.md',
  'WORKFLOW_COMPONENT_STANDARD.md',
  'AGENT_WORKFLOW_RUNTIME.md',
  'DECOMPOSITION_STANDARD.md',
  'DELIVERABLE_SCOPE_OF_WORK_STANDARD.md',
  'PRD_ROOT.md',
  'SOFTWARE_WORKFLOW_PROFILE.md',
  'rubrics/AUDIT_AGENT.md',
  'templates/MEMORY_TEMPLATE.md'
];
export const WORKFLOW_METADATA_FILES = [
  'catalog.yaml',
  'catalog.schema.json',
  'index.json',
  'legacy-agents.json',
  'legacy-methods.json'
];
export const TOOL_FILES = [
  'scaffolding/scaffold_package.sh',
  'scaffolding/scaffold_deliverable.sh',
  'scaffolding/scaffold_tool_root.sh',
  'scaffolding/write_status.sh',
  'validation/check_min_viable_fileset.sh',
  'validation/validate_id_format.sh',
  'validation/scan_deliverable_consistency.py',
  'scope_of_work/common.py',
  'retrieval/scaffold_research_packet.py',
  'retrieval/query_source_index.py',
  'source_catalog/check_snapshot_freshness.py',
  'source_catalog/source_database.py',
  'source_catalog/research_packet.py',
  'software_workflow/compare_structured.py',
  'software_workflow/discover_repository.py',
  'software_workflow/run_registered_checks.py',
  'software_workflow/select_affected_checks.py',
  'software_workflow/software_workflow_common.py',
  'software_workflow/validate_change_scope.py',
  'software_workflow/verify_generated_manifest.py'
];
export const EXCLUDED_BUNDLED_SKILLS = new Set(['chirality-change']);
export const BUNDLED_SKILL_NAMES = [
  'deliverable-consistency',
  'drawing-titleblock-page',
  'preparation',
  'proposal-format',
  'researcher',
  'software-code-review',
  'software-defect-diagnosis'
];
export const BUNDLE_MANIFEST = 'instruction-bundle-manifest.json';

export const SKILL_TOOL_CLOSURE = {
  preparation: {
    toolMembers: TOOL_FILES.filter((entry) => entry.startsWith('scaffolding/') || entry.startsWith('validation/check_') || entry.startsWith('validation/validate_id_')),
    externalPrerequisites: [
      { name: 'zsh', condition: 'required by the packaged scaffolding and validation shell helpers' },
      { name: 'git', condition: 'required by write_status.sh for governed transitions inside a Git repository' },
      { name: 'python3', condition: 'required by write_status.sh when checking Root execution policy' },
      { name: 'PyYAML', condition: 'required by write_status.sh when checking Root execution policy' }
    ]
  },
  'deliverable-consistency': {
    toolMembers: ['validation/scan_deliverable_consistency.py', 'scope_of_work/common.py'],
    externalPrerequisites: [{ name: 'python3', condition: 'required' }]
  },
  researcher: {
    toolMembers: TOOL_FILES.filter((entry) => entry.startsWith('retrieval/') || entry.startsWith('source_catalog/')),
    externalPrerequisites: [
      { name: 'python3', condition: 'required' },
      { name: 'numpy', condition: 'required by query_source_index.py' }
    ]
  },
  'software-code-review': {
    toolMembers: [
      'software_workflow/select_affected_checks.py',
      'software_workflow/software_workflow_common.py',
      'software_workflow/validate_change_scope.py',
      'software_workflow/compare_structured.py',
      'software_workflow/verify_generated_manifest.py'
    ],
    externalPrerequisites: [
      { name: 'python3', condition: 'required' },
      { name: 'git', condition: 'required by validate_change_scope.py when changed paths are not supplied explicitly' }
    ]
  },
  'software-defect-diagnosis': {
    toolMembers: [
      'software_workflow/discover_repository.py',
      'software_workflow/select_affected_checks.py',
      'software_workflow/software_workflow_common.py',
      'software_workflow/run_registered_checks.py'
    ],
    externalPrerequisites: [
      { name: 'python3', condition: 'required' },
      {
        name: 'project-registered check toolchains',
        condition: 'required only for commands selected and executed by run_registered_checks.py'
      }
    ]
  }
};

function toPosix(value) {
  return value.split(path.sep).join('/');
}

function assertPlainName(value, label) {
  if (typeof value !== 'string' || !/^[a-z0-9][a-z0-9-]{0,63}$/u.test(value)) {
    throw new Error(`Invalid ${label}: ${String(value)}`);
  }
}

async function resolvePotentialPath(value) {
  let cursor = path.resolve(value);
  const suffix = [];
  while (true) {
    try {
      return path.join(await realpath(cursor), ...suffix.reverse());
    } catch (error) {
      if (error?.code !== 'ENOENT') throw error;
      const parent = path.dirname(cursor);
      if (parent === cursor) throw error;
      suffix.push(path.basename(cursor));
      cursor = parent;
    }
  }
}

async function requireContainedDirectory(sourceRoot, candidate, label) {
  const lexicalSourceRoot = path.resolve(sourceRoot);
  const lexicalCandidate = path.resolve(candidate);
  if ((await lstat(lexicalSourceRoot)).isSymbolicLink()) {
    throw new Error(`Canonical ${label} source root must not be a symlink: ${sourceRoot}`);
  }
  const relative = path.relative(lexicalSourceRoot, lexicalCandidate);
  if (relative === '..' || relative.startsWith(`..${path.sep}`) || path.isAbsolute(relative)) {
    throw new Error(`Canonical ${label} source root escapes source-root: ${candidate}`);
  }
  let cursor = lexicalSourceRoot;
  for (const segment of relative.split(path.sep).filter(Boolean)) {
    cursor = path.join(cursor, segment);
    if ((await lstat(cursor)).isSymbolicLink()) {
      throw new Error(`Canonical ${label} source root must not traverse a symlink: ${candidate}`);
    }
  }
  const canonicalSourceRoot = await realpath(lexicalSourceRoot);
  const canonicalCandidate = await realpath(lexicalCandidate);
  if (
    canonicalCandidate !== canonicalSourceRoot &&
    !canonicalCandidate.startsWith(`${canonicalSourceRoot}${path.sep}`)
  ) {
    throw new Error(`Canonical ${label} source root escapes source-root: ${candidate}`);
  }
  if (!(await stat(canonicalCandidate)).isDirectory()) {
    throw new Error(`Canonical ${label} source root is not a directory: ${candidate}`);
  }
  return canonicalCandidate;
}

async function requireContainedFile(root, relativePath) {
  if (
    typeof relativePath !== 'string' ||
    !relativePath ||
    path.isAbsolute(relativePath) ||
    relativePath.split(/[\\/]/u).includes('..')
  ) {
    throw new Error(`Invalid instruction resource path: ${String(relativePath)}`);
  }
  const canonicalRoot = await realpath(root);
  const candidate = path.resolve(root, relativePath);
  let current = path.resolve(root);
  for (const segment of relativePath.split(/[\\/]/u)) {
    current = path.join(current, segment);
    if ((await lstat(current)).isSymbolicLink()) {
      throw new Error(`Instruction resource must not traverse a symlink: ${relativePath}`);
    }
  }
  const canonicalCandidate = await realpath(candidate);
  if (
    canonicalCandidate !== canonicalRoot &&
    !canonicalCandidate.startsWith(`${canonicalRoot}${path.sep}`)
  ) {
    throw new Error(`Instruction resource escapes its source root: ${relativePath}`);
  }
  if (!(await stat(canonicalCandidate)).isFile()) {
    throw new Error(`Instruction resource is not a file: ${relativePath}`);
  }
  return canonicalCandidate;
}

async function listFiles(root) {
  const files = [];
  async function visit(directory, prefix = '') {
    for (const entry of await readdir(directory, { withFileTypes: true })) {
      const relativePath = prefix ? `${prefix}/${entry.name}` : entry.name;
      if (entry.isDirectory()) {
        await visit(path.join(directory, entry.name), relativePath);
      } else if (entry.isFile()) {
        files.push(relativePath);
      } else {
        throw new Error(`Unsupported instruction source entry: ${relativePath}`);
      }
    }
  }
  await visit(root);
  return files.sort();
}

function filteredIndex(index) {
  if (index?.schema !== 'chirality-method-index/v1' || !Array.isArray(index.methods)) {
    throw new Error('workflows/index.json must use chirality-method-index/v1');
  }
  const methods = index.methods.filter(
    (entry) => !(entry?.kind === 'skill' && EXCLUDED_BUNDLED_SKILLS.has(entry.name))
  );
  return { value: { ...index, methods }, changed: methods.length !== index.methods.length };
}

export async function buildExpectedInstructionManifest({
  rootFilesRoot,
  agentsRoot,
  docsRoot,
  workflowsRoot = path.join(rootFilesRoot, 'workflows'),
  skillsRoot = path.join(rootFilesRoot, '.agents', 'skills'),
  toolsRoot = path.join(rootFilesRoot, 'tools')
}) {
  const lexicalRootFilesRoot = rootFilesRoot;
  const canonicalRootFilesRoot = await requireContainedDirectory(
    lexicalRootFilesRoot,
    lexicalRootFilesRoot,
    'root-files'
  );
  agentsRoot = await requireContainedDirectory(lexicalRootFilesRoot, agentsRoot, 'agents');
  docsRoot = await requireContainedDirectory(lexicalRootFilesRoot, docsRoot, 'docs');
  workflowsRoot = await requireContainedDirectory(lexicalRootFilesRoot, workflowsRoot, 'workflows');
  skillsRoot = await requireContainedDirectory(lexicalRootFilesRoot, skillsRoot, 'skills');
  toolsRoot = await requireContainedDirectory(lexicalRootFilesRoot, toolsRoot, 'tools');
  rootFilesRoot = canonicalRootFilesRoot;
  const entries = [];
  const add = async (bundlePath, sourceRoot, sourcePath = bundlePath) => {
    entries.push({
      bundlePath: toPosix(bundlePath),
      sourcePath: await requireContainedFile(sourceRoot, sourcePath)
    });
  };

  for (const fileName of ROOT_FILES) {
    await add(fileName, rootFilesRoot, fileName === 'AGENTS.md' ? PRODUCT_AGENTS_SOURCE : fileName);
  }

  const registryPath = await requireContainedFile(agentsRoot, 'registry.json');
  const registry = JSON.parse(await readFile(registryPath, 'utf8'));
  const registeredRoleIds = Object.keys(registry?.roles ?? {}).sort();
  if (JSON.stringify(registeredRoleIds) !== JSON.stringify([...ROLE_IDS].sort())) {
    throw new Error(`agents/registry.json must declare exactly: ${ROLE_IDS.join(', ')}`);
  }
  await add('agents/registry.json', agentsRoot, 'registry.json');
  for (const roleId of ROLE_IDS) {
    const instruction = registry.roles[roleId]?.instruction;
    const expected = `agents/AGENT_${roleId}.md`;
    if (instruction !== expected) {
      throw new Error(`Registry instruction mismatch for ${roleId}: ${String(instruction)}`);
    }
    await add(expected, agentsRoot, `AGENT_${roleId}.md`);
  }

  for (const fileName of DOC_FILES) await add(`docs/${fileName}`, docsRoot, fileName);
  for (const fileName of TOOL_FILES) await add(`tools/${fileName}`, toolsRoot, fileName);
  for (const fileName of WORKFLOW_METADATA_FILES) {
    await add(`workflows/${fileName}`, workflowsRoot, fileName);
  }

  const indexPath = await requireContainedFile(workflowsRoot, 'index.json');
  const sourceIndexBytes = await readFile(indexPath);
  const filtered = filteredIndex(JSON.parse(sourceIndexBytes.toString('utf8')));
  const index = filtered.value;
  const indexEntry = entries.find((entry) => entry.bundlePath === 'workflows/index.json');
  indexEntry.expectedContent = filtered.changed
    ? Buffer.from(`${JSON.stringify(index, null, 2)}\n`, 'utf8')
    : sourceIndexBytes;
  const allSkillDirectories = (await readdir(skillsRoot, { withFileTypes: true }))
    .filter((entry) => entry.isDirectory())
    .map((entry) => entry.name)
    .sort();
  const expectedSkillDirectories = [...BUNDLED_SKILL_NAMES, ...EXCLUDED_BUNDLED_SKILLS].sort();
  if (JSON.stringify(allSkillDirectories) !== JSON.stringify(expectedSkillDirectories)) {
    throw new Error(`Canonical skill membership mismatch: expected ${expectedSkillDirectories.join(', ')}`);
  }
  const identities = new Set();
  for (const method of index.methods) {
    assertPlainName(method?.name, 'method name');
    if (!['workflow', 'skill'].includes(method.kind)) {
      throw new Error(`Invalid method kind for ${method.name}: ${String(method.kind)}`);
    }
    const identity = `${method.kind}:${method.name}`;
    if (identities.has(identity)) throw new Error(`Duplicate method identity: ${identity}`);
    identities.add(identity);
    if (!Array.isArray(method.resources) || method.resources.length === 0) {
      throw new Error(`Method has no resources: ${identity}`);
    }
    const sourceRoot = method.kind === 'workflow' ? workflowsRoot : skillsRoot;
    const bundlePrefix = method.kind === 'workflow' ? 'workflows' : '.agents/skills';
    for (const resource of method.resources) {
      await add(
        `${bundlePrefix}/${method.name}/${resource}`,
        path.join(sourceRoot, method.name),
        resource
      );
    }
  }

  const indexedWorkflows = index.methods
    .filter((method) => method.kind === 'workflow')
    .map((method) => method.name)
    .sort();
  const actualWorkflows = [];
  for (const entry of await readdir(workflowsRoot, { withFileTypes: true })) {
    if (entry.isDirectory()) {
      try {
        await requireContainedFile(path.join(workflowsRoot, entry.name), 'WORKFLOW.md');
        actualWorkflows.push(entry.name);
      } catch (error) {
        if (error?.code !== 'ENOENT') throw error;
      }
    }
  }
  actualWorkflows.sort();
  if (JSON.stringify(indexedWorkflows) !== JSON.stringify(actualWorkflows)) {
    throw new Error('Workflow index membership does not match canonical workflow packages');
  }

  const skillDirectories = [...BUNDLED_SKILL_NAMES].sort();
  for (const skillName of skillDirectories) {
    assertPlainName(skillName, 'skill directory');
    const skillRoot = path.join(skillsRoot, skillName);
    await requireContainedFile(skillRoot, 'SKILL.md');
    for (const resource of await listFiles(skillRoot)) {
      const bundlePath = `.agents/skills/${skillName}/${resource}`;
      if (!entries.some((entry) => entry.bundlePath === bundlePath)) {
        await add(bundlePath, skillRoot, resource);
      }
    }
  }

  const duplicate = entries.find(
    (entry, index_) => entries.findIndex((candidate) => candidate.bundlePath === entry.bundlePath) !== index_
  );
  if (duplicate) throw new Error(`Duplicate bundled path: ${duplicate.bundlePath}`);

  return {
    entries: entries.sort((left, right) => left.bundlePath.localeCompare(right.bundlePath)),
    index
  };
}

export async function preparePackagedInstructionRoot({ sourceRoot, docsRoot, outputRoot }) {
  const resolvedSourceRoot = await realpath(sourceRoot);
  const resolvedDocsRoot = await realpath(docsRoot);
  const resolvedOutputRoot = path.resolve(outputRoot);
  const canonicalOutputRoot = await resolvePotentialPath(outputRoot);
  const overlaps = (left, right) =>
    left === right || left.startsWith(`${right}${path.sep}`) || right.startsWith(`${left}${path.sep}`);
  if (
    overlaps(resolvedOutputRoot, path.resolve(sourceRoot)) &&
    (resolvedOutputRoot === path.resolve(sourceRoot) || path.resolve(sourceRoot).startsWith(`${resolvedOutputRoot}${path.sep}`))
  ) {
    throw new Error('output-root must not equal or contain source-root');
  }
  const lexicalInstructionRoots = [
    path.join(path.resolve(sourceRoot), 'projects', 'chirality-app-dev', 'instructions'),
    path.resolve(docsRoot),
    path.join(path.resolve(sourceRoot), 'agents'),
    path.join(path.resolve(sourceRoot), 'workflows'),
    path.join(path.resolve(sourceRoot), '.agents', 'skills'),
    path.join(path.resolve(sourceRoot), 'tools')
  ];
  const canonicalInstructionRoots = await Promise.all(
    lexicalInstructionRoots.map((entry) => realpath(entry))
  );
  if (
    lexicalInstructionRoots.some((entry) => overlaps(resolvedOutputRoot, entry)) ||
    canonicalInstructionRoots.some((entry) => overlaps(canonicalOutputRoot, entry))
  ) {
    throw new Error('output-root must not overlap a canonical instruction source root');
  }
  const agentsRoot = path.join(sourceRoot, 'agents');
  const { entries, index } = await buildExpectedInstructionManifest({
    rootFilesRoot: sourceRoot,
    agentsRoot,
    docsRoot
  });

  await rm(outputRoot, { recursive: true, force: true });
  await mkdir(outputRoot, { recursive: true });
  for (const entry of entries) {
    const destination = path.join(outputRoot, entry.bundlePath);
    if (!path.resolve(destination).startsWith(`${resolvedOutputRoot}${path.sep}`)) {
      throw new Error(`Bundled destination escapes output-root: ${entry.bundlePath}`);
    }
    await mkdir(path.dirname(destination), { recursive: true });
    if (entry.bundlePath === 'workflows/index.json') {
      await writeFile(destination, entry.expectedContent);
    } else {
      await cp(entry.sourcePath, destination);
    }
  }
  const files = [];
  for (const entry of entries) {
    const data = await readFile(path.join(outputRoot, entry.bundlePath));
    files.push({
      path: entry.bundlePath,
      sizeBytes: data.length,
      sha256: createHash('sha256').update(data).digest('hex')
    });
  }
  const bundledSkills = (await readdir(path.join(outputRoot, '.agents', 'skills'), { withFileTypes: true }))
    .filter((entry) => entry.isDirectory())
    .map((entry) => entry.name)
    .sort();
  const manifest = {
    schema: 'chirality-instruction-bundle-manifest/v2',
    sourceSchema: index.schema,
    documentationClosure: {
      rule: 'direct-root-doc-references-from-bundled-entry-roles-workflows-and-skills',
      files: DOC_FILES.map((entry) => `docs/${entry}`)
    },
    excludedSkillNames: [...EXCLUDED_BUNDLED_SKILLS].sort(),
    toolMembersSemantics:
      'packaged dependency bytes only; allowed capabilities and commands come from each skill execution.json and the outer policy intersection',
    skills: bundledSkills.map((name) => ({
      name,
      resources: files.filter((entry) => entry.path.startsWith(`.agents/skills/${name}/`)).map((entry) => entry.path),
      toolMembers: (SKILL_TOOL_CLOSURE[name]?.toolMembers ?? []).map((entry) => `tools/${entry}`),
      externalPrerequisites: SKILL_TOOL_CLOSURE[name]?.externalPrerequisites ?? []
    })),
    files
  };
  await writeFile(path.join(outputRoot, BUNDLE_MANIFEST), `${JSON.stringify(manifest, null, 2)}\n`, 'utf8');
  return entries.map((entry) => entry.bundlePath);
}

function parseArgs(argv) {
  const values = {};
  for (let index = 0; index < argv.length; index += 2) {
    const flag = argv[index];
    const value = argv[index + 1];
    if (!value || !['--source-root', '--docs-root', '--output-root'].includes(flag)) {
      throw new Error(`Usage: prepare-packaged-instruction-root.mjs --source-root <root> --docs-root <root> --output-root <root>`);
    }
    values[flag.slice(2).replace(/-([a-z])/gu, (_, letter) => letter.toUpperCase())] = path.resolve(value);
  }
  if (!values.sourceRoot || !values.docsRoot || !values.outputRoot) {
    throw new Error('source-root, docs-root, and output-root are required');
  }
  return values;
}

if (process.argv[1] && path.resolve(process.argv[1]) === scriptPath) {
  try {
    const files = await preparePackagedInstructionRoot(parseArgs(process.argv.slice(2)));
    console.log(`prepared packaged instruction root (${files.length} files)`);
  } catch (error) {
    console.error(`packaged instruction-root preparation failed: ${error instanceof Error ? error.message : String(error)}`);
    process.exitCode = 1;
  }
}
