// Local model settings (DEL-01-05) in the mounted control, with a controlled
// IPC peer and invented values. The native commands `local_model_settings_read`
// and `local_model_settings_save` are checked by the Rust tests named
// `native_local_settings_*`. No supplier, model server, key or person act.
import test from 'node:test';
import assert from 'node:assert/strict';
import {loadSrc} from './support/load-src.mjs';
import {installMiniDom} from './support/mini-dom.mjs';
import {installIdleNativeWaiting} from './support/idle-native-waiting.mjs';
const document = installMiniDom();
const React = (await import('react')).default;
const {createRoot} = await import('react-dom/client');
const {LocalModelSettings, localSettingsFrom, localEndpointValid, localModelValid} = loadSrc('LocalProviderAccess');

const props = node => node[Object.keys(node).find(k => k.startsWith('__reactProps$'))];
const nodes = (c, tag) => c.querySelectorAll(node => node.localName === tag);
const button = (c, label) => nodes(c, 'button').find(node => node.textContent === label);
const labelled = (c, label) => nodes(c, 'input').find(node => node.parentNode.textContent.startsWith(label));
const offered = {endpoint:'http://127.0.0.1:8000/v1'};
const reading = (over = {}) => ({state:'unset', settings:null, offered, inForce:null, relaunchRequired:false, ...over});
const set = (endpoint, model, over = {}) => reading({state:'set', settings:{endpoint, model}, ...over});

async function mounted(handler, check, changed = () => {}) {
  const c = document.createElement('div'); document.body.appendChild(c); const root = createRoot(c); const calls = [];
  const idle = installIdleNativeWaiting(async (command, args) => { calls.push({command, args:args === undefined ? undefined : structuredClone(args)}); return handler(command, args); });
  const ui = {c, calls,
    press:label => React.act(async () => { const node = button(c, label); assert.ok(node, label); assert.equal(!!props(node).disabled, false, label); await props(node).onClick(); }),
    change:(label, value) => React.act(async () => { const node = labelled(c, label); assert.ok(node, label); props(node).onChange({target:{value}}); }),
    save:() => button(c, 'Save local model settings…')};
  try { await React.act(() => root.render(React.createElement(LocalModelSettings, {disabled:false, changed}))); await check(ui); }
  finally { const text = c.textContent; await React.act(() => root.unmount()); document.body.removeChild(c); idle.restore(text); }
}

test('only a complete reply is a settings reading; anything else shows nothing as set', () => {
  assert.deepEqual(localSettingsFrom(reading()), {state:'unset', settings:null, offered, inForce:null, relaunchRequired:false, outcome:undefined, keyRemoved:false});
  assert.equal(localSettingsFrom(set('http://127.0.0.1:9/v1', 'm')).settings.model, 'm');
  for (const bad of [null, {}, reading({state:'saved'}), reading({state:'set'}), set('http://127.0.0.1:9/v1', 'm', {state:'unset'}), reading({offered:{}}), reading({relaunchRequired:'no'}),
    reading({state:'set', settings:{endpoint:'http://127.0.0.1:9/v1'}}), reading({outcome:'written'})]) assert.equal(localSettingsFrom(bad), null, JSON.stringify(bad));
  // A key removal is claimed only when the host says exactly true.
  assert.equal(localSettingsFrom(set('http://127.0.0.1:9/v1', 'm', {outcome:'saved', keyRemoved:'yes'})).keyRemoved, false);
});

test('the early checks accept only a same-machine address and a plain model name', () => {
  for (const ok of ['http://127.0.0.1:8000/v1', 'http://[::1]:9000/v1', 'https://127.0.0.1/v1', 'http://127.0.0.1:1']) assert.equal(localEndpointValid(ok), true, ok);
  for (const bad of ['', 'http://localhost:8000/v1', 'http://192.168.1.5:8000/v1', 'http://127.0.0.1.example.invalid/v1', 'http://user@127.0.0.1:8000/v1', 'http://127.0.0.1:8000/v1?x=1',
    'http://127.0.0.1:8000/v1#f', 'ftp://127.0.0.1/v1', 'http://127.0.0.1:08000/v1', ' http://127.0.0.1:8000/v1', 'http://127.0.0.1:8000/v1 ']) assert.equal(localEndpointValid(bad), false, bad);
  for (const ok of ['mlx-community/Model-8bit', 'a', 'name:tag@1+x_y.z']) assert.equal(localModelValid(ok), true, ok);
  for (const bad of ['', 'two words', 'quote"d', 'back\\slash', 'line\nbreak', 'x'.repeat(129)]) assert.equal(localModelValid(bad), false, bad);
});

test('nothing is read until the person asks; an unset reading offers the address and names no model', async () => {
  await mounted(async command => { if (command === 'local_model_settings_read') return reading(); throw Error(`unexpected ${command}`); }, async ui => {
    assert.equal(ui.calls.length, 0, 'no read on mount');
    assert.equal(ui.save(), undefined);
    await ui.press('Show local model settings');
    assert.deepEqual(ui.calls.map(call => call.command), ['local_model_settings_read']);
    assert.deepEqual(ui.calls[0].args ?? {}, {}, 'the read takes no argument');
    assert.match(ui.c.textContent, /No local model server is set yet\./);
    assert.equal(props(labelled(ui.c, 'Server address ')).value, 'http://127.0.0.1:8000/v1');
    assert.equal(props(labelled(ui.c, 'Model name on the server ')).value, '', 'no model is named for the person');
    assert.equal(props(ui.save()).disabled, true, 'nothing can be saved without a model name');
    await ui.change('Model name on the server ', 'bad name');
    assert.match(ui.c.textContent, /This name cannot be used/); assert.equal(props(ui.save()).disabled, true);
    await ui.change('Server address ', 'http://192.168.1.5:8000/v1');
    assert.match(ui.c.textContent, /This address cannot be used/);
    assert.equal(ui.calls.length, 1, 'an invalid draft is never sent');
  });
});

test('Save sends exactly the two typed values, and each outcome is said as what it is', async () => {
  const replies = [];
  let notified = 0;
  await mounted(async (command, args) => {
    if (command === 'local_model_settings_read') return set('http://127.0.0.1:8000/v1', 'first-model');
    if (command === 'local_model_settings_save') return replies.shift()(args);
    throw Error(`unexpected ${command}`);
  }, async ui => {
    await ui.press('Show local model settings');
    assert.match(ui.c.textContent, /Saved: server http:\/\/127\.0\.0\.1:8000\/v1 · model first-model\./);
    assert.equal(props(ui.save()).disabled, true, 'no change to save');
    // Cancelled: nothing claimed, the draft is kept.
    await ui.change('Server address ', 'http://[::1]:9000/v1');
    replies.push(() => set('http://127.0.0.1:8000/v1', 'first-model', {outcome:'cancelled', keyRemoved:false}));
    await ui.press('Save local model settings…');
    assert.deepEqual(ui.calls.at(-1), {command:'local_model_settings_save', args:{endpoint:'http://[::1]:9000/v1', model:'first-model'}});
    assert.match(ui.c.textContent, /Not saved: you cancelled\. Nothing was changed\./);
    assert.equal(props(labelled(ui.c, 'Server address ')).value, 'http://[::1]:9000/v1');
    assert.equal(notified, 0);
    // Refused by the host: its fixed sentence is shown, nothing is shown as saved.
    replies.push(() => { throw 'Prepare the local connection first, so that Codex can remove the saved key; the local model settings were not changed.'; });
    await ui.press('Save local model settings…');
    assert.match(ui.c.textContent, /Prepare the local connection first/);
    assert.match(ui.c.textContent, /Saved: server http:\/\/127\.0\.0\.1:8000\/v1 · model first-model\./, 'the earlier saved reading still stands');
    assert.equal(notified, 0);
    // Saved with the key removed, in a session that was using the old settings.
    replies.push(args => set(args.endpoint, args.model, {outcome:'saved', keyRemoved:true, inForce:{endpoint:'http://127.0.0.1:8000/v1', model:'first-model'}, relaunchRequired:true}));
    await ui.press('Save local model settings…');
    assert.match(ui.c.textContent, /Saved\. Codex removed the saved key for the earlier address; enter the key again/);
    assert.match(ui.c.textContent, /Saved: server http:\/\/\[::1\]:9000\/v1 · model first-model\./);
    assert.match(ui.c.textContent, /In use in this session: server http:\/\/127\.0\.0\.1:8000\/v1/);
    assert.match(ui.c.textContent, /Quit and reopen the App to use the saved ones/);
    assert.equal(notified, 1);
    // A reply that is not a settings reading shows nothing new as set.
    await ui.change('Model name on the server ', 'second-model');
    replies.push(() => ({state:'set'}));
    await ui.press('Save local model settings…');
    assert.match(ui.c.textContent, /The reply was not a local model settings reading; nothing is shown as set\./);
    assert.equal(notified, 1);
  }, () => { notified++; });
});

test('settings that cannot be read are shown as unavailable, with no form and nothing shown as set', async () => {
  await mounted(async () => reading({state:'unavailable'}), async ui => {
    await ui.press('Show local model settings');
    assert.match(ui.c.textContent, /could not be read, so nothing is shown as set/);
    assert.equal(ui.save(), undefined); assert.equal(labelled(ui.c, 'Server address '), undefined);
  });
  await mounted(async () => { throw Error('INVENTED_PRIVATE_DIAGNOSTIC'); }, async ui => {
    await ui.press('Show local model settings');
    assert.match(ui.c.textContent, /Local model settings are unavailable; nothing was changed\./);
    assert.doesNotMatch(ui.c.textContent, /INVENTED_PRIVATE_DIAGNOSTIC/);
    assert.equal(ui.save(), undefined);
  });
});
