import { describe, expect, it } from "vitest";
import type { AgentEngineRunInput, HarnessEvent, UIEvent } from "@chirality/runtime-contracts";
import { createDelegatedEngineAdapter } from "@chirality/runtime-core";

async function project(scripted: readonly (readonly [string, unknown])[]): Promise<HarnessEvent[]> {
  const adapter = createDelegatedEngineAdapter({ selection: { adapterId: "codex", providerId: "openai", model: "test" }, delegated: {
      async turn(_project: string, request: { turnId: string }, _tools: unknown[], observer: { onProgress(event: unknown): void }) {
        observer.onProgress({ type: "started", providerThreadId: "parent", providerTurnId: "native" });
        for (const [method, params] of scripted) observer.onProgress({ type: "notification", providerThreadId: "parent", providerTurnId: "native", method, params, occurredAt: "now" });
        return { terminal: { outcome: "completed", turnId: request.turnId }, output: "", providerThreadId: "parent" };
      }
    } as never });
  const input: AgentEngineRunInput = { projectId: "p", session: { projectId: "p", projectRoot: "/tmp/project", sessionId: "s", role: "untyped", engineSelection: { adapterId: "codex", providerId: "openai", model: "test" } } as never,
      message: "hello", turnId: "runtime", opts: { model: "test", tools: [], maxTurns: 10, persona: "HELP_HUMAN", mode: "workspaceWrite" } };
  await adapter.preflight(input);
  const received: UIEvent[] = []; for await (const value of adapter.startTurn(input)) received.push(value);
  const events = received.filter((value): value is Extract<UIEvent,{type:"harness:event"}> => value.type === "harness:event").map(value => value.data);
  return events;
}

describe("Native item notifications across the delegated adapter", () => {
  it("retains message/summary/checklist updates and actual child identity independently of completed collaboration calls", async () => {
    const scripted = [
      ["item/agentMessage/delta", { threadId: "parent", turnId: "native", itemId: "m", delta: "hello" }],
      ["item/reasoning/summaryPartAdded", { threadId: "parent", turnId: "native", itemId: "r", summaryIndex: 0 }],
      ["item/reasoning/summaryTextDelta", { threadId: "parent", turnId: "native", itemId: "r", summaryIndex: 0, delta: "Checking" }],
      ["turn/plan/updated", { threadId: "parent", turnId: "native", explanation: null, plan: [{ step: "Check", status: "inProgress" }] }],
      ["turn/plan/updated", { threadId: "parent", turnId: "native", explanation: null, plan: [{ step: "Check", status: "completed" }] }],
      ["item/completed", { threadId: "parent", turnId: "native", item: { type: "collabAgentToolCall", id: "spawn", tool: "spawnAgent", status: "completed", receiverThreadIds: ["child"], agentsStates: { child: { status: "running", message: null } } } }],
      ["turn/started", { threadId: "child", turn: { id: "child-turn", status: "inProgress" } }],
      ["item/completed", { threadId: "child", turnId: "child-turn", item: { type: "agentMessage", id: "cm", text: "Child result", phase: "final_answer" } }],
      ["turn/completed", { threadId: "child", turn: { id: "child-turn", status: "completed" } }]
    ] as const;
    const events = await project(scripted);
    const native = events.filter(event => event.type === "codex.notification");
    expect(native.map(event => event.data.method)).toEqual(scripted.map(([method]) => method));
    expect(events.some(event => event.type === "subagent.completed")).toBe(false);
    expect(events).toContainEqual(expect.objectContaining({ type: "tool.completed", data: expect.objectContaining({ toolUseId: "spawn" }) }));
    expect(native.at(-1)?.data.codex).toMatchObject({ providerThreadId: "child", providerTurnId: "child-turn", isPrimaryThread: false });
    expect(native[0]?.data.codex).toMatchObject({ providerThreadId: "parent", providerTurnId: "native", isPrimaryThread: true });
    expect(native[5]?.data.params).toEqual(scripted[5][1]);
  });
  it("preserves stock v2 activity pairs for one child across item IDs and empty-target waits without fabricating legacy tasks", async () => {
    // Stock 0.154 multi_agents_v2::emit_sub_agent_activity emits both item
    // phases for every activity. A v2 wait carries no target/status map.
    const scope = { threadId: "parent", turnId: "native" };
    const activity = (id: string, kind: string) => ({ ...scope, item: { type: "subAgentActivity", id, kind, agentThreadId: "child-C", agentPath: "/root/checker" } });
    const pair = (params: unknown): (readonly [string, unknown])[] => [["item/started", params], ["item/completed", params]];
    const wait = (id: string, status: string) => ({ ...scope, item: { type: "collabAgentToolCall", id, tool: "wait", status, senderThreadId: "parent", receiverThreadIds: [], agentsStates: {}, prompt: null, model: null, reasoningEffort: null } });
    const scripted: (readonly [string, unknown])[] = [
      ...pair(activity("activity-A", "started")),
      ["item/started", wait("wait-1", "inProgress")], ["item/completed", wait("wait-1", "completed")],
      ["item/started", wait("wait-2", "inProgress")], ["item/completed", wait("wait-2", "completed")],
      ...pair(activity("activity-B", "completed")),
      ["turn/completed", { threadId: "parent", turn: { id: "native", status: "completed" } }]
    ];
    const events = await project(scripted);
    const native = events.filter(event => event.type === "codex.notification");
    expect(native.map(event => [event.data.method, event.data.params])).toEqual(scripted);
    expect(events.filter(event => event.type.startsWith("subagent."))).toEqual([]);
    const activities = native.filter(event => (event.data.params as { item?: { type?: string } }).item?.type === "subAgentActivity");
    expect(activities.map(event => (event.data.params as { item: unknown }).item)).toEqual([
      activity("activity-A", "started").item, activity("activity-A", "started").item,
      activity("activity-B", "completed").item, activity("activity-B", "completed").item
    ]);
    expect(new Set(activities.map(event => (event.data.params as { item: { agentThreadId: string } }).item.agentThreadId))).toEqual(new Set(["child-C"]));
    expect(events.filter(event => event.type === "tool.completed").map(event => event.data.agentThreadIds)).toEqual([[], []]);
    for (const event of activities) expect(event.data.codex).toMatchObject({ providerThreadId: "parent", providerTurnId: "native", isPrimaryThread: true });

    // Interactions and interruptions also keep their supplier kind, and parent
    // completion must not synthesize a terminal child activity that is absent.
    for (const kind of ["started", "interacted", "interrupted"]) {
      const partial = await project([...pair(activity("only-activity", kind)), scripted.at(-1)!]);
      expect(partial.filter(event => event.type.startsWith("subagent."))).toEqual([]);
      expect(partial.filter(event => event.type === "codex.notification").map(event => event.data.params)).toEqual([activity("only-activity", kind), activity("only-activity", kind), scripted.at(-1)![1]]);
    }
  });

});
