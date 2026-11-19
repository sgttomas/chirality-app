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
function accountReads(host: Json): Json[] {
  const mode = host?.homeRouting?.activeModeHomeClass, generation = host?.generation;
  return host?.homeAccess?.modeHomeClass === mode && Array.isArray(host?.homeAccess?.observations)
    ? host.homeAccess.observations.filter((row: Json) => row?.source?.attemptedFrame?.method === "account/read"
      && sameActivityGeneration(row.source.generation, generation) && row.source.home === generation.home) : [];
}
const latestAccountRead = (host: Json): Json => accountReads(host).at(-1);
const refOf = (row: Json): string | null => typeof row?.source?.requestRef === "string" && row.source.requestRef ? row.source.requestRef : null;
/** The latest account read of this connection, by its request reference; null before any, or where it has none. */
export const accountReadRef = (host: Json): string | null => refOf(latestAccountRead(host));
/** Every account read of this connection the status lists, by request reference. The host lists each read as it is
 * issued, in that order (runtime_session.rs read_native_home_access, account_view). */
export const accountReadRefs = (host: Json): string[] => accountReads(host).map(refOf).filter((ref): ref is string => ref !== null);
/** Codex's own message for the latest account read of this connection, where that read answered with an error. */
export function accountReadError(host: Json): string | null {
  if (accountReading(host) !== "failed") return null;
  const source = latestAccountRead(host)?.source;
  const message = source?.lastClientObservation?.error?.message ?? source?.response?.error?.message;
  return typeof message === "string" && message !== "" ? message : null;
}
/** The plan Codex reports for a current ChatGPT account reading, from the App's own list of plan types; else null. */
export function reportedPlan(host: Json): string | null {
  if (accountReading(host) !== "chatgpt-account") return null;
  const plan = host?.accountObservation?.nativeAccount?.planType;
  return PLAN_TYPES.includes(plan) && plan !== "unknown" ? plan : null;
}
const accountCheckpoint = (host: Json) => {
  const source = latestAccountRead(host)?.source;
  return JSON.stringify([source?.requestRef, source?.outcome, source?.authResponseShapeValid, host?.accountObservation?.state]);
};
/** What the App knows of this connection's sign-in, read from the account reads the host recorded for the
 * current Codex process and home. The host reads the account itself when Codex becomes ready, at launch and
 * after each start or restart (recorded as the App's read, not the person's); a read also follows the person's
 * own Check account status, a sign-in the person completed (the check below runs then without a press) and a
 * sign-out the person started (the host reads the account again). A read still waiting for Codex's answer is
 * "reading"; one Codex left unanswered past the host's wait is "pending". A reading from an earlier process or
 * home is never carried forward: latestAccountRead keeps only reads of the current generation.
 * One state decides both the account panel's sentence and the workspace's, so the two never disagree. */
export type AccountReading = "unread" | "reading" | "stale" | "failed" | "pending" | "unavailable" | "omitted" | "changed" | "no-account" | "chatgpt-account" | "api-key" | "unsupported";
/** The readings in which Codex did not say whether anyone is signed in: never taken for "not signed in". */
export const DIDNT_SAY: readonly AccountReading[] = ["stale", "failed", "pending", "unavailable", "omitted", "changed", "unsupported"];
export function accountReading(host: Json): AccountReading {
  if (!host?.generation) return "unread";
  const generation = host.generation, latest = latestAccountRead(host), source = latest?.source, observation = latest?.accountObservation;
  if (!latest) return "unread";
  if (source.sourceCurrent !== true) return "stale";
  if (source.outcome === "response-observed-error") return "failed";
  if (source.outcome !== "response-observed-result")
    return ["pending", "unknown/in-progress"].includes(source.outcome) && source.waitingEnded !== true ? "reading" : "pending";
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
  reading: "Checking with Codex whether you're signed in…",
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
/** The workspace line for each reading while Codex is running: the same fact as the panel's. Each outcome rests on
 * positive evidence only: signed in when Codex reported a ChatGPT account, not signed in when Codex reported no
 * account; an error, an unanswered or unreadable read, or one no longer current is "didn't say", never "not signed in".
 * "Not checked" is "hasn't established" here, since a check the panel holds as failed or in progress leaves no
 * host record yet and the workspace line must stay true then too.
 * These words are App Agent 0's decision and are kept here and nowhere else. */
const DIDNT_SAY_LINE = "Codex is running. It didn't say whether you're signed in.";
export const SIGN_IN_WORDS: Record<AccountReading, string> = {
  unread: "Codex is running. The App hasn't established whether you're signed in for this connection. Check or sign in under Connection and access, then choose a model and start a conversation.",
  reading: "Codex is running. Checking whether you're signed in. If a sign-in is kept, Codex checks it with OpenAI.",
  stale: DIDNT_SAY_LINE,
  failed: DIDNT_SAY_LINE,
  pending: DIDNT_SAY_LINE,
  unavailable: DIDNT_SAY_LINE,
  omitted: DIDNT_SAY_LINE,
  changed: DIDNT_SAY_LINE,
  "no-account": "Codex is running. You're not signed in.",
  "chatgpt-account": "Codex is running and you're signed in with your ChatGPT account.",
  "api-key": "Codex is running. Codex reports an API key for this connection, not a ChatGPT sign-in. Open Connection and access to see how this connection signs in.",
  unsupported: DIDNT_SAY_LINE,
};
/** Where Codex reports the plan of a ChatGPT account, the line names it. */
export const planWords = (plan: string | null) => plan ? ` Plan: ${plan}.` : "";
/** A sign-in Codex completed for the current process and home, as a key that names that completion once; else null.
 * The App moves to a new conversation once per such completion, after the read confirms an account. */
export function signInCompletion(host: Json): string | null {
  const generation = host?.generation, oauth = host?.homeOAuth, source = oauth?.source;
  if (host?.state !== "ready" || host?.generationClosed || host?.homeRouting?.activeModeHomeClass !== "account" || oauth?.state !== "source-observed"
    || !sameActivityGeneration(source?.generation, generation)) return null;
  const identity = source?.requestIdentity;
  return source.phase === "CompletedSuccess" && source.actualWriteObserved === true
    && typeof source.observationRef === "string" && !!source.observationRef
    && ((typeof identity === "string" && !!identity) || (typeof identity === "number" && Number.isSafeInteger(identity)))
    ? JSON.stringify([generation, source.observationRef, identity]) : null;
}
/** What Codex reports of the sign-in started for the current process and home, where the host observed one: the one
 * reading behind the sign-in line of the account panel and of the account popover. A sign-in of an earlier process
 * or of another home is "none". */
export type SignInPhase = "none" | "cancel-not-found" | "canceled" | "completed" | "failed" | "pending" | "unresolved";
/** The phases the host reports for a sign-in that has ended (hosting.rs oauth_terminal, account_oauth_observation). Any
 * other phase it reports is a sign-in not yet ended, beside which the host refuses to start another. */
const ENDED_PHASES = ["CompletedSuccess", "CompletedFailure", "Cancelled", "StartRejected"];
/** The phases of a sign-in waiting for Codex or for the person (oauth_control.rs Phase). */
const WAITING_PHASES = ["AwaitingWrite", "AwaitingReply", "Pending"];
const observedSignIn = (host: Json): Json => {
  const generation = host?.generation, oauth = host?.homeOAuth, source = oauth?.source;
  return host?.state === "ready" && !host?.generationClosed && host?.homeRouting?.activeModeHomeClass === "account"
    && oauth?.state === "source-observed" && sameActivityGeneration(source?.generation, generation) ? source : null;
};
export function signInPhase(host: Json): SignInPhase {
  const source = observedSignIn(host);
  if (!source) return "none";
  return source.cancelStatus === "notFound" ? "cancel-not-found" : source.cancelStatus === "canceled" ? "canceled"
    : source.phase === "CompletedSuccess" ? "completed" : ["CompletedFailure", "StartRejected"].includes(source.phase) ? "failed"
    : WAITING_PHASES.includes(source.phase) ? "pending" : source.phase === "Cancelled" ? "none" : "unresolved";
}
/** The host reports a sign-in for the current process and home in a phase that has not ended (waiting, cancelling,
 * or one whose end the host could not establish): no other sign-in is offered or sent beside it. */
export function signInUnresolved(host: Json): boolean {
  const source = observedSignIn(host);
  return !!source && !ENDED_PHASES.includes(source.phase);
}
/** The App's sentence for each sign-in phase. */
export const SIGN_IN_PHASE_WORDS: Record<SignInPhase, string> = {
  none: "",
  "cancel-not-found": "Codex had no pending sign-in to cancel. Account status is separate.",
  canceled: "The pending sign-in was canceled. Account status is separate.",
  completed: "Sign-in completed.",
  failed: "Sign-in did not complete. Private details are withheld.",
  pending: "Waiting for sign-in to complete.",
  unresolved: "An earlier sign-in has not ended. Another can start once it has ended or been canceled.",
};
/** A sign-in Codex reports pending for the current process and home. */
export const signInPending = (host: Json): boolean => signInPhase(host) === "pending";
/** The App's words for a sign-in Codex reports completed while no account read made after it has answered: the
 * account is being checked, or has not been read since. The row, its popover and the line above the conversation all
 * say these, and none of them says the earlier reading. */
export const SIGN_IN_COMPLETED: Record<"checking" | "unread", { detail: string; sentence: string }> = {
  checking: { detail: "Checking the account…", sentence: "Codex reports the sign-in completed. Checking the account with Codex…" },
  unread: { detail: "Account not read yet", sentence: "Codex reports the sign-in completed. The account has not been read since." },
};
/** The account panel's sentence for the current reading: for a ChatGPT account, the account as Codex reports it. */
export function accountSummary(host: Json): string {
  const reading = accountReading(host);
  return reading === "chatgpt-account" ? `Codex reports a ChatGPT account for this connection: ${reportedChatgptAccount(host?.accountObservation)}.` : ACCOUNT_PANEL_WORDS[reading];
}

/** The account panel. `auto` (default true): it reads the account itself when it sees a completed sign-in; the App
 * passes false, since its account controller makes that read (AccountControls.tsx useAccountController). `awaiting`:
 * the controller holds a completed sign-in that no account read made after it has answered, and the earlier reading
 * is not said. */
export function AccountStatus({ host, navigating, busy, read, auto = true, awaiting = false }: { host: Json; navigating: boolean; busy: boolean; read: ReadAccountStatus; auto?: boolean; awaiting?: boolean }) {
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
    if (!auto || !completion || busy || pending.current || context.current.epoch !== epoch || checkedCompletions.current.has(completion)) return;
    checkedCompletions.current.add(completion);
    void check();
  }, [auto, completion, busy, readEpoch]); // eslint-disable-line react-hooks/exhaustive-deps
  const signIn = ready ? SIGN_IN_PHASE_WORDS[signInPhase(host)] : "";
  return <div aria-label="Account status">
    <h3>Account status</h3>
    {signIn && <p>{signIn}</p>}
    <p role="status">{!ready ? "Account status is unavailable while this connection is changing or stopped."
      : readEpoch === epoch ? "Checking account status…" : failure?.epoch === epoch && failure.checkpoint === accountCheckpoint(host) ? failure.message : awaiting ? SIGN_IN_COMPLETED.unread.sentence : accountSummary(host)}</p>
    <button disabled={!ready || busy || readEpoch !== null} onClick={check}>Check account status</button>
    <p>This check does not sign you in again. The email and plan are what Codex reports; the App does not verify identity or that the sign-in is still valid.</p>
  </div>;
}
