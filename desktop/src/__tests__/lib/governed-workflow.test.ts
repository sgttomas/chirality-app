import { describe, expect, it } from 'vitest';
import {
  advanceWorkflowAtGate, bindWorkflowContent, isCanonicalWorkflowFolder,
  nextWorkflowGate, parseGovernedWorkflow, serializeGovernedWorkflow,
  validateGovernedWorkflow, workflowSourceCurrency, type WorkflowVocabulary
} from '../../lib/workspace/governed-workflow';

// Fixture vocabulary only: production callers supply live role and setting registries.
const vocabulary: WorkflowVocabulary = {
  agent1Roles: ['WORKING_ITEMS', 'REVIEW'], permissions: ['WORK', 'REVIEW'],
  policies: ['none', 'ask-before-each-brief', 'approve-each-write', 'bounded-briefs'],
  briefsRunOn: ['local', 'hosted-account']
};
const digest = 'a'.repeat(64);
const example = `---
agent: WORKING_ITEMS
folder: /Users/alice/Project
permission: WORK
policy: bounded-briefs
briefsRunOn: local
roadmapSource:
  identity: agents/AGENT_WORKING_ITEMS.md
  sha256: ${digest}
acceptedAt: 2026-09-05T12:00:00.000Z
---

1. Prepare the package
2. [gate] Human accepts the brief
3. Produce the outputs
4. [gate] Human reviews the outputs
`;

const parse = (content = example) => parseGovernedWorkflow(content, vocabulary);

describe('governed workflow file contract', () => {
  it('round trips a derivative roadmap with source metadata and default initial position', () => {
    const workflow = parse();
    expect(workflow.current).toBe(1);
    expect(workflow.advancedBy).toBeNull();
    expect(workflow.roadmap[1]).toEqual({ text: 'Human accepts the brief', humanGate: true });
    expect(parse(serializeGovernedWorkflow(workflow, vocabulary))).toEqual(workflow);
    expect(parse(example.replace(/\n/g, '\r\n'))).toEqual(workflow);
    expect(workflow.acceptedAt).toBe('2026-09-05T12:00:00.000Z');
  });

  it('preserves quoted scalar punctuation and unicode without interpreting YAML', () => {
    const workflow = parse();
    workflow.roadmapSource.identity = 'template: "review" # élève';
    workflow.folder = '/Users/alice/Project A';
    expect(parse(serializeGovernedWorkflow(workflow, vocabulary))).toEqual(workflow);
  });

  it.each([
    ['missing opening', example.slice(4)],
    ['missing closing', example.replace('\n---\n\n1.', '\n\n1.')],
    ['duplicate key', example.replace('agent: WORKING_ITEMS', 'agent: WORKING_ITEMS\nagent: REVIEW')],
    ['duplicate nested key', example.replace('  sha256:', '  identity: other\n  sha256:')],
    ['missing key', example.replace('permission: WORK\n', '')],
    ['empty field', example.replace('policy: bounded-briefs', 'policy:')],
    ['unknown role', example.replace('WORKING_ITEMS', 'TASK')],
    ['unknown permission', example.replace('permission: WORK', 'permission: arbitrary')],
    ['unknown policy', example.replace('bounded-briefs', 'unbounded')],
    ['unknown briefs destination', example.replace('briefsRunOn: local', 'briefsRunOn: arbitrary')],
    ['YAML alias', example.replace('agent: WORKING_ITEMS', 'agent: *manager')],
    ['bad quote', example.replace('agent: WORKING_ITEMS', 'agent: "WORKING_ITEMS')],
    ['unknown source field', example.replace('  sha256:', '  approval: accepted\n  sha256:')],
    ['short hash', example.replace(digest, 'a'.repeat(63))],
    ['bad hex', example.replace(digest, 'z'.repeat(64))],
    ['invalid date', example.replace('2026-09-05', '2026-02-30')],
    ['timestamp without zone', example.replace('.000Z', '')],
    ['relative path', example.replace('/Users/alice/Project', 'Project')],
    ['traversal path', example.replace('/Users/alice/Project', '/Users/../Project')],
    ['empty roadmap', example.slice(0, example.indexOf('\n1.'))],
    ['unordered list', example.replace('1. Prepare', '- Prepare')],
    ['nonsequential list', example.replace('2. [gate]', '3. [gate]')],
    ['leading zero', example.replace('1. Prepare', '01. Prepare')],
    ['empty step', example.replace('1. Prepare the package', '1. ')],
    ['embedded gate', example.replace('1. Prepare', '1. Prepare [gate]')],
    ['checkbox status', example.replace('1. Prepare', '1. [x] Prepare')],
    ['extra prose', `${example}\nStatus: done`],
    ['noninteger current', `${example}\ncurrent: 1.5`],
    ['out of range', `${example}\ncurrent: 6\nadvancedBy: Alice`],
    ['duplicate current', `${example}\ncurrent: 1\ncurrent: 1`],
    ['initial attribution', `${example}\ncurrent: 1\nadvancedBy: Alice`],
    ['missing attribution', `${example}\ncurrent: 3`],
    ['attribution before position', `${example}\nadvancedBy: Alice`],
    ['duplicate attribution', `${example}\ncurrent: 3\nadvancedBy: Alice\nadvancedBy: Bob`],
    ['not after a gate', `${example}\ncurrent: 2\nadvancedBy: Alice`],
    ['misplaced step', `${example}\ncurrent: 1\n5. Extra`]
  ])('rejects %s', (_label, content) => {
    expect(() => parse(content)).toThrow();
  });

  it.each(['status', 'approvals', 'evidence', 'approval', 'title', '__proto__'])('refuses %s fields in files and values', (field) => {
    expect(() => parse(example.replace('agent:', `${field}: value\nagent:`))).toThrow();
    expect(() => validateGovernedWorkflow({ ...parse(), [field]: 'value' }, vocabulary)).toThrow();
    expect(() => serializeGovernedWorkflow({ ...parse(), [field]: 'value' }, vocabulary)).toThrow();
  });

  it('rejects nested extra state fields when serializing', () => {
    const workflow = parse();
    expect(() => serializeGovernedWorkflow({ ...workflow,
      roadmapSource: { ...workflow.roadmapSource, evidence: 'record' }
    } as typeof workflow, vocabulary)).toThrow();
    expect(() => serializeGovernedWorkflow({ ...workflow,
      roadmap: [{ ...workflow.roadmap[0], status: 'done' }]
    } as unknown as typeof workflow, vocabulary)).toThrow();
  });

  it('advances only at the next human gate, with attribution, without changing its input', () => {
    const workflow = parse();
    expect(nextWorkflowGate(workflow, vocabulary)).toBe(2);
    for (const gate of [1, 3, 4, -1, 2.5]) {
      expect(() => advanceWorkflowAtGate(workflow, gate, 'alice@example.test', vocabulary)).toThrow();
    }
    expect(() => advanceWorkflowAtGate(workflow, 2, '', vocabulary)).toThrow();
    const next = advanceWorkflowAtGate(workflow, 2, 'alice@example.test', vocabulary);
    expect(next.current).toBe(3);
    expect(next.advancedBy).toBe('alice@example.test');
    expect(workflow.current).toBe(1);
    expect(next.roadmap).not.toBe(workflow.roadmap);
    expect(parse(serializeGovernedWorkflow(next, vocabulary))).toEqual(next);
    expect(nextWorkflowGate(next, vocabulary)).toBe(4);
    const completed = advanceWorkflowAtGate(next, 4, 'bob@example.test', vocabulary);
    expect(completed.current).toBe(5);
    expect(completed.advancedBy).toBe('bob@example.test');
    expect(nextWorkflowGate(completed, vocabulary)).toBeNull();
    expect(() => advanceWorkflowAtGate(completed, 4, 'Bob', vocabulary)).toThrow();
  });

  it('cannot advance a roadmap without a human gate', () => {
    const workflow = parse(example.replaceAll('[gate] ', ''));
    expect(nextWorkflowGate(workflow, vocabulary)).toBeNull();
    expect(() => advanceWorkflowAtGate(workflow, 4, 'Alice', vocabulary)).toThrow();
  });

  it('binds a detached copy, retaining source identity/hash/acceptance date but resetting position and attribution', () => {
    const advanced = advanceWorkflowAtGate(parse(), 2, 'Alice', vocabulary);
    const content = serializeGovernedWorkflow(advanced, vocabulary);
    const copy = parse(bindWorkflowContent(content, '/Users/bob/Other', vocabulary));
    expect(copy.folder).toBe('/Users/bob/Other');
    expect(copy.current).toBe(1);
    expect(copy.advancedBy).toBeNull();
    expect(copy.roadmapSource).toEqual(advanced.roadmapSource);
    expect(copy.acceptedAt).toBe(advanced.acceptedAt);
    expect(parse(content)).toEqual(advanced);
    expect(() => bindWorkflowContent(content, '../Other', vocabulary)).toThrow();
  });

  it('reports source currency without rewriting either source', () => {
    const source = parse().roadmapSource;
    expect(workflowSourceCurrency(source, { ...source, sha256: digest.toUpperCase() })).toBe('current');
    expect(workflowSourceCurrency(source, { ...source, identity: 'other' })).toBe('changed');
    expect(workflowSourceCurrency(source, { ...source, sha256: 'b'.repeat(64) })).toBe('changed');
    expect(workflowSourceCurrency(source, null)).toBe('unavailable');
    expect(() => workflowSourceCurrency(source, { ...source, sha256: '' })).toThrow();
    expect(source.sha256).toBe(digest);
  });

  it.each(['relative', '/a//b', '/a/./b', '/a/../b', '/a/', '//host/a', 'C:\\root', '/a\\b', '/a\n'])('rejects noncanonical folder %s', (folder) => {
    expect(isCanonicalWorkflowFolder(folder)).toBe(false);
  });

  it('allows canonical POSIX root and ordinary spaces', () => {
    expect(isCanonicalWorkflowFolder('/')).toBe(true);
    expect(isCanonicalWorkflowFolder('/Users/Alice/Project A')).toBe(true);
  });
});
