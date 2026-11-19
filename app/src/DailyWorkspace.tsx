import { useEffect, useRef, useState, type MouseEvent, type ReactNode } from "react";
import { DIDNT_SAY, SIGN_IN_WORDS, planWords, type AccountReading } from "./AccountStatus";
import { AgentText } from "./AgentText";

/** Presentation only: disclosures retain every child while closed. */
export function WorkspaceDisclosure({ id, title, description, open, onToggle, children }: { id: string; title: string; description: string; open?: boolean; onToggle?: (open: boolean) => void; children: ReactNode }) {
  return <details id={id} className="workspace-disclosure" open={open} onToggle={onToggle ? event => onToggle((event.currentTarget as HTMLDetailsElement).open) : undefined}>
    <summary><strong>{title}</strong><span>{description}</span></summary>
    <div className="workspace-disclosure-content">{children}</div>
  </details>;
}

let activateView: ((view: string) => void) | null = null;
/** The App registers how a reveal shows the view that holds its target (the conversation, or a right panel tab). */
export function registerWorkspaceViews(activate: (view: string) => void): () => void {
  activateView = activate;
  return () => { if (activateView === activate) activateView = null; };
}
function viewOf(target: HTMLElement | null): string | null {
  for (let node: HTMLElement | null = target; node; node = node.parentNode as HTMLElement | null) {
    const view = node.getAttribute?.("data-workspace-view");
    if (view) return view;
  }
  return null;
}
/** Reveal an existing target; it changes no source, choice or host state.
 * A target in another task view first makes that view visible. */
export function revealWorkspaceTarget(id: string, focus = false): void {
  if (typeof document?.getElementById !== "function") return;
  const target = document.getElementById(id);
  const view = viewOf(target);
  if (view && activateView) activateView(view);
  for (let node: HTMLElement | null = target; node; node = node.parentNode as HTMLElement | null) {
    if (node.tagName === "DETAILS") (node as HTMLDetailsElement).open = true;
  }
  if (focus && target) {
    const destination = target.tagName === "DETAILS"
      ? Array.from(target.childNodes).find(node => (node as HTMLElement).tagName === "SUMMARY") as HTMLElement | undefined
      : target;
    if (destination) {
      if (destination.tagName !== "SUMMARY") destination.setAttribute("tabindex", "-1");
      destination.focus?.({ preventScroll: true });
    }
  }
  target?.scrollIntoView?.({ block: "start" });
}
const targets = new Set(["waiting-on-you", "view-run", "view-make", "run-workflow", "make-workflow", "workflow-drafts", "desktop-setup", "workflow-reviews", "conversation", "workflow-studio", "workspace-start", "workspace-connection", "workspace-tools", "workspace-history", "file-acts", "other-requests"]);
/** The workspace root's click handler: a "#target" link to a known target reveals it instead of navigating. */
export function revealWorkspaceLink(event: MouseEvent<HTMLElement>): void {
  for (let node = event.target as HTMLElement | null; node && node !== event.currentTarget; node = node.parentNode as HTMLElement | null) {
    const href = node.tagName === "A" ? node.getAttribute("href") : null;
    if (href?.startsWith("#") && targets.has(href.slice(1))) { event.preventDefault?.(); revealWorkspaceTarget(href.slice(1), true); return; }
    // A clean trial's own composer; if it isn't shown, its conversation view.
    if (href?.startsWith("#run-evidence-")) { event.preventDefault?.(); revealWorkspaceTarget(document.getElementById(href.slice(1)) ? href.slice(1) : "workflow-studio", true); return; }
    if (href?.startsWith("#registered-revision-")) { event.preventDefault?.(); revealWorkspaceTarget(document.getElementById(href.slice(1)) ? href.slice(1) : "workflow-studio", true); return; }
    if (href?.startsWith("#new-trial-")) { event.preventDefault?.(); revealWorkspaceTarget(document.getElementById(href.slice(1)) ? href.slice(1) : "conversation", true); return; }
  }
}

/** A reading of the host snapshot, never a start/admission or model selection. */
/** Codex states in which no start is under way and Codex is not connected. */
const NO_START_UNDER_WAY = new Set(["absent", "stopped", "refused", "exited-unexpectedly", "halted-after-repeated-failure"]);
/**
 * Why a start of Codex was refused, in the person's words, with what they can do, from the cause the
 * host chose where it refused the start (`startRefusalCause`) and the build kind. `link` says whether
 * Connection and access has something for the person to do about it.
 */
export function refusedStartWords(cause?: string | null, build?: string | null): { words: string; link: boolean } {
  switch (cause) {
    // A mismatch, or a read of the files that failed: the scan records both as a mismatch, so the
    // words say both, and put a relaunch first.
    case "changed": return { link: false, words: "The App found that its copy of Codex, or its own files, do not match what this App was built with, or could not read them, so it did not start Codex. Quit and open the App again; if this happens again, reinstall the App from its original download." };
    case "unconfirmed": return build === "development"
      // A version probe that failed once gives this too, so a later attempt can succeed.
      ? { link: true, words: "This build of the App could not confirm a copy of Codex, so it did not start Codex. Use Start Codex under Connection and access to try again; if it happens again, this build may not include a usable copy of Codex." }
      : { link: false, words: "The App could not confirm that its copy of Codex is the one it was built with, so it did not start Codex. Quit and open the App again; if this happens again, reinstall the App from its original download." };
    case "busy": return { link: true, words: "The App was busy with another step when Codex was due to start, so it did not start it. Use Start Codex under Connection and access to try again." };
    default: return { link: true, words: "The App did not record why. Connection and access shows Codex's controls." };
  }
}
/** The connection facts of the host status that the workspace line and the account row both read. */
export type ConnectionFacts = {
  state?: string; setupRequired?: boolean; savedSetup?: boolean; generationClosed?: boolean;
  /** The host status's `lastStartRefusal`: why the last start of Codex was refused before it was spawned, and for which home. */
  startRefusal?: { reason?: string; home?: string } | null;
  /** The host status's `codexHome`: the home this status is for. */
  codexHome?: string | null;
  /** The host status's `startRefusalCause` and `build`. */
  refusalCause?: string | null; build?: string | null;
};
function connectionReading({ state, setupRequired, savedSetup, generationClosed, startRefusal, codexHome, refusalCause, build }: ConnectionFacts) {
  const ready = state === "ready" && generationClosed !== true;
  const homeRefusal = !setupRequired && !!state && NO_START_UNDER_WAY.has(state) && !!startRefusal?.reason && !!codexHome && startRefusal.home === codexHome;
  // A start refused before anything connected is said as not started, never as a lost connection.
  const refused = !setupRequired && (state === "refused" || homeRefusal);
  const cause = state === "refused" && !setupRequired && !homeRefusal ? refusedStartWords(refusalCause, build) : null;
  // While Codex is running, the sign-in reading speaks instead (null here).
  const title = setupRequired ? savedSetup ? "Setup saved — reopen to use it" : "Setup needed"
    : !state ? "Reading connection status…" : ready ? null
    : state === "starting" ? "Codex is starting…" : state === "stopping" ? "Codex is stopping…"
    : refused ? "Codex was not started"
    : state === "exited-unexpectedly" ? "Codex could not stay connected"
    : "Codex is not connected";
  const guidance = setupRequired ? savedSetup ? "Your saved choices apply on the next launch." : "Choose shared settings and a project below."
    // Codex started and the App reached it. Whether anyone is signed in is what the account reads the host
    // recorded for this connection establish; the host reads the account itself once Codex is ready.
    : ready ? ""
    : !state ? "Waiting for the App to report its current connection."
    : cause ? cause.words
    : "Open Connection and access to inspect the current status and available controls.";
  return { ready, homeRefusal, cause, title, guidance };
}
/** The connection's words while Codex is not running and ready (or setup is needed): its title and guidance, as the
 * workspace line says them; null while Codex is ready, when the sign-in reading speaks. The workspace line and the
 * account row both take their words from here, so the two never disagree. */
export function connectionWords(facts: ConnectionFacts): { title: string; guidance: string } | null {
  const { title, guidance } = connectionReading(facts);
  return title === null ? null : { title, guidance };
}
/** The workspace line's sentence while Codex is ready: the sign-in reading's own (SIGN_IN_WORDS), which says Codex is
 * running, with the plan Codex reports for a ChatGPT account. */
export function signInSentence(signIn: AccountReading, plan: string | null): string {
  return `${SIGN_IN_WORDS[signIn]}${signIn === "chatgpt-account" ? planWords(plan) : ""}`;
}
export function WorkspaceConnectionStatus({ state, setupRequired, savedSetup, generationClosed, startRefusal, codexHome, refusalCause, build, signIn = "unread", plan = null, codexError = null, busy = false, checkAgain, startSignIn }: ConnectionFacts & {
  /** What the App has established of this connection's sign-in (AccountStatus.tsx, accountReading): the same
   * reading the account panel shows, so the two never disagree. */
  signIn?: AccountReading;
  /** The plan Codex reports with a ChatGPT account (AccountStatus.tsx, reportedPlan). */
  plan?: string | null;
  /** Codex's own message where the account read answered with an error (AccountStatus.tsx, accountReadError). */
  codexError?: string | null;
  /** An account action is under way elsewhere, or a sign-in is waiting to complete: neither button is pressed then. */
  busy?: boolean;
  /** Reads the account again, as the account panel's check does: offered when Codex didn't say. */
  checkAgain?: () => Promise<void>;
  /** The sign-in Connection and access starts: offered here when Codex reports no account. */
  startSignIn?: () => Promise<void>;
}) {
  const { ready, homeRefusal, cause, title: connectionTitle, guidance } = connectionReading({ state, setupRequired, savedSetup, generationClosed, startRefusal, codexHome, refusalCause, build });
  const mounted = useRef(true);
  useEffect(() => { mounted.current = true; return () => { mounted.current = false; }; }, []);
  const [acting, setActing] = useState(false);
  const act = async (action?: () => Promise<void>) => {
    if (!action || acting) return;
    setActing(true);
    try { await action(); } catch { /* the panel and the App line say what happened */ } finally { if (mounted.current) setActing(false); }
  };
  const didntSay = ready && DIDNT_SAY.includes(signIn);
  const offerSignIn = ready && signIn === "no-account" && !!startSignIn;
  // While Codex is running, the line is the sign-in reading's own sentence (SIGN_IN_WORDS), which says Codex is running.
  const title = connectionTitle ?? signInSentence(signIn, plan);
  const linkUseful = !cause || cause.link;
  return <section className="workspace-connection-status" aria-label="Workspace connection status">
    <p role="status" aria-live="polite"><strong>{title}</strong>{guidance ? <> <span>{guidance}</span></> : null}</p>
    {didntSay && codexError && <p aria-label="What Codex said"><AgentText value={codexError} source="codex"/></p>}
    {didntSay && checkAgain && <p><button disabled={acting || busy} onClick={() => { void act(checkAgain); }}>Check again</button></p>}
    {offerSignIn && <p><button className="setup-primary" disabled={acting || busy} onClick={() => { void act(startSignIn); }}>Sign in with your ChatGPT account (through Codex)…</button></p>}
    {/* Only while no start is under way, and only for the home being shown. */}
    {homeRefusal && startRefusal?.reason
      && <p role="alert" aria-label="Why Codex was not started">{startRefusal.reason.startsWith("Codex was not started") ? startRefusal.reason : `Codex was not started: ${startRefusal.reason}`}</p>}
    {!setupRequired && state && linkUseful && !offerSignIn && <a href={ready && signIn === "chatgpt-account" ? "#workspace-start" : "#workspace-connection"}>{ready && signIn === "chatgpt-account" ? "Choose a new conversation" : "Open connection controls"}</a>}
  </section>;
}
