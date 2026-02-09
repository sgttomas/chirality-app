import { NextResponse } from "next/server";
import fs from "node:fs";
import path from "node:path";
import { getInstructionRoot, isInstructionRootWritable } from "@/lib/harness/instruction-root";

const CONFIG_FILE = "CLAUDE.md";

export async function GET() {
  try {
    const instructionRoot = getInstructionRoot();
    const configPath = path.join(instructionRoot, CONFIG_FILE);
    const writable = isInstructionRootWritable(instructionRoot);

    if (!fs.existsSync(configPath)) {
      return NextResponse.json({ model: null, instructionRoot, writable });
    }

    const content = fs.readFileSync(configPath, "utf-8");
    const match = content.match(/^model:\s*(.+)$/m);
    const model = match ? match[1].trim() : null;

    return NextResponse.json({ model, instructionRoot, writable });
  } catch (error) {
    return NextResponse.json({ error: String(error) }, { status: 500 });
  }
}

export async function POST(request: Request) {
  try {
    const body = await request.json();
    const { model } = body;
    
    if (!model) {
      return NextResponse.json({ error: "Model is required" }, { status: 400 });
    }

    const instructionRoot = getInstructionRoot();
    const writable = isInstructionRootWritable(instructionRoot);
    if (!writable) {
      return NextResponse.json(
        { error: "Instruction root is read-only. Update model via a release update.", instructionRoot },
        { status: 403 },
      );
    }

    const configPath = path.join(instructionRoot, CONFIG_FILE);

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

    return NextResponse.json({ success: true, model, instructionRoot });
  } catch (error) {
    return NextResponse.json({ error: String(error) }, { status: 500 });
  }
}
