import { afterEach, describe, expect, it, vi } from 'vitest';
import { EmbeddedAgentSession, type WorkspaceExecution, type AgentRunReceipt } from './embeddedAgentSession';
import type { PreviewModel, ModelHashEvidence, MechanicsResult } from '../types';
import type { AgentBasis } from './embeddedAgentBridge';
const mocks=vi.hoisted(()=>({validate:vi.fn()}));
vi.mock('./operationBatchService',()=>({validateOperationBatch:mocks.validate}));
const hash={algorithm:'sha256',canonicalization:'rfc8785_jcs',payload_scope:'model_payload',payload_ref:'invented',value:'a'.repeat(64),hash_status:'computed_local_preview'} as ModelHashEvidence;
// The workspace and the engine write `sha256:` hex; the agent's catalog form is the hex alone.
const engineHash={...hash,value:`sha256:${hash.value}`} as ModelHashEvidence;
const basis:AgentBasis={workspaceHandle:'workspace-invented',applicationGeneration:1,modelRevision:1,modelHash:hash,stateId:null,runId:null};
function deferred<T>(){let resolve!:(v:T)=>void;const promise=new Promise<T>(r=>{resolve=r;});return {resolve,promise};}
function setup(workspaceHash:ModelHashEvidence=engineHash){
 let revision=1,generation=1,tool='swbpipe_read_model_summary',args:Record<string,unknown>={},reference='invented-session:1',turn='turn-1';
 const model={schema_version:'0.8.0',project:{id:'invented',units:{length:'m'}},nodes:[{id:'node-1',label:'N1',position:{x:-0,y:1,z:2}}]} as unknown as PreviewModel;
 let result:MechanicsResult|null=null;
 const owner:WorkspaceExecution={snapshot:()=>({model,hash:workspaceHash,revision,generation,result,standing:null}),register:vi.fn(async()=> 'batch-key'),proposal:vi.fn(()=>({status:'pending_review' as const,outcomeModelHash:null})),solve:vi.fn(async()=>undefined),withdraw:vi.fn()};
 const sent:Record<string,unknown>[]=[];
 const invoke=vi.fn(async(value:Record<string,unknown>):Promise<unknown>=>{
  sent.push(value);
  switch(value.kind){
   case 'register':return {...basis,ownerCapability:'private-owner-capability'};
   case 'start':return {status:'starting'};
   case 'poll':return {status:'ready',notices:[reference],messages:[],closed:false,turnActive:false,turnStatus:'none'};
   case 'claim':return {raw:JSON.stringify({requestRef:reference,threadId:'thread-1',turnId:turn,callId:'call-1',basis:{...basis,modelHash:Object.fromEntries(Object.entries(hash).reverse())},tool,arguments:args})};
   case 'interrupt':return {status:'queued',turnId:turn};
   case 'publish_actual':return {recorded:true};
   case 'complete':return {delivery:'detached'};
   default:return {};
  }
 });
 const session=new EmbeddedAgentSession(owner,invoke);
 return {session,owner,invoke,sent,model,setResult:(value:MechanicsResult)=>{result=value;},edit:()=>{revision++;},retire:()=>{generation++;},call:(name:string,a:Record<string,unknown>={},ref='invented-session:1',turnId='turn-1')=>{tool=name;args=a;reference=ref;turn=turnId;}};
}
afterEach(()=>{vi.useRealTimers();vi.clearAllMocks();});
async function drain(){for(let i=0;i<16;i++)await Promise.resolve();}
describe('workspace-owned live embedded agent adapter',()=>{
 it('gives the agent the catalog form of the workspace hash in its basis, updates and solve output',async()=>{
  vi.useFakeTimers();const {session,sent,owner,call}=setup();
  await session.start('revision');await session.poll();await drain();
  const bases=sent.filter(v=>v.kind==='register'||v.kind==='basis').map(v=>(v.basis as {modelHash:ModelHashEvidence}).modelHash);
  expect(sent.some(v=>v.kind==='basis')).toBe(true);expect(bases.every(item=>JSON.stringify(item)===JSON.stringify(hash))).toBe(true);
  expect(JSON.parse(session.actual('invented-session:1')!.outcome).status).toBe('ok');
  vi.mocked(owner.solve).mockResolvedValueOnce({jobId:'job-1',runId:'run-1',modelHash:engineHash,solverMode:'sparse_interactive',health:'ok'});
  call('swbpipe_solve',{},'invented-session:2');await session.poll();await drain();
  const solved=JSON.parse(session.actual('invented-session:2')!.outcome);expect(solved.status).toBe('completed');expect(solved.data.evaluatedModelHash).toEqual(hash);
  await session.close();
 });
 it('validates the batch on the engine form and reports an applied outcome in the catalog form',async()=>{
  vi.useFakeTimers();const {session,sent,owner,call}=setup();mocks.validate.mockResolvedValueOnce({validation:{batch_validation_status:'passed'}});
  call('swbpipe_propose_operations',{operations:[{operation_id:'operation-1'}],assumptions:[]});
  await session.start('revision');await session.poll();await drain();
  const [,batch,validationHash]=mocks.validate.mock.calls[0];expect(batch.source_model_hash).toBe(engineHash.value);expect(validationHash).toEqual(engineHash);
  const handle=JSON.parse(session.actual('invented-session:1')!.outcome).data.proposalHandle;
  vi.mocked(owner.proposal).mockReturnValueOnce({status:'applied',outcomeModelHash:{...engineHash,value:`sha256:${'b'.repeat(64)}`}});
  call('swbpipe_observe_proposal',{proposalHandle:handle},'invented-session:2');await session.poll();await drain();
  const observed=JSON.parse(session.actual('invented-session:2')!.outcome);expect(observed.status).toBe('applied');expect(observed.data.outcomeModelHash.value).toBe('b'.repeat(64));
  expect((sent.filter(v=>v.kind==='publish_actual').at(-1)!.proof as {outcomeModelHash:ModelHashEvidence}).outcomeModelHash.value).toBe('b'.repeat(64));
  await session.close();
 });
 it('refuses a workspace hash in any form but sha256: and 64 lowercase hex digits',async()=>{
  for(const value of [hash.value,`sha256:${hash.value.toUpperCase()}`,`sha256:${hash.value.slice(1)}`,`SHA256:${hash.value}`]){
   const {session,invoke}=setup({...hash,value});
   await expect(session.start('revision')).rejects.toThrow('AGENT-ENGINE-HASH-FORM-REFUSED');
   expect(invoke.mock.calls.some(([request])=>request.kind==='register')).toBe(false);
  }
 });
 it('refuses an agent basis hash in any form but 64 lowercase hex digits, by name',async()=>{
  const {agentHash,catalogHash}=await import('./embeddedAgentSession');
  expect(agentHash(engineHash)).toEqual(hash);expect(catalogHash(hash)).toBe(hash);expect(catalogHash(null)).toBeNull();
  for(const value of [engineHash.value,hash.value.toUpperCase(),hash.value.slice(1)])expect(()=>catalogHash({...hash,value})).toThrow('AGENT-CATALOG-HASH-FORM-REFUSED');
 });
 it('constructs without any native call or timer',()=>{const {invoke}=setup();expect(invoke).not.toHaveBeenCalled();});
 it('keeps private authority outside tool responses and records actual before delivery',async()=>{
  vi.useFakeTimers();const {session,sent}=setup();await session.start('revision');await session.poll();await drain();
  const publish=sent.find(v=>v.kind==='publish_actual')!;expect(publish).toBeDefined();
  expect(String(publish.outcome)).not.toContain('private-owner-capability');
  expect(sent.findIndex(v=>v.kind==='publish_actual')).toBeLessThan(sent.findIndex(v=>v.kind==='complete'));
  expect(session.actual('invented-session:1')).toBeDefined();await session.close();
 });
 it('returns bounded source-unit pages with negative zero preserved',async()=>{
  vi.useFakeTimers();const {session,sent,call}=setup();call('swbpipe_read_nodes',{page:{cursor:null,limit:50}});
  await session.start('revision');await session.poll();await drain();
  const raw=sent.find(v=>v.kind==='publish_actual')!.outcome as string;
  expect(raw).toContain('"x":-0');expect(JSON.parse(raw).data.nodes).toHaveLength(1);await session.close();
 });
 it('rechecks the workspace after asynchronous validation before queue registration',async()=>{
  vi.useFakeTimers();const {session,owner,call,edit}=setup();const gate=deferred<unknown>();mocks.validate.mockReturnValueOnce(gate.promise);
  call('swbpipe_propose_operations',{operations:[{operation_id:'operation-1'}],assumptions:[]});
  await session.start('revision');await session.poll();await drain();edit();gate.resolve({validation:{batch_validation_status:'passed'}});await drain();
  expect(owner.register).not.toHaveBeenCalled();expect(JSON.parse(session.actual('invented-session:1')!.outcome).status).toBe('stale_basis');await session.close();
 });
 it('stamps proposal attribution and retains late actual after close during registration',async()=>{
  vi.useFakeTimers();const {session,owner,call}=setup();mocks.validate.mockResolvedValueOnce({validation:{batch_validation_status:'passed'}});
  const gate=deferred<string|null>();vi.mocked(owner.register).mockReturnValueOnce(gate.promise);
  call('swbpipe_propose_operations',{operations:[{operation_id:'operation-1',author_type:'human',source:{source_ref:'forged'},validation:{application_status:'applied'}}],assumptions:[]});
  await session.start('revision');await session.poll();await drain();const closing=session.close();gate.resolve('actual-batch-key');await closing;
  const [batch,context]=vi.mocked(owner.register).mock.calls[0];
  expect(batch.operations[0].author_type).toBe('agent');expect(batch.operations[0].source?.source_ref).toBe('invented-session:1');
  expect(context.threadId).toBe('thread-1');expect(JSON.parse(session.actual('invented-session:1')!.outcome).status).toBe('pending_review');
 });
 it('binds the actual solve receipt to its evaluated basis after a live edit',async()=>{
  vi.useFakeTimers();const {session,owner,call,edit,sent}=setup();const gate=deferred<AgentRunReceipt|undefined>();vi.mocked(owner.solve).mockReturnValueOnce(gate.promise);
  call('swbpipe_solve');await session.start('revision');await session.poll();await drain();edit();
  gate.resolve({jobId:'job-1',runId:'run-1',modelHash:engineHash,solverMode:'sparse_interactive',health:'ok'});await drain();
  const actual=JSON.parse(session.actual('invented-session:1')!.outcome);expect(actual.basis.modelRevision).toBe(1);expect(actual.data.runId).toBe('run-1');
  expect(sent.find(v=>v.kind==='publish_actual')!.proof).toMatchObject({nativeJobId:'job-1',status:'completed'});await session.close();
 });
 it('tells the agent when a solve treated bends awaiting the person\'s k as straight chords',async()=>{
  vi.useFakeTimers();const {session,owner,call,model}=setup();
  (model as unknown as Record<string,unknown>).components=[{id:'component:b1',kind:'bend'},{id:'component:t1',kind:'tee'}];
  vi.mocked(owner.solve).mockResolvedValueOnce({jobId:'job-1',runId:'run-1',modelHash:engineHash,solverMode:'sparse_interactive',health:'ok'});
  call('swbpipe_solve');await session.start('revision');await session.poll();await drain();
  const message=JSON.parse(session.actual('invented-session:1')!.outcome).message;
  expect(message).toContain('component:b1');expect(message).toContain('straight chords');expect(message).toContain('k does not affect chord stiffness');expect(message).not.toContain('component:t1');
  expect(message).toContain('None has a supplied scalar SIF, so no intensified measure is published');expect(message).not.toContain('applies to');
  await session.close();
 });
 it('says a scalar SIF applies only to chords that have one',async()=>{
  vi.useFakeTimers();const {session,owner,call,model}=setup();
  (model as unknown as Record<string,unknown>).components=[{id:'component:b1',kind:'bend',modifiers:{sif_user_value:{value:1.5,unit:'none'}}},{id:'component:b2',kind:'bend',modifiers:{sif_user_value:{value:0,unit:'none'}}}];
  vi.mocked(owner.solve).mockResolvedValue({jobId:'job-1',runId:'run-1',modelHash:engineHash,solverMode:'sparse_interactive',health:'ok'});
  call('swbpipe_solve');await session.start('revision');await session.poll();await drain();
  let message:string=JSON.parse(session.actual('invented-session:1')!.outcome).message;
  expect(message).toContain('A supplied scalar SIF applies to the other chords; no scalar SIF was supplied for 1 of them (component:b2)');
  await session.close();
  (model as unknown as Record<string,unknown>).components=[{id:'component:b1',kind:'bend',modifiers:{sif_user_value:{value:1.5,unit:'none'}}}];
  call('swbpipe_solve',{},'invented-session:2');await session.start('revision');await session.poll();await drain();
  message=JSON.parse(session.actual('invented-session:2')!.outcome).message;
  expect(message).toContain('Each has a supplied scalar SIF, which applies to its chord.');await session.close();
 });
 it('keeps summary and both solve messages inside the catalog bounds for long identifiers',async()=>{
  vi.useFakeTimers();const {session,owner,call,model}=setup();
  const long=(i:number)=>`component:${String(i).padStart(3,'0')}${'x'.repeat(147)}`;
  (model as unknown as Record<string,unknown>).components=[{id:`component:${'y'.repeat(200)}`,kind:'tee'},...Array.from({length:40},(_,i)=>({id:long(i),kind:'bend'}))];
  await session.start('revision');await session.poll();await drain();
  const summary=JSON.parse(session.actual('invented-session:1')!.outcome).data.componentsAwaitingUserModifiers;
  expect(summary.count).toBe(41);expect(summary.ids).toHaveLength(32);expect(summary.ids.every((id:string)=>id.length<=160)).toBe(true);
  await session.close();
  vi.mocked(owner.solve).mockResolvedValueOnce({jobId:'job-1',runId:'run-1',modelHash:engineHash,solverMode:'sparse_interactive',health:'ok'});
  call('swbpipe_solve',{},'invented-session:2');await session.start('revision');await session.poll();await drain();
  const chord=JSON.parse(session.actual('invented-session:2')!.outcome);
  expect(chord.status).toBe('completed');expect(chord.message.length).toBeLessThanOrEqual(1000);expect(chord.message).toContain(long(0));expect(chord.message).toContain('…');
  await session.close();
  (model as unknown as Record<string,unknown>).pressure_contract={version:'3.0.0',mode:'exact_pressure_v3',shear_model:'euler_bernoulli'};
  call('swbpipe_solve',{},'invented-session:3');await session.start('revision');await session.poll();await drain();
  const exact=JSON.parse(session.actual('invented-session:3')!.outcome);
  expect(exact.status).toBe('unavailable');expect(exact.message.length).toBeLessThanOrEqual(1000);expect(exact.message).toContain('…');
  await session.close();
 });
 it('refuses to solve on the exact route while a bend is unrealized, naming it',async()=>{
  vi.useFakeTimers();const {session,owner,call,model}=setup();
  Object.assign(model as unknown as Record<string,unknown>,{pressure_contract:{version:'3.0.0',mode:'exact_pressure_v3',shear_model:'euler_bernoulli'},components:[{id:'component:b1',kind:'bend'},{id:'component:b2',kind:'bend',mechanics_interface:{solver_consumption:'curved_bend_macro_element'}}]});
  call('swbpipe_solve');await session.start('revision');await session.poll();await drain();
  const outcome=JSON.parse(session.actual('invented-session:1')!.outcome);
  expect(outcome.status).toBe('unavailable');expect(outcome.message).toContain('component:b1');expect(outcome.message).not.toContain('component:b2');
  expect(owner.solve).not.toHaveBeenCalled();await session.close();
 });
 it('never retries a repeated notice and closes on project replacement',async()=>{
  vi.useFakeTimers();const {session,owner,retire,call}=setup();call('swbpipe_solve');await session.start('revision');await session.poll();await drain();await session.poll();await drain();
  expect(owner.solve).toHaveBeenCalledOnce();retire();await session.poll();await expect(session.text('invented')).rejects.toThrow('AGENT-CLOSED');
 });
 it('interrupts only the current native turn without withdrawing an older pending proposal',async()=>{
  vi.useFakeTimers();const {session,owner,call}=setup();mocks.validate.mockResolvedValue({validation:{batch_validation_status:'passed'}});
  vi.mocked(owner.register).mockResolvedValueOnce('first-key').mockResolvedValueOnce('second-key');
  call('swbpipe_propose_operations',{operations:[{operation_id:'operation-1'}],assumptions:[]});
  await session.start('revision');await session.poll();await drain();
  call('swbpipe_propose_operations',{operations:[{operation_id:'operation-2'}],assumptions:[]},'invented-session:2','turn-2');
  await session.poll();await drain();await session.interrupt();
  expect(owner.withdraw).toHaveBeenCalledExactlyOnceWith('second-key');await session.close();
 });

 it('does not let a poll answered after Stop reopen the closed view',async()=>{
  vi.useFakeTimers();const {session,invoke}=setup();const baseline=invoke.getMockImplementation()!;
  const late=deferred<unknown>();
  invoke.mockImplementation(async request=>request.kind==='poll'?late.promise:baseline(request));
  let last:import('./embeddedAgentSession').AgentSessionView|undefined;const remove=session.subscribe(view=>{last=view;});
  await session.start('revision');
  const pending=session.poll();await drain();
  await session.close();
  expect(last).toMatchObject({closed:true,turnActive:false});
  late.resolve({status:'ready',notices:[],messages:[{itemId:'late',kind:'final',text:'late'}],closed:false,turnActive:true,turnStatus:'in_progress'});
  expect(await pending).toBeNull();
  expect(last).toMatchObject({closed:true,turnActive:false});expect(last!.messages).toEqual([]);
  remove();
 });
 it('uses final message standing to replace deltas and keeps transcript eviction separate',async()=>{
  vi.useFakeTimers();const {session,invoke}=setup();const baseline=invoke.getMockImplementation()!;
  let frame:Record<string,unknown>={status:'ready',closed:false,notices:[],messages:[]};
  invoke.mockImplementation(async request=>request.kind==='poll'?frame:baseline(request));
  let last:import('./embeddedAgentSession').AgentSessionView|undefined;const remove=session.subscribe(view=>{last=view;});
  await session.start('revision');
  for(const [kind,text] of [['delta','Hello'],['delta',' model'],['final','Hello model']]){
   frame={...frame,messages:[{itemId:'answer',kind,text}]};await session.poll();
  }
  expect(last!.messages.map(message=>message.text)).toEqual(['Hello model']);
  frame={...frame,messages:[{itemId:'large',kind:'final',text:'x'.repeat(65000)}]};await session.poll();
  frame={...frame,messages:[{itemId:'new',kind:'final',text:'y'.repeat(1000)}]};await session.poll();
  expect(last!.truncated).toBe(true);expect(last!.messages).toHaveLength(1);remove();await session.close();
 });

 it('reports the admitted kinds, project identity and the exact pressure-profile before-text',async()=>{
  vi.useFakeTimers();const {session,sent,model}=setup();await session.start('revision');await session.poll();await drain();
  let data=JSON.parse(sent.filter(v=>v.kind==='publish_actual').at(-1)!.outcome as string).data;
  expect(data).toMatchObject({projectId:'invented',schemaVersion:'0.8.0',pressureContract:null,pressureProfileBefore:'{"schema_version":"0.8.0"}'});
  expect(data.admittedOperationKinds).toContain('insert/Component/insert_component_symbol');expect(data.admittedOperationKinds).toHaveLength(16);expect(data.componentsAwaitingUserModifiers).toEqual({count:0,ids:[]});
  await session.close();
  (model as unknown as Record<string,unknown>).pressure_contract={version:'3.0.0',mode:'exact_pressure_v3',shear_model:'euler_bernoulli'};
  await session.start('revision');await session.poll();await drain();
  data=JSON.parse(sent.filter(v=>v.kind==='publish_actual').at(-1)!.outcome as string).data;
  expect(data.pressureProfileBefore).toBe('{"pressure_contract":{"mode":"exact_pressure_v3","shear_model":"euler_bernoulli","version":"3.0.0"},"schema_version":"0.8.0"}');
  await session.close();
 });
 it('pages records with exact before texts and binds the cursor to its family',async()=>{
  vi.useFakeTimers();const {session,call,model}=setup();
  (model as unknown as Record<string,unknown>).supports=[{id:'support:a',label:' Anchor A ',node:'node-1',restraints:['UX'],family:'anchor',provenance:'p'},{id:'support:b',label:'Guide B',node:'node-1',restraints:['UZ'],provenance:'p'}];
  call('swbpipe_read_records',{family:'supports',page:{cursor:null,limit:1}});await session.start('revision');await session.poll();await drain();
  const first=JSON.parse(session.actual('invented-session:1')!.outcome).data;
  expect(first.records).toHaveLength(1);expect(first.records[0].id).toBe('support:a');
  expect(first.records[0].before.delete).toBe('Anchor A');
  expect(first.records[0].before.configuration).toBe('{"family":"anchor","provenance":"p","restraints":["UX"]}');
  expect(first.nextCursor).toEqual(expect.any(String));
  call('swbpipe_read_records',{family:'supports',page:{cursor:first.nextCursor,limit:1}},'invented-session:2');await session.poll();await drain();
  const second=JSON.parse(session.actual('invented-session:2')!.outcome).data;expect(second.records[0].id).toBe('support:b');expect(second.nextCursor).toBeNull();
  call('swbpipe_read_records',{family:'nodes',page:{cursor:first.nextCursor,limit:1}},'invented-session:3');await session.poll();await drain();
  expect(JSON.parse(session.actual('invented-session:3')!.outcome).status).toBe('execution_error');
  call('swbpipe_read_records',{family:'nodes',page:{cursor:null,limit:5}},'invented-session:4');await session.poll();await drain();
  const nodes=JSON.parse(session.actual('invented-session:4')!.outcome).data;expect(Object.keys(nodes.records[0].before)).toEqual(['delete']);expect(nodes.records[0].before.delete).toBe('N1; x=0; y=1; z=2');
  await session.close();
 });
 it('bounds record pages in UTF-8 bytes and never cuts an oversized first entry',async()=>{
  vi.useFakeTimers();const {session,call,model}=setup();
  const records=model as unknown as Record<string,unknown>;
  // 6000 three-byte characters: under 16384 UTF-16 units, over 16384 bytes.
  records.supports=[{id:'support:wide',label:'€'.repeat(6000),node:'node-1',restraints:['UX'],provenance:'p'}];
  call('swbpipe_read_records',{family:'supports',page:{cursor:null,limit:5}});await session.start('revision');await session.poll();await drain();
  let outcome=JSON.parse(session.actual('invented-session:1')!.outcome);expect(outcome.status).toBe('unavailable');expect(outcome.message).toContain('support:wide');
  // Two records of about 30 KB each: the page holds one and resumes at the next.
  records.supports=[0,1].map(i=>({id:`support:${i}`,label:'€'.repeat(5000),node:'node-1',restraints:['UX'],provenance:'p'}));
  call('swbpipe_read_records',{family:'supports',page:{cursor:null,limit:5}},'invented-session:2');await session.poll();await drain();
  outcome=JSON.parse(session.actual('invented-session:2')!.outcome);expect(outcome.data.records.map((r:{id:string})=>r.id)).toEqual(['support:0']);expect(outcome.data.nextCursor).toEqual(expect.any(String));
  expect(outcome.data.records[0].before.delete).toBe('€'.repeat(5000));
  // Each text fits 16 KiB, but escaping makes the single entry larger than a page.
  records.supports=[{id:'support:quoted',label:'"'.repeat(3900),node:'node-1',restraints:['UX'],provenance:'"'.repeat(3900)}];
  call('swbpipe_read_records',{family:'supports',page:{cursor:null,limit:5}},'invented-session:3');await session.poll();await drain();
  outcome=JSON.parse(session.actual('invented-session:3')!.outcome);expect(outcome.status).toBe('unavailable');expect(outcome.message).toContain('support:quoted');
  await session.close();
 });
 it('filters result pages by kind and entity and binds the filter to the cursor',async()=>{
  vi.useFakeTimers();const {session,owner,call,sent,setResult}=setup();
  const rows=Array.from({length:60},(_,i)=>({id:`r${i}`,kind:i%2?'support_reaction_component_v2':'global_nodal_displacement_x',entity_ref:i%4<2?'support:a':'node:c',unit:'N',value:i}));
  setResult({run_id:'run-1',results:rows} as unknown as MechanicsResult);
  vi.mocked(owner.solve).mockResolvedValueOnce({jobId:'job-1',runId:'run-1',modelHash:engineHash,solverMode:'sparse_interactive',health:'ok'});
  call('swbpipe_solve');await session.start('revision');await session.poll();await drain();
  const runHandle=JSON.parse(session.actual('invented-session:1')!.outcome).data.runHandle;
  const filter={kinds:['support_reaction_component_v2'],entityRefs:['support:a']};
  call('swbpipe_read_results',{runHandle,page:{cursor:null,limit:50},filter},'invented-session:2');await session.poll();await drain();
  const page=JSON.parse(session.actual('invented-session:2')!.outcome).data;
  expect(page.values.map((v:{id:string})=>v.id)).toEqual(rows.filter(r=>r.kind==='support_reaction_component_v2'&&r.entity_ref==='support:a').map(r=>r.id));
  expect(page.nextCursor).toBeNull();
  call('swbpipe_read_results',{runHandle,page:{cursor:null,limit:10}},'invented-session:3');await session.poll();await drain();
  const first=JSON.parse(session.actual('invented-session:3')!.outcome).data;expect(first.values).toHaveLength(10);expect(first.nextCursor).toEqual(expect.any(String));
  call('swbpipe_read_results',{runHandle,page:{cursor:first.nextCursor,limit:10},filter},'invented-session:4');await session.poll();await drain();
  expect(JSON.parse(session.actual('invented-session:4')!.outcome).status).toBe('execution_error');
  expect(sent.some(v=>v.kind==='complete')).toBe(true);await session.close();
 });

});
