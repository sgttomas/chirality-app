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
      if (response && !Array.isArray(response)) outcome = Object.entries(response).filter(([key]) =>
        ["state", "status", "error", "nativeError", "limit", "acknowledged", "sent"].includes(key));
    } catch { /* Keep the supplied text intact in the disclosure. */ }
  }
  return <div className="action-feedback" aria-label={label}>
    {technical ? <>
      <p role="status">A response was received. Check the current state of your work below.</p>
      {outcome.map(([key, value]) => <p role="status" key={key} style={{ whiteSpace: "pre-wrap" }}>{key}: {typeof value === "string" ? value : JSON.stringify(value)}</p>)}
      <details><summary>Response details</summary><pre>{message}</pre></details>
    </> : <p role="status" style={{ whiteSpace: "pre-wrap" }}>{message}</p>}
  </div>;
}
