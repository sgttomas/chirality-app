type Json = any;

// The plan-mode element (DEL-01-03 §5.3–§5.5, EX-1…EX-3). Sending in plan or
// default mode is ordinary conversation input, never a recorded act. Codex
// keeps a requested mode on later turns until another mode is sent.
export function PlanModeControl({ planMode, requested, ready, busy, hasText, check, send }: {
  planMode: Json; requested: Json | null; ready: boolean; busy: boolean; hasText: boolean;
  check: () => void; send: (mode: "plan" | "default") => void;
}) {
  const state = planMode?.state ?? "not-checked";
  return <div aria-label="Plan mode">
    {state === "offered" ? <p>
      <button disabled={!ready || busy || !hasText} onClick={() => send("plan")}>Send in plan mode (experimental)</button>{" "}
      <button disabled={!ready || busy || !hasText} onClick={() => send("default")}>Send in default mode (carry out / leave plan mode)</button>
      {" "}Plan mode stays on until you leave it. Asking Codex to carry out a plan is ordinary input, not an approval.
    </p> : <p>
      Plan mode: {state === "not-checked" ? "not checked for this Codex connection" : `not offered — ${planMode?.reason ?? "reason not reported"}`}.{" "}
      {state === "not-checked" && <button disabled={!ready || busy} onClick={check}>Check plan mode availability</button>}
    </p>}
    {requested && <p>Last mode this App requested for this conversation: <b>{String(requested.mode)}</b> ({String(requested.standing)}).</p>}
  </div>;
}
