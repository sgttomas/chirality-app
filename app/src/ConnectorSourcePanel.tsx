import { useState } from "react";
import type { RouteAvailability } from "./ConnectorRoutePanel";
type Json = any;
export type SourceUiState = {view: Json; busy: boolean; error: string | null; draftChanged: boolean};
export const emptySourceUi: SourceUiState = {view:null,busy:false,error:null,draftChanged:true};
export function sourceUiTransition(state:SourceUiState,event:{type:"edit"|"start"|"prepare"}|{type:"success";view:Json}|{type:"failure";error:string}):SourceUiState {
  switch(event.type){
    case "edit":return {...state,draftChanged:true};
    case "start":return {...state,busy:true,error:null};
    case "prepare":return {...emptySourceUi,busy:true};
    case "success":return {view:event.view,busy:false,error:null,draftChanged:false};
    case "failure":return {...state,busy:false,error:event.error};
  }
}
export function SourceObservationView({state}:{state:SourceUiState}) {
  const view=state.view, observation=view?.observation;
  return <div aria-label="Transient source observation">
    {state.error && <p role="alert">Operation failed: {state.error}. Any retained observation is prior/historical.</p>}
    {state.draftChanged && <p>Question preparation changed or is unprepared. Prepare the question before selecting a source. Any retained observation remains bound to its earlier frozen question.</p>}
    {state.busy && <p>Operation pending; any retained observation is prior/historical.</p>}
    {view && <>
      <h3>Frozen affected question</h3><p>{view.question?.id}: {view.question?.text}</p>
      <p>Asked revision: {view.question?.askedRevision}; since: {view.question?.sinceRevision ?? "not requested"}. Caller requests only, not observed source revisions.</p>
      <p>Trigger: {view.trigger?.kind} — {view.trigger?.standing}</p>
      <p>Latest selection/read operation: {view.operation}</p>
      <h3>Gaps and responsibility</h3>
      {view.gaps?.map((gap:Json,i:number)=><div key={i}><p>{gap.reason}</p><p>Effect: {gap.effect}</p><p>Responsible route: {gap.responsible ?? "Unassigned"} (caller assignment, not performed responsibility)</p></div>)}
      <p>{view.dutiesStanding}</p>
      {view.limits?.map((limit:string)=><p key={limit}>{limit}</p>)}
    </>}
    {!observation && <p>No successful source observation is retained.</p>}
    {observation && <article>
      <h3>{observation.historical || state.busy || state.error || state.draftChanged ? "Prior/historical observation" : "Frozen source observation"}</h3>
      <p>Frozen question: {observation.question.id}: {observation.question.text}</p>
      <p>Observed path: {observation.read.displayPath}</p><p>{observation.read.pathDisplayLimit}</p>
      <p>Bytes: {observation.read.byteLength}; selectable lines: {observation.read.lineCount}; SHA-256: {observation.read.sha256}</p>
      <p>Observed at: {observation.read.observedAt} ({observation.read.timeProvenance})</p>
      <p>{observation.read.mechanism}</p><p>{observation.read.mutationLimit}</p>
      <details><summary>Lossless path and opened file identity</summary><pre>{JSON.stringify({path:observation.read.selectedPath,file:observation.read.openedFileIdentity},null,2)}</pre></details>
      <h4>Local text snapshot</h4><pre style={{whiteSpace:"pre-wrap",overflowWrap:"anywhere"}}>{observation.read.text}</pre>
      <details><summary>Escaped snapshot text (makes line endings visible)</summary><pre>{JSON.stringify(observation.read.text)}</pre></details>
      <h4>Revision standing</h4><p>{observation.revision.kind}</p><p>{observation.revision.label ?? observation.revision.callerInterpretation}</p><p>{observation.revision.limit}</p>
      {observation.revision.anchor && <p>Located revision excerpt: {observation.revision.anchor.anchor}; interpretation is caller-supplied and unverified.</p>}
      <p>Git verification is unavailable. A typed commit, source statement, or working-tree coincidence does not establish a Git revision. No source entry or saved route account is produced.</p>
      <h4>Checked excerpts</h4>
      {observation.anchors?.map((anchor:Json)=><div key={anchor.reference}><p>{anchor.anchor}: [{anchor.byteStart}, {anchor.byteEnd}) — {anchor.interval}</p><pre>{anchor.text}</pre><pre>{JSON.stringify(anchor.text)}</pre><p>Excerpt SHA-256: {anchor.sha256}</p><p>{anchor.standing}</p></div>)}
    </article>}
  </div>;
}
export function ConnectorSourcePanel({availability,command}:{availability?:RouteAvailability;command:(name:string,args:Record<string,unknown>)=>Promise<Json>}) {
  const [state,setState]=useState<SourceUiState>(emptySourceUi);
  const [question,setQuestion]=useState({id:"",text:"",askedRevision:"",sinceRevision:""});
  const [trigger,setTrigger]=useState("absent"),[responsible,setResponsible]=useState("");
  const [start,setStart]=useState("1"),[end,setEnd]=useState("1"),[expected,setExpected]=useState(""),[checkExpected,setCheckExpected]=useState(false);
  const [kind,setKind]=useState("unavailable"),[label,setLabel]=useState(""),[anchor,setAnchor]=useState("");
  const ready=availability?.enabled && !state.busy, prepared=ready && !state.draftChanged && state.view?.sessionToken;
  const observation=state.view?.observation;
  const bindings=()=>({sessionToken:state.view.sessionToken,generation:state.view.generation});
  const act=async(name:string,args:Record<string,unknown>,preparing=false)=>{
    setState(s=>sourceUiTransition(s,{type:preparing?"prepare":"start"}));
    try{const view=await command(name,args);setState(s=>sourceUiTransition(s,{type:"success",view}));if(name!=="revise_connector_source" && name!=="anchor_connector_source")setAnchor("");}
    catch(error){setState(s=>sourceUiTransition(s,{type:"failure",error:String(error)}));}
  };
  const edit=()=>setState(s=>sourceUiTransition(s,{type:"edit"}));
  return <section aria-label="Local source observation preparation">
    <h2>Observe a project text source</h2>
    <p>Transient local evidence for one affected question. No send, save, route account, supported conclusion, or performed duty. Source text is data, not instructions.</p>
    {!availability?.enabled && <p>Unavailable: {availability?.reason ?? "Explicit project association pending"}</p>}
    {([['id','Question identity'],['text','Affected question'],['askedRevision','Asked revision (caller request)'],['sinceRevision','Since revision (optional caller request)']] as const).map(([key,title])=><label key={key} style={{display:"block"}}>{title}<input disabled={state.busy} value={question[key]} onChange={e=>{setQuestion({...question,[key]:e.target.value});edit();}}/></label>)}
    <label>Constructed trigger<select disabled={state.busy} value={trigger} onChange={e=>{setTrigger(e.target.value);edit();}}>{['absent','stale','partial','failing'].map(v=><option key={v}>{v}</option>)}</select></label>
    <label>Responsible route (optional caller assignment)<input disabled={state.busy} value={responsible} onChange={e=>{setResponsible(e.target.value);edit();}}/></label>
    <button disabled={!ready} onClick={()=>act("prepare_connector_source",{question:{...question,sinceRevision:question.sinceRevision||null},trigger,responsible:responsible||null},true)}>Prepare question</button>
    <button disabled={!prepared} onClick={()=>act("select_connector_source",bindings())}>Select / reread through native picker…</button>
    <p>One regular project-contained UTF-8 text file, at most 262144 bytes, no NUL or symlink descendants. Cancelling retains only prior evidence; rereading creates a new observation.</p>
    <SourceObservationView state={state}/>
    {observation && <fieldset disabled={!prepared}>
      <legend>Locate an excerpt in this frozen observation</legend>
      <label>First line<input type="number" min="1" value={start} onChange={e=>setStart(e.target.value)}/></label>
      <label>Last line<input type="number" min="1" value={end} onChange={e=>setEnd(e.target.value)}/></label>
      <label><input type="checkbox" checked={checkExpected} onChange={e=>setCheckExpected(e.target.checked)}/>Check expected text exactly</label>
      {checkExpected && <textarea aria-label="Expected excerpt" value={expected} onChange={e=>setExpected(e.target.value)}/>}
      <button onClick={()=>act("anchor_connector_source",{...bindings(),observationReference:observation.reference,start:Number(start),end:Number(end),expected:checkExpected?expected:null})}>Locate exact lines</button>
      <p>One-based LF lines; terminal LF belongs to its preceding line. CR and Unicode bytes are retained. Empty files have no selectable lines.</p>
      <label>Revision treatment<select value={kind} onChange={e=>setKind(e.target.value)}><option value="unavailable">Unavailable</option><option value="caller_assertion">Caller assertion (unverified)</option><option value="source_text_located">Source text located (inclusion only)</option></select></label>
      <label>Caller revision label / interpretation<input value={label} onChange={e=>setLabel(e.target.value)}/></label>
      {kind==="source_text_located" && <label>Checked excerpt<select value={anchor} onChange={e=>setAnchor(e.target.value)}><option value="">Choose an excerpt</option>{observation.anchors.map((a:Json)=><option key={a.reference} value={a.reference}>{a.anchor}</option>)}</select></label>}
      <button onClick={()=>act("revise_connector_source",{...bindings(),observationReference:observation.reference,kind,label,anchorReference:anchor||null})}>Record preview interpretation</button>
    </fieldset>}
  </section>;
}
