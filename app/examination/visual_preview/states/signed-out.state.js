// J1: the launch after setup. The saved request was admitted; Codex is ready in the new App-owned home; the App's own
// account read at ready answered with no account; the stored conversations were read to the end and list none.
// The first view moves to Settings & tools with Connection and access open at the sign-in (App.tsx first-view rule).
import { readyHost, accountRead, historyEmpty } from "./_shared.js";
import { selfIssued, availableModels } from "./_commands.js";

export default {
  title: "Relaunch: Codex ready, not signed in",
  host: readyHost({ ...accountRead(null), nativeHistory: historyEmpty() }),
  commands: selfIssued({ read_available_models: availableModels }),
};
