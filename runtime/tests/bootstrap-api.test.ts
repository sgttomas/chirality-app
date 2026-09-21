import { mkdir, mkdtemp, readFile, realpath, rm, stat, symlink, writeFile } from "node:fs/promises";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { afterEach, describe, expect, it, vi } from "vitest";
import { AuthRegistry, EngineRegistry, ProjectRegistry, ResidencyCoordinator, RuntimeService, SessionStore, TurnCoordinator } from "@chirality/runtime-core";
import { RuntimeClient } from "@chirality/runtime-client";
import { RuntimeDaemon } from "@chirality/runtime-daemon";
import { HOSTED_BOOTSTRAP_CLIENT_ID, resolveHostedProjectTokenFile } from "../packages/daemon/src/hosted-paths.js";

const roots: string[] = [];
const daemons: RuntimeDaemon[] = [];
afterEach(async () => {
  await Promise.all(daemons.splice(0).map(daemon => daemon.stop().catch(() => undefined)));
  await Promise.all(roots.splice(0).map(root => rm(root, { recursive: true, force: true })));
});

function manifest(projectId: string) {
  return {
    schemaVersion: "chirality.project/v2",
    projectId,
    displayName: projectId,
    workingRoot: ".",
    instructionRoot: { mode: "runtime" },
    defaultExecutionRoot: ".",
    profiles: { domain: [], capability: [], dataBoundary: [] },
    enabledAdapterIds: ["codex-app-server"],
    embeddedUi: { declared: false }
  } as const;
}

async function setup(hostedBootstrap: any) {
  const root = await realpath(await mkdtemp(join(tmpdir(), "chirality-bootstrap-api-")));
  roots.push(root);
  const runtime = join(root, "runtime");
  const instructionRoot = join(root, "instructions");
  await mkdir(instructionRoot, { recursive: true });
  const projects = new ProjectRegistry(runtime, { CHIRALITY_INSTRUCTION_ROOT: instructionRoot });
  const sessions = new SessionStore(runtime, projects);
  const engines = new EngineRegistry();
  const residency = new ResidencyCoordinator({ async listStatus() { return []; }, async load() {}, async unload() {} }, runtime);
  const auth = new AuthRegistry(runtime);
  const service = new RuntimeService(projects, sessions, engines, residency, new TurnCoordinator(projects, sessions, engines, residency), auth, {
    async get() { return undefined; }, async status() { return { configured: false }; }, async set() {}, async remove() {}
  });
  const bootstrapClient = await auth.ensureClient(HOSTED_BOOTSTRAP_CLIENT_ID, ["runtime:read", "projects:write", "credentials:write"]);
  const socketPath = join(root, "runtime.sock");
  const daemon = new RuntimeDaemon({ runtimeDirectory: runtime, socketPath, service, hostedBootstrap });
  daemons.push(daemon);
  await daemon.start();
  return { root, runtime, projects, auth, daemon, bootstrapClient: new RuntimeClient({ socketPath, tokenFile: bootstrapClient.tokenFile }), socketPath };
}

describe("hosted bootstrap API", () => {
  it("registers an explicit manifest, derives provenance, and keeps the project token server-only", async () => {
    const status = { schema: "chirality-hosted-bootstrap-status/v1", projectId: "bootstrap-project", ceremony: "ready-to-start", admission: "unavailable", canStartLogin: true } as const;
    const grant = vi.fn(async (_projectId: string, _provenance: unknown, _signal?: AbortSignal) => ({ ...status, ceremony: "ready-to-start", canStartLogin: true } as const));
    const signOut = vi.fn(async (_projectId: string, _signal?: AbortSignal) => status);
    const port = { status: vi.fn(async () => status), grantProviderNetworkConsent: grant, startLogin: vi.fn(async () => ({ loginId: "login-1", authUrl: "https://auth.example.test/authorize?state=opaque" })), cancelLogin: vi.fn(async () => ({ ...status, ceremony: "cancelled", canStartLogin: true } as const)), signOut };
    const fixture = await setup(port);
    const projectRoot = join(fixture.root, "project");
    await mkdir(projectRoot);
    const manifestPath = join(projectRoot, "chirality.project.json");
    await writeFile(manifestPath, `${JSON.stringify(manifest("bootstrap-project"))}\n`, "utf8");

    const registered = await fixture.bootstrapClient.registerHostedBootstrapProject({ manifestPath });
    expect(registered).toEqual({ projectId: "bootstrap-project", manifestHash: expect.stringMatching(/^[a-f0-9]{64}$/u) });
    expect(Object.keys(registered).sort()).toEqual(["manifestHash", "projectId"]);
    const record = await fixture.projects.requireAuthorized("bootstrap-project");
    expect(record.clientId).toBe("hosted-project-bootstrap-project");
    expect(record.approval.approvedBy).toBe(`runtime-client:${HOSTED_BOOTSTRAP_CLIENT_ID}`);
    expect(record.approval.approvalReference).toMatch(/^hosted-bootstrap:[a-f0-9-]{36}:[a-f0-9-]{36}$/u);

    const projectTokenFile = resolveHostedProjectTokenFile(fixture.runtime, "bootstrap-project");
    expect((await stat(projectTokenFile)).mode & 0o777).toBe(0o600);
    const projectClient = new RuntimeClient({ socketPath: fixture.socketPath, tokenFile: projectTokenFile });
    expect((await projectClient.projectStatus("bootstrap-project")).project.projectId).toBe("bootstrap-project");
    await expect(projectClient.projectStatus("another-project")).rejects.toMatchObject({ code: "FORBIDDEN" });

    expect(await fixture.bootstrapClient.hostedBootstrapStatus("bootstrap-project")).toEqual(status);
    expect(await fixture.bootstrapClient.grantHostedProviderNetworkConsent("bootstrap-project")).toMatchObject({ ceremony: "ready-to-start" });
    expect(grant).toHaveBeenCalledWith("bootstrap-project", expect.objectContaining({
      approvedBy: `runtime-client:${HOSTED_BOOTSTRAP_CLIENT_ID}`,
      approvalReference: expect.stringMatching(/^hosted-bootstrap:/u),
      approvedAt: expect.stringMatching(/^\d{4}-\d{2}-\d{2}T/u)
    }), expect.any(AbortSignal));
    expect(grant.mock.calls[0]![2].aborted).toBe(false);
    expect(await fixture.bootstrapClient.startHostedBootstrapLogin("bootstrap-project")).toEqual({ loginId: "login-1", authUrl: "https://auth.example.test/authorize?state=opaque" });
    expect(await fixture.bootstrapClient.cancelHostedBootstrapLogin("bootstrap-project")).toMatchObject({ ceremony: "cancelled" });
    expect(await fixture.bootstrapClient.signOutHostedProject("bootstrap-project")).toEqual(status);
    expect(signOut).toHaveBeenCalledWith("bootstrap-project", expect.any(AbortSignal));
    expect(signOut.mock.calls[0]![1].aborted).toBe(false);
    await expect(fixture.bootstrapClient.requestJson("/v3/projects/bootstrap-project/hosted-bootstrap/logout", { method: "POST", body: { accountWide: true } })).rejects.toMatchObject({ code: "INVALID_REQUEST" });
  });

  it("initializes only an absent manifest and never overwrites an existing entry", async () => {
    const port = { status: vi.fn(), grantProviderNetworkConsent: vi.fn(), startLogin: vi.fn(), cancelLogin: vi.fn(async () => ({ schema: "chirality-hosted-bootstrap-status/v1", projectId: "unused", ceremony: "cancelled", admission: "unavailable", canStartLogin: true })), signOut: vi.fn() };
    const fixture = await setup(port);
    const projectRoot = join(fixture.root, "new-project");
    await mkdir(projectRoot);
    const response = await fixture.bootstrapClient.initializeHostedBootstrapProject({ projectRoot });
    const manifestPath = join(projectRoot, "chirality.project.json");
    const created = JSON.parse(await readFile(manifestPath, "utf8"));
    expect(response).toEqual({ projectId: created.projectId, manifestHash: expect.stringMatching(/^[a-f0-9]{64}$/u) });
    expect(created).toEqual({
      schemaVersion: "chirality.project/v2",
      projectId: expect.stringMatching(/^[a-f0-9-]{36}$/u),
      displayName: "new-project",
      workingRoot: ".",
      instructionRoot: { mode: "runtime" },
      defaultExecutionRoot: ".",
      profiles: { domain: [], capability: [], dataBoundary: [] },
      enabledAdapterIds: ["codex-app-server"],
      embeddedUi: { declared: false }
    });
    const firstBytes = await readFile(manifestPath, "utf8");
    expect((await fixture.bootstrapClient.initializeHostedBootstrapProject({ projectRoot })).projectId).toBe(created.projectId);
    expect(await readFile(manifestPath, "utf8")).toBe(firstBytes);

    const malformedRoot = join(fixture.root, "malformed");
    await mkdir(malformedRoot);
    const malformedPath = join(malformedRoot, "chirality.project.json");
    await writeFile(malformedPath, "not-json\n", "utf8");
    await expect(fixture.bootstrapClient.initializeHostedBootstrapProject({ projectRoot: malformedRoot })).rejects.toMatchObject({ code: "PROJECT_MANIFEST_INVALID" });
    expect(await readFile(malformedPath, "utf8")).toBe("not-json\n");

    const linkedRoot = join(fixture.root, "linked-root");
    await symlink(projectRoot, linkedRoot);
    await expect(fixture.bootstrapClient.initializeHostedBootstrapProject({ projectRoot: linkedRoot })).rejects.toMatchObject({ code: "INVALID_REQUEST" });
    await expect(fixture.bootstrapClient.initializeHostedBootstrapProject({ projectRoot: `${projectRoot}/.` })).rejects.toMatchObject({ code: "INVALID_REQUEST" });
    await expect(fixture.bootstrapClient.initializeHostedBootstrapProject({ projectRoot: "/" })).rejects.toMatchObject({ code: "INVALID_REQUEST" });
  });

  it("rejects extra fields and unsafe host projections, and cancels an in-flight ceremony on shutdown", async () => {
    let release!: () => void;
    const pending = new Promise<void>(resolve => { release = resolve; });
    const cancel = vi.fn(async () => { release(); return { schema: "chirality-hosted-bootstrap-status/v1", projectId: "strict-project", ceremony: "cancelled", admission: "unavailable", canStartLogin: true } as const; });
    const port = {
      status: vi.fn(async () => ({ schema: "chirality-hosted-bootstrap-status/v1", projectId: "wrong-project", ceremony: "ready-to-start", admission: "unavailable", canStartLogin: true } as const)),
      grantProviderNetworkConsent: vi.fn(),
      startLogin: vi.fn(async () => { await pending; return { loginId: "late", authUrl: "http://unsafe.example.test" }; }),
      cancelLogin: cancel,
      signOut: vi.fn()
    };
    const fixture = await setup(port);
    const projectRoot = join(fixture.root, "strict");
    await mkdir(projectRoot);
    const manifestPath = join(projectRoot, "chirality.project.json");
    await writeFile(manifestPath, `${JSON.stringify(manifest("strict-project"))}\n`, "utf8");
    await fixture.bootstrapClient.registerHostedBootstrapProject({ manifestPath });

    await expect(fixture.bootstrapClient.requestJson("/v3/hosted-bootstrap/projects/register", { method: "POST", body: { manifestPath, approvedBy: "renderer" } })).rejects.toMatchObject({ code: "INVALID_REQUEST" });
    await expect(fixture.bootstrapClient.requestJson("/v3/projects/strict-project/hosted-bootstrap/provider-network-consent", { method: "POST", body: { consent: false } })).rejects.toMatchObject({ code: "INVALID_REQUEST" });
    await expect(fixture.bootstrapClient.requestJson("/v3/projects/strict-project/hosted-bootstrap/login/cancel", { method: "POST", body: { approvalReference: "renderer" } })).rejects.toMatchObject({ code: "INVALID_REQUEST" });
    await expect(fixture.bootstrapClient.hostedBootstrapStatus("strict-project")).rejects.toMatchObject({ code: "INTERNAL_FAILURE" });

    const started = fixture.bootstrapClient.startHostedBootstrapLogin("strict-project").catch(error => error);
    await vi.waitFor(() => expect(port.startLogin).toHaveBeenCalledTimes(1));
    await fixture.daemon.stop();
    daemons.splice(daemons.indexOf(fixture.daemon), 1);
    await expect(started).resolves.toMatchObject({ code: "ENGINE_UNAVAILABLE" });
    expect(cancel).toHaveBeenCalled();
  });
});
