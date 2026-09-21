import type { HarnessOpts } from '@chirality/runtime-contracts/types';

export const TOOLKIT_STORAGE_KEY = 'chirality.toolkit.v1';

// The model and reasoning effort are chosen per session from the authenticated
// Codex catalog in the chat panel; the toolkit carries no free-text `opts.model`
// so the session record stays the single source of truth.
export type ToolkitValues = {
  tools: string;
  maxTurns: string;
  includeSubagentGovernance: boolean;
  contextSealed: boolean;
  pipelineRunApproved: boolean;
  approvalRef: string;
};

export type ToolkitPreset = {
  id: string;
  name: string;
  values: ToolkitValues;
  createdAt: string;
  updatedAt: string;
};

export type ToolkitState = {
  visible: boolean;
  values: ToolkitValues;
  presets: ToolkitPreset[];
  selectedPresetId: string | null;
};

const MAX_PRESET_COUNT = 25;

export function defaultToolkitValues(): ToolkitValues {
  return {
    tools: '',
    maxTurns: '',
    includeSubagentGovernance: false,
    contextSealed: false,
    pipelineRunApproved: false,
    approvalRef: ''
  };
}

export function defaultToolkitState(): ToolkitState {
  return {
    visible: false,
    values: defaultToolkitValues(),
    presets: [],
    selectedPresetId: null
  };
}

function readString(value: unknown): string {
  if (typeof value !== 'string') {
    return '';
  }
  return value.trim();
}

function readBoolean(value: unknown): boolean {
  return value === true;
}

function sanitizeToolkitValues(value: unknown): ToolkitValues {
  if (!value || typeof value !== 'object') {
    return defaultToolkitValues();
  }

  const record = value as Record<string, unknown>;
  return {
    tools: readString(record.tools),
    maxTurns: readString(record.maxTurns),
    includeSubagentGovernance: readBoolean(record.includeSubagentGovernance),
    contextSealed: readBoolean(record.contextSealed),
    pipelineRunApproved: readBoolean(record.pipelineRunApproved),
    approvalRef: readString(record.approvalRef)
  };
}

function sanitizePreset(value: unknown): ToolkitPreset | null {
  if (!value || typeof value !== 'object') {
    return null;
  }

  const record = value as Record<string, unknown>;
  const id = readString(record.id);
  const name = readString(record.name);
  if (!id || !name) {
    return null;
  }

  const createdAt = readString(record.createdAt) || new Date(0).toISOString();
  const updatedAt = readString(record.updatedAt) || createdAt;

  return {
    id,
    name,
    values: sanitizeToolkitValues(record.values),
    createdAt,
    updatedAt
  };
}

export function sanitizeToolkitState(value: unknown): ToolkitState {
  if (!value || typeof value !== 'object') {
    return defaultToolkitState();
  }

  const record = value as Record<string, unknown>;
  const rawPresets = Array.isArray(record.presets) ? record.presets : [];
  const presets = rawPresets
    .map((entry) => sanitizePreset(entry))
    .filter((entry): entry is ToolkitPreset => Boolean(entry))
    .slice(0, MAX_PRESET_COUNT);

  const selectedPresetId = readString(record.selectedPresetId) || null;
  const selectedExists = selectedPresetId
    ? presets.some((preset) => preset.id === selectedPresetId)
    : false;

  return {
    visible: readBoolean(record.visible),
    values: sanitizeToolkitValues(record.values),
    presets,
    selectedPresetId: selectedExists ? selectedPresetId : null
  };
}

function splitTools(tools: string): string[] {
  return tools
    .split(/[\n,]/)
    .map((item) => item.trim())
    .filter((item) => item.length > 0);
}

export function buildHarnessOptsFromToolkit(values: ToolkitValues): HarnessOpts | undefined {
  const tools = splitTools(values.tools);
  const maxTurns = Number.parseInt(values.maxTurns, 10);

  const opts: HarnessOpts = {};

  if (tools.length > 0) {
    opts.tools = tools;
  }

  if (Number.isFinite(maxTurns) && maxTurns > 0) {
    opts.maxTurns = maxTurns;
  }

  if (values.includeSubagentGovernance) {
    const governance: Record<string, unknown> = {
      contextSealed: values.contextSealed,
      pipelineRunApproved: values.pipelineRunApproved
    };
    const approvalRef = values.approvalRef.trim();
    if (approvalRef) {
      governance.approvalRef = approvalRef;
    }
    opts.subagentGovernance = governance;
  }

  return Object.keys(opts).length > 0 ? opts : undefined;
}

export function createToolkitPreset(name: string, values: ToolkitValues, now = new Date()): ToolkitPreset {
  const timestamp = now.toISOString();
  const normalizedName = name.trim();
  return {
    id: `preset-${now.getTime()}-${Math.random().toString(16).slice(2, 8)}`,
    name: normalizedName,
    values: sanitizeToolkitValues(values),
    createdAt: timestamp,
    updatedAt: timestamp
  };
}

export function upsertToolkitPreset(
  existing: ToolkitPreset[],
  nextPreset: ToolkitPreset
): ToolkitPreset[] {
  const filtered = existing.filter((preset) => preset.id !== nextPreset.id);
  return [nextPreset, ...filtered].slice(0, MAX_PRESET_COUNT);
}
