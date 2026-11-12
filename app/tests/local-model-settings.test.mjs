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
  assert.deepEqual(localSettingsFrom(reading()), {state:'unset', settings:null, offered, inForce:null, relaunchRequired:false, outcome:undefined, keyRemoved:false, keyMismatch:null});
  assert.equal(localSettingsFrom(set('http://127.0.0.1:9/v1', 'm')).settings.model, 'm');
  for (const bad of [null, {}, reading({state:'saved'}), reading({state:'set'}), set('http://127.0.0.1:9/v1', 'm', {state:'unset'}), reading({offered:{}}), reading({relaunchRequired:'no'}),
    reading({state:'set', settings:{endpoint:'http://127.0.0.1:9/v1'}}), reading({outcome:'written'})]) assert.equal(localSettingsFrom(bad), null, JSON.stringify(bad));
  // A saved key entered for another address: only the host's exact shape is that reading.
  const mismatch = over => set('http://127.0.0.1:9200/v1', 'm', {state:'unavailable', reason:'key-address-mismatch', keyAddress:'http://127.0.0.1:9100/v1', ...over});
  assert.deepEqual(localSettingsFrom(mismatch()).keyMismatch, {recorded:'http://127.0.0.1:9100/v1'});
  assert.deepEqual(localSettingsFrom(mismatch({keyAddress:null})).keyMismatch, {recorded:null});
  assert.equal(localSettingsFrom(set('http://127.0.0.1:9/v1', 'm', {reason:null, keyAddress:null})).keyMismatch, null);
  for (const bad of [mismatch({state:'set'}), mismatch({settings:null}), mismatch({keyAddress:undefined}), mismatch({keyAddress:'http://192.168.1.5:8000/v1'}), mismatch({keyAddress:'http://127.0.0.1:9200/v1'}),
    mismatch({reason:'other'}), set('http://127.0.0.1:9/v1', 'm', {keyAddress:'http://127.0.0.1:9100/v1'}), reading({state:'unavailable', settings:{endpoint:'http://127.0.0.1:9/v1', model:'m'}})]) assert.equal(localSettingsFrom(bad), null, JSON.stringify(bad));
  // A key removal is claimed only when the host says exactly true.
  assert.equal(localSettingsFrom(set('http://127.0.0.1:9/v1', 'm', {outcome:'saved', keyRemoved:'yes'})).keyRemoved, false);
});

test('the early checks accept only a same-machine address and a plain model name', () => {
  for (const ok of ['http://127.0.0.1:8000/v1', 'http://[::1]:9000/v1', 'https://127.0.0.1/v1', 'http://127.0.0.1:1', 'http://127.0.0.1:65535/v1']) assert.equal(localEndpointValid(ok), true, ok);
  for (const bad of ['', 'http://localhost:8000/v1', 'http://192.168.1.5:8000/v1', 'http://127.0.0.1.example.invalid/v1', 'http://user@127.0.0.1:8000/v1', 'http://127.0.0.1:8000/v1?x=1',
    'http://127.0.0.1:8000/v1#f', 'ftp://127.0.0.1/v1', 'http://127.0.0.1:08000/v1', 'http://127.0.0.1:65536/v1', 'http://127.0.0.1:99999/v1', ' http://127.0.0.1:8000/v1', 'http://127.0.0.1:8000/v1 ']) assert.equal(localEndpointValid(bad), false, bad);
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
    assert.match(ui.c.textContent, /Whether anything changed is not established here/);
    assert.doesNotMatch(ui.c.textContent, /Saved: server/, 'after a save with no reading, nothing is shown as saved');
    assert.equal(ui.save(), undefined, 'and nothing can be saved again until the settings are read again');
    assert.equal(notified, 1, 'the route and key state beside it are withdrawn');
    await ui.press('Show local model settings');
    await ui.change('Server address ', 'http://[::1]:9000/v1');
    // Saved with the key removed, in a session that was using the old settings.
    replies.push(args => set(args.endpoint, args.model, {outcome:'saved', keyRemoved:true, inForce:{endpoint:'http://127.0.0.1:8000/v1', model:'first-model'}, relaunchRequired:true}));
    await ui.press('Save local model settings…');
    assert.match(ui.c.textContent, /Saved\. Codex removed the saved key for the earlier address; enter the key again/);
    assert.match(ui.c.textContent, /Saved: server http:\/\/\[::1\]:9000\/v1 · model first-model\./);
    assert.match(ui.c.textContent, /In use in this session: server http:\/\/127\.0\.0\.1:8000\/v1/);
    assert.match(ui.c.textContent, /Quit and reopen the App to use the saved ones/);
    assert.equal(notified, 2);
    // A reply that is not a settings reading shows nothing new as set.
    await ui.change('Model name on the server ', 'second-model');
    replies.push(() => ({state:'set'}));
    await ui.press('Save local model settings…');
    assert.match(ui.c.textContent, /The reply was not a local model settings reading; nothing is shown as set\./);
    assert.doesNotMatch(ui.c.textContent, /Saved: server/);
    assert.equal(notified, 3);
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
    assert.match(ui.c.textContent, /Local model settings are unavailable\. Nothing was changed\./);
    assert.doesNotMatch(ui.c.textContent, /INVENTED_PRIVATE_DIAGNOSTIC/);
    assert.equal(ui.save(), undefined);
  });
});

test('a saved key entered for another address: both addresses are shown, and the only offer is setting the address back', async () => {
  const mismatch = keyAddress => set('http://127.0.0.1:9200/v1', 'org/m', {state:'unavailable', reason:'key-address-mismatch', keyAddress});
  let notified = 0;
  await mounted(async (command, args) => {
    if (command === 'local_model_settings_read') return mismatch('http://127.0.0.1:9100/v1');
    if (command === 'local_model_settings_save') return set(args.endpoint, args.model, {outcome:'saved', keyRemoved:false, reason:null, keyAddress:null});
    throw Error(`unexpected ${command}`);
  }, async ui => {
    await ui.press('Show local model settings');
    assert.match(ui.c.textContent, /The saved key was entered for http:\/\/127\.0\.0\.1:9100\/v1, and the address now set is http:\/\/127\.0\.0\.1:9200\/v1\. The App will not use that key with another address\./);
    assert.doesNotMatch(ui.c.textContent, /Saved: server/, 'the address set is not shown as usable');
    assert.equal(ui.save(), undefined, 'no other change is offered in this state');
    assert.equal(labelled(ui.c, 'Server address '), undefined);
    await ui.press('Set the address back to http://127.0.0.1:9100/v1…');
    assert.deepEqual(ui.calls.at(-1), {command:'local_model_settings_save', args:{endpoint:'http://127.0.0.1:9100/v1', model:'org/m'}}, 'the recorded address and the model name already set, nothing typed');
    assert.match(ui.c.textContent, /Saved: server http:\/\/127\.0\.0\.1:9100\/v1 · model org\/m\./);
    assert.doesNotMatch(ui.c.textContent, /Codex removed the saved key/, 'no key removal is claimed');
    assert.equal(notified, 1);
  }, () => { notified++; });
  await mounted(async () => mismatch(null), async ui => {
    await ui.press('Show local model settings');
    assert.match(ui.c.textContent, /the App has no record of the server address it was entered for, so it will not use that key at any address\. This cannot be put right from the App\./);
    assert.equal(nodes(ui.c, 'button').filter(node => node.textContent.startsWith('Set the address back')).length, 0);
    assert.equal(ui.save(), undefined);
  });
});
