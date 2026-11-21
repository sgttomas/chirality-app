import { StrictMode } from "react";
import { createRoot } from "react-dom/client";

import { applyTheme, describeError, Store, storedTheme, type EngineClient, type Host, type PanelTab } from "@chirality/engine-ui";
import { inTauri } from "@chirality/engine-ui/tauri";
import "@chirality/engine-ui/tokens.css";
import "@chirality/engine-ui/page.css";

import { Root } from "./App";

interface Start {
  engine: EngineClient;
  host: Host;
  project?: string;
  thread?: string;
  panel?: PanelTab;
}

/** The real engine inside the app; the scripted fake in a browser (`?scene=` picks where it starts). */
async function connect(): Promise<Start> {
  if (inTauri()) {
    const { tauriEngine, tauriHost } = await import("@chirality/engine-ui/tauri");
    return { engine: tauriEngine, host: tauriHost };
  }
  const { buildScene, fakeHost, sceneNames } = await import("@chirality/engine-ui/fake");
  const asked = new URLSearchParams(location.search).get("scene");
  const name = sceneNames.find((n) => n === asked) ?? "home";
  return { ...(await buildScene(name)), host: fakeHost };
}

async function boot() {
  const theme = new URLSearchParams(location.search).get("theme");
  applyTheme(theme === "dark" || theme === "system" ? theme : storedTheme());
  const start = await connect();
  const store = new Store(start.engine, start.host);
  const started = store.start().then(
    async () => {
      if (start.thread) await store.selectThread(start.thread);
      else if (start.project) store.selectProject(start.project);
      return null;
    },
    (e: unknown) => describeError(e),
  );
  createRoot(document.getElementById("root")!).render(
    <StrictMode>
      <Root store={store} started={started} panel={start.panel} />
    </StrictMode>,
  );
}

void boot();
