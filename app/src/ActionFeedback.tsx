/** Presentation only: retain the response exactly, without interpreting a
 * native acknowledgment as completed work or an accepted workflow. */
export function ActionFeedback({ message, label = "Latest App response" }: { message: string; label?: string }) {
  if (!message) return null;
  const technical = /^[^:\n]+:\s*[\[{]/.test(message);
  return <div className="action-feedback" aria-label={label}>
    {technical ? <>
      <p role="status">A response was received. Check the current state of your work below.</p>
      <details><summary>Response details</summary><pre>{message}</pre></details>
    </> : <p role="status" style={{ whiteSpace: "pre-wrap" }}>{message}</p>}
  </div>;
}
