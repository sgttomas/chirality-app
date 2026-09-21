import { createHash } from 'node:crypto';
import { readFile } from 'node:fs/promises';
import path from 'node:path';
import { readAgentInstruction } from './agent-instruction';
import { assertInstructionRootReadable } from './instruction-root';
import {
  HARNESS_PERMISSION_POLICY_VERSION,
  normalizeHarnessPermissionMode
} from './permission-overlay';
import { SUBAGENT_BRIDGE_POLICY_VERSION } from './subagent-bridge';
import { resolveHarnessToolPool } from './tool-pool';
import { HARNESS_TOOL_REGISTRY_VERSION } from '@chirality/runtime-contracts/tool-descriptor';
import { CHIRALITY_MCP_SERVER_NAME } from '@chirality/runtime-contracts/mcp/tool-names';
import { IPersonaManager } from '@chirality/runtime-contracts/types';
import { GENERALIST_AGENT2_PERSONA, UNTYPED_PERSONA } from './agent-roster';

export const PERSONA_COMPOSER_VERSION = 'persona-composer.v2.role-selective';

const HASH_LENGTH = 64;

const GOVERNANCE_RESOURCE_PATHS = [
  'AGENTS.md'
] as const;

type GovernanceResource = {
  relativePath: string;
  content: string;
  contentHash: string;
};

type PersonaComposition = {
  systemPrompt: string;
  promptHash: string;
  bootFingerprint: string;
};

function sha256Hex(value: string): string {
  return createHash('sha256').update(value).digest('hex');
}

function normalizeMarkdown(value: string): string {
  return value.replace(/\r\n/g, '\n').trim();
}

function normalizeTools(tools: readonly string[] | undefined): string[] {
  return (tools ?? [])
    .map((tool) => tool.trim())
    .filter((tool) => tool.length > 0);
}

function createCacheKey(input: {
  projectRoot?: string;
  persona: string;
  mode: string;
  tools?: readonly string[];
}): string {
  return JSON.stringify({
    projectRoot: input.projectRoot ? path.resolve(input.projectRoot) : undefined,
    persona: input.persona.trim(),
    mode: input.mode.trim(),
    tools: normalizeTools(input.tools)
  });
}

async function readGovernanceResources(instructionRoot: string): Promise<GovernanceResource[]> {
  const resources: GovernanceResource[] = [];

  for (const relativePath of GOVERNANCE_RESOURCE_PATHS) {
    const content = await readFile(path.join(instructionRoot, relativePath), 'utf8');
    resources.push({
      relativePath,
      content,
      contentHash: sha256Hex(normalizeMarkdown(content))
    });
  }

  return resources;
}

function renderGovernancePreface(resources: readonly GovernanceResource[]): string {
  const resourceSections = resources.map((resource) =>
    [
      `### ${resource.relativePath}`,
      `contentSha256: ${resource.contentHash}`,
      normalizeMarkdown(resource.content)
    ].join('\n')
  );

  return [
    '## Chirality Governance Preface',
    `composerVersion: ${PERSONA_COMPOSER_VERSION}`,
    'The role overview below is sourced from the resolved instruction root. Runtime supplies selected method bodies and resources separately as a frozen context basis.',
    'Agents propose; humans approve. Do not represent runtime output or validation evidence as approval, issuance, publication authorization, certification, sealing, authentication, code-compliance acceptance, or a substitute for professional judgment.',
    ...resourceSections
  ].join('\n\n');
}

function renderWorkingRootPolicy(projectRoot: string): string {
  const normalizedProjectRoot = path.resolve(projectRoot);
  return [
    '## Working Root Policy',
    `projectRoot: ${normalizedProjectRoot}`,
    'Treat projectRoot as the mutable workspace boundary for this turn.',
    'Keep the release-managed instruction root read-only during ordinary project execution.',
    'Do not write outside projectRoot. Do not mutate instruction-root resources. Do not treat runtime logs, transcripts, or generated artifacts as authoritative decomposition truth.'
  ].join('\n');
}

function renderModePolicy(mode: string): string {
  const normalizedMode = normalizeHarnessPermissionMode(mode);
  const modePolicy: Record<typeof normalizedMode, string> = {
    readOnly:
      'Read-only posture. Read-class tools may be pre-approved; write, shell, network, and unexpected tools are denied.',
    workspaceWrite:
      'Workspace-write posture. Write/Edit/Bash remain subject to descriptor resolution, permission overlay, path hooks, instruction-root protection, symlink rejection, and provenance evidence.',
    dontAsk:
      'Do-not-ask posture. Exact safe tools may run without prompting; unapproved tools deny without model-visible escalation.',
    ask:
      'Ask posture. Governed writes and shell actions require application approval before execution.',
    bypass:
      'Developer-local bypass posture. Explicit hard-deny rules, disallowed tools, path hooks, instruction-root protection, and subagent governance still apply.'
  };

  return [
    '## Mode Policy',
    `requestedMode: ${mode}`,
    `normalizedMode: ${normalizedMode}`,
    modePolicy[normalizedMode]
  ].join('\n');
}

function renderToolSurface(input: {
  sessionId: string;
  mode: string;
  tools: readonly string[];
}): string {
  const toolPool = resolveHarnessToolPool({
    sessionId: input.sessionId,
    requestedTools: input.tools,
    mode: input.mode
  });
  const allowed = toolPool.allowedToolNames.length > 0 ? toolPool.allowedToolNames.join(', ') : 'none';
  const disallowed =
    toolPool.disallowedToolNames.length > 0 ? toolPool.disallowedToolNames.join(', ') : 'none';
  const denied =
    toolPool.deniedTools.length > 0
      ? toolPool.deniedTools
          .map((issue) =>
            issue.type === 'DENIED_BY_CURRENT_PHASE'
              ? `${issue.toolName} -> ${issue.descriptorName}: ${issue.message}`
              : `${issue.toolName}: ${issue.message}`
          )
          .join('\n')
      : 'none';
  const unknown =
    toolPool.unknownTools.length > 0
      ? toolPool.unknownTools.map((issue) => issue.toolName).join(', ')
      : 'none';

  return [
    '## Tool Surface Posture',
    `toolRegistryVersion: ${HARNESS_TOOL_REGISTRY_VERSION}`,
    `permissionPolicyVersion: ${HARNESS_PERMISSION_POLICY_VERSION}`,
    `subagentPolicyVersion: ${SUBAGENT_BRIDGE_POLICY_VERSION}`,
    `mcpServerNames: ${CHIRALITY_MCP_SERVER_NAME}`,
    `requestedTools: ${toolPool.requestedTools.length > 0 ? toolPool.requestedTools.join(', ') : 'none'}`,
    `allowedAdapterTools: ${allowed}`,
    `disallowedAdapterTools: ${disallowed}`,
    `deniedRequestedTools:\n${denied}`,
    `unknownRequestedTools: ${unknown}`,
    'allowedTools alone is not a security boundary; permissionMode, disallowedTools, canUseTool, hooks, and Chirality policy remain authoritative at execution time.'
  ].join('\n');
}

function renderPersonaSection(input: {
  persona: string;
  relativePath: string;
  content: string;
  contentHash: string;
}): string {
  return [
    '## Active Persona Instruction',
    `persona: ${input.persona}`,
    `source: ${input.relativePath}`,
    `contentSha256: ${input.contentHash}`,
    normalizeMarkdown(input.content)
  ].join('\n');
}

export class PersonaComposer implements IPersonaManager {
  private readonly compositions = new Map<string, PersonaComposition>();

  async buildSystemPrompt(
    projectRoot: string,
    persona: string,
    mode: string,
    tools?: readonly string[]
  ): Promise<string> {
    const instructionRoot = await assertInstructionRootReadable();
    const [personaInstruction, governanceResources] = await Promise.all([
      [UNTYPED_PERSONA, GENERALIST_AGENT2_PERSONA].includes(persona.trim().toUpperCase())
        ? Promise.resolve({
            instructionRoot,
            path: path.join(instructionRoot, 'AGENTS.md'),
            content: persona.trim().toUpperCase() === UNTYPED_PERSONA
              ? '# Untyped Direct Session\n\nFollow root AGENTS.md and current human steering. No persistent agent role is selected. Do not delegate until the human selects HELP_HUMAN or a named Agent 1 manager.'
              : '# Ephemeral Generalist Agent 2\n\nFollow the Agent 2 base contract in root AGENTS.md and the sealed launch brief. You have no persistent role package. Use only declared context, tools, and write targets. Return to the direct parent and do not delegate.'
          })
        : readAgentInstruction(persona, instructionRoot),
      readGovernanceResources(instructionRoot)
    ]);
    const personaContentHash = sha256Hex(normalizeMarkdown(personaInstruction.content));
    const relativePersonaPath = path.relative(instructionRoot, personaInstruction.path);
    const normalizedTools = normalizeTools(tools);

    const systemPrompt = [
      '# Chirality Agent Runtime Context',
      renderGovernancePreface(governanceResources),
      renderPersonaSection({
        persona,
        relativePath: relativePersonaPath,
        content: personaInstruction.content,
        contentHash: personaContentHash
      }),
      renderWorkingRootPolicy(projectRoot),
      renderModePolicy(mode),
      renderToolSurface({
        sessionId: `persona:${persona}`,
        mode,
        tools: normalizedTools
      })
    ].join('\n\n---\n\n');

    const promptHash = sha256Hex(systemPrompt);
    const cacheKey = createCacheKey({
      projectRoot,
      persona,
      mode,
      tools: normalizedTools
    });
    this.compositions.set(cacheKey, {
      systemPrompt,
      promptHash,
      bootFingerprint: promptHash.slice(0, HASH_LENGTH)
    });

    return systemPrompt;
  }

  getBootFingerprint(
    persona: string,
    mode: string,
    projectRoot?: string,
    tools?: readonly string[]
  ): string {
    const cacheKey = createCacheKey({
      projectRoot,
      persona,
      mode,
      tools
    });
    const composition = this.compositions.get(cacheKey);
    if (composition) {
      return composition.bootFingerprint;
    }

    return sha256Hex(
      JSON.stringify({
        composerVersion: PERSONA_COMPOSER_VERSION,
        persona: persona.trim(),
        mode: mode.trim(),
        projectRoot: projectRoot ? path.resolve(projectRoot) : undefined,
        tools: normalizeTools(tools)
      })
    ).slice(0, HASH_LENGTH);
  }
}
