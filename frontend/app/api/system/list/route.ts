import { NextRequest, NextResponse } from "next/server";
import fs from "fs";
import path from "path";

export type SystemNode = {
  name: string;
  path: string;
  isDirectory: boolean;
  hasChildren?: boolean; // Hint for UI
};

export async function GET(req: NextRequest) {
  const { searchParams } = new URL(req.url);
  const targetPath = searchParams.get("path") || "/";

  try {
    if (!fs.existsSync(targetPath)) {
        return NextResponse.json({ error: "Path not found" }, { status: 404 });
    }

    const stats = fs.lstatSync(targetPath);
    if (!stats.isDirectory()) {
        return NextResponse.json({ error: "Not a directory" }, { status: 400 });
    }

    const entries = fs.readdirSync(targetPath, { withFileTypes: true });
    
    const nodes: SystemNode[] = entries.map(entry => {
        const fullPath = path.join(targetPath, entry.name);
        return {
            name: entry.name,
            path: fullPath,
            isDirectory: entry.isDirectory(),
            hasChildren: entry.isDirectory() // We could check this but it's expensive, assume yes for now
        };
    }).sort((a, b) => {
        if (a.isDirectory && !b.isDirectory) return -1;
        if (!a.isDirectory && b.isDirectory) return 1;
        return a.name.localeCompare(b.name);
    });

    return NextResponse.json({ nodes, current: targetPath });

  } catch (error: any) {
    console.error("System List Error:", error);
    return NextResponse.json({ error: error.message }, { status: 500 });
  }
}
