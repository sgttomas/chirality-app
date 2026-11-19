import { useEffect, useRef, useState, type CSSProperties, type KeyboardEvent, type PointerEvent, type ReactNode } from "react";

type Json = any;

/** The right panel's tabs: the App's views other than the conversation, in this order, each with the element a
 * person lands on when they select it. */
export const RIGHT_PANEL_TABS = [
  { id: "run", label: "Run a workflow", target: "view-run" },
  { id: "make", label: "Make a workflow", target: "view-make" },
  { id: "history", label: "History", target: "workspace-history" },
  { id: "settings", label: "Settings & tools", target: "workspace-tools" },
] as const;
export type RightPanelTab = typeof RIGHT_PANEL_TABS[number]["id"];
/** How a tab was selected: pressed, or reached by the arrow keys while moving along the tabs. */
export type TabSelection = "press" | "keys";
export const isRightPanelTab = (view: string): view is RightPanelTab => RIGHT_PANEL_TABS.some(tab => tab.id === view);

/** What the status strip says for the conversation shown in the centre. */
export type TurnPhase = "working" | "waiting" | "idle" | null;
/** From that conversation's thread row: a request waiting for the person's answer first, then Codex's status type.
 * Anything else, or no conversation, says nothing. */
export function turnPhase(row: Json | null | undefined, waitingForAnswer: boolean): TurnPhase {
  if (!row) return null;
  if (waitingForAnswer) return "waiting";
  const type = row?.status?.type;
  return type === "active" ? "working" : type === "idle" ? "idle" : null;
}
const PHASE_WORDS: Record<Exclude<TurnPhase, null>, string> = { working: "Working", waiting: "Waiting for you", idle: "Idle" };

export function ActivityStrip({ phase }: { phase: TurnPhase }) {
  return <div className="woven-activity-strip" aria-label="Activity status" data-turn-phase={phase ?? undefined}>
    <span role="status">{phase ? PHASE_WORDS[phase] : ""}</span>
  </div>;
}

/** The right region's frame: the tab strip, the panel's own controls, and the selected view. Every view stays
 * mounted; the App hides the ones not selected. */
export function RightPanel({ tab, onTab, expanded, onExpand, onClose, hidden, children }: {
  /** `onExpand` is null where widening the panel would change nothing (the regions are stacked). */
  tab: RightPanelTab; onTab: (tab: RightPanelTab, by: TabSelection) => void; expanded: boolean; onExpand: (() => void) | null; onClose: () => void; hidden: boolean; children: ReactNode;
}) {
  const tabsRef = useRef<HTMLDivElement>(null);
  const keyDown = (event: KeyboardEvent<HTMLDivElement>) => {
    if (!["ArrowLeft", "ArrowRight", "Home", "End"].includes(event.key)) return;
    event.preventDefault();
    const ids = RIGHT_PANEL_TABS.map(t => t.id);
    const index = Math.max(0, ids.indexOf(tab));
    const next = event.key === "Home" ? ids[0] : event.key === "End" ? ids[ids.length - 1] : ids[(index + (event.key === "ArrowRight" ? 1 : ids.length - 1)) % ids.length];
    onTab(next, "keys");
    (tabsRef.current?.querySelector?.(`[data-view="${next}"]`) as HTMLElement | null)?.focus?.();
  };
  return <section className="woven-right-panel" aria-label="Right panel" hidden={hidden}>
    <header className="woven-region-header woven-right-panel-header workflows-header">
      <div ref={tabsRef} className="workflows-tabs" role="tablist" aria-label="Right panel views" onKeyDown={keyDown}>
        {RIGHT_PANEL_TABS.map(t => <button key={t.id} type="button" role="tab" id={`right-tab-${t.id}`} data-view={t.id} aria-controls="right-view-content"
          aria-selected={tab === t.id} tabIndex={tab === t.id ? 0 : -1} onClick={() => onTab(t.id, "press")}>{t.label}</button>)}
      </div>
      <div className="woven-right-panel-controls">
        {onExpand ? <button type="button" aria-label={expanded ? "Return panel" : "Expand panel"} title={expanded ? "Return panel" : "Expand panel"} aria-pressed={expanded} onClick={onExpand}>{expanded ? "⤡" : "⤢"}</button> : null}
        <button type="button" aria-label="Collapse right panel" onClick={onClose}>×</button>
      </div>
    </header>
    <div id="right-view-content" role="tabpanel" aria-labelledby={`right-tab-${tab}`} style={{ minHeight: 0, flex: 1, overflow: "auto" }}>
      {children}
    </div>
  </section>;
}

const clamp = (value: number, minimum: number, maximum: number) => Math.max(minimum, Math.min(maximum, value));
/** Region widths, in pixels: the navigator's range and starting width, the right region's narrowest and starting
 * width, a collapsed region's width, and the window width below which the regions stack. */
export const NAVIGATOR_MIN = 220, NAVIGATOR_MAX = 360, NAVIGATOR_DEFAULT = 292;
export const RIGHT_MIN = 280, RIGHT_DEFAULT = 480, COLLAPSED = 56, STACK_BELOW = 960;

/** The grid's widths for an available width and the layout state; null columns when the regions stack. */
export function shellLayout(available: number, s: { navigatorWidth: number; navigatorCollapsed: boolean; rightWidth: number; rightCollapsed: boolean; rightExpanded: boolean }) {
  const stacked = available < STACK_BELOW;
  const left = s.navigatorCollapsed ? COLLAPSED : Math.min(clamp(s.navigatorWidth, NAVIGATOR_MIN, NAVIGATOR_MAX), Math.max(NAVIGATOR_MIN, available - 724));
  const expandedWidth = Math.round(available * 0.6 / 8) * 8;
  const right = Math.max(RIGHT_MIN, Math.min(s.rightExpanded ? expandedWidth : s.rightWidth, available - left - 444));
  const rightMax = Math.max(RIGHT_MIN, Math.min(expandedWidth, available - (s.navigatorCollapsed ? COLLAPSED : clamp(s.navigatorWidth, NAVIGATOR_MIN, NAVIGATOR_MAX)) - 444));
  const visibleRight = s.rightCollapsed ? COLLAPSED : right;
  return { stacked, left, right, rightMax, columns: stacked ? null : `${left}px 12px minmax(420px, 1fr) 12px ${visibleRight}px` };
}

/**
 * The three regions over the status strip: the navigator on the left, the conversation in the centre, the right
 * panel. Widths, collapse and expansion live in memory for this session only. The right region's collapse is the
 * App's, since a reveal in one of its views opens it.
 */
export function WorkspaceShell({ hidden, navigator, collapsedNavigator, centre, rightTab, onRightTab, rightCollapsed, setRightCollapsed, right, strip }: {
  hidden: boolean; navigator: ReactNode; collapsedNavigator: (openNavigator: () => void) => ReactNode; centre: ReactNode;
  rightTab: RightPanelTab; onRightTab: (tab: RightPanelTab, by: TabSelection) => void; rightCollapsed: boolean; setRightCollapsed: (collapsed: boolean) => void;
  right: ReactNode; strip: ReactNode;
}) {
  const [available, setAvailable] = useState(1440);
  const [navigatorWidth, setNavigatorWidth] = useState(NAVIGATOR_DEFAULT);
  const [navigatorCollapsed, setNavigatorCollapsed] = useState(false);
  const [rightWidth, setRightWidth] = useState(RIGHT_DEFAULT);
  // Expanding widens the right region and collapses the navigator; returning restores both.
  const [expanded, setExpanded] = useState<{ navigatorCollapsed: boolean } | null>(null);
  const workspace = useRef<HTMLElement | null>(null);
  const drag = useRef<{ target: "navigator" | "right"; startX: number; startValue: number } | null>(null);
  useEffect(() => {
    const element = workspace.current;
    if (!element || typeof ResizeObserver === "undefined") return;
    const observer = new ResizeObserver(entries => { const width = entries[0]?.contentRect.width; if (width) setAvailable(width); });
    observer.observe(element);
    return () => observer.disconnect();
  }, []);
  const layout = shellLayout(available, { navigatorWidth, navigatorCollapsed, rightWidth, rightCollapsed, rightExpanded: expanded !== null });
  const restoreExpanded = () => {
    if (!expanded) return;
    setNavigatorCollapsed(expanded.navigatorCollapsed);
    setExpanded(null);
  };
  const toggleExpanded = () => {
    if (expanded) { restoreExpanded(); return; }
    setExpanded({ navigatorCollapsed });
    setNavigatorCollapsed(true);
    setRightCollapsed(false);
  };
  const resizeTo = (target: "navigator" | "right", value: number, collapse = false) => {
    if (target === "navigator") { setNavigatorWidth(clamp(value, NAVIGATOR_MIN, NAVIGATOR_MAX)); setNavigatorCollapsed(collapse); }
    else { setRightWidth(clamp(value, RIGHT_MIN, layout.rightMax)); setRightCollapsed(collapse); }
  };
  useEffect(() => {
    if (typeof window === "undefined" || typeof window.addEventListener !== "function") return;
    const move = (event: globalThis.PointerEvent) => {
      const d = drag.current;
      if (!d) return;
      resizeTo(d.target, d.target === "navigator" ? d.startValue + event.clientX - d.startX : d.startValue - event.clientX + d.startX);
    };
    const up = () => { drag.current = null; };
    window.addEventListener("pointermove", move);
    window.addEventListener("pointerup", up);
    window.addEventListener("pointercancel", up);
    return () => { window.removeEventListener("pointermove", move); window.removeEventListener("pointerup", up); window.removeEventListener("pointercancel", up); };
  });
  const beginDrag = (event: PointerEvent<HTMLDivElement>, target: "navigator" | "right") => {
    if (event.button !== 0) return;
    event.preventDefault();
    if (target === "right") restoreExpanded();
    drag.current = { target, startX: event.clientX, startValue: target === "navigator" ? clamp(navigatorWidth, NAVIGATOR_MIN, NAVIGATOR_MAX) : layout.right };
  };
  const resizeByKey = (event: KeyboardEvent<HTMLDivElement>, target: "navigator" | "right") => {
    if (!["ArrowLeft", "ArrowRight", "Home", "End"].includes(event.key)) return;
    event.preventDefault();
    const step = event.shiftKey ? 40 : 16;
    if (target === "navigator") {
      const now = clamp(navigatorWidth, NAVIGATOR_MIN, NAVIGATOR_MAX);
      resizeTo("navigator", event.key === "Home" ? NAVIGATOR_MIN : event.key === "End" ? NAVIGATOR_MAX : now + (event.key === "ArrowRight" ? step : -step), event.key === "Home");
    } else {
      restoreExpanded();
      resizeTo("right", event.key === "Home" ? RIGHT_MIN : event.key === "End" ? layout.rightMax : layout.right + (event.key === "ArrowLeft" ? step : -step), event.key === "Home");
    }
  };
  const selectTab = (tab: RightPanelTab, by: TabSelection) => { restoreExpanded(); onRightTab(tab, by); };
  const style = { ...(layout.columns ? { gridTemplateColumns: layout.columns } : {}), "--woven-activity-height": "32px" } as CSSProperties;
  const openNavigator = () => setNavigatorCollapsed(false);
  return <section ref={workspace} className={`woven-workspace woven-t3-workspace${layout.stacked ? " is-stacked" : ""}`} style={style} hidden={hidden}>
    <div className={`woven-region woven-region--navigator${navigatorCollapsed ? " is-collapsed" : ""}`}>
      <button type="button" className="woven-region-toggle button-muted" aria-label={navigatorCollapsed ? "Open Navigator" : "Close Navigator"} onClick={() => setNavigatorCollapsed(!navigatorCollapsed)}>
        {navigatorCollapsed ? <span className="woven-collapsed-brand" aria-hidden="true">C</span> : <span aria-hidden="true">‹</span>}
      </button>
      {navigatorCollapsed ? collapsedNavigator(openNavigator) : navigator}
    </div>
    {/* The regions are placed by the grid, not by their order here. The navigator comes first in the page so that
        reading and tab order follow what is seen left to right, and the page's first heading is the workspace's own. */}
    <section className="woven-dialogue-region" aria-label="Conversation">{centre}</section>
    <div className="woven-resize-handle woven-resize-handle--vertical woven-resize-handle--navigator" role="separator" tabIndex={0} aria-label="Resize Navigator" aria-orientation="vertical"
      aria-valuemin={NAVIGATOR_MIN} aria-valuemax={NAVIGATOR_MAX} aria-valuenow={clamp(navigatorWidth, NAVIGATOR_MIN, NAVIGATOR_MAX)}
      onPointerDown={event => beginDrag(event, "navigator")} onKeyDown={event => resizeByKey(event, "navigator")}/>
    <div className="woven-resize-handle woven-resize-handle--vertical woven-resize-handle--coordination" role="separator" tabIndex={0} aria-label="Resize right panel" aria-orientation="vertical"
      aria-valuemin={RIGHT_MIN} aria-valuemax={layout.rightMax} aria-valuenow={layout.right}
      onPointerDown={event => beginDrag(event, "right")} onKeyDown={event => resizeByKey(event, "right")}/>
    <aside className={`woven-region woven-region--coordination${rightCollapsed ? " is-collapsed" : ""}`}>
      {rightCollapsed ? <button type="button" className="woven-region-toggle button-muted" aria-label="Open right panel" onClick={() => setRightCollapsed(false)}>›</button> : null}
      <RightPanel tab={rightTab} onTab={selectTab} expanded={expanded !== null} onExpand={layout.stacked && expanded === null ? null : toggleExpanded} onClose={() => { restoreExpanded(); setRightCollapsed(true); }} hidden={rightCollapsed}>{right}</RightPanel>
      {rightCollapsed ? <span className="woven-collapsed-label">{RIGHT_PANEL_TABS.find(t => t.id === rightTab)?.label}</span> : null}
    </aside>
    {strip}
  </section>;
}
