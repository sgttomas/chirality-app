import { describe, expect, it } from 'vitest';
import {
  buildHarnessOptsFromToolkit,
  defaultToolkitState,
  sanitizeToolkitState,
  upsertToolkitPreset
} from '../../lib/harness/toolkit';

describe('toolkit helpers', () => {
  it('builds no opts payload when values are empty', () => {
    const payload = buildHarnessOptsFromToolkit(defaultToolkitState().values);
    expect(payload).toBeUndefined();
  });

  it('builds opts payload from explicit tools/maxTurns values', () => {
    const payload = buildHarnessOptsFromToolkit({
      tools: 'bash, read_file\nwrite_file',
      maxTurns: '8',
      includeSubagentGovernance: false,
      contextSealed: false,
      pipelineRunApproved: false,
      approvalRef: ''
    });

    expect(payload).toEqual({
      tools: ['bash', 'read_file', 'write_file'],
      maxTurns: 8
    });
  });

  it('never emits opts.model: the model is a session-fixed catalog choice, not a toolkit value', () => {
    const payload = buildHarnessOptsFromToolkit({
      ...defaultToolkitState().values,
      ...({ model: 'stray-model' } as Record<string, unknown>),
      maxTurns: '2'
    });
    expect(payload).toEqual({ maxTurns: 2 });
    expect(payload).not.toHaveProperty('model');
  });

  it('includes subagentGovernance only when explicitly enabled', () => {
    const payload = buildHarnessOptsFromToolkit({
      tools: '',
      maxTurns: '',
      includeSubagentGovernance: true,
      contextSealed: true,
      pipelineRunApproved: false,
      approvalRef: 'APPROVAL-123'
    });

    expect(payload).toEqual({
      subagentGovernance: {
        contextSealed: true,
        pipelineRunApproved: false,
        approvalRef: 'APPROVAL-123'
      }
    });
  });

  it('sanitizes persisted toolkit state and clears dangling selectedPresetId', () => {
    const state = sanitizeToolkitState({
      visible: true,
      values: {
        model: '  claude-opus  ',
        tools: 'bash',
        maxTurns: '5',
        includeSubagentGovernance: true,
        contextSealed: true,
        pipelineRunApproved: true,
        approvalRef: ' APPROVAL '
      },
      presets: [
        {
          id: 'p1',
          name: ' Default ',
          values: {
            model: 'claude-opus',
            tools: 'bash',
            maxTurns: '5',
            includeSubagentGovernance: false,
            contextSealed: false,
            pipelineRunApproved: false,
            approvalRef: ''
          },
          createdAt: '2026-02-24T00:00:00.000Z',
          updatedAt: '2026-02-24T00:00:00.000Z'
        }
      ],
      selectedPresetId: 'missing'
    });

    expect(state.visible).toBe(true);
    expect(state.values).not.toHaveProperty('model');
    expect(state.presets[0].values).not.toHaveProperty('model');
    expect(state.values.approvalRef).toBe('APPROVAL');
    expect(state.presets).toHaveLength(1);
    expect(state.presets[0].name).toBe('Default');
    expect(state.selectedPresetId).toBeNull();
  });

  it('keeps newest preset at the front when upserting', () => {
    const next = upsertToolkitPreset(
      [
        {
          id: 'old',
          name: 'Old',
          values: defaultToolkitState().values,
          createdAt: '2026-02-24T00:00:00.000Z',
          updatedAt: '2026-02-24T00:00:00.000Z'
        }
      ],
      {
        id: 'new',
        name: 'New',
        values: defaultToolkitState().values,
        createdAt: '2026-02-24T00:01:00.000Z',
        updatedAt: '2026-02-24T00:01:00.000Z'
      }
    );

    expect(next.map((item) => item.id)).toEqual(['new', 'old']);
  });
});
