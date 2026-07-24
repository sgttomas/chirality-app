import { readFile } from "node:fs/promises";
import {
  RuntimeClient,
  RuntimeTransportError,
  type RuntimeStream
} from "@chirality/runtime-client";
import {
  RuntimeError,
  type Agent1RunRequest,
  type CreateSessionRequest,
  type SessionTurnRequest
} from "@chirality/runtime-contracts";
import {
  resolveCliRuntimePaths,
  runtimeClientOptions,
  type CliRuntimePaths
} from "./config.js";
import { LaunchAgentManager } from "./launch-agent.js";

export interface CliIo {
  stdout(text: string): void;
  stderr(text: string): void;
  readStdin(): Promise<string>;
}

export interface RuntimeCliClient {
  daemonStatus(): Promise<unknown>;
  registerProject(request: {
    manifestPath: string;
    approvedBy: string;
    approvalReference: string;
  }): Promise<unknown>;
  listProjects(): Promise<unknown>;
  projectStatus(projectId: string): Promise<unknown>;
  listModels(): Promise<unknown>;
  activateModel(modelId: string, approvalReference: string): Promise<unknown>;
  createSession(
    projectId: string,
    request: CreateSessionRequest
  ): Promise<unknown>;
  listSessions(projectId: string): Promise<unknown>;
  replaySession(projectId: string, sessionId: string): Promise<unknown>;
  turnSession(
    projectId: string,
    sessionId: string,
    request: SessionTurnRequest
  ): Promise<RuntimeStream>;
  interruptSession(projectId: string, sessionId: string): Promise<unknown>;
  runAgent1(projectId: string, request: Agent1RunRequest): Promise<RuntimeStream>;
}

export interface RuntimeLaunchAgent {
  install(executablePath: string): Promise<void>;
  start(): Promise<void>;
  stop(): Promise<void>;
  status(): Promise<unknown>;
  uninstall(): Promise<void>;
}

export interface CliDependencies {
  client: RuntimeCliClient;
  launchAgent: RuntimeLaunchAgent;
  paths: CliRuntimePaths;
  executablePath: string;
  readTextFile(path: string): Promise<string>;
}

type ParsedArguments = {
  positionals: string[];
  options: Map<string, string | true>;
};

export class CliUsageError extends Error {
  constructor(message: string) {
    super(message);
    this.name = "CliUsageError";
  }
}

function parseArguments(args: readonly string[]): ParsedArguments {
  const positionals: string[] = [];
  const options = new Map<string, string | true>();
  for (let index = 0; index < args.length; index += 1) {
    const argument = args[index];
    if (argument === undefined) continue;
    if (!argument.startsWith("--")) {
      positionals.push(argument);
      continue;
    }
    const equals = argument.indexOf("=");
    if (equals > 2) {
      options.set(argument.slice(2, equals), argument.slice(equals + 1));
      continue;
    }
    const key = argument.slice(2);
    if (key === "json") {
      options.set(key, true);
      continue;
    }
    const value = args[index + 1];
    if (value === undefined || value.startsWith("--")) {
      throw new CliUsageError(`Option --${key} requires a value`);
    }
    options.set(key, value);
    index += 1;
  }
  return { positionals, options };
}

function option(args: ParsedArguments, name: string): string | undefined {
  const value = args.options.get(name);
  return typeof value === "string" ? value : undefined;
}

function requiredOption(args: ParsedArguments, name: string): string {
  const value = option(args, name);
  if (value === undefined || value.length === 0) {
    throw new CliUsageError(`Missing required --${name}`);
  }
  return value;
}

function flag(args: ParsedArguments, name: string): boolean {
  return args.options.get(name) === true;
}

function printJson(io: CliIo, value: unknown, json: boolean): void {
  io.stdout(`${JSON.stringify(value, null, json ? 0 : 2)}\n`);
}

async function streamEvents(
  io: CliIo,
  stream: RuntimeStream,
  json: boolean
): Promise<number> {
  let processExitCode: number | undefined;
  for await (const event of stream) {
    if (processExitCode !== undefined) {
      throw new RuntimeError(
        "INTERNAL_FAILURE",
        "Runtime stream emitted data after terminal process:exit",
        502
      );
    }
    if (json) {
      io.stdout(`${JSON.stringify(event)}\n`);
    } else if (event.type === "chat:delta") {
      io.stdout(event.data.text);
    } else if (event.type === "turn:error") {
      io.stderr(`${event.data.errorType}: ${event.data.message}\n`);
    } else if (event.type === "process:exit" && event.data.exitCode !== 0) {
      io.stderr(`process exited ${event.data.exitCode}\n`);
    } else if (event.type !== "harness:event") {
      io.stdout(`[${event.type}]\n`);
    }
    if (event.type === "process:exit") {
      processExitCode = event.data.exitCode;
    }
  }
  if (processExitCode === undefined) {
    throw new RuntimeError(
      "INTERNAL_FAILURE",
      "Runtime stream ended without terminal process:exit",
      502
    );
  }
  return Number.isInteger(processExitCode) && processExitCode > 0
    ? processExitCode
    : processExitCode === 0
      ? 0
      : 1;
}

async function readRequestFile<T>(
  path: string,
  deps: CliDependencies
): Promise<T> {
  let value: unknown;
  try {
    value = JSON.parse(await deps.readTextFile(path));
  } catch {
    throw new CliUsageError(`Request file is not valid JSON: ${path}`);
  }
  if (typeof value !== "object" || value === null || Array.isArray(value)) {
    throw new CliUsageError(`Request file must contain a JSON object: ${path}`);
  }
  return value as T;
}

async function readPrompt(
  args: ParsedArguments,
  io: CliIo,
  deps: CliDependencies
): Promise<SessionTurnRequest> {
  const requestFile = option(args, "request-file");
  if (requestFile !== undefined) {
    return readRequestFile<SessionTurnRequest>(requestFile, deps);
  }
  const prompt = option(args, "prompt") ?? (await io.readStdin()).trim();
  if (!prompt) {
    throw new CliUsageError(
      "Session turn requires --prompt, --request-file, or standard input"
    );
  }
  return { prompt };
}

async function readRunRequest(
  args: ParsedArguments,
  io: CliIo,
  deps: CliDependencies
): Promise<{ projectId: string; request: Agent1RunRequest }> {
  const requestFile = option(args, "request-file");
  if (requestFile !== undefined) {
    const input = await readRequestFile<
      Agent1RunRequest & { project?: string; agent?: string }
    >(requestFile, deps);
    const projectId = option(args, "project") ?? input.project;
    if (!projectId) throw new CliUsageError("Run request requires --project");
    const { project: _project, agent: legacyAgent, ...request } = input;
    return {
      projectId,
      request: {
        ...request,
        agentId: input.agentId ?? option(args, "agent") ?? legacyAgent
      }
    };
  }

  const projectId = requiredOption(args, "project");
  const agentId = requiredOption(args, "agent");
  const briefFile = option(args, "brief-file");
  const localModel = option(args, "local-model");
  const brief =
    briefFile === undefined
      ? (await io.readStdin()).trim()
      : (await deps.readTextFile(briefFile)).trim();
  if (!brief) {
    throw new CliUsageError(
      "Run requires --brief-file, --request-file, or standard input"
    );
  }
  return {
    projectId,
    request: {
      brief,
      agentId,
      approvalReference:
        option(args, "approval-reference") ?? `cli-agent1:${agentId}`,
      ...(localModel === undefined
        ? {}
        : {
            localModel,
            readOnlyTool: {
              name: "read_file",
              relativePath: option(args, "read-file") ?? "chirality.project.json"
            }
          })
    }
  };
}

export async function runCli(
  argv: readonly string[],
  io: CliIo,
  deps: CliDependencies
): Promise<number> {
  try {
    const group = argv[0];
    if (!group) throw new CliUsageError("A command is required");
    const action = group === "run" ? undefined : argv[1];
    const rest = group === "run" ? argv.slice(1) : argv.slice(2);
    const args = parseArguments(rest);
    const json = flag(args, "json");

    if (group === "daemon") {
      if (action === "install") {
        await deps.launchAgent.install(
          option(args, "executable") ?? deps.executablePath
        );
        printJson(io, { installed: true }, json);
      } else if (action === "start") {
        await deps.launchAgent.start();
        printJson(io, { started: true }, json);
      } else if (action === "stop") {
        await deps.launchAgent.stop();
        printJson(io, { stopped: true }, json);
      } else if (action === "status") {
        printJson(
          io,
          {
            launchAgent: await deps.launchAgent.status(),
            daemon: await deps.client.daemonStatus()
          },
          json
        );
      } else if (action === "uninstall") {
        await deps.launchAgent.uninstall();
        printJson(io, { uninstalled: true }, json);
      } else {
        throw new CliUsageError(
          "daemon requires install, start, stop, status, or uninstall"
        );
      }
      return 0;
    }

    if (group === "project") {
      if (action === "register") {
        const manifestPath =
          option(args, "manifest") ?? args.positionals[0];
        if (!manifestPath) {
          throw new CliUsageError(
            "project register requires a manifest path or --manifest"
          );
        }
        printJson(
          io,
          await deps.client.registerProject({
            manifestPath,
            approvedBy: option(args, "approved-by") ?? "local-operator",
            approvalReference:
              option(args, "approval-reference") ?? "cli-explicit-registration"
          }),
          json
        );
      } else if (action === "list") {
        printJson(io, await deps.client.listProjects(), json);
      } else if (action === "status") {
        printJson(
          io,
          await deps.client.projectStatus(
            option(args, "project") ?? args.positionals[0] ??
              requiredOption(args, "project")
          ),
          json
        );
      } else {
        throw new CliUsageError("project requires register, list, or status");
      }
      return 0;
    }

    if (group === "models") {
      if (action === "list") {
        printJson(io, await deps.client.listModels(), json);
      } else if (action === "activate") {
        const modelId =
          option(args, "model") ?? args.positionals[0];
        if (!modelId) throw new CliUsageError("models activate requires an exact model ID");
        printJson(
          io,
          await deps.client.activateModel(
            modelId,
            option(args, "approval-reference") ??
              "cli-explicit-model-activation"
          ),
          json
        );
      } else {
        throw new CliUsageError("models requires list or activate");
      }
      return 0;
    }

    if (group === "session") {
      const projectId = requiredOption(args, "project");
      if (action === "create") {
        const requestFile = option(args, "request-file");
        const request =
          requestFile === undefined
            ? {
                projectId,
                role: requiredOption(args, "role") as CreateSessionRequest["role"],
                engineSelection: {
                  adapterId: requiredOption(args, "adapter"),
                  providerId: requiredOption(args, "provider"),
                  model: requiredOption(args, "model")
                },
                ...(option(args, "parent-session") === undefined
                  ? {}
                  : { parentSessionId: option(args, "parent-session") })
              }
            : await readRequestFile<CreateSessionRequest>(requestFile, deps);
        printJson(io, await deps.client.createSession(projectId, request), json);
      } else if (action === "list") {
        printJson(io, await deps.client.listSessions(projectId), json);
      } else {
        const sessionId =
          option(args, "session") ?? args.positionals[0];
        if (!sessionId) {
          throw new CliUsageError(`session ${action ?? ""} requires --session`);
        }
        if (action === "replay") {
          printJson(io, await deps.client.replaySession(projectId, sessionId), json);
        } else if (action === "turn") {
          return await streamEvents(
            io,
            await deps.client.turnSession(
              projectId,
              sessionId,
              await readPrompt(args, io, deps)
            ),
            json
          );
        } else if (action === "interrupt") {
          printJson(
            io,
            await deps.client.interruptSession(projectId, sessionId),
            json
          );
        } else {
          throw new CliUsageError(
            "session requires create, list, replay, turn, or interrupt"
          );
        }
      }
      return 0;
    }

    if (group === "run") {
      const run = await readRunRequest(args, io, deps);
      return await streamEvents(
        io,
        await deps.client.runAgent1(run.projectId, run.request),
        json
      );
    }

    throw new CliUsageError(`Unknown command: ${argv.join(" ")}`);
  } catch (error) {
    if (error instanceof CliUsageError) {
      io.stderr(`chirality: ${error.message}\n`);
      return 2;
    }
    if (error instanceof RuntimeError) {
      io.stderr(`${error.code}: ${error.message}\n`);
      return error.code === "INTERRUPTED" ? 130 : 1;
    }
    if (error instanceof RuntimeTransportError) {
      io.stderr(`RUNTIME_UNAVAILABLE: ${error.message}\n`);
      return 1;
    }
    io.stderr(`INTERNAL_FAILURE: ${error instanceof Error ? error.message : String(error)}\n`);
    return 1;
  }
}

async function readStandardInput(): Promise<string> {
  const chunks: Buffer[] = [];
  for await (const chunk of process.stdin) {
    chunks.push(Buffer.isBuffer(chunk) ? chunk : Buffer.from(chunk));
  }
  return Buffer.concat(chunks).toString("utf8");
}

export function createDefaultCliDependencies(): CliDependencies {
  const paths = resolveCliRuntimePaths();
  return {
    paths,
    client: new RuntimeClient(runtimeClientOptions(paths)),
    launchAgent: new LaunchAgentManager({
      launchAgentsDirectory: paths.launchAgentsDirectory,
      runtimeDirectory: paths.runtimeDirectory
    }),
    executablePath: process.execPath,
    readTextFile: (path) => readFile(path, "utf8")
  };
}

export const processCliIo: CliIo = {
  stdout(text) {
    process.stdout.write(text);
  },
  stderr(text) {
    process.stderr.write(text);
  },
  readStdin: readStandardInput
};
