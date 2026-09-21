/** GET response shapes for contained file previews; no workflow authority is inferred. */
export type WorkflowFile = { name: string; path: string; size: number; modifiedAt: string };
export type WorkflowList = { projectRoot: string; files: WorkflowFile[]; directoryMissing: boolean };
export type WorkflowPreview = { projectRoot: string; file: WorkflowFile; content: string; sha256: string };
