// The chosen workflow's required-tool check, in the person's words, before a
// run starts (DEL-02-03 REQ-001). It reads the host's own evaluation of the
// selection; it never infers a requirement from the workflow's prose, never
// reads an undeclared workflow as needing nothing, and never blocks a start.
type Json = any; // eslint-disable-line @typescript-eslint/no-explicit-any
const list = (value: Json): Json[] => (Array.isArray(value) ? value : []);
const text = (value: Json): string => (typeof value === "string" ? value : "");

/** How a declared tool reads, with why when the App could not say it is available. */
export function toolReading(tool: Json, row: Json): { state: "available" | "missing" | "unknown"; words: string } {
  const outcome = text(row?.outcome), reason = text(row?.reason);
  const delegation = tool?.class === "harness_capability" && tool?.capability === "agent-delegation";
  if (outcome === "present") return { state: "available", words: "Available." };
  if (outcome === "present_currently_unavailable") return { state: "available", words: "Present, but not available at the moment." };
  if (outcome === "missing") {
    if (delegation && reason.includes("multiAgentVersion disabled")) return { state: "missing", words: "Missing: this conversation's model doesn't offer sub-agents." };
    if (delegation && reason.includes("multi_agent = false")) return { state: "missing", words: "Missing: your Codex settings turn sub-agents off." };
    if (tool?.class === "host_operation") return { state: "missing", words: "Missing: the connected application doesn't offer it." };
    return { state: "missing", words: "Missing: Codex reports it isn't offered in this conversation." };
  }
  if (outcome === "version_mismatch") return { state: "missing", words: "Missing: the connected application offers another version of it." };
  if (outcome === "not_exposed_on_this_surface") return { state: "missing", words: "Missing: the connected application doesn't offer it to the App." };
  if (outcome === "channel_not_enabled") return { state: "missing", words: "Missing: the connection to that application isn't turned on." };
  const why = row === undefined ? "the App made no check for it"
    : tool?.class === "host_operation" ? "it belongs to a connected application, and this App isn't connected to one, so it can't see what that application offers"
    : reason.includes("no adopted supplier availability account") ? "at the Codex version this App runs, the App has no confirmed way to tell whether Codex offers it"
    : delegation && reason.includes("signals not read") ? "the App hasn't yet read whether this conversation's model offers sub-agents; it reads that shortly after a conversation starts"
    : delegation ? "the App couldn't read whether this conversation's model offers sub-agents"
    : reason.includes("element not established") ? "the App couldn't read how this tool is declared"
    : "the App couldn't tell";
  return { state: "unknown", words: `Couldn't be established: ${why}.` };
}

/** The check for the chosen workflow. `selection` is the host's selection row. */
export function RequirementCheck({ selection }: { selection: Json }) {
  const compatibility = selection?.compatibility;
  const preparation = compatibility?.preparation;
  const declaration = preparation?.declaration ?? selection?.declaration;
  const category = declaration?.categories?.required_tools;
  const label = "Tools this workflow needs";
  if (!declaration || declaration.reading === "undeclared" || category === "undeclared" || category === undefined && declaration.reading === "recognized")
    return <div aria-label={label}><p role="note">This workflow's required tools aren't declared, so the App can't say which tools it needs or whether this conversation has them. That isn't a fault, and it doesn't mean the workflow needs none. You can still start it.</p></div>;
  if (declaration.reading !== "recognized" || category !== "recognized" && category !== "declared_empty")
    return <div aria-label={label}><p role="note">The App couldn't read this workflow's declared tools, so it can't say which ones it needs. You can still start it.</p></div>;
  if (category === "declared_empty")
    return <div aria-label={label}><p role="note">This workflow declares that it needs no tools.</p></div>;
  const elements = list(declaration?.elements?.required_tools);
  const rows = list(preparation?.requirements);
  const tools = elements.map((element: Json, index: number) => {
    const tool = element?.value ?? {};
    const reading = toolReading(tool, preparation ? rows[index] : undefined);
    return { tool, reading, required: tool.necessity !== "optional" };
  });
  const required = tools.filter(t => t.required), optional = tools.filter(t => !t.required);
  const missing = required.filter(t => t.reading.state === "missing").length;
  const unknown = required.filter(t => t.reading.state === "unknown").length;
  const result = text(preparation?.check?.result);
  const summary = !preparation ? "The App couldn't check this workflow's tools for this conversation. You can still start it."
    : missing ? `Requirement check not passed: ${missing === 1 ? "one required tool is" : `${missing} required tools are`} missing. You can still start the run; the agent may be unable to do the steps that use ${missing === 1 ? "it" : "them"}.`
    : unknown ? `Requirement check not established: the App couldn't tell whether ${unknown === 1 ? "one required tool is" : `${unknown} required tools are`} available. You can still start the run.`
    : result === "compatible" ? "Requirement check passed: every required tool was available to this conversation when the App checked. This says what the App could see, not that the run will succeed."
    : result === "unsupported" ? "Requirement check not passed for this conversation, though every required tool was available: the workflow is written for a different conversation role than this one's. You can still start the run."
    : "Requirement check not established for this conversation. You can still start the run.";
  const pin = text(preparation?.basis?.acting_pin).replace(/^App /, "");
  const sentence = (value: Json) => { const words = text(value).trim(); return words && !/[.!?]$/.test(words) ? `${words}.` : words; };
  const item = ({ tool, reading }: { tool: Json; reading: { words: string } }, index: number) =>
    <li key={index}><strong>{text(tool.name) || "Unnamed tool"}</strong>{sentence(tool.purpose) ? <> — {sentence(tool.purpose)}</> : "."} {reading.words}
      {tool.necessity === "optional" && tool.fallback ? <> <small>Without it: {text(tool.fallback)}</small></> : null}</li>;
  return <div aria-label={label}>
    <p role="note">{summary}</p>
    {required.length > 0 && <ul aria-label="Required tools">{required.map(item)}</ul>}
    {optional.length > 0 && <><p>Optional tools; the workflow can go on without them:</p><ul aria-label="Optional tools">{optional.map(item)}</ul></>}
    {preparation && <p><small>Checked for this conversation{pin ? ` with ${pin}` : ""}. The App isn't connected to another application, so it read no application's list of operations.</small></p>}
  </div>;
}
