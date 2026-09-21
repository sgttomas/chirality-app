import {
  createSdkMcpServer,
  tool,
  type McpServerConfig,
  type McpSdkServerConfigWithInstance,
  type SdkMcpToolDefinition
} from '@anthropic-ai/claude-agent-sdk';
import type { CallToolResult } from '@modelcontextprotocol/sdk/types.js';
import { createHash } from 'node:crypto';
import { readFile, realpath, stat } from 'node:fs/promises';
import path from 'node:path';
import { z } from 'zod/v4';
import { previewScaffoldExecutionRoot } from '../scaffold';
import type { CoordinationMode } from '../scaffold';
import { createHarnessEvent } from '../event-factory';
import {
  readDeliverableDependencies,
  readDeliverableStatus,
  transitionDeliverableStatus,
  writeDeliverableDependencies
} from '../../workspace/deliverable-contracts';
import type { DependencyRegisterRow } from '../../dependencies/schema';
import { normalizeProjectRoot, scanProjectScopes } from '../../workspace/filesystem';
import { HarnessError } from '@chirality/runtime-contracts/errors';
import {
  appendHarnessPermissionDecisionEvent,
  resolveHarnessPermissionDecision
} from '../permission-overlay';
import { appendHarnessEvent } from '../session-events';
import {
  summarizeToolDescriptor,
  summarizeToolError,
  summarizeToolInput,
  summarizeToolResult,
  withToolResultPersistence
} from '../tool-evidence';
import { persistToolResultArtifact } from '../tool-result-artifacts';
import { getHarnessToolDescriptor } from '@chirality/runtime-contracts/tool-descriptor';
import { evaluateToolPathPolicy } from '../tool-path-policy';
import {
  CHIRALITY_MCP_SERVER_NAME,
  CHIRALITY_MCP_SERVER_VERSION,
  isChiralityMcpAllowedToolName,
  toChiralityMcpAllowedToolName,
  type ChiralityMcpAllowedToolName,
  type ChiralityMcpDomainToolName,
  type ChiralityMcpMutatingToolName,
  type ChiralityMcpReadToolName
} from '@chirality/runtime-contracts/mcp/tool-names';
import {
  resolveDomainEngineProfile,
  type DomainEngineProfileRegistryEntry,
  type DomainReadToolId
} from './domain-profile-registry';
import {
  domainProposalValidateTool,
  domainProposeOperationTool,
  PEC_PROPOSAL_CONTRACTS,
  type DomainProposalValidateArgs,
  type DomainProposeOperationArgs
} from './domain-proposal-tools';
import { buildCoordinationMcpTools } from './coordination-tools';
import { runConfiguredHeadlessPreview } from './domain-headless-preview-runner';

export type ChiralityReadMcpContext = {
  projectRoot: string;
  sessionId: string;
  persona?: string;
  mode?: string;
  tools?: readonly string[];
};

export type ChiralityMutatingMcpContext = ChiralityReadMcpContext & {
  mode: string;
};

export type StatusReadArgs = {
  deliverablePath: string;
};

export type DependenciesReadArgs = {
  deliverablePath: string;
};

export type ScopeScanArgs = Record<string, never>;

export type ScaffoldPreviewArgs = {
  executionRoot: string;
  decompositionPath: string;
  projectName?: string;
  coordinationMode?: string;
};

export type DomainCompletenessCheckArgs = {
  profileId: string;
  inputRef: string;
};

export type DomainRuleCheckRunArgs = {
  profileId: string;
  rulePackRef: string;
  valueBindingsRef: string;
};

export type DomainHeadlessPreviewRunArgs = {
  profileId: string;
  runnerInputRef: string;
};

export type StatusTransitionArgs = {
  deliverablePath: string;
  targetState: string;
  actor: string;
  date?: string;
  approvalSha?: string;
  metadata?: Record<string, string>;
};

export type DependenciesWriteArgs = {
  deliverablePath: string;
  rows: DependencyRegisterRow[];
};

type FileEvidence =
  | {
      exists: true;
      sha256: string;
      byteLength: number;
    }
  | {
      exists: false;
      sha256?: undefined;
      byteLength: 0;
    };

function asRecord(value: unknown): Record<string, unknown> | undefined {
  return Boolean(value) && typeof value === 'object' && !Array.isArray(value)
    ? (value as Record<string, unknown>)
    : undefined;
}

function jsonToolResult(value: unknown): CallToolResult {
  return {
    content: [
      {
        type: 'text',
        text: JSON.stringify(value, null, 2)
      }
    ]
  };
}

async function runReadMcpToolWithEvidence(input: {
  context: ChiralityReadMcpContext;
  toolName: ChiralityMcpReadToolName | ChiralityMcpDomainToolName;
  args: unknown;
  execute: () => Promise<CallToolResult>;
}): Promise<CallToolResult> {
  const descriptor = getHarnessToolDescriptor(input.toolName);
  const adapterToolName =
    descriptor?.adapter.claudeAgentSdk?.toolName ?? toChiralityMcpAllowedToolName(input.toolName);
  const eventBase = {
    source: 'chirality-mcp',
    adapterToolName,
    toolName: descriptor?.name ?? input.toolName,
    ...summarizeToolDescriptor(descriptor)
  };
  const startedAt = Date.now();

  await appendHarnessEvent(
    createHarnessEvent({
      sessionId: input.context.sessionId,
      type: 'tool.started',
      data: {
        ...eventBase,
        inputMetadata: summarizeToolInput(input.args)
      }
    })
  );

  try {
    const result = await input.execute();
    const artifactMetadata = await persistToolResultArtifact({
      sessionId: input.context.sessionId,
      toolUseId: `${input.toolName}-${startedAt}`,
      toolName: adapterToolName,
      descriptor,
      result
    });
    await appendHarnessEvent(
      createHarnessEvent({
        sessionId: input.context.sessionId,
        type: 'tool.completed',
        data: {
          ...eventBase,
          durationMs: Date.now() - startedAt,
          resultMetadata: withToolResultPersistence(
            summarizeToolResult(result, descriptor),
            Boolean(artifactMetadata)
          ),
          artifactMetadata
        }
      })
    );
    return result;
  } catch (error) {
    try {
      await appendHarnessEvent(
        createHarnessEvent({
          sessionId: input.context.sessionId,
          type: 'tool.failed',
          data: {
            ...eventBase,
            failureSource: 'handler',
            durationMs: Date.now() - startedAt,
            error: summarizeToolError(error)
          }
        })
      );
    } catch {
      // Preserve the original tool failure if failure-evidence persistence also fails.
    }
    throw error;
  }
}

async function assertReadMcpPermission(input: {
  context: ChiralityReadMcpContext;
  toolName: ChiralityMcpDomainToolName;
  args: unknown;
}): Promise<Record<string, unknown>> {
  const descriptor = getHarnessToolDescriptor(input.toolName);
  const pathPolicy = await evaluateToolPathPolicy({
    descriptor,
    projectRoot: input.context.projectRoot,
    toolInput: input.args
  });
  const decision = resolveHarnessPermissionDecision({
    sessionId: input.context.sessionId,
    mode: input.context.mode ?? 'readOnly',
    toolName: toChiralityMcpAllowedToolName(input.toolName),
    descriptor,
    source: 'chirality-policy',
    toolInput: asRecord(input.args),
    explicitDeny: !pathPolicy.allowed,
    explicitDenyReason: pathPolicy.allowed ? undefined : pathPolicy.reason,
    safeMetadata: {
      inputMetadata: summarizeToolInput(input.args),
      pathMetadata: pathPolicy.metadata
    }
  });
  await appendHarnessPermissionDecisionEvent({ decision, descriptor });
  if (decision.decision !== 'allow') {
    throw new HarnessError('INVALID_REQUEST', 403, decision.reason, {
      decisionId: decision.decisionId,
      decision: decision.decision,
      safeMetadata: decision.safeMetadata
    });
  }
  return {
    decisionId: decision.decisionId,
    pathMetadata: pathPolicy.metadata
  };
}

function resolveProjectPath(projectRoot: string, candidatePath: string): string {
  return path.isAbsolute(candidatePath)
    ? path.resolve(candidatePath)
    : path.resolve(projectRoot, candidatePath);
}

async function readFileEvidence(filePath: string): Promise<FileEvidence> {
  try {
    const content = await readFile(filePath);
    return {
      exists: true,
      sha256: createHash('sha256').update(content).digest('hex'),
      byteLength: content.byteLength
    };
  } catch (error) {
    if ((error as NodeJS.ErrnoException).code === 'ENOENT') {
      return {
        exists: false,
        byteLength: 0
      };
    }
    throw error;
  }
}

function summarizeFileChange(before: FileEvidence, after: FileEvidence): Record<string, unknown> {
  return {
    before: {
      exists: before.exists,
      sha256: before.sha256,
      byteLength: before.byteLength
    },
    after: {
      exists: after.exists,
      sha256: after.sha256,
      byteLength: after.byteLength
    },
    diffSummary: {
      existedBefore: before.exists,
      existsAfter: after.exists,
      byteDelta: after.byteLength - before.byteLength,
      shaChanged: before.sha256 !== after.sha256
    }
  };
}

async function assertMutatingMcpPermission(input: {
  context: ChiralityMutatingMcpContext;
  toolName: ChiralityMcpMutatingToolName;
  args: unknown;
  targetFilePath: string;
}): Promise<Record<string, unknown>> {
  const descriptor = getHarnessToolDescriptor(input.toolName);
  const deliverablePathPolicy = await evaluateToolPathPolicy({
    descriptor,
    projectRoot: input.context.projectRoot,
    toolInput: input.args
  });
  const targetPathPolicy = await evaluateToolPathPolicy({
    descriptor,
    projectRoot: input.context.projectRoot,
    toolInput: {
      path: input.targetFilePath
    }
  });
  const explicitDeny = !deliverablePathPolicy.allowed || !targetPathPolicy.allowed;
  const explicitDenyReason = !deliverablePathPolicy.allowed
    ? deliverablePathPolicy.reason
    : !targetPathPolicy.allowed
      ? targetPathPolicy.reason
      : undefined;
  const decision = resolveHarnessPermissionDecision({
    sessionId: input.context.sessionId,
    mode: input.context.mode,
    toolName: toChiralityMcpAllowedToolName(input.toolName),
    descriptor,
    source: 'chirality-policy',
    toolInput: asRecord(input.args),
    explicitDeny,
    explicitDenyReason,
    safeMetadata: {
      inputMetadata: summarizeToolInput(input.args),
      pathMetadata: deliverablePathPolicy.metadata,
      targetPathMetadata: targetPathPolicy.metadata
    }
  });

  await appendHarnessPermissionDecisionEvent({
    decision,
    descriptor
  });

  if (decision.decision !== 'allow') {
    throw new HarnessError('INVALID_REQUEST', 403, decision.reason, {
      decisionId: decision.decisionId,
      decision: decision.decision,
      safeMetadata: decision.safeMetadata
    });
  }

  return {
    decisionId: decision.decisionId,
    pathMetadata: deliverablePathPolicy.metadata,
    targetPathMetadata: targetPathPolicy.metadata
  };
}

async function runMutatingMcpToolWithEvidence(input: {
  context: ChiralityMutatingMcpContext;
  toolName: ChiralityMcpMutatingToolName;
  args: unknown;
  targetFilePath: string;
  execute: () => Promise<{
    result: CallToolResult;
    resultSummary: Record<string, unknown>;
  }>;
}): Promise<CallToolResult> {
  const descriptor = getHarnessToolDescriptor(input.toolName);
  const adapterToolName =
    descriptor?.adapter.claudeAgentSdk?.toolName ?? toChiralityMcpAllowedToolName(input.toolName);
  const eventBase = {
    source: 'chirality-mcp',
    adapterToolName,
    toolName: descriptor?.name ?? input.toolName,
    ...summarizeToolDescriptor(descriptor)
  };
  const startedAt = Date.now();

  await appendHarnessEvent(
    createHarnessEvent({
      sessionId: input.context.sessionId,
      type: 'tool.started',
      data: {
        ...eventBase,
        inputMetadata: summarizeToolInput(input.args)
      }
    })
  );

  try {
    const permissionMetadata = await assertMutatingMcpPermission({
      context: input.context,
      toolName: input.toolName,
      args: input.args,
      targetFilePath: input.targetFilePath
    });
    const before = await readFileEvidence(input.targetFilePath);
    const { result, resultSummary } = await input.execute();
    const after = await readFileEvidence(input.targetFilePath);
    const fileEvidence = summarizeFileChange(before, after);
    const artifactMetadata = await persistToolResultArtifact({
      sessionId: input.context.sessionId,
      toolUseId: `${input.toolName}-${startedAt}`,
      toolName: adapterToolName,
      descriptor,
      result
    });

    await appendHarnessEvent(
      createHarnessEvent({
        sessionId: input.context.sessionId,
        type: 'tool.completed',
        data: {
          ...eventBase,
          durationMs: Date.now() - startedAt,
          permissionMetadata,
          resultSummary,
          fileEvidence,
          resultMetadata: withToolResultPersistence(
            summarizeToolResult(result, descriptor),
            Boolean(artifactMetadata)
          ),
          artifactMetadata
        }
      })
    );
    return result;
  } catch (error) {
    try {
      await appendHarnessEvent(
        createHarnessEvent({
          sessionId: input.context.sessionId,
          type: 'tool.failed',
          data: {
            ...eventBase,
            failureSource: 'handler',
            durationMs: Date.now() - startedAt,
            error: summarizeToolError(error)
          }
        })
      );
    } catch {
      // Preserve the original tool failure if failure-evidence persistence also fails.
    }
    throw error;
  }
}

function assertLexicallyWithinProjectRoot(input: {
  projectRoot: string;
  candidatePath: string;
  field: string;
}): string {
  const projectRoot = path.resolve(input.projectRoot);
  const candidatePath = path.resolve(input.candidatePath);
  const relative = path.relative(projectRoot, candidatePath);
  if (relative.startsWith('..') || path.isAbsolute(relative)) {
    throw new HarnessError(
      'INVALID_REQUEST',
      400,
      `${input.field} must resolve inside projectRoot`,
      {
        projectRoot,
        [input.field]: candidatePath
      }
    );
  }
  return candidatePath;
}

async function assertExistingPathWithinProjectRoot(input: {
  projectRoot: string;
  candidatePath: string;
  field: string;
}): Promise<string> {
  const projectRoot = await realpath(path.resolve(input.projectRoot));
  const candidatePath = await realpath(path.resolve(input.candidatePath));
  const relative = path.relative(projectRoot, candidatePath);
  if (relative.startsWith('..') || path.isAbsolute(relative)) {
    throw new HarnessError(
      'INVALID_REQUEST',
      400,
      `${input.field} must resolve inside projectRoot`,
      {
        projectRoot,
        [input.field]: candidatePath
      }
    );
  }
  return candidatePath;
}

function summarizeJsonValue(value: unknown): Record<string, unknown> {
  if (Array.isArray(value)) {
    return {
      topLevelType: 'array',
      length: value.length
    };
  }
  if (value && typeof value === 'object') {
    const keys = Object.keys(value as Record<string, unknown>).sort();
    return {
      topLevelType: 'object',
      keys: keys.slice(0, 32),
      keyCount: keys.length
    };
  }
  return {
    topLevelType: value === null ? 'null' : typeof value
  };
}

async function readProjectTextReference(input: {
  projectRoot: string;
  reference: string;
  field: string;
}): Promise<{
  content: string;
  evidence: {
    path: string;
    relativePath: string;
    sha256: string;
    byteLength: number;
  };
}> {
  const projectRoot = await realpath(path.resolve(input.projectRoot));
  const filePath = await assertExistingPathWithinProjectRoot({
    projectRoot,
    candidatePath: resolveProjectPath(projectRoot, input.reference),
    field: input.field
  });
  const content = await readFile(filePath, 'utf8');
  return {
    content,
    evidence: {
      path: filePath,
      relativePath: path.relative(projectRoot, filePath),
      sha256: createHash('sha256').update(content).digest('hex'),
      byteLength: Buffer.byteLength(content)
    }
  };
}

async function readProjectBinaryReference(input: {
  projectRoot: string;
  reference: string;
  field: string;
}): Promise<{
  content: Buffer;
  evidence: {
    relativePath: string;
    sha256: string;
    byteLength: number;
  };
}> {
  const projectRoot = await realpath(path.resolve(input.projectRoot));
  let filePath: string;
  try {
    filePath = await assertExistingPathWithinProjectRoot({
      projectRoot,
      candidatePath: resolveProjectPath(projectRoot, input.reference),
      field: input.field
    });
  } catch (error) {
    if (error instanceof HarnessError) {
      throw error;
    }
    throw new HarnessError('INVALID_REQUEST', 400, `${input.field} is not an accessible file`, {
      field: input.field,
      errorCode: 'HEADLESS_RUNNER_INPUT_REF_INVALID'
    });
  }
  const fileStat = await stat(filePath);
  if (!fileStat.isFile()) {
    throw new HarnessError('INVALID_REQUEST', 400, `${input.field} must reference a regular file`, {
      field: input.field
    });
  }
  const content = await readFile(filePath);
  return {
    content,
    evidence: {
      relativePath: path.relative(projectRoot, filePath),
      sha256: createHash('sha256').update(content).digest('hex'),
      byteLength: content.byteLength
    }
  };
}

async function readProjectJsonReference(input: {
  projectRoot: string;
  reference: string;
  field: string;
}): Promise<{
  field: string;
  path: string;
  relativePath: string;
  sha256: string;
  byteLength: number;
  json: Record<string, unknown>;
}> {
  const { content, evidence } = await readProjectTextReference(input);
  let parsed: unknown;
  try {
    parsed = JSON.parse(content);
  } catch (error) {
    throw new HarnessError(
      'INVALID_REQUEST',
      400,
      `${input.field} must reference a JSON document`,
      {
        field: input.field,
        path: evidence.path,
        error: error instanceof Error ? error.message : String(error)
      }
    );
  }

  return {
    field: input.field,
    ...evidence,
    json: summarizeJsonValue(parsed)
  };
}

async function readRegisteredDomainProfile(input: {
  projectRoot: string;
  profileId: string;
  toolId: DomainReadToolId;
}): Promise<{
  evidence: {
    path: string;
    relativePath: string;
    sha256: string;
    byteLength: number;
  };
  entry: DomainEngineProfileRegistryEntry;
}> {
  const entry = resolveDomainEngineProfile(input.profileId);

  const { content, evidence } = await readProjectTextReference({
    projectRoot: input.projectRoot,
    reference: entry.profileRelativePath,
    field: 'profileId'
  });
  if (!content.includes(entry.identityMarker)) {
    throw new HarnessError(
      'INVALID_REQUEST',
      400,
      'profile file does not match the registered profileId',
      {
        profileId: input.profileId,
        profilePath: evidence.path
      }
    );
  }
  const gate = entry.toolGate[input.toolId];
  if (gate.requiredMarker !== null && !content.includes(gate.requiredMarker)) {
    throw new HarnessError(
      'INVALID_REQUEST',
      400,
      'profileId does not expose the requested deterministic tool',
      {
        profileId: input.profileId,
        toolId: input.toolId,
        profilePath: evidence.path
      }
    );
  }
  return { evidence, entry };
}

function domainReadTransportStatus(
  entry: DomainEngineProfileRegistryEntry,
  toolId: DomainReadToolId
) {
  return {
    status: 'live',
    posture: entry.transportStatus.posture,
    tranche: entry.transportStatus.tranche,
    toolId,
    writes: false,
    network: false,
    shell: false,
    engineKind: entry.engineKind,
    readTransportBinding: entry.readTransportBinding,
    declaredDeterministicToolId: entry.toolGate[toolId].declaredDeterministicToolId,
    inputContract: entry.transportStatus.inputContract,
    deterministicToolExecution: entry.transportStatus.deterministicToolExecution,
    resultSemantics: entry.transportStatus.resultSemantics
  };
}

export async function statusReadTool(
  context: ChiralityReadMcpContext,
  args: StatusReadArgs
): Promise<CallToolResult> {
  return runReadMcpToolWithEvidence({
    context,
    toolName: 'status_read',
    args,
    execute: async () =>
      jsonToolResult(await readDeliverableStatus(context.projectRoot, args.deliverablePath))
  });
}

export async function dependenciesReadTool(
  context: ChiralityReadMcpContext,
  args: DependenciesReadArgs
): Promise<CallToolResult> {
  return runReadMcpToolWithEvidence({
    context,
    toolName: 'deps_read',
    args,
    execute: async () =>
      jsonToolResult(await readDeliverableDependencies(context.projectRoot, args.deliverablePath))
  });
}

export async function scopeScanTool(
  context: ChiralityReadMcpContext,
  _args: ScopeScanArgs = {}
): Promise<CallToolResult> {
  return runReadMcpToolWithEvidence({
    context,
    toolName: 'scope_scan',
    args: _args,
    execute: async () => {
      const projectRoot = await normalizeProjectRoot(context.projectRoot);
      return jsonToolResult({
        projectRoot,
        scannedAt: new Date().toISOString(),
        ...(await scanProjectScopes(projectRoot))
      });
    }
  });
}

export async function scaffoldPreviewTool(
  context: ChiralityReadMcpContext,
  args: ScaffoldPreviewArgs
): Promise<CallToolResult> {
  return runReadMcpToolWithEvidence({
    context,
    toolName: 'scaffold_preview',
    args,
    execute: async () => {
      const executionRoot = assertLexicallyWithinProjectRoot({
        projectRoot: context.projectRoot,
        candidatePath: args.executionRoot,
        field: 'executionRoot'
      });
      const decompositionPath = await assertExistingPathWithinProjectRoot({
        projectRoot: context.projectRoot,
        candidatePath: args.decompositionPath,
        field: 'decompositionPath'
      });

      return jsonToolResult(
        await previewScaffoldExecutionRoot({
          executionRoot,
          decompositionPath,
          projectName: args.projectName,
          coordinationMode: args.coordinationMode as CoordinationMode | undefined
        })
      );
    }
  });
}

export async function domainCompletenessCheckTool(
  context: ChiralityReadMcpContext,
  args: DomainCompletenessCheckArgs
): Promise<CallToolResult> {
  return runReadMcpToolWithEvidence({
    context,
    toolName: 'domain_completeness_check',
    args,
    execute: async () => {
      const { evidence: profile, entry } = await readRegisteredDomainProfile({
        projectRoot: context.projectRoot,
        profileId: args.profileId,
        toolId: 'completeness_checker'
      });
      const input = await readProjectJsonReference({
        projectRoot: context.projectRoot,
        reference: args.inputRef,
        field: 'inputRef'
      });

      return jsonToolResult({
        profileId: args.profileId,
        toolId: 'completeness_checker',
        transportStatus: domainReadTransportStatus(entry, 'completeness_checker'),
        profile,
        inputs: [input]
      });
    }
  });
}

export async function domainRuleCheckRunTool(
  context: ChiralityReadMcpContext,
  args: DomainRuleCheckRunArgs
): Promise<CallToolResult> {
  return runReadMcpToolWithEvidence({
    context,
    toolName: 'domain_rule_check_run',
    args,
    execute: async () => {
      const { evidence: profile, entry } = await readRegisteredDomainProfile({
        projectRoot: context.projectRoot,
        profileId: args.profileId,
        toolId: 'rule_check_runner'
      });
      const rulePack = await readProjectJsonReference({
        projectRoot: context.projectRoot,
        reference: args.rulePackRef,
        field: 'rulePackRef'
      });
      const valueBindings = await readProjectJsonReference({
        projectRoot: context.projectRoot,
        reference: args.valueBindingsRef,
        field: 'valueBindingsRef'
      });

      return jsonToolResult({
        profileId: args.profileId,
        toolId: 'rule_check_runner',
        transportStatus: domainReadTransportStatus(entry, 'rule_check_runner'),
        profile,
        inputs: [rulePack, valueBindings]
      });
    }
  });
}

export async function domainHeadlessPreviewRunTool(
  context: ChiralityReadMcpContext,
  args: DomainHeadlessPreviewRunArgs
): Promise<CallToolResult> {
  return runReadMcpToolWithEvidence({
    context,
    toolName: 'domain_headless_preview_run',
    args,
    execute: async () => {
      if (!args || typeof args.runnerInputRef !== 'string' || !args.runnerInputRef.trim()) {
        throw new HarnessError('INVALID_REQUEST', 400, 'runnerInputRef is required', {
          errorCode: 'HEADLESS_RUNNER_INPUT_REF_MISSING'
        });
      }
      await assertReadMcpPermission({
        context,
        toolName: 'domain_headless_preview_run',
        args
      });
      if (args.profileId !== 'open_pipe_stress') {
        throw new HarnessError(
          'INVALID_REQUEST',
          400,
          'domain_headless_preview_run supports only profileId open_pipe_stress',
          {
            errorCode: 'HEADLESS_RUNNER_PROFILE_REFUSED',
            profileId: args.profileId || '(missing)'
          }
        );
      }
      await readRegisteredDomainProfile({
        projectRoot: context.projectRoot,
        profileId: args.profileId,
        toolId: 'headless_runner'
      });
      const runnerInput = await readProjectBinaryReference({
        projectRoot: context.projectRoot,
        reference: args.runnerInputRef,
        field: 'runnerInputRef'
      });
      const runner = await runConfiguredHeadlessPreview({
        requestBytes: runnerInput.content
      });
      const value = {
        profileId: args.profileId,
        toolId: 'headless_runner',
        transportStatus: {
          status: runner.exitCode === 0 ? 'completed' : 'blocking',
          policyRef: 'DEC-065',
          transport: 'configured-local-process',
          executableIdentity: 'caller-configured absolute realpath plus pinned SHA-256',
          command: 'solve',
          stdin: 'exact validated runnerInputRef bytes',
          stdout: 'sole structured result channel',
          stderr: 'bounded and never model-visible',
          writes: false,
          network: false,
          daemon: false,
          telemetry: false,
          exitCode: runner.exitCode
        },
        inputEvidence: runnerInput.evidence,
        result: runner.result
      };
      return {
        ...jsonToolResult(value),
        ...(runner.exitCode === 1 ? { isError: true } : {})
      };
    }
  });
}

export async function statusTransitionTool(
  context: ChiralityMutatingMcpContext,
  args: StatusTransitionArgs
): Promise<CallToolResult> {
  const deliverablePath = resolveProjectPath(context.projectRoot, args.deliverablePath);
  const statusFilePath = path.join(deliverablePath, '_STATUS.md');

  return runMutatingMcpToolWithEvidence({
    context,
    toolName: 'status_transition',
    args,
    targetFilePath: statusFilePath,
    execute: async () => {
      const transitioned = await transitionDeliverableStatus({
        projectRoot: context.projectRoot,
        deliverablePath,
        targetState: args.targetState,
        actor: args.actor,
        date: args.date,
        approvalSha: args.approvalSha,
        metadata: args.metadata
      });
      const summary = {
        ok: true,
        projectRoot: transitioned.projectRoot,
        deliverablePath: transitioned.deliverablePath,
        statusFilePath: transitioned.statusFilePath,
        transition: transitioned.transition,
        status: {
          currentState: transitioned.status.currentState,
          lastUpdated: transitioned.status.lastUpdated,
          historyLength: transitioned.status.history.length
        }
      };
      return {
        result: jsonToolResult(summary),
        resultSummary: summary
      };
    }
  });
}

export async function dependenciesWriteTool(
  context: ChiralityMutatingMcpContext,
  args: DependenciesWriteArgs
): Promise<CallToolResult> {
  const deliverablePath = resolveProjectPath(context.projectRoot, args.deliverablePath);
  const dependenciesFilePath = path.join(deliverablePath, 'Dependencies.csv');

  return runMutatingMcpToolWithEvidence({
    context,
    toolName: 'deps_write',
    args,
    targetFilePath: dependenciesFilePath,
    execute: async () => {
      const written = await writeDeliverableDependencies({
        projectRoot: context.projectRoot,
        deliverablePath,
        rows: args.rows
      });
      const summary = {
        ok: true,
        projectRoot: written.projectRoot,
        deliverablePath: written.deliverablePath,
        dependenciesFilePath: written.dependenciesFilePath,
        rowCount: written.rows.length,
        warningCount: written.warnings.length,
        warnings: written.warnings
      };
      return {
        result: jsonToolResult(summary),
        resultSummary: summary
      };
    }
  });
}

export function createChiralityReadMcpServer(
  context: ChiralityReadMcpContext
): McpSdkServerConfigWithInstance {
  return createSdkMcpServer({
    name: CHIRALITY_MCP_SERVER_NAME,
    version: CHIRALITY_MCP_SERVER_VERSION,
    instructions:
      'Chirality read-only MCP tools expose project status, dependency, scope, and scaffold-preview data. They do not write files, run shell commands, or access networks (the D-APP-52 pec domain proposal tools, which use a loopback-only HTTP transport, are not part of this read-only server).',
    tools: [
      tool(
        'status_read',
        'Read parsed lifecycle state from a deliverable _STATUS.md file.',
        {
          deliverablePath: z.string().min(1)
        },
        (args) => statusReadTool(context, args)
      ),
      tool(
        'deps_read',
        'Read parsed dependency rows and warnings from a deliverable Dependencies.csv file, or explicit absence status when only _DEPENDENCIES.md is available.',
        {
          deliverablePath: z.string().min(1)
        },
        (args) => dependenciesReadTool(context, args)
      ),
      tool(
        'scope_scan',
        'Scan project-root deliverable and knowledge-type scopes without reading document bodies.',
        {},
        (args) => scopeScanTool(context, args)
      ),
      tool(
        'scaffold_preview',
        'Preview execution-root scaffold paths from a decomposition markdown file without writing files.',
        {
          executionRoot: z.string().min(1),
          decompositionPath: z.string().min(1),
          projectName: z.string().optional(),
          coordinationMode: z.string().optional()
        },
        (args) => scaffoldPreviewTool(context, args)
      )
    ]
  });
}

export function buildChiralityMcpTools(input: {
  context: ChiralityReadMcpContext;
  mode?: string;
  allowedToolNames: readonly string[];
}): SdkMcpToolDefinition<any>[] {
  const allowed = new Set(input.allowedToolNames);
  const tools: SdkMcpToolDefinition<any>[] = [];

  if (allowed.has('mcp__chirality__status_read')) {
    tools.push(
      tool(
        'status_read',
        'Read parsed lifecycle state from a deliverable _STATUS.md file.',
        {
          deliverablePath: z.string().min(1)
        },
        (args) => statusReadTool(input.context, args)
      )
    );
  }

  if (allowed.has('mcp__chirality__deps_read')) {
    tools.push(
      tool(
        'deps_read',
        'Read parsed dependency rows and warnings from a deliverable Dependencies.csv file.',
        {
          deliverablePath: z.string().min(1)
        },
        (args) => dependenciesReadTool(input.context, args)
      )
    );
  }

  if (allowed.has('mcp__chirality__scope_scan')) {
    tools.push(
      tool(
        'scope_scan',
        'Scan project-root deliverable and knowledge-type scopes without reading document bodies.',
        {},
        (args) => scopeScanTool(input.context, args)
      )
    );
  }

  if (allowed.has('mcp__chirality__scaffold_preview')) {
    tools.push(
      tool(
        'scaffold_preview',
        'Preview execution-root scaffold paths from a decomposition markdown file without writing files.',
        {
          executionRoot: z.string().min(1),
          decompositionPath: z.string().min(1),
          projectName: z.string().optional(),
          coordinationMode: z.string().optional()
        },
        (args) => scaffoldPreviewTool(input.context, args)
      )
    );
  }

  tools.push(...buildCoordinationMcpTools({
    context: {
      projectRoot: input.context.projectRoot,
      sessionId: input.context.sessionId,
      persona: input.context.persona ?? '',
      mode: input.mode ?? input.context.mode ?? 'readOnly',
      tools: input.context.tools ?? []
    },
    allowedToolNames: allowed
  }));

  const mutatingContext: ChiralityMutatingMcpContext = {
    ...input.context,
    mode: input.mode ?? 'readOnly'
  };

  if (allowed.has('mcp__chirality__status_transition')) {
    tools.push(
      tool(
        'status_transition',
        'Apply a governed lifecycle transition to a deliverable _STATUS.md file.',
        {
          deliverablePath: z.string().min(1),
          targetState: z.string().min(1),
          actor: z.string().min(1),
          date: z.string().optional(),
          approvalSha: z.string().optional(),
          metadata: z.record(z.string(), z.string()).optional()
        },
        (args) => statusTransitionTool(mutatingContext, args)
      )
    );
  }

  if (allowed.has('mcp__chirality__deps_write')) {
    tools.push(
      tool(
        'deps_write',
        'Write a governed Dependencies.csv register using v3.1 dependency writer semantics.',
        {
          deliverablePath: z.string().min(1),
          rows: z.array(z.record(z.string(), z.string()))
        },
        (args) =>
          dependenciesWriteTool(mutatingContext, {
            deliverablePath: args.deliverablePath,
            rows: args.rows as DependencyRegisterRow[]
          })
      )
    );
  }

  if (allowed.has('mcp__chirality__domain_completeness_check')) {
    tools.push(
      tool(
        'domain_completeness_check',
        'Return registry-gated read-side domain transport evidence (D-APP-50 tranche-1 open_pipe_stress; D-APP-51 P1 pec) for the completeness_checker wrapper.',
        {
          profileId: z.string().min(1),
          inputRef: z.string().min(1)
        },
        (args) => domainCompletenessCheckTool(input.context, args)
      )
    );
  }

  if (allowed.has('mcp__chirality__domain_rule_check_run')) {
    tools.push(
      tool(
        'domain_rule_check_run',
        'Return registry-gated read-side domain transport evidence (D-APP-50 tranche-1 open_pipe_stress; D-APP-51 P1 pec) for the rule_check_runner wrapper.',
        {
          profileId: z.string().min(1),
          rulePackRef: z.string().min(1),
          valueBindingsRef: z.string().min(1)
        },
        (args) => domainRuleCheckRunTool(input.context, args)
      )
    );
  }

  if (allowed.has('mcp__chirality__domain_headless_preview_run')) {
    tools.push(
      tool(
        'domain_headless_preview_run',
        'Run one open_pipe_stress DEC-065 solve request through a configured, hash-pinned local openpipestress-runner process. Read-only; no network, apply, proposal, or filesystem output path.',
        {
          profileId: z.literal('open_pipe_stress'),
          runnerInputRef: z.string().min(1)
        },
        (args) => domainHeadlessPreviewRunTool(input.context, args)
      )
    );
  }

  if (allowed.has('mcp__chirality__domain_propose_operation')) {
    tools.push(
      tool(
        'domain_propose_operation',
        'Create (mode propose) or refresh (mode refresh) a pec import-proposal dry-run record over the D-APP-52 loopback-only allowlisted HTTP transport; refresh mutates and voids any prior acceptance. Acceptance and application remain human acts in pec (no apply tool exists).',
        {
          profileId: z.string().min(1),
          projectId: z.number().int().positive(),
          mode: z.enum(['propose', 'refresh']).optional(),
          contract: z.enum(PEC_PROPOSAL_CONTRACTS).optional(),
          csvContent: z.string().optional(),
          csvFileRef: z.string().optional(),
          sourceName: z.string().optional(),
          proposalId: z.number().int().positive().optional(),
          expectedVersion: z.number().int().optional()
        },
        (args) => domainProposeOperationTool(mutatingContext, args as DomainProposeOperationArgs)
      )
    );
  }

  if (allowed.has('mcp__chirality__domain_proposal_validate')) {
    tools.push(
      tool(
        'domain_proposal_validate',
        'Read a pec import-proposal record and its stored dry-run report over the D-APP-52 loopback-only allowlisted HTTP transport; read-only, never recomputes.',
        {
          profileId: z.string().min(1),
          projectId: z.number().int().positive(),
          proposalId: z.number().int().positive()
        },
        (args) => domainProposalValidateTool(input.context, args as DomainProposalValidateArgs)
      )
    );
  }

  return tools;
}

export function createChiralityMcpServers(input: {
  context: ChiralityReadMcpContext;
  allowedToolNames: readonly string[];
  mode?: string;
}): Record<string, McpServerConfig> {
  const allowedToolNames = input.allowedToolNames.filter(isChiralityMcpAllowedToolName);
  const tools = buildChiralityMcpTools({
    context: input.context,
    mode: input.mode,
    allowedToolNames
  });
  if (tools.length === 0) {
    return {};
  }

  return {
    [CHIRALITY_MCP_SERVER_NAME]: createSdkMcpServer({
      name: CHIRALITY_MCP_SERVER_NAME,
      version: CHIRALITY_MCP_SERVER_VERSION,
      instructions:
        'Chirality MCP tools expose explicitly requested local project status, dependency, scope, scaffold-preview, read-only domain transport evidence, and governed write operations. Mutating tools require workspaceWrite mode and handler-level permission/evidence checks. These tools do not run shell commands. domain_headless_preview_run is open_pipe_stress-only and directly spawns one explicitly configured absolute, executable, SHA-256-pinned local openpipestress-runner with argv solve, exact project-contained request bytes on stdin, bounded stdout/stderr, a minimal environment, and no network, output path, proposal, or apply behavior. The two pec domain proposal tools (domain_propose_operation, domain_proposal_validate) use a loopback-only (127.0.0.1) endpoint-allowlisted HTTP transport to the local pec engine seam (D-APP-52); every other tool accesses no network.',
      tools
    })
  };
}

export function createChiralityReadMcpServers(input: {
  context: ChiralityReadMcpContext;
  allowedToolNames: readonly string[];
}): Record<string, McpServerConfig> {
  return createChiralityMcpServers(input);
}

export function filterChiralityMcpAllowedToolNames(
  toolNames: readonly string[]
): ChiralityMcpAllowedToolName[] {
  return toolNames.filter(isChiralityMcpAllowedToolName);
}
