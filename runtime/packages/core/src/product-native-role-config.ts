import { createHash } from "node:crypto";
import { constants } from "node:fs";
import { lstat, mkdir, open, realpath, writeFile } from "node:fs/promises";
import { dirname, isAbsolute, join, resolve } from "node:path";
import { CHIRALITY_ROLE_NAMES, RuntimeError, type ResolveSelectedContextResponse } from "@chirality/runtime-contracts";

/** Materialize only captured bytes. Old paths remain valid for in-flight descendants. */
export async function materializeProductNativeRoles(context: ResolveSelectedContextResponse | undefined, directory: string): Promise<Record<string, string>> {
  const supplied = context?.supplied ?? [];
  const common = supplied.filter(entry => entry.kind === "root" || entry.id === "product:library").map(entry => entry.content).join("\n\n");
  if (!supplied.some(entry => entry.kind === "root") || !supplied.some(entry => entry.id === "product:library")) throw new RuntimeError("ENGINE_UNAVAILABLE", "Product instruction basis is incomplete", 503);
  const config: Record<string, string> = {};
  if (!isAbsolute(directory) || resolve(directory) !== directory || await realpath(dirname(directory)) !== dirname(directory)) throw new RuntimeError("ENGINE_UNAVAILABLE", "Native role directory must be a direct canonical path", 503);
  try { await mkdir(directory, { mode: 0o700 }); }
  catch (error) { if ((error as NodeJS.ErrnoException).code !== "EEXIST") throw error; }
  const directoryInfo = await lstat(directory);
  if (!directoryInfo.isDirectory() || directoryInfo.isSymbolicLink() || await realpath(directory) !== directory) throw new RuntimeError("ENGINE_UNAVAILABLE", "Native role directory must be a direct canonical directory", 503);
  for (const role of CHIRALITY_ROLE_NAMES) {
    const entry = supplied.find(candidate => candidate.id === `native-role:${role}`);
    if (!entry || createHash("sha256").update(entry.content).digest("hex") !== entry.sha256) throw new RuntimeError("ENGINE_UNAVAILABLE", `Captured native role is unavailable: ${role}`, 503);
    const body = `developer_instructions = ${JSON.stringify(`${common}\n\n# Active role: ${role}\n\n${entry.content}`)}\n`;
    const digest = createHash("sha256").update(body).digest("hex");
    const path = join(directory, `${role}-${digest}.toml`);
    try { await writeFile(path, body, { flag: "wx", mode: 0o600 }); }
    catch (error) {
      if ((error as NodeJS.ErrnoException).code !== "EEXIST") throw error;
      const file = await open(path, constants.O_RDONLY | constants.O_NOFOLLOW);
      try {
        const info = await file.stat();
        if (!info.isFile() || info.size !== Buffer.byteLength(body) || await realpath(path) !== path || await file.readFile("utf8") !== body) throw new RuntimeError("ENGINE_UNAVAILABLE", "Captured native role file was modified or aliased", 503);
      } finally { await file.close(); }
    }
    config[`agents.${role}.description`] = `Chirality ${role}; use a fresh context and bounded brief.`;
    config[`agents.${role}.config_file`] = path;
  }
  return config;
}
