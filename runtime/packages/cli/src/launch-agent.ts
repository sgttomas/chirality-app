import { spawn } from "node:child_process";
import { chmod, mkdir, open, rename, unlink } from "node:fs/promises";
import { basename, dirname, join, resolve } from "node:path";

export const RUNTIME_LAUNCH_AGENT_LABEL = "com.chirality.runtime";

export interface CommandResult {
  exitCode: number;
  stdout: string;
  stderr: string;
}

export type CommandRunner = (
  executable: string,
  args: readonly string[]
) => Promise<CommandResult>;

export interface LaunchAgentPaths {
  launchAgentsDirectory: string;
  runtimeDirectory: string;
}

export interface LaunchAgentStatus {
  installed: boolean;
  loaded: boolean;
  detail?: string;
}

function xml(value: string): string {
  return value
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&apos;");
}

export function renderRuntimeLaunchAgent(input: {
  executablePath: string;
  runtimeDirectory: string;
}): string {
  const logs = join(input.runtimeDirectory, "logs");
  return `<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>Label</key>
  <string>${RUNTIME_LAUNCH_AGENT_LABEL}</string>
  <key>ProgramArguments</key>
  <array>
    <string>${xml(resolve(input.executablePath))}</string>
    <string>--runtime-daemon</string>
  </array>
  <key>RunAtLoad</key>
  <true/>
  <key>KeepAlive</key>
  <dict>
    <key>SuccessfulExit</key>
    <false/>
  </dict>
  <key>ThrottleInterval</key>
  <integer>10</integer>
  <key>StandardOutPath</key>
  <string>${xml(join(logs, "daemon.stdout.log"))}</string>
  <key>StandardErrorPath</key>
  <string>${xml(join(logs, "daemon.stderr.log"))}</string>
</dict>
</plist>
`;
}

async function defaultCommandRunner(
  executable: string,
  args: readonly string[]
): Promise<CommandResult> {
  return new Promise((resolveResult, reject) => {
    const child = spawn(executable, [...args], {
      stdio: ["ignore", "pipe", "pipe"]
    });
    let stdout = "";
    let stderr = "";
    child.stdout.setEncoding("utf8");
    child.stderr.setEncoding("utf8");
    child.stdout.on("data", (chunk: string) => {
      stdout += chunk;
    });
    child.stderr.on("data", (chunk: string) => {
      stderr += chunk;
    });
    child.once("error", reject);
    child.once("exit", (code) => {
      resolveResult({ exitCode: code ?? 1, stdout, stderr });
    });
  });
}

async function atomicWrite(filePath: string, content: string): Promise<void> {
  await mkdir(dirname(filePath), { recursive: true });
  const temporary = join(
    dirname(filePath),
    `.${basename(filePath)}.${process.pid}.${Date.now()}.tmp`
  );
  let committed = false;
  try {
    const handle = await open(temporary, "wx", 0o600);
    try {
      await handle.writeFile(content, "utf8");
      await handle.sync();
    } finally {
      await handle.close();
    }
    await rename(temporary, filePath);
    await chmod(filePath, 0o600);
    committed = true;
  } finally {
    if (!committed) {
      await unlink(temporary).catch((error: NodeJS.ErrnoException) => {
        if (error.code !== "ENOENT") throw error;
      });
    }
  }
}

async function ensurePrivateDirectory(path: string): Promise<void> {
  await mkdir(path, { recursive: true, mode: 0o700 });
  await chmod(path, 0o700);
}

export class LaunchAgentManager {
  readonly plistPath: string;
  private readonly domain: string;
  private readonly service: string;

  constructor(
    private readonly paths: LaunchAgentPaths,
    private readonly runCommand: CommandRunner = defaultCommandRunner,
    userId = process.getuid?.() ?? 0
  ) {
    this.plistPath = join(
      resolve(paths.launchAgentsDirectory),
      `${RUNTIME_LAUNCH_AGENT_LABEL}.plist`
    );
    this.domain = `gui/${userId}`;
    this.service = `${this.domain}/${RUNTIME_LAUNCH_AGENT_LABEL}`;
  }

  async install(executablePath: string): Promise<void> {
    await ensurePrivateDirectory(this.paths.runtimeDirectory);
    await ensurePrivateDirectory(join(this.paths.runtimeDirectory, "logs"));
    await atomicWrite(
      this.plistPath,
      renderRuntimeLaunchAgent({
        executablePath,
        runtimeDirectory: this.paths.runtimeDirectory
      })
    );
  }

  async start(): Promise<void> {
    const bootstrap = await this.runCommand("launchctl", [
      "bootstrap",
      this.domain,
      this.plistPath
    ]);
    if (
      bootstrap.exitCode !== 0 &&
      !/already loaded|service already loaded|bootstrap failed: 5/iu.test(
        `${bootstrap.stdout}\n${bootstrap.stderr}`
      )
    ) {
      throw new Error(bootstrap.stderr.trim() || "Unable to bootstrap runtime LaunchAgent");
    }
    const start = await this.runCommand("launchctl", ["kickstart", "-k", this.service]);
    if (start.exitCode !== 0) {
      throw new Error(start.stderr.trim() || "Unable to start runtime LaunchAgent");
    }
  }

  async stop(): Promise<void> {
    const result = await this.runCommand("launchctl", ["bootout", this.service]);
    if (
      result.exitCode !== 0 &&
      !/could not find service|no such process|not found/iu.test(
        `${result.stdout}\n${result.stderr}`
      )
    ) {
      throw new Error(result.stderr.trim() || "Unable to stop runtime LaunchAgent");
    }
  }

  async status(): Promise<LaunchAgentStatus> {
    const installed = await import("node:fs/promises").then(({ stat }) =>
      stat(this.plistPath).then(
        () => true,
        () => false
      )
    );
    const result = await this.runCommand("launchctl", ["print", this.service]);
    return {
      installed,
      loaded: result.exitCode === 0,
      ...(result.exitCode === 0
        ? { detail: result.stdout.trim() }
        : result.stderr.trim()
          ? { detail: result.stderr.trim() }
          : {})
    };
  }

  async uninstall(): Promise<void> {
    await this.stop();
    await unlink(this.plistPath).catch((error: NodeJS.ErrnoException) => {
      if (error.code !== "ENOENT") throw error;
    });
  }
}
