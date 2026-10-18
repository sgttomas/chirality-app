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
const {NativeRequestCard,WaitingRequestsIndicator,cardState,decisionForms,decisionWords,hostRequests,refusalWords,requestTitle,answerable}=cards;

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

test('closed unknown retains the answer and cannot claim receipt, action or permit another answer',()=>{
  const prepared=entry({state:'reply-outcome-unknown',closedGeneration:true,replyWriteResult:'unknown',settlement:{kind:'answer',origin:{class:'person-via-interaction',actorRef:'person:synthetic (identity not verified)'},nativeContent:{decision:'accept'}}});
  assert.match(cardState(prepared),/^Reply outcome unknown:/);
  assert.match(cardState(prepared),/Whether Codex received or acted on the reply is unknown/);
  assert.equal(answerable(prepared),false);const html=render(prepared);assert.doesNotMatch(html,/<button/);assert.match(html,/&quot;decision&quot;: &quot;accept&quot;/,'original answer is kept in the visible native evidence');
  for(const state of ['answered','declined','errored']) {
    const known={...prepared,state,replyWriteResult:'written'};if(state==='errored')known.settlement={...known.settlement,kind:'error'};
    assert.match(cardState(known),/written locally/);assert.match(cardState(known),/whether Codex received or acted on it is unknown/);assert.equal(answerable(known),false);
  }
  assert.match(cardState({...prepared,state:'settle-write-failed',replyWriteResult:'write-failed'}),/whether Codex received it is unknown/);
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

test('the waiting indicator shows the native all-home groups and source limits (WI-1…WI-3)',()=>{
  const overview={groups:[{modeHomeClass:'account',generation:g,threadId:'T',count:3},{modeHomeClass:'api-key',generation:{...g,home:'key'},threadId:'T',count:1}],sources:[{modeHomeClass:'account',state:'ready'},{modeHomeClass:'api-key',state:'ready'}],coverage:'Sequential local snapshots; no supplier read.'};
  const html=renderToStaticMarkup(React.createElement(WaitingRequestsIndicator,{overview,open:()=>{}}));
  assert.match(html,/4 requests from Codex waiting for your answer/);assert.match(html,/conversation T: 3/);assert.match(html,/it answers nothing/);
  assert.match(html,/api-key.*conversation T: 1/);assert.match(html,/Sequential local snapshots/);
  assert.match(renderToStaticMarkup(React.createElement(WaitingRequestsIndicator,{overview:{groups:[],sources:[{modeHomeClass:'account',state:'stopped'}]},open:()=>{}})),/account: stopped; no current waiting groups shown/);
  assert.match(renderToStaticMarkup(React.createElement(WaitingRequestsIndicator,{overview:null,open:()=>{}})),/overview unavailable/);
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
  const written='Not this folder.\n\tUse the scratch copy: ünïcödé 🙂 👩‍💻 עברית "quoted" \\ back';
  for(const ok of ['',written,'x'.repeat(REJECTION_LIMIT),'🙂'.repeat(REJECTION_LIMIT)]) assert.equal(rejectionProblem(ok),null,'within bounds');
  assert.deepEqual(deniedWith(written),{decision:{denied:{rejection:written}}},'verbatim');
  assert.match(rejectionProblem('x'.repeat(REJECTION_LIMIT+1)),/longer than 2000 characters/);
  for(const bad of ['bell\u0007','cr\r','nul\u0000','del\u007f','c1\u0085','esc\u001b[31m']) assert.match(rejectionProblem(bad),/control character/,JSON.stringify(bad));
  // The host's BIDI_FORMATTING set, exactly; other format characters stay allowed.
  for(const bad of ['‪','‫','‬','‭','‮','⁦','⁧','⁨','⁩','‎','‏','؜']) assert.match(rejectionProblem(`x${bad}y`),/bidirectional formatting character/,JSON.stringify(bad));
  for(const allowed of ['‍','​','⁠','﻿',' ']) assert.equal(rejectionProblem(`x${allowed}y`),null,JSON.stringify(allowed));
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
  for(const bad of ['bell\u0007','x'.repeat(REJECTION_LIMIT+1),'name‮txt.exe']){
    await type(bad);
    assert.equal(props(deny()).disabled,true,'refused before sending');
    assert.ok(container.querySelectorAll(n=>n.localName==='p'&&n.getAttribute?.('role')==='alert').length===1);
  }
  assert.equal(sent.length,2,'nothing more was sent');
  await React.act(()=>root.unmount());
});

// Actual App -> native request card promise boundary. The controlled peer
// returns Host::answer_server_request's write observation, then loses only
// the window's custody refresh; it never invokes a supplier or native dialog.
async function withReplyObserver(check, {outcome='written',failRefresh=true,permission=false,beforeReply,afterCommandRead,withConversation=false,identity}={}) {
  const {installMiniDom}=await import('./support/mini-dom.mjs');
  const document=installMiniDom();const {createRoot}=await import('react-dom/client');
  const {loadSrc}=await import('./support/load-src.mjs');const {App}=loadSrc('App');
  const container=document.createElement('div');document.body.appendChild(container);let root=createRoot(container);
  const original=permission?request('item/fileChange/requestApproval',{threadId:'T',turnId:'u',itemId:'i',reason:'Synthetic requested file change'},{id:identity??'original-permission'}):
    request('item/tool/requestUserInput',{threadId:'T',turnId:'u',itemId:'i',questions:[{id:'q',header:'Choice',question:'Which option?',isOther:false,isSecret:false,options:[{label:'One',description:'Use one'}]}]},{id:identity??'original-question'});
  let custody=original,other=null,stale=null,currentOutcome=outcome;
  let commandSeen=false,refreshUnavailable=false;const calls=[];
  const snapshot=()=>({state:'ready',generation:(other??custody).generation,threads:withConversation?[{generation:g,threadId:'T',model:'synthetic',modelProvider:'synthetic',appRole:{standing:'unknown'}}]:[],homeRouting:{activeModeHomeClass:'account'},serverRequests:[other??stale??custody]});
  const previous=window.__TAURI_INTERNALS__;
  window.__TAURI_INTERNALS__={invoke:async(command,args)=>{
    calls.push({command,args});
    if(command==='host_status'){const delayed=commandSeen&&afterCommandRead?await afterCommandRead(snapshot()):null;if(refreshUnavailable)throw Error('reconnect snapshot unavailable');return delayed??snapshot();}
    if(command==='decision_view')return {rows:[]};
    if(command==='native_confirmation_content')return [];
    if(command==='read_home_access')return {};
    assert.equal(command,'answer_native_request');commandSeen=true;
    if(beforeReply)await beforeReply();
    refreshUnavailable=failRefresh;
    if(currentOutcome==='refused'){custody={...custody,state:'resolved-by-supplier',supplierResolution:{source:'serverRequest/resolved'}};throw 'already-resolved';}
    if(currentOutcome==='refused-pending')throw 'invalid-answer';
    if(currentOutcome==='dismissed')return {state:'dismissed',replyWriteResult:'not-attempted'};
    if(currentOutcome==='write-failed'){custody={...custody,state:'settle-write-failed',replyWriteResult:'write-failed'};throw 'synthetic reply IO failed';}
    if(currentOutcome==='unknown')return {replyWriteResult:'unknown'};
    custody={...custody,state:permission?'declined':'answered',replyWriteResult:'written',settlement:{kind:permission?'decline':'answer',origin:{class:'person-via-interaction'}}};
    return {replyWriteResult:'written',acknowledgment:'not-observed'};
  }};
  const props=node=>node[Object.keys(node).find(key=>key.startsWith('__reactProps$'))];
  const button=label=>container.querySelectorAll(node=>node.localName==='button'&&node.textContent===label)[0];
  const send=()=>permission?container.querySelectorAll(node=>node.localName==='button'&&node.textContent.startsWith("Don't allow; the agent continues the turn"))[0]:button('Send current question answers…');
  const render=()=>React.act(async()=>root.render(React.createElement(App)));
  try {
    await render();
    await check({container,calls,props,button,send,get custody(){return custody;},original,
      async choose(){if(!permission)await React.act(()=>props(button('One · Use one')).onClick());},
      async answer(){if(!permission)await React.act(()=>props(button('One · Use one')).onClick());await React.act(async()=>props(send()).onClick());},
      async read(){await React.act(async()=>props(button('Read current request state')).onClick());},
      async selectConversation(threadId){const select=container.querySelectorAll(node=>node.localName==='select'&&node.parentNode.textContent.startsWith('Current-generation conversation '))[0];await React.act(()=>props(select).onChange({target:{value:threadId?JSON.stringify([g,threadId]):''}}));},
      allowRefresh(){refreshUnavailable=false;},replyAs(next){currentOutcome=next;},
      staleSnapshot(){stale=structuredClone(original);},canonicalSnapshot(){stale=null;},
      async swapSource(next){other=next;await React.act(async()=>props(button('Read native login policy and account')).onClick());},
      async reconnect(){await React.act(()=>root.unmount());refreshUnavailable=false;root=createRoot(container);await render();},
      get commandSeen(){return commandSeen;}});
  } finally {await React.act(()=>root.unmount());document.body.removeChild(container);window.__TAURI_INTERNALS__=previous;}
}

test('a written native answer remains written when its observer refresh fails, without enabling a stale waiting reply',async()=>{
  await withReplyObserver(async ui=>{
    await ui.answer();
    assert.equal(ui.custody.state,'answered');assert.equal(ui.custody.replyWriteResult,'written');
    assert.doesNotMatch(ui.container.textContent,/Last answer not taken:/,'an observer read failure cannot turn a completed native write into a rejected answer');
    assert.match(ui.container.textContent,/request state unavailable/i);
    assert.ok(!ui.send()||ui.props(ui.send()).disabled,'stale outstanding custody cannot invite another answer');
    assert.deepEqual(ui.calls.filter(call=>call.command==='answer_native_request'),[{command:'answer_native_request',args:{generation:g,requestId:'original-question',answer:{answers:{q:{answers:['One']}}}}}]);
    await ui.reconnect();
    assert.match(ui.container.textContent,/Your answer was written to Codex; Codex has not confirmed it/);
    assert.equal(ui.send(),undefined);assert.equal(ui.calls.filter(call=>call.command==='answer_native_request').length,1,'reopening does not resend');
  });
});

test('moving the same original card between the request list and conversation keeps its written-reply guard',async()=>{
  await withReplyObserver(async ui=>{
    await ui.answer();assert.equal(!!ui.send(),false);
    await ui.selectConversation('T');
    assert.equal(!!ui.send(),false,'moving an answered original request into its conversation must not reopen stale reply controls');
    assert.match(ui.container.textContent,/The reply was written locally/);
    await ui.selectConversation('');assert.equal(!!ui.send(),false);
    assert.equal(ui.calls.filter(call=>call.command==='answer_native_request').length,1);
  },{withConversation:true});
});

test('moving a pending original request keeps its command latch without issuing another reply',async()=>{
  let release;const held=new Promise(resolve=>{release=resolve;});
  await withReplyObserver(async ui=>{
    await ui.choose();let pending;
    await React.act(()=>{pending=ui.props(ui.send()).onClick();});
    await ui.selectConversation('T');assert.equal(!!ui.send(),false);
    assert.match(ui.container.textContent,/Answer command in progress/);
    await ui.selectConversation('');assert.equal(!!ui.send(),false);
    assert.equal(ui.calls.filter(call=>call.command==='answer_native_request').length,1);
    release();await React.act(async()=>{await pending;});
    assert.equal(!!ui.send(),false);assert.match(ui.container.textContent,/The reply was written locally/);
    assert.equal(ui.calls.filter(call=>call.command==='answer_native_request').length,1);
  },{withConversation:true,beforeReply:()=>held});
});

test('an explicit native decline is written without becoming supplier acknowledgment or an inferred answer',async()=>{
  await withReplyObserver(async ui=>{
    await ui.answer();assert.equal(ui.custody.state,'declined');
    assert.match(ui.container.textContent,/The reply was written locally/);
    assert.doesNotMatch(ui.container.textContent,/Last answer not taken|Codex reported the request resolved/);
    await ui.reconnect();assert.match(ui.container.textContent,/You declined; written to Codex; Codex has not confirmed it/);
    assert.deepEqual(ui.calls.filter(call=>call.command==='answer_native_request').map(call=>call.args),[{generation:g,requestId:'original-permission',answer:{decision:'decline'}}]);
  },{permission:true});
});

test('dismissed native confirmation stays not-attempted and retry requires current original custody',async()=>{
  await withReplyObserver(async ui=>{
    await ui.answer();assert.equal(ui.custody.state,'outstanding');
    assert.match(ui.container.textContent,/Native confirmation dismissed; no reply write was attempted/);
    assert.doesNotMatch(ui.container.textContent,/Last answer not taken:/);
    assert.equal(ui.send(),undefined,'unavailable custody does not offer a fresh answer yet');
    ui.allowRefresh();await ui.read();assert.ok(ui.send());
    assert.equal(ui.calls.filter(call=>call.command==='answer_native_request').length,1,'a custody read is never an answer or retry');
    ui.replyAs('written');await ui.answer();
    assert.equal(ui.custody.state,'answered');assert.equal(ui.send(),undefined);
    assert.equal(ui.calls.filter(call=>call.command==='answer_native_request').length,2,'only the next explicit answer press retries');
  },{outcome:'dismissed'});
});

test('supplier resolution after interruption remains a supplier resolution and its native refusal survives observer failure',async()=>{
  await withReplyObserver(async ui=>{
    await ui.answer();
    assert.equal(ui.custody.state,'resolved-by-supplier');
    assert.match(ui.container.textContent,/Native answer command reported: already-resolved/);
    assert.match(ui.container.textContent,/Request state unavailable: Error: reconnect snapshot unavailable/);
    assert.equal(ui.send(),undefined);
    const call=ui.calls.find(call=>call.command==='answer_native_request');
    assert.deepEqual(call.args,{generation:g,requestId:'original-permission',answer:{decision:'decline'}});
    ui.allowRefresh();await ui.read();
    assert.match(ui.container.textContent,/Resolved by Codex before you answered/);
    assert.doesNotMatch(ui.container.textContent,/You declined; written/,'the person’s refused decline does not become a settlement');
    assert.equal(ui.send(),undefined);assert.equal(ui.calls.filter(call=>call.command==='answer_native_request').length,1);
  },{outcome:'refused',permission:true});
});

test('a rejected invalid answer can be retried only after current outstanding custody is read',async()=>{
  await withReplyObserver(async ui=>{
    await ui.answer();assert.match(ui.container.textContent,/Native answer command reported: invalid-answer/);assert.equal(ui.send(),undefined);
    ui.allowRefresh();await ui.read();assert.ok(ui.send());
    ui.replyAs('written');await ui.answer();assert.equal(ui.custody.state,'answered');
    assert.equal(ui.calls.filter(call=>call.command==='answer_native_request').length,2);
  },{outcome:'refused-pending'});
});

test('failed or unconfirmed reply writes stay uncertain and are never upgraded or automatically retried',async()=>{
  for(const outcome of ['write-failed','unknown'])await withReplyObserver(async ui=>{
    await ui.answer();assert.equal(ui.send(),undefined);
    assert.doesNotMatch(ui.container.textContent,/The reply was written locally|Last answer not taken:/);
    if(outcome==='write-failed')assert.match(ui.container.textContent,/synthetic reply IO failed/);
    else assert.match(ui.container.textContent,/Reply write outcome not established \(unknown\)/);
    ui.allowRefresh();await ui.read();
    assert.equal(ui.send(),undefined,'uncertain local evidence does not authorize another response');
    assert.equal(ui.calls.filter(call=>call.command==='answer_native_request').length,1);
    if(outcome==='write-failed')assert.match(ui.container.textContent,/Your answer could not be written; whether Codex received it is unknown/);
  },{outcome});
});

test('a written reply guard survives a successful but stale outstanding refresh',async()=>{
  await withReplyObserver(async ui=>{
    ui.staleSnapshot();await ui.answer();
    assert.equal(ui.custody.state,'answered');assert.equal(ui.send(),undefined);
    assert.match(ui.container.textContent,/Last observed: Waiting for your answer/);
    await ui.read();assert.equal(ui.send(),undefined,'another stale outstanding snapshot cannot undo the completed write');
    ui.canonicalSnapshot();await ui.read();assert.match(ui.container.textContent,/Your answer was written to Codex; Codex has not confirmed it/);
    assert.equal(ui.calls.filter(call=>call.command==='answer_native_request').length,1);
  },{failRefresh:false});
});

test('queued response presses write once, and an obsolete button cannot resend after completion',async()=>{
  let release;const held=new Promise(resolve=>{release=resolve;});
  await withReplyObserver(async ui=>{
    await ui.choose();const click=ui.props(ui.send()).onClick;let pending,duplicate;
    await React.act(()=>{pending=click();duplicate=click();});
    assert.equal(ui.calls.filter(call=>call.command==='answer_native_request').length,1);
    release();await React.act(async()=>{await pending;await duplicate;});
    await React.act(async()=>{await click();});
    assert.equal(ui.calls.filter(call=>call.command==='answer_native_request').length,1);
  },{beforeReply:()=>held});
});

test('late reply refresh completion cannot attach its observation to another source or a lookalike typed request ID',async()=>{
  for(const {next,identity} of [
    {next:request('item/tool/requestUserInput',{threadId:'T',turnId:'u',itemId:'i',questions:[]},{id:'original-question',generation:{...g,home:'other-home'}})},
    {next:request('item/tool/requestUserInput',{threadId:'T',turnId:'u',itemId:'i',questions:[]},{id:17}),identity:'17'},
  ]) {
    let release,reached;const held=new Promise(resolve=>{release=resolve;});const ready=new Promise(resolve=>{reached=resolve;});let hold=true;
    await withReplyObserver(async ui=>{
      await ui.choose();let pending;
      await React.act(()=>{pending=ui.props(ui.send()).onClick();});
      await ready;await ui.swapSource(next);
      assert.ok(ui.send(),'the other original request remains independently answerable');
      release();await React.act(async()=>{await pending;});
      assert.ok(ui.send());assert.equal(ui.props(ui.send()).disabled,false);
      const native=ui.container.querySelectorAll(node=>node.getAttribute('aria-label')==='Native reply observation');
      assert.equal(native.length,0,'the completed earlier command supplies no local result to the other card');
      assert.equal(ui.calls.filter(call=>call.command==='answer_native_request').length,1);
      assert.equal(ui.calls.find(call=>call.command==='answer_native_request').args.requestId,identity??'original-question');
    },{identity,failRefresh:false,afterCommandRead:async()=>{if(hold){hold=false;reached();await held;}}});
  }
});

test('an older custody reread cannot replace the safe observation of a newer explicit reply',async()=>{
  let release,reached;const held=new Promise(resolve=>{release=resolve;});const ready=new Promise(resolve=>{reached=resolve;});let reads=0;
  await withReplyObserver(async ui=>{
    await ui.answer();ui.allowRefresh();
    await ui.read();await ready;
    // The read is still held in the first card. Move to the same original
    // request's other location and obtain a newer current custody observation.
    await ui.selectConversation('T');await ui.read();assert.ok(ui.send());
    ui.replyAs('written');await ui.answer();assert.equal(ui.custody.state,'answered');
    release();await React.act(async()=>{await new Promise(resolve=>setImmediate(resolve));});
    assert.equal(ui.send(),undefined,'the stale outstanding page cannot erase the newer written observation');
    assert.match(ui.container.textContent,/The reply was written locally/);
    assert.equal(ui.calls.filter(call=>call.command==='answer_native_request').length,2,'only the two person-directed replies were invoked');
  },{outcome:'dismissed',withConversation:true,afterCommandRead:async snapshot=>{reads++;if(reads===2){reached();await held;return snapshot;}}});
});
