import { HarnessErrorType } from './types.js';

export class HarnessError extends Error {
  readonly type: HarnessErrorType;
  readonly status: number;
  readonly details?: unknown;

  constructor(type: HarnessErrorType, status: number, message: string, details?: unknown) {
    super(message);
    this.name = 'HarnessError';
    this.type = type;
    this.status = status;
    this.details = details;
  }
}

const HARNESS_ERROR_TYPES: Readonly<Record<HarnessErrorType, true>> = {
  INVALID_REQUEST: true,
  TURN_IN_PROGRESS: true,
  MISSING_API_KEY: true,
  SESSION_NOT_FOUND: true,
  PERSONA_NOT_FOUND: true,
  INSTRUCTION_ROOT_INVALID: true,
  SDK_FAILURE: true,
  ENGINE_UNAVAILABLE: true,
  MODEL_UNAVAILABLE: true,
  PROVIDER_AUTH_FAILURE: true,
  PROVIDER_PROTOCOL_FAILURE: true,
  CONTEXT_EXHAUSTED: true,
  WORKING_ROOT_INACCESSIBLE: true,
  WORKING_ROOT_CONFLICT: true,
  ATTACHMENT_FAILURE: true
};

function isHarnessErrorType(value: unknown): value is HarnessErrorType {
  return (
    typeof value === 'string' &&
    Object.prototype.hasOwnProperty.call(HARNESS_ERROR_TYPES, value)
  );
}

function isHarnessErrorLike(
  error: unknown
): error is {
  type: HarnessErrorType;
  status: number;
  message: string;
  details?: unknown;
} {
  if (!error || typeof error !== 'object') {
    return false;
  }

  const candidate = error as {
    type?: unknown;
    status?: unknown;
    message?: unknown;
    details?: unknown;
  };

  return (
    isHarnessErrorType(candidate.type) &&
    typeof candidate.status === 'number' &&
    Number.isFinite(candidate.status) &&
    typeof candidate.message === 'string'
  );
}

export function asHarnessError(error: unknown): HarnessError {
  if (error instanceof HarnessError) {
    return error;
  }

  if (isHarnessErrorLike(error)) {
    return new HarnessError(error.type, error.status, error.message, error.details);
  }

  if (error instanceof Error) {
    return new HarnessError('SDK_FAILURE', 500, error.message);
  }

  return new HarnessError('SDK_FAILURE', 500, 'Unexpected harness runtime error');
}
