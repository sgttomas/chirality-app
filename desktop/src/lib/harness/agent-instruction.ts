import { constants as fsConstants } from 'node:fs';
import { access, readFile } from 'node:fs/promises';
import path from 'node:path';
import { HarnessError } from '@chirality/runtime-contracts/errors';
import { assertInstructionRootReadable } from './instruction-root';

export type ParsedFrontmatter = Record<string, unknown>;
export type AgentClass = 'PERSONA' | 'TASK';
export type AgentInstructionSection = 'PROTOCOL' | 'SPEC' | 'STRUCTURE' | 'RATIONALE';

export type AgentInstructionConformanceIssueCode =
  | 'INVALID_AGENT_FILENAME'
  | 'MISSING_DOC_MARKER'
  | 'MISSING_TITLE'
  | 'MISSING_AGENT_TYPE'
  | 'MISSING_AGENT_TYPE_TABLE_ROW'
  | 'INVALID_AGENT_CLASS'
  | 'TYPE2_NON_TASK_CLASS'
  | 'MISSING_SECTION_MARKER'
  | 'MALFORMED_SECTION_MARKER_PAIR'
  | 'MISSING_WRITE_SCOPE'
  | 'UNKNOWN_WRITE_SCOPE'
  | 'UNKNOWN_FRONTMATTER_KEY';

export type AgentInstructionConformanceIssue = {
  severity: 'error' | 'warning';
  code: AgentInstructionConformanceIssueCode;
  message: string;
  field?: string;
};

export type AgentInstructionConformanceReport = {
  passed: boolean;
  issues: AgentInstructionConformanceIssue[];
};

export type AgentInstruction = {
  instructionRoot: string;
  path: string;
  content: string;
};

type ParseFrontmatterOptions = {
  warnPrefix?: string;
};

const REQUIRED_AGENT_TYPE_TABLE_FIELDS = [
  'AGENT_TYPE',
  'AGENT_CLASS',
  'INTERACTION_SURFACE',
  'WRITE_SCOPE',
  'BLOCKING',
  'PRIMARY_OUTPUTS'
] as const;

const REQUIRED_AGENT_INSTRUCTION_SECTIONS = [
  'PROTOCOL',
  'SPEC',
  'STRUCTURE',
  'RATIONALE'
] as const satisfies readonly AgentInstructionSection[];

const ALLOWED_AGENT_FRONTMATTER_KEYS = new Set([
  'description',
  'subagents',
  'tools',
  'model',
  'max_turns',
  'disallowed_tools',
  'auto_approve_tools',
  'allow_generalist_agent2',
  'dedicated_agent2_approval'
]);

const ALLOWED_WRITE_SCOPES = new Set([
  'repo-wide',
  'project-level',
  'package-level',
  'bounded-task-brief',
  'deliverable-local',
  'tool-root-only',
  'workspace-scaffold-only',
  'repo-metadata-only',
  'none'
]);

function normalizeAgentName(agentName: string): string {
  return agentName.trim().replace(/-/g, '_');
}

function normalizeMarkdown(markdown: string): string {
  return markdown.replace(/\r\n/g, '\n');
}

function parseYamlScalar(raw: string): unknown {
  const value = raw.trim();
  if (!value) {
    return '';
  }
  if (
    (value.startsWith('"') && value.endsWith('"')) ||
    (value.startsWith("'") && value.endsWith("'"))
  ) {
    return value.slice(1, -1);
  }
  if (value === 'true') {
    return true;
  }
  if (value === 'false') {
    return false;
  }
  if (/^-?\d+$/.test(value)) {
    const parsed = Number.parseInt(value, 10);
    if (Number.isSafeInteger(parsed)) {
      return parsed;
    }
  }
  return value;
}

function parseYamlInlineList(raw: string): string[] {
  const inner = raw.slice(1, -1).trim();
  if (!inner) {
    return [];
  }
  return inner
    .split(',')
    .map((item) => {
      const parsed = parseYamlScalar(item);
      return typeof parsed === 'string' ? parsed.trim() : '';
    })
    .filter((item) => item.length > 0);
}

export function parseFrontmatter(
  markdown: string,
  options?: ParseFrontmatterOptions
): ParsedFrontmatter {
  const normalized = normalizeMarkdown(markdown);
  if (!normalized.startsWith('---\n')) {
    return {};
  }

  const closingIndex = normalized.indexOf('\n---\n', 4);
  if (closingIndex === -1) {
    if (options?.warnPrefix) {
      console.warn(
        `${options.warnPrefix} Ignoring malformed persona frontmatter: missing closing delimiter.`
      );
    }
    return {};
  }

  const block = normalized.slice(4, closingIndex);
  const result: ParsedFrontmatter = {};
  let activeListKey: string | undefined;

  for (const rawLine of block.split('\n')) {
    const trimmed = rawLine.trim();
    if (!trimmed || trimmed.startsWith('#')) {
      continue;
    }

    const keyMatch = trimmed.match(/^([a-zA-Z0-9_]+):(.*)$/);
    if (keyMatch) {
      const key = keyMatch[1];
      const trailing = keyMatch[2].trim();
      if (!trailing) {
        result[key] = [];
        activeListKey = key;
      } else if (trailing.startsWith('[') && trailing.endsWith(']')) {
        result[key] = parseYamlInlineList(trailing);
        activeListKey = undefined;
      } else {
        result[key] = parseYamlScalar(trailing);
        activeListKey = undefined;
      }
      continue;
    }

    if (activeListKey && trimmed.startsWith('-')) {
      const list = Array.isArray(result[activeListKey]) ? result[activeListKey] : [];
      const nextValue = parseYamlScalar(trimmed.slice(1).trim());
      if (typeof nextValue === 'string' && nextValue.trim().length > 0) {
        (list as unknown[]).push(nextValue.trim());
      }
      result[activeListKey] = list;
      continue;
    }

    activeListKey = undefined;
  }

  return result;
}

export function asNonEmptyString(value: unknown): string | undefined {
  if (typeof value !== 'string') {
    return undefined;
  }
  const trimmed = value.trim();
  return trimmed.length > 0 ? trimmed : undefined;
}

export function asStringArray(value: unknown): string[] | undefined {
  if (!Array.isArray(value)) {
    return undefined;
  }

  const normalized: string[] = [];
  for (const item of value) {
    if (typeof item !== 'string') {
      return undefined;
    }
    const trimmed = item.trim();
    if (trimmed.length > 0) {
      normalized.push(trimmed);
    }
  }

  return normalized;
}

export function parseCommaSeparatedList(value: unknown): string[] {
  if (Array.isArray(value)) {
    return value
      .filter((item): item is string => typeof item === 'string')
      .map((item) => item.trim())
      .filter((item) => item.length > 0);
  }
  if (typeof value !== 'string') {
    return [];
  }
  return value
    .split(',')
    .map((item) => item.trim())
    .filter((item) => item.length > 0);
}

function extractAgentClass(value: string): AgentClass | undefined {
  const normalized = value.trim().toUpperCase();
  if (normalized.startsWith('TASK')) {
    return 'TASK';
  }
  if (normalized.startsWith('PERSONA')) {
    return 'PERSONA';
  }
  return undefined;
}

export function parseAgentType(content: string): number | undefined {
  const bodyHeaderMatch = content.match(/^\s*AGENT_TYPE:\s*(?:TYPE\s*)?([0-2])\b/m);
  if (bodyHeaderMatch?.[1]) {
    return Number.parseInt(bodyHeaderMatch[1], 10);
  }

  const tableMatch = content.match(/^\|\s*\*\*AGENT_TYPE\*\*\s*\|\s*TYPE\s*([0-2])\s*\|/im);
  if (tableMatch?.[1]) {
    return Number.parseInt(tableMatch[1], 10);
  }

  return undefined;
}

export function parseAgentClass(content: string): AgentClass | undefined {
  const bodyHeaderMatch = content.match(/^\s*AGENT_CLASS:\s*([^\n]+)/im);
  if (bodyHeaderMatch?.[1]) {
    return extractAgentClass(bodyHeaderMatch[1]);
  }

  const tableMatch = content.match(/^\|\s*\*\*AGENT_CLASS\*\*\s*\|\s*([^|]+)\|/im);
  if (tableMatch?.[1]) {
    return extractAgentClass(tableMatch[1]);
  }

  return undefined;
}

function extractAgentTypeTableRows(content: string): Map<string, string> {
  const rows = new Map<string, string>();
  const normalized = normalizeMarkdown(content);
  const rowPattern = /^\|\s*\*\*([A-Z_]+)\*\*\s*\|\s*([^|]*)\|/gm;
  let match: RegExpExecArray | null;

  while ((match = rowPattern.exec(normalized)) !== null) {
    rows.set(match[1], match[2].trim());
  }

  return rows;
}

function addIssue(
  issues: AgentInstructionConformanceIssue[],
  issue: AgentInstructionConformanceIssue
): void {
  issues.push(issue);
}

function validateInstructionSections(
  content: string,
  requiredSections: readonly AgentInstructionSection[],
  issues: AgentInstructionConformanceIssue[]
): void {
  for (const section of requiredSections) {
    const begin = `[[BEGIN:${section}]]`;
    const end = `[[END:${section}]]`;
    const beginIndex = content.indexOf(begin);
    const endIndex = content.indexOf(end);

    if (beginIndex === -1 || endIndex === -1) {
      addIssue(issues, {
        severity: 'error',
        code: 'MISSING_SECTION_MARKER',
        field: section,
        message: `Agent instruction is missing required ${section} marker pair.`
      });
      continue;
    }

    if (beginIndex > endIndex) {
      addIssue(issues, {
        severity: 'error',
        code: 'MALFORMED_SECTION_MARKER_PAIR',
        field: section,
        message: `Agent instruction has ${section} end marker before begin marker.`
      });
    }
  }
}

export function validateAgentInstructionConformance(input: {
  content: string;
  fileName?: string;
  requiredSections?: readonly AgentInstructionSection[];
}): AgentInstructionConformanceReport {
  const content = normalizeMarkdown(input.content);
  const issues: AgentInstructionConformanceIssue[] = [];
  const requiredSections = input.requiredSections ?? REQUIRED_AGENT_INSTRUCTION_SECTIONS;

  if (input.fileName && !/^AGENT_.+\.md$/.test(path.basename(input.fileName))) {
    addIssue(issues, {
      severity: 'error',
      code: 'INVALID_AGENT_FILENAME',
      message: 'Agent instruction files must use the AGENT_*.md naming convention.'
    });
  }

  if (!content.includes('[[DOC:AGENT_INSTRUCTIONS]]')) {
    addIssue(issues, {
      severity: 'error',
      code: 'MISSING_DOC_MARKER',
      message: 'Agent instruction is missing [[DOC:AGENT_INSTRUCTIONS]].'
    });
  }

  if (!/^#\s+AGENT INSTRUCTIONS\s+(?:-|\u2014)\s+\S+/m.test(content)) {
    addIssue(issues, {
      severity: 'error',
      code: 'MISSING_TITLE',
      message: 'Agent instruction is missing the required AGENT INSTRUCTIONS title.'
    });
  }

  const agentType = parseAgentType(content);
  if (agentType === undefined) {
    addIssue(issues, {
      severity: 'error',
      code: 'MISSING_AGENT_TYPE',
      field: 'AGENT_TYPE',
      message: 'Agent instruction is missing a valid AGENT_TYPE declaration.'
    });
  }

  const tableRows = extractAgentTypeTableRows(content);
  for (const field of REQUIRED_AGENT_TYPE_TABLE_FIELDS) {
    if (!tableRows.get(field)) {
      addIssue(issues, {
        severity: 'error',
        code: 'MISSING_AGENT_TYPE_TABLE_ROW',
        field,
        message: `Agent Type table is missing required ${field} row.`
      });
    }
  }

  const agentClass = parseAgentClass(content);
  if (!agentClass) {
    addIssue(issues, {
      severity: 'error',
      code: 'INVALID_AGENT_CLASS',
      field: 'AGENT_CLASS',
      message: 'Agent instruction is missing a valid AGENT_CLASS value.'
    });
  } else if (agentType === 2 && agentClass !== 'TASK') {
    addIssue(issues, {
      severity: 'warning',
      code: 'TYPE2_NON_TASK_CLASS',
      field: 'AGENT_CLASS',
      message: 'AGENT_TYPE 2 candidates should declare AGENT_CLASS TASK.'
    });
  }

  const writeScope = tableRows.get('WRITE_SCOPE');
  if (!writeScope) {
    addIssue(issues, {
      severity: 'error',
      code: 'MISSING_WRITE_SCOPE',
      field: 'WRITE_SCOPE',
      message: 'Agent Type table is missing an explicit WRITE_SCOPE value.'
    });
  } else if (!ALLOWED_WRITE_SCOPES.has(writeScope)) {
    addIssue(issues, {
      severity: 'warning',
      code: 'UNKNOWN_WRITE_SCOPE',
      field: 'WRITE_SCOPE',
      message: `WRITE_SCOPE '${writeScope}' is not in the canonical TYPES.md write-scope vocabulary.`
    });
  }

  validateInstructionSections(content, requiredSections, issues);

  const frontmatter = parseFrontmatter(content);
  for (const key of Object.keys(frontmatter)) {
    if (!ALLOWED_AGENT_FRONTMATTER_KEYS.has(key)) {
      addIssue(issues, {
        severity: 'warning',
        code: 'UNKNOWN_FRONTMATTER_KEY',
        field: key,
        message: `Unknown agent frontmatter key '${key}' is ignored by runtime policy.`
      });
    }
  }

  return {
    passed: !issues.some((issue) => issue.severity === 'error'),
    issues
  };
}

function getAgentInstructionPath(agentName: string, instructionRoot: string): string {
  return path.join(instructionRoot, 'agents', `AGENT_${normalizeAgentName(agentName)}.md`);
}

async function resolveInstructionRoot(
  instructionRootOverride?: string
): Promise<string> {
  if (instructionRootOverride) {
    return path.resolve(instructionRootOverride);
  }
  return assertInstructionRootReadable();
}

export async function readAgentInstruction(
  agentName: string,
  instructionRootOverride?: string
): Promise<AgentInstruction> {
  const instructionRoot = await resolveInstructionRoot(instructionRootOverride);
  const candidate = getAgentInstructionPath(agentName, instructionRoot);

  try {
    await access(candidate, fsConstants.R_OK);
  } catch {
    throw new HarnessError('PERSONA_NOT_FOUND', 404, `Persona '${agentName}' was not found`, {
      persona: agentName,
      instructionRoot
    });
  }

  const content = await readFile(candidate, 'utf8');
  return {
    instructionRoot,
    path: candidate,
    content
  };
}

export async function tryReadAgentInstruction(
  agentName: string,
  instructionRootOverride?: string
): Promise<AgentInstruction | undefined> {
  try {
    return await readAgentInstruction(agentName, instructionRootOverride);
  } catch (error) {
    if (error instanceof HarnessError && error.type === 'PERSONA_NOT_FOUND') {
      return undefined;
    }
    throw error;
  }
}
