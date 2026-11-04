// Ordinary sends without a native acknowledgement (native J2 baseline, main
// 9248a36e: an unknown outcome rendered like a refusal and Send stayed
// enabled, so one press could duplicate a turn). Mounted ConversationPanel with
// a controlled send; invented conversations. No supplier, model or person act.
import test from 'node:test';
import assert from 'node:assert/strict';
import {installMiniDom} from './support/mini-dom.mjs';
import {loadSrc} from './support/load-src.mjs';
const document = installMiniDom();
const React = (await import('react')).default;
const {createRoot} = await import('react-dom/client');
const {ConversationPanel} = loadSrc('App');
const g = {appSession:'s', home:'account', spawnCounter:1};
const g2 = {...g, spawnCounter:2};
const thread = (threadId, generation = g) => ({generation, threadId, model:'invented-model', appRole:{standing:'app-observed', role:null}, roleRelation:{kind:'start'}, futureGuidanceNotices:[]});
const hostFor = (generation = g) => ({state:'ready', generation, roleLimits:{account:{roles:[]}}, threads:[thread('thread-a', generation), thread('thread-b', generation)]});
const props = node => node[Object.keys(node).find(k => k.startsWith('__reactProps$'))];
const nodes = (c, tag) => c.querySelectorAll(node => node.localName === tag);
const button = (c, label) => nodes(c, 'button').find(node => node.textContent === label);
const noop = async () => {};

async function mounted(reply, check) {
  const c = document.createElement('div'); document.body.appendChild(c); const root = createRoot(c); const sends = [];
  let current = {host:hostFor(), threadKey:JSON.stringify([g, 'thread-a'])};
  const render = async next => { current = {...current, ...next}; await React.act(() => root.render(React.createElement(ConversationPanel, {...current, setThreadKey:() => {}, answer:noop, runAct:noop,
    send:async (...args) => { sends.push(args); return reply(args, sends.length); }, steer:noop, submitAttachments:noop, interrupt:noop, checkPlanMode:noop, codexBusy:false}))); };
  const settle = () => React.act(async () => { for (let i = 0; i < 10; i++) await Promise.resolve(); });
  const field = () => nodes(c, 'textarea').find(node => node.getAttribute('id') === 'ordinary-composer-text');
  const ui = {c, sends, render, settle, field,
    type:async value => React.act(async () => { props(field()).onChange({target:{value}}); }),
    send:() => button(c, 'Send text'),
    readiness:() => c.querySelectorAll(node => node.getAttribute('id') === 'ordinary-send-readiness')[0].textContent,
    notices:() => c.querySelectorAll(node => node.getAttribute('aria-label') === 'Unconfirmed messages')[0]};
  try { await render({}); await check(ui); }
  finally { await React.act(() => root.unmount()); document.body.removeChild(c); }
}

test('an unacknowledged ordinary send keeps its text, holds that conversation for every send control and is lifted only by an explicit acknowledgement', async () => {
  await mounted((args, n) => { if (n === 1) throw 'invented: no response from Codex'; return {id:1, result:{turn:{id:'t'}}}; }, async ui => {
    await ui.type('Please summarise the report');
    const retained = props(ui.send()).onClick;
    await React.act(async () => { retained(); }); await ui.settle();
    assert.equal(ui.sends.length, 1);
    assert.equal(props(ui.field()).value, 'Please summarise the report', 'the text is not cleared without a native acknowledgement');
    assert.match(ui.notices().textContent, /Your message to this conversation may have been sent\..*isn't resent and its text was not cleared.*held until you've read it.*Please summarise the report.*Reported: invented: no response from Codex/);
    assert.equal(props(ui.send()).disabled, true, 'Send is held');
    assert.match(ui.readiness(), /An earlier message to this conversation wasn't confirmed and may have been sent/);
    await React.act(async () => { retained(); }); await ui.settle();
    assert.equal(ui.sends.length, 1, 'a retained Send control issues nothing');
    await ui.type('A different message');
    assert.equal(props(ui.send()).disabled, true, 'an edit does not lift the hold');
    // Another conversation is not held, and does not inherit the record's authority.
    await ui.render({threadKey:JSON.stringify([g, 'thread-b'])});
    assert.equal(props(ui.send()).disabled, false);
    assert.match(ui.notices().textContent, /Your message to Conversation 1 · invented-model may have been sent/, 'the record stays listed by where it went');
    // A Codex restart keeps the hold for the same conversation ID, described plainly.
    await ui.render({host:hostFor(g2), threadKey:JSON.stringify([g2, 'thread-a'])});
    assert.equal(props(ui.send()).disabled, true, 'held for the same conversation ID after a restart');
    assert.match(ui.notices().textContent, /Your message to conversation thread-a in a Codex session that isn't loaded now may have been sent\..*The conversation shown now has the same ID, so sending to it is held too/);
    const before = ui.sends.length;
    await React.act(async () => { props(button(ui.notices(), 'I\'ve read that conversation — allow sending again')).onClick(); });
    assert.equal(ui.sends.length, before, 'acknowledging sends nothing');
    assert.match(ui.notices().textContent, /You've said you read that conversation.*Reported: invented: no response from Codex/, 'the original record stays');
    assert.equal(props(ui.send()).disabled, false);
    await React.act(async () => { props(ui.send()).onClick(); }); await ui.settle();
    assert.equal(ui.sends.length, 2, 'the person\'s separate new intent sends once');
    assert.equal(props(ui.field()).value, '', 'an acknowledged send clears its own text');
  });
});

test('a send that resolves without a result is not an acknowledgement: nothing is cleared and the conversation is held', async () => {
  await mounted(() => null, async ui => {
    await ui.type('Draft that may have gone');
    await React.act(async () => { props(ui.send()).onClick(); }); await ui.settle();
    assert.equal(props(ui.field()).value, 'Draft that may have gone');
    assert.match(ui.notices().textContent, /may have been sent.*Reported: The host did not report this send's outcome; it may or may not have been sent\./);
    assert.equal(props(ui.send()).disabled, true);
    assert.doesNotMatch(ui.c.textContent, /Native turn\/start response received/, 'no acknowledgement is claimed');
  });
});
