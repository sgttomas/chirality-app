import test from 'node:test';
import assert from 'node:assert/strict';
import {installMiniDom} from './support/mini-dom.mjs';
import {loadSrc} from './support/load-src.mjs';
import {installIdleNativeWaiting} from './support/idle-native-waiting.mjs';
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
// The account home's one connection route: the built-in OpenAI provider with the ChatGPT account entry.
const ROUTE = 'Use my ChatGPT account (built-in OpenAI)';
const routeChosen = container => { const route = button(container, ROUTE); return !!route && props(route)['aria-pressed'] === true; };
const chooseRoute = async container => { if (!routeChosen(container)) await React.act(async () => { await props(button(container, ROUTE)).onClick(); }); };

async function ordinaryStartCase({initialThread = false, startGeneration = g, outcome = 'success'}) {
  const container = document.createElement('div');
  document.body.appendChild(container);
  const root = createRoot(container);
  const calls = [];
  let snapshot = {...host, threads: initialThread ? [thread('existing', null)] : [],
    homeRouting: {activeModeHomeClass: 'account'},
    roleSet: {available: true, defaultRole: 'HELP_HUMAN', roles: [{name: 'HELP_HUMAN', meaning: 'Alignment', default_for_new_chat: true}]}};
  const idle = installIdleNativeWaiting(async (command, args) => {
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
  });
  try {
    await React.act(async () => {root.render(React.createElement(App));});
    const conversation = () => container.querySelectorAll(element => element.getAttribute('id') === 'conversation')[0];
    const selectedKey = () => props(elements(conversation(), 'select')[0]).value;
    if (initialThread) await change(elements(conversation(), 'select')[0], key('existing'));
    await chooseRoute(container);
    await change(labelled(container, 'input', 'Model '), 'chosen-model');
    const draft = 'Unsent person text é / 家';
    await change(elements(conversation(), 'textarea')[0], draft);
    const start = button(container, 'Start thread');
    assert.equal(props(start).disabled, false);
    await React.act(async () => {await props(start).onClick();});
    assert.deepEqual(calls.filter(call => call.command === 'thread_start'), [{command: 'thread_start', args: {
      model: 'chosen-model', modelProvider: 'openai', entryId: 'chatgpt-account', modeHomeClass: 'account', generation: g, role: 'HELP_HUMAN', preselected: true,
    }}], 'one person-initiated start with the chosen configuration');
    assert.ok(calls.every(call => ['host_status', 'decision_view', 'native_confirmation_content', 'thread_start'].includes(call.command)), 'Start never sends composer text or retries');
    assert.equal(props(elements(conversation(), 'textarea')[0]).value, draft, 'unsent composer retained');
    if (outcome === 'success') {
      assert.equal(selectedKey(), JSON.stringify([startGeneration, 'created']), 'opens the native ID in the returned start generation');
      // ACCESS REQ-004/CS-9: admission consumes this new-conversation choice;
      // it does not apply the same choice to another conversation.
      assert.equal(props(labelled(container, 'input', 'Model ')).value, '', 'the next conversation has no model selected');
      assert.equal(routeChosen(container), false, 'the next conversation has no connection chosen');
      assert.equal(props(button(container, 'Start thread')).disabled, true, 'a second start needs a fresh explicit choice');
      assert.equal(props(button(conversation(), 'Send text')).disabled, false, 'the displayed new conversation can receive an explicit send');
      const headers = conversation().querySelectorAll(element => element.getAttribute('aria-label') === 'Conversation role');
      assert.equal(headers.length, 1);
      assert.ok(headers[0].textContent.startsWith('Role: HELP_HUMAN.'), 'shows the new conversation');
    } else {
      assert.equal(selectedKey(), initialThread ? key('existing') : '', 'unsuccessful start keeps the selection');
      assert.deepEqual([props(labelled(container,'input','Model ')).value, routeChosen(container)],
        ['chosen-model', true],'a refused, unknown or incomplete attempt keeps its explicit chooser for retry');
      assert.equal(props(button(container,'Start thread')).disabled,false);
      assert.equal(props(button(conversation(), 'Send text')).disabled, !initialThread);
      if (outcome === 'refused' || outcome === 'failed') assert.ok(container.textContent.includes('thread_start: Error: Native start'));
    }
  } finally {
    const renderedText = container.textContent;
    await React.act(() => root.unmount());
    document.body.removeChild(container);
    idle.restore(renderedText);
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
// configured source homes, including observed legacy API homes. No provider/authentication is invoked by this peer.
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
  const idle=installIdleNativeWaiting(async(command,args)=>{
    calls.push({command,args});
    if(command==='host_status'){if(statusFailure)throw Error('Current status read unavailable');return snapshot();}
    if(command==='decision_view')return decisionReply?decisionReply(active):{rows:[]};
    if(command==='native_confirmation_content')return [];
    if(command==='select_home'){if(homeReply)await homeReply(args,active);active=args.modeHomeClass;return {state:'selected'};}
    if(command==='read_home_access')return {state:'synthetic source read'};
    assert.equal(command,'thread_start');
    const index=calls.filter(call=>call.command==='thread_start').length;
    return startReply?startReply(args,index,admitted):admitted(args,index);
  });
  const field=(tag,label)=>labelled(container,tag,label);
  // The model field and the route button exist only in the account home.
  const values=()=>({model:field('input','Model ')?props(field('input','Model ')).value:null,route:routeChosen(container)});
  const edit=async(patch)=>{if(patch.route)await chooseRoute(container);if(patch.model!==undefined)await change(field('input','Model '),patch.model);};
  const press=async(text)=>React.act(async()=>{await props(button(container,text)).onClick();});
  try {
    await React.act(async()=>root.render(React.createElement(App)));
    await check({container,calls,idle,homes,values,edit,press,start:()=>button(container,'Start thread'),
      observeHome:async mode=>{active=mode;document.visibilityState='visible';await React.act(async()=>{for(const {type,listener} of [...document.listeners])if(type==='visibilitychange')listener();});},
      failStatus:()=>{statusFailure=true;},generation:()=>homes[active].generation});
  } finally {const renderedText=container.textContent;await React.act(()=>root.unmount());document.body.removeChild(container);idle.restore(renderedText);}
}
const selectedChoice={model:'chosen-model',route:true};
const blankChoice={model:'',route:false};
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
  // The route cannot be unchosen or changed in the account home, so the newer edits are of the model.
  for(const patch of [{model:'new-model'},null]) {
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
    // The omitted legacy home offers no route and no model field, so no choice can be made there.
    await ui.observeHome('api-key');assert.deepEqual(ui.values(),{model:null,route:false});
    assert.equal(button(ui.container,ROUTE),undefined);
    reply.resolve();await React.act(async()=>{await pending;});
    assert.deepEqual(ui.values(),{model:null,route:false});assert.equal(props(ui.start()).disabled,true,'omitted legacy mode cannot dispatch');
    assert.equal(ui.calls.filter(c=>c.command==='thread_start').length,1);
    await ui.press('Start thread');assert.equal(ui.calls.filter(c=>c.command==='thread_start').length,1);
    await ui.press('Use account home');assert.deepEqual(ui.values(),blankChoice,'returning does not restore an invalidated choice');
    await ui.edit(selectedChoice);await ui.press('Start thread');assert.deepEqual(ui.values(),blankChoice);

  },async(args,index,admitted)=>{if(index===1)await reply.promise;return admitted(args,index);});
});

test('an away-and-back home transition protects a newer same-valued choice from the earlier pending success',async()=>{
  const reply=deferred();
  await withStartChooser(async ui=>{
    await ui.edit(selectedChoice);let pending;
    await React.act(()=>{pending=props(ui.start()).onClick();});
    await ui.observeHome('api-key');await ui.press('Use account home');
    assert.deepEqual(ui.values(),blankChoice);await ui.edit(selectedChoice);
    reply.resolve();await React.act(async()=>{await pending;});
    assert.deepEqual(ui.values(),selectedChoice);assert.equal(props(ui.start()).disabled,false);
    assert.equal(ui.calls.filter(c=>c.command==='thread_start').length,1);
  },async(args,index,admitted)=>{await reply.promise;return admitted(args,index);});
});

test('a home transition invalidates prior-home edits but preserves newer target-home edits while its refresh and an older Start finish',async()=>{
  const startReply=deferred(),homeReply=deferred(),targetRead=deferred(),targetReadReached=deferred();
  let holdTargetRead=true,targetSelecting=false;
  await withStartChooser(async ui=>{
    await ui.edit(selectedChoice);let pendingStart,pendingHome;
    await React.act(()=>{pendingStart=props(ui.start()).onClick();});
    await ui.observeHome('api-key');
    await React.act(()=>{pendingHome=props(button(ui.container,'Use account home')).onClick();});
    assert.deepEqual(ui.values(),{model:null,route:false},'the legacy home offers no choice while the account home is selected');
    assert.equal(props(ui.start()).disabled,true,'nothing can start during selection');
    await React.act(async()=>{homeReply.resolve();await targetReadReached.promise;});
    assert.ok(button(ui.container,'Use my ChatGPT account (built-in OpenAI)'));
    assert.deepEqual(ui.values(),blankChoice,'edits made in the legacy source do not become account-home choices');
    const targetChoice={model:'target-home-model',route:true};
    await ui.edit(targetChoice);
    startReply.resolve();await React.act(async()=>{await pendingStart;});
    assert.deepEqual(ui.values(),targetChoice,'the earlier account admission cannot consume the visible account-home draft');
    assert.equal(props(ui.start()).disabled,true,'the home refresh is still pending');
    targetRead.resolve();await React.act(async()=>{await pendingHome;});
    assert.deepEqual(ui.values(),targetChoice);assert.equal(props(ui.start()).disabled,false);
    assert.equal(ui.calls.filter(c=>c.command==='thread_start').length,1,'neither home transition nor editing dispatches a start');
    await ui.press('Start thread');assert.deepEqual(ui.values(),blankChoice);
  },async(args,index,admitted)=>{if(index===1)await startReply.promise;return admitted(args,index);},{
    homeReply:async()=>{await homeReply.promise;targetSelecting=true;},
    decisionReply:async active=>{if(active==='account'&&targetSelecting&&holdTargetRead){holdTargetRead=false;targetReadReached.resolve();await targetRead.promise;}return {rows:[]};},
  });
});

test('a same-class actual generation update while Start is pending does not become another chooser edit',async()=>{
  const reply=deferred();
  await withStartChooser(async ui=>{
    await ui.edit(selectedChoice);let pending;
    await React.act(()=>{pending=props(ui.start()).onClick();});
    const actual={appSession:'actual-session',home:'actual-account-home',spawnCounter:2};
    ui.homes.account.generation=actual;
    await ui.press('Check account status');
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
    assert.ok(ui.container.textContent.includes("thread_start: ")&&ui.container.textContent.includes("The App could not read Codex's status afterwards, so what is shown may be out of date."),'the start outcome stands, then the fixed refresh line');assert.doesNotMatch(ui.container.textContent,/Current status read unavailable/);
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
  const query = {factory_id: 1, query_id: 2, home: source.home, generation: source, method: 'thread/resume', params: {threadId: 'stored', excludeTurns: true}};
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
  const idle = installIdleNativeWaiting(async (command, args) => {
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
      resume: {thread: {...metadata.thread, status: {type: 'idle'}}}, streamResolutions: {'thread-state': {outcome: 'native-result-observed', query, revision: 2}}}, dispatches: [dispatch]};
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
  });
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
        const nextSource={...source,home:'chosen-other-home',spawnCounter:2};
        snapshot={...snapshot,generation:nextSource,homeRouting:{...snapshot.homeRouting,activeModeHomeClass:'api-key'},threads:[{...thread('other-current',null),generation:nextSource}],nativeHistory:{...snapshot.nativeHistory,generation:nextSource,home:nextSource.home,selectionEpoch:0,selected:null,dispatches:[]}};
        document.visibilityState='visible';await React.act(async()=>{for(const {type,listener} of [...document.listeners])if(type==='visibilitychange')listener();});
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
    const renderedText = container.textContent;
    await React.act(() => root.unmount());
    document.body.removeChild(container);
    idle.restore(renderedText);
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


test('idle native waiting startup reads no intent, performs no action and cleans up its listener and polling on App unmount', async t => {
  const intervals = new Map();
  t.mock.method(globalThis, 'setInterval', (callback, delay) => {
    const token = {}; intervals.set(token, {callback, delay}); return token;
  });
  t.mock.method(globalThis, 'clearInterval', token => {
    assert.ok(intervals.delete(token), 'clear an installed App interval exactly once');
  });
  let idle, waitingPoll;
  await withStartChooser(async ui => {
    idle = ui.idle;
    assert.deepEqual(idle.calls.map(call => call.command), ['checkpoint_native_waiting_ui', 'plugin:event|listen', 'claim_native_waiting_intent'],
      'startup acknowledges its UI checkpoint, installs the listener, then reads host intent once');
    assert.ok(ui.calls.every(call => ['host_status', 'decision_view', 'native_confirmation_content'].includes(call.command)),
      'a null waiting claim never navigates, starts, resumes, sends or answers');
    assert.deepEqual(ui.values(), blankChoice);
    idle.assertClean(ui.container);
    for (const {callback} of intervals.values()) {
      const claimsBefore = idle.calls.filter(call => call.command === 'claim_native_waiting_intent').length;
      await React.act(async () => {callback();});
      if (idle.calls.filter(call => call.command === 'claim_native_waiting_intent').length > claimsBefore) waitingPoll = callback;
    }
    assert.equal(typeof waitingPoll, 'function', 'the mounted App installs its waiting recovery poll');
    assert.deepEqual(idle.calls.filter(call => call.command === 'claim_native_waiting_intent').map(call => call.args.consumer),
      [idle.calls[0].args.consumer, idle.calls[0].args.consumer], 'polls read the same single-use consumer without a target');
    // read_fleet_records is the "Waiting on you" timer's read, on hostReads' timed-read list: it writes nothing.
    assert.ok(ui.calls.every(call => ['host_status', 'decision_view', 'native_confirmation_content', 'read_fleet_records'].includes(call.command)),
      'an idle recovery poll also performs no navigation or supplier action');
  });
  assert.equal(intervals.size, 0, 'App unmount clears every installed poll, including native waiting');
  assert.equal(idle.calls.filter(call => call.command === 'plugin:event|unlisten').length, 1);
  const callsAfterUnmount = idle.calls.length;
  await waitingPoll();
  assert.equal(idle.calls.length, callsAfterUnmount, 'an already queued waiting tick stops after effect cleanup');
});

const ordinaryModelLabel = 'Optional model identifier for next ordinary text turn ';
const region = (container, label) => container.querySelectorAll(e => e.getAttribute('aria-label') === label)[0];
const flush = () => new Promise(resolve => setImmediate(resolve));

async function withOrdinarySend(check, native) {
  const container = document.createElement('div'); document.body.appendChild(container); const root = createRoot(container);
  const calls = []; let refreshFailure = false;
  const snapshot = {...host, homeRouting: {activeModeHomeClass: 'account'}, planMode: {state: 'offered'},
    threads: host.threads.map(row => ({...row, model: 'reported-original', modelProvider: 'original-provider'}))};
  const idle = installIdleNativeWaiting(async (command, args) => {
    calls.push({command, args});
    if (command === 'host_status') {if (refreshFailure) throw Error('Original observer unavailable'); return snapshot;}
    if (command === 'decision_view') return {rows: []};
    if (command === 'native_confirmation_content') return [];
    assert.equal(command, 'conversation_send_text', 'ordinary controls have one native command');
    return native(args, () => {refreshFailure = true;});
  });
  try {
    await React.act(async () => root.render(React.createElement(App)));
    const panel = () => container.querySelectorAll(e => e.getAttribute('id') === 'conversation')[0];
    await change(elements(panel(), 'select')[0], key('thread-a'));
    await check({container, calls, panel, model: () => labelled(panel(), 'input', ordinaryModelLabel), text: () => elements(panel(), 'textarea')[0],
      press: async label => React.act(async () => {props(button(panel(), label)).onClick(); await flush();})});
  } finally {const text = container.textContent; await React.act(() => root.unmount()); document.body.removeChild(container); idle.restore(text);}
}

test('mounted App ordinary controls send only their exact explicit choice and full current target', async () => {
  for (const [mode, label] of [[undefined, 'Send text'], ['plan', 'Send in plan mode (experimental)'], ['default', 'Send in default mode (carry out / leave plan mode)']]) {
    for (const model of ['', 'exact-model/é']) await withOrdinarySend(async ui => {
      await change(labelled(ui.container, 'input', 'Model '), 'new-conversation-only');
      await change(ui.model(), model); await change(ui.text(), 'Exact ordinary text 家\n');
      assert.equal(ui.calls.filter(c => c.command === 'conversation_send_text').length, 0, 'editing sends nothing');
      await ui.press(label);
      assert.deepEqual(ui.calls.filter(c => c.command === 'conversation_send_text'), [{command: 'conversation_send_text', args: {
        generation: g, threadId: 'thread-a', text: 'Exact ordinary text 家\n', mode: mode ?? null, ...(model ? {model} : {}),
      }}]);
      assert.equal(props(ui.model()).value, ''); assert.equal(props(ui.text()).value, '');
      assert.equal(props(labelled(ui.container, 'input', 'Model ')).value, 'new-conversation-only');
      assert.match(region(ui.panel(), 'Ordinary text submission outcome').textContent, /Model adoption, execution and completion remain unestablished/);
      assert.match(ui.panel().textContent, /this turn and subsequent native turns; clearing this field does not revert it/);
      assert.match(ui.panel().textContent, /reported-original via original-provider/);
    }, async () => ({result: {turn: {id: 'native-turn', status: 'inProgress', items: []}}}));
  }
});

test('ordinary native result is immutable across observer failure, with refusal/unknown drafts retained', async () => {
  for (const outcome of ['acknowledged', 'refused', 'unknown']) await withOrdinarySend(async ui => {
    await change(ui.model(), 'unsent-explicit'); await change(ui.text(), 'Unsent ordinary draft');
    await ui.press('Send text');
    const shown = region(ui.panel(), 'Ordinary text submission outcome').textContent;
    assert.match(shown, /Original ordinary text turn · conversation thread-a · Home h · App session s · spawn 1/);
    // A failed refresh is shown only as the fixed line (App Agent 0's decision), never its raw diagnostic.
    assert.ok(shown.includes("The App could not read Codex's status afterwards, so what is shown may be out of date."), shown); assert.doesNotMatch(shown, /Original observer unavailable/);
    if (outcome === 'acknowledged') {
      assert.match(shown, /Native turn\/start response received/); assert.doesNotMatch(shown, /Original native/);
      assert.equal(props(ui.model()).value, ''); assert.equal(props(ui.text()).value, '');
    } else {
      assert.match(shown, new RegExp(`Original native ${outcome}`));
      assert.equal(props(ui.model()).value, 'unsent-explicit'); assert.equal(props(ui.text()).value, 'Unsent ordinary draft');
    }
    assert.equal(ui.calls.filter(c => c.command === 'conversation_send_text').length, 1, 'no retry, substitution or fallback');
  }, async (_args, failRefresh) => {failRefresh(); if (outcome !== 'acknowledged') throw Error(`Original native ${outcome}`); return {result: {turn: {id: 'ack'}}};});
});

async function withOrdinaryPanel(check, send = noop, observeOrdinaryView = noop) {
  const container = document.createElement('div'); const root = createRoot(container); document.body.appendChild(container);
  const show = async (generation = g, threadId = 'thread-a', state = 'ready') => React.act(() => root.render(React.createElement(ConversationPanel, {
    host: {...host, generation, state, threads: [{...thread(threadId, null), generation}]}, threadKey: JSON.stringify([generation, threadId]), setThreadKey: noop,
    answer: noop, runAct: noop, send, observeOrdinaryView, steer: noop, submitAttachments: noop, interrupt: noop, checkPlanMode: noop, codexBusy: false,
  })));
  const model = () => labelled(container, 'input', ordinaryModelLabel), text = () => elements(container, 'textarea')[0];
  try {await show(); await check({container, show, model, text, press: () => React.act(async () => {props(button(container, 'Send text')).onClick(); await flush();})});}
  finally {await React.act(() => root.unmount()); document.body.removeChild(container);}
}

test('local ordinary model lifetime follows full conversation identity while the ordinary text draft stays global', async () => {
  await withOrdinaryPanel(async ui => {
    await change(ui.text(), 'One global ordinary text draft');
    for (const [generation, id] of [[g, 'thread-b'], [{...g, home: 'foreign-home'}, 'thread-b'], [{...g, appSession: 'new-session'}, 'thread-b'], [{...g, spawnCounter: 2}, 'thread-b'], [g, 'thread-a']]) {
      await change(ui.model(), 'previous-conversation-choice'); await ui.show(generation, id);
      assert.equal(props(ui.model()).value, '', 'no previous full conversation choice is applied');
      assert.equal(props(ui.text()).value, 'One global ordinary text draft');
    }
  });
});

test('late ordinary outcome cannot clear newer text/model, including away-and-back edits and targets', async () => {
  for (const supersession of ['edits', 'conversation', 'home', 'generation', 'close', 'away-back']) {
    const held = deferred(); const calls = [];
    await withOrdinaryPanel(async ui => {
      await change(ui.text(), 'original text'); await change(ui.model(), 'original-model');
      await ui.press();
      assert.deepEqual(calls, [[g, 'thread-a', 'original text', undefined, 'original-model']]);
      if (supersession === 'edits') {
        await change(ui.text(), 'temporary'); await change(ui.text(), 'original text');
        await change(ui.model(), 'temporary'); await change(ui.model(), 'original-model');
      } else {
        if (supersession === 'away-back') {await ui.show(g, 'thread-b'); await ui.show();}
        else if (supersession === 'conversation') await ui.show(g, 'thread-b');
        else if (supersession === 'home') await ui.show({...g, home: 'another-home'});
        else if (supersession === 'generation') await ui.show({...g, spawnCounter: 2});
        else await ui.show(g, 'thread-a', 'stopped');
        await change(ui.text(), 'newer text'); await change(ui.model(), 'newer-model');
      }
      await React.act(async () => {held.resolve({result: {turn: {id: 'original-native'}}}); await flush();});
      assert.equal(props(ui.text()).value, supersession === 'edits' ? 'original text' : 'newer text');
      assert.equal(props(ui.model()).value, supersession === 'edits' ? 'original-model' : 'newer-model');
      const shown = region(ui.container, 'Ordinary text submission outcome').textContent;
      assert.match(shown, /conversation thread-a · Home h · App session s · spawn 1/);
      assert.match(shown, /requested model original-model/);
      assert.match(shown, /Native turn\/start response received/);
      assert.match(shown, /original observer failure/);
      assert.equal(calls.length, 1);
    }, async (...args) => {calls.push(args); return held.promise;}, async () => {throw Error('original observer failure');});
  }
});

// Deferred mocked IPC exercises the mounted App and its actual polling/home/
// conversation handlers. No native producer, supplier or filesystem is invoked.
async function withDeferredConversationAction(t, command, check, {refused = false, refreshFailed = false} = {}) {
  const native = deferred(), read = deferred(), calls = [], unexpected = [];
  let nativeFinished = false, readStarted = false, snapshot;
  const makeSnapshot = (generation = g, mode = 'account', marker = 'original-view') => ({...host, generation,
    supplierStanding: marker, homeRouting: {activeModeHomeClass: mode, entries: [{modeHomeClass: 'account'}, {modeHomeClass: 'api-key'}]},
    threads: host.threads.map(row => ({...row, generation})),
    conversationTurns: [{generation, threadId: 'thread-a', turnId: 'live-a', nativeTurn: {id: 'live-a', status: 'inProgress', items: []}}],
    steeringTargets: [{generation, threadId: 'thread-a', target: {generation, threadId: 'thread-a', turnId: 'live-a'}}],
  });
  snapshot = makeSnapshot();
  const idle = installIdleNativeWaiting(async (name, args) => {
    calls.push({command: name, args: structuredClone(args)});
    if (name === command) {
      await native.promise; nativeFinished = true;
      if (refused) throw Error('Original native refusal');
      return {nativeAcknowledgment: 'original-request'};
    }
    if (name === 'host_status') {
      if (nativeFinished && !readStarted) {
        readStarted = true;
        await read.promise;
        if (refreshFailed) throw Error('Original refresh failure');
        return makeSnapshot(g, 'account', 'original-command-refresh');
      }
      return structuredClone(snapshot);
    }
    if (name === 'decision_view') return {rows: []};
    if (name === 'native_confirmation_content') return [];
    if (name === 'select_home') {
      snapshot = makeSnapshot(args.modeHomeClass === 'account' ? g : {...g, home: 'other-home'}, args.modeHomeClass, 'navigated-view');
      return {};
    }
    unexpected.push(name); throw Error(`Unexpected IPC: ${name}`);
  });
  t.mock.timers.enable({apis: ['setInterval']});
  const container = document.createElement('div'); document.body.appendChild(container); const root = createRoot(container);
  const panel = () => container.querySelectorAll(e => e.getAttribute('id') === 'conversation')[0];
  const text = () => elements(panel(), 'textarea')[0];
  const actionLabel = command === 'conversation_steer_text' ? 'Steer current live turn' : 'Interrupt selected live turn';
  const ui = {container, calls, panel, text,
    async start() {
      await change(elements(panel(), 'select')[0], key('thread-a'));
      await change(text(), 'original steering text');
      if (command === 'conversation_interrupt') await change(labelled(panel(), 'select', 'Observed live turn '), 'live-a');
      const control = button(panel(), actionLabel); assert.equal(!!props(control).disabled, false);
      // Two deliveries before React commits busy state must still dispatch once.
      await React.act(async () => {props(control).onClick(); props(control).onClick(); await flush();});
    },
    async releaseNative() {await React.act(async () => {native.resolve(); await flush();});},
    async releaseRead() {await React.act(async () => {read.resolve(); await flush();});},
    get readStarted() {return readStarted;},
    async supersede(kind) {
      if (kind === 'text' || kind === 'same-text') {
        // Controlled edit delivery stresses the revision guard even while the
        // composer is disabled; these are not claims about browser input timing.
        await change(text(), 'newer steering text');
        if (kind === 'same-text') await change(text(), 'original steering text');
      } else if (kind === 'thread') {
        await change(elements(panel(), 'select')[0], key('thread-b'));
      } else if (kind === 'thread-away-back') {
        // Other App navigation surfaces can change this shared selection. Drive
        // the real handler twice before rendering: final thread/generation and
        // object equality cannot detect this; the dispatch intent ticket must.
        const choose = props(elements(panel(), 'select')[0]).onChange;
        await React.act(() => {
          choose({target: {value: key('thread-b')}});
          choose({target: {value: key('thread-a')}});
        });
      } else if (kind === 'home' || kind === 'home-away-back') {
        snapshot=makeSnapshot({...g,home:'other-home'},'api-key','navigated-view');
        await React.act(async()=>{t.mock.timers.tick(1000);await flush();});
        if (kind === 'home-away-back') await React.act(async () => {await props(button(container, 'Use account home')).onClick();});
      } else if (kind === 'generation' || kind === 'snapshot') {
        snapshot = makeSnapshot(kind === 'generation' ? {...g, spawnCounter: 2} : g, 'account', 'newer-poll-view');
        await React.act(async () => {t.mock.timers.tick(1000); await flush();});
      }
    },
  };
  try {
    await React.act(async () => {root.render(React.createElement(App));});
    await check(ui);
    const sent = calls.filter(row => row.command === command);
    assert.equal(sent.length, 1, 'one dispatch, no double delivery or automatic retry');
    assert.deepEqual(sent[0].args, command === 'conversation_steer_text'
      ? {generation: g, threadId: 'thread-a', expectedTurnId: 'live-a', text: 'original steering text'}
      : {generation: g, threadId: 'thread-a', turnId: 'live-a'});
    assert.deepEqual(unexpected, []);
  } finally {
    await React.act(async () => {native.resolve(); read.resolve(); await flush();});
    idle.assertClean(container); const rendered = container.textContent;
    await React.act(async () => {root.unmount();}); document.body.removeChild(container); idle.restore(rendered);
  }
}

for (const command of ['conversation_steer_text', 'conversation_interrupt']) {
  test(`deferred ${command} dispatches once before busy commits`, async t => {
    await withDeferredConversationAction(t, command, async ui => {
      await ui.start(); await ui.releaseNative(); await ui.releaseRead();
    });
  });

  test(`deferred ${command} preserves newer ownership, text and native outcome`, async t => {
    for (const phase of ['native', 'refresh']) for (const kind of ['none', 'text', 'same-text', 'thread', 'home', 'generation', 'snapshot', 'home-away-back', 'thread-away-back']) {
      await t.test(`${phase}: ${kind}`, async t => {
        await withDeferredConversationAction(t, command, async ui => {
          await ui.start();
          if (phase === 'refresh') {await ui.releaseNative(); assert.equal(ui.readStarted, true);}
          if (kind !== 'none') await ui.supersede(kind);
          const shownBefore = ui.container.textContent;
          await ui.releaseNative(); await ui.releaseRead();
          const superseded = ['thread', 'home', 'generation', 'home-away-back', 'thread-away-back'].includes(kind);
          const expectedText = kind === 'text' ? 'newer steering text'
            : command === 'conversation_interrupt' || superseded || kind === 'same-text' ? 'original steering text' : '';
          assert.equal(props(ui.text()).value, expectedText, 'only unchanged text owned by the original steering may clear');
          if (kind === 'snapshot' || kind === 'generation') assert.ok(ui.container.textContent.includes('newer-poll-view'), 'late action read cannot replace the newer poll');
          if (kind === 'home' || kind === 'home-away-back') assert.ok(ui.container.textContent.includes('navigated-view'), 'late action read cannot undo home navigation');
          const outcome = region(ui.container, 'Original conversation action outcome');
          assert.ok(outcome, 'result remains explicitly bound to the original request');
          assert.match(outcome.textContent, /conversation thread-a · Home h · App session s · spawn 1 · turn live-a/);
          assert.match(outcome.textContent, command === 'conversation_steer_text' ? /Native steering acknowledgment received/ : /Native interrupt acknowledgment received/);
          assert.match(outcome.textContent, /No automatic retry/);
          if (superseded || kind === 'snapshot') assert.match(outcome.textContent, /refresh.*superseded/i);
          if (phase === 'native' && (superseded || kind === 'snapshot')) assert.equal(ui.readStarted, false, 'superseded dispatch does not start an old refresh');
          if (phase === 'refresh') assert.match(shownBefore, /Native (steering|interrupt) acknowledgment received/, 'native result visible while refresh waits');
        });
      });
    }
  });

  test(`deferred ${command} preserves refusal separately from refresh failure or supersession`, async t => {
    for (const refused of [false, true]) for (const superseded of [false, 'thread', 'thread-away-back']) await t.test(`${refused ? 'refusal' : 'ack'}: ${superseded || 'refresh fails'}`, async t => {
      await withDeferredConversationAction(t, command, async ui => {
        await ui.start();
        if (superseded) await ui.supersede(superseded);
        await ui.releaseNative(); await ui.releaseRead();
        assert.equal(props(ui.text()).value, refused || superseded || command === 'conversation_interrupt' ? 'original steering text' : '');
        const outcome = region(ui.container, 'Original conversation action outcome');
        assert.ok(outcome);
        assert.match(outcome.textContent, refused ? /Original native refusal/ : /Native (steering|interrupt) acknowledgment received/);
        // A supersession keeps its own message; a failed refresh is shown only as the fixed line (App Agent 0's decision).
        if (superseded) assert.match(outcome.textContent, /superseded/); else assert.ok(outcome.textContent.includes("The App could not read Codex's status afterwards, so what is shown may be out of date."), outcome.textContent);
        assert.doesNotMatch(outcome.textContent, /Original refresh failure/);
        assert.match(outcome.textContent, /command outcome.*unchanged/i);
        assert.equal(ui.panel().querySelectorAll(e => e.getAttribute('role') === 'alert').filter(e => e.textContent.includes('Original native refusal')).length, 0,
          'old refusal is not assigned to the selected conversation error');
      }, {refused, refreshFailed: true});
    });
  });
}

async function withReadinessPanel(check) {
  const c=document.createElement('div');document.body.appendChild(c);const root=createRoot(c),calls=[];
  let current={...host,conversationTurns:[{generation:g,threadId:'thread-a',turnId:'live-a',nativeTurn:{id:'live-a',status:'inProgress'}}]},selected=key('thread-a'),processBusy=false;
  let interruptResult=async()=>true;
  const show=()=>React.act(()=>root.render(React.createElement(ConversationPanel,{host:current,threadKey:selected,setThreadKey:value=>{selected=value;},answer:noop,runAct:noop,send:async(...args)=>calls.push(['send',args]),steer:noop,submitAttachments:noop,interrupt:async(...args)=>{calls.push(['interrupt',args]);return interruptResult();},checkPlanMode:noop,codexBusy:processBusy})));
  const byId=id=>c.querySelectorAll(n=>n.getAttribute('id')===id)[0];
  try {await show();await check({c,calls,show,byId,get host(){return current;},setHost:value=>{current=value;},choose:value=>{selected=value;},setBusy:value=>{processBusy=value;},interruptWith:value=>{interruptResult=value;}});}
  finally {await React.act(()=>root.unmount());document.body.removeChild(c);}
}

test('ordinary send explains disconnected, unselected, empty and ready states without losing the draft',async()=>{
 await withReadinessPanel(async ui=>{
  assert.match(ui.byId('ordinary-send-readiness').textContent,/Write a message/);
  await change(elements(ui.c,'textarea')[0],'Retained ordinary draft');
  assert.match(ui.byId('ordinary-send-readiness').textContent,/Ready to send text to Conversation 1 · model not reported\./,'the destination is named in the person\'s words');
  assert.equal(props(button(ui.c,'Send text'))['aria-describedby'],'ordinary-send-readiness');
  ui.choose('');await ui.show();assert.match(ui.byId('ordinary-send-readiness').textContent,/Choose a current conversation/);
  assert.equal(props(button(ui.c,'Send text')).disabled,true);
  ui.setHost({...ui.host,state:'stopped'});await ui.show();assert.match(ui.byId('ordinary-send-readiness').textContent,/Connect to Codex/);
  assert.equal(props(elements(ui.c,'textarea')[0]).value,'Retained ordinary draft');assert.deepEqual(ui.calls,[]);
 });
});

test('offered interrupt works during process-operation busy while sends stay paused and duplicate callbacks refuse',async()=>{
 await withReadinessPanel(async ui=>{
  await change(elements(ui.c,'textarea')[0],'Keep this text');
  await change(labelled(ui.c,'select','Observed live turn '),'live-a');
  ui.setBusy(true);await ui.show();
  assert.equal(props(button(ui.c,'Send text')).disabled,true);
  const interrupt=button(ui.c,'Interrupt selected live turn');assert.equal(props(interrupt).disabled,false);
  const held=deferred();ui.interruptWith(()=>held.promise);let pending;
  await React.act(()=>{pending=props(interrupt).onClick();void props(interrupt).onClick();});
  assert.deepEqual(ui.calls,[['interrupt',[g,'thread-a','live-a']]]);
  assert.equal(props(button(ui.c,'Interrupt selected live turn')).disabled,true);
  assert.match(ui.byId('conversation-interrupt-readiness').textContent,/pending conversation operation/);
  await React.act(async()=>{held.resolve(true);await pending;});
  assert.equal(props(elements(ui.c,'textarea')[0]).value,'Keep this text');
  assert.match(ui.byId('conversation-interrupt-readiness').textContent,/does not end a workflow run/);
  assert.equal(props(button(ui.c,'Send text')).disabled,true);
 });
});

test('closed sources, unobserved turns and already requested interruption explain refusal without dispatch',async()=>{
 await withReadinessPanel(async ui=>{
  assert.match(ui.byId('conversation-interrupt-readiness').textContent,/Choose an observed live turn/);
  await change(labelled(ui.c,'select','Observed live turn '),'live-a');
  ui.setHost({...ui.host,generationClosed:true});await ui.show();
  const interrupted=button(ui.c,'Interrupt selected live turn');assert.equal(props(interrupted).disabled,true);
  await React.act(async()=>props(interrupted).onClick());assert.deepEqual(ui.calls,[]);
  assert.match(ui.byId('conversation-interrupt-readiness').textContent,/source is not ready/);
  ui.setHost({...ui.host,generationClosed:false,turnInterruptRequests:[{binding:{generation:g,threadId:'thread-a',turnId:'live-a'},clientRequest:{outcome:'response-observed-result'}}]});await ui.show();
  assert.equal(props(button(ui.c,'Interrupt selected live turn')).disabled,true);assert.match(ui.byId('conversation-interrupt-readiness').textContent,/already requested/);
  ui.setHost({...ui.host,conversationTurns:[]});await ui.show();assert.match(ui.byId('conversation-interrupt-readiness').textContent,/No current live turn is observed/);
  assert.deepEqual(ui.calls,[]);
 });
});

// Wiring of the Codex process controls and the conversation's stop labels,
// exercised through mounted components rather than read from source text.
test('Stop and Restart Codex call only the asking codex_stop command for the current generation', async () => {
  const {CodexProcessControls} = loadSrc('CodexControls');
  const c = document.createElement('div'); document.body.appendChild(c); const root = createRoot(c);
  const calls = [];
  try {
    await React.act(() => root.render(React.createElement(CodexProcessControls, {
      host: {state: 'ready', generation: g, homeRouting: {activeModeHomeClass: 'account'}, codexStops: {outcomes: [], stopWaitLimitSeconds: 10, records: ''}},
      busy: false, act: (command, args) => calls.push([command, args])})));
    for (const control of elements(c, 'button')) await React.act(() => props(control).onClick());
    assert.deepEqual(calls.filter(([command]) => command === 'codex_stop'),
      [['codex_stop', {generation: g, restart: false}], ['codex_stop', {generation: g, restart: true}]]);
    assert.deepEqual(calls.map(([command]) => command).sort(), ['codex_stop', 'codex_stop', 'host_start'],
      'no control sends an unconfirmed stop');
  } finally { await React.act(() => root.unmount()); document.body.removeChild(c); }
});

test('conversation activity labels a turn from this home\'s stop records and the Stop Codex outcome', async () => {
  const c = document.createElement('div'); document.body.appendChild(c); const root = createRoot(c);
  const view = {home: g.home, generation: g, typesPin: '0.160.0', supplierStanding: 'unverified-development', limits: [],
    items: ['t1', 't2'].map((turnId, i) => ({threadId: 'thread-a', turnId, native: {id: `m-${turnId}`, type: 'agentMessage', text: `reply ${turnId}`},
      displayState: 'completed', observedOrder: i, standing: 'live-observed'})),
    turns: [{id: 't1', status: 'interrupted', startedAt: 1}, {id: 't2', status: 'interrupted', startedAt: 2}],
    turnRecords: [{threadId: 'thread-a', turnId: 't1'}, {threadId: 'thread-a', turnId: 't2'}], revisions: [], goals: {}, checklistGaps: [], descendants: []};
  const record = {stopRequestId: 'stop:1', appSession: 's', earlierSession: false, home: 'H-acct', generation: 'gen', threadId: 'thread-a', turnId: 't1',
    cause: 'person-interrupt', requestedAt: '2026-10-10T00:00:01Z', state: 'outcome-observed', label: 'interrupted by the person',
    reading: 'Final status observed when the turn ended.', codexReported: 'interrupted', persistence: 'recorded in the App ledger'};
  const outcome = {action: 'Stop Codex', state: 'stopped', generation: g, turns: [{threadId: 'thread-a', turnId: 't2', label: 'interrupted by Stop Codex', codexReported: 'interrupted'}]};
  const show = activeModeHomeClass => React.act(() => root.render(React.createElement(ConversationPanel, {
    host: {...host, nativeView: view, homeRouting: {activeModeHomeClass}, codexStops: {outcomes: [outcome]}, stopRequests: {records: [record], limits: []}},
    threadKey: key('thread-a'), setThreadKey: () => {}, answer: noop, runAct: noop, send: noop, steer: noop, submitAttachments: noop, interrupt: noop, checkPlanMode: noop, codexBusy: false})));
  const labels = () => c.querySelectorAll(element => element.localName === 'p' && element.textContent.startsWith('App label:')).map(element => element.textContent);
  try {
    await show('account');
    assert.ok(labels().some(label => label.includes('interrupted by the person')), 'the recorded request of this home labels t1');
    assert.ok(labels().some(label => label.includes('interrupted by Stop Codex')), 'the Stop Codex outcome labels t2');
    await show('api-key');
    assert.ok(!labels().some(label => label.includes('interrupted by the person')), 'another home\'s ledger row does not label this home\'s turn');
    assert.ok(labels().some(label => label.includes('interrupted by Stop Codex')));
  } finally { await React.act(() => root.unmount()); document.body.removeChild(c); }
});

test('while Stop or Restart Codex runs, sends pause but the conversation and live turn stay selectable', async () => {
  await withReadinessPanel(async ui => {
    ui.setBusy(true); await ui.show();
    assert.equal(props(button(ui.c, 'Send text')).disabled, true);
    assert.equal(props(labelled(ui.c, 'select', 'Current-generation conversation ')).disabled, false);
    assert.equal(props(labelled(ui.c, 'select', 'Observed live turn ')).disabled, false);
    await change(labelled(ui.c, 'select', 'Observed live turn '), 'live-a');
    assert.equal(props(button(ui.c, 'Interrupt selected live turn')).disabled, false);
  });
});

test('the App pauses conversation sends for exactly the duration of Stop Codex', async () => {
  const container = document.createElement('div'); document.body.appendChild(container); const root = createRoot(container);
  const calls = [], held = deferred();
  const snapshot = {...host, threads: [thread('existing', null)], homeRouting: {activeModeHomeClass: 'account'}, codexStops: {outcomes: [], stopWaitLimitSeconds: 10, records: ''}};
  const idle = installIdleNativeWaiting(async (command, args) => {
    calls.push({command, args});
    if (command === 'host_status') return snapshot;
    if (command === 'decision_view') return {rows: []};
    if (command === 'native_confirmation_content') return [];
    if (command === 'codex_stop') return held.promise;
    throw Error(`Unexpected native command: ${command}`);
  });
  try {
    await React.act(async () => {root.render(React.createElement(App));});
    const conversation = () => container.querySelectorAll(element => element.getAttribute('id') === 'conversation')[0];
    await change(elements(conversation(), 'select')[0], key('existing'));
    await change(elements(conversation(), 'textarea')[0], 'Kept while Codex stops');
    assert.equal(props(button(conversation(), 'Send text')).disabled, false);
    let pending;
    await React.act(async () => {pending = props(button(container, 'Stop Codex…')).onClick();});
    assert.deepEqual(calls.filter(call => call.command === 'codex_stop').map(call => call.args), [{generation: g, restart: false}]);
    assert.equal(props(button(conversation(), 'Send text')).disabled, true, 'sends wait while Stop Codex runs');
    await React.act(async () => {held.resolve({action: 'Stop Codex', state: 'cancelled', reading: 'kept running'}); await pending;});
    assert.equal(props(button(conversation(), 'Send text')).disabled, false, 'sends resume when it ends');
    assert.equal(props(elements(conversation(), 'textarea')[0]).value, 'Kept while Codex stops');
  } finally {
    const renderedText = container.textContent;
    await React.act(() => root.unmount());
    document.body.removeChild(container);
    idle.restore(renderedText);
  }
});

test('Continue as begins through continue_as_begin for the selected conversation and changes no role', async () => {
  const c = document.createElement('div'); document.body.appendChild(c); const root = createRoot(c);
  const acts = [];
  try {
    await React.act(() => root.render(React.createElement(ConversationPanel, {host, threadKey: key('thread-a'), setThreadKey: () => {}, answer: noop,
      runAct: async (command, args) => { acts.push([command, args]); return {}; }, send: noop, steer: noop, submitAttachments: noop, interrupt: noop, checkPlanMode: noop, codexBusy: false})));
    const offers = elements(c, 'button').filter(element => element.textContent.startsWith('Continue as'));
    assert.ok(offers.length > 0, 'a Continue as control is offered');
    await React.act(async () => { await props(offers[0]).onClick(); });
    assert.equal(acts.length, 1);
    assert.equal(acts[0][0], 'continue_as_begin');
    assert.deepEqual({generation: acts[0][1].generation, threadId: acts[0][1].threadId}, {generation: g, threadId: 'thread-a'});
  } finally { await React.act(() => root.unmount()); document.body.removeChild(c); }
});

test('the App start display has its own role group and one shared model field and the built-in route', async () => {
  const container = document.createElement('div'); document.body.appendChild(container); const root = createRoot(container);
  const snapshot = {...host, threads: [], homeRouting: {activeModeHomeClass: 'account'},
    roleSet: {available: true, defaultRole: 'HELP_HUMAN', roles: [{name: 'HELP_HUMAN', meaning: 'Alignment', default_for_new_chat: true}, {name: 'TASK', meaning: 'Bounded', default_for_new_chat: false}]}};
  const idle = installIdleNativeWaiting(async command => {
    if (command === 'host_status') return snapshot;
    if (command === 'decision_view') return {rows: []};
    if (command === 'native_confirmation_content') return [];
    throw Error(`Unexpected native command: ${command}`);
  });
  try {
    await React.act(async () => {root.render(React.createElement(App));});
    const radios = elements(container, 'input').filter(element => props(element).type === 'radio');
    assert.ok(radios.length >= 2);
    assert.deepEqual([...new Set(radios.map(element => props(element).name))], ['start-thread-role'], 'the Start thread picker keeps its own group');
    const field = label => elements(container, 'input').filter(element => element.parentNode.textContent.startsWith(label));
    assert.equal(field('Model ').length, 1);
    assert.equal(field('Configured Codex provider ').length, 0, 'the provider is never typed');
    assert.equal(elements(container, 'select').filter(element => element.parentNode.textContent.startsWith('Access entry ')).length, 0, 'there is no access-entry select');
    await chooseRoute(container);
    await change(field('Model ')[0], 'chosen-model');
    assert.deepEqual([props(field('Model ')[0]).value, routeChosen(container)], ['chosen-model', true]);
    assert.match(container.querySelectorAll(e => e.getAttribute('aria-label') === 'New conversation choice')[0].textContent, /chosen-model via openai \(chatgpt-account\)/);
  } finally {
    const renderedText = container.textContent;
    await React.act(() => root.unmount());
    document.body.removeChild(container);
    idle.restore(renderedText);
  }
});

// Constructed packets follow the existing redacted HomeSession/account RPC and
// RuntimeSession projections. These mounted checks do not authenticate a real
// account, read auth files, or qualify native sign-in/credential custody.
const {AccountStatus} = loadSrc('AccountStatus');
const accountCanary = 'INVENTED_ACCOUNT_PRIVATE_913@example.invalid';
const accountHost = (extra={}) => ({state:'ready',generationClosed:false,generation:g,
  homeRouting:{activeModeHomeClass:'account',entries:[{modeHomeClass:'account'},{modeHomeClass:'api-key'}]},...extra});
const completionPacket = (extra={}) => ({state:'source-observed',source:{generation:g,requestIdentity:31,
  observationRef:'original-login-31',phase:'CompletedSuccess',mode:'Browser',actualWriteObserved:true,...extra}});
function accountReadPacket(kind='chatgpt', extra={}) {
  const account = kind === null ? null : {type:kind,detailsUnavailable:true};
  return {source:{generation:g,home:g.home,requestIdentity:32,requestRef:'read-32',sourceCurrent:true,
    attemptedFrame:{method:'account/read',params:{}},outcome:'response-observed-result',authResponseShapeValid:true},
    accountObservation:{state:kind === null ? 'native account null observed':'native account type observed',account,identityVerified:false},...extra};
}
function withAccountRead(base, row=accountReadPacket()) {
  return {...base,homeAccess:{modeHomeClass:base.homeRouting.activeModeHomeClass,observations:[row]},
    accountObservation:{generation:base.generation,home:base.generation.home,state:'observed',
      nativeAccount:row.accountObservation?.account,codexAccount:accountCanary,identityVerified:false}};
}
async function mountedAccount(check, {initial=accountHost(),read=async()=>{},strict=false}={}) {
  const container=document.createElement('div');document.body.appendChild(container);const root=createRoot(container);
  let source=initial,navigating=false,busy=false;const reads=[];
  const render=()=>{
    const view=React.createElement(AccountStatus,{host:source,navigating,busy,read:async(...args)=>{reads.push(args);await read(...args);}});
    root.render(strict?React.createElement(React.StrictMode,null,view):view);
  };
  try {
    await React.act(render);
    await check({container,reads,check:()=>React.act(async()=>props(button(container,'Check account status')).onClick()),
      show:async(next,{nav=false,blocked=false}={})=>{source=next;navigating=nav;busy=blocked;await React.act(render);}});
  } finally {await React.act(()=>root.unmount());document.body.removeChild(container);}
}

test('matching sign-in completion checks once, including StrictMode and repeated polls, without reauth',async()=>{
  for(const strict of [false,true]) {
    let complete;
    await mountedAccount(async ui=>{
      assert.equal(ui.reads.length,1);assert.deepEqual(ui.reads[0].slice(0,2),[g,'account']);
      assert.match(ui.container.textContent,/Checking account status/);
      await ui.show(accountHost({homeOAuth:completionPacket()}));assert.equal(ui.reads.length,1);
      complete.resolve();await React.act(async()=>{});
      await ui.show(withAccountRead(accountHost({homeOAuth:completionPacket()})));
      assert.match(ui.container.textContent,/Codex reports a ChatGPT account for this connection/);
      assert.equal(ui.reads.length,1);
      await ui.show(accountHost());await ui.show(accountHost({homeOAuth:completionPacket()}));
      assert.equal(ui.reads.length,1,'a known completion is not retried after an observation gap');
    },{strict,initial:accountHost({homeOAuth:completionPacket()}),read:()=>{complete=deferred();return complete.promise;}});
  }
});

test('no implicit check on restart, pending, failed, foreign, missing or unavailable completion',async()=>{
  const invalid=[accountHost(),accountHost({homeOAuth:completionPacket({phase:'Pending'})}),
    accountHost({homeOAuth:completionPacket({phase:'CompletedFailure'})}),accountHost({homeOAuth:completionPacket({phase:'StartRejected'})}),
    accountHost({homeOAuth:completionPacket({actualWriteObserved:false})}),accountHost({homeOAuth:completionPacket({observationRef:null})}),
    accountHost({homeOAuth:completionPacket({requestIdentity:null})}),accountHost({homeOAuth:completionPacket({generation:{...g,spawnCounter:2}})}),
    accountHost({homeOAuth:{...completionPacket(),state:'unknown/source-unavailable'}}),
    accountHost({homeOAuth:completionPacket(),generationClosed:true}),accountHost({homeOAuth:completionPacket(),state:'stopped'}),
    accountHost({homeOAuth:completionPacket(),homeRouting:{activeModeHomeClass:'api-key'}}),
    accountHost({homeOAuth:completionPacket(),generation:{...g,extra:'invalid'}})];
  for(const initial of invalid)await mountedAccount(async ui=>{assert.equal(ui.reads.length,0);},{initial});
  await mountedAccount(async ui=>{
    await ui.show(accountHost({homeOAuth:completionPacket()}),{nav:true});assert.equal(ui.reads.length,0);
    await ui.show(accountHost({homeOAuth:completionPacket()}),{blocked:true});assert.equal(ui.reads.length,0);
    await ui.show(accountHost({homeOAuth:completionPacket()}));assert.equal(ui.reads.length,1,'one check once the exact source is usable');
  });
});

test('the account view shows the email and plan Codex reports, says when no email is reported, and never an unrecognised plan',()=>{
  const {reportedChatgptAccount}=loadSrc('AccountStatus');
  assert.equal(reportedChatgptAccount({codexAccount:'person@example.invalid',nativeAccount:{type:'chatgpt',planType:'plus'}}),'person@example.invalid · plan plus');
  assert.equal(reportedChatgptAccount({codexAccount:'ChatGPT account (no email reported)',nativeAccount:{type:'chatgpt',planType:'pro'}}),'ChatGPT account (no email reported) · plan pro');
  for(const current of [{},{codexAccount:''},{codexAccount:null},{codexAccount:'two\nlines@example.invalid'},{codexAccount:'x'.repeat(255)}])
    assert.match(reportedChatgptAccount(current),/^ChatGPT account \(no email reported\) · plan not reported$/);
  for(const planType of ['unknown','INVENTED_PLAN',null,3,undefined])
    assert.equal(reportedChatgptAccount({codexAccount:'person@example.invalid',nativeAccount:{planType}}),'person@example.invalid · plan not reported');
});
test('ordinary account summary distinguishes kinds, absence, omission, pending, invalid and failed latest reads',async()=>{
  const cases=[
    [accountReadPacket('chatgpt'),/reports a ChatGPT account/],
    [accountReadPacket('apiKey'),/reports an API key/],
    [accountReadPacket(null),/reports no account/],
    [accountReadPacket('chatgptAuthTokens'),/supported account status.*unknown/],
    [accountReadPacket('private-invented-kind'),/supported account status.*unknown/],
    [accountReadPacket('chatgpt',{accountObservation:{state:'account omitted; unknown/unavailable',account:null}}),/did not report account status.*does not mean you are signed out/],
    [accountReadPacket('chatgpt',{source:{...accountReadPacket().source,outcome:'response-observed-error',response:{error:{message:accountCanary}}}}),/could not read account status/],
    [accountReadPacket('chatgpt',{source:{...accountReadPacket().source,authResponseShapeValid:false}}),/unavailable account response/],
    [accountReadPacket('chatgpt',{source:{...accountReadPacket().source,outcome:'pending'}}),/has not produced a result/],
    [accountReadPacket('chatgpt',{source:{...accountReadPacket().source,sourceCurrent:false}}),/no longer current/],
  ];
  await mountedAccount(async ui=>{
    for(const [row,expected] of cases){
      const source=withAccountRead(accountHost(),row);
      source.homeAccess.observations.unshift(accountReadPacket());
      await ui.show(source);assert.match(ui.container.textContent,expected,'latest read controls; no fallback to old success');
      // DEL-01-05 REQ-001: the email and plan appear only with a current ChatGPT account report, never with any other outcome.
      if(row===cases[0][0]) assert.match(ui.container.textContent,new RegExp(`reports a ChatGPT account for this connection: ${accountCanary.replace('.','\\.')} · plan not reported\\.`));
      else assert.doesNotMatch(ui.container.textContent,new RegExp(accountCanary));
    }
    const invalidated=withAccountRead(accountHost());invalidated.accountObservation.state='unknown';
    await ui.show(invalidated);assert.match(ui.container.textContent,/changed or is no longer confirmed/);
    await ui.show({...withAccountRead(accountHost()),generation:{...g,spawnCounter:2}});
    assert.match(ui.container.textContent,/has not been checked for this connection/);
    await ui.check();assert.deepEqual(ui.reads.at(-1).slice(0,2),[{...g,spawnCounter:2},'account'],'restart offers existing read, without sign-in');
  });
});

test('failed completion read stays private, never auto retries, and allows an explicit account check',async()=>{
  await mountedAccount(async ui=>{
    assert.equal(ui.reads.length,1);assert.match(ui.container.textContent,/could not be confirmed/);
    assert.doesNotMatch(ui.container.textContent,new RegExp(accountCanary));
    await ui.show(accountHost({homeOAuth:completionPacket()}));assert.equal(ui.reads.length,1);
    await ui.check();assert.equal(ui.reads.length,2);
    await ui.show(withAccountRead(accountHost({homeOAuth:completionPacket()})));
    assert.match(ui.container.textContent,/reports a ChatGPT account/,'a later native account result replaces a local read failure');
    await ui.show(accountHost({homeOAuth:completionPacket({cancelStatus:'canceled'})}));
    assert.match(ui.container.textContent,/pending sign-in was canceled/);assert.doesNotMatch(ui.container.textContent,/Signed out:/);
    await ui.show(accountHost({homeOAuth:completionPacket({cancelStatus:'notFound'})}));
    assert.match(ui.container.textContent,/no pending sign-in to cancel/);assert.doesNotMatch(ui.container.textContent,/Signed out:/);
  },{initial:accountHost({homeOAuth:completionPacket()}),read:async()=>{throw Error(accountCanary);}});
});

// The full App dispatcher below exercises the new source guards across native
// read and subsequent host refresh, using only constructed offline IPC replies.
async function mountedAccountApp(check,{readReply,statusReply}={}) {
  const container=document.createElement('div');document.body.appendChild(container);const root=createRoot(container),calls=[];
  let snapshot=accountHost();
  const idle=installIdleNativeWaiting(async(command,args)=>{
    calls.push({command,args});
    if(command==='host_status')return statusReply?statusReply(snapshot,calls):snapshot;
    if(command==='decision_view')return {rows:[]};
    if(command==='native_confirmation_content')return [];
    if(command==='oauth_start'){snapshot={...snapshot,homeOAuth:completionPacket()};return {state:'source-observed'};}
    if(command==='read_home_access'){
      if(readReply)await readReply(args);
      snapshot=withAccountRead(snapshot);return snapshot.homeAccess;
    }
    if(command==='select_home'){snapshot=accountHost({generation:args.modeHomeClass==='account'?g:{...g,home:'key-home'},
      homeRouting:{activeModeHomeClass:args.modeHomeClass,entries:[{modeHomeClass:'account'},{modeHomeClass:'api-key'}]}});return {};}
    throw Error(`Unexpected command ${command}`);
  });
  const summary=()=>container.querySelectorAll(e=>e.getAttribute('aria-label')==='Account status')[0];
  const press=async text=>React.act(async()=>props(button(container,text)).onClick());
  const observe=async next=>{
    snapshot=next;document.visibilityState='visible';
    await React.act(async()=>{for(const {type,listener} of [...document.listeners])if(type==='visibilitychange')listener();});
  };
  try{await React.act(async()=>root.render(React.createElement(App)));await check({container,calls,summary,press,observe});}
  finally{const text=container.textContent;await React.act(()=>root.unmount());document.body.removeChild(container);idle.restore(text);}
}

test('App matching completion dispatches only the existing non-forced read and shows the current account',async()=>{
  await mountedAccountApp(async ui=>{
    assert.match(ui.summary().textContent,/not been checked/);
    await ui.press('Sign in with your ChatGPT account (through Codex)…');
    assert.deepEqual(ui.calls.filter(c=>c.command==='read_home_access'),[{command:'read_home_access',args:{generation:g,modeHomeClass:'account'}}]);
    assert.match(ui.summary().textContent,/reports a ChatGPT account/);
    assert.match(ui.summary().textContent,new RegExp(accountCanary),'the account Codex reports is shown');
    assert.ok(ui.calls.every(c=>['host_status','decision_view','native_confirmation_content','oauth_start','read_home_access'].includes(c.command)),
      'completion never refreshes credentials, signs in again, or calls a model');
    const diagnostics=elements(ui.container,'details').find(d=>d.textContent.startsWith('Source-owned account observations and limits'));
    assert.equal(props(diagnostics).open,undefined,'diagnostics remain available as a disclosure');
  });
});

test('late native account read cannot publish across source replacement or home away and back',async()=>{
  for(const transition of ['generation','home','away-back']) {
    const held=deferred();
    await mountedAccountApp(async ui=>{
      await ui.press('Sign in with your ChatGPT account (through Codex)…');
      assert.equal(ui.calls.filter(c=>c.command==='read_home_access').length,1);
      if(transition==='generation')await ui.observe(accountHost({generation:{...g,spawnCounter:2}}));
      else {await ui.observe(accountHost({generation:{...g,home:'key-home'},homeRouting:{activeModeHomeClass:'api-key',entries:[{modeHomeClass:'account'}]}}));if(transition==='away-back')await ui.press('Use account home');}
      const reads=ui.calls.filter(c=>c.command==='host_status').length;
      held.resolve();await React.act(async()=>{});
      assert.equal(ui.calls.filter(c=>c.command==='host_status').length,reads,'stale read does not request or apply a source refresh');
      assert.doesNotMatch(ui.summary().textContent,/reports a ChatGPT account/);
    },{readReply:()=>held.promise});
  }
});

test('late account host refresh cannot replace a newer App observation',async()=>{
 for(const changedSource of [false,true]) {
  const held=deferred(),reached=deferred();let hold=false;
  await mountedAccountApp(async ui=>{
    hold=true;await ui.press('Sign in with your ChatGPT account (through Codex)…');await reached.promise;
    await ui.observe(accountHost({generation:changedSource?{...g,spawnCounter:2}:g}));
    held.resolve();await React.act(async()=>{});
    assert.match(ui.summary().textContent,/not been checked for this connection/);
    assert.doesNotMatch(ui.summary().textContent,/reports a ChatGPT account/);
  },{statusReply:async snapshot=>{
    if(hold&&snapshot.homeAccess){hold=false;const old=structuredClone(snapshot);reached.resolve();await held.promise;return old;}
    return snapshot;
  }});
 }
});

test('explicit account checks latch queued presses and obsolete handlers cannot read another source',async()=>{
  const held=deferred();
  await mountedAccount(async ui=>{
    const click=props(button(ui.container,'Check account status')).onClick;
    let first,second;
    await React.act(()=>{first=click();second=click();});
    assert.equal(ui.reads.length,1,'one non-forced read even for queued duplicate delivery');
    await ui.show(accountHost({generation:{...g,spawnCounter:2}}));
    assert.match(ui.container.textContent,/not been checked for this connection/,'old pending read is not current-source progress');
    await React.act(async()=>{await click();});assert.equal(ui.reads.length,1,'stale handler cannot dispatch a current-source read');
    held.reject(Error(accountCanary));await React.act(async()=>{await first;await second;});
    assert.doesNotMatch(ui.container.textContent,/could not be confirmed/,'old failure cannot be presented as the new connection');
    assert.doesNotMatch(ui.container.textContent,new RegExp(accountCanary));
  },{read:()=>held.promise});
});

// Offered per-model effort, mounted through the real ordinary composer.
const effortPacket = {state:'observed',conversationModel:'m',generation:g,modeHomeClass:'account',serverProviderState:'named',serverProvider:'openai',complete:true,limits:[],models:[{
  id:'m',model:'m',displayName:'Offered model',description:'',isDefault:true,defaultReasoningEffort:'medium',
  supportedReasoningEfforts:[{reasoningEffort:'medium',description:'Balanced'},{reasoningEffort:'future-offered',description:'Supplier choice'}]
}]};

test('mounted ordinary chooser sends only deliberate offered effort, binds model, rejects old Send and resets on conversation change', async () => {
  const c=document.createElement('div');document.body.appendChild(c);const root=createRoot(c);
  const calls=[];const sends=[];let failSend=false;
  window.__TAURI_INTERNALS__={invoke:async(command,args)=>{calls.push({command,args});assert.equal(command,'read_available_models');return effortPacket;}};
  const host={state:'ready',generation:g,homeRouting:{activeModeHomeClass:'account'},threads:['t','other'].map(threadId=>({generation:g,threadId,model:'obsolete-thread-report',modelProvider:'openai'})),planMode:{state:'offered'}};
  const show = thread => React.act(()=>root.render(React.createElement(ConversationPanel,{host,threadKey:JSON.stringify([g,thread]),setThreadKey:noop,answer:noop,runAct:noop,send:async(...args)=>{sends.push(args);if(failSend)throw Error("unknown send");return {result:{}};},steer:noop,submitAttachments:noop,interrupt:noop,checkPlanMode:noop,codexBusy:false})));
  const change=(element,value)=>React.act(()=>props(element).onChange({target:{value}}));
  const effort=()=>elements(c,'select').find(e=>e.parentNode.textContent.startsWith('Reasoning effort for'));
  try {
    await show('t');assert.equal(calls.length,0,'no implicit read');
    assert.equal(props(effort()).value,'','catalog default not chosen');
    await React.act(()=>props(button(c,'Read effort choices for this model')).onClick());
    assert.equal(calls.length,1);assert.ok(c.textContent.includes('future-offered'));
    const oldChoice=props(effort()).onChange;
    const oldRead=props(button(c,'Read effort choices for this model')).onClick;
    const textarea=()=>elements(c,'textarea').find(e=>props(e).id==='ordinary-composer-text');
    await change(textarea(),'Exact text');
    const oldSend=props(button(c,'Send text')).onClick;
    await change(effort(),'future-offered');
    await React.act(()=>oldSend());assert.equal(sends.length,0,'earlier Send cannot carry a new effort');
    await React.act(()=>props(button(c,'Send in plan mode (experimental)')).onClick());
    assert.deepEqual(sends[0],[g,'t','Exact text','plan','m','future-offered']);
    assert.equal(props(effort()).value,'','successful send leaves native sticky setting in force');
    await change(effort(),'medium');
    await React.act(()=>props(button(c,'Read effort choices for this model')).onClick());
    await React.act(()=>oldChoice({target:{value:'future-offered'}}));
    assert.equal(props(effort()).value,'medium','old observation cannot choose after reread');
    await show('other');assert.equal(props(effort()).value,'','other conversation inherits no local choice');
    assert.equal(props(effort()).disabled,true,'old list not matched to other conversation');
    await show('t');
    const readCount=calls.length;
    await React.act(()=>oldRead());assert.equal(calls.length,readCount,'old read cannot revive after A to B to A');
    await React.act(()=>oldChoice({target:{value:'future-offered'}}));assert.equal(props(effort()).value,'');
    await React.act(()=>props(button(c,'Read effort choices for this model')).onClick());
    await change(effort(),'medium');await change(textarea(),'Uncertain text');failSend=true;
    await React.act(()=>props(button(c,'Send text')).onClick());
    assert.equal(sends.length,2);assert.equal(props(effort()).value,'medium','unknown outcome keeps effort');
    assert.equal(props(textarea()).value,'Uncertain text');
    assert.equal(props(button(c,'Send text')).disabled,true,'no automatic resend after unknown outcome');
  } finally {await React.act(()=>root.unmount());document.body.removeChild(c);delete window.__TAURI_INTERNALS__;}
});


test('delayed effort replies cannot populate another source and readiness disables retained controls', async () => {
  const {OfferedEffortChoice} = loadSrc('ModelChoice');
  const c=document.createElement('div');document.body.appendChild(c);const root=createRoot(c);
  const calls=[], choices=[], replies=[];
  const previous=window.__TAURI_INTERNALS__;
  window.__TAURI_INTERNALS__={invoke:(command,args)=>{
    assert.equal(command,'read_available_models');calls.push(args);
    const held=deferred();replies.push(held);return held.promise;
  }};
  let current={owner:'original',threadId:'t',generation:g,homeClass:'account',modelProvider:'openai',entryId:'chatgpt-account',model:'',effort:'',disabled:false,choose:(...args)=>choices.push(args)};
  const show=async patch=>{current={...current,...patch};await React.act(()=>root.render(React.createElement(OfferedEffortChoice,current)));};
  const effort=()=>elements(c,'select')[0];
  const read=()=>React.act(()=>props(button(c,'Read effort choices for this model')).onClick());
  try {
    await show({});await read();const oldRead=props(button(c,'Read effort choices for this model')).onClick;
    const replacement={...g,spawnCounter:2};
    await show({owner:'replacement',generation:replacement});
    await React.act(async()=>{replies[0].resolve(effortPacket);});
    assert.equal(props(effort()).disabled,true);assert.ok(!c.textContent.includes('future-offered'),'old-source reply is discarded');
    await read();await show({disabled:true});
    await React.act(async()=>{replies[1].resolve({...effortPacket,generation:replacement});});
    assert.equal(props(effort()).disabled,true,'a current reply grants no action while source is unavailable');
    const retainedChoice=props(effort()).onChange;
    await React.act(()=>retainedChoice({target:{value:'medium'}}));assert.equal(choices.length,0);
    await show({disabled:false});
    await React.act(()=>oldRead());assert.equal(calls.length,2,'original read callback stays obsolete');
    await read();
    const next={...g,spawnCounter:3};await show({owner:'next',generation:next});
    await React.act(async()=>{replies[2].reject(Error('obsolete read failed'));});
    assert.ok(!c.textContent.includes('could not be read'),'delayed old error is not attributed to the new source');
    await React.act(()=>retainedChoice({target:{value:'medium'}}));assert.equal(choices.length,0);
  } finally {
    await React.act(()=>root.unmount());document.body.removeChild(c);window.__TAURI_INTERNALS__=previous;
  }
});
