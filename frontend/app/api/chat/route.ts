import { NextRequest, NextResponse } from "next/server";
import Anthropic from "@anthropic-ai/sdk";
import fs from "fs";
import path from "path";

const tools: Anthropic.Tool[] = [
  {
    name: "read_file",
    description: "Read the content of a file from the project filesystem.",
    input_schema: {
      type: "object",
      properties: {
        path: { type: "string", description: "The relative path to the file." },
      },
      required: ["path"],
    },
  },
  {
    name: "write_file",
    description: "Write content to a file in the project filesystem.",
    input_schema: {
      type: "object",
      properties: {
        path: { type: "string", description: "The relative path to the file." },
        content: { type: "string", description: "The content to write." },
      },
      required: ["path", "content"],
    },
  },
  {
    name: "list_directory",
    description: "List the contents of a directory.",
    input_schema: {
      type: "object",
      properties: {
        path: { type: "string", description: "The relative path to the directory." },
      },
      required: ["path"],
    },
  },
];

export async function POST(req: NextRequest) {
  try {
    const { messages, apiKey, model } = await req.json();

    if (!apiKey) {
      return NextResponse.json({ error: "API Key required" }, { status: 401 });
    }

    const anthropic = new Anthropic({
      apiKey: apiKey,
    });

    let currentMessages = [...messages];
    // Use the requested model or default to the latest Haiku
    const MODEL = model || "claude-3-5-haiku-latest";
    
    const msg = await anthropic.messages.create({
      model: MODEL,
      max_tokens: 4096,
      messages: currentMessages,
      tools: tools,
    });

    if (msg.stop_reason === "tool_use") {
      const toolResults = [];
      const assistantMessage = { role: "assistant", content: msg.content };
      currentMessages.push(assistantMessage);

      for (const contentBlock of msg.content) {
        if (contentBlock.type === "tool_use") {
          const toolName = contentBlock.name;
          const toolInput = contentBlock.input as any;
          let toolResultContent = "";

          try {
            const rootPath = path.resolve(process.cwd(), "..");
            
            if (toolName === "read_file") {
                const fullPath = path.join(rootPath, toolInput.path);
                if (fs.existsSync(fullPath)) {
                    toolResultContent = fs.readFileSync(fullPath, "utf-8");
                } else {
                    toolResultContent = "Error: File not found.";
                }
            } else if (toolName === "write_file") {
                const fullPath = path.join(rootPath, toolInput.path);
                fs.mkdirSync(path.dirname(fullPath), { recursive: true });
                fs.writeFileSync(fullPath, toolInput.content);
                toolResultContent = "Success: Written.";
            } else if (toolName === "list_directory") {
                const fullPath = path.join(rootPath, toolInput.path);
                if (fs.existsSync(fullPath)) {
                    const files = fs.readdirSync(fullPath);
                    let listStr = "";
                    for (let i = 0; i < files.length; i++) {
                        listStr += files[i];
                        if (i < files.length - 1) {
                            listStr += String.fromCharCode(10);
                        }
                    }
                    toolResultContent = listStr;
                } else {
                    toolResultContent = "Error: Directory not found.";
                }
            }
          } catch (e: any) {
            toolResultContent = "Error: Execution failed.";
          }

          toolResults.push({
            type: "tool_result",
            tool_use_id: contentBlock.id,
            content: toolResultContent,
          });
        }
      }

      currentMessages.push({
        role: "user",
        content: toolResults as any,
      });

      const finalMsg = await anthropic.messages.create({
        model: MODEL,
        max_tokens: 4096,
        messages: currentMessages,
      });

      return NextResponse.json(finalMsg);
    }

    return NextResponse.json(msg);

  } catch (error: any) {
    console.error("Chat API Error:", error);
    return NextResponse.json({ error: error.message }, { status: 500 });
  }
}