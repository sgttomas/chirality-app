import { NextRequest, NextResponse } from "next/server";
import fs from "fs";
import path from "path";
import { execFile } from "node:child_process";
import { promisify } from "node:util";

const execFileAsync = promisify(execFile);
const GIT_MAX_BUFFER = 8 * 1024 * 1024;

type GitFileState = "modified" | "added" | "deleted" | "renamed" | "untracked" | "conflicted";

type GitStatusSummary = {
  changed: number;
  modified: number;
  added: number;
  deleted: number;
  renamed: number;
  untracked: number;
  conflicted: number;
};

type GitStatusResponse = {
  state: "ready" | "not_repo";
  statuses: Record<string, GitFileState>;
  summary: GitStatusSummary;
  message?: string;
};

type ParsedStatusEntry = {
  code: string;
  repoRelativePath: string;
};

const STATE_PRIORITY: Record<GitFileState, number> = {
  conflicted: 6,
  deleted: 5,
  renamed: 4,
  modified: 3,
  added: 2,
  untracked: 1,
};

function normalizePathForGit(value: string): string {
  return value.split(path.sep).join("/");
}

function classifyStatus(code: string): GitFileState | null {
  if (code === "??") return "untracked";
  if (code === "!!") return null;
  if (code.includes("U") || code === "AA" || code === "DD") return "conflicted";
  if (code.includes("D")) return "deleted";
  if (code.includes("R") || code.includes("C")) return "renamed";
  if (code.includes("A")) return "added";
  return "modified";
}

function parsePorcelainEntries(output: string): ParsedStatusEntry[] {
  const chunks = output.split("\0").filter(Boolean);
  const entries: ParsedStatusEntry[] = [];

  for (let index = 0; index < chunks.length; index += 1) {
    const chunk = chunks[index];
    if (chunk.length < 3) {
      continue;
    }

    const code = chunk.slice(0, 2);
    let repoRelativePath = chunk.slice(3);
    const isRenameOrCopy = code.includes("R") || code.includes("C");
    if (isRenameOrCopy && chunks[index + 1]) {
      repoRelativePath = chunks[index + 1];
      index += 1;
    }

    entries.push({ code, repoRelativePath });
  }

  return entries;
}

function buildSummary(statuses: Record<string, GitFileState>): GitStatusSummary {
  const summary: GitStatusSummary = {
    changed: 0,
    modified: 0,
    added: 0,
    deleted: 0,
    renamed: 0,
    untracked: 0,
    conflicted: 0,
  };

  Object.values(statuses).forEach((state) => {
    summary.changed += 1;
    summary[state] += 1;
  });

  return summary;
}

function mergeState(existing: GitFileState | undefined, incoming: GitFileState): GitFileState {
  if (!existing) {
    return incoming;
  }
  return STATE_PRIORITY[incoming] > STATE_PRIORITY[existing] ? incoming : existing;
}

async function listGitStatus(basePath: string): Promise<GitStatusResponse> {
  let repoRoot = "";
  try {
    const { stdout } = await execFileAsync("git", ["-C", basePath, "rev-parse", "--show-toplevel"], {
      maxBuffer: GIT_MAX_BUFFER,
    });
    repoRoot = stdout.trim();
  } catch {
    return {
      state: "not_repo",
      statuses: {},
      summary: buildSummary({}),
      message: "Selected path is outside a git repository.",
    };
  }

  const baseRelative = normalizePathForGit(path.relative(repoRoot, basePath));
  if (baseRelative.startsWith("..")) {
    return {
      state: "not_repo",
      statuses: {},
      summary: buildSummary({}),
      message: "Selected path is outside the active git repository.",
    };
  }

  const statusArgs = [
    "-C",
    repoRoot,
    "status",
    "--porcelain=v1",
    "-z",
    "--untracked-files=all",
    "--ignored=matching",
  ];
  if (baseRelative && baseRelative !== ".") {
    statusArgs.push("--", baseRelative);
  }

  const { stdout } = await execFileAsync("git", statusArgs, { maxBuffer: GIT_MAX_BUFFER });
  const entries = parsePorcelainEntries(stdout);
  const statuses: Record<string, GitFileState> = {};

  entries.forEach((entry) => {
    const state = classifyStatus(entry.code);
    if (!state) {
      return;
    }

    const absolutePath = path.resolve(repoRoot, entry.repoRelativePath);
    let relativeToBase = path.relative(basePath, absolutePath);
    if (!relativeToBase || relativeToBase.startsWith("..")) {
      return;
    }

    relativeToBase = normalizePathForGit(relativeToBase);
    if (relativeToBase === ".") {
      return;
    }

    statuses[relativeToBase] = mergeState(statuses[relativeToBase], state);
  });

  return {
    state: "ready",
    statuses,
    summary: buildSummary(statuses),
  };
}

export async function GET(req: NextRequest) {
  const queryPath = req.nextUrl.searchParams.get("path");

  try {
    const basePath = queryPath ? path.resolve(queryPath) : path.resolve(process.cwd(), "..");
    if (!fs.existsSync(basePath)) {
      return NextResponse.json({ error: "Path does not exist" }, { status: 404 });
    }

    const stat = fs.lstatSync(basePath);
    if (!stat.isDirectory()) {
      return NextResponse.json({ error: "Path must be a directory" }, { status: 400 });
    }

    const result = await listGitStatus(basePath);
    return NextResponse.json(result);
  } catch (error) {
    console.error("Git Status API Error:", error);
    return NextResponse.json({ error: "Failed to read git status" }, { status: 500 });
  }
}
