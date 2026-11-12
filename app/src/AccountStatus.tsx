import { useEffect, useRef, useState } from "react";
import { sameActivityGeneration } from "./NativeActivity";

type Json = any; // eslint-disable-line @typescript-eslint/no-explicit-any
export type ReadAccountStatus = (generation: Json, modeHomeClass: string, isCurrent: () => boolean) => Promise<void>;

// Read only the existing redacted, source-owned projection. Of the account
// Codex reports, only the email and plan type are shown (DEL-01-05 REQ-001);
// no other response string, native detail or diagnostic is summarized.
const PLAN_TYPES = ["free", "go", "plus", "pro", "prolite", "promax", "team", "self_serve_business_prolite", "self_serve_business_usage_based", "business", "ent26",
  "enterprise_cbp_automation", "enterprise_cbp_usage_based", "enterprise", "edu", "edu_plus", "edu_pro", "sci", "sci_plus", "unknown"];
/** The ChatGPT account as Codex reports it for this home: the email, or that none was reported, and the plan type. */
export function reportedChatgptAccount(current: Json): string {
  const who = typeof current?.codexAccount === "string" && current.codexAccount !== "" && current.codexAccount.length <= 254 && !/[\u0000-\u001f\u007f]/.test(current.codexAccount)
    ? current.codexAccount : "ChatGPT account (no email reported)";
  const plan = PLAN_TYPES.includes(current?.nativeAccount?.planType) && current.nativeAccount.planType !== "unknown" ? current.nativeAccount.planType : null;
  return `${who} · plan ${plan ?? "not reported"}`;
}
function latestAccountRead(host: Json): Json {
  const mode = host?.homeRouting?.activeModeHomeClass, generation = host?.generation;
  const rows = host?.homeAccess?.modeHomeClass === mode && Array.isArray(host?.homeAccess?.observations)
    ? host.homeAccess.observations.filter((row: Json) => row?.source?.attemptedFrame?.method === "account/read"
      && sameActivityGeneration(row.source.generation, generation) && row.source.home === generation.home) : [];
  return rows.at(-1);
}
const accountCheckpoint = (host: Json) => {
  const source = latestAccountRead(host)?.source;
  return JSON.stringify([source?.requestRef, source?.outcome, source?.authResponseShapeValid, host?.accountObservation?.state]);
};
function accountSummary(host: Json): string {
  const generation = host.generation, latest = latestAccountRead(host), source = latest?.source, observation = latest?.accountObservation;
  if (!latest) return "Account status has not been checked for this connection.";
  if (source.sourceCurrent !== true) return "The earlier account check is no longer current. Check account status again.";
  if (source.outcome === "response-observed-error") return "Codex could not read account status. Check again when ready.";
  if (source.outcome !== "response-observed-result") return "The account read has not produced a result. Account status is unknown.";
  if (source.authResponseShapeValid !== true) return "Codex returned an unavailable account response. Account status is unknown.";
  if (observation?.state === "account omitted; unknown/unavailable") return "Codex did not report account status. This does not mean you are signed out.";
  const current = host?.accountObservation;
  if (!sameActivityGeneration(current?.generation, generation) || current?.home !== generation.home || current?.state !== "observed") {
    return "Account status changed or is no longer confirmed for this connection. Check account status again.";
  }
  if (observation?.state === "native account null observed" && observation.account === null && current.nativeAccount === null) {
    return "Codex reports no account for this connection.";
  }
  if (observation?.state === "native account type observed" && observation.account?.type === current.nativeAccount?.type) {
    if (observation.account.type === "chatgpt") return `Codex reports a ChatGPT account for this connection: ${reportedChatgptAccount(current)}.`;
    if (observation.account.type === "apiKey") return "Codex reports an API key for this connection.";
  }
  return "Codex did not provide a supported account status. Account status is unknown.";
}

export function AccountStatus({ host, navigating, busy, read }: { host: Json; navigating: boolean; busy: boolean; read: ReadAccountStatus }) {
  const generation = host?.generation, mode = host?.homeRouting?.activeModeHomeClass;
  const ready = host?.state === "ready" && !host?.generationClosed && sameActivityGeneration(generation, generation)
    && ["account", "api-key"].includes(mode) && !navigating;
  const scope = JSON.stringify([generation, mode, host?.state, host?.generationClosed, navigating]);
  const context = useRef({ scope, epoch: 0 });
  if (context.current.scope !== scope) context.current = { scope, epoch: context.current.epoch + 1 };
  const epoch = context.current.epoch;
  const mounted = useRef(true), pending = useRef(false), checkedCompletions = useRef(new Set<string>());
  const [readEpoch, setReadEpoch] = useState<number | null>(null);
  const [failure, setFailure] = useState<{ epoch: number; checkpoint: string; message: string } | null>(null);
  useEffect(() => { mounted.current = true; return () => { mounted.current = false; }; }, []);
  const check = async () => {
    const current = () => mounted.current && context.current.epoch === epoch;
    if (!ready || busy || pending.current || !current()) return;
    pending.current = true; setReadEpoch(epoch); setFailure(null);
    try { await read(generation, mode, current); }
    catch { if (current()) setFailure({ epoch, checkpoint: accountCheckpoint(host), message: "Account status could not be confirmed. Try checking again; this does not mean you are signed out." }); }
    finally { pending.current = false; if (mounted.current) setReadEpoch(null); }
  };
  const oauth = host?.homeOAuth, source = oauth?.source;
  const matching = ready && mode === "account" && oauth?.state === "source-observed"
    && sameActivityGeneration(source?.generation, generation);
  const identity = source?.requestIdentity;
  const completed = matching && source.phase === "CompletedSuccess" && source.actualWriteObserved === true
    && typeof source.observationRef === "string" && !!source.observationRef
    && ((typeof identity === "string" && !!identity) || (typeof identity === "number" && Number.isSafeInteger(identity)));
  const completion = completed ? JSON.stringify([generation, source.observationRef, identity]) : null;
  useEffect(() => {
    if (!completion || busy || pending.current || context.current.epoch !== epoch || checkedCompletions.current.has(completion)) return;
    checkedCompletions.current.add(completion);
    void check();
  }, [completion, busy, readEpoch]);
  const signIn = !matching ? "" : source.cancelStatus === "notFound" ? "Codex had no pending sign-in to cancel. Account status is separate."
    : source.cancelStatus === "canceled" ? "The pending sign-in was canceled. Account status is separate."
    : source.phase === "CompletedSuccess" ? "Sign-in completed. Account status is checked separately below."
    : ["CompletedFailure", "StartRejected"].includes(source.phase) ? "Sign-in did not complete. Private details are withheld."
    : source.phase === "Pending" ? "Waiting for sign-in to complete." : "";
  return <div aria-label="Account status">
    <h3>Account status</h3>
    {signIn && <p>{signIn}</p>}
    <p role="status">{!ready ? "Account status is unavailable while this connection is changing or stopped."
      : readEpoch === epoch ? "Checking account status…" : failure?.epoch === epoch && failure.checkpoint === accountCheckpoint(host) ? failure.message : accountSummary(host)}</p>
    <button disabled={!ready || busy || readEpoch !== null} onClick={check}>Check account status</button>
    <p>This check does not sign you in again. The email and plan are what Codex reports; the App does not verify identity or that the sign-in is still valid.</p>
  </div>;
}
