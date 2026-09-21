import {
  LifecycleState,
  ParsedStatusDocument,
  StatusField,
  StatusHistoryEntry,
  parseLifecycleState,
  parseStatusDocument
} from './status-parser';

const ISO_DATE_PATTERN = /^\d{4}-\d{2}-\d{2}$/;

export interface StatusWriterInput {
  title: string;
  currentState: LifecycleState;
  lastUpdated: string;
  history: StatusHistoryEntry[];
  extraFields?: StatusField[];
}

export interface StatusUpdateInput {
  targetState: LifecycleState;
  actor: string;
  date?: string;
  metadata?: Record<string, string>;
}

function assertIsoDate(value: string, field: string): void {
  if (!ISO_DATE_PATTERN.test(value)) {
    throw new Error(`${field} must be YYYY-MM-DD`);
  }
}

function toFieldLabel(key: string): string {
  const withSpaces = key
    .trim()
    .replace(/[_-]+/g, ' ')
    .replace(/([a-z0-9])([A-Z])/g, '$1 $2');

  return withSpaces
    .split(/\s+/)
    .filter(Boolean)
    .map((part) => {
      const upper = part.toUpperCase();
      if (upper === 'SHA') {
        return 'SHA';
      }
      return part.charAt(0).toUpperCase() + part.slice(1).toLowerCase();
    })
    .join(' ');
}

function mergeFields(
  existing: StatusField[],
  metadata: Record<string, string> | undefined
): StatusField[] {
  if (!metadata) {
    return existing;
  }

  const merged = [...existing];
  for (const [key, value] of Object.entries(metadata)) {
    const trimmedValue = value.trim();
    if (!trimmedValue) {
      continue;
    }

    const label = toFieldLabel(key);
    const existingIndex = merged.findIndex(
      (field) => field.key.trim().toLowerCase() === label.toLowerCase()
    );

    if (existingIndex >= 0) {
      merged[existingIndex] = { key: label, value: trimmedValue };
      continue;
    }

    merged.push({ key: label, value: trimmedValue });
  }

  return merged;
}

function formatHistoryEntry(entry: StatusHistoryEntry): string {
  const actor = entry.actor.trim() || 'UNKNOWN';
  const notesSuffix = entry.notes?.trim() ? ` [${entry.notes.trim()}]` : '';
  return `- ${entry.date} - State set to ${entry.state} (${actor})${notesSuffix}`;
}

export function writeStatusDocument(input: StatusWriterInput): string {
  parseLifecycleState(input.currentState);
  assertIsoDate(input.lastUpdated, 'Last Updated');

  const normalizedHistory = [...input.history];
  for (const entry of normalizedHistory) {
    parseLifecycleState(entry.state);
    assertIsoDate(entry.date, 'History date');
  }

  const lines: string[] = [];
  lines.push(`# ${input.title.trim()}`);
  lines.push('');
  lines.push(`**Current State:** ${input.currentState}`);
  lines.push(`**Last Updated:** ${input.lastUpdated}`);

  for (const field of input.extraFields ?? []) {
    const key = field.key.trim();
    if (!key || !field.value.trim()) {
      continue;
    }
    lines.push(`**${key}:** ${field.value.trim()}`);
  }

  lines.push('');
  lines.push('## History');
  if (normalizedHistory.length === 0) {
    lines.push('-');
  } else {
    lines.push(...normalizedHistory.map(formatHistoryEntry));
  }
  lines.push('');

  return lines.join('\n');
}

export function updateStatusDocument(
  content: string,
  input: StatusUpdateInput
): { content: string; parsed: ParsedStatusDocument } {
  const parsed = parseStatusDocument(content);
  const targetState = parseLifecycleState(input.targetState);
  const actor = input.actor.trim() || 'UNKNOWN';
  const date = input.date?.trim() || new Date().toISOString().slice(0, 10);
  assertIsoDate(date, 'Transition date');

  const nextHistory: StatusHistoryEntry[] = [
    ...parsed.history,
    {
      date,
      state: targetState,
      actor,
      source: 'list',
      raw: ''
    }
  ];

  const nextFields = mergeFields(parsed.extraFields, input.metadata);

  const nextContent = writeStatusDocument({
    title: parsed.title,
    currentState: targetState,
    lastUpdated: date,
    history: nextHistory,
    extraFields: nextFields
  });

  return {
    content: nextContent,
    parsed: parseStatusDocument(nextContent)
  };
}
