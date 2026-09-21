import { lstat } from 'node:fs/promises';
import path from 'node:path';
import { instructionRootContainsPath, resolveInstructionRootPath } from './instruction-root';
import type { HarnessToolDescriptor } from '@chirality/runtime-contracts/tool-descriptor';

export type HarnessToolPathPolicyDeny = {
  reason: string;
  metadata: Record<string, unknown>;
};

export type HarnessToolPathPolicyAllow = {
  pathField?: string;
  rawPath?: string;
  resolvedPath?: string;
  projectRoot?: string;
  pathScope?: HarnessToolDescriptor['pathScope'];
};

export type HarnessToolPathPolicyResult =
  | {
      allowed: true;
      metadata: HarnessToolPathPolicyAllow;
    }
  | {
      allowed: false;
      reason: string;
      metadata: Record<string, unknown>;
    };

const PRIMARY_PATH_FIELDS = [
  'file_path',
  'path',
  'notebook_path',
  'deliverablePath',
  'executionRoot',
  'decompositionPath',
  'runnerInputRef'
] as const;

function isRecord(value: unknown): value is Record<string, unknown> {
  return Boolean(value) && typeof value === 'object' && !Array.isArray(value);
}

function isWithinRoot(root: string, candidate: string): boolean {
  const relative = path.relative(path.resolve(root), path.resolve(candidate));
  return relative === '' || (!relative.startsWith('..') && !path.isAbsolute(relative));
}

function readPrimaryPathField(toolInput: unknown): { field: string; value: string } | undefined {
  if (!isRecord(toolInput)) {
    return undefined;
  }

  for (const field of PRIMARY_PATH_FIELDS) {
    const value = toolInput[field];
    if (typeof value === 'string' && value.trim().length > 0) {
      return {
        field,
        value: value.trim()
      };
    }
  }

  return undefined;
}

function resolveToolPath(projectRoot: string, rawPath: string): string {
  return path.isAbsolute(rawPath) ? path.resolve(rawPath) : path.resolve(projectRoot, rawPath);
}

function denyPath(input: {
  reason: string;
  denyClass: string;
  projectRoot?: string;
  pathField?: string;
  rawPath?: string;
  resolvedPath?: string;
  pathScope?: HarnessToolDescriptor['pathScope'];
  extra?: Record<string, unknown>;
}): HarnessToolPathPolicyResult {
  return {
    allowed: false,
    reason: input.reason,
    metadata: {
      denyClass: input.denyClass,
      projectRoot: input.projectRoot ? path.resolve(input.projectRoot) : undefined,
      pathField: input.pathField,
      requestedPath: input.rawPath,
      resolvedPath: input.resolvedPath,
      pathScope: input.pathScope,
      ...input.extra
    }
  };
}

async function rejectSymlinkPath(input: {
  projectRoot: string;
  rawPath: string;
  resolvedPath: string;
  pathField: string;
  pathScope: HarnessToolDescriptor['pathScope'];
  access: 'read' | 'write';
}): Promise<HarnessToolPathPolicyResult | undefined> {
  const root = path.resolve(input.projectRoot);
  const relative = path.relative(root, input.resolvedPath);
  const segments = relative === '' ? [] : relative.split(path.sep);
  let current = root;

  for (const [index, segment] of ['', ...segments].entries()) {
    if (segment) {
      current = path.join(current, segment);
    }

    try {
      const stats = await lstat(current);
      if (stats.isSymbolicLink()) {
        return denyPath({
          reason: `${input.access === 'read' ? 'Read' : 'Write'} path '${input.rawPath}' crosses symbolic link '${current}'.`,
          denyClass: `symlink-${input.access}`,
          projectRoot: input.projectRoot,
          pathField: input.pathField,
          rawPath: input.rawPath,
          resolvedPath: input.resolvedPath,
          pathScope: input.pathScope,
          extra: {
            symlinkPath: current
          }
        });
      }
    } catch (error) {
      if ((error as NodeJS.ErrnoException).code === 'ENOENT') {
        if (index === 0) {
          return denyPath({
            reason: `Project root '${input.projectRoot}' is not accessible for write policy checks.`,
            denyClass: 'project-root-missing',
            projectRoot: input.projectRoot,
            pathField: input.pathField,
            rawPath: input.rawPath,
            resolvedPath: input.resolvedPath,
            pathScope: input.pathScope
          });
        }
        return undefined;
      }

      return denyPath({
          reason: `${input.access === 'read' ? 'Read' : 'Write'} path '${input.rawPath}' could not be checked for symbolic links.`,
        denyClass: 'path-stat-failed',
        projectRoot: input.projectRoot,
        pathField: input.pathField,
        rawPath: input.rawPath,
        resolvedPath: input.resolvedPath,
        pathScope: input.pathScope,
        extra: {
          error: error instanceof Error ? error.message : 'unknown path stat failure'
        }
      });
    }
  }

  return undefined;
}

export async function evaluateToolPathPolicy(input: {
  descriptor?: HarnessToolDescriptor;
  projectRoot?: string;
  toolInput: unknown;
  blockedPath?: string;
  instructionRoot?: string;
  allowedReadScopes?: readonly string[];
  allowedWriteTargets?: readonly string[];
}): Promise<HarnessToolPathPolicyResult> {
  if (input.blockedPath) {
    return denyPath({
      reason: `Path '${input.blockedPath}' is blocked by SDK path policy.`,
      denyClass: 'path-containment',
      rawPath: input.blockedPath,
      resolvedPath: path.resolve(input.blockedPath),
      pathScope: input.descriptor?.pathScope,
      extra: {
        blockedPath: input.blockedPath
      }
    });
  }

  const pathScope = input.descriptor?.pathScope;
  if (
    !input.projectRoot ||
    (pathScope !== 'project-root-read' && pathScope !== 'project-root-write')
  ) {
    return {
      allowed: true,
      metadata: {
        pathScope
      }
    };
  }

  const pathField = readPrimaryPathField(input.toolInput);
  const projectRoot = path.resolve(input.projectRoot);
  const managedScopes =
    pathScope === 'project-root-read'
      ? input.allowedReadScopes
      : pathScope === 'project-root-write'
        ? input.allowedWriteTargets
        : undefined;
  if (!pathField) {
    if (input.descriptor?.permissions.includes('shell')) {
      return {
        allowed: true,
        metadata: {
          projectRoot,
          pathScope
        }
      };
    }
    if (
      managedScopes !== undefined &&
      !managedScopes.some((scope) => path.resolve(scope) === projectRoot)
    ) {
      return denyPath({
        reason: `${pathScope === 'project-root-read' ? 'Read' : 'Write'} tool requires an explicit path inside the managed child scope.`,
        denyClass: 'managed-scope-path-required',
        projectRoot: input.projectRoot,
        pathScope,
        extra: {
          managedScopes: managedScopes.map((scope) => path.resolve(scope))
        }
      });
    }
    return {
      allowed: true,
      metadata: {
        projectRoot: path.resolve(input.projectRoot),
        pathScope
      }
    };
  }

  const resolvedPath = resolveToolPath(input.projectRoot, pathField.value);
  const allowMetadata = {
    projectRoot: path.resolve(input.projectRoot),
    pathField: pathField.field,
    rawPath: pathField.value,
    resolvedPath,
    pathScope
  };

  if (!isWithinRoot(input.projectRoot, resolvedPath)) {
    return denyPath({
      reason: `Path '${pathField.value}' resolves outside the active project root.`,
      denyClass: 'path-containment',
      projectRoot: input.projectRoot,
      pathField: pathField.field,
      rawPath: pathField.value,
      resolvedPath,
      pathScope
    });
  }

  if (
    managedScopes !== undefined &&
    !managedScopes.some((scope) => isWithinRoot(scope, resolvedPath))
  ) {
    return denyPath({
      reason: `Path '${pathField.value}' is outside the managed child's declared ${pathScope === 'project-root-read' ? 'read scope' : 'write targets'}.`,
      denyClass: pathScope === 'project-root-read' ? 'managed-read-scope' : 'managed-write-scope',
      projectRoot: input.projectRoot,
      pathField: pathField.field,
      rawPath: pathField.value,
      resolvedPath,
      pathScope,
      extra: {
        managedScopes: managedScopes.map((scope) => path.resolve(scope))
      }
    });
  }

  const symlinkDeny = await rejectSymlinkPath({
    projectRoot: input.projectRoot,
    rawPath: pathField.value,
    resolvedPath,
    pathField: pathField.field,
    pathScope,
    access: pathScope === 'project-root-read' ? 'read' : 'write'
  });
  if (symlinkDeny) {
    return symlinkDeny;
  }

  if (pathScope !== 'project-root-write') {
    return {
      allowed: true,
      metadata: allowMetadata
    };
  }

  const instructionRoot = input.instructionRoot ?? resolveInstructionRootPath();
  if (instructionRootContainsPath(resolvedPath, instructionRoot)) {
    return denyPath({
      reason: `Write path '${pathField.value}' resolves under the instruction root.`,
      denyClass: 'instruction-root',
      projectRoot: input.projectRoot,
      pathField: pathField.field,
      rawPath: pathField.value,
      resolvedPath,
      pathScope,
      extra: {
        instructionRoot: path.resolve(instructionRoot)
      }
    });
  }

  return {
    allowed: true,
    metadata: allowMetadata
  };
}
