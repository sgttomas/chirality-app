import { useCallback, useEffect, useId, useRef, useState } from "react";
import { ACCOUNT_PANEL_WORDS, DIDNT_SAY, SIGN_IN_COMPLETED, SIGN_IN_PHASE_WORDS, accountReadError, accountReadIdentities, accountReadIdentity, accountReadReplied, accountReading, accountSummary, reportedPlan, signInCompletion, signInPhase, signInUnresolved, type ReadAccountStatus } from "./AccountStatus";
import { connectionWords, signInSentence, type ConnectionFacts } from "./DailyWorkspace";
import { AgentText } from "./AgentText";
import { readingSentence } from "./readingSentences";

type Json = any; // eslint-disable-line @typescript-eslint/no-explicit-any

/** The account action a state offers. */
export type AccountActionName = "sign-in" | "check-again" | "sign-out";
/** The App's present commands for the account, each for the Codex process and home it is given. Each rejects where
 * its command was refused or failed, having said so on the App line. */
export type AccountCommands = {
  /** Reads the account again: the workspace line's Check again and the account panel's Check account status. */
  checkAgain: (generation: Json, modeHomeClass: string, isCurrent?: () => boolean) => Promise<void>;
  /** oauth_start with mode "browser": the sign-in Connection and access starts. Resolves with the command's result. */
  startSignIn: (generation: Json) => Promise<Json>;
  /** logout_home for the account home: Connection and access's Sign out of ChatGPT. Resolves with the command's result. */
  signOut: (generation: Json, modeHomeClass: string) => Promise<Json>;
  /** One read of the host's status, applied as the App applies its reads, resolving with the status read. */
  readStatus: () => Promise<Json>;
};
/** Where the App holds a completed sign-in not yet confirmed: the account is being read now, or has not been read since. */
export type CompletedState = "checking" | "unread";
/** An account command another surface sends (Connection and access): "sign-in" for either of its sign-ins, "sign-out"
 * for its sign-out. */
export type PanelAccountCommand = "sign-in" | "sign-out";
/** The account's actions as every surface that offers them shares them (useAccountController). */
export type AccountController = {
  /** One account command is under way, from whichever surface it was pressed (the row, the strip, the line or
   * Connection and access). */
  acting: boolean;
  /** What the App says of the last attempt that was not sent, was declined at its confirmation or did not go through,
   * while the account of the Codex process and home it was made for still stands as it did then; else null. */
  feedback: string | null;
  /** A sign-in Codex reports completed for the current process and home that no account read made after it has
   * answered with a result: the account is being read, or has not been read since; else null. A completion this view
   * did not watch completing (one already there when it was mounted) is held the same way, since nothing here shows
   * which reads came after it. */
  completed: CompletedState | null;
  /** `completed` is not null. */
  awaiting: boolean;
  /** The completed sign-in an account read made after it confirmed as a ChatGPT account, by the completion's own
   * identity; else null. */
  confirmed: string | null;
  /** Sends the action for the status `shown` when it was pressed, and only if the latest status the App has accepted
   * has the same Codex process and home, the App is not moving between homes, no other account command is under way
   * and the action is still the one the account's state offers. Otherwise nothing is sent. */
  act: (action: AccountActionName, shown: Json) => Promise<void>;
  /** Runs one of Connection and access's own account commands under the same admission: nothing is run while another
   * account command is under way or the App is moving between homes, and no sign-in while the host reports one that has
   * not ended or a completed one is unconfirmed. Resolves with whether it ran. */
  run: (command: PanelAccountCommand, send: () => Promise<void>) => Promise<boolean>;
  /** The account panel's read, under the same admission and as part of the same proof of a completed sign-in. */
  admitRead: (reader: ReadAccountStatus) => ReadAccountStatus;
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
 * which Codex didn't say is never "Not signed in". `completed` (the controller's) is a sign-in Codex reported
 * completed with no account read made after it answered: the earlier reading is not said then. The email is never here. */
export function accountRowWords(host: Json, completed: CompletedState | null = null): { state: string; detail: string | null; signedIn: boolean } {
  const connection = connectionWords(connectionFacts(host));
  if (connection) return { state: connection.title, detail: null, signedIn: false };
  const reading = accountReading(host);
  if (completed) return { state: "Sign-in completed", detail: SIGN_IN_COMPLETED[completed].detail, signedIn: false };
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
export function accountAction(host: Json, completed: CompletedState | null = null): AccountActionName | null {
  if (connectionWords(connectionFacts(host))) return null;
  const reading = accountReading(host);
  if (completed) return completed === "checking" ? null : "check-again";
  return reading === "no-account" ? "sign-in" : reading === "chatgpt-account" ? "sign-out"
    : reading === "unread" || DIDNT_SAY.includes(reading) ? "check-again" : null;
}

/** The popover's sentence under the state. Where Codex didn't say, it is the account panel's own sentence for the
 * reading, so a read that failed, one left unanswered and the rest stay distinct. */
function accountSentence(host: Json, completed: CompletedState | null): string {
  const connection = connectionWords(connectionFacts(host));
  if (connection) return connection.guidance;
  const reading = accountReading(host);
  if (completed) return SIGN_IN_COMPLETED[completed].sentence;
  if (reading !== "chatgpt-account" && DIDNT_SAY.includes(reading)) return ACCOUNT_PANEL_WORDS[reading as Exclude<typeof reading, "chatgpt-account">];
  return signInSentence(reading, reportedPlan(host));
}

/** The Codex process and home a status is for: a control drawn for one is a different control from one drawn for another. */
export const sourceKey = (host: Json) => JSON.stringify([host?.generation ?? null, host?.homeRouting?.activeModeHomeClass ?? null]);
const NOT_SENT = "The connection or the account changed before this was sent. Nothing was sent.";
const FAILED: Record<AccountActionName, string> = {
  "sign-in": "The App could not confirm that a sign-in started.",
  "check-again": "Account status could not be confirmed. Try checking again; this does not mean you are signed out.",
  "sign-out": "The App could not confirm the sign-out. Check again to see the account.",
};
/** The results the host's commands return where the person declined the native confirmation and nothing was sent
 * (runtime_session.rs start_native_oauth, logout_native_home), with the App's sentence for each. */
const DECLINED: Partial<Record<AccountActionName, { state: string; words: string }>> = {
  "sign-in": { state: "native start confirmation dismissed; no sign-in RPC", words: "Sign-in was not started." },
  "sign-out": { state: "native confirmation cancelled; no logout request", words: "You were not signed out." },
};

/** The command's result says the person declined its native confirmation, and nothing was sent. */
export const accountDeclined = (action: AccountActionName, result: Json): boolean => !!DECLINED[action] && result?.state === DECLINED[action]!.state;

/** Which Codex processes, and which completed sign-ins in them, this App view has seen. A completion first seen in a
 * status of a process seen before without it was watched completing; one already there when the process was first
 * seen was not. Only a watched completion closes the popover and moves to a new conversation once confirmed. */
type Seen = { generations: string[]; completions: Record<string, boolean> };
const generationKey = (host: Json): string | null => host?.generation ? JSON.stringify(host.generation) : null;
const watchedIn = (seen: Seen, completion: string, generation: string | null) =>
  Object.hasOwn(seen.completions, completion) ? seen.completions[completion] : !!generation && seen.generations.includes(generation);
/** The latest account read of the status was registered after the baseline was taken: its request identity is not
 * one the baseline lists (the reads are already of the status's own process: AccountStatus.tsx accountReads). */
function madeAfter(baseline: string[] | undefined, host: Json): boolean {
  const identity = accountReadIdentity(host);
  return !!baseline && identity !== null && !baseline.includes(identity);
}
/** The latest account read was made after the completion and has answered with a result. A read whose wait ended
 * without a reply, or that was answered with an error, settles nothing. */
const answeredAfter = (baseline: string[] | undefined, host: Json): boolean => madeAfter(baseline, host) && accountReadReplied(host);
function completedIn(baselines: Record<string, string[]>, host: Json, reading: boolean): CompletedState | null {
  const completion = signInCompletion(host);
  if (!completion) return null;
  const baseline = baselines[completion];
  if (answeredAfter(baseline, host)) return null;
  return reading || (madeAfter(baseline, host) && accountReading(host) === "reading") ? "checking" : "unread";
}
/** How long the controller waits for the status read that gives a baseline before it gives up and offers Check again. */
export const BASELINE_STATUS_WAIT_MS = 10_000;
type Acting = "sign-in" | "sign-out" | "read" | null;

/**
 * The account's actions for every surface that offers them (the account row in the navigator and in its collapsed
 * strip, the workspace line, and Connection and access): one account command at a time across all of them, each bound
 * to the Codex process and home shown when it was pressed and checked against the latest status the App has accepted
 * (`latest`), none while the App is moving between homes (`moving`).
 *
 * A completed sign-in is confirmed only by an account read issued after the completion. The host status gives no
 * order between its account reads and the completion, so the controller makes one: on seeing the completion it reads
 * the host's status once (a read started after the status that showed the completion arrived) and keeps, as the
 * baseline, the request identity of every account read the host had registered for that process by then
 * (accountReadIdentities), whether or not its account reads list it yet; then it issues one account read. A read whose
 * identity the baseline does not hold was registered after that status was taken, so after the completion; the latest
 * such read, once it has answered with a result, is the confirmation. A read registered earlier is never taken for it,
 * even one the status lists only later. Until then the completion is `completed`, and a read that ended without a
 * result leaves it so, with Check again. A status read that does not return within `baselineWait` (ms) is given up,
 * with Check again. Every check of the account made while it is unconfirmed does the same. Nothing is stored, and
 * nothing is recorded during render.
 */
export function useAccountController(host: Json, latest: () => Json, commands: AccountCommands, moving: () => boolean = () => false, baselineWait: number = BASELINE_STATUS_WAIT_MS): AccountController {
  const mounted = useRef(true);
  useEffect(() => { mounted.current = true; return () => { mounted.current = false; }; }, []);
  const inFlight = useRef(false);
  const [acting, setActing] = useState<Acting>(null);
  const [feedback, setFeedback] = useState<{ checkpoint: string; words: string } | null>(null);
  const [seen, setSeen] = useState<Seen>({ generations: [], completions: {} });
  const [baselines, setBaselines] = useState<Record<string, string[]>>({});
  const [autoRead, setAutoRead] = useState<string[]>([]);
  // The baselines, for a press or a read: kept by an effect and by the read that takes a baseline, never during render.
  const baselinesNow = useRef(baselines);
  useEffect(() => { baselinesNow.current = { ...baselines, ...baselinesNow.current }; }, [baselines]);
  const generation = generationKey(host), completion = signInCompletion(host);
  useEffect(() => {
    if (!generation) return;
    setSeen(old => {
      const known = old.generations.includes(generation);
      if (known && (!completion || Object.hasOwn(old.completions, completion))) return old;
      return { generations: known ? old.generations : [...old.generations, generation],
        completions: completion && !Object.hasOwn(old.completions, completion) ? { ...old.completions, [completion]: known } : old.completions };
    });
  }, [generation, completion]);
  const watched = !!completion && watchedIn(seen, completion, generation);
  const completed = completedIn(baselines, host, acting === "read");
  const confirmed = completion && watched && answeredAfter(baselines[completion], host) && accountReading(host) === "chatgpt-account" ? completion : null;
  const completedNow = (status: Json) => completedIn(baselinesNow.current, status, false);
  const checkpoint = (status: Json, held: CompletedState | null) => JSON.stringify([sourceKey(status), accountReading(status), signInPhase(status), held !== null]);
  const admit = (kind: Exclude<Acting, null>): (() => void) | null => {
    if (inFlight.current || moving()) return null;
    inFlight.current = true; setActing(kind);
    return () => { inFlight.current = false; if (mounted.current) setActing(null); };
  };
  // One check of the account for the status shown, by `reader`; false where the status changed first and nothing was read.
  const readFor = async (shown: Json, reader: ReadAccountStatus, isCurrent: () => boolean = () => true): Promise<boolean> => {
    const key = signInCompletion(shown);
    if (key && !baselinesNow.current[key]) {
      let timer: ReturnType<typeof setTimeout> | undefined;
      const status = await Promise.race([commands.readStatus(),
        new Promise<never>((_, reject) => { timer = setTimeout(() => reject(Error("The status read for the account check did not return.")), baselineWait); })])
        .finally(() => clearTimeout(timer));
      if (sourceKey(status) !== sourceKey(shown) || signInCompletion(status) !== key) return false;
      const baseline = accountReadIdentities(status);
      if (!baseline) throw Error("The status did not list the account reads under way.");
      baselinesNow.current = { ...baselinesNow.current, [key]: baseline };
      if (mounted.current) setBaselines(old => old[key] ? old : { ...old, [key]: baseline });
    }
    await reader(shown.generation, shown.homeRouting.activeModeHomeClass, isCurrent);
    return true;
  };
  const sameSource = (a: Json, b: Json) => sourceKey(a) === sourceKey(b) && !!a?.generation && typeof a?.homeRouting?.activeModeHomeClass === "string";
  const act = async (action: AccountActionName, shown: Json) => {
    if (inFlight.current) return;
    const now = latest(), held = completedNow(now), mode = now?.homeRouting?.activeModeHomeClass;
    const eligible = !moving() && sameSource(now, shown) && accountAction(now, held) === action
      && (action === "check-again" || mode === "account") && !(action === "sign-in" && signInUnresolved(now));
    if (!eligible) { setFeedback({ checkpoint: checkpoint(now, held), words: NOT_SENT }); return; }
    const release = admit(action === "check-again" ? "read" : action);
    if (!release) return;
    // The attempt's own Codex process, home and account state: what it reports is said only while they stand.
    const attempt = checkpoint(now, held);
    setFeedback(null);
    try {
      if (action === "check-again") {
        if (!await readFor(now, commands.checkAgain) && mounted.current) setFeedback({ checkpoint: checkpoint(latest(), completedNow(latest())), words: NOT_SENT });
        return;
      }
      const result = action === "sign-in" ? await commands.startSignIn(now.generation) : await commands.signOut(now.generation, mode);
      if (accountDeclined(action, result) && mounted.current) setFeedback({ checkpoint: attempt, words: DECLINED[action]!.words });
    } catch (error) {
      if (mounted.current) setFeedback({ checkpoint: attempt, words: (action === "check-again" ? readingSentence(error) : null) ?? FAILED[action] });
    } finally { release(); }
  };
  // A completion not yet confirmed, for the status shown: one account read, made after a baseline, without a press.
  useEffect(() => {
    if (!completion || baselines[completion] || autoRead.includes(completion) || acting) return;
    const now = latest();
    if (!sameSource(now, host) || signInCompletion(now) !== completion) return;
    const release = admit("read");
    if (!release) return;
    setAutoRead(old => [...old, completion]);
    const attempt = checkpoint(now, completedNow(now));
    void readFor(now, commands.checkAgain).catch(error => {
      if (mounted.current) setFeedback({ checkpoint: attempt, words: readingSentence(error) ?? FAILED["check-again"] });
    }).finally(release);
  }, [completion, baselines, autoRead, acting]); // eslint-disable-line react-hooks/exhaustive-deps
  const run = async (command: PanelAccountCommand, send: () => Promise<void>) => {
    const now = latest();
    if (command === "sign-in" && (signInUnresolved(now) || completedNow(now) !== null)) return false;
    const release = admit(command);
    if (!release) return false;
    try { await send(); return true; } finally { release(); }
  };
  const admitRead = (reader: ReadAccountStatus): ReadAccountStatus => async (generation, modeHomeClass, isCurrent) => {
    const now = latest();
    if (!sameSource(now, { generation, homeRouting: { activeModeHomeClass: modeHomeClass } })) return;
    const release = admit("read");
    if (!release) return;
    try { await readFor(now, reader, isCurrent); } finally { release(); }
  };
  return { acting: acting !== null, feedback: feedback && feedback.checkpoint === checkpoint(host, completed) ? feedback.words : null,
    completed, awaiting: completed !== null, confirmed, act, run, admitRead };
}

function AccountPopover({ host, account, reveals, close }: { host: Json; account: AccountController; reveals: AccountReveals; close: () => void }) {
  const words = accountRowWords(host, account.completed), connection = connectionWords(connectionFacts(host));
  const reading = accountReading(host), action = accountAction(host, account.completed);
  const generation = host?.generation, accountHome = host?.homeRouting?.activeModeHomeClass === "account";
  const codexError = !connection && !account.awaiting && DIDNT_SAY.includes(reading) ? accountReadError(host) : null;
  // The sign-in line: the account panel's own words for a sign-in that is waiting, did not complete, was canceled or
  // has not ended. A completed one is said by the state above.
  const phase = signInPhase(host);
  const phaseWords = !connection && !words.signedIn && phase !== "completed" ? SIGN_IN_PHASE_WORDS[phase] : "";
  const busy = account.acting;
  // Keyed by the Codex process and home: a control drawn for one is never the control of another, so a press that
  // began on it before they were replaced does not land on a control of the replacement.
  return <>
    <section key={sourceKey(host)} className="account-controls-group" aria-label="Account">
      <strong>{words.state}</strong>
      <p>{accountSentence(host, account.completed)}</p>
      {!connection && !account.awaiting && reading === "chatgpt-account" ? <p>{accountSummary(host)}</p> : null}
      {codexError ? <p aria-label="What Codex said"><AgentText value={codexError} source="codex"/></p> : null}
      {phaseWords ? <p>{phaseWords}</p> : null}
      {action === "sign-in" ? <button type="button" className="setup-primary" disabled={busy || !accountHome || !generation || signInUnresolved(host)} onClick={() => { void account.act("sign-in", host); }}>Sign in with your ChatGPT account (through Codex)…</button> : null}
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
 * it was open: focus then goes to the row if it was inside. It takes focus back only where the control that held
 * focus inside it was removed and focus has gone nowhere else. No focus it moves scrolls. Nothing is stored.
 */
export function AccountRow({ host, account, reveals }: { host: Json; account: AccountController; reveals: AccountReveals }) {
  const [open, setOpen] = useState(false);
  const root = useRef<HTMLDivElement>(null), trigger = useRef<HTMLButtonElement>(null), panel = useRef<HTMLDivElement>(null);
  const id = useId();
  const words = accountRowWords(host, account.completed);
  // The control inside the popover that last took focus.
  const heldFocus = useRef<Node | null>(null);
  const focusOn = (element: HTMLElement | null) => { element?.focus?.({ preventScroll: true }); };
  const focusInside = () => {
    const active = typeof document === "undefined" ? null : (document as Json).activeElement as Node | null | undefined;
    return !!active && !!panel.current && typeof panel.current.contains === "function" && panel.current.contains(active);
  };
  const dismiss = useCallback(() => { setOpen(false); focusOn(trigger.current); }, []);
  // Closed by the App, not the person: focus stays where the person put it unless it was inside.
  const closeItself = useCallback(() => { const inside = focusInside(); setOpen(false); if (inside) focusOn(trigger.current); }, []);
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
    heldFocus.current = null;
    focusOn(panel.current);
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
  // After each change of what is shown: the popover follows its row, and focus that sat on a control inside it which
  // the new state removed (the action just taken) goes to the popover instead of being lost. Focus the person moved
  // elsewhere, or a window left for another, is not taken: the control that held it is still there.
  useEffect(() => {
    if (!open || typeof document === "undefined") return;
    position();
    const held = heldFocus.current, box = panel.current;
    if (!held || !box || box.contains(held)) return;
    heldFocus.current = null;
    const active = "activeElement" in document ? document.activeElement : null;
    if (!active || active === document.body) focusOn(box);
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
    {open ? <div ref={panel} id={id} role="dialog" aria-label="Account and settings" tabIndex={-1} className="account-controls-popover" onFocus={event => { heldFocus.current = event.target as Node; }}>
      <AccountPopover host={host} account={account} reveals={reveals} close={dismiss}/>
    </div> : null}
  </div>;
}
