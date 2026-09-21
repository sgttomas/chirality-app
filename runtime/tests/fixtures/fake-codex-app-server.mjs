// Controlled stand-in for the stock `codex app-server` JSON-RPC surface. It
// speaks the v2 shapes the daemon relies on (thread/start, thread/resume,
// thread/settings/update, turn/start, turn/interrupt, account/*, model/list)
// and scripts a turn from the prompt text. No account data ever appears here.
export function createFakeCodexServer(options = {}) {
  const state = { signedIn: options.signedIn ?? true, threads: new Map(), nextThread: 1, nextTurn: 1, login: undefined, requests: [], notes: [] };
  let sink = () => {};
  let nextServerId = 1000;
  const pendingServerRequests = new Map();
  const liveTurns = new Map();
  const send = frame => sink(`${JSON.stringify(frame)}\n`);
  const notify = (method, params) => send({ jsonrpc: "2.0", method, params });
  const serverRequest = (method, params) => { const id = nextServerId++; return new Promise(resolve => { pendingServerRequests.set(id, resolve); send({ jsonrpc: "2.0", id, method, params }); }); };
  const delay = ms => new Promise(resolve => setTimeout(resolve, ms));
  const models = [
    { id: "gpt-5-codex", model: "gpt-5-codex", displayName: "GPT-5 Codex", hidden: false, supportedReasoningEfforts: [{ reasoningEffort: "medium", description: "" }, { reasoningEffort: "high", description: "" }], defaultReasoningEffort: "medium", isDefault: true },
    { id: "gpt-5-mini", model: "gpt-5-mini", displayName: "GPT-5 mini", hidden: false, supportedReasoningEfforts: [{ reasoningEffort: "low", description: "" }, { reasoningEffort: "medium", description: "" }], defaultReasoningEffort: "low", isDefault: false },
    { id: "hidden-model", model: "hidden-model", displayName: "Hidden", hidden: true, supportedReasoningEfforts: [], defaultReasoningEffort: "low", isDefault: false }
  ];

  async function runTurn(thread, turn, input) {
    // Scripted behaviour keys off the user prompt, which is the last text item; an
    // attachments may precede it.
    const text = input.filter(item => item.type === "text").at(-1)?.text ?? "";
    const live = { interrupted: false, resolveInterrupt: undefined };
    liveTurns.set(turn.id, live);
    notify("turn/started", { threadId: thread.id, turn: { ...turn, status: "inProgress" } });
    if (text.includes("hang")) {
      await new Promise(resolve => { live.resolveInterrupt = resolve; });
      liveTurns.delete(turn.id);
      notify("turn/completed", { threadId: thread.id, turn: { ...turn, status: "interrupted" } });
      return;
    }
    if (text.includes("fail")) {
      liveTurns.delete(turn.id);
      notify("turn/completed", { threadId: thread.id, turn: { ...turn, status: "failed", error: { message: "scripted failure", codexErrorInfo: "other", additionalDetails: null } } });
      return;
    }
    if (text.includes("approve")) {
      const itemId = `cmd-${turn.id}`;
      notify("item/started", { threadId: thread.id, turnId: turn.id, item: { type: "commandExecution", id: itemId, command: "ls", cwd: thread.cwd, status: "inProgress", processId: null, commandActions: [], aggregatedOutput: null, exitCode: null, durationMs: null } });
      const decision = await serverRequest("item/commandExecution/requestApproval", { threadId: thread.id, turnId: turn.id, itemId, approvalId: null, reason: "scripted", command: "ls", cwd: thread.cwd, commandActions: [], proposedExecpolicyAmendment: null, availableDecisions: null, additionalPermissions: null, networkApprovalContext: null });
      state.notes.push({ decision });
      notify("serverRequest/resolved", { threadId: thread.id, requestId: null });
      const accepted = decision && (decision.decision === "accept" || decision.decision === "acceptForSession");
      notify("item/completed", { threadId: thread.id, turnId: turn.id, item: { type: "commandExecution", id: itemId, command: "ls", cwd: thread.cwd, status: accepted ? "completed" : "declined", processId: null, commandActions: [], aggregatedOutput: accepted ? "file\n" : null, exitCode: accepted ? 0 : null, durationMs: 1 } });
    }
    if (text.includes("question")) {
      const itemId = `ask-${turn.id}`;
      const answers = await serverRequest("item/tool/requestUserInput", { threadId: thread.id, turnId: turn.id, itemId, questions: [{ id: "q1", header: "Scope", question: "Which scope?", isOther: false, isSecret: false, options: null }], isBlocking: true, autoResolutionMs: null });
      state.notes.push({ answers });
    }
    if (text.includes("plan") && thread.mode === "plan") {
      notify("item/completed", { threadId: thread.id, turnId: turn.id, item: { type: "plan", id: `plan-${turn.id}`, text: "1. Look\n2. Act" } });
    }
    const messageId = `msg-${turn.id}`;
    const reply = `echo: ${text.split("\n").pop()}`;
    notify("item/started", { threadId: thread.id, turnId: turn.id, item: { type: "agentMessage", id: messageId, text: "", phase: "final_answer" } });
    notify("item/agentMessage/delta", { threadId: thread.id, turnId: turn.id, itemId: messageId, delta: reply.slice(0, 5) });
    await delay(1);
    notify("item/completed", { threadId: thread.id, turnId: turn.id, item: { type: "agentMessage", id: messageId, text: reply, phase: "final_answer" } });
    liveTurns.delete(turn.id);
    notify("turn/completed", { threadId: thread.id, turn: { ...turn, status: "completed" } });
  }

  function handle(frame) {
    const { id, method, params } = frame;
    if (typeof method !== "string") {
      if (id !== undefined && pendingServerRequests.has(id)) { const settle = pendingServerRequests.get(id); pendingServerRequests.delete(id); settle(frame.error !== undefined ? { error: frame.error } : frame.result); }
      return;
    }
    state.requests.push({ method, params });
    const reply = result => { if (id !== undefined) send({ jsonrpc: "2.0", id, result }); };
    const fail = (code, message) => { if (id !== undefined) send({ jsonrpc: "2.0", id, error: { code, message } }); };
    switch (method) {
      case "initialize": return reply({ userAgent: "fake-codex/0.154.0", codexHome: process.env.CODEX_HOME ?? "", platformFamily: "unix", platformOs: "macos" });
      case "initialized": return;
      case "account/read": return reply(state.signedIn ? { account: { type: "chatgpt", planType: "plus" }, requiresOpenaiAuth: false } : { account: null, requiresOpenaiAuth: true });
      case "account/login/start": { state.login = { loginId: `login-${Date.now()}`, pending: true }; return reply({ type: "chatgpt", loginId: state.login.loginId, authUrl: "https://auth.example.test/authorize?state=opaque" }); }
      case "account/login/cancel": { if (state.login) state.login.pending = false; return reply({ status: "cancelled" }); }
      case "account/logout": { state.signedIn = false; return reply({}); }
      case "model/list": return reply({ data: state.signedIn ? models : [], nextCursor: null });
      case "collaborationMode/list": return reply({ data: [{ name: "Plan", mode: "plan", model: null, reasoning_effort: null, developer_instructions: null }, { name: "Default", mode: "default", model: null, reasoning_effort: null, developer_instructions: null }] });
      case "thread/start": {
        const thread = { history: params?.developerInstructions ? [{ type: "message", role: "developer", content: [{ type: "input_text", text: params.developerInstructions }] }] : [], loaded: true, developerInstructions: params?.developerInstructions, config: params?.config, id: `thread-${state.nextThread++}`, cwd: params?.cwd ?? "", model: params?.model ?? "gpt-5-codex", mode: "default", policy: { approvalPolicy: params?.approvalPolicy, sandbox: params?.sandbox } };
        state.threads.set(thread.id, thread);
        notify("thread/started", { thread: { id: thread.id, parentThreadId: null } });
        return reply({ thread: { id: thread.id, preview: "", modelProvider: "openai", createdAt: 0, updatedAt: 0, path: null, cwd: thread.cwd, cliVersion: "0.154.0", source: "vscode", gitInfo: null, name: null, ephemeral: false, turns: [] }, model: thread.model, modelProvider: "openai", cwd: thread.cwd, instructionSources: [], approvalPolicy: thread.policy.approvalPolicy ?? "on-request", sandbox: { type: "readOnly", networkAccess: false }, reasoningEffort: null });
      }
      case "thread/resume": {
        const existing = state.threads.get(params?.threadId);
        const thread = existing ?? { history: [], id: params?.threadId, cwd: params?.cwd ?? "", model: params?.model ?? "gpt-5-codex", mode: "default", policy: {} };
        // Cold resume changes config but retains reconstructed model-visible history.
        if (!thread.loaded) { thread.developerInstructions = params?.developerInstructions; thread.config = params?.config; }
        thread.loaded = true;
        state.threads.set(thread.id, thread);
        return reply({ thread: { id: thread.id, cwd: thread.cwd, status: { type: "idle" } }, model: thread.model, modelProvider: "openai", cwd: thread.cwd, instructionSources: [], approvalPolicy: "on-request", sandbox: { type: "readOnly", networkAccess: false }, reasoningEffort: null });
      }
      case "thread/inject_items": {
        const thread = state.threads.get(params?.threadId);
        if (!thread?.loaded) return fail(-32602, "thread is not loaded");
        const outcome = state.injectionOutcome;
        state.injectionOutcome = undefined;
        if (outcome === "reject") return fail(-32000, "injection rejected");
        thread.history ??= [];
        thread.history.push(...structuredClone(params.items));
        if (outcome === "applied-error") return fail(-32000, "injection persistence acknowledgement failed");
        return reply({});
      }
      case "thread/loaded/list": return reply({ data: [...state.threads.values()].filter(thread => thread.loaded).map(thread => thread.id), nextCursor: null });
      case "thread/read": {
        const thread = state.threads.get(params?.threadId);
        return reply({ thread: { id: params?.threadId, parentThreadId: thread?.parentThreadId ?? null, status: { type: thread?.loaded ? thread.status ?? "idle" : "notLoaded" } } });
      }
      case "thread/unsubscribe": {
        const thread = state.threads.get(params?.threadId);
        if (!thread?.loaded) return reply({ status: "notLoaded" });
        thread.loaded = false;
        reply({ status: "unsubscribed" });
        notify("thread/closed", { threadId: thread.id });
        return;
      }
      case "thread/settings/update": {
        const thread = state.threads.get(params?.threadId);
        if (!thread) return fail(-32602, "unknown thread");
        thread.mode = params?.collaborationMode?.mode ?? thread.mode;
        return reply({});
      }
      case "turn/start": {
        const thread = state.threads.get(params?.threadId);
        if (!thread) return fail(-32602, "unknown thread");
        state.notes.push({ modelHistory: structuredClone(thread.history ?? []) });
        const turn = { id: `turn-${state.nextTurn++}`, items: [], status: "inProgress", error: null };
        reply({ turn });
        void runTurn(thread, turn, Array.isArray(params?.input) ? params.input : []);
        return;
      }
      case "turn/interrupt": {
        const live = liveTurns.get(params?.turnId);
        reply({});
        if (live?.resolveInterrupt) live.resolveInterrupt();
        return;
      }
      case "chirality/never": return; // deliberately never answered
      default: return fail(-32601, `unknown method ${method}`);
    }
  }
  let buffer = "";
  return {
    state,
    attach(write) { sink = write; },
    feed(chunk) {
      buffer += chunk;
      let index;
      while ((index = buffer.indexOf("\n")) >= 0) {
        const line = buffer.slice(0, index); buffer = buffer.slice(index + 1);
        if (!line.trim()) continue;
        try { handle(JSON.parse(line)); } catch (error) { state.notes.push({ malformed: String(error) }); }
      }
    },
    notify,
    serverRequest
  };
}
