// The App's words for the values Codex sends in fields with a fixed vocabulary (the pinned app-server protocol,
// resources/supplier/0.167.0/codex_app_server_protocol.v2.schemas.json). A value in a table is shown in the App's
// word for it; any other value, including one a later Codex adds, is shown boxed as Codex's text (Word and wordOf,
// AgentText.tsx). A generated type is no guarantee at run time: the host keeps native values as it receives them.
// Every export here is a table of literal words; the presentation guard's test checks that.

/** TurnStatus. */
export const TURN_STATUS = { completed: "completed", interrupted: "interrupted", failed: "failed", inProgress: "in progress" } as const;
/** The status of an item: CommandExecutionStatus, PatchApplyStatus, McpToolCallStatus, DynamicToolCallStatus, CollabAgentToolCallStatus. */
export const ITEM_STATUS = { inProgress: "in progress", completed: "completed", failed: "failed", declined: "declined", interrupted: "interrupted" } as const;
/** CollabAgentStatus: a delegated agent's state as Codex reports it. */
export const AGENT_STATUS = { pendingInit: "starting", running: "running", interrupted: "interrupted", completed: "completed", errored: "errored", shutdown: "shut down", notFound: "not found" } as const;
/** CollabAgentTool. */
export const AGENT_TOOL = { spawnAgent: "start an agent", sendInput: "send input", resumeAgent: "resume an agent", wait: "wait", closeAgent: "close an agent", sendMessage: "send a message", followupTask: "follow-up task", interruptAgent: "interrupt an agent", listAgents: "list agents" } as const;
/** ReasoningEffort. */
export const REASONING_EFFORT = { none: "none", minimal: "minimal", low: "low", medium: "medium", high: "high", xhigh: "extra high" } as const;
/** MessagePhase. */
export const MESSAGE_PHASE = { commentary: "commentary", partial_answer: "partial answer", final_answer: "final answer" } as const;
/** CommandExecutionSource. */
export const COMMAND_SOURCE = { agent: "the agent", userShell: "your shell", unifiedExecStartup: "a session start", unifiedExecInteraction: "a session interaction" } as const;
/** PatchChangeKind. */
export const CHANGE_KIND = { add: "add", delete: "delete", update: "update" } as const;
/** ThreadItem's type. */
export const ITEM_KIND = {
  userMessage: "user message", hookPrompt: "hook prompt", agentMessage: "agent message", functionCallOutput: "function call output", plan: "plan",
  reasoning: "reasoning", commandExecution: "command", fileChange: "file change", mcpToolCall: "MCP tool call", dynamicToolCall: "dynamic tool call",
  collabAgentToolCall: "delegation", subAgentActivity: "sub-agent activity", webSearch: "web search", imageView: "image view", sleep: "sleep",
  imageGeneration: "image generation", enteredReviewMode: "entered review mode", exitedReviewMode: "exited review mode", contextCompaction: "context compaction",
} as const;
/** TurnPlanStepStatus. */
export const STEP_STATUS = { pending: "pending", inProgress: "in progress", completed: "completed" } as const;
/** TurnItemsView. */
export const ITEMS_VIEW = { notLoaded: "not loaded", summary: "summary", full: "full" } as const;
/** SubAgentSource. */
export const SUBAGENT_KIND = { review: "review", compact: "compaction", memory_consolidation: "memory consolidation" } as const;
/** SubAgentActivityKind. */
export const SUBAGENT_ACTIVITY = { started: "started", interacted: "interacted", interrupted: "interrupted", completed: "completed" } as const;
/** A descendant's last observed status: CollabAgentStatus, or ThreadStatus's type. */
export const CHILD_STATUS = { pendingInit: "starting", running: "running", interrupted: "interrupted", completed: "completed", errored: "errored", shutdown: "shut down", notFound: "not found", notLoaded: "not loaded", idle: "idle", systemError: "system error", active: "active" } as const;
