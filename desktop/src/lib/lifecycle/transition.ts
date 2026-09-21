import { readFile } from 'node:fs/promises';
import { writeTextFileAtomically } from '../atomic-write';
import { LifecycleState, LIFECYCLE_STATES, parseLifecycleState, parseStatusDocument } from './status-parser';
import { updateStatusDocument } from './status-writer';

const STATE_INDEX = new Map<LifecycleState, number>(
  LIFECYCLE_STATES.map((state, index) => [state, index])
);

type ActorRequirement =
  | 'PREPARATION'
  | '4_DOCUMENTS'
  | 'CHIRALITY_FRAMEWORK'
  | 'WORKING_ITEMS'
  | 'HUMAN';

interface TransitionRule {
  from: LifecycleState;
  to: LifecycleState;
  actors: readonly ActorRequirement[];
}

const TRANSITION_RULES: TransitionRule[] = [
  { from: 'OPEN', to: 'INITIALIZED', actors: ['4_DOCUMENTS'] },
  { from: 'INITIALIZED', to: 'SEMANTIC_READY', actors: ['CHIRALITY_FRAMEWORK'] },
  { from: 'INITIALIZED', to: 'IN_PROGRESS', actors: ['HUMAN', 'WORKING_ITEMS'] },
  { from: 'SEMANTIC_READY', to: 'IN_PROGRESS', actors: ['HUMAN', 'WORKING_ITEMS'] },
  { from: 'IN_PROGRESS', to: 'CHECKING', actors: ['HUMAN'] },
  { from: 'CHECKING', to: 'ISSUED', actors: ['HUMAN'] }
];

export type TransitionErrorCode =
  | 'INVALID_STATE'
  | 'BACKWARD_TRANSITION'
  | 'TRANSITION_NOT_ALLOWED'
  | 'UNAUTHORIZED_ACTOR'
  | 'APPROVAL_SHA_REQUIRED'
  | 'INVALID_APPROVAL_SHA';

export class LifecycleTransitionError extends Error {
  readonly code: TransitionErrorCode;
  readonly details?: unknown;

  constructor(code: TransitionErrorCode, message: string, details?: unknown) {
    super(message);
    this.name = 'LifecycleTransitionError';
    this.code = code;
    this.details = details;
  }
}

export interface LifecycleTransitionOptions {
  date?: string;
  metadata?: Record<string, string>;
  approvalSha?: string;
}

export interface LifecycleTransitionResult {
  from: LifecycleState;
  to: LifecycleState;
  actor: string;
  content: string;
}

const APPROVAL_SHA_PATTERN = /^[0-9a-f]{7,64}$/i;

function normalizeActor(actor: string): string {
  const normalized = actor.trim().toUpperCase().replace(/\s+/g, '_');
  if (normalized === 'HUMAN' || normalized === 'USER' || normalized === 'OPERATOR') {
    return 'HUMAN';
  }
  return normalized;
}

function isBackwardTransition(from: LifecycleState, to: LifecycleState): boolean {
  const fromIndex = STATE_INDEX.get(from);
  const toIndex = STATE_INDEX.get(to);
  if (fromIndex === undefined || toIndex === undefined) {
    return false;
  }
  return toIndex < fromIndex;
}

function findTransitionRule(from: LifecycleState, to: LifecycleState): TransitionRule | undefined {
  return TRANSITION_RULES.find((rule) => rule.from === from && rule.to === to);
}

function isHumanGateTransition(to: LifecycleState): boolean {
  return to === 'CHECKING' || to === 'ISSUED';
}

function parseApprovalShaForTransition(
  to: LifecycleState,
  options: LifecycleTransitionOptions
): string | undefined {
  const approvalSha = options.approvalSha?.trim();
  if (!isHumanGateTransition(to)) {
    return approvalSha;
  }

  if (!approvalSha) {
    throw new LifecycleTransitionError(
      'APPROVAL_SHA_REQUIRED',
      `Transition ${to} requires approvalSha evidence`,
      { to }
    );
  }

  if (!APPROVAL_SHA_PATTERN.test(approvalSha)) {
    throw new LifecycleTransitionError(
      'INVALID_APPROVAL_SHA',
      'approvalSha must be a git SHA-like hexadecimal token (7-64 chars)',
      { to, approvalSha }
    );
  }

  return approvalSha;
}

function mergeTransitionMetadata(
  to: LifecycleState,
  options: LifecycleTransitionOptions,
  approvalSha: string | undefined
): Record<string, string> | undefined {
  const metadata: Record<string, string> = { ...(options.metadata ?? {}) };
  if (approvalSha) {
    if (to === 'CHECKING') {
      metadata.checkingApprovalSha = approvalSha;
    }
    if (to === 'ISSUED') {
      metadata.approvalSha = approvalSha;
    }
  }
  return Object.keys(metadata).length > 0 ? metadata : undefined;
}

export function applyLifecycleTransition(
  currentStatusContent: string,
  targetStateInput: string,
  actorInput: string,
  options: LifecycleTransitionOptions = {}
): LifecycleTransitionResult {
  const parsed = parseStatusDocument(currentStatusContent);
  const from = parsed.currentState;

  let to: LifecycleState;
  try {
    to = parseLifecycleState(targetStateInput);
  } catch (error) {
    throw new LifecycleTransitionError('INVALID_STATE', 'Target state is invalid', { error });
  }

  if (isBackwardTransition(from, to)) {
    throw new LifecycleTransitionError(
      'BACKWARD_TRANSITION',
      `Backward transitions are not allowed (${from} -> ${to})`,
      { from, to }
    );
  }

  const rule = findTransitionRule(from, to);
  if (!rule) {
    throw new LifecycleTransitionError(
      'TRANSITION_NOT_ALLOWED',
      `Transition ${from} -> ${to} is not allowed`,
      { from, to }
    );
  }

  const normalizedActor = normalizeActor(actorInput);
  if (!rule.actors.includes(normalizedActor as ActorRequirement)) {
    throw new LifecycleTransitionError(
      'UNAUTHORIZED_ACTOR',
      `Actor '${actorInput}' is not authorized for transition ${from} -> ${to}`,
      { from, to, actor: actorInput, expected: rule.actors }
    );
  }

  const actor = actorInput.trim() || normalizedActor;
  const approvalSha = parseApprovalShaForTransition(to, options);
  const metadata = mergeTransitionMetadata(to, options, approvalSha);
  const updated = updateStatusDocument(currentStatusContent, {
    targetState: to,
    actor,
    date: options.date,
    metadata
  });

  return {
    from,
    to,
    actor,
    content: updated.content
  };
}

export async function transitionStatusFile(
  statusFilePath: string,
  targetStateInput: string,
  actorInput: string,
  options: LifecycleTransitionOptions = {}
): Promise<LifecycleTransitionResult> {
  const existingContent = await readFile(statusFilePath, 'utf8');
  const result = applyLifecycleTransition(
    existingContent,
    targetStateInput,
    actorInput,
    options
  );
  await writeTextFileAtomically(statusFilePath, result.content);
  return result;
}
