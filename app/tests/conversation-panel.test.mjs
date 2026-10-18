import test from 'node:test';
import assert from 'node:assert/strict';
import {installMiniDom} from './support/mini-dom.mjs';
import {loadSrc} from './support/load-src.mjs';
import {continuationFixture} from './support/continuation-fixture.mjs';

// The conversation section is mounted with react-dom/client on a minimal
// in-memory document, so the test sees what React actually leaves mounted
// when the person moves between conversations (native witness 2026-10-10 D-1:
// one more role header per conversation viewed).
const document = installMiniDom();
const React = (await import('react')).default;
const {createRoot} = await import('react-dom/client');
const {App, ConversationPanel} = loadSrc('App');

const g = {appSession: 's', home: 'h', spawnCounter: 1};
const thread = (threadId, role, relation = {kind: 'start'}) => ({generation: g, threadId, appRole: {standing: 'app-observed', role, supply_ref: `sup:${threadId}`}, roleRelation: relation, futureGuidanceNotices: []});
const host = {state: 'ready', generation: g, roleLimits: {account: {roles: []}},
  threads: [thread('thread-a', null), thread('thread-b', null), thread('thread-c', 'HELPS_HUMANS', {kind: 'continued-from', from: {sourceThread: 'thread-b', sourceRole: {standing: 'app-observed', role: null}}})]};
const key = threadId => JSON.stringify([g, threadId]);
const noop = async () => {};

test('exactly one role header, for the selected conversation, as the person moves between conversations', async () => {
  const errors = [];
  const consoleError = console.error;
  console.error = (...args) => { errors.push(args.map(String).join(' ')); };
  try {
    const container = document.createElement('div');
    document.body.appendChild(container);
    const root = createRoot(container);
    const show = threadKey => React.act(() => root.render(React.createElement(ConversationPanel, {host, threadKey, setThreadKey: () => {}, answer: noop, runAct: noop, send: noop, steer: noop, submitAttachments: noop, interrupt: noop, checkPlanMode: noop, codexBusy: false})));
    const headers = () => container.querySelectorAll(e => e.getAttribute('aria-label') === 'Conversation role');
    await show('');
    assert.equal(headers().length, 0, 'no conversation selected, no header');
    // The witness order: a conversation, the resumed one, then the Continue as conversation, and back.
    for (const [threadId, line] of [['thread-a', 'No role'], ['thread-b', 'No role'], ['thread-c', 'HELPS_HUMANS'], ['thread-a', 'No role']]) {
      await show(key(threadId));
      const shown = headers();
      assert.equal(shown.length, 1, `one header after selecting ${threadId}`);
      assert.ok(shown[0].textContent.startsWith(`Role: ${line}.`), `the header is ${threadId}'s`);
      assert.equal(shown[0].textContent.includes('Continues conversation thread-b'), threadId === 'thread-c');
    }
    await React.act(() => root.unmount());
    assert.equal(headers().length, 0);
  } finally {
    console.error = consoleError;
  }
  assert.deepEqual(errors.filter(e => e.includes('same key')), [], 'no two children of the section share a key');
});

// Exercise the ordinary Start button through App's native invoke boundary,
// including the refresh that supplies the newly admitted native thread.
const props = element => element[Object.keys(element).find(key => key.startsWith('__reactProps$'))];
const elements = (container, tag) => container.querySelectorAll(element => element.localName === tag);
const button = (container, text) => elements(container, 'button').find(element => element.textContent === text);
const labelled = (container, tag, text) => elements(container, tag).find(element => element.parentNode.textContent.startsWith(text));
const change = (element, value) => React.act(() => props(element).onChange({target: {value}}));

async function ordinaryStartCase({initialThread = false, startGeneration = g, outcome = 'success'}) {
  const container = document.createElement('div');
  document.body.appendChild(container);
  const root = createRoot(container);
  const calls = [];
  let snapshot = {...host, threads: initialThread ? [thread('existing', null)] : [],
    homeRouting: {activeModeHomeClass: 'account'},
    roleSet: {available: true, defaultRole: 'HELP_HUMAN', roles: [{name: 'HELP_HUMAN', meaning: 'Alignment', default_for_new_chat: true}]}};
  const previous = window.__TAURI_INTERNALS__;
  window.__TAURI_INTERNALS__ = {invoke: async (command, args) => {
    calls.push({command, args});
    if (command === 'host_status') return snapshot;
    if (command === 'decision_view') return {rows: []};
    if (command === 'native_confirmation_content') return [];
    if (command !== 'thread_start') throw Error(`Unexpected native command: ${command}`);
    if (outcome === 'refused') throw Error('Native start refused before send');
    if (outcome === 'failed') throw Error('Native start result unknown; no automatic retry');
    if (outcome === 'missing-id') return {startGeneration, result: {thread: {}}};
    if (outcome === 'missing-generation') return {result: {thread: {id: 'created'}}};
    const created = {...thread('created', 'HELP_HUMAN'), generation: startGeneration, model: args.model, modelProvider: args.modelProvider};
    snapshot = {...snapshot, generation: startGeneration, threads: [...snapshot.threads, created]};
    return {id: 42, startGeneration, result: {thread: {id: created.threadId}}, roleSupplyRecord: {state: 'recorded'}};
  }};
  try {
    await React.act(async () => {root.render(React.createElement(App));});
    const conversation = () => container.querySelectorAll(element => element.getAttribute('id') === 'conversation')[0];
    const selectedKey = () => props(elements(conversation(), 'select')[0]).value;
    if (initialThread) await change(elements(conversation(), 'select')[0], key('existing'));
    await change(labelled(container, 'input', 'Model '), 'chosen-model');
    await change(labelled(container, 'input', 'Configured Codex provider '), 'openai');
    await change(labelled(container, 'select', 'Access entry '), 'chatgpt-account');
    const draft = 'Unsent person text é / 家';
    await change(elements(conversation(), 'textarea')[0], draft);
    const start = button(container, 'Start thread');
    assert.equal(props(start).disabled, false);
    await React.act(async () => {await props(start).onClick();});
    assert.deepEqual(calls.filter(call => call.command === 'thread_start'), [{command: 'thread_start', args: {
      model: 'chosen-model', modelProvider: 'openai', entryId: 'chatgpt-account', modeHomeClass: 'account', role: 'HELP_HUMAN', preselected: true,
    }}], 'one person-initiated start with the chosen configuration');
    assert.ok(calls.every(call => ['host_status', 'decision_view', 'native_confirmation_content', 'thread_start'].includes(call.command)), 'Start never sends composer text or retries');
    assert.equal(props(elements(conversation(), 'textarea')[0]).value, draft, 'unsent composer retained');
    if (outcome === 'success') {
      assert.equal(selectedKey(), JSON.stringify([startGeneration, 'created']), 'opens the native ID in the returned start generation');
      // ACCESS REQ-004/CS-9: admission consumes this new-conversation choice;
      // it does not apply the same choice to another conversation.
      assert.equal(props(labelled(container, 'input', 'Model ')).value, '', 'the next conversation has no model selected');
      assert.equal(props(labelled(container, 'input', 'Configured Codex provider ')).value, '');
      assert.equal(props(labelled(container, 'select', 'Access entry ')).value, '');
      assert.equal(props(button(container, 'Start thread')).disabled, true, 'a second start needs a fresh explicit choice');
      assert.equal(props(button(conversation(), 'Send text')).disabled, false, 'the displayed new conversation can receive an explicit send');
      const headers = conversation().querySelectorAll(element => element.getAttribute('aria-label') === 'Conversation role');
      assert.equal(headers.length, 1);
      assert.ok(headers[0].textContent.startsWith('Role: HELP_HUMAN.'), 'shows the new conversation');
    } else {
      assert.equal(selectedKey(), initialThread ? key('existing') : '', 'unsuccessful start keeps the selection');
      assert.deepEqual(['Model ', 'Configured Codex provider ', 'Access entry '].map((label,index)=>props(labelled(container,index===2?'select':'input',label)).value),
        ['chosen-model','openai','chatgpt-account'],'a refused, unknown or incomplete attempt keeps its explicit chooser for retry');
      assert.equal(props(button(container,'Start thread')).disabled,false);
      assert.equal(props(button(conversation(), 'Send text')).disabled, !initialThread);
      if (outcome === 'refused' || outcome === 'failed') assert.ok(container.textContent.includes('thread_start: Error: Native start'));
    }
  } finally {
    await React.act(() => root.unmount());
    document.body.removeChild(container);
    window.__TAURI_INTERNALS__ = previous;
  }
}

test('ordinary Start opens the admitted conversation without sending its composer', async () => {
  await ordinaryStartCase({});
  await ordinaryStartCase({initialThread: true});
  // The host's actual start generation can differ from the pre-click snapshot.
  await ordinaryStartCase({initialThread: true, startGeneration: {appSession: 's', home: 'other-home', spawnCounter: 2}});
});

test('refused, failed and identity-incomplete Start preserve selection and composer', async () => {
  for (const outcome of ['refused', 'failed', 'missing-id', 'missing-generation']) {
    await ordinaryStartCase({outcome});
    await ordinaryStartCase({initialThread: true, outcome});
  }
});

// The ordinary form's actual native boundary with held responses and two
// configured source homes. No provider/authentication is invoked by this peer.
async function withStartChooser(check, startReply, {homeReply,decisionReply}={}) {
  const container=document.createElement('div');document.body.appendChild(container);const root=createRoot(container);
  const calls=[];
  const homes={account:{generation:g,threads:[]},'api-key':{generation:{...g,home:'key-home'},threads:[]}};
  let active='account',statusFailure=false;
  const snapshot=()=>({...host,state:'ready',generation:homes[active].generation,threads:homes[active].threads,
    homeRouting:{activeModeHomeClass:active,entries:Object.keys(homes).map(modeHomeClass=>({modeHomeClass}))},
    roleSet:{available:true,defaultRole:'HELP_HUMAN',roles:[{name:'HELP_HUMAN',meaning:'Alignment',default_for_new_chat:true}]},
    accessSelection:{state:'started',thread:{threadId:'prior-native-selection'}}});
  const admitted=(args,index,extra={})=>{
    const generation=extra.startGeneration??homes[args.modeHomeClass].generation;
    const id=`created-${index}`;
    homes[args.modeHomeClass].generation=generation;
    homes[args.modeHomeClass].threads.push({...thread(id,args.role),generation,model:args.model,modelProvider:args.modelProvider});
    // Record publication can fail independently of native admission, and the
    // native reported destination need not equal what the person requested.
    return {id:index,startGeneration:generation,result:{thread:{id},model:'native-reported-model',modelProvider:'native-reported-provider'},roleSupplyRecord:{state:'not-confirmed'},...extra};
  };
  const previous=window.__TAURI_INTERNALS__;
  window.__TAURI_INTERNALS__={invoke:async(command,args)=>{
    calls.push({command,args});
    if(command==='host_status'){if(statusFailure)throw Error('Current status read unavailable');return snapshot();}
    if(command==='decision_view')return decisionReply?decisionReply(active):{rows:[]};
    if(command==='native_confirmation_content')return [];
    if(command==='select_home'){if(homeReply)await homeReply(args,active);active=args.modeHomeClass;return {state:'selected'};}
    if(command==='read_home_access')return {state:'synthetic source read'};
    assert.equal(command,'thread_start');
    const index=calls.filter(call=>call.command==='thread_start').length;
    return startReply?startReply(args,index,admitted):admitted(args,index);
  }};
  const field=(tag,label)=>labelled(container,tag,label);
  const values=()=>({model:props(field('input','Model ')).value,modelProvider:props(field('input','Configured Codex provider ')).value,entryId:props(field('select','Access entry ')).value});
  const edit=async(patch)=>{for(const [key,value] of Object.entries(patch)){const [tag,label]=key==='model'?['input','Model ']:key==='modelProvider'?['input','Configured Codex provider ']:['select','Access entry '];await change(field(tag,label),value);}};
  const press=async(text)=>React.act(async()=>{await props(button(container,text)).onClick();});
  try {
    await React.act(async()=>root.render(React.createElement(App)));
    await check({container,calls,homes,values,edit,press,start:()=>button(container,'Start thread'),
      failStatus:()=>{statusFailure=true;},generation:()=>homes[active].generation});
  } finally {await React.act(()=>root.unmount());document.body.removeChild(container);window.__TAURI_INTERNALS__=previous;}
}
const selectedChoice={model:'chosen-model',modelProvider:'openai',entryId:'chatgpt-account'};
const blankChoice={model:'',modelProvider:'',entryId:''};
const deferred=()=>{let resolve,reject;const promise=new Promise((yes,no)=>{resolve=yes;reject=no;});return {promise,resolve,reject};};

test('each successful ordinary Start consumes only its choice and a second conversation needs a new explicit choice',async()=>{
  await withStartChooser(async ui=>{
    assert.deepEqual(ui.values(),blankChoice);assert.equal(props(ui.start()).disabled,true);
    await ui.edit(selectedChoice);assert.deepEqual(ui.calls.filter(c=>c.command==='thread_start'),[],'editing dispatches nothing');
    const conversation=()=>ui.container.querySelectorAll(e=>e.getAttribute('id')==='conversation')[0];
    await change(elements(conversation(),'textarea')[0],'Kept unsent draft / 家');
    await ui.press('Start thread');
    assert.deepEqual(ui.values(),blankChoice);assert.equal(props(ui.start()).disabled,true);
    assert.match(ui.container.querySelectorAll(e=>e.getAttribute('aria-label')==='New conversation choice')[0].textContent,/no model selected/);
    assert.equal(props(elements(conversation(),'select')[0]).value,JSON.stringify([g,'created-1']));
    assert.equal(props(elements(conversation(),'textarea')[0]).value,'Kept unsent draft / 家');
    assert.match(conversation().textContent,/HELP_HUMAN/,'the started conversation retains its role');
    await ui.press('Start thread');
    assert.equal(ui.calls.filter(c=>c.command==='thread_start').length,1,'even a queued press on an unselected chooser sends nothing');
    await ui.edit({...selectedChoice,model:'second-model'});await ui.press('Start thread');
    assert.equal(props(elements(conversation(),'select')[0]).value,JSON.stringify([g,'created-2']));
    assert.deepEqual(ui.values(),blankChoice);
    assert.deepEqual(ui.calls.filter(c=>c.command==='thread_start').map(c=>c.args.model),['chosen-model','second-model']);
    assert.equal(ui.calls.filter(c=>c.command==='turn/start'||c.command==='conversation_send_text').length,0);
  });
});

test('refused, unknown and incomplete ordinary starts retain a usable choice for an explicit retry',async()=>{
  for(const outcome of ['refused','unknown','missing-id','missing-generation','partial-generation','extra-generation-field','empty-generation-home','zero-generation','fractional-generation','error-envelope']) {
    await withStartChooser(async ui=>{
      await ui.edit(selectedChoice);await ui.press('Start thread');
      assert.deepEqual(ui.values(),selectedChoice,outcome);assert.equal(props(ui.start()).disabled,false,outcome);
      assert.equal(ui.calls.filter(c=>c.command==='thread_start').length,1,'no automatic retry');
      await ui.press('Start thread');assert.deepEqual(ui.values(),blankChoice,`${outcome}: explicit retry can succeed`);
      assert.equal(ui.calls.filter(c=>c.command==='thread_start').length,2);
    },(args,index,admitted)=>{
      if(index>1)return admitted(args,index);
      if(outcome==='refused'||outcome==='unknown')throw Error(`Native start ${outcome}`);
      if(outcome==='missing-id')return {startGeneration:g,result:{thread:{}}};
      if(outcome==='missing-generation')return {result:{thread:{id:'unconfirmed'}}};
      if(outcome==='error-envelope')return {startGeneration:g,result:{thread:{id:'unconfirmed'}},error:{code:-32000}};
      const generation=outcome==='partial-generation'?{home:g.home}:outcome==='extra-generation-field'?{...g,extra:true}:
        {...g,home:outcome==='empty-generation-home'?'':g.home,spawnCounter:outcome==='zero-generation'?0:outcome==='fractional-generation'?1.5:1};
      return {startGeneration:generation,result:{thread:{id:'unconfirmed'}}};
    });
  }
});

test('a pending ordinary Start latches queued duplicate presses and preserves every newer edit, including away and back',async()=>{
  for(const patch of [{model:'new-model'},{modelProvider:'new-provider'},{entryId:'local-provider'},null]) {
    const reply=deferred();let complete;
    await withStartChooser(async ui=>{
      await ui.edit(selectedChoice);
      let pending,duplicate;
      const click=props(ui.start()).onClick;
      await React.act(()=>{pending=click();duplicate=click();});
      assert.equal(props(ui.start()).disabled,true);assert.equal(ui.calls.filter(c=>c.command==='thread_start').length,1);
      if(patch)await ui.edit(patch);
      else {await ui.edit({model:'temporary'});await ui.edit({model:'chosen-model'});}
      const newer=ui.values();reply.resolve();
      await React.act(async()=>{await pending;await duplicate;});
      assert.deepEqual(ui.values(),newer,'the older success cannot consume a newer edit revision');
      assert.equal(props(ui.start()).disabled,false);
      assert.equal(ui.calls.filter(c=>c.command==='thread_start').length,1);
    },async(args,index,admitted)=>{complete=()=>admitted(args,index);await reply.promise;return complete();});
  }
});

test('home choices during a pending Start neither reuse the old choice nor let its success erase a newer home choice',async()=>{
  const reply=deferred();
  await withStartChooser(async ui=>{
    await ui.edit(selectedChoice);let pending;
    await React.act(()=>{pending=props(ui.start()).onClick();});
    await ui.press('Use api-key home');assert.deepEqual(ui.values(),blankChoice);
    const keyChoice={model:'key-model',modelProvider:'openai',entryId:'api-key'};
    await ui.edit(keyChoice);
    reply.resolve();await React.act(async()=>{await pending;});
    assert.deepEqual(ui.values(),keyChoice);assert.equal(props(ui.start()).disabled,false);
    assert.equal(ui.calls.filter(c=>c.command==='thread_start').length,1);
    await ui.edit({entryId:'chatgpt-account'});
    assert.equal(props(ui.start()).disabled,true,'a cloud entry from another home is not a compatible choice');
    await ui.press('Start thread');assert.equal(ui.calls.filter(c=>c.command==='thread_start').length,1);
    await ui.edit(keyChoice);await ui.press('Start thread');assert.deepEqual(ui.values(),blankChoice);
    await ui.press('Use account home');assert.deepEqual(ui.values(),blankChoice,'returning to the prior home does not restore a consumed or invalidated choice');
  },async(args,index,admitted)=>{if(index===1)await reply.promise;return admitted(args,index);});
});

test('an away-and-back home transition protects a newer same-valued choice from the earlier pending success',async()=>{
  const reply=deferred();
  await withStartChooser(async ui=>{
    await ui.edit(selectedChoice);let pending;
    await React.act(()=>{pending=props(ui.start()).onClick();});
    await ui.press('Use api-key home');await ui.press('Use account home');
    assert.deepEqual(ui.values(),blankChoice);await ui.edit(selectedChoice);
    reply.resolve();await React.act(async()=>{await pending;});
    assert.deepEqual(ui.values(),selectedChoice);assert.equal(props(ui.start()).disabled,false);
    assert.equal(ui.calls.filter(c=>c.command==='thread_start').length,1);
  },async(args,index,admitted)=>{await reply.promise;return admitted(args,index);});
});

test('a home transition invalidates prior-home edits but preserves newer target-home edits while its refresh and an older Start finish',async()=>{
  const startReply=deferred(),homeReply=deferred(),targetRead=deferred(),targetReadReached=deferred();
  let holdTargetRead=true;
  await withStartChooser(async ui=>{
    await ui.edit(selectedChoice);let pendingStart,pendingHome;
    await React.act(()=>{pendingStart=props(ui.start()).onClick();});
    await React.act(()=>{pendingHome=props(button(ui.container,'Use api-key home')).onClick();});
    assert.deepEqual(ui.values(),blankChoice);
    await ui.edit({...selectedChoice,model:'edited-before-target-was-active'});
    assert.equal(props(ui.start()).disabled,true,'the prior-home draft cannot start during selection');
    await React.act(async()=>{homeReply.resolve();await targetReadReached.promise;});
    assert.match(ui.container.textContent,/Active home class: api-key/);
    assert.deepEqual(ui.values(),blankChoice,'edits made while account was still active do not become key-home choices');
    const targetChoice={model:'target-home-model',modelProvider:'openai',entryId:'api-key'};
    await ui.edit(targetChoice);
    startReply.resolve();await React.act(async()=>{await pendingStart;});
    assert.deepEqual(ui.values(),targetChoice,'the earlier account admission cannot consume the visible key-home draft');
    assert.equal(props(ui.start()).disabled,true,'the home refresh is still pending');
    targetRead.resolve();await React.act(async()=>{await pendingHome;});
    assert.deepEqual(ui.values(),targetChoice);assert.equal(props(ui.start()).disabled,false);
    assert.equal(ui.calls.filter(c=>c.command==='thread_start').length,1,'neither home transition nor editing dispatches a start');
    await ui.press('Start thread');assert.deepEqual(ui.values(),blankChoice);
  },async(args,index,admitted)=>{if(index===1)await startReply.promise;return admitted(args,index);},{
    homeReply:()=>homeReply.promise,
    decisionReply:async active=>{if(active==='api-key'&&holdTargetRead){holdTargetRead=false;targetReadReached.resolve();await targetRead.promise;}return {rows:[]};},
  });
});

test('a same-class actual generation update while Start is pending does not become another chooser edit',async()=>{
  const reply=deferred();
  await withStartChooser(async ui=>{
    await ui.edit(selectedChoice);let pending;
    await React.act(()=>{pending=props(ui.start()).onClick();});
    const actual={appSession:'actual-session',home:'actual-account-home',spawnCounter:2};
    ui.homes.account.generation=actual;
    await ui.press('Read native login policy and account');
    assert.deepEqual(ui.values(),selectedChoice,'a source observation is not another person choice');
    reply.resolve();await React.act(async()=>{await pending;});
    assert.deepEqual(ui.values(),blankChoice);
    const conversation=ui.container.querySelectorAll(e=>e.getAttribute('id')==='conversation')[0];
    assert.equal(props(elements(conversation,'select')[0]).value,JSON.stringify([actual,'created-1']),'opens the actual returned H5, never the stale pre-click tuple');
    assert.equal(ui.calls.filter(c=>c.command==='thread_start').length,1);
  },async(args,index,admitted)=>{await reply.promise;return admitted(args,index);});
});

test('an admitted start consumes its chooser before an independent refresh failure',async()=>{
  await withStartChooser(async ui=>{
    await ui.edit(selectedChoice);ui.failStatus();await ui.press('Start thread');
    assert.deepEqual(ui.values(),blankChoice);assert.equal(props(ui.start()).disabled,true);
    assert.match(ui.container.textContent,/current host view unavailable/);
    assert.equal(ui.calls.filter(c=>c.command==='thread_start').length,1);
  });
});

async function ordinaryContinueCase({initialThread = false, outcome = 'success', source = g, contextState = null}) {
  const container = document.createElement('div');
  document.body.appendChild(container);
  const root = createRoot(container);
  const calls = [];
  const unknownRole = {standing: 'unknown', reason: 'original App role not established in this App process'};
  const metadata = {thread: {id: 'stored', status: {type: 'notLoaded'}, agentRole: 'HELP_HUMAN'}};
  const query = {factory_id: 1, query_id: 2, home: source.home, generation: source, method: 'thread/resume', params: {threadId: 'stored'}};
  const existing = {...thread('existing', null), generation: source};
  let continueResponded = false;
  const interleave = outcome === 'delayed-source-choice' || outcome === 'delayed-chat-choice';
  let releaseDecision, decisionHeld, pendingContinue;
  const heldDecision = new Promise(resolve => {releaseDecision = resolve;});
  const reachedDecision = new Promise(resolve => {decisionHeld = resolve;});
  let holdNextDecision = interleave;
  let expectedKey = outcome === 'success' ? JSON.stringify([source, 'stored']) : initialThread ? JSON.stringify([source, 'existing']) : '';
  let snapshot = {...host, generation: source, threads: interleave ? [existing, {...thread('other-current', null), generation: source}] : initialThread ? [existing] : [],
    homeRouting: {activeModeHomeClass: 'account', entries: [{modeHomeClass: 'account'}, {modeHomeClass: 'api-key'}]},
    nativeHistory: {state: 'history-receiving', home: source.home, generation: source, selectionEpoch: 0, threads: [{native: metadata.thread}], dispatches: outcome === 'old-admission' ? [{requestRef: 'req:resume'}] : []}};
  const previous = window.__TAURI_INTERNALS__;
  window.__TAURI_INTERNALS__ = {invoke: async (command, args) => {
    calls.push({command, args});
    if (command === 'host_status') {
      if (outcome === 'refresh-failed' && continueResponded) throw Error('Current source read failed');
      return snapshot;
    }
    if (command === 'decision_view') {
      if (continueResponded && holdNextDecision) {holdNextDecision = false; decisionHeld(); return heldDecision;}
      return {rows: []};
    }
    if (command === 'select_home') {
      const nextSource = {...source, home: 'chosen-other-home', spawnCounter: 2};
      snapshot = {...snapshot, generation: nextSource, homeRouting: {...snapshot.homeRouting, activeModeHomeClass: args.modeHomeClass},
        threads: [{...thread('other-current', null), generation: nextSource}],
        nativeHistory: {...snapshot.nativeHistory, generation: nextSource, home: nextSource.home, selectionEpoch: 0, selected: null, dispatches: []}};
      return {state: 'selected'};
    }
    if (command === 'native_confirmation_content') return [];
    if (command === 'history_select') {
      snapshot = {...snapshot, nativeHistory: {...snapshot.nativeHistory, selectionEpoch: 1, selected: {threadId: args.threadId, state: 'indexed-read-only', appRole: unknownRole}}};
      return snapshot.nativeHistory;
    }
    if (command !== 'history_action') throw Error(`Unexpected native command: ${command}`);
    if (args.action === 'metadata') {
      snapshot = {...snapshot, nativeHistory: {...snapshot.nativeHistory, selected: {...snapshot.nativeHistory.selected, metadata}}};
      return snapshot.nativeHistory;
    }
    assert.equal(args.action, 'continue');
    if (outcome === 'refused' || outcome === 'failed') throw Error(`Native resume ${outcome}`);
    const admitted = {generation: source, threadId: 'stored', status: {type: 'idle'}, appRole: unknownRole, nativeResumeObserved: true, resumeRequestRef: 'req:resume'};
    const dispatch = {generation: source, home: source.home, requestRef: 'req:resume', writeResult: 'written', outcome: 'response-observed-result', sourceCurrent: true, localQuery: query, activeAdmission: admitted};
    const result = {...snapshot.nativeHistory, selected: {...snapshot.nativeHistory.selected, state: 'resume-response-observed', resumeEligibilityCurrent: true,
      resume: {thread: {...metadata.thread, status: {type: 'idle'}}}, streamResolutions: {'thread-state': {outcome: 'native-result-observed', query}}}, dispatches: [dispatch]};
    if (outcome === 'read-only') result.selected.state = 'indexed-read-only';
    if (outcome === 'ineligible') result.selected.resumeEligibilityCurrent = false;
    if (outcome === 'not-admitted') delete dispatch.activeAdmission;
    if (outcome === 'pending') dispatch.outcome = 'pending';
    if (outcome === 'stale-dispatch') dispatch.sourceCurrent = false;
    if (outcome === 'missing-id') delete admitted.threadId;
    if (outcome === 'missing-generation') delete admitted.generation;
    if (outcome === 'wrong-id') admitted.threadId = 'other';
    if (outcome === 'wrong-query') dispatch.localQuery = {...query, query_id: 99};
    snapshot = {...snapshot, nativeHistory: result, threads: [...snapshot.threads, {...admitted, generation: source, threadId: 'stored'}]};
    if (contextState) {
      const context = continuationFixture({generation: source, admissionSelectionEpoch: 1, state: contextState});
      if (contextState === 'unavailable') {
        context.error = 'Context item read failed';
        context.history.selected.state = 'unavailable';
        context.history.selected.streamResolutions['item-pages'].outcome = 'native-error-observed';
        context.history.selected.errorsByStream['item-pages'] = {message: 'Context item read failed'};
      }
      snapshot = {...snapshot, continuationContexts: [context]};
    }
    if (outcome === 'not-ready') snapshot = {...snapshot, state: 'stopped'};
    if (outcome === 'no-current-thread') snapshot = {...snapshot, threads: initialThread ? [existing] : []};
    continueResponded = true;
    if (outcome === 'source-changed') snapshot = {...snapshot, generation: {...source, spawnCounter: 9}};
    if (outcome === 'selection-changed') snapshot = {...snapshot, nativeHistory: {...result, selectionEpoch: 2}};
    if (outcome === 'query-superseded') snapshot = {...snapshot, nativeHistory: {...result, selected: {...result.selected, streamResolutions: {'thread-state': {outcome: 'native-result-observed', query: {...query, query_id: 99}}}}}};
    return result;
  }};
  try {
    await React.act(async () => {root.render(React.createElement(App));});
    const conversation = () => container.querySelectorAll(element => element.getAttribute('id') === 'conversation')[0];
    const selectedKey = () => props(elements(conversation(), 'select')[0]).value;
    const priorKey = JSON.stringify([source, 'existing']);
    if (initialThread) await change(elements(conversation(), 'select')[0], priorKey);
    const draft = 'Unsent continuation text é / 家';
    await change(elements(conversation(), 'textarea')[0], draft);
    await React.act(async () => {await props(labelled(container, 'select', 'Stored conversation ')).onChange({target: {value: 'stored'}});});
    await React.act(async () => {await props(button(container, 'Read metadata')).onClick();});
    assert.equal(selectedKey(), initialThread ? priorKey : '', 'index and metadata reads do not open an operational chat');
    const continueButton = button(container, 'Continue selected conversation');
    assert.equal(props(continueButton).disabled, false);
    if (interleave) {
      await React.act(async () => {pendingContinue = props(continueButton).onClick(); await reachedDecision;});
      // The old host_status has rendered, but its decision_view is still held.
      if (outcome === 'delayed-source-choice') {
        await React.act(async () => {await props(button(container, 'Use api-key home')).onClick();});
      }
      expectedKey = JSON.stringify([snapshot.generation, 'other-current']);
      await change(elements(conversation(), 'select')[0], expectedKey);
      assert.equal(selectedKey(), expectedKey, 'the person has chosen the newer current chat');
      await React.act(async () => {releaseDecision({rows: []}); await pendingContinue;});
    } else {
      await React.act(async () => {await props(continueButton).onClick();});
    }
    assert.deepEqual(calls.filter(call => call.command === 'history_action').map(call => call.args), ['metadata', 'continue'].map(action => ({generation: source, selectionEpoch: 1, action, cursor: null, direction: 'desc', reference: null})), 'one explicit Continue and no retry');
    assert.ok(calls.every(call => ['host_status', 'decision_view', 'native_confirmation_content', 'history_select', 'history_action', 'select_home'].includes(call.command)), 'Continue never sends text or changes role');
    assert.equal(props(elements(conversation(), 'textarea')[0]).value, draft);
    assert.equal(selectedKey(), expectedKey, 'a delayed Continue cannot replace a newer source or chat choice');
    if (outcome === 'success') {
      assert.equal(props(button(conversation(), 'Send text')).disabled, false);
      assert.ok(conversation().textContent.includes('Role not established in this App process'), 'cold role stays unknown despite native agentRole');
      if (contextState) {
        assert.ok(conversation().textContent.includes('Prior work'), 'the admitted conversation consumes its context');
        if (contextState === 'reading') assert.ok(conversation().textContent.includes('Prior work is loading. The conversation is open'));
        if (contextState === 'unavailable') assert.ok(conversation().textContent.includes('Context item read failed'));
        if (contextState === 'partial') assert.ok(conversation().textContent.includes('Prior agent response') && conversation().textContent.includes('Prior tool output'));
      }
    }
  } finally {
    if (pendingContinue) await React.act(async () => {releaseDecision({rows: []}); await pendingContinue;});
    await React.act(() => root.unmount());
    document.body.removeChild(container);
    window.__TAURI_INTERNALS__ = previous;
  }
}

test('explicit Continue opens the newly admitted current conversation and retains the cold role limit', async () => {
  await ordinaryContinueCase({});
  await ordinaryContinueCase({initialThread: true, source: {...g, home: 'another-home', spawnCounter: 2}});
});

test('Continue opens with pending, failed or accepted bounded prior work while preserving the composer and original admission guard', async () => {
  for (const contextState of ['reading', 'unavailable', 'partial']) await ordinaryContinueCase({initialThread: true, contextState});
});

test('Continue with no matching new current admission preserves selection and composer', async () => {
  for (const outcome of ['read-only', 'ineligible', 'not-admitted', 'refused', 'failed', 'pending', 'stale-dispatch', 'missing-id', 'missing-generation', 'wrong-id', 'wrong-query', 'old-admission', 'source-changed', 'selection-changed', 'query-superseded', 'not-ready', 'no-current-thread', 'refresh-failed']) {
    await ordinaryContinueCase({initialThread: true, outcome});
  }
});


test('a Continue refresh awaiting decision_view cannot overwrite a newer source or chat choice', async () => {
  await ordinaryContinueCase({initialThread: true, outcome: 'delayed-source-choice'});
  await ordinaryContinueCase({initialThread: true, outcome: 'delayed-chat-choice'});
});
