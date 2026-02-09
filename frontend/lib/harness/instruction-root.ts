import fs from "node:fs";
import path from "node:path";

const INSTRUCTION_ROOT_ENV = "CHIRALITY_INSTRUCTION_ROOT";
const REQUIRED_FILES = ["AGENTS.md", "README.md", "agents"] as const;

let cachedInstructionRoot: string | null = null;

function isInstructionRoot(candidate: string): boolean {
  const root = path.resolve(candidate);

  try {
    for (const entry of REQUIRED_FILES) {
      const fullPath = path.join(root, entry);
      if (!fs.existsSync(fullPath)) {
        return false;
      }
    }

    return fs.statSync(path.join(root, "agents")).isDirectory();
  } catch {
    return false;
  }
}

function walkUpDirectories(fromDir: string): string[] {
  const directories: string[] = [];
  let cursor = path.resolve(fromDir);

  while (true) {
    directories.push(cursor);
    const parent = path.dirname(cursor);
    if (parent === cursor) {
      break;
    }
    cursor = parent;
  }

  return directories;
}

function candidateInstructionRoots(): string[] {
  const candidates: string[] = [];
  const envRoot = process.env[INSTRUCTION_ROOT_ENV];
  if (envRoot && envRoot.trim()) {
    candidates.push(path.resolve(envRoot));
  }

  candidates.push(...walkUpDirectories(process.cwd()));
  candidates.push(path.resolve(process.cwd(), ".."));

  return Array.from(new Set(candidates));
}

function resolveInstructionRootUncached(): string {
  const candidates = candidateInstructionRoots();
  for (const candidate of candidates) {
    if (isInstructionRoot(candidate)) {
      return path.resolve(candidate);
    }
  }

  return path.resolve(process.cwd(), "..");
}

export function getInstructionRoot(): string {
  if (!cachedInstructionRoot) {
    cachedInstructionRoot = resolveInstructionRootUncached();
  }

  return cachedInstructionRoot;
}

export function isInstructionRootWritable(root: string = getInstructionRoot()): boolean {
  try {
    fs.accessSync(root, fs.constants.W_OK);
    return true;
  } catch {
    return false;
  }
}

export function getInstructionRootEnvName(): string {
  return INSTRUCTION_ROOT_ENV;
}
