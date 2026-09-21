import { NextResponse } from 'next/server';
import { HarnessError } from '@chirality/runtime-contracts/errors';
import type { ReplyNativePlanClarificationRequest } from '@chirality/runtime-contracts/v3';
import { errorResponse, readJsonBody, requireNonEmptyString } from '../../../../../../../../lib/harness/http';
import { getDaemonHarnessPort } from '../../../../../../../../lib/runtime-client/daemon-harness-port';

function isRecord(value: unknown): value is Record<string, unknown> {
  return value !== null && typeof value === 'object' && !Array.isArray(value);
}

function requireReplyRequest(value: unknown): ReplyNativePlanClarificationRequest {
  if (!isRecord(value)) {
    throw new HarnessError('INVALID_REQUEST', 400, 'Request body must be an object');
  }
  const requestId = value.requestId;
  if (
    !(
      typeof requestId === 'string' ||
      (typeof requestId === 'number' && Number.isFinite(requestId))
    )
  ) {
    throw new HarnessError(
      'INVALID_REQUEST',
      400,
      "Field 'requestId' must be a string or finite number"
    );
  }
  if (!isRecord(value.answers)) {
    throw new HarnessError('INVALID_REQUEST', 400, "Field 'answers' must be an object");
  }

  const answers: Record<string, { answers: readonly string[] }> = Object.create(null) as Record<
    string,
    { answers: readonly string[] }
  >;
  for (const [questionId, answer] of Object.entries(value.answers)) {
    if (
      !isRecord(answer) ||
      !Array.isArray(answer.answers) ||
      answer.answers.some((item) => typeof item !== 'string')
    ) {
      throw new HarnessError(
        'INVALID_REQUEST',
        400,
        "Each 'answers' entry must have an array of strings"
      );
    }
    answers[questionId] = { answers: answer.answers };
  }

  return { requestId, answers };
}

export async function POST(
  request: Request,
  context: { params: Promise<{ id: string }> }
): Promise<Response> {
  try {
    const sessionId = requireNonEmptyString((await context.params).id, 'sessionId');
    const body = requireReplyRequest(await readJsonBody<unknown>(request));
    const result = await getDaemonHarnessPort().replyNativePlanClarification(
      sessionId,
      body.requestId,
      body.answers,
      { signal: request.signal }
    );
    return NextResponse.json(result, { status: 200 });
  } catch (error) {
    return errorResponse(error);
  }
}
