import { AgentText, wordOf } from "./AgentText";
/** The outcome fields of a response the App reports beside it, in the App's words. */
const OUTCOME_FIELDS = { state: "state", status: "status", error: "error", nativeError: "nativeError", limit: "limit", acknowledged: "acknowledged", sent: "sent" } as const;
/** Presentation only: retain the supplied already-safe App response text
 * exactly, without interpreting an acknowledgment as completed/accepted work.
 * Plain errors and refusals stay direct; no private supplier data is fetched. */
export function ActionFeedback({ message, label = "Latest App response" }: { message: string; label?: string }) {
  if (!message) return null;
  const technical = /^[^:\n]+:\s*[\[{]/.test(message);
  // Report explicit App outcome fields verbatim, including negative/unknown
  // acknowledgments. This does not infer success from the other response data.
  let outcome: [string, unknown][] = [];
  if (technical) {
    try {
      const response = JSON.parse(message.slice(message.indexOf(":") + 1));
      if (response && !Array.isArray(response)) outcome = Object.entries(response).filter(([key]) => wordOf(OUTCOME_FIELDS, key) !== null);
    } catch { /* Keep the supplied text intact in the disclosure. */ }
  }
  return <div className="action-feedback" aria-label={label}>
    {technical ? <>
      <p role="status">A response was received. Check the current state of your work below.</p>
      {outcome.map(([key, value]) => <p role="status" key={key}><AgentText value={typeof value === "string" ? value : JSON.stringify(value)} source="record" label={`${wordOf(OUTCOME_FIELDS, key)}:`} name="A field of the response as reported, not the App's words" /></p>)}
      <details><summary>Response details</summary><AgentText block value={message} source="record" /></details>
    </> : <p role="status"><AgentText value={message} source="record" label="Response:" name="The latest response, which may carry text the App received, not only the App's words" /></p>}
  </div>;
}
