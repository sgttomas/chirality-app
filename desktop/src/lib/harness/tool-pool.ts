import {
  HARNESS_TOOL_REGISTRY_VERSION,
  getCurrentTrancheDisallowedToolNames,
  getHarnessToolDescriptor,
  getKnownHarnessToolNames,
  type ClaudeAgentSdkToolName,
  type HarnessToolDescriptor,
  type HarnessToolResolutionIssue
} from '@chirality/runtime-contracts/tool-descriptor';
import {
  resolveHarnessPermissionDecision,
  type HarnessPermissionDecision
} from './permission-overlay';

export type HarnessToolPoolResolution = {
  registryVersion: typeof HARNESS_TOOL_REGISTRY_VERSION;
  mode: string;
  requestedTools: readonly string[];
  requestedDescriptors: readonly HarnessToolDescriptor[];
  permissionDecisions: readonly HarnessPermissionDecision[];
  allowedToolNames: readonly ClaudeAgentSdkToolName[];
  disallowedToolNames: readonly ClaudeAgentSdkToolName[];
  deniedTools: readonly HarnessToolResolutionIssue[];
  unknownTools: readonly HarnessToolResolutionIssue[];
  issues: readonly HarnessToolResolutionIssue[];
};

function uniqueValues<T>(values: readonly T[]): T[] {
  return Array.from(new Set(values));
}

function getSdkToolName(descriptor: HarnessToolDescriptor): ClaudeAgentSdkToolName | undefined {
  return descriptor.adapter.claudeAgentSdk?.toolName;
}

export function resolveHarnessToolPool(input: {
  sessionId?: string;
  requestedTools?: readonly string[];
  mode?: string;
}): HarnessToolPoolResolution {
  const requestedTools = uniqueValues(
    (input.requestedTools ?? [])
      .map((toolName) => toolName.trim())
      .filter((toolName) => toolName.length > 0)
  );
  const requestedDescriptors: HarnessToolDescriptor[] = [];
  const deniedTools: HarnessToolResolutionIssue[] = [];
  const unknownTools: HarnessToolResolutionIssue[] = [];
  const permissionDecisions: HarnessPermissionDecision[] = [];
  const allowedToolNames: ClaudeAgentSdkToolName[] = [];
  const seenDescriptors = new Set<string>();
  const knownTools = getKnownHarnessToolNames();

  for (const toolName of requestedTools) {
    const descriptor = getHarnessToolDescriptor(toolName);
    if (!descriptor) {
      permissionDecisions.push(
        resolveHarnessPermissionDecision({
          sessionId: input.sessionId,
          toolName,
          mode: input.mode,
          source: 'chirality-policy'
        })
      );
      unknownTools.push({
        type: 'UNKNOWN_TOOL',
        toolName,
        message: `Unknown harness tool '${toolName}'.`,
        knownTools
      });
      continue;
    }

    if (!seenDescriptors.has(descriptor.name)) {
      seenDescriptors.add(descriptor.name);
      requestedDescriptors.push(descriptor);
      const decision = resolveHarnessPermissionDecision({
        sessionId: input.sessionId,
        toolName,
        mode: input.mode,
        descriptor,
        source: 'chirality-policy'
      });
      permissionDecisions.push(decision);

      const sdkToolName = getSdkToolName(descriptor);
      if (decision.decision === 'allow' && descriptor.runtime.exposedToModel && sdkToolName) {
        allowedToolNames.push(sdkToolName);
      } else {
        deniedTools.push({
          type: 'DENIED_BY_CURRENT_PHASE',
          toolName,
          descriptorName: descriptor.name,
          message: descriptor.runtime.exposedToModel ? decision.reason : descriptor.runtime.reason
        });
      }
    }
  }

  return {
    registryVersion: HARNESS_TOOL_REGISTRY_VERSION,
    mode: input.mode ?? 'default',
    requestedTools,
    requestedDescriptors,
    permissionDecisions,
    allowedToolNames: uniqueValues(allowedToolNames),
    disallowedToolNames: getCurrentTrancheDisallowedToolNames(allowedToolNames),
    deniedTools,
    unknownTools,
    issues: [...unknownTools, ...deniedTools]
  };
}
