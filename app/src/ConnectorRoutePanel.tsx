/** Cold account inspection only. No source URI is opened or interpreted. */
export type RouteAvailability = { enabled: boolean; status: string; reason: string; detail?: string; projectReference?: string };
type Account = { questionText?: string; gaps?: {gap:string;effect:string;responsible:string}[]; duties?: {duty:string;actor_role:string;standing:string;actor?:string;evidence?:string;reason?:string}[]; relativePath: string; accountId: string; bindingText: string; accountText: string; sourceCount: number; sections: {label: string; text: string}[] };
export type RouteView = {
  status: string; availability?: RouteAvailability; error?: unknown;
  projectDisplay?: string; projectIdentityText?: string; directoryAbsent?: boolean; enumerationComplete?: boolean;
  accounts?: Account[]; issues?: {relative_path: string; kind: string; detail: string}[]; byAccountId?: Record<string, string[]>;
};
export type RouteReadState = { busy: boolean; view: RouteView | null; error: string | null };
export const emptyRouteRead: RouteReadState = { busy: false, view: null, error: null };
export function routeReadTransition(state: RouteReadState, event: {type: "start" | "clear"} | {type: "success"; view: RouteView} | {type: "failure"; error: string}): RouteReadState {
  switch (event.type) {
    case "start": return {busy: true, view: null, error: null};
    case "clear": return emptyRouteRead;
    case "success": return {busy: false, view: event.view, error: null};
    case "failure": return {busy: false, view: null, error: event.error};
  }
}
export function ConnectorRoutePanel({availability, state, onRead}: {availability?: RouteAvailability; state: RouteReadState; onRead: () => void}) {
  const view = state.view;
  return <section aria-label="Recorded connector route accounts">
    <h2>Recorded connector route accounts</h2>
    <p>Read-only inspection of accounts in the explicit App project. All account contents are recorded claims. Schema validity and matching hashes do not establish source truth, successful publication, or performed duties.</p>
    <button disabled={!availability?.enabled || state.busy} onClick={onRead}>{state.busy ? "Reading accounts…" : "Read / refresh accounts"}</button>
    {!availability?.enabled && <p>Unavailable: {availability?.status ?? "project association pending"}. {availability?.reason} {availability?.detail}</p>}
    {state.error && <p role="alert">Read failed: {state.error}. Previous results have been cleared.</p>}
    {!view && !state.busy && !state.error && <p>No account observation loaded.</p>}
    {view?.status === "unavailable" && <p>Unavailable: {view.availability?.status}. {view.availability?.reason} {view.availability?.detail}</p>}
    {view?.status === "project_open_failed" && <><p role="alert">The associated project could not be opened.</p><pre>{JSON.stringify(view.error, null, 2)}</pre></>}
    {view?.status === "observed" && <>
      <p>Observed project: {view.projectDisplay}</p>
      <details><summary>Lossless project identity</summary><pre>{view.projectIdentityText}</pre></details>
      <p>Cold observation at this read only; no continuously current pathname guarantee. These bindings were discovered, not resolved against a separately held prior reference. No source files or cited anchors were read by this view.</p>
      {view.directoryAbsent && <p>The canonical account directory is absent. Nothing was created.</p>}
      {!view.enumerationComplete && <p role="alert">Enumeration is incomplete. Displayed accounts are only the observed subset; missing results do not mean no accounts or no work.</p>}
      {!view.directoryAbsent && view.enumerationComplete && !view.accounts?.length && <p>No valid accounts were observed in the existing directory. Inspect discovery issues below.</p>}
      <h3>Discovery issues</h3>
      {!view.issues?.length && <p>No discovery issues reported by this read.</p>}
      {view.issues?.map((issue, i) => <div key={i}><strong>{issue.kind}</strong><pre>{issue.relative_path}</pre><p>{issue.detail}</p></div>)}
      {Object.entries(view.byAccountId ?? {}).filter(([, paths]) => paths.length > 1).map(([id, paths]) => <div key={id} role="alert"><p>Duplicate recorded account ID: {id}. No winner selected.</p><pre>{paths.join("\n")}</pre></div>)}
      {view.accounts?.map(account => <article key={account.relativePath}>
        <h3>Recorded account: {account.accountId}</h3><p>{account.relativePath}</p>
        <h4>Recorded question</h4><p>{account.questionText ?? "Not recorded"}</p>
        <h4>Recorded gaps and responsibility</h4>
        {account.gaps?.map((gap,i)=><div key={i}><p>{gap.gap}</p><p>Effect: {gap.effect}</p><p>Responsible: {gap.responsible}</p></div>)}
        <h4>Recorded duties</h4>
        {account.duties?.map((duty,i)=><div key={i}><p>{duty.duty}: {duty.standing} ({duty.actor_role})</p><p>Actor: {duty.actor ?? "Not recorded"}</p><p>Evidence: {duty.evidence ?? "Not recorded"}</p><p>{duty.reason ?? "Reason not recorded"}</p></div>)}
        {account.sourceCount === 0 && <p>No sources are recorded. This account does not establish an answer reconstructed from files.</p>}
        <p>Duties, actors, evidence, and time below are as recorded; inspection does not perform or independently verify them. Missing metadata remains missing. Source paths and anchors are literal citations only.</p>
        <p>Account fields below are the host’s parsed JSON representation, not original file bytes. Parsing and serialization normalize formatting and may round large integers or high-precision decimals. Text display avoids further JavaScript number conversion; it cannot recover precision already lost by the host parser.</p>
        {account.sections.map(section => <details key={section.label}><summary>{section.label} — host-parsed fields</summary><pre style={{whiteSpace: "pre-wrap", overflowWrap: "anywhere"}}>{section.text}</pre></details>)}
        <details><summary>Full host-parsed account</summary><pre>{account.accountText}</pre></details>
        <details><summary>Cold-observed binding (not publication or prior-reference resolution proof)</summary><p>The binding hash identifies bytes observed by the host. This display does not verify those bytes or certify the precision of the parsed account representation.</p><pre>{account.bindingText}</pre></details>
      </article>)}
    </>}
  </section>;
}
