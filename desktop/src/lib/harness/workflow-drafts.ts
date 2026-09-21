export type WorkflowDraftSource = 'project' | 'user';
export interface WorkflowDraft {
  name: string;
  source: WorkflowDraftSource;
  description: string;
  content: string;
  reviewToken: string;
  files: { path: string; sha256: string; size: number; mode?: string; content?: string }[];
  destinationExists: boolean;
  registered?: boolean;
}
export interface WorkflowDraftsResponse { drafts: WorkflowDraft[] }
export interface RegisterWorkflowDraftRequest {
  projectRoot: string; name: string; source: WorkflowDraftSource; reviewToken: string;
}
async function request<T>(url: string, init: RequestInit): Promise<T> {
  const response = await fetch(url, init);
  const body = await response.json();
  if (!response.ok) throw new Error(body?.error?.message ?? 'Workflow drafts are unavailable.');
  return body as T;
}
export function listWorkflowDrafts(projectRoot: string, signal?: AbortSignal): Promise<WorkflowDraftsResponse> {
  return request(`/api/working-root/workflow-drafts?${new URLSearchParams({ projectRoot })}`, { signal });
}
export function registerWorkflowDraft(input: RegisterWorkflowDraftRequest, signal?: AbortSignal): Promise<{ name: string; source: WorkflowDraftSource; path: string }> {
  return request('/api/working-root/workflow-drafts', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(input), signal });
}
