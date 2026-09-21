export type WorkflowFeedbackRequest = {
  sequence: number;
  projectRoot: string;
  name: string;
  source: 'project' | 'user';
};

export function workflowFeedbackPrompt(request: Omit<WorkflowFeedbackRequest, 'sequence'>): string {
  const location = request.source === 'project' ? '.chirality/workflow-drafts' : '~/.chirality/workflow-drafts';
  return `Revise the proposed workflow at ${location}/${request.name}/WORKFLOW.md. Keep it as a draft for my review; do not register it.\n\nChanges I want:\n`;
}
