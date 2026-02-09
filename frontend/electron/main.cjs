/* eslint-disable @typescript-eslint/no-require-imports */
const { app, BrowserWindow, shell, dialog } = require("electron");
const fs = require("node:fs");
const http = require("node:http");
const path = require("node:path");
const next = require("next");

const WEB_HOST = "127.0.0.1";
const DEFAULT_WEB_PORT = 33077;

let nextServer = null;
let nextInstance = null;
let mainWindow = null;
let lastServerUrl = null;

function isInstructionRoot(rootPath) {
  const required = ["AGENTS.md", "README.md", "agents"];
  try {
    for (const entry of required) {
      if (!fs.existsSync(path.join(rootPath, entry))) {
        return false;
      }
    }

    return fs.statSync(path.join(rootPath, "agents")).isDirectory();
  } catch {
    return false;
  }
}

function resolveFrontendRoot() {
  return path.resolve(__dirname, "..");
}

function resolveInstructionRoot(frontendRoot) {
  const fromEnv = process.env.CHIRALITY_INSTRUCTION_ROOT;
  if (fromEnv && isInstructionRoot(fromEnv)) {
    return path.resolve(fromEnv);
  }

  if (app.isPackaged) {
    const packagedRoot = path.join(process.resourcesPath, "instruction-root");
    if (isInstructionRoot(packagedRoot)) {
      return packagedRoot;
    }
  }

  const repoRoot = path.resolve(frontendRoot, "..");
  if (isInstructionRoot(repoRoot)) {
    return repoRoot;
  }

  return repoRoot;
}

function resolveWebPort() {
  const configured = Number.parseInt(process.env.CHIRALITY_APP_PORT ?? "", 10);
  if (Number.isFinite(configured) && configured > 0) {
    return configured;
  }

  return DEFAULT_WEB_PORT;
}

async function startNextServer(frontendRoot, serverPort, isDev) {
  nextInstance = next({
    dev: isDev,
    dir: frontendRoot,
    hostname: WEB_HOST,
    port: serverPort,
  });

  await nextInstance.prepare();
  const requestHandler = nextInstance.getRequestHandler();

  nextServer = http.createServer((req, res) => {
    void requestHandler(req, res);
  });

  await new Promise((resolve, reject) => {
    if (!nextServer) {
      reject(new Error("Next.js server failed to initialize."));
      return;
    }

    nextServer.once("error", reject);
    nextServer.listen(serverPort, WEB_HOST, () => resolve());
  });
}

function createWindow(targetUrl) {
  mainWindow = new BrowserWindow({
    width: 1520,
    height: 980,
    minWidth: 1100,
    minHeight: 720,
    backgroundColor: "#0f172a",
    autoHideMenuBar: true,
    webPreferences: {
      preload: path.join(__dirname, "preload.cjs"),
      contextIsolation: true,
      nodeIntegration: false,
      sandbox: true,
    },
  });

  mainWindow.loadURL(targetUrl).catch((error) => {
    dialog.showErrorBox("Failed to load Chirality App", String(error));
  });

  mainWindow.webContents.setWindowOpenHandler(({ url }) => {
    void shell.openExternal(url);
    return { action: "deny" };
  });

  mainWindow.on("closed", () => {
    mainWindow = null;
  });
}

async function stopNextServer() {
  if (!nextServer) {
    return;
  }

  await new Promise((resolve) => {
    if (!nextServer) {
      resolve(undefined);
      return;
    }

    nextServer.close(() => resolve(undefined));
  });

  nextServer = null;
  nextInstance = null;
}

async function bootstrap() {
  const isDev = process.env.CHIRALITY_ELECTRON_DEV === "1" || !app.isPackaged;
  const frontendRoot = resolveFrontendRoot();
  const instructionRoot = resolveInstructionRoot(frontendRoot);

  process.env.CHIRALITY_INSTRUCTION_ROOT = instructionRoot;

  const serverPort = resolveWebPort();

  try {
    await startNextServer(frontendRoot, serverPort, isDev);
    lastServerUrl = `http://${WEB_HOST}:${serverPort}`;
    createWindow(lastServerUrl);
  } catch (error) {
    dialog.showErrorBox("Chirality App failed to start", String(error));
    await stopNextServer();
    app.quit();
  }
}

app.on("ready", () => {
  void bootstrap();
});

app.on("window-all-closed", () => {
  if (process.platform !== "darwin") {
    app.quit();
  }
});

app.on("activate", () => {
  if (!mainWindow && lastServerUrl) {
    createWindow(lastServerUrl);
  }
});

app.on("before-quit", () => {
  void stopNextServer();
});
