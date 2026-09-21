import { afterEach, describe, expect, it } from 'vitest';
import {
  isToolResultFailure,
  summarizeShellResultStreams,
  summarizeToolInput,
  summarizeToolResult,
  withToolResultPersistence
} from '../../lib/harness/tool-evidence';
import { getHarnessToolDescriptor } from '@chirality/runtime-contracts/tool-descriptor';

afterEach(() => {
  delete process.env.CHIRALITY_ANTHROPIC_API_KEY;
});

describe('tool evidence summaries', () => {
  it('stores only input metadata and safe path fields', () => {
    const summary = summarizeToolInput({
      file_path: 'docs/SPEC.md',
      content: 'raw file body',
      nested: {
        value: true
      }
    });

    expect(summary).toEqual({
      inputType: 'object',
      inputKeys: ['content', 'file_path', 'nested'],
      pathFields: {
        file_path: 'docs/SPEC.md'
      }
    });
  });

  it('classifies result budgets without storing raw result text', () => {
    const descriptor = getHarnessToolDescriptor('Read');
    const result = {
      type: 'tool_result',
      content: [
        {
          type: 'text',
          text: 'x'.repeat(70 * 1024)
        }
      ]
    };

    const summary = summarizeToolResult(result, descriptor);

    expect(summary).toMatchObject({
      contentItemCount: 1,
      contentTextByteLength: 70 * 1024,
      contentTypes: ['text'],
      inlineByteLimit: 65536,
      artifactByteLimit: 2097152,
      overflowPolicy: 'artifact',
      budgetClass: 'requires-artifact-overflow',
      outputPersisted: false,
      rawOutputPersisted: false
    });
    expect(JSON.stringify(summary)).not.toContain('x'.repeat(128));
  });

  it('marks persistence separately from result-size classification', () => {
    const descriptor = getHarnessToolDescriptor('Write');
    const summary = withToolResultPersistence(
      summarizeToolResult({ ok: true }, descriptor),
      true
    );

    expect(summary).toMatchObject({
      budgetClass: 'within-inline-budget',
      outputPersisted: true,
      rawOutputPersisted: false
    });
  });

  it('summarizes shell streams as byte counts and flags only', () => {
    const summary = summarizeShellResultStreams({
      stdout: 'test output',
      stderr: 'warning',
      interrupted: false,
      rawOutputPath: '/tmp/raw.log',
      dangerouslyDisableSandbox: false
    });

    expect(summary).toEqual({
      stdoutPresent: true,
      stderrPresent: true,
      stdoutByteLength: 11,
      stderrByteLength: 7,
      interrupted: false,
      isImage: undefined,
      backgroundTask: false,
      backgroundedByUser: undefined,
      assistantAutoBackgrounded: undefined,
      rawOutputPathPresent: true,
      dangerouslyDisableSandbox: false
    });
  });

  it('treats interrupted tool results as non-success outcomes', () => {
    expect(isToolResultFailure({ type: 'tool_result', interrupted: true })).toBe(true);
    expect(isToolResultFailure({ type: 'tool_result', interrupted: false })).toBe(false);
    expect(isToolResultFailure({ type: 'tool_result', is_error: true })).toBe(true);
    expect(isToolResultFailure({ type: 'tool_result', isError: true })).toBe(true);
  });
});
