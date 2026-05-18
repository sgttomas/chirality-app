/**
 * Toolkit configuration module.
 *
 * Pure functions for building, validating, and persisting toolkit overrides.
 * No React dependency — testable independently.
 *
 * @module toolkit-config
 */

import type { TurnOpts, SubagentGovernance } from "@/lib/harness/types";

// ---------------------------------------------------------------------------
// Types
// ---------------------------------------------------------------------------

/**
 * Tri-state for includePartialMessages.
 *
 * - `"inherit"` — omit from TurnOpts (SDK/harness default applies)
 * - `true` / `false` — explicit override
 */
export type PartialMessagesSetting = "inherit" | boolean;

/**
 * Session-scoped toolkit overrides.
 *
 * Every field is optional. When `undefined`, the field is omitted from the
 * built `TurnOpts`, preserving persona/harness defaults.
 */
export interface ToolkitOverrides {
  // Tier A — safe, high value
  model?: string;
  maxTurns?: number;
  tools?: string;
  disallowedTools?: string[];
  autoApproveTools?: string[];
  includePartialMessages?: PartialMessagesSetting;

  // Tier C — restricted, validation-gated
  subagentGovernance?: SubagentGovernance;
}

export interface ToolkitPreset {
  id: string;
  name: string;
  createdAt: string;
  updatedAt: string;
  version: number;
  overrides: ToolkitOverrides;
}

export interface ToolkitValidationError {
  field: keyof ToolkitOverrides;
  message: string;
}

export interface ToolkitWarning {
  code: string;
  message: string;
}

// ---------------------------------------------------------------------------
// Constants
// ---------------------------------------------------------------------------

/** Identity element — no overrides active. */
export const EMPTY_OVERRIDES: Readonly<ToolkitOverrides> = Object.freeze({});

const PRESET_STORAGE_KEY = "toolkit_presets";
const PRESET_SCHEMA_VERSION = 1;
const MAX_PRESETS = 20;
const MAX_PRESET_NAME_LENGTH = 60;
const MAX_TURNS_UPPER = 200;

// ---------------------------------------------------------------------------
// Override introspection
// ---------------------------------------------------------------------------

/** Fields that count toward the active-override indicator. */
const COUNTABLE_FIELDS: (keyof ToolkitOverrides)[] = [
  "model",
  "maxTurns",
  "tools",
  "disallowedTools",
  "autoApproveTools",
  "includePartialMessages",
  "subagentGovernance",
];

function isFieldActive(overrides: ToolkitOverrides, field: keyof ToolkitOverrides): boolean {
  const value = overrides[field];
  if (value === undefined) return false;
  if (field === "includePartialMessages" && value === "inherit") return false;
  if (field === "disallowedTools" || field === "autoApproveTools") {
    return Array.isArray(value) && value.length > 0;
  }
  return true;
}

/** Returns `true` if any toolkit field has a non-default value. */
export function hasActiveOverrides(overrides: ToolkitOverrides): boolean {
  return COUNTABLE_FIELDS.some((field) => isFieldActive(overrides, field));
}

/** Counts how many toolkit fields have non-default values. */
export function countActiveOverrides(overrides: ToolkitOverrides): number {
  return COUNTABLE_FIELDS.filter((field) => isFieldActive(overrides, field)).length;
}

// ---------------------------------------------------------------------------
// Normalization helpers
// ---------------------------------------------------------------------------

/**
 * Normalizes a raw CSV tools string: trims whitespace, removes empties,
 * deduplicates, and joins with ", ".
 */
export function normalizeToolsCsv(raw: string): string {
  const seen = new Set<string>();
  const result: string[] = [];

  for (const entry of raw.split(",")) {
    const trimmed = entry.trim();
    if (trimmed && !seen.has(trimmed)) {
      seen.add(trimmed);
      result.push(trimmed);
    }
  }

  return result.join(", ");
}

/**
 * Splits a comma-separated or newline-separated string into a cleaned
 * string array: trims, removes empties, deduplicates.
 */
export function normalizeStringArray(raw: string): string[] {
  const seen = new Set<string>();
  const result: string[] = [];

  for (const entry of raw.split(/[,\n]/)) {
    const trimmed = entry.trim();
    if (trimmed && !seen.has(trimmed)) {
      seen.add(trimmed);
      result.push(trimmed);
    }
  }

  return result;
}

// ---------------------------------------------------------------------------
// Validation
// ---------------------------------------------------------------------------

/**
 * Client-side validation of toolkit overrides.
 * Returns an array of errors. Empty array = valid.
 * Runs at send-time in sendPrompt() to gate API calls.
 */
export function validateToolkitOverrides(overrides: ToolkitOverrides): ToolkitValidationError[] {
  const errors: ToolkitValidationError[] = [];

  // model
  if (overrides.model !== undefined) {
    const trimmed = overrides.model.trim();
    if (!trimmed) {
      errors.push({ field: "model", message: "Model must be a non-empty string." });
    }
  }

  // maxTurns
  if (overrides.maxTurns !== undefined) {
    if (
      !Number.isInteger(overrides.maxTurns) ||
      overrides.maxTurns < 1 ||
      overrides.maxTurns > MAX_TURNS_UPPER
    ) {
      errors.push({
        field: "maxTurns",
        message: `Max turns must be an integer between 1 and ${MAX_TURNS_UPPER}.`,
      });
    }
  }

  // tools
  if (overrides.tools !== undefined) {
    const normalized = normalizeToolsCsv(overrides.tools);
    if (!normalized) {
      errors.push({ field: "tools", message: "Tools must contain at least one tool name." });
    }
  }

  // disallowedTools
  if (overrides.disallowedTools !== undefined && overrides.disallowedTools.length > 0) {
    const hasEmpty = overrides.disallowedTools.some((t) => !t.trim());
    if (hasEmpty) {
      errors.push({ field: "disallowedTools", message: "Disallowed tools contains empty entries." });
    }
  }

  // autoApproveTools
  if (overrides.autoApproveTools !== undefined && overrides.autoApproveTools.length > 0) {
    const hasEmpty = overrides.autoApproveTools.some((t) => !t.trim());
    if (hasEmpty) {
      errors.push({ field: "autoApproveTools", message: "Auto-approve tools contains empty entries." });
    }
  }

  // subagentGovernance — if ANY field set, ALL required fields must be valid
  if (overrides.subagentGovernance !== undefined) {
    const gov = overrides.subagentGovernance;
    const anyFieldSet =
      gov.contextSealed !== undefined ||
      gov.pipelineRunApproved !== undefined ||
      (gov.approvalRef !== undefined && gov.approvalRef.trim() !== "") ||
      (gov.approvedBy !== undefined && gov.approvedBy.trim() !== "");

    if (anyFieldSet) {
      if (gov.contextSealed !== true) {
        errors.push({
          field: "subagentGovernance",
          message: "Governance incomplete: contextSealed must be true.",
        });
      }
      if (gov.pipelineRunApproved !== true) {
        errors.push({
          field: "subagentGovernance",
          message: "Governance incomplete: pipelineRunApproved must be true.",
        });
      }
      if (!gov.approvalRef || !gov.approvalRef.trim()) {
        errors.push({
          field: "subagentGovernance",
          message: "Governance incomplete: approvalRef must be a non-empty string.",
        });
      }
    }
  }

  return errors;
}

// ---------------------------------------------------------------------------
// Warnings
// ---------------------------------------------------------------------------

/**
 * Computes non-blocking warnings for risky or contradictory configurations.
 * Displayed reactively in the toolkit panel — do NOT block send.
 */
export function computeToolkitWarnings(overrides: ToolkitOverrides): ToolkitWarning[] {
  const warnings: ToolkitWarning[] = [];

  // High turn limit
  if (overrides.maxTurns !== undefined && overrides.maxTurns > 100) {
    warnings.push({
      code: "HIGH_MAX_TURNS",
      message: "High turn limit may result in extended runs and significant API costs.",
    });
  }

  // Conflicting tool rules
  if (overrides.disallowedTools && overrides.autoApproveTools) {
    const disallowedSet = new Set(overrides.disallowedTools.map((t) => t.trim()));
    for (const tool of overrides.autoApproveTools) {
      if (disallowedSet.has(tool.trim())) {
        warnings.push({
          code: "CONFLICTING_TOOL_RULES",
          message: `Tool "${tool.trim()}" appears in both disallowed and auto-approve lists.`,
        });
      }
    }
  }

  // Governance without feature flag
  if (overrides.subagentGovernance !== undefined) {
    warnings.push({
      code: "GOVERNANCE_NO_FEATURE_FLAG",
      message:
        "Subagent governance token is set. Runtime delegation requires CHIRALITY_ENABLE_SUBAGENTS=true, an allowlisted persona, and persona-declared subagents.",
    });
  }

  return warnings;
}

// ---------------------------------------------------------------------------
// TurnOpts builder
// ---------------------------------------------------------------------------

/**
 * Builds a `TurnOpts` object from toolkit overrides and the API key.
 *
 * Only includes fields where the override has a non-undefined, non-inherit
 * value. When overrides are empty (`EMPTY_OVERRIDES`), the result is
 * `{ apiKey }` — preserving zero-impact default behavior.
 */
export function buildTurnOptsFromToolkit(
  overrides: ToolkitOverrides,
  apiKey: string | undefined,
): TurnOpts {
  const opts: TurnOpts = {};

  if (apiKey) {
    opts.apiKey = apiKey;
  }

  if (overrides.model !== undefined) {
    opts.model = overrides.model.trim();
  }

  if (overrides.maxTurns !== undefined) {
    opts.maxTurns = overrides.maxTurns;
  }

  if (overrides.tools !== undefined) {
    opts.tools = normalizeToolsCsv(overrides.tools);
  }

  if (overrides.disallowedTools !== undefined && overrides.disallowedTools.length > 0) {
    opts.disallowedTools = overrides.disallowedTools.map((t) => t.trim()).filter(Boolean);
  }

  if (overrides.autoApproveTools !== undefined && overrides.autoApproveTools.length > 0) {
    opts.autoApproveTools = overrides.autoApproveTools.map((t) => t.trim()).filter(Boolean);
  }

  // Tri-state: "inherit" → omit (SDK default), true/false → explicit
  if (overrides.includePartialMessages !== undefined && overrides.includePartialMessages !== "inherit") {
    opts.includePartialMessages = overrides.includePartialMessages;
  }

  if (overrides.subagentGovernance !== undefined) {
    opts.subagentGovernance = {
      contextSealed: overrides.subagentGovernance.contextSealed,
      pipelineRunApproved: overrides.subagentGovernance.pipelineRunApproved,
      approvalRef: overrides.subagentGovernance.approvalRef?.trim() ?? "",
      ...(overrides.subagentGovernance.approvedBy?.trim()
        ? { approvedBy: overrides.subagentGovernance.approvedBy.trim() }
        : {}),
    };
  }

  return opts;
}

// ---------------------------------------------------------------------------
// Preset storage
// ---------------------------------------------------------------------------

/** Loads saved presets from localStorage. Malformed entries are silently dropped. */
export function loadPresets(): ToolkitPreset[] {
  if (typeof window === "undefined") return [];

  try {
    const raw = localStorage.getItem(PRESET_STORAGE_KEY);
    if (!raw) return [];

    const parsed = JSON.parse(raw);
    if (!Array.isArray(parsed)) return [];

    const presets: ToolkitPreset[] = [];

    for (const candidate of parsed) {
      if (!candidate || typeof candidate !== "object") continue;

      const id = typeof candidate.id === "string" ? candidate.id : null;
      const name = typeof candidate.name === "string" ? candidate.name.slice(0, MAX_PRESET_NAME_LENGTH) : null;
      const createdAt = typeof candidate.createdAt === "string" ? candidate.createdAt : null;
      const updatedAt = typeof candidate.updatedAt === "string" ? candidate.updatedAt : createdAt;
      const version = typeof candidate.version === "number" ? candidate.version : PRESET_SCHEMA_VERSION;
      const overrides =
        candidate.overrides && typeof candidate.overrides === "object"
          ? normalizeOverridesFromStorage(candidate.overrides)
          : {};

      if (!id || !name || !createdAt) continue;

      presets.push({ id, name, createdAt, updatedAt: updatedAt ?? createdAt, version, overrides });
    }

    return presets.slice(0, MAX_PRESETS);
  } catch {
    return [];
  }
}

/** Saves presets to localStorage. Enforces capacity limit. */
export function savePresets(presets: ToolkitPreset[]): void {
  if (typeof window === "undefined") return;

  const capped = presets.slice(0, MAX_PRESETS);
  localStorage.setItem(PRESET_STORAGE_KEY, JSON.stringify(capped));
}

/** Creates a new preset from the current overrides. */
export function createPreset(name: string, overrides: ToolkitOverrides): ToolkitPreset {
  const now = new Date().toISOString();
  return {
    id: crypto.randomUUID(),
    name: name.trim().slice(0, MAX_PRESET_NAME_LENGTH),
    createdAt: now,
    updatedAt: now,
    version: PRESET_SCHEMA_VERSION,
    overrides: { ...overrides },
  };
}

// ---------------------------------------------------------------------------
// Storage normalization (defensive parsing for overrides from localStorage)
// ---------------------------------------------------------------------------

/**
 * Normalizes an overrides object read from localStorage.
 * Unknown fields are silently dropped. Malformed values revert to undefined.
 */
function normalizeOverridesFromStorage(raw: Record<string, unknown>): ToolkitOverrides {
  const result: ToolkitOverrides = {};

  // model
  if (typeof raw.model === "string" && raw.model.trim()) {
    result.model = raw.model.trim();
  }

  // maxTurns
  if (typeof raw.maxTurns === "number" && Number.isInteger(raw.maxTurns) && raw.maxTurns >= 1) {
    result.maxTurns = raw.maxTurns;
  }

  // tools
  if (typeof raw.tools === "string" && raw.tools.trim()) {
    result.tools = raw.tools;
  }

  // disallowedTools
  if (Array.isArray(raw.disallowedTools)) {
    const cleaned = raw.disallowedTools.filter((t): t is string => typeof t === "string" && t.trim() !== "");
    if (cleaned.length > 0) result.disallowedTools = cleaned;
  }

  // autoApproveTools
  if (Array.isArray(raw.autoApproveTools)) {
    const cleaned = raw.autoApproveTools.filter((t): t is string => typeof t === "string" && t.trim() !== "");
    if (cleaned.length > 0) result.autoApproveTools = cleaned;
  }

  // includePartialMessages (tri-state)
  if (raw.includePartialMessages === true || raw.includePartialMessages === false) {
    result.includePartialMessages = raw.includePartialMessages;
  } else if (raw.includePartialMessages === "inherit") {
    result.includePartialMessages = "inherit";
  }

  // subagentGovernance
  if (raw.subagentGovernance && typeof raw.subagentGovernance === "object") {
    const gov = raw.subagentGovernance as Record<string, unknown>;
    result.subagentGovernance = {
      contextSealed: gov.contextSealed === true,
      pipelineRunApproved: gov.pipelineRunApproved === true,
      approvalRef: typeof gov.approvalRef === "string" ? gov.approvalRef : "",
      ...(typeof gov.approvedBy === "string" && gov.approvedBy.trim() ? { approvedBy: gov.approvedBy.trim() } : {}),
    };
  }

  return result;
}

/**
 * Normalizes a `toolkitOverrides` field read from a stored `LocalChatSession`.
 * Handles absent field (backward compatibility), malformed data, and unknown shapes.
 */
export function normalizeStoredOverrides(raw: unknown): ToolkitOverrides {
  if (!raw || typeof raw !== "object") return { ...EMPTY_OVERRIDES };
  return normalizeOverridesFromStorage(raw as Record<string, unknown>);
}
