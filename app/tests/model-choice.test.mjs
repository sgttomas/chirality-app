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
const {modelMatch, validModelPacket} = loadSrc('ModelChoice');

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
const packet = (over = {}) => ({state:'observed', generation:g, modeHomeClass:'account', serverProvider:'openai', serverProviderState:'named', models, complete:true, limits:[], readAt:'2026-11-03T00:00:00Z',
  standing:'Models Codex reports for the app-server\'s own provider in this Codex generation, read now at your press. A listed model is the supplier\'s reported availability for that provider, not your account\'s entitlement or access; Start still checks the current configuration.', ...over});
const snapshotFor = (mode = 'account', generation = g) => ({state:'ready', generation, homeRouting:{activeModeHomeClass:mode}, threads:[],
  roleLimits:{account:{roles:[]}, 'api-key':{roles:[]}}, roleSet:{available:true, defaultRole:'HELP_HUMAN', roles:[{name:'HELP_HUMAN', meaning:'fixture role', default_for_new_chat:true}]}});

// Optional one-shot hold of the next host_status read (its snapshot is taken first).
let hostGate = null;
// When set, every host_status read rejects with it (a status refresh that fails).
let statusFailure = null;
async function mounted(handler, check, initial = snapshotFor()) {
  const c = document.createElement('div'); document.body.appendChild(c); const root = createRoot(c); const calls = [];
  let snapshot = initial;
  const idle = installIdleNativeWaiting(async (command, args) => {
    calls.push({command, args:structuredClone(args)});
    if (command === 'host_status') { if (statusFailure) throw statusFailure; const value = structuredClone(snapshot), gate = hostGate; hostGate = null; if (gate) await gate; return value; }
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
  const unnamed = packet({serverProvider:null, serverProviderState:'unnamed', providerLimit:'the app-server\'s configuration names no provider; the list is not matched to any conversation provider'});
  assert.equal(modelMatch(unnamed, 'openai', 'chatgpt-account'), 'unconfirmed');
  assert.equal(modelMatch(unnamed, 'openai', 'api-key'), 'none');
  assert.equal(modelMatch(unnamed, 'local-lab', 'local-provider'), 'none', 'an unnamed provider is never matched to a local one');
  assert.equal(modelMatch(unnamed, 'openai', 'local-provider'), 'none');
  assert.equal(modelMatch(packet({serverProvider:null, serverProviderState:'not-established', providerLimit:'provider not established: disagree'}), 'openai', 'chatgpt-account'), 'none', 'a disagreeing configuration is not established');
  assert.equal(validModelPacket(packet(), g, 'account'), true);
  assert.equal(validModelPacket(packet(), {...g, spawnCounter:2}, 'account'), false);
  assert.equal(validModelPacket(packet(), g, 'api-key'), false);
  assert.equal(validModelPacket(packet({models:[{id:'x', model:'', displayName:'X', description:'', isDefault:false}]}), g, 'account'), false);
  assert.equal(validModelPacket({...packet(), complete:undefined}, g, 'account'), false);
  assert.equal(validModelPacket(packet({serverProviderState:'unnamed'}), g, 'account'), false, 'a named provider with an unnamed state is contradictory');
  assert.equal(validModelPacket(packet({serverProviderState:'guessed'}), g, 'account'), false);
  assert.equal(modelMatch(packet({serverProviderState:undefined}), 'openai', 'chatgpt-account'), 'none', 'an untyped reading is never matched');
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

test('a long already-safe App response keeps its distinct tail in optional details; a start error stays direct', async () => {
  const response = {acknowledged:false, error:'Explicit negative acknowledgment.', notice:'Invented safe App response '.repeat(40), tail:'distinct-response-tail-6921'};
  let refuse = false;
  await mounted(async command => {
    if (command === 'read_available_models') return packet();
    if (command === 'thread_start') {
      if (refuse) throw Error('Explicit fixture refusal; nothing admitted.');
      return response;
    }
    throw Error(`unexpected ${command}`);
  }, async ui => {
    await ui.press('Use my ChatGPT account (built-in OpenAI)');
    await ui.press('Read available models'); await ui.press('Use Model B');
    await ui.press('Start thread');
    const feedback = region(ui.c, 'Latest App response');
    const details = nodes(feedback, 'details')[0];
    assert.ok(details); assert.equal(!!props(details).open, false);
    const expected = `thread_start: ${JSON.stringify(response)}`;
    assert.ok(expected.length > 600);
    assert.equal(nodes(details, 'pre')[0].textContent, expected);
    assert.doesNotMatch(nodes(feedback, 'p')[0].textContent, /success|completed|accepted/i);
    assert.ok(nodes(feedback, 'p').some(node => node.textContent === 'acknowledged: false'));
    assert.ok(nodes(feedback, 'p').some(node => node.textContent === 'error: Explicit negative acknowledgment.'));
    refuse = true; await ui.press('Start thread');
    assert.equal(nodes(feedback, 'details').length, 0);
    assert.match(nodes(feedback, 'p')[0].textContent, /Explicit fixture refusal; nothing admitted\./);
    assert.equal(ui.issued().filter(call => call.command === 'thread_start').length, 2, 'one dispatch per press, no retry');
  });
});

test('a list for another provider, an unnamed provider and a stale or failed read never choose a model', async () => {
  let reply = packet({serverProvider:'local-lab'});
  await mounted(async command => { if (command === 'read_available_models') { if (reply instanceof Error) throw reply; return reply; } throw Error(`unexpected ${command}`); }, async ui => {
    await ui.press('Use my ChatGPT account (built-in OpenAI)');
    await ui.press('Read available models');
    assert.match(region(ui.c, 'Available models').textContent, /This list isn't for this conversation's provider \(openai; the list is for local-lab\)/);
    assert.deepEqual(buttons(ui.c, 'Use Model'), [], 'no choice from another provider\'s list');
    reply = packet({serverProvider:null, serverProviderState:'unnamed', providerLimit:'the app-server\'s configuration names no provider; the list is not matched to any conversation provider'});
    await ui.press('Read available models');
    assert.match(region(ui.c, 'Available models').textContent, /can't confirm these models are for the built-in OpenAI route.*it doesn't confirm this model is offered on it/);
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

test('omitted OpenAI-key mode offers no product entry or dispatch; account and local remain independent', async () => {
  await mounted(async command => { throw Error(`unexpected ${command}`); }, async ui => {
    assert.equal(button(ui.c, "Use this home's API key (built-in OpenAI)"), undefined);
    assert.equal(button(ui.c, 'Add or replace key in native secure field…'), undefined);
    assert.equal(button(ui.c, 'Use api-key home'), undefined);
    assert.equal(!!props(button(ui.c, 'Read available models')).disabled, true);
    assert.equal(!!props(button(ui.c, 'Start thread')).disabled, true);
    assert.ok(!nodes(ui.c, 'option').some(n => props(n).value === 'api-key'));
    assert.equal(ui.issued().filter(x => ['add_api_key','read_available_models','thread_start'].includes(x.command)).length, 0);
    ui.setSnapshot(snapshotFor()); await ui.refresh();
    assert.ok(button(ui.c, 'Use my ChatGPT account (built-in OpenAI)'));
    assert.ok(nodes(ui.c, 'option').some(n => props(n).value === 'local-provider'));
    assert.match(region(ui.c, 'Account connection').textContent, /Keyed oMLX runs Codex in a separate local home/);
    assert.ok(button(ui.c, 'Prepare the oMLX connection'), 'keyed local access is offered separately from account sign-in');
    assert.equal(button(ui.c, 'Enter oMLX key in a secure field…'), undefined, 'no key entry before a current local source exists');
    const advanced=nodes(ui.c,'details').find(n=>n.textContent.startsWith('Other sign-in options'));
    assert.ok(advanced);assert.equal(!!props(advanced).open,false);
    assert.equal(props(button(ui.c,'Sign in with your ChatGPT account (through Codex)…')).className,'setup-primary');
  }, snapshotFor('api-key', {...g, home:'api-key'}));
});

test('an incomplete account model list remains explicit', async () => {
  await mounted(async command => {
    if (command === 'read_available_models') return packet({complete:false, limits:['model list incomplete: Codex repeated a page cursor']});
    throw Error(`unexpected ${command}`);
  }, async ui => {
    await ui.press('Use my ChatGPT account (built-in OpenAI)'); await ui.press('Read available models');
    assert.match(region(ui.c, 'Available models').textContent, /The list may be incomplete: model list incomplete: Codex repeated a page cursor/);
    await ui.press('Use Model A'); assert.match(ui.summary(), /model-a via openai \(chatgpt-account\)/);
  });
});

// Keyed oMLX glue. Fixture view shapes follow native_local_provider::view at
// PR198 337c28590c6cc9871e2d671cc47b2b77d772d690 (prepare_local_provider() and
// submit_local_provider_key(generation), both native-window bound). No key,
// server, model or native secure field is used; the IPC peer is invented.
const lg = {home:'local-home', appSession:'s1', spawnCounter:1};
const LOCAL = {providerId:'chirality-omlx', endpoint:'http://127.0.0.1:8000/v1', model:'mlx-community/Qwen3.6-35B-A3B-8bit'};
const localView = (credentialState, generation = lg, over = {}) => ({modeHomeClass:'local-provider', entryId:'local-provider-keyed', ...LOCAL, generation, credentialState,
  credentialCustody:'Codex auth.json in the dedicated local home; App never reads it', validity:'not verified by configuration, login acknowledgment or account type', ...over});
const routed = (active, local = null) => ({...snapshotFor(active, active === 'local-provider' ? local : g),
  homeRouting:{activeModeHomeClass:active, entries:[{modeHomeClass:'account', generation:g, state:'ready'}, ...(local ? [{modeHomeClass:'local-provider', generation:local, state:'ready'}] : [])]}});
let ui;
const localAllowed = ['prepare_local_provider', 'submit_local_provider_key', 'select_home', 'thread_start', 'read_account_status', 'read_home_access'];
const assertNoSecretTraffic = ui => {
  for (const call of ui.issued()) {
    assert.ok(localAllowed.includes(call.command), call.command);
    if (call.command === 'submit_local_provider_key') assert.deepEqual(Object.keys(call.args), ['generation'], 'key entry carries only the generation');
    if (call.command === 'prepare_local_provider') assert.deepEqual(call.args ?? {}, {}, 'preparation takes no argument');
  }
};

test('keyed oMLX: prepare, native key entry, local home Start and return to account without API mode', async () => {
  await mounted(async (command, args, peer) => {
    if (command === 'prepare_local_provider') { ui.setSnapshot(routed('account', lg)); return localView('entry-required'); }
    if (command === 'submit_local_provider_key') { assert.deepEqual(args, {generation:lg}); return localView('configured-not-verified'); }
    if (command === 'select_home') { ui.setSnapshot(routed(args.modeHomeClass, lg)); return {state:'selected'}; }
    if (command === 'thread_start') return {startGeneration:lg, result:{thread:{id:'local-1'}}};
    throw Error(`unexpected ${command}`);
  }, async u => {
    ui = u;
    assert.equal(button(ui.c, 'Enter oMLX key in a secure field…'), undefined);
    assert.equal(button(ui.c, 'Use local oMLX home'), undefined, 'no local home before preparation');
    await ui.press('Prepare the oMLX connection');
    const destination = region(ui.c, 'oMLX destination').textContent;
    for (const value of Object.values(LOCAL)) assert.ok(destination.includes(value), value);
    assert.match(region(ui.c, 'Keyed oMLX connection').textContent, /Key entry required/);
    await ui.press('Enter oMLX key in a secure field…');
    assert.match(region(ui.c, 'Keyed oMLX connection').textContent, /Key saved by Codex — not verified/);
    assert.equal(button(ui.c, 'Enter oMLX key in a secure field…'), undefined);
    assert.doesNotMatch(ui.c.textContent, /auth\.json|credentialCustody/, 'only named nonsecret fields are shown');
    await ui.press('Use local oMLX home');
    assert.equal(!!props(button(ui.c, 'Sign in with your ChatGPT account (through Codex)…')).disabled, true, 'account sign-in belongs to the account home');
    assert.equal(button(ui.c, 'Use my ChatGPT account (built-in OpenAI)'), undefined);
    assert.equal(!!props(button(ui.c, 'Start thread')).disabled, true, 'no route chosen yet');
    await ui.press(`Use oMLX model ${LOCAL.model}`);
    assert.match(ui.summary(), new RegExp(`${LOCAL.model} via chirality-omlx \\(local-provider-keyed\\)`));
    await ui.press('Start thread');
    const start = ui.issued().filter(call => call.command === 'thread_start');
    assert.equal(start.length, 1);
    assert.deepEqual({model:start[0].args.model, modelProvider:start[0].args.modelProvider, entryId:start[0].args.entryId, modeHomeClass:start[0].args.modeHomeClass, generation:start[0].args.generation},
      {model:LOCAL.model, modelProvider:LOCAL.providerId, entryId:'local-provider-keyed', modeHomeClass:'local-provider', generation:lg});
    await ui.press('Use account home');
    assert.ok(button(ui.c, 'Use my ChatGPT account (built-in OpenAI)'), 'account route is available again beside the retained local home');
    assert.ok(button(ui.c, 'Use local oMLX home'));
    assert.equal(button(ui.c, 'Use api-key home'), undefined);
    assert.ok(!nodes(ui.c, 'option').some(n => props(n).value === 'api-key'));
    assertNoSecretTraffic(ui);
  });
});

test('keyed oMLX key entry is offered once per Codex session, including cancel and refusal', async () => {
  let generation = lg, submit = 0;
  await mounted(async (command, args) => {
    if (command === 'prepare_local_provider') { ui.setSnapshot(routed('account', generation)); return localView('entry-required', generation); }
    if (command === 'submit_local_provider_key') {
      submit++; assert.deepEqual(args, {generation});
      if (submit === 1) return localView('entry-required', generation);
      throw Error('Local oMLX source unavailable; no fallback or automatic credential retry');
    }
    throw Error(`unexpected ${command}`);
  }, async u => {
    ui = u;
    await ui.press('Prepare the oMLX connection');
    await ui.press('Enter oMLX key in a secure field…');
    assert.match(ui.c.textContent, /No key was saved: the secure field closed without one/);
    assert.equal(button(ui.c, 'Enter oMLX key in a secure field…'), undefined, 'a cancelled entry still uses this session');
    assert.match(ui.c.textContent, /Key entry for this Codex session has been used/);
    generation = {...lg, spawnCounter:2}; ui.setSnapshot(routed('account', generation)); await ui.refresh();
    assert.match(ui.c.textContent, /from an earlier Codex session or home/);
    assert.equal(region(ui.c, 'oMLX destination'), undefined, 'a superseded view is not shown as current');
    await ui.press('Prepare the oMLX connection');
    await ui.press('Enter oMLX key in a secure field…');
    assert.match(region(ui.c, 'Keyed oMLX connection').textContent, /oMLX key entry did not complete: .*no fallback or automatic credential retry/);
    assert.equal(button(ui.c, 'Enter oMLX key in a secure field…'), undefined, 'an unknown outcome is not retried');
    assert.equal(submit, 2);
    assertNoSecretTraffic(ui);
  });
});

test('keyed oMLX refuses incomplete views, stale routes and duplicate presses', async () => {
  let reply = localView('entry-required', lg, {entryId:'api-key'}), held = null;
  await mounted(async command => {
    if (command === 'prepare_local_provider') { if (held) await held.promise; ui.setSnapshot(routed('account', lg)); return reply; }
    if (command === 'select_home') { ui.setSnapshot(routed('local-provider', {...lg, spawnCounter:2})); return {state:'selected'}; }
    throw Error(`unexpected ${command}`);
  }, async u => {
    ui = u;
    await ui.press('Prepare the oMLX connection');
    assert.match(ui.c.textContent, /oMLX preparation: the reply was not an oMLX status, so nothing from it is shown/);
    assert.equal(region(ui.c, 'oMLX destination'), undefined);
    reply = localView('entry-required');
    let resolve; held = {promise:new Promise(yes => { resolve = yes; })};
    const click = props(button(ui.c, 'Prepare the oMLX connection')).onClick;
    await React.act(async () => { click(); click(); });
    assert.equal(!!props(button(ui.c, 'Prepare the oMLX connection')).disabled, true);
    await React.act(async () => { resolve(); });
    assert.equal(ui.issued().filter(call => call.command === 'prepare_local_provider').length, 2, 'the duplicate press shares the pending latch');
    assert.ok(region(ui.c, 'oMLX destination'));
    await ui.press('Use local oMLX home');
    assert.match(ui.c.textContent, /Prepare the oMLX connection under Connection & access for this Codex session first/, 'a view for another generation offers no route');
    assert.equal(button(ui.c, `Use oMLX model ${LOCAL.model}`), undefined);
    assert.equal(!!props(button(ui.c, 'Start thread')).disabled, true);
    assertNoSecretTraffic(ui);
  });
});

test('review: a retained local Start cannot dispatch against a replacement generation', async () => {
  await mounted(async (command, args) => {
    if (command === 'prepare_local_provider') { ui.setSnapshot(routed('account', lg)); return localView('entry-required'); }
    if (command === 'select_home') { ui.setSnapshot(routed(args.modeHomeClass, lg)); return {state:'selected'}; }
    throw Error(`unexpected ${command}`);
  }, async u => {
    ui = u;
    await ui.press('Prepare the oMLX connection'); await ui.press('Use local oMLX home'); await ui.press(`Use oMLX model ${LOCAL.model}`);
    const retained = props(button(ui.c, 'Start thread')).onClick;
    assert.equal(!!props(button(ui.c, 'Start thread')).disabled, false);
    ui.setSnapshot(routed('local-provider', {...lg, spawnCounter:2})); await ui.refresh();
    assert.equal(!!props(button(ui.c, 'Start thread')).disabled, true);
    await React.act(async () => { await retained(); });
    assert.equal(ui.issued().filter(call => call.command === 'thread_start').length, 0, 'the earlier generation route is not sent to its successor');
    assertNoSecretTraffic(ui);
  });
});

test('review: a consumed key entry is not offered again after a renderer reload of the same generation', async () => {
  const store = new Map(), previous = Object.getOwnPropertyDescriptor(globalThis, 'sessionStorage');
  Object.defineProperty(globalThis, 'sessionStorage', {configurable:true, value:{getItem:k => store.has(k) ? store.get(k) : null, setItem:(k, v) => store.set(k, String(v))}});
  try {
    const handler = async (command, args) => {
      if (command === 'prepare_local_provider') { ui.setSnapshot(routed('account', lg)); return localView('entry-required'); }
      if (command === 'submit_local_provider_key') return localView('entry-required');
      throw Error(`unexpected ${command}`);
    };
    await mounted(handler, async u => { ui = u; await ui.press('Prepare the oMLX connection'); await ui.press('Enter oMLX key in a secure field…'); });
    await mounted(handler, async u => {
      ui = u; await ui.press('Prepare the oMLX connection');
      assert.equal(button(ui.c, 'Enter oMLX key in a secure field…'), undefined, 'the reloaded window keeps the consumed generation');
      assert.match(ui.c.textContent, /Key entry for this Codex session has been used/);
      assert.equal(ui.issued().filter(call => call.command === 'submit_local_provider_key').length, 0);
    });
  } finally { if (previous) Object.defineProperty(globalThis, 'sessionStorage', previous); else delete globalThis.sessionStorage; }
});

test('review: an older preparation refresh cannot replace a newer host observation', async () => {
  let release;
  await mounted(async command => {
    if (command === 'prepare_local_provider') { ui.setSnapshot(routed('account', lg)); hostGate = new Promise(yes => { release = yes; }); return localView('entry-required'); }
    throw Error(`unexpected ${command}`);
  }, async u => {
    ui = u;
    await ui.press('Prepare the oMLX connection');
    assert.equal(!!props(button(ui.c, 'Prepare the oMLX connection')).disabled, true, 'the latch is held through the refresh');
    ui.setSnapshot(routed('account', {...lg, spawnCounter:2})); await ui.refresh();
    assert.match(ui.c.textContent, /from an earlier Codex session or home/);
    await React.act(async () => { release(); });
    assert.match(ui.c.textContent, /from an earlier Codex session or home/, 'the held older snapshot is not published over the newer one');
    assert.equal(region(ui.c, 'oMLX destination'), undefined);
    assert.equal(!!props(button(ui.c, 'Prepare the oMLX connection')).disabled, false);
  });
});

// Native d448c92a8a81e46fd62f3c97b24fe8d26c9f2426: preparation reports the
// original generation's no-refresh account observation; administrator Codex
// configuration presence refuses with the same fixed limit.
const LIMIT = 'Local oMLX source unavailable; no fallback or automatic credential retry';
test('keyed oMLX: a saved key after restart is shown as saved and not verified, with no key entry offered', async () => {
  await mounted(async command => {
    if (command === 'prepare_local_provider') { ui.setSnapshot(routed('account', lg)); return localView('configured-not-verified'); }
    throw Error(`unexpected ${command}`);
  }, async u => {
    ui = u;
    await ui.press('Prepare the oMLX connection');
    assert.match(region(ui.c, 'Keyed oMLX connection').textContent, /Key saved by Codex — not verified/);
    assert.equal(button(ui.c, 'Enter oMLX key in a secure field…'), undefined);
    assert.doesNotMatch(ui.c.textContent, /Key entry required/);
    assertNoSecretTraffic(ui);
  });
});

test('keyed oMLX: a refused preparation or Start shows the fixed limit and withdraws any earlier key state', async () => {
  let refuse = false;
  await mounted(async (command, args) => {
    if (command === 'prepare_local_provider') { ui.setSnapshot(routed('account', lg)); if (refuse) throw Error(LIMIT); return localView('configured-not-verified'); }
    if (command === 'select_home') { ui.setSnapshot(routed(args.modeHomeClass, lg)); return {state:'selected'}; }
    if (command === 'thread_start') throw Error(LIMIT);
    throw Error(`unexpected ${command}`);
  }, async u => {
    ui = u;
    await ui.press('Prepare the oMLX connection'); await ui.press('Use local oMLX home'); await ui.press(`Use oMLX model ${LOCAL.model}`);
    await ui.press('Start thread');
    assert.ok(ui.c.textContent.includes(`thread_start: Error: ${LIMIT}`), 'the fixed refusal is shown as given');
    assert.match(region(ui.c, 'Keyed oMLX connection').textContent, /Key saved by Codex — not verified/, 'a Start refusal is not a key observation');
    refuse = true; await ui.press('Prepare the oMLX connection');
    const local = region(ui.c, 'Keyed oMLX connection').textContent;
    assert.ok(local.includes(`oMLX preparation did not complete: Error: ${LIMIT}`));
    assert.doesNotMatch(local, /Key saved by Codex|Key entry required|earlier Codex session/, 'a refusal supplies no key state');
    assert.equal(region(ui.c, 'oMLX destination'), undefined);
    assert.equal(button(ui.c, 'Enter oMLX key in a secure field…'), undefined);
    assert.equal(button(ui.c, `Use oMLX model ${LOCAL.model}`), undefined, 'no local route without a current observation');
    assertNoSecretTraffic(ui);
  });
});

// oMLX key entry refused (a reading sentence, or an ordinary refusal), then a failed status refresh:
// the entry's own message stands, then the fixed refresh line once; nothing raw from the refresh.
for (const [label, refusal] of [['the gate sentence', loadSrc('readingSentences').READING_GATE], ['an ordinary refusal', 'Keyed oMLX unavailable: invented refusal']]) test(`keyed oMLX: key entry refused (${label}) then a failed refresh shows its message, then the fixed line`, async () => {
  const {REFRESH_FAILED} = loadSrc('statusRefresh');
  try {
    await mounted(async command => {
      if (command === 'prepare_local_provider') { ui.setSnapshot(routed('account', lg)); return localView('entry-required'); }
      if (command === 'submit_local_provider_key') { statusFailure = 'INVENTED_PRIVATE_REFRESH_DIAGNOSTIC_58'; throw refusal; }
      throw Error(`unexpected ${command}`);
    }, async u => {
      ui = u;
      await ui.press('Prepare the oMLX connection');
      await ui.press('Enter oMLX key in a secure field…');
      const shown = region(ui.c, 'Keyed oMLX connection').textContent;
      assert.ok(shown.includes(`oMLX key entry did not complete: ${refusal} ${REFRESH_FAILED}`), shown);
      assert.doesNotMatch(ui.c.textContent, /INVENTED_PRIVATE_REFRESH_DIAGNOSTIC_58/);
      statusFailure = null;
    });
  } finally { statusFailure = null; }
});

// The model list's provider note ending with a reading sentence (model_catalog.rs `providerLimit`):
// the sentence is shown as it is, with no second full stop after it.
test('a provider note ending with a reading sentence is shown once, without a doubled full stop', async () => {
  const {READING_GATE} = loadSrc('readingSentences');
  const note = `provider not established: ${READING_GATE}`;
  await mounted(async command => { if (command === 'read_available_models') return packet({serverProvider:null, serverProviderState:'not-established', providerLimit:note}); throw Error(`unexpected ${command}`); }, async ui => {
    await ui.press('Use my ChatGPT account (built-in OpenAI)');
    await ui.press('Read available models');
    const shown = region(ui.c, 'Available models').textContent;
    assert.ok(shown.includes(note), shown);
    assert.ok(!shown.includes(`${READING_GATE}.`), 'no second full stop after the sentence');
  });
});
