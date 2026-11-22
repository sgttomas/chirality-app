import { useEffect, useState } from "react";

import { EngineProvider, StandardLayout, type PanelTab, type Store } from "@chirality/engine-ui";

import { featuredWorkflows } from "./workflows";

/** The Chirality App: projects and threads, the conversation, and the side panel. */
export function App({ panel }: { panel?: PanelTab }) {
  return <StandardLayout brand="Chirality" panel={panel} featuredWorkflows={featuredWorkflows} />;
}

/** The app over `store` once it has started; `started` resolves with why it could not, if it could not. */
export function Root({ store, started, panel }: { store: Store; started: Promise<string | null>; panel?: PanelTab }) {
  const [failed, setFailed] = useState<string | null>(null);
  useEffect(() => void started.then(setFailed), [started]);
  return (
    <EngineProvider store={store} fallback={failed ? <StartFailed message={failed} /> : <div className="app-loading" />}>
      <App panel={panel} />
    </EngineProvider>
  );
}

function StartFailed({ message }: { message: string }) {
  return (
    <main className="first-use">
      <div className="first-use-card" role="alert">
        <h1 className="brand">Chirality couldn't start</h1>
        <p>{message}</p>
      </div>
    </main>
  );
}
