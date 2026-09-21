/**
 * Governed workflow v1: derivative steering context, never an authority record.
 *
 * Strict Markdown grammar (not general YAML): exactly seven front-matter keys;
 * string values are JSON-quoted or plain single-line scalars. roadmapSource is
 * a block with exactly two indented scalars: identity and sha256. No comments,
 * YAML aliases, implicit types, multiline scalars, or extra fields are supported.
 * Body: consecutive `1. Text` / `2. [gate] Text` lines, then optional `current: n`
 * and `advancedBy: "human identity"`. Blank body lines are ignored. current is
 * one-based (omitted means 1); length + 1 means beyond the final human gate.
 * advancedBy is attribution only, never an approval/evidence record. acceptedAt
 * is source acceptance metadata, not proof of acceptance or an authorization.
 *
 * Vocabulary is supplied from the caller's live Agent 1 and setting registries;
 * this module cannot assign agent roles or grant permissions. Folder validation
 * is lexical POSIX validation for this macOS app. Callers must resolve/verify
 * real canonical roots, write containment, prerequisites, human identity and
 * acceptance of exact content before writing. Concurrent editing is unsupported:
 * a caller must reject stale content before applying an accepted transformation.
 */
export interface WorkflowVocabulary {
  agent1Roles: readonly string[];
  permissions: readonly string[];
  policies: readonly string[];
  briefsRunOn: readonly string[];
}

export interface RoadmapSource {
  identity: string;
  sha256: string;
}

export interface GovernedWorkflow {
  agent: string;
  folder: string;
  permission: string;
  policy: string;
  briefsRunOn: string;
  roadmapSource: RoadmapSource;
  acceptedAt: string;
  roadmap: { text: string; humanGate: boolean }[];
  current: number;
  advancedBy: string | null;
}

export class WorkflowContractError extends Error {
  constructor(message: string) {
    super(message);
    this.name = 'WorkflowContractError';
  }
}

function requireContract(condition: unknown, message: string): asserts condition {
  if (!condition) throw new WorkflowContractError(message);
}

function isRecord(value: unknown): value is Record<string, unknown> {
  return value !== null && typeof value === 'object' && !Array.isArray(value);
}

function exactKeys(value: Record<string, unknown>, keys: readonly string[], label: string) {
  requireContract(Object.keys(value).length === keys.length &&
    keys.every((key) => Object.hasOwn(value, key)), `${label}: missing or unknown field`);
}

function singleLine(value: unknown): value is string {
  return typeof value === 'string' && value.length > 0 && value === value.trim() &&
    !/[\u0000-\u001f\u007f\u2028\u2029]/u.test(value);
}

export function isCanonicalWorkflowFolder(value: unknown): value is string {
  return singleLine(value) && value.startsWith('/') && !value.includes('\\') &&
    (value === '/' || value.slice(1).split('/').every((part) => part !== '' && part !== '.' && part !== '..'));
}

function validateSource(value: unknown): asserts value is RoadmapSource {
  requireContract(isRecord(value), 'roadmapSource must be an object');
  exactKeys(value, ['identity', 'sha256'], 'roadmapSource');
  requireContract(singleLine(value.identity), 'roadmapSource identity required');
  requireContract(typeof value.sha256 === 'string' && /^[a-fA-F0-9]{64}$/.test(value.sha256),
    'roadmapSource requires a SHA256 hex digest');
}

/** Runtime validation is also applied to serializer/helper inputs; extra fields never disappear silently. */
export function validateGovernedWorkflow(value: unknown, vocabulary: WorkflowVocabulary): asserts value is GovernedWorkflow {
  requireContract(isRecord(value), 'workflow must be an object');
  exactKeys(value, ['agent', 'folder', 'permission', 'policy', 'briefsRunOn', 'roadmapSource',
    'acceptedAt', 'roadmap', 'current', 'advancedBy'], 'workflow');
  for (const [field, allowed] of [
    ['agent', vocabulary.agent1Roles], ['permission', vocabulary.permissions],
    ['policy', vocabulary.policies], ['briefsRunOn', vocabulary.briefsRunOn]
  ] as const) {
    requireContract(singleLine(value[field]) && allowed.includes(value[field] as string),
      `${field}: value is not in the supplied live vocabulary`);
  }
  requireContract(isCanonicalWorkflowFolder(value.folder), 'folder must be a canonical absolute POSIX path');
  validateSource(value.roadmapSource);
  // Exact UTC millisecond format avoids JS Date's permissive rollover parsing.
  requireContract(typeof value.acceptedAt === 'string' &&
    /^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{3}Z$/.test(value.acceptedAt) &&
    Number.isFinite(Date.parse(value.acceptedAt)) &&
    new Date(value.acceptedAt).toISOString() === value.acceptedAt,
  'acceptedAt must be an ISO UTC timestamp with milliseconds');
  requireContract(Array.isArray(value.roadmap) && value.roadmap.length > 0, 'roadmap must not be empty');
  for (const step of value.roadmap) {
    requireContract(isRecord(step), 'roadmap step must be an object');
    exactKeys(step, ['text', 'humanGate'], 'roadmap step');
    requireContract(singleLine(step.text) && !step.text.includes('[gate]') &&
      !/^\[(?: |x|X)\]/.test(step.text), 'roadmap text must be a single line without gate or status markers');
    requireContract(typeof step.humanGate === 'boolean', 'humanGate must be boolean');
  }
  requireContract(typeof value.current === 'number' && Number.isSafeInteger(value.current) &&
    value.current >= 1 && value.current <= value.roadmap.length + 1, 'current is out of range');
  if (value.current === 1) {
    requireContract(value.advancedBy === null, 'initial position must have no advance attribution');
  } else {
    requireContract(value.roadmap[value.current - 2].humanGate && singleLine(value.advancedBy),
      'advanced position must follow a human gate and identify who advanced it');
  }
}

function scalar(raw: string): string {
  requireContract(raw.length > 0, 'empty scalar');
  if (raw.startsWith('"')) {
    let decoded: unknown;
    try { decoded = JSON.parse(raw); } catch { throw new WorkflowContractError('invalid JSON-quoted scalar'); }
    requireContract(singleLine(decoded), 'invalid scalar');
    return decoded;
  }
  requireContract(singleLine(raw) && !/^[\[\]{}&*!>|'`@%#?\-]/.test(raw) &&
    !/^(?:null|true|false|~)$/i.test(raw) && !raw.includes(' #') && !raw.includes(': '),
  'unsupported plain scalar; use a JSON-quoted string');
  return raw;
}

export function parseGovernedWorkflow(content: string, vocabulary: WorkflowVocabulary): GovernedWorkflow {
  const lines = content.replace(/\r\n/g, '\n').split('\n');
  requireContract(lines[0] === '---', 'front matter must start on the first line');
  const end = lines.indexOf('---', 1);
  requireContract(end > 1, 'front matter is not closed');
  const metadata: Record<string, unknown> = {};
  const source: Record<string, unknown> = {};
  let inSource = false;
  for (const line of lines.slice(1, end)) {
    const nested = /^  (identity|sha256): (.+)$/.exec(line);
    if (nested && inSource) {
      requireContract(!Object.hasOwn(source, nested[1]), 'duplicate roadmapSource field');
      source[nested[1]] = scalar(nested[2]);
      continue;
    }
    const match = /^(agent|folder|permission|policy|briefsRunOn|roadmapSource|acceptedAt):(?: (.+))?$/.exec(line);
    requireContract(match, 'unknown or malformed front matter field');
    const [, key, raw] = match;
    requireContract(!Object.hasOwn(metadata, key), 'duplicate front matter field');
    inSource = key === 'roadmapSource';
    if (inSource) {
      requireContract(raw === undefined, 'roadmapSource must be an indented identity/sha256 block');
      metadata[key] = source;
    } else {
      requireContract(raw !== undefined, 'front matter value required');
      metadata[key] = scalar(raw);
    }
  }
  const roadmap: GovernedWorkflow['roadmap'] = [];
  let current = 1;
  let advancedBy: string | null = null;
  let seenCurrent = false;
  let seenAttribution = false;
  let positionStarted = false;
  for (const line of lines.slice(end + 1)) {
    if (line === '') continue;
    const step = /^([1-9]\d*)\. (\[gate\] )?(.+)$/.exec(line);
    if (step) {
      requireContract(!positionStarted && Number(step[1]) === roadmap.length + 1, 'roadmap must be consecutively ordered before position');
      roadmap.push({ text: step[3], humanGate: Boolean(step[2]) });
      continue;
    }
    positionStarted = true;
    const position = /^current: ([1-9]\d*)$/.exec(line);
    if (position) {
      requireContract(!seenCurrent && !seenAttribution, 'duplicate or misplaced current');
      seenCurrent = true;
      current = Number(position[1]);
      continue;
    }
    const attribution = /^advancedBy: (.+)$/.exec(line);
    requireContract(attribution && seenCurrent && !seenAttribution, 'unknown or malformed roadmap/position field');
    seenAttribution = true;
    advancedBy = scalar(attribution[1]);
  }
  const workflow = { ...metadata, roadmap, current, advancedBy };
  validateGovernedWorkflow(workflow, vocabulary);
  return workflow;
}

export function serializeGovernedWorkflow(workflow: GovernedWorkflow, vocabulary: WorkflowVocabulary): string {
  validateGovernedWorkflow(workflow, vocabulary);
  const quote = JSON.stringify;
  return [
    '---', `agent: ${quote(workflow.agent)}`, `folder: ${quote(workflow.folder)}`,
    `permission: ${quote(workflow.permission)}`, `policy: ${quote(workflow.policy)}`,
    `briefsRunOn: ${quote(workflow.briefsRunOn)}`, 'roadmapSource:',
    `  identity: ${quote(workflow.roadmapSource.identity)}`, `  sha256: ${quote(workflow.roadmapSource.sha256)}`,
    `acceptedAt: ${quote(workflow.acceptedAt)}`, '---', '',
    ...workflow.roadmap.map((step, index) => `${index + 1}. ${step.humanGate ? '[gate] ' : ''}${step.text}`),
    '', `current: ${workflow.current}`,
    ...(workflow.advancedBy === null ? [] : [`advancedBy: ${quote(workflow.advancedBy)}`]), ''
  ].join('\n');
}

/** First pending gate; ordinary steps do not independently advance stored position (Q16). */
export function nextWorkflowGate(workflow: GovernedWorkflow, vocabulary: WorkflowVocabulary): number | null {
  validateGovernedWorkflow(workflow, vocabulary);
  const index = workflow.roadmap.findIndex((step, i) => i >= workflow.current - 1 && step.humanGate);
  return index === -1 ? null : index + 1;
}

/** Pure content change only. Caller must authenticate the human and gate acceptance against exact content. */
export function advanceWorkflowAtGate(
  workflow: GovernedWorkflow, gate: number, humanIdentity: string, vocabulary: WorkflowVocabulary
): GovernedWorkflow {
  requireContract(nextWorkflowGate(workflow, vocabulary) === gate, 'only the next human gate can advance position');
  const next = { ...workflow, current: gate + 1, advancedBy: humanIdentity };
  validateGovernedWorkflow(next, vocabulary);
  // Return a detached value; callers cannot mutate the input through the result.
  return parseGovernedWorkflow(serializeGovernedWorkflow(next, vocabulary), vocabulary);
}

/** Bind retains accepted source metadata, resets position/attribution; never approves or writes the copy. */
export function bindWorkflowContent(content: string, destinationFolder: string, vocabulary: WorkflowVocabulary): string {
  const workflow = parseGovernedWorkflow(content, vocabulary);
  return serializeGovernedWorkflow({ ...workflow, folder: destinationFolder, current: 1, advancedBy: null }, vocabulary);
}

/** Compare caller-computed accepted source digests; no IO, mutation, or implicit re-acceptance. */
export function workflowSourceCurrency(source: RoadmapSource, available: RoadmapSource | null): 'current' | 'changed' | 'unavailable' {
  validateSource(source);
  if (available === null) return 'unavailable';
  validateSource(available);
  return source.identity === available.identity && source.sha256.toLowerCase() === available.sha256.toLowerCase()
    ? 'current' : 'changed';
}
