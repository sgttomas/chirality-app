import { describe, expect, it } from 'vitest';
import { resolveHarnessToolPool } from '../../lib/harness/tool-pool';
import { createDescriptorLookup, getCurrentTrancheDisallowedToolNames, getHarnessToolDescriptor, HARNESS_TOOL_REGISTRY_VERSION, listHarnessToolDescriptors, type ClaudeAgentSdkToolName, type HarnessToolDescriptor } from '@chirality/runtime-contracts/tool-descriptor';
import { buildChiralityMcpTools } from '../../lib/harness/mcp/read-tools';
import {
  CHIRALITY_MCP_ALLOWED_TOOL_NAMES,
  type ChiralityMcpAllowedToolName
} from '@chirality/runtime-contracts/mcp/tool-names';

function normalizeLookupKey(toolName: string): string {
  return toolName.trim().toLowerCase();
}

function descriptorLookupKeys(descriptor: HarnessToolDescriptor): Array<{
  rawKey: string;
  kind: string;
}> {
  return [
    { rawKey: descriptor.name, kind: 'name' },
    ...descriptor.aliases.map((alias) => ({ rawKey: alias, kind: 'alias' })),
    ...(descriptor.adapter.claudeAgentSdk?.toolName
      ? [
          {
            rawKey: descriptor.adapter.claudeAgentSdk.toolName,
            kind: 'adapter.claudeAgentSdk.toolName'
          }
        ]
      : [])
  ];
}

function toRawChiralityMcpToolName(toolName: ChiralityMcpAllowedToolName): string {
  return toolName.replace(/^mcp__chirality__/, '');
}

const READ_MCP_TOOL_NAMES = [
  'mcp__chirality__status_read',
  'mcp__chirality__deps_read',
  'mcp__chirality__scope_scan',
  'mcp__chirality__scaffold_preview'
] as const;

const MUTATING_MCP_TOOL_NAMES = [
  'mcp__chirality__status_transition',
  'mcp__chirality__deps_write'
] as const;

const COORDINATION_MCP_TOOL_NAMES = [
  'mcp__chirality__delegate_agent',
  'mcp__chirality__report_coordination_notice',
  'mcp__chirality__send_agent_update',
  'mcp__chirality__ack_agent_update'
] as const;

const LIVE_DOMAIN_MCP_TOOL_NAMES = [
  'mcp__chirality__domain_completeness_check',
  'mcp__chirality__domain_rule_check_run',
  'mcp__chirality__domain_headless_preview_run'
] as const;

// D-APP-52: first live pec-scoped exposure of the two proposal tool names.
const PEC_PROPOSAL_DOMAIN_MCP_TOOL_NAMES = [
  'mcp__chirality__domain_propose_operation',
  'mcp__chirality__domain_proposal_validate'
] as const;

const DOMAIN_MCP_TOOL_NAMES = [
  ...LIVE_DOMAIN_MCP_TOOL_NAMES,
  ...PEC_PROPOSAL_DOMAIN_MCP_TOOL_NAMES
] as const;

const ALL_MCP_TOOL_NAMES = [
  ...READ_MCP_TOOL_NAMES,
  ...COORDINATION_MCP_TOOL_NAMES,
  ...MUTATING_MCP_TOOL_NAMES,
  ...DOMAIN_MCP_TOOL_NAMES
] as const;

describe('tool descriptor registry', () => {
  it('fails closed on duplicate descriptor lookup keys', () => {
    const [readFile] = listHarnessToolDescriptors();
    const duplicate: HarnessToolDescriptor = {
      ...readFile,
      name: 'duplicate_read_file',
      aliases: ['duplicate_read'],
      adapter: {
        claudeAgentSdk: {
          toolName: 'Read'
        }
      }
    };

    expect(() => createDescriptorLookup([readFile, duplicate])).toThrow(
      /Duplicate harness tool descriptor key "Read"/
    );
  });

  it('keeps descriptor names, aliases, and adapter tool names collision-free across descriptors', () => {
    const registrations = new Map<
      string,
      { descriptorName: string; rawKey: string; kind: string }
    >();

    for (const descriptor of listHarnessToolDescriptors()) {
      for (const key of descriptorLookupKeys(descriptor)) {
        const normalized = normalizeLookupKey(key.rawKey);
        const existing = registrations.get(normalized);
        if (existing) {
          expect(existing.descriptorName).toBe(descriptor.name);
          continue;
        }
        registrations.set(normalized, {
          descriptorName: descriptor.name,
          rawKey: key.rawKey,
          kind: key.kind
        });
      }
    }
  });

  it('keeps built-in SDK tool names disjoint from Chirality MCP adapter names', () => {
    const descriptors = listHarnessToolDescriptors();
    const builtinToolNames = descriptors
      .map((descriptor) => descriptor.adapter.claudeAgentSdk?.toolName)
      .filter((toolName): toolName is ClaudeAgentSdkToolName =>
        Boolean(toolName && !toolName.startsWith('mcp__chirality__'))
      );
    const chiralityMcpToolNames = descriptors
      .map((descriptor) => descriptor.adapter.claudeAgentSdk?.toolName)
      .filter((toolName): toolName is ChiralityMcpAllowedToolName =>
        Boolean(toolName?.startsWith('mcp__chirality__'))
      );

    expect(new Set(chiralityMcpToolNames)).toEqual(new Set(CHIRALITY_MCP_ALLOWED_TOOL_NAMES));
    expect(builtinToolNames.filter((toolName) => toolName.startsWith('mcp__chirality__'))).toEqual(
      []
    );
    expect(
      builtinToolNames.filter((toolName) => chiralityMcpToolNames.includes(toolName as ChiralityMcpAllowedToolName))
    ).toEqual([]);
  });

  it('keeps live Chirality MCP tool registrations in parity with descriptor metadata', () => {
    const liveToolNames = buildChiralityMcpTools({
      context: { projectRoot: '/tmp/chirality-project', sessionId: 'sess_descriptor_parity' },
      mode: 'workspaceWrite',
      allowedToolNames: CHIRALITY_MCP_ALLOWED_TOOL_NAMES
    }).map((definition) => (definition as { name: string }).name);
    const descriptorToolNames = listHarnessToolDescriptors()
      .filter((descriptor) => descriptor.surface === 'chirality-mcp')
      .map((descriptor) => descriptor.adapter.claudeAgentSdk?.toolName)
      .filter((toolName): toolName is ChiralityMcpAllowedToolName => Boolean(toolName))
      .map(toRawChiralityMcpToolName);

    expect(liveToolNames).toEqual(descriptorToolNames);
  });

  it('exposes read-class tools plus bounded Write/Edit descriptors for the current tranche', () => {
    const descriptors = listHarnessToolDescriptors();

    expect(descriptors.map((descriptor) => descriptor.name)).toEqual([
      'read_file',
      'find_files',
      'search_files',
      'list_files',
      'status_read',
      'dependency_read',
      'scope_scan',
      'scaffold_preview',
      'delegate_agent',
      'report_coordination_notice',
      'send_agent_update',
      'ack_agent_update',
      'status_transition',
      'dependency_write',
      'domain_completeness_check',
      'domain_rule_check_run',
      'domain_headless_preview_run',
      'domain_propose_operation',
      'domain_proposal_validate',
      'write_file',
      'edit_file',
      'multi_edit_file',
      'notebook_edit',
      'shell',
      'web_fetch',
      'web_search',
      'agent'
    ]);
    expect(
      descriptors
        .filter((descriptor) => descriptor.permissions.includes('read'))
        .map((descriptor) => descriptor.name)
    ).toEqual([
      'read_file',
      'find_files',
      'search_files',
      'list_files',
      'status_read',
      'dependency_read',
      'scope_scan',
      'scaffold_preview',
      'domain_completeness_check',
      'domain_rule_check_run',
      'domain_headless_preview_run',
      'domain_proposal_validate'
    ]);
    expect(
      descriptors
        .filter((descriptor) => descriptor.permissions.includes('read'))
        .every((descriptor) =>
          descriptor.surface === 'reserved'
            ? descriptor.runtime.exposedToModel === false
            : descriptor.runtime.exposedToModel === true
        )
    ).toBe(true);
    expect(
      descriptors
        .filter((descriptor) => ['write_file', 'edit_file'].includes(descriptor.name))
        .every((descriptor) => descriptor.runtime.exposedToModel === true)
    ).toBe(true);
    expect(
      descriptors
        .filter(
          (descriptor) =>
            !descriptor.permissions.includes('read') &&
            ![
              'status_transition',
              'dependency_write',
              'domain_propose_operation',
              'delegate_agent',
              'report_coordination_notice',
              'send_agent_update',
              'ack_agent_update',
              'write_file',
              'edit_file',
              'shell'
            ].includes(descriptor.name)
        )
        .every((descriptor) => descriptor.runtime.exposedToModel === false)
    ).toBe(true);

    const readFile = getHarnessToolDescriptor('read');
    expect(readFile?.permissions).toEqual(['read']);
    expect(readFile?.pathScope).toBe('project-root-read');
    expect(readFile?.humanGate.required).toBe(false);

    const writeFile = getHarnessToolDescriptor('Write');
    expect(writeFile?.permissions).toEqual(['workspace-write']);
    expect(writeFile?.pathScope).toBe('project-root-write');
    expect(writeFile?.humanGate.required).toBe(true);

    const bash = getHarnessToolDescriptor('bash');
    expect(bash?.permissions).toEqual(['shell', 'workspace-write', 'danger']);
    expect(bash?.pathScope).toBe('project-root-write');
    expect(bash?.humanGate.required).toBe(true);
    expect(bash?.runtime.exposedToModel).toBe(true);
  });

  it('registers D-APP-50 read-side domain MCP exposure including the DEC-065 headless tool', () => {
    const liveDomainDescriptors = LIVE_DOMAIN_MCP_TOOL_NAMES.map((toolName) =>
      getHarnessToolDescriptor(toolName)
    );

    expect(liveDomainDescriptors.map((descriptor) => descriptor?.name)).toEqual([
      'domain_completeness_check',
      'domain_rule_check_run',
      'domain_headless_preview_run'
    ]);
    for (const descriptor of liveDomainDescriptors) {
      expect(descriptor?.surface).toBe('chirality-mcp');
      expect(descriptor?.permissions).toEqual(['read']);
      expect(descriptor?.pathScope).toBe('project-root-read');
      expect(descriptor?.runtime.exposedToModel).toBe(true);
      expect(descriptor?.runtime.reason).toContain('D-APP-50');
      expect(descriptor?.humanGate).toEqual({ required: false });
      expect(descriptor?.provenance.recordsDiff).toBe(false);
    }

    expect(getHarnessToolDescriptor('domain_headless_preview_run')).toMatchObject({
      surface: 'chirality-mcp',
      permissions: ['read'],
      pathScope: 'project-root-read',
      idempotence: 'input-dependent',
      concurrency: 'exclusive',
      humanGate: { required: false },
      inputSchema: {
        required: ['profileId', 'runnerInputRef'],
        properties: {
          profileId: { const: 'open_pipe_stress' },
          runnerInputRef: { type: 'string' }
        }
      }
    });
    expect(
      [
        ...liveDomainDescriptors,
        ...PEC_PROPOSAL_DOMAIN_MCP_TOOL_NAMES.map((toolName) => getHarnessToolDescriptor(toolName))
      ].map((descriptor) => descriptor?.adapter.claudeAgentSdk?.toolName)
    ).toEqual(DOMAIN_MCP_TOOL_NAMES);
  });

  it('registers the D-APP-52 pec proposal tools live with unchanged grades and no apply surface', () => {
    const propose = getHarnessToolDescriptor('domain_propose_operation');
    expect(propose).toMatchObject({
      name: 'domain_propose_operation',
      surface: 'chirality-mcp',
      permissions: ['workspace-write'],
      pathScope: 'project-root-read',
      idempotence: 'mutating',
      interruptBehavior: 'block',
      humanGate: {
        required: true,
        gate: 'interactive-confirmation',
        reason: expect.stringContaining('K-DOMAIN-3')
      },
      runtime: {
        exposedToModel: true,
        reason: expect.stringContaining('D-APP-52')
      }
    });
    expect(propose?.description).toContain('loopback-only');
    expect(propose?.inputSchema).toMatchObject({
      required: ['profileId', 'projectId'],
      properties: expect.objectContaining({
        mode: expect.objectContaining({ enum: ['propose', 'refresh'] }),
        contract: expect.objectContaining({
          enum: ['mdl', 'rail', 'decisions', 'risks', 'schedule']
        }),
        csvContent: expect.anything(),
        csvFileRef: expect.anything(),
        proposalId: expect.anything(),
        expectedVersion: expect.anything()
      })
    });

    const validate = getHarnessToolDescriptor('domain_proposal_validate');
    expect(validate).toMatchObject({
      name: 'domain_proposal_validate',
      surface: 'chirality-mcp',
      permissions: ['read'],
      pathScope: 'project-root-read',
      humanGate: { required: false },
      provenance: expect.objectContaining({
        recordsDiff: false,
        storeOutput: 'inline-or-artifact'
      }),
      runtime: {
        exposedToModel: true,
        reason: expect.stringContaining('D-APP-52')
      }
    });
    expect(validate?.description).toContain('never recomputes');
    expect(validate?.inputSchema).toMatchObject({
      required: ['profileId', 'projectId', 'proposalId']
    });

    expect(HARNESS_TOOL_REGISTRY_VERSION).toBe('harness-tools.v14.headless-preview-live');

    // D-APP-50 rider-2 / D-APP-52 rider-5 pins: no accept/apply/force name
    // exists in any registry, under any alias.
    for (const absent of [
      'domain_apply',
      'domain_proposal_apply',
      'domain_proposal_accept',
      'domain_proposal_reject',
      'domain_proposal_force',
      'domain_force_apply',
      'mcp__chirality__domain_proposal_apply',
      'mcp__chirality__domain_proposal_accept'
    ]) {
      expect(getHarnessToolDescriptor(absent)).toBeUndefined();
    }
  });

  it('resolves Write/Edit/Bash only in workspaceWrite mode', () => {
    const resolution = resolveHarnessToolPool({
      requestedTools: ['read', 'write', 'Edit', 'multi_edit', 'bash'],
      mode: 'workspaceWrite'
    });

    expect(resolution.allowedToolNames).toEqual(['Read', 'Write', 'Edit', 'Bash']);
    expect(resolution.disallowedToolNames).toEqual([
      'Glob',
      'Grep',
      'LS',
      ...ALL_MCP_TOOL_NAMES,
      'MultiEdit',
      'NotebookEdit',
      'WebFetch',
      'WebSearch',
      'Agent'
    ]);
    expect(resolution.deniedTools).toEqual([
      expect.objectContaining({
        toolName: 'multi_edit',
        descriptorName: 'multi_edit_file'
      })
    ]);

    const askResolution = resolveHarnessToolPool({
      requestedTools: ['write', 'Edit'],
      mode: 'ask'
    });
    expect(askResolution.allowedToolNames).toEqual([]);
    expect(askResolution.disallowedToolNames).toContain('Write');
    expect(askResolution.disallowedToolNames).toContain('Edit');
  });

  it('resolves read-only Chirality MCP descriptors without opening write or shell tools', () => {
    const resolution = resolveHarnessToolPool({
      requestedTools: ['status_read', 'deps_read', 'scope_scan', 'scaffold_preview'],
      mode: 'readOnly'
    });

    expect(resolution.requestedDescriptors.map((descriptor) => descriptor.name)).toEqual([
      'status_read',
      'dependency_read',
      'scope_scan',
      'scaffold_preview'
    ]);
    expect(resolution.allowedToolNames).toEqual([
      'mcp__chirality__status_read',
      'mcp__chirality__deps_read',
      'mcp__chirality__scope_scan',
      'mcp__chirality__scaffold_preview'
    ]);
    expect(resolution.deniedTools).toEqual([]);
    expect(resolution.disallowedToolNames).toEqual([
      'Read',
      'Glob',
      'Grep',
      'LS',
      ...COORDINATION_MCP_TOOL_NAMES,
      ...MUTATING_MCP_TOOL_NAMES,
      ...DOMAIN_MCP_TOOL_NAMES,
      'Write',
      'Edit',
      'MultiEdit',
      'NotebookEdit',
      'Bash',
      'WebFetch',
      'WebSearch',
      'Agent'
    ]);
  });

  it('resolves mutating Chirality MCP descriptors only in workspaceWrite mode', () => {
    const resolution = resolveHarnessToolPool({
      requestedTools: ['status_transition', 'deps_write'],
      mode: 'workspaceWrite'
    });

    expect(resolution.requestedDescriptors.map((descriptor) => descriptor.name)).toEqual([
      'status_transition',
      'dependency_write'
    ]);
    expect(resolution.allowedToolNames).toEqual([
      'mcp__chirality__status_transition',
      'mcp__chirality__deps_write'
    ]);
    expect(resolution.deniedTools).toEqual([]);
    expect(resolution.disallowedToolNames).not.toContain('mcp__chirality__status_transition');
    expect(resolution.disallowedToolNames).not.toContain('mcp__chirality__deps_write');

    const readOnly = resolveHarnessToolPool({
      requestedTools: ['status_transition', 'deps_write'],
      mode: 'readOnly'
    });

    expect(readOnly.allowedToolNames).toEqual([]);
    expect(readOnly.disallowedToolNames).toContain('mcp__chirality__status_transition');
    expect(readOnly.disallowedToolNames).toContain('mcp__chirality__deps_write');
    expect(readOnly.deniedTools).toEqual([
      expect.objectContaining({
        toolName: 'status_transition',
        descriptorName: 'status_transition'
      }),
      expect.objectContaining({
        toolName: 'deps_write',
        descriptorName: 'dependency_write'
      })
    ]);
  });

  it('resolves D-APP-50 tranche-1 read-side domain MCP tools when explicitly requested', () => {
    const readOnly = resolveHarnessToolPool({
      requestedTools: ['domain_completeness_check', 'domain_rule_check_run'],
      mode: 'readOnly'
    });

    expect(readOnly.allowedToolNames).toEqual(LIVE_DOMAIN_MCP_TOOL_NAMES.slice(0, 2));
    expect(readOnly.disallowedToolNames).toEqual(
      getCurrentTrancheDisallowedToolNames(LIVE_DOMAIN_MCP_TOOL_NAMES.slice(0, 2))
    );
    expect(readOnly.deniedTools).toEqual([]);
    expect(
      buildChiralityMcpTools({
        context: { projectRoot: '/tmp/chirality-project', sessionId: 'sess_domain_read' },
        allowedToolNames: readOnly.allowedToolNames
      }).map((definition) => (definition as { name: string }).name)
    ).toEqual(['domain_completeness_check', 'domain_rule_check_run']);
  });

  it('resolves the D-APP-50 DEC-065 headless preview tool when explicitly requested', () => {
    const readOnly = resolveHarnessToolPool({
      requestedTools: ['domain_headless_preview_run'],
      mode: 'readOnly'
    });

    expect(readOnly.allowedToolNames).toEqual([
      'mcp__chirality__domain_headless_preview_run'
    ]);
    expect(readOnly.deniedTools).toEqual([]);
  });

  it('resolves the D-APP-52 pec proposal tools per their grades and modes', () => {
    // validate is read-grade: resolvable in readOnly mode.
    const readOnly = resolveHarnessToolPool({
      requestedTools: ['domain_proposal_validate', 'domain_propose_operation'],
      mode: 'readOnly'
    });
    expect(readOnly.allowedToolNames).toEqual(['mcp__chirality__domain_proposal_validate']);
    expect(readOnly.deniedTools).toEqual([
      expect.objectContaining({
        toolName: 'domain_propose_operation',
        descriptorName: 'domain_propose_operation',
        message: expect.stringContaining('denied in readOnly mode')
      })
    ]);

    // propose is workspace-write-grade: resolvable only in workspaceWrite mode.
    const workspaceWrite = resolveHarnessToolPool({
      requestedTools: ['domain_propose_operation', 'domain_proposal_validate'],
      mode: 'workspaceWrite'
    });
    expect(workspaceWrite.allowedToolNames).toEqual([
      'mcp__chirality__domain_propose_operation',
      'mcp__chirality__domain_proposal_validate'
    ]);
    expect(workspaceWrite.deniedTools).toEqual([]);

    expect(
      buildChiralityMcpTools({
        context: { projectRoot: '/tmp/chirality-project', sessionId: 'sess_pec_proposal_pool' },
        mode: 'workspaceWrite',
        allowedToolNames: workspaceWrite.allowedToolNames
      }).map((definition) => (definition as { name: string }).name)
    ).toEqual(['domain_propose_operation', 'domain_proposal_validate']);
  });

  it('resolves aliases deterministically and reports structured unknown tool issues', () => {
    const resolution = resolveHarnessToolPool({
      requestedTools: ['Read', 'read', 'bash', 'mystery', 'LS'],
      mode: 'readOnly'
    });

    expect(resolution.registryVersion).toBe(HARNESS_TOOL_REGISTRY_VERSION);
    expect(resolution.requestedTools).toEqual(['Read', 'read', 'bash', 'mystery', 'LS']);
    expect(resolution.requestedDescriptors.map((descriptor) => descriptor.name)).toEqual([
      'read_file',
      'shell',
      'list_files'
    ]);
    expect(
      resolution.permissionDecisions.map((decision) => ({
        toolName: decision.toolName,
        decision: decision.decision
      }))
    ).toEqual([
      { toolName: 'Read', decision: 'allow' },
      { toolName: 'bash', decision: 'deny' },
      { toolName: 'mystery', decision: 'deny' },
      { toolName: 'LS', decision: 'allow' }
    ]);
    expect(resolution.allowedToolNames).toEqual(['Read', 'LS']);
    expect(resolution.disallowedToolNames).toEqual(getCurrentTrancheDisallowedToolNames(['Read', 'LS']));
    expect(resolution.unknownTools).toEqual([
      expect.objectContaining({
        type: 'UNKNOWN_TOOL',
        toolName: 'mystery',
        knownTools: expect.arrayContaining(['read_file', 'list_files'])
      })
    ]);
    expect(resolution.deniedTools).toEqual([
      expect.objectContaining({
        type: 'DENIED_BY_CURRENT_PHASE',
        toolName: 'bash',
        descriptorName: 'shell'
      })
    ]);
  });

  it('keeps denied and unrequested tools out of the model context', () => {
    expect(getCurrentTrancheDisallowedToolNames()).toEqual([
      'Read',
      'Glob',
      'Grep',
      'LS',
      ...ALL_MCP_TOOL_NAMES,
      'Write',
      'Edit',
      'MultiEdit',
      'NotebookEdit',
      'Bash',
      'WebFetch',
      'WebSearch',
      'Agent'
    ]);
    expect(getCurrentTrancheDisallowedToolNames(['Read', 'Grep'])).toEqual([
      'Glob',
      'LS',
      ...ALL_MCP_TOOL_NAMES,
      'Write',
      'Edit',
      'MultiEdit',
      'NotebookEdit',
      'Bash',
      'WebFetch',
      'WebSearch',
      'Agent'
    ]);
  });
});
