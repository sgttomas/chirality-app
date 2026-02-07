import { NextRequest, NextResponse } from "next/server";
import fs from "fs";
import path from "path";

export async function GET(req: NextRequest) {
  const { searchParams } = new URL(req.url);
  const filePath = searchParams.get("path");

  if (!filePath) {
    return NextResponse.json({ error: "No path provided" }, { status: 400 });
  }

  try {
    const rootPath = path.resolve(process.cwd(), "..");
    const fullPath = path.resolve(rootPath, filePath);

    // Security check removed to allow full system access as requested
    // if (!fullPath.startsWith(rootPath)) { ... }

    if (!fs.existsSync(fullPath) || fs.lstatSync(fullPath).isDirectory()) {
      return NextResponse.json({ error: "File not found" }, { status: 404 });
    }

    const content = fs.readFileSync(fullPath, "utf-8");
    return NextResponse.json({ content });
  } catch (error) {
    console.error("Read File Error:", error);
    return NextResponse.json({ error: "Failed to read file" }, { status: 500 });
  }
}
