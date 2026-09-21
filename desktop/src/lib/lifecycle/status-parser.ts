const ISO_DATE_PATTERN = /^\d{4}-\d{2}-\d{2}$/;

export const LIFECYCLE_STATES = [
  'OPEN',
  'INITIALIZED',
  'SEMANTIC_READY',
  'IN_PROGRESS',
  'CHECKING',
  'ISSUED'
] as const;

const LIFECYCLE_STATE_SET = new Set<string>(LIFECYCLE_STATES);

export type LifecycleState = (typeof LIFECYCLE_STATES)[number];

export type StatusHistoryEntrySource = 'list' | 'table';

export interface StatusHistoryEntry {
  date: string;
  state: LifecycleState;
  actor: string;
  source: StatusHistoryEntrySource;
  fromState?: string;
  notes?: string;
  raw: string;
}

export interface StatusField {
  key: string;
  value: string;
}

export interface ParsedStatusDocument {
  title: string;
  currentState: LifecycleState;
  lastUpdated: string;
  history: StatusHistoryEntry[];
  extraFields: StatusField[];
}

export type StatusParseErrorCode =
  | 'INVALID_STATUS_FORMAT'
  | 'INVALID_STATE'
  | 'INVALID_DATE';

export class StatusParseError extends Error {
  readonly code: StatusParseErrorCode;
  readonly details?: unknown;

  constructor(code: StatusParseErrorCode, message: string, details?: unknown) {
    super(message);
    this.name = 'StatusParseError';
    this.code = code;
    this.details = details;
  }
}

function assertIsoDate(value: string, field: string): void {
  if (!ISO_DATE_PATTERN.test(value.trim())) {
    throw new StatusParseError('INVALID_DATE', `${field} must be YYYY-MM-DD`, { field, value });
  }
}

export function parseLifecycleState(value: string): LifecycleState {
  const normalized = value.trim().toUpperCase();
  if (!LIFECYCLE_STATE_SET.has(normalized)) {
    throw new StatusParseError('INVALID_STATE', `Unsupported lifecycle state '${value}'`, { value });
  }
  return normalized as LifecycleState;
}

function findRequiredLine(content: string, pattern: RegExp, errorMessage: string): string {
  const match = content.match(pattern);
  if (!match || !match[1]) {
    throw new StatusParseError('INVALID_STATUS_FORMAT', errorMessage);
  }
  return match[1].trim();
}

function parseListHistory(historyLines: string[]): StatusHistoryEntry[] {
  const entries: StatusHistoryEntry[] = [];
  const entryPattern =
    /^-\s*(\d{4}-\d{2}-\d{2})\s*(?:-|—)\s*State set to\s+([A-Za-z_]+)\s+\(([^)]+)\)(?:\s+\[(.+)\])?\s*$/;

  for (const line of historyLines) {
    const trimmed = line.trim();
    if (!trimmed.startsWith('-')) {
      continue;
    }

    const match = trimmed.match(entryPattern);
    if (!match) {
      continue;
    }

    const [, date, stateRaw, actor, notes] = match;
    assertIsoDate(date, 'History date');
    const state = parseLifecycleState(stateRaw);
    entries.push({
      date,
      state,
      actor: actor.trim(),
      notes: notes?.trim(),
      source: 'list',
      raw: line
    });
  }

  return entries;
}

function parseMarkdownTableLine(line: string): string[] {
  const trimmed = line.trim();
  if (!trimmed.startsWith('|') || !trimmed.endsWith('|')) {
    return [];
  }
  return trimmed
    .slice(1, -1)
    .split('|')
    .map((cell) => cell.trim());
}

function parseTableHistory(historyLines: string[]): StatusHistoryEntry[] {
  const tableLines = historyLines.filter((line) => line.trim().startsWith('|'));
  if (tableLines.length === 0) {
    return [];
  }

  const rows = tableLines
    .map(parseMarkdownTableLine)
    .filter((cells) => cells.length >= 5);

  if (rows.length <= 1) {
    return [];
  }

  const entries: StatusHistoryEntry[] = [];
  for (const cells of rows) {
    const [date, fromState, toState, actor, notes] = cells;
    const lowerDate = date.toLowerCase();
    const separatorRow = cells.every((value) => /^:?-{2,}:?$/.test(value));
    if (lowerDate === 'date' || separatorRow) {
      continue;
    }

    assertIsoDate(date, 'History date');
    const normalizedToState = parseLifecycleState(toState);
    entries.push({
      date,
      state: normalizedToState,
      actor: actor.trim(),
      fromState: fromState.trim(),
      notes: notes.trim(),
      source: 'table',
      raw: `|${cells.join('|')}|`
    });
  }

  return entries;
}

function getHistoryLines(content: string): string[] {
  const lines = content.split(/\r?\n/);
  const historyIndex = lines.findIndex((line) => /^##\s+History\s*$/.test(line.trim()));
  if (historyIndex < 0) {
    throw new StatusParseError('INVALID_STATUS_FORMAT', "Missing '## History' section");
  }

  let nextHeadingIndex = lines.length;
  for (let index = historyIndex + 1; index < lines.length; index += 1) {
    if (/^##\s+/.test(lines[index].trim())) {
      nextHeadingIndex = index;
      break;
    }
  }

  return lines.slice(historyIndex + 1, nextHeadingIndex);
}

function parseHistory(content: string): StatusHistoryEntry[] {
  const historyLines = getHistoryLines(content);
  const listEntries = parseListHistory(historyLines);
  if (listEntries.length > 0) {
    return listEntries;
  }

  const tableEntries = parseTableHistory(historyLines);
  if (tableEntries.length > 0) {
    return tableEntries;
  }

  return [];
}

function parseExtraFields(content: string): StatusField[] {
  const fields: StatusField[] = [];
  const fieldPattern = /^\*\*([^*]+):\*\*\s*(.*?)\s*$/gm;

  for (const match of content.matchAll(fieldPattern)) {
    const key = match[1]?.trim() ?? '';
    const value = match[2]?.trim() ?? '';
    const normalizedKey = key.toLowerCase();
    if (normalizedKey === 'current state' || normalizedKey === 'last updated') {
      continue;
    }
    fields.push({ key, value });
  }

  return fields;
}

export function parseStatusDocument(content: string): ParsedStatusDocument {
  const title = findRequiredLine(content, /^#\s+(.+)\s*$/m, 'Missing status title heading');
  const currentStateRaw = findRequiredLine(
    content,
    /^\*\*Current State:\*\*\s*(.+?)\s*$/m,
    "Missing '**Current State:**' field"
  );
  const lastUpdated = findRequiredLine(
    content,
    /^\*\*Last Updated:\*\*\s*(.+?)\s*$/m,
    "Missing '**Last Updated:**' field"
  );

  const currentState = parseLifecycleState(currentStateRaw);
  assertIsoDate(lastUpdated, 'Last Updated');
  const history = parseHistory(content);
  const extraFields = parseExtraFields(content);

  return {
    title,
    currentState,
    lastUpdated,
    history,
    extraFields
  };
}
