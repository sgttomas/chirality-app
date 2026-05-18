import { NextRequest, NextResponse } from "next/server";
import fs from "fs";
import path from "path";
import { execFile } from "node:child_process";
import { promisify } from "node:util";

const execFileAsync = promisify(execFile);
const GIT_MAX_BUFFER = 8 * 1024 * 1024;
const FULL_FILE_UNIFIED_CONTEXT = 999999;

type DiffState = "changed" | "clean" | "untracked" | "ignored" | "not_repo";

type DiffResponse = {
  state: DiffState;
  diff: string;
  message?: string;
};

type ExecError = NodeJS.ErrnoException & {
  code?: number;
  stdout?: string;
  stderr?: string;
};

function normalizePathForGit(value: string): string {
  return value.split(path.sep).join("/");
}

function isExecError(error: unknown): error is ExecError {
  return typeof error === "object" && error !== null;
}

async function git(repoPath: string, args: string[]): Promise<string> {
  const { stdout } = await execFileAsync("git", ["-C", repoPath, ...args], {
    maxBuffer: GIT_MAX_BUFFER,
  });
  return stdout.trimEnd();
}

async function isIgnoredByGit(repoPath: string, relativePath: string): Promise<boolean> {
  try {
    await execFileAsync("git", ["-C", repoPath, "check-ignore", "-q", "--", relativePath], {
      maxBuffer: GIT_MAX_BUFFER,
    });
    return true;
  } catch (error) {
    if (isExecError(error) && error.code === 1) {
      return false;
    }
    return false;
  }
}

async function diffForUntrackedFile(repoPath: string, relativePath: string): Promise<string> {
  try {
    const { stdout } = await execFileAsync(
      "git",
      [
        "-C",
        repoPath,
        "diff",
        "--no-color",
        `--unified=${FULL_FILE_UNIFIED_CONTEXT}`,
        "--no-index",
        "--",
        "/dev/null",
        relativePath,
      ],
      { maxBuffer: GIT_MAX_BUFFER },
    );
    return stdout.trimEnd();
  } catch (error) {
    if (isExecError(error) && typeof error.stdout === "string" && error.stdout.trim()) {
      return error.stdout.trimEnd();
    }
    if (isExecError(error) && error.code === 1) {
      return `+++ b/${relativePath}`;
    }
    throw error;
  }
}

function buildRepoStateResponse(state: DiffState, diff = "", message?: string): DiffResponse {
  return { state, diff, message };
}

export async function GET(req: NextRequest) {
  const searchParams = req.nextUrl.searchParams;
  const filePath = searchParams.get("path");
  const projectRootParam = searchParams.get("projectRoot");

  if (!filePath) {
    return NextResponse.json({ error: "No path provided" }, { status: 400 });
  }

  try {
    const projectRoot = projectRootParam ? path.resolve(projectRootParam) : path.resolve(process.cwd(), "..");
    const fullPath = path.isAbsolute(filePath) ? path.resolve(filePath) : path.resolve(projectRoot, filePath);

    if (!fs.existsSync(fullPath) || fs.lstatSync(fullPath).isDirectory()) {
      return NextResponse.json({ error: "File not found" }, { status: 404 });
    }

    let repoRoot: string;
    try {
      repoRoot = (await git(path.dirname(fullPath), ["rev-parse", "--show-toplevel"])).trim();
    } catch {
      return NextResponse.json(
        buildRepoStateResponse("not_repo", "", "Selected file is outside a git repository."),
      );
    }

    const relativePath = normalizePathForGit(path.relative(repoRoot, fullPath));
    if (!relativePath || relativePath.startsWith("..")) {
      return NextResponse.json(
        buildRepoStateResponse("not_repo", "", "Selected file is outside the active git repository."),
      );
    }

    const statusOutput = await git(repoRoot, ["status", "--porcelain", "--", relativePath]);
    const statusLine = statusOutput
      .split("\n")
      .map((line) => line.trimEnd())
      .find((line) => line.length > 0);

    if (!statusLine) {
      const ignored = await isIgnoredByGit(repoRoot, relativePath);
      if (ignored) {
        return NextResponse.json(
          buildRepoStateResponse("ignored", "", "This file is ignored by git and has no diff."),
        );
      }
      return NextResponse.json(buildRepoStateResponse("clean", "", "No git changes for this file."));
    }

    if (statusLine.startsWith("??")) {
      const diff = await diffForUntrackedFile(repoRoot, relativePath);
      return NextResponse.json(buildRepoStateResponse("untracked", diff, "Untracked file."));
    }

    const diff = await git(
      repoRoot,
      ["diff", "--no-color", `--unified=${FULL_FILE_UNIFIED_CONTEXT}`, "HEAD", "--", relativePath],
    );
    if (!diff.trim()) {
      return NextResponse.json(buildRepoStateResponse("clean", "", "No git changes for this file."));
    }

    return NextResponse.json(buildRepoStateResponse("changed", diff));
  } catch (error) {
    console.error("Diff API Error:", error);
    return NextResponse.json({ error: "Failed to compute file diff" }, { status: 500 });
  }
}
