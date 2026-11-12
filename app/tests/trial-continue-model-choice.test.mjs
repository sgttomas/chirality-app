// Clean-trial and Continue-as model choice in the mounted composers with a
// controlled IPC peer (invented generations and models). The native read is
// the same `read_available_models` checked by the Rust fixture test
// `model_catalog_lists_the_server_providers_models_at_a_press_and_keeps_no_configuration`.
// No supplier, model, sign-in, network or person act.
import test from 'node:test';
import assert from 'node:assert/strict';
import {loadSrc} from './support/load-src.mjs';
import {installMiniDom} from './support/mini-dom.mjs';
import {installIdleNativeWaiting} from './support/idle-native-waiting.mjs';
const document = installMiniDom();
const React = (await import('react')).default;
const {createRoot} = await import('react-dom/client');
const {CleanTrialPanel} = loadSrc('TrialComposer');
const {ContinueAsPanel} = loadSrc('ConversationRoles');
const {AvailableModels, modelMatch} = loadSrc('ModelChoice');

const g = {home:'account', appSession:'s1', spawnCounter:1};
const g2 = {...g, spawnCounter:2};
const props = node => node[Object.keys(node).find(k => k.startsWith('__reactProps$'))];
const nodes = (c, tag) => c.querySelectorAll(node => node.localName === tag);
const region = (c, label) => c.querySelectorAll(node => node.getAttribute('aria-label') === label)[0];
const button = (c, label) => nodes(c, 'button').find(node => node.textContent === label);
const buttons = (c, prefix) => nodes(c, 'button').filter(node => node.textContent.startsWith(prefix));
const labelled = (c, tag, label) => nodes(c, tag).find(node => node.parentNode.textContent.startsWith(label));
const models = [
  {id:'model-a', model:'model-a', displayName:'Model A', description:'Invented general model', isDefault:true},
  {id:'model-b', model:'model-b', displayName:'Model B', description:'Invented small model', isDefault:false},
];
const packet = (over = {}) => ({state:'observed', generation:g, modeHomeClass:'account', serverProvider:'openai', serverProviderState:'named', models, complete:true, limits:[], readAt:'2026-11-04T00:00:00Z',
  standing:'Models Codex reports for the app-server\'s own provider; not your account\'s entitlement or access.', ...over});
const roleSet = {available:true, defaultRole:null, roles:[{name:'HELP_HUMAN', meaning:'fixture role'}, {name:'WORKING_ITEMS', meaning:'fixture role'}], conversationRoles:['HELP_HUMAN', 'WORKING_ITEMS']};
const entries = [{value:'chatgpt-account', label:'ChatGPT account'}];
const pending = (over = {}) => ({reference:'trial:7', sequence:4, kind:'clean', draftName:'load-check', location:'project', card:'trial 4 of draft load-check — not registered; not a workflow run',
  text:'[Chirality] Workflow trial 4', textIdentity:{value:'feedface'}, bytes:30, message:'Inputs for this trial: …', authoring:null, cleanConversation:null, delegation:null, runInForce:null, draftChanged:null,
  workFolder:'.chirality/workflow-trials/w1', state:'pre-filled', limit:null, ...over});
const handoff = (over = {}) => ({id:'handoff-1', sourceThread:'thread-1', sourceRoleLabel:'HELP_HUMAN', targetRole:'WORKING_ITEMS', draft:{state:'drafted', reading:'Drafted from the source turn.'},
  draftText:'Summary for WORKING_ITEMS', requestText:'Please summarise', request:{state:'answered'}, started:null, ...over});

async function mounted(component, initial, handler, check) {
  const c = document.createElement('div'); document.body.appendChild(c); const root = createRoot(c); const calls = [];
  const idle = installIdleNativeWaiting(async (command, args) => { calls.push({command, args:structuredClone(args)}); return handler(command, args); });
  let current = initial;
  const render = async next => { current = {...current, ...next}; await React.act(() => root.render(React.createElement(component, current))); };
  const settle = () => React.act(async () => { for (let i = 0; i < 5; i++) await Promise.resolve(); });
  const ui = {c, calls, render, settle,
    press:async (label, scope = c) => React.act(async () => { const node = button(scope, label); assert.ok(node, label); assert.equal(!!props(node).disabled, false, label); await props(node).onClick(); }),
    change:async (node, value) => React.act(async () => { assert.ok(node); props(node).onChange({target:{value}}); }),
    issued:() => calls.filter(call => call.command === 'read_available_models')};
  try { await render({}); await check(ui); }
  finally { const text = c.textContent; await React.act(() => root.unmount()); document.body.removeChild(c); idle.restore(text); }
}
const cleanProps = act => ({pending:pending(), roleSet, limits:{}, entries, modeHomeClass:'account', generation:g, busy:false, ready:true, act});

test('a clean trial chooses the built-in route and a reported model, and Send starts it with exactly that choice', async () => {
  const acts = [];
  await mounted(CleanTrialPanel, cleanProps(async (command, args) => { acts.push([command, args]); return {thread:{threadId:'clean-1'}}; }),
    async command => { if (command === 'read_available_models') return packet(); throw Error(`unexpected ${command}`); }, async ui => {
    const panel = region(ui.c, 'New trial conversation');
    assert.match(panel.textContent, /no model selected; choose how it connects and its model/);
    assert.equal(!!props(button(ui.c, 'Send')).disabled, true, 'nothing preselected, nothing to send');
    await ui.press('Use my ChatGPT account (built-in OpenAI)');
    assert.deepEqual(ui.calls, [], 'choosing the route issues nothing');
    assert.equal(!!props(button(ui.c, 'Send')).disabled, true, 'a route without a model is not enough');
    await ui.press('Read available models'); await ui.settle();
    assert.deepEqual(ui.issued(), [{command:'read_available_models', args:{generation:g, modeHomeClass:'account'}}]);
    assert.match(region(ui.c, 'Available models').textContent, /Model A model-a · Codex's default/);
    assert.equal(!!props(button(ui.c, 'Send')).disabled, true, 'the reported default is not preselected');
    await ui.change(labelled(ui.c, 'textarea', 'Inputs for this trial'), 'my edited inputs');
    await ui.press('Use Model B');
    assert.match(region(ui.c, 'Available models').textContent, /Model B model-b · chosen/);
    assert.deepEqual(acts, [], 'choosing a model sends nothing');
    await ui.press('Send'); await ui.settle();
    assert.deepEqual(acts, [['workflow_trial_start_clean', {reference:'trial:7', model:'model-b', modelProvider:'openai', entryId:'chatgpt-account', modeHomeClass:'account', generation:g, role:null, preselected:false, personText:'my edited inputs'}]]);
    assert.match(panel.textContent, /Sent in the new trial conversation clean-1/);
    assert.equal(ui.issued().length, 1, 'nothing re-reads on its own');
  });
});

test('a home or generation change keeps the clean trial inputs, makes the choice and list stale and refuses an earlier Send press', async () => {
  const acts = []; let reply = packet();
  await mounted(CleanTrialPanel, cleanProps(async (command, args) => { acts.push([command, args]); return {}; }),
    async command => { if (command === 'read_available_models') return reply; throw Error(`unexpected ${command}`); }, async ui => {
    await ui.press('Use my ChatGPT account (built-in OpenAI)');
    await ui.press('Read available models'); await ui.settle();
    await ui.press('Use Model A');
    await ui.change(labelled(ui.c, 'textarea', 'Inputs for this trial'), 'kept inputs');
    const earlierSend = props(button(ui.c, 'Send')).onClick;
    await ui.render({generation:g2});
    const panel = region(ui.c, 'New trial conversation');
    assert.match(panel.textContent, /Codex, the home or its generation changed since you chose\. Your text is kept/);
    assert.match(region(ui.c, 'Available models').textContent, /This model list is out of date/);
    assert.deepEqual(buttons(ui.c, 'Use Model'), [], 'a stale list offers nothing');
    assert.equal(!!props(button(ui.c, 'Send')).disabled, true, 'a stale choice cannot be sent');
    assert.equal(labelled(ui.c, 'textarea', 'Inputs for this trial').value ?? props(labelled(ui.c, 'textarea', 'Inputs for this trial')).value, 'kept inputs');
    await React.act(async () => { earlierSend(); });
    assert.deepEqual(acts, [], 'a press from before the change starts nothing');
    assert.match(panel.textContent, /Not started: the connection and model you pressed for are no longer the current choice \(Codex, the home or the choice changed\)\. Your inputs are kept; choose again/);
    // A reply that arrives after the source changed is ignored.
    let release; reply = new Promise(resolve => { release = resolve; });
    await ui.press('Use my ChatGPT account (built-in OpenAI)');
    await ui.press('Read available models');
    assert.deepEqual(ui.issued().at(-1).args, {generation:g2, modeHomeClass:'account'}, 'the read is for the current generation');
    await ui.render({modeHomeClass:'api-key', generation:{...g2, home:'api-key'}});
    release(packet({generation:g2})); await ui.settle();
    assert.deepEqual(buttons(ui.c, 'Use Model'), [], 'a late reply for the earlier source chooses and offers nothing');
    assert.doesNotMatch(region(ui.c, 'Available models').textContent, /Models Codex reports|out of date/, 'the late reply is not shown at all');
    assert.equal(button(ui.c, 'Use this home\'s API key (built-in OpenAI)'), undefined, 'the omitted OpenAI-key mode offers no route');
    assert.deepEqual(acts, []);
  });
});

test('a clean trial refuses lists for another provider or generation, marks an unnamed provider and keeps a typed model ID under Advanced', async () => {
  const acts = []; let reply = packet({serverProvider:'local-lab'});
  await mounted(CleanTrialPanel, cleanProps(async (command, args) => { acts.push([command, args]); return {}; }),
    async command => { if (command === 'read_available_models') { if (reply instanceof Error) throw reply; return reply; } throw Error(`unexpected ${command}`); }, async ui => {
    await ui.press('Use my ChatGPT account (built-in OpenAI)');
    await ui.press('Read available models'); await ui.settle();
    assert.match(region(ui.c, 'Available models').textContent, /This list isn't for this conversation's provider \(openai; the list is for local-lab\)/);
    assert.deepEqual(buttons(ui.c, 'Use Model'), []);
    reply = packet({generation:g2});
    await ui.press('Read available models'); await ui.settle();
    assert.match(region(ui.c, 'Available models').textContent, /Model list unavailable: the reply was not a model list for this Codex source/);
    reply = Error('invented: model/list answered with an error');
    await ui.press('Read available models'); await ui.settle();
    assert.match(region(ui.c, 'Available models').textContent, /Model list unavailable: .*invented: model\/list answered with an error.*Advanced: enter a model ID yourself/);
    reply = packet({serverProvider:null, serverProviderState:'unnamed', providerLimit:'the app-server\'s configuration names no provider'});
    await ui.press('Read available models'); await ui.settle();
    await ui.press('Use Model A (provider not confirmed)');
    assert.equal(!!props(button(ui.c, 'Send')).disabled, false);
    const advanced = nodes(ui.c, 'details').find(node => node.textContent.startsWith('Advanced: enter a model ID yourself'));
    assert.ok(advanced, 'a typed model ID is under Advanced');
    assert.equal(labelled(advanced, 'input', 'Configured Codex provider '), undefined, 'the provider is never typed');
    assert.equal(labelled(advanced, 'select', 'Access entry '), undefined, 'there is no access-entry select');
    await ui.change(labelled(advanced, 'input', 'Model '), 'Typed/Model-ID:8bit');
    await ui.press('Send'); await ui.settle();
    assert.deepEqual(acts.map(([command, args]) => [command, args.model, args.modelProvider, args.entryId]), [['workflow_trial_start_clean', 'Typed/Model-ID:8bit', 'openai', 'chatgpt-account']], 'the typed ID is sent as typed on the built-in route');
  });
});

test('in the dedicated local home a clean trial offers the prepared oMLX route and Send starts it with that fixed choice', async () => {
  const acts = [], gl = {home:'local', appSession:'s1', spawnCounter:1};
  const local = {entryId:'local-provider-keyed', providerId:'chirality-omlx', endpoint:'http://127.0.0.1:8000/v1', model:'invented-local-model', credentialState:'entry-required'};
  const base = {...cleanProps(async (command, args) => { acts.push([command, args]); return {thread:{threadId:'clean-local'}}; }),
    entries:[{value:'local-provider-keyed', label:'oMLX in the local home'}], modeHomeClass:'local-provider', generation:gl};
  await mounted(CleanTrialPanel, {...base, local}, async command => { throw Error(`unexpected ${command}`); }, async ui => {
    assert.equal(!!props(button(ui.c, 'Send')).disabled, true, 'nothing preselected');
    assert.equal(button(ui.c, 'Read available models'), undefined, 'no Codex list is offered before a route is chosen in the local home');
    assert.match(region(ui.c, 'How this conversation connects').textContent, /No key is saved for this server yet/);
    await ui.press('Use oMLX model invented-local-model');
    assert.match(region(ui.c, 'Available models').textContent, /This connection uses one model: invented-local-model — chosen/);
    assert.equal(nodes(region(ui.c, 'Available models'), 'input').length, 0, 'the fixed route takes no typed model');
    await ui.press('Send');
    assert.deepEqual(acts.map(([command, args]) => [command, args.model, args.modelProvider, args.entryId, args.modeHomeClass, args.generation]),
      [['workflow_trial_start_clean', 'invented-local-model', 'chirality-omlx', 'local-provider-keyed', 'local-provider', gl]]);
    assert.equal(ui.issued().length, 0, 'no model list is read for the local route');
  });
  // Not prepared: nothing to choose and nothing starts.
  await mounted(CleanTrialPanel, {...base, local:null}, async command => { throw Error(`unexpected ${command}`); }, async ui => {
    assert.match(region(ui.c, 'How this conversation connects').textContent, /Prepare the oMLX connection/);
    assert.equal(!!props(button(ui.c, 'Send')).disabled, true);
  });
});

// The account home can no longer choose a local entry; what remains true of the
// model step is that Codex's list is never matched to a local entry, and that a
// local entry with a model setter asks for the server's model name, not a list.
test('Codex\'s list is never offered for a local entry; the model step asks for the server\'s model name', async () => {
  for (const entryId of ['local-provider', 'local-provider-keyed']) {
    assert.equal(modelMatch(packet({serverProvider:'local-lab'}), 'local-lab', entryId), 'none', `${entryId}: a list named for the same provider is not the server's`);
    assert.equal(modelMatch(packet({serverProvider:null, serverProviderState:'unnamed'}), 'openai', entryId), 'none', `${entryId}: an unnamed provider is never matched`);
  }
  let typed = null;
  const shown = {packet:packet({serverProvider:'local-lab'}), current:true, reading:false, message:'', model:'', modelProvider:'local-lab', entryId:'local-provider', disabled:false,
    read:() => assert.fail('no read'), choose:() => assert.fail('no list choice'), setModel:value => { typed = value; }};
  await mounted(AvailableModels, shown, async command => { throw Error(`unexpected ${command}`); }, async ui => {
    const step = region(ui.c, 'Available models');
    assert.match(step.textContent, /The App has no list of this server's models/);
    assert.doesNotMatch(step.textContent, /Model A|Model B|Models Codex reports/);
    assert.equal(buttons(ui.c, 'Use Model').length, 0, 'a provider named like the list\'s provider is still not offered the list');
    assert.equal(button(ui.c, 'Read available models'), undefined);
    await ui.change(labelled(step, 'input', 'Model name on the local server '), 'Exact/Server-Model:8bit');
    assert.equal(typed, 'Exact/Server-Model:8bit', 'the name is passed on as typed');
    await ui.render({model:typed});
    assert.equal(props(labelled(region(ui.c, 'Available models'), 'input', 'Model name on the local server ')).value, 'Exact/Server-Model:8bit');
    assert.deepEqual(ui.calls, [], 'the model step issues nothing');
  });
});

test('a started clean trial still retries in its own conversation without a new model choice', async () => {
  const acts = [];
  await mounted(CleanTrialPanel, {...cleanProps(async (command, args) => { acts.push([command, args]); return {}; }), pending:pending({cleanConversation:{generation:g, threadId:'clean-1'}, state:'started; trial message not sent'})},
    async command => { throw Error(`unexpected ${command}`); }, async ui => {
    assert.equal(region(ui.c, 'Connection and model'), undefined);
    await ui.press('Send'); await ui.settle();
    assert.deepEqual(acts, [['workflow_trial_send', {reference:'trial:7', generation:g, threadId:'clean-1', personText:'Inputs for this trial: …'}]]);
  });
});

test('Continue as chooses a route and reported model, keeps the edited handoff across a source change and starts only the current choice', async () => {
  const starts = [], sends = [];
  const base = {handoff:handoff(), entries, homeClass:'account', generation:g, busy:false, ready:true, start:(choice, source) => starts.push({...choice, ...source}), send:async text => { sends.push(text); return {state:'sent'}; }, open:() => {}, dismiss:() => {}};
  await mounted(ContinueAsPanel, base, async (command, args) => { if (command === 'read_available_models') return packet({generation:args.generation}); throw Error(`unexpected ${command}`); }, async ui => {
    const start = 'Start new conversation as WORKING_ITEMS';
    assert.equal(!!props(button(ui.c, start)).disabled, true, 'no model, no start');
    await ui.change(labelled(ui.c, 'textarea', 'Handoff message'), 'Edited handoff');
    await ui.press('Use my ChatGPT account (built-in OpenAI)');
    await ui.press('Read available models'); await ui.settle();
    assert.deepEqual(ui.issued(), [{command:'read_available_models', args:{generation:g, modeHomeClass:'account'}}]);
    await ui.press('Use Model B');
    const earlierStart = props(button(ui.c, start)).onClick;
    await ui.render({generation:g2});
    assert.equal(!!props(button(ui.c, start)).disabled, true, 'a stale choice cannot start');
    assert.match(region(ui.c, 'Continue as').textContent, /Codex, the home or its generation changed since you chose/);
    assert.equal(props(labelled(ui.c, 'textarea', 'Handoff message')).value, 'Edited handoff', 'the unsent handoff is kept');
    await React.act(async () => { earlierStart(); });
    assert.deepEqual(starts, [], 'a press from before the change starts nothing');
    assert.match(region(ui.c, 'Continue as').textContent, /Not started: the connection and model you pressed for are no longer the current choice \(Codex, the home or the choice changed\)\. Your handoff message is kept/);
    await ui.press('Use my ChatGPT account (built-in OpenAI)');
    await ui.press('Read available models'); await ui.settle();
    assert.deepEqual(ui.issued().at(-1).args, {generation:g2, modeHomeClass:'account'});
    await ui.press('Use Model A');
    await ui.press(start);
    assert.deepEqual(starts, [{model:'model-a', modelProvider:'openai', entryId:'chatgpt-account', generation:g2, modeHomeClass:'account'}], 'the start carries the generation the choice was made for');
    assert.deepEqual(sends, [], 'starting sends no handoff message');
    assert.equal(props(labelled(ui.c, 'textarea', 'Handoff message')).value, 'Edited handoff');
  });
});

// The transition the native rendered after-pass found (PR #117 head c64e81a3):
// in the App, a generation change (and a home change) must not remount the
// clean composer, so its edited inputs stay and the stale choice is named.
test('in the App, a generation or home change keeps the clean trial composer and its edited inputs, and names the stale choice', async () => {
  const {App} = loadSrc('App');
  const {preparedMessages} = loadSrc('preparedMessages');
  const status = (generation, mode = 'account', sourceRef = 'workflow-home:a') => ({state:'ready', generation, homeRouting:{activeModeHomeClass:mode}, threads:[], roleLimits:{account:{roles:[]}, 'api-key':{roles:[]}}, roleSet,
    workflowRoot:{context:{sourceRef, generation}, projectLibraryAvailable:true, activeLibrary:null, libraries:[], selections:[], runs:[], drafts:{drafts:[]}, pendingTrials:[pending()]}});
  assert.equal(preparedMessages(status(g))[0].identity, preparedMessages(status(g2, 'api-key', 'workflow-home:b'))[0].identity, 'the clean composer keeps its identity across home and generation');
  const c = document.createElement('div'); document.body.appendChild(c); const root = createRoot(c); const acts = [];
  let snapshot = status(g);
  const idle = installIdleNativeWaiting(async (command, args) => {
    if (command === 'host_status') return structuredClone(snapshot);
    if (command === 'decision_view') return {rows:[]};
    if (command === 'native_confirmation_content') return [];
    if (command === 'read_available_models') return packet({generation:args.generation, serverProvider:null, serverProviderState:'unnamed', providerLimit:'the app-server\'s configuration names no provider'});
    acts.push(command); throw Error(`unexpected ${command}`);
  });
  const intervals = new Map(), previous = {setInterval:globalThis.setInterval, clearInterval:globalThis.clearInterval, getElementById:document.getElementById}; let timer = 0;
  globalThis.setInterval = fn => { intervals.set(++timer, fn); return timer; }; globalThis.clearInterval = id => intervals.delete(id);
  document.getElementById = id => c.querySelectorAll(node => node.getAttribute('id') === id)[0] ?? null;
  const refresh = () => React.act(async () => { for (const fn of intervals.values()) await fn(); });
  const panel = () => region(c, 'New trial conversation');
  const press = async label => React.act(async () => { const node = button(panel(), label); assert.ok(node, label); assert.equal(!!props(node).disabled, false, label); await props(node).onClick(); });
  const inputs = () => labelled(panel(), 'textarea', 'Inputs for this trial');
  try {
    await React.act(async () => root.render(React.createElement(App)));
    await press('Use my ChatGPT account (built-in OpenAI)');
    await press('Read available models'); await React.act(async () => { for (let i = 0; i < 5; i++) await Promise.resolve(); });
    await press('Use Model A (provider not confirmed)');
    await React.act(async () => { props(inputs()).onChange({target:{value:'EDITED before generation change'}}); });
    const before = panel();
    snapshot = status(g2); await refresh();
    assert.equal(panel(), before, 'the same composer stays mounted');
    assert.equal(props(inputs()).value, 'EDITED before generation change', 'the edited inputs are kept');
    assert.match(panel().textContent, /Codex, the home or its generation changed since you chose\. Your text is kept/);
    assert.match(panel().textContent, /This model list is out of date/);
    assert.equal(!!props(button(panel(), 'Send')).disabled, true);
    snapshot = status({...g2, home:'api-key'}, 'api-key', 'workflow-home:b'); await refresh();
    assert.equal(panel(), before, 'a home change keeps it too');
    assert.equal(props(inputs()).value, 'EDITED before generation change');
    assert.equal(button(panel(), 'Use this home\'s API key (built-in OpenAI)'), undefined, 'the omitted mode does not offer a route; edited inputs remain kept');
    assert.deepEqual(acts, [], 'nothing was started or sent');
  } finally {
    const text = c.textContent; await React.act(() => root.unmount()); document.body.removeChild(c); idle.restore(text);
    globalThis.setInterval = previous.setInterval; globalThis.clearInterval = previous.clearInterval; document.getElementById = previous.getElementById;
  }
});

// Native after-pass finding on head 8a61a49b: a Continue as start that the host
// rejects showed nothing in the panel, and Start was enabled again after an
// unknown outcome. Its outcome now shows in the panel and Start is held until
// the person has checked; the host's message is not read for whether it started.
test('in the App, a rejected Continue as start is reported in its panel and holds Start until the person has checked', async () => {
  const {App} = loadSrc('App');
  const status = {state:'ready', generation:g, homeRouting:{activeModeHomeClass:'account'}, threads:[], roleLimits:{account:{roles:[]}, 'api-key':{roles:[]}}, roleSet, continueAs:[handoff()]};
  const c = document.createElement('div'); document.body.appendChild(c); const root = createRoot(c); const starts = [];
  let reply = Error('invented: outcome unknown; the native receipt was retained');
  const idle = installIdleNativeWaiting(async (command, args) => {
    if (command === 'host_status') return structuredClone(status);
    if (command === 'decision_view') return {rows:[]};
    if (command === 'native_confirmation_content') return [];
    if (command === 'read_available_models') return packet();
    if (command === 'thread_start') { starts.push(structuredClone(args)); if (reply instanceof Error) throw reply.message; return reply; }
    throw Error(`unexpected ${command}`);
  });
  const previous = {setInterval:globalThis.setInterval, clearInterval:globalThis.clearInterval, getElementById:document.getElementById};
  globalThis.setInterval = () => 0; globalThis.clearInterval = () => {};
  document.getElementById = id => c.querySelectorAll(node => node.getAttribute('id') === id)[0] ?? null;
  const panel = () => region(c, 'Continue as');
  const settle = () => React.act(async () => { for (let i = 0; i < 10; i++) await Promise.resolve(); });
  const press = async label => { await React.act(async () => { const node = button(panel(), label); assert.ok(node, label); assert.equal(!!props(node).disabled, false, label); await props(node).onClick(); }); await settle(); };
  const start = 'Start new conversation as WORKING_ITEMS';
  try {
    await React.act(async () => root.render(React.createElement(App)));
    await React.act(async () => { props(labelled(panel(), 'textarea', 'Handoff message')).onChange({target:{value:'Edited handoff'}}); });
    await press('Use my ChatGPT account (built-in OpenAI)');
    await press('Read available models');
    await press('Use Model B');
    const beforeOutcomeStart = props(button(panel(), start)).onClick;
    await press(start);
    assert.equal(starts.length, 1);
    assert.deepEqual({model:starts[0].model, modelProvider:starts[0].modelProvider, entryId:starts[0].entryId, modeHomeClass:starts[0].modeHomeClass, generation:starts[0].generation, continueAs:starts[0].continueAs}, {model:'model-b', modelProvider:'openai', entryId:'chatgpt-account', modeHomeClass:'account', generation:g, continueAs:'handoff-1'});
    const outcome = region(panel(), 'Start outcome');
    assert.ok(outcome, 'the outcome is shown in the Continue as panel');
    assert.equal(outcome.getAttribute('role'), 'alert');
    assert.match(outcome.textContent, /^The new conversation wasn't confirmed as started\. Your handoff message is kept\.It may still have started\. Check the conversation list first/);
    assert.match(outcome.textContent, /What was reported.*invented: outcome unknown; the native receipt was retained.*Command: thread_start for handoff handoff-1/);
    assert.doesNotMatch(c.textContent, /did not complete; see the message below/, 'no App-wide alert points elsewhere');
    assert.equal(!!props(button(panel(), start)).disabled, true, 'Start is held after an unconfirmed start');
    assert.equal(props(labelled(panel(), 'textarea', 'Handoff message')).value, 'Edited handoff');
    await React.act(async () => { beforeOutcomeStart(); }); await settle();
    assert.equal(starts.length, 1, 'a Start control from before the press cannot start again after an unconfirmed outcome');
    const earlierStart = props(button(panel(), start)).onClick;
    await press('Use Model A');
    assert.equal(!!props(button(panel(), start)).disabled, true, 'choosing another model does not lift the hold');
    assert.match(region(panel(), 'Start outcome').textContent, /It may still have started/);
    await React.act(async () => { earlierStart(); }); await settle();
    assert.equal(starts.length, 1, 'a Start control from before the outcome cannot start again');
    await press('I\'ve checked — let me start again');
    assert.equal(starts.length, 1, 'acknowledging starts nothing');
    assert.match(region(panel(), 'Start outcome').textContent, /You can start again/);
    reply = {thread:{generation:g, threadId:'thread-2'}};
    await press(start);
    assert.equal(starts.length, 2, 'only a press after the acknowledgement starts again');
    assert.equal(region(panel(), 'Start outcome'), undefined, 'a confirmed start clears the outcome');
  } finally {
    const text = c.textContent; await React.act(() => root.unmount()); document.body.removeChild(c); idle.restore(text);
    globalThis.setInterval = previous.setInterval; globalThis.clearInterval = previous.clearInterval; document.getElementById = previous.getElementById;
  }
});

test('retained callbacks from an earlier render stay refused after reselecting on a new generation', async () => {
  const acts = [];
  await mounted(CleanTrialPanel, cleanProps(async (command, args) => { acts.push([command, args]); return {thread:{threadId:'clean-2'}}; }),
    async (command, args) => { if (command === 'read_available_models') return packet({generation:args.generation}); throw Error(`unexpected ${command}`); }, async ui => {
    await ui.press('Use my ChatGPT account (built-in OpenAI)');
    await ui.press('Read available models'); await ui.settle();
    const earlierUse = props(button(ui.c, 'Use Model A')).onClick;
    await ui.press('Use Model B');
    const earlierSend = props(button(ui.c, 'Send')).onClick;
    const earlierRead = props(button(ui.c, 'Read available models')).onClick;
    const earlierRoute = props(button(ui.c, 'Use my ChatGPT account (built-in OpenAI)') ?? nodes(ui.c, 'button').find(node => node.textContent.startsWith('Use my ChatGPT'))).onClick;
    await ui.render({modeHomeClass:'api-key', generation:{...g, home:'api-key'}});
    await React.act(async () => { earlierRoute(); });
    assert.equal(button(ui.c, 'Use my ChatGPT account (built-in OpenAI)'), undefined, 'the retained legacy home offers no route');
    assert.equal(!!props(button(ui.c, 'Send')).disabled, true, 'an earlier route control chooses nothing in the new home');
    await ui.render({modeHomeClass:'account', generation:g2});
    assert.equal(props(button(ui.c, 'Use my ChatGPT account (built-in OpenAI)'))['aria-pressed'], false, 'nor in the home after it');
    await ui.press('Use my ChatGPT account (built-in OpenAI)');
    await ui.press('Read available models'); await ui.settle();
    await ui.press('Use Model B');
    const reads = ui.issued().length;
    await React.act(async () => { earlierUse(); earlierRead(); }); await ui.settle();
    assert.equal(ui.issued().length, reads, 'an earlier Read control reads nothing');
    assert.match(region(ui.c, 'Available models').textContent, /Model B model-b · chosen/, 'an earlier Use control changes nothing');
    await React.act(async () => { earlierSend(); }); await ui.settle();
    assert.deepEqual(acts, [], 'an earlier Send is refused even though the same model is chosen again on the new generation');
    await ui.press('Send'); await ui.settle();
    assert.deepEqual(acts.map(([command, args]) => [command, args.model, args.generation]), [['workflow_trial_start_clean', 'model-b', g2]], 'the current Send carries the new generation');
  });
  const starts = [];
  await mounted(ContinueAsPanel, {handoff:handoff(), entries, homeClass:'account', generation:g, busy:false, ready:true, start:(choice, source) => { starts.push({...choice, ...source}); }, send:async () => ({state:'sent'}), open:() => {}, dismiss:() => {}},
    async (command, args) => { if (command === 'read_available_models') return packet({generation:args.generation}); throw Error(`unexpected ${command}`); }, async ui => {
    const start = 'Start new conversation as WORKING_ITEMS';
    await ui.press('Use my ChatGPT account (built-in OpenAI)');
    await ui.press('Read available models'); await ui.settle();
    await ui.press('Use Model A');
    const earlierStart = props(button(ui.c, start)).onClick;
    await ui.render({generation:g2});
    await ui.press('Use my ChatGPT account (built-in OpenAI)');
    await ui.press('Read available models'); await ui.settle();
    await ui.press('Use Model A');
    await React.act(async () => { earlierStart(); });
    assert.deepEqual(starts, [], 'an earlier Start is refused after the same choice is made on the new generation');
    await ui.press(start);
    assert.deepEqual(starts, [{model:'model-a', modelProvider:'openai', entryId:'chatgpt-account', generation:g2, modeHomeClass:'account'}]);
  });
});

test('retained callbacks stay refused after a second model-list read in the same generation', async () => {
  const acts = []; let reply = packet();
  await mounted(CleanTrialPanel, cleanProps(async (command, args) => { acts.push([command, args]); return {thread:{threadId:'clean-3'}}; }),
    async command => { if (command === 'read_available_models') return reply; throw Error(`unexpected ${command}`); }, async ui => {
    await ui.press('Use my ChatGPT account (built-in OpenAI)');
    await ui.press('Read available models'); await ui.settle();
    await ui.press('Use Model A');
    const firstListUseB = props(button(ui.c, 'Use Model B')).onClick;
    const sendForA = props(button(ui.c, 'Send')).onClick;
    reply = packet({models:[models[0]]});
    await ui.press('Read available models'); await ui.settle();
    await React.act(async () => { firstListUseB(); }); await ui.settle();
    assert.match(region(ui.c, 'Available models').textContent, /Model A model-a · Codex's default · chosen/, 'a Use control from the earlier list changes nothing');
    assert.equal(buttons(ui.c, 'Use Model B').length, 0);
    reply = packet();
    await ui.press('Read available models'); await ui.settle();
    await ui.press('Use Model B');
    await React.act(async () => { sendForA(); }); await ui.settle();
    assert.deepEqual(acts, [], 'a Send from before the newer choice is refused');
    await ui.press('Send'); await ui.settle();
    assert.deepEqual(acts.map(([command, args]) => [command, args.model, args.generation]), [['workflow_trial_start_clean', 'model-b', g]]);
  });
});

test('a clean pre-fill with the same reference but changed content does not inherit the edited inputs', async () => {
  const {App} = loadSrc('App');
  const {preparedMessages} = loadSrc('preparedMessages');
  const status = trial => ({state:'ready', generation:g, homeRouting:{activeModeHomeClass:'account'}, threads:[], roleLimits:{account:{roles:[]}, 'api-key':{roles:[]}}, roleSet,
    workflowRoot:{context:{sourceRef:'workflow-home:a', generation:g}, projectLibraryAvailable:true, activeLibrary:null, libraries:[], selections:[], runs:[], drafts:{drafts:[]}, pendingTrials:[trial]}});
  const changed = pending({text:'[Chirality] Workflow trial 4 — changed text', textIdentity:{value:'beadbead'}, message:'Inputs for the changed trial: …'});
  for (const [field, value] of [['text', 'other text'], ['textIdentity', {value:'other'}], ['content', {value:'other-content'}], ['draftName', 'other-draft'], ['location', 'user'], ['workFolder', '.chirality/workflow-trials/w2'], ['message', 'other message']])
    assert.notEqual(preparedMessages(status(pending({[field]:value})))[0].identity, preparedMessages(status(pending()))[0].identity, `${field} stays part of the identity`);
  const c = document.createElement('div'); document.body.appendChild(c); const root = createRoot(c);
  let snapshot = status(pending());
  const idle = installIdleNativeWaiting(async command => {
    if (command === 'host_status') return structuredClone(snapshot);
    if (command === 'decision_view') return {rows:[]};
    if (command === 'native_confirmation_content') return [];
    throw Error(`unexpected ${command}`);
  });
  const intervals = new Map(), previous = {setInterval:globalThis.setInterval, clearInterval:globalThis.clearInterval, getElementById:document.getElementById}; let timer = 0;
  globalThis.setInterval = fn => { intervals.set(++timer, fn); return timer; }; globalThis.clearInterval = id => intervals.delete(id);
  document.getElementById = id => c.querySelectorAll(node => node.getAttribute('id') === id)[0] ?? null;
  const inputs = () => labelled(region(c, 'New trial conversation'), 'textarea', 'Inputs for this trial');
  try {
    await React.act(async () => root.render(React.createElement(App)));
    await React.act(async () => { props(inputs()).onChange({target:{value:'EDITED for the first pre-fill'}}); });
    snapshot = status(changed); await React.act(async () => { for (const fn of intervals.values()) await fn(); });
    assert.equal(props(inputs()).value, 'Inputs for the changed trial: …', 'the changed pre-fill starts from its own message');
    assert.match(region(c, 'New trial conversation').textContent, /changed text/);
  } finally {
    const text = c.textContent; await React.act(() => root.unmount()); document.body.removeChild(c); idle.restore(text);
    globalThis.setInterval = previous.setInterval; globalThis.clearInterval = previous.clearInterval; document.getElementById = previous.getElementById;
  }
});

// Native J2 finding on #119 head dd47ee35: an unconfirmed bring-back send
// withdraws its pre-fill, so its composer and outcome vanished and the Make
// guide offered a blind second bring-back. The App now keeps that fact.
test('in the App, an unconfirmed bring-back send is named in its conversation and holds the guide\'s next bring-back', async () => {
  const {App} = loadSrc('App');
  const thread = id => ({generation:g, threadId:id, model:'invented-model', status:{type:'idle'}, appRole:{standing:'app-observed', role:null}, roleRelation:{kind:'start'}, futureGuidanceNotices:[]});
  const trial = {reference:'trial:lib-a:2', sequence:2, kind:'clean', content:{value:'c'}, version:'current', trialConversation:'thread-clean-2', authoringConversation:'thread-authoring', authoringSourceLimit:'saved', sourceLimit:null, broughtBack:[], time:'t', link:{}, standing:'s', fidelity:{}};
  const bringBack = {id:'bb-1', trial:'trial:lib-a:2', run:null, sequence:2, draftName:'spacing-check', target:{generation:g, threadId:'T1'}, source:{kind:'clean'}, prompt:'Here is how trial 2 went', transcript:'…', card:'transcript of trial 2', textIdentity:{value:'aa'}, bytes:10, includeNative:false, shortenings:[]};
  const root0 = pending => ({context:{sourceRef:'src', generation:g}, projectLibraryAvailable:true, activeLibrary:'lib:project', libraries:[{reference:'lib:project', origin:'project', root:{encoding:'unix_bytes', bytes:[...new TextEncoder().encode('/invented/project')]}, registered:[]}],
    selections:[], runs:[], drafts:{drafts:[{name:'spacing-check', state:'draft', trials:[trial]}]}, pendingTrials:[], pendingBringBacks:pending});
  let snapshot = {state:'ready', generation:g, homeRouting:{activeModeHomeClass:'account'}, threads:[thread('T1')], roleLimits:{account:{roles:[]}, 'api-key':{roles:[]}}, roleSet, workflowRoot:root0([bringBack])};
  const c = document.createElement('div'); document.body.appendChild(c); const root = createRoot(c); const sends = [];
  const idle = installIdleNativeWaiting(async (command, args) => {
    if (command === 'host_status') return structuredClone(snapshot);
    if (command === 'decision_view') return {rows:[]};
    if (command === 'native_confirmation_content') return [];
    if (command === 'workflow_bring_back_send') { sends.push(structuredClone(args)); snapshot = {...snapshot, workflowRoot:root0([])};
      throw {message:'invented: no reply. The send\'s outcome is not established; nothing is recorded or resent', prefillKept:false}; }
    throw Error(`unexpected ${command}`);
  });
  const previous = {setInterval:globalThis.setInterval, clearInterval:globalThis.clearInterval, getElementById:document.getElementById};
  globalThis.setInterval = () => 0; globalThis.clearInterval = () => {};
  document.getElementById = id => c.querySelectorAll(node => node.getAttribute('id') === id)[0] ?? null;
  const settle = () => React.act(async () => { for (let i = 0; i < 10; i++) await Promise.resolve(); });
  const byId = id => c.querySelectorAll(node => node.getAttribute('id') === id)[0];
  try {
    await React.act(async () => root.render(React.createElement(App)));
    await React.act(async () => { props(nodes(byId('conversation'), 'select')[0]).onChange({target:{value:JSON.stringify([g, 'T1'])}}); });
    const composer = region(c, 'Bring back composer');
    assert.ok(composer, 'the prepared results composer is in its conversation');
    await React.act(async () => { props(button(composer, 'Send')).onClick(); }); await settle();
    assert.equal(sends.length, 1);
    assert.equal(region(c, 'Bring back composer'), undefined, 'the host withdrew the pre-fill');
    const notice = region(c, 'Bring-back send not confirmed');
    assert.ok(notice, 'the conversation names the unconfirmed send');
    assert.match(notice.textContent, /Trial 2's results may have been sent to this conversation\..*nothing is resent.*held until you've checked.*Your message: Here is how trial 2 went.*Reported: .*not established/);
    const guide = region(c, 'Make a workflow from your work');
    await React.act(async () => { props(nodes(guide, 'select')[0]).onChange({target:{value:JSON.stringify([g, 'T1'])}}); });
    await React.act(async () => { props(nodes(guide, 'input')[0]).onChange({target:{value:'spacing-check'}}); });
    assert.ok(region(c, 'Trial 2 results may have been sent'), 'the guide names it too');
    const bring = nodes(guide, 'button').find(node => node.textContent.startsWith('Bring trial 2 back'));
    assert.equal(!!props(bring).disabled, true, 'no blind second bring-back');
    assert.equal(sends.length, 1, 'nothing is resent');
  } finally {
    const text = c.textContent; await React.act(() => root.unmount()); document.body.removeChild(c); idle.restore(text);
    globalThis.setInterval = previous.setInterval; globalThis.clearInterval = previous.clearInterval; document.getElementById = previous.getElementById;
  }
});

// Parent source review of #119 f280a050 and the native after-pass: the guard is
// read against the host's current view at dispatch, a missing result is an
// unconfirmed one, and a run's doubt is acknowledged from its own notice.
async function mountBringBacks(initialRoot, handler, check) {
  const {App} = loadSrc('App');
  const thread = id => ({generation:g, threadId:id, model:'invented-model', status:{type:'idle'}, appRole:{standing:'app-observed', role:null}, roleRelation:{kind:'start'}, futureGuidanceNotices:[]});
  const state = {snapshot:{state:'ready', generation:g, homeRouting:{activeModeHomeClass:'account'}, threads:[thread('T1'), thread('T2')], roleLimits:{account:{roles:[]}, 'api-key':{roles:[]}}, roleSet, workflowRoot:initialRoot}};
  const c = document.createElement('div'); document.body.appendChild(c); const root = createRoot(c); const calls = [];
  const idle = installIdleNativeWaiting(async (command, args) => {
    if (command === 'host_status') return structuredClone(state.snapshot);
    if (['decision_view'].includes(command)) return {rows:[]};
    if (command === 'native_confirmation_content') return [];
    calls.push({command, args:structuredClone(args)});
    return handler(command, args, state);
  });
  const previous = {setInterval:globalThis.setInterval, clearInterval:globalThis.clearInterval, getElementById:document.getElementById};
  globalThis.setInterval = () => 0; globalThis.clearInterval = () => {};
  document.getElementById = id => c.querySelectorAll(node => node.getAttribute('id') === id)[0] ?? null;
  const settle = () => React.act(async () => { for (let i = 0; i < 12; i++) await Promise.resolve(); });
  const byId = id => c.querySelectorAll(node => node.getAttribute('id') === id)[0];
  const ui = {c, calls, state, settle, select:async id => React.act(async () => { props(nodes(byId('conversation'), 'select')[0]).onChange({target:{value:JSON.stringify([g, id])}}); })};
  try { await React.act(async () => root.render(React.createElement(App))); await check(ui); }
  finally {
    const text = c.textContent; await React.act(() => root.unmount()); document.body.removeChild(c); idle.restore(text);
    globalThis.setInterval = previous.setInterval; globalThis.clearInterval = previous.clearInterval; document.getElementById = previous.getElementById;
  }
}
const bbTrial = {reference:'trial:lib-a:2', sequence:2, kind:'clean', content:{value:'c'}, version:'current', trialConversation:'thread-clean-2', authoringConversation:'thread-authoring', authoringSourceLimit:'saved', sourceLimit:null, broughtBack:[], time:'t', link:{}, standing:'s', fidelity:{}};
const bbRow = over => ({id:'bb-1', trial:'trial:lib-a:2', run:null, sequence:2, draftName:'spacing-check', target:{generation:g, threadId:'T1'}, source:{kind:'clean'}, prompt:'Here is how trial 2 went', transcript:'…', card:'transcript of trial 2', textIdentity:{value:'aa'}, bytes:10, includeNative:false, shortenings:[], ...over});
const bbRoot = pending => ({context:{sourceRef:'src', generation:g}, projectLibraryAvailable:true, activeLibrary:'lib:project', libraries:[{reference:'lib:project', origin:'project', root:{encoding:'unix_bytes', bytes:[...new TextEncoder().encode('/invented/project')]}, registered:[]}],
  selections:[], runs:[], drafts:{drafts:[{name:'spacing-check', state:'draft', trials:[bbTrial]}]}, pendingTrials:[], pendingBringBacks:pending});

test('in the App, two prepared composers for the same trial and conversation: after the first send is unconfirmed, the second Send and a retained first Send issue nothing', async () => {
  await mountBringBacks(bbRoot([bbRow(), bbRow({id:'bb-2', prompt:'Second composer'})]), async (command, args, state) => {
    if (command === 'workflow_bring_back_send') { state.snapshot = {...state.snapshot, workflowRoot:bbRoot(state.snapshot.workflowRoot.pendingBringBacks.filter(row => row.id !== args.id))};
      throw {message:'invented: no reply. The send\'s outcome is not established; nothing is recorded or resent', prefillKept:false}; }
    throw Error(`unexpected ${command}`);
  }, async ui => {
    await ui.select('T1');
    const composers = () => ui.c.querySelectorAll(node => node.getAttribute('aria-label') === 'Bring back composer');
    assert.equal(composers().length, 2);
    const firstSend = props(button(composers()[0], 'Send')).onClick;
    await React.act(async () => { firstSend(); }); await ui.settle();
    assert.equal(ui.calls.filter(call => call.command === 'workflow_bring_back_send').length, 1);
    assert.equal(composers().length, 1, 'the host withdrew the first pre-fill');
    await React.act(async () => { props(button(composers()[0], 'Send')).onClick(); }); await ui.settle();
    await React.act(async () => { firstSend(); }); await ui.settle();
    assert.equal(ui.calls.filter(call => call.command === 'workflow_bring_back_send').length, 1, 'neither the second composer nor a retained Send issues IPC');
    assert.match(composers()[0].textContent, /Not sent: an earlier send of these results to this conversation wasn't confirmed/);
  });
});

test('in the App, a send that resolves without a reported outcome is held as unconfirmed', async () => {
  await mountBringBacks(bbRoot([bbRow()]), async (command, args, state) => {
    if (command === 'workflow_bring_back_send') { state.snapshot = {...state.snapshot, workflowRoot:bbRoot([])}; return null; }
    throw Error(`unexpected ${command}`);
  }, async ui => {
    await ui.select('T1');
    await React.act(async () => { props(button(region(ui.c, 'Bring back composer'), 'Send')).onClick(); }); await ui.settle();
    assert.match(region(ui.c, 'Bring-back send not confirmed').textContent, /may have been sent to this conversation.*Reported: The host did not report the send's outcome\./);
  });
});

test('in the App, a retained guide Bring after its preparation was published issues nothing more', async () => {
  await mountBringBacks(bbRoot([]), async (command, args, state) => {
    if (command === 'workflow_trial_bring_back') { state.snapshot = {...state.snapshot, workflowRoot:bbRoot([bbRow({id:'bb-new'})])}; return {state:'pre-filled'}; }
    if (command === 'workflow_observe_drafts') return {};
    throw Error(`unexpected ${command}`);
  }, async ui => {
    const guide = region(ui.c, 'Make a workflow from your work');
    await React.act(async () => { props(nodes(guide, 'select')[0]).onChange({target:{value:JSON.stringify([g, 'T1'])}}); });
    await React.act(async () => { props(nodes(guide, 'input')[0]).onChange({target:{value:'spacing-check'}}); });
    const retained = props(nodes(guide, 'button').find(node => node.textContent.startsWith('Bring trial 2 back'))).onClick;
    await React.act(async () => { retained(); }); await ui.settle();
    assert.equal(ui.calls.filter(call => call.command === 'workflow_trial_bring_back').length, 1);
    await React.act(async () => { retained(); }); await ui.settle();
    assert.equal(ui.calls.filter(call => call.command === 'workflow_trial_bring_back').length, 1, 'the published identical preparation refuses the retained control at dispatch');
    assert.ok(nodes(guide, 'button').find(node => node.textContent === 'Read and send trial 2\'s prepared results'));
  });
});

test('in the App, an unconfirmed run bring-back is acknowledged from its own notice, which starts nothing and keeps the record', async () => {
  const {RunBringBackView} = loadSrc('RunPanel');
  const run = {reference:'run-1', run:'run-1'};
  const runRow = bbRow({id:'bb-run', trial:null, run:'run-1', sequence:null, draftName:null});
  await mountBringBacks(bbRoot([runRow]), async (command, args, state) => {
    if (command === 'workflow_bring_back_send') { state.snapshot = {...state.snapshot, workflowRoot:bbRoot([])}; throw {message:'invented run send unknown', prefillKept:false}; }
    throw Error(`unexpected ${command}`);
  }, async ui => {
    await ui.select('T1');
    await React.act(async () => { props(button(region(ui.c, 'Bring back composer'), 'Send')).onClick(); }); await ui.settle();
    const notice = () => region(ui.c, 'Bring-back send not confirmed');
    assert.match(notice().textContent, /The run's results may have been sent to this conversation\..*held until you've checked/);
    const view = () => RunBringBackView({run, conversations:[{threadId:'T1', generation:g, model:'m'}], target:JSON.stringify([g, 'T1']), setTarget:() => {}, includeNative:false, setIncludeNative:() => {}, busy:false, act:() => assert.fail('held')});
    const find = (node, out = []) => { if (Array.isArray(node)) { node.forEach(n => find(n, out)); return out; } if (!node || typeof node !== 'object') return out; if (node.type === 'button') out.push(node); find(node.props?.children, out); return out; };
    assert.equal(find(view())[0].props.disabled, true, 'the run bring-back is held');
    const before = ui.calls.length;
    await React.act(async () => { props(button(notice(), 'I\'ve checked this conversation — allow bringing it back again')).onClick(); });
    assert.equal(ui.calls.length, before, 'acknowledging starts nothing');
    assert.match(notice().textContent, /You've said you checked.*Reported: invented run send unknown/, 'the original outcome stays');
    assert.equal(find(view())[0].props.disabled, false, 'the run bring-back is allowed again');
  });
});

test('in the App, a null send result that leaves the pre-fill visible is not shown as sent, keeps the edited text and holds further sends', async () => {
  await mountBringBacks(bbRoot([bbRow()]), async command => {
    if (command === 'workflow_bring_back_send') return null;
    throw Error(`unexpected ${command}`);
  }, async ui => {
    await ui.select('T1');
    const composer = () => region(ui.c, 'Bring back composer');
    const field = () => nodes(composer(), 'textarea')[0];
    await React.act(async () => { props(field()).onChange({target:{value:'Edited prompt for trial 2'}}); });
    const send = props(button(composer(), 'Send')).onClick;
    await React.act(async () => { send(); }); await ui.settle();
    assert.ok(composer(), 'the pre-fill is still shown');
    assert.doesNotMatch(composer().textContent, /Transcript sent/, 'no success words for a missing result');
    assert.match(composer().textContent, /Not confirmed: the host did not report the send's outcome/);
    assert.equal(props(field()).value, 'Edited prompt for trial 2', 'the edited text is kept');
    const notice = () => region(ui.c, 'Bring-back send not confirmed');
    assert.match(notice().textContent, /Its prepared message is still listed, but that copy is not sent again/, 'no withdrawal claim while the pre-fill is listed');
    assert.doesNotMatch(notice().textContent, /was withdrawn/);
    assert.match(notice().textContent, /Reported: The host did not report the send's outcome\./);
    assert.equal(!!props(button(composer(), 'Send')).disabled, true, 'Send is visibly held');
    assert.match(composer().textContent, /Send is held: this copy's earlier send wasn't confirmed and may have arrived, so it is not sent again/);
    await React.act(async () => { props(button(composer(), 'Send')).onClick(); }); await ui.settle();
    await React.act(async () => { send(); }); await ui.settle();
    assert.equal(ui.calls.filter(call => call.command === 'workflow_bring_back_send').length, 1, 'neither Send nor a retained callback issues another send while held');
    const calls = ui.calls.length;
    await React.act(async () => { props(button(notice(), 'I\'ve checked this conversation — allow bringing it back again')).onClick(); });
    assert.equal(ui.calls.length, calls, 'acknowledging issues nothing');
    assert.ok(composer(), 'the attempted copy is not removed');
    assert.equal(props(field()).value, 'Edited prompt for trial 2');
    assert.equal(!!props(button(composer(), 'Send')).disabled, true, 'the already-attempted copy does not become sendable after the acknowledgement');
    assert.match(composer().textContent, /remove it and bring the results back again if you still need to/);
    await React.act(async () => { send(); }); await ui.settle();
    assert.equal(ui.calls.filter(call => call.command === 'workflow_bring_back_send').length, 1, 'nor through a retained callback');
    assert.match(notice().textContent, /You've said you checked/, 'the original record stays');
  });
});
