import { HarnessApiClientError, harnessApiErrorMessage } from './client';
import type { AttachmentError, HarnessErrorType } from '@chirality/runtime-contracts/types';

export type HarnessUiError = {
  title: string;
  message: string;
  nextStep: string;
  code?: string;
};

const ERROR_COPY: Partial<Record<HarnessErrorType, Omit<HarnessUiError, 'code'>>> = {
  WORKING_ROOT_INACCESSIBLE: {
    title: 'Working Root Unavailable',
    message: 'The selected projectRoot is missing or inaccessible.',
    nextStep: 'Re-select a valid Working Root, then retry.'
  },
  WORKING_ROOT_CONFLICT: {
    title: 'Working Root Conflicts With Instruction Root',
    message: 'The selected projectRoot overlaps the bundled instruction root.',
    nextStep: 'Choose a separate execution directory outside instruction-root paths.'
  },
  INSTRUCTION_ROOT_INVALID: {
    title: 'Instruction Root Invalid',
    message: 'Required instruction files are missing or unreadable.',
    nextStep: 'Reinstall or rebuild the app bundle and verify instruction resources.'
  },
  INSTRUCTION_ADOPTION_PENDING: {
    title: 'Instruction update pending',
    message: 'The updated instructions could not be applied yet. Your next turn has not started.',
    nextStep: 'Let active work finish, then retry in this chat. If this persists, reopen Chirality after the work finishes.'
  },
  PERSONA_NOT_FOUND: {
    title: 'Persona Not Found',
    message: 'The selected agent persona could not be resolved from instruction root.',
    nextStep: 'Choose a valid WORKBENCH agent or verify instruction-root agent files.'
  },
  SDK_FAILURE: {
    title: 'Runtime Bootstrap Failed',
    message: 'The harness runtime failed while booting or running the turn.',
    nextStep: 'Retry once. If it persists, inspect runtime logs and boot configuration.'
  },
  SESSION_NOT_FOUND: {
    title: 'Session Not Found',
    message: 'The active harness session no longer exists.',
    nextStep: 'Start a new session and send the prompt again.'
  },
  ATTACHMENT_FAILURE: {
    title: 'Attachment Validation Failed',
    message: 'No executable attachment content was available for this turn.',
    nextStep: 'Attach readable files or include non-empty text content.'
  },
  TURN_IN_PROGRESS: {
    title: 'Turn Already In Progress',
    message: 'This session already has an active turn stream.',
    nextStep: 'Wait for the current turn to complete or interrupt it, then retry.'
  },
  MISSING_API_KEY: {
    title: 'API Key Not Configured',
    message: 'Anthropic API key is missing for provider-backed turns.',
    nextStep: 'Set ANTHROPIC_API_KEY and retry the turn.'
  },
  INVALID_REQUEST: {
    title: 'Invalid Request',
    message: 'The request payload failed server-side validation.',
    nextStep: 'Check required fields and retry.'
  }
};

const MAX_ATTACHMENT_ERROR_DETAILS = 2;

function parseAttachmentError(value: unknown): AttachmentError | null {
  if (!value || typeof value !== 'object') {
    return null;
  }

  const path = (value as Record<string, unknown>).path;
  const reason = (value as Record<string, unknown>).reason;
  if (typeof path !== 'string' || typeof reason !== 'string') {
    return null;
  }

  return {
    path,
    reason
  };
}

function parseAttachmentFailureDetails(details: unknown): {
  attachmentErrors: AttachmentError[];
  rejectedAttachmentCount: number;
} | null {
  if (!details || typeof details !== 'object') {
    return null;
  }

  const rawErrors = (details as Record<string, unknown>).attachmentErrors;
  if (!Array.isArray(rawErrors)) {
    return null;
  }

  const attachmentErrors = rawErrors
    .map((entry) => parseAttachmentError(entry))
    .filter((entry): entry is AttachmentError => entry !== null);
  if (attachmentErrors.length === 0) {
    return null;
  }

  const explicitCount = (details as Record<string, unknown>).rejectedAttachmentCount;
  const rejectedAttachmentCount =
    typeof explicitCount === 'number' && Number.isFinite(explicitCount)
      ? explicitCount
      : attachmentErrors.length;

  return {
    attachmentErrors,
    rejectedAttachmentCount
  };
}

function basenameLike(rawPath: string): string {
  const segments = rawPath.split(/[\\/]/).filter((segment) => segment.length > 0);
  if (segments.length === 0) {
    return rawPath;
  }
  return segments[segments.length - 1];
}

function withAttachmentFailureDetails(baseMessage: string, details: unknown): string {
  const parsed = parseAttachmentFailureDetails(details);
  if (!parsed) {
    return baseMessage;
  }

  const preview = parsed.attachmentErrors
    .slice(0, MAX_ATTACHMENT_ERROR_DETAILS)
    .map((entry) => `${basenameLike(entry.path)}: ${entry.reason}`);
  const remaining = parsed.rejectedAttachmentCount - preview.length;
  const suffix = remaining > 0 ? ` (+${remaining} more)` : '';

  return `${baseMessage} Rejections: ${preview.join(' | ')}${suffix}`;
}

export const MODEL_NOT_IN_CATALOG_REASON = 'MODEL_NOT_IN_CATALOG';

function readDetailString(details: unknown, key: string): string | undefined {
  if (!details || typeof details !== 'object') return undefined;
  const value = (details as Record<string, unknown>)[key];
  return typeof value === 'string' && value.trim().length > 0 ? value : undefined;
}

/**
 * Where a `MODEL_NOT_IN_CATALOG` rejection arose. `session-create` is the
 * create request for a chat that has not started (the renderer's catalog
 * snapshot was stale); `session` is the boot route or the turn stream of an
 * existing session whose recorded model left the catalog.
 */
export type ModelNotInCatalogOrigin = 'session-create' | 'session';

export type HarnessUiErrorContext = {
  /** The caller retained the unsent draft after a boot request failed. */
  bootBeforePrompt?: boolean;
  /** Names the model when the details omit it (the turn stream forwards only `runtimeCode` and `reason`). */
  sessionModel?: string;
  /** Defaults to `session`. */
  origin?: ModelNotInCatalogOrigin;
};

/**
 * Runtime reports a model outside the authenticated Codex catalog with
 * `details.reason = MODEL_NOT_IN_CATALOG`. For an existing session (boot route
 * and the turn stream's `turn:error`) the record is never rewritten; the
 * operator starts a new chat. For session creation no chat exists yet, so the
 * operator refreshes the account status and chooses again.
 */
export function modelNotInCatalogUiError(error: unknown, context: HarnessUiErrorContext = {}): HarnessUiError | null {
  if (!(error instanceof HarnessApiClientError)) return null;
  if (readDetailString(error.details, 'reason') !== MODEL_NOT_IN_CATALOG_REASON) return null;
  const model = readDetailString(error.details, 'model') ?? context.sessionModel;
  if (context.origin === 'session-create') {
    return {
      title: 'Model No Longer Offered',
      message: model
        ? `Model ${model} is no longer offered by your Codex account. Refresh your account status and choose again.`
        : 'The chosen model is no longer offered by your Codex account. Refresh your account status and choose again.',
      nextStep: 'Refresh your account status and choose a model your account offers.',
      code: error.code
    };
  }
  return {
    title: 'Model No Longer Offered',
    message: model
      ? `This chat used ${model}, which your Codex account no longer offers. Start a new chat.`
      : 'This chat used a model your Codex account no longer offers. Start a new chat.',
    nextStep: 'Start a new chat to choose a model your account offers.',
    code: error.code
  };
}

export function toHarnessUiError(error: unknown, context: HarnessUiErrorContext = {}): HarnessUiError {
  const catalogError = modelNotInCatalogUiError(error, context);
  if (catalogError) return catalogError;
  if (error instanceof HarnessApiClientError) {
    const bootstrapState = readDetailString(error.details, 'bootstrapState');
    const bootTimeout = readDetailString(error.details, 'operation') === 'boot' &&
      (readDetailString(error.details, 'transportReason') === 'timeout' || readDetailString(error.details, 'reason') === 'BOOT_TIMEOUT');
    const bootTransportFailure = readDetailString(error.details, 'operation') === 'boot' && readDetailString(error.details, 'transportReason') === 'transport';
    const bootCancelled = readDetailString(error.details, 'operation') === 'boot' && readDetailString(error.details, 'reason') === 'BOOT_CANCELLED';
    if (bootTimeout || bootTransportFailure || bootCancelled || bootstrapState) {
      const failed = bootstrapState === 'failed' || bootCancelled;
      const conflict = bootstrapState === 'conflict';
      return {
        title: bootTimeout ? 'Chat took too long to start' : failed ? 'Chat could not start' : conflict ? 'Chat context changed' : bootstrapState === 'pending' ? 'Chat is still starting' : 'Chat start is not confirmed',
        message: context.bootBeforePrompt ? 'Your message is saved.' : 'The chat did not finish starting.',
        nextStep: failed ? 'Start a new chat to try again.' : conflict ? "Return to this chat's original role and folder, or start a new chat." : 'Send again to check this chat, or start a new chat.',
        code: error.code
      };
    }
    if (readDetailString(error.details, 'transportReason') === 'timeout') return {
      title: 'Runtime Request Timed Out', message: 'Runtime did not respond within the request wait period.',
      nextStep: 'Check the current session before retrying.', code: error.code
    };
    const copy = ERROR_COPY[error.code as HarnessErrorType];
    if (copy) {
      const message =
        error.code === 'ATTACHMENT_FAILURE'
          ? withAttachmentFailureDetails(copy.message, error.details)
          : copy.message;
      return {
        ...copy,
        message,
        code: error.code
      };
    }

    return {
      title: 'Harness Request Failed',
      message: `${error.code}: ${error.message}`,
      nextStep: 'Review the request context and retry.',
      code: error.code
    };
  }

  return {
    title: 'Unexpected Harness Failure',
    message: harnessApiErrorMessage(error),
    nextStep: 'Retry once and inspect frontend console/runtime logs if the issue persists.'
  };
}
