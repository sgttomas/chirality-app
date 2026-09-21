import type { CanUseTool, PermissionResult } from '@anthropic-ai/claude-agent-sdk';
import { randomUUID } from 'node:crypto';
import { createHarnessEvent } from './event-factory';
import type { HarnessEvent } from '@chirality/runtime-contracts/event-schema';
import { appendHarnessEvent } from './session-events';
import { summarizeToolDescriptor, summarizeToolInput } from './tool-evidence';
import { evaluateToolPathPolicy } from './tool-path-policy';
import { evaluateShellCommandPolicy } from './tool-shell-policy';
import type { HarnessToolDescriptor } from '@chirality/runtime-contracts/tool-descriptor';
import { evaluateSubagentPreflight } from './subagent-bridge';

export const HARNESS_PERMISSION_POLICY_VERSION = 'harness-permission.v7.coordination-mode';

export type HarnessPermissionDecisionValue = 'allow' | 'deny' | 'ask';

export type HarnessPermissionDecisionSource =
  | 'sdk-option'
  | 'sdk-callback'
  | 'chirality-policy'
  | 'hook'
  | 'human'
  | 'prompt-support';

export type NormalizedHarnessPermissionMode =
  | 'readOnly'
  | 'workspaceWrite'
  | 'dontAsk'
  | 'ask'
  | 'bypass';

export type HarnessPermissionDecision = {
  decisionId: string;
  sessionId: string;
  turnId?: string;
  toolName: string;
  decision: HarnessPermissionDecisionValue;
  reason: string;
  source: HarnessPermissionDecisionSource;
  decidedAt: string;
  safeMetadata?: Record<string, unknown>;
};

export type ResolveHarnessPermissionDecisionInput = {
  sessionId?: string;
  turnId?: string;
  toolName: string;
  mode?: string;
  descriptor?: HarnessToolDescriptor;
  source?: HarnessPermissionDecisionSource;
  explicitDeny?: boolean;
  explicitDenyReason?: string;
  delegatedSubagents?: readonly string[];
  toolInput?: Record<string, unknown>;
  safeMetadata?: Record<string, unknown>;
};

export function normalizeHarnessPermissionMode(mode: string | undefined): NormalizedHarnessPermissionMode {
  if (mode === 'readOnly') {
    return 'readOnly';
  }
  if (mode === 'workspaceWrite') {
    return 'workspaceWrite';
  }
  if (mode === 'dontAsk') {
    return 'dontAsk';
  }
  if (mode === 'bypass') {
    return 'bypass';
  }
  return 'ask';
}

function createDecision(
  input: ResolveHarnessPermissionDecisionInput,
  decision: HarnessPermissionDecisionValue,
  reason: string,
  extraMetadata?: Record<string, unknown>
): HarnessPermissionDecision {
  const descriptor = input.descriptor;
  const mode = normalizeHarnessPermissionMode(input.mode);
  return {
    decisionId: `perm_${randomUUID()}`,
    sessionId: input.sessionId ?? 'session:unbound',
    turnId: input.turnId,
    toolName: input.toolName,
    decision,
    reason,
    source: input.source ?? 'chirality-policy',
    decidedAt: new Date().toISOString(),
    safeMetadata: {
      policyVersion: HARNESS_PERMISSION_POLICY_VERSION,
      mode,
      descriptorName: descriptor?.name,
      adapterToolName: descriptor?.adapter.claudeAgentSdk?.toolName,
      permissions: descriptor ? [...descriptor.permissions] : undefined,
      pathScope: descriptor?.pathScope,
      surface: descriptor?.surface,
      humanGate: descriptor?.humanGate,
      ...input.safeMetadata,
      ...extraMetadata
    }
  };
}

function hasDescriptorPermission(
  descriptor: HarnessToolDescriptor,
  permission: HarnessToolDescriptor['permissions'][number]
): boolean {
  return descriptor.permissions.includes(permission);
}

export function resolveHarnessPermissionDecision(
  input: ResolveHarnessPermissionDecisionInput
): HarnessPermissionDecision {
  const descriptor = input.descriptor;
  const mode = normalizeHarnessPermissionMode(input.mode);

  if (input.explicitDeny) {
    return createDecision(
      input,
      'deny',
      input.explicitDenyReason ?? 'Denied by explicit Chirality hard-deny policy.',
      { hardDeny: true }
    );
  }

  if (!descriptor) {
    return createDecision(input, 'deny', `Unknown harness tool '${input.toolName}'.`, {
      hardDeny: true,
      denyClass: 'unknown-tool'
    });
  }

  if (descriptor.surface === 'reserved') {
    return createDecision(input, 'deny', `${descriptor.name} is reserved for future policy.`, {
      hardDeny: true,
      denyClass: 'reserved-tool'
    });
  }

  if (hasDescriptorPermission(descriptor, 'shell')) {
    if (mode === 'workspaceWrite') {
      return createDecision(
        input,
        'allow',
        `${descriptor.name} is allowed by workspaceWrite mode after Chirality shell hooks pass.`,
        {
          allowClass: 'shell',
          requiresHookApproval: true
        }
      );
    }

    if (mode === 'ask') {
      return createDecision(
        input,
        'ask',
        `${descriptor.name} requires interactive approval and shell hooks before execution.`,
        {
          requiresHumanApproval: true,
          denyClass: 'shell'
        }
      );
    }

    return createDecision(input, 'deny', `${descriptor.name} is denied in ${mode} mode.`, {
      denyClass: 'shell'
    });
  }

  if (hasDescriptorPermission(descriptor, 'danger')) {
    return createDecision(
      input,
      'deny',
      `${descriptor.name} is denied because it carries a danger-class capability.`,
      {
        hardDeny: true,
        denyClass: 'danger'
      }
    );
  }

  if (hasDescriptorPermission(descriptor, 'network')) {
    return createDecision(
      input,
      'deny',
      'Network-capable tools require a future governed implementation tranche.',
      {
        hardDeny: true,
        denyClass: 'network'
      }
    );
  }

  if (hasDescriptorPermission(descriptor, 'subagent')) {
    const preflight = evaluateSubagentPreflight({
      toolInput: input.toolInput ?? {},
      eligibleAgentNames: input.delegatedSubagents
    });
    if (preflight.allowed && mode === 'workspaceWrite') {
      return createDecision(input, 'allow', preflight.reason, {
        allowClass: 'subagent',
        requiresHookApproval: true,
        ...preflight.safeMetadata
      });
    }

    return createDecision(
      input,
      'deny',
      preflight.allowed
        ? 'Subagent execution requires workspaceWrite mode under the D-APP-10 Option C executable bridge.'
        : preflight.reason,
      {
        hardDeny: true,
        denyClass: 'subagent',
        requiresSubagentPreflight: true,
        ...preflight.safeMetadata
      }
    );
  }

  if (hasDescriptorPermission(descriptor, 'coordination')) {
    if (mode !== 'workspaceWrite') {
      return createDecision(
        input,
        'deny',
        `${descriptor.name} mutates the orchestration control plane and requires workspaceWrite mode.`,
        {
          hardDeny: true,
          denyClass: 'coordination-mode',
          requiresManagedDelegationPolicy: true
        }
      );
    }
    return createDecision(
      input,
      'allow',
      `${descriptor.name} is admitted to handler-level hierarchy and control-plane validation.`,
      {
        allowClass: 'coordination',
        requiresManagedDelegationPolicy: true
      }
    );
  }

  if (hasDescriptorPermission(descriptor, 'control')) {
    return createDecision(
      input,
      'allow',
      `${descriptor.name} is admitted as bounded Runtime session control.`,
      {
        allowClass: 'control',
        filesystemCapability: false,
        processCapability: false,
        networkCapability: false
      }
    );
  }

  if (hasDescriptorPermission(descriptor, 'workspace-write')) {
    if (mode === 'workspaceWrite') {
      return createDecision(
        input,
        'allow',
        `${descriptor.name} is allowed by workspaceWrite mode after Chirality write hooks pass.`,
        {
          allowClass: 'workspace-write',
          requiresHookApproval: true
        }
      );
    }

    if (mode === 'ask') {
      return createDecision(
        input,
        'ask',
        `${descriptor.name} requires interactive approval and write hooks before execution.`,
        {
          requiresHumanApproval: true
        }
      );
    }

    return createDecision(
      input,
      'deny',
      `${descriptor.name} is denied in ${mode} mode because it can modify workspace files.`,
      {
        denyClass: 'workspace-write'
      }
    );
  }

  if (hasDescriptorPermission(descriptor, 'read')) {
    return createDecision(input, 'allow', `${descriptor.name} is allowed by ${mode} mode.`, {
      allowClass: 'read'
    });
  }

  return createDecision(input, 'deny', `${descriptor.name} has no supported permission class.`, {
    denyClass: 'unsupported-permission'
  });
}

export function permissionDecisionToSdkResult(
  decision: HarnessPermissionDecision,
  toolUseID?: string
): PermissionResult {
  if (decision.decision === 'allow') {
    return {
      behavior: 'allow',
      toolUseID
    };
  }

  return {
    behavior: 'deny',
    message:
      decision.decision === 'ask'
        ? `Chirality permission requires application approval; denying SDK auto-execution for this tranche. ${decision.reason}`
        : decision.reason,
    toolUseID
  };
}

export async function appendHarnessPermissionDecisionEvent(input: {
  decision: HarnessPermissionDecision;
  descriptor?: HarnessToolDescriptor;
  sdkToolUseId?: string;
  // When provided, the persisted event is also published to the live channel so
  // it reaches the browser while the SDK is suspended awaiting a verdict.
  publishEvent?: (event: HarnessEvent) => void;
}): Promise<void> {
  const event = createHarnessEvent({
    sessionId: input.decision.sessionId,
    type: 'tool.permission',
    turnId: input.decision.turnId,
    data: {
      behavior: input.decision.decision,
      decisionId: input.decision.decisionId,
      reason: input.decision.reason,
      source: input.decision.source,
      toolName: input.decision.toolName,
      adapterToolUseId: input.sdkToolUseId,
      toolUseId: input.sdkToolUseId,
      mode: input.decision.safeMetadata?.mode,
      ...summarizeToolDescriptor(input.descriptor),
      safeMetadata: input.decision.safeMetadata
    }
  });
  await appendHarnessEvent(event);
  input.publishEvent?.(event);
}

export type HumanPermissionRequest = {
  sessionId: string;
  toolUseId?: string;
  toolName: string;
  reason: string;
  decisionId: string;
};

export function createHarnessCanUseTool(input: {
  sessionId: string;
  mode: string;
  projectRoot?: string;
  allowedReadScopes?: readonly string[];
  allowedWriteTargets?: readonly string[];
  delegatedSubagents?: readonly string[];
  resolveDescriptor: (toolName: string) => HarnessToolDescriptor | undefined;
  // When provided, an `ask` decision suspends until the operator returns a
  // verdict (the inline approval pause). When absent, `ask` denies as before.
  requestHumanDecision?: (request: HumanPermissionRequest) => Promise<HarnessPermissionDecisionValue>;
  // When provided, each persisted permission decision is also published to the
  // live channel so it reaches the browser in real time.
  publishEvent?: (event: HarnessEvent) => void;
}): CanUseTool {
  return async (toolName, toolInput, options) => {
    const descriptor = input.resolveDescriptor(toolName);
    const pathPolicy = await evaluateToolPathPolicy({
      descriptor,
      projectRoot: input.projectRoot,
      toolInput,
      blockedPath: options.blockedPath,
      allowedReadScopes: input.allowedReadScopes,
      allowedWriteTargets: input.allowedWriteTargets
    });
    const shellPolicy =
      pathPolicy.allowed && descriptor?.permissions.includes('shell')
        ? await evaluateShellCommandPolicy({
            descriptor,
            projectRoot: input.projectRoot,
            toolInput,
            allowedReadScopes: input.allowedReadScopes,
            allowedWriteTargets: input.allowedWriteTargets
          })
        : undefined;
    const explicitDeny = !pathPolicy.allowed || shellPolicy?.allowed === false;
    const decision = resolveHarnessPermissionDecision({
      sessionId: input.sessionId,
      mode: input.mode,
      toolName,
      descriptor,
      source: 'sdk-callback',
      delegatedSubagents: input.delegatedSubagents,
      toolInput,
      explicitDeny,
      explicitDenyReason: !pathPolicy.allowed
        ? pathPolicy.reason
        : shellPolicy?.allowed === false
          ? shellPolicy.reason
          : undefined,
      safeMetadata: {
        inputMetadata: summarizeToolInput(toolInput),
        decisionReason: options.decisionReason,
        title: options.title,
        displayName: options.displayName,
        description: options.description,
        sdkToolUseId: options.toolUseID,
        pathMetadata: pathPolicy.allowed ? pathPolicy.metadata : undefined,
        shellMetadata: shellPolicy?.metadata,
        ...(pathPolicy.allowed ? {} : pathPolicy.metadata),
        ...(shellPolicy?.allowed === false ? shellPolicy.metadata : {})
      }
    });

    try {
      await appendHarnessPermissionDecisionEvent({
        decision,
        descriptor,
        sdkToolUseId: options.toolUseID,
        publishEvent: input.publishEvent
      });
    } catch (error) {
      const message = error instanceof Error ? error.message : 'unknown audit append failure';
      return {
        behavior: 'deny',
        message: `Chirality audit event append failed; denying tool execution. ${message}`,
        toolUseID: options.toolUseID
      };
    }

    // Only suspend for a human verdict when the call has an addressable id the UI
    // can echo back to the broker; without it, fall through to the standalone
    // ask→deny rather than registering an unreachable pending entry.
    if (decision.decision === 'ask' && input.requestHumanDecision && options.toolUseID) {
      let verdict: HarnessPermissionDecisionValue = 'deny';
      try {
        verdict = await input.requestHumanDecision({
          sessionId: input.sessionId,
          toolUseId: options.toolUseID,
          toolName,
          reason: decision.reason,
          decisionId: decision.decisionId
        });
      } catch {
        verdict = 'deny';
      }

      const humanDecision: HarnessPermissionDecision = {
        ...decision,
        decisionId: `perm_${randomUUID()}`,
        decision: verdict === 'allow' ? 'allow' : 'deny',
        source: 'human',
        decidedAt: new Date().toISOString(),
        reason:
          verdict === 'allow'
            ? `Operator approved ${descriptor?.name ?? toolName}.`
            : `Operator denied ${descriptor?.name ?? toolName}.`,
        safeMetadata: {
          ...decision.safeMetadata,
          humanVerdict: verdict,
          askDecisionId: decision.decisionId
        }
      };

      try {
        await appendHarnessPermissionDecisionEvent({
          decision: humanDecision,
          descriptor,
          sdkToolUseId: options.toolUseID,
          publishEvent: input.publishEvent
        });
      } catch {
        // Best-effort audit of the human verdict; the SDK result below is authoritative.
      }

      return permissionDecisionToSdkResult(humanDecision, options.toolUseID);
    }

    return permissionDecisionToSdkResult(decision, options.toolUseID);
  };
}
