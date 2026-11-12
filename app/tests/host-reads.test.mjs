import test from 'node:test';
import assert from 'node:assert/strict';
import {installMiniDom} from './support/mini-dom.mjs';
import {loadSrc} from './support/load-src.mjs';

// The order of the web view's host status reads. Controlled replies only: an
// invented host_status that the test resolves in the order it chooses.
installMiniDom();
const React = (await import('react')).default;
const {createRoot} = await import('react-dom/client');
const {useOrderedHost, shownBeforePress} = loadSrc('hostReads');

function controlledHost() {
  const pending = [];
  const previous = window.__TAURI_INTERNALS__;
  window.__TAURI_INTERNALS__ = {invoke(command) { assert.equal(command, 'host_status'); return new Promise((resolve, reject) => pending.push({resolve, reject})); }};
  return {pending, restore() { window.__TAURI_INTERNALS__ = previous; }};
}
async function mount() {
  const api = {}; const c = document.createElement('div'); const root = createRoot(c);
  function Harness() { Object.assign(api, useOrderedHost()); return React.createElement('p', null, JSON.stringify(api.host)); }
  await React.act(async () => root.render(React.createElement(Harness)));
  return {api, text:() => c.textContent, close:() => React.act(async () => root.unmount())};
}

test('a reply is applied only if its read started after the one whose reply is shown', async () => {
  const host = controlledHost(); const ui = await mount();
  try {
    assert.equal(ui.api.hostReads.started(), 0); assert.equal(ui.api.hostReads.applied, 0); assert.equal(ui.api.host, null);
    const first = ui.api.readHost(window.__TAURI_INTERNALS__.invoke('host_status')), second = ui.api.readHost(window.__TAURI_INTERNALS__.invoke('host_status')), third = ui.api.readHost(window.__TAURI_INTERNALS__.invoke('host_status'));
    assert.equal(ui.api.hostReads.started(), 3, 'a read is numbered when it starts, not when it replies');
    // The second read replies first.
    host.pending[1].resolve({view:'second'});
    await React.act(async () => { assert.equal(ui.api.applyHost(await second), true); });
    assert.equal(ui.text(), '{"view":"second"}'); assert.equal(ui.api.hostReads.applied, 2);
    // The first read's reply arrives late: it is older and is not applied.
    host.pending[0].resolve({view:'first'});
    await React.act(async () => { assert.equal(ui.api.applyHost(await first), false, 'an older read never replaces a newer one'); });
    assert.equal(ui.text(), '{"view":"second"}'); assert.equal(ui.api.hostReads.applied, 2);
    // The same read is not applied twice, and a newer one is.
    await React.act(async () => { assert.equal(ui.api.applyHost(await second), false); });
    host.pending[2].resolve({view:'third'});
    await React.act(async () => { assert.equal(ui.api.applyHost(await third), true); });
    assert.equal(ui.text(), '{"view":"third"}'); assert.equal(ui.api.hostReads.applied, 3);
    // A read that fails is numbered and applies nothing.
    const failed = ui.api.readHost(window.__TAURI_INTERNALS__.invoke('host_status')); host.pending[3].reject(new Error('invented failure'));
    await assert.rejects(failed, /invented failure/);
    assert.equal(ui.api.hostReads.started(), 4); assert.equal(ui.api.hostReads.applied, 3);
  } finally { await ui.close(); host.restore(); }
});

test('a view is from before a press until a read started after the press settled has been applied', () => {
  const reads = applied => ({started:() => 0, applied});
  assert.equal(shownBeforePress(null, reads(5)), false, 'no press has settled');
  assert.equal(shownBeforePress(3, undefined), false, 'without the reads\' order nothing is claimed either way');
  assert.equal(shownBeforePress(3, reads(2)), true, 'the read shown started before the press settled');
  assert.equal(shownBeforePress(3, reads(3)), true, 'the last read started before the settle is still from before it');
  assert.equal(shownBeforePress(3, reads(4)), false, 'a read started after the settle');
});
