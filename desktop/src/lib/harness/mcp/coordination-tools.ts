import {
  tool,
  type SdkMcpToolDefinition
} from '@anthropic-ai/claude-agent-sdk';
import type { CallToolResult } from '@modelcontextprotocol/sdk/types.js';
import { z } from 'zod/v4';
import { readFile, readdir, writeFile } from 'node:fs/promises';
import path from 'node:path';
import type { SessionRecord } from '@chirality/runtime-contracts/types';
import {
  acknowledgeAgentUpdate,
  assertValidManagedChildReturn,
  ManagedDelegationService,
  refreshOrchestrationHandoff,
  reportCoordinationNotice,
  sendAgentUpdate,
  type DelegateAgentInput,
  type ManagedChildLaunch
} from '../managed-delegation';
import { parseAgentType, readAgentInstruction } from '../agent-instruction';

export type CoordinationMcpContext = {
  projectRoot: string;
  sessionId: string;
  persona: string;
  mode: string;
  tools: readonly string[];
};

function jsonResult(value: unknown): CallToolResult {
  return { content: [{ type: 'text', text: JSON.stringify(value, null, 2) }] };
}

async function parentSession(context: CoordinationMcpContext): Promise<SessionRecord> {
  const { getHarnessRuntime } = await import('../runtime');
  return getHarnessRuntime().sessionManager.getById(context.sessionId);
}

export async function launchManagedChild(input: ManagedChildLaunch) {
  const { getHarnessRuntime } = await import('../runtime');
  const runtime = getHarnessRuntime();
  const parentInstruction = await readAgentInstruction(input.parent.persona);
  const parentAgentType = parseAgentType(parentInstruction.content);
  if (parentAgentType !== 0 && parentAgentType !== 1) {
    throw new Error('Managed parent must be Agent 0 or Agent 1');
  }
  const child = await runtime.sessionManager.create({
    projectRoot: input.parent.projectRoot,
    persona: input.childPersona,
    mode: input.parent.mode
  });
  await runtime.sessionManager.save(child.sessionId, {
    orchestrationRunId: input.runId,
    executionRoot: input.parent.executionRoot ?? 'execution',
    agentInstanceId: input.childInstanceId,
    parentSessionId: input.parent.sessionId,
    parentInstanceId: input.parent.agentInstanceId,
    parentAgentType,
    agentType: input.childAgentType,
    childKind: input.childKind,
    planVersion: input.parent.planVersion,
    approvalRef: input.approvalRef,
    instructionPath: input.instructionPath,
    instructionHash: input.instructionHash,
    briefHash: input.briefHash,
    declaredContext: input.declaredContext,
    declaredTools: input.tools,
    engineSelection: input.engineSelection,
    allowedWriteTargets: input.writeTargets,
    childRunStatus: 'RUNNING'
  });

  const instanceRoot = path.join(
    input.parent.projectRoot,
    input.parent.executionRoot ?? 'execution',
    '_Coordination',
    'AgentRuns',
    input.runId,
    'instances',
    input.childInstanceId
  );
  const runRoot = path.dirname(path.dirname(instanceRoot));
  const runningStatus = JSON.parse(
    await readFile(path.join(instanceRoot, 'STATUS.json'), 'utf8')
  ) as Record<string, unknown>;
  await writeFile(
    path.join(instanceRoot, 'STATUS.json'),
    `${JSON.stringify({
      ...runningStatus,
      childSessionId: child.sessionId,
      engineSelection: input.engineSelection,
      status: 'RUNNING'
    }, null, 2)}\n`,
    'utf8'
  );

  const readUndeliveredUpdates = async (delivered: ReadonlySet<string>) => {
    let names: string[] = [];
    try {
      names = await readdir(path.join(runRoot, 'updates'));
    } catch {
      return [];
    }
    const updates: Array<Record<string, unknown> & { updateId: string }> = [];
    for (const name of names.sort()) {
      if (!name.endsWith('.json')) continue;
      try {
        const update = JSON.parse(
          await readFile(path.join(runRoot, 'updates', name), 'utf8')
        ) as Record<string, unknown>;
        const updateId = typeof update.updateId === 'string' ? update.updateId : '';
        if (
          updateId &&
          update.childInstanceId === input.childInstanceId &&
          !delivered.has(updateId)
        ) {
          updates.push({ ...update, updateId });
        }
      } catch {
        // A malformed update is not delivered; the parent-side record remains evidence.
      }
    }
    return updates;
  };

  const execute = async () => {
    const outputs: string[] = [];
    let failed = false;
    let blocked = false;
    const runChildTurn = async (message: string) => {
      let turnOutput = '';
      const turn = await runtime.turnEngine.runTurn({
        sessionId: child.sessionId,
        message,
        attachments: [],
        opts: {
          persona: input.childPersona,
          mode: input.parent.mode,
          tools: input.tools,
          subagentGovernance: {
            contextSealed: true,
            pipelineRunApproved: true,
            approvalRef: input.approvalRef,
            approvedBy: input.parent.persona
          }
        }
      });
      for await (const event of turn.events) {
        if (event.type === 'chat:complete') turnOutput = event.data.text;
        if (event.type === 'turn:error') {
          failed = true;
          turnOutput = turnOutput || event.data.message;
        }
        if (event.type === 'process:exit' && (event.data.exitCode !== 0 || event.data.error)) {
          failed = true;
          turnOutput = turnOutput || event.data.error || `Child exited ${event.data.exitCode}`;
        }
      }
      outputs.push(turnOutput);
    };

    await runChildTurn(input.brief);
    const delivered = new Set<string>();
    for (let cycle = 0; cycle < 8 && !failed; cycle += 1) {
      const updates = await readUndeliveredUpdates(delivered);
      if (updates.length === 0) break;
      updates.forEach((update) => delivered.add(update.updateId));
      await runChildTurn([
        '# Parent Coordination Update',
        '',
        'The following durable updates arrived during your active run. Incorporate them only at this safe turn boundary. Preserve each claim status and call ack_agent_update once for every UpdateID before returning.',
        '',
        ...updates.map((update) => `## UpdateID ${update.updateId}\n\n${JSON.stringify(update, null, 2)}`)
      ].join('\n'));
      for (const update of updates) {
        try {
          await readFile(path.join(runRoot, 'acknowledgments', `${update.updateId}.json`), 'utf8');
        } catch {
          blocked = true;
          outputs.push(`[Managed coordination blocked: update ${update.updateId} was not acknowledged.]`);
        }
      }
      if (blocked) break;
    }
    if (!failed && !blocked) {
      const overflow = await readUndeliveredUpdates(delivered);
      if (overflow.length > 0) {
        blocked = true;
        outputs.push('[Managed coordination blocked: safe-boundary update cycle limit reached.]');
      }
    }
    let output = outputs.filter(Boolean).join('\n\n');
    const status = failed ? 'FAILED' : blocked ? 'BLOCKED' : 'COMPLETED';
    if (status === 'COMPLETED') {
      try {
        assertValidManagedChildReturn(outputs.at(-1) ?? '', input.requiredReturnMarkers);
      } catch (error) {
        failed = true;
        output = `${output.trimEnd()}\n\n[Managed return validation failed: ${error instanceof Error ? error.message : 'invalid return'}]`;
      }
    }
    const validatedStatus = failed ? 'FAILED' : blocked ? 'BLOCKED' : 'COMPLETED';
    await runtime.sessionManager.save(child.sessionId, { childRunStatus: validatedStatus });
    return { sessionId: child.sessionId, status: validatedStatus, output: output || '(child returned no chat output)' } as const;
  };

  if (input.executionMode === 'BACKGROUND') {
    setImmediate(() => {
      void execute()
        .then(async (result) => {
          await writeFile(path.join(instanceRoot, 'RETURN.md'), `${result.output.trimEnd()}\n`, 'utf8');
          const current = JSON.parse(await readFile(path.join(instanceRoot, 'STATUS.json'), 'utf8')) as Record<string, unknown>;
          await writeFile(path.join(instanceRoot, 'STATUS.json'), `${JSON.stringify({ ...current, childSessionId: result.sessionId, status: result.status, outputArtifact: path.join(instanceRoot, 'RETURN.md') }, null, 2)}\n`, 'utf8');
          await refreshOrchestrationHandoff(path.dirname(path.dirname(instanceRoot)));
        })
        .catch(async (error) => {
          try {
            const current = JSON.parse(await readFile(path.join(instanceRoot, 'STATUS.json'), 'utf8')) as Record<string, unknown>;
            await writeFile(path.join(instanceRoot, 'STATUS.json'), `${JSON.stringify({ ...current, childSessionId: child.sessionId, status: 'FAILED', error: error instanceof Error ? error.message : 'background child failed' }, null, 2)}\n`, 'utf8');
            await runtime.sessionManager.save(child.sessionId, { childRunStatus: 'FAILED' });
            await refreshOrchestrationHandoff(path.dirname(path.dirname(instanceRoot)));
          } catch (recordError) {
            console.error('[managed-delegation] failed to record background child failure', recordError);
          }
        });
    });
    return { sessionId: child.sessionId, status: 'RUNNING', output: 'Managed child launched in background.' } as const;
  }

  return execute();
}

const delegateSchema = {
  executionRoot: z.string().min(1),
  runId: z.string().min(1),
  planVersion: z.string().min(1),
  selectionAuthority: z.enum(['HUMAN', 'AGENT_0', 'AGENT_1']),
  posture: z.enum(['TERMINAL_FAN_OUT_IN', 'SUPERVISED_MANY_TO_MANY', 'MIXED']),
  acceptedBasis: z.array(z.string()),
  workGraph: z.record(z.string(), z.unknown()).optional(),
  childKind: z.enum(['named', 'task', 'generalist']),
  agentName: z.string().optional(),
  purpose: z.string().min(1),
  brief: z.string().min(1),
  declaredContext: z.array(z.string()),
  tools: z.array(z.string()),
  engineSelection: z.object({
    adapterId: z.string().min(1),
    providerId: z.string().min(1),
    model: z.string().min(1)
  }).optional(),
  writeTargets: z.array(z.string()),
  dependencies: z.array(z.string()),
  acceptedPredecessors: z.array(z.string()).optional(),
  expectedOutput: z.string().min(1),
  acceptanceCriteria: z.array(z.string()),
  requiredReturnMarkers: z.array(z.string().min(1)).min(1),
  executionMode: z.enum(['WAIT', 'BACKGROUND']).optional(),
  contextSealed: z.boolean(),
  pipelineRunApproved: z.boolean(),
  approvalRef: z.string().min(1)
};

export function buildCoordinationMcpTools(input: {
  context: CoordinationMcpContext;
  allowedToolNames: ReadonlySet<string>;
}): SdkMcpToolDefinition<any>[] {
  const tools: SdkMcpToolDefinition<any>[] = [];
  if (input.allowedToolNames.has('mcp__chirality__delegate_agent')) {
    tools.push(tool(
      'delegate_agent',
      'Launch one governed direct child session and persist its orchestration records.',
      delegateSchema,
      async (args) => {
        const runtimeModule = await import('../runtime');
        const runtime = runtimeModule.getHarnessRuntime();
        const existing = await runtime.sessionManager.getById(input.context.sessionId);
        if (existing.orchestrationRunId && existing.orchestrationRunId !== args.runId) {
          throw new Error('Managed child must remain in the parent orchestration run');
        }
        const parent: SessionRecord = {
          ...existing,
          orchestrationRunId: args.runId,
          executionRoot: args.executionRoot,
          planVersion: args.planVersion,
          declaredTools: [...input.context.tools]
        };
        const service = new ManagedDelegationService(
          launchManagedChild,
          async (validatedParent) => runtime.sessionManager.save(existing.sessionId, {
            orchestrationRunId: validatedParent.orchestrationRunId,
            executionRoot: validatedParent.executionRoot,
            planVersion: validatedParent.planVersion,
            declaredTools: [...input.context.tools]
          })
        );
        return jsonResult(await service.delegate(parent, input.context.tools, args as DelegateAgentInput));
      }
    ));
  }
  if (input.allowedToolNames.has('mcp__chirality__report_coordination_notice')) {
    tools.push(tool(
      'report_coordination_notice',
      'Report a typed coordination notice to the direct parent.',
      {
        noticeType: z.string().min(1),
        claimStatus: z.enum(['PROVISIONAL', 'VALIDATED', 'ACCEPTED', 'DISPUTED']),
        summary: z.string().min(1),
        evidenceRefs: z.array(z.string()),
        affectedScopes: z.array(z.string()),
        requestedAction: z.string().min(1),
        blocking: z.boolean(),
        humanDecisionRequired: z.boolean(),
        acceptedBasisRef: z.string().min(1),
        validationRef: z.string().min(1).optional(),
        humanAcceptanceRef: z.string().min(1).optional()
      },
      async (args) => jsonResult(await reportCoordinationNotice(await parentSession(input.context), args))
    ));
  }
  if (input.allowedToolNames.has('mcp__chirality__send_agent_update')) {
    tools.push(tool(
      'send_agent_update',
      'Relay information or a versioned brief amendment to one direct child.',
      {
        childInstanceId: z.string().min(1),
        noticeId: z.string().optional(),
        disposition: z.enum(['RECORD', 'RELAY', 'AMEND', 'HOLD', 'REPLAN', 'ESCALATE', 'ROUTE']),
        summary: z.string().min(1),
        claimStatus: z.enum(['PROVISIONAL', 'VALIDATED', 'ACCEPTED', 'DISPUTED']),
        evidenceRefs: z.array(z.string()),
        consequential: z.boolean(),
        humanRulingRef: z.string().optional(),
        amendment: z.string().optional(),
        planVersion: z.string().optional(),
        selectionAuthority: z.enum(['HUMAN', 'AGENT_0', 'AGENT_1']).optional(),
        posture: z.enum(['TERMINAL_FAN_OUT_IN', 'SUPERVISED_MANY_TO_MANY', 'MIXED']).optional(),
        acceptedBasis: z.array(z.string()).optional(),
        workGraph: z.record(z.string(), z.unknown()).optional(),
        validationRef: z.string().min(1).optional(),
        humanAcceptanceRef: z.string().min(1).optional(),
        amendmentCategories: z.array(z.enum([
          'INFORMATION', 'CONTEXT', 'SEQUENCING', 'SCOPE', 'RISK',
          'AUTHORITY', 'SHARED_WRITE', 'ACCEPTANCE'
        ])).optional(),
        amendmentVersion: z.string().min(1).optional()
      },
      async (args) => jsonResult(await sendAgentUpdate(await parentSession(input.context), args))
    ));
  }
  if (input.allowedToolNames.has('mcp__chirality__ack_agent_update')) {
    tools.push(tool(
      'ack_agent_update',
      'Acknowledge an update from the direct parent.',
      {
        updateId: z.string().min(1),
        acknowledgment: z.enum(['INCORPORATED', 'NO_EFFECT', 'BLOCKED', 'CONFLICT', 'HUMAN_DECISION_REQUIRED']),
        summary: z.string().optional()
      },
      async (args) => jsonResult(await acknowledgeAgentUpdate(await parentSession(input.context), args))
    ));
  }
  return tools;
}
