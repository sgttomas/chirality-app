import { spawn, spawnSync, type ChildProcess } from "node:child_process";
import { mkdtemp, stat } from "node:fs/promises";
import { tmpdir } from "node:os";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";
import { describe, expect, it } from "vitest";
import { installRuntimeDaemonSignalShutdown } from "../packages/daemon/src/signal-shutdown.js";

interface ChildExit {
  code: number | null;
  signal: NodeJS.Signals | null;
}

interface ChildEvents {
  events: Record<string, unknown>[];
  output: string;
}

function waitForArmed(
  child: ChildProcess,
  timeoutMs: number,
  diagnostic: () => string,
  observed: ChildEvents
): Promise<Record<string, unknown>> {
  return new Promise((resolve, reject) => {
    let pendingOutput = "";
    const timer = setTimeout(
      () =>
        reject(
          new Error(`child did not arm: stdout=${observed.output} stderr=${diagnostic()}`)
        ),
      timeoutMs
    );
    child.stdout?.setEncoding("utf8");
    child.stdout?.on("data", (chunk: string) => {
      observed.output += chunk;
      pendingOutput += chunk;
      let newline = pendingOutput.indexOf("\n");
      while (newline !== -1) {
        const line = pendingOutput.slice(0, newline);
        pendingOutput = pendingOutput.slice(newline + 1);
        newline = pendingOutput.indexOf("\n");
        if (line.trim() === "") continue;
        let event: Record<string, unknown>;
        try {
          event = JSON.parse(line) as Record<string, unknown>;
        } catch {
          continue;
        }
        observed.events.push(event);
        if (event["event"] === "ARMED") {
          clearTimeout(timer);
          resolve(event);
          return;
        }
      }
    });
    child.once("exit", (code, signal) => {
      clearTimeout(timer);
      reject(
        new Error(
          `child exited before arming: code=${code} signal=${signal} stderr=${diagnostic()}`
        )
      );
    });
  });
}

function waitForExit(child: ChildProcess, timeoutMs: number): Promise<ChildExit> {
  return new Promise((resolve, reject) => {
    const timer = setTimeout(() => {
      child.kill("SIGKILL");
      reject(new Error(`child did not exit within ${timeoutMs} ms after SIGTERM`));
    }, timeoutMs);
    child.once("exit", (code, signal) => {
      clearTimeout(timer);
      resolve({ code, signal });
    });
  });
}

async function expectAbsent(path: string): Promise<void> {
  await expect(stat(path)).rejects.toMatchObject({ code: "ENOENT" });
}

describe("runtime daemon process signal shutdown", () => {
  it("normalizes a synchronous stop failure, reports once, and disposes its listener", async () => {
    const originalListeners = process.listeners("SIGTERM");
    const originalExitCode = process.exitCode;
    const failure = new Error("synchronous stop failure");
    let stops = 0;
    const reported: unknown[] = [];
    const shutdown = installRuntimeDaemonSignalShutdown(
      {
        stop(): Promise<void> {
          stops += 1;
          throw failure;
        }
      },
      {
        signals: ["SIGTERM"],
        failureExitCode: 7,
        reportFailure(error) {
          reported.push(error);
        }
      }
    );
    const installed = process
      .listeners("SIGTERM")
      .filter((listener) => !originalListeners.includes(listener));
    expect(installed).toHaveLength(1);

    try {
      installed[0]?.();
      installed[0]?.();
      await expect(shutdown.completion).rejects.toBe(failure);
      expect(stops).toBe(1);
      expect(reported).toEqual([failure]);
      expect(process.exitCode).toBe(7);
      expect(process.listeners("SIGTERM")).toEqual(originalListeners);
    } finally {
      shutdown.dispose();
      process.exitCode = originalExitCode;
    }
  });

  it("tears down within a bound when SIGTERM arrives with an incomplete request held open", async () => {
    const runtimeDirectory = await mkdtemp(join(tmpdir(), "chirality-signal-stop-"));
    const runtimeRoot = dirname(dirname(fileURLToPath(import.meta.url)));
    const nodeModules =
      process.env["CHIRALITY_RUNTIME_NODE_MODULES"] ?? join(runtimeRoot, "node_modules");
    const fixture = join(runtimeRoot, "tests", "fixtures", "runtime-daemon-signal-child.ts");
    const bundle = join(runtimeDirectory, "runtime-daemon-signal-child.mjs");
    const esbuild = join(nodeModules, "esbuild", "bin", "esbuild");
    const bundled = spawnSync(
      esbuild,
      [
        fixture,
        "--bundle",
        "--platform=node",
        "--format=esm",
        "--target=node22",
        `--alias:@chirality/runtime-contracts=${join(
          runtimeRoot,
          "packages",
          "contracts",
          "src",
          "index.ts"
        )}`,
        `--alias:@chirality/runtime-core=${join(
          runtimeRoot,
          "packages",
          "core",
          "src",
          "index.ts"
        )}`,
        `--alias:yaml=${join(nodeModules, "yaml", "browser", "index.js")}`,
        `--outfile=${bundle}`
      ],
      { cwd: runtimeRoot, encoding: "utf8" }
    );
    expect(
      { status: bundled.status, signal: bundled.signal },
      `${bundled.stdout}\n${bundled.stderr}`
    ).toEqual({ status: 0, signal: null });

    const child = spawn(process.execPath, [bundle], {
      cwd: runtimeRoot,
      env: {
        ...process.env,
        CHIRALITY_SIGNAL_FIXTURE_RUNTIME: runtimeDirectory,
        NO_COLOR: "1"
      },
      stdio: ["ignore", "pipe", "pipe"]
    });
    let stderr = "";
    const observed: ChildEvents = { events: [], output: "" };
    child.stderr?.setEncoding("utf8");
    child.stderr?.on("data", (chunk: string) => {
      stderr += chunk;
    });

    try {
      const armed = await waitForArmed(child, 5_000, () => stderr, observed);
      expect(armed).toMatchObject({
        event: "ARMED",
        declaredLength: 100,
        suppliedLength: 1,
        requestParsed: true,
        requestComplete: false,
        requestReadableEnded: false,
        installedSigtermListeners: 1
      });
      const socketPath = String(armed["socketPath"]);
      const ownerFile = String(armed["ownerFile"]);
      await expect(stat(socketPath)).resolves.toBeDefined();
      await expect(stat(ownerFile)).resolves.toBeDefined();

      const began = performance.now();
      expect(child.kill("SIGTERM")).toBe(true);
      const exited = await waitForExit(child, 4_000);
      const elapsed = performance.now() - began;

      expect(exited, stderr).toEqual({ code: 0, signal: null });
      expect(elapsed).toBeGreaterThanOrEqual(1_900);
      expect(elapsed).toBeLessThan(4_000);
      expect(observed.events).toContainEqual({
        event: "STOPPED",
        sigtermListenersRestored: true
      });
      await expectAbsent(socketPath);
      await expectAbsent(ownerFile);
    } finally {
      if (child.exitCode === null && child.signalCode === null) child.kill("SIGKILL");
    }
  }, 10_000);
});
