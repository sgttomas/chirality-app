import type { MouseEvent, ReactNode } from "react";

/** Presentation only: disclosures retain every child while closed. */
export function WorkspaceDisclosure({ id, title, description, open, children }: { id: string; title: string; description: string; open?: boolean; children: ReactNode }) {
  return <details id={id} className="workspace-disclosure" open={open}>
    <summary><strong>{title}</strong><span>{description}</span></summary>
    <div className="workspace-disclosure-content">{children}</div>
  </details>;
}

/** Reveal an existing target; it changes no source, choice or host state. */
export function revealWorkspaceTarget(id: string): void {
  const target = document.getElementById(id);
  for (let node: HTMLElement | null = target; node; node = node.parentNode as HTMLElement | null) {
    if (node.tagName === "DETAILS") (node as HTMLDetailsElement).open = true;
  }
  target?.scrollIntoView?.({ block: "start" });
}
const targets = new Set(["conversation", "workflow-studio", "workspace-start", "workspace-connection", "workspace-tools", "file-acts", "other-requests"]);
function revealLink(event: MouseEvent<HTMLElement>): void {
  for (let node = event.target as HTMLElement | null; node && node !== event.currentTarget; node = node.parentNode as HTMLElement | null) {
    const href = node.tagName === "A" ? node.getAttribute("href") : null;
    if (href?.startsWith("#") && targets.has(href.slice(1))) { revealWorkspaceTarget(href.slice(1)); return; }
  }
}

export function DailyWorkspace({ children }: { children: ReactNode }) {
  return <main className="daily-workspace" onClick={revealLink}>
    <style>{`
      .daily-workspace { --workspace-line:#dce2e8; --workspace-muted:#536272; --workspace-reveal-gap:72px; font-family:system-ui,sans-serif; color:#182531; background:#f6f8fa; padding:clamp(12px,2.4vw,32px); line-height:1.5; overflow-wrap:anywhere; max-width:1680px; margin:auto; }
      .daily-workspace * { box-sizing:border-box; }
      .daily-workspace h1 { font-size:1.65rem; margin:0; letter-spacing:-.035em; }
      .daily-workspace h2 { font-size:1.1rem; margin:0 0 12px; }
      .daily-workspace h3 { font-size:1rem; }
      .daily-workspace p { margin:10px 0; }
      .daily-workspace a { color:#1b5b87; text-underline-offset:3px; }
      .daily-workspace button,.daily-workspace input,.daily-workspace select,.daily-workspace textarea { font:inherit; max-width:100%; }
      .daily-workspace button { border:1px solid #bac7d1; background:#fff; color:#173e57; border-radius:6px; padding:5px 10px; cursor:pointer; }
      .daily-workspace button:disabled { color:#65717b; cursor:default; background:#eef1f4; }
      .daily-workspace button:focus-visible,.daily-workspace a:focus-visible,.daily-workspace summary:focus-visible { outline:3px solid #71b9eb; outline-offset:3px; }
      .daily-workspace input:not([type=radio]):not([type=checkbox]),.daily-workspace select,.daily-workspace textarea { border:1px solid #bac7d1; border-radius:5px; padding:5px 7px; background:#fff; color:inherit; }
      .daily-workspace textarea { resize:vertical; min-height:76px; }
      .daily-workspace pre { white-space:pre-wrap; overflow-wrap:anywhere; max-width:100%; overflow-x:auto; font-size:.84rem; background:#f2f5f7; padding:10px; border-radius:5px; }
      .daily-workspace code,.daily-workspace dd { overflow-wrap:anywhere; }
      .daily-workspace dl { margin:8px 0; }
      .daily-workspace dt { font-size:.78rem; color:var(--workspace-muted); }
      .daily-workspace dd { margin:0 0 7px; }
      .daily-workspace table { display:block; overflow-x:auto; max-width:100%; border-collapse:collapse; }
      .daily-workspace th,.daily-workspace td { padding:7px; text-align:left; vertical-align:top; border:1px solid var(--workspace-line); }
      .daily-workspace summary { cursor:pointer; }
      .daily-workspace [id],.daily-workspace #conversation>div { scroll-margin-top:var(--workspace-reveal-gap); }
      .workspace-heading { display:flex; align-items:center; gap:16px; justify-content:space-between; margin-bottom:16px; }
      .workspace-heading p { color:var(--workspace-muted); margin:0; font-size:.88rem; }
      .workspace-nav { position:sticky; top:0; z-index:2; display:flex; flex-wrap:wrap; gap:8px 20px; padding:10px 0; background:#f6f8faf5; border-bottom:1px solid var(--workspace-line); margin-bottom:18px; font-size:.9rem; }
      .workspace-start-fields { display:flex; flex-wrap:wrap; align-items:end; gap:10px 18px; }
      .workspace-start-fields>* { min-width:0; max-width:100%; }
      .workspace-start-fields p { margin:0; }
      .workspace-primary { display:grid; grid-template-columns:minmax(0,1fr) minmax(0,1fr); gap:20px; align-items:start; }
      .workspace-primary-column { min-width:0; padding:18px; border:1px solid var(--workspace-line); border-radius:10px; background:#fff; }
      .workspace-primary-column>section { min-width:0; }
      .workspace-primary-column [aria-label="Workflow working context"] { background:#f1f6f9; border-left:3px solid #548eb2; padding:10px 12px; margin:12px 0; font-size:.85rem; }
      .workspace-primary-column [aria-label="Workflow working context"] details { margin:3px 0; }
      .workspace-primary-column [aria-label="Workflow drafts"] article { margin:14px 0; }
      .workspace-tools { margin-top:24px; }
      .workspace-tools>h2 { color:var(--workspace-muted); font-size:.9rem; }
      .workspace-disclosure { border:1px solid var(--workspace-line); border-radius:8px; background:#fff; margin:10px 0; }
      .workspace-disclosure>summary { padding:12px 16px; }
      .workspace-disclosure>summary span { display:inline; margin-left:12px; color:var(--workspace-muted); font-size:.82rem; }
      .workspace-disclosure-content { padding:4px 16px 16px; min-width:0; }
      .workspace-notices:empty { display:none; }
      .workspace-notices { margin:12px 0; }
      .workspace-notices [role=alert] { border-left:3px solid #b97b26; padding-left:10px; }
      @media (max-width:1000px) { .workspace-primary { grid-template-columns:minmax(0,1fr); } .workspace-heading { align-items:start; flex-direction:column; gap:3px; } }
      @media (max-width:560px) { .daily-workspace { --workspace-reveal-gap:116px; } .workspace-primary-column { padding:12px; } .workspace-disclosure>summary span { display:block; margin:3px 0 0 17px; } .workspace-nav { gap:6px 14px; font-size:.82rem; } }
    `}</style>
    {children}
  </main>;
}
