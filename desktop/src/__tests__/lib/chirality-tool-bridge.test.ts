import { mkdtemp, mkdir, rm, writeFile } from 'node:fs/promises';
import os from 'node:os';
import path from 'node:path';
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';
import { getHarnessToolDescriptor } from '@chirality/runtime-contracts/tool-descriptor';
import {
  createBoundedReadToolDefinitions,
  createChiralityToolDefinition,
  executeChiralityTool,
  type ChiralityToolExecutionContext
} from '../../lib/harness/chirality-tool-bridge';
import { bindChiralityToolsForClaude } from '../../lib/harness/claude-tool-binder';
import { bindChiralityToolsForPi } from '../../lib/harness/pi-tool-binder';
import { replayHarnessEvents } from '../../lib/harness/session-events';

let tempRoot: string;
let projectRoot: string;
let sessionRoot: string;
let previousSessionRoot: string | undefined;

function context(sessionId: string): ChiralityToolExecutionContext {
  return {
    projectRoot,
    sessionId,
    turnId: 'turn_tool_bridge',
    mode: 'readOnly',
    allowedReadScopes: [projectRoot]
  };
}

beforeEach(async () => {
  tempRoot = await mkdtemp(path.join(os.tmpdir(), 'chirality-tool-bridge-'));
  projectRoot = path.join(tempRoot, 'project');
  sessionRoot = path.join(tempRoot, 'sessions');
  await mkdir(projectRoot, { recursive: true });
  previousSessionRoot = process.env.CHIRALITY_SESSION_ROOT;
  process.env.CHIRALITY_SESSION_ROOT = sessionRoot;
});

afterEach(async () => {
  if (previousSessionRoot === undefined) {
    delete process.env.CHIRALITY_SESSION_ROOT;
  } else {
    process.env.CHIRALITY_SESSION_ROOT = previousSessionRoot;
  }
  await rm(tempRoot, { recursive: true, force: true });
});

describe('provider-neutral Chirality tool bridge', () => {
  it('returns equivalent allowed results through the Claude and Pi binders', async () => {
    const filePath = path.join(projectRoot, 'known.txt');
    await writeFile(filePath, 'known bounded content\n', 'utf8');
    const definitions = createBoundedReadToolDefinitions({
      context: context('sess_tool_bridge_equivalence'),
      allowedToolNames: ['read_file']
    });
    const claudeTools = bindChiralityToolsForClaude(definitions);
    const piTools = bindChiralityToolsForPi(definitions);

    expect(claudeTools.map((candidate) => candidate.name)).toEqual(['read_file']);
    expect(piTools.map((candidate) => candidate.name)).toEqual(['read_file']);

    const claudeResult = await claudeTools[0]!.handler({ file_path: 'known.txt' }, {});
    const piResult = await piTools[0]!.execute(
      'pi_tool_1',
      { file_path: 'known.txt' },
      undefined,
      undefined,
      {} as never
    );

    expect(piResult.content).toEqual(claudeResult.content);
    expect(piResult.content).toEqual([{ type: 'text', text: 'known bounded content\n' }]);
    expect(piResult.details).toEqual({
      source: 'chirality-tool-bridge',
      chiralityToolName: 'read_file',
      toolUseId: 'pi_tool_1'
    });
    expect(piTools[0]!.chirality).toEqual({
      descriptorName: 'read_file',
      permissions: ['read'],
      pathScope: 'project-root-read',
      readOnly: true,
      evidenceSource: 'chirality-tool-bridge'
    });

    const { events } = await replayHarnessEvents('sess_tool_bridge_equivalence');
    expect(events.map((event) => event.type)).toEqual([
      'tool.permission',
      'tool.started',
      'tool.completed',
      'tool.permission',
      'tool.started',
      'tool.completed'
    ]);
  });

  it('denies an escaping path before invoking the shared handler', async () => {
    const descriptor = getHarnessToolDescriptor('read_file');
    expect(descriptor).toBeDefined();
    const handler = vi.fn(async () => ({
      content: [{ type: 'text' as const, text: 'must not run' }]
    }));
    const definition = createChiralityToolDefinition({
      descriptor: descriptor!,
      context: context('sess_tool_bridge_denied'),
      handler
    });

    await expect(
      definition.execute({ file_path: '../outside.txt' }, { toolUseId: 'denied_tool_1' })
    ).rejects.toMatchObject({ status: 403 });
    expect(handler).not.toHaveBeenCalled();

    const { events } = await replayHarnessEvents('sess_tool_bridge_denied');
    expect(events.map((event) => event.type)).toEqual(['tool.permission']);
    expect(events[0]?.data).toMatchObject({
      behavior: 'deny',
      toolName: 'read_file',
      safeMetadata: {
        hardDeny: true,
        pathMetadata: {
          denyClass: 'path-containment'
        }
      }
    });
  });

  it('fails closed for malformed, extra, and unknown inputs without invoking a handler', async () => {
    const descriptor = getHarnessToolDescriptor('read_file');
    expect(descriptor).toBeDefined();
    const handler = vi.fn(async () => ({
      content: [{ type: 'text' as const, text: 'must not run' }]
    }));
    const definition = createChiralityToolDefinition({
      descriptor: descriptor!,
      context: context('sess_tool_bridge_invalid'),
      handler
    });

    await expect(definition.execute({})).rejects.toMatchObject({ status: 400 });
    await expect(
      definition.execute({ file_path: 'known.txt', unexpected: true })
    ).rejects.toMatchObject({ status: 400 });
    await expect(
      executeChiralityTool({
        definitions: [definition],
        toolName: 'ambient_shell',
        args: {}
      })
    ).rejects.toMatchObject({ status: 400 });
    await expect(
      Promise.resolve().then(() =>
        createBoundedReadToolDefinitions({
          context: context('sess_tool_bridge_invalid'),
          allowedToolNames: ['bash']
        })
      )
    ).rejects.toMatchObject({ status: 400 });
    expect(handler).not.toHaveBeenCalled();

    const bounded = createBoundedReadToolDefinitions({
      context: context('sess_tool_bridge_invalid'),
      allowedToolNames: ['read_file']
    });
    await expect(bounded[0]!.execute({ file_path: '' })).rejects.toMatchObject({ status: 400 });
  });

  it('binds only explicitly supplied tools and never adds native or ambient tools', () => {
    const definitions = createBoundedReadToolDefinitions({
      context: context('sess_tool_bridge_explicit'),
      allowedToolNames: ['read_file', 'read_file']
    });
    const claudeTools = bindChiralityToolsForClaude(definitions);
    const piTools = bindChiralityToolsForPi(definitions);

    expect(definitions).toHaveLength(1);
    expect(claudeTools.map((candidate) => candidate.name)).toEqual(['read_file']);
    expect(piTools.map((candidate) => candidate.name)).toEqual(['read_file']);
    expect(piTools.map((candidate) => candidate.name)).not.toEqual(
      expect.arrayContaining(['read', 'bash', 'write', 'edit', 'Agent', 'delegate_agent'])
    );
  });
});
