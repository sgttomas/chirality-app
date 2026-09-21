import { readFile, readdir, stat } from 'node:fs/promises';
import path from 'node:path';
import { parseStatusDocument } from '../lifecycle/status-parser';

const MAX_TREE_ENTRIES_PER_DIRECTORY = 60;
const MAX_SCOPE_SCAN_DIRECTORIES = 2500;
const SKIP_DIRECTORY_NAMES = new Set([
  '.git',
  '.next',
  'node_modules',
  'dist',
  'dist-electron',
  'out'
]);
// The admitted engine's per-candidate scratch directory lives under the project
// root while a candidate is alive. It is runtime custody, not project content.
const RUNTIME_SCRATCH_DIRECTORY_PATTERN = /^\.chirality-scratch-/;

export function isRuntimeScratchEntryName(name: string): boolean {
  return RUNTIME_SCRATCH_DIRECTORY_PATTERN.test(name);
}

export class WorkspaceValidationError extends Error {
  status: number;
  code: string;

  constructor(code: string, status: number, message: string) {
    super(message);
    this.name = 'WorkspaceValidationError';
    this.status = status;
    this.code = code;
  }
}

export class WorkspaceOperationError extends Error {
  status: number;
  code: string;
  details?: unknown;

  constructor(code: string, status: number, message: string, details?: unknown) {
    super(message);
    this.name = 'WorkspaceOperationError';
    this.status = status;
    this.code = code;
    this.details = details;
  }
}

export type TreeNode = {
  name: string;
  path: string;
  kind: 'directory' | 'file' | 'symlink';
  children?: TreeNode[];
  truncated?: boolean;
};

export type ScopeItem = {
  id: string;
  label: string;
  path: string;
};

export type ScopeScanResult = {
  deliverables: ScopeItem[];
  knowledgeTypes: ScopeItem[];
  hasKnowledgeDecomposition: boolean;
  truncated: boolean;
};

export type ProjectDeliverable = {
  id: string;
  name: string;
  pkg: string;
  status: string;
  path: string;
};

export type DeliverableContractFindingSeverity = 'info' | 'warning' | 'error';

export type DeliverableContractFindingCategory =
  | 'required_metadata'
  | 'preparation_baseline'
  | 'document_kit'
  | 'scope_of_work'
  | 'canonical_memory'
  | 'optional_file'
  | 'prohibited_file'
  | 'source_hash_warning'
  | 'unknown_unsupported_condition';

export type DeliverableContractFileState = {
  fileName: string;
  path: string;
  present: boolean;
};

export type DeliverableContractFinding = {
  deliverableId: string;
  path: string;
  category: DeliverableContractFindingCategory;
  condition: string;
  lifecycleState: string;
  severity: DeliverableContractFindingSeverity;
  sourceRef: string;
  evidence: string;
  message: string;
};

export type DeliverableContractScanResult = {
  deliverableId: string;
  path: string;
  lifecycleState: string;
  valid: boolean;
  errorCount: number;
  warningCount: number;
  infoCount: number;
  requiredMetadata: DeliverableContractFileState[];
  preparationBaseline: DeliverableContractFileState[];
  documentKit: DeliverableContractFileState[];
  documentFormat: DeliverableProductionFormat;
  selectedProductionDocuments: DeliverableContractFileState[];
  scopeOfWork: DeliverableContractFileState;
  canonicalMemory: DeliverableContractFileState;
  optionalFiles: DeliverableContractFileState[];
  findings: DeliverableContractFinding[];
};

export type DeliverableProductionFormat =
  | 'LEGACY_FOUR_DOC'
  | 'SOW_V1'
  | 'MIGRATION_DUAL'
  | 'AMBIGUOUS'
  | 'INVALID';

export type ScopeOfWorkMigrationActivation = {
  mode: 'MIGRATION_DUAL';
  isolatedWorkspace: true;
  authorityRef: string;
  allowedDeliverablePaths: readonly string[];
};

export type KnowledgeTypeOption = {
  id: string;
  label: string;
  matchingDeliverableKeys: string[];
};

export type ProjectDeliverablesScanResult = {
  deliverables: ProjectDeliverable[];
  deliverableContracts: DeliverableContractScanResult[];
  knowledgeDecomposition: {
    enabled: boolean;
    markerFile: string | null;
  };
  knowledgeTypes: KnowledgeTypeOption[];
  truncated: boolean;
};

const KNOWLEDGE_MARKER_PATTERNS = [
  /\bknowledge\s+categories\b/i,
  /\bknowledge\s+types\b/i,
  /\bdomain[_\s-]*decomp/i,
  /\bdomain\s+decomposition\b/i
];

const REQUIRED_METADATA_FILES = [
  '_STATUS.md',
  '_CONTEXT.md',
  '_DEPENDENCIES.md',
  '_REFERENCES.md'
] as const;

const PREPARATION_BASELINE_FILES = ['_SEMANTIC.md'] as const;

const DOCUMENT_KIT_FILES = [
  'Datasheet.md',
  'Specification.md',
  'Guidance.md',
  'Procedure.md'
] as const;

const SCOPE_OF_WORK_FILE = 'ScopeOfWork.md';
const SCOPE_OF_WORK_SCHEMA = 'chirality-deliverable-sow/v1';
const ACCEPTED_SCOPE_OF_WORK_MIGRATION_AUTHORITY =
  'D-GOV-16@7584718aa32b112e415331736d1a8e68c12ac176';
const SCOPE_OF_WORK_SECTIONS = [
  'Purpose and Objective Traceability',
  'Deliverable Definition — Ontology',
  'Completion and Reliance Basis — Epistemology',
  'Production and Verification Method — Praxeology',
  'Governing Values and Decisions — Axiology',
  'Output and Evaluation Matrix'
] as const;
const SCOPE_OF_WORK_REQUIRED_FRONTMATTER = [
  'schema',
  'deliverable_id',
  'package_id',
  'decomposition_basis',
  'project_scope_refs',
  'package_objective_refs'
] as const;
const SCOPE_OF_WORK_LOCAL_ID = /\b(?:OUT|CLM|REQ|AC|VER|AX|TBD|CON|REM)-\d{3}\b/g;
const SCOPE_OF_WORK_DEFINITION = /^(?:[-*]\s+\*\*|#{3,6}\s+)((?:OUT|CLM|REQ|AC|VER|AX|TBD|CON|REM)-\d{3})(?:\*\*)?\s+[—-]\s+/gm;

const OPTIONAL_DELIVERABLE_FILES = [
  'Dependencies.csv',
  '_SEMANTIC_LENSING.md',
  'HASH_VERIFICATION_BYPASS.jsonl'
] as const;

const CANONICAL_MEMORY_FILE = 'MEMORY.md';
const PROHIBITED_MEMORY_FILE = '_MEMORY.md';

const KNOWLEDGE_TYPE_BUCKETS: Array<{
  id: string;
  label: string;
  matches: (fileNames: Set<string>) => boolean;
}> = [
  {
    id: 'scope-of-work',
    label: 'Scope of Work',
    matches: (fileNames) => fileNames.has(SCOPE_OF_WORK_FILE)
  },
  {
    id: 'datasheet',
    label: 'Datasheet',
    matches: (fileNames) => fileNames.has('Datasheet.md')
  },
  {
    id: 'specification',
    label: 'Specification',
    matches: (fileNames) => fileNames.has('Specification.md')
  },
  {
    id: 'guidance',
    label: 'Guidance',
    matches: (fileNames) => fileNames.has('Guidance.md')
  },
  {
    id: 'procedure',
    label: 'Procedure',
    matches: (fileNames) => fileNames.has('Procedure.md')
  },
  {
    id: 'dependencies',
    label: 'Dependencies',
    matches: (fileNames) => fileNames.has('_DEPENDENCIES.md') || fileNames.has('Dependencies.csv')
  },
  {
    id: 'references',
    label: 'References',
    matches: (fileNames) => fileNames.has('_REFERENCES.md')
  },
  {
    id: 'context',
    label: 'Context',
    matches: (fileNames) => fileNames.has('_CONTEXT.md')
  },
  {
    id: 'status',
    label: 'Status',
    matches: (fileNames) => fileNames.has('_STATUS.md')
  },
  {
    id: 'semantic',
    label: 'Semantic',
    matches: (fileNames) => fileNames.has('_SEMANTIC.md') || fileNames.has('_SEMANTIC_LENSING.md')
  },
  {
    id: 'memory',
    label: 'Memory',
    matches: (fileNames) => fileNames.has('MEMORY.md')
  }
];

function compareDirectoryEntries(a: { name: string; isDirectory(): boolean }, b: { name: string; isDirectory(): boolean }): number {
  if (a.isDirectory() && !b.isDirectory()) {
    return -1;
  }

  if (!a.isDirectory() && b.isDirectory()) {
    return 1;
  }

  return a.name.localeCompare(b.name);
}

function ensureAbsolutePath(input: string): string {
  const trimmed = input.trim();
  if (!trimmed) {
    throw new WorkspaceValidationError(
      'INVALID_PROJECT_ROOT',
      400,
      "Missing or invalid 'projectRoot'"
    );
  }

  if (!path.isAbsolute(trimmed)) {
    throw new WorkspaceValidationError(
      'INVALID_PROJECT_ROOT',
      400,
      'projectRoot must be an absolute filesystem path'
    );
  }

  return path.resolve(trimmed);
}

export async function normalizeProjectRoot(projectRootInput: string): Promise<string> {
  const normalized = ensureAbsolutePath(projectRootInput);

  let rootStat;
  try {
    rootStat = await stat(normalized);
  } catch {
    throw new WorkspaceValidationError(
      'WORKING_ROOT_INACCESSIBLE',
      404,
      'projectRoot is not accessible'
    );
  }

  if (!rootStat.isDirectory()) {
    throw new WorkspaceValidationError(
      'WORKING_ROOT_INACCESSIBLE',
      404,
      'projectRoot must point to a directory'
    );
  }

  return normalized;
}

async function buildTree(currentPath: string, remainingDepth: number): Promise<TreeNode> {
  const baseName = path.basename(currentPath) || currentPath;
  const node: TreeNode = {
    name: baseName,
    path: currentPath,
    kind: 'directory'
  };

  if (remainingDepth <= 0) {
    return node;
  }

  let entries;
  try {
    entries = await readdir(currentPath, { withFileTypes: true });
  } catch {
    return {
      ...node,
      truncated: true
    };
  }

  const filtered = entries
    .filter((entry) => !SKIP_DIRECTORY_NAMES.has(entry.name) && !isRuntimeScratchEntryName(entry.name))
    .sort(compareDirectoryEntries);
  const limited = filtered.slice(0, MAX_TREE_ENTRIES_PER_DIRECTORY);
  const children: TreeNode[] = [];

  for (const entry of limited) {
    const childPath = path.join(currentPath, entry.name);

    if (entry.isSymbolicLink()) {
      children.push({
        name: entry.name,
        path: childPath,
        kind: 'symlink'
      });
      continue;
    }

    if (entry.isDirectory()) {
      children.push(await buildTree(childPath, remainingDepth - 1));
      continue;
    }

    children.push({
      name: entry.name,
      path: childPath,
      kind: 'file'
    });
  }

  if (children.length > 0) {
    node.children = children;
  }

  if (filtered.length > MAX_TREE_ENTRIES_PER_DIRECTORY) {
    node.truncated = true;
  }

  return node;
}

export async function readProjectRootTree(projectRoot: string, depth: number): Promise<TreeNode> {
  const boundedDepth = Number.isFinite(depth) ? Math.max(1, Math.min(6, Math.floor(depth))) : 3;
  return buildTree(projectRoot, boundedDepth);
}

function splitStableId(folderName: string): { id: string; label: string } {
  const separator = folderName.indexOf('_');
  if (separator < 0) {
    return { id: folderName, label: folderName };
  }

  const id = folderName.slice(0, separator);
  const label = folderName.slice(separator + 1).replace(/_/g, ' ');
  return { id, label };
}

function isDeliverableDirectory(name: string): boolean {
  return /^DEL-\d{2,3}-\d{2}(?:$|_)/.test(name);
}

function isKnowledgeTypeDirectory(name: string): boolean {
  return /^KTY-[A-Za-z0-9]{2}-[A-Za-z0-9]{2}(?:$|_)/.test(name);
}

export function buildDeliverableCompositeKey(pkg: string, deliverableId: string): string {
  return `${pkg}::${deliverableId}`;
}

function getPackageFolderForDeliverable(projectRoot: string, deliverablePath: string): string {
  const relativePath = path.relative(projectRoot, deliverablePath);
  if (!relativePath || relativePath.startsWith('..')) {
    return 'UNKNOWN_PACKAGE';
  }

  const segments = relativePath.split(path.sep).filter(Boolean);
  const packageSegment = segments.find((segment) => /^PKG-\d{2,3}(?:$|_)/.test(segment));
  return packageSegment ?? 'UNKNOWN_PACKAGE';
}

async function parseDeliverableStatus(deliverablePath: string): Promise<string> {
  const statusPath = path.join(deliverablePath, '_STATUS.md');
  try {
    const content = await readFile(statusPath, 'utf8');
    return parseStatusDocument(content).currentState.toLowerCase();
  } catch {
    return 'unknown';
  }
}

async function readDirectoryFileSet(directoryPath: string): Promise<Set<string>> {
  const fileNames = new Set<string>();
  try {
    const entries = await readdir(directoryPath, { withFileTypes: true });
    for (const entry of entries) {
      if (entry.isFile()) {
        fileNames.add(entry.name);
      }
    }
  } catch {
    return fileNames;
  }
  return fileNames;
}

function buildFileStates(
  deliverablePath: string,
  fileNames: readonly string[],
  presentFileNames: Set<string>
): DeliverableContractFileState[] {
  return fileNames.map((fileName) => ({
    fileName,
    path: path.join(deliverablePath, fileName),
    present: presentFileNames.has(fileName)
  }));
}

function countFindings(
  findings: DeliverableContractFinding[],
  severity: DeliverableContractFindingSeverity
): number {
  return findings.filter((finding) => finding.severity === severity).length;
}

function buildFinding(input: {
  deliverableId: string;
  deliverablePath: string;
  fileName?: string;
  category: DeliverableContractFindingCategory;
  condition: string;
  lifecycleState: string;
  severity: DeliverableContractFindingSeverity;
  sourceRef: string;
  evidence: string;
  message: string;
}): DeliverableContractFinding {
  return {
    deliverableId: input.deliverableId,
    path: path.join(input.deliverablePath, input.fileName ?? ''),
    category: input.category,
    condition: input.condition,
    lifecycleState: input.lifecycleState,
    severity: input.severity,
    sourceRef: input.sourceRef,
    evidence: input.evidence,
    message: input.message
  };
}

async function readDeliverableLifecycleState(
  deliverablePath: string,
  deliverableId: string
): Promise<{ lifecycleState: string; parseFinding?: DeliverableContractFinding }> {
  const statusPath = path.join(deliverablePath, '_STATUS.md');

  try {
    const content = await readFile(statusPath, 'utf8');
    return {
      lifecycleState: parseStatusDocument(content).currentState
    };
  } catch (error) {
    const message = error instanceof Error ? error.message : 'Unable to parse _STATUS.md';
    return {
      lifecycleState: 'UNKNOWN',
      parseFinding: buildFinding({
        deliverableId,
        deliverablePath,
        fileName: '_STATUS.md',
        category: 'unknown_unsupported_condition',
        condition: 'status_unparseable',
        lifecycleState: 'UNKNOWN',
        severity: 'warning',
        sourceRef: 'docs/TYPES.md#lifecycle-state-table',
        evidence: message,
        message: '_STATUS.md is present but its lifecycle state could not be parsed.'
      })
    };
  }
}

function addReferenceWarnings(input: {
  deliverableId: string;
  deliverablePath: string;
  lifecycleState: string;
  referencesContent: string;
  findings: DeliverableContractFinding[];
}): void {
  const lines = input.referencesContent.split(/\r?\n/);

  for (const line of lines) {
    const normalized = line.toUpperCase();
    const trimmed = line.trim();
    if (!trimmed) {
      continue;
    }

    if (normalized.includes('HASH_MISMATCH') || normalized.includes('SOURCE_HASH_MISMATCH')) {
      input.findings.push(
        buildFinding({
          deliverableId: input.deliverableId,
          deliverablePath: input.deliverablePath,
          fileName: '_REFERENCES.md',
          category: 'source_hash_warning',
          condition: 'reference_hash_warning',
          lifecycleState: input.lifecycleState,
          severity: 'warning',
          sourceRef: '_REFERENCES.md#Authoritative Source Corpus',
          evidence: trimmed,
          message: '_REFERENCES.md records a source hash warning that must stay visible.'
        })
      );
      continue;
    }

    if (normalized.includes('UNKNOWN') || normalized.includes('UNSUPPORTED')) {
      input.findings.push(
        buildFinding({
          deliverableId: input.deliverableId,
          deliverablePath: input.deliverablePath,
          fileName: '_REFERENCES.md',
          category: 'unknown_unsupported_condition',
          condition: 'reference_unknown_condition',
          lifecycleState: input.lifecycleState,
          severity: 'warning',
          sourceRef: '_REFERENCES.md#Authoritative Source Corpus',
          evidence: trimmed,
          message: '_REFERENCES.md records an unknown or unsupported source condition.'
        })
      );
    }
  }
}

export async function scanDeliverableDocumentKitContract(input: {
  deliverableId: string;
  deliverablePath: string;
  scopeOfWorkMigration?: ScopeOfWorkMigrationActivation;
  requestedFormat?: DeliverableProductionFormat | 'AUTO';
}): Promise<DeliverableContractScanResult> {
  const fileNames = await readDirectoryFileSet(input.deliverablePath);
  const findings: DeliverableContractFinding[] = [];
  const lifecycle = await readDeliverableLifecycleState(input.deliverablePath, input.deliverableId);
  const lifecycleState = lifecycle.lifecycleState;

  if (lifecycle.parseFinding) {
    findings.push(lifecycle.parseFinding);
  }

  const requiredMetadata = buildFileStates(
    input.deliverablePath,
    REQUIRED_METADATA_FILES,
    fileNames
  );
  const preparationBaseline = buildFileStates(
    input.deliverablePath,
    PREPARATION_BASELINE_FILES,
    fileNames
  );
  const documentKit = buildFileStates(input.deliverablePath, DOCUMENT_KIT_FILES, fileNames);
  const scopeOfWork = buildFileStates(input.deliverablePath, [SCOPE_OF_WORK_FILE], fileNames)[0];
  const optionalFiles = buildFileStates(input.deliverablePath, OPTIONAL_DELIVERABLE_FILES, fileNames);
  const canonicalMemory = buildFileStates(input.deliverablePath, [CANONICAL_MEMORY_FILE], fileNames)[0];

  for (const file of requiredMetadata) {
    if (!file.present) {
      findings.push(
        buildFinding({
          deliverableId: input.deliverableId,
          deliverablePath: input.deliverablePath,
          fileName: file.fileName,
          category: 'required_metadata',
          condition: 'missing_required_metadata',
          lifecycleState,
          severity: 'error',
          sourceRef: 'docs/SPEC.md#section-3.1; docs/PRD.md#section-10.8',
          evidence: `${file.fileName} not found in deliverable directory listing`,
          message: `${file.fileName} is required deliverable metadata.`
        })
      );
    }
  }

  for (const file of preparationBaseline) {
    if (!file.present) {
      findings.push(
        buildFinding({
          deliverableId: input.deliverableId,
          deliverablePath: input.deliverablePath,
          fileName: file.fileName,
          category: 'preparation_baseline',
          condition: 'missing_preparation_baseline',
          lifecycleState,
          severity: 'warning',
          sourceRef: 'docs/SPEC.md#section-3.1; docs/PRD.md#section-10.8',
          evidence: `${file.fileName} not found in deliverable directory listing`,
          message: `${file.fileName} is part of the PREPARATION baseline fileset.`
        })
      );
    }
  }

  const hasAllLegacy = documentKit.every((file) => file.present);
  const hasAnyLegacy = documentKit.some((file) => file.present);
  const migrationAuthority = input.scopeOfWorkMigration?.authorityRef ?? '';
  const migrationPathAllowed = input.scopeOfWorkMigration?.mode === 'MIGRATION_DUAL'
    && input.scopeOfWorkMigration.isolatedWorkspace === true
    && migrationAuthority === ACCEPTED_SCOPE_OF_WORK_MIGRATION_AUTHORITY
    && input.scopeOfWorkMigration.allowedDeliverablePaths
      .map((allowedPath) => path.resolve(allowedPath))
      .includes(path.resolve(input.deliverablePath));
  let documentFormat: DeliverableProductionFormat = scopeOfWork.present
    ? hasAllLegacy
      ? 'AMBIGUOUS'
      : hasAnyLegacy
        ? 'INVALID'
      : 'SOW_V1'
    : hasAllLegacy
      ? 'LEGACY_FOUR_DOC'
      : 'INVALID';

  let validScopeOfWork = false;
  let scopeOfWorkBindsMigrationAuthority = false;
  if (scopeOfWork.present) {
    try {
      const content = await readFile(scopeOfWork.path, 'utf8');
      const frontmatterMatch = content.match(/^---\r?\n([\s\S]*?)\r?\n---\r?\n/);
      const frontmatter = new Map<string, string>();
      for (const line of frontmatterMatch?.[1].split(/\r?\n/) ?? []) {
        const separator = line.indexOf(':');
        if (separator > 0) {
          frontmatter.set(line.slice(0, separator).trim(), line.slice(separator + 1).trim());
        }
      }
      const headings = [...content.matchAll(/^##\s+(.+?)\s*$/gm)].map((match) => match[1]);
      const requiredHeadings = headings.filter((heading) =>
        (SCOPE_OF_WORK_SECTIONS as readonly string[]).includes(heading)
      );
      const definitions = [...content.matchAll(SCOPE_OF_WORK_DEFINITION)].map((match) => match[1]);
      const references = [...content.matchAll(SCOPE_OF_WORK_LOCAL_ID)].map((match) => match[0]);
      const defined = new Set(definitions);
      const matrixSection = content.split('## Output and Evaluation Matrix')[1] ?? '';
      const matrixRows = matrixSection.split(/\r?\n/).filter((line) => /^\|\s*OUT-\d{3}\s*\|/.test(line));
      const requiredKinds = ['OUT-', 'AC-', 'VER-'];
      validScopeOfWork = Boolean(frontmatterMatch)
        && SCOPE_OF_WORK_REQUIRED_FRONTMATTER.every((key) => {
          const value = frontmatter.get(key);
          return typeof value === 'string' && value.length > 0 && value !== '[]';
        })
        && frontmatter.get('schema') === SCOPE_OF_WORK_SCHEMA
        && requiredHeadings.join('\n') === SCOPE_OF_WORK_SECTIONS.join('\n')
        && requiredHeadings.length === SCOPE_OF_WORK_SECTIONS.length
        && new Set(definitions).size === definitions.length
        && references.every((reference) => defined.has(reference))
        && requiredKinds.every((prefix) => definitions.some((definition) => definition.startsWith(prefix)))
        && matrixRows.length > 0
        && matrixRows.every((row) => /\|\s*AC-\d{3}\s*\|\s*VER-\d{3}\s*\|/.test(row));
      scopeOfWorkBindsMigrationAuthority = migrationAuthority.length > 0
        && content.includes(`<!-- migration-authority: ${migrationAuthority} -->`);
      if (!validScopeOfWork) {
        findings.push(
          buildFinding({
            deliverableId: input.deliverableId,
            deliverablePath: input.deliverablePath,
            fileName: SCOPE_OF_WORK_FILE,
            category: 'scope_of_work',
            condition: 'invalid_scope_of_work_candidate',
            lifecycleState,
            severity: 'error',
            sourceRef: 'docs/DELIVERABLE_SCOPE_OF_WORK_STANDARD.md',
            evidence: `${SCOPE_OF_WORK_FILE} lacks the candidate schema marker or required sections`,
            message: `${SCOPE_OF_WORK_FILE} does not satisfy the candidate v1 structural contract.`
          })
        );
      }
    } catch {
      findings.push(
        buildFinding({
          deliverableId: input.deliverableId,
          deliverablePath: input.deliverablePath,
          fileName: SCOPE_OF_WORK_FILE,
          category: 'scope_of_work',
          condition: 'unreadable_scope_of_work_candidate',
          lifecycleState,
          severity: 'error',
          sourceRef: 'docs/DELIVERABLE_SCOPE_OF_WORK_STANDARD.md',
          evidence: `${SCOPE_OF_WORK_FILE} could not be read`,
          message: `${SCOPE_OF_WORK_FILE} is present but unreadable.`
        })
      );
    }
  }

  if (scopeOfWork.present && !validScopeOfWork) {
    documentFormat = 'INVALID';
  } else if (scopeOfWork.present && hasAllLegacy) {
    documentFormat = migrationPathAllowed && scopeOfWorkBindsMigrationAuthority
      ? 'MIGRATION_DUAL'
      : 'AMBIGUOUS';
  }

  if (documentFormat === 'AMBIGUOUS') {
    findings.push(
      buildFinding({
        deliverableId: input.deliverableId,
        deliverablePath: input.deliverablePath,
        fileName: SCOPE_OF_WORK_FILE,
        category: 'scope_of_work',
        condition: 'ambiguous_deliverable_format',
        lifecycleState,
        severity: 'error',
        sourceRef: 'docs/DELIVERABLE_SCOPE_OF_WORK_STANDARD.md#7-format-resolution-and-transition',
        evidence: `${SCOPE_OF_WORK_FILE} and all four legacy production documents coexist`,
        message: migrationPathAllowed && !scopeOfWorkBindsMigrationAuthority
          ? 'Dual format is ambiguous because ScopeOfWork.md does not bind the supplied migration authority.'
          : 'Dual format is ambiguous outside an exact authorized isolated migration workspace.'
      })
    );
  } else if (documentFormat === 'MIGRATION_DUAL') {
    findings.push(
      buildFinding({
        deliverableId: input.deliverableId,
        deliverablePath: input.deliverablePath,
        fileName: SCOPE_OF_WORK_FILE,
        category: 'scope_of_work',
        condition: 'migration_dual_authorized',
        lifecycleState,
        severity: 'info',
        sourceRef: 'docs/DELIVERABLE_SCOPE_OF_WORK_STANDARD.md#7-format-resolution-and-transition',
        evidence: `isolated workspace and ${migrationAuthority} are bound in ${SCOPE_OF_WORK_FILE}`,
        message: 'Dual format is authorized only for this isolated migration workspace.'
      })
    );
  } else if (documentFormat === 'SOW_V1') {
    findings.push(
      buildFinding({
        deliverableId: input.deliverableId,
        deliverablePath: input.deliverablePath,
        fileName: SCOPE_OF_WORK_FILE,
        category: 'scope_of_work',
        condition: 'scope_of_work_activated',
        lifecycleState,
        severity: 'info',
        sourceRef: 'docs/DELIVERABLE_SCOPE_OF_WORK_STANDARD.md#7-format-resolution-and-transition',
        evidence: `${SCOPE_OF_WORK_FILE} is the only production contract`,
        message: 'ScopeOfWork.md is the selected canonical production contract.'
      })
    );
  } else if (documentFormat === 'INVALID' && hasAnyLegacy && !hasAllLegacy) {
    findings.push(
      buildFinding({
        deliverableId: input.deliverableId,
        deliverablePath: input.deliverablePath,
        fileName: scopeOfWork.present
          ? SCOPE_OF_WORK_FILE
          : documentKit.find((file) => !file.present)?.fileName ?? SCOPE_OF_WORK_FILE,
        category: 'document_kit',
        condition: scopeOfWork.present
          ? 'invalid_mixed_production_format'
          : 'partial_legacy_production_kit',
        lifecycleState,
        severity: 'error',
        sourceRef: 'docs/DELIVERABLE_SCOPE_OF_WORK_STANDARD.md#7-format-resolution',
        evidence: scopeOfWork.present
          ? `${SCOPE_OF_WORK_FILE} coexists with only part of the legacy four-document kit`
          : 'only part of the legacy four-document kit is present',
        message: scopeOfWork.present
          ? 'Partial legacy coexistence is invalid and cannot be authorized as a migration workspace.'
          : 'A partial legacy four-document kit is not a valid production contract.'
      })
    );
  }

  if (documentFormat === 'INVALID' && !scopeOfWork.present && !hasAnyLegacy && lifecycleState !== 'OPEN') {
    findings.push(
      buildFinding({
        deliverableId: input.deliverableId,
        deliverablePath: input.deliverablePath,
        fileName: SCOPE_OF_WORK_FILE,
        category: 'document_kit',
        condition: 'missing_production_contract',
        lifecycleState,
        severity: 'error',
        sourceRef: 'docs/DELIVERABLE_SCOPE_OF_WORK_STANDARD.md#7-format-resolution-and-transition',
        evidence: 'neither ScopeOfWork.md nor a complete legacy four-document kit is present',
        message: 'A deliverable at or beyond INITIALIZED must have one valid production contract.'
      })
    );
  }

  const requestedFormat = input.requestedFormat ?? 'AUTO';
  if (requestedFormat !== 'AUTO' && requestedFormat !== documentFormat) {
    findings.push(
      buildFinding({
        deliverableId: input.deliverableId,
        deliverablePath: input.deliverablePath,
        fileName: SCOPE_OF_WORK_FILE,
        category: 'scope_of_work',
        condition: 'requested_format_mismatch',
        lifecycleState,
        severity: 'error',
        sourceRef: 'docs/DELIVERABLE_SCOPE_OF_WORK_STANDARD.md#7-format-resolution-and-transition',
        evidence: `requested ${requestedFormat}; resolved ${documentFormat}`,
        message: 'The requested production format does not match the fail-closed resolver result.'
      })
    );
  }

  for (const file of documentKit) {
    if (!file.present) {
      findings.push(
        buildFinding({
          deliverableId: input.deliverableId,
          deliverablePath: input.deliverablePath,
          fileName: file.fileName,
          category: 'document_kit',
          condition: 'missing_document_kit_file',
          lifecycleState,
          severity: 'warning',
          sourceRef: 'docs/SPEC.md#section-3.1; docs/PRD.md#FR-049',
          evidence: `${file.fileName} not found in deliverable directory listing`,
          message: `${file.fileName} is absent from the four-document kit.`
        })
      );
    }
  }

  findings.push(
    buildFinding({
      deliverableId: input.deliverableId,
      deliverablePath: input.deliverablePath,
      fileName: CANONICAL_MEMORY_FILE,
      category: 'canonical_memory',
      condition: canonicalMemory.present ? 'canonical_memory_present' : 'canonical_memory_absent',
      lifecycleState,
      severity: 'info',
      sourceRef: 'docs/SPEC.md#section-5.4; docs/PRD.md#section-10.8',
      evidence: canonicalMemory.present
        ? `${CANONICAL_MEMORY_FILE} found in deliverable directory listing`
        : `${CANONICAL_MEMORY_FILE} not found in deliverable directory listing`,
      message: canonicalMemory.present
        ? 'MEMORY.md is present as the canonical deliverable-local working memory file.'
        : 'MEMORY.md is not present; requiredness remains visible without invalidating the folder.'
    })
  );

  if (fileNames.has(PROHIBITED_MEMORY_FILE)) {
    findings.push(
      buildFinding({
        deliverableId: input.deliverableId,
        deliverablePath: input.deliverablePath,
        fileName: PROHIBITED_MEMORY_FILE,
        category: 'prohibited_file',
        condition: 'prohibited_memory_file',
        lifecycleState,
        severity: 'error',
        sourceRef: 'docs/SPEC.md#section-3.1; docs/SPEC.md#section-5.4',
        evidence: `${PROHIBITED_MEMORY_FILE} found in deliverable directory listing`,
        message: '_MEMORY.md is prohibited for this project profile; use MEMORY.md.'
      })
    );
  }

  for (const file of optionalFiles) {
    if (file.present) {
      findings.push(
        buildFinding({
          deliverableId: input.deliverableId,
          deliverablePath: input.deliverablePath,
          fileName: file.fileName,
          category: 'optional_file',
          condition: 'optional_file_present',
          lifecycleState,
          severity: 'info',
          sourceRef: 'docs/SPEC.md#section-3.1; docs/PRD.md#section-10.8',
          evidence: `${file.fileName} found in deliverable directory listing`,
          message: `${file.fileName} is recognized as an optional deliverable-local file.`
        })
      );
    }
  }

  if (fileNames.has('HASH_VERIFICATION_BYPASS.jsonl')) {
    findings.push(
      buildFinding({
        deliverableId: input.deliverableId,
        deliverablePath: input.deliverablePath,
        fileName: 'HASH_VERIFICATION_BYPASS.jsonl',
        category: 'source_hash_warning',
        condition: 'hash_verification_bypass_present',
        lifecycleState,
        severity: 'warning',
        sourceRef: 'docs/SPEC.md#section-3.1',
        evidence: 'HASH_VERIFICATION_BYPASS.jsonl found in deliverable directory listing',
        message: 'A durable hash-verification bypass record is present and must remain visible.'
      })
    );
  }

  if (fileNames.has('_REFERENCES.md')) {
    try {
      const referencesContent = await readFile(path.join(input.deliverablePath, '_REFERENCES.md'), 'utf8');
      addReferenceWarnings({
        deliverableId: input.deliverableId,
        deliverablePath: input.deliverablePath,
        lifecycleState,
        referencesContent,
        findings
      });
    } catch (error) {
      const message = error instanceof Error ? error.message : 'Unable to read _REFERENCES.md';
      findings.push(
        buildFinding({
          deliverableId: input.deliverableId,
          deliverablePath: input.deliverablePath,
          fileName: '_REFERENCES.md',
          category: 'unknown_unsupported_condition',
          condition: 'reference_read_failed',
          lifecycleState,
          severity: 'warning',
          sourceRef: '_REFERENCES.md',
          evidence: message,
          message: '_REFERENCES.md is present but could not be scanned for source-state warnings.'
        })
      );
    }
  }

  const errorCount = countFindings(findings, 'error');
  const warningCount = countFindings(findings, 'warning');
  const infoCount = countFindings(findings, 'info');
  const hasSelectableProductionFormat = documentFormat === 'LEGACY_FOUR_DOC'
    || documentFormat === 'SOW_V1'
    || documentFormat === 'MIGRATION_DUAL';
  const selectedProductionDocuments = documentFormat === 'LEGACY_FOUR_DOC'
    ? documentKit
    : documentFormat === 'SOW_V1' || documentFormat === 'MIGRATION_DUAL'
      ? [scopeOfWork]
      : [];

  return {
    deliverableId: input.deliverableId,
    path: input.deliverablePath,
    lifecycleState,
    valid: hasSelectableProductionFormat && errorCount === 0,
    errorCount,
    warningCount,
    infoCount,
    requiredMetadata,
    preparationBaseline,
    documentKit,
    documentFormat,
    selectedProductionDocuments,
    scopeOfWork,
    canonicalMemory,
    optionalFiles,
    findings
  };
}

function buildKnowledgeTypeOptions(
  rows: Array<{ key: string; fileNames: Set<string> }>,
  includeScopeOfWork = false
): KnowledgeTypeOption[] {
  const buckets = includeScopeOfWork
    ? KNOWLEDGE_TYPE_BUCKETS
    : KNOWLEDGE_TYPE_BUCKETS.filter((bucket) => bucket.id !== 'scope-of-work');
  const byBucket = new Map<string, { label: string; keys: Set<string> }>();

  for (const bucket of buckets) {
    byBucket.set(bucket.id, {
      label: bucket.label,
      keys: new Set<string>()
    });
  }

  for (const row of rows) {
    for (const bucket of buckets) {
      if (bucket.matches(row.fileNames)) {
        byBucket.get(bucket.id)?.keys.add(row.key);
      }
    }
  }

  return buckets.map((bucket) => {
    const entry = byBucket.get(bucket.id);
    return {
      id: bucket.id,
      label: bucket.label,
      matchingDeliverableKeys: [...(entry?.keys ?? new Set<string>())].sort((a, b) =>
        a.localeCompare(b)
      )
    };
  }).filter((entry) => entry.matchingDeliverableKeys.length > 0);
}

async function detectKnowledgeMarkerFile(projectRoot: string): Promise<string | null> {
  const decompositionDirectory = path.join(projectRoot, '_Decomposition');

  try {
    const entries = await readdir(decompositionDirectory, { withFileTypes: true });
    const sortedFiles = entries
      .filter((entry) => entry.isFile() && /\.md$/i.test(entry.name))
      .map((entry) => entry.name)
      .sort((a, b) => a.localeCompare(b));

    for (const fileName of sortedFiles) {
      const filePath = path.join(decompositionDirectory, fileName);
      try {
        const content = await readFile(filePath, 'utf8');
        if (
          KNOWLEDGE_MARKER_PATTERNS.some((pattern) => pattern.test(content)) ||
          /domain/i.test(fileName)
        ) {
          return filePath;
        }
      } catch {
        continue;
      }
    }

    return null;
  } catch {
    return null;
  }
}

export async function scanProjectScopes(projectRoot: string): Promise<ScopeScanResult> {
  const deliverables: ScopeItem[] = [];
  const knowledgeTypes: ScopeItem[] = [];
  const visited = new Set<string>();
  let scannedCount = 0;
  let truncated = false;

  async function walk(currentPath: string, depth: number): Promise<void> {
    if (truncated || depth > 8) {
      return;
    }

    if (visited.has(currentPath)) {
      return;
    }
    visited.add(currentPath);

    scannedCount += 1;
    if (scannedCount > MAX_SCOPE_SCAN_DIRECTORIES) {
      truncated = true;
      return;
    }

    let entries;
    try {
      entries = await readdir(currentPath, { withFileTypes: true });
    } catch {
      return;
    }

    const hasStatusFile = entries.some((entry) => entry.isFile() && entry.name === '_STATUS.md');
    const folderName = path.basename(currentPath);

    if (hasStatusFile && isDeliverableDirectory(folderName)) {
      const { id, label } = splitStableId(folderName);
      deliverables.push({ id, label, path: currentPath });
    }

    if (hasStatusFile && isKnowledgeTypeDirectory(folderName)) {
      const { id, label } = splitStableId(folderName);
      knowledgeTypes.push({ id, label, path: currentPath });
    }

    if (depth >= 8) {
      return;
    }

    const childDirectories = entries
      .filter((entry) => entry.isDirectory())
      .filter((entry) => !SKIP_DIRECTORY_NAMES.has(entry.name))
      .sort(compareDirectoryEntries);

    for (const entry of childDirectories) {
      await walk(path.join(currentPath, entry.name), depth + 1);
      if (truncated) {
        return;
      }
    }
  }

  await walk(projectRoot, 0);

  const sortById = (a: ScopeItem, b: ScopeItem): number => a.id.localeCompare(b.id);
  deliverables.sort(sortById);
  knowledgeTypes.sort(sortById);

  return {
    deliverables,
    knowledgeTypes,
    hasKnowledgeDecomposition: (await detectKnowledgeMarkerFile(projectRoot)) !== null,
    truncated
  };
}

export async function scanProjectDeliverables(
  projectRoot: string,
  options: {
    scopeOfWorkMigration?: ScopeOfWorkMigrationActivation;
    requestedFormat?: DeliverableProductionFormat | 'AUTO';
  } = {}
): Promise<ProjectDeliverablesScanResult> {
  const deliverables: ProjectDeliverable[] = [];
  const visited = new Set<string>();
  let scannedCount = 0;
  let truncated = false;

  async function walk(currentPath: string, depth: number): Promise<void> {
    if (truncated || depth > 8) {
      return;
    }
    if (visited.has(currentPath)) {
      return;
    }
    visited.add(currentPath);

    scannedCount += 1;
    if (scannedCount > MAX_SCOPE_SCAN_DIRECTORIES) {
      truncated = true;
      return;
    }

    let entries;
    try {
      entries = await readdir(currentPath, { withFileTypes: true });
    } catch {
      return;
    }

    const hasStatusFile = entries.some((entry) => entry.isFile() && entry.name === '_STATUS.md');
    const folderName = path.basename(currentPath);

    if (hasStatusFile && isDeliverableDirectory(folderName)) {
      const { id, label } = splitStableId(folderName);
      const pkg = getPackageFolderForDeliverable(projectRoot, currentPath);
      const status = await parseDeliverableStatus(currentPath);
      deliverables.push({
        id,
        name: label,
        pkg,
        status,
        path: currentPath
      });
    }

    if (depth >= 8) {
      return;
    }

    const childDirectories = entries
      .filter((entry) => entry.isDirectory())
      .filter((entry) => !SKIP_DIRECTORY_NAMES.has(entry.name))
      .sort(compareDirectoryEntries);

    for (const entry of childDirectories) {
      await walk(path.join(currentPath, entry.name), depth + 1);
      if (truncated) {
        return;
      }
    }
  }

  await walk(projectRoot, 0);

  deliverables.sort((a, b) => {
    const pkgCompare = a.pkg.localeCompare(b.pkg);
    if (pkgCompare !== 0) {
      return pkgCompare;
    }
    return a.id.localeCompare(b.id);
  });

  const knowledgeRows = await Promise.all(
    deliverables.map(async (deliverable) => ({
      key: buildDeliverableCompositeKey(deliverable.pkg, deliverable.id),
      fileNames: await readDirectoryFileSet(deliverable.path)
    }))
  );
  const deliverableContracts = await Promise.all(
    deliverables.map((deliverable) =>
      scanDeliverableDocumentKitContract({
        deliverableId: deliverable.id,
        deliverablePath: deliverable.path,
        scopeOfWorkMigration: options.scopeOfWorkMigration,
        requestedFormat: options.requestedFormat
      })
    )
  );
  const knowledgeMarkerFile = await detectKnowledgeMarkerFile(projectRoot);

  return {
    deliverables,
    deliverableContracts,
    knowledgeDecomposition: {
      enabled: knowledgeMarkerFile !== null,
      markerFile: knowledgeMarkerFile
    },
    knowledgeTypes: buildKnowledgeTypeOptions(knowledgeRows, true),
    truncated
  };
}

export function workspaceErrorPayload(error: unknown): {
  status: number;
  body: { error: { type: string; message: string; details?: unknown } };
} {
  if (error instanceof WorkspaceValidationError) {
    return {
      status: error.status,
      body: {
        error: {
          type: error.code,
          message: error.message
        }
      }
    };
  }

  if (error instanceof WorkspaceOperationError) {
    return {
      status: error.status,
      body: {
        error: {
          type: error.code,
          message: error.message,
          details: error.details
        }
      }
    };
  }

  const fallbackMessage = error instanceof Error ? error.message : 'Unexpected workspace failure';
  return {
    status: 500,
    body: {
      error: {
        type: 'WORKSPACE_FAILURE',
        message: fallbackMessage
      }
    }
  };
}
