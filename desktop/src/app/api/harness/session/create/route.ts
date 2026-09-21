import { NextResponse } from 'next/server';
import {
  errorResponse,
  readJsonBody,
  requireNonEmptyString
} from '../../../../../lib/harness/http';
import { getDaemonHarnessPort } from '../../../../../lib/runtime-client/daemon-harness-port';
import { SessionCreateRequest } from '@chirality/runtime-contracts/types';
import { HarnessError } from '@chirality/runtime-contracts/errors';
import {
  CHIRALITY_ROLES,
  type ChiralityRoleName,
  type MethodReference,
  type ResolveSelectedContextRequest
} from '@chirality/runtime-contracts/v3';

type CreateRequest = SessionCreateRequest & {
  roleId?: ChiralityRoleName;
  interactionMode?: ResolveSelectedContextRequest['interactionMode'];
  permissionMode?: ResolveSelectedContextRequest['permissionMode'];
  selectedMethods?: readonly MethodReference[];
  declaredContext?: string[];
  allowedWriteTargets?: string[];
  modelSelection?: { model: string; reasoningEffort: string };
};

export async function POST(request: Request): Promise<Response> {
  try {
    const body = await readJsonBody<CreateRequest>(request);
    const projectRoot = requireNonEmptyString(body.projectRoot, 'projectRoot');

    const legacyPersona = body.persona?.trim();
    if (body.roleId !== undefined && legacyPersona && legacyPersona !== body.roleId) {
      throw new HarnessError(
        'INVALID_REQUEST',
        400,
        `Role '${body.roleId}' conflicts with persona '${legacyPersona}'.`
      );
    }
    const canonicalDirectRole = CHIRALITY_ROLES.find((role) =>
      role.directEntry && role.id === legacyPersona
    )?.id;
    const roleId = body.roleId ?? canonicalDirectRole ?? (
      legacyPersona === undefined || legacyPersona === '' ? 'HELP_HUMAN' : undefined
    );

    const result = await getDaemonHarnessPort().createSession(
      {
        projectRoot,
        persona: legacyPersona || roleId,
        mode: body.mode,
        ...(roleId === undefined ? {} : { roleId }),
        ...(body.interactionMode === undefined ? {} : { interactionMode: body.interactionMode }),
        ...(body.permissionMode === undefined ? {} : { permissionMode: body.permissionMode }),
        ...(body.selectedMethods === undefined ? {} : { selectedMethods: body.selectedMethods }),
        ...(body.declaredContext === undefined ? {} : { declaredContext: body.declaredContext }),
        ...(body.allowedWriteTargets === undefined
          ? {}
          : { allowedWriteTargets: body.allowedWriteTargets }),
        // Passed through verbatim: Runtime validates the pair against the
        // authenticated catalog and reports MODEL_NOT_IN_CATALOG /
        // REASONING_EFFORT_UNSUPPORTED / MODEL_SELECTION_INVALID itself.
        ...(body.modelSelection === undefined ? {} : { modelSelection: body.modelSelection })
      },
      { signal: request.signal }
    );
    return NextResponse.json(result, { status: 200 });
  } catch (error) {
    return errorResponse(error);
  }
}
