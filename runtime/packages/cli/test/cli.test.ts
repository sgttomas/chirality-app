import { mkdtemp, readFile, rm, stat, writeFile } from "node:fs/promises";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { afterEach, describe, expect, it, vi } from "vitest";
import type { RuntimeStream } from "@chirality/runtime-client";
import type { RuntimeSseFrame } from "@chirality/runtime-contracts";
import {
  LaunchAgentManager,
  RUNTIME_LAUNCH_AGENT_LABEL,
  renderRuntimeLaunchAgent
} from "../src/launch-agent.js";
import {
  runCli,
  type CliDependencies,
  type CliIo,
  type RuntimeCliClient,
  type RuntimeLaunchAgent
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

function fakeLaunchAgent(
  overrides: Partial<RuntimeLaunchAgent> = {}
): RuntimeLaunchAgent {
  return {
    async install() {},
    async start() {},
    async stop() {},
    async status() {
      return { installed: false, loaded: false };
    },
    async uninstall() {},
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

function dependencies(
  client: RuntimeCliClient,
  launchAgent: RuntimeLaunchAgent = fakeLaunchAgent()
): CliDependencies {
  return {
    client,
    launchAgent,
    paths: {
      userData: "/tmp/chirality-test",
      runtimeDirectory: "/tmp/chirality-test/runtime",
      socketPath: "/tmp/chirality-test/runtime/control.sock",
      tokenFile: "/tmp/chirality-test/runtime/operator.token",
      launchAgentsDirectory: "/tmp/chirality-test/LaunchAgents"
    },
    executablePath: "/Applications/Chirality.app/Contents/MacOS/Chirality",
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

  it("renders and installs a private opt-in LaunchAgent without a model argument", async () => {
    const root = await mkdtemp(join(tmpdir(), "chirality-launch-agent-"));
    temporaryDirectories.push(root);
    const launchAgentsDirectory = join(root, "LaunchAgents");
    const runtimeDirectory = join(root, "user-data", "runtime");
    const calls: Array<{ executable: string; args: readonly string[] }> = [];
    const manager = new LaunchAgentManager(
      { launchAgentsDirectory, runtimeDirectory },
      async (executable, args) => {
        calls.push({ executable, args });
        return { exitCode: 0, stdout: "ok", stderr: "" };
      },
      501
    );
    const executablePath = "/Applications/Chirality.app/Contents/MacOS/Chirality";

    await manager.install(executablePath);
    const source = await readFile(manager.plistPath, "utf8");
    const metadata = await stat(manager.plistPath);
    const runtimeMetadata = await stat(runtimeDirectory);
    const logsMetadata = await stat(join(runtimeDirectory, "logs"));
    expect(metadata.mode & 0o777).toBe(0o600);
    expect(runtimeMetadata.mode & 0o777).toBe(0o700);
    expect(logsMetadata.mode & 0o777).toBe(0o700);
    expect(source).toContain(`<string>${RUNTIME_LAUNCH_AGENT_LABEL}</string>`);
    expect(source).toContain("<string>--runtime-daemon</string>");
    expect(source).toContain("<key>RunAtLoad</key>");
    expect(source).toContain("<key>KeepAlive</key>");
    expect(source).toContain("<key>SuccessfulExit</key>");
    expect(source).toContain("<false/>");
    expect(source).toContain("<key>ThrottleInterval</key>");
    expect(source).not.toMatch(/model|activate|omlx/iu);

    await manager.start();
    expect(calls).toEqual([
      {
        executable: "launchctl",
        args: ["bootstrap", "gui/501", manager.plistPath]
      },
      {
        executable: "launchctl",
        args: ["kickstart", "-k", "gui/501/com.chirality.runtime"]
      }
    ]);
  });

  it("escapes executable and log paths in the LaunchAgent plist", () => {
    const source = renderRuntimeLaunchAgent({
      executablePath: "/Applications/A&B<Dev>.app/Chirality",
      runtimeDirectory: "/tmp/A&B"
    });
    expect(source).toContain("A&amp;B&lt;Dev&gt;");
    expect(source).toContain("/tmp/A&amp;B/logs");
  });
});
