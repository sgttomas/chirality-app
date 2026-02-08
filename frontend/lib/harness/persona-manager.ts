import type { Dirent } from "node:fs";
import { mkdir, readFile, readdir, rename, rm, stat, writeFile } from "node:fs/promises";
import path from "node:path";

import { DEFAULT_SYSTEM_PROMPT, PROMPT_TOKEN_BUDGET } from "./defaults";
import type { PersonaConfig, SessionMode } from "./types";

const CHAR_PER_TOKEN_ESTIMATE = 4;
const PROMPT_CHAR_BUDGET = PROMPT_TOKEN_BUDGET * CHAR_PER_TOKEN_ESTIMATE;
const PERSONA_FILE_PREFIX = "AGENT_";
const PERSONA_FILE_SUFFIX = ".md";

type CachedText = {
  mtimeMs: number;
  content: string;
};

type FrontmatterRecord = Record<string, unknown>;

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

  private projectPersonaDir(projectRoot: string): string {
    return path.join(path.resolve(projectRoot), "agents");
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

    return parsed;
  }

  async load(projectRoot: string, personaId: string): Promise<PersonaConfig | null> {
    const normalizedId = normalizePersonaId(personaId);
    if (!normalizedId) {
      return null;
    }

    const directPath = path.join(this.projectPersonaDir(projectRoot), `${PERSONA_FILE_PREFIX}${normalizedId}${PERSONA_FILE_SUFFIX}`);
    const directMatch = await this.parsePersonaFile(directPath);
    if (directMatch) {
      return directMatch;
    }

    const available = await this.list(projectRoot);
    return (
      available.find((persona) => {
        return normalizePersonaId(persona.id) === normalizedId;
      }) ?? null
    );
  }

  async getGlobalModel(projectRoot: string): Promise<string | null> {
    const claudePath = path.join(path.resolve(projectRoot), "CLAUDE.md");
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

  async list(projectRoot: string): Promise<PersonaConfig[]> {
    const personasDir = this.projectPersonaDir(projectRoot);

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

  async buildSystemPrompt(projectRoot: string, persona: PersonaConfig | null, mode: SessionMode): Promise<string> {
    const root = path.resolve(projectRoot);

    const baseSection = [
      DEFAULT_SYSTEM_PROMPT,
      `Project root: ${root}`,
      `Mode: ${mode}`,
      modeInstruction(mode),
    ].join("\n\n");

    const readmePath = path.join(root, "README.md");
    const agentsPath = path.join(root, "AGENTS.md");

    const [readmeContents, agentsContents] = await Promise.all([
      this.readCachedTextFile(readmePath),
      this.readCachedTextFile(agentsPath),
    ]);

    const projectContextSections: string[] = [];
    const readmeText = readmeContents?.trim();
    const agentsText = agentsContents?.trim();
    if (readmeText) {
      projectContextSections.push(`README.md:\n${readmeText}`);
    }
    if (agentsText) {
      projectContextSections.push(`AGENTS.md:\n${agentsText}`);
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
