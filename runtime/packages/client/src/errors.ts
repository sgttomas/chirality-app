import {
  RUNTIME_ERROR_CODES,
  RuntimeError,
  type RuntimeErrorBody,
  type RuntimeErrorCode
} from "@chirality/runtime-contracts";

const runtimeErrorCodes = new Set<string>(RUNTIME_ERROR_CODES);

export class RuntimeTransportError extends Error {
  readonly cause?: unknown;

  constructor(message: string, cause?: unknown) {
    super(message);
    this.name = "RuntimeTransportError";
    if (cause !== undefined) this.cause = cause;
  }
}

export function runtimeErrorFromResponse(
  status: number,
  value: unknown
): RuntimeError {
  if (
    typeof value === "object" &&
    value !== null &&
    typeof (value as RuntimeErrorBody).error === "object" &&
    (value as RuntimeErrorBody).error !== null
  ) {
    const error = (value as RuntimeErrorBody).error;
    const code = runtimeErrorCodes.has(error.code)
      ? (error.code as RuntimeErrorCode)
      : "INTERNAL_FAILURE";
    return new RuntimeError(
      code,
      typeof error.message === "string"
        ? error.message
        : `Runtime request failed with HTTP ${status}`,
      status,
      error.details
    );
  }
  return new RuntimeError(
    "INTERNAL_FAILURE",
    `Runtime request failed with HTTP ${status}`,
    status
  );
}
