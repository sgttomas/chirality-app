import { asNonEmptyString, asStringArray } from './agent-instruction';
import type { HarnessOpts, ResolvedOpts, SessionRecord } from '@chirality/runtime-contracts/types';

const DEFAULT_MODEL = 'haiku';
const DEFAULT_TOOLS = ['read', 'write', 'bash'];
const DEFAULT_MAX_TURNS = 12;
const SUPPORTED_OPT_KEYS = new Set(['model', 'tools', 'maxTurns', 'persona', 'mode', 'subagentGovernance']);

function asPositiveInteger(value: unknown): number | undefined {
  return typeof value === 'number' && Number.isInteger(value) && value > 0 ? value : undefined;
}

function warnOnUnknownOpts(opts: HarnessOpts | undefined): void {
  if (!opts || typeof opts !== 'object') return;
  const unknownKeys = Object.keys(opts as Record<string, unknown>)
    .filter((key) => !SUPPORTED_OPT_KEYS.has(key))
    .sort((left, right) => left.localeCompare(right));
  if (unknownKeys.length > 0) {
    console.warn(`[harness/options] Ignoring unknown opts field(s): ${unknownKeys.join(', ')}`);
  }
}

/**
 * Legacy in-process defaults only. Role and method configuration is resolved
 * by Runtime and must never be inferred from instruction Markdown frontmatter.
 */
export async function resolveRuntimeOptions(session: SessionRecord, opts?: HarnessOpts): Promise<ResolvedOpts> {
  warnOnUnknownOpts(opts);
  return {
    model: asNonEmptyString(opts?.model) ?? DEFAULT_MODEL,
    tools: asStringArray(opts?.tools) ?? DEFAULT_TOOLS,
    maxTurns: asPositiveInteger(opts?.maxTurns) ?? DEFAULT_MAX_TURNS,
    persona: asNonEmptyString(opts?.persona) ?? session.persona,
    mode: asNonEmptyString(opts?.mode) ?? session.mode,
    subagentGovernance: opts?.subagentGovernance
  };
}
