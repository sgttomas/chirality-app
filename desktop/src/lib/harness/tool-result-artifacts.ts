import { Buffer } from 'node:buffer';
import { createHash } from 'node:crypto';
import { mkdir, writeFile } from 'node:fs/promises';
import path from 'node:path';
import { redactJsonLike } from './run-logger';
import type { HarnessToolDescriptor } from '@chirality/runtime-contracts/tool-descriptor';

export type ToolResultArtifactMetadata = {
  artifactPath: string;
  artifactRelativePath: string;
  artifactByteLength: number;
  originalByteLength: number;
  sha256: string;
  toolName?: string;
  turnId?: string;
  retentionPolicy: 'session-lifetime';
  redacted: true;
  truncated: boolean;
};

export type ChildOutputArtifactMetadata = {
  artifactPath: string;
  artifactRelativePath: string;
  artifactByteLength: number;
  originalByteLength: number;
  sha256: string;
  toolName: 'Agent';
  turnId?: string;
  taskId?: string;
  childRunId?: string;
  toolUseId?: string;
  sourceOutputFile?: string;
  retentionPolicy: 'session-lifetime';
  redacted: true;
  truncated: boolean;
};

const CHILD_OUTPUT_INLINE_BYTE_LIMIT = 16 * 1024;
const CHILD_OUTPUT_ARTIFACT_BYTE_LIMIT = 512 * 1024;

function getSessionRootDirectory(): string {
  return process.env.CHIRALITY_SESSION_ROOT ?? path.join(process.cwd(), '.chirality', 'sessions');
}

function safePathSegment(value: string | undefined, fallback: string): string {
  const candidate = value?.replace(/[^A-Za-z0-9_.-]/g, '_').slice(0, 80);
  return candidate && candidate.length > 0 ? candidate : fallback;
}

function byteLength(value: string): number {
  return Buffer.byteLength(value, 'utf8');
}

function sha256Hex(value: string): string {
  return createHash('sha256').update(value, 'utf8').digest('hex');
}

export async function persistToolResultArtifact(input: {
  sessionId: string;
  turnId?: string;
  toolUseId?: string;
  toolName?: string;
  descriptor?: HarnessToolDescriptor;
  result: unknown;
}): Promise<ToolResultArtifactMetadata | undefined> {
  const budget = input.descriptor?.resultBudget;
  if (!budget || budget.overflow !== 'artifact') {
    return undefined;
  }

  const redactedResult = redactJsonLike(input.result);
  const toolName =
    input.toolName ?? input.descriptor?.name ?? input.descriptor?.adapter.claudeAgentSdk?.toolName;
  const serialized = `${JSON.stringify(
    {
      schemaVersion: 1,
      toolName,
      toolUseId: input.toolUseId,
      turnId: input.turnId,
      descriptorName: input.descriptor?.name,
      adapterToolName: input.descriptor?.adapter.claudeAgentSdk?.toolName,
      redacted: true,
      result: redactedResult
    },
    null,
    2
  )}\n`;
  const originalByteLength = byteLength(serialized);
  if (originalByteLength <= budget.inlineByteLimit) {
    return undefined;
  }

  const truncated = originalByteLength > budget.artifactByteLimit;
  const content = truncated
    ? `${JSON.stringify(
        {
          schemaVersion: 1,
          toolName,
          toolUseId: input.toolUseId,
          turnId: input.turnId,
          descriptorName: input.descriptor?.name,
          adapterToolName: input.descriptor?.adapter.claudeAgentSdk?.toolName,
          redacted: true,
          truncated: true,
          originalByteLength,
          preview: serialized.slice(0, budget.inlineByteLimit)
        },
        null,
        2
      )}\n`
    : serialized;

  const artifactRelativePath = path.join(
    input.sessionId,
    'artifacts',
    'tools',
    `${safePathSegment(input.toolUseId, 'tool-result')}-${safePathSegment(
      input.toolName,
      'tool'
    )}.json`
  );
  const artifactPath = path.join(getSessionRootDirectory(), artifactRelativePath);
  await mkdir(path.dirname(artifactPath), { recursive: true });
  await writeFile(artifactPath, content, 'utf8');
  const artifactByteLength = byteLength(content);

  return {
    artifactPath,
    artifactRelativePath,
    artifactByteLength,
    originalByteLength,
    sha256: sha256Hex(content),
    toolName,
    turnId: input.turnId,
    retentionPolicy: 'session-lifetime',
    redacted: true,
    truncated
  };
}

export async function persistChildOutputArtifact(input: {
  sessionId: string;
  turnId?: string;
  taskId?: string;
  childRunId?: string;
  toolUseId?: string;
  agentName?: string;
  status?: string;
  outputFile?: string;
  summary?: string;
  usage?: unknown;
  skipTranscript?: boolean;
}): Promise<ChildOutputArtifactMetadata | undefined> {
  const serialized = `${JSON.stringify(
    {
      schemaVersion: 1,
      artifactKind: 'subagent-output',
      toolName: 'Agent',
      turnId: input.turnId,
      taskId: input.taskId,
      childRunId: input.childRunId,
      toolUseId: input.toolUseId,
      agentName: input.agentName,
      status: input.status,
      sourceOutputFile: input.outputFile,
      skipTranscript: input.skipTranscript,
      redacted: true,
      output: redactJsonLike({
        summary: input.summary,
        usage: input.usage
      })
    },
    null,
    2
  )}\n`;
  const originalByteLength = byteLength(serialized);
  if (originalByteLength <= CHILD_OUTPUT_INLINE_BYTE_LIMIT) {
    return undefined;
  }

  const truncated = originalByteLength > CHILD_OUTPUT_ARTIFACT_BYTE_LIMIT;
  const content = truncated
    ? `${JSON.stringify(
        {
          schemaVersion: 1,
          artifactKind: 'subagent-output',
          toolName: 'Agent',
          turnId: input.turnId,
          taskId: input.taskId,
          childRunId: input.childRunId,
          toolUseId: input.toolUseId,
          agentName: input.agentName,
          status: input.status,
          sourceOutputFile: input.outputFile,
          skipTranscript: input.skipTranscript,
          redacted: true,
          truncated: true,
          originalByteLength,
          preview: serialized.slice(0, CHILD_OUTPUT_INLINE_BYTE_LIMIT)
        },
        null,
        2
      )}\n`
    : serialized;

  const artifactRelativePath = path.join(
    input.sessionId,
    'artifacts',
    'subagents',
    `${safePathSegment(
      input.taskId ?? input.childRunId ?? input.toolUseId,
      'child-output'
    )}-${safePathSegment(input.agentName ?? 'Agent', 'subagent')}.json`
  );
  const artifactPath = path.join(getSessionRootDirectory(), artifactRelativePath);
  await mkdir(path.dirname(artifactPath), { recursive: true });
  await writeFile(artifactPath, content, 'utf8');
  const artifactByteLength = byteLength(content);

  return {
    artifactPath,
    artifactRelativePath,
    artifactByteLength,
    originalByteLength,
    sha256: sha256Hex(content),
    toolName: 'Agent',
    turnId: input.turnId,
    taskId: input.taskId,
    childRunId: input.childRunId,
    toolUseId: input.toolUseId,
    sourceOutputFile: input.outputFile,
    retentionPolicy: 'session-lifetime',
    redacted: true,
    truncated
  };
}
