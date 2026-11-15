import { useEffect, useRef, useState } from "react";
import { sameActivityGeneration } from "./NativeActivity";
import { readingSentence } from "./readingSentences";

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
/** What the App knows of this connection's sign-in, read from the account reads the host recorded for the
 * current Codex process and home. The App makes no automatic account read at launch; a read follows the
 * person's own Check account status, a sign-in the person completed (the check below runs then without a
 * press) and a sign-out the person started (the host reads the account again). A reading from an earlier
 * process or home is never carried forward: latestAccountRead keeps only reads of the current generation.
 * One state decides both the account panel's sentence and the workspace's, so the two never disagree. */
export type AccountReading = "unread" | "stale" | "failed" | "pending" | "unavailable" | "omitted" | "changed" | "no-account" | "chatgpt-account" | "api-key" | "unsupported";
export function accountReading(host: Json): AccountReading {
  if (!host?.generation) return "unread";
  const generation = host.generation, latest = latestAccountRead(host), source = latest?.source, observation = latest?.accountObservation;
  if (!latest) return "unread";
  if (source.sourceCurrent !== true) return "stale";
  if (source.outcome === "response-observed-error") return "failed";
  if (source.outcome !== "response-observed-result") return "pending";
  if (source.authResponseShapeValid !== true) return "unavailable";
  if (observation?.state === "account omitted; unknown/unavailable") return "omitted";
  const current = host?.accountObservation;
  if (!sameActivityGeneration(current?.generation, generation) || current?.home !== generation.home || current?.state !== "observed") return "changed";
  if (observation?.state === "native account null observed" && observation.account === null && current.nativeAccount === null) return "no-account";
  if (observation?.state === "native account type observed" && observation.account?.type === current.nativeAccount?.type) {
    if (observation.account.type === "chatgpt") return "chatgpt-account";
    if (observation.account.type === "apiKey") return "api-key";
  }
  return "unsupported";
}
/** The account panel's sentence for each reading. */
export const ACCOUNT_PANEL_WORDS: Record<Exclude<AccountReading, "chatgpt-account">, string> = {
  unread: "Account status has not been checked for this connection.",
  stale: "The earlier account check is no longer current. Check account status again.",
  failed: "Codex could not read account status. Check again when ready.",
  pending: "The account read has not produced a result. Account status is unknown.",
  unavailable: "Codex returned an unavailable account response. Account status is unknown.",
  omitted: "Codex did not report account status. This does not mean you are signed out.",
  changed: "Account status changed or is no longer confirmed for this connection. Check account status again.",
  "no-account": "Codex reports no account for this connection.",
  "api-key": "Codex reports an API key for this connection.",
  unsupported: "Codex did not provide a supported account status. Account status is unknown.",
};
/** The workspace's sentence for each reading while Codex is running: the same fact as the panel's, with where to act.
 * "Not checked" is "hasn't established" here, since a check the panel holds as failed or in progress leaves no
 * host record yet and the workspace line must stay true then too. */
export const SIGN_IN_WORDS: Record<AccountReading, string> = {
  unread: "The App hasn't established whether you're signed in for this connection. Check or sign in under Connection and access, then choose a model and start a conversation.",
  stale: "The App's earlier sign-in check is no longer current, so whether you're signed in is unknown. Check again under Connection and access.",
  failed: "Codex could not read whether you're signed in. Check again under Connection and access.",
  pending: "The App's sign-in check has not produced a result, so whether you're signed in is unknown.",
  unavailable: "Codex returned an unavailable account response, so whether you're signed in is unknown. Check again under Connection and access.",
  omitted: "Codex did not report whether you're signed in; this does not mean you are signed out. Check again under Connection and access.",
  changed: "Whether you're signed in changed or is no longer confirmed for this connection. Check again under Connection and access.",
  "no-account": "Codex reports that you're not signed in. Sign in under Connection and access to choose a model.",
  "chatgpt-account": "Choose a conversation, or choose a model for a new one.",
  "api-key": "Codex reports an API key for this connection, not a ChatGPT sign-in. Open Connection and access to see how this connection signs in.",
  unsupported: "Codex did not report a sign-in the App reads, so whether you're signed in is unknown. Check again under Connection and access.",
};
function accountSummary(host: Json): string {
  const reading = accountReading(host);
  return reading === "chatgpt-account" ? `Codex reports a ChatGPT account for this connection: ${reportedChatgptAccount(host?.accountObservation)}.` : ACCOUNT_PANEL_WORDS[reading];
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
    catch (error) { if (current()) setFailure({ epoch, checkpoint: accountCheckpoint(host), message: readingSentence(error) ?? "Account status could not be confirmed. Try checking again; this does not mean you are signed out." }); }
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
