import { NextRequest, NextResponse } from "next/server";
import Anthropic from "@anthropic-ai/sdk";
import fs from "fs";
import path from "path";
import { exec } from "child_process";
import util from "util";

/* eslint-disable @typescript-eslint/no-explicit-any, @typescript-eslint/no-unused-vars, prefer-const */
/**
 * @deprecated Legacy Anthropic SDK chat route retained for backward compatibility.
 * Prefer harness APIs (`/api/harness/session/*`, `/api/harness/turn`, `/api/harness/interrupt`) for all new integrations.
 */
const execAsync = util.promisify(exec);

// Path for persistent session storage
const SESSION_FILE = path.resolve(process.cwd(), ".sessions.json");

function loadSessions(): Record<string, { cwd: string; env: Record<string, string> }> {
    try {
        if (fs.existsSync(SESSION_FILE)) {
            return JSON.parse(fs.readFileSync(SESSION_FILE, "utf-8"));
        }
    } catch (e) {
        console.error("Failed to load sessions", e);
    }
    return {};
}

function saveSessions(sessions: Record<string, any>) {
    try {
        fs.writeFileSync(SESSION_FILE, JSON.stringify(sessions, null, 2));
    } catch (e) {
        console.error("Failed to save sessions", e);
    }
}

const tools: Anthropic.Tool[] = [
  {
    name: "read_file",
    description: "Read the content of a file.",
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
    description: "Write content to a file.",
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
  {
    name: "execute_command",
    description: "Execute a shell command. Maintains CWD and environment across calls in a session.",
    input_schema: {
      type: "object",
      properties: {
        command: { type: "string", description: "The shell command to execute." },
      },
      required: ["command"],
    },
  },
];

export async function POST(req: NextRequest) {
  try {
    const { messages, apiKey, model, sessionId = "default", systemAction } = await req.json();

    if (!apiKey) {
      return NextResponse.json({ error: "API Key required" }, { status: 401 });
    }

    const sessions = loadSessions();

    // Initialize or retrieve session state
    if (!sessions[sessionId]) {
      sessions[sessionId] = {
        cwd: path.resolve(process.cwd(), ".."),
        env: { ...process.env } as Record<string, string>
      };
    }
    const session = sessions[sessionId];

    // Handle Direct System Actions (Bypasses Claude)
    if (systemAction) {
        if (systemAction.type === "set_cwd") {
            const targetPath = path.resolve(session.cwd, systemAction.path);
            if (fs.existsSync(targetPath) && fs.lstatSync(targetPath).isDirectory()) {
                session.cwd = targetPath;
                saveSessions(sessions);
                return NextResponse.json({ 
                    content: `System: CWD updated to ${session.cwd}`,
                    session: { cwd: session.cwd } 
                });
            } else {
                return NextResponse.json({ error: "Directory not found" }, { status: 404 });
            }
        }
    }

    const anthropic = new Anthropic({ apiKey });

    // Read System Instructions
    let systemInstructions = "";
    try {
        const rootPath = path.resolve(process.cwd(), "..");
        const readme = fs.readFileSync(path.join(rootPath, "README.md"), "utf-8");
        const agents = fs.readFileSync(path.join(rootPath, "AGENTS.md"), "utf-8");
        systemInstructions = `YOU ARE THE CHIRALITY APP AGENT. ADHERE TO THE FOLLOWING PROJECT SPECIFICATIONS:\n\n${readme}\n\n${agents}\n\nCURRENT WORKING DIRECTORY: ${session.cwd}\nENVIRONMENT IS PERSISTENT. USE execute_command FOR SHELL TASKS. USE read_file/write_file FOR FILE EDITS.`;
    } catch (e) {
        systemInstructions = "You are a DevOps assistant.";
    }

    let currentMessages = [...messages];
    const MODEL = model || "claude-3-5-haiku-latest";
    
    const msg = await anthropic.messages.create({
      model: MODEL,
      max_tokens: 4096,
      system: systemInstructions,
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
            if (toolName === "read_file") {
                const fullPath = path.resolve(session.cwd, toolInput.path);
                toolResultContent = fs.readFileSync(fullPath, "utf-8");
            } else if (toolName === "write_file") {
                const fullPath = path.resolve(session.cwd, toolInput.path);
                fs.mkdirSync(path.dirname(fullPath), { recursive: true });
                fs.writeFileSync(fullPath, toolInput.content);
                toolResultContent = "Success: Written.";
            } else if (toolName === "list_directory") {
                const fullPath = path.resolve(session.cwd, toolInput.path);
                const files = fs.readdirSync(fullPath);
                toolResultContent = files.join(String.fromCharCode(10));
            } else if (toolName === "execute_command") {
                if (toolInput.command.trim().startsWith("cd ")) {
                    const newDir = toolInput.command.trim().substring(3).trim();
                    const targetPath = path.resolve(session.cwd, newDir);
                    if (fs.existsSync(targetPath) && fs.lstatSync(targetPath).isDirectory()) {
                        session.cwd = targetPath;
                        toolResultContent = `Changed directory to: ${session.cwd}`;
                    } else {
                        toolResultContent = `Error: Directory not found: ${newDir}`;
                    }
                } else {
                    const { stdout, stderr } = await execAsync(toolInput.command, { 
                        cwd: session.cwd,
                        env: session.env as NodeJS.ProcessEnv 
                    });
                    toolResultContent = stdout || stderr || "(No output)";
                }
            }
          } catch (e: any) {
            toolResultContent = `Error: ${e.message}`;
          }

          toolResults.push({
            type: "tool_result",
            tool_use_id: contentBlock.id,
            content: toolResultContent,
          });
        }
      }

      currentMessages.push({ role: "user", content: toolResults as any });

      const finalMsg = await anthropic.messages.create({
        model: MODEL,
        max_tokens: 4096,
        system: systemInstructions,
        messages: currentMessages,
      });

      saveSessions(sessions);
      return NextResponse.json({ ...finalMsg, session: { cwd: session.cwd } });
    }

    saveSessions(sessions);
    return NextResponse.json({ ...msg, session: { cwd: session.cwd } });

  } catch (error: any) {
    console.error("Chat API Error:", error);
    return NextResponse.json({ error: error.message }, { status: 500 });
  }
}
