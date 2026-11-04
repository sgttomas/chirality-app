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
const entries = [{value:'chatgpt-account', label:'ChatGPT account'}, {value:'local-provider', label:'Local provider'}];
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
    assert.deepEqual(acts, [['workflow_trial_start_clean', {reference:'trial:7', model:'model-b', modelProvider:'openai', entryId:'chatgpt-account', modeHomeClass:'account', role:null, personText:'my edited inputs'}]]);
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
    assert.match(panel.textContent, /Not started: the connection and model were chosen for an earlier Codex source\. Your inputs are kept; choose again/);
    // A reply that arrives after the source changed is ignored.
    let release; reply = new Promise(resolve => { release = resolve; });
    await ui.press('Use my ChatGPT account (built-in OpenAI)');
    await ui.press('Read available models');
    assert.deepEqual(ui.issued().at(-1).args, {generation:g2, modeHomeClass:'account'}, 'the read is for the current generation');
    await ui.render({modeHomeClass:'api-key', generation:{...g2, home:'api-key'}});
    release(packet({generation:g2})); await ui.settle();
    assert.deepEqual(buttons(ui.c, 'Use Model'), [], 'a late reply for the earlier source chooses and offers nothing');
    assert.doesNotMatch(region(ui.c, 'Available models').textContent, /Models Codex reports|out of date/, 'the late reply is not shown at all');
    assert.ok(button(ui.c, 'Use this home\'s API key (built-in OpenAI)'), 'the API-key home offers its own route');
    assert.deepEqual(acts, []);
  });
});

test('a clean trial refuses lists for another provider or generation, marks an unnamed provider and keeps manual IDs under Advanced', async () => {
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
    assert.match(region(ui.c, 'Available models').textContent, /Model list unavailable: .*invented: model\/list answered with an error.*Advanced: enter IDs yourself/);
    reply = packet({serverProvider:null, serverProviderState:'unnamed', providerLimit:'the app-server\'s configuration names no provider'});
    await ui.press('Read available models'); await ui.settle();
    await ui.press('Use Model A (provider not confirmed)');
    assert.equal(!!props(button(ui.c, 'Send')).disabled, false);
    const advanced = nodes(ui.c, 'details').find(node => node.textContent.startsWith('Advanced: enter IDs yourself'));
    assert.ok(advanced, 'manual IDs are under Advanced');
    await ui.change(labelled(advanced, 'input', 'Model '), 'lab-model');
    await ui.change(labelled(advanced, 'input', 'Configured Codex provider '), 'local-lab');
    await ui.change(labelled(advanced, 'select', 'Access entry '), 'local-provider');
    await ui.press('Send'); await ui.settle();
    assert.deepEqual(acts.map(([command, args]) => [command, args.model, args.modelProvider, args.entryId]), [['workflow_trial_start_clean', 'lab-model', 'local-lab', 'local-provider']]);
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
  const base = {handoff:handoff(), entries, homeClass:'account', generation:g, busy:false, ready:true, start:choice => starts.push(choice), send:async text => { sends.push(text); return {state:'sent'}; }, open:() => {}, dismiss:() => {}};
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
    assert.match(region(ui.c, 'Continue as').textContent, /Not started: the connection and model were chosen for an earlier Codex source\. Your handoff message is kept/);
    await ui.press('Use my ChatGPT account (built-in OpenAI)');
    await ui.press('Read available models'); await ui.settle();
    assert.deepEqual(ui.issued().at(-1).args, {generation:g2, modeHomeClass:'account'});
    await ui.press('Use Model A');
    await ui.press(start);
    assert.deepEqual(starts, [{model:'model-a', modelProvider:'openai', entryId:'chatgpt-account'}]);
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
    assert.ok(button(panel(), 'Use this home\'s API key (built-in OpenAI)'), 'the new home offers its own route');
    assert.deepEqual(acts, [], 'nothing was started or sent');
  } finally {
    const text = c.textContent; await React.act(() => root.unmount()); document.body.removeChild(c); idle.restore(text);
    globalThis.setInterval = previous.setInterval; globalThis.clearInterval = previous.clearInterval; document.getElementById = previous.getElementById;
  }
});
