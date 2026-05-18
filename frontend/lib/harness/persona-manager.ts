import { createHash } from "node:crypto";
import type { Dirent } from "node:fs";
import { mkdir, readFile, readdir, rename, rm, stat, writeFile } from "node:fs/promises";
import path from "node:path";

import { DEFAULT_SYSTEM_PROMPT, PROMPT_TOKEN_BUDGET } from "./defaults";
import { getInstructionRoot } from "./instruction-root";
import type { PersonaConfig, SessionMode, SubagentDefinition } from "./types";

const CHAR_PER_TOKEN_ESTIMATE = 4;
const PROMPT_CHAR_BUDGET = PROMPT_TOKEN_BUDGET * CHAR_PER_TOKEN_ESTIMATE;
const PERSONA_FILE_PREFIX = "AGENT_";
const PERSONA_FILE_SUFFIX = ".md";

/**
 * Subagent prompt compaction threshold. If a subagent instruction body exceeds
 * this character count (~3K tokens), non-operational sections are stripped.
 * Set to 0 to disable compaction entirely.
 */
const SUBAGENT_COMPACT_THRESHOLD = 12_000;

/** Regex patterns for sections stripped during prompt compaction. */
const COMPACT_STRIP_PATTERNS: RegExp[] = [
  /\[\[DOC:AGENT_INSTRUCTIONS\]\][\s\S]*?(?=\n#|\n\[\[|$)/gi,
  /\[\[BEGIN:RATIONALE\]\][\s\S]*?\[\[END:RATIONALE\]\]/gi,
];

const VALID_SUBAGENT_MODELS = new Set(["sonnet", "opus", "haiku", "inherit"]);

type CachedText = {
  mtimeMs: number;
  content: string;
};

type FrontmatterRecord = Record<string, unknown>;
type RegistryIssueSeverity = "error" | "warn";
type RegistryIssue = {
  agentId: string;
  code: string;
  severity: RegistryIssueSeverity;
  message: string;
};
type RegistryValidationResult = {
  valid: string[];
  errors: string[];
  issues: RegistryIssue[];
};

function modeInstruction(mode: SessionMode): string {
  if (mode === "workbench") {
    return "Interactive workbench mode. Engage conversationally. Explain your reasoning. Ask for clarification when needed.";
  }
  if (mode === "pipeline") {
    return "Pipeline execution mode. Execute efficiently and report results concisely.";
  }
  return "Direct terminal mode. Execute commands as requested with minimal commentary.";
}

function normalizePersonaId(personaId: string): string {
  const baseName = path.basename(personaId.trim());
  const withoutExt = baseName.replace(/\.md$/i, "");
  const withoutPrefix = withoutExt.replace(/^AGENT_/i, "");
  return withoutPrefix.toUpperCase();
}

function stringifyScalar(value: unknown): string | null {
  if (typeof value === "string") {
    return value.trim();
  }

  if (typeof value === "number" || typeof value === "boolean") {
    return String(value);
  }

  return null;
}

function toStringList(value: unknown): string[] | undefined {
  const normalized = (Array.isArray(value) ? value : [value])
    .flatMap((item) => {
      if (typeof item === "string") {
        return item.includes(",")
          ? item
              .split(",")
              .map((piece) => piece.trim())
              .filter(Boolean)
          : [item.trim()];
      }

      const scalar = stringifyScalar(item);
      return scalar ? [scalar] : [];
    })
    .map((item) => item.trim())
    .filter(Boolean);

  return normalized.length > 0 ? normalized : undefined;
}

function toToolsValue(value: unknown): string | undefined {
  const list = toStringList(value);
  if (!list) {
    return undefined;
  }
  return list.join(",");
}

function toPositiveInteger(value: unknown): number | undefined {
  if (typeof value === "number" && Number.isFinite(value) && value > 0) {
    return Math.floor(value);
  }

  if (typeof value === "string") {
    const parsed = Number.parseInt(value.trim(), 10);
    if (Number.isFinite(parsed) && parsed > 0) {
      return parsed;
    }
  }

  return undefined;
}

function parseScalarValue(value: string): unknown {
  const trimmed = value.trim();
  if (!trimmed) {
    return "";
  }

  if (
    (trimmed.startsWith('"') && trimmed.endsWith('"')) ||
    (trimmed.startsWith("'") && trimmed.endsWith("'"))
  ) {
    return trimmed.slice(1, -1);
  }

  if (/^-?\d+$/.test(trimmed)) {
    return Number.parseInt(trimmed, 10);
  }

  if (/^-?\d+\.\d+$/.test(trimmed)) {
    return Number.parseFloat(trimmed);
  }

  if (trimmed === "true") {
    return true;
  }

  if (trimmed === "false") {
    return false;
  }

  if (trimmed === "null" || trimmed === "~") {
    return null;
  }

  return trimmed;
}

function splitInlineList(input: string): string[] {
  const inner = input.slice(1, -1).trim();
  if (!inner) {
    return [];
  }

  const parts: string[] = [];
  let current = "";
  let quote: '"' | "'" | null = null;
  let escaping = false;

  for (const char of inner) {
    if (escaping) {
      current += char;
      escaping = false;
      continue;
    }

    if (char === "\\") {
      escaping = true;
      current += char;
      continue;
    }

    if (quote) {
      if (char === quote) {
        quote = null;
      }
      current += char;
      continue;
    }

    if (char === '"' || char === "'") {
      quote = char;
      current += char;
      continue;
    }

    if (char === ",") {
      parts.push(current.trim());
      current = "";
      continue;
    }

    current += char;
  }

  if (current.trim()) {
    parts.push(current.trim());
  }

  return parts;
}

function parseFrontmatterValue(value: string): unknown {
  const trimmed = value.trim();
  if (!trimmed) {
    return "";
  }

  if (trimmed.startsWith("[") && trimmed.endsWith("]")) {
    return splitInlineList(trimmed).map((part) => parseScalarValue(part));
  }

  return parseScalarValue(trimmed);
}

function parseSimpleYaml(frontmatterText: string): FrontmatterRecord {
  const lines = frontmatterText.replace(/\r\n/g, "\n").split("\n");
  const record: FrontmatterRecord = {};

  for (let index = 0; index < lines.length; index += 1) {
    const rawLine = lines[index];
    if (!rawLine.trim() || rawLine.trim().startsWith("#")) {
      continue;
    }

    const keyValueMatch = rawLine.match(/^\s*([A-Za-z0-9_]+)\s*:\s*(.*)$/);
    if (!keyValueMatch) {
      continue;
    }

    const key = keyValueMatch[1];
    const remainder = keyValueMatch[2].trim();

    if (remainder.length > 0) {
      record[key] = parseFrontmatterValue(remainder);
      continue;
    }

    const listValues: unknown[] = [];
    let cursor = index + 1;
    while (cursor < lines.length) {
      const listMatch = lines[cursor].match(/^\s*-\s*(.+)\s*$/);
      if (!listMatch) {
        break;
      }

      listValues.push(parseFrontmatterValue(listMatch[1]));
      cursor += 1;
    }

    if (listValues.length > 0) {
      record[key] = listValues;
      index = cursor - 1;
      continue;
    }

    record[key] = "";
  }

  return record;
}

function splitFrontmatter(document: string): { frontmatter: FrontmatterRecord; body: string } {
  const normalized = document.replace(/\r\n/g, "\n");
  const match = normalized.match(/^---\n([\s\S]*?)\n---(?:\n|$)/);
  if (!match) {
    return { frontmatter: {}, body: normalized.trim() };
  }

  const frontmatter = parseSimpleYaml(match[1]);
  const body = normalized.slice(match[0].length).trim();
  return { frontmatter, body };
}

function createRegistryIssue(
  agentId: string,
  code: string,
  severity: RegistryIssueSeverity,
  message: string,
): RegistryIssue {
  return { agentId, code, severity, message };
}

function parseAgentTypeFromBody(body: string): number | null {
  const match = body.match(/^AGENT_TYPE:\s*([0-2])\s*$/m);
  if (!match) {
    return null;
  }

  return Number.parseInt(match[1], 10);
}

function parseAgentClassFromBody(body: string): string | null {
  const tableMatch = body.match(/^\|\s*\*\*AGENT_CLASS\*\*\s*\|\s*([^|]+?)\s*\|/m);
  if (tableMatch && tableMatch[1].trim()) {
    return tableMatch[1].trim().toUpperCase();
  }

  const scalarMatch = body.match(/^AGENT_CLASS:\s*([A-Za-z_]+)\s*$/m);
  if (scalarMatch && scalarMatch[1].trim()) {
    return scalarMatch[1].trim().toUpperCase();
  }

  return null;
}

function truncateSection(section: string, overflowChars: number, label: string): string {
  if (overflowChars <= 0 || !section) {
    return section;
  }

  const targetLength = section.length - overflowChars;
  if (targetLength <= 0) {
    return "";
  }

  const suffix = `\n\n[${label} truncated to fit prompt budget]`;
  if (targetLength <= suffix.length) {
    return suffix.slice(0, targetLength);
  }

  return `${section.slice(0, targetLength - suffix.length)}${suffix}`;
}

function joinPromptSections(base: string, projectContext: string, personaSection: string): string {
  const sections = [base];
  if (projectContext) {
    sections.push(projectContext);
  }
  if (personaSection) {
    sections.push(personaSection);
  }
  return sections.join("\n\n");
}

export class PersonaManager {
  private readonly textCache = new Map<string, CachedText>();
  private readonly instructionRoot: string;

  constructor(instructionRoot: string = getInstructionRoot()) {
    this.instructionRoot = path.resolve(instructionRoot);
  }

  getInstructionRoot(): string {
    return this.instructionRoot;
  }

  private instructionPersonaDir(): string {
    return path.join(this.instructionRoot, "agents");
  }

  private async fileStatSignature(filePath: string): Promise<string> {
    try {
      const fileStat = await stat(filePath);
      return `${path.resolve(filePath)}:${fileStat.mtimeMs}:${fileStat.size}`;
    } catch {
      return `${path.resolve(filePath)}:missing`;
    }
  }

  private async readCachedTextFile(filePath: string): Promise<string | null> {
    let fileStat;
    try {
      fileStat = await stat(filePath);
    } catch {
      this.textCache.delete(filePath);
      return null;
    }

    const cached = this.textCache.get(filePath);
    if (cached && cached.mtimeMs === fileStat.mtimeMs) {
      return cached.content;
    }

    let content: string;
    try {
      content = await readFile(filePath, "utf8");
    } catch {
      this.textCache.delete(filePath);
      return null;
    }

    this.textCache.set(filePath, { mtimeMs: fileStat.mtimeMs, content });
    return content;
  }

  private async parsePersonaFile(filePath: string): Promise<PersonaConfig | null> {
    const fileContents = await this.readCachedTextFile(filePath);
    if (fileContents === null) {
      return null;
    }

    const { frontmatter, body } = splitFrontmatter(fileContents);
    const id = path.basename(filePath).replace(/^AGENT_/i, "").replace(/\.md$/i, "");

    const parsed: PersonaConfig = {
      id,
      sourceFile: filePath,
    };

    if (body) {
      parsed.body = body;
    }

    const tools = toToolsValue(frontmatter.tools);
    if (tools) {
      parsed.tools = tools;
    }

    const disallowedTools = toStringList(frontmatter.disallowed_tools);
    if (disallowedTools) {
      parsed.disallowedTools = disallowedTools;
    }

    const autoApproveTools = toStringList(frontmatter.auto_approve_tools);
    if (autoApproveTools) {
      parsed.autoApproveTools = autoApproveTools;
    }

    const maxTurns = toPositiveInteger(frontmatter.max_turns);
    if (typeof maxTurns === "number") {
      parsed.maxTurns = maxTurns;
    }

    const description = stringifyScalar(frontmatter.description);
    if (description) {
      parsed.description = description;
    }

    const subagents = toStringList(frontmatter.subagents);
    if (subagents) {
      parsed.subagents = subagents;
    }

    return parsed;
  }

  async load(personaId: string): Promise<PersonaConfig | null> {
    const normalizedId = normalizePersonaId(personaId);
    if (!normalizedId) {
      return null;
    }

    const directPath = path.join(this.instructionPersonaDir(), `${PERSONA_FILE_PREFIX}${normalizedId}${PERSONA_FILE_SUFFIX}`);
    const directMatch = await this.parsePersonaFile(directPath);
    if (directMatch) {
      return directMatch;
    }

    const available = await this.list();
    return (
      available.find((persona) => {
        return normalizePersonaId(persona.id) === normalizedId;
      }) ?? null
    );
  }

  async getGlobalModel(): Promise<string | null> {
    const claudePath = path.join(this.instructionRoot, "CLAUDE.md");
    const content = await this.readCachedTextFile(claudePath);
    if (!content) {
      return null;
    }

    const { frontmatter } = splitFrontmatter(content);
    const modelInFrontmatter = stringifyScalar(frontmatter.model);
    if (modelInFrontmatter) {
      return modelInFrontmatter;
    }

    // Fallback: look for "model: value" in the body
    const match = content.match(/^model:\s*(.+)$/m);
    return match ? match[1].trim() : null;
  }

  async getBootFingerprint(persona: PersonaConfig | null, mode: SessionMode): Promise<string> {
    const files = [
      path.join(this.instructionRoot, "README.md"),
      path.join(this.instructionRoot, "AGENTS.md"),
      path.join(this.instructionRoot, "CLAUDE.md"),
    ];

    if (persona?.sourceFile) {
      files.push(path.resolve(persona.sourceFile));
    }

    const signatures = await Promise.all(files.map((filePath) => this.fileStatSignature(filePath)));
    signatures.sort((left, right) => left.localeCompare(right));

    const hash = createHash("sha256");
    hash.update(`mode:${mode}\n`);
    hash.update(`persona:${persona?.id ?? "none"}\n`);

    for (const signature of signatures) {
      hash.update(`${signature}\n`);
    }

    return hash.digest("hex");
  }

  async list(): Promise<PersonaConfig[]> {
    const personasDir = this.instructionPersonaDir();

    let entries: Dirent[];
    try {
      entries = await readdir(personasDir, { withFileTypes: true });
    } catch {
      return [];
    }

    const personas: PersonaConfig[] = [];
    for (const entry of entries) {
      if (!entry.isFile()) {
        continue;
      }

      if (!entry.name.startsWith(PERSONA_FILE_PREFIX) || !entry.name.endsWith(PERSONA_FILE_SUFFIX)) {
        continue;
      }

      const parsedPersona = await this.parsePersonaFile(path.join(personasDir, entry.name));
      if (parsedPersona) {
        personas.push(parsedPersona);
      }
    }

    return personas.sort((left, right) => left.id.localeCompare(right.id));
  }

  // ---------------------------------------------------------------------------
  // Subagent registry — builds SDK-native SubagentDefinition records from
  // agent instruction files for injection into Type 1 sessions.
  // ---------------------------------------------------------------------------

  /**
   * Compacts a subagent instruction body by stripping non-operational sections.
   * Only runs when the body exceeds `SUBAGENT_COMPACT_THRESHOLD`.
   * Returns the original body unchanged if compaction is disabled (threshold=0)
   * or if the body is under the threshold.
   */
  private compactSubagentPrompt(body: string, agentId: string): string {
    if (SUBAGENT_COMPACT_THRESHOLD <= 0 || body.length <= SUBAGENT_COMPACT_THRESHOLD) {
      return body;
    }

    let compacted = body;
    for (const pattern of COMPACT_STRIP_PATTERNS) {
      compacted = compacted.replace(pattern, "");
    }

    // Collapse runs of 3+ blank lines into 2
    compacted = compacted.replace(/\n{3,}/g, "\n\n").trim();

    if (compacted.length < body.length) {
      console.info(
        `[harness] Compacted subagent '${agentId}' prompt: ${body.length} → ${compacted.length} chars (${Math.round((1 - compacted.length / body.length) * 100)}% reduction)`,
      );
    }

    return compacted;
  }

  private collectRegistryIssues(agentId: string, frontmatter: FrontmatterRecord, body: string): RegistryIssue[] {
    const issues: RegistryIssue[] = [];

    if (!body.trim()) {
      issues.push(createRegistryIssue(agentId, "empty_instruction_body", "error", `${agentId}: empty instruction body`));
      return issues;
    }

    const parsedAgentType = parseAgentTypeFromBody(body);
    if (parsedAgentType === null) {
      issues.push(createRegistryIssue(agentId, "missing_agent_type", "error", `${agentId}: missing AGENT_TYPE in body header`));
    } else if (parsedAgentType !== 2) {
      issues.push(
        createRegistryIssue(
          agentId,
          "invalid_agent_type",
          "error",
          `${agentId}: AGENT_TYPE must be 2 for delegated subagents (found ${parsedAgentType})`,
        ),
      );
    }

    const parsedAgentClass = parseAgentClassFromBody(body);
    if (!parsedAgentClass) {
      issues.push(
        createRegistryIssue(
          agentId,
          "missing_agent_class",
          "warn",
          `${agentId}: missing AGENT_CLASS in Agent Type table (preferred TASK)`,
        ),
      );
    } else if (parsedAgentClass !== "TASK") {
      issues.push(
        createRegistryIssue(
          agentId,
          "agent_class_not_task",
          "warn",
          `${agentId}: AGENT_CLASS should be TASK for delegated subagents (found ${parsedAgentClass})`,
        ),
      );
    }

    if (!stringifyScalar(frontmatter.description)) {
      issues.push(
        createRegistryIssue(
          agentId,
          "missing_description_frontmatter",
          "warn",
          `${agentId}: missing 'description' frontmatter (runtime will use fallback)`,
        ),
      );
    }

    return issues;
  }

  /**
   * Builds SDK-native subagent definitions for a list of agent IDs.
   *
   * For each ID, resolves `agents/AGENT_{ID}.md`, reads/parses frontmatter,
   * and constructs a SubagentDefinition. Missing files or invalid configs are
   * logged and skipped — the parent turn proceeds with whatever agents resolved.
   *
   * @param agentIds - Array of Type 2 agent IDs (e.g., ["PREPARATION", "4_DOCUMENTS"])
   * @returns Record mapping agent ID to SubagentDefinition
   */
  async buildSubagentDefinitions(agentIds: string[]): Promise<Record<string, SubagentDefinition>> {
    const definitions: Record<string, SubagentDefinition> = {};
    const seen = new Set<string>();

    for (const rawId of agentIds) {
      const normalizedId = normalizePersonaId(rawId);
      if (!normalizedId) {
        console.warn(`[harness] Skipping empty subagent ID.`);
        continue;
      }

      // Duplicate check — first-wins
      if (seen.has(normalizedId)) {
        console.warn(`[harness] Duplicate subagent ID '${normalizedId}' — skipping.`);
        continue;
      }
      seen.add(normalizedId);

      const filePath = path.join(
        this.instructionPersonaDir(),
        `${PERSONA_FILE_PREFIX}${normalizedId}${PERSONA_FILE_SUFFIX}`,
      );

      const fileContents = await this.readCachedTextFile(filePath);
      if (fileContents === null) {
        console.warn(`[harness] Subagent file not found: ${filePath} — skipping '${normalizedId}'.`);
        continue;
      }

      const { frontmatter, body } = splitFrontmatter(fileContents);
      const registryIssues = this.collectRegistryIssues(normalizedId, frontmatter, body);
      const registryErrors = registryIssues.filter((issue) => issue.severity === "error");

      for (const issue of registryIssues) {
        const prefix = issue.severity === "error" ? "[harness] Subagent registry error" : "[harness] Subagent registry warning";
        console.warn(`${prefix}: ${issue.message}`);
      }

      if (registryErrors.length > 0) {
        continue;
      }

      // Description — required; fallback to first heading or first line
      let description = stringifyScalar(frontmatter.description) ?? null;
      if (!description) {
        const headingMatch = body.match(/^#\s+(.+)$/m);
        if (headingMatch) {
          description = headingMatch[1].trim();
          console.warn(
            `[harness] Subagent '${normalizedId}' missing 'description' frontmatter — falling back to heading: "${description}"`,
          );
        } else {
          description = `Agent ${normalizedId}`;
          console.warn(
            `[harness] Subagent '${normalizedId}' missing 'description' frontmatter and no heading found — using default.`,
          );
        }
      }

      // Prompt — compacted instruction body
      const prompt = this.compactSubagentPrompt(body, normalizedId);
      if (!prompt) {
        console.warn(`[harness] Subagent '${normalizedId}' has empty instruction body — skipping.`);
        continue;
      }

      // Tools — from frontmatter; strip "Task" to prevent nesting
      let tools = toStringList(frontmatter.tools) as string[] | undefined;
      if (tools && tools.includes("Task")) {
        console.warn(`[harness] Stripping 'Task' from subagent '${normalizedId}' tools — nesting not permitted.`);
        tools = tools.filter((t) => t !== "Task");
        if (tools.length === 0) {
          tools = undefined;
        }
      }

      // Model — validate if present
      const rawModel = stringifyScalar(frontmatter.model) ?? null;
      let model: SubagentDefinition["model"];
      if (rawModel) {
        const lower = rawModel.toLowerCase();
        if (VALID_SUBAGENT_MODELS.has(lower)) {
          model = lower as SubagentDefinition["model"];
        } else {
          console.warn(
            `[harness] Subagent '${normalizedId}' has invalid model '${rawModel}' — omitting (will inherit parent model).`,
          );
        }
      }

      const def: SubagentDefinition = { description, prompt };
      if (tools) {
        def.tools = tools;
      }
      if (model) {
        def.model = model;
      }

      definitions[normalizedId] = def;
    }

    return definitions;
  }

  /**
   * Machine-readable registry validation. Returns which agent IDs resolved
   * successfully and which had errors. Does not modify state.
   */
  async validateRegistry(agentIds: string[]): Promise<RegistryValidationResult> {
    const valid: string[] = [];
    const errors: string[] = [];
    const issues: RegistryIssue[] = [];
    const seen = new Set<string>();

    for (const rawId of agentIds) {
      const normalizedId = normalizePersonaId(rawId);
      if (!normalizedId) {
        issues.push(createRegistryIssue(String(rawId), "empty_agent_id", "error", `Empty agent ID from input '${rawId}'`));
        continue;
      }

      if (seen.has(normalizedId)) {
        issues.push(
          createRegistryIssue(normalizedId, "duplicate_agent_id", "warn", `${normalizedId}: duplicate agent ID in input list`),
        );
        continue;
      }
      seen.add(normalizedId);

      const filePath = path.join(
        this.instructionPersonaDir(),
        `${PERSONA_FILE_PREFIX}${normalizedId}${PERSONA_FILE_SUFFIX}`,
      );

      const fileContents = await this.readCachedTextFile(filePath);
      if (fileContents === null) {
        issues.push(
          createRegistryIssue(
            normalizedId,
            "file_not_found",
            "error",
            `${normalizedId}: file not found at ${filePath}`,
          ),
        );
        continue;
      }

      const { frontmatter, body } = splitFrontmatter(fileContents);
      const perAgentIssues = this.collectRegistryIssues(normalizedId, frontmatter, body);
      issues.push(...perAgentIssues);

      const hasError = perAgentIssues.some((issue) => issue.severity === "error");
      if (!hasError) {
        valid.push(normalizedId);
      }
    }

    for (const issue of issues) {
      if (issue.severity === "error") {
        errors.push(issue.message);
      }
    }

    return { valid, errors, issues };
  }

  async buildSystemPrompt(projectRoot: string, persona: PersonaConfig | null, mode: SessionMode): Promise<string> {
    const root = path.resolve(projectRoot);

    const baseSection = [
      DEFAULT_SYSTEM_PROMPT,
      `Project root: ${root}`,
      `Instruction root: ${this.instructionRoot}`,
      `Mode: ${mode}`,
      modeInstruction(mode),
    ].join("\n\n");

    const readmePath = path.join(this.instructionRoot, "README.md");
    const agentsPath = path.join(this.instructionRoot, "AGENTS.md");

    const [readmeContents, agentsContents] = await Promise.all([
      this.readCachedTextFile(readmePath),
      this.readCachedTextFile(agentsPath),
    ]);

    const projectContextSections: string[] = [];
    const readmeText = readmeContents?.trim();
    const agentsText = agentsContents?.trim();
    if (readmeText) {
      projectContextSections.push(`Instruction README.md:\n${readmeText}`);
    }
    if (agentsText) {
      projectContextSections.push(`Instruction AGENTS.md:\n${agentsText}`);
    }

    let projectContext = projectContextSections.join("\n\n");

    let personaBody = "";
    if (persona?.sourceFile) {
      const sourceContents = await this.readCachedTextFile(persona.sourceFile);
      if (sourceContents !== null) {
        personaBody = splitFrontmatter(sourceContents).body.trim();
      } else if (persona.body) {
        personaBody = persona.body.trim();
      }
    } else if (persona?.body) {
      personaBody = persona.body.trim();
    }

    let personaSection = "";
    if (personaBody) {
      personaSection = `Persona instructions (${persona?.id ?? "unknown"}):\n${personaBody}`;
    }

    let prompt = joinPromptSections(baseSection, projectContext, personaSection);
    let overflow = prompt.length - PROMPT_CHAR_BUDGET;

    if (overflow > 0 && personaSection) {
      personaSection = truncateSection(personaSection, overflow, "Persona instructions");
      prompt = joinPromptSections(baseSection, projectContext, personaSection);
      overflow = prompt.length - PROMPT_CHAR_BUDGET;
    }

    if (overflow > 0 && projectContext) {
      projectContext = truncateSection(projectContext, overflow, "Project context");
      prompt = joinPromptSections(baseSection, projectContext, personaSection);
    }

    return prompt;
  }

  async writeSystemPromptFile(projectRoot: string, sessionId: string, prompt: string): Promise<string> {
    const promptsDir = path.join(path.resolve(projectRoot), ".chirality", "prompts");
    const filePath = path.join(promptsDir, `${sessionId}-system.txt`);
    const tmpPath = `${filePath}.tmp-${process.pid}-${Date.now()}`;

    await mkdir(promptsDir, { recursive: true });

    try {
      await writeFile(tmpPath, prompt, "utf8");
      await rename(tmpPath, filePath);
    } catch (error) {
      await rm(tmpPath, { force: true }).catch(() => undefined);
      throw error;
    }

    return filePath;
  }
}
