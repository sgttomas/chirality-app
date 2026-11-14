import type { MouseEvent, ReactNode } from "react";

/** Presentation only: disclosures retain every child while closed. */
export function WorkspaceDisclosure({ id, title, description, open, children }: { id: string; title: string; description: string; open?: boolean; children: ReactNode }) {
  return <details id={id} className="workspace-disclosure" open={open}>
    <summary><strong>{title}</strong><span>{description}</span></summary>
    <div className="workspace-disclosure-content">{children}</div>
  </details>;
}

/** Task views. Every view stays mounted; an inactive view is only hidden. */
export const WORKSPACE_VIEWS = [
  { id: "run", label: "Run a workflow", target: "view-run" },
  { id: "make", label: "Make a workflow", target: "view-make" },
  { id: "conversation", label: "Conversation", target: "conversation" },
  { id: "history", label: "History", target: "workspace-history" },
  { id: "settings", label: "Settings & tools", target: "workspace-tools" },
] as const;
let activateView: ((view: string) => void) | null = null;
/** The App registers how a reveal shows the view that holds its target. */
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
const targets = new Set(["view-run", "view-make", "run-workflow", "make-workflow", "workflow-drafts", "desktop-setup", "workflow-reviews", "conversation", "workflow-studio", "workspace-start", "workspace-connection", "workspace-tools", "workspace-history", "file-acts", "other-requests"]);
function revealLink(event: MouseEvent<HTMLElement>): void {
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
    case "changed": return { link: false, words: "The App found that its copy of Codex, or its own files, are not what this App was built with, so it did not start Codex. Reinstall the App from its original download." };
    case "unconfirmed": return build === "development"
      ? { link: false, words: "This build of the App cannot confirm a copy of Codex, so Codex cannot be started from it. There is nothing to do about this in the App." }
      : { link: false, words: "The App could not confirm that its copy of Codex is the one it was built with, so it did not start Codex. Quit and open the App again; if this happens again, reinstall the App from its original download." };
    case "busy": return { link: true, words: "The App was busy with another step when Codex was due to start, so it did not start it. Use Start Codex under Connection and access to try again." };
    default: return { link: true, words: "The App did not record why. Connection and access shows Codex's controls." };
  }
}
export function WorkspaceConnectionStatus({ state, setupRequired, savedSetup, generationClosed, startRefusal, codexHome, refusalCause, build }: {
  state?: string; setupRequired?: boolean; savedSetup?: boolean; generationClosed?: boolean;
  /** The host status's `lastStartRefusal`: why the last start of Codex was refused before it was spawned, and for which home. */
  startRefusal?: { reason?: string; home?: string } | null;
  /** The host status's `codexHome`: the home this status is for. */
  codexHome?: string | null;
  /** The host status's `startRefusalCause` and `build`. */
  refusalCause?: string | null; build?: string | null;
}) {
  const ready = state === "ready" && generationClosed !== true;
  const homeRefusal = !setupRequired && !!state && NO_START_UNDER_WAY.has(state) && !!startRefusal?.reason && !!codexHome && startRefusal.home === codexHome;
  // A start refused before anything connected is said as not started, never as a lost connection.
  const refused = !setupRequired && (state === "refused" || homeRefusal);
  const cause = state === "refused" && !setupRequired && !homeRefusal ? refusedStartWords(refusalCause, build) : null;
  const title = setupRequired ? savedSetup ? "Setup saved — reopen to use it" : "Setup needed"
    : !state ? "Reading connection status…" : ready ? "Codex is connected"
    : state === "starting" ? "Codex is starting…" : state === "stopping" ? "Codex is stopping…"
    : refused ? "Codex was not started"
    : state === "exited-unexpectedly" ? "Codex could not stay connected"
    : "Codex is not connected";
  const linkUseful = !cause || cause.link;
  const guidance = setupRequired ? savedSetup ? "Your saved choices apply on the next launch." : "Choose shared settings and a project below."
    : ready ? "Choose a conversation, or select a model and access entry for a new one."
    : !state ? "Waiting for the App to report its current connection."
    : cause ? cause.words
    : "Open Connection and access to inspect the current status and available controls.";
  return <section className="workspace-connection-status" aria-label="Workspace connection status">
    <p role="status" aria-live="polite"><strong>{title}</strong> <span>{guidance}</span></p>
    {/* Only while no start is under way, and only for the home being shown. */}
    {homeRefusal && startRefusal?.reason
      && <p role="alert" aria-label="Why Codex was not started">{startRefusal.reason.startsWith("Codex was not started") ? startRefusal.reason : `Codex was not started: ${startRefusal.reason}`}</p>}
    {!setupRequired && state && linkUseful && <a href={ready ? "#workspace-start" : "#workspace-connection"}>{ready ? "Choose a new conversation" : "Open connection controls"}</a>}
  </section>;
}

export function DailyWorkspace({ children }: { children: ReactNode }) {
  return <main className="daily-workspace" onClick={revealLink}>
    <style>{`
      .daily-workspace { --workspace-line:var(--rule); --workspace-muted:var(--ink-soft); --workspace-reveal-gap:72px; font-family:var(--font-body); color:var(--ink); background:var(--ground); padding:clamp(12px,2.4vw,32px); line-height:1.5; overflow-wrap:anywhere; max-width:1680px; margin:auto; }
      .daily-workspace * { box-sizing:border-box; }
      .daily-workspace h1 { font-family:var(--font-display); font-weight:400; font-size:1.65rem; margin:0; letter-spacing:-.035em; }
      .daily-workspace h2 { font-family:var(--font-display); font-weight:600; font-size:1.1rem; margin:0 0 12px; }
      .daily-workspace h3 { font-size:1rem; }
      .daily-workspace p { margin:10px 0; }
      .daily-workspace a { color:var(--accent); text-underline-offset:3px; }
      .daily-workspace button,.daily-workspace input,.daily-workspace select,.daily-workspace textarea { font:inherit; max-width:100%; }
      .daily-workspace button { border:1px solid var(--rule-strong); background:var(--card); color:var(--ink); border-radius:6px; padding:5px 10px; cursor:pointer; }
      .daily-workspace button:disabled { color:var(--ink-faint); cursor:default; background:var(--surface); }
      .daily-workspace button:focus-visible,.daily-workspace a:focus-visible,.daily-workspace summary:focus-visible,.daily-workspace input:focus-visible,.daily-workspace select:focus-visible,.daily-workspace textarea:focus-visible,.daily-workspace [tabindex="-1"]:focus-visible { outline:3px solid var(--accent); outline-offset:3px; }
      .daily-workspace input:not([type=radio]):not([type=checkbox]),.daily-workspace select,.daily-workspace textarea { border:1px solid var(--rule-strong); border-radius:5px; padding:5px 7px; background:var(--card); color:inherit; }
      .daily-workspace textarea { resize:vertical; min-height:76px; }
      .daily-workspace pre { font-family:var(--font-code); white-space:pre-wrap; overflow-wrap:anywhere; max-width:100%; overflow-x:auto; font-size:.84rem; background:var(--surface); padding:10px; border-radius:5px; }
      .daily-workspace code,.daily-workspace dd { overflow-wrap:anywhere; }
      .daily-workspace dl { margin:8px 0; }
      .daily-workspace dt { font-size:.78rem; color:var(--workspace-muted); }
      .daily-workspace dd { margin:0 0 7px; }
      .daily-workspace table { display:block; overflow-x:auto; max-width:100%; border-collapse:collapse; }
      .daily-workspace th,.daily-workspace td { padding:7px; text-align:left; vertical-align:top; border:1px solid var(--workspace-line); }
      .daily-workspace summary { cursor:pointer; }
      .daily-workspace [id],.daily-workspace #conversation>div { scroll-margin-top:var(--workspace-reveal-gap); }
      .workspace-connection-status { border-bottom:1px solid var(--rule); padding:0 0 16px; margin:0 0 16px; }
      .workspace-connection-status span { color:var(--ink-soft); }
      .workspace-heading { display:flex; align-items:center; gap:16px; justify-content:space-between; margin-bottom:16px; }
      .workspace-heading p { color:var(--workspace-muted); margin:0; font-size:.88rem; }
      .workspace-nav { position:sticky; top:0; z-index:2; display:flex; flex-wrap:wrap; gap:6px 6px; padding:10px 0; background:var(--ground); border-bottom:1px solid var(--workspace-line); margin-bottom:18px; font-size:.95rem; }
      .workspace-nav a { text-decoration:none; color:var(--ink); padding:6px 12px; border-radius:6px; border:1px solid transparent; }
      .workspace-nav a:hover { border-color:var(--rule-strong); }
      .workspace-nav a[aria-current="page"] { background:var(--cta); color:var(--cta-ink); }
      .workspace-view { min-width:0; }
      .workspace-view-narrow { max-width:980px; }
      .workspace-advanced { margin-top:24px; }
      .workspace-start-fields>* { min-width:0; max-width:100%; }
      .workspace-start-fields h3 { margin:16px 0 6px; font-family:var(--font-display); }
      .workspace-start-fields [aria-label="Available models"] li { margin:8px 0; }
      .workspace-primary { display:block; }
      .workspace-primary-column { min-width:0; padding:18px; border-top:1px solid var(--workspace-line); background:var(--surface); }
      .workspace-primary-column>section { min-width:0; }
      .workspace-primary-column [aria-label="Workflow working context"] { background:var(--surface); border-left:3px solid var(--accent); padding:10px 12px; margin:12px 0; font-size:.85rem; }
      .workspace-primary-column [aria-label="Workflow working context"] details { margin:3px 0; }
      .workspace-primary-column [aria-label="Workflow drafts"] article { margin:14px 0; }
      .workspace-tools { margin-top:24px; }
      .workspace-tools>h2 { color:var(--workspace-muted); font-size:.9rem; }
      .workspace-disclosure { border-top:1px solid var(--workspace-line); background:var(--card); margin:10px 0; }
      .workspace-disclosure>summary { padding:12px 16px; }
      .workspace-disclosure>summary span { display:inline; margin-left:12px; color:var(--workspace-muted); font-size:.82rem; }
      .workspace-disclosure-content { padding:4px 16px 16px; min-width:0; }
      .local-access-alternative { border-top:1px solid var(--rule); padding:12px 0; margin-top:18px; }
      .conversation-options { margin:10px 0; color:var(--ink-soft); }
      .conversation-options>summary { font-size:.9rem; }
      .action-feedback { border-left:3px solid var(--rule-strong); padding:0 12px; margin:12px 0; }
      .action-feedback>details { font-size:.88rem; color:var(--ink-soft); }
      [aria-label="Native activity"]>section { padding:12px 0; }
      [aria-label="Native activity"] h4 { font-family:var(--font-display); margin:8px 0; }
      .workspace-notices:empty { display:none; }
      .workspace-notices { margin:12px 0; }
      .workspace-notices [role=alert] { border-left:3px solid var(--danger); padding-left:10px; }
      .workflow-stage { border-top:1px solid var(--rule); padding:12px 0; margin:12px 0; }
      .workflow-stage h3 { font-family:var(--font-display); }
      .workflow-stage input { margin:6px 0; }
      .history-browser { border-top:1px solid var(--rule); border-bottom:1px solid var(--rule); padding:12px 0; margin:12px 0; }
      .history-search { display:flex; flex-wrap:wrap; align-items:end; gap:8px; margin-top:16px; }
      .history-search label { display:flex; flex:1 1 250px; flex-direction:column; gap:4px; }
      .history-hint,.history-pagination small { color:var(--ink-soft); font-size:.88rem; }
      .history-pagination { display:inline-flex; flex-wrap:wrap; align-items:center; gap:6px; }
      .setup-steps { display:grid; grid-template-columns:repeat(2,minmax(0,1fr)); gap:20px; }
      .setup-step { border:0; border-top:1px solid var(--rule); padding:14px 0; margin:0; min-width:0; }
      .setup-step legend { font-weight:600; padding-right:12px; }
      .setup-step label { display:block; }
      .setup-step input:not([type=radio]) { width:100%; }
      .setup-field { display:flex; flex-wrap:wrap; align-items:end; gap:8px; margin:14px 0; }
      .setup-field label { flex:1 1 220px; }
      .setup-actions { border-top:1px solid var(--rule); padding-top:16px; margin-top:12px; }
      .daily-workspace .setup-primary:not(:disabled) { background:var(--cta); color:var(--cta-ink); border-color:var(--cta); }
      .setup-guidance { color:var(--ink-soft); }
      .setup-state { border-left:3px solid var(--accent); padding:4px 16px; margin:14px 0; }
      .setup-effects { background:var(--surface); padding:16px; margin:16px 0; border:1px solid var(--rule-strong); }
      .first-use { max-width:760px; margin:24px auto 48px; }
      .first-use h1 { font-size:2rem; margin-bottom:8px; }
      .first-use-lead { color:var(--ink-soft); font-size:1.02rem; }
      .first-use-steps { padding-left:22px; }
      .first-use-steps>li { border-top:1px solid var(--rule); padding:14px 0 18px; }
      .first-use-steps h2 { margin:0 0 6px; }
      .first-use-routes { border:0; padding:0; margin:8px 0; }
      .first-use-routes label { display:block; margin:10px 0; }
      .first-use-routes .visually-plain { padding:0; font-weight:400; color:var(--ink-soft); }
      .first-use-saved { border-left:3px solid var(--cta); padding:6px 16px; margin:18px 0; }
      .first-use-path { font-family:var(--font-code); font-size:.82rem; color:var(--ink-soft); overflow-wrap:anywhere; }
      .first-use [aria-label="Your existing Codex settings"] input { width:min(100%, 30rem); }
      .first-use [aria-label="Your existing Codex settings"] label { display:inline-flex; flex-wrap:wrap; gap:4px 8px; align-items:center; max-width:100%; }
      .setup-explainer { margin:14px 0; }
      .setup-explainer li { margin:6px 0; }
      .run-journey { border-top:3px solid var(--accent); padding-top:14px; }
      .run-journey-next { border-left:3px solid var(--accent); padding:4px 12px; }
      .run-journey-steps { padding-left:22px; margin:8px 0; }
      .run-journey-steps>li { padding:6px 0 10px; border-bottom:1px solid var(--workspace-line); }
      .run-journey-steps h3 { margin:4px 0; font-family:var(--font-display); }
      .run-journey-steps label { display:block; }
      .run-journey-steps textarea { width:100%; }
      .run-journey-state { padding:4px 12px; border-left:3px solid var(--rule-strong); }
      .run-journey-waiting { border-left-color:var(--accent); }
      .run-journey-failed { border-left-color:var(--danger); }
      .run-journey-done { border-left-color:var(--cta); }
      .setup-diagnostics { margin-top:20px; color:var(--ink-soft); font-size:.88rem; }
      @media (max-width:720px) { .setup-steps { grid-template-columns:minmax(0,1fr); gap:0; } }
      @media (max-width:1000px) { .workspace-heading { align-items:start; flex-direction:column; gap:3px; } }
      @media (max-width:560px) { .daily-workspace { --workspace-reveal-gap:116px; } .workspace-primary-column { padding:12px; } .workspace-disclosure>summary span { display:block; margin:3px 0 0 17px; } .workspace-nav { gap:6px 14px; font-size:.82rem; } }
    `}</style>
    {children}
  </main>;
}
