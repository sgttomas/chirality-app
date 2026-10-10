import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync,mkdtempSync,rmSync} from 'node:fs';
import {spawnSync} from 'node:child_process';
import {tmpdir} from 'node:os';
import {join} from 'node:path';
import {fileURLToPath} from 'node:url';
import {createRequire} from 'node:module';
import ts from 'typescript';
import React from 'react';
import {renderToStaticMarkup} from 'react-dom/server';
import {localRequire} from './support/load-src.mjs';
const url=new URL('../src/ConnectorSourcePanel.tsx',import.meta.url);
const compiled=ts.transpileModule(readFileSync(url,'utf8'),{compilerOptions:{module:ts.ModuleKind.CommonJS,jsx:ts.JsxEmit.ReactJSX}});
const reconstructionUrl=new URL('../src/ConnectorReconstruction.tsx',import.meta.url);
const reconstructionCode=ts.transpileModule(readFileSync(reconstructionUrl,'utf8'),{compilerOptions:{module:ts.ModuleKind.CommonJS,jsx:ts.JsxEmit.ReactJSX}}).outputText;
const reconstructionExports={};new Function('require','exports',reconstructionCode)(localRequire(createRequire(reconstructionUrl)),reconstructionExports);
const connectedRequire=name=>name==='./ConnectorReconstruction'?reconstructionExports:localRequire(createRequire(url))(name);
const exports={};new Function('require','exports',compiled.outputText)(connectedRequire,exports);
const {SourceObservationView,ConnectorSourcePanel,sourceUiTransition,emptySourceUi}=exports;
const question={id:'Q-fixture',text:'What can be read?',askedRevision:'typed-commit',sinceRevision:'typed-since'};
const view={question,trigger:{kind:'absent',standing:'constructed caller context'},operation:'observed',gaps:[{reason:'Revision unverified',effect:'No source/account',responsible:null}],limits:['No continuous pathname guarantee','No coherent historical revision'],dutiesStanding:'Unperformed/outstanding; no duty authored',observation:{reference:'opaque',question,historical:false,read:{displayPath:'fixture.txt',selectedPath:{encoding:'fixture'},openedFileIdentity:{inode:'18446744073709551615'},text:'<script>do not run</script>\r\né\n',sha256:'host-buffer-hash',byteLength:32,lineCount:2,observedAt:'fixture-time',timeProvenance:'fixture-only',mechanism:'injected picker fixture, not person evidence',mutationLimit:'Transient writes can evade metadata checks'},revision:{kind:'unavailable',limit:'No revision evidence supplied'},anchors:[{reference:'anchor-id',anchor:'L1',byteStart:0,byteEnd:3,interval:'zero-based half-open',text:'é\n',sha256:'excerpt-hash',standing:'Inclusion only, not truth'}]}};
const state=(v=view)=>({view:v,busy:false,error:null,draftChanged:false});
const render=s=>renderToStaticMarkup(React.createElement(SourceObservationView,{state:s}));
test('source content, anchors, read limits and gaps remain escaped and separate',()=>{
 const html=render(state());
 for(const text of ['Q-fixture','typed-commit','typed-since','Revision unverified','Unassigned','Transient writes','No coherent historical revision','host-buffer-hash','excerpt-hash','[0, 3)','Inclusion only','18446744073709551615'])assert.ok(html.includes(text),text);
 assert.ok(html.includes('&lt;script&gt;'));assert.ok(!html.includes('<script>'));assert.ok(!html.includes('<a '));assert.ok(html.includes('\\r\\n'));
 assert.match(html,/This local snapshot is not a Git binding/);assert.match(html,/No source entry or saved route account is produced/);
});
test('every revision treatment retains unverified provenance and typed hashes cannot promote it',()=>{
 for(const kind of ['unavailable','caller_assertion','source_text_located']){
  const v=structuredClone(view);v.observation.revision={kind,label:'0123456789abcdef',callerInterpretation:'Caller meaning',limit:'Unverified assertion; not Git evidence',...(kind==='source_text_located'?{anchor:{anchor:'L1'}}:{})};
  const html=render(state(v));assert.ok(html.includes(kind));assert.match(html,/not Git evidence/);assert.match(html,/working-tree coincidence does not establish a Git revision/);
 }
});
test('cancel, pending, failure and edited question label old snapshot historical with unchanged read time',()=>{
 for(const change of [{view:{...view,operation:'cancelled',observation:{...view.observation,historical:true}}},{busy:true},{error:'read failed'},{draftChanged:true}]){
  const html=render({...state(),...change});assert.match(html,/Prior\/historical observation/);assert.match(html,/fixture-time/);assert.match(html,/Frozen question: Q-fixture/);
 }
 const next=sourceUiTransition(state(),{type:'prepare'});assert.equal(next.view,null);
 const fail=sourceUiTransition(sourceUiTransition(state(),{type:'start'}),{type:'failure',error:'failure'});assert.equal(fail.view,view);assert.match(render(fail),/prior\/historical/);
 assert.equal(sourceUiTransition(state(),{type:'edit'}).draftChanged,true);
 assert.equal(sourceUiTransition(emptySourceUi,{type:'success',view}).draftChanged,false);
});
test('constructed trigger variants preserve question and gaps; assignments are never performed duties',()=>{
 for(const kind of ['absent','stale','partial','failing']){
  const v=structuredClone(view);v.trigger.kind=kind;v.gaps[0].responsible='Caller assigned manager';
  const html=render(state(v));assert.match(html,/What can be read\?/);assert.match(html,/Revision unverified/);assert.match(html,/caller assignment, not performed responsibility/);assert.match(html,/Unperformed\/outstanding/);
 }
});
test('unavailable association disables preparation/selection and exposes no file path/body input',()=>{
 const html=renderToStaticMarkup(React.createElement(ConnectorSourcePanel,{availability:{enabled:false,reason:'No explicit project'},command(){throw Error('render must not invoke');}}));
 assert.match(html,/No explicit project/);assert.ok((html.match(/<button disabled=""/g)||[]).length>=2);
 assert.ok(!html.includes('type="file"'));assert.ok(!html.includes('name="path"'));assert.match(html,/262144/);assert.match(html,/no NUL or symlink descendants/);
});

test('historical excerpts retain separately labeled unresolved read and excerpt causes',()=>{
 const v=structuredClone(view);v.operation='failed';v.observation.historical=true;
 v.gaps.push({kind:'Selection/read',reason:'DISTINCT_READ_FAILURE',effect:'No new source observation',responsible:null},{kind:'Excerpt',reason:'Expected excerpt mismatch',effect:'No new anchor',responsible:null});
 const html=render(state(v));for(const value of ['Selection/read gap','DISTINCT_READ_FAILURE','Excerpt gap','Expected excerpt mismatch','No new source observation','No new anchor'])assert.ok(html.includes(value),value);
 assert.match(html,/Prior\/historical observation/);assert.match(html,/fixture-time/);
});

test('Git sides and gaps render separately without promoting local text, and historical failure persists',()=>{
 const v=structuredClone(view);v.git={operation:'failed',error:'deadline after at side; new result discarded',result:{historical:true,reference:'git-observation',observation:{status:'partial',at:{status:'Git-object-verified',object:{readCommit:'exact-commit',blob:'exact-blob',sha256:'blob-hash',byteLength:5,text:'<script>committed</script>',standing:'same-engine consistency only'}},since:{status:'gap',kind:'missing',reason:'promised object unavailable'},limits:['Not source truth or authorship','No semantic conclusion'],association:{externalMetadata:true},engine:{mechanism:'restricted Git'}},anchors:[{reference:'git-anchor',side:'at',anchor:'L1',byteStart:0,byteEnd:5,commit:'exact-commit',blob:'exact-blob',text:'text',standing:'Inclusion only'}]}};
 const html=render(state(v));for(const text of ['Prior/historical Git result','partial','exact-commit','exact-blob','blob-hash','promised object unavailable','deadline after at side','Not source truth','No semantic conclusion','Local text snapshot','Checked Git excerpts'])assert.ok(html.includes(text),text);
 assert.ok(html.includes('&lt;script&gt;committed'));assert.ok(!html.includes('<script>'));assert.ok(!html.includes('Frozen Git result'));
 v.git.result.observation.at={status:'gap',kind:'type',reason:'not a commit'};v.git.result.observation.status='gaps-only';assert.match(render(state(v)),/gaps-only/);
});
test('actual panel handlers send only opaque session and pin/side arguments, with a separate cancellation action',async()=>{
 let cursor=0;const slots=[];const localExports={};const require=connectedRequire;
 new Function('require','exports',compiled.outputText)(name=>name==='react'?{...React,useRef(initial){const i=cursor++;if(!(i in slots))slots[i]={current:initial};return slots[i];},useState(initial){const i=cursor++;if(!(i in slots))slots[i]=typeof initial==='function'?initial():initial;return[slots[i],value=>{slots[i]=typeof value==='function'?value(slots[i]):value;}];}}:require(name),localExports);
 const calls=[];let pendingRead;
 const observed={...structuredClone(view),sessionToken:'host-private-token',generation:'host-generation'};
 const gitView={...observed,git:{operation:'completed',result:{reference:'host-git-reference',historical:false,observation:{status:'complete',at:{status:'Git-object-verified',object:{text:'committed'}}},anchors:[]}}};
 const command=async(name,args)=>{calls.push({name,args});if(name==='read_connector_git')return await new Promise(resolve=>{pendingRead=resolve;});return name==='anchor_connector_git'?gitView:name==='cancel_connector_git'?{...gitView,git:{...gitView.git,operation:'cancelled',result:{...gitView.git.result,historical:true}}}:observed;};
 const draw=()=>{cursor=0;return localExports.ConnectorSourcePanel({availability:{enabled:true},command});};
 const nodes=(node,out=[])=>{if(Array.isArray(node)){for(const n of node)nodes(n,out);}else if(node&&typeof node==='object'){out.push(node);nodes(node.props?.children,out);}return out;};
 const button=(tree,label)=>nodes(tree).find(n=>n.type==='button'&&n.props.children===label);
 await button(draw(),'Prepare question').props.onClick();
 await button(draw(),'Select / reread through native picker…').props.onClick();
 const labels=nodes(draw()).filter(n=>n.type==='label');
 for(const [title,value] of [['At commit','a'.repeat(40)],['Since commit (optional)','b'.repeat(40)]]){
   const label=labels.find(n=>Array.isArray(n.props.children)&&n.props.children[0]===title);label.props.children[1].props.onChange({target:{value}});
 }
 const work=button(draw(),'Read Git objects').props.onClick();
 assert.deepEqual(calls.at(-1),{name:'read_connector_git',args:{sessionToken:'host-private-token',generation:'host-generation',observationReference:'opaque',at:'a'.repeat(40),since:'b'.repeat(40)}});
 await button(draw(),'Cancel Git request').props.onClick();assert.equal(calls.at(-1).name,'cancel_connector_git');assert.deepEqual(Object.keys(calls.at(-1).args).sort(),['generation','sessionToken']);
 pendingRead(gitView);await work;
 const displayed=nodes(draw()).find(n=>n.type===localExports.SourceObservationView);assert.equal(displayed.props.state.view.git.operation,'cancelled');assert.equal(displayed.props.state.view.git.result.historical,true,'late read must not overwrite cancellation');
 await button(draw(),'Locate exact Git lines').props.onClick();assert.deepEqual(calls.at(-1),{name:'anchor_connector_git',args:{sessionToken:'host-private-token',generation:'host-generation',observationReference:'host-git-reference',side:'at',start:1,end:1,expected:null}});
 assert.ok(calls.every(c=>!('path' in c.args)&&!('root' in c.args)&&!('text' in c.args)));
});
test('draft handlers freeze only explicit refs/claims and keep actual publication result after cancellation reply',async()=>{
 let cursor=0;const slots=[];const localExports={};const require=connectedRequire;
 new Function('require','exports',compiled.outputText)(name=>name==='react'?{...React,useEffect(){},useRef(initial){const i=cursor++;if(!(i in slots))slots[i]={current:initial};return slots[i];},useState(initial){const i=cursor++;if(!(i in slots))slots[i]=typeof initial==='function'?initial():initial;return[slots[i],value=>{slots[i]=typeof value==='function'?value(slots[i]):value;}];}}:require(name),localExports);
 const calls=[];let finishPublish;
 const source=state({...view,sessionToken:'session',generation:'generation',git:{operation:'completed',result:{reference:'git-ref',historical:false,observation:{at:{status:'Git-object-verified',object:{reference:'side-ref',readCommit:'commit'}},since:null},anchors:[]}}});
 const frozen={revision:'1',used:1,capacity:64,entries:[{token:'draft-token',generation:'draft-generation',accountId:'ra:fixture',status:'prepared',draft:{byteLength:500,sha256:'frozen-hash',account:{question:{text:'Frozen question',at_revision:'commit'},sources:[],interpretations:[],gaps:[],duties:[]}},outcomeText:'null',reconciliationText:'null'}]};
 const publishing={...frozen,revision:'2',inflight:'draft-token',entries:[{...frozen.entries[0],status:'publishing',draft:null}]};
 const published={...frozen,revision:'3',entries:[{...frozen.entries[0],status:'published',draft:null,outcomeText:'Exact actual binding'}]};
 const command=async(name,args)=>{calls.push({name,args});if(name==='publish_connector_draft')return new Promise(resolve=>{finishPublish=resolve;});return name==='cancel_connector_draft'?publishing:frozen;};
 const draw=()=>{cursor=0;return localExports.ConnectorDraftPanel({source,availability:{enabled:true},command});};
 const nodes=(node,out=[])=>{if(Array.isArray(node))node.forEach(n=>nodes(n,out));else if(node&&typeof node==='object'){out.push(node);nodes(node.props?.children,out);}return out;};
 const button=(label)=>nodes(draw()).find(n=>n.type==='button'&&n.props.children===label);
 const setLabel=(label,value)=>{const n=nodes(draw()).find(n=>n.type==='label'&&Array.isArray(n.props.children)&&n.props.children[0]===label);n.props.children[1].props.onChange({target:{value}});};
 assert.equal(nodes(draw()).filter(n=>n.type==='select'&&n.props.value==='').length,4,'connector and all duties require explicit input');
 setLabel('Constructed connector label','pec');
 const include=nodes(draw()).find(n=>n.type==='label'&&Array.isArray(n.props.children)&&n.props.children[1]==='Include this successfully observed side');include.props.children[0].props.onChange({target:{checked:true}});
 setLabel('Intended source role (caller assertion)','Caller purpose');
 for(const duty of ['locate_compare','review_integrate','cross_undertaking_coordination']){
   const field=()=>nodes(draw()).find(n=>n.type==='fieldset'&&n.props.children?.[0]?.type==='legend'&&n.props.children[0].props.children?.[0]===duty);
   nodes(field()).find(n=>n.type==='select').props.onChange({target:{value:'outstanding'}});
   nodes(field()).find(n=>n.type==='input').props.onChange({target:{value:'Explicit outstanding reason'}});
 }
 await button('Freeze draft for inspection').props.onClick();
 const input=calls.at(-1).args.input;assert.equal(input.gitReference,'git-ref');assert.equal(input.sessionToken,'session');assert.deepEqual(input.sources,[{reference:'side-ref',role:'Caller purpose',anchors:[]}]);assert.ok(input.duties.every(d=>d.standing==='outstanding'&&d.reason==='Explicit outstanding reason'));assert.ok(!('account' in input)&&!('path' in input)&&!('recorder' in input));
 const write=button('Publish this frozen draft once').props.onClick();assert.deepEqual(calls.at(-1).args,{token:'draft-token',generation:'draft-generation'});
 await button('Cancel draft (started publication may finish)').props.onClick();finishPublish(published);await write;
 const html=renderToStaticMarkup(draw());assert.match(html,/published/);assert.match(html,/Exact actual binding/);assert.ok(!html.includes('Publish this frozen draft once'));
 assert.equal(localExports.acceptDraftReply(published,publishing),published,'stale cancellation reply cannot replace actual newer result');
});
test('record-comparison handler carries explicit references and edits invalidate the frozen token',async()=>{
 let cursor=0;const slots=[];const local={};new Function('require','exports',compiled.outputText)(name=>name==='react'?{...React,useEffect(){},useRef(initial){const i=cursor++;if(!(i in slots))slots[i]={current:initial};return slots[i];},useState(initial){const i=cursor++;if(!(i in slots))slots[i]=typeof initial==='function'?initial():initial;return[slots[i],v=>slots[i]=typeof v==='function'?v(slots[i]):v];}}:connectedRequire(name),local);
 const calls=[];const source=state({...view,sessionToken:'private-session',generation:'private-generation',git:{operation:'completed',result:{reference:'git-reference',historical:false,observation:{at:{status:'Git-object-verified',object:{reference:'at-ref',readCommit:'at-pin'}},since:{status:'Git-object-verified',object:{reference:'since-ref',readCommit:'since-pin'}}},anchors:[{reference:'at-anchor',side:'at',sideObservationReference:'at-ref',anchor:'L1',text:'after'},{reference:'since-anchor',side:'since',sideObservationReference:'since-ref',anchor:'L1',text:'before'}]}}});
 const response={revision:'1',used:1,capacity:64,entries:[{token:'frozen',generation:'frozen-generation',status:'prepared',accountId:'ra:test',draft:null}]};const command=async(name,args)=>{calls.push({name,args});return response;};const draw=()=>{cursor=0;return local.ConnectorDraftPanel({source,availability:{enabled:true},command});};
 const nodes=(x,out=[])=>{if(Array.isArray(x))x.forEach(n=>nodes(n,out));else if(x&&typeof x==='object'){out.push(x);nodes(x.props?.children,out);}return out;};
 const label=(name)=>nodes(draw()).find(x=>x.type==='label'&&x.props.children?.[0]===name);
 label('Account format').props.children[1].props.onChange({target:{value:'0.4'}});
 const data={pairs:[{key:'pair',sinceAnchor:'since-anchor',atAnchor:'at-anchor'}],claims:[{key:'claim',statement:'Record reports a change',assertedBy:'Caller',assertedRole:'agent',scope:'record_change',anchors:['at-anchor'],pairs:['pair']}],contradictions:[],reports:[{key:'local-only',duty:'locate_compare',reportedBy:'Caller',reportedActor:'Reported actor',reportedStatus:'performed',reason:'Unverified',anchors:['at-anchor']}]};
 const fields=()=>nodes(draw()).find(x=>x.type===reconstructionExports.ReconstructionFields);fields().props.onChange(data);
 await nodes(draw()).find(x=>x.type==='button'&&x.props.children==='Freeze draft for inspection').props.onClick();const sent=calls.at(-1);assert.equal(sent.name,'prepare_connector_reconstruction');assert.equal(sent.args.input.draft.sessionToken,'private-session');assert.deepEqual(sent.args.input.pairs,data.pairs);assert.ok(!('key'in sent.args.input.reports[0]));assert.deepEqual(sent.args.input.draft.interpretations,[]);assert.ok(!('facts'in sent.args.input)&&!('account'in sent.args.input)&&!('path'in sent.args.input));
 fields().props.onChange({...data,claims:[{...data.claims[0],statement:'Edited'}]});assert.equal(calls.at(-1).name,'cancel_connector_draft');assert.deepEqual(calls.at(-1).args,{token:'frozen',generation:'frozen-generation'});
 const html=renderToStaticMarkup(React.createElement(reconstructionExports.ReconstructionFields,{value:data,onChange(){},anchors:source.view.git.result.anchors}));assert.match(html,/not prove truth, entailment, authorship, permission or performance/);assert.match(html,/Reported status/);assert.match(html,/Record change/);
});
test('format toggle remount preserves unique pair and claim keys and existing citations',()=>{
 const nodes=(x,out=[])=>{if(Array.isArray(x))x.forEach(n=>nodes(n,out));else if(x&&typeof x==='object'){out.push(x);nodes(x.props?.children,out);}return out;};
 let parentCursor=0,childCursor=0,childSlots=[];const parentSlots=[],child={},parent={};
 new Function('require','exports',reconstructionCode)(name=>name==='react'?{...React,useRef(initial){const i=childCursor++;if(!(i in childSlots))childSlots[i]={current:initial};return childSlots[i];}}:localRequire(createRequire(reconstructionUrl))(name),child);
 new Function('require','exports',compiled.outputText)(name=>name==='./ConnectorReconstruction'?child:name==='react'?{...React,useEffect(){},useRef(initial){const i=parentCursor++;if(!(i in parentSlots))parentSlots[i]={current:initial};return parentSlots[i];},useState(initial){const i=parentCursor++;if(!(i in parentSlots))parentSlots[i]=typeof initial==='function'?initial():initial;return[parentSlots[i],v=>parentSlots[i]=typeof v==='function'?v(parentSlots[i]):v];}}:connectedRequire(name),parent);
 const draw=()=>{parentCursor=0;return parent.ConnectorDraftPanel({source:state(),availability:{enabled:true},command:async()=>({})});};
 const toggle=version=>{nodes(draw()).find(n=>n.type==='label'&&n.props.children?.[0]==='Account format').props.children[1].props.onChange({target:{value:version}});if(version==='0.3')childSlots=[];};
 const element=()=>nodes(draw()).find(n=>n.type===child.ReconstructionFields);
 const fields=()=>{childCursor=0;return child.ReconstructionFields(element().props);};
 const add=label=>nodes(fields()).find(n=>n.type==='button'&&n.props.children===label).props.onClick();
 toggle('0.4');add('Add explicit excerpt pair');add('Add attributed claim');
 let value=element().props.value;const pair=value.pairs[0].key,claim=value.claims[0].key;
 element().props.onChange({...value,claims:[{...value.claims[0],pairs:[pair]}],contradictions:[{key:'retained-conflict',claims:[claim],description:'retained',effect:'unresolved',responsible:{standing:'unassigned',identity:null}}]});
 toggle('0.3');assert.equal(element(),undefined);toggle('0.4');add('Add explicit excerpt pair');add('Add attributed claim');
 value=element().props.value;assert.equal(new Set(value.pairs.map(x=>x.key)).size,2);assert.equal(new Set(value.claims.map(x=>x.key)).size,2);assert.deepEqual(value.claims[0].pairs,[pair]);assert.deepEqual(value.contradictions[0].claims,[claim]);
 element().props.onChange({...value,pairs:value.pairs.slice(1),claims:value.claims.slice(1).map(c=>({...c,pairs:[pair]}))});
 toggle('0.3');toggle('0.4');add('Add explicit excerpt pair');add('Add attributed claim');value=element().props.value;
 assert.ok(value.pairs.every(p=>p.key!==pair));assert.ok(value.claims.every(c=>c.key!==claim));assert.deepEqual(value.contradictions[0].claims,[claim]);
});

function recheckHarness(registry,reply){
 let cursor=0;const slots=[],local={},calls=[];let availability={enabled:true,status:'available',projectReference:'project-one'},pending;const requests=[];
 new Function('require','exports',compiled.outputText)(name=>name==='react'?{...React,useEffect(){},useRef(initial){const i=cursor++;if(!(i in slots))slots[i]={current:initial};return slots[i];},useState(initial){const i=cursor++;if(!(i in slots))slots[i]=typeof initial==='function'?initial():initial;return[slots[i],v=>slots[i]=typeof v==='function'?v(slots[i]):v];}}:connectedRequire(name),local);
 const command=async(name,args)=>{calls.push({name,args});if(name==='inspect_connector_drafts')return registry;return new Promise((resolve,reject)=>{pending={resolve,reject};requests.push(pending);});};
 const draw=()=>{cursor=0;return local.ConnectorDraftPanel({source:emptySourceUi,availability,command});};
 const nodes=(n,out=[])=>{if(Array.isArray(n))n.forEach(x=>nodes(x,out));else if(n&&typeof n==='object'){out.push(n);nodes(n.props?.children,out);}return out;};
 const button=label=>nodes(draw()).find(n=>n.type==='button'&&n.props.children===label);
 return{draw,nodes,button,calls,finish:()=>pending.resolve(reply),finishAt:(index,value)=>requests[index].resolve(value),fail:e=>pending.reject(e),project:value=>availability=value};
}
test('published inspection handler sends only original token/generation, escapes detail and preserves outcome',async()=>{
 const entry={token:'published-token',generation:'published-generation',status:'published',accountId:'ra:fixture',recheckAvailable:true,outcomeText:'Original exact publication binding',reconciliationText:'null'};
 const reply={token:entry.token,generation:entry.generation,inspection:{status:'changed',detail:'<script>untrusted</script>',limit:'No namespace uniqueness'}};
 const h=recheckHarness({entries:[entry],used:1,capacity:64},reply);await h.button('Refresh retained draft outcomes').props.onClick();
 assert.equal(h.button('Recheck this published file').props.disabled,false,'source session absent does not erase published custody');
 const work=h.button('Recheck this published file').props.onClick();assert.deepEqual(h.calls.at(-1),{name:'recheck_published_connector_draft',args:{token:entry.token,generation:entry.generation}});h.finish();await work;
 const html=renderToStaticMarkup(h.draw());assert.match(html,/Original exact publication binding/);assert.match(html,/Current exact-file inspection/);assert.match(html,/&lt;script&gt;/);assert.doesNotMatch(html,/<script>/);assert.match(html,/namespace uniqueness/);
 const failed=h.button('Recheck this published file').props.onClick();h.fail({kind:'busy',detail:'No read queued'});await failed;assert.match(renderToStaticMarkup(h.draw()),/Inspection not completed/);assert.doesNotMatch(renderToStaticMarkup(h.draw()),/untrusted/);
});
test('published inspection late reply is discarded across project change',async()=>{
 const entry={token:'t',generation:'g',status:'published',accountId:'ra:a',recheckAvailable:true,outcomeText:'Original retained result'};
 const h=recheckHarness({entries:[entry]}, {token:'t',generation:'g',inspection:{status:'current_match',detail:'LATE_RESULT'}});await h.button('Refresh retained draft outcomes').props.onClick();const work=h.button('Recheck this published file').props.onClick();
 h.project({enabled:false,status:'absent',projectReference:'another'});h.draw();h.finish();await work;
 assert.doesNotMatch(renderToStaticMarkup(h.draw()),/LATE_RESULT/);assert.match(renderToStaticMarkup(h.draw()),/Original retained result/);assert.equal(h.button('Recheck this published file').props.disabled,true);
});
test('actual host command projection renders both published formats through maintained joined test',async()=>{
 const dir=mkdtempSync(join(tmpdir(),'published-recheck-view-'));
 try{
 const result=spawnSync('cargo',['test','--offline','--locked','--manifest-path','src-tauri/Cargo.toml','--lib','connector_git_guard_tests::connector_published_recheck_actual_appstate_handler_and_project_guards','--','--exact','--test-threads=1'],{cwd:fileURLToPath(new URL('..',import.meta.url)),env:{...process.env,CARGO_NET_OFFLINE:'true',CARGO_INCREMENTAL:'0',CHIRALITY_SKIP_CODEX:'1',C3_PUB_RECHECK_TEST_OUTPUT:dir},encoding:'utf8',timeout:120000});
 assert.equal(result.status,0,result.stderr||result.error?.message);
 for(const version of ['0.3','0.4']){const {registry,reply}=JSON.parse(readFileSync(`${dir}/handler-${version}.json`,'utf8'));assert.equal(reply.inspection.status,'current_match');const h=recheckHarness(registry,reply);await h.button('Refresh retained draft outcomes').props.onClick();const work=h.button('Recheck this published file').props.onClick();h.finish();await work;const html=renderToStaticMarkup(h.draw());assert.match(html,/current_match/);assert.ok(html.includes(reply.inspection.observed.sha256));assert.match(html,/Original publication outcome/);assert.match(html,/namespace uniqueness/);}
 }finally{rmSync(dir,{recursive:true,force:true});}
});

test('published inspection older selected-entry reply cannot replace newer selection',async()=>{
 const entries=['first','second'].map(token=>({token,generation:'g',status:'published',accountId:token,recheckAvailable:true,outcomeText:'Retained '+token}));
 const h=recheckHarness({entries},null);await h.button('Refresh retained draft outcomes').props.onClick();
 const buttons=()=>h.nodes(h.draw()).filter(n=>n.type==='button'&&n.props.children==='Recheck this published file');
 const first=buttons()[0].props.onClick();const second=buttons()[1].props.onClick();
 h.finishAt(1,{token:'second',generation:'g',inspection:{status:'current_match',detail:'SECOND_CURRENT'}});await second;
 h.finishAt(0,{token:'first',generation:'g',inspection:{status:'changed',detail:'FIRST_LATE'}});await first;
 const html=renderToStaticMarkup(h.draw());assert.match(html,/SECOND_CURRENT/);assert.doesNotMatch(html,/FIRST_LATE/);assert.match(html,/Retained first/);assert.match(html,/Retained second/);
});
