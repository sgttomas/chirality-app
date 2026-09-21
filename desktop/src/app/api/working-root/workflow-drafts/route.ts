import { NextResponse } from 'next/server';
import { homedir } from 'node:os';
import { realpath } from 'node:fs/promises';
import { assertProjectRootAccessible } from '../../../../lib/harness/session-manager';
import { resolveInstructionRootPath } from '../../../../lib/harness/instruction-root';
import type { WorkflowDraftSource } from '../../../../lib/harness/workflow-drafts';
import { fileError, FilePolicyError, validateRevealRoot } from '../file/file-policy';
import { listDrafts, readWorkflowDraft, registerDraft, validateDraftIdentity } from './workflow-draft-store';
export const runtime = 'nodejs';
const headers = { 'Cache-Control': 'no-store', 'X-Content-Type-Options': 'nosniff' };
async function roots(projectRoot: unknown) {
  if (typeof projectRoot !== 'string') throw new FilePolicyError('INVALID_REQUEST', 400, 'Choose a current project folder.');
  const selected = await assertProjectRootAccessible(projectRoot);
  return { project: await validateRevealRoot({ projectRoot: selected }, resolveInstructionRootPath()), user: await realpath(homedir()) };
}
function errorResponse(error: unknown): Response {
  const typed = error as { type?: string; status?: number };
  const result = typeof typed?.type === 'string' && typeof typed.status === 'number'
    ? { status: typed.status, body: { error: { code: typed.type, message: 'The current folder is unavailable or outside the allowed workspace.' } } }
    : fileError(error);
  return NextResponse.json(result.body, { status: result.status, headers });
}
export async function GET(request: Request): Promise<Response> {
  try {
    const params = new URL(request.url).searchParams;
    if ([...params.keys()].some(key => !['projectRoot', 'name', 'source'].includes(key)) ||
        params.getAll('projectRoot').length !== 1 || params.getAll('name').length > 1 || params.getAll('source').length > 1 ||
        params.has('name') !== params.has('source')) throw new FilePolicyError('INVALID_REQUEST', 400, 'Choose a project folder and optionally one draft name and source.');
    const sources = await roots(params.get('projectRoot'));
    if (params.has('name')) {
      const name = params.get('name'); const source = params.get('source');
      validateDraftIdentity(name, source);
      return NextResponse.json({ drafts: [await readWorkflowDraft(sources[source as WorkflowDraftSource], name, source as WorkflowDraftSource)] }, { headers });
    }
    const drafts = [...await listDrafts(sources.project, 'project'), ...await listDrafts(sources.user, 'user')];
    return NextResponse.json({ drafts }, { headers });
  } catch (error) { return errorResponse(error); }
}
function hasLocalOrigin(request: Request): boolean {
  const requested = new URL(request.url);
  const host = request.headers.get('host') ?? requested.host;
  const origin = request.headers.get('origin');
  if (!origin || request.headers.get('sec-fetch-site') === 'cross-site') return false;
  try {
    // Next may normalize Request.url to localhost; Host retains the renderer’s
    // actual loopback address. Match its port as well and reject rebinding hosts.
    const expected = new URL(`${requested.protocol}//${host}`);
    const loopback = new Set(['localhost', '127.0.0.1', '[::1]']);
    return requested.protocol === 'http:' && loopback.has(requested.hostname)
      && loopback.has(expected.hostname) && expected.host === host
      && origin === expected.origin;
  } catch { return false; }
}
export async function POST(request: Request): Promise<Response> {
  try {
    // Browser callers must originate from this app, including on localhost.
    if (!hasLocalOrigin(request))
      throw new FilePolicyError('INVALID_ORIGIN', 403, 'Workflow registration requires a request from this app.');
    if (!request.headers.get('content-type')?.startsWith('application/json')) throw new FilePolicyError('INVALID_REQUEST', 400, 'Workflow registration requires JSON.');
    const reader = request.body?.getReader();
    const chunks: Uint8Array[] = [];
    let size = 0;
    if (reader) {
      try {
        for (;;) {
          const chunk = await reader.read();
          if (chunk.done) break;
          size += chunk.value.length;
          if (size > 4096) { await reader.cancel(); throw new FilePolicyError('INVALID_REQUEST', 400, 'Workflow registration request is too large.'); }
          chunks.push(chunk.value);
        }
      } finally { reader.releaseLock(); }
    }
    const raw = Buffer.concat(chunks).toString('utf8');
    let body: Record<string, unknown>;
    try { body = JSON.parse(raw); } catch { throw new FilePolicyError('INVALID_REQUEST', 400, 'Workflow registration requires valid JSON.'); }
    if (!body || typeof body !== 'object' || Array.isArray(body) || Object.keys(body).some(key => !['projectRoot', 'name', 'source', 'reviewToken'].includes(key)))
      throw new FilePolicyError('INVALID_REQUEST', 400, 'Invalid workflow registration request.');
    validateDraftIdentity(body.name, body.source);
    const sources = await roots(body.projectRoot);
    return NextResponse.json(await registerDraft(sources[body.source as WorkflowDraftSource], body.name, body.source as WorkflowDraftSource, body.reviewToken as string), { headers });
  } catch (error) { return errorResponse(error); }
}
