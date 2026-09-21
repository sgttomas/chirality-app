import { createHash } from "node:crypto";
import { lstat, readdir, readFile, realpath, stat } from "node:fs/promises";
import { isAbsolute, join, relative, resolve, sep } from "node:path";
import { parseDocument } from "yaml";
import type {
  ChiralityRoleName,
  MethodCatalogIssue,
  MethodDescriptor,
  MethodInspectionResponse,
  MethodKind,
  MethodCompatibilityMapping,
  MethodNavigation,
  MethodReference,
  MethodResourceDescriptor,
  MethodSource,
  MethodsResponse,
  QualifiedMethodReference,
  RoleDescriptor,
  RolesResponse,
  UnqualifiedMethodReference,
  WorkflowExecutionMetadata
} from "@chirality/runtime-contracts";
import { CHIRALITY_ROLE_NAMES, CHIRALITY_ROLES } from "@chirality/runtime-contracts";

const SOURCE_ORDER: Readonly<Record<MethodSource, number>> = {
  project: 0,
  user: 1,
  bundled: 2
};
const METHOD_NAME = /^(?=.{1,64}$)[a-z0-9]+(?:-[a-z0-9]+)*$/;
const SOURCE_ROOT_ID = /^[A-Za-z0-9][A-Za-z0-9._-]{0,127}$/;
const SHA256 = /^[a-f0-9]{64}$/;
const ROLE_SET = new Set<string>(CHIRALITY_ROLE_NAMES);

export interface MethodSourceRoot {
  /** Stable identifier registered by the host. Never derived from a renderer path. */
  sourceRootId: string;
  source: MethodSource;
  rootPath: string;
  version?: string;
  skillDirectory?: string;
  workflowDirectory?: string;
}

export interface CatalogMethodEntry {
  descriptor: MethodDescriptor;
  /** Host-only canonical paths. These never appear in response contracts. */
  packageRoot: string;
  entrypointPath: string;
  sourceRootPath: string;
  sourceRootVersion: string;
}

export interface MethodCatalog {
  response: MethodsResponse;
  entries: readonly CatalogMethodEntry[];
  blocked: readonly MethodCatalogIssue[];
  legacyTaskSkillAliases: ReadonlyMap<string, UnqualifiedMethodReference>;
}

export type MethodResolution =
  | { index: number; requested: MethodReference; status: "resolved"; method: CatalogMethodEntry }
  | { index: number; requested: MethodReference; status: "not-found" }
  | { index: number; requested: MethodReference; status: "forbidden"; method: QualifiedMethodReference }
  | { index: number; requested: MethodReference; status: "malformed"; issues: readonly MethodCatalogIssue[] }
  | { index: number; requested: MethodReference; status: "ambiguous"; candidates: readonly QualifiedMethodReference[] };

export class MethodCatalogError extends Error {
  readonly code: string;
  constructor(code: string, message: string) {
    super(message);
    this.name = "MethodCatalogError";
    this.code = code;
  }
}

function sha256(content: string | Buffer): string {
  return createHash("sha256").update(content).digest("hex");
}

function contained(root: string, candidate: string): boolean {
  const rel = relative(root, candidate);
  return rel === "" || (!rel.startsWith(`..${sep}`) && rel !== ".." && !isAbsolute(rel));
}

function qualifiedId(reference: QualifiedMethodReference): string {
  return `${reference.sourceRootId}:${reference.source}:${reference.kind}:${reference.name}`;
}

export function formatQualifiedMethodId(reference: QualifiedMethodReference): string {
  for (const value of [reference.sourceRootId, reference.name]) {
    if (value.includes(":")) throw new MethodCatalogError("INVALID_METHOD_REFERENCE", "Qualified method identity components cannot contain colons");
  }
  return qualifiedId(reference);
}

export function parseQualifiedMethodId(value: string): QualifiedMethodReference {
  const parts = value.split(":");
  if (parts.length !== 4) throw new MethodCatalogError("INVALID_METHOD_REFERENCE", "Invalid qualified method identity");
  const [sourceRootId, source, kind, name] = parts;
  if (!sourceRootId || !SOURCE_ROOT_ID.test(sourceRootId) || !name || !METHOD_NAME.test(name)
    || !["project", "user", "bundled"].includes(source ?? "")
    || !["skill", "workflow"].includes(kind ?? "")) {
    throw new MethodCatalogError("INVALID_METHOD_REFERENCE", "Invalid qualified method identity");
  }
  return { sourceRootId, source: source as MethodSource, kind: kind as MethodKind, name };
}

function parseFrontmatter(content: string): { name: string; description: string; metadata?: Readonly<Record<string, unknown>> } {
  const lines = content.replace(/\r\n/g, "\n").split("\n");
  if (lines[0] !== "---") throw new Error("entrypoint must begin with YAML frontmatter");
  const end = lines.indexOf("---", 1);
  if (end < 0) throw new Error("frontmatter closing delimiter is missing");
  const document = parseDocument(lines.slice(1, end).join("\n"), { uniqueKeys: true, strict: true });
  if (document.errors.length || document.warnings.length) {
    throw new Error([...document.errors, ...document.warnings].map(value => value.message).join("; "));
  }
  const fields: unknown = document.toJS({ mapAsMap: false });
  if (!fields || typeof fields !== "object" || Array.isArray(fields)) throw new Error("frontmatter must be a metadata mapping");
  const name = (fields as Record<string, unknown>).name;
  const description = (fields as Record<string, unknown>).description;
  if (typeof name !== "string" || name.trim() === "" || typeof description !== "string" || description.trim() === "") {
    throw new Error("frontmatter requires string name and description");
  }
  const metadata = (fields as Record<string, unknown>).metadata;
  if (metadata !== undefined && (!metadata || typeof metadata !== "object" || Array.isArray(metadata))) {
    throw new Error("frontmatter metadata must be a mapping when present");
  }
  return { name, description, ...(metadata === undefined ? {} : { metadata: metadata as Readonly<Record<string, unknown>> }) };
}

function stringArray(value: unknown, label: string): string[] {
  if (!Array.isArray(value) || value.some(item => typeof item !== "string" || item.trim() === "")) {
    throw new Error(`${label} must be an array of non-empty strings`);
  }
  return [...new Set(value as string[])];
}

function parseExecution(content: string): WorkflowExecutionMetadata {
  let value: unknown;
  try { value = JSON.parse(content); } catch { throw new Error("execution.json is not valid JSON"); }
  if (!value || typeof value !== "object" || Array.isArray(value)) throw new Error("execution.json must be an object");
  const object = value as Record<string, unknown>;
  if (object.schema_version !== 1) throw new Error("execution.json schema_version must be 1");
  const compatibleRoles = stringArray(object.compatible_roles, "compatible_roles");
  if (compatibleRoles.some(role => !ROLE_SET.has(role))) throw new Error("execution.json contains an unknown compatible role");
  let tools: WorkflowExecutionMetadata["tools"];
  if (object.tools !== undefined) {
    if (!object.tools || typeof object.tools !== "object" || Array.isArray(object.tools)) throw new Error("tools must be an object");
    const rawTools = object.tools as Record<string, unknown>;
    tools = {
      ...(rawTools.capabilities === undefined ? {} : { capabilities: stringArray(rawTools.capabilities, "tools.capabilities") }),
      ...(rawTools.commands === undefined ? {} : { commands: stringArray(rawTools.commands, "tools.commands") })
    };
  }
  return { schemaVersion: 1, compatibleRoles: compatibleRoles as ChiralityRoleName[], ...(tools ? { tools } : {}) };
}

interface IndexEntry {
  kind: MethodKind;
  name: string;
  description: string;
  central: boolean;
  compatibility: "canonical" | "legacy";
  executionRoleIds: ChiralityRoleName[];
  resources: string[];
  navigation?: MethodNavigation;
}

const NAVIGATION_CATEGORIES = new Set<string>(["core", "specialist", "superseded"]);
const NAVIGATION_TIERS = new Set<string>(["primary", "supporting"]);
const NAVIGATION_FIELDS = new Set<string>(["category", "tier", "order", "displayName", "group", "supersededBy"]);

function parseNavigation(value: unknown): MethodNavigation {
  if (!value || typeof value !== "object" || Array.isArray(value)) throw new Error("method index navigation must be an object");
  const raw = value as Record<string, unknown>;
  if (Object.keys(raw).some(key => !NAVIGATION_FIELDS.has(key))) throw new Error("method index navigation contains unknown fields");
  const { category, tier, order, displayName, group, supersededBy } = raw;
  if (typeof category !== "string" || !NAVIGATION_CATEGORIES.has(category)) throw new Error("method index navigation category is invalid");
  if (typeof tier !== "string" || !NAVIGATION_TIERS.has(tier)) throw new Error("method index navigation tier is invalid");
  if (typeof order !== "number" || !Number.isInteger(order) || order < 0) throw new Error("method index navigation order must be a non-negative integer");
  if (displayName !== undefined && (typeof displayName !== "string" || displayName.trim() === "")) throw new Error("method index navigation displayName must be a non-empty string");
  let parsedGroup: MethodNavigation["group"];
  if (group !== undefined) {
    if (!group || typeof group !== "object" || Array.isArray(group)) throw new Error("method index navigation group must be an object");
    const rawGroup = group as Record<string, unknown>;
    if (Object.keys(rawGroup).some(key => key !== "key" && key !== "label" && key !== "order") || typeof rawGroup.key !== "string" || !METHOD_NAME.test(rawGroup.key)
      || typeof rawGroup.label !== "string" || rawGroup.label.trim() === "") throw new Error("method index navigation group requires a kebab-case key and a non-empty label");
    if (typeof rawGroup.order !== "number" || !Number.isInteger(rawGroup.order) || rawGroup.order < 0) throw new Error("method index navigation group order must be a non-negative integer");
    if (category !== "specialist") throw new Error("method index navigation group is only valid for specialist workflows");
    parsedGroup = { key: rawGroup.key, label: rawGroup.label, order: rawGroup.order };
  } else if (category === "specialist") {
    throw new Error("method index navigation specialist workflows require a group");
  }
  if (supersededBy !== undefined) {
    if (typeof supersededBy !== "string" || !METHOD_NAME.test(supersededBy)) throw new Error("method index navigation supersededBy must be a workflow name");
    if (category !== "superseded") throw new Error("method index navigation supersededBy is only valid for superseded workflows");
  } else if (category === "superseded") {
    throw new Error("method index navigation superseded workflows require supersededBy");
  }
  return {
    category: category as MethodNavigation["category"],
    tier: tier as MethodNavigation["tier"],
    order,
    ...(displayName === undefined ? {} : { displayName }),
    ...(parsedGroup === undefined ? {} : { group: parsedGroup }),
    ...(supersededBy === undefined ? {} : { supersededBy })
  };
}

async function readMethodIndex(root: string, source: MethodSource, sourceRootId: string): Promise<Map<string, IndexEntry>> {
  const indexPath = join(root, "workflows", "index.json");
  let content: string;
  try { content = await readFile(indexPath, "utf8"); } catch (error) {
    if ((error as NodeJS.ErrnoException).code === "ENOENT") return new Map();
    throw error;
  }
  const raw: unknown = JSON.parse(content);
  if (!raw || typeof raw !== "object" || Array.isArray(raw)) throw new Error("workflows/index.json must be an object");
  const object = raw as Record<string, unknown>;
  const library = object.library as Record<string, unknown> | undefined;
  if (object.schema !== "chirality-method-index/v1" || library?.source !== source || library.sourceRootId !== sourceRootId || !Array.isArray(object.methods)) {
    throw new Error("workflows/index.json identity or schema is invalid");
  }
  const result = new Map<string, IndexEntry>();
  for (const item of object.methods) {
    if (!item || typeof item !== "object" || Array.isArray(item)) throw new Error("method index entry must be an object");
    const entry = item as Record<string, unknown>;
    if (!["skill", "workflow"].includes(entry.kind as string) || typeof entry.name !== "string" || !METHOD_NAME.test(entry.name)
      || typeof entry.description !== "string" || entry.description.trim() === "" || typeof entry.central !== "boolean"
      || !["current", "canonical", "legacy"].includes(entry.compatibility as string)) throw new Error("method index entry fields are invalid");
    const roles = stringArray(entry.executionRoleIds, "executionRoleIds");
    if (roles.some(role => !ROLE_SET.has(role))) throw new Error("method index entry contains an unknown role");
    const resources = stringArray(entry.resources, "resources");
    const parsed: IndexEntry = { kind: entry.kind as MethodKind, name: entry.name, description: entry.description,
      central: entry.central, compatibility: entry.compatibility === "legacy" ? "legacy" : "canonical", executionRoleIds: roles as ChiralityRoleName[], resources };
    if (entry.navigation !== undefined) {
      if (parsed.kind !== "workflow") throw new Error("method index navigation is only valid for workflows");
      const navigation = parseNavigation(entry.navigation);
      if ((navigation.category === "superseded") !== (parsed.compatibility === "legacy")) throw new Error("method index navigation category disagrees with compatibility");
      parsed.navigation = navigation;
    }
    const key = `${parsed.kind}\0${parsed.name}`;
    if (result.has(key)) throw new Error("method index contains a duplicate identity");
    result.set(key, parsed);
  }
  return result;
}

function issue(root: MethodSourceRoot, code: MethodCatalogIssue["code"], message: string, kind?: MethodKind, packageName?: string): MethodCatalogIssue {
  return { code, sourceRootId: root.sourceRootId, source: root.source, ...(kind ? { kind } : {}), ...(packageName ? { packageName } : {}), message };
}

async function scanKind(root: MethodSourceRoot, canonicalRoot: string, kind: MethodKind, directory: string,
  index: ReadonlyMap<string, IndexEntry>, entries: CatalogMethodEntry[], issues: MethodCatalogIssue[]): Promise<void> {
  const collectionPath = resolve(canonicalRoot, directory);
  if (!contained(canonicalRoot, collectionPath)) {
    issues.push(issue(root, "invalid-source-root", `${kind} directory escapes its source root`, kind));
    return;
  }
  let collectionRoot: string;
  try { collectionRoot = await realpath(collectionPath); } catch (error) {
    if ((error as NodeJS.ErrnoException).code === "ENOENT") return;
    issues.push(issue(root, "unreadable-source-root", `cannot read ${kind} directory`, kind));
    return;
  }
  if (!contained(canonicalRoot, collectionRoot)) {
    issues.push(issue(root, "invalid-source-root", `${kind} directory resolves outside its source root`, kind));
    return;
  }
  const children = (await readdir(collectionRoot, { withFileTypes: true })).sort((a, b) => a.name.localeCompare(b.name));
  for (const child of children) {
    if (!METHOD_NAME.test(child.name) || (!child.isDirectory() && !child.isSymbolicLink())
      || (root.source === "bundled" && kind === "skill" && child.name === "chirality-change")) continue;
    const packagePath = join(collectionRoot, child.name);
    let packageRoot: string;
    try {
      packageRoot = await realpath(packagePath);
      if (!(await stat(packageRoot)).isDirectory()) continue;
    } catch { continue; }
    if (!contained(collectionRoot, packageRoot)) {
      issues.push(issue(root, "entrypoint-escape", "package resolves outside its method library", kind, child.name));
      continue;
    }
    const entrypointPath = join(packageRoot, kind === "skill" ? "SKILL.md" : "WORKFLOW.md");
    let canonicalEntrypoint: string;
    let content: string;
    try {
      canonicalEntrypoint = await realpath(entrypointPath);
      if (!contained(packageRoot, canonicalEntrypoint) || !(await stat(canonicalEntrypoint)).isFile()) {
        issues.push(issue(root, "entrypoint-escape", "method entrypoint resolves outside its package", kind, child.name));
        continue;
      }
      content = await readFile(canonicalEntrypoint, "utf8");
    } catch (error) {
      if ((error as NodeJS.ErrnoException).code === "ENOENT") continue;
      issues.push(issue(root, "malformed-frontmatter", "method entrypoint is unreadable", kind, child.name));
      continue;
    }
    let metadata: { name: string; description: string; metadata?: Readonly<Record<string, unknown>> };
    try { metadata = parseFrontmatter(content); } catch (error) {
      issues.push(issue(root, "malformed-frontmatter", (error as Error).message, kind, child.name));
      continue;
    }
    if (metadata.name !== child.name) {
      issues.push(issue(root, "metadata-name-mismatch", `metadata name ${metadata.name} does not match package ${child.name}`, kind, child.name));
      continue;
    }
    let execution: WorkflowExecutionMetadata | undefined;
    try {
      const executionContent = await readFile(join(packageRoot, "execution.json"), "utf8");
      execution = parseExecution(executionContent);
    } catch (error) {
      if ((error as NodeJS.ErrnoException).code !== "ENOENT") {
        issues.push(issue(root, "malformed-execution-metadata", (error as Error).message, kind, child.name));
        continue;
      }
    }
    const central = index.get(`${kind}\0${child.name}`);
    if (central && central.description !== metadata.description) {
      issues.push(issue(root, "malformed-frontmatter", "entrypoint description disagrees with central method index", kind, child.name));
      continue;
    }
    const executionRoleIds = execution?.compatibleRoles ?? CHIRALITY_ROLE_NAMES;
    if (central && JSON.stringify(central.executionRoleIds) !== JSON.stringify(executionRoleIds)) {
      issues.push(issue(root, "malformed-execution-metadata", "package execution roles disagree with central method index", kind, child.name));
      continue;
    }
    const reference = { sourceRootId: root.sourceRootId, source: root.source, kind, name: child.name } as const;
    const descriptor: MethodDescriptor = {
      ...reference,
      qualifiedId: qualifiedId(reference),
      description: metadata.description,
      central: central?.central ?? false,
      compatibility: central?.compatibility ?? "canonical",
      executionRoleIds,
      resources: central?.resources ?? [],
      ...(metadata.metadata === undefined ? {} : { metadata: metadata.metadata }),
      ...(execution ? { execution } : {}),
      ...(central?.navigation === undefined ? {} : { navigation: central.navigation })
    };
    entries.push({ descriptor, packageRoot, entrypointPath: canonicalEntrypoint, sourceRootPath: canonicalRoot, sourceRootVersion: root.version ?? "unversioned" });
  }
}

export async function discoverMethodCatalog(sourceRoots: readonly MethodSourceRoot[]): Promise<MethodCatalog> {
  const entries: CatalogMethodEntry[] = [];
  const issues: MethodCatalogIssue[] = [];
  const seenIds = new Set<string>();
  for (const root of [...sourceRoots].sort((a, b) => SOURCE_ORDER[a.source] - SOURCE_ORDER[b.source] || a.sourceRootId.localeCompare(b.sourceRootId))) {
    if (!SOURCE_ROOT_ID.test(root.sourceRootId) || !isAbsolute(root.rootPath)) {
      issues.push(issue(root, "invalid-source-root", "source root requires a stable ID and an absolute host path"));
      continue;
    }
    if (seenIds.has(root.sourceRootId)) {
      issues.push(issue(root, "duplicate-source-root", "sourceRootId must be globally unique"));
      continue;
    }
    seenIds.add(root.sourceRootId);
    let canonicalRoot: string;
    try { canonicalRoot = await realpath(root.rootPath); } catch {
      issues.push(issue(root, "unreadable-source-root", "source root is unavailable"));
      continue;
    }
    let index = new Map<string, IndexEntry>();
    try { index = await readMethodIndex(canonicalRoot, root.source, root.sourceRootId); } catch (error) {
      issues.push(issue(root, "malformed-execution-metadata", (error as Error).message));
      continue;
    }
    if (root.source === "bundled") await scanKind(root, canonicalRoot, "skill", root.skillDirectory ?? ".agents/skills", index, entries, issues);
    await scanKind(root, canonicalRoot, "workflow", root.workflowDirectory ?? "workflows", index, entries, issues);
  }
  const unique: CatalogMethodEntry[] = [];
  const seenQualified = new Set<string>();
  for (const entry of entries) {
    if (seenQualified.has(entry.descriptor.qualifiedId)) {
      issues.push({ code: "duplicate-method", sourceRootId: entry.descriptor.sourceRootId, source: entry.descriptor.source,
        kind: entry.descriptor.kind, packageName: entry.descriptor.name, message: "duplicate qualified method identity" });
      continue;
    }
    seenQualified.add(entry.descriptor.qualifiedId);
    unique.push(entry);
  }
  unique.sort((a, b) => SOURCE_ORDER[a.descriptor.source] - SOURCE_ORDER[b.descriptor.source]
    || a.descriptor.sourceRootId.localeCompare(b.descriptor.sourceRootId)
    || a.descriptor.kind.localeCompare(b.descriptor.kind) || a.descriptor.name.localeCompare(b.descriptor.name));
  issues.sort((a, b) => SOURCE_ORDER[a.source] - SOURCE_ORDER[b.source] || a.sourceRootId.localeCompare(b.sourceRootId)
    || (a.kind ?? "").localeCompare(b.kind ?? "") || (a.packageName ?? "").localeCompare(b.packageName ?? "") || a.code.localeCompare(b.code));
  const legacyTaskSkillAliases = new Map<string, UnqualifiedMethodReference>();
  for (const root of sourceRoots.filter(value => value.source === "bundled")) {
    try {
      const canonicalRoot = await realpath(root.rootPath);
      const raw: unknown = JSON.parse(await readFile(join(canonicalRoot, "workflows", "legacy-methods.json"), "utf8"));
      if (!raw || typeof raw !== "object" || Array.isArray(raw)) throw new Error("legacy-methods.json must be an object");
      const object = raw as Record<string, unknown>;
      if (object.schema !== "chirality-legacy-methods/v1" || !object.convertedWorkflowAliases || typeof object.convertedWorkflowAliases !== "object" || Array.isArray(object.convertedWorkflowAliases)) {
        throw new Error("legacy-methods.json schema is invalid");
      }
      for (const [alias, target] of Object.entries(object.convertedWorkflowAliases as Record<string, unknown>).sort(([a], [b]) => a.localeCompare(b))) {
        if (!METHOD_NAME.test(alias) || !target || typeof target !== "object" || Array.isArray(target)) throw new Error("legacy method alias is invalid");
        const reference = target as Record<string, unknown>;
        if (!["skill", "workflow"].includes(reference.kind as string) || typeof reference.name !== "string" || !METHOD_NAME.test(reference.name)) throw new Error("legacy method alias is invalid");
        legacyTaskSkillAliases.set(alias, { kind: reference.kind as MethodKind, name: reference.name });
      }
    } catch (error) {
      if ((error as NodeJS.ErrnoException).code !== "ENOENT") issues.push(issue(root, "malformed-execution-metadata", (error as Error).message));
    }
  }
  return { response: { schemaVersion: "chirality.methods/v3", methods: unique.map(entry => entry.descriptor), malformedPackages: issues }, entries: unique, blocked: issues, legacyTaskSkillAliases };
}

export interface MethodSelectionCompatibilityInput {
  methods?: readonly MethodReference[];
  workflow?: string;
  taskSkill?: string;
}

export function normalizeMethodSelection(catalog: MethodCatalog, input: MethodSelectionCompatibilityInput): {
  methods: readonly MethodReference[];
  compatibilityInputs: readonly ("Workflow" | "TaskSkill")[];
  compatibilityMappings: readonly MethodCompatibilityMapping[];
} {
  const methods = [...(input.methods ?? [])];
  for (const method of methods) {
    if ("sourceRootId" in method && resolvedQualifiedReferenceId(catalog, method) === undefined) {
      throw new MethodCatalogError("UNSUPPORTED_METHOD_ORIGIN", `Qualified method origin is outside the declared Root catalog: ${method.sourceRootId}`);
    }
  }
  const compatibilityInputs: ("Workflow" | "TaskSkill")[] = [];
  const compatibilityMappings: MethodCompatibilityMapping[] = [];
  let workflowMethod: MethodReference | undefined;
  let taskSkillMethod: UnqualifiedMethodReference | undefined;
  if (input.workflow !== undefined) {
    const converted = catalog.legacyTaskSkillAliases.get(input.workflow);
    if (converted) {
      workflowMethod = converted;
      compatibilityMappings.push(mappingDecision(catalog, "Workflow", input.workflow, converted, "converted-alias"));
    } else if (input.workflow.includes(":")) {
      const qualified = parseQualifiedMethodId(input.workflow);
      if (qualified.kind !== "workflow") throw new MethodCatalogError("INVALID_METHOD_REFERENCE", "Workflow qualified identity must select a workflow");
      workflowMethod = qualified;
      compatibilityMappings.push(mappingDecision(catalog, "Workflow", input.workflow, qualified, "explicit-qualified-historical-workflow"));
    } else {
      if (!METHOD_NAME.test(input.workflow)) throw new MethodCatalogError("INVALID_METHOD_REFERENCE", "Workflow must be a canonical method name or qualified workflow identity");
      workflowMethod = { kind: "workflow", name: input.workflow };
      compatibilityMappings.push(mappingDecision(catalog, "Workflow", input.workflow, workflowMethod, "unmapped-canonical-workflow"));
    }
    compatibilityInputs.push("Workflow");
  }
  if (input.taskSkill !== undefined) {
    const normalizedAlias = input.taskSkill.replaceAll("_", "-");
    taskSkillMethod = catalog.legacyTaskSkillAliases.get(normalizedAlias);
    if (!taskSkillMethod) throw new MethodCatalogError("UNKNOWN_LEGACY_METHOD", `TaskSkill names an unknown legacy method alias: ${input.taskSkill}`);
    compatibilityInputs.push("TaskSkill");
    compatibilityMappings.push({ ...mappingDecision(catalog, "TaskSkill", input.taskSkill, taskSkillMethod, "converted-alias"), normalizedAlias });
  }
  if (workflowMethod && taskSkillMethod && qualifiedReferenceId(catalog, workflowMethod) !== qualifiedReferenceId(catalog, taskSkillMethod)) {
    throw new MethodCatalogError("CONFLICTING_METHOD_SELECTION", "conflicting Workflow/TaskSkill inputs select different methods");
  }
  const selected = workflowMethod ?? taskSkillMethod;
  if (selected) {
    const selectedId = qualifiedReferenceId(catalog, selected);
    const alreadyOrdered = methods.some(value => resolvedQualifiedReferenceId(catalog, value) === selectedId);
    if (!alreadyOrdered) methods.push(selected);
  }
  return { methods, compatibilityInputs, compatibilityMappings };
}

function mappingDecision(
  catalog: MethodCatalog,
  field: MethodCompatibilityMapping["field"],
  original: string,
  reference: MethodReference,
  mapping: MethodCompatibilityMapping["mapping"]
): MethodCompatibilityMapping {
  return { field, original, mapping, resolved: qualifiedReference(catalog, reference) };
}

function qualifiedReference(catalog: MethodCatalog, reference: MethodReference): QualifiedMethodReference {
  const resolution = resolveMethodReferences(catalog, [reference])[0];
  if (resolution?.status === "resolved") {
    const { sourceRootId, source, kind, name } = resolution.method.descriptor;
    return { sourceRootId, source, kind, name };
  }
  if (resolution?.status === "ambiguous") throw new MethodCatalogError("AMBIGUOUS_METHOD_REFERENCE", "Compatibility method reference is ambiguous");
  if (resolution?.status === "malformed") throw new MethodCatalogError("MALFORMED_METHOD_REFERENCE", "Compatibility method reference is blocked by malformed metadata");
  if (resolution?.status === "forbidden") throw new MethodCatalogError("UNSUPPORTED_METHOD_ORIGIN", `Skills may be loaded only from a trusted bundled source: ${qualifiedId(resolution.method)}`);
  if ("sourceRootId" in reference) throw new MethodCatalogError("UNSUPPORTED_METHOD_ORIGIN", `Qualified method origin is outside the declared Root catalog: ${reference.sourceRootId}`);
  throw new MethodCatalogError("UNKNOWN_METHOD", `Compatibility method is unavailable: ${reference.kind}:${reference.name}`);
}

function qualifiedReferenceId(catalog: MethodCatalog, reference: MethodReference): string {
  return qualifiedId(qualifiedReference(catalog, reference));
}

function resolvedQualifiedReferenceId(catalog: MethodCatalog, reference: MethodReference): string | undefined {
  const resolution = resolveMethodReferences(catalog, [reference])[0];
  return resolution?.status === "resolved" ? resolution.method.descriptor.qualifiedId : undefined;
}

function referenceMatch(entry: CatalogMethodEntry, reference: MethodReference): boolean {
  return entry.descriptor.kind === reference.kind && entry.descriptor.name === reference.name
    && (!("sourceRootId" in reference) || (entry.descriptor.sourceRootId === reference.sourceRootId && entry.descriptor.source === reference.source));
}

function issueMatch(value: MethodCatalogIssue, reference: MethodReference): boolean {
  return value.kind === reference.kind && value.packageName === reference.name
    && (!("sourceRootId" in reference) || (value.sourceRootId === reference.sourceRootId && value.source === reference.source));
}

export function resolveMethodReferences(catalog: MethodCatalog, requested: readonly MethodReference[]): readonly MethodResolution[] {
  return requested.map((reference, index): MethodResolution => {
    if ("sourceRootId" in reference) {
      if (reference.kind === "skill" && reference.source !== "bundled") {
        return { index, requested: reference, status: "forbidden", method: reference };
      }
      const malformed = catalog.blocked.filter(value => issueMatch(value, reference));
      if (malformed.length) return { index, requested: reference, status: "malformed", issues: malformed };
      const found = catalog.entries.find(entry => referenceMatch(entry, reference));
      return found ? { index, requested: reference, status: "resolved", method: found } : { index, requested: reference, status: "not-found" };
    }
    for (const source of ["project", "user", "bundled"] as const) {
      const malformed = catalog.blocked.filter(value => value.source === source && issueMatch(value, reference));
      const candidates = catalog.entries.filter(entry => entry.descriptor.source === source && referenceMatch(entry, reference));
      if (malformed.length) return { index, requested: reference, status: "malformed", issues: malformed };
      if (candidates.length === 1) return { index, requested: reference, status: "resolved", method: candidates[0]! };
      if (candidates.length > 1) return { index, requested: reference, status: "ambiguous", candidates: candidates.map(entry => entry.descriptor) };
    }
    return { index, requested: reference, status: "not-found" };
  });
}

async function resolveContainedResource(entry: CatalogMethodEntry, resourcePath: string): Promise<string> {
  if (!resourcePath || isAbsolute(resourcePath) || resourcePath.includes("\0")) throw new MethodCatalogError("RESOURCE_ESCAPE", "Resource path must be package-relative");
  let target: string;
  try { target = await realpath(resolve(entry.packageRoot, resourcePath)); } catch {
    throw new MethodCatalogError("RESOURCE_UNAVAILABLE", `Method resource is unavailable: ${resourcePath}`);
  }
  if (!contained(entry.packageRoot, target) || !(await stat(target)).isFile()) {
    throw new MethodCatalogError("RESOURCE_ESCAPE", `Method resource escapes its package: ${resourcePath}`);
  }
  return target;
}

async function listResources(entry: CatalogMethodEntry): Promise<string[]> {
  if (entry.descriptor.resources.length) return [...entry.descriptor.resources];
  const resourceRoot = join(entry.packageRoot, "resources");
  let canonical: string;
  try { canonical = await realpath(resourceRoot); } catch { return []; }
  if (!contained(entry.packageRoot, canonical)) throw new MethodCatalogError("RESOURCE_ESCAPE", "Method resources directory escapes its package");
  const result: string[] = [];
  const visitedDirectories = new Set<string>();
  const visit = async (directory: string): Promise<void> => {
    if (visitedDirectories.has(directory)) throw new MethodCatalogError("RESOURCE_ESCAPE", "Method resource directory cycle is not allowed");
    visitedDirectories.add(directory);
    for (const child of (await readdir(directory, { withFileTypes: true })).sort((a, b) => a.name.localeCompare(b.name))) {
      const path = join(directory, child.name);
      const canonicalChild = await realpath(path);
      if (!contained(entry.packageRoot, canonicalChild)) throw new MethodCatalogError("RESOURCE_ESCAPE", "Method resource escapes its package");
      const metadata = await lstat(path);
      const target = await stat(canonicalChild);
      if (target.isDirectory()) await visit(canonicalChild);
      else if (target.isFile()) result.push(relative(entry.packageRoot, path).split(sep).join("/"));
      else if (metadata.isSymbolicLink()) throw new MethodCatalogError("RESOURCE_ESCAPE", "Unsupported method resource symlink target");
    }
  };
  await visit(canonical);
  return result.sort();
}

export async function inspectMethod(entry: CatalogMethodEntry): Promise<MethodInspectionResponse> {
  const content = await readFile(entry.entrypointPath, "utf8");
  const resources: MethodResourceDescriptor[] = [];
  for (const path of await listResources(entry)) {
    const target = await resolveContainedResource(entry, path);
    resources.push({ path, sha256: sha256(await readFile(target)) });
  }
  return { schemaVersion: "chirality.method-inspection/v3", method: entry.descriptor,
    entrypoint: { content, sha256: sha256(content) }, resources };
}

export async function readMethodResource(entry: CatalogMethodEntry, resourcePath: string): Promise<{ content: string; sha256: string }> {
  const content = await readFile(await resolveContainedResource(entry, resourcePath), "utf8");
  return { content, sha256: sha256(content) };
}

interface RegistryRole {
  instruction: unknown;
  type: unknown;
  direct_entry: unknown;
  delegates_to: unknown;
  allow_generalist_agent2: unknown;
  tools: unknown;
  write_scope: unknown;
}

function expectedRole(id: ChiralityRoleName): RoleDescriptor {
  return CHIRALITY_ROLES.find(role => role.id === id)!;
}

async function rolesFromRegistryBytes(root: string, content: string): Promise<RolesResponse> {
  let raw: unknown;
  try { raw = JSON.parse(content); }
  catch { throw new MethodCatalogError("INVALID_ROLE_REGISTRY", "Role registry must be valid JSON"); }
  if (!raw || typeof raw !== "object" || Array.isArray(raw)) throw new MethodCatalogError("INVALID_ROLE_REGISTRY", "Role registry must be an object");
  const registry = raw as Record<string, unknown>;
  if (registry.schema_version !== 1 || !registry.roles || typeof registry.roles !== "object" || Array.isArray(registry.roles)) {
    throw new MethodCatalogError("INVALID_ROLE_REGISTRY", "Role registry schema_version and roles are required");
  }
  const roleMap = registry.roles as Record<string, unknown>;
  const ids = Object.keys(roleMap).sort();
  if (ids.join("\0") !== [...CHIRALITY_ROLE_NAMES].sort().join("\0")) throw new MethodCatalogError("INVALID_ROLE_REGISTRY", "Role registry must contain exactly the four v3 role IDs");
  const roles: RoleDescriptor[] = [];
  for (const id of CHIRALITY_ROLE_NAMES) {
    const rawRole = roleMap[id];
    if (!rawRole || typeof rawRole !== "object" || Array.isArray(rawRole)) throw new MethodCatalogError("INVALID_ROLE_REGISTRY", `Invalid role record: ${id}`);
    const role = rawRole as unknown as RegistryRole;
    const expected = expectedRole(id);
    const delegates = stringArray(role.delegates_to, `${id}.delegates_to`);
    const tools = stringArray(role.tools, `${id}.tools`);
    if (typeof role.instruction !== "string" || !Number.isInteger(role.type) || typeof role.direct_entry !== "boolean"
      || typeof role.allow_generalist_agent2 !== "boolean" || typeof role.write_scope !== "string" || role.write_scope.trim() === "" || tools.length === 0
      || role.type !== expected.agentType || role.direct_entry !== expected.directEntry
      || (id === "TASK" ? delegates.length !== 0 || role.allow_generalist_agent2 !== false : false)
      || (id !== "TASK" ? role.allow_generalist_agent2 !== true : false)) {
      throw new MethodCatalogError("INVALID_ROLE_REGISTRY", `Role fields conflict with the v3 contract: ${id}`);
    }
    const target = await realpath(resolve(root, role.instruction));
    if (!contained(root, target) || !(await stat(target)).isFile()) throw new MethodCatalogError("INVALID_ROLE_REGISTRY", `Role instruction escapes or is unavailable: ${id}`);
    roles.push({ ...expected, instruction: role.instruction, delegatesTo: delegates as ChiralityRoleName[], tools });
  }
  return { schemaVersion: "chirality.roles/v3", defaultRole: "HELP_HUMAN", roles };
}

/** Validates already-held registry bytes without reopening a replaceable path. */
export async function loadRolesFromCapturedRegistry(instructionRoot: string, content: string): Promise<RolesResponse> {
  if (!isAbsolute(instructionRoot)) throw new MethodCatalogError("INVALID_ROLE_REGISTRY", "Instruction root must be an absolute host path");
  const root = await realpath(instructionRoot);
  return await rolesFromRegistryBytes(root, content);
}

export async function loadRoles(instructionRoot: string): Promise<RolesResponse> {
  if (!isAbsolute(instructionRoot)) throw new MethodCatalogError("INVALID_ROLE_REGISTRY", "Instruction root must be an absolute host path");
  const root = await realpath(instructionRoot);
  const registryPath = await realpath(join(root, "agents", "registry.json"));
  if (!contained(root, registryPath)) throw new MethodCatalogError("INVALID_ROLE_REGISTRY", "Role registry escapes the instruction root");
  return await rolesFromRegistryBytes(root, await readFile(registryPath, "utf8"));
}
