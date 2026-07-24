export const RUNTIME_ERROR_CODES = [
  "INVALID_REQUEST",
  "UNAUTHORIZED",
  "FORBIDDEN",
  "NOT_FOUND",
  "PROJECT_NOT_FOUND",
  "PROJECT_MANIFEST_INVALID",
  "PROJECT_MANIFEST_DRIFT",
  "SESSION_NOT_FOUND",
  "SESSION_TURN_IN_PROGRESS",
  "ENGINE_UNAVAILABLE",
  "MODEL_UNAVAILABLE",
  "MODEL_NOT_RESIDENT",
  "RESIDENCY_TRANSITION_IN_PROGRESS",
  "RESIDENCY_DRAIN_TIMEOUT",
  "RESIDENCY_UNMANAGED_CONFLICT",
  "OMLX_AUTHENTICATION_FAILED",
  "OMLX_PROTOCOL_FAILURE",
  "OMLX_UNAVAILABLE",
  "REQUIRED_DELEGATION_MISSING",
  "DELEGATION_POLICY_VIOLATION",
  "INTERRUPTED",
  "INTERNAL_FAILURE"
] as const;

export type RuntimeErrorCode = (typeof RUNTIME_ERROR_CODES)[number];

export class RuntimeError extends Error {
  readonly code: RuntimeErrorCode;
  readonly status: number;
  readonly details?: Readonly<Record<string, unknown>>;

  constructor(
    code: RuntimeErrorCode,
    message: string,
    status = 400,
    details?: Readonly<Record<string, unknown>>
  ) {
    super(message);
    this.name = "RuntimeError";
    this.code = code;
    this.status = status;
    if (details !== undefined) this.details = details;
  }
}

export interface RuntimeErrorBody {
  error: {
    code: RuntimeErrorCode;
    message: string;
    details?: Readonly<Record<string, unknown>>;
  };
}
