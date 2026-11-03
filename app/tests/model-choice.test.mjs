// New-conversation model discovery in the mounted App with a controlled IPC
// peer (invented snapshot and models). The native read itself is checked by
// the Rust fixture test `model_catalog_lists_the_server_providers_models_at_a_press_and_keeps_no_configuration`.
// No supplier, model, sign-in, network or person act.
import test from 'node:test';
import assert from 'node:assert/strict';
import {loadSrc} from './support/load-src.mjs';
import {installMiniDom} from './support/mini-dom.mjs';
import {installIdleNativeWaiting} from './support/idle-native-waiting.mjs';
const document = installMiniDom();
const React = (await import('react')).default;
const {createRoot} = await import('react-dom/client');
const {App} = loadSrc('App');
const {modelMatch, validModelPacket, NO_PROVIDER_LIMIT} = loadSrc('ModelChoice');

const g = {home:'account', appSession:'s1', spawnCounter:1};
const props = node => node[Object.keys(node).find(k => k.startsWith('__reactProps$'))];
const nodes = (c, tag) => c.querySelectorAll(node => node.localName === tag);
const region = (c, label) => c.querySelectorAll(node => node.getAttribute('aria-label') === label)[0];
const button = (c, label) => nodes(c, 'button').find(node => node.textContent === label);
const buttons = (c, prefix) => nodes(c, 'button').filter(node => node.textContent.startsWith(prefix));
const models = [
  {id:'model-a', model:'model-a', displayName:'Model A', description:'Invented general model', isDefault:true},
  {id:'model-b', model:'model-b', displayName:'Model B', description:'Invented small model', isDefault:false},
];
const packet = (over = {}) => ({state:'observed', generation:g, modeHomeClass:'account', serverProvider:'openai', models, complete:true, limits:[], readAt:'2026-11-03T00:00:00Z',
  standing:'Models Codex reports for the app-server\'s own provider in this Codex generation, read now at your press. A listed model is the supplier\'s reported availability for that provider, not your account\'s entitlement or access; Start still checks the current configuration.', ...over});
const snapshotFor = (mode = 'account', generation = g) => ({state:'ready', generation, homeRouting:{activeModeHomeClass:mode}, threads:[],
  roleLimits:{account:{roles:[]}, 'api-key':{roles:[]}}, roleSet:{available:true, defaultRole:'HELP_HUMAN', roles:[{name:'HELP_HUMAN', meaning:'fixture role', default_for_new_chat:true}]}});

async function mounted(handler, check, initial = snapshotFor()) {
  const c = document.createElement('div'); document.body.appendChild(c); const root = createRoot(c); const calls = [];
  let snapshot = initial;
  const idle = installIdleNativeWaiting(async (command, args) => {
    calls.push({command, args:structuredClone(args)});
    if (command === 'host_status') return structuredClone(snapshot);
    if (command === 'decision_view') return {rows:[]};
    if (command === 'native_confirmation_content') return [];
    return handler(command, args, {get snapshot() { return snapshot; }});
  });
  const intervals = new Map(), previous = {setInterval:globalThis.setInterval, clearInterval:globalThis.clearInterval, getElementById:document.getElementById}; let timer = 0;
  globalThis.setInterval = fn => { intervals.set(++timer, fn); return timer; }; globalThis.clearInterval = id => intervals.delete(id);
  document.getElementById = id => c.querySelectorAll(node => node.getAttribute('id') === id)[0] ?? null;
  const ui = {c, calls, press:async label => React.act(async () => { const node = button(c, label); assert.ok(node, label); assert.equal(!!props(node).disabled, false, label); await props(node).onClick(); }),
    setSnapshot:value => { snapshot = value; }, refresh:async () => React.act(async () => { for (const fn of intervals.values()) await fn(); }),
    summary:() => region(c, 'New conversation choice').textContent, issued:() => calls.filter(call => !['host_status', 'decision_view', 'native_confirmation_content'].includes(call.command))};
  try { await React.act(() => root.render(React.createElement(App))); await check(ui); }
  finally { const text = c.textContent; await React.act(() => root.unmount()); document.body.removeChild(c); idle.restore(text);
    globalThis.setInterval = previous.setInterval; globalThis.clearInterval = previous.clearInterval; document.getElementById = previous.getElementById; }
}

test('a listed model is offered only for a confirmed or explicitly unconfirmed built-in match', () => {
  assert.equal(modelMatch(packet(), 'openai', 'chatgpt-account'), 'confirmed');
  assert.equal(modelMatch(packet(), 'local-lab', 'local-provider'), 'none', 'a list for another provider is not this provider\'s');
  assert.equal(modelMatch(packet(), '', ''), 'none', 'no provider chosen yet');
  const unnamed = packet({serverProvider:null, providerLimit:NO_PROVIDER_LIMIT});
  assert.equal(modelMatch(unnamed, 'openai', 'chatgpt-account'), 'unconfirmed');
  assert.equal(modelMatch(unnamed, 'openai', 'api-key'), 'unconfirmed');
  assert.equal(modelMatch(unnamed, 'local-lab', 'local-provider'), 'none', 'an unnamed provider is never matched to a local one');
  assert.equal(modelMatch(unnamed, 'openai', 'local-provider'), 'none');
  assert.equal(modelMatch(packet({serverProvider:null, providerLimit:'provider not established: disagree'}), 'openai', 'chatgpt-account'), 'none', 'a disagreeing configuration is not established');
  assert.equal(validModelPacket(packet(), g, 'account'), true);
  assert.equal(validModelPacket(packet(), {...g, spawnCounter:2}, 'account'), false);
  assert.equal(validModelPacket(packet(), g, 'api-key'), false);
  assert.equal(validModelPacket(packet({models:[{id:'x', model:'', displayName:'X', description:'', isDefault:false}]}), g, 'account'), false);
  assert.equal(validModelPacket({...packet(), complete:undefined}, g, 'account'), false);
});

test('a first-time account user chooses the built-in route and a reported model, then Start sends exactly that choice', async () => {
  await mounted(async (command, args) => {
    if (command === 'read_available_models') return packet();
    if (command === 'thread_start') return {state:'refused-for-fixture'};
    throw Error(`unexpected ${command}`);
  }, async ui => {
    assert.match(ui.summary(), /no model selected/);
    await ui.press('Use my ChatGPT account (built-in OpenAI)');
    assert.deepEqual(ui.issued(), [], 'choosing the route issues nothing');
    assert.match(region(ui.c, 'How this conversation connects').textContent, /chosen/);
    await ui.press('Read available models');
    assert.deepEqual(ui.issued(), [{command:'read_available_models', args:{generation:g, modeHomeClass:'account'}}]);
    const list = region(ui.c, 'Available models').textContent;
    assert.match(list, /Models Codex reports for provider openai/); assert.match(list, /Model A model-a · Codex's default/); assert.match(list, /not your account's entitlement or access/);
    assert.match(ui.summary(), /no model selected/, 'the reported default is not preselected');
    await ui.press('Use Model B');
    assert.match(ui.summary(), /New conversation choice: model-b via openai \(chatgpt-account\)/);
    assert.match(region(ui.c, 'Available models').textContent, /Model B model-b · chosen/);
    await ui.press('Start thread');
    const start = ui.issued().find(call => call.command === 'thread_start');
    assert.deepEqual({model:start.args.model, modelProvider:start.args.modelProvider, entryId:start.args.entryId, modeHomeClass:start.args.modeHomeClass},
      {model:'model-b', modelProvider:'openai', entryId:'chatgpt-account', modeHomeClass:'account'});
    assert.equal(ui.issued().filter(call => call.command === 'read_available_models').length, 1, 'nothing re-reads or retries on its own');
  });
});

test('a list for another provider, an unnamed provider and a stale or failed read never choose a model', async () => {
  let reply = packet({serverProvider:'local-lab'});
  await mounted(async command => { if (command === 'read_available_models') { if (reply instanceof Error) throw reply; return reply; } throw Error(`unexpected ${command}`); }, async ui => {
    await ui.press('Use my ChatGPT account (built-in OpenAI)');
    await ui.press('Read available models');
    assert.match(region(ui.c, 'Available models').textContent, /This list isn't for this conversation's provider \(openai; the list is for local-lab\)/);
    assert.deepEqual(buttons(ui.c, 'Use Model'), [], 'no choice from another provider\'s list');
    reply = packet({serverProvider:null, providerLimit:NO_PROVIDER_LIMIT});
    await ui.press('Read available models');
    assert.match(region(ui.c, 'Available models').textContent, /can't confirm these models are for the built-in OpenAI route/);
    await ui.press('Use Model A (provider not confirmed)');
    assert.match(ui.summary(), /model-a via openai/);
    ui.setSnapshot(snapshotFor('account', {...g, spawnCounter:2})); await ui.refresh();
    assert.match(region(ui.c, 'Available models').textContent, /This model list is out of date/);
    assert.deepEqual(buttons(ui.c, 'Use Model'), [], 'a stale list offers nothing');
    reply = Error('invented: model/list answered with an error');
    await ui.press('Read available models');
    assert.match(region(ui.c, 'Available models').textContent, /Model list unavailable: .*invented: model\/list answered with an error.*Advanced: enter IDs yourself/);
    reply = packet({generation:g});
    await ui.press('Read available models');
    assert.match(region(ui.c, 'Available models').textContent, /Model list unavailable: the reply was not a model list for this Codex source/, 'a reply for another generation is refused');
    assert.equal(ui.issued().filter(call => call.command === 'thread_start').length, 0);
  });
});

test('an incomplete list says so, and the API-key home offers its own built-in route', async () => {
  await mounted(async command => {
    if (command === 'read_available_models') return packet({modeHomeClass:'api-key', generation:{...g, home:'api-key'}, complete:false, limits:['model list incomplete: Codex repeated a page cursor']});
    throw Error(`unexpected ${command}`);
  }, async ui => {
    assert.equal(button(ui.c, 'Use my ChatGPT account (built-in OpenAI)'), undefined);
    await ui.press('Use this home\'s API key (built-in OpenAI)');
    await ui.press('Read available models');
    assert.deepEqual(ui.issued().at(-1), {command:'read_available_models', args:{generation:{...g, home:'api-key'}, modeHomeClass:'api-key'}});
    const list = region(ui.c, 'Available models').textContent;
    assert.match(list, /The list may be incomplete: model list incomplete: Codex repeated a page cursor/);
    await ui.press('Use Model A');
    assert.match(ui.summary(), /model-a via openai \(api-key\)/);
  }, snapshotFor('api-key', {...g, home:'api-key'}));
});
