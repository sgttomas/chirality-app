import { constants as fsConstants } from 'node:fs';
import { access, copyFile, mkdir, readFile, stat, writeFile } from 'node:fs/promises';
import path from 'node:path';
import { HarnessError } from '@chirality/runtime-contracts/errors';
import { sanitizeNonEmptyLabel } from './sanitize';

const PKG_ID_PATTERN = /^PKG-\d{2,3}$/;
const DEL_ID_PATTERN = /^DEL-\d{2,3}-\d{2}$/;

const EXECUTION_ROOT_DIRECTORIES = [
  '_Aggregation',
  '_Aggregation/_Archive',
  '_Aggregation/_Templates',
  '_Change',
  '_Coordination',
  '_Decomposition',
  '_Decomposition/_Archive',
  '_Estimates',
  '_Reconciliation',
  '_Archive',
  '_Scripts',
  '_Sources'
] as const;

const REQUIRED_PACKAGE_SUBDIRECTORIES = [
  '0_References',
  '0_References/_Archive',
  '1_Working',
  '1_Working/_Archive',
  '2_Checking',
  '2_Checking/From',
  '2_Checking/To',
  '3_Issued',
  '3_Issued/_Archive'
] as const;

const PREPARATION_REQUIRED_METADATA_FILES = [
  '_STATUS.md',
  '_CONTEXT.md',
  '_DEPENDENCIES.md',
  '_REFERENCES.md',
  '_SEMANTIC.md'
] as const;

const COORDINATION_MODES = ['SCHEDULE_FIRST', 'DEPENDENCY_TRACKED', 'HYBRID'] as const;

export type CoordinationMode = (typeof COORDINATION_MODES)[number];

type ParsedDeliverable = {
  id: string;
  name: string;
};

type ParsedPackage = {
  id: string;
  name: string;
  deliverables: ParsedDeliverable[];
};

type ParsedDecomposition = {
  projectName: string;
  packages: ParsedPackage[];
};

type PackagePlan = {
  id: string;
  name: string;
  path: string;
  expectedPaths: string[];
  deliverables: Array<{
    id: string;
    name: string;
    path: string;
  }>;
};

export type LayoutValidationItem = {
  id: string;
  path: string;
  valid: boolean;
  missing: string[];
};

export type LayoutValidationResult = {
  valid: boolean;
  executionRoot: {
    path: string;
    valid: boolean;
    missing: string[];
  };
  packages: LayoutValidationItem[];
  deliverables: LayoutValidationItem[];
};

export type PreparationCompatibilityItem = {
  id: string;
  path: string;
  ready: boolean;
  issues: string[];
};

export type PreparationCompatibilityResult = {
  ready: boolean;
  deliverablesChecked: number;
  issueCount: number;
  deliverables: PreparationCompatibilityItem[];
};

export type ScaffoldExecutionRootInput = {
  executionRoot: string;
  decompositionPath: string;
  projectName?: string;
  coordinationMode?: CoordinationMode;
  now?: Date;
};

export type ScaffoldExecutionRootPreviewInput = Omit<ScaffoldExecutionRootInput, 'now'>;

export type ScaffoldExecutionRootResult = {
  executionRoot: string;
  decompositionPath: string;
  copiedDecompositionPath: string;
  projectName: string;
  coordinationMode: CoordinationMode;
  packageCount: number;
  deliverableCount: number;
  created: {
    directories: string[];
    files: string[];
  };
  layoutValidation: LayoutValidationResult;
  preparationCompatibility: PreparationCompatibilityResult;
};

export type ScaffoldExecutionRootPreviewResult = {
  executionRoot: string;
  decompositionPath: string;
  copiedDecompositionPath: string;
  projectName: string;
  coordinationMode: CoordinationMode;
  packageCount: number;
  deliverableCount: number;
  planned: {
    directories: string[];
    files: string[];
  };
  packages: PackagePlan[];
};

type ScaffoldFailureStage =
  | 'ensure_execution_root'
  | 'ensure_tool_root'
  | 'copy_decomposition'
  | 'write_init'
  | 'write_coordination'
  | 'create_package'
  | 'create_package_subdir'
  | 'create_deliverable'
  | 'seed_preparation_file'
  | 'validate_layout'
  | 'validate_preparation_compatibility';

function isErrnoCode(error: unknown, code: string): boolean {
  if (typeof error !== 'object' || error === null) {
    return false;
  }

  const value = (error as NodeJS.ErrnoException).code;
  return value === code;
}

function asDetailsRecord(details: unknown): Record<string, unknown> | null {
  if (typeof details !== 'object' || details === null || Array.isArray(details)) {
    return null;
  }

  return details as Record<string, unknown>;
}

function withScaffoldFailureContext(
  error: unknown,
  stage: ScaffoldFailureStage,
  targetPath: string,
  createdDirectories: string[],
  createdFiles: string[]
): HarnessError {
  const contextDetails: Record<string, unknown> = {
    scaffoldStrategy: 'FAIL_FAST',
    stage,
    targetPath,
    created: {
      directories: createdDirectories,
      files: createdFiles
    },
    guidance:
      'Resolve the filesystem error and rerun scaffolding. Existing created paths are preserved.'
  };

  if (error instanceof HarnessError) {
    const existingDetails = asDetailsRecord(error.details);
    return new HarnessError(error.type, error.status, error.message, {
      ...(existingDetails ?? {}),
      ...contextDetails
    });
  }

  if (error instanceof Error) {
    return new HarnessError('SDK_FAILURE', 500, error.message, contextDetails);
  }

  return new HarnessError('SDK_FAILURE', 500, 'Scaffolding failed unexpectedly', contextDetails);
}

function requireAbsolutePath(input: unknown, field: string): string {
  if (typeof input !== 'string' || input.trim().length === 0) {
    throw new HarnessError('INVALID_REQUEST', 400, `Missing or invalid '${field}'`);
  }

  const trimmed = input.trim();
  if (!path.isAbsolute(trimmed)) {
    throw new HarnessError('INVALID_REQUEST', 400, `${field} must be an absolute filesystem path`);
  }

  return path.resolve(trimmed);
}

function parseMarkdownTableRow(line: string): string[] | null {
  const trimmed = line.trim();
  if (!trimmed.startsWith('|') || !trimmed.endsWith('|')) {
    return null;
  }

  const cells = trimmed
    .slice(1, -1)
    .split('|')
    .map((cell) => cell.trim());

  const isSeparator = cells.every((cell) => /^:?-{3,}:?$/.test(cell));
  if (isSeparator) {
    return null;
  }

  return cells;
}

function extractProjectName(markdown: string): string {
  const titleLine = markdown
    .split(/\r?\n/)
    .map((line) => line.trim())
    .find((line) => line.startsWith('# '));

  if (!titleLine) {
    return 'Chirality Project';
  }

  const heading = titleLine.replace(/^#\s+/, '').trim();
  const splitOnDash = heading.split(/\s+[—-]\s+/);
  if (splitOnDash[0].trim().length > 0) {
    return splitOnDash[0].trim();
  }

  return heading || 'Chirality Project';
}

function parseDecomposition(markdown: string): ParsedDecomposition {
  const lines = markdown.split(/\r?\n/);
  const packageNameById = new Map<string, string>();
  const deliverablesByPackage = new Map<string, Map<string, string>>();

  let currentPackageId: string | undefined;

  for (const line of lines) {
    const packageHeadingMatch = line.match(/^###\s+(PKG-\d{2,3})\s+[—-]\s+(.+?)\s*$/);
    if (packageHeadingMatch) {
      const packageId = packageHeadingMatch[1];
      const packageName = packageHeadingMatch[2].trim();
      currentPackageId = packageId;

      if (!packageNameById.has(packageId)) {
        packageNameById.set(packageId, packageName);
      }
      if (!deliverablesByPackage.has(packageId)) {
        deliverablesByPackage.set(packageId, new Map<string, string>());
      }
      continue;
    }

    const row = parseMarkdownTableRow(line);
    if (!row || row.length < 2) {
      continue;
    }

    const first = row[0];
    const second = row[1];

    if (PKG_ID_PATTERN.test(first)) {
      if (!packageNameById.has(first)) {
        packageNameById.set(first, second);
      }
      if (!deliverablesByPackage.has(first)) {
        deliverablesByPackage.set(first, new Map<string, string>());
      }
      continue;
    }

    if (currentPackageId && DEL_ID_PATTERN.test(first)) {
      const deliverables = deliverablesByPackage.get(currentPackageId);
      if (!deliverables) {
        continue;
      }
      if (!deliverables.has(first)) {
        deliverables.set(first, second);
      }
    }
  }

  const packageIds = new Set([...packageNameById.keys(), ...deliverablesByPackage.keys()]);
  const packages = [...packageIds]
    .sort((a, b) => a.localeCompare(b))
    .map((packageId) => {
      const packageName = packageNameById.get(packageId) ?? packageId;
      const deliverablesMap = deliverablesByPackage.get(packageId) ?? new Map<string, string>();
      const deliverables = [...deliverablesMap.entries()]
        .sort((a, b) => a[0].localeCompare(b[0]))
        .map(([deliverableId, deliverableName]) => ({
          id: deliverableId,
          name: deliverableName
        }));

      return {
        id: packageId,
        name: packageName,
        deliverables
      };
    });

  const deliverableCount = packages.reduce((total, pkg) => total + pkg.deliverables.length, 0);

  if (packages.length === 0 || deliverableCount === 0) {
    throw new HarnessError(
      'INVALID_REQUEST',
      400,
      'Decomposition document does not contain parseable package and deliverable tables'
    );
  }

  return {
    projectName: extractProjectName(markdown),
    packages
  };
}

function parseCoordinationMode(input: unknown): CoordinationMode {
  if (input === undefined) {
    return 'DEPENDENCY_TRACKED';
  }

  if (typeof input !== 'string') {
    throw new HarnessError(
      'INVALID_REQUEST',
      400,
      "coordinationMode must be one of 'SCHEDULE_FIRST', 'DEPENDENCY_TRACKED', 'HYBRID'"
    );
  }

  const normalized = input.trim().toUpperCase() as CoordinationMode;
  if (!COORDINATION_MODES.includes(normalized)) {
    throw new HarnessError(
      'INVALID_REQUEST',
      400,
      "coordinationMode must be one of 'SCHEDULE_FIRST', 'DEPENDENCY_TRACKED', 'HYBRID'",
      { coordinationMode: input }
    );
  }

  return normalized;
}

function buildPackagePlans(executionRoot: string, parsed: ParsedDecomposition): PackagePlan[] {
  return parsed.packages.map((pkg) => {
    const packageLabel = sanitizeNonEmptyLabel(pkg.name, `package '${pkg.id}' name`);
    const packageFolder = `${pkg.id}_${packageLabel}`;
    const packagePath = path.join(executionRoot, packageFolder);
    const expectedPackagePaths = [
      packagePath,
      ...REQUIRED_PACKAGE_SUBDIRECTORIES.map((subDirectory) =>
        path.join(packagePath, subDirectory)
      )
    ];

    return {
      id: pkg.id,
      name: pkg.name,
      path: packagePath,
      expectedPaths: expectedPackagePaths,
      deliverables: pkg.deliverables.map((deliverable) => {
        const deliverableLabel = sanitizeNonEmptyLabel(
          deliverable.name,
          `deliverable '${deliverable.id}' name`
        );
        return {
          id: deliverable.id,
          name: deliverable.name,
          path: path.join(packagePath, '1_Working', `${deliverable.id}_${deliverableLabel}`)
        };
      })
    };
  });
}

function getPlannedDirectories(executionRoot: string, packagePlans: readonly PackagePlan[]): string[] {
  return [
    executionRoot,
    ...EXECUTION_ROOT_DIRECTORIES.map((relativePath) => path.join(executionRoot, relativePath)),
    ...packagePlans.flatMap((pkg) => [
      ...pkg.expectedPaths,
      ...pkg.deliverables.map((deliverable) => deliverable.path)
    ])
  ];
}

function getPlannedPreparationFiles(packagePlans: readonly PackagePlan[]): string[] {
  return packagePlans.flatMap((pkg) =>
    pkg.deliverables.flatMap((deliverable) =>
      PREPARATION_REQUIRED_METADATA_FILES.map((metadataFile) =>
        path.join(deliverable.path, metadataFile)
      )
    )
  );
}

async function ensureDirectory(targetPath: string, createdDirectories: string[]): Promise<void> {
  try {
    const existing = await stat(targetPath);
    if (!existing.isDirectory()) {
      throw new HarnessError(
        'WORKING_ROOT_INACCESSIBLE',
        409,
        `Expected directory but found file at '${targetPath}'`
      );
    }
    return;
  } catch (error) {
    if (!isErrnoCode(error, 'ENOENT')) {
      if (error instanceof HarnessError) {
        throw error;
      }
      throw new HarnessError(
        'WORKING_ROOT_INACCESSIBLE',
        500,
        `Unable to inspect directory '${targetPath}'`
      );
    }
  }

  await mkdir(targetPath, { recursive: true });
  createdDirectories.push(targetPath);
}

async function ensureFile(
  targetPath: string,
  content: string,
  createdFiles: string[]
): Promise<void> {
  try {
    await access(targetPath, fsConstants.F_OK);
    return;
  } catch (error) {
    if (!isErrnoCode(error, 'ENOENT')) {
      throw new HarnessError('SDK_FAILURE', 500, `Unable to access '${targetPath}'`);
    }
  }

  await writeFile(targetPath, content, 'utf8');
  createdFiles.push(targetPath);
}

async function findMissingPaths(pathsToCheck: string[]): Promise<string[]> {
  const missing: string[] = [];

  for (const candidatePath of pathsToCheck) {
    try {
      await access(candidatePath, fsConstants.F_OK);
    } catch {
      missing.push(candidatePath);
    }
  }

  return missing;
}

async function pathExists(candidatePath: string): Promise<boolean> {
  try {
    await access(candidatePath, fsConstants.F_OK);
    return true;
  } catch {
    return false;
  }
}

export async function previewScaffoldExecutionRoot(
  input: ScaffoldExecutionRootPreviewInput
): Promise<ScaffoldExecutionRootPreviewResult> {
  const executionRoot = requireAbsolutePath(input.executionRoot, 'executionRoot');
  const decompositionPath = requireAbsolutePath(input.decompositionPath, 'decompositionPath');
  const coordinationMode = parseCoordinationMode(input.coordinationMode);

  let decompositionMarkdown: string;
  try {
    decompositionMarkdown = await readFile(decompositionPath, 'utf8');
  } catch {
    throw new HarnessError(
      'INVALID_REQUEST',
      400,
      'decompositionPath must point to a readable markdown file',
      { decompositionPath }
    );
  }

  const parsed = parseDecomposition(decompositionMarkdown);
  const projectName = input.projectName?.trim() || parsed.projectName;
  const copiedDecompositionPath = path.join(executionRoot, '_Decomposition', path.basename(decompositionPath));
  const packagePlans = buildPackagePlans(executionRoot, parsed);
  const deliverableCount = packagePlans.reduce((count, pkg) => count + pkg.deliverables.length, 0);

  return {
    executionRoot,
    decompositionPath,
    copiedDecompositionPath,
    projectName,
    coordinationMode,
    packageCount: packagePlans.length,
    deliverableCount,
    planned: {
      directories: getPlannedDirectories(executionRoot, packagePlans),
      files: [
        copiedDecompositionPath,
        path.join(executionRoot, 'INIT.md'),
        path.join(executionRoot, '_Coordination', '_COORDINATION.md'),
        ...getPlannedPreparationFiles(packagePlans)
      ]
    },
    packages: packagePlans
  };
}

function buildInitTemplate(
  projectName: string,
  decompositionReference: string,
  coordinationMode: CoordinationMode,
  now: Date
): string {
  const date = now.toISOString().slice(0, 10);
  return `# Execution Init

**Project Name:** ${projectName}
**Initialized:** ${date}
**Decomposition Reference:** ${decompositionReference}
**Coordination Mode:** ${coordinationMode}

## Session Parameters

- Update this file with project-specific startup constraints as needed.
`;
}

function buildCoordinationTemplate(coordinationMode: CoordinationMode): string {
  return `# Coordination Record

**Representation:** ${coordinationMode}
**Dependency tracking mode:** FULL_GRAPH

## Coordination Representations

- SCHEDULE_FIRST
- DEPENDENCY_TRACKED
- HYBRID

## Selection Notes

- Full dependency graph remains audit truth.
- Blocker subset may be used as execution sequencing truth per project policy.
`;
}

function buildStatusTemplate(deliverable: PackagePlan['deliverables'][number], now: Date): string {
  const date = now.toISOString().slice(0, 10);
  return `# Status: ${deliverable.id} ${deliverable.name}

**Current State:** OPEN
**Last Updated:** ${date}

## History

- ${date} - State set to OPEN (PREPARATION) [Scaffold baseline created.]
`;
}

function buildContextTemplate(
  pkg: PackagePlan,
  deliverable: PackagePlan['deliverables'][number],
  decompositionReference: string
): string {
  return `# Context: ${deliverable.id} ${deliverable.name}

## Identity

| Field | Value |
|---|---|
| PackageID | ${pkg.id} |
| PackageName | ${pkg.name} |
| DeliverableID | ${deliverable.id} |
| DeliverableName | ${deliverable.name} |
| DecompositionReference | ${decompositionReference} |
| ResponsibleParty | TBD |

## Scaffold Notes

This file was seeded by Chirality scaffold PREPARATION. Replace TBD fields only through the governed
project workflow.
`;
}

function buildDependenciesTemplate(deliverable: PackagePlan['deliverables'][number]): string {
  return `# Dependencies: ${deliverable.id} ${deliverable.name}

## Dependency Tracking

No accepted upstream dependency edges are recorded by the scaffold baseline.

## Scaffold Notes

Populate this file through governed dependency-discovery or dependency-closure workflows. Do not infer
dependency satisfaction from scaffold creation.
`;
}

function buildReferencesTemplate(deliverable: PackagePlan['deliverables'][number]): string {
  return `# References: ${deliverable.id} ${deliverable.name}

## Authoritative Source Corpus

TBD pending governed reference discovery.

## Scaffold Notes

This placeholder records that source references have not yet been accepted for this deliverable.
`;
}

function buildSemanticTemplate(deliverable: PackagePlan['deliverables'][number]): string {
  return `# Semantic Placeholder: ${deliverable.id} ${deliverable.name}

## Status

TBD pending semantic decomposition, lensed analysis, or an explicit deferral record.
`;
}

function buildPreparationFileTemplate(
  metadataFile: (typeof PREPARATION_REQUIRED_METADATA_FILES)[number],
  pkg: PackagePlan,
  deliverable: PackagePlan['deliverables'][number],
  decompositionReference: string,
  now: Date
): string {
  switch (metadataFile) {
    case '_STATUS.md':
      return buildStatusTemplate(deliverable, now);
    case '_CONTEXT.md':
      return buildContextTemplate(pkg, deliverable, decompositionReference);
    case '_DEPENDENCIES.md':
      return buildDependenciesTemplate(deliverable);
    case '_REFERENCES.md':
      return buildReferencesTemplate(deliverable);
    case '_SEMANTIC.md':
      return buildSemanticTemplate(deliverable);
  }
}

async function validateLayout(
  executionRoot: string,
  copiedDecompositionPath: string,
  packagePlans: PackagePlan[]
): Promise<LayoutValidationResult> {
  const executionExpectedPaths = [
    path.join(executionRoot, 'INIT.md'),
    path.join(executionRoot, '_Coordination', '_COORDINATION.md'),
    copiedDecompositionPath,
    ...EXECUTION_ROOT_DIRECTORIES.map((entry) => path.join(executionRoot, entry))
  ];

  const executionMissing = await findMissingPaths(executionExpectedPaths);
  const packageResults: LayoutValidationItem[] = [];
  const deliverableResults: LayoutValidationItem[] = [];

  for (const pkg of packagePlans) {
    const missing = await findMissingPaths(pkg.expectedPaths);
    packageResults.push({
      id: pkg.id,
      path: pkg.path,
      valid: missing.length === 0,
      missing
    });

    for (const deliverable of pkg.deliverables) {
      const deliverableMissing = await findMissingPaths([deliverable.path]);
      deliverableResults.push({
        id: deliverable.id,
        path: deliverable.path,
        valid: deliverableMissing.length === 0,
        missing: deliverableMissing
      });
    }
  }

  const valid =
    executionMissing.length === 0 &&
    packageResults.every((pkg) => pkg.valid) &&
    deliverableResults.every((deliverable) => deliverable.valid);

  return {
    valid,
    executionRoot: {
      path: executionRoot,
      valid: executionMissing.length === 0,
      missing: executionMissing
    },
    packages: packageResults,
    deliverables: deliverableResults
  };
}

async function validatePreparationCompatibility(
  packagePlans: PackagePlan[]
): Promise<PreparationCompatibilityResult> {
  const deliverableChecks: PreparationCompatibilityItem[] = [];

  for (const pkg of packagePlans) {
    const workingDirectory = path.join(pkg.path, '1_Working');
    const hasWorkingDirectory = await pathExists(workingDirectory);

    for (const deliverable of pkg.deliverables) {
      const issues: string[] = [];

      if (!hasWorkingDirectory) {
        issues.push(`Missing required package working directory '${workingDirectory}'.`);
      }

      let deliverableStat;
      try {
        deliverableStat = await stat(deliverable.path);
      } catch {
        issues.push(`Deliverable directory '${deliverable.path}' does not exist.`);
      }

      if (deliverableStat && !deliverableStat.isDirectory()) {
        issues.push(`Expected a directory at '${deliverable.path}'.`);
      }

      if (deliverableStat?.isDirectory()) {
        try {
          await access(deliverable.path, fsConstants.R_OK | fsConstants.W_OK);
        } catch {
          issues.push(`Deliverable directory '${deliverable.path}' is not writable.`);
        }

        for (const metadataFile of PREPARATION_REQUIRED_METADATA_FILES) {
          const metadataPath = path.join(deliverable.path, metadataFile);

          if (!(await pathExists(metadataPath))) {
            issues.push(`Missing required PREPARATION metadata file '${metadataPath}'.`);
            continue;
          }

          let metadataStat;
          try {
            metadataStat = await stat(metadataPath);
          } catch {
            issues.push(`Unable to inspect metadata target '${metadataPath}'.`);
            continue;
          }

          if (metadataStat.isDirectory()) {
            issues.push(
              `Metadata target '${metadataPath}' is a directory; PREPARATION expects a writable file path.`
            );
            continue;
          }

          try {
            await access(metadataPath, fsConstants.R_OK | fsConstants.W_OK);
          } catch {
            issues.push(`Metadata target '${metadataPath}' is not writable.`);
          }
        }
      }

      deliverableChecks.push({
        id: deliverable.id,
        path: deliverable.path,
        ready: issues.length === 0,
        issues
      });
    }
  }

  const issueCount = deliverableChecks.reduce((count, item) => count + item.issues.length, 0);

  return {
    ready: issueCount === 0,
    deliverablesChecked: deliverableChecks.length,
    issueCount,
    deliverables: deliverableChecks
  };
}

export async function scaffoldExecutionRoot(
  input: ScaffoldExecutionRootInput
): Promise<ScaffoldExecutionRootResult> {
  const executionRoot = requireAbsolutePath(input.executionRoot, 'executionRoot');
  const decompositionPath = requireAbsolutePath(input.decompositionPath, 'decompositionPath');
  const coordinationMode = parseCoordinationMode(input.coordinationMode);
  const now = input.now ?? new Date();

  let decompositionMarkdown: string;
  try {
    decompositionMarkdown = await readFile(decompositionPath, 'utf8');
  } catch {
    throw new HarnessError(
      'INVALID_REQUEST',
      400,
      'decompositionPath must point to a readable markdown file',
      { decompositionPath }
    );
  }

  const parsed = parseDecomposition(decompositionMarkdown);
  const projectName = input.projectName?.trim() || parsed.projectName;
  const copiedDecompositionPath = path.join(executionRoot, '_Decomposition', path.basename(decompositionPath));
  const packagePlans = buildPackagePlans(executionRoot, parsed);

  const createdDirectories: string[] = [];
  const createdFiles: string[] = [];
  let failureStage: ScaffoldFailureStage = 'ensure_execution_root';
  let failurePath = executionRoot;

  try {
    failureStage = 'ensure_execution_root';
    failurePath = executionRoot;
    await ensureDirectory(executionRoot, createdDirectories);

    for (const relativePath of EXECUTION_ROOT_DIRECTORIES) {
      const targetPath = path.join(executionRoot, relativePath);
      failureStage = 'ensure_tool_root';
      failurePath = targetPath;
      await ensureDirectory(targetPath, createdDirectories);
    }

    if (path.resolve(copiedDecompositionPath) !== path.resolve(decompositionPath)) {
      failureStage = 'copy_decomposition';
      failurePath = copiedDecompositionPath;
      try {
        await access(copiedDecompositionPath, fsConstants.F_OK);
      } catch (error) {
        if (!isErrnoCode(error, 'ENOENT')) {
          throw new HarnessError('SDK_FAILURE', 500, `Unable to access '${copiedDecompositionPath}'`);
        }
        await copyFile(decompositionPath, copiedDecompositionPath);
        createdFiles.push(copiedDecompositionPath);
      }
    }

    failureStage = 'write_init';
    failurePath = path.join(executionRoot, 'INIT.md');
    await ensureFile(
      failurePath,
      buildInitTemplate(
        projectName,
        path.relative(executionRoot, copiedDecompositionPath) || path.basename(copiedDecompositionPath),
        coordinationMode,
        now
      ),
      createdFiles
    );

    failureStage = 'write_coordination';
    failurePath = path.join(executionRoot, '_Coordination', '_COORDINATION.md');
    await ensureFile(failurePath, buildCoordinationTemplate(coordinationMode), createdFiles);

    const decompositionReference =
      path.relative(executionRoot, copiedDecompositionPath) || path.basename(copiedDecompositionPath);

    for (const pkg of packagePlans) {
      failureStage = 'create_package';
      failurePath = pkg.path;
      await ensureDirectory(pkg.path, createdDirectories);

      for (const absoluteSubDirectory of pkg.expectedPaths.slice(1)) {
        failureStage = 'create_package_subdir';
        failurePath = absoluteSubDirectory;
        await ensureDirectory(absoluteSubDirectory, createdDirectories);
      }

      for (const deliverable of pkg.deliverables) {
        failureStage = 'create_deliverable';
        failurePath = deliverable.path;
        await ensureDirectory(deliverable.path, createdDirectories);

        for (const metadataFile of PREPARATION_REQUIRED_METADATA_FILES) {
          const metadataPath = path.join(deliverable.path, metadataFile);
          failureStage = 'seed_preparation_file';
          failurePath = metadataPath;
          await ensureFile(
            metadataPath,
            buildPreparationFileTemplate(metadataFile, pkg, deliverable, decompositionReference, now),
            createdFiles
          );
        }
      }
    }

    const deliverableCount = packagePlans.reduce((count, pkg) => count + pkg.deliverables.length, 0);
    failureStage = 'validate_layout';
    failurePath = executionRoot;
    const layoutValidation = await validateLayout(executionRoot, copiedDecompositionPath, packagePlans);
    failureStage = 'validate_preparation_compatibility';
    const preparationCompatibility = await validatePreparationCompatibility(packagePlans);

    return {
      executionRoot,
      decompositionPath,
      copiedDecompositionPath,
      projectName,
      coordinationMode,
      packageCount: packagePlans.length,
      deliverableCount,
      created: {
        directories: createdDirectories,
        files: createdFiles
      },
      layoutValidation,
      preparationCompatibility
    };
  } catch (error) {
    throw withScaffoldFailureContext(
      error,
      failureStage,
      failurePath,
      createdDirectories,
      createdFiles
    );
  }
}
