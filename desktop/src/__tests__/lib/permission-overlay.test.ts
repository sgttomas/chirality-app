import { mkdir, mkdtemp, rm, symlink, writeFile } from 'node:fs/promises';
import os from 'node:os';
import path from 'node:path';
import { afterEach, describe, expect, it } from 'vitest';
import {
  createHarnessCanUseTool,
  HARNESS_PERMISSION_POLICY_VERSION,
  permissionDecisionToSdkResult,
  resolveHarnessPermissionDecision
} from '../../lib/harness/permission-overlay';
import { replayHarnessEvents } from '../../lib/harness/session-events';
import { getHarnessToolDescriptor } from '@chirality/runtime-contracts/tool-descriptor';

const sessionId = 'sess_permission_overlay';
let tmpDir = '';

async function useTempSessionRoot(): Promise<void> {
  tmpDir = await mkdtemp(path.join(os.tmpdir(), 'chirality-permission-overlay-'));
  process.env.CHIRALITY_SESSION_ROOT = path.join(tmpDir, 'sessions');
}

afterEach(async () => {
  delete process.env.CHIRALITY_SESSION_ROOT;
  delete process.env.CHIRALITY_INSTRUCTION_ROOT;
  if (tmpDir) {
    await rm(tmpDir, { recursive: true, force: true });
    tmpDir = '';
  }
});

function decisionFor(toolName: string, mode: string, explicitDeny = false) {
  return resolveHarnessPermissionDecision({
    sessionId,
    toolName,
    mode,
    descriptor: getHarnessToolDescriptor(toolName),
    explicitDeny,
    explicitDenyReason: explicitDeny ? 'Test hard deny.' : undefined
  });
}

describe('permission overlay', () => {
  it('allows read-class tools at the abstract policy layer', () => {
    const decision = decisionFor('Read', 'readOnly');

    expect(decision).toMatchObject({
      sessionId,
      toolName: 'Read',
      decision: 'allow',
      source: 'chirality-policy',
      reason: expect.stringContaining('allowed')
    });
    expect(decision.safeMetadata).toMatchObject({
      policyVersion: HARNESS_PERMISSION_POLICY_VERSION,
      mode: 'readOnly',
      descriptorName: 'read_file',
      adapterToolName: 'Read',
      allowClass: 'read'
    });
  });

  it('requires application approval for governed write surfaces in ask mode', () => {
    const decision = decisionFor('Write', 'ask');

    expect(decision).toMatchObject({
      decision: 'ask',
      reason: expect.stringContaining('requires interactive approval')
    });
    expect(decision.safeMetadata).toMatchObject({
      mode: 'ask',
      descriptorName: 'write_file',
      requiresHumanApproval: true
    });

    expect(permissionDecisionToSdkResult(decision, 'tool_1')).toMatchObject({
      behavior: 'deny',
      message: expect.stringContaining('requires application approval'),
      toolUseID: 'tool_1'
    });
  });

  it('allows governed write surfaces in workspaceWrite mode after hook policy', () => {
    const decision = decisionFor('Write', 'workspaceWrite');

    expect(decision).toMatchObject({
      decision: 'allow',
      reason: expect.stringContaining('workspaceWrite mode')
    });
    expect(decision.safeMetadata).toMatchObject({
      mode: 'workspaceWrite',
      descriptorName: 'write_file',
      allowClass: 'workspace-write',
      requiresHookApproval: true
    });

    expect(permissionDecisionToSdkResult(decision, 'tool_write')).toMatchObject({
      behavior: 'allow',
      toolUseID: 'tool_write'
    });
  });

  it('denies mutating coordination tools outside workspaceWrite mode', () => {
    const readOnly = decisionFor('mcp__chirality__delegate_agent', 'readOnly');
    const writable = decisionFor('mcp__chirality__delegate_agent', 'workspaceWrite');
    expect(readOnly).toMatchObject({
      decision: 'deny',
      safeMetadata: { denyClass: 'coordination-mode' }
    });
    expect(writable).toMatchObject({
      decision: 'allow',
      safeMetadata: { allowClass: 'coordination' }
    });
  });

  it('allows governed Bash only in workspaceWrite mode after shell hook policy', () => {
    const workspaceShell = decisionFor('Bash', 'workspaceWrite');
    const askShell = decisionFor('Bash', 'ask');
    const readOnlyShell = decisionFor('Bash', 'readOnly');

    expect(workspaceShell).toMatchObject({
      decision: 'allow',
      reason: expect.stringContaining('workspaceWrite mode')
    });
    expect(workspaceShell.safeMetadata).toMatchObject({
      mode: 'workspaceWrite',
      descriptorName: 'shell',
      allowClass: 'shell',
      requiresHookApproval: true
    });
    expect(permissionDecisionToSdkResult(workspaceShell, 'tool_bash')).toMatchObject({
      behavior: 'allow',
      toolUseID: 'tool_bash'
    });

    expect(askShell).toMatchObject({
      decision: 'ask',
      reason: expect.stringContaining('requires interactive approval')
    });
    expect(permissionDecisionToSdkResult(askShell, 'tool_bash_ask')).toMatchObject({
      behavior: 'deny',
      message: expect.stringContaining('requires application approval')
    });

    expect(readOnlyShell).toMatchObject({
      decision: 'deny',
      reason: expect.stringContaining('readOnly mode')
    });
  });

  it('lets explicit hard denies override abstract allow and ask decisions', () => {
    const readDecision = decisionFor('Read', 'readOnly', true);
    const writeDecision = decisionFor('Write', 'ask', true);

    expect(readDecision).toMatchObject({
      decision: 'deny',
      reason: 'Test hard deny.'
    });
    expect(readDecision.safeMetadata).toMatchObject({ hardDeny: true });
    expect(writeDecision).toMatchObject({
      decision: 'deny',
      reason: 'Test hard deny.'
    });
    expect(writeDecision.safeMetadata).toMatchObject({ hardDeny: true });
  });

  it('denies unapproved write, shell, network, subagent, and unknown tools in dontAsk mode', () => {
    const decisions = ['Write', 'Bash', 'WebFetch', 'Agent', 'mystery'].map((toolName) =>
      decisionFor(toolName, 'dontAsk')
    );

    expect(decisions.map((decision) => decision.decision)).toEqual([
      'deny',
      'deny',
      'deny',
      'deny',
      'deny'
    ]);
    expect(decisions.map((decision) => decision.safeMetadata?.denyClass)).toEqual([
      'workspace-write',
      'shell',
      'reserved-tool',
      'subagent-execution',
      'unknown-tool'
    ]);
    expect(decisions[3]).toMatchObject({
      reason: expect.stringContaining('legacy SDK Agent bridge is disabled')
    });
    expect(decisions[3].safeMetadata).toMatchObject({
      hardDeny: true,
      executableBridge: false,
      requiresSubagentPreflight: true
    });
  });

  it('denies the retired Agent bridge in every mode', () => {
    const workspaceDecision = resolveHarnessPermissionDecision({
      sessionId,
      toolName: 'Agent',
      mode: 'workspaceWrite',
      descriptor: getHarnessToolDescriptor('Agent'),
      toolInput: {
        agent: 'TASK',
        prompt: 'run this'
      },
      delegatedSubagents: ['TASK']
    });

    expect(workspaceDecision).toMatchObject({
      decision: 'deny',
      reason: expect.stringContaining('legacy SDK Agent bridge is disabled')
    });
    expect(workspaceDecision.safeMetadata).toMatchObject({
      denyClass: 'subagent-execution',
      executionPosture: 'hard-denied',
      executableBridge: false,
      childToolNames: [],
      childCapabilityInheritance: false
    });

    const askDecision = resolveHarnessPermissionDecision({
      sessionId,
      toolName: 'Agent',
      mode: 'ask',
      descriptor: getHarnessToolDescriptor('Agent'),
      toolInput: {
        agent: 'TASK'
      },
      delegatedSubagents: ['TASK']
    });
    expect(askDecision).toMatchObject({
      decision: 'deny',
      reason: expect.stringContaining('legacy SDK Agent bridge is disabled')
    });
  });

  it('keeps bypass mode subject to Chirality hard-deny rules', () => {
    const safeRead = decisionFor('Read', 'bypass');
    const shell = decisionFor('Bash', 'bypass');
    const explicit = decisionFor('Read', 'bypass', true);

    expect(safeRead.decision).toBe('allow');
    expect(shell).toMatchObject({
      decision: 'deny',
      reason: expect.stringContaining('bypass mode')
    });
    expect(explicit).toMatchObject({
      decision: 'deny',
      reason: 'Test hard deny.'
    });
  });

  it('hard-denies unsafe Bash callbacks before SDK execution', async () => {
    await useTempSessionRoot();
    const projectRoot = path.join(tmpDir, 'project');
    const instructionRoot = path.join(projectRoot, 'instruction-root');
    await mkdir(projectRoot, { recursive: true });
    await mkdir(instructionRoot, { recursive: true });
    process.env.CHIRALITY_INSTRUCTION_ROOT = instructionRoot;

    const canUseTool = createHarnessCanUseTool({
      sessionId,
      mode: 'workspaceWrite',
      projectRoot,
      resolveDescriptor: getHarnessToolDescriptor
    });

    await expect(
      canUseTool(
        'Bash',
        { command: 'npm test' },
        {
          signal: new AbortController().signal,
          toolUseID: 'tool_bash_allowed'
        }
      )
    ).resolves.toMatchObject({
      behavior: 'allow',
      toolUseID: 'tool_bash_allowed'
    });

    await expect(
      canUseTool(
        'Bash',
        { command: 'curl https://example.com' },
        {
          signal: new AbortController().signal,
          toolUseID: 'tool_bash_network'
        }
      )
    ).resolves.toMatchObject({
      behavior: 'deny',
      message: expect.stringContaining('Network-capable Bash command')
    });

    await expect(
      canUseTool(
        'Bash',
        { command: 'node scripts/check.js', dangerouslyDisableSandbox: true },
        {
          signal: new AbortController().signal,
          toolUseID: 'tool_bash_sandbox'
        }
      )
    ).resolves.toMatchObject({
      behavior: 'deny',
      message: expect.stringContaining('sandbox override')
    });

    await expect(
      canUseTool(
        'Bash',
        { command: 'echo outside > ../outside.txt' },
        {
          signal: new AbortController().signal,
          toolUseID: 'tool_bash_outside'
        }
      )
    ).resolves.toMatchObject({
      behavior: 'deny',
      message: expect.stringContaining('parent-directory traversal')
    });

    const replay = await replayHarnessEvents(sessionId);
    expect(replay.events.map((event) => event.type)).toEqual([
      'tool.permission',
      'tool.permission',
      'tool.permission',
      'tool.permission'
    ]);
    expect(replay.events.map((event) => event.data.behavior)).toEqual([
      'allow',
      'deny',
      'deny',
      'deny'
    ]);
    expect(replay.events[0].data.safeMetadata).toMatchObject({
      shellMetadata: {
        shellPolicyVersion: expect.any(String),
        effectiveTimeoutMs: 120000,
        timeoutSource: 'defaulted'
      }
    });
    expect(replay.events[1].data.safeMetadata).toMatchObject({
      denyClass: 'network-command'
    });
    expect(replay.events[2].data.safeMetadata).toMatchObject({
      denyClass: 'sandbox-override'
    });
    expect(replay.events[3].data.safeMetadata).toMatchObject({
      denyClass: 'path-traversal'
    });
  });

  it('hard-denies path-bearing read callbacks outside the active project root', async () => {
    await useTempSessionRoot();
    const projectRoot = path.join(tmpDir, 'project');
    await mkdir(path.join(projectRoot, 'PKG-01'), { recursive: true });
    const canUseTool = createHarnessCanUseTool({
      sessionId,
      mode: 'readOnly',
      projectRoot,
      resolveDescriptor: getHarnessToolDescriptor
    });

    await expect(
      canUseTool(
        'Read',
        { file_path: '../outside.md' },
        {
          signal: new AbortController().signal,
          toolUseID: 'tool_outside'
        }
      )
    ).resolves.toMatchObject({
      behavior: 'deny',
      message: expect.stringContaining('outside the active project root'),
      toolUseID: 'tool_outside'
    });

    await expect(
      canUseTool(
        'LS',
        { path: 'PKG-01' },
        {
          signal: new AbortController().signal,
          toolUseID: 'tool_inside'
        }
      )
    ).resolves.toMatchObject({
      behavior: 'allow',
      toolUseID: 'tool_inside'
    });

    const replay = await replayHarnessEvents(sessionId);
    expect(replay.events.map((event) => event.type)).toEqual([
      'tool.permission',
      'tool.permission'
    ]);
    expect(replay.events[0]).toMatchObject({
      sessionId,
      type: 'tool.permission',
      data: {
        behavior: 'deny',
        decisionId: expect.stringMatching(/^perm_/),
        descriptorName: 'read_file',
        adapterToolName: 'Read',
        mode: 'readOnly',
        surface: 'claude-agent-sdk-builtin'
      }
    });
    expect(replay.events[0].data.safeMetadata).toMatchObject({
      inputMetadata: {
        inputKeys: ['file_path'],
        pathFields: {
          file_path: '../outside.md'
        }
      },
      denyClass: 'path-containment'
    });
    expect(replay.events[1]).toMatchObject({
      type: 'tool.permission',
      data: {
        behavior: 'allow',
        descriptorName: 'list_files',
        adapterToolName: 'LS'
      }
    });
  });

  it('enforces managed child read scopes, write targets, and fail-closed shell boundaries', async () => {
    await useTempSessionRoot();
    const projectRoot = path.join(tmpDir, 'project');
    const packageRoot = path.join(projectRoot, 'PKG-01');
    await mkdir(packageRoot, { recursive: true });
    const canUseTool = createHarnessCanUseTool({
      sessionId,
      mode: 'workspaceWrite',
      projectRoot,
      allowedReadScopes: [packageRoot],
      allowedWriteTargets: [packageRoot],
      resolveDescriptor: getHarnessToolDescriptor
    });

    const options = (toolUseID: string) => ({
      signal: new AbortController().signal,
      toolUseID
    });
    await expect(
      canUseTool('Read', { file_path: 'PKG-01/in.md' }, options('managed_read_inside'))
    ).resolves.toMatchObject({ behavior: 'allow' });
    await expect(
      canUseTool('Read', { file_path: 'PKG-02/out.md' }, options('managed_read_outside'))
    ).resolves.toMatchObject({
      behavior: 'deny',
      message: expect.stringContaining('declared read scope')
    });
    await expect(
      canUseTool('Glob', { pattern: '**/*.md' }, options('managed_unbounded_glob'))
    ).resolves.toMatchObject({
      behavior: 'deny',
      message: expect.stringContaining('requires an explicit path')
    });
    await expect(
      canUseTool(
        'Write',
        { file_path: 'PKG-01/out.md', content: 'inside' },
        options('managed_write_inside')
      )
    ).resolves.toMatchObject({ behavior: 'allow' });
    await expect(
      canUseTool(
        'Write',
        { file_path: 'PKG-02/out.md', content: 'outside' },
        options('managed_write_outside')
      )
    ).resolves.toMatchObject({
      behavior: 'deny',
      message: expect.stringContaining('declared write targets')
    });
    await expect(
      canUseTool('Bash', { command: 'npm test' }, options('managed_shell'))
    ).resolves.toMatchObject({
      behavior: 'deny',
      message: expect.stringContaining('Bash is denied for a managed child')
    });
  });

  it('hard-denies unsafe write callback paths before SDK execution', async () => {
    await useTempSessionRoot();
    const projectRoot = path.join(tmpDir, 'project');
    const instructionRoot = path.join(projectRoot, 'instruction-root');
    const externalRoot = path.join(tmpDir, 'external');
    await mkdir(projectRoot, { recursive: true });
    await mkdir(instructionRoot, { recursive: true });
    await mkdir(externalRoot, { recursive: true });
    await writeFile(path.join(externalRoot, 'target.md'), 'outside', 'utf8');
    await symlink(externalRoot, path.join(projectRoot, 'linked'));
    process.env.CHIRALITY_INSTRUCTION_ROOT = instructionRoot;

    const canUseTool = createHarnessCanUseTool({
      sessionId,
      mode: 'workspaceWrite',
      projectRoot,
      resolveDescriptor: getHarnessToolDescriptor
    });

    await expect(
      canUseTool(
        'Write',
        { file_path: 'notes.md', content: 'inside' },
        {
          signal: new AbortController().signal,
          toolUseID: 'tool_inside_write'
        }
      )
    ).resolves.toMatchObject({
      behavior: 'allow',
      toolUseID: 'tool_inside_write'
    });

    await expect(
      canUseTool(
        'Write',
        { file_path: '../outside.md', content: 'outside' },
        {
          signal: new AbortController().signal,
          toolUseID: 'tool_outside_write'
        }
      )
    ).resolves.toMatchObject({
      behavior: 'deny',
      message: expect.stringContaining('outside the active project root')
    });

    await expect(
      canUseTool(
        'Edit',
        { file_path: path.join(instructionRoot, 'AGENT.md'), old_string: 'a', new_string: 'b' },
        {
          signal: new AbortController().signal,
          toolUseID: 'tool_instruction_write'
        }
      )
    ).resolves.toMatchObject({
      behavior: 'deny',
      message: expect.stringContaining('instruction root')
    });

    await expect(
      canUseTool(
        'Write',
        { file_path: 'linked/target.md', content: 'through symlink' },
        {
          signal: new AbortController().signal,
          toolUseID: 'tool_symlink_write'
        }
      )
    ).resolves.toMatchObject({
      behavior: 'deny',
      message: expect.stringContaining('symbolic link')
    });

    await expect(
      canUseTool(
        'Read',
        { file_path: 'linked/target.md' },
        {
          signal: new AbortController().signal,
          toolUseID: 'tool_symlink_read'
        }
      )
    ).resolves.toMatchObject({
      behavior: 'deny',
      message: expect.stringContaining('symbolic link')
    });

    const replay = await replayHarnessEvents(sessionId);
    expect(replay.events.map((event) => event.type)).toEqual([
      'tool.permission',
      'tool.permission',
      'tool.permission',
      'tool.permission',
      'tool.permission'
    ]);
    expect(replay.events.map((event) => event.data.behavior)).toEqual([
      'allow',
      'deny',
      'deny',
      'deny',
      'deny'
    ]);
    expect(replay.events[1].data.safeMetadata).toMatchObject({
      denyClass: 'path-containment'
    });
    expect(replay.events[2].data.safeMetadata).toMatchObject({
      denyClass: 'instruction-root'
    });
    expect(replay.events[3].data.safeMetadata).toMatchObject({
      denyClass: 'symlink-write'
    });
    expect(replay.events[4].data.safeMetadata).toMatchObject({
      denyClass: 'symlink-read'
    });
  });
});
