import type { MouseEvent, ReactNode } from "react";

/** Presentation only: disclosures retain every child while closed. */
export function WorkspaceDisclosure({ id, title, description, open, children }: { id: string; title: string; description: string; open?: boolean; children: ReactNode }) {
  return <details id={id} className="workspace-disclosure" open={open}>
    <summary><strong>{title}</strong><span>{description}</span></summary>
    <div className="workspace-disclosure-content">{children}</div>
  </details>;
}

/** Reveal an existing target; it changes no source, choice or host state. */
export function revealWorkspaceTarget(id: string, focus = false): void {
  const target = document.getElementById(id);
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
const targets = new Set(["conversation", "workflow-studio", "workspace-start", "workspace-connection", "workspace-tools", "workspace-history", "file-acts", "other-requests"]);
function revealLink(event: MouseEvent<HTMLElement>): void {
  for (let node = event.target as HTMLElement | null; node && node !== event.currentTarget; node = node.parentNode as HTMLElement | null) {
    const href = node.tagName === "A" ? node.getAttribute("href") : null;
    if (href?.startsWith("#") && targets.has(href.slice(1))) { event.preventDefault?.(); revealWorkspaceTarget(href.slice(1), true); return; }
  }
}

/** A reading of the host snapshot, never a start/admission or model selection. */
export function WorkspaceConnectionStatus({ state, setupRequired, savedSetup, generationClosed }: {
  state?: string; setupRequired?: boolean; savedSetup?: boolean; generationClosed?: boolean;
}) {
  const ready = state === "ready" && generationClosed !== true;
  const title = setupRequired ? savedSetup ? "Setup saved — reopen to use it" : "Setup needed"
    : !state ? "Reading connection status…" : ready ? "Codex is connected"
    : state === "starting" ? "Codex is starting…" : state === "stopping" ? "Codex is stopping…"
    : state === "refused" || state === "exited-unexpectedly" ? "Codex could not stay connected"
    : "Codex is not connected";
  const guidance = setupRequired ? savedSetup ? "Your saved choices apply on the next launch." : "Choose shared settings and a project below."
    : ready ? "Choose a conversation, or select a model and access entry for a new one."
    : !state ? "Waiting for the App to report its current connection."
    : "Open Connection & access to inspect the current status and available controls.";
  return <section className="workspace-connection-status" aria-label="Workspace connection status">
    <p role="status" aria-live="polite"><strong>{title}</strong> <span>{guidance}</span></p>
    {!setupRequired && state && <a href={ready ? "#workspace-start" : "#workspace-connection"}>{ready ? "Choose a new conversation" : "Open connection controls"}</a>}
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
      .workspace-nav { position:sticky; top:0; z-index:2; display:flex; flex-wrap:wrap; gap:8px 20px; padding:10px 0; background:var(--ground); border-bottom:1px solid var(--workspace-line); margin-bottom:18px; font-size:.9rem; }
      .workspace-start-fields { display:flex; flex-wrap:wrap; align-items:end; gap:10px 18px; }
      .workspace-start-fields>* { min-width:0; max-width:100%; }
      .workspace-start-fields p { margin:0; }
      .workspace-primary { display:grid; grid-template-columns:minmax(0,1fr) minmax(0,1fr); gap:20px; align-items:start; }
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
      .workspace-notices:empty { display:none; }
      .workspace-notices { margin:12px 0; }
      .workspace-notices [role=alert] { border-left:3px solid var(--danger); padding-left:10px; }
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
      .setup-diagnostics { margin-top:20px; color:var(--ink-soft); font-size:.88rem; }
      @media (max-width:720px) { .setup-steps { grid-template-columns:minmax(0,1fr); gap:0; } }
      @media (max-width:1000px) { .workspace-primary { grid-template-columns:minmax(0,1fr); } .workspace-heading { align-items:start; flex-direction:column; gap:3px; } }
      @media (max-width:560px) { .daily-workspace { --workspace-reveal-gap:116px; } .workspace-primary-column { padding:12px; } .workspace-disclosure>summary span { display:block; margin:3px 0 0 17px; } .workspace-nav { gap:6px 14px; font-size:.82rem; } }
    `}</style>
    {children}
  </main>;
}
