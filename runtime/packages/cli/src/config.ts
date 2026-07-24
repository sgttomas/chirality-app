import { homedir } from "node:os";
import { join, resolve } from "node:path";
import type { RuntimeClientOptions } from "@chirality/runtime-client";

export interface CliRuntimePaths {
  userData: string;
  runtimeDirectory: string;
  socketPath: string;
  tokenFile: string;
  launchAgentsDirectory: string;
}

export function resolveCliRuntimePaths(
  environment: NodeJS.ProcessEnv = process.env,
  homeDirectory = homedir()
): CliRuntimePaths {
  const userData = resolve(
    environment["CHIRALITY_USER_DATA"] ??
      join(homeDirectory, "Library", "Application Support", "Chirality")
  );
  const runtimeDirectory = join(userData, "runtime");
  return {
    userData,
    runtimeDirectory,
    socketPath: resolve(
      environment["CHIRALITY_RUNTIME_SOCKET_PATH"] ??
        join(runtimeDirectory, "control.sock")
    ),
    tokenFile: resolve(
      environment["CHIRALITY_RUNTIME_TOKEN_FILE"] ??
        join(runtimeDirectory, "auth", "tokens", "operator.token")
    ),
    launchAgentsDirectory: resolve(
      environment["CHIRALITY_LAUNCH_AGENTS_DIRECTORY"] ??
        join(homeDirectory, "Library", "LaunchAgents")
    )
  };
}

export function runtimeClientOptions(paths: CliRuntimePaths): RuntimeClientOptions {
  return {
    socketPath: paths.socketPath,
    tokenFile: paths.tokenFile
  };
}
