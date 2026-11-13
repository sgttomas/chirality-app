// The two sentences a configuration reading ends with when it was not sent reach the person
// unchanged at every web catch that receives them, and nothing else does. The mounted App runs
// against a controlled IPC peer (invented snapshot and replies); the Rust side, where the
// sentences are made and passed through, is checked by hosting::reading_gate_tests and
// desktop_startup::access_provider_saves_state_the_write_first_when_reading_again_is_not_sent.
// No supplier, model, sign-in, network or person act.
import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {loadSrc} from './support/load-src.mjs';
import {installMiniDom} from './support/mini-dom.mjs';
import {installIdleNativeWaiting} from './support/idle-native-waiting.mjs';
const document = installMiniDom();
const React = (await import('react')).default;
const {createRoot} = await import('react-dom/client');
const {App, EffectiveAccessSettingsPanel} = loadSrc('App');
const {AccountStatus} = loadSrc('AccountStatus');
const {READING_GATE, READING_WITHDRAWN, WRITE_THEN_READING, CHILD_ROLES_IN_PLACE} = loadSrc('readingSentences');

const canary = 'INVENTED_PRIVATE_READING_DIAGNOSTIC_602';
const statusCanary = 'INVENTED_PRIVATE_REFRESH_DIAGNOSTIC_77';
const sentences = [READING_GATE, READING_WITHDRAWN];
const g = {home:'account', appSession:'s1', spawnCounter:1};
const project = {reference:'/invented/work'};
const props = node => node[Object.keys(node).find(k => k.startsWith('__reactProps$'))];
const nodes = (c, tag) => c.querySelectorAll(node => node.localName === tag);
const region = (c, label) => c.querySelectorAll(node => node.getAttribute('aria-label') === label)[0];
const button = (c, label) => nodes(c, 'button').find(node => node.textContent === label);
const labelled = (c, tag, label) => nodes(c, tag).find(node => node.parentNode.textContent.startsWith(label));
const change = (node, value) => React.act(() => props(node).onChange({target:{value}}));
const press = (c, label) => React.act(async () => { const node = button(c, label); assert.ok(node, label); assert.equal(!!props(node).disabled, false, label); await props(node).onClick(); });

test('the web strings equal the Rust constants they stand for', () => {
  const rust = readFileSync(new URL('../src-tauri/src/hosting_reading_gate.rs', import.meta.url), 'utf8');
  const constant = name => { const m = rust.match(new RegExp(`const ${name}: &str =\\s*"((?:[^"\\\\]|\\\\.)*)";`)); assert.ok(m, name); return JSON.parse(`"${m[1]}"`); };
  assert.equal(READING_GATE, constant('READING_GATE'));
  assert.equal(READING_WITHDRAWN, constant('READING_WITHDRAWN'));
  assert.equal(WRITE_THEN_READING, constant('WRITE_THEN_READING'));
  const provider = readFileSync(new URL('../src-tauri/src/access_provider.rs', import.meta.url), 'utf8');
  const prefix = provider.match(/const CHILD_ROLES_IN_PLACE: &str =\s*"((?:[^"\\]|\\.)*)";/);
  assert.ok(prefix, 'CHILD_ROLES_IN_PLACE'); assert.equal(CHILD_ROLES_IN_PLACE, JSON.parse(`"${prefix[1]}"`));
});

// Effective access settings: the panel alone, its native read refused.
test('the settings reading shows either sentence and withholds any other error text', async () => {
  for (const error of [...sentences, canary]) {
    const c = document.createElement('div'); document.body.appendChild(c); const root = createRoot(c);
    const host = {state:'ready', generationClosed:false, generation:g, homeRouting:{activeModeHomeClass:'account'}, accessSettingsReadRevision:null, currentAppProjectContext:project};
    const idle = installIdleNativeWaiting(async command => { assert.equal(command, 'read_effective_access_settings'); throw error; });
    try {
      await React.act(() => root.render(React.createElement(EffectiveAccessSettingsPanel, {host, navigating:false, refresh:async () => host})));
      await press(c, 'Read effective storage and plugin settings');
      const text = region(c, 'Effective access settings').textContent;
      if (error === canary) { assert.match(text, /private diagnostic withheld/); assert.doesNotMatch(text, new RegExp(canary)); }
      else assert.ok(text.includes(error), `the sentence is shown unchanged: ${text}`);
    } finally { const text = c.textContent; await React.act(() => root.unmount()); document.body.removeChild(c); idle.restore(text); }
  }
});

// Account status: the component alone, its read refused.
test('the account status check shows either sentence and withholds any other error text', async () => {
  for (const error of [...sentences, canary]) {
    const c = document.createElement('div'); document.body.appendChild(c); const root = createRoot(c);
    const host = {state:'ready', generationClosed:false, generation:g, homeRouting:{activeModeHomeClass:'account', entries:[{modeHomeClass:'account'}]}};
    try {
      await React.act(() => root.render(React.createElement(AccountStatus, {host, navigating:false, busy:false, read:async () => { throw error; }})));
      await press(c, 'Check account status');
      const text = region(c, 'Account status').textContent;
      if (error === canary) { assert.match(text, /Account status could not be confirmed/); assert.doesNotMatch(text, new RegExp(canary)); }
      else assert.ok(text.includes(error), `the sentence is shown unchanged: ${text}`);
    } finally { await React.act(() => root.unmount()); document.body.removeChild(c); }
  }
});

// The mounted App against a controlled IPC peer.
const snapshotFor = () => ({state:'ready', generationClosed:false, generation:g, homeRouting:{activeModeHomeClass:'account'}, threads:[], currentAppProjectContext:project,
  roleLimits:{account:{roles:[]}, 'api-key':{roles:[]}}, roleSet:{available:true, defaultRole:'HELP_HUMAN', roles:[{name:'HELP_HUMAN', meaning:'fixture role', default_for_new_chat:true}]}});
async function mounted(answers, check) {
  const c = document.createElement('div'); document.body.appendChild(c); const root = createRoot(c); const calls = [];
  let snapshot = snapshotFor(), failStatus = false;
  const idle = installIdleNativeWaiting(async (command, args) => {
    calls.push(command);
    if (command === 'host_status') { if (failStatus) throw statusCanary; return structuredClone(snapshot); }
    if (command === 'decision_view') return {rows:[]};
    if (command === 'native_confirmation_content') return [];
    if (command === 'provider_endpoint_discard' || command === 'provider_create_discard') return 'invented-epoch';
    const answer = answers[command]; assert.ok(answer, command);
    const {error, value, host, refreshFails} = answer();
    if (host) snapshot = {...snapshot, ...host};
    if (refreshFails) failStatus = true;
    if (error !== undefined) throw error;
    return structuredClone(value);
  });
  const intervals = new Map(), previous = {setInterval:globalThis.setInterval, clearInterval:globalThis.clearInterval, getElementById:document.getElementById}; let timer = 0;
  globalThis.setInterval = fn => { intervals.set(++timer, fn); return timer; }; globalThis.clearInterval = id => intervals.delete(id);
  document.getElementById = id => c.querySelectorAll(node => node.getAttribute('id') === id)[0] ?? null;
  const poll = () => React.act(async () => { for (const fn of intervals.values()) await fn(); });
  try { await React.act(() => root.render(React.createElement(App))); await check(c, calls, {poll, failStatus:() => { failStatus = true; }}); }
  finally { const text = c.textContent; await React.act(() => root.unmount()); document.body.removeChild(c); idle.restore(text);
    globalThis.setInterval = previous.setInterval; globalThis.clearInterval = previous.clearInterval; document.getElementById = previous.getElementById; }
}
// The clean trial's start refused at its reading: the host's refusal
// (runtime_session::…a_clean_start_that_fails…) is shown as the composer's failure, as given.
const {pressSend, hostMessage} = loadSrc('TrialComposer');
test('a clean trial start refused at its reading shows the host refusal as given', async () => {
  for (const sentence of sentences) {
    const message = `The trial conversation was not started; the pre-filled trial was withdrawn. ${sentence}`;
    const outcomes = [];
    pressSend(async () => { throw {message, prefillKept:false}; }, 'workflow_trial_start_clean', {}, outcome => outcomes.push(outcome), () => 'sent');
    await new Promise(resolve => setTimeout(resolve, 0));
    assert.deepEqual(outcomes.at(-1), {state:'failed', failure:message, prefillKept:false});
  }
  // Continue as shows the start's rejection as given: the host returns the bare sentence.
  for (const sentence of sentences) assert.equal(hostMessage(sentence), sentence);
});

// The status poll that fails shows the fixed refresh line alone and nothing raw; an action that
// succeeds with a successful refresh shows what it showed before (no refresh line).
const {REFRESH_FAILED} = loadSrc('statusRefresh');
test('a failed status poll shows the fixed line alone and withholds the raw diagnostic', async () => {
  await mounted({}, async (c, calls, ui) => {
    ui.failStatus(); await ui.poll();
    const once = c.textContent.split(REFRESH_FAILED).length - 1;
    assert.ok(once >= 1, 'the fixed line is shown');
    await ui.poll(); await ui.poll();
    assert.equal(c.textContent.split(REFRESH_FAILED).length - 1, once, 'added once, however often the poll fails');
    assert.doesNotMatch(c.textContent, new RegExp(statusCanary));
  });
});
// The configured-provider read this test pressed is gone from option A's UI (98558c40). The same
// protection is held on a writer of option A's account view: the account status check, whose
// status read follows it.
const statusLine = (c, label) => nodes(region(c, label), 'p').find(node => node.getAttribute('role') === 'status').textContent;
const accountRead = {homeAccess:{modeHomeClass:'account', observations:[{source:{attemptedFrame:{method:'account/read'}, generation:g, home:'account', sourceCurrent:true, outcome:'response-observed-result', authResponseShapeValid:true},
  accountObservation:{state:'native account type observed', account:{type:'chatgpt'}}}]},
  accountObservation:{generation:g, home:'account', state:'observed', nativeAccount:{type:'chatgpt', planType:'plus'}, codexAccount:'invented@example.invalid'}};
test('an action that succeeds with a successful refresh shows no refresh line', async () => {
  await mounted({read_home_access:() => ({value:{state:'read'}, host:accountRead})}, async (c, calls) => {
    await press(c, 'Check account status');
    assert.equal(statusLine(c, 'Account status'), 'Codex reports a ChatGPT account for this connection: invented@example.invalid · plan plus.', 'the status is shown as read');
    assert.ok(calls.lastIndexOf('host_status') > calls.indexOf('read_home_access'), 'the status was read after the command');
    assert.doesNotMatch(c.textContent, new RegExp(REFRESH_FAILED.replace(/[.?]/g, '\\$&')));
  });
});

// Option A's account view, mounted: the status check refused at a reading shows the sentence alone.
test('the account view: a status check refused at its reading shows the sentence alone and withholds any other error text', async () => {
  for (const error of [...sentences, canary]) await mounted({read_home_access:() => ({error})}, async c => {
    await press(c, 'Check account status');
    const status = statusLine(c, 'Account status');
    if (error === canary) { assert.equal(status, 'Account status could not be confirmed. Try checking again; this does not mean you are signed out.'); assert.doesNotMatch(c.textContent, new RegExp(canary)); }
    else assert.equal(status, error, 'the sentence alone');
  });
});

// Option A's oMLX connection view: a preparation or key entry refused at a reading shows its own
// attribution and then the sentence as it is, and nothing after it (the key entry's form is the one
// model-choice.test.mjs pins with a failed refresh). No key is entered or seen.
const lg = {home:'local-home', appSession:'s1', spawnCounter:1};
const withLocal = {homeRouting:{activeModeHomeClass:'account', entries:[{modeHomeClass:'account', generation:g, state:'ready'}, {modeHomeClass:'local-provider', generation:lg, state:'ready'}]}};
const localView = credentialState => ({modeHomeClass:'local-provider', entryId:'local-provider-keyed', providerId:'chirality-omlx', endpoint:'http://127.0.0.1:8000/v1', model:'invented-local-model', generation:lg, credentialState});
const localAlerts = c => nodes(region(c, 'Keyed oMLX connection'), 'p').filter(node => node.getAttribute('role') === 'alert').map(node => node.textContent);
test('the oMLX connection: a preparation or key entry refused at its reading shows its attribution, then the sentence as it is', async () => {
  for (const sentence of sentences) {
    await mounted({prepare_local_provider:() => ({error:sentence, host:withLocal})}, async c => {
      await press(c, 'Prepare the oMLX connection');
      assert.deepEqual(localAlerts(c), [`oMLX preparation did not complete: ${sentence}`]);
    });
    await mounted({prepare_local_provider:() => ({value:localView('entry-required'), host:withLocal}), submit_local_provider_key:() => ({error:sentence})}, async (c, calls) => {
      await press(c, 'Prepare the oMLX connection'); await press(c, 'Enter oMLX key in a secure field…');
      assert.deepEqual(localAlerts(c), [`oMLX key entry did not complete: ${sentence}`]);
      assert.equal(calls.filter(command => command === 'submit_local_provider_key').length, 1, 'sent once');
    });
  }
});

// Option A's model step: the model list's provider note ending with either sentence
// (model_catalog.rs `providerLimit`) shows the sentence as it is, with no second full stop.
test('the model step: a provider note ending with either sentence shows it as it is', async () => {
  for (const sentence of sentences) {
    const note = `provider not established: ${sentence}`;
    const list = {state:'observed', generation:g, modeHomeClass:'account', serverProvider:null, serverProviderState:'not-established', providerLimit:note, models:[], complete:true, limits:[]};
    await mounted({read_available_models:() => ({value:list})}, async c => {
      await press(c, 'Use my ChatGPT account (built-in OpenAI)'); await press(c, 'Read available models');
      const shown = region(c, 'Available models').textContent;
      assert.ok(shown.includes(note), shown);
      assert.ok(!shown.includes(`${sentence}.`), 'no second full stop after the sentence');
    });
  }
});

// Round 4: the four Conversation-view refresh writers. A Start refused at its reading puts the
// sentence on this view; then each operation runs and its status read fails with a private canary.
// The sentence stays; the operation's own outcome (acknowledged, or its own failure) stays with its
// attribution; the fixed line appears once; the canary appears nowhere; the command is sent once
// (a failed read supplies no snapshot and triggers no retry).
const conversationCanary = 'INVENTED_PRIVATE_STATUS_READ_DIAGNOSTIC_R4';
async function conversationWriter(operation, commandFails, check) {
  const g = {appSession:'r4-session', home:'r4-home', spawnCounter:1};
  const live = {generation:g, threadId:'thread-a', turnId:'live-a'};
  const snapshot = {state:'ready', generation:g, homeRouting:{activeModeHomeClass:'account', entries:[{modeHomeClass:'account'}]},
    roleLimits:{account:{roles:[]}}, roleSet:{available:true, defaultRole:null, roles:[{name:'HELP_HUMAN', meaning:'fixture role'}]},
    threads:[{generation:g, threadId:'thread-a', model:'reported-original', modelProvider:'openai', appRole:{standing:'app-observed', role:null, supply_ref:'sup:r4'}}],
    ...(['steer', 'interrupt'].includes(operation) ? {conversationTurns:[{...live, nativeTurn:{id:'live-a', status:'inProgress', items:[]}}], steeringTargets:[{generation:g, threadId:'thread-a', target:live}]} : {}),
    attachmentCustody:{state:'opened'}, ...(operation === 'attach' ? {attachmentSelections:{ownerRef:'owner-r4', listRevision:1, selections:[{selection:{selectionRef:'sel-r4', displayName:'invented.txt'}}], submissions:[]}} : {})};
  const commands = {send:'conversation_send_text', plan:'collaboration_modes_read', attach:'submit_attachments', steer:'conversation_steer_text', interrupt:'conversation_interrupt'};
  let failStatus = false; const calls = [];
  const idle = installIdleNativeWaiting(async command => {
    calls.push(command);
    if (command === 'host_status') { if (failStatus) throw Error(conversationCanary); return structuredClone(snapshot); }
    if (command === 'decision_view') return {rows:[]};
    if (command === 'native_confirmation_content') return [];
    if (command === 'thread_start') throw READING_GATE;
    if (command === commands[operation]) { failStatus = true; if (commandFails) throw `invented ${operation} refusal`; return operation === 'send' ? {result:{turn:{id:'r4-turn'}}} : {}; }
    throw Error(`unexpected ${command}`);
  });
  const previous = {setInterval:globalThis.setInterval, clearInterval:globalThis.clearInterval, getElementById:document.getElementById};
  globalThis.setInterval = () => 0; globalThis.clearInterval = () => {};
  const c = document.createElement('div'); document.body.appendChild(c); const root = createRoot(c);
  document.getElementById = id => c.querySelectorAll(node => node.getAttribute('id') === id)[0] ?? null;
  const settle = () => React.act(async () => { for (let i = 0; i < 12; i++) await Promise.resolve(); });
  const tap = async label => { await React.act(async () => { const node = button(c, label); assert.ok(node, label); assert.equal(!!props(node).disabled, false, label); await props(node).onClick(); }); await settle(); };
  try {
    await React.act(async () => root.render(React.createElement(App)));
    const panel = () => c.querySelectorAll(node => node.getAttribute('id') === 'conversation')[0];
    await change(nodes(panel(), 'select')[0], JSON.stringify([g, 'thread-a']));
    // The account start's one route (the built-in provider with the ChatGPT account entry), then its model.
    await tap('Use my ChatGPT account (built-in OpenAI)'); await change(labelled(c, 'input', 'Model '), 'r4-model');
    await tap('Start thread');
    assert.ok(c.textContent.includes(`thread_start: ${READING_GATE}`), 'the reading sentence is on this view');
    if (operation !== 'plan' && operation !== 'interrupt') await change(nodes(panel(), 'textarea')[0], 'invented r4 text');
    if (operation === 'interrupt') await change(labelled(panel(), 'select', 'Observed live turn '), 'live-a');
    await tap({send:'Send text', plan:'Check plan mode availability', attach:'Send text and ordered attachments', steer:'Steer current live turn', interrupt:'Interrupt selected live turn'}[operation]);
    assert.ok(c.textContent.includes(READING_GATE), 'the reading sentence stays');
    assert.doesNotMatch(c.textContent, new RegExp(conversationCanary), 'the raw status-read diagnostic appears nowhere');
    assert.equal(calls.filter(command => command === commands[operation]).length, 1, 'sent once: no automatic retry');
    await check(c);
  } finally {
    const text = c.textContent; await React.act(() => root.unmount()); document.body.removeChild(c); idle.restore(text);
    Object.assign(globalThis, {setInterval:previous.setInterval, clearInterval:previous.clearInterval}); document.getElementById = previous.getElementById;
  }
}
const once = (text, part) => text.split(part).length - 1;
for (const commandFails of [false, true]) {
  test(`ordinary send ${commandFails ? 'refused' : 'acknowledged'}, then a failed status read: its outcome stays, the fixed line once, nothing raw`, async () => {
    await conversationWriter('send', commandFails, c => {
      const shown = region(c, 'Ordinary text submission outcome').textContent;
      assert.match(shown, /Original ordinary text turn · conversation thread-a · Home r4-home/, 'attributed to its own request');
      if (commandFails) assert.ok(shown.includes('invented send refusal'), 'its own failure stays'); else assert.match(shown, /Native turn\/start response received/);
      assert.equal(once(shown, REFRESH_FAILED), 1);
    });
  });
  test(`plan-mode check ${commandFails ? 'refused' : 'completed'}, then a failed status read: ${commandFails ? 'its failure, then' : 'only'} the fixed line`, async () => {
    await conversationWriter('plan', commandFails, c => {
      assert.ok(c.textContent.includes(commandFails ? `invented plan refusal ${REFRESH_FAILED}` : REFRESH_FAILED), c.textContent.slice(-400));
      if (!commandFails) assert.doesNotMatch(c.textContent, /invented plan refusal/);
    });
  });
  test(`attachment send ${commandFails ? 'refused' : 'acknowledged'}, then a failed status read: its outcome stays, the fixed line once, nothing raw`, async () => {
    await conversationWriter('attach', commandFails, c => {
      const shown = region(c, 'Attachment submission outcome').textContent;
      assert.match(shown, /Original Send with ordered attachments · conversation thread-a · Home r4-home/, 'attributed to its own request');
      if (commandFails) assert.ok(shown.includes('invented attach refusal'), 'its own failure stays'); else assert.match(shown, /Matching attachment native acknowledgment observed/);
      assert.equal(once(shown, REFRESH_FAILED), 1);
    });
  });
  for (const operation of ['steer', 'interrupt']) test(`${operation} ${commandFails ? 'refused' : 'acknowledged'}, then a failed status read: its outcome stays, the fixed line once, nothing raw`, async () => {
    await conversationWriter(operation, commandFails, c => {
      const shown = region(c, 'Original conversation action outcome').textContent;
      assert.match(shown, new RegExp(`Original ${operation === 'steer' ? 'steering' : 'interrupt'} request · conversation thread-a · Home r4-home`), 'attributed to its own request');
      if (commandFails) assert.ok(shown.includes(`Original native request failed: invented ${operation} refusal`), 'its own failure stays');
      else assert.match(shown, operation === 'steer' ? /Native steering acknowledgment received/ : /Native interrupt acknowledgment received/);
      assert.equal(once(shown, REFRESH_FAILED), 1);
    });
  });
}

// Status reads after a command whose failure used to change what the command's caller sees, or went
// unhandled: the workflow assurance setting, the attachment selection panel, the external observation
// selection, the trace selection, the generic act (decide) and the Codex process controls. The
// command's own outcome stands (a completed command does not reject; its own failure is shown as
// before), the fixed line is added once to the App line, the raw diagnostic appears nowhere, and the
// command is sent once.
const afterCanary = 'INVENTED_PRIVATE_STATUS_READ_DIAGNOSTIC_AFTER';
async function afterCommand(kind, commandFails, check) {
  const g = {appSession:'after-session', home:'after-home', spawnCounter:1};
  const snapshot = {state:'ready', generation:g, homeRouting:{activeModeHomeClass:'account', entries:[{modeHomeClass:'account'}]}, threads:[],
    roleLimits:{account:{roles:[]}}, roleSet:{available:true, defaultRole:null, roles:[{name:'HELP_HUMAN', meaning:'fixture role'}]},
    ...(kind === 'assurance' ? {workflowRoot:{assuranceSetting:{level:'robust', policy:'Require verified approval', source:'Stored in this App\'s settings', verification:{state:'available', available:true, detail:'invented'}, robustWithoutVerification:'invented'}}} : {}),
    ...(kind === 'attachment' ? {attachmentCustody:{state:'opened'}, attachmentSelections:{ownerRef:'owner-after', listRevision:1, selections:[{selection:{selectionRef:'sel-after', displayName:'invented.txt'}}], submissions:[]}} : {}),
    ...(kind === 'external' ? {externalObservation:{selection:{state:'not-selected'}}} : {}),
    ...(kind === 'trace' ? {traceReceiving:{selection:{state:'not-selected'}}} : {})};
  const commands = {assurance:'workflow_assurance_relaxed', attachment:'remove_attachment', external:'select_external_observation', trace:'select_trace_record', decide:'decide', process:'host_start'};
  const offer = {offerId:'offer-after', wording:'Invented decision', actKind:'decide', subject:{ref:'subject-after', contentIdentity:{value:'identity-after'}}, purpose:'invented', scope:'invented', answers:{standing:'invented'}, alternatives:[{id:'alt-a', statement:'invented', consequences:['none']}]};
  let failStatus = false; const calls = [];
  const idle = installIdleNativeWaiting(async command => {
    calls.push(command);
    if (command === 'host_status') { if (failStatus) throw Error(afterCanary); return structuredClone(snapshot); }
    if (command === 'decision_view') return kind === 'decide' ? {rows:[{package:'pkg-after', actRequested:'decide', state:'pending', alternatives:[], subject:[], purpose:'invented'}]} : {rows:[]};
    if (command === 'native_confirmation_content') return [];
    if (command === 'compose_offer') return structuredClone(offer);
    if (command === commands[kind]) { failStatus = true; if (commandFails) throw `invented ${kind} refusal`; return {selection:{state:'invented-selected', stage:'invented-stage'}}; }
    throw Error(`unexpected ${command}`);
  });
  const previous = {setInterval:globalThis.setInterval, clearInterval:globalThis.clearInterval, getElementById:document.getElementById};
  globalThis.setInterval = () => 0; globalThis.clearInterval = () => {};
  const c = document.createElement('div'); document.body.appendChild(c); const root = createRoot(c);
  document.getElementById = id => c.querySelectorAll(node => node.getAttribute('id') === id)[0] ?? null;
  const settle = () => React.act(async () => { for (let i = 0; i < 12; i++) await Promise.resolve(); });
  const tap = async label => { await React.act(async () => { const node = button(c, label); assert.ok(node, label); assert.equal(!!props(node).disabled, false, label); await props(node).onClick(); }); await settle(); };
  try {
    await React.act(async () => root.render(React.createElement(App)));
    if (kind === 'trace') { const selects = nodes(region(c, 'Supplied trace record') ?? c, 'select').filter(node => [...nodes(node, 'option')].some(o => props(o).value === 'exam_result') || [...nodes(node, 'option')].some(o => props(o).value === 'own_code'));
      await change(selects[0], 'exam_result'); await change(selects[1], 'own_code'); }
    if (kind === 'decide') { await tap('Open act control (decide)'); const radio = nodes(c, 'input').find(node => props(node).value === 'alt-a'); await React.act(async () => { props(radio).onChange({target:{value:'alt-a'}}); }); }
    await tap({assurance:'Allow disk records (native confirmation)…', attachment:'Remove', external:'Select observation documents…', trace:'Select supplied record…', decide:'Decide…', process:'Start Codex'}[kind]);
    assert.doesNotMatch(c.textContent, new RegExp(afterCanary), 'the raw status-read diagnostic appears nowhere');
    assert.equal(calls.filter(command => command === commands[kind]).length, 1, 'sent once: no automatic retry');
    assert.ok(c.textContent.includes(REFRESH_FAILED), 'the fixed line is shown');
    await check(c);
  } finally {
    const text = c.textContent; await React.act(() => root.unmount()); document.body.removeChild(c); idle.restore(text);
    Object.assign(globalThis, {setInterval:previous.setInterval, clearInterval:previous.clearInterval}); document.getElementById = previous.getElementById;
  }
}
const alerts = c => nodes(c, 'p').filter(node => node.getAttribute('role') === 'alert').map(node => node.textContent);
for (const kind of ['assurance', 'attachment', 'external', 'trace', 'decide', 'process']) for (const commandFails of [false, true]) test(`${kind}: a ${commandFails ? 'refused' : 'completed'} command whose status refresh fails keeps its own outcome; the fixed line once, nothing raw`, async () => {
  await afterCommand(kind, commandFails, c => {
    const own = `invented ${kind} refusal`;
    if (kind === 'decide') {
      assert.ok(c.textContent.includes(commandFails ? `decide: ${own} ${REFRESH_FAILED}` : `decide: {"selection"`), 'the decision outcome stands');
      assert.ok(!c.textContent.includes('Act control: Invented decision'), 'decide closes its offer after the command, as before');
    } else if (kind === 'external') {
      assert.ok(c.textContent.includes(`${commandFails ? own : 'External selection: invented-selected invented-stage'} ${REFRESH_FAILED}`), 'the selection outcome stands, then the fixed line');
    } else if (kind === 'process') {
      assert.ok(c.textContent.includes(commandFails ? `host_start: ${own} ${REFRESH_FAILED}` : `host_start: {"selection"`), 'the process outcome stands');
      assert.equal(once(region(c, 'Latest App response').textContent, REFRESH_FAILED), 1, 'the fixed line once on the App line');
      assert.equal(!!props(button(c, 'Start Codex')).disabled, false, 'the busy state is cleared as before');
    } else if (kind === 'trace' && !commandFails) {
      assert.ok(c.textContent.includes(`Supplied trace selection: invented-selected ${REFRESH_FAILED}`), 'the selection outcome stands, then the fixed line');
    }
    // The command's caller: its own panel shows its own failure, and no failure at all when it completed.
    if (commandFails && !['external', 'decide', 'process'].includes(kind)) assert.ok(alerts(c).some(text => text === own), `${kind}: its own failure is shown as before`);
    if (!commandFails) assert.ok(!alerts(c).some(text => text === REFRESH_FAILED), `${kind}: a completed command is not shown as failed`);
  });
});
