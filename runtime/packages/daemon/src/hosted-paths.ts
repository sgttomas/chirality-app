import { isAbsolute, join, resolve } from "node:path";
import { RuntimeError } from "@chirality/runtime-contracts";

export const HOSTED_BOOTSTRAP_CLIENT_ID = "hosted-bootstrap-host";

function runtimeRoot(value: string): void {
  if (typeof value !== "string" || !isAbsolute(value) || resolve(value) !== value || /[\x00-\x1f]/.test(value)) throw new RuntimeError("INVALID_REQUEST", "Runtime directory must be a normalized absolute path");
}

export function hostedProjectClientId(projectId: string): string {
  if (typeof projectId !== "string" || !/^[A-Za-z0-9][A-Za-z0-9._-]{0,127}$/.test(projectId)) throw new RuntimeError("INVALID_REQUEST", "Invalid project ID");
  return `hosted-project-${projectId}`;
}

export function resolveHostedProjectTokenFile(runtimeDirectory: string, projectId: string): string {
  runtimeRoot(runtimeDirectory);
  return join(runtimeDirectory, "auth", "tokens", `${hostedProjectClientId(projectId)}.token`);
}
