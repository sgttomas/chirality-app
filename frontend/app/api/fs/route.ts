import { NextRequest, NextResponse } from "next/server";
import fs from "fs";
import path from "path";

export type FileNode = {
  name: string;
  path: string;
  isDirectory: boolean;
  children?: FileNode[];
};

const IGNORED_DIRS = [
  "node_modules",
  ".git",
  ".next",
  "dist",
  ".Archive",
  ".gemini",
];

function readDirectory(dir: string, baseDir: string): FileNode[] {
  const entries = fs.readdirSync(dir, { withFileTypes: true });
  
  return entries
    .filter(entry => !IGNORED_DIRS.includes(entry.name))
    .map(entry => {
      const fullPath = path.join(dir, entry.name);
      const relativePath = path.relative(baseDir, fullPath);
      
      const node: FileNode = {
        name: entry.name,
        path: relativePath,
        isDirectory: entry.isDirectory(),
      };

      if (node.isDirectory) {
        node.children = readDirectory(fullPath, baseDir);
      }

      return node;
    })
    .sort((a, b) => {
      // Directories first, then alphabetical
      if (a.isDirectory && !b.isDirectory) return -1;
      if (!a.isDirectory && b.isDirectory) return 1;
      return a.name.localeCompare(b.name);
    });
}

export async function GET(req: NextRequest) {
  try {
    const searchParams = req.nextUrl.searchParams;
    const queryPath = searchParams.get("path");

    // Starting from the project root (one level up from frontend) or the provided path
    const rootPath = queryPath ? path.resolve(queryPath) : path.resolve(process.cwd(), "..");
    
    // Ensure the path exists
    if (!fs.existsSync(rootPath)) {
       return NextResponse.json({ error: "Path does not exist" }, { status: 404 });
    }

    const tree = readDirectory(rootPath, rootPath);
    return NextResponse.json(tree);
  } catch (error) {
    console.error("FS API Error:", error);
    return NextResponse.json({ error: "Failed to read filesystem" }, { status: 500 });
  }
}
