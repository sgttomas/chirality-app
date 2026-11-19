import { useCallback, useEffect, useId, useRef, useState } from "react";
import { DIDNT_SAY, accountReadError, accountReading, accountSummary, reportedPlan, signInCompletion, signInPending } from "./AccountStatus";
import { connectionWords, signInSentence, type ConnectionFacts } from "./DailyWorkspace";
import { AgentText } from "./AgentText";

type Json = any; // eslint-disable-line @typescript-eslint/no-explicit-any

/** What the account row's popover can do: each is the App's present command or reveal, under its present conditions. */
export type AccountActions = {
  /** Selects Settings & tools, as the row did before it had a popover. */
  openSettings: () => void;
  /** Reveals Connection and access in Settings & tools. */
  openConnection: () => void;
  /** Reads the account again: the workspace line's Check again. */
  checkAgain: () => Promise<void>;
  /** oauth_start with mode "browser": the sign-in Connection and access starts. */
  startSignIn: () => Promise<void>;
  /** logout_home for the account home: Connection and access's Sign out of ChatGPT. */
  signOut: () => Promise<void>;
};

/** The connection facts of the host status, read as the App reads them for the workspace line. */
export const connectionFacts = (host: Json): ConnectionFacts => ({
  state: host?.state, setupRequired: host?.desktopSetup?.launch?.state === "setup-required", savedSetup: !!host?.desktopSetup?.pending,
  generationClosed: host?.generationClosed, startRefusal: host?.lastStartRefusal, codexHome: host?.codexHome,
  refusalCause: host?.startRefusalCause, build: host?.build,
});

/** The row's words: the state in a few of the App's words, a small line under it where one says more, and whether
 * the avatar takes its signed-in form. While Codex is not ready, the state is the workspace line's own title for the
 * connection. While it is ready, each rests on the sign-in reading alone (accountReading): signed in only where Codex
 * reported a ChatGPT account, not signed in only where it reported none; a reading in which Codex didn't say is never
 * "Not signed in". The email is never here. */
export function accountRowWords(host: Json): { state: string; detail: string | null; signedIn: boolean } {
  const connection = connectionWords(connectionFacts(host));
  if (connection) return { state: connection.title, detail: null, signedIn: false };
  const reading = accountReading(host);
  if (reading === "chatgpt-account") {
    const plan = reportedPlan(host);
    return { state: "Signed in", detail: plan ? `Plan: ${plan}` : "ChatGPT account", signedIn: true };
  }
  if (reading === "no-account") return { state: "Not signed in", detail: "Sign in to start", signedIn: false };
  if (reading === "reading") return { state: "Checking sign-in…", detail: null, signedIn: false };
  if (reading === "unread") return { state: "Sign-in not checked", detail: null, signedIn: false };
  if (reading === "api-key") return { state: "API key connection", detail: "Not a ChatGPT sign-in", signedIn: false };
  return { state: "Sign-in unknown", detail: "Codex didn't say", signedIn: false };
}

/** The one action the popover offers for the state: none while Codex is not ready, while the account is being read,
 * or for an API key connection. */
export function accountAction(host: Json): "sign-in" | "check-again" | "sign-out" | null {
  if (connectionWords(connectionFacts(host))) return null;
  const reading = accountReading(host);
  return reading === "no-account" ? "sign-in" : reading === "chatgpt-account" ? "sign-out"
    : reading === "unread" || DIDNT_SAY.includes(reading) ? "check-again" : null;
}

function AccountPopover({ host, actions, close }: { host: Json; actions: AccountActions; close: () => void }) {
  const mounted = useRef(true);
  useEffect(() => { mounted.current = true; return () => { mounted.current = false; }; }, []);
  const [acting, setActing] = useState(false);
  const act = async (action: () => Promise<void>) => {
    if (acting) return;
    setActing(true);
    try { await action(); } catch { /* the App line says what happened */ } finally { if (mounted.current) setActing(false); }
  };
  const words = accountRowWords(host), connection = connectionWords(connectionFacts(host));
  const reading = accountReading(host), action = accountAction(host);
  const generation = host?.generation, accountHome = host?.homeRouting?.activeModeHomeClass === "account";
  const codexError = !connection && DIDNT_SAY.includes(reading) ? accountReadError(host) : null;
  return <>
    <section className="account-controls-group" aria-label="Account">
      <strong>{words.state}</strong>
      <p>{connection ? connection.guidance : signInSentence(reading, reportedPlan(host))}</p>
      {!connection && reading === "chatgpt-account" ? <p>{accountSummary(host)}</p> : null}
      {codexError ? <p aria-label="What Codex said"><AgentText value={codexError} source="codex"/></p> : null}
      {signInPending(host) ? <p>Waiting for sign-in to complete.</p> : null}
      {action === "sign-in" ? <button type="button" className="setup-primary" disabled={acting || !accountHome || !generation} onClick={() => { void act(actions.startSignIn); }}>Sign in with your ChatGPT account (through Codex)…</button> : null}
      {action === "check-again" ? <button type="button" disabled={acting} onClick={() => { void act(actions.checkAgain); }}>Check again</button> : null}
      {action === "sign-out" ? <button type="button" disabled={acting || !generation || !accountHome} onClick={() => { void act(actions.signOut); }}>Sign out of ChatGPT…</button> : null}
    </section>
    <section className="account-controls-group" aria-label="App controls">
      <button type="button" className="account-controls-menu-action" onClick={() => { close(); actions.openConnection(); }}>Connection and access…</button>
      <button type="button" className="account-controls-menu-action" onClick={() => { close(); actions.openSettings(); }}>Settings &amp; tools…</button>
    </section>
  </>;
}

/**
 * The account row at the foot of the navigator, and in its collapsed strip as the avatar alone: the sign-in state, and
 * a popover with that state, its one action and the App's controls. The popover opens beside the row within the
 * window, above it when there is more room above, and takes focus; Escape closes it and returns focus to the row, as
 * does a press outside it or focus leaving it, and a sign-in that completes while it is open. Nothing is stored.
 */
export function AccountRow({ host, actions }: { host: Json; actions: AccountActions }) {
  const [open, setOpen] = useState(false);
  const root = useRef<HTMLDivElement>(null), trigger = useRef<HTMLButtonElement>(null), panel = useRef<HTMLDivElement>(null);
  const id = useId();
  const words = accountRowWords(host);
  const position = useCallback(() => {
    const button = trigger.current, box = panel.current;
    if (!button || !box || typeof button.getBoundingClientRect !== "function" || typeof window.innerHeight !== "number") return;
    const rect = button.getBoundingClientRect();
    const width = Math.min(300, window.innerWidth - 24);
    const above = rect.top - 16, below = window.innerHeight - rect.bottom - 16, up = above >= below;
    Object.assign(box.style, { width: `${width}px`, left: `${Math.max(12, Math.min(rect.left, window.innerWidth - width - 12))}px`,
      top: up ? "auto" : `${rect.bottom + 8}px`, bottom: up ? `${window.innerHeight - rect.top + 8}px` : "auto",
      maxHeight: `${Math.max(100, up ? above : below)}px` });
  }, []);
  const dismiss = useCallback(() => { setOpen(false); trigger.current?.focus?.(); }, []);
  useEffect(() => {
    if (!open || typeof document === "undefined") return;
    position();
    panel.current?.focus?.();
    const outside = (event: Event) => { const target = event.target as Node | null; if (target && !root.current?.contains(target)) setOpen(false); };
    const key = (event: KeyboardEvent) => { if (event.key === "Escape") { event.preventDefault?.(); dismiss(); } };
    document.addEventListener("pointerdown", outside);
    document.addEventListener("keydown", key);
    window.addEventListener("resize", position);
    window.addEventListener("scroll", position, true);
    return () => {
      document.removeEventListener("pointerdown", outside); document.removeEventListener("keydown", key);
      window.removeEventListener("resize", position); window.removeEventListener("scroll", position, true);
    };
  }, [open, position, dismiss]);
  // A sign-in that completes while the popover is open closes it: the row now says the state. A completion already
  // seen when it opened does not.
  const completion = signInCompletion(host);
  const seenCompletion = useRef(completion);
  useEffect(() => {
    const before = seenCompletion.current;
    seenCompletion.current = completion;
    if (completion && completion !== before) setOpen(false);
  }, [completion]);
  return <div ref={root} className="account-controls-root" onBlur={event => {
    const next = event.relatedTarget as Node | null;
    if (next && !event.currentTarget.contains(next)) setOpen(false);
  }}>
    <button ref={trigger} type="button" className="account-controls-row" aria-label={`Account and settings, ${words.state}`} aria-expanded={open} aria-controls={id} aria-haspopup="dialog" onClick={() => setOpen(!open)}>
      <span className={words.signedIn ? "account-controls-avatar account-controls-avatar-signed-in" : "account-controls-avatar"} data-signed-in={words.signedIn ? "true" : "false"} aria-hidden="true">
        <svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" focusable="false"><circle cx="12" cy="8.5" r="3.5"/><path d="M4.5 20c.9-3.6 3.8-5.5 7.5-5.5s6.6 1.9 7.5 5.5"/></svg>
      </span>
      <span className="account-controls-identity"><strong>{words.state}</strong>{words.detail ? <small>{words.detail}</small> : null}</span>
      <span aria-hidden="true">⌃</span>
    </button>
    {open ? <div ref={panel} id={id} role="dialog" aria-label="Account and settings" tabIndex={-1} className="account-controls-popover">
      <AccountPopover host={host} actions={actions} close={dismiss}/>
    </div> : null}
  </div>;
}
