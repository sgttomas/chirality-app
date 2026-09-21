import { Buffer } from 'node:buffer';
import type { HarnessToolDescriptor, HarnessToolResultBudget } from '@chirality/runtime-contracts/tool-descriptor';
import { redactJsonLike } from './run-logger';

const SAFE_PATH_FIELD_NAMES = [
  'file_path',
  'path',
  'deliverablePath',
  'executionRoot',
  'decompositionPath',
  'runnerInputRef',
  'projectRoot'
] as const;

type JsonRecord = Record<string, unknown>;

export type ToolInputEvidence = {
  inputType: string;
  inputKeys: string[];
  pathFields: Record<string, string>;
};

export type ToolResultBudgetClass =
  | 'unknown-descriptor'
  | 'within-inline-budget'
  | 'requires-artifact-overflow'
  | 'exceeds-artifact-budget';

export type ToolResultEvidence = {
  resultByteLength: number;
  contentItemCount: number;
  contentTextByteLength: number;
  contentTypes: string[];
  inlineByteLimit?: number;
  artifactByteLimit?: number;
  overflowPolicy?: HarnessToolResultBudget['overflow'];
  budgetClass: ToolResultBudgetClass;
  outputPersisted: boolean;
  rawOutputPersisted: false;
};

export type ShellResultStreamEvidence = {
  stdoutPresent: boolean;
  stderrPresent: boolean;
  stdoutByteLength: number;
  stderrByteLength: number;
  interrupted?: boolean;
  isImage?: boolean;
  backgroundTask: boolean;
  backgroundedByUser?: boolean;
  assistantAutoBackgrounded?: boolean;
  rawOutputPathPresent: boolean;
  dangerouslyDisableSandbox?: boolean;
};

function isRecord(value: unknown): value is JsonRecord {
  return Boolean(value) && typeof value === 'object' && !Array.isArray(value);
}

function readString(value: unknown): string | undefined {
  return typeof value === 'string' && value.length > 0 ? value : undefined;
}

function byteLength(value: string): number {
  return Buffer.byteLength(value, 'utf8');
}

function byteLengthOfJsonLike(value: unknown): number {
  try {
    return byteLength(JSON.stringify(redactJsonLike(value)) ?? '');
  } catch {
    return byteLength(String(value));
  }
}

function describeInputType(value: unknown): string {
  if (Array.isArray(value)) {
    return 'array';
  }
  if (value === null) {
    return 'null';
  }
  return typeof value;
}

function collectContentItems(result: unknown): unknown[] {
  if (!isRecord(result) || !Array.isArray(result.content)) {
    return [];
  }
  return result.content;
}

function classifyResultBudget(
  resultByteLength: number,
  descriptor?: HarnessToolDescriptor
): ToolResultBudgetClass {
  const budget = descriptor?.resultBudget;
  if (!budget) {
    return 'unknown-descriptor';
  }
  if (resultByteLength <= budget.inlineByteLimit) {
    return 'within-inline-budget';
  }
  if (resultByteLength <= budget.artifactByteLimit) {
    return 'requires-artifact-overflow';
  }
  return 'exceeds-artifact-budget';
}

export function summarizeToolInput(input: unknown): ToolInputEvidence {
  if (!isRecord(input)) {
    return {
      inputType: describeInputType(input),
      inputKeys: [],
      pathFields: {}
    };
  }

  const pathFields = Object.fromEntries(
    SAFE_PATH_FIELD_NAMES.flatMap((fieldName) => {
      const value = readString(input[fieldName]);
      return value ? [[fieldName, value]] : [];
    })
  );

  return {
    inputType: 'object',
    inputKeys: Object.keys(input).sort(),
    pathFields: redactJsonLike(pathFields)
  };
}

export function summarizeToolResult(
  result: unknown,
  descriptor?: HarnessToolDescriptor
): ToolResultEvidence {
  const contentItems = collectContentItems(result);
  const contentTypes = Array.from(
    new Set(
      contentItems
        .map((item) => (isRecord(item) ? readString(item.type) : undefined))
        .filter((type): type is string => Boolean(type))
    )
  ).sort();
  const contentTextByteLength = contentItems.reduce<number>((total, item) => {
    const text = isRecord(item) ? readString(item.text) : undefined;
    return total + (text ? byteLength(text) : 0);
  }, 0);
  const resultByteLength = byteLengthOfJsonLike(result);
  const budget = descriptor?.resultBudget;

  return {
    resultByteLength,
    contentItemCount: contentItems.length,
    contentTextByteLength,
    contentTypes,
    inlineByteLimit: budget?.inlineByteLimit,
    artifactByteLimit: budget?.artifactByteLimit,
    overflowPolicy: budget?.overflow,
    budgetClass: classifyResultBudget(resultByteLength, descriptor),
    outputPersisted: false,
    rawOutputPersisted: false
  };
}

export function withToolResultPersistence(
  evidence: ToolResultEvidence,
  outputPersisted: boolean
): ToolResultEvidence {
  return {
    ...evidence,
    outputPersisted
  };
}

export function summarizeShellResultStreams(result: unknown): ShellResultStreamEvidence {
  const record = isRecord(result) ? result : {};
  const stdout = readString(record.stdout);
  const stderr = readString(record.stderr);
  return {
    stdoutPresent: stdout !== undefined,
    stderrPresent: stderr !== undefined,
    stdoutByteLength: stdout ? byteLength(stdout) : 0,
    stderrByteLength: stderr ? byteLength(stderr) : 0,
    interrupted: typeof record.interrupted === 'boolean' ? record.interrupted : undefined,
    isImage: typeof record.isImage === 'boolean' ? record.isImage : undefined,
    backgroundTask: readString(record.backgroundTaskId) !== undefined,
    backgroundedByUser:
      typeof record.backgroundedByUser === 'boolean' ? record.backgroundedByUser : undefined,
    assistantAutoBackgrounded:
      typeof record.assistantAutoBackgrounded === 'boolean'
        ? record.assistantAutoBackgrounded
        : undefined,
    rawOutputPathPresent: readString(record.rawOutputPath) !== undefined,
    dangerouslyDisableSandbox:
      typeof record.dangerouslyDisableSandbox === 'boolean'
        ? record.dangerouslyDisableSandbox
        : undefined
  };
}

export function summarizeToolDescriptor(
  descriptor?: HarnessToolDescriptor
): Record<string, unknown> {
  return {
    descriptorName: descriptor?.name,
    adapterToolName: descriptor?.adapter.claudeAgentSdk?.toolName,
    surface: descriptor?.surface,
    permissions: descriptor ? [...descriptor.permissions] : undefined,
    pathScope: descriptor?.pathScope,
    humanGate: descriptor?.humanGate,
    resultBudget: descriptor?.resultBudget
  };
}

export function summarizeToolError(error: unknown): Record<string, unknown> {
  if (error instanceof Error) {
    return redactJsonLike({
      errorName: error.name,
      message: error.message
    });
  }

  if (isRecord(error)) {
    return redactJsonLike({
      errorName: readString(error.name),
      message: readString(error.message) ?? 'Tool execution failed',
      type: error.type,
      status: error.status
    });
  }

  return redactJsonLike({
    message: String(error)
  });
}

export function isToolResultFailure(result: unknown): boolean {
  if (!isRecord(result)) {
    return false;
  }
  return result.is_error === true || result.isError === true || result.interrupted === true;
}
