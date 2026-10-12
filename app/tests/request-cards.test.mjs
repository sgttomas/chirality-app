import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {createRequire} from 'node:module';
import ts from 'typescript';
import React from 'react';
import {renderToStaticMarkup} from 'react-dom/server';
import {localRequire} from './support/load-src.mjs';

// Each module is transpiled alone; a local import is served from the modules already loaded.
const load=(name,local={})=>{
  const url=new URL(`../src/${name}.tsx`,import.meta.url);
  const compiled=ts.transpileModule(readFileSync(url,'utf8'),{compilerOptions:{module:ts.ModuleKind.CommonJS,target:ts.ScriptTarget.ES2022,jsx:ts.JsxEmit.ReactJSX}});
  const exports={};const base=createRequire(url);
  new Function('require','exports',compiled.outputText)(spec=>local[spec]??localRequire(base)(spec),exports);return exports;
};
const activity=load('NativeActivity');
const cards=load('RequestCards',{'./NativeActivity':activity});
const {NativeRequestCard,WaitingRequestsIndicator,cardState,decisionForms,decisionWords,hostRequests,refusalWords,requestTitle,waitingByConversation,answerable}=cards;

// Invented register records in the host shape (native_requests.rs records()).
const g={appSession:'s',home:'h',spawnCounter:1};
const request=(method,parameters,extra={})=>({recordKind:'server-request-entry',requestIdentity:extra.id??method,generation:g,method,classification:'known-answerable',
  originClass:['item/tool/requestUserInput','mcpServer/elicitation/request'].includes(method)?'person-input':'a14',nativeParameters:parameters,state:'outstanding',replyWriteResult:'not-attempted',acknowledgmentObservation:{status:'not-observed'},...extra});
const at={threadId:'T',turnId:'u',itemId:'i'};
const command=(params={},extra={})=>request('item/commandExecution/requestApproval',{...at,command:'ls -la',cwd:'/work',reason:'List the folder',proposedExecpolicyAmendment:['ls'],...params},extra);
const entry=extra=>command({},extra);
const render=(r,view=null)=>renderToStaticMarkup(React.createElement(NativeRequestCard,{request:r,view,answer:async()=>{}}));
// The App's own words: everything except code spans, quoted supplier text and preformatted native JSON.
const appWords=html=>html.replace(/<pre[\s\S]*?<\/pre>/g,'').replace(/<code>[\s\S]*?<\/code>/g,'').replace(/<q>[\s\S]*?<\/q>/g,'').replace(/<[^>]+>/g,' ');
const A14={
  'item/commandExecution/requestApproval':command({reason:'Needs approval to accept'}),
  'item/fileChange/requestApproval':request('item/fileChange/requestApproval',{...at,reason:'Approve these edits',grantRoot:'/work'}),
  'item/permissions/requestApproval':request('item/permissions/requestApproval',{...at,cwd:'/work',permissions:{network:{enabled:true}},reason:null}),
  execCommandApproval:request('execCommandApproval',{conversationId:'T',callId:'c',command:['rm','x'],cwd:'/work',parsedCmd:[]}),
  applyPatchApproval:request('applyPatchApproval',{conversationId:'T',callId:'c',fileChanges:{'a.txt':{}}}),
};

test('tool-permission cards are titled and read without the raw JSON',()=>{
  const html=render(command());
  assert.match(html,/<h3>Tool permission: run a command<\/h3>/);
  const outside=html.replace(/<details>[\s\S]*?<\/details>/g,'');
  assert.ok(outside.includes('<code>ls -la</code>')&&outside.includes('<code>/work</code>')&&outside.includes('<q>List the folder</q>'),'command, folder and reason are shown readably');
  assert.ok(outside.includes('<b>Waiting for your answer</b>'));
  assert.ok(!/item\/commandExecution\/requestApproval/.test(outside),'the method name is not the title');
  for(const [method,r] of Object.entries(A14)) assert.ok(requestTitle(r).startsWith('Tool permission: '),method);
  assert.equal(requestTitle(request('item/tool/requestUserInput',{...at,questions:[],isBlocking:true})),'Question from the agent');
  // RS §13.9: a records capability call is the App's own answer, not one it leaves unanswered.
  assert.match(requestTitle({...request('item/tool/call',{...at,tool:'chirality_records_read_v1'}),originClass:'named-service'}),/read this project's records/);
  assert.match(requestTitle(request('item/tool/call',{...at,tool:'other'})),/does not answer itself/);
});

test('LB-1/LB-2/LB-3: App words never say accept or approve; the native value is shown beside them',()=>{
  for(const [method,r] of Object.entries(A14)){
    const html=render(r);
    assert.doesNotMatch(appWords(html),/accept|approv/i,`${method}: ${appWords(html)}`);
    assert.match(html,/Tool permission only\..*does not mark anything checked, take the work as done, give engineering sign-off or rely on the result/,method);
  }
  const html=render(command());
  assert.match(html,/Allow once <code>&quot;accept&quot;<\/code>/);
  assert.match(html,/Don&#x27;t allow, and interrupt the turn <code>&quot;cancel&quot;<\/code>/);
  assert.match(html,/Allow, and add the proposed rule to your Codex exec policy <code>/);
  assert.equal(decisionWords('decline'),"Don't allow; the agent continues the turn");
  assert.equal(decisionWords({mystery:1}),'Codex option','an unknown form gets neutral words and keeps its value');
});

test('answer forms and values are exactly the native ones (FO-1…FO-3, unchanged semantics)',()=>{
  const offered=command({availableDecisions:['accept','acceptWithExecpolicyAmendment','cancel']});
  assert.deepEqual(decisionForms(offered).map(f=>f.answer),[{decision:'accept'},{decision:'acceptWithExecpolicyAmendment'},{decision:'cancel'}],'availableDecisions exactly, in order');
  assert.deepEqual(decisionForms(command()).map(f=>f.answer),[{decision:'accept'},{decision:'acceptForSession'},{decision:'decline'},{decision:'cancel'},{decision:{acceptWithExecpolicyAmendment:{execpolicy_amendment:['ls']}}}]);
  assert.deepEqual(decisionForms(command({proposedExecpolicyAmendment:undefined,proposedNetworkPolicyAmendments:[{host:'x',action:'allow'}]})).map(f=>f.answer).slice(4),[{decision:{applyNetworkPolicyAmendment:{network_policy_amendment:{host:'x',action:'allow'}}}}]);
  assert.deepEqual(decisionForms(A14['item/fileChange/requestApproval']).map(f=>f.answer.decision),['accept','acceptForSession','decline','cancel']);
  assert.deepEqual(decisionForms(A14.execCommandApproval).map(f=>f.answer),[{decision:'approved'},{decision:'approved_for_session'},{decision:'abort'},{decision:{denied:{rejection:''}}}],'legacy forms never include timed_out');
  assert.deepEqual(decisionForms(A14['item/permissions/requestApproval']),[],'permission grants keep their own controls');
});

test('classification is unchanged: answer controls only for an outstanding known-answerable request',()=>{
  assert.ok(answerable(command()));
  for(const [extra,why] of [[{state:'answered'},'settled'],[{classification:'known-app-unsupported',originClass:'none',state:'errored'},'unsupported'],[{originClass:'named-service'},'named service'],[{state:'resolved-by-supplier'},'resolved by Codex'],[{state:'ended-unanswered'},'ended']]){
    const r=entry(extra);assert.ok(!answerable(r),why);
    assert.ok(!/<button/.test(render(r)),`${why}: no answer control`);
  }
  assert.ok(/<button/.test(render(command())));
});

test('card states use the person words for each register state (CS)',()=>{
  const cases=[
    [{state:'settling'},'Sending your answer: not yet written to Codex'],
    [{state:'answered'},'Your answer was written to Codex; Codex has not confirmed it'],
    [{state:'answered',acknowledgmentObservation:{status:'observed'}},'Your answer was written; Codex reported the request resolved'],
    [{state:'declined',settlement:{origin:{class:'person-via-interaction'}}},'You declined; written to Codex; Codex has not confirmed it'],
    [{state:'declined',settlement:{origin:{class:'app-rule',ruleName:'on-stop'}}},'Declined by App rule on-stop, not by you'],
    [{state:'settle-write-failed'},'Your answer could not be written; whether Codex received it is unknown'],
    [{state:'resolved-by-supplier',supplierResolution:{source:'serverRequest/resolved'}},'Resolved by Codex before you answered (cause: not reported)'],
    [{state:'ended-unanswered'},'Ended unanswered: the Codex process ended'],
    [{state:'ended-unanswered',endContext:'app-quit'},'Ended unanswered: the Codex process ended when you quit'],
    [{state:'ended-unanswered',endContext:'supplier-exit'},'Ended unanswered: the Codex process ended'],
    [{state:'errored',settlement:{origin:{class:'app-rule',ruleName:'no-dynamic-tools'}}},'Codex asked for something the App does not provide (item/commandExecution/requestApproval): answered with an error by rule no-dynamic-tools'],
  ];
  for(const [extra,words] of cases) assert.equal(cardState(entry(extra)),words);
  assert.equal(refusalWords('already-settled'),'Last answer not taken: already answered (already-settled)');
  assert.equal(refusalWords('generation-closed: closed'),'Last answer not taken: Codex restarted since this was asked (generation-closed: closed)');
});

test('questions and input requests say they are conversation input and offer the act control plainly (LB-4)',()=>{
  const q=request('item/tool/requestUserInput',{...at,isBlocking:false,questions:[{id:'q1',header:'Pick',question:'Which?',options:[{label:'A',description:'first'}],isOther:false,isSecret:false}]});
  const html=render(q);
  assert.match(html,/Your answer goes to the agent as conversation input; it is not a recorded act\./);
  assert.match(html,/<a href="#file-acts">Open the App act control<\/a>/);
  assert.match(html,/Not blocking the turn/);assert.match(html,/Decline to answer/);
  const e=request('mcpServer/elicitation/request',{threadId:'T',turnId:'u',serverName:'srv',mode:'url',message:'Open this',url:'https://example.invalid/x',elicitationId:'e'});
  const eh=render(e);
  assert.match(eh,/Input request from MCP server srv or the agent \(not established\)/);
  assert.match(eh,/the App never opens it/);assert.ok(!/<a href="https:/.test(eh),'the address is never a link');
});

test('item anchors link the card and the activity row both ways (§4.7, TR-6)',()=>{
  const row={threadId:'T',turnId:'u',native:{id:'i',type:'commandExecution',command:'ls -la',status:'inProgress'},displayState:'waiting-on-request',standing:'live-observed',observedOrder:0,requestRef:{generation:g,requestIdentity:'item/commandExecution/requestApproval'}};
  const view={items:[row],turns:[],turnRecords:[{threadId:'T',turnId:'u'}],revisions:[],descendants:[]};
  const r=command();
  const cardHtml=render(r,view);
  const item=activity.itemAnchorId('T','u','i');const card=activity.requestAnchorId(g,r.requestIdentity);
  assert.ok(cardHtml.includes(`id="${card}"`)&&cardHtml.includes(`href="#${item}"`),'card has its id and links to the row');
  const rowHtml=renderToStaticMarkup(React.createElement(activity.NativeActivityView,{view,threadId:'T'}));
  assert.ok(rowHtml.includes(`id="${item}"`)&&rowHtml.includes(`href="#${card}"`),'row has its id and links to the card');
  assert.ok(!/<button/.test(rowHtml),'the activity row never offers an answer control');
  assert.match(render(r,null),/About: Codex item <code>i<\/code> in turn <code>u<\/code>/,'without the row, the supplier identity only');
});

test('the waiting indicator counts only requests that wait for the person, per conversation (WI-1…WI-3)',()=>{
  const rs=[entry({id:'a'}),entry({id:'b'}),entry({id:'c',nativeParameters:{threadId:'U',turnId:'v',itemId:'j'}}),entry({id:'d',state:'answered'}),entry({id:'e',originClass:'named-service'}),A14.execCommandApproval];
  assert.deepEqual(waitingByConversation(rs),[{thread:'T',count:3},{thread:'U',count:1}]);
  const html=renderToStaticMarkup(React.createElement(WaitingRequestsIndicator,{requests:rs,open:()=>{}}));
  assert.match(html,/4 requests from Codex waiting for your answer/);assert.match(html,/conversation T: 3/);assert.match(html,/it answers nothing/);
  assert.match(renderToStaticMarkup(React.createElement(WaitingRequestsIndicator,{requests:[],open:()=>{}})),/No requests from Codex are waiting/);
});

test('an ended request carries the context its process ended in, matched by generation and identity (CS-7)',()=>{
  const generation={appSession:'s',home:'h',spawnCounter:1};
  const host={serverRequests:[entry({requestIdentity:7,generation,state:'ended-unanswered'}),entry({requestIdentity:8,generation,state:'ended-unanswered'}),entry({requestIdentity:7,generation:{...generation,spawnCounter:2},state:'ended-unanswered'})],
    serverRequestEndContexts:[{generation,requestIdentity:7,context:'app-quit'},{generation,requestIdentity:8,context:'supplier-exit'}]};
  assert.deepEqual(hostRequests(host).map(cardState),['Ended unanswered: the Codex process ended when you quit','Ended unanswered: the Codex process ended','Ended unanswered: the Codex process ended']);
  assert.deepEqual(hostRequests({}),[]);
});

test('DM-3: a legacy decline carries the person\'s reason as written, empty when none, and invalid text is not sent',async()=>{
  const {REJECTION_LIMIT,rejectionProblem,deniedWith}=cards;
  for(const r of [A14.execCommandApproval,A14.applyPatchApproval]){
    const html=render(r);
    assert.match(html,/<label>Reason for Codex with “Don&#x27;t allow; the agent tries something else” \(optional; sent exactly as written, up to 2000 characters\) <textarea/,'the card offers the field');
    assert.match(html,/Don&#x27;t allow; the agent tries something else <code>\{&quot;denied&quot;:\{&quot;rejection&quot;:&quot;&quot;\}\}<\/code>/,'an empty field sends ""');
    assert.match(html,/Don&#x27;t allow; the agent waits for your next message <code>&quot;abort&quot;<\/code>/,'abort keeps its label');
    assert.doesNotMatch(appWords(html),/accept|approv/i);
  }
  for(const r of [command(),A14['item/fileChange/requestApproval']]) assert.doesNotMatch(render(r),/<textarea/,'only legacy requests take a reason');
  assert.equal(REJECTION_LIMIT,2000);
  const written='Not this folder.\n\tUse the scratch copy: ünïcödé 🙂 "quoted" \\ back';
  for(const ok of ['',written,'x'.repeat(REJECTION_LIMIT),'🙂'.repeat(REJECTION_LIMIT)]) assert.equal(rejectionProblem(ok),null,'within bounds');
  assert.deepEqual(deniedWith(written),{decision:{denied:{rejection:written}}},'verbatim');
  assert.match(rejectionProblem('x'.repeat(REJECTION_LIMIT+1)),/longer than 2000 characters/);
  for(const bad of ['bell\u0007','cr\r','nul\u0000','del\u007f','c1\u0085','esc\u001b[31m']) assert.match(rejectionProblem(bad),/control character/,JSON.stringify(bad));
  // Mounted: what the decline sends as the person writes.
  const {installMiniDom}=await import('./support/mini-dom.mjs');
  const document=installMiniDom();
  const {createRoot}=await import('react-dom/client');
  const sent=[];
  const container=document.createElement('div');document.body.appendChild(container);
  const root=createRoot(container);
  await React.act(()=>root.render(React.createElement(NativeRequestCard,{request:A14.execCommandApproval,view:null,answer:async(_r,a)=>{sent.push(a);}})));
  const props=node=>node[Object.keys(node).find(k=>k.startsWith('__reactProps$'))];
  const deny=()=>container.querySelectorAll(n=>n.localName==='button'&&n.textContent.startsWith("Don't allow; the agent tries something else"))[0];
  const box=()=>container.querySelectorAll(n=>n.localName==='textarea')[0];
  const type=async text=>React.act(()=>props(box()).onChange({target:{value:text}}));
  await React.act(()=>props(deny()).onClick());
  assert.deepEqual(sent.at(-1),{decision:{denied:{rejection:''}}},'nothing written: ""');
  await type(written);
  assert.equal(deny().textContent,`Don't allow; the agent tries something else ${JSON.stringify({denied:{rejection:written}})}`,'the native value shown is the one sent');
  await React.act(()=>props(deny()).onClick());
  assert.deepEqual(sent.at(-1),{decision:{denied:{rejection:written}}},'written text, verbatim');
  assert.equal(props(box()).value,'','the draft is cleared once sent');
  for(const bad of ['bell\u0007','x'.repeat(REJECTION_LIMIT+1)]){
    await type(bad);
    assert.equal(props(deny()).disabled,true,'refused before sending');
    assert.ok(container.querySelectorAll(n=>n.localName==='p'&&n.getAttribute?.('role')==='alert').length===1);
  }
  assert.equal(sent.length,2,'nothing more was sent');
  await React.act(()=>root.unmount());
});
