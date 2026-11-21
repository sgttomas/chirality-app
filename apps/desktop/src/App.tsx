import { StandardLayout, type PanelTab } from "@chirality/engine-ui";

/** The Chirality App: projects and threads, the conversation, and the side panel. */
export function App({ panel }: { panel?: PanelTab }) {
  return <StandardLayout brand="Chirality" panel={panel} />;
}
