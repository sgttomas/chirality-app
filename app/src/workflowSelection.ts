// The displayed pending choice is for one opaque App home source and chat.
// Inspection with no chat is explicit and never supplies a new-chat default.
type Json = any;
export function chatWorkflow(data: Json, sourceRef: string | undefined, thread: string): Json {
  if (!sourceRef || !thread) return undefined;
  return (data?.selections ?? []).find((row: Json) => row.sourceRef === sourceRef && row.threadId === thread)?.selection;
}
export function workflowContext(data: Json, host: Json, thread: string): Json {
  const source = data?.context;
  if (!source?.sourceRef || host?.workflowRoot?.context?.sourceRef !== source.sourceRef || JSON.stringify(source.generation) !== JSON.stringify(host?.generation)) return undefined;
  if (thread && !(host?.threads ?? []).some((row: Json) => row.threadId === thread && JSON.stringify(row.generation) === JSON.stringify(source.generation))) return undefined;
  return structuredClone({sourceRef:source.sourceRef,generation:source.generation,historyEpoch:source.historyEpoch ?? null,
    threadId:thread || null,selectionRef:chatWorkflow(data, source.sourceRef, thread)?.reference ?? null,
    inspectionRef:data?.inspection?.reference ?? null,libraryRef:data?.activeLibrary ?? null});
}
const scoped = new Set(["workflow_select_development", "workflow_select_production_bundle", "workflow_select_production_copy",
  "workflow_select_registered", "workflow_select_listed", "workflow_follow_newer_revision", "workflow_create_draft",
  "workflow_open_library", "workflow_open_project_library", "workflow_observe_drafts", "workflow_prepare_run", "workflow_end_and_start"]);
export function workflowArguments(command: string, args: Record<string, unknown>, data: Json, host: Json, thread: string): Record<string, unknown> {
  if (!scoped.has(command)) return args;
  const target = typeof args.threadId === "string" ? args.threadId : thread;
  const context = workflowContext(data, host, target);
  if (!context) throw new Error("Workflow source or chat changed; refresh the displayed choice before acting");
  return {...args, context};
}
