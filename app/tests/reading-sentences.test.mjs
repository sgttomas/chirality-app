// The two sentences a configuration reading ends with when it was not sent reach the person
// unchanged at every web catch that receives them, and nothing else does. The mounted App runs
// against a controlled IPC peer (invented snapshot, rows and offers); the Rust side, where the
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
const {READING_GATE, READING_WITHDRAWN, WRITE_THEN_READING} = loadSrc('readingSentences');

const canary = 'INVENTED_PRIVATE_READING_DIAGNOSTIC_602';
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

// The mounted App: configured providers, the endpoint and Add offers, and both saves.
const snapshotFor = () => ({state:'ready', generationClosed:false, generation:g, homeRouting:{activeModeHomeClass:'account'}, threads:[], currentAppProjectContext:project,
  providerEndpointEdit:{available:true}, providerCreate:{available:true}, configuredProviderReadRevision:null, providerOfferReadRevision:null,
  roleLimits:{account:{roles:[]}, 'api-key':{roles:[]}}, roleSet:{available:true, defaultRole:'HELP_HUMAN', roles:[{name:'HELP_HUMAN', meaning:'fixture role', default_for_new_chat:true}]}});
const scope = readRevision => ({generation:g, projectContext:project, modeHomeClass:'account', cwd:'/invented/work', readRevision});
const rows = {state:'observed', schema:'ConfigReadResponse', scope:scope('provider-read-1'), limit:'Configured metadata only; not authentication, reachability, model/capability availability or Start authority',
  rows:[{id:'fixture.dot', label:'Configured local provider', endpoint:'https://example.invalid/old', wireApi:'responses'}]};
const endpointOffer = {token:'endpoint-token', providerId:'fixture.dot', label:'Configured local provider', proposedEndpoint:'https://example.invalid/new', currentEndpoint:'https://example.invalid/old', wireApi:'responses', scope:scope('offer-1')};
const addOffer = {kind:'add-provider', token:'add-token', providerId:'fixture.new', submittedName:'Invented name', endpoint:'https://example.invalid/new', wireApi:'responses', requiresOpenaiAuth:false, scope:scope('offer-2')};

async function mounted(answers, check) {
  const c = document.createElement('div'); document.body.appendChild(c); const root = createRoot(c); const calls = [];
  let snapshot = snapshotFor();
  const idle = installIdleNativeWaiting(async (command, args) => {
    calls.push(command);
    if (command === 'host_status') return structuredClone(snapshot);
    if (command === 'decision_view') return {rows:[]};
    if (command === 'native_confirmation_content') return [];
    if (command === 'provider_endpoint_discard' || command === 'provider_create_discard') return 'invented-epoch';
    const answer = answers[command]; assert.ok(answer, command);
    const {error, value, host} = answer();
    if (host) snapshot = {...snapshot, ...host};
    if (error !== undefined) throw error;
    return structuredClone(value);
  });
  const intervals = new Map(), previous = {setInterval:globalThis.setInterval, clearInterval:globalThis.clearInterval, getElementById:document.getElementById}; let timer = 0;
  globalThis.setInterval = fn => { intervals.set(++timer, fn); return timer; }; globalThis.clearInterval = id => intervals.delete(id);
  document.getElementById = id => c.querySelectorAll(node => node.getAttribute('id') === id)[0] ?? null;
  try { await React.act(() => root.render(React.createElement(App))); await check(c, calls); }
  finally { const text = c.textContent; await React.act(() => root.unmount()); document.body.removeChild(c); idle.restore(text);
    globalThis.setInterval = previous.setInterval; globalThis.clearInterval = previous.clearInterval; document.getElementById = previous.getElementById; }
}
const listed = () => ({value:rows, host:{configuredProviderReadRevision:'provider-read-1'}});

test('reading configured providers shows either sentence and withholds any other error text', async () => {
  for (const error of [...sentences, canary]) await mounted({read_configured_providers:() => ({error})}, async c => {
    await press(c, 'Read configured local providers');
    const text = region(c, 'Configured local providers').textContent;
    if (error === canary) { assert.match(text, /Configured provider observation unavailable; private diagnostic withheld/); assert.doesNotMatch(text, new RegExp(canary)); }
    else assert.ok(text.includes(error), `the sentence is shown unchanged: ${text}`);
  });
});

test('the endpoint offer shows either sentence and withholds any other error text', async () => {
  for (const error of [...sentences, canary]) await mounted({read_configured_providers:listed, provider_endpoint_offer:() => ({error})}, async c => {
    await press(c, 'Read configured local providers'); await press(c, 'Edit endpoint fixture.dot');
    await change(labelled(c, 'input', 'Endpoint URL '), 'https://example.invalid/new'); await press(c, 'Review endpoint change');
    const text = region(c, 'Provider endpoint editor').textContent;
    if (error === canary) { assert.match(text, /Endpoint edit unavailable; private values and diagnostics withheld/); assert.doesNotMatch(text, new RegExp(canary)); }
    else assert.ok(text.includes(error), `the sentence is shown unchanged: ${text}`);
  });
});

test('the Add offer shows either sentence and withholds any other error text', async () => {
  for (const error of [...sentences, canary]) await mounted({provider_create_offer:() => ({error})}, async c => {
    await press(c, 'Add local provider…');
    await change(labelled(c, 'input', 'Provider ID '), 'fixture.new'); await change(labelled(c, 'input', 'Submitted name '), 'Invented name');
    await change(labelled(c, 'input', 'Endpoint URL '), 'https://example.invalid/new'); await press(c, 'Review provider Add');
    const text = region(c, 'Provider Add editor').textContent;
    if (error === canary) { assert.match(text, /Provider Add unavailable; absence or safe review could not be established/); assert.doesNotMatch(text, new RegExp(canary)); }
    else assert.ok(text.includes(error), `the sentence is shown unchanged: ${text}`);
  });
});

// After a save, the view offers no save retry (the offer is spent and its Save control gone)
// and keeps the explicit read-again control, "Read configured local providers".
const saveCases = [
  {kind:'endpoint', editor:'Provider endpoint editor', save:'Save endpoint…', command:'provider_endpoint_save', fixed:/Write observed; the current source has not been continued/,
    open:async c => { await press(c, 'Read configured local providers'); await press(c, 'Edit endpoint fixture.dot'); await change(labelled(c, 'input', 'Endpoint URL '), 'https://example.invalid/new'); await press(c, 'Review endpoint change'); },
    answers:{read_configured_providers:listed, provider_endpoint_offer:() => ({value:endpointOffer, host:{providerOfferReadRevision:'offer-1'}})}},
  {kind:'Add', editor:'Provider Add editor', save:'Add provider…', command:'provider_create_save', fixed:/Provider addition write observed; the current source has not been continued/,
    open:async c => { await press(c, 'Add local provider…'); await change(labelled(c, 'input', 'Provider ID '), 'fixture.new'); await change(labelled(c, 'input', 'Submitted name '), 'Invented name'); await change(labelled(c, 'input', 'Endpoint URL '), 'https://example.invalid/new'); await press(c, 'Review provider Add'); },
    answers:{provider_create_offer:() => ({value:addOffer, host:{providerOfferReadRevision:'offer-2'}})}},
];
for (const save of saveCases) test(`an ${save.kind} save whose reading afterwards was not sent states the write first, then the sentence, and offers reading again, not saving again`, async () => {
  for (const after of [...sentences, canary]) {
    const message = `${WRITE_THEN_READING}${after}`;
    await mounted({...save.answers, [save.command]:() => ({value:{state:'write-observed-source-unconfirmed', message}})}, async (c, calls) => {
      await save.open(c); await press(c, save.save);
      const status = nodes(region(c, save.editor), 'p').find(node => node.getAttribute('role') === 'status').textContent;
      if (after === canary) { assert.match(status, save.fixed, 'anything else after the prefix keeps the fixed outcome'); assert.doesNotMatch(c.textContent, new RegExp(canary)); }
      else {
        assert.equal(status, message, 'the write outcome, then the sentence, unchanged');
        assert.ok(status.startsWith('Write observed; no retry. '), 'the write is stated first and on its own');
      }
      assert.equal(button(c, save.save), undefined, 'no save retry is offered');
      assert.equal(calls.filter(command => command === save.command).length, 1, 'the save was sent once');
      assert.equal(!!props(button(c, 'Read configured local providers')).disabled, false, 'reading again is offered');
    });
  }
});
