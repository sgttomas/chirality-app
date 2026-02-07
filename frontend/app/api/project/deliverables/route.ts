import { NextRequest, NextResponse } from "next/server";
import fs from "fs";
import path from "path";

export type Deliverable = {
  id: string;
  name: string;
  pkg: string;
  status: "open" | "in-progress" | "checking" | "issued";
  path: string;
};

function getStatusFromContent(content: string): Deliverable['status'] {
    if (content.includes("ISSUED")) return "issued";
    if (content.includes("CHECKING")) return "checking";
    if (content.includes("IN_PROGRESS")) return "in-progress";
    return "open";
}

export async function GET(req: NextRequest) {
  const { searchParams } = new URL(req.url);
  const rootPath = searchParams.get("path");

  if (!rootPath || !fs.existsSync(rootPath)) {
    return NextResponse.json({ error: "Invalid project path" }, { status: 400 });
  }

  const deliverables: Deliverable[] = [];

  try {
    const packages = fs.readdirSync(rootPath, { withFileTypes: true })
        .filter(d => d.isDirectory() && d.name.startsWith("PKG-"));

    for (const pkg of packages) {
        const workingDir = path.join(rootPath, pkg.name, "1_Working");
        if (fs.existsSync(workingDir)) {
            const dels = fs.readdirSync(workingDir, { withFileTypes: true })
                .filter(d => d.isDirectory() && d.name.startsWith("DEL-"));
            
            for (const del of dels) {
                const delPath = path.join(workingDir, del.name);
                const statusPath = path.join(delPath, "_STATUS.md");
                let status: Deliverable['status'] = "open";

                if (fs.existsSync(statusPath)) {
                    const content = fs.readFileSync(statusPath, "utf-8");
                    status = getStatusFromContent(content);
                }

                // Parse ID and Name from folder name (e.g., "DEL-01.01_SitePlan")
                const parts = del.name.split("_");
                const id = parts[0];
                const name = parts.slice(1).join(" ").replace(/([A-Z])/g, ' $1').trim() || "Untitled Deliverable";

                deliverables.push({
                    id,
                    name,
                    pkg: pkg.name,
                    status,
                    path: delPath
                });
            }
        }
    }

    return NextResponse.json({ deliverables });
  } catch (error: any) {
    console.error("Scan Error:", error);
    return NextResponse.json({ error: error.message }, { status: 500 });
  }
}
