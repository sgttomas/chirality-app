import { useEffect, useRef, useState } from "react";
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
      {view.gaps?.map((gap:Json,i:number)=><div key={i}>{gap.kind && <h4>{gap.kind} gap</h4>}<p>{gap.reason}</p><p>Effect: {gap.effect}</p><p>Responsible route: {gap.responsible ?? "Unassigned"} (caller assignment, not performed responsibility)</p></div>)}
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
      <p>This local snapshot is not a Git binding. A typed commit, source statement, or working-tree coincidence does not establish a Git revision. No source entry or saved route account is produced.</p>
      <h4>Checked excerpts</h4>
      {observation.anchors?.map((anchor:Json)=><div key={anchor.reference}><p>{anchor.anchor}: [{anchor.byteStart}, {anchor.byteEnd}) — {anchor.interval}</p><pre>{anchor.text}</pre><pre>{JSON.stringify(anchor.text)}</pre><p>Excerpt SHA-256: {anchor.sha256}</p><p>{anchor.standing}</p></div>)}
    </article>}
    <p>Git gap responsibility: {view?.gaps?.[0]?.responsible ?? "Unassigned"}; caller assignment only, no performed responsibility.</p>
    <GitObservationView git={view?.git} historical={state.busy || !!state.error || state.draftChanged}/>
  </div>;
}
export function GitObservationView({git,historical=false}:{git:Json;historical?:boolean}) {
  if(!git)return null;
  const result=git.result, observation=result?.observation;
  return <section aria-label="Separate Git object observations">
    <h3>Git object evidence</h3><p>Operation: {git.operation}</p>
    {git.error && <p role="alert">Git request gap: {git.error}. No new result from this failed or cancelled request.</p>}
    {!result && <p>No Git object result is retained.</p>}
    {result && <>
      <h4>{result.historical || historical ? "Prior/historical Git result" : "Frozen Git result"}: {observation.status}</h4>
      <p>Requested at: {observation.request?.at}; since: {observation.request?.since ?? "not requested"}.</p>
      <p>Local preview stays separate. This result concerns exact requested commits and stored object bytes.</p>
      {(["at","since"] as const).map(side=>observation[side] && <article key={side}>
        <h4>{side === "at" ? "At requested commit" : "Since requested commit"}: {observation[side].status}</h4>
        {observation[side].status === "gap" ? <p>{observation[side].kind}: {observation[side].reason}. This side has no verified text.</p> : <>
          <p>Commit: {observation[side].object.readCommit}</p><p>Blob: {observation[side].object.blob}</p>
          <p>Content SHA-256: {observation[side].object.sha256}; bytes: {observation[side].object.byteLength}</p>
          <p>Observed: {observation[side].object.observedAt} ({observation[side].object.timeProvenance})</p>
          <p>{observation[side].object.standing}</p>
          <pre style={{whiteSpace:"pre-wrap",overflowWrap:"anywhere"}}>{observation[side].object.text}</pre>
          <details><summary>Object path, raw commit and tree evidence</summary><pre>{JSON.stringify(observation[side].object,null,2)}</pre></details>
        </>}
      </article>)}
      {observation.comparison && <p>{observation.comparison}</p>}
      {observation.limits?.map((limit:string)=><p key={limit}>{limit}</p>)}
      <details><summary>Repository association and restricted Git mechanism</summary><pre>{JSON.stringify({association:observation.association,engine:observation.engine},null,2)}</pre></details>
      <h4>Checked Git excerpts</h4>
      {result.anchors?.map((a:Json)=><div key={a.reference}><p>{a.side}: {a.anchor}, [{a.byteStart}, {a.byteEnd})</p><p>Commit: {a.commit}; blob: {a.blob}</p><pre>{a.text}</pre><p>{a.standing}</p></div>)}
    </>}
  </section>;
}
export function ConnectorSourcePanel({availability,command}:{availability?:RouteAvailability;command:(name:string,args:Record<string,unknown>)=>Promise<Json>}) {
  const [state,setState]=useState<SourceUiState>(emptySourceUi);
  const [question,setQuestion]=useState({id:"",text:"",askedRevision:"",sinceRevision:""});
  const [trigger,setTrigger]=useState("absent"),[responsible,setResponsible]=useState("");
  const [start,setStart]=useState("1"),[end,setEnd]=useState("1"),[expected,setExpected]=useState(""),[checkExpected,setCheckExpected]=useState(false);
  const [kind,setKind]=useState("unavailable"),[label,setLabel]=useState(""),[anchor,setAnchor]=useState("");
  const [gitAt,setGitAt]=useState(""),[gitSince,setGitSince]=useState(""),[gitSide,setGitSide]=useState("at");
  const [gitPending,setGitPending]=useState(false);
  const gitRequest=useRef(0);
  const ready=availability?.enabled && !state.busy, prepared=ready && !state.draftChanged && state.view?.sessionToken;
  const observation=state.view?.observation;
  const bindings=()=>({sessionToken:state.view.sessionToken,generation:state.view.generation});
  const act=async(name:string,args:Record<string,unknown>,preparing=false)=>{
    setState(s=>sourceUiTransition(s,{type:preparing?"prepare":"start"}));
    try{const view=await command(name,args);setState(s=>sourceUiTransition(s,{type:"success",view}));if(name!=="revise_connector_source" && name!=="anchor_connector_source")setAnchor("");}
    catch(error){setState(s=>sourceUiTransition(s,{type:"failure",error:String(error)}));}
  };
  const readGit=async()=>{
    const request=++gitRequest.current;setGitPending(true);setState(s=>sourceUiTransition(s,{type:"start"}));
    try{const view=await command("read_connector_git",{...bindings(),observationReference:observation.reference,at:gitAt,since:gitSince||null});if(request===gitRequest.current)setState(s=>sourceUiTransition(s,{type:"success",view}));}
    catch(error){if(request===gitRequest.current)setState(s=>sourceUiTransition(s,{type:"failure",error:String(error)}));}
    finally{if(request===gitRequest.current)setGitPending(false);}
  };
  const cancelGit=async()=>{
    const request=++gitRequest.current;setGitPending(false);
    try{const view=await command("cancel_connector_git",bindings());if(request===gitRequest.current)setState(s=>sourceUiTransition(s,{type:"success",view}));}
    catch(error){if(request===gitRequest.current)setState(s=>sourceUiTransition(s,{type:"failure",error:String(error)}));}
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
    <fieldset disabled={!prepared || state.view?.operation!=="observed"}>
      <legend>Inspect exact Git commits for the selected source path</legend>
      <p>Lowercase full commit IDs only (40 or 64 hex characters). No branch, tag, path or repository input. The local preview remains separate from committed bytes.</p>
      <label>At commit<input value={gitAt} onChange={e=>setGitAt(e.target.value)}/></label>
      <label>Since commit (optional)<input value={gitSince} onChange={e=>setGitSince(e.target.value)}/></label>
      <button onClick={readGit}>Read Git objects</button>
    </fieldset>
    {gitPending && <button onClick={cancelGit}>Cancel Git request</button>}
    {state.view?.git?.result && <fieldset disabled={!prepared}>
      <legend>Locate exact lines in a Git side</legend>
      <label>Git side<select value={gitSide} onChange={e=>setGitSide(e.target.value)}><option value="at">At</option><option value="since">Since</option></select></label>
      <label>First line<input type="number" min="1" value={start} onChange={e=>setStart(e.target.value)}/></label>
      <label>Last line<input type="number" min="1" value={end} onChange={e=>setEnd(e.target.value)}/></label>
      <label><input type="checkbox" checked={checkExpected} onChange={e=>setCheckExpected(e.target.checked)}/>Check expected text exactly</label>
      {checkExpected && <textarea aria-label="Expected Git excerpt" value={expected} onChange={e=>setExpected(e.target.value)}/>}
      <button onClick={()=>act("anchor_connector_git",{...bindings(),observationReference:state.view.git.result.reference,side:gitSide,start:Number(start),end:Number(end),expected:checkExpected?expected:null})}>Locate exact Git lines</button>
    </fieldset>}
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
    <ConnectorDraftPanel source={state} availability={availability} command={command}/>
  </section>;
}
export function acceptDraftReply(previous:Json,next:Json){return !previous||BigInt(next.revision??"0")>=BigInt(previous.revision??"0")?next:previous;}
export function ConnectorDraftPanel({source,availability,command}:{source:SourceUiState;availability?:RouteAvailability;command:(name:string,args:Record<string,unknown>)=>Promise<Json>}){
 const [registry,setRegistry]=useState<Json>(null),[error,setError]=useState<string|null>(null),[busy,setBusy]=useState(false),[dirty,setDirty]=useState(true);
 const [connector,setConnector]=useState("");
 const [choices,setChoices]=useState<Record<string,{selected:boolean;role:string;anchors:string[]}>>({});
 const [statement,setStatement]=useState(""),[assertedBy,setAssertedBy]=useState(""),[linkEvidence,setLinkEvidence]=useState(false);
 const [gap,setGap]=useState(""),[effect,setEffect]=useState(""),[assigned,setAssigned]=useState(false),[responsible,setResponsible]=useState("");
 const [unsupported,setUnsupported]=useState(""),[unsupportedWhy,setUnsupportedWhy]=useState("");
 const [duties,setDuties]=useState<Record<string,{standing:string;reason:string}>>({locate_compare:{standing:"",reason:""},review_integrate:{standing:"",reason:""},cross_undertaking_coordination:{standing:"",reason:""}});
 const prepared=registry?.entries?.find((e:Json)=>e.status==="prepared"),result=source.view?.git?.result;
 const eligible=availability?.enabled&&!source.busy&&!source.error&&!source.draftChanged&&source.view?.operation==="observed"&&source.view?.git?.operation==="completed"&&!result?.historical;
 const action=async(name:string,args:Record<string,unknown>,preparing=false)=>{setBusy(true);setError(null);try{const next=await command(name,args);setRegistry((old:Json)=>acceptDraftReply(old,next));if(preparing)setDirty(false);}catch(e){setError(String(e));}finally{setBusy(false);}};
 const invalidate=()=>{setDirty(true);if(prepared)void action("cancel_connector_draft",{token:prepared.token,generation:prepared.generation});};
 useEffect(()=>{if(prepared&&!eligible)void action("cancel_connector_draft",{token:prepared.token,generation:prepared.generation});},[eligible,source.view?.generation,source.view?.git?.result?.reference,prepared?.token]);
 useEffect(()=>{setChoices({});setDirty(true);if(prepared)void action("cancel_connector_draft",{token:prepared.token,generation:prepared.generation});},[result?.reference,source.view?.generation]);
 const choose=(reference:string,change:Partial<{selected:boolean;role:string;anchors:string[]}>)=>{invalidate();setChoices(old=>({...old,[reference]:{...(old[reference]??{selected:false,role:"",anchors:[]}),...change}}));};
 const prepare=()=>{const selected=Object.entries(choices).filter(([,c])=>c.selected),references=selected.map(([ref])=>ref),anchors=selected.flatMap(([,c])=>c.anchors);return action("prepare_connector_draft",{input:{sessionToken:source.view.sessionToken,generation:source.view.generation,gitReference:result.reference,connector,sources:selected.map(([reference,c])=>({reference,role:c.role,anchors:c.anchors})),interpretations:statement?[{statement,assertedBy,sourceReferences:linkEvidence?references:[],anchorReferences:linkEvidence?anchors:[]}]:[],gaps:gap?[{gap,effect,responsible:{standing:assigned?"caller_assigned":"unassigned",identity:assigned?responsible:null}}]:[],unsupported:unsupported?[{conclusion:unsupported,why:unsupportedWhy}]:[],duties:Object.entries(duties).map(([duty,value])=>({duty,...value}))}},true);};
 return <section aria-label="Source evidence draft materialization">
 <h2>Prepare a source-evidence draft</h2><p>Evidence and separately attributed interpretations only; not a reconstructed answer. Facts and supported conclusions stay empty. No performed duty is recorded.</p>
 {!eligible&&<p>Preparation requires current local selection and completed Git evidence with matching frozen question pins. Partial and gaps-only results remain explicit.</p>}
 <p>Editing these inputs cancels an unsubmitted frozen draft. Publication already started may finish; its actual outcome remains below.</p>
 <fieldset disabled={!eligible||busy||!!registry?.inflight}><legend>Explicit caller inputs</legend>
 <label>Constructed connector label<select value={connector} onChange={e=>{invalidate();setConnector(e.target.value);}}><option value="">Choose…</option><option value="pec">PEC</option><option value="domains">Domains</option></select></label>
 {(["at","since"] as const).map(side=>{const item=result?.observation?.[side];if(item?.status!=="Git-object-verified")return null;const ref=item.object.reference,c=choices[ref]??{selected:false,role:"",anchors:[]};return <fieldset key={ref}><legend>{side}: {item.object.readCommit}</legend>
 <label><input type="checkbox" checked={c.selected} onChange={e=>choose(ref,{selected:e.target.checked})}/>Include this successfully observed side</label>
 <label>Intended source role (caller assertion)<input value={c.role} onChange={e=>choose(ref,{role:e.target.value})}/></label>
 {result.anchors?.filter((a:Json)=>a.sideObservationReference===ref).map((a:Json)=><label key={a.reference}><input type="checkbox" checked={c.anchors.includes(a.reference)} onChange={e=>choose(ref,{anchors:e.target.checked?[...c.anchors,a.reference]:c.anchors.filter(x=>x!==a.reference)})}/>Include checked excerpt {a.anchor}: {a.text}</label>)}
 </fieldset>;})}
 <label>Optional caller interpretation<textarea value={statement} onChange={e=>{invalidate();setStatement(e.target.value);}}/></label>
 <label>Asserted by (unverified caller identity)<input value={assertedBy} onChange={e=>{invalidate();setAssertedBy(e.target.value);}}/></label>
 <label><input type="checkbox" checked={linkEvidence} onChange={e=>{invalidate();setLinkEvidence(e.target.checked);}}/>Reference explicitly selected evidence in this interpretation</label>
 <label>Optional caller gap<input value={gap} onChange={e=>{invalidate();setGap(e.target.value);}}/></label><label>Caller gap effect<input value={effect} onChange={e=>{invalidate();setEffect(e.target.value);}}/></label>
 <label><input type="checkbox" checked={assigned} onChange={e=>{invalidate();setAssigned(e.target.checked);}}/>Assign responsibility for this caller gap</label>
 {assigned&&<label>Caller-assigned identity<input value={responsible} onChange={e=>{invalidate();setResponsible(e.target.value);}}/></label>}
 <label>Optional unsupported conclusion<input value={unsupported} onChange={e=>{invalidate();setUnsupported(e.target.value);}}/></label><label>Why unsupported<input value={unsupportedWhy} onChange={e=>{invalidate();setUnsupportedWhy(e.target.value);}}/></label>
 {Object.entries(duties).map(([duty,value])=><fieldset key={duty}><legend>{duty} — caller-reported, unverified</legend><label>Explicit standing<select value={value.standing} onChange={e=>{invalidate();setDuties(old=>({...old,[duty]:{...value,standing:e.target.value}}));}}><option value="">Choose…</option><option value="prepared">Prepared only</option><option value="outstanding">Outstanding</option></select></label><label>Explicit reason<input value={value.reason} onChange={e=>{invalidate();setDuties(old=>({...old,[duty]:{...value,reason:e.target.value}}));}}/></label></fieldset>)}
 <button onClick={prepare}>Freeze draft for inspection</button></fieldset>
 {error&&<p role="alert">Draft operation: {error}. Actual retained outcomes remain below.</p>}{busy&&<p>Operation pending. Cancellation after publication starts cannot guarantee rollback.</p>}
 <button onClick={()=>action("inspect_connector_drafts",{})}>Refresh retained draft outcomes</button>
 {registry&&<p>{registry.used} of {registry.capacity} App-instance identities retained. {registry.limit}</p>}
 {registry?.entries?.map((entry:Json)=><article key={entry.token}><h3>{entry.accountId}: {entry.status}</h3>
 {entry.draft&&<><h4>Frozen question</h4><p>{entry.draft.account.question.text}</p><p>At: {entry.draft.account.question.at_revision}; since: {entry.draft.account.question.since_revision??"not requested"}</p><p>Exact serialized draft: {entry.draft.byteLength} bytes; SHA-256 {entry.draft.sha256}</p>
 <h4>Selected source evidence</h4>{entry.draft.account.sources.map((s:Json)=><div key={s.source_id}><p>{s.path} — {s.revision}; {s.role} (caller assertion)</p><p>Blob: {s.provenance.blob}; content hash: {s.sha256}</p>{s.excerpts.map((e:Json)=><div key={e.excerpt_id}><p>{e.anchor}: [{e.byte_start}, {e.byte_end})</p><pre>{e.text}</pre></div>)}</div>)}
 <h4>Unreviewed caller interpretations</h4>{entry.draft.account.interpretations.map((i:Json)=><p key={i.interpretation_id}>{i.statement} — {i.asserted_by} (caller asserted identity)</p>)}
 <h4>Gaps and responsibility</h4>{entry.draft.account.gaps.map((g:Json,i:number)=><p key={i}>{g.origin}: {g.gap}. {g.effect}. Responsible: {g.responsible.identity??"Unassigned"}</p>)}
 <h4>Reported duties</h4>{entry.draft.account.duties.map((d:Json)=><p key={d.duty}>{d.duty}: {d.standing}; {d.reason} (unverified)</p>)}
 <details><summary>Complete frozen draft and compact receipt limits</summary><pre>{JSON.stringify(entry.draft.account,null,2)}</pre></details>
 <button disabled={busy||dirty||!eligible} onClick={()=>action("publish_connector_draft",{token:entry.token,generation:entry.generation})}>Publish this frozen draft once</button></>}
 {(entry.status==="prepared"||entry.status==="publishing")&&<button onClick={()=>action("cancel_connector_draft",{token:entry.token,generation:entry.generation})}>Cancel draft (started publication may finish)</button>}
 {entry.status==="uncertain"&&<button onClick={()=>action("reconcile_connector_draft",{token:entry.token,generation:entry.generation})}>Inspect exact uncertain attempt</button>}
 <pre>{entry.outcomeText}</pre><pre>{entry.reconciliationText}</pre></article>)}
 <p>Actual outcomes outlive source preparation for this App instance. Process loss loses hot tokens; cold records neither prove prior publication nor restore custody. No automatic retry, rollback or unlink.</p>
 </section>;
}
