import { HarnessError } from '@chirality/runtime-contracts/errors';
import type { ServerRequestAnswer } from '@chirality/runtime-contracts';

export function isRecord(value: unknown): value is Record<string, unknown> {
  return value !== null && typeof value === 'object' && !Array.isArray(value);
}

/**
 * Shape check only. The Runtime validates the answer against the request's
 * Codex method and rejects a mismatched kind; nothing here implies approval.
 */
export function requireServerRequestAnswer(value: unknown): ServerRequestAnswer {
  if (!isRecord(value)) {
    throw new HarnessError('INVALID_REQUEST', 400, "Field 'answer' must be an object");
  }
  switch (value.kind) {
    case 'approval': {
      if (value.verdict !== 'allow' && value.verdict !== 'deny' && value.verdict !== 'allowForSession') {
        throw new HarnessError('INVALID_REQUEST', 400, "Field 'answer.verdict' must be 'allow', 'deny' or 'allowForSession'");
      }
      return { kind: 'approval', verdict: value.verdict };
    }
    case 'userInput': {
      if (!isRecord(value.answers)) {
        throw new HarnessError('INVALID_REQUEST', 400, "Field 'answer.answers' must be an object");
      }
      const answers: Record<string, { answers: string[] }> = {};
      for (const [questionId, entry] of Object.entries(value.answers)) {
        if (!isRecord(entry) || !Array.isArray(entry.answers) || entry.answers.some((item) => typeof item !== 'string')) {
          throw new HarnessError('INVALID_REQUEST', 400, "Each 'answer.answers' entry must carry an array of strings");
        }
        answers[questionId] = { answers: [...(entry.answers as string[])] };
      }
      return { kind: 'userInput', answers };
    }
    case 'elicitation': {
      if (value.action !== 'accept' && value.action !== 'decline' && value.action !== 'cancel') {
        throw new HarnessError('INVALID_REQUEST', 400, "Field 'answer.action' must be 'accept', 'decline' or 'cancel'");
      }
      return { kind: 'elicitation', action: value.action, ...('content' in value ? { content: value.content } : {}) };
    }
    default:
      throw new HarnessError('INVALID_REQUEST', 400, "Field 'answer.kind' must be 'approval', 'userInput' or 'elicitation'");
  }
}

/** POST /api/harness/session/[id]/requests/[requestId]/answer: answers one Codex server request. */
