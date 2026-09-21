import { NextResponse } from 'next/server';
import {
  DeliverableStatusTransitionInput,
  transitionDeliverableStatus
} from '../../../../../../lib/workspace/deliverable-contracts';
import {
  WorkspaceValidationError,
  workspaceErrorPayload
} from '../../../../../../lib/workspace/filesystem';

type TransitionRequest = {
  projectRoot: string;
  deliverablePath: string;
  targetState: string;
  actor: string;
  date?: string;
  metadata?: Record<string, string>;
  approvalSha?: string;
};

function requireNonEmptyString(value: unknown, field: string): string {
  if (typeof value !== 'string' || value.trim().length === 0) {
    throw new WorkspaceValidationError('INVALID_REQUEST', 400, `Missing or invalid '${field}'`);
  }
  return value.trim();
}

function parseMetadata(value: unknown): Record<string, string> | undefined {
  if (value === undefined) {
    return undefined;
  }

  if (typeof value !== 'object' || value === null || Array.isArray(value)) {
    throw new WorkspaceValidationError('INVALID_REQUEST', 400, 'metadata must be an object');
  }

  const parsed: Record<string, string> = {};
  for (const [key, item] of Object.entries(value)) {
    if (typeof item !== 'string') {
      throw new WorkspaceValidationError(
        'INVALID_REQUEST',
        400,
        `metadata.${key} must be a string`
      );
    }
    parsed[key] = item;
  }

  return parsed;
}

export async function POST(request: Request): Promise<Response> {
  try {
    const body = (await request.json()) as TransitionRequest;
    const transitionInput: DeliverableStatusTransitionInput = {
      projectRoot: requireNonEmptyString(body.projectRoot, 'projectRoot'),
      deliverablePath: requireNonEmptyString(body.deliverablePath, 'deliverablePath'),
      targetState: requireNonEmptyString(body.targetState, 'targetState'),
      actor: requireNonEmptyString(body.actor, 'actor'),
      date: body.date?.trim(),
      metadata: parseMetadata(body.metadata),
      approvalSha: body.approvalSha?.trim()
    };

    const result = await transitionDeliverableStatus(transitionInput);
    return NextResponse.json(result, { status: 200 });
  } catch (error) {
    const payload = workspaceErrorPayload(error);
    return NextResponse.json(payload.body, { status: payload.status });
  }
}
