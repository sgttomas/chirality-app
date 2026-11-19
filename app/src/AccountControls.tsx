import { useCallback, useEffect, useId, useRef, useState } from "react";
import { ACCOUNT_PANEL_WORDS, DIDNT_SAY, SIGN_IN_PHASE_WORDS, accountReadError, accountReadRef, accountReading, accountSummary, reportedPlan, signInCompletion, signInPending, signInPhase } from "./AccountStatus";
import { connectionWords, signInSentence, type ConnectionFacts } from "./DailyWorkspace";
import { AgentText } from "./AgentText";
import { readingSentence } from "./readingSentences";

type Json = any; // eslint-disable-line @typescript-eslint/no-explicit-any

/** The account action a state offers. */
export type AccountActionName = "sign-in" | "check-again" | "sign-out";
/** The App's present commands for the account, each for the Codex process and home it is given. Each rejects where
 * its command was refused or failed, having said so on the App line. */
export type AccountCommands = {
  /** Reads the account again: the workspace line's Check again. */
  checkAgain: (generation: Json, modeHomeClass: string) => Promise<void>;
  /** oauth_start with mode "browser": the sign-in Connection and access starts. */
  startSignIn: (generation: Json) => Promise<void>;
  /** logout_home for the account home: Connection and access's Sign out of ChatGPT. */
  signOut: (generation: Json, modeHomeClass: string) => Promise<void>;
};
/** The account's actions as every surface that offers them shares them (useAccountController). */
export type AccountController = {
  /** One of the actions is under way, from whichever surface it was pressed. */
  acting: boolean;
  /** What the App says of the last action that was not sent or did not go through, while the account still stands as
   * it did then; else null. */
  feedback: string | null;
  /** Codex reported a sign-in completed and no account read made after it has answered yet. */
  awaiting: boolean;
  /** The completed sign-in the account read after it confirmed, by the completion's own identity; else null. */
  confirmed: string | null;
  /** Sends the action for the status `shown` when it was pressed, and only if that status's Codex process and home are
   * still the current ones and the action is still the one the account's state offers. Otherwise nothing is sent. */
  act: (action: AccountActionName, shown: Json) => Promise<void>;
};
/** The App's reveals the popover offers. */
export type AccountReveals = {
  /** Selects Settings & tools. */
  openSettings: () => void;
  /** Reveals Connection and access in Settings & tools. */
  openConnection: () => void;
};

/** The connection facts of the host status, read as the App reads them for the workspace line. */
export const connectionFacts = (host: Json): ConnectionFacts => ({
  state: host?.state, setupRequired: host?.desktopSetup?.launch?.state === "setup-required", savedSetup: !!host?.desktopSetup?.pending,
  generationClosed: host?.generationClosed, startRefusal: host?.lastStartRefusal, codexHome: host?.codexHome,
  refusalCause: host?.startRefusalCause, build: host?.build,
});

/** The row's words: the state in a few of the App's words, a small line under it where one says more, and whether
 * the avatar takes its signed-in form. While Codex is not ready, or setup is needed, the state is the workspace
 * line's own title for the connection. While it is ready, each rests on the sign-in reading alone (accountReading):
 * signed in only where Codex reported a ChatGPT account, not signed in only where it reported none; a reading in
 * which Codex didn't say is never "Not signed in". `awaiting` (the controller's) is a sign-in Codex reported
 * completed with no account read answered since: the earlier reading is not said then. The email is never here. */
export function accountRowWords(host: Json, awaiting = false): { state: string; detail: string | null; signedIn: boolean } {
  const connection = connectionWords(connectionFacts(host));
  if (connection) return { state: connection.title, detail: null, signedIn: false };
  const reading = accountReading(host);
  if (awaiting) return { state: "Sign-in completed", detail: reading === "reading" ? "Checking the account…" : "Account not read yet", signedIn: false };
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

/** The one action the popover offers for the state, where it offers one: none while Codex is not ready, while the
 * account is being read, or for an API key connection. After a completed sign-in the account is read, never signed
 * in to again, until a read answers. */
export function accountAction(host: Json, awaiting = false): AccountActionName | null {
  if (connectionWords(connectionFacts(host))) return null;
  const reading = accountReading(host);
  if (awaiting) return reading === "reading" ? null : "check-again";
  return reading === "no-account" ? "sign-in" : reading === "chatgpt-account" ? "sign-out"
    : reading === "unread" || DIDNT_SAY.includes(reading) ? "check-again" : null;
}

/** The popover's sentence under the state. Where Codex didn't say, it is the account panel's own sentence for the
 * reading, so a read that failed, one left unanswered and the rest stay distinct. */
function accountSentence(host: Json, awaiting: boolean): string {
  const connection = connectionWords(connectionFacts(host));
  if (connection) return connection.guidance;
  const reading = accountReading(host);
  if (awaiting) return reading === "reading" ? "Codex reports the sign-in completed. Checking the account with Codex…"
    : "Codex reports the sign-in completed. The account has not been read since.";
  if (reading !== "chatgpt-account" && DIDNT_SAY.includes(reading)) return ACCOUNT_PANEL_WORDS[reading as Exclude<typeof reading, "chatgpt-account">];
  return signInSentence(reading, reportedPlan(host));
}

const sourceKey = (host: Json) => JSON.stringify([host?.generation ?? null, host?.homeRouting?.activeModeHomeClass ?? null]);
const NOT_SENT = "The connection or the account changed before this was sent. Nothing was sent.";
const FAILED: Record<AccountActionName, string> = {
  "sign-in": "The App could not confirm that a sign-in started.",
  "check-again": "Account status could not be confirmed. Try checking again; this does not mean you are signed out.",
  "sign-out": "The App could not confirm the sign-out. Check again to see the account.",
};

/**
 * The account's actions for every surface that offers them (the account row in the navigator and in its collapsed
 * strip, and the workspace line): one action at a time across all of them, each bound to the status shown when it was
 * pressed, and one reading of a completed sign-in that the account read has not yet confirmed. `latest` gives the
 * App's current host status at the moment of sending. Nothing is stored.
 */
export function useAccountController(host: Json, latest: () => Json, commands: AccountCommands): AccountController {
  const mounted = useRef(true);
  useEffect(() => { mounted.current = true; return () => { mounted.current = false; }; }, []);
  const inFlight = useRef(false);
  const [acting, setActing] = useState(false);
  const [feedback, setFeedback] = useState<{ checkpoint: string; words: string } | null>(null);
  // Each completed sign-in, by its own identity, with the account read that was the latest before it was first seen.
  // One already present the first time a Codex process is seen was not watched completing, and is never awaited.
  const completions = useRef(new Map<string, { before: string | null; settled: boolean; watched: boolean }>());
  const generations = useRef(new Map<string, string | null>());
  const generationKey = host?.generation ? JSON.stringify(host.generation) : null;
  const completion = signInCompletion(host), readRef = accountReadRef(host), reading = accountReading(host);
  if (completion && !completions.current.has(completion)) {
    const watched = !!generationKey && generations.current.has(generationKey);
    completions.current.set(completion, { before: watched ? generations.current.get(generationKey!) ?? null : readRef, settled: !watched, watched });
  }
  if (generationKey) generations.current.set(generationKey, readRef);
  const entry = completion ? completions.current.get(completion) : undefined;
  if (entry && !entry.settled && readRef !== entry.before && reading !== "reading") entry.settled = true;
  const awaitingOf = (status: Json) => {
    const key = signInCompletion(status), known = key ? completions.current.get(key) : undefined;
    return !!known && !known.settled;
  };
  const awaiting = !!entry && !entry.settled;
  const confirmed = completion && entry?.watched && entry.settled && reading === "chatgpt-account" ? completion : null;
  const checkpoint = (status: Json) => JSON.stringify([sourceKey(status), accountReading(status), signInPhase(status), awaitingOf(status)]);
  const act = async (action: AccountActionName, shown: Json) => {
    if (inFlight.current) return;
    const now = latest(), generation = now?.generation, mode = now?.homeRouting?.activeModeHomeClass;
    const eligible = sourceKey(now) === sourceKey(shown) && !!generation && typeof mode === "string"
      && accountAction(now, awaitingOf(now)) === action && (action === "check-again" || mode === "account")
      && !(action === "sign-in" && signInPending(now));
    if (!eligible) { setFeedback({ checkpoint: checkpoint(now), words: NOT_SENT }); return; }
    inFlight.current = true; setActing(true); setFeedback(null);
    try {
      if (action === "sign-in") await commands.startSignIn(generation);
      else if (action === "sign-out") await commands.signOut(generation, mode);
      else await commands.checkAgain(generation, mode);
    } catch (error) {
      if (mounted.current) setFeedback({ checkpoint: checkpoint(latest()), words: (action === "check-again" ? readingSentence(error) : null) ?? FAILED[action] });
    } finally { inFlight.current = false; if (mounted.current) setActing(false); }
  };
  return { acting, feedback: feedback && feedback.checkpoint === checkpoint(host) ? feedback.words : null, awaiting, confirmed, act };
}

function AccountPopover({ host, account, reveals, close }: { host: Json; account: AccountController; reveals: AccountReveals; close: () => void }) {
  const words = accountRowWords(host, account.awaiting), connection = connectionWords(connectionFacts(host));
  const reading = accountReading(host), action = accountAction(host, account.awaiting);
  const generation = host?.generation, accountHome = host?.homeRouting?.activeModeHomeClass === "account";
  const codexError = !connection && !account.awaiting && DIDNT_SAY.includes(reading) ? accountReadError(host) : null;
  // The sign-in line: the account panel's own words for a sign-in that is waiting, did not complete or was canceled.
  // A completed one is said by the state above.
  const phase = signInPhase(host);
  const phaseWords = !connection && !words.signedIn && phase !== "completed" ? SIGN_IN_PHASE_WORDS[phase] : "";
  const busy = account.acting;
  return <>
    <section className="account-controls-group" aria-label="Account">
      <strong>{words.state}</strong>
      <p>{accountSentence(host, account.awaiting)}</p>
      {!connection && !account.awaiting && reading === "chatgpt-account" ? <p>{accountSummary(host)}</p> : null}
      {codexError ? <p aria-label="What Codex said"><AgentText value={codexError} source="codex"/></p> : null}
      {phaseWords ? <p>{phaseWords}</p> : null}
      {action === "sign-in" ? <button type="button" className="setup-primary" disabled={busy || !accountHome || !generation || phase === "pending"} onClick={() => { void account.act("sign-in", host); }}>Sign in with your ChatGPT account (through Codex)…</button> : null}
      {action === "check-again" ? <button type="button" disabled={busy} onClick={() => { void account.act("check-again", host); }}>Check again</button> : null}
      {action === "sign-out" ? <button type="button" disabled={busy || !generation || !accountHome} onClick={() => { void account.act("sign-out", host); }}>Sign out of ChatGPT…</button> : null}
      {account.feedback ? <p role="status">{account.feedback}</p> : null}
    </section>
    <section className="account-controls-group" aria-label="App controls">
      <button type="button" className="account-controls-menu-action" onClick={() => { close(); reveals.openConnection(); }}>Connection and access…</button>
      <button type="button" className="account-controls-menu-action" onClick={() => { close(); reveals.openSettings(); }}>Settings &amp; tools…</button>
    </section>
  </>;
}

/**
 * The account row at the foot of the navigator, and in its collapsed strip as the avatar alone (marked when signed
 * in, the state in its name and its tooltip): the sign-in state, and a popover with that state, up to one action for
 * it and the App's controls. The popover opens beside the row within the window, above it when there is more room
 * above, follows the row when the layout moves it and closes when the row leaves view. It takes focus; Escape closes
 * it and returns focus to the row, as does a press outside it or focus leaving it. It closes by itself when the Codex
 * process or home it was opened for is replaced, and when the account read confirms a sign-in that completed while
 * it was open: focus then goes to the row if it was inside. Nothing is stored.
 */
export function AccountRow({ host, account, reveals }: { host: Json; account: AccountController; reveals: AccountReveals }) {
  const [open, setOpen] = useState(false);
  const root = useRef<HTMLDivElement>(null), trigger = useRef<HTMLButtonElement>(null), panel = useRef<HTMLDivElement>(null);
  const id = useId();
  const words = accountRowWords(host, account.awaiting);
  const focusInside = () => {
    const active = typeof document === "undefined" ? null : (document as Json).activeElement as Node | null | undefined;
    return !!active && !!panel.current && typeof panel.current.contains === "function" && panel.current.contains(active);
  };
  const dismiss = useCallback(() => { setOpen(false); trigger.current?.focus?.(); }, []);
  // Closed by the App, not the person: focus stays where the person put it unless it was inside.
  const closeItself = useCallback(() => { const inside = focusInside(); setOpen(false); if (inside) trigger.current?.focus?.(); }, []);
  const position = useCallback(() => {
    const button = trigger.current, box = panel.current;
    if (!button || !box || typeof button.getBoundingClientRect !== "function" || typeof window.innerHeight !== "number") return;
    const rect = button.getBoundingClientRect();
    if (rect.bottom <= 0 || rect.top >= window.innerHeight || (rect.width === 0 && rect.height === 0)) { closeItself(); return; }
    const width = Math.min(300, window.innerWidth - 24);
    const above = rect.top - 16, below = window.innerHeight - rect.bottom - 16, up = above >= below;
    Object.assign(box.style, { width: `${width}px`, left: `${Math.max(12, Math.min(rect.left, window.innerWidth - width - 12))}px`,
      top: up ? "auto" : `${rect.bottom + 8}px`, bottom: up ? `${window.innerHeight - rect.top + 8}px` : "auto",
      maxHeight: `${Math.max(100, up ? above : below)}px` });
  }, [closeItself]);
  useEffect(() => {
    if (!open || typeof document === "undefined") return;
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
  // After each change of what is shown: the popover follows its row, and focus that sat on a control the new state
  // removed (the action just taken) goes to the popover instead of being lost.
  useEffect(() => {
    if (!open || typeof document === "undefined") return;
    position();
    if ("activeElement" in document) { const active = document.activeElement; if (!active || active === document.body) panel.current?.focus?.(); }
  });
  // The Codex process or home the popover was opened for is replaced: it closes, so no control of the earlier one
  // stays to be pressed.
  const source = sourceKey(host), shownSource = useRef(source);
  useEffect(() => { if (shownSource.current !== source) { shownSource.current = source; closeItself(); } }, [source, closeItself]);
  // The account read confirms a sign-in that completed: the popover closes and the row says the state. Each
  // completion closes it once, by its identity: one confirmed before this row was shown never does, nor one seen
  // again after a status in which it was not readable.
  const seenConfirmed = useRef(new Set<string>(account.confirmed ? [account.confirmed] : []));
  useEffect(() => {
    if (!account.confirmed || seenConfirmed.current.has(account.confirmed)) return;
    seenConfirmed.current.add(account.confirmed);
    closeItself();
  }, [account.confirmed, closeItself]);
  return <div ref={root} className="account-controls-root" onBlur={event => {
    const next = event.relatedTarget as Node | null;
    if (next && !event.currentTarget.contains(next)) setOpen(false);
  }}>
    <button ref={trigger} type="button" className="account-controls-row" title={words.state} aria-label={`Account and settings, ${words.state}`} aria-expanded={open} aria-controls={id} aria-haspopup="dialog" onClick={() => setOpen(!open)}>
      <span className={words.signedIn ? "account-controls-avatar account-controls-avatar-signed-in" : "account-controls-avatar"} data-signed-in={words.signedIn ? "true" : "false"} aria-hidden="true">
        <svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" focusable="false"><circle cx="12" cy="8.5" r="3.5"/><path d="M4.5 20c.9-3.6 3.8-5.5 7.5-5.5s6.6 1.9 7.5 5.5"/></svg>
        {words.signedIn ? <span className="account-controls-avatar-mark">✓</span> : null}
      </span>
      <span className="account-controls-identity"><strong>{words.state}</strong>{words.detail ? <small>{words.detail}</small> : null}</span>
      <span aria-hidden="true">⌃</span>
    </button>
    {open ? <div ref={panel} id={id} role="dialog" aria-label="Account and settings" tabIndex={-1} className="account-controls-popover">
      <AccountPopover host={host} account={account} reveals={reveals} close={dismiss}/>
    </div> : null}
  </div>;
}
