import { ReconstructionView } from "./ConnectorReconstruction";
/** Cold account inspection only. No source URI is opened or interpreted. */
export type RouteAvailability = { enabled: boolean; status: string; reason: string; detail?: string; projectReference?: string };
type Account = { answerOnly?:any; recordedAnswerAccount?:any; reconstruction?:any; draftSources?:any[]; interpretations?:any[]; formatVersion?:string; standing?:string; questionText?: string; gaps?: {gap:string;effect:string;responsible:string|{standing:string;identity:string|null}}[]; duties?: {duty:string;actor_role:string;standing:string;actor?:string;evidence?:string;reason?:string}[]; relativePath: string; accountId: string; bindingText: string; accountText: string; sourceCount: number; sections: {label: string; text: string}[] };
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
    <p>Discovery acquires candidate files before recognizing their format. Version-specific size checks do not bound total discovery allocation; exact known answer/base references use bounded reads.</p>
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
      {view.accounts?.map(account => account.formatVersion==="0.5" ? <AnswerOnlyAccount key={account.relativePath} account={account}/> : <article key={account.relativePath}>
        <h3>Recorded account: {account.accountId}</h3><p>{account.relativePath}</p>
        {account.formatVersion==="0.3" && <><h4>Source-evidence draft</h4><p>This is not a reconstructed answer. Facts and supported conclusions are empty; duty statuses and interpretation identities are unverified caller reports.</p><p>Compact receipt hashes do not reconstruct omitted objects or revive hot custody. Excerpts are recorded inclusion claims, not source bytes reverified at this read. The 1 MiB format limit is checked after identified bytes have been read; discovery does not promise bounded pre-read allocation.</p></>}
        {(account.formatVersion==="0.3"||account.formatVersion==="0.4") && <><h4>Recorded source evidence and excerpts</h4>{account.draftSources?.map(s=><div key={s.source_id}><p>{s.path}: {s.revision}; role {s.role} (caller assertion)</p><p>{s.provenance.side}; blob {s.provenance.blob}; content SHA-256 {s.sha256}; {s.provenance.verification}</p>{s.excerpts.map((e:any)=><div key={e.excerpt_id}><p>{e.anchor}: [{e.byte_start}, {e.byte_end}); {e.standing}</p><pre>{e.text}</pre></div>)}</div>)}<h4>Recorded unreviewed interpretations</h4>{account.interpretations?.map(i=><div key={i.interpretation_id}><p>{i.statement}</p><p>Asserted by: {i.asserted_by} ({i.attribution_standing}); {i.standing}</p><p>Source references: {i.source_ids.join(", ")}; excerpt references: {i.excerpt_ids.join(", ")}</p></div>)}</>}
        {account.formatVersion==="0.4"&&<ReconstructionView account={account.reconstruction??{}}/>}
        <h4>Recorded question</h4><p>{account.questionText ?? "Not recorded"}</p>
        <h4>Recorded gaps and responsibility</h4>
        {account.gaps?.map((gap,i)=><div key={i}><p>{gap.gap}</p><p>Effect: {gap.effect}</p><p>Responsible: {typeof gap.responsible==="string" ? gap.responsible : gap.responsible.standing==="unassigned" ? "Unassigned" : `${gap.responsible.identity} (caller assigned, unverified)`}</p></div>)}
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

function AnswerOnlyAccount({account}:{account:Account}){
 const e=account.answerOnly,a=account.recordedAnswerAccount;
 return <article><h3>Recorded answer-only account: {account.accountId}</h3><p>{account.relativePath}</p>
 <p>Cold recorded-content inspection only. Internally consistent receipt strings can be fabricated; no original authorship, admitted TASK emission, current permission, accepted answer or performed duty is authenticated.</p>
 <h4>Recorded question and exact base</h4><p>{a.question_id}: {e.baseQuestion.text}</p><p>{a.base_account.account_id}; {a.base_account.relative_path}; original SHA-256 {a.base_account.sha256}; {a.base_account.byte_length} bytes</p><p>{e.baseResolution}</p>
 <h4>Recorded answer</h4><p style={{whiteSpace:"pre-wrap"}}>{e.answer.answer_text}</p>
 {e.answer.claims.map((c:any)=><div key={c.claim_id}><p>{c.claim_id}: {c.statement}</p><p>Cited base claims: {c.base_claim_ids.join(", ")}; facts: {c.fact_ids.join(", ")}; comparisons: {c.comparison_ids.join(", ")}. Links do not prove entailment or quality.</p></div>)}
 <h4>Manager review and integration outstanding</h4><p>The selected subset records no review, plan, integration or integration attempt. Nothing is accepted or integrated by this read.</p>
 <h4>Explicit recorded gaps and responsibility</h4>{a.gaps.map((g:any,i:number)=><p key={i}>{g.gap}; effect: {g.effect}; responsibility: {g.responsibility}</p>)}
 <p>Carried base gap pointers: {e.answer.retained_gap_pointers.join(", ")}; contradiction IDs: {e.answer.retained_contradiction_ids.join(", ")}</p>
 <details><summary>Resolved base gaps and contradictions</summary><pre>{JSON.stringify({gaps:e.baseGaps,contradictions:e.baseContradictions},null,2)}</pre></details>
 <h4>Recorded known conflicts — no winner selected</h4>{!a.known_conflicts.length&&<p>None recorded; absence is not proved.</p>}{a.known_conflicts.map((c:any,i:number)=><p key={i}>{c.reference}; {c.sha256}; {c.effect}</p>)}
 <h4>Human responsibilities remain separate</h4><p>{a.human_responsibility.standing}: {a.human_responsibility.reason}; {a.human_responsibility.limit}</p>
 <h4>Recorded provenance, not authenticated origin</h4><p>Claimed role {a.answer.receipt.supplied_role}; recorded liveness {a.answer.receipt.liveness_at_recording}; recorder {a.recorder.identity}; time {a.written_at} ({a.written_at_source})</p>
 <details><summary>Recorded receipt identity strings and limits</summary><pre>{JSON.stringify(a.answer.receipt,null,2)}</pre></details>
 <p>{e.limit}. {a.cold_limit}</p><p>Generic discovery acquires candidate bytes before recognizing format0.5. Its 1 MiB cap is post-acquisition, not a total discovery allocation bound. Known exact0.5 references and the exact0.4 base use bounded reads; parsed structures still have overhead.</p>
 <details><summary>Exact embedded answer text as recorded</summary><pre>{a.answer.artifact.text}</pre></details>
 <details><summary>Original account text observed by the host</summary><pre>{e.rawAccountText}</pre></details>
 <details><summary>Cold-observed bindings, not publication proof</summary><pre>{account.bindingText}</pre><pre>{e.baseBindingText}</pre></details>
 </article>;
}
