import type {
  ChiralityRoleName,
  ExportNativePlanResponse,
  MethodDescriptor,
  MethodInspectionResponse,
  MethodReference,
  MethodsResponse,
  NativePlanCapabilityResponse,
  NativePlanClarificationsResponse,
  NativePlanRevisionsResponse,
  ReplaceSelectedMethodsRequest,
  ReplaceSelectedMethodsResponse,
  ResolveSelectedContextResponse,
  ReplyNativePlanClarificationRequest,
  ReplyNativePlanClarificationResponse,
  RoleDescriptor,
  RolesResponse,
  QualifiedMethodReference
} from '@chirality/runtime-contracts/v3';

export type { ChiralityRoleName, MethodDescriptor, MethodReference, QualifiedMethodReference, RoleDescriptor } from '@chirality/runtime-contracts/v3';
export type InteractionMode = 'chat' | 'native-plan';

export class MethodSelectionClientError extends Error {
  constructor(readonly status: number, message: string) {
    super(message);
    this.name = 'MethodSelectionClientError';
  }
}

async function requestJson<T>(url: string, init?: RequestInit): Promise<T> {
  const response = await fetch(url, init);
  let payload: unknown;
  try { payload = await response.json(); } catch { payload = undefined; }
  if (!response.ok) {
    const message = payload && typeof payload === 'object' && 'error' in payload &&
      typeof (payload as { error?: { message?: unknown } }).error?.message === 'string'
      ? (payload as { error: { message: string } }).error.message
      : 'The Runtime method service is unavailable.';
    throw new MethodSelectionClientError(response.status, message);
  }
  return payload as T;
}

export function qualifiedMethodId(method: Pick<MethodDescriptor, 'sourceRootId' | 'source' | 'kind' | 'name'>): string {
  return 'qualifiedId' in method ? String(method.qualifiedId) : [method.sourceRootId, method.source, method.kind, method.name].map(encodeURIComponent).join(':');
}

export async function listRoles(projectRoot: string, signal?: AbortSignal): Promise<readonly RoleDescriptor[]> {
  const result = await requestJson<RolesResponse>(`/api/harness/roles?projectRoot=${encodeURIComponent(projectRoot)}`, { signal });
  return result.roles;
}

export async function listMethods(projectRoot: string, query = '', signal?: AbortSignal): Promise<MethodsResponse> {
  const params = new URLSearchParams({ projectRoot });
  if (query.trim()) params.set('query', query.trim());
  return requestJson<MethodsResponse>(`/api/harness/methods?${params}`, { signal });
}

export async function inspectMethod(projectRoot: string, method: MethodDescriptor, signal?: AbortSignal): Promise<MethodInspectionResponse> {
  const params = new URLSearchParams({ projectRoot, qualifiedId: qualifiedMethodId(method) });
  return requestJson<MethodInspectionResponse>(`/api/harness/methods/inspect?${params}`, { signal });
}

export async function replaceSelectedMethods(
  sessionId: string,
  methods: readonly MethodReference[] | undefined,
  transition: Partial<Pick<ReplaceSelectedMethodsRequest, 'expectedBasisId' | 'expectedRevision' | 'roleId' | 'boundaryConfirmed' | 'selectionMode'>> = {}
): Promise<ReplaceSelectedMethodsResponse> {
  return requestJson(`/api/harness/session/${encodeURIComponent(sessionId)}/methods`, {
    method: 'PUT', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ ...(methods === undefined ? {} : { methods }), ...transition })
  });
}

export async function resolveSelectedContext(input: {
  sessionId: string; roleId: ChiralityRoleName; methods: readonly MethodReference[];
  interactionMode: InteractionMode; permissionMode: 'readOnly' | 'ask' | 'workspaceWrite' | 'bypass';
}): Promise<ResolveSelectedContextResponse> {
  return requestJson(`/api/harness/session/${encodeURIComponent(input.sessionId)}/context/resolve`, {
    method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({
      roleId: input.roleId, methods: input.methods, interactionMode: input.interactionMode, permissionMode: input.permissionMode
    })
  });
}

export async function getNativePlanCapability(sessionId: string, signal?: AbortSignal): Promise<NativePlanCapabilityResponse> {
  return requestJson(`/api/harness/session/${encodeURIComponent(sessionId)}/native-plan/capability`, { signal });
}

export async function listNativePlanRevisions(sessionId: string, signal?: AbortSignal): Promise<NativePlanRevisionsResponse> {
  return requestJson(`/api/harness/session/${encodeURIComponent(sessionId)}/native-plan/revisions`, { signal });
}

export async function listNativePlanClarifications(
  sessionId: string,
  signal?: AbortSignal
): Promise<NativePlanClarificationsResponse> {
  return requestJson(
    `/api/harness/session/${encodeURIComponent(sessionId)}/native-plan/clarifications`,
    { signal }
  );
}

export async function replyNativePlanClarification(input: {
  sessionId: string;
  requestId: string | number;
  answers: ReplyNativePlanClarificationRequest['answers'];
}): Promise<ReplyNativePlanClarificationResponse> {
  return requestJson(
    `/api/harness/session/${encodeURIComponent(input.sessionId)}/native-plan/clarifications/reply`,
    {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ requestId: input.requestId, answers: input.answers })
    }
  );
}

/** App file handoff only. Runtime plan evidence remains in conversation history. */
export async function exportNativePlanRevision(input: {
  sessionId: string; revision: number; targetRelativePath: string; overwrite?: boolean;
}): Promise<ExportNativePlanResponse> {
  return requestJson(`/api/harness/session/${encodeURIComponent(input.sessionId)}/native-plan/export`, {
    method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({
      revision: input.revision, targetRelativePath: input.targetRelativePath,
      ...(input.overwrite ? { overwrite: true } : {})
    })
  });
}
