// The Workflows tab when the project's registration ledger cannot be read: its last line has no newline, so
// registered_listing reports the limit (workflow_library.rs read_ledger) and the entry listing that open_project_library
// observes at once is unavailable for the same cause (workflow_library_entries.rs EntryListing::observe → scan).
import { readyHost, accountRead, CHATGPT_ACCOUNT, signInCompleted, threadRow, workflowRoot, projectLibrary, LIBRARY_REF, PROJECT, nativePath, at, historyEmpty } from "./_shared.js";
import { selfIssued, pressesAfterMount, chooseWorkflowsTab } from "./_commands.js";

pressesAfterMount("workflows-tab-ledger-unread", [chooseWorkflowsTab]);

const LEDGER_LIMIT = `registration ledger malformed: ${PROJECT}/.chirality/workflow-registry.jsonl: incomplete final line (no newline) at line 3`;
const unreadLibrary = { ...projectLibrary, registered: { limit: LEDGER_LIMIT },
  entryListing: { reference: "workflow-library-listing:6d8f0b2c-4e6a-4c8e-9a0c-2e4a6c8e0a2c", libraryRef: LIBRARY_REF, observedAt: at(2, 40), state: "unavailable",
    source: { origin: "project", sourceRoot: PROJECT, root: nativePath(PROJECT) }, entries: [], limits: [LEDGER_LIMIT],
    standing: "explicit library observation; files are not registration, selection or an act; refresh to observe changes" } }; // workflow_library_entries.rs STANDING

export default {
  title: "Workflows tab: the project's ledger could not be read",
  host: readyHost({
    ...accountRead(CHATGPT_ACCOUNT),
    homeOAuth: signInCompleted,
    threads: [threadRow()],
    nativeHistory: historyEmpty(),
    workflowRoot: workflowRoot({ libraries: [unreadLibrary], activeLibrary: LIBRARY_REF }),
  }),
  commands: selfIssued(),
};
