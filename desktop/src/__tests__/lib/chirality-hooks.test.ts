import { mkdir, mkdtemp, readFile, rm, symlink, writeFile } from 'node:fs/promises';
import os from 'node:os';
import path from 'node:path';
import { afterEach, beforeEach, describe, expect, it } from 'vitest';
import { createChiralityToolHooks } from '../../lib/harness/chirality-hooks';
import { replayHarnessEvents } from '../../lib/harness/session-events';
import { getHarnessToolDescriptor } from '@chirality/runtime-contracts/tool-descriptor';

const sessionId = 'sess_chirality_hooks';
let tmpDir = '';
let projectRoot = '';
let instructionRoot = '';

beforeEach(async () => {
  tmpDir = await mkdtemp(path.join(os.tmpdir(), 'chirality-hooks-'));
  projectRoot = path.join(tmpDir, 'project');
  instructionRoot = path.join(projectRoot, 'instruction-root');
  await mkdir(projectRoot, { recursive: true });
  await mkdir(instructionRoot, { recursive: true });
  process.env.CHIRALITY_SESSION_ROOT = path.join(tmpDir, 'sessions');
  process.env.CHIRALITY_INSTRUCTION_ROOT = instructionRoot;
});

afterEach(async () => {
  delete process.env.CHIRALITY_SESSION_ROOT;
  delete process.env.CHIRALITY_INSTRUCTION_ROOT;
  delete process.env.CHIRALITY_ANTHROPIC_API_KEY;
  if (tmpDir) {
    await rm(tmpDir, { recursive: true, force: true });
    tmpDir = '';
  }
});

function getHooks(delegatedSubagents?: readonly string[]) {
  return createChiralityToolHooks({
    sessionId,
    projectRoot,
    instructionRoot,
    delegatedSubagents,
    resolveDescriptor: getHarnessToolDescriptor
  });
}

describe('Chirality write hooks', () => {
  it('allows project-root-contained Write and records post-write provenance metadata', async () => {
    const hooks = getHooks();
    const preToolUse = hooks.PreToolUse?.[0]?.hooks[0];
    const postToolUse = hooks.PostToolUse?.[0]?.hooks[0];
    expect(preToolUse).toBeTypeOf('function');
    expect(postToolUse).toBeTypeOf('function');

    const preResult = await preToolUse?.(
      {
        hook_event_name: 'PreToolUse',
        tool_name: 'Write',
        tool_input: {
          file_path: 'notes.md',
          content: 'after'
        },
        tool_use_id: 'tool_write'
      } as never,
      'tool_write',
      { signal: new AbortController().signal }
    );

    expect(preResult).toMatchObject({
      continue: true,
      hookSpecificOutput: {
        hookEventName: 'PreToolUse',
        permissionDecision: 'allow'
      }
    });

    await writeFile(path.join(projectRoot, 'notes.md'), 'after', 'utf8');

    const postResult = await postToolUse?.(
      {
        hook_event_name: 'PostToolUse',
        tool_name: 'Write',
        tool_input: {
          file_path: 'notes.md'
        },
        tool_response: {
          ok: true,
          content: [{ type: 'text', text: 'x'.repeat(17 * 1024) }]
        },
        tool_use_id: 'tool_write',
        duration_ms: 7
      } as never,
      'tool_write',
      { signal: new AbortController().signal }
    );

    expect(postResult).toMatchObject({
      continue: true,
      hookSpecificOutput: {
        hookEventName: 'PostToolUse'
      }
    });

    const replay = await replayHarnessEvents(sessionId);
    expect(replay.events.map((event) => event.type)).toEqual([
      'hook.started',
      'hook.completed',
      'hook.started',
      'hook.completed'
    ]);
    expect(replay.events[1].data).toMatchObject({
      hookName: 'chirality.write.pre_tool_use',
      decision: 'approve',
      descriptorName: 'write_file',
      pathMetadata: {
        rawPath: 'notes.md',
        resolvedPath: path.join(projectRoot, 'notes.md'),
        pathScope: 'project-root-write'
      },
      beforeState: {
        exists: false
      },
      recordsDiff: true
    });
    expect(replay.events[3].data).toMatchObject({
      hookName: 'chirality.write.post_tool_use',
      descriptorName: 'write_file',
      beforeState: {
        exists: false
      },
      afterState: {
        exists: true,
        kind: 'file',
        byteLength: 5,
        sha256: expect.any(String)
      },
      resultMetadata: {
        outputPersisted: true,
        budgetClass: 'requires-artifact-overflow',
        rawOutputPersisted: false
      },
      artifactMetadata: {
        artifactPath: expect.any(String),
        redacted: true,
        truncated: false
      },
      diffSummary: {
        beforeExists: false,
        afterExists: true,
        afterByteLength: 5,
        byteDelta: 5,
        beforeLineCount: 0,
        afterLineCount: 1,
        addedLineCount: 1,
        removedLineCount: 0,
        diffAlgorithm: 'bounded-lcs'
      },
      recordsDiff: true
    });

    const artifactMetadata = replay.events[3].data.artifactMetadata as
      | { artifactPath?: unknown }
      | undefined;
    const artifactPath = artifactMetadata?.artifactPath;
    expect(typeof artifactPath).toBe('string');
    const artifact = await readFile(artifactPath as string, 'utf8');
    expect(artifact).toContain('"ok": true');
  });

  it('blocks outside-root, instruction-root, and symlink write attempts', async () => {
    const externalRoot = path.join(tmpDir, 'external');
    await mkdir(externalRoot, { recursive: true });
    await writeFile(path.join(externalRoot, 'target.md'), 'outside', 'utf8');
    await symlink(externalRoot, path.join(projectRoot, 'linked'));

    const preToolUse = getHooks().PreToolUse?.[0]?.hooks[0];

    const outside = await preToolUse?.(
      {
        hook_event_name: 'PreToolUse',
        tool_name: 'Write',
        tool_input: {
          file_path: '../outside.md',
          content: 'outside'
        },
        tool_use_id: 'tool_outside'
      } as never,
      'tool_outside',
      { signal: new AbortController().signal }
    );
    const instruction = await preToolUse?.(
      {
        hook_event_name: 'PreToolUse',
        tool_name: 'Edit',
        tool_input: {
          file_path: path.join(instructionRoot, 'AGENT.md'),
          old_string: 'a',
          new_string: 'b'
        },
        tool_use_id: 'tool_instruction'
      } as never,
      'tool_instruction',
      { signal: new AbortController().signal }
    );
    const symlinked = await preToolUse?.(
      {
        hook_event_name: 'PreToolUse',
        tool_name: 'Write',
        tool_input: {
          file_path: 'linked/target.md',
          content: 'through symlink'
        },
        tool_use_id: 'tool_symlink'
      } as never,
      'tool_symlink',
      { signal: new AbortController().signal }
    );

    expect(outside).toMatchObject({
      continue: false,
      decision: 'block',
      hookSpecificOutput: {
        permissionDecision: 'deny'
      }
    });
    expect(JSON.stringify(outside)).toContain('outside the active project root');
    expect(instruction).toMatchObject({
      continue: false,
      decision: 'block',
      hookSpecificOutput: {
        permissionDecision: 'deny'
      }
    });
    expect(JSON.stringify(instruction)).toContain('instruction root');
    expect(symlinked).toMatchObject({
      continue: false,
      decision: 'block',
      hookSpecificOutput: {
        permissionDecision: 'deny'
      }
    });
    expect(JSON.stringify(symlinked)).toContain('symbolic link');

    const replay = await replayHarnessEvents(sessionId);
    expect(replay.events.map((event) => event.type)).toEqual([
      'hook.started',
      'hook.completed',
      'hook.started',
      'hook.completed',
      'hook.started',
      'hook.completed'
    ]);
    expect(replay.events[1].data.safeMetadata).toMatchObject({
      denyClass: 'path-containment'
    });
    expect(replay.events[3].data.safeMetadata).toMatchObject({
      denyClass: 'instruction-root'
    });
    expect(replay.events[5].data.safeMetadata).toMatchObject({
      denyClass: 'symlink-write'
    });
  });

  it('blocks Edit when old_string is missing from the target file before execution', async () => {
    await writeFile(path.join(projectRoot, 'notes.md'), 'before\n', 'utf8');
    const preToolUse = getHooks().PreToolUse?.[0]?.hooks[0];

    const result = await preToolUse?.(
      {
        hook_event_name: 'PreToolUse',
        tool_name: 'Edit',
        tool_input: {
          file_path: 'notes.md',
          old_string: 'not present',
          new_string: 'after'
        },
        tool_use_id: 'tool_edit_stale'
      } as never,
      'tool_edit_stale',
      { signal: new AbortController().signal }
    );

    expect(result).toMatchObject({
      continue: false,
      decision: 'block',
      hookSpecificOutput: {
        hookEventName: 'PreToolUse',
        permissionDecision: 'deny'
      }
    });
    expect(JSON.stringify(result)).toContain('old_string was not found');

    const replay = await replayHarnessEvents(sessionId);
    expect(replay.events.map((event) => event.type)).toEqual(['hook.started', 'hook.completed']);
    expect(replay.events[1].data).toMatchObject({
      hookName: 'chirality.write.pre_tool_use',
      decision: 'block',
      descriptorName: 'edit_file',
      safeMetadata: {
        denyClass: 'exact-edit-precondition',
        reason: 'old-string-not-found',
        oldStringByteLength: 11
      },
      beforeState: {
        exists: true,
        kind: 'file',
        byteLength: 7,
        sha256: expect.any(String)
      }
    });
  });

  it('allows Edit when old_string is present and records exact-edit metadata', async () => {
    await writeFile(path.join(projectRoot, 'notes.md'), 'before\n', 'utf8');
    const preToolUse = getHooks().PreToolUse?.[0]?.hooks[0];

    const result = await preToolUse?.(
      {
        hook_event_name: 'PreToolUse',
        tool_name: 'Edit',
        tool_input: {
          file_path: 'notes.md',
          old_string: 'before',
          new_string: 'after'
        },
        tool_use_id: 'tool_edit_exact'
      } as never,
      'tool_edit_exact',
      { signal: new AbortController().signal }
    );

    expect(result).toMatchObject({
      continue: true,
      hookSpecificOutput: {
        hookEventName: 'PreToolUse',
        permissionDecision: 'allow'
      }
    });

    const replay = await replayHarnessEvents(sessionId);
    expect(replay.events.map((event) => event.type)).toEqual(['hook.started', 'hook.completed']);
    expect(replay.events[1].data).toMatchObject({
      hookName: 'chirality.write.pre_tool_use',
      decision: 'approve',
      descriptorName: 'edit_file',
      exactEditPrecondition: {
        preconditionClass: 'exact-edit',
        oldStringByteLength: 6,
        oldStringMatchCount: 1
      }
    });
  });

  it('allows governed Bash, injects timeout, and records redacted overflow artifact metadata', async () => {
    process.env.CHIRALITY_ANTHROPIC_API_KEY = 'sk-test-secret';
    const hooks = getHooks();
    const preToolUse = hooks.PreToolUse?.[0]?.hooks[0];
    const postToolUse = hooks.PostToolUse?.[0]?.hooks[0];
    expect(preToolUse).toBeTypeOf('function');
    expect(postToolUse).toBeTypeOf('function');

    const preResult = await preToolUse?.(
      {
        hook_event_name: 'PreToolUse',
        tool_name: 'Bash',
        tool_input: {
          command: 'npm test'
        },
        tool_use_id: 'tool_bash'
      } as never,
      'tool_bash',
      { signal: new AbortController().signal }
    );

    expect(preResult).toMatchObject({
      continue: true,
      hookSpecificOutput: {
        hookEventName: 'PreToolUse',
        permissionDecision: 'allow',
        updatedInput: {
          command: 'npm test',
          timeout: 120000
        }
      }
    });

    const stdout = `${'x'.repeat(17 * 1024)} sk-test-secret`;
    const postResult = await postToolUse?.(
      {
        hook_event_name: 'PostToolUse',
        tool_name: 'Bash',
        tool_input: {
          command: 'npm test'
        },
        tool_response: {
          stdout,
          stderr: 'warning',
          interrupted: false
        },
        tool_use_id: 'tool_bash',
        duration_ms: 12
      } as never,
      'tool_bash',
      { signal: new AbortController().signal }
    );

    expect(postResult).toMatchObject({
      continue: true,
      hookSpecificOutput: {
        hookEventName: 'PostToolUse'
      }
    });

    const replay = await replayHarnessEvents(sessionId);
    expect(replay.events.map((event) => event.type)).toEqual([
      'hook.started',
      'hook.completed',
      'hook.started',
      'hook.completed'
    ]);
    expect(replay.events[1].data).toMatchObject({
      hookName: 'chirality.shell.pre_tool_use',
      decision: 'approve',
      descriptorName: 'shell',
      shellMetadata: {
        shellPolicyVersion: expect.any(String),
        effectiveTimeoutMs: 120000,
        timeoutSource: 'defaulted'
      }
    });
    expect(replay.events[3].data).toMatchObject({
      hookName: 'chirality.shell.post_tool_use',
      descriptorName: 'shell',
      resultMetadata: {
        outputPersisted: true,
        budgetClass: 'requires-artifact-overflow',
        rawOutputPersisted: false
      },
      shellResultMetadata: {
        stdoutPresent: true,
        stderrPresent: true,
        stdoutByteLength: expect.any(Number),
        stderrByteLength: 7,
        interrupted: false
      },
      artifactMetadata: {
        artifactPath: expect.any(String),
        redacted: true,
        truncated: false
      }
    });

    const artifactMetadata = replay.events[3].data.artifactMetadata as
      | { artifactPath?: unknown }
      | undefined;
    const artifactPath = artifactMetadata?.artifactPath;
    expect(typeof artifactPath).toBe('string');
    const artifact = await readFile(artifactPath as string, 'utf8');
    expect(artifact).not.toContain('sk-test-secret');
    expect(artifact).toContain('[REDACTED_API_KEY]');
  });

  it('blocks Bash network, instruction-root, and symlink redirection attempts', async () => {
    const externalRoot = path.join(tmpDir, 'external');
    await mkdir(externalRoot, { recursive: true });
    await writeFile(path.join(externalRoot, 'target.md'), 'outside', 'utf8');
    await symlink(externalRoot, path.join(projectRoot, 'linked'));

    const preToolUse = getHooks().PreToolUse?.[0]?.hooks[0];

    const network = await preToolUse?.(
      {
        hook_event_name: 'PreToolUse',
        tool_name: 'Bash',
        tool_input: {
          command: 'curl https://example.com'
        },
        tool_use_id: 'tool_bash_network'
      } as never,
      'tool_bash_network',
      { signal: new AbortController().signal }
    );
    const instruction = await preToolUse?.(
      {
        hook_event_name: 'PreToolUse',
        tool_name: 'Bash',
        tool_input: {
          command: `cat ${path.join(instructionRoot, 'AGENT.md')}`
        },
        tool_use_id: 'tool_bash_instruction'
      } as never,
      'tool_bash_instruction',
      { signal: new AbortController().signal }
    );
    const symlinked = await preToolUse?.(
      {
        hook_event_name: 'PreToolUse',
        tool_name: 'Bash',
        tool_input: {
          command: 'echo hi > linked/target.md'
        },
        tool_use_id: 'tool_bash_symlink'
      } as never,
      'tool_bash_symlink',
      { signal: new AbortController().signal }
    );

    expect(network).toMatchObject({
      continue: false,
      decision: 'block'
    });
    expect(JSON.stringify(network)).toContain('Network-capable Bash command');
    expect(instruction).toMatchObject({
      continue: false,
      decision: 'block'
    });
    expect(JSON.stringify(instruction)).toContain('instruction root');
    expect(symlinked).toMatchObject({
      continue: false,
      decision: 'block'
    });
    expect(JSON.stringify(symlinked)).toContain('symbolic link');

    const replay = await replayHarnessEvents(sessionId);
    expect(replay.events.map((event) => event.type)).toEqual([
      'hook.started',
      'hook.completed',
      'hook.started',
      'hook.completed',
      'hook.started',
      'hook.completed'
    ]);
    expect(replay.events[1].data.safeMetadata).toMatchObject({
      denyClass: 'network-command'
    });
    expect(replay.events[3].data.safeMetadata).toMatchObject({
      denyClass: 'instruction-root'
    });
    expect(replay.events[5].data.safeMetadata).toMatchObject({
      denyClass: 'symlink-write'
    });
  });

  it('blocks the retired Agent bridge even for formerly eligible children', async () => {
    const preToolUse = getHooks(['TASK']).PreToolUse?.[0]?.hooks[0];

    const result = await preToolUse?.(
      {
        hook_event_name: 'PreToolUse',
        tool_name: 'Agent',
        tool_input: {
          agent: 'TASK',
          prompt: 'run this'
        },
        tool_use_id: 'tool_agent'
      } as never,
      'tool_agent',
      { signal: new AbortController().signal }
    );

    expect(result).toMatchObject({
      continue: false,
      decision: 'block',
      hookSpecificOutput: {
        hookEventName: 'PreToolUse',
        permissionDecision: 'deny'
      }
    });

    const unknown = await preToolUse?.(
      {
        hook_event_name: 'PreToolUse',
        tool_name: 'Agent',
        tool_input: {
          agent: 'UNKNOWN',
          prompt: 'run this'
        },
        tool_use_id: 'tool_agent_unknown'
      } as never,
      'tool_agent_unknown',
      { signal: new AbortController().signal }
    );
    expect(unknown).toMatchObject({
      continue: false,
      decision: 'block',
      hookSpecificOutput: {
        permissionDecision: 'deny'
      }
    });

    const replay = await replayHarnessEvents(sessionId);
    expect(replay.events.map((event) => event.type)).toEqual([
      'hook.started',
      'hook.completed',
      'hook.started',
      'hook.completed'
    ]);
    expect(replay.events[1].data).toMatchObject({
      hookName: 'chirality.subagent.pre_tool_use',
      decision: 'block',
      descriptorName: 'agent',
      safeMetadata: {
        denyClass: 'subagent-execution',
        executionPosture: 'hard-denied',
        executableBridge: false,
        requestedAgent: 'TASK'
      }
    });
    expect(replay.events[3].data.safeMetadata).toMatchObject({
      denyClass: 'subagent-execution',
      requestedAgent: 'UNKNOWN'
    });
  });
});
