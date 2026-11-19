// The chosen workflow's required-tool check, in the person's words, before a
// run starts (DEL-02-03 REQ-001). It reads the host's own evaluation of the
// selection; it never infers a requirement from the workflow's prose, never
// reads an undeclared workflow as needing nothing, and never blocks a start.
type Json = any; // eslint-disable-line @typescript-eslint/no-explicit-any
const list = (value: Json): Json[] => (Array.isArray(value) ? value : []);
const text = (value: Json): string => (typeof value === "string" ? value : "");

/** How a declared tool reads, with why when the App could not say it is available. */
export type ToolState = "available" | "unavailable" | "missing" | "unknown";
export function toolReading(tool: Json, row: Json): { state: ToolState; words: string } {
  const outcome = text(row?.outcome), reason = text(row?.reason);
  const delegation = tool?.class === "harness_capability" && tool?.capability === "agent-delegation";
  if (outcome === "present") return { state: "available", words: delegation ? "Available as native tools; child execution and remaining capacity are not established." : "Available." };
  // Present but not available now is not available: the host counts it as a hold on the run, not as passing.
  if (outcome === "present_currently_unavailable") return { state: "unavailable", words: "Present, but not available at the moment." };
  if (outcome === "missing") {
    if (delegation && reason.includes("multiAgentVersion disabled")) return { state: "missing", words: "Missing: this conversation's model doesn't offer sub-agents." };
    if (delegation && reason.includes("agents.enabled is false")) return { state: "missing", words: "Missing: your Codex settings turn sub-agents off." };
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
    : delegation && reason.includes("features.multi_agent_v2") ? "features.multi_agent_v2 is set; the App could not establish native tool availability for that setting"
    : delegation && reason.includes("features.multi_agent") ? "features.multi_agent is set; the legacy setting alone does not establish delegation"
    : delegation && reason.includes("agents.enabled") ? "agents.enabled is set; the App could not establish delegation for that setting"
    : delegation ? "the App couldn't read whether this conversation's model offers sub-agents"
    : reason.includes("element not established") ? "the App couldn't read how this tool is declared"
    : "the App couldn't tell";
  return { state: "unknown", words: `Couldn't be established: ${why}.` };
}

/** The declared required-tool part of a selection as the App reads it: undeclared, unreadable, declared empty, or the
 * declared tools, each with the host's evaluation for this conversation where it made one. The guide's check and the
 * composer's line beside a picked workflow both read it, so the two cannot disagree. */
export type RequirementReading =
  | { kind: "undeclared" } | { kind: "unreadable" } | { kind: "empty" }
  | { kind: "tools"; checked: boolean; preparation: Json; tools: { tool: Json; reading: { state: ToolState; words: string }; required: boolean }[] };
export function requirementReading(selection: Json): RequirementReading {
  const preparation = selection?.compatibility?.preparation;
  const declaration = preparation?.declaration ?? selection?.declaration;
  const category = declaration?.categories?.required_tools;
  if (!declaration || declaration.reading === "undeclared" || category === "undeclared" || category === undefined && declaration.reading === "recognized") return { kind: "undeclared" };
  if (declaration.reading !== "recognized" || category !== "recognized" && category !== "declared_empty") return { kind: "unreadable" };
  if (category === "declared_empty") return { kind: "empty" };
  const rows = list(preparation?.requirements);
  return { kind: "tools", checked: !!preparation, preparation, tools: list(declaration?.elements?.required_tools).map((element: Json, index: number) => {
    const tool = element?.value ?? {};
    return { tool, reading: toolReading(tool, preparation ? rows[index] : undefined), required: tool.necessity !== "optional" };
  }) };
}

/** The check for the chosen workflow. `selection` is the host's selection row. */
export function RequirementCheck({ selection }: { selection: Json }) {
  const label = "Tools this workflow needs";
  const read = requirementReading(selection);
  if (read.kind === "undeclared")
    return <div aria-label={label}><p role="note">This workflow's required tools aren't declared, so the App can't say which tools it needs or whether this conversation has them. That isn't a fault, and it doesn't mean the workflow needs none. You can still start it.</p></div>;
  if (read.kind === "unreadable")
    return <div aria-label={label}><p role="note">The App couldn't read this workflow's declared tools, so it can't say which ones it needs. You can still start it.</p></div>;
  if (read.kind === "empty")
    return <div aria-label={label}><p role="note">This workflow declares that it needs no tools.</p></div>;
  const { preparation, tools } = read;
  const required = tools.filter(t => t.required), optional = tools.filter(t => !t.required);
  const missing = required.filter(t => t.reading.state === "missing").length;
  const unknown = required.filter(t => t.reading.state === "unknown").length;
  const unavailable = required.filter(t => t.reading.state === "unavailable").length;
  const result = text(preparation?.check?.result);
  const summary = !preparation ? "The App couldn't check this workflow's tools for this conversation. You can still start it."
    : missing ? `Requirement check not passed: ${missing === 1 ? "one required tool is" : `${missing} required tools are`} missing. You can still start the run; the agent may be unable to do the steps that use ${missing === 1 ? "it" : "them"}.`
    : unknown ? `Requirement check not established: the App couldn't tell whether ${unknown === 1 ? "one required tool is" : `${unknown} required tools are`} available. You can still start the run.`
    : unavailable ? `Requirement check not passed now: ${unavailable === 1 ? "one required tool is" : `${unavailable} required tools are`} present but not available at the moment. You can still start the run; the agent may be unable to do the steps that use ${unavailable === 1 ? "it" : "them"}.`
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
