
import { NextResponse } from "next/server";
import fs from "node:fs";
import path from "node:path";

const CONFIG_FILE = "CLAUDE.md";

function getProjectRoot() {
  // In a real app, this might come from a header or session, 
  // but for this local tool, we assume a relative path or fixed root for now,
  // or rely on the client passing it. 
  // However, the harness usually knows the root. 
  // For simplicity, we'll try to resolve it relative to CWD or accept a query param.
  return path.resolve(process.cwd(), "..");
}

export async function GET(request: Request) {
  try {
    const { searchParams } = new URL(request.url);
    const rootParam = searchParams.get("projectRoot");
    const projectRoot = rootParam ? path.resolve(rootParam) : getProjectRoot();
    const configPath = path.join(projectRoot, CONFIG_FILE);

    if (!fs.existsSync(configPath)) {
      return NextResponse.json({ model: null });
    }

    const content = fs.readFileSync(configPath, "utf-8");
    const match = content.match(/^model:\s*(.+)$/m);
    const model = match ? match[1].trim() : null;

    return NextResponse.json({ model });
  } catch (error) {
    return NextResponse.json({ error: String(error) }, { status: 500 });
  }
}

export async function POST(request: Request) {
  try {
    const body = await request.json();
    const { model, projectRoot: rootParam } = body;
    
    if (!model) {
      return NextResponse.json({ error: "Model is required" }, { status: 400 });
    }

    const projectRoot = rootParam ? path.resolve(rootParam) : getProjectRoot();
    const configPath = path.join(projectRoot, CONFIG_FILE);

    let content = "";
    if (fs.existsSync(configPath)) {
      content = fs.readFileSync(configPath, "utf-8");
    } else {
      content = "# Claude Configuration\n\n";
    }

    // Replace or append model
    if (content.match(/^model:\s*.+$/m)) {
        content = content.replace(/^model:\s*.+$/m, `model: ${model}`);
    } else {
        content = content.trim() + `
model: ${model}
`;
    }

    fs.writeFileSync(configPath, content, "utf-8");

    return NextResponse.json({ success: true, model });
  } catch (error) {
    return NextResponse.json({ error: String(error) }, { status: 500 });
  }
}
