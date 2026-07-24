import type { HarnessEventType } from './event-schema.js';
import {
  toChiralityMcpAllowedToolName,
  type ChiralityMcpAllowedToolName,
  type ChiralityMcpCoordinationToolName,
  type ChiralityMcpDomainToolName,
  type ChiralityMcpMutatingToolName,
  type ChiralityMcpReadToolName
} from './mcp/tool-names.js';

export const HARNESS_TOOL_REGISTRY_VERSION = 'harness-tools.v14.headless-preview-live';

export type ClaudeAgentSdkBuiltinToolName =
  | 'Read'
  | 'Glob'
  | 'Grep'
  | 'LS'
  | 'Write'
  | 'Edit'
  | 'MultiEdit'
  | 'NotebookEdit'
  | 'Bash'
  | 'WebFetch'
  | 'WebSearch'
  | 'Agent';

export type ClaudeAgentSdkToolName = ClaudeAgentSdkBuiltinToolName | ChiralityMcpAllowedToolName;

export type HarnessToolPermission =
  | 'read'
  | 'workspace-write'
  | 'network'
  | 'shell'
  | 'subagent'
  | 'coordination'
  | 'danger';

export type HarnessToolPathScope =
  | 'none'
  | 'project-root-read'
  | 'project-root-write'
  | 'instruction-root-read'
  | 'external-network';

export type HarnessToolIdempotence = 'idempotent' | 'input-dependent' | 'mutating';
export type HarnessToolConcurrency = 'safe' | 'serialized-by-path' | 'exclusive';
export type HarnessToolInterruptBehavior = 'cancel' | 'block' | 'not-applicable';
export type HarnessToolSurface = 'claude-agent-sdk-builtin' | 'chirality-mcp' | 'reserved';

export type HarnessToolHumanGate =
  | {
      required: false;
    }
  | {
      required: true;
      gate: 'interactive-confirmation' | 'approval-sha' | 'future-policy';
      reason: string;
    };

export type HarnessToolResultBudget = {
  inlineByteLimit: number;
  artifactByteLimit: number;
  overflow: 'artifact' | 'deny' | 'summarize';
};

export type HarnessToolProvenance = {
  emits: readonly HarnessEventType[];
  storeInput: 'metadata' | 'redacted' | 'none';
  storeOutput: 'inline-or-artifact' | 'metadata' | 'none';
  recordsDiff: boolean;
};

export type HarnessToolRuntimeSupport =
  | {
      exposedToModel: true;
      reason: string;
    }
  | {
      exposedToModel: false;
      reason: string;
    };

export type HarnessToolDescriptor = {
  name: string;
  aliases: readonly string[];
  description: string;
  surface: HarnessToolSurface;
  permissions: readonly HarnessToolPermission[];
  pathScope: HarnessToolPathScope;
  idempotence: HarnessToolIdempotence;
  concurrency: HarnessToolConcurrency;
  interruptBehavior: HarnessToolInterruptBehavior;
  resultBudget: HarnessToolResultBudget;
  provenance: HarnessToolProvenance;
  humanGate: HarnessToolHumanGate;
  adapter: {
    claudeAgentSdk?: {
      toolName: ClaudeAgentSdkToolName;
    };
  };
  inputSchema: Record<string, unknown>;
  outputSchema?: Record<string, unknown>;
  runtime: HarnessToolRuntimeSupport;
};

export type HarnessToolResolutionIssue =
  | {
      type: 'UNKNOWN_TOOL';
      toolName: string;
      message: string;
      knownTools: readonly string[];
    }
  | {
      type: 'DENIED_BY_CURRENT_PHASE';
      toolName: string;
      descriptorName: string;
      message: string;
    };

const TOOL_EVENTS = [
  'tool.permission',
  'tool.started',
  'tool.progress',
  'tool.completed',
  'tool.failed'
] as const satisfies readonly HarnessEventType[];

const SDK_READ_RUNTIME: HarnessToolRuntimeSupport = {
  exposedToModel: true,
  reason:
    'Read-class SDK built-ins are exposed behind Chirality permission overlay and hard-deny policy.'
};

const CHIRALITY_READ_MCP_RUNTIME: HarnessToolRuntimeSupport = {
  exposedToModel: true,
  reason:
    'Read-only Chirality MCP tools are exposed behind descriptor resolution and permission overlay policy.'
};

const CHIRALITY_DOMAIN_READ_MCP_RUNTIME: HarnessToolRuntimeSupport = {
  exposedToModel: true,
  reason:
    'D-APP-50 tranche-1 read-only domain wrappers are exposed through DEC-041 in-process MCP transport.'
};

const CHIRALITY_MUTATING_MCP_RUNTIME: HarnessToolRuntimeSupport = {
  exposedToModel: true,
  reason:
    'Mutating Chirality MCP tools are exposed only when requested in workspaceWrite mode and enforced by the handler-level permission/evidence wrapper.'
};

const CHIRALITY_COORDINATION_MCP_RUNTIME: HarnessToolRuntimeSupport = {
  exposedToModel: true,
  reason:
    'Managed coordination tools require workspaceWrite mode, write runtime-owned control-plane records, and enforce hierarchy, seals, parentage, capabilities, and project path boundaries.'
};

const CHIRALITY_DOMAIN_DESCRIPTOR_ONLY_RUNTIME: HarnessToolRuntimeSupport = {
  exposedToModel: false,
  reason:
    'D-APP-50 registers the governed domain MCP descriptor, but keeps it descriptor-only until runtime transport and write quarantine are sound.'
};

const SDK_WRITE_RUNTIME: HarnessToolRuntimeSupport = {
  exposedToModel: true,
  reason:
    'Write/Edit SDK built-ins are exposed only in workspaceWrite mode after descriptor resolution, permission overlay, and Chirality write hooks.'
};

const SDK_SHELL_RUNTIME: HarnessToolRuntimeSupport = {
  exposedToModel: true,
  reason:
    'Bash is exposed only in workspaceWrite mode after descriptor resolution, permission overlay, timeout policy, and Chirality shell hooks.'
};

const DESCRIPTOR_ONLY_RUNTIME: HarnessToolRuntimeSupport = {
  exposedToModel: false,
  reason:
    'This tool is not exposed until its permission overlay, hooks, result storage, and validation tranche land.'
};

const READ_RESULT_BUDGET: HarnessToolResultBudget = {
  inlineByteLimit: 64 * 1024,
  artifactByteLimit: 2 * 1024 * 1024,
  overflow: 'artifact'
};

const WRITE_RESULT_BUDGET: HarnessToolResultBudget = {
  inlineByteLimit: 16 * 1024,
  artifactByteLimit: 512 * 1024,
  overflow: 'artifact'
};

const SHELL_RESULT_BUDGET: HarnessToolResultBudget = {
  inlineByteLimit: 16 * 1024,
  artifactByteLimit: 2 * 1024 * 1024,
  overflow: 'artifact'
};

function normalizeToolName(toolName: string): string {
  return toolName.trim().toLowerCase();
}

function uniqueDescriptorAliases(input: {
  name: string;
  aliases: readonly string[];
  adapterToolName: string;
}): string[] {
  const reservedKeys = new Set([
    normalizeToolName(input.name),
    normalizeToolName(input.adapterToolName)
  ]);
  const aliases: string[] = [];
  for (const alias of input.aliases) {
    const key = normalizeToolName(alias);
    if (reservedKeys.has(key)) {
      continue;
    }
    reservedKeys.add(key);
    aliases.push(alias);
  }
  return aliases;
}

function readOnlyDescriptor(input: {
  name: string;
  aliases: readonly string[];
  description: string;
  sdkToolName: ClaudeAgentSdkToolName;
  inputSchema: Record<string, unknown>;
}): HarnessToolDescriptor {
  return {
    name: input.name,
    aliases: uniqueDescriptorAliases({
      name: input.name,
      aliases: input.aliases,
      adapterToolName: input.sdkToolName
    }),
    description: input.description,
    surface: 'claude-agent-sdk-builtin',
    permissions: ['read'],
    pathScope: 'project-root-read',
    idempotence: 'idempotent',
    concurrency: 'safe',
    interruptBehavior: 'cancel',
    resultBudget: READ_RESULT_BUDGET,
    provenance: {
      emits: TOOL_EVENTS,
      storeInput: 'metadata',
      storeOutput: 'inline-or-artifact',
      recordsDiff: false
    },
    humanGate: {
      required: false
    },
    adapter: {
      claudeAgentSdk: {
        toolName: input.sdkToolName
      }
    },
    inputSchema: input.inputSchema,
    runtime: SDK_READ_RUNTIME
  };
}

function chiralityReadMcpDescriptor(input: {
  name: string;
  aliases: readonly string[];
  description: string;
  mcpToolName: ChiralityMcpReadToolName;
  inputSchema: Record<string, unknown>;
  outputSchema?: Record<string, unknown>;
}): HarnessToolDescriptor {
  return {
    name: input.name,
    aliases: uniqueDescriptorAliases({
      name: input.name,
      aliases: [...input.aliases, input.mcpToolName],
      adapterToolName: toChiralityMcpAllowedToolName(input.mcpToolName)
    }),
    description: input.description,
    surface: 'chirality-mcp',
    permissions: ['read'],
    pathScope: 'project-root-read',
    idempotence: 'idempotent',
    concurrency: 'safe',
    interruptBehavior: 'cancel',
    resultBudget: READ_RESULT_BUDGET,
    provenance: {
      emits: TOOL_EVENTS,
      storeInput: 'metadata',
      storeOutput: 'inline-or-artifact',
      recordsDiff: false
    },
    humanGate: {
      required: false
    },
    adapter: {
      claudeAgentSdk: {
        toolName: toChiralityMcpAllowedToolName(input.mcpToolName)
      }
    },
    inputSchema: input.inputSchema,
    outputSchema: input.outputSchema,
    runtime: CHIRALITY_READ_MCP_RUNTIME
  };
}

function chiralityDomainReadMcpDescriptor(input: {
  name: ChiralityMcpDomainToolName;
  aliases: readonly string[];
  description: string;
  mcpToolName: ChiralityMcpDomainToolName;
  inputSchema: Record<string, unknown>;
  outputSchema?: Record<string, unknown>;
  idempotence?: HarnessToolIdempotence;
  concurrency?: HarnessToolConcurrency;
  runtimeReason?: string;
}): HarnessToolDescriptor {
  return {
    name: input.name,
    aliases: uniqueDescriptorAliases({
      name: input.name,
      aliases: [...input.aliases, input.mcpToolName],
      adapterToolName: toChiralityMcpAllowedToolName(input.mcpToolName)
    }),
    description: input.description,
    surface: 'chirality-mcp',
    permissions: ['read'],
    pathScope: 'project-root-read',
    idempotence: input.idempotence ?? 'idempotent',
    concurrency: input.concurrency ?? 'safe',
    interruptBehavior: 'cancel',
    resultBudget: READ_RESULT_BUDGET,
    provenance: {
      emits: TOOL_EVENTS,
      storeInput: 'metadata',
      storeOutput: 'inline-or-artifact',
      recordsDiff: false
    },
    humanGate: {
      required: false
    },
    adapter: {
      claudeAgentSdk: {
        toolName: toChiralityMcpAllowedToolName(input.mcpToolName)
      }
    },
    inputSchema: input.inputSchema,
    outputSchema: input.outputSchema,
    runtime: input.runtimeReason
      ? { exposedToModel: true, reason: input.runtimeReason }
      : CHIRALITY_DOMAIN_READ_MCP_RUNTIME
  };
}

function chiralityMutatingMcpDescriptor(input: {
  name: string;
  aliases: readonly string[];
  description: string;
  mcpToolName: ChiralityMcpMutatingToolName;
  inputSchema: Record<string, unknown>;
  outputSchema?: Record<string, unknown>;
  humanGate: HarnessToolHumanGate;
}): HarnessToolDescriptor {
  return {
    name: input.name,
    aliases: uniqueDescriptorAliases({
      name: input.name,
      aliases: [...input.aliases, input.mcpToolName],
      adapterToolName: toChiralityMcpAllowedToolName(input.mcpToolName)
    }),
    description: input.description,
    surface: 'chirality-mcp',
    permissions: ['workspace-write'],
    pathScope: 'project-root-write',
    idempotence: 'mutating',
    concurrency: 'serialized-by-path',
    interruptBehavior: 'block',
    resultBudget: WRITE_RESULT_BUDGET,
    provenance: {
      emits: TOOL_EVENTS,
      storeInput: 'metadata',
      storeOutput: 'metadata',
      recordsDiff: true
    },
    humanGate: input.humanGate,
    adapter: {
      claudeAgentSdk: {
        toolName: toChiralityMcpAllowedToolName(input.mcpToolName)
      }
    },
    inputSchema: input.inputSchema,
    outputSchema: input.outputSchema,
    runtime: CHIRALITY_MUTATING_MCP_RUNTIME
  };
}

function chiralityCoordinationMcpDescriptor(input: {
  name: ChiralityMcpCoordinationToolName;
  aliases: readonly string[];
  description: string;
  inputSchema: Record<string, unknown>;
}): HarnessToolDescriptor {
  return {
    name: input.name,
    aliases: uniqueDescriptorAliases({
      name: input.name,
      aliases: input.aliases,
      adapterToolName: toChiralityMcpAllowedToolName(input.name)
    }),
    description: input.description,
    surface: 'chirality-mcp',
    permissions: ['coordination'],
    pathScope: 'none',
    idempotence: 'mutating',
    concurrency: 'exclusive',
    interruptBehavior: 'block',
    resultBudget: READ_RESULT_BUDGET,
    provenance: {
      emits: TOOL_EVENTS,
      storeInput: 'metadata',
      storeOutput: 'inline-or-artifact',
      recordsDiff: false
    },
    humanGate: { required: false },
    adapter: {
      claudeAgentSdk: { toolName: toChiralityMcpAllowedToolName(input.name) }
    },
    inputSchema: input.inputSchema,
    runtime: CHIRALITY_COORDINATION_MCP_RUNTIME
  };
}

function chiralityDomainDescriptorOnly(input: {
  name: string;
  aliases: readonly string[];
  description: string;
  mcpToolName: ChiralityMcpDomainToolName;
  permissions: readonly HarnessToolPermission[];
  pathScope: HarnessToolPathScope;
  idempotence: HarnessToolIdempotence;
  concurrency: HarnessToolConcurrency;
  resultBudget: HarnessToolResultBudget;
  inputSchema: Record<string, unknown>;
  outputSchema?: Record<string, unknown>;
  gateReason: string;
}): HarnessToolDescriptor {
  return {
    name: input.name,
    aliases: uniqueDescriptorAliases({
      name: input.name,
      aliases: [...input.aliases, input.mcpToolName],
      adapterToolName: toChiralityMcpAllowedToolName(input.mcpToolName)
    }),
    description: input.description,
    surface: 'reserved',
    permissions: input.permissions,
    pathScope: input.pathScope,
    idempotence: input.idempotence,
    concurrency: input.concurrency,
    interruptBehavior: input.permissions.includes('workspace-write') ? 'block' : 'cancel',
    resultBudget: input.resultBudget,
    provenance: {
      emits: TOOL_EVENTS,
      storeInput: 'metadata',
      storeOutput: input.permissions.includes('workspace-write') ? 'metadata' : 'inline-or-artifact',
      recordsDiff: input.permissions.includes('workspace-write')
    },
    humanGate: {
      required: true,
      gate: 'future-policy',
      reason: input.gateReason
    },
    adapter: {
      claudeAgentSdk: {
        toolName: toChiralityMcpAllowedToolName(input.mcpToolName)
      }
    },
    inputSchema: input.inputSchema,
    outputSchema: input.outputSchema,
    runtime: {
      ...CHIRALITY_DOMAIN_DESCRIPTOR_ONLY_RUNTIME,
      reason: `D-APP-50 descriptor-only park: ${input.gateReason}`
    }
  };
}

export const HARNESS_TOOL_DESCRIPTORS = [
  readOnlyDescriptor({
    name: 'read_file',
    aliases: ['read', 'sdk.read'],
    description: 'Read one project-root-contained file.',
    sdkToolName: 'Read',
    inputSchema: {
      type: 'object',
      required: ['file_path'],
      properties: {
        file_path: {
          type: 'string'
        }
      }
    }
  }),
  readOnlyDescriptor({
    name: 'find_files',
    aliases: ['glob', 'sdk.glob'],
    description: 'Find project files by glob pattern.',
    sdkToolName: 'Glob',
    inputSchema: {
      type: 'object',
      required: ['pattern'],
      properties: {
        pattern: {
          type: 'string'
        }
      }
    }
  }),
  readOnlyDescriptor({
    name: 'search_files',
    aliases: ['grep', 'search', 'sdk.grep'],
    description: 'Search project files for text patterns.',
    sdkToolName: 'Grep',
    inputSchema: {
      type: 'object',
      required: ['pattern'],
      properties: {
        pattern: {
          type: 'string'
        },
        path: {
          type: 'string'
        }
      }
    }
  }),
  readOnlyDescriptor({
    name: 'list_files',
    aliases: ['list', 'ls', 'sdk.ls'],
    description: 'List files and directories inside the project root.',
    sdkToolName: 'LS',
    inputSchema: {
      type: 'object',
      required: ['path'],
      properties: {
        path: {
          type: 'string'
        }
      }
    }
  }),
  chiralityReadMcpDescriptor({
    name: 'status_read',
    aliases: ['status', 'mcp.status_read'],
    description: 'Read parsed lifecycle state from a project-root-contained deliverable _STATUS.md.',
    mcpToolName: 'status_read',
    inputSchema: {
      type: 'object',
      required: ['deliverablePath'],
      properties: {
        deliverablePath: {
          type: 'string'
        }
      }
    },
    outputSchema: {
      type: 'object',
      required: ['projectRoot', 'deliverablePath', 'statusFilePath', 'status']
    }
  }),
  chiralityReadMcpDescriptor({
    name: 'dependency_read',
    aliases: ['dependencies', 'deps', 'deps_read', 'mcp.deps_read'],
    description: 'Read parsed dependency rows and warnings from a deliverable Dependencies.csv.',
    mcpToolName: 'deps_read',
    inputSchema: {
      type: 'object',
      required: ['deliverablePath'],
      properties: {
        deliverablePath: {
          type: 'string'
        }
      }
    },
    outputSchema: {
      type: 'object',
      required: ['projectRoot', 'deliverablePath', 'dependenciesFilePath', 'headers', 'rows', 'warnings']
    }
  }),
  chiralityReadMcpDescriptor({
    name: 'scope_scan',
    aliases: ['scope', 'mcp.scope_scan'],
    description: 'Scan deliverable and knowledge-type scopes inside the selected project root.',
    mcpToolName: 'scope_scan',
    inputSchema: {
      type: 'object',
      properties: {}
    },
    outputSchema: {
      type: 'object',
      required: ['projectRoot', 'deliverables', 'knowledgeTypes', 'truncated']
    }
  }),
  chiralityReadMcpDescriptor({
    name: 'scaffold_preview',
    aliases: ['scaffold_dry_run', 'mcp.scaffold_preview'],
    description: 'Preview execution-root scaffold paths from decomposition markdown without writing files.',
    mcpToolName: 'scaffold_preview',
    inputSchema: {
      type: 'object',
      required: ['executionRoot', 'decompositionPath'],
      properties: {
        executionRoot: {
          type: 'string'
        },
        decompositionPath: {
          type: 'string'
        },
        projectName: {
          type: 'string'
        },
        coordinationMode: {
          type: 'string'
        }
      }
    },
    outputSchema: {
      type: 'object',
      required: ['executionRoot', 'decompositionPath', 'planned', 'packages']
    }
  }),
  chiralityCoordinationMcpDescriptor({
    name: 'delegate_agent',
    aliases: ['delegate', 'mcp.delegate_agent'],
    description: 'Launch a governed direct child session under the Agent 0→1 or Agent 1→2 hierarchy and persist its work graph, brief, status, and return.',
    inputSchema: {
      type: 'object',
      required: ['executionRoot', 'runId', 'planVersion', 'selectionAuthority', 'posture', 'acceptedBasis', 'childKind', 'purpose', 'brief', 'declaredContext', 'tools', 'writeTargets', 'dependencies', 'expectedOutput', 'acceptanceCriteria', 'requiredReturnMarkers', 'contextSealed', 'pipelineRunApproved', 'approvalRef'],
      properties: {
        engineSelection: {
          type: 'object',
          required: ['adapterId', 'providerId', 'model'],
          properties: {
            adapterId: { type: 'string' },
            providerId: { type: 'string' },
            model: { type: 'string' }
          }
        }
      }
    }
  }),
  chiralityCoordinationMcpDescriptor({
    name: 'report_coordination_notice',
    aliases: ['coordination_notice', 'mcp.report_coordination_notice'],
    description: 'Report a typed, evidence-linked coordination notice from a managed child to its direct parent.',
    inputSchema: {
      type: 'object',
      required: ['noticeType', 'claimStatus', 'summary', 'evidenceRefs', 'affectedScopes', 'requestedAction', 'blocking', 'humanDecisionRequired', 'acceptedBasisRef'],
      conditional: {
        VALIDATED: ['validationRef'],
        ACCEPTED: ['humanAcceptanceRef']
      }
    }
  }),
  chiralityCoordinationMcpDescriptor({
    name: 'send_agent_update',
    aliases: ['agent_update', 'mcp.send_agent_update'],
    description: 'Relay information or a versioned amendment from a parent to one direct child.',
    inputSchema: {
      type: 'object',
      required: ['childInstanceId', 'disposition', 'summary', 'claimStatus', 'evidenceRefs', 'consequential'],
      conditional: {
        RELAY: ['noticeId'],
        AMEND_REPLAN: ['amendmentCategories', 'amendmentVersion or planVersion'],
        VALIDATED: ['validationRef'],
        ACCEPTED: ['humanAcceptanceRef']
      }
    }
  }),
  chiralityCoordinationMcpDescriptor({
    name: 'ack_agent_update',
    aliases: ['agent_update_ack', 'mcp.ack_agent_update'],
    description: 'Acknowledge a parent update as incorporated, no-effect, blocked, conflicting, or requiring a human decision.',
    inputSchema: {
      type: 'object',
      required: ['updateId', 'acknowledgment']
    }
  }),
  chiralityMutatingMcpDescriptor({
    name: 'status_transition',
    aliases: ['mcp.status_transition', 'transition_status'],
    description:
      'Apply a governed lifecycle transition to a deliverable _STATUS.md file.',
    mcpToolName: 'status_transition',
    inputSchema: {
      type: 'object',
      required: ['deliverablePath', 'targetState', 'actor'],
      properties: {
        deliverablePath: {
          type: 'string'
        },
        targetState: {
          type: 'string'
        },
        actor: {
          type: 'string'
        },
        date: {
          type: 'string'
        },
        approvalSha: {
          type: 'string'
        },
        metadata: {
          type: 'object',
          additionalProperties: {
            type: 'string'
          }
        }
      }
    },
    outputSchema: {
      type: 'object',
      required: ['ok', 'transition', 'status', 'fileEvidence']
    },
    humanGate: {
      required: true,
      gate: 'approval-sha',
      reason: 'CHECKING and ISSUED transitions require HUMAN actor approvalSha evidence.'
    }
  }),
  chiralityMutatingMcpDescriptor({
    name: 'dependency_write',
    aliases: ['deps_write', 'mcp.deps_write', 'write_dependencies'],
    description:
      'Write a governed Dependencies.csv register using v3.1 dependency writer semantics.',
    mcpToolName: 'deps_write',
    inputSchema: {
      type: 'object',
      required: ['deliverablePath', 'rows'],
      properties: {
        deliverablePath: {
          type: 'string'
        },
        rows: {
          type: 'array',
          items: {
            type: 'object',
            additionalProperties: {
              type: 'string'
            }
          }
        }
      }
    },
    outputSchema: {
      type: 'object',
      required: ['ok', 'rowCount', 'warnings', 'fileEvidence']
    },
    humanGate: {
      required: true,
      gate: 'interactive-confirmation',
      reason: 'Dependency register writes require workspaceWrite mode and governed row validation.'
    }
  }),
  chiralityDomainReadMcpDescriptor({
    name: 'domain_completeness_check',
    aliases: ['mcp.domain_completeness_check'],
    description:
      'Registry-gated domain MCP read wrapper for completeness_checker transport evidence (D-APP-50 tranche-1 open_pipe_stress; D-APP-51 P1 pec).',
    mcpToolName: 'domain_completeness_check',
    inputSchema: {
      type: 'object',
      required: ['profileId', 'inputRef'],
      properties: {
        profileId: {
          type: 'string'
        },
        inputRef: {
          type: 'string'
        }
      }
    },
    outputSchema: {
      type: 'object',
      required: ['profileId', 'toolId', 'transportStatus']
    }
  }),
  chiralityDomainReadMcpDescriptor({
    name: 'domain_rule_check_run',
    aliases: ['mcp.domain_rule_check_run'],
    description:
      'Registry-gated domain MCP read wrapper for rule_check_runner transport evidence (D-APP-50 tranche-1 open_pipe_stress; D-APP-51 P1 pec).',
    mcpToolName: 'domain_rule_check_run',
    inputSchema: {
      type: 'object',
      required: ['profileId', 'rulePackRef', 'valueBindingsRef'],
      properties: {
        profileId: {
          type: 'string'
        },
        rulePackRef: {
          type: 'string'
        },
        valueBindingsRef: {
          type: 'string'
        }
      }
    },
    outputSchema: {
      type: 'object',
      required: ['profileId', 'toolId', 'transportStatus']
    }
  }),
  chiralityDomainReadMcpDescriptor({
    name: 'domain_headless_preview_run',
    aliases: ['mcp.domain_headless_preview_run'],
    description:
      'Run one complete DEC-065 open_pipe_stress solve request through an explicitly configured, absolute, executable, SHA-256-pinned local openpipestress-runner process.',
    mcpToolName: 'domain_headless_preview_run',
    idempotence: 'input-dependent',
    concurrency: 'exclusive',
    inputSchema: {
      type: 'object',
      additionalProperties: false,
      required: ['profileId', 'runnerInputRef'],
      properties: {
        profileId: {
          type: 'string',
          const: 'open_pipe_stress'
        },
        runnerInputRef: {
          type: 'string'
        }
      }
    },
    outputSchema: {
      type: 'object',
      required: ['profileId', 'toolId', 'transportStatus']
    },
    runtimeReason:
      'D-APP-50 read-side live exposure through the DEC-065 configured local openpipestress-runner solve transport; requires an absolute executable path and exact SHA-256 in local process configuration.'
  }),
  {
    name: 'domain_propose_operation',
    aliases: uniqueDescriptorAliases({
      name: 'domain_propose_operation',
      aliases: ['mcp.domain_propose_operation', 'domain_propose_operation'],
      adapterToolName: toChiralityMcpAllowedToolName('domain_propose_operation')
    }),
    description:
      'Create (mode propose) or refresh (mode refresh) a pec import-proposal dry-run record over the D-APP-52 loopback-only (127.0.0.1) endpoint-allowlisted HTTP transport, acting as the owner-provisioned pec agent person; refresh mutates and voids any prior acceptance. The domain human gate — acceptance and application — lives in pec behind admin-only RBAC and is not tool-reachable (K-DOMAIN-3).',
    surface: 'chirality-mcp',
    permissions: ['workspace-write'],
    pathScope: 'project-root-read',
    idempotence: 'mutating',
    concurrency: 'serialized-by-path',
    interruptBehavior: 'block',
    resultBudget: WRITE_RESULT_BUDGET,
    provenance: {
      emits: TOOL_EVENTS,
      storeInput: 'metadata',
      storeOutput: 'metadata',
      recordsDiff: false
    },
    humanGate: {
      required: true,
      gate: 'interactive-confirmation',
      reason:
        'pec proposal-record mutations require workspaceWrite mode; domain acceptance/application remain human in-app acts behind pec admin-only RBAC (K-DOMAIN-3).'
    },
    adapter: {
      claudeAgentSdk: {
        toolName: toChiralityMcpAllowedToolName('domain_propose_operation')
      }
    },
    inputSchema: {
      type: 'object',
      required: ['profileId', 'projectId'],
      properties: {
        profileId: {
          type: 'string'
        },
        projectId: {
          type: 'integer',
          minimum: 1
        },
        mode: {
          type: 'string',
          enum: ['propose', 'refresh'],
          default: 'propose'
        },
        contract: {
          type: 'string',
          enum: ['mdl', 'rail', 'decisions', 'risks', 'schedule']
        },
        csvContent: {
          type: 'string'
        },
        csvFileRef: {
          type: 'string'
        },
        sourceName: {
          type: 'string'
        },
        proposalId: {
          type: 'integer',
          minimum: 1
        },
        expectedVersion: {
          type: 'integer'
        }
      }
    },
    outputSchema: {
      type: 'object',
      required: ['profileId', 'toolId', 'transportStatus']
    },
    runtime: {
      exposedToModel: true,
      reason:
        'D-APP-52 exposes the pec proposal write wrapper in workspaceWrite mode over the loopback-only endpoint-allowlisted HTTP transport with handler-level permission/evidence checks.'
    }
  },
  {
    name: 'domain_proposal_validate',
    aliases: uniqueDescriptorAliases({
      name: 'domain_proposal_validate',
      aliases: ['mcp.domain_proposal_validate', 'domain_proposal_validate'],
      adapterToolName: toChiralityMcpAllowedToolName('domain_proposal_validate')
    }),
    description:
      'Read a pec import-proposal record and its stored dry-run report over the D-APP-52 loopback-only (127.0.0.1) endpoint-allowlisted HTTP transport. GET only: never issues a POST, never recomputes, never mutates; staleness is inspectable via the stored dryRunAt/basisHistoryId.',
    surface: 'chirality-mcp',
    permissions: ['read'],
    pathScope: 'project-root-read',
    idempotence: 'input-dependent',
    concurrency: 'safe',
    interruptBehavior: 'cancel',
    resultBudget: READ_RESULT_BUDGET,
    provenance: {
      emits: TOOL_EVENTS,
      storeInput: 'metadata',
      storeOutput: 'inline-or-artifact',
      recordsDiff: false
    },
    humanGate: {
      required: false
    },
    adapter: {
      claudeAgentSdk: {
        toolName: toChiralityMcpAllowedToolName('domain_proposal_validate')
      }
    },
    inputSchema: {
      type: 'object',
      required: ['profileId', 'projectId', 'proposalId'],
      properties: {
        profileId: {
          type: 'string'
        },
        projectId: {
          type: 'integer',
          minimum: 1
        },
        proposalId: {
          type: 'integer',
          minimum: 1
        }
      }
    },
    outputSchema: {
      type: 'object',
      required: ['profileId', 'toolId', 'transportStatus']
    },
    runtime: {
      exposedToModel: true,
      reason:
        'D-APP-52 exposes the pec proposal read wrapper (GET-only, never recomputes) over the loopback-only endpoint-allowlisted HTTP transport.'
    }
  },
  {
    name: 'write_file',
    aliases: ['sdk.write'],
    description: 'Write a project-root-contained file after policy approval.',
    surface: 'claude-agent-sdk-builtin',
    permissions: ['workspace-write'],
    pathScope: 'project-root-write',
    idempotence: 'mutating',
    concurrency: 'serialized-by-path',
    interruptBehavior: 'block',
    resultBudget: WRITE_RESULT_BUDGET,
    provenance: {
      emits: TOOL_EVENTS,
      storeInput: 'metadata',
      storeOutput: 'metadata',
      recordsDiff: true
    },
    humanGate: {
      required: true,
      gate: 'interactive-confirmation',
      reason: 'Workspace writes require an accepted permission policy and human gate.'
    },
    adapter: {
      claudeAgentSdk: {
        toolName: 'Write'
      }
    },
    inputSchema: {
      type: 'object',
      required: ['file_path', 'content'],
      properties: {
        file_path: {
          type: 'string'
        },
        content: {
          type: 'string'
        }
      }
    },
    runtime: SDK_WRITE_RUNTIME
  },
  {
    name: 'edit_file',
    aliases: ['sdk.edit'],
    description: 'Apply an exact project-root-contained file edit after policy approval.',
    surface: 'claude-agent-sdk-builtin',
    permissions: ['workspace-write'],
    pathScope: 'project-root-write',
    idempotence: 'mutating',
    concurrency: 'serialized-by-path',
    interruptBehavior: 'block',
    resultBudget: WRITE_RESULT_BUDGET,
    provenance: {
      emits: TOOL_EVENTS,
      storeInput: 'metadata',
      storeOutput: 'metadata',
      recordsDiff: true
    },
    humanGate: {
      required: true,
      gate: 'interactive-confirmation',
      reason: 'File edits require path containment, diff provenance, and permission policy.'
    },
    adapter: {
      claudeAgentSdk: {
        toolName: 'Edit'
      }
    },
    inputSchema: {
      type: 'object',
      required: ['file_path', 'old_string', 'new_string'],
      properties: {
        file_path: {
          type: 'string'
        },
        old_string: {
          type: 'string'
        },
        new_string: {
          type: 'string'
        }
      }
    },
    runtime: SDK_WRITE_RUNTIME
  },
  {
    name: 'multi_edit_file',
    aliases: ['multi_edit', 'sdk.multiedit'],
    description: 'Apply multiple exact project-root-contained edits after policy approval.',
    surface: 'claude-agent-sdk-builtin',
    permissions: ['workspace-write'],
    pathScope: 'project-root-write',
    idempotence: 'mutating',
    concurrency: 'serialized-by-path',
    interruptBehavior: 'block',
    resultBudget: WRITE_RESULT_BUDGET,
    provenance: {
      emits: TOOL_EVENTS,
      storeInput: 'metadata',
      storeOutput: 'metadata',
      recordsDiff: true
    },
    humanGate: {
      required: true,
      gate: 'interactive-confirmation',
      reason: 'Multi-file edits require same-file serialization and accepted write policy.'
    },
    adapter: {
      claudeAgentSdk: {
        toolName: 'MultiEdit'
      }
    },
    inputSchema: {
      type: 'object',
      required: ['file_path', 'edits'],
      properties: {
        file_path: {
          type: 'string'
        },
        edits: {
          type: 'array'
        }
      }
    },
    runtime: DESCRIPTOR_ONLY_RUNTIME
  },
  {
    name: 'notebook_edit',
    aliases: ['sdk.notebookedit'],
    description: 'Reserved SDK notebook mutation surface; not part of the current Chirality runtime.',
    surface: 'reserved',
    permissions: ['workspace-write', 'danger'],
    pathScope: 'project-root-write',
    idempotence: 'mutating',
    concurrency: 'serialized-by-path',
    interruptBehavior: 'block',
    resultBudget: WRITE_RESULT_BUDGET,
    provenance: {
      emits: TOOL_EVENTS,
      storeInput: 'metadata',
      storeOutput: 'metadata',
      recordsDiff: true
    },
    humanGate: {
      required: true,
      gate: 'future-policy',
      reason: 'Notebook mutation is reserved until a product policy accepts notebook support.'
    },
    adapter: {
      claudeAgentSdk: {
        toolName: 'NotebookEdit'
      }
    },
    inputSchema: {
      type: 'object'
    },
    runtime: DESCRIPTOR_ONLY_RUNTIME
  },
  {
    name: 'shell',
    aliases: ['sdk.bash'],
    description: 'Run a project-root-contained shell command after shell policy and audit controls pass.',
    surface: 'claude-agent-sdk-builtin',
    permissions: ['shell', 'workspace-write', 'danger'],
    pathScope: 'project-root-write',
    idempotence: 'input-dependent',
    concurrency: 'exclusive',
    interruptBehavior: 'cancel',
    resultBudget: SHELL_RESULT_BUDGET,
    provenance: {
      emits: TOOL_EVENTS,
      storeInput: 'metadata',
      storeOutput: 'inline-or-artifact',
      recordsDiff: false
    },
    humanGate: {
      required: true,
      gate: 'interactive-confirmation',
      reason: 'Shell execution requires governed workspace mode, timeout, hook, and audit policy.'
    },
    adapter: {
      claudeAgentSdk: {
        toolName: 'Bash'
      }
    },
    inputSchema: {
      type: 'object',
      required: ['command'],
      properties: {
        command: {
          type: 'string'
        },
        timeout: {
          type: 'number'
        },
        description: {
          type: 'string'
        },
        run_in_background: {
          type: 'boolean'
        },
        dangerouslyDisableSandbox: {
          type: 'boolean'
        }
      }
    },
    runtime: SDK_SHELL_RUNTIME
  },
  {
    name: 'web_fetch',
    aliases: ['sdk.webfetch'],
    description: 'Reserved network fetch surface outside the current Anthropic-only runtime policy.',
    surface: 'reserved',
    permissions: ['network'],
    pathScope: 'external-network',
    idempotence: 'input-dependent',
    concurrency: 'safe',
    interruptBehavior: 'cancel',
    resultBudget: READ_RESULT_BUDGET,
    provenance: {
      emits: TOOL_EVENTS,
      storeInput: 'redacted',
      storeOutput: 'inline-or-artifact',
      recordsDiff: false
    },
    humanGate: {
      required: true,
      gate: 'future-policy',
      reason: 'Non-Anthropic network access requires a future governed scope amendment.'
    },
    adapter: {
      claudeAgentSdk: {
        toolName: 'WebFetch'
      }
    },
    inputSchema: {
      type: 'object'
    },
    runtime: DESCRIPTOR_ONLY_RUNTIME
  },
  {
    name: 'web_search',
    aliases: ['sdk.websearch'],
    description: 'Reserved network search surface outside the current Anthropic-only runtime policy.',
    surface: 'reserved',
    permissions: ['network'],
    pathScope: 'external-network',
    idempotence: 'input-dependent',
    concurrency: 'safe',
    interruptBehavior: 'cancel',
    resultBudget: READ_RESULT_BUDGET,
    provenance: {
      emits: TOOL_EVENTS,
      storeInput: 'redacted',
      storeOutput: 'inline-or-artifact',
      recordsDiff: false
    },
    humanGate: {
      required: true,
      gate: 'future-policy',
      reason: 'Non-Anthropic network access requires a future governed scope amendment.'
    },
    adapter: {
      claudeAgentSdk: {
        toolName: 'WebSearch'
      }
    },
    inputSchema: {
      type: 'object'
    },
    runtime: DESCRIPTOR_ONLY_RUNTIME
  },
  {
    name: 'agent',
    aliases: ['subagent', 'sdk.agent'],
    description: 'Invoke a governed subagent after Type 2 allowlist and parent-child audit policy exist.',
    surface: 'claude-agent-sdk-builtin',
    permissions: ['subagent'],
    pathScope: 'none',
    idempotence: 'input-dependent',
    concurrency: 'exclusive',
    interruptBehavior: 'cancel',
    resultBudget: READ_RESULT_BUDGET,
    provenance: {
      emits: ['tool.permission', 'subagent.started', 'subagent.completed', 'subagent.failed'],
      storeInput: 'metadata',
      storeOutput: 'inline-or-artifact',
      recordsDiff: false
    },
    humanGate: {
      required: true,
      gate: 'future-policy',
      reason: 'Subagent execution requires SDK agent definitions and fail-closed governance hooks.'
    },
    adapter: {
      claudeAgentSdk: {
        toolName: 'Agent'
      }
    },
    inputSchema: {
      type: 'object',
      required: ['agent'],
      properties: {
        agent: {
          type: 'string'
        }
      }
    },
    runtime: DESCRIPTOR_ONLY_RUNTIME
  }
] as const satisfies readonly HarnessToolDescriptor[];

type DescriptorLookupKeyKind = 'name' | 'alias' | 'adapter.claudeAgentSdk.toolName';

type DescriptorLookupRegistration = {
  descriptorName: string;
  rawKey: string;
  kind: DescriptorLookupKeyKind;
};

function addDescriptorLookupEntry(input: {
  lookup: Map<string, HarnessToolDescriptor>;
  registrations: Map<string, DescriptorLookupRegistration>;
  descriptor: HarnessToolDescriptor;
  rawKey: string;
  kind: DescriptorLookupKeyKind;
}): void {
  const normalizedKey = normalizeToolName(input.rawKey);
  const existing = input.registrations.get(normalizedKey);
  if (existing) {
    if (existing.descriptorName === input.descriptor.name) {
      return;
    }
    throw new Error(
      [
        `Duplicate harness tool descriptor key "${input.rawKey}" (${input.kind})`,
        `for "${input.descriptor.name}"; already registered`,
        `"${existing.rawKey}" (${existing.kind}) for "${existing.descriptorName}".`
      ].join(' ')
    );
  }
  input.registrations.set(normalizedKey, {
    descriptorName: input.descriptor.name,
    rawKey: input.rawKey,
    kind: input.kind
  });
  input.lookup.set(normalizedKey, input.descriptor);
}

export function createDescriptorLookup(
  descriptors: readonly HarnessToolDescriptor[] = HARNESS_TOOL_DESCRIPTORS
): Map<string, HarnessToolDescriptor> {
  const lookup = new Map<string, HarnessToolDescriptor>();
  const registrations = new Map<string, DescriptorLookupRegistration>();
  for (const descriptor of descriptors) {
    addDescriptorLookupEntry({
      lookup,
      registrations,
      descriptor,
      rawKey: descriptor.name,
      kind: 'name'
    });
    for (const alias of descriptor.aliases) {
      addDescriptorLookupEntry({
        lookup,
        registrations,
        descriptor,
        rawKey: alias,
        kind: 'alias'
      });
    }
    const sdkToolName = descriptor.adapter.claudeAgentSdk?.toolName;
    if (sdkToolName) {
      addDescriptorLookupEntry({
        lookup,
        registrations,
        descriptor,
        rawKey: sdkToolName,
        kind: 'adapter.claudeAgentSdk.toolName'
      });
    }
  }
  return lookup;
}

const DESCRIPTOR_LOOKUP = createDescriptorLookup();

function uniqueValues<T>(values: readonly T[]): T[] {
  return Array.from(new Set(values));
}

export function listHarnessToolDescriptors(): HarnessToolDescriptor[] {
  return [...HARNESS_TOOL_DESCRIPTORS];
}

export function getHarnessToolDescriptor(toolName: string): HarnessToolDescriptor | undefined {
  return DESCRIPTOR_LOOKUP.get(normalizeToolName(toolName));
}

export function getKnownHarnessToolNames(): string[] {
  return HARNESS_TOOL_DESCRIPTORS.map((descriptor) => descriptor.name);
}

function getSdkToolName(descriptor: HarnessToolDescriptor): ClaudeAgentSdkToolName | undefined {
  return descriptor.adapter.claudeAgentSdk?.toolName;
}

export function getCurrentTrancheDisallowedToolNames(
  allowedToolNames: readonly ClaudeAgentSdkToolName[] = []
): ClaudeAgentSdkToolName[] {
  const allowed = new Set(allowedToolNames);
  return uniqueValues(
    HARNESS_TOOL_DESCRIPTORS.flatMap((descriptor) => {
      const sdkToolName = getSdkToolName(descriptor);
      return sdkToolName && !allowed.has(sdkToolName) ? [sdkToolName] : [];
    })
  );
}
