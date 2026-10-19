import { Fragment } from "react";
import { nativePathText } from "./presentation";

type Json = any; // eslint-disable-line @typescript-eslint/no-explicit-any

// WR RB-2: display the frozen presentation, whether received in a review's
// status or as the content named by an open A15 confirmation. No actions,
// reads, normalization or digest input are produced by this component.
const labels: Record<string, string> = {
  review_ref: "Review reference", descriptor_id: "Descriptor identity",
  library: "Library folder", origin: "Origin", source_root: "Source root",
  identity: "Workflow tuple", disposition: "Disposition", message: "Disposition message",
  reviewed_reference: "Reviewed content reference", content: "Content identity",
  kind: "Kind", name: "Name", revision: "Revision", revision_method: "Revision method",
  method: "Method", value: "Value", reconfirmation: "Re-confirmation",
  registration_notice: "Registration notice", declaration: "Declared part (information)",
  reading: "Reading", raw: "Reported declaration", categories: "Categories", elements: "Elements",
  expected_inputs: "Expected inputs", required_tools: "Required tools", checkpoints: "Checkpoints",
  returned_outputs: "Returned outputs", returned_evidence: "Returned evidence", findings: "Findings",
  hygiene: "Package hygiene findings", prior_revision: "Prior revision tuple", base: "Draft base tuple",
  stale_base: "Draft base differs from prior revision", lineage: "Derived-from lineage",
  derived_from: "Derived from", prior_comparison: "Difference against prior revision",
  base_comparison: "Difference against draft base", files: "File manifest", changes: "Changed files",
  path: "Path", bytes: "Bytes", before: "Before", after: "After",
  comparison: "Comparison", unavailable: "Unavailable", reason: "Reason", limit: "Limit",
  evidence_limits: "Evidence limits", ledger_observation: "Registration ledger observation",
  ledger: "Ledger", slot_lines: "Observed slot lines", standing: "Standing",
  base_observation: "App-kept base observation", observed: "Observed source",
  same_name_elsewhere: "Same name elsewhere", compatibility: "Environment compatibility",
  sequence: "Sequence", reconfirms: "Re-confirms", registered_earlier: "Earlier registration observation",
  written_at: "Recorded time", act: "Recorded act", label: "Label", slot_latest: "Slot latest tuple",
  statement: "Statement",
};
const literal = { whiteSpace: "pre-wrap", overflowWrap: "anywhere" } as const;
const record = (value: Json): value is Record<string, Json> => value !== null && typeof value === "object" && !Array.isArray(value);
const own = (value: Json, key: string) => record(value) && Object.hasOwn(value, key);

function ReportedFields({ value, keys = Object.keys(value), literalKeys = false }: { value: Record<string, Json>; keys?: string[]; literalKeys?: boolean }) {
  return <dl>{keys.filter(key => own(value, key)).map(key => <Fragment key={key}>
    <dt>{!literalKeys && Object.hasOwn(labels, key) ? labels[key] : key}</dt><dd><ReportedValue value={value[key]} literalKeys={literalKeys || key === "raw" || key === "value"} /></dd>
  </Fragment>)}</dl>;
}

/** Keep null, an unavailable report, empty values and an omitted field distinct.
 * Unknown keys are displayed too; no registration or compatibility is inferred. */
function ReportedValue({ value, literalKeys = false }: { value: Json; literalKeys?: boolean }) {
  if (value === undefined) return <span>Not reported</span>;
  if (value === null) return <span>Reported null</span>;
  const path = nativePathText(value);
  if (path !== null) return <>
    <span style={literal}>{path}</span>
    <details><summary>Reported path identity</summary><pre style={literal}>{JSON.stringify(value, null, 2)}</pre></details>
  </>;
  if (Array.isArray(value)) return value.length
    ? <ol>{value.map((item, index) => <li key={index}><ReportedValue value={item} literalKeys={literalKeys} /></li>)}</ol>
    : <span>Reported empty list</span>;
  if (record(value)) return Object.keys(value).length
    ? <ReportedFields value={value} literalKeys={literalKeys} /> : <span>Reported empty object</span>;
  return <span style={literal}>{value === "" ? "Reported empty string" : String(value)}</span>;
}

function Manifest({ files }: { files: Json }) {
  if (!Array.isArray(files) || files.length === 0) return <ReportedValue value={files} />;
  return <table><thead><tr><th scope="col">Path</th><th scope="col">Bytes</th><th scope="col">Content identity</th><th scope="col">Other reported fields</th></tr></thead>
    <tbody>{files.map((file, index) => record(file) ? <tr key={index}>
      <td><ReportedValue value={own(file, "path") ? file.path : undefined} /></td>
      <td><ReportedValue value={own(file, "bytes") ? file.bytes : undefined} /></td>
      <td><ReportedValue value={own(file, "content") ? file.content : undefined} /></td>
      <td><ReportedFields value={file} keys={Object.keys(file).filter(key => !["path", "bytes", "content"].includes(key))} /></td>
    </tr> : <tr key={index}><td colSpan={4}><ReportedValue value={file} /></td></tr>)}</tbody>
  </table>;
}

const entryHeader = ["identity", "disposition", "message", "reconfirmation", "reviewed_reference", "content"];
function ReviewEntry({ entry, index }: { entry: Json; index: number }) {
  if (!record(entry)) return <ReportedValue value={entry} />;
  const name = typeof entry.identity?.name === "string" ? entry.identity.name : `Entry ${index + 1}`;
  return <section aria-label={`Reviewed workflow ${index + 1}`}>
    <h4>{name}</h4>
    <ReportedFields value={entry} keys={entryHeader} />
    <h5>WORKFLOW.md</h5>
    {typeof entry.workflow_text === "string"
      ? <pre aria-label="Frozen WORKFLOW.md text" style={literal}>{entry.workflow_text}</pre>
      : <ReportedValue value={own(entry, "workflow_text") ? entry.workflow_text : undefined} />}
    <h5>File manifest</h5><Manifest files={own(entry, "files") ? entry.files : undefined} />
    <ReportedFields value={entry} keys={Object.keys(entry).filter(key => ![...entryHeader, "workflow_text", "files"].includes(key))} />
  </section>;
}

export function WorkflowRegistrationReview({ presentation }: { presentation: Json }) {
  return <div aria-label="Frozen workflow registration review">
    {record(presentation) ? <>
      <ReportedFields value={presentation} keys={Object.keys(presentation).filter(key => key !== "entries")} />
      <h4>Reviewed workflows</h4>
      {Array.isArray(presentation.entries)
        ? presentation.entries.length ? <ol aria-label="Reviewed workflow order">{presentation.entries.map((entry: Json, index: number) => <li key={index}><ReviewEntry entry={entry} index={index} /></li>)}</ol> : <ReportedValue value={presentation.entries} />
        : <ReportedValue value={own(presentation, "entries") ? presentation.entries : undefined} />}
    </> : <ReportedValue value={presentation} />}
    <details><summary>Complete reported review (diagnostic JSON)</summary>
      <pre style={literal}>{JSON.stringify(presentation, null, 2)}</pre>
    </details>
  </div>;
}
