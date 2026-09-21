import type { CallToolResult } from '@modelcontextprotocol/sdk/types.js';
import { createHash } from 'node:crypto';
import { readFile, realpath } from 'node:fs/promises';
import path from 'node:path';
import { HarnessError } from '@chirality/runtime-contracts/errors';
import { getHarnessToolDescriptor } from '@chirality/runtime-contracts/tool-descriptor';
import {
  toChiralityMcpAllowedToolName,
  type ChiralityMcpDomainToolName
} from '@chirality/runtime-contracts/mcp/tool-names';
import { createHarnessEvent } from '../event-factory';
import { appendHarnessEvent } from '../session-events';
import {
  appendHarnessPermissionDecisionEvent,
  resolveHarnessPermissionDecision
} from '../permission-overlay';
import {
  summarizeToolDescriptor,
  summarizeToolError,
  summarizeToolInput,
  summarizeToolResult,
  withToolResultPersistence
} from '../tool-evidence';
import { persistToolResultArtifact } from '../tool-result-artifacts';
import {
  resolveDomainEngineProfile,
  type DomainEngineProfileRegistryEntry
} from './domain-profile-registry';
import {
  PecBridgeClient,
  PecBridgeError,
  resolvePecBridgeConfig
} from './pec-bridge-client';

/**
 * D-APP-52 live pec proposal tool handlers (bridge-lane P2).
 *
 * First live exposure of the already-registered `domain_propose_operation`
 * (propose + refresh) and `domain_proposal_validate` (read-only get) names,
 * scoped to the D-APP-51 registry's `pec` entry: the pec HTTP client is
 * reachable ONLY for a registered profile whose entry declares the pec
 * loopback HTTP binding (`engineKind: 'http-api'`) — structurally unreachable
 * under any other profileId. Acceptance, application, rejection-of-others, and
 * `force` are not implemented here, not registered anywhere, and not reachable
 * from any code path this module adds (packet rider 5; K-DOMAIN-3).
 */

export type DomainProposalToolContext = {
  projectRoot: string;
  sessionId: string;
};

export type DomainProposalMutatingToolContext = DomainProposalToolContext & {
  mode: string;
};

export type DomainProposeOperationArgs = {
  profileId: string;
  projectId: number;
  /** default 'propose'; 'refresh' mutates and voids any prior acceptance. */
  mode?: 'propose' | 'refresh';
  contract?: string;
  csvContent?: string;
  csvFileRef?: string;
  sourceName?: string;
  proposalId?: number;
  expectedVersion?: number;
};

export type DomainProposalValidateArgs = {
  profileId: string;
  projectId: number;
  proposalId: number;
};

/** The structural client seam; the runtime default is the loopback PecBridgeClient. */
export type PecProposalTransportClient = {
  login(): Promise<void>;
  createProposal(
    projectId: number,
    contract: string,
    csv: string,
    sourceName?: string
  ): Promise<unknown>;
  refreshProposal(
    projectId: number,
    proposalId: number,
    expectedVersion: number
  ): Promise<unknown>;
  getProposal(projectId: number, proposalId: number): Promise<unknown>;
  endpointDescriptor(): { host: '127.0.0.1'; port: number };
  dispose(): void;
};

export type DomainProposalToolOverrides = {
  createClient?: () => PecProposalTransportClient;
};

export const PEC_PROPOSAL_CONTRACTS = ['mdl', 'rail', 'decisions', 'risks', 'schedule'] as const;

const PEC_PROPOSAL_RESULT_SEMANTICS =
  'transport/evidence envelope only; no domain verdict; a green dry-run is NOT acceptance — acceptance and application are human acts in pec behind admin-only RBAC (K-DOMAIN-3/K-DOMAIN-4)';
const PEC_TRANSPORT_POSTURE = 'D-T0-19 O-2A loopback HTTP transport (bridge P2, D-APP-52)';
const PEC_TRANSPORT_ACTOR_MODEL =
  'owner-provisioned pec agent person (is_admin=0, import.propose grant); credentials from local environment, never in results';
const PEC_TRANSPORT_NETWORK =
  'loopback-only; endpoint allowlist: login, propose, refresh, get-proposal';
const PEC_TRANSPORT_ORIGIN_HEADER =
  'none (RV-21 permits header-less programmatic clients; recorded, not hidden)';

function defaultCreateClient(): PecProposalTransportClient {
  return new PecBridgeClient(resolvePecBridgeConfig());
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

function asRecord(value: unknown): Record<string, unknown> | undefined {
  return Boolean(value) && typeof value === 'object' && !Array.isArray(value)
    ? (value as Record<string, unknown>)
    : undefined;
}

/**
 * Registry gate: the pec transport handlers refuse every profileId whose
 * registry entry does not declare the pec HTTP binding. `open_pipe_stress`
 * (deterministic-cli) and unregistered ids are structurally unable to reach
 * the pec client.
 */
function resolvePecTransportProfile(profileId: string): DomainEngineProfileRegistryEntry {
  const entry = resolveDomainEngineProfile(profileId);
  if (entry.engineKind !== 'http-api') {
    throw new HarnessError(
      'INVALID_REQUEST',
      400,
      'profileId is not registered for the pec loopback HTTP proposal transport',
      {
        profileId,
        engineKind: entry.engineKind,
        requiredEngineKind: 'http-api'
      }
    );
  }
  return entry;
}

function assertPositiveInteger(value: unknown, field: string): number {
  if (typeof value !== 'number' || !Number.isInteger(value) || value <= 0) {
    throw new HarnessError('INVALID_REQUEST', 400, `${field} must be a positive integer`, {
      [field]: value
    });
  }
  return value;
}

function pecTransportStatus(input: {
  client: PecProposalTransportClient;
  method: 'GET' | 'POST';
  path: string;
}): Record<string, unknown> {
  const endpoint = input.client.endpointDescriptor();
  return {
    status: 'live',
    posture: PEC_TRANSPORT_POSTURE,
    endpoint: {
      host: endpoint.host,
      port: endpoint.port,
      method: input.method,
      path: input.path
    },
    actorModel: PEC_TRANSPORT_ACTOR_MODEL,
    network: PEC_TRANSPORT_NETWORK,
    filesystemWrites: false,
    shell: false,
    originHeader: PEC_TRANSPORT_ORIGIN_HEADER
  };
}

/** Safe field picks from the engine proposal record for evidence summaries. */
function summarizeEngineProposal(engine: unknown): Record<string, unknown> {
  const record = asRecord(engine);
  if (!record) {
    return {};
  }
  const picked: Record<string, unknown> = {};
  for (const field of [
    'id',
    'ref',
    'state',
    'version',
    'sourceSha256',
    'dryRunAt',
    'basisHistoryId'
  ]) {
    if (field in record) {
      picked[field] = record[field];
    }
  }
  return picked;
}

/**
 * PecBridgeError → structured tool result: the taxonomy is the point, so it
 * reaches the model as an `ok: false` result (409 STALE_PROPOSAL as normal
 * flow), never as a tool crash. tool.failed stays reserved for harness-side
 * faults (bad args, refused profile, refused permission).
 */
function pecTaxonomyResult(input: {
  error: PecBridgeError;
  profileId: string;
  toolId: ChiralityMcpDomainToolName;
  mode?: 'propose' | 'refresh';
  transportStatus: Record<string, unknown>;
}): { result: CallToolResult; resultSummary: Record<string, unknown> } {
  const payload = {
    ok: false,
    profileId: input.profileId,
    toolId: input.toolId,
    ...(input.mode ? { mode: input.mode } : {}),
    errorClass: input.error.errorClass,
    status: input.error.status,
    engineError: input.error.engineError,
    normalFlow: input.error.normalFlow,
    guidance: input.error.guidance,
    message: input.error.message,
    transportStatus: input.transportStatus,
    resultSemantics: PEC_PROPOSAL_RESULT_SEMANTICS
  };
  return {
    result: jsonToolResult(payload),
    resultSummary: {
      ok: false,
      errorClass: input.error.errorClass,
      status: input.error.status,
      normalFlow: input.error.normalFlow
    }
  };
}

async function assertExistingPathWithinProjectRoot(input: {
  projectRoot: string;
  candidatePath: string;
  field: string;
}): Promise<string> {
  const projectRoot = await realpath(path.resolve(input.projectRoot));
  const candidatePath = await realpath(
    path.isAbsolute(input.candidatePath)
      ? path.resolve(input.candidatePath)
      : path.resolve(projectRoot, input.candidatePath)
  );
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

async function resolvePecProposalCsv(
  context: DomainProposalToolContext,
  args: DomainProposeOperationArgs
): Promise<{ content: string; inputEvidence: Record<string, unknown> }> {
  const hasInline = typeof args.csvContent === 'string';
  const hasFileRef = typeof args.csvFileRef === 'string' && args.csvFileRef.length > 0;
  if (hasInline === hasFileRef) {
    throw new HarnessError(
      'INVALID_REQUEST',
      400,
      'propose mode requires exactly one of csvContent or csvFileRef',
      {
        csvContentProvided: hasInline,
        csvFileRefProvided: hasFileRef
      }
    );
  }

  if (hasInline) {
    const content = args.csvContent as string;
    return {
      content,
      inputEvidence: {
        source: 'inline',
        sha256: createHash('sha256').update(content).digest('hex'),
        byteLength: Buffer.byteLength(content, 'utf8')
      }
    };
  }

  const projectRoot = await realpath(path.resolve(context.projectRoot));
  const filePath = await assertExistingPathWithinProjectRoot({
    projectRoot,
    candidatePath: args.csvFileRef as string,
    field: 'csvFileRef'
  });
  const content = await readFile(filePath, 'utf8');
  return {
    content,
    inputEvidence: {
      source: 'fileRef',
      relativePath: path.relative(projectRoot, filePath),
      sha256: createHash('sha256').update(content).digest('hex'),
      byteLength: Buffer.byteLength(content, 'utf8')
    }
  };
}

async function runPecDomainToolWithEvidence(input: {
  sessionId: string;
  toolName: ChiralityMcpDomainToolName;
  args: unknown;
  assertPermission?: () => Promise<Record<string, unknown>>;
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
      sessionId: input.sessionId,
      type: 'tool.started',
      data: {
        ...eventBase,
        inputMetadata: summarizeToolInput(input.args)
      }
    })
  );

  try {
    const permissionMetadata = input.assertPermission ? await input.assertPermission() : undefined;
    const { result, resultSummary } = await input.execute();
    const artifactMetadata = await persistToolResultArtifact({
      sessionId: input.sessionId,
      toolUseId: `${input.toolName}-${startedAt}`,
      toolName: adapterToolName,
      descriptor,
      result
    });
    await appendHarnessEvent(
      createHarnessEvent({
        sessionId: input.sessionId,
        type: 'tool.completed',
        data: {
          ...eventBase,
          durationMs: Date.now() - startedAt,
          ...(permissionMetadata ? { permissionMetadata } : {}),
          resultSummary,
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
          sessionId: input.sessionId,
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

async function assertPecProposalWritePermission(input: {
  context: DomainProposalMutatingToolContext;
  args: unknown;
}): Promise<Record<string, unknown>> {
  const descriptor = getHarnessToolDescriptor('domain_propose_operation');
  const decision = resolveHarnessPermissionDecision({
    sessionId: input.context.sessionId,
    mode: input.context.mode,
    toolName: toChiralityMcpAllowedToolName('domain_propose_operation'),
    descriptor,
    source: 'chirality-policy',
    toolInput: asRecord(input.args),
    safeMetadata: {
      inputMetadata: summarizeToolInput(input.args)
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
    decisionId: decision.decisionId
  };
}

export async function domainProposeOperationTool(
  context: DomainProposalMutatingToolContext,
  args: DomainProposeOperationArgs,
  overrides?: DomainProposalToolOverrides
): Promise<CallToolResult> {
  return runPecDomainToolWithEvidence({
    sessionId: context.sessionId,
    toolName: 'domain_propose_operation',
    args,
    assertPermission: () => assertPecProposalWritePermission({ context, args }),
    execute: async () => {
      resolvePecTransportProfile(args.profileId);
      const projectId = assertPositiveInteger(args.projectId, 'projectId');
      const mode = args.mode ?? 'propose';
      if (mode !== 'propose' && mode !== 'refresh') {
        throw new HarnessError('INVALID_REQUEST', 400, "mode must be 'propose' or 'refresh'", {
          mode: args.mode
        });
      }

      if (mode === 'refresh') {
        const proposalId = assertPositiveInteger(args.proposalId, 'proposalId');
        if (typeof args.expectedVersion !== 'number' || !Number.isInteger(args.expectedVersion)) {
          throw new HarnessError(
            'INVALID_REQUEST',
            400,
            'refresh mode requires expectedVersion (the integer version the agent last read)',
            {
              expectedVersion: args.expectedVersion
            }
          );
        }
        const requestPath = `/api/projects/${projectId}/import-proposals/${proposalId}/refresh`;
        const client = (overrides?.createClient ?? defaultCreateClient)();
        try {
          const transportStatus = pecTransportStatus({
            client,
            method: 'POST',
            path: requestPath
          });
          try {
            const engine = await client.refreshProposal(
              projectId,
              proposalId,
              args.expectedVersion
            );
            const summary = summarizeEngineProposal(engine);
            return {
              result: jsonToolResult({
                ok: true,
                profileId: args.profileId,
                toolId: 'domain_propose_operation',
                mode,
                transportStatus,
                inputs: {
                  proposalId,
                  expectedVersion: args.expectedVersion
                },
                engine,
                resultSemantics: PEC_PROPOSAL_RESULT_SEMANTICS
              }),
              resultSummary: { ok: true, mode, ...summary }
            };
          } catch (error) {
            if (error instanceof PecBridgeError) {
              return pecTaxonomyResult({
                error,
                profileId: args.profileId,
                toolId: 'domain_propose_operation',
                mode,
                transportStatus
              });
            }
            throw error;
          }
        } finally {
          client.dispose();
        }
      }

      if (
        typeof args.contract !== 'string' ||
        !(PEC_PROPOSAL_CONTRACTS as readonly string[]).includes(args.contract)
      ) {
        throw new HarnessError(
          'INVALID_REQUEST',
          400,
          `propose mode requires contract ∈ {${PEC_PROPOSAL_CONTRACTS.join(', ')}}`,
          {
            contract: args.contract
          }
        );
      }
      const csv = await resolvePecProposalCsv(context, args);
      const requestPath = `/api/projects/${projectId}/import-proposals`;
      const client = (overrides?.createClient ?? defaultCreateClient)();
      try {
        const transportStatus = pecTransportStatus({
          client,
          method: 'POST',
          path: requestPath
        });
        try {
          const engine = await client.createProposal(
            projectId,
            args.contract,
            csv.content,
            args.sourceName
          );
          const summary = summarizeEngineProposal(engine);
          return {
            result: jsonToolResult({
              ok: true,
              profileId: args.profileId,
              toolId: 'domain_propose_operation',
              mode,
              transportStatus,
              inputs: {
                contract: args.contract,
                ...(args.sourceName !== undefined ? { sourceName: args.sourceName } : {}),
                csv: csv.inputEvidence
              },
              engine,
              resultSemantics: PEC_PROPOSAL_RESULT_SEMANTICS
            }),
            resultSummary: { ok: true, mode, ...summary }
          };
        } catch (error) {
          if (error instanceof PecBridgeError) {
            return pecTaxonomyResult({
              error,
              profileId: args.profileId,
              toolId: 'domain_propose_operation',
              mode,
              transportStatus
            });
          }
          throw error;
        }
      } finally {
        client.dispose();
      }
    }
  });
}

/**
 * Read-grade handler: resolves the pec registry entry and issues exactly one
 * GET (client.getProposal). No propose/refresh/accept/apply-capable call
 * exists on any code path in this function (packet rider 7; test-pinned).
 */
export async function domainProposalValidateTool(
  context: DomainProposalToolContext,
  args: DomainProposalValidateArgs,
  overrides?: DomainProposalToolOverrides
): Promise<CallToolResult> {
  return runPecDomainToolWithEvidence({
    sessionId: context.sessionId,
    toolName: 'domain_proposal_validate',
    args,
    execute: async () => {
      resolvePecTransportProfile(args.profileId);
      const projectId = assertPositiveInteger(args.projectId, 'projectId');
      const proposalId = assertPositiveInteger(args.proposalId, 'proposalId');
      const requestPath = `/api/projects/${projectId}/import-proposals/${proposalId}`;
      const client = (overrides?.createClient ?? defaultCreateClient)();
      try {
        const transportStatus = pecTransportStatus({
          client,
          method: 'GET',
          path: requestPath
        });
        try {
          const engine = await client.getProposal(projectId, proposalId);
          const summary = summarizeEngineProposal(engine);
          return {
            result: jsonToolResult({
              ok: true,
              profileId: args.profileId,
              toolId: 'domain_proposal_validate',
              transportStatus,
              engine,
              resultSemantics: PEC_PROPOSAL_RESULT_SEMANTICS
            }),
            resultSummary: { ok: true, ...summary }
          };
        } catch (error) {
          if (error instanceof PecBridgeError) {
            return pecTaxonomyResult({
              error,
              profileId: args.profileId,
              toolId: 'domain_proposal_validate',
              transportStatus
            });
          }
          throw error;
        }
      } finally {
        client.dispose();
      }
    }
  });
}
