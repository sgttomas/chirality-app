import { NextResponse } from 'next/server';
import { DependencyRegisterRow } from '../../../../../lib/dependencies/schema';
import {
  readDeliverableDependencies,
  writeDeliverableDependencies
} from '../../../../../lib/workspace/deliverable-contracts';
import {
  WorkspaceValidationError,
  workspaceErrorPayload
} from '../../../../../lib/workspace/filesystem';

type DependenciesWriteRequest = {
  projectRoot: string;
  deliverablePath: string;
  rows: unknown;
};

function requireNonEmptyString(value: unknown, field: string): string {
  if (typeof value !== 'string' || value.trim().length === 0) {
    throw new WorkspaceValidationError('INVALID_REQUEST', 400, `Missing or invalid '${field}'`);
  }
  return value.trim();
}

function normalizeDependencyRows(input: unknown): DependencyRegisterRow[] {
  if (!Array.isArray(input)) {
    throw new WorkspaceValidationError('INVALID_REQUEST', 400, "Field 'rows' must be an array");
  }

  return input.map((item, index) => {
    if (typeof item !== 'object' || item === null || Array.isArray(item)) {
      throw new WorkspaceValidationError(
        'INVALID_REQUEST',
        400,
        `rows[${index}] must be an object`
      );
    }

    const normalized: DependencyRegisterRow = {
      DependencyID: '',
      FromPackageID: '',
      FromDeliverableID: '',
      FromDeliverableName: '',
      DependencyClass: '',
      AnchorType: '',
      Direction: '',
      DependencyType: '',
      TargetType: '',
      Origin: '',
      FirstSeen: '',
      LastSeen: '',
      Status: ''
    };

    for (const [key, value] of Object.entries(item)) {
      if (value === undefined || value === null) {
        normalized[key] = '';
        continue;
      }

      if (typeof value !== 'string') {
        throw new WorkspaceValidationError(
          'INVALID_REQUEST',
          400,
          `rows[${index}].${key} must be a string`
        );
      }

      normalized[key] = value;
    }

    return normalized;
  });
}

export async function GET(request: Request): Promise<Response> {
  try {
    const url = new URL(request.url);
    const projectRoot = url.searchParams.get('projectRoot') ?? '';
    const deliverablePath = url.searchParams.get('deliverablePath') ?? '';
    const snapshot = await readDeliverableDependencies(projectRoot, deliverablePath);

    return NextResponse.json(snapshot, { status: 200 });
  } catch (error) {
    const payload = workspaceErrorPayload(error);
    return NextResponse.json(payload.body, { status: payload.status });
  }
}

export async function PUT(request: Request): Promise<Response> {
  try {
    const body = (await request.json()) as DependenciesWriteRequest;
    const projectRoot = requireNonEmptyString(body.projectRoot, 'projectRoot');
    const deliverablePath = requireNonEmptyString(body.deliverablePath, 'deliverablePath');
    const rows = normalizeDependencyRows(body.rows);
    const result = await writeDeliverableDependencies({
      projectRoot,
      deliverablePath,
      rows
    });

    return NextResponse.json(result, { status: 200 });
  } catch (error) {
    const payload = workspaceErrorPayload(error);
    return NextResponse.json(payload.body, { status: payload.status });
  }
}
