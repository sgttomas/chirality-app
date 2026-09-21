import { NextResponse } from 'next/server';
import { assertProjectRootAccessible } from '../../../../lib/harness/session-manager';
import { resolveInstructionRootPath } from '../../../../lib/harness/instruction-root';
import { fileError, FilePolicyError, validateRevealRoot } from '../file/file-policy';
import { listWorkflowFiles, readWorkflowFile } from './workflow-store';
export const runtime = 'nodejs';
export async function GET(request: Request): Promise<Response> {
  const headers = { 'Cache-Control': 'no-store', 'X-Content-Type-Options': 'nosniff' };
  try {
    const params = new URL(request.url).searchParams;
    if ([...params.keys()].some(key => key !== 'projectRoot' && key !== 'name') || params.getAll('projectRoot').length !== 1 || params.getAll('name').length > 1)
      throw new FilePolicyError('INVALID_REQUEST', 400, 'Choose a current folder and one workflow file.');
    const selectedRoot = await assertProjectRootAccessible(params.get('projectRoot') ?? '');
    const instruction = resolveInstructionRootPath();
    const root = await validateRevealRoot({ projectRoot: selectedRoot }, instruction);
    const body = params.has('name') ? await readWorkflowFile(root, params.get('name')!, instruction) : await listWorkflowFiles(root, instruction);
    return NextResponse.json(body, { headers });
  } catch (error) {
    const typed = error as { type?: string; status?: number };
    const result = typeof typed.type === 'string' && typeof typed.status === 'number'
      ? { status: typed.status, body: { error: { code: typed.type, message: 'The current folder is unavailable or outside the allowed workspace. Choose another folder and retry.' } } }
      : fileError(error);
    // Never forward filesystem paths or arbitrary root-policy exception text.
    return NextResponse.json(result.body, { status: result.status, headers });
  }
}
