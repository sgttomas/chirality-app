/* eslint-disable @typescript-eslint/no-require-imports */
const { app, BrowserWindow, shell, dialog, ipcMain } = require("electron");
const fs = require("node:fs");
const http = require("node:http");
const https = require("node:https");
const path = require("node:path");
const next = require("next");

const WEB_HOST = "127.0.0.1";
const DEFAULT_WEB_PORT = 33077;
const DEFAULT_RELEASE_REPO = process.env.CHIRALITY_RELEASE_REPO || "sgttomas/chirality-app";
const DEFAULT_RELEASES_API_URL =
  process.env.CHIRALITY_RELEASES_API_URL || `https://api.github.com/repos/${DEFAULT_RELEASE_REPO}/releases/latest`;
const DEFAULT_RELEASE_PAGE_URL =
  process.env.CHIRALITY_RELEASE_PAGE_URL || `https://github.com/${DEFAULT_RELEASE_REPO}/releases/latest`;

let nextServer = null;
let nextInstance = null;
let mainWindow = null;
let lastServerUrl = null;

function normalizeVersion(rawVersion) {
  if (typeof rawVersion !== "string") {
    return "0.0.0";
  }

  const trimmed = rawVersion.trim().replace(/^v/i, "");
  return trimmed || "0.0.0";
}

function parseSemver(version) {
  const match = /^(\d+)\.(\d+)\.(\d+)(?:-([0-9A-Za-z.-]+))?$/.exec(version);
  if (!match) {
    return null;
  }

  return {
    major: Number.parseInt(match[1], 10),
    minor: Number.parseInt(match[2], 10),
    patch: Number.parseInt(match[3], 10),
    pre: match[4] ? match[4].split(".") : [],
  };
}

function comparePreRelease(aParts, bParts) {
  const maxLen = Math.max(aParts.length, bParts.length);
  for (let index = 0; index < maxLen; index += 1) {
    const aRaw = aParts[index];
    const bRaw = bParts[index];

    if (aRaw === undefined) {
      return -1;
    }

    if (bRaw === undefined) {
      return 1;
    }

    const aNumber = /^\d+$/.test(aRaw) ? Number.parseInt(aRaw, 10) : null;
    const bNumber = /^\d+$/.test(bRaw) ? Number.parseInt(bRaw, 10) : null;

    if (aNumber !== null && bNumber !== null) {
      if (aNumber !== bNumber) {
        return aNumber > bNumber ? 1 : -1;
      }
      continue;
    }

    if (aNumber !== null && bNumber === null) {
      return -1;
    }

    if (aNumber === null && bNumber !== null) {
      return 1;
    }

    if (aRaw !== bRaw) {
      return aRaw > bRaw ? 1 : -1;
    }
  }

  return 0;
}

function compareVersions(aRaw, bRaw) {
  const a = parseSemver(normalizeVersion(aRaw));
  const b = parseSemver(normalizeVersion(bRaw));

  if (!a || !b) {
    return normalizeVersion(aRaw).localeCompare(normalizeVersion(bRaw), undefined, { numeric: true });
  }

  if (a.major !== b.major) {
    return a.major > b.major ? 1 : -1;
  }

  if (a.minor !== b.minor) {
    return a.minor > b.minor ? 1 : -1;
  }

  if (a.patch !== b.patch) {
    return a.patch > b.patch ? 1 : -1;
  }

  const aHasPre = a.pre.length > 0;
  const bHasPre = b.pre.length > 0;

  if (!aHasPre && !bHasPre) {
    return 0;
  }

  if (!aHasPre && bHasPre) {
    return 1;
  }

  if (aHasPre && !bHasPre) {
    return -1;
  }

  return comparePreRelease(a.pre, b.pre);
}

async function fetchJson(url) {
  return new Promise((resolve, reject) => {
    const request = https.get(
      url,
      {
        headers: {
          Accept: "application/vnd.github+json",
          "User-Agent": "chirality-app-update-check",
        },
      },
      (response) => {
        const chunks = [];

        response.on("data", (chunk) => {
          chunks.push(chunk);
        });

        response.on("end", () => {
          const status = response.statusCode ?? 0;
          const body = Buffer.concat(chunks).toString("utf8");

          if (status < 200 || status >= 300) {
            reject(new Error(`Update check failed with status ${status}.`));
            return;
          }

          try {
            resolve(JSON.parse(body));
          } catch {
            reject(new Error("Update check returned invalid JSON."));
          }
        });
      },
    );

    request.setTimeout(8000, () => {
      request.destroy(new Error("Update check timed out."));
    });

    request.on("error", reject);
  });
}

async function checkForDesktopUpdate() {
  const currentVersion = normalizeVersion(app.getVersion());
  const payload = await fetchJson(DEFAULT_RELEASES_API_URL);
  const latestTag = typeof payload.tag_name === "string" ? payload.tag_name : null;

  if (!latestTag) {
    throw new Error("Latest release tag is missing.");
  }

  const latestVersion = normalizeVersion(latestTag);
  const updateAvailable = compareVersions(currentVersion, latestVersion) < 0;
  const downloadUrl = typeof payload.html_url === "string" ? payload.html_url : DEFAULT_RELEASE_PAGE_URL;

  return {
    ok: true,
    currentVersion,
    latestVersion,
    latestTag,
    updateAvailable,
    downloadUrl,
    publishedAt: typeof payload.published_at === "string" ? payload.published_at : null,
  };
}

function registerDesktopUpdateHandlers() {
  ipcMain.handle("desktop:update:check", async () => {
    try {
      return await checkForDesktopUpdate();
    } catch (error) {
      return {
        ok: false,
        currentVersion: normalizeVersion(app.getVersion()),
        latestVersion: null,
        latestTag: null,
        updateAvailable: false,
        downloadUrl: DEFAULT_RELEASE_PAGE_URL,
        publishedAt: null,
        error: error instanceof Error ? error.message : "Failed to check for updates.",
      };
    }
  });

  ipcMain.handle("desktop:update:open-download", async (_event, url) => {
    const targetUrl = typeof url === "string" && /^https:\/\//i.test(url) ? url : DEFAULT_RELEASE_PAGE_URL;
    try {
      await shell.openExternal(targetUrl);
      return { ok: true };
    } catch (error) {
      return {
        ok: false,
        error: error instanceof Error ? error.message : "Failed to open download page.",
      };
    }
  });
}

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
  registerDesktopUpdateHandlers();
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
