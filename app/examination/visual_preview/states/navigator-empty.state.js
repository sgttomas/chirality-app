// No projects yet: the App was launched with no project, the records store lists no folder, and Codex lists no
// conversation. The panel says so in the App's words; it says it only for an answer, never for a reading that failed.
import { workflowRoot } from "./_shared.js";
import { selfIssued } from "./_commands.js";
import { navigatorAnswer } from "./_navigator.js";
import { navigatorHost } from "./_navigator-host.js";

export default {
  title: "Navigator: no projects or conversations yet",
  // As pick-no-project: no explicit App project, so no project library either.
  host: navigatorHost({ over: { currentAppProjectContext: null, currentAppProjectContextLimit: "explicit App project reference not established", workflowRoot: workflowRoot({ projectLibraryAvailable: false }) } }),
  commands: selfIssued({ navigator_read: navigatorAnswer([]) }),
};
