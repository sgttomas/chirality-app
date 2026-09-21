import { createHash } from "node:crypto";
import { constants } from "node:fs";
import { open, realpath, stat } from "node:fs/promises";
import { isAbsolute, join, relative, resolve, sep } from "node:path";
import {
  CHIRALITY_ROLE_NAMES,
  RuntimeError,
  type ChiralityRoleName,
  type RoleDescriptor
} from "@chirality/runtime-contracts";
import { loadRolesFromCapturedRegistry } from "./method-catalog.js";

const SHA256 = /^[a-f0-9]{64}$/u;

function sha256(value: string): string {
  return createHash("sha256").update(value).digest("hex");
}

function contained(root: string, candidate: string): boolean {
  const path = relative(root, candidate);
  return path === "" || (path !== ".." && !path.startsWith(`..${sep}`) && !isAbsolute(path));
}

function sameIdentity(a: { dev: bigint; ino: bigint; size: bigint; mtimeNs: bigint; ctimeNs: bigint }, b: { dev: bigint; ino: bigint; size: bigint; mtimeNs: bigint; ctimeNs: bigint }): boolean {
  return a.dev === b.dev && a.ino === b.ino && a.size === b.size && a.mtimeNs === b.mtimeNs && a.ctimeNs === b.ctimeNs;
}

async function stableRead(path: string): Promise<{ content: string; sha256: string }> {
  const pathBefore = await import("node:fs/promises").then(fs => fs.lstat(path, { bigint: true }));
  if (!pathBefore.isFile() || pathBefore.isSymbolicLink() || await realpath(path) !== path) throw new RuntimeError("ENGINE_UNAVAILABLE", "Trusted role source path is not a direct canonical file", 503);
  const handle = await open(path, constants.O_RDONLY | constants.O_NOFOLLOW);
  try {
    const before = await handle.stat({ bigint: true });
    if (!before.isFile() || before.size > BigInt(1024 * 1024) || !sameIdentity(pathBefore, before)) throw new RuntimeError("ENGINE_UNAVAILABLE", "Trusted role source is unavailable or exceeds its bound", 503);
    const content = await handle.readFile("utf8");
    const after = await handle.stat({ bigint: true });
    const pathAfter = await import("node:fs/promises").then(fs => fs.lstat(path, { bigint: true }));
    if (!sameIdentity(before, after) || !sameIdentity(after, pathAfter) || pathAfter.isSymbolicLink() || await realpath(path) !== path || BigInt(Buffer.byteLength(content)) !== after.size) {
      throw new RuntimeError("ENGINE_UNAVAILABLE", "Trusted role source changed while it was read", 503);
    }
    return { content, sha256: sha256(content) };
  } finally {
    await handle.close();
  }
}

export interface TrustedNativeRoleSource {
  roleId: ChiralityRoleName;
  description: string;
  instructionRelativePath: string;
  /** Host-only canonical source path. It is never supplied to a model. */
  instructionOrigin: string;
  instructionSha256: string;
  instruction: string;
}

export interface TrustedNativeRoleEntry extends TrustedNativeRoleSource {
  configFileName: string;
  configToml: string;
  configSha256: string;
}

export interface TrustedNativeRoleConfiguration {
  schemaVersion: "chirality.codex-native-roles/v1";
  pins: Readonly<{ agentsEnabled: true; multiAgentV1: true; multiAgentV2: false; maxDepth: 2 }>;
  registry: Readonly<{ origin: string; sha256: string }>;
  /** Optional inspection projection. It never changes the four-role native config digest. */
  activeRole?: TrustedNativeRoleSource;
  nativeRoles: readonly TrustedNativeRoleEntry[];
  digest: string;
}

function roleConfigToml(instruction: string): string {
  // JSON strings are valid TOML basic strings for this bounded UTF-8 source.
  return `developer_instructions = ${JSON.stringify(instruction)}\n`;
}

function configurationDigest(
  pins: TrustedNativeRoleConfiguration["pins"],
  registrySha256: string,
  nativeRoles: readonly TrustedNativeRoleEntry[]
): string {
  return sha256(JSON.stringify({
    schemaVersion: "chirality.codex-native-roles/v1",
    pins,
    registrySha256,
    roles: nativeRoles.map(({ roleId, description, instructionRelativePath, instructionSha256, configFileName, configSha256 }) => ({ roleId, description, instructionRelativePath, instructionSha256, configFileName, configSha256 }))
  }));
}

async function readRole(root: string, descriptor: RoleDescriptor): Promise<TrustedNativeRoleEntry> {
  const unresolved = resolve(root, descriptor.instruction);
  if (!contained(root, unresolved)) throw new RuntimeError("ENGINE_UNAVAILABLE", `Trusted role source escapes the instruction root: ${descriptor.id}`, 503);
  const canonical = await realpath(unresolved);
  if (canonical !== unresolved || !contained(root, canonical) || !(await stat(canonical)).isFile()) {
    throw new RuntimeError("ENGINE_UNAVAILABLE", `Trusted role source must be a direct contained regular file: ${descriptor.id}`, 503);
  }
  const source = await stableRead(canonical);
  const configToml = roleConfigToml(source.content);
  return Object.freeze({
    roleId: descriptor.id,
    description: descriptor.description,
    instructionRelativePath: descriptor.instruction.split(sep).join("/"),
    instructionOrigin: canonical,
    instructionSha256: source.sha256,
    instruction: source.content,
    configFileName: `${descriptor.id}.toml`,
    configToml,
    configSha256: sha256(configToml)
  });
}

/**
 * Loads the exact bundled role registry and isolates one parent role from the
 * four role-specific native child configurations. This prepares bytes only;
 * it does not qualify or execute native delegation.
 */
export async function loadTrustedNativeRoleConfiguration(
  instructionRoot: string,
  activeRoleId?: ChiralityRoleName
): Promise<TrustedNativeRoleConfiguration> {
  if (!isAbsolute(instructionRoot) || (activeRoleId !== undefined && !CHIRALITY_ROLE_NAMES.includes(activeRoleId))) {
    throw new RuntimeError("INVALID_REQUEST", "Trusted native role configuration requires an absolute instruction root and known active role", 400);
  }
  const root = await realpath(instructionRoot);
  if (root !== resolve(instructionRoot)) throw new RuntimeError("ENGINE_UNAVAILABLE", "Instruction root must identify its canonical directory", 503);
  const registryPath = join(root, "agents", "registry.json");
  const capturedRegistry = await stableRead(registryPath);
  const registry = await loadRolesFromCapturedRegistry(root, capturedRegistry.content);
  const nativeRoles = Object.freeze(await Promise.all(registry.roles.map(role => readRole(root, role))));
  const active = activeRoleId === undefined ? undefined : nativeRoles.find(role => role.roleId === activeRoleId);
  if (activeRoleId !== undefined && !active) throw new RuntimeError("ENGINE_UNAVAILABLE", `Trusted active role is unavailable: ${activeRoleId}`, 503);
  const activeRole = active === undefined ? undefined : Object.freeze({
    roleId: active.roleId,
    description: active.description,
    instructionRelativePath: active.instructionRelativePath,
    instructionOrigin: active.instructionOrigin,
    instructionSha256: active.instructionSha256,
    instruction: active.instruction
  });
  // Two descendant edges support HELP_HUMAN -> manager -> TASK. This is the
  // supplier's native V1 depth setting, not a Runtime scheduler or allowlist.
  const pins = Object.freeze({ agentsEnabled: true as const, multiAgentV1: true as const, multiAgentV2: false as const, maxDepth: 2 as const });
  const digest = configurationDigest(pins, capturedRegistry.sha256, nativeRoles);
  return Object.freeze({
    schemaVersion: "chirality.codex-native-roles/v1",
    pins,
    registry: Object.freeze({ origin: registryPath, sha256: capturedRegistry.sha256 }),
    ...(activeRole === undefined ? {} : { activeRole }),
    nativeRoles,
    digest
  });
}

/** Builds trusted Codex config overrides after the host materializes every role file. */
export function codexNativeRoleConfigOverrides(
  configuration: TrustedNativeRoleConfiguration,
  configFiles: Readonly<Record<ChiralityRoleName, string>>
): readonly string[] {
  if (configuration.schemaVersion !== "chirality.codex-native-roles/v1" || !SHA256.test(configuration.digest)
    || !SHA256.test(configuration.registry.sha256)
    || JSON.stringify(configuration.pins) !== JSON.stringify({ agentsEnabled: true, multiAgentV1: true, multiAgentV2: false, maxDepth: 2 })
    || configuration.nativeRoles.length !== CHIRALITY_ROLE_NAMES.length
    || configuration.nativeRoles.some((role, index) => role.roleId !== CHIRALITY_ROLE_NAMES[index]
      || role.configFileName !== `${role.roleId}.toml`
      || role.instructionSha256 !== sha256(role.instruction)
      || role.configToml !== roleConfigToml(role.instruction)
      || role.configSha256 !== sha256(role.configToml))
    || (configuration.activeRole !== undefined && configuration.activeRole.instructionSha256 !== sha256(configuration.activeRole.instruction))
    || configurationDigest(configuration.pins, configuration.registry.sha256, configuration.nativeRoles) !== configuration.digest) {
    throw new RuntimeError("INVALID_REQUEST", "Invalid trusted native role configuration", 400);
  }
  if (configuration.activeRole !== undefined) {
    const selected = configuration.nativeRoles.find(role => role.roleId === configuration.activeRole!.roleId);
    if (!selected || selected.description !== configuration.activeRole.description || selected.instructionRelativePath !== configuration.activeRole.instructionRelativePath
      || selected.instructionOrigin !== configuration.activeRole.instructionOrigin || selected.instructionSha256 !== configuration.activeRole.instructionSha256
      || selected.instruction !== configuration.activeRole.instruction) throw new RuntimeError("INVALID_REQUEST", "Active native role does not match its trusted role entry", 400);
  }
  const keys = Object.keys(configFiles).sort();
  if (keys.join("\0") !== [...CHIRALITY_ROLE_NAMES].sort().join("\0")) throw new RuntimeError("INVALID_REQUEST", "Native role config paths must identify exactly four roles", 400);
  const paths = CHIRALITY_ROLE_NAMES.map(roleId => configFiles[roleId]);
  if (paths.some(path => !isAbsolute(path) || resolve(path) !== path) || new Set(paths).size !== paths.length) throw new RuntimeError("INVALID_REQUEST", "Native role config paths must be distinct normalized absolute paths", 400);
  const roleById = new Map(configuration.nativeRoles.map(role => [role.roleId, role]));
  if (roleById.size !== CHIRALITY_ROLE_NAMES.length) throw new RuntimeError("INVALID_REQUEST", "Native role configuration is incomplete", 400);
  return Object.freeze([
    "agents.enabled=true",
    "features.multi_agent=true",
    "features.multi_agent_v2=false",
    "agents.max_depth=2",
    ...CHIRALITY_ROLE_NAMES.flatMap(roleId => {
      const role = roleById.get(roleId);
      if (!role) throw new RuntimeError("INVALID_REQUEST", `Native role configuration is missing ${roleId}`, 400);
      return [
        `agents.${roleId}.description=${JSON.stringify(role.description)}`,
        `agents.${roleId}.config_file=${JSON.stringify(configFiles[roleId])}`
      ];
    })
  ]);
}
