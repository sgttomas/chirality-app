// The open conversation with define-work picked and chosen for it, as pick-chosen, but with an invented declaration of
// three required tools and one input, and the host's evaluation of them for this conversation in its three readings
// (execution_compatibility.rs Outcome: present, present_currently_unavailable, missing). The included define-work
// declares nothing (workflow_declaration::read); this declaration is constructed to show the composer's line before the
// second press and is not the Library's.
import { readyHost, accountRead, CHATGPT_ACCOUNT, signInCompleted, threadRow, workflowRoot, projectLibrary, includedSelection, LIBRARY_REF, historyEmpty, PERSON_TEXT } from "./_shared.js";
import { selfIssued, pressesAfterMount, chooseConversation, chooseWorkflowsTab, pickIncludedCard, typeInComposer } from "./_commands.js";

pressesAfterMount("pick-tools", [chooseConversation, chooseWorkflowsTab, pickIncludedCard("define-work"), typeInComposer(PERSON_TEXT)]);

const tool = (name, capability, purpose) => ({ value: { name, purpose, necessity: "required", stages: ["Method"], class: "harness_capability", capability }, reading: "recognized", findings: [] });
const declaration = { reading: "recognized", findings: [], categories: { required_tools: "recognized", expected_inputs: "recognized" },
  elements: {
    required_tools: [tool("read-notes", "file-read", "Read the survey notes."), tool("run-checks", "shell-command", "Run the report's checks."), tool("delegate", "agent-delegation", "Hand the review to a sub-agent.")],
    expected_inputs: [{ value: { name: "survey notes", necessity: "required", kind: "host_read", meaning: "The notes the report summarises." } }],
  } };
const compatibility = { advisory: true, statement: "requirement check (advisory)",
  preparation: { declaration, check: { result: "compatible", tools: [] }, basis: { acting_pin: "App Codex 0.169.0", surface: "app-server" },
    requirements: [{ outcome: "present", reason: "" }, { outcome: "present_currently_unavailable", reason: "the shell is busy with another command" },
      { outcome: "missing", reason: "agents.enabled is false with neither delegation feature set" }] } };
const chosen = includedSelection("define-work");
chosen.selection = { ...chosen.selection, declaration, compatibility };

export default {
  title: "Conversation: define-work picked and chosen, its required tools in three readings",
  host: readyHost({
    ...accountRead(CHATGPT_ACCOUNT), homeOAuth: signInCompleted,
    threads: [threadRow()],
    nativeHistory: historyEmpty(),
    workflowRoot: workflowRoot({ libraries: [projectLibrary], activeLibrary: LIBRARY_REF, selections: [chosen] }),
  }),
  commands: selfIssued(),
};
