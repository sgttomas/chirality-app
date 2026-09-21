import { mkdtemp, readFile, rm, writeFile } from "node:fs/promises";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { afterEach, describe, expect, it, vi } from "vitest";
import type { RuntimeStream } from "@chirality/runtime-client";
import { RuntimeError } from "@chirality/runtime-contracts";
import type { RuntimeSseFrame } from "@chirality/runtime-contracts";
import { resolveCliRuntimePaths } from "../src/config.js";
import {
  runCli,
  type CliDependencies,
  type CliIo,
  type RuntimeCliClient
} from "../src/cli.js";

const temporaryDirectories: string[] = [];

function stream(events: readonly RuntimeSseFrame[]): RuntimeStream {
  return {
    async *[Symbol.asyncIterator]() {
      yield* events;
    },
    cancel() {}
  };
}

function fakeClient(
  overrides: Partial<RuntimeCliClient> = {}
): RuntimeCliClient {
  const unexpected = async (): Promise<never> => {
    throw new Error("Unexpected fake client method");
  };
  return {
    daemonStatus: unexpected,
    registerProject: unexpected,
    listProjects: unexpected,
    projectStatus: unexpected,
    listModels: unexpected,
    activateModel: unexpected,
    createSession: unexpected,
    listSessions: unexpected,
    replaySession: unexpected,
    turnSession: unexpected,
    interruptSession: unexpected,
    runAgent1: unexpected,
    ...overrides
  };
}

function io(stdin = ""): {
  io: CliIo;
  stdout: string[];
  stderr: string[];
} {
  const stdout: string[] = [];
  const stderr: string[] = [];
  return {
    stdout,
    stderr,
    io: {
      stdout(text) {
        stdout.push(text);
      },
      stderr(text) {
        stderr.push(text);
      },
      async readStdin() {
        return stdin;
      }
    }
  };
}

function dependencies(client: RuntimeCliClient): CliDependencies {
  return {
    client,
    paths: {
      userData: "/tmp/chirality-test",
      runtimeDirectory: "/tmp/chirality-test/runtime",
      socketPath: "/tmp/chirality-test/runtime/control.sock",
      tokenFile: "/tmp/chirality-test/runtime/operator.token"
    },
    readTextFile: (path) => readFile(path, "utf8")
  };
}

afterEach(async () => {
  await Promise.all(
    temporaryDirectories.splice(0).map((directory) =>
      rm(directory, { recursive: true, force: true })
    )
  );
  vi.restoreAllMocks();
});

describe("chirality CLI", () => {
  it("runs an Agent 1 request from a brief file and emits UIEvent NDJSON", async () => {
    const root = await mkdtemp(join(tmpdir(), "chirality-cli-run-"));
    temporaryDirectories.push(root);
    const briefFile = join(root, "brief.md");
    await writeFile(briefFile, "Inspect the bounded fixture.\n");
    const runAgent1 = vi.fn(async () =>
      stream([
        { type: "chat:delta", data: { text: "evidence" } },
        { type: "session:complete", data: {} },
        { type: "process:exit", data: { exitCode: 0 } }
      ])
    );
    const output = io();

    const exitCode = await runCli(
      [
        "run",
        "--project",
        "app-dev",
        "--agent",
        "WORKING_ITEMS",
        "--brief-file",
        briefFile,
        "--local-model",
        "mlx-community/model",
        "--json"
      ],
      output.io,
      dependencies(fakeClient({ runAgent1 }))
    );

    expect(exitCode).toBe(0);
    expect(runAgent1).toHaveBeenCalledWith("app-dev", {
      brief: "Inspect the bounded fixture.",
      agentId: "WORKING_ITEMS",
      approvalReference: "cli-agent1:WORKING_ITEMS",
      localModel: "mlx-community/model",
      readOnlyTool: {
        name: "read_file",
        relativePath: "chirality.project.json"
      }
    });
    expect(output.stdout.map((line) => JSON.parse(line))).toEqual([
      { type: "chat:delta", data: { text: "evidence" } },
      { type: "session:complete", data: {} },
      { type: "process:exit", data: { exitCode: 0 } }
    ]);
  });

  it("accepts a session-turn request through stdin and keeps human output non-JSON", async () => {
    const turnSession = vi.fn(async () =>
      stream([
        { type: "chat:delta", data: { text: "local text" } },
        { type: "process:exit", data: { exitCode: 0 } }
      ])
    );
    const output = io("prompt from stdin\n");

    const exitCode = await runCli(
      [
        "session",
        "turn",
        "--project",
        "app-dev",
        "--session",
        "sess-1"
      ],
      output.io,
      dependencies(fakeClient({ turnSession }))
    );

    expect(exitCode).toBe(0);
    expect(turnSession).toHaveBeenCalledWith("app-dev", "sess-1", {
      prompt: "prompt from stdin"
    });
    expect(output.stdout.join("")).toBe("local text[process:exit]\n");
  });

  it("propagates a failed session turn process exit", async () => {
    const turnSession = vi.fn(async () =>
      stream([
        {
          type: "turn:error",
          data: {
            phase: "mid-stream",
            errorType: "SDK_FAILURE",
            message: "manager failed",
            status: 502,
            severity: "error",
            fatal: true
          }
        },
        { type: "process:exit", data: { exitCode: 7, error: "manager failed" } }
      ])
    );
    const output = io("prompt\n");

    const exitCode = await runCli(
      [
        "session",
        "turn",
        "--project",
        "app-dev",
        "--session",
        "sess-failed"
      ],
      output.io,
      dependencies(fakeClient({ turnSession }))
    );

    expect(exitCode).toBe(7);
    expect(output.stderr.join("")).toContain("SDK_FAILURE: manager failed");
    expect(output.stderr.join("")).toContain("process exited 7");
  });

  it("rejects an Agent 1 stream that ends without process:exit", async () => {
    const runAgent1 = vi.fn(async () =>
      stream([
        { type: "chat:delta", data: { text: "partial" } },
        { type: "session:complete", data: {} }
      ])
    );
    const output = io("bounded brief\n");

    const exitCode = await runCli(
      ["run", "--project", "app-dev", "--agent", "WORKING_ITEMS"],
      output.io,
      dependencies(fakeClient({ runAgent1 }))
    );

    expect(exitCode).toBe(1);
    expect(output.stderr.join("")).toContain(
      "INTERNAL_FAILURE: Runtime stream ended without terminal process:exit"
    );
  });

  it("registers and lists projects through the v1 client with the JSON output convention", async () => {
    const registered = { project: { projectId: "app-dev" }, warnings: [] };
    const registerProject = vi.fn(async () => registered);
    const listProjects = vi.fn(async () => [{ project: { projectId: "app-dev" }, manifestDrift: false, adaptersEnabled: true }]);
    const client = fakeClient({ registerProject, listProjects });

    const register = io();
    expect(await runCli(["project", "register", "/projects/app-dev/chirality.project.json", "--json"], register.io, dependencies(client))).toBe(0);
    expect(registerProject).toHaveBeenCalledWith({
      manifestPath: "/projects/app-dev/chirality.project.json",
      approvedBy: "local-operator",
      approvalReference: "cli-explicit-registration"
    });
    expect(register.stdout).toEqual([`${JSON.stringify(registered)}\n`]);

    const list = io();
    expect(await runCli(["project", "list"], list.io, dependencies(client))).toBe(0);
    expect(listProjects).toHaveBeenCalledOnce();
    expect(JSON.parse(list.stdout.join(""))).toEqual([{ project: { projectId: "app-dev" }, manifestDrift: false, adaptersEnabled: true }]);
  });

  it("reports the daemon status without any job-management surface", async () => {
    const status = { daemonId: "daemon-1", startedAt: "2026-09-12T00:00:00.000Z" };
    const daemonStatus = vi.fn(async () => status);
    const output = io();

    expect(await runCli(["daemon", "status", "--json"], output.io, dependencies(fakeClient({ daemonStatus })))).toBe(0);
    expect(daemonStatus).toHaveBeenCalledOnce();
    expect(output.stdout).toEqual([`${JSON.stringify(status)}\n`]);

    for (const action of ["install", "start", "stop", "uninstall"]) {
      const retired = io();
      expect(await runCli(["daemon", action], retired.io, dependencies(fakeClient()))).toBe(2);
      expect(retired.stderr.join("")).toContain("daemon requires status");
    }
  });

  it("has no credential command surface", async () => {
    const output = io();
    const client = fakeClient({ listProjects: vi.fn() });

    const exitCode = await runCli(
      ["credential", "set"],
      output.io,
      dependencies(client)
    );

    expect(exitCode).toBe(2);
    expect(output.stderr.join("")).toContain("Unknown command");
    expect(client.listProjects).not.toHaveBeenCalled();
  });

  it("no longer offers the retired v2 login, delegated, approval and release commands", async () => {
    for (const argv of [
      ["hosted-login", "start", "--project", "project"],
      ["delegated", "turn", "--project", "project", "--turn-id", "turn-one", "--prompt", "hello"],
      ["approvals", "list", "--project", "project"],
      ["release", "measure-support", "--recipe", "/private/recipe.json"]
    ]) {
      const output = io();
      const client = fakeClient({ daemonStatus: vi.fn(), listProjects: vi.fn() });
      expect(await runCli(argv, output.io, dependencies(client))).toBe(2);
      expect(output.stderr.join("")).toContain("Unknown command");
      expect(client.daemonStatus).not.toHaveBeenCalled();
      expect(client.listProjects).not.toHaveBeenCalled();
    }
  });

  it("does not reject ordinary request paths or model IDs containing credential-like words", async () => {
    const root = await mkdtemp(join(tmpdir(), "chirality-cli-token-named-file-"));
    temporaryDirectories.push(root);
    const briefFile = join(root, "api-key-token-analysis.md");
    await writeFile(briefFile, "Analyze naming without handling credentials.\n");
    const runAgent1 = vi.fn(async () =>
      stream([{ type: "process:exit", data: { exitCode: 0 } }])
    );
    const output = io();

    const exitCode = await runCli(
      [
        "run",
        "--project",
        "app-dev",
        "--agent",
        "WORKING_ITEMS",
        "--brief-file",
        briefFile,
        "--local-model",
        "mlx-community/token-counter"
      ],
      output.io,
      dependencies(fakeClient({ runAgent1 }))
    );

    expect(exitCode).toBe(0);
    expect(runAgent1).toHaveBeenCalledOnce();
  });

  it("shows the retained command surface without contacting the runtime", async () => {
    const output = io();
    const daemonStatus = vi.fn();
    expect(await runCli(["--help"], output.io, dependencies(fakeClient({ daemonStatus })))).toBe(0);
    const usage = output.stdout.join("");
    for (const line of ["daemon status", "project register", "project list", "session create", "session turn", "session interrupt", "run --project"]) {
      expect(usage).toContain(line);
    }
    expect(usage).not.toMatch(/hosted-login|delegated|approvals|measure-support|LaunchAgent|daemon install/u);
    expect(daemonStatus).not.toHaveBeenCalled();
  });

  it("preserves every compatibility mismatch machine field on CLI stderr", async () => {
    const details = { operation_id: "turn:one", project_id: "project", daemon_identity: "safe-daemon", client_compatibility_identity: "root-runtime-2", daemon_compatibility_identity: "root-runtime-1", client_contract_basis_sha256: "a".repeat(64), daemon_contract_basis_sha256: "b".repeat(64), retryable: false, consequential_work_started: false, diagnostic: "unequal" };
    const output = io();
    const result = await runCli(["daemon", "status"], output.io, dependencies(fakeClient({ async daemonStatus() { throw new RuntimeError("RUNTIME_COMPATIBILITY_MISMATCH", "mismatch", 409, details); } })));
    expect(result).toBe(1);
    expect(JSON.parse(output.stderr.join(""))).toEqual({ error: { code: "RUNTIME_COMPATIBILITY_MISMATCH", message: "mismatch", details } });
  });
});

describe("resolveCliRuntimePaths", () => {
  it("resolves the socket and token file under the App user data by default", () => {
    const paths = resolveCliRuntimePaths({}, "/Users/example");
    expect(paths).toEqual({
      userData: "/Users/example/Library/Application Support/Chirality",
      runtimeDirectory: "/Users/example/Library/Application Support/Chirality/runtime",
      socketPath: "/Users/example/Library/Application Support/Chirality/runtime/control.sock",
      tokenFile: "/Users/example/Library/Application Support/Chirality/runtime/auth/tokens/operator.token"
    });
  });

  it("honours the explicit environment overrides and carries no job directory", () => {
    const paths = resolveCliRuntimePaths(
      {
        CHIRALITY_USER_DATA: "/tmp/user-data",
        CHIRALITY_RUNTIME_SOCKET_PATH: "/tmp/runtime/service.sock",
        CHIRALITY_RUNTIME_TOKEN_FILE: "/tmp/runtime/client-token"
      },
      "/Users/example"
    );
    expect(paths).toEqual({
      userData: "/tmp/user-data",
      runtimeDirectory: "/tmp/user-data/runtime",
      socketPath: "/tmp/runtime/service.sock",
      tokenFile: "/tmp/runtime/client-token"
    });
    expect(paths).not.toHaveProperty("launchAgentsDirectory");
  });
});
