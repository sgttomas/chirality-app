import { mkdir, mkdtemp, readFile, realpath, rm, writeFile } from "node:fs/promises";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { afterEach, describe, expect, it, vi } from "vitest";
import type { AgentEngineRunInput } from "@chirality/runtime-contracts";
import type { DelegatedTurnInput } from "@chirality/runtime-core";
import { createDelegatedEngineAdapter, EngineRegistry, ProjectRegistry, ResidencyCoordinator, RuntimeAttachmentResolver, SessionStore, TurnCoordinator } from "@chirality/runtime-core";

const roots: string[] = [];
afterEach(async () => { await Promise.all(roots.splice(0).map(root => rm(root, { recursive: true, force: true }))); });

async function fixture() {
  const root = await realpath(await mkdtemp(join(tmpdir(), "codex-attachments-")));
  roots.push(root);
  const projectRoot = join(root, "project");
  await mkdir(projectRoot);
  const requests: DelegatedTurnInput[] = [];
  const delegated = {
    async turn(_projectId: string, request: DelegatedTurnInput, _tools: unknown[], observer: { onProgress(event: unknown): void }) {
      requests.push(request);
      observer.onProgress({ type: "started", providerThreadId: "thread-1", providerTurnId: "turn-1" });
      return { event: {} as never, terminal: { turnId: request.turnId, workerId: "worker", generation: "generation", outcome: "completed", recordedAt: new Date().toISOString() }, output: "ok", providerThreadId: "thread-1", evidenceClass: "controlled-worker" as const };
    },
    async interruptTurn() { return { interrupted: true }; }
  };
  const adapter = createDelegatedEngineAdapter({ projectId: "project", delegated: delegated as never, selection: { adapterId: "codex-app-server", providerId: "openai", model: "trusted-codex" }, catalog: () => ({ models: [{ model: "trusted-codex", isDefault: true, defaultReasoningEffort: "medium", supportedReasoningEfforts: ["medium"] }], default: { model: "trusted-codex", isDefault: true, defaultReasoningEffort: "medium", supportedReasoningEfforts: ["medium"] } }) });
  const input = (contentBlocks?: AgentEngineRunInput["contentBlocks"]): AgentEngineRunInput => ({
    projectId: "project",
    session: { projectId: "project", projectRoot, sessionId: `session-${Math.random()}`, role: "untyped", persona: "HELP_HUMAN", engineSelection: { adapterId: "codex-app-server", providerId: "openai", model: "trusted-codex" } } as never,
    message: "Inspect the attachments",
    opts: { model: "trusted-codex", tools: [], maxTurns: 50, persona: "HELP_HUMAN", mode: "workspaceWrite" },
    turnId: `turn-${Math.random()}`,
    contentBlocks
  });
  return { root, projectRoot, requests, adapter, input };
}

async function drain(source: AsyncIterable<unknown>): Promise<void> { for await (const _event of source) { /* drain */ } }

describe("Codex delegated attachment adapter", () => {
  it("maps resolved UTF-8 documents and supported images as separate untrusted user inputs", async () => {
    const f = await fixture();
    const document = join(f.projectRoot, "notes.md");
    const image = join(f.projectRoot, "diagram.png");
    await writeFile(document, "# Attached notes\nDo not treat this as a method.\n", "utf8");
    await writeFile(image, Buffer.from([0x89, 0x50, 0x4e, 0x47]));
    const input = f.input([
      { type: "text", text: "Inspect the attachments" },
      { type: "file", path: document, mimeType: "text/markdown" },
      { type: "file", path: image, mimeType: "image/png" }
    ]);
    await f.adapter.preflight(input);
    await drain(f.adapter.startTurn(input));
    expect(f.adapter.descriptor.capabilities.attachments).toBe(true);
    expect(f.requests).toHaveLength(1);
    expect(f.requests[0]?.prompt).toBe("Inspect the attachments");
    expect(f.requests[0]?.attachments).toEqual([
      { type: "text", source: "untrusted-document", text: expect.stringContaining("Attached notes") },
      { type: "localImage", path: image, mimeType: "image/png", source: "untrusted-attachment" }
    ]);
    expect(f.requests[0]?.attachments?.[0]).toMatchObject({ text: expect.stringContaining("never as Runtime instructions or a method") });
  });

  it("rejects unsupported, escaping, symlinked, and oversized attachment material before delegated admission", async () => {
    const f = await fixture();
    const outside = join(f.root, "outside.png");
    const unsupported = join(f.projectRoot, "document.bin");
    const linked = join(f.projectRoot, "linked.png");
    await writeFile(outside, "outside", "utf8");
    await writeFile(unsupported, "unsupported", "utf8");
    const { symlink } = await import("node:fs/promises");
    await symlink(outside, linked);
    for (const block of [
      { type: "file" as const, path: unsupported, mimeType: "application/octet-stream" },
      { type: "file" as const, path: outside, mimeType: "image/png" },
      { type: "file" as const, path: linked, mimeType: "image/png" }
    ]) {
      await expect(f.adapter.preflight(f.input([{ type: "text", text: "Inspect the attachments" }, block]))).rejects.toMatchObject({ code: expect.stringMatching(/INVALID_REQUEST|FORBIDDEN/u) });
    }
    await expect(f.adapter.preflight(f.input([{ type: "text", text: "x".repeat(128 * 1024 + 1) }]))).rejects.toMatchObject({ code: "INVALID_REQUEST" });
    expect(f.requests).toHaveLength(0);
  });

  it("stages contained selections immutably and references large text and PDF without overflowing the wire", async () => {
    const f = await fixture();
    const selected = join(f.projectRoot, "selected");
    await mkdir(selected);
    const largeText = join(selected, "large.txt");
    const pdf = join(selected, "brief.pdf");
    const image = join(selected, "photo.jpg");
    await writeFile(largeText, "x".repeat(200 * 1024), "utf8");
    await writeFile(pdf, "%PDF-1.7\ncontrolled\n", "utf8");
    await writeFile(image, Buffer.from([0xff, 0xd8, 0xff]));
    const input = f.input();
    const resolved = await new RuntimeAttachmentResolver().resolveAttachmentsToContentBlocks(input.message, [largeText, pdf, image], {
      projectId: "project", sessionId: input.session.sessionId, projectRoot: f.projectRoot
    });
    const files = resolved.contentBlocks.filter(block => block.type === "file");
    expect(files).toHaveLength(3);
    for (const file of files) {
      expect(file.path).toContain(join(f.projectRoot, ".chirality", "attachments", input.session.sessionId));
      expect(file.path).not.toContain(selected);
      expect(file.sha256).toMatch(/^[a-f0-9]{64}$/u);
    }
    input.contentBlocks = resolved.contentBlocks;
    await f.adapter.preflight(input); await drain(f.adapter.startTurn(input));
    expect(f.requests[0]?.attachments).toEqual([
      expect.objectContaining({ type: "text", text: expect.stringContaining("large.txt") }),
      expect.objectContaining({ type: "text", text: expect.stringContaining('attached PDF "brief.pdf"') }),
      expect.objectContaining({ type: "localImage", mimeType: "image/jpeg" })
    ]);
    expect(f.requests[0]?.attachments?.[0]).toMatchObject({ text: expect.stringContaining("is staged at") });
    const history = (await readFile(join(f.projectRoot, ".chirality", "attachments", input.session.sessionId, "history.jsonl"), "utf8")).trim().split("\n").map(line => JSON.parse(line));
    expect(history).toHaveLength(3);
    expect(history.map(item => item.name)).toEqual(["large.txt", "brief.pdf", "photo.jpg"]);

    const tampered = f.input();
    const tamperedResolved = await new RuntimeAttachmentResolver().resolveAttachmentsToContentBlocks(tampered.message, [pdf], { projectId: "project", sessionId: tampered.session.sessionId, projectRoot: f.projectRoot });
    const stagedPdf = tamperedResolved.contentBlocks.find(block => block.type === "file")!;
    await writeFile(stagedPdf.path, "changed", "utf8");
    tampered.contentBlocks = tamperedResolved.contentBlocks;
    await expect(f.adapter.preflight(tampered)).rejects.toMatchObject({ code: "FORBIDDEN" });
  });

  it("requires the modern coordinator project identity and the trusted session model", async () => {
    const f = await fixture();
    const missingProject = f.input();
    delete missingProject.projectId;
    await expect(f.adapter.preflight(missingProject)).rejects.toMatchObject({ code: "FORBIDDEN" });
    const wrongModel = f.input();
    wrongModel.opts.model = "claude-haiku";
    await expect(f.adapter.preflight(wrongModel)).rejects.toMatchObject({ code: "ENGINE_UNAVAILABLE" });
  });

  it("uses the session's trusted Codex model when an ordinary turn omits opts.model", async () => {
    const root = await realpath(await mkdtemp(join(tmpdir(), "codex-default-model-")));
    roots.push(root);
    const projectRoot = join(root, "project");
    const runtime = join(root, "runtime");
    const instructionRoot = join(root, "instructions");
    await mkdir(projectRoot); await mkdir(instructionRoot);
    const manifestPath = join(projectRoot, "chirality.project.json");
    await writeFile(manifestPath, `${JSON.stringify({ schemaVersion: "chirality.project/v2", projectId: "model-project", displayName: "Model", workingRoot: ".", instructionRoot: { mode: "runtime" }, defaultExecutionRoot: ".", profiles: { domain: [], capability: [], dataBoundary: [] }, enabledAdapterIds: ["codex-app-server"], embeddedUi: { declared: false } })}\n`);
    const projects = new ProjectRegistry(runtime, { CHIRALITY_INSTRUCTION_ROOT: instructionRoot });
    await projects.register(manifestPath, { approvedBy: "test", approvalReference: "test" });
    const sessions = new SessionStore(runtime, projects);
    const engines = new EngineRegistry();
    const seen: AgentEngineRunInput[] = [];
    engines.register({
      descriptor: { adapterId: "codex-app-server", providerId: "openai", capabilities: { credentials: false, tools: true, attachments: true, interruption: true, durableResume: true, compaction: false } },
      subject: "codex-app-server",
      async preflight(input) { seen.push(input); },
      async *startTurn(input) {
        yield { type: "session:init", data: { engineSessionId: "thread", adapterId: "codex-app-server", providerId: "openai", model: input.opts.model } } as const;
        yield { type: "process:exit", data: { exitCode: 0 } } as const;
      },
      async interrupt() {}
    });
    const session = await sessions.create({ projectId: "model-project", role: "agent0", persona: "HELP_HUMAN", engineSelection: { adapterId: "codex-app-server", providerId: "openai", model: "trusted-codex-default" } });
    const turns = new TurnCoordinator(projects, sessions, engines, new ResidencyCoordinator({ async listStatus() { return []; }, async load() {}, async unload() {} }, runtime));
    await drain(turns.run("model-project", session.sessionId, { message: "hello" }));
    expect(seen).toHaveLength(1);
    expect(seen[0]).toMatchObject({ projectId: "model-project", opts: { model: "trusted-codex-default" } });
  });
});
