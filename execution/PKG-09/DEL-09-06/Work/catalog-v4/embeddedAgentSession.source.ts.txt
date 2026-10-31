/** Explicit workspace-owned live binding. The private execution capability is
 * kept in closures, never tool data, an event, a log, storage or a provider call.
 * No invocation, timer, listener or launcher runs at module construction. */
import { jsonTextKeepingNegativeZero } from './jsonText';
import { invokeWithIngress } from './nativeIngress';
import { EmbeddedAgentBridge, type AgentActual, type AgentBasis, type AgentCall, type AgentDelivery, type AgentScope } from './embeddedAgentBridge';
import type { PreviewModel, ModelHashEvidence, EditorOperationIntent, MechanicsResult } from '../types';
import type { OperationBatch } from './operationBatchService';
import { validateOperationBatch } from './operationBatchService';
import { overlayMayShowRow, type ResultOverlayStanding } from '../features/results/numericalHealth';
import { canonicalJsonString } from './hashService';

export type AgentAssumption=Readonly<{assumptionId:string;statement:string;affectedOperationIds:readonly string[]}>;
export type AgentContext = Readonly<{requestRef:string;threadId:string;turnId:string;callId:string;basis:AgentBasis;assumptions:readonly AgentAssumption[]}>;
export type AgentRunReceipt = Readonly<{jobId:string;runId:string;modelHash:ModelHashEvidence;solverMode:string;health:string}>;
export interface WorkspaceExecution {
 snapshot(): {model:PreviewModel|null;hash:ModelHashEvidence|null;revision:number;generation:number;result:MechanicsResult|null;standing:ResultOverlayStanding|null};
 register(batch:OperationBatch,context:AgentContext):Promise<string|null>;
 proposal(key:string):{status:'pending_review'|'withdrawn'|'applied'|'unknown';outcomeModelHash:ModelHashEvidence|null}|null;
 solve():Promise<AgentRunReceipt|undefined>;
 withdraw(key:string):void;
}
export type AgentSessionView=Readonly<{status:string;closed:boolean;turnActive:boolean;turnStatus:string;failure:string|null;messages:readonly {itemId:string;text:string;role?:'user'|'agent'}[];truncated?:boolean}>;
type Authority=AgentScope&{ownerCapability:string};
type Invoke=(request:Record<string,unknown>)=>Promise<unknown>;
type Proposal={basis:AgentBasis;key:string;context:AgentContext};
type Run={basis:AgentBasis;receipt:AgentRunReceipt};
type Proof=Record<string,unknown>;
const LIMITS={argumentBytes:16384,resultBytes:65536,pageRows:50,pendingCalls:16,proposalOperations:16};
const plain=(x:unknown):x is Record<string,unknown>=>!!x&&typeof x==='object'&&!Array.isArray(x);
/** The native kinds swbpipe-catalog/4 admits; the catalog schema is their gate and the applier their authority. */
export const ADMITTED_OPERATION_KINDS=Object.freeze(['modify/Node/set_field/position','create/Material/create_material','create/Node/create_node','connect/Element/connect_pipe_run','create/Support/create_support','create/Load/create_load_case','create/Load/create_primitive_load','modify/Load/update_load/pressure_regions','modify/Model/set_field/pressure_profile','insert/Component/insert_component_symbol','modify/Component/set_field/objective_connector','modify/Support/update_support/configuration','delete/Component/delete_component','delete/Support/delete_support','delete/Element/delete_pipe_run','delete/Node/delete_node']);
export const RECORD_FAMILIES=['components','supports','pipe_segments','nodes'] as const;
export type RecordFamily=typeof RECORD_FAMILIES[number];
const SUPPORT_CONFIGURATION=['family','restraints','stiffness','hanger','nonlinear','provenance'] as const;
const RECORD_PAGE_BYTES=48*1024,RECORD_TEXT_BYTES=16384,ID_CHARS=160;
const utf8=new TextEncoder();
const byteLength=(text:string)=>utf8.encode(text).byteLength;
/** The leading identifiers that fit `budget` characters, then an ellipsis for any not
 * shown, so a tool message stays inside the catalog's 1000-character bound. */
function namedIds(ids:readonly string[],budget:number):string{
 const shown:string[]=[];let used=0;for(const id of ids){if(used+id.length+2>budget)break;shown.push(id);used+=id.length+2;}
 return `${shown.join(', ')}${shown.length<ids.length?`${shown.length?', ':''}…`:''}`;
}
const blankText=(value:unknown)=>typeof value!=='string'||!value.trim();
/** The bends and tees the solver reports as lacking user-entered modifiers
 * (product_physics validation BEND_/BRANCH_USER_MODIFIER_INPUT_MISSING): the
 * person enters k, SIFs and their source; the agent never authors them. */
export function componentsAwaitingUserModifiers(model:PreviewModel):string[]{
 const awaiting:string[]=[];
 for(const component of model.components??[]){
  const record=component as unknown as Record<string,unknown>,modifiers=plain(record.modifiers)?record.modifiers:null,kind=String(record.kind);
  const missing=(key:string)=>!modifiers||modifiers[key]===undefined||modifiers[key]===null;
  // A realized arc uses only the directional SIF pair; a geometry-only marker the scalar.
  const realized=plain(record.mechanics_interface)&&record.mechanics_interface.solver_consumption==='curved_bend_macro_element';
  const sifMissing=realized?missing('sif_in_plane_user_value')||missing('sif_out_of_plane_user_value'):missing('sif_user_value');
  if(['bend','elbow'].includes(kind)&&(!modifiers||sifMissing||missing('flexibility_factor_user_value')||blankText(modifiers.source_reference)))awaiting.push(String(record.id));
  else if(['branch','tee','branch_connection'].includes(kind)&&(!modifiers||missing('branch_header_sif_user_value')||missing('branch_branch_sif_user_value')||missing('flexibility_factor_user_value')||blankText(modifiers.source_reference)))awaiting.push(String(record.id));
 }
 return awaiting;
}
/** The applier's `display_number`: an integral value below 1e15 as an integer,
 * any other in Rust's shortest round-trip decimal, which never uses an exponent. */
export function engineDisplayNumber(value:number):string{
 if(Number.isInteger(value)&&Math.abs(value)<1e15)return String(value);
 const text=String(value),match=/^(-?)(\d)(?:\.(\d+))?e([+-]\d+)$/.exec(text);if(!match)return text;
 const [,sign,lead,fraction='',exponent]=match,digits=lead+fraction,point=1+Number(exponent);
 if(point<=0)return `${sign}0.${'0'.repeat(-point)}${digits}`;
 return point>=digits.length?sign+digits+'0'.repeat(point-digits.length):`${sign}${digits.slice(0,point)}.${digits.slice(point)}`;
}
const trimmed=(value:unknown)=>typeof value==='string'?value.trim():'';
/** The deletion summaries the applier compares (node_delete_display, pipe_delete_display,
 * the support's trimmed label); empty when the applier would refuse the record's deletion. */
function deleteText(family:Exclude<RecordFamily,'components'>,record:Record<string,unknown>):string{
 const label=trimmed(record.label);if(!label)return '';
 if(family==='supports')return label;
 if(family==='pipe_segments'){const [from,to,material]=[record.from,record.to,record.material].map(trimmed);return from&&to&&material?`${label}; ${from}->${to}; material=${material}`:'';}
 const position=plain(record.position)?record.position:{},axes=(['x','y','z'] as const).map(axis=>position[axis]);
 return axes.every(value=>typeof value==='number'&&Number.isFinite(value))?`${label}; x=${engineDisplayNumber(axes[0] as number)}; y=${engineDisplayNumber(axes[1] as number)}; z=${engineDisplayNumber(axes[2] as number)}`:'';
}
/** Bend markers the person has not realized (no curved macro-element yet). */
export function unrealizedBends(model:PreviewModel):string[]{
 return (model.components??[]).filter(component=>{const record=component as unknown as Record<string,unknown>;const iface=plain(record.mechanics_interface)?record.mechanics_interface:{};
  return ['bend','elbow'].includes(String(record.kind))&&iface.solver_consumption!=='curved_bend_macro_element';}).map(component=>String((component as unknown as Record<string,unknown>).id));
}
/** How the scalar SIF stands on the given unrealized bends, for the pressure-free solve message. */
export function chordSifText(model:PreviewModel,chords:readonly string[]):string{
 const without=chords.filter(id=>{const record=(model.components??[]).find(component=>component.id===id) as unknown as Record<string,unknown>|undefined;
  const sif=plain(record?.modifiers)&&plain(record.modifiers.sif_user_value)?record.modifiers.sif_user_value.value:undefined;return !(typeof sif==='number'&&Number.isFinite(sif)&&sif>0);});
 if(!without.length)return 'Each has a supplied scalar SIF, which applies to its chord.';
 const named=`no scalar SIF was supplied for ${without.length} of them (${namedIds(without,200)}), so no intensified measure is published for those`;
 return without.length===chords.length?`None has a supplied scalar SIF, so no intensified measure is published for them.`:`A supplied scalar SIF applies to the other chords; ${named}.`;
}
/** Exact before texts for the admitted edits of one record, as the applier compares
 * them: the engine's canonical JSON for components and support configuration, the
 * applier's deletion summary otherwise. A deletion the applier would refuse has no text. */
export async function recordBefore(family:RecordFamily,record:Record<string,unknown>,recordText:string):Promise<Record<string,string>>{
 if(family==='components'){
  const before:Record<string,string>={delete:recordText};const connector=record.objective_connector;
  if(plain(connector))for(const key of ['hardware','pressure_model'])if(connector[key]!==undefined)before[`objective_connector.${key}`]=await canonicalJsonString(connector[key]);
  return before;
 }
 if(family==='supports'){
  const configuration=Object.fromEntries(SUPPORT_CONFIGURATION.filter(key=>record[key]!==undefined).map(key=>[key,record[key]]));
  const text=deleteText(family,record);return {...(text?{delete:text}:{}),configuration:await canonicalJsonString(configuration)};
 }
 const text=deleteText(family,record);return text?{delete:text}:{};
}
const AUDIT_BOUNDARY=Object.freeze({mutation_route:'structured_operations_only',direct_model_mutation_allowed:false,requires_user_acceptance:true,mutates_accepted_model_state:false} as const);
const PROFESSIONAL_BOUNDARY=Object.freeze({
 human_review_required:true,
 software_makes_compliance_claim:false,
 software_makes_certification_claim:false,
 software_makes_sealing_claim:false,
 software_makes_approval_claim:false,
 software_makes_authentication_claim:false
} as const);
/** The agent supplies operation_id, operation_kind, target, change and rationale; the host
 * stamps status, attribution, queue/source and the constant validation and boundary records.
 * A host field in the arguments never survives (the catalog already refuses one). */
export function stampAgentOperations(operations:readonly Record<string,unknown>[],proposalHandle:string,requestRef:string):EditorOperationIntent[]{
 return operations.map(operation=>({...structuredClone(operation),author_type:'agent' as const,operation_status:'proposed' as const,queue_id:proposalHandle,source:{source_ref:requestRef,source_channel:'embedded_agent',source_role:'agent'},validation:{schema_validation:'not_run',constraint_validation:'not_run',unit_validation:'not_run',diff_preview_status:'not_run',application_status:'not_applied'},audit_boundary:{...AUDIT_BOUNDARY},professional_boundary:{...PROFESSIONAL_BOUNDARY}}) as unknown as EditorOperationIntent);
}
/** RFC 8785 text of a string-only object tree: the `before` the applier compares for pressure_profile. */
function stringTreeText(value:unknown):string{
 if(typeof value==='string')return JSON.stringify(value);
 if(!plain(value))throw new Error('AGENT-PROFILE-UNREPRESENTABLE');
 return `{${Object.keys(value).sort().map(key=>`${JSON.stringify(key)}:${stringTreeText(value[key])}`).join(',')}}`;
}
function same(a:unknown,b:unknown):boolean {
 if(Object.is(a,b))return true;
 if(Array.isArray(a)&&Array.isArray(b))return a.length===b.length&&a.every((value,i)=>same(value,b[i]));
 if(!plain(a)||!plain(b))return false;
 const keys=Object.keys(a);return keys.length===Object.keys(b).length&&keys.every(key=>Object.hasOwn(b,key)&&same(a[key],b[key]));
}
const defaultInvoke:Invoke=request=>invokeWithIngress('embedded_agent_host',{request});
function opaque():string {const bytes=new Uint8Array(24);crypto.getRandomValues(bytes);return Array.from(bytes,byte=>byte.toString(16).padStart(2,'0')).join('');}
function small(value:unknown):string {const raw=jsonTextKeepingNegativeZero(value);if(new TextEncoder().encode(raw).byteLength>64*1024)throw new Error('AGENT-OUTPUT-LIMIT');return raw;}
/** Only the workspace session constructs this class with its actual getters and
 * handlers. A model tool call cannot register or replace that execution owner. */
export class EmbeddedAgentSession {
 #authority:Authority|null=null;#scope:AgentScope|null=null;#generation=-1;#bridge:EmbeddedAgentBridge|null=null;
 #actual=new Map<string,AgentActual>();#proposals=new Map<string,Proposal>();#runs=new Map<string,Run>();
 #cursors=new Map<string,{tool:string;basis:AgentBasis;offset:number;run?:string;filter?:unknown}>();
 #interrupted=new Set<string>();
 #listeners=new Set<(view:AgentSessionView)=>void>();
 #messages=new Map<string,string>();#roles=new Map<string,'user'|'agent'>();#messageChars=0;#truncated=false;
 #view:AgentSessionView={status:'closed',closed:true,turnActive:false,turnStatus:'none',failure:null,messages:[]};
 subscribe(listener:(view:AgentSessionView)=>void):()=>void {this.#listeners.add(listener);try{listener(this.#view);}catch{this.#listeners.delete(listener);}return ()=>{this.#listeners.delete(listener);};}
 private publish(view:AgentSessionView){this.#view=Object.freeze(view);for(const listener of this.#listeners){try{listener(this.#view);}catch{/* A view callback cannot break session custody. */}}}
 private boundedViewMessages(){
  while(this.#messages.size>64||this.#messageChars>65536){const first=this.#messages.keys().next().value!;this.#messageChars-=this.#messages.get(first)!.length;this.#messages.delete(first);this.#roles.delete(first);this.#truncated=true;}
  return [...this.#messages].map(([itemId,text])=>({itemId,text,role:this.#roles.get(itemId)??'agent' as const}));
 }
 private acceptView(frame:Record<string,unknown>){
  if(Array.isArray(frame.messages))for(const message of frame.messages){
   if(!plain(message)||typeof message.itemId!=='string'||message.itemId.length>256||typeof message.text!=='string'||message.text.length>65536||!['delta','final'].includes(String(message.kind)))continue;
   const old=this.#messages.get(message.itemId)??'';const next=message.kind==='final'?message.text:old+message.text;
   this.#messageChars+=next.length-old.length;this.#messages.set(message.itemId,next);this.#roles.set(message.itemId,'agent');
   // This is a bounded conversation view, not the actual queue/job ledger.
   this.boundedViewMessages();
  }
  this.publish({status:typeof frame.status==='string'?frame.status:'unavailable',closed:frame.closed===true,turnActive:frame.turnActive===true,turnStatus:typeof frame.turnStatus==='string'?frame.turnStatus:'none',failure:typeof frame.failure==='string'?frame.failure:null,messages:this.boundedViewMessages(),truncated:this.#truncated});
 }

 #starting=false;#inflight=new Set<Promise<unknown>>();
 #timer:ReturnType<typeof setTimeout>|null=null;#closed=true;#polling=false;
 // Advanced by close(); a poll answered after Stop or restart is stale and is not published.
 #lifecycle=0;
 constructor(private readonly owner:WorkspaceExecution,private readonly invoke:Invoke=defaultInvoke){}
 async availability():Promise<unknown>{return this.invoke({kind:'availability'});}
 async provider(request:Record<string,unknown>):Promise<unknown>{
  if(!['provider_snapshot','provider_save','provider_clear','provider_recover'].includes(String(request.kind)))throw new Error('AGENT-CONFIG-REQUEST');
  return this.invoke(request);
 }
 async start(providerRevision:string):Promise<unknown>{
  if(this.#starting)throw new Error('AGENT-START-IN-PROGRESS');
  this.#starting=true;
  try{return await this.startOwned(providerRevision);}finally{this.#starting=false;}
 }
 private async startOwned(providerRevision:string):Promise<unknown>{
  if(this.#authority)await this.close();
  this.#messages.clear();this.#roles.clear();this.#messageChars=0;this.#truncated=false;this.#cursors.clear();this.#proposals.clear();this.#runs.clear();this.#interrupted.clear();
  this.publish({...this.#view,messages:[],truncated:false});
  const before=this.owner.snapshot();if(!before.model||!before.hash)throw new Error('AGENT-WORKSPACE-NOT-READY');
  const registered=await this.invoke({kind:'register',basis:{modelRevision:before.revision,modelHash:before.hash,stateId:null,runId:null}});
  if(!plain(registered)||typeof registered.workspaceHandle!=='string'||typeof registered.applicationGeneration!=='number'||typeof registered.ownerCapability!=='string')throw new Error('AGENT-REGISTRATION-REFUSED');
  this.#authority={workspaceHandle:registered.workspaceHandle,applicationGeneration:registered.applicationGeneration,ownerCapability:registered.ownerCapability};
  this.#scope={workspaceHandle:registered.workspaceHandle,applicationGeneration:registered.applicationGeneration};this.#generation=before.generation;
  this.#closed=false;
  const authority=this.#authority;
  this.#bridge=new EmbeddedAgentBridge(this.#scope,{
   claim:async requestRef=>{const value=await this.invoke({kind:'claim',authority,requestRef});if(!plain(value)||typeof value.raw!=='string')throw new Error('AGENT-CLAIM-REFUSED');return value.raw;},
   complete:async(requestRef,outcome)=>{
    const actual=this.#actual.get(requestRef);if(!actual||actual.outcome!==outcome)throw new Error('AGENT-OWNER-RECORD-MISSING');
    await this.invoke({kind:'publish_actual',authority,requestRef,outcome,proof:actual.record});
    const result=await this.invoke({kind:'complete',authority,requestRef,outcome});
    if(!plain(result)||!['queued','detached','lost','unconfirmed'].includes(String(result.delivery)))return 'unconfirmed';
    return result.delivery as AgentDelivery;
   }
  },{isCurrent:call=>!this.#closed&&this.owner.snapshot().generation===this.#generation&&call.basis.workspaceHandle===this.#scope?.workspaceHandle&&call.basis.applicationGeneration===this.#scope?.applicationGeneration,execute:async call=>{
   let actual:AgentActual;
   try{actual=await this.execute(call);}catch{actual=this.failure(call,'Outcome unavailable; inspect the retained queue or job record.','execution_error');}
   this.#actual.set(call.requestRef,Object.freeze(actual));return actual;
  }});
  if(this.owner.snapshot().generation!==before.generation||this.owner.snapshot().revision!==before.revision){await this.close();throw new Error('AGENT-WORKSPACE-RETIRED');}
  try {const response=await this.invoke({kind:'start',authority,providerRevision});
   if(plain(response)&&response.status==='starting'){this.acceptView({status:'starting',closed:false});this.schedule();}else await this.close();return response;
  }catch(error){try{const frame=await this.invoke({kind:'poll',authority});if(plain(frame))this.acceptView(frame);}catch{/* Preserve the original static refusal. */}await this.close();throw error;}
 }
 private schedule(){if(this.#closed)return;this.#timer=setTimeout(()=>{void this.poll().catch(()=>{void this.close();}).finally(()=>this.schedule());},40);}
 async poll():Promise<unknown>{
  if(!this.#authority||this.#polling)return null;this.#polling=true;
  try{
   const snap=this.owner.snapshot();if(snap.generation!==this.#generation){this.#messages.clear();this.#roles.clear();this.#messageChars=0;this.#truncated=false;this.publish({...this.#view,messages:[],truncated:false});await this.close();return null;}
   if(snap.hash)await this.invoke({kind:'basis',authority:this.#authority,basis:{modelRevision:snap.revision,modelHash:snap.hash,stateId:null,runId:null}});
   const lifecycle=this.#lifecycle;
   const result=await this.invoke({kind:'poll',authority:this.#authority});
   if(lifecycle!==this.#lifecycle)return null;
   if(plain(result)&&Array.isArray(result.notices))for(const reference of result.notices){
    if(typeof reference==='string'&&this.#bridge){const task=this.#bridge.notify({requestRef:reference});this.#inflight.add(task);void task.finally(()=>this.#inflight.delete(task));}
   }
   if(plain(result))this.acceptView(result);
   if(plain(result)&&result.closed===true){this.#closed=true;this.#bridge?.close();}
   return result;
  }finally{this.#polling=false;}
 }
 async text(text:string){if(!this.#authority||this.#closed)throw new Error('AGENT-CLOSED');const result=await this.invoke({kind:'text',authority:this.#authority,text});const id=opaque();this.#messages.set(id,text);this.#roles.set(id,'user');this.#messageChars+=text.length;this.publish({...this.#view,turnActive:true,turnStatus:'starting',messages:this.boundedViewMessages(),truncated:this.#truncated});return result;}
 async interrupt(){if(!this.#authority)return;const result=await this.invoke({kind:'interrupt',authority:this.#authority});if(plain(result)&&typeof result.turnId==='string'){this.#interrupted.add(result.turnId);for(const proposal of this.#proposals.values())if(proposal.context.turnId===result.turnId)this.owner.withdraw(proposal.key);}return result;}
 async close(){this.#lifecycle++;this.#closed=true;this.publish({...this.#view,status:'stopping',closed:true,turnActive:false});if(this.#timer)clearTimeout(this.#timer);this.#timer=null;this.#bridge?.close();const response=this.#authority?await this.invoke({kind:'close',authority:this.#authority}):null;await Promise.allSettled([...this.#inflight]);return response;}
 actual(reference:string){return this.#actual.get(reference);}
 private current(call:AgentCall){
  const live=this.owner.snapshot();
  if(this.#closed||live.generation!==this.#generation||call.basis.workspaceHandle!==this.#scope?.workspaceHandle||call.basis.applicationGeneration!==this.#scope?.applicationGeneration)return false;
  if(call.tool==='swbpipe_observe_proposal')return same(this.#proposals.get(String(call.arguments.proposalHandle))?.basis,call.basis);
  if(call.tool==='swbpipe_read_results')return same(this.#runs.get(String(call.arguments.runHandle))?.basis,call.basis);
  return !!live.hash&&call.basis.modelRevision===live.revision&&same(call.basis.modelHash,live.hash);
 }
 private failure(call:AgentCall,message:string,status='unavailable'):AgentActual{return {outcome:small({status,basis:call.basis,message,data:null}),record:{kind:'failure'}};}
 private result(call:AgentCall,status:string,message:string,data:unknown,proof:Proof):AgentActual{return {outcome:small({status,basis:call.basis,message,data}),record:proof};}
 private offset(call:AgentCall,run?:string):number {
  const page=call.arguments.page as {cursor:string|null;limit:number};if(page.cursor===null)return 0;
  const saved=this.#cursors.get(page.cursor);if(!saved||saved.tool!==call.tool||!same(saved.basis,call.basis)||saved.run!==run||!same(saved.filter,call.arguments.filter??call.arguments.family))throw new Error('AGENT-CURSOR-REFUSED');return saved.offset;
 }
 private cursor(call:AgentCall,offset:number,more:boolean,run?:string):string|null {
  if(!more)return null;if(this.#cursors.size>=64)throw new Error('AGENT-CURSOR-LIMIT');const ref=opaque();this.#cursors.set(ref,{tool:call.tool,basis:call.basis,offset,run,filter:structuredClone(call.arguments.filter??call.arguments.family)});return ref;
 }
 private async execute(call:AgentCall):Promise<AgentActual>{
  if(call.tool==='swbpipe_observe_proposal'){
   const handle=String(call.arguments.proposalHandle),record=this.#proposals.get(handle);if(!record||!same(record.basis,call.basis))return this.failure(call,'Proposal is unavailable.');
   const standing=this.owner.proposal(record.key);const status=standing?.status??'unknown';const hash=standing?.outcomeModelHash??null;
   return this.result(call,status,'Recorded proposal standing.',{proposalHandle:handle,proposalBasis:record.basis,outcomeModelHash:hash,author_type:'agent',assumptions:record.context.assumptions},{kind:'proposal',handle,basis:record.basis,status,outcomeModelHash:hash});
  }
  if(call.tool==='swbpipe_read_results')return this.readResults(call);
  if(!this.current(call))return this.failure(call,'Workspace basis changed.','stale_basis');
  const snap=this.owner.snapshot();const model=snap.model!;
  if(call.tool==='swbpipe_read_model_summary'){
   const counts:Record<string,number>={};for(const key of ['nodes','pipe_segments','supports','materials','sections','load_cases','primitive_loads','combinations','components']){
    const value=(model as unknown as Record<string,unknown>)[key];if(Array.isArray(value))counts[key]=value.length;
   }
   const contract=(model as unknown as Record<string,unknown>).pressure_contract;
   if(contract!==undefined&&(!plain(contract)||Object.values(contract).some(value=>typeof value!=='string')))return this.failure(call,'The pressure contract is not representable in this catalog summary.');
   const awaiting=componentsAwaitingUserModifiers(model);
   const profile:Record<string,unknown>={};if(model.schema_version!==undefined)profile.schema_version=model.schema_version;if(contract!==undefined)profile.pressure_contract=contract;
   return this.result(call,'ok','Current admitted workspace; changes require human review.',{workspaceHandle:call.basis.workspaceHandle,projectId:model.project.id,schemaVersion:model.schema_version,pressureContract:contract??null,pressureProfileBefore:stringTreeText(profile),projectUnits:model.project.units,objectCounts:counts,admittedOperationKinds:[...ADMITTED_OPERATION_KINDS],componentsAwaitingUserModifiers:{count:awaiting.length,ids:awaiting.filter(id=>id&&id.length<=ID_CHARS).slice(0,32)},limits:LIMITS},{kind:'read'});
  }
  if(call.tool==='swbpipe_read_nodes'){
   const offset=this.offset(call),page=call.arguments.page as {limit:number};const end=Math.min(model.nodes.length,offset+page.limit);
   const nodes=[];for(let i=offset;i<end;i++){const node=model.nodes[i];if(node.id.length>160)return this.failure(call,'Node identifier exceeds this catalog page.');nodes.push({id:node.id,position:{x:node.position.x,y:node.position.y,z:node.position.z},unit:model.project.units.length});}
   return this.result(call,'ok','Bounded node page at the captured basis.',{nodes,projectUnits:model.project.units,nextCursor:this.cursor(call,end,end<model.nodes.length)},{kind:'read'});
  }
  if(call.tool==='swbpipe_read_records'){
   const family=call.arguments.family as RecordFamily;if(!RECORD_FAMILIES.includes(family))return this.failure(call,'Record family is unavailable.');
   const rows=((model as unknown as Record<string,unknown>)[family] as Record<string,unknown>[]|undefined)??[];
   const offset=this.offset(call),page=call.arguments.page as {limit:number};const records=[];let bytes=0,end=offset;
   for(;end<rows.length&&records.length<page.limit;end++){
    const record=rows[end];if(typeof record?.id!=='string'||!record.id||record.id.length>ID_CHARS)return this.failure(call,'Record identifier exceeds this catalog page.');
    const recordText=await canonicalJsonString(record);const before=await recordBefore(family,record,recordText);
    // Bounds are UTF-8 bytes; a record whose escaped entry alone exceeds a page is unavailable, never cut.
    if(byteLength(recordText)>RECORD_TEXT_BYTES||Object.values(before).some(text=>byteLength(text)>RECORD_TEXT_BYTES))return this.failure(call,`Record ${record.id} exceeds this catalog page.`);
    const entry={id:record.id,recordText,before};const size=byteLength(JSON.stringify(entry));
    if(size>RECORD_PAGE_BYTES)return this.failure(call,`Record ${record.id} exceeds this catalog page.`);
    if(bytes+size>RECORD_PAGE_BYTES)break;bytes+=size;records.push(entry);
   }
   if(!this.current(call))return this.failure(call,'Workspace changed while reading records.','stale_basis');
   return this.result(call,'ok','Bounded record page at the captured basis; before texts are exact for that basis only.',{family,records,nextCursor:this.cursor(call,end,end<rows.length)},{kind:'read'});
  }
  if(call.tool==='swbpipe_propose_operations'){
   if(this.#proposals.size>=64)return this.failure(call,'Proposal retention is full.');
   const handle=opaque();const context:AgentContext=Object.freeze({requestRef:call.requestRef,threadId:call.threadId,turnId:call.turnId,callId:call.callId,basis:structuredClone(call.basis),assumptions:structuredClone(call.arguments.assumptions as AgentAssumption[])});
   const operations=stampAgentOperations(call.arguments.operations as Record<string,unknown>[],handle,call.requestRef);
   const batch:OperationBatch={batch_id:`agent-${handle}`,operations,source_model_hash:snap.hash!.value};
   const validation=await validateOperationBatch(model,batch,snap.hash);if(!this.current(call))return this.failure(call,'Workspace changed during proposal preparation.','stale_basis');
   if(validation.validation.batch_validation_status!=='passed')return this.failure(call,'The operation engine refused the proposal; nothing was queued.');
   if(this.#interrupted.has(call.turnId))return this.failure(call,'Turn interrupted before registration.');
   const key=await this.owner.register(batch,context);if(!key)return this.failure(call,'Proposal registration was not confirmed.');
   this.#proposals.set(handle,{basis:structuredClone(call.basis),key,context});
   if(this.#interrupted.has(call.turnId)){this.owner.withdraw(key);return this.failure(call,'Turn interrupted; inspect the retained queue record.','unknown');}
   return this.result(call,'pending_review','Immutable batch registered for explicit human review.',{proposalHandle:handle,author_type:'agent'},{kind:'proposal',handle,basis:call.basis,status:'pending_review',outcomeModelHash:null});
  }
  if(call.tool==='swbpipe_solve'){
   if(this.#runs.size>=64)return this.failure(call,'Run retention is full.');
   // An unrealized bend marker: the exact route refuses it before solving
   // (EXACT_PRESSURE_FAMILY_NOT_ADMITTED); the pressure-free route solves it as a
   // straight chord whose stiffness k never affects. A supplied positive scalar SIF
   // applies to the chord; without one no intensified measure is published.
   const chords=unrealizedBends(model);
   if(chords.length&&(model as unknown as Record<string,unknown>).pressure_contract!==undefined)return this.failure(call,`Not solved: the exact route refuses unrealized bends (${namedIds(chords,300)}). Ask the person to realize each with Insert bend at corner and enter k, the SIFs and their source, then solve.`);
   const receipt=await this.owner.solve();if(!receipt||!same(receipt.modelHash,call.basis.modelHash))return this.failure(call,'No matching completed native solve is available.');
   const handle=opaque();this.#runs.set(handle,{basis:structuredClone(call.basis),receipt});
   const solved=chords.length?`Native solve completed. ${chords.length} unrealized bend(s) (${namedIds(chords,300)}) were solved as straight chords; k does not affect chord stiffness. ${chordSifText(model,chords)} Say so when reporting these results. Applicability and professional acceptance remain separate.`:'Native solve completed; applicability and professional acceptance remain separate.';
   return this.result(call,'completed',solved,{runHandle:handle,runId:receipt.runId,evaluatedModelHash:receipt.modelHash,health:receipt.health,solverMode:receipt.solverMode},{kind:'run',handle,runId:receipt.runId,basis:call.basis,status:'completed',nativeJobId:receipt.jobId});
  }
  return this.failure(call,'Tool is unavailable.');
 }
 private readResults(call:AgentCall):AgentActual{
  const handle=String(call.arguments.runHandle),run=this.#runs.get(handle);if(!run||!same(run.basis,call.basis))return this.failure(call,'Run is unavailable.');
  const snap=this.owner.snapshot(),result=snap.result;if(!result||result.run_id!==run.receipt.runId)return this.failure(call,'The retained run is no longer held by the result owner.');
  const filter=call.arguments.filter as {kinds:string[];entityRefs:string[]}|undefined;
  const rows=filter?result.results.filter(row=>(!filter.kinds.length||filter.kinds.includes(row.kind))&&(!filter.entityRefs.length||filter.entityRefs.includes(row.entity_ref))):result.results;
  const offset=this.offset(call,handle),page=call.arguments.page as {limit:number},end=Math.min(rows.length,offset+page.limit);const values=[];
  for(let i=offset;i<end;i++){
   const row=rows[i];if([row.id,row.kind,row.entity_ref].some(v=>v.length>160)||row.unit.length>40)return this.failure(call,'Result identifiers exceed this catalog page.');
   const permitted=overlayMayShowRow(snap.standing,row)&&!result.retained_precision&&Number.isFinite(row.value);
   values.push({id:row.id,kind:row.kind,entityRef:row.entity_ref,value:permitted?row.value:null,exactDecimal:null,unit:row.unit,availability:permitted?'available':'withheld',reason:permitted?null:'The existing numerical view does not permit this binary64 value.'});
  }
  return this.result(call,'ok','Permitted bounded source-unit values; withheld values have no substitute number.',{runHandle:handle,runId:run.receipt.runId,evaluatedModelHash:run.basis.modelHash,values,nextCursor:this.cursor(call,end,end<rows.length,handle),standing:{route:result.producer?.semantic_contract_id??'unavailable',health:run.receipt.health,checks:snap.standing?.eligible?['numerical_view_eligible']:['numerical_view_withheld']}},{kind:'run',handle,runId:run.receipt.runId,basis:run.basis,status:'completed',nativeJobId:run.receipt.jobId});
 }
}
