/** A16's standing uses closed App sentences. Supplied record identifiers that do not fit
 * are placeholders here; native_text gives those values their labelled native form. */
const CAUSES = [
  "The decision records could not all be read",
  "The record history may be incomplete",
  "The request could not be resolved uniquely",
  "The request was not found in the decision view",
  "The request's recorded standing could not be resolved",
];
type Standing = {form?: string; alternative?: unknown; recordedAt?: unknown; cause?: unknown};
type Other = Standing & {requestRef?: unknown; relation?: unknown; differentContent?: unknown};
const identifier = (v: unknown) => typeof v === "string" && /^[A-Za-z0-9_.:/-]{1,128}$/.test(v) ? v : "(a value the App does not show here)";
const time = (v: unknown) => typeof v === "string" && /^[0-9][0-9T.Z+:-]{0,39}$/.test(v) ? v : "(recording time not uniquely established)";
const cause = (v: unknown) => typeof v === "string" && CAUSES.includes(v) ? v : CAUSES[4];

export function packageStandingLine(value?: Standing): string {
  switch (value?.form) {
    case "decided": return `A decision on this request is already recorded: alternative ${identifier(value.alternative)}, recorded at ${time(value.recordedAt)}. Deciding again records another decision; both are kept.`;
    case "several-unordered": return "Several decisions on this request are recorded, and the records do not establish which stands. Deciding again records another decision; all are kept.";
    case "none-recorded": return "No decision on this request is recorded.";
    default: return `Whether a decision on this request is already recorded is not known: ${cause(value?.cause)}.`;
  }
}
export function otherRequestLine(row: Other): string {
  const prefix = row.relation === "earlier" ? "An earlier request" : row.relation === "later" ? "A later request" : "Another request";
  const ref = identifier(row.requestRef);
  let line: string;
  switch (row.form) {
    case "decided": line = `${prefix} for the file at this path has a recorded decision: alternative ${identifier(row.alternative)}, recorded at ${time(row.recordedAt)} (request ${ref}).`; break;
    case "several-unordered": line = `${prefix} for the file at this path: decisions recorded, order not established (request ${ref}).`; break;
    case "none-recorded": line = `${prefix} for the file at this path: no decision recorded (request ${ref}).`; break;
    default: line = `${prefix} for the file at this path: standing not known: ${cause(row.cause)} (request ${ref}).`;
  }
  return line + (row.differentContent === true ? " It was made on different content." : "");
}
export function PackageStanding({standing, other}: {standing?: Standing; other?: {state?: string; rows?: Other[]}}) {
  return <div aria-label="Recorded standing for this request and path">
    <p>{packageStandingLine(standing)}</p>
    {other?.state !== "read-whole" && <p>Other requests for the file at this path could not all be read.</p>}
    {(other?.rows ?? []).map((row, i) => <p key={i}>{otherRequestLine(row)}</p>)}
  </div>;
}
